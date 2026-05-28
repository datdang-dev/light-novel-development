"""
Qwen2VLChatHandler — custom chat handler for Qwen2-VL / ToriiGate models.

Fixes the root cause: Llava15ChatHandler passes image-pad token IDs through
create_completion, which re-evaluates them as regular text embeddings,
OVERWRITING the correct image embeddings that mtmd_helper_eval_chunk_single
placed in the KV cache.

Solution: after mtmd chunk evaluation, generate directly by sampling from the
current logits (which already have correct image context). No re-evaluation
of prompt tokens through create_completion.
"""

import copy
import ctypes
import sys
import time
import uuid
from typing import Any, Dict, List, Optional

from jinja2.sandbox import ImmutableSandboxedEnvironment

from llama_cpp import llama_cpp, llama_types
from llama_cpp.llama_chat_format import (
    Llava15ChatHandler,
    _convert_completion_to_chat,
    _get_system_message,
    _grammar_for_response_format,
)


class Qwen2VLChatHandler(Llava15ChatHandler):
    """Custom chat handler for Qwen2-VL vision-language models.

    Key differences from Llava15ChatHandler:
    - Renders the GGUF Jinja2 template with <__media__> markers instead of
      <|vision_start|><|image_pad|><|vision_end|> so mtmd_tokenize can
      correctly place image embeddings.
    - After mtmd chunk evaluation, generates tokens by DIRECT sampling from
      the current logits (not by passing tokens through create_completion,
      which would destroy image embeddings).
    """

    DEFAULT_SYSTEM_MESSAGE = ""  # Let the GGUF template handle system msg

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gguf_template_str: Optional[str] = None

    # ── GGUF template helpers ──

    def set_gguf_template(self, template_str: str):
        """Override the GGUF chat template.

        The template should emit <__media__> where images should be placed,
        instead of <|vision_start|><|image_pad|><|vision_end|>.
        """
        self._gguf_template_str = template_str

    @staticmethod
    def adapt_gguf_template(template_str: str) -> str:
        """Replace Qwen2-VL vision tokens with the <__media__> marker.

        The GGUF template for Qwen2-VL emits:
            <|vision_start|><|image_pad|><|vision_end|>
        for each image. mtmd_tokenize expects <__media__> to know where
        to inject image embeddings.
        """
        media_marker = "<__media__>"
        adapted = template_str.replace(
            "<|vision_start|><|image_pad|><|vision_end|>",
            media_marker,
        )
        adapted = adapted.replace(
            "<|vision_start|><|video_pad|><|vision_end|>",
            media_marker,
        )
        # Strip add_vision_id prefix
        adapted = adapted.replace(
            "{% if add_vision_id %}Picture {{ image_count.value }}: {% endif %}",
            "",
        )
        adapted = adapted.replace(
            "{% if add_vision_id %}Video {{ video_count.value }}: {% endif %}",
            "",
        )
        return adapted

    def _render_messages(
        self,
        llama: Any,
        messages: List[llama_types.ChatCompletionRequestMessage],
        add_generation_prompt: bool = True,
    ) -> str:
        """Render messages through the GGUF Jinja2 template.

        Reads the chat template from llama.metadata (if not overridden).
        """
        if self._gguf_template_str:
            template_str = self._gguf_template_str
        else:
            # Read and adapt template from model metadata
            try:
                raw_template = llama.metadata.get("tokenizer.chat_template", self.CHAT_FORMAT)
            except Exception:
                raw_template = self.CHAT_FORMAT
            adapted = self.adapt_gguf_template(raw_template)
            self._gguf_template_str = adapted
            template_str = adapted

        tpl = ImmutableSandboxedEnvironment(
            trim_blocks=True,
            lstrip_blocks=True,
        ).from_string(template_str)

        return tpl.render(
            messages=messages,
            add_generation_prompt=add_generation_prompt,
            eos_token="<|im_end|>",
            bos_token="",
            add_vision_id=False,
        )

    # ── Direct token generation ──

    @staticmethod
    def _truncate_at_stop(text: str, stop: List[str]) -> str:
        """Truncate text at the first occurrence of any stop string."""
        for s in stop:
            idx = text.find(s)
            if idx != -1:
                return text[:idx]
        return text

    def _generate_direct(
        self,
        llama: Any,
        max_tokens: int,
        temperature: float,
        top_p: float,
        top_k: int,
        min_p: float,
        typical_p: float,
        repeat_penalty: float,
        frequency_penalty: float,
        presence_penalty: float,
        tfs_z: float,
        mirostat_mode: int,
        mirostat_tau: float,
        mirostat_eta: float,
        stop: List[str],
        seed: Optional[int],
    ) -> str:
        """Generate tokens directly by sampling, without re-evaluating prompt.

        Uses llama.sample() to draw tokens and llama.eval() to append them
        to the context. This preserves the image embeddings that mtmd placed
        in the KV cache.
        """
        assert llama.n_tokens > 0, "No tokens in context to sample from"

        eos_token_id = llama.token_eos()
        stop_token_ids = set()
        if eos_token_id != -1:
            stop_token_ids.add(eos_token_id)

        # Explicit Qwen2-VL / Qwen special stop tokens (like <|im_end|>)
        for qwen_stop_id in [151645, 151643]:
            stop_token_ids.add(qwen_stop_id)

        # Map special stop strings to their token IDs
        for s in stop:
            if s.startswith("<|") and s.endswith("|>"):
                try:
                    t_ids = llama.tokenize(s.encode("utf-8"), add_bos=False, special=True)
                    for tid in t_ids:
                        stop_token_ids.add(tid)
                except Exception:
                    pass

        generated_ids: List[int] = []

        for _ in range(max_tokens):
            token_id = llama.sample(
                top_k=top_k,
                top_p=top_p,
                min_p=min_p,
                typical_p=typical_p,
                temp=temperature,
                repeat_penalty=repeat_penalty,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                tfs_z=tfs_z,
                mirostat_mode=mirostat_mode,
                mirostat_tau=mirostat_tau,
                mirostat_eta=mirostat_eta,
            )

            # Check for EOS token
            if token_id in stop_token_ids:
                break

            generated_ids.append(token_id)

            # Stream tokens in real-time to stdout and active log files (for tail -f)
            token_text = llama.detokenize([token_id]).decode("utf-8", errors="replace")
            
            stream_tokens = getattr(self, "stream_tokens", True)
            if stream_tokens:
                sys.stdout.write(token_text)
                sys.stdout.flush()
                
                import logging
                for logger_name in ["", "caption-engine-orchestrator", "toriigate-api-server", "in_process_qwen2vl_adapter"]:
                    for handler in logging.getLogger(logger_name).handlers:
                        if isinstance(handler, logging.FileHandler):
                            try:
                                handler.stream.write(token_text)
                                handler.stream.flush()
                            except Exception:
                                pass

            # Check stop strings
            text_so_far = llama.detokenize(generated_ids).decode(
                "utf-8", errors="replace"
            )
            if any(s in text_so_far for s in stop):
                return self._truncate_at_stop(text_so_far, stop)

            # Append to context (preserves the KV cache from mtmd eval)
            llama.eval([token_id])

        # Decode all generated tokens
        result = llama.detokenize(generated_ids).decode("utf-8", errors="replace")
        return self._truncate_at_stop(result, stop)

    @staticmethod
    def _count_tokens(llama: Any, text: str) -> int:
        """Approximate token count using the model's tokenizer."""
        try:
            tokens = llama.tokenize(text.encode("utf-8"), add_bos=False, special=False)
            return len(tokens)
        except Exception:
            return len(text.split())

    # ── Main __call__ ──

    def __call__(
        self,
        *,
        llama: Any,
        messages: List[llama_types.ChatCompletionRequestMessage],
        **kwargs,
    ) -> Dict[str, Any]:
        """Process multimodal messages and generate a response.

        Flow:
        1. Render messages through (adapted) GGUF template -> text with <__media__>
        2. Initialize mtmd context
        3. Load images, create bitmaps
        4. mtmd_tokenize -> chunks (text chunks + image chunks)
        5. mtmd_helper_eval_chunk_single for each chunk -> populates KV cache
        6. Generate tokens directly by sampling (no create_completion re-eval)
        7. Return chat completion dict
        """
        # ── Extract parameters ──
        temperature = kwargs.pop("temperature", 0.7)
        top_p = kwargs.pop("top_p", 0.95)
        top_k = kwargs.pop("top_k", 40)
        min_p = kwargs.pop("min_p", 0.05)
        typical_p = kwargs.pop("typical_p", 1.0)
        max_tokens = kwargs.pop("max_tokens", 256)
        stop: List[str] = list(kwargs.pop("stop", [])) or []
        seed = kwargs.pop("seed", None)
        presence_penalty = kwargs.pop("presence_penalty", 0.0)
        frequency_penalty = kwargs.pop("frequency_penalty", 0.0)
        repeat_penalty = kwargs.pop("repeat_penalty", 1.1)
        tfs_z = kwargs.pop("tfs_z", 1.0)
        mirostat_mode = kwargs.pop("mirostat_mode", 0)
        mirostat_tau = kwargs.pop("mirostat_tau", 5.0)
        mirostat_eta = kwargs.pop("mirostat_eta", 0.1)
        logits_processor = kwargs.pop("logits_processor", None)
        grammar = kwargs.pop("grammar", None)
        logit_bias = kwargs.pop("logit_bias", None)
        stream = kwargs.pop("stream", False)
        response_format = kwargs.pop("response_format", None)
        functions = kwargs.pop("functions", None)
        function_call = kwargs.pop("function_call", None)
        tools = kwargs.pop("tools", None)
        tool_choice = kwargs.pop("tool_choice", None)

        if stream:
            # TODO: streaming support for Qwen2-VL
            raise NotImplementedError(
                "Streaming not yet supported for Qwen2VLChatHandler"
            )

        # ── Handle system message ──
        messages = copy.deepcopy(messages)
        system_prompt = _get_system_message(messages)
        if system_prompt == "" and self.DEFAULT_SYSTEM_MESSAGE:
            messages = [
                llama_types.ChatCompletionRequestSystemMessage(
                    role="system", content=self.DEFAULT_SYSTEM_MESSAGE,
                )
            ] + messages

        # ── Get image URLs ──
        image_urls = self.get_image_urls(messages)

        # ── Render messages through GGUF template ──
        text = self._render_messages(llama, messages)

        if self.verbose:
            print("=== Rendered text ===", file=sys.stderr)
            print(text, file=sys.stderr)

        # ── Ensure media markers are present ──
        media_marker = self._mtmd_cpp.mtmd_default_marker().decode("utf-8")
        if image_urls and media_marker not in text:
            for url in image_urls:
                text = text.replace(url, media_marker)

        if self.verbose:
            print("=== Text with media markers ===", file=sys.stderr)
            print(text, file=sys.stderr)

        # ── Initialize mtmd ──
        self._init_mtmd_context(llama)
        assert self.mtmd_ctx is not None

        # ── Create bitmaps from images ──
        bitmaps = []
        cleanup_handles = []
        try:
            for image_url in image_urls:
                image_bytes = self.load_image(image_url)
                bitmap = self._create_bitmap_from_bytes(image_bytes)
                bitmaps.append(bitmap)
                cleanup_handles.append(bitmap)

            # ── Tokenize via mtmd ──
            input_text = self._mtmd_cpp.mtmd_input_text()
            input_text.text = text.encode("utf-8")
            input_text.add_special = True
            input_text.parse_special = True

            chunks = self._mtmd_cpp.mtmd_input_chunks_init()
            if chunks is None:
                raise ValueError("Failed to create input chunks")

            try:
                bitmap_array = (
                    self._mtmd_cpp.mtmd_bitmap_p_ctypes * len(bitmaps)
                )(*bitmaps)
                result = self._mtmd_cpp.mtmd_tokenize(
                    self.mtmd_ctx,
                    chunks,
                    ctypes.byref(input_text),
                    bitmap_array,
                    len(bitmaps),
                )
                if result != 0:
                    raise ValueError(
                        f"mtmd_tokenize failed: error code {result}"
                    )

                # ── Reset llama context (clear any prior state) ──
                llama.reset()
                llama._ctx.kv_cache_clear()

                # ── Evaluate chunks into KV cache via mtmd ──
                n_chunks = self._mtmd_cpp.mtmd_input_chunks_size(chunks)

                for i in range(n_chunks):
                    chunk = self._mtmd_cpp.mtmd_input_chunks_get(chunks, i)
                    if chunk is None:
                        continue

                    chunk_type = self._mtmd_cpp.mtmd_input_chunk_get_type(chunk)

                    if chunk_type == self._mtmd_cpp.MTMD_INPUT_CHUNK_TYPE_TEXT:
                        n_tokens_out = ctypes.c_size_t()
                        tokens_ptr = (
                            self._mtmd_cpp.mtmd_input_chunk_get_tokens_text(
                                chunk, ctypes.byref(n_tokens_out)
                            )
                        )
                        if tokens_ptr and n_tokens_out.value > 0:
                            tokens = [
                                tokens_ptr[j] for j in range(n_tokens_out.value)
                            ]
                            if llama.n_tokens + len(tokens) > llama.n_ctx():
                                raise ValueError(
                                    f"Prompt exceeds n_ctx: "
                                    f"{llama.n_tokens + len(tokens)} > "
                                    f"{llama.n_ctx()}"
                                )
                            llama.eval(tokens)

                    elif chunk_type in (
                        self._mtmd_cpp.MTMD_INPUT_CHUNK_TYPE_IMAGE,
                        self._mtmd_cpp.MTMD_INPUT_CHUNK_TYPE_AUDIO,
                    ):
                        chunk_n_tokens = (
                            self._mtmd_cpp.mtmd_input_chunk_get_n_tokens(chunk)
                        )
                        if llama.n_tokens + chunk_n_tokens > llama.n_ctx():
                            raise ValueError(
                                f"Prompt exceeds n_ctx: "
                                f"{llama.n_tokens + chunk_n_tokens} > "
                                f"{llama.n_ctx()}"
                            )

                        new_n_past = llama_cpp.llama_pos(0)
                        result = (
                            self._mtmd_cpp.mtmd_helper_eval_chunk_single(
                                self.mtmd_ctx,
                                llama._ctx.ctx,
                                chunk,
                                llama_cpp.llama_pos(llama.n_tokens),
                                llama_cpp.llama_seq_id(0),
                                llama.n_batch,
                                False,
                                ctypes.byref(new_n_past),
                            )
                        )
                        if result != 0:
                            raise ValueError(
                                f"Failed to eval chunk: error code {result}"
                            )
                        llama.n_tokens = new_n_past.value

                # ── KV cache now has correct image + text embeddings ──

                # Default stop tokens
                if not stop:
                    stop = ["<|im_end|>", "<|end|>"]
                if llama.token_eos() != -1:
                    eos_str = llama.detokenize(
                        [llama.token_eos()]
                    ).decode("utf-8", errors="replace")
                    if eos_str and eos_str not in stop:
                        stop.append(eos_str)

                # Response format grammar
                if (
                    response_format is not None
                    and response_format["type"] == "json_object"
                ):
                    grammar = _grammar_for_response_format(response_format)

                # ── Generate by direct sampling ──
                content = self._generate_direct(
                    llama=llama,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    min_p=min_p,
                    typical_p=typical_p,
                    repeat_penalty=repeat_penalty,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    tfs_z=tfs_z,
                    mirostat_mode=mirostat_mode,
                    mirostat_tau=mirostat_tau,
                    mirostat_eta=mirostat_eta,
                    stop=stop,
                    seed=seed,
                )

                # ── Build response ──
                completion_id = f"cmpl-{str(uuid.uuid4())}"
                created = int(time.time())

                response = llama_types.CreateCompletionResponse(
                    id=completion_id,
                    created=created,
                    model=(getattr(llama, "model_path", None) or (llama.metadata.get("general.name") if hasattr(llama, "metadata") else None) or "qwen2-vl"),
                    choices=[
                        llama_types.CompletionChoice(
                            index=0,
                            text=content,
                            logprobs=None,
                            finish_reason="stop",
                        )
                    ],
                    usage=llama_types.CompletionUsage(
                        prompt_tokens=llama.n_tokens,
                        completion_tokens=(
                            n_completion := self._count_tokens(llama, content)
                        ),
                        total_tokens=llama.n_tokens + n_completion,
                    )
                    if hasattr(llama, 'n_tokens')
                    else None,
                )

                # Convert to chat format
                return _convert_completion_to_chat(response, stream=False)

            finally:
                self._mtmd_cpp.mtmd_input_chunks_free(chunks)

        finally:
            for bitmap in cleanup_handles:
                self._mtmd_cpp.mtmd_bitmap_free(bitmap)
