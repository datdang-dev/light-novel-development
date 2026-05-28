import base64
import logging
import sys
from io import BytesIO
from PIL import Image
import asyncio

from studio.core.caption_engine.interfaces.mcp_client import MCPClient

log = logging.getLogger("in_process_qwen2vl_adapter")


class InProcessQwen2VLAdapter(MCPClient):
    """In-process model runner executing Qwen2-VL directly inside the calling process."""

    def __init__(
        self,
        model_path: str,
        mmproj_path: str,
        ngl: int = -1,
        n_ctx: int = 16384,
        verbose: bool = False,
    ):
        self.model_path = model_path
        self.mmproj_path = mmproj_path
        self.ngl = ngl
        self.n_ctx = n_ctx
        self.verbose = verbose
        self._llm = None
        self._handler = None

    def _ensure_model(self) -> None:
        """Lazily initialize the llama_cpp Llama engine in-process."""
        if self._llm is not None:
            return

        log.info(
            "Loading Qwen2-VL model in-process (model=%s, mmproj=%s, ngl=%d, ctx=%d)...",
            self.model_path,
            self.mmproj_path,
            self.ngl,
            self.n_ctx,
        )
        from llama_cpp import Llama
        from studio.core.caption_engine.server.chat_handler_qwen2vl import Qwen2VLChatHandler

        self._handler = Qwen2VLChatHandler(
            clip_model_path=self.mmproj_path,
            verbose=self.verbose,
        )

        self._llm = Llama(
            model_path=self.model_path,
            chat_handler=self._handler,
            n_gpu_layers=self.ngl,
            n_ctx=self.n_ctx,
            verbose=self.verbose,
        )
        log.info("In-process Qwen2-VL model loaded successfully ✓")

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 JPEG representation."""
        img = Image.open(image_path)
        buf = BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=90)
        return base64.b64encode(buf.getvalue()).decode()

    async def _call_model(
        self,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
        stream_tokens: bool = True,
    ) -> str:
        """Execute chat completion directly against the in-process llama.cpp engine."""
        self._ensure_model()
        assert self._llm is not None

        # Dynamically inject stream_tokens option directly into the chat handler instance
        if self._handler is not None:
            self._handler.stream_tokens = stream_tokens

        # Resolve any file:// URLs to base64
        for m in messages:
            if isinstance(m.get("content"), list):
                for part in m["content"]:
                    if part.get("type") == "image_url":
                        url = part["image_url"]["url"]
                        if url.startswith("file://"):
                            fp = url[7:]
                            log.info("Converting file:// -> base64 inside in-process adapter: %s", fp)
                            buf = BytesIO()
                            img = Image.open(fp)
                            img.convert("RGB").save(buf, format="JPEG", quality=85)
                            b64 = base64.b64encode(buf.getvalue()).decode()
                            part["image_url"]["url"] = f"data:image/jpeg;base64,{b64}"

        log.info(
            "Executing in-process inference (max_tokens=%d, temperature=%.2f, stream_tokens=%s)...",
            max_tokens,
            temperature,
            stream_tokens,
        )

        # Run synchronous llama.cpp inference in a separate thread pool.
        result = await asyncio.to_thread(
            self._llm.create_chat_completion,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.9,
            top_k=40,
            min_p=0.05,
            repeat_penalty=1.1,
            stream=False,
        )

        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        log.info("Inference complete. Output length: %d chars", len(content))
        return content

    async def analyze_forensic(
        self,
        image_path: str,
        compiled_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.3,
        stream_tokens: bool = True,
    ) -> str:
        image_b64 = self._encode_image(image_path)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    {"type": "text", "text": compiled_prompt},
                ],
            },
        ]
        return await self._call_model(messages, max_tokens, temperature, stream_tokens=stream_tokens)

    async def generate_prelude(
        self,
        image_path: str,
        compiled_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.5,
        stream_tokens: bool = True,
    ) -> str:
        image_b64 = self._encode_image(image_path)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    {"type": "text", "text": compiled_prompt},
                ],
            },
        ]
        return await self._call_model(messages, max_tokens, temperature, stream_tokens=stream_tokens)

    async def generate_caption(
        self,
        image_path: str,
        compiled_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.5,
        stream_tokens: bool = True,
    ) -> str:
        image_b64 = self._encode_image(image_path)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    {"type": "text", "text": compiled_prompt},
                ],
            },
        ]
        return await self._call_model(messages, max_tokens, temperature, stream_tokens=stream_tokens)
