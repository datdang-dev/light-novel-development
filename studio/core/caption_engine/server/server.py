#!/usr/bin/env python3
"""
ToriiGate Production API Server — High-Performance Vision & Captioning API.

Exposes an OpenAI-compatible /v1/chat/completions endpoint (with streaming support)
and a direct task-based /v1/caption endpoint mapped directly to our CaptionEngine.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, AsyncGenerator

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# ── ANSI Terminal Color Constants ────────────────────────────────────────────
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_MAGENTA = "\033[95m"
C_CYAN = "\033[96m"

# ── Paths & Setup ────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent


def get_workspace_root() -> Path:
    """Find the workspace root by looking for studio/ or .git/ or module.yaml starting from ROOT."""
    curr = ROOT
    for _ in range(5):
        if (curr / "studio").exists() or (curr / "module.yaml").exists() or (curr / ".git").exists():
            return curr
        curr = curr.parent
    return ROOT.parent.parent.parent  # default fallback


# Append workspace root to sys.path to resolve clean engine imports
sys.path.insert(0, str(get_workspace_root()))

from studio.core.caption_engine import CaptionEngine
from studio.core.caption_engine.adapters.in_process_qwen2vl_adapter import InProcessQwen2VLAdapter

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("toriigate-api-server")

# Configure a beautiful custom console logging layout
ws = get_workspace_root()
log_dir = ws / "_lnd-output"
log_dir.mkdir(parents=True, exist_ok=True)
server_log_file = log_dir / "caption_engine.log"

file_handler = logging.FileHandler(server_log_file, encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)
log.addHandler(file_handler)

# ── Configuration ────────────────────────────────────────────────────────────
MODEL_PATH = os.getenv(
    "TORIIGATE_MODEL",
    str(ROOT.parent / "models" / "ToriiGate-0.5_Q4_K_L.gguf"),
)
MMPROJ_PATH = os.getenv(
    "TORIIGATE_MMPROJ",
    str(ROOT.parent / "models" / "mmproj_Q8_0.gguf"),
)
NGL = int(os.getenv("TORIIGATE_NGL", "99"))
NCTX = int(os.getenv("TORIIGATE_NCTX", "16384"))

LND_OUTPUT = Path(
    os.getenv(
        "LND_OUTPUT_DIR",
        str(get_workspace_root() / "_lnd-output" / "_captions"),
    )
)

# ── FastAPI & Initialization ─────────────────────────────────────────────────
app = FastAPI(
    title="ToriiGate Vision & Captioning API Server",
    description="Production REST API for Qwen2-VL R18 Visual Captioning",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazily initialized CaptionEngine & Model Runner
_engine: CaptionEngine | None = None
_adapter: InProcessQwen2VLAdapter | None = None


def get_engine_and_adapter() -> tuple[CaptionEngine, InProcessQwen2VLAdapter]:
    """Return the instantiated unified CaptionEngine and internal model runner."""
    global _engine, _adapter
    if _engine is None or _adapter is None:
        log.info("Initializing In-Process Qwen2-VL Engine backend...")
        _adapter = InProcessQwen2VLAdapter(
            model_path=MODEL_PATH,
            mmproj_path=MMPROJ_PATH,
            ngl=NGL,
            n_ctx=NCTX,
            verbose=False,
        )
        _engine = CaptionEngine(
            workspace_root=str(get_workspace_root()),
            output_dir=str(LND_OUTPUT),
            mcp_client=_adapter,
        )
        log.info("Production backend loaded successfully ✓")
    return _engine, _adapter


# ── Middleware for Beautiful Request Tracing ───────────────────────────────

@app.middleware("http")
async def trace_requests(request: Request, call_next):
    """Trace and benchmark every HTTP request with a beautiful visual layout."""
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    
    # Exclude basic metrics endpoints to prevent noise
    if request.url.path not in ["/health", "/metrics", "/favicon.ico"]:
        log.info(
            f"{C_BLUE}HTTP {request.method} {request.url.path}{C_RESET} finished "
            f"with status {C_GREEN if response.status_code == 200 else C_RED}{response.status_code}{C_RESET} in {C_BOLD}{duration:.4f}s{C_RESET}"
        )
    return response


# ── API Schemas ──────────────────────────────────────────────────────────────


class CaptionRequest(BaseModel):
    image_path: str = Field(..., description="Absolute path to the target image file")
    caption_type: str = Field("direct_caption", description="Prompt style (e.g., long_thoughts_v2, json, md_comic)")
    mood_seed: str = Field("AUTO", description="Mood settings")
    user_context: str = Field("", description="Optional prompt context insertion")
    temperature: float = Field(0.5, description="Generation temperature")
    max_tokens: int = Field(4096, description="Max response tokens")


class ChatMessagePart(BaseModel):
    type: str
    text: str | None = None
    image_url: dict[str, Any] | None = None


class ChatMessage(BaseModel):
    role: str
    content: str | list[ChatMessagePart]


class ChatCompletionRequest(BaseModel):
    messages: list[ChatMessage]
    max_tokens: int = 4096
    temperature: float = 0.5
    stream: bool = False


# ── HTTP Endpoints ───────────────────────────────────────────────────────────


@app.get("/health")
async def health_check():
    """Verify that the model engine is successfully initialized and loaded."""
    try:
        _, adapter = get_engine_and_adapter()
        adapter._ensure_model()
        return {
            "status": "healthy",
            "model_path": MODEL_PATH,
            "gpu_layers": NGL,
            "context_window": NCTX,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine load error: {str(e)}")


@app.post("/v1/caption")
async def generate_caption(request: CaptionRequest):
    """Run a high-level captioning task directly using the specified template and image path."""
    p = Path(request.image_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Image not found at: {request.image_path}")

    # Build gorgeous request block (colored for terminal stdout)
    req_border_colored = (
        "\n"
        f"{C_CYAN}┌────────────────────────────────────────────────────────────┐{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}             {C_BOLD}{C_GREEN}API: TASK-BASED CAPTIONING REQUEST{C_RESET}             {C_CYAN}│{C_RESET}\n"
        f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Target Image{C_RESET}    : {C_BOLD}{p.name}{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Template Type{C_RESET}   : {C_YELLOW}{request.caption_type}{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Mood Seed{C_RESET}       : {C_BLUE}{request.mood_seed}{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Temperature{C_RESET}     : {request.temperature}\n"
        f"{C_CYAN}└────────────────────────────────────────────────────────────┘{C_RESET}\n"
    )
    
    req_border_uncolored = (
        "\n"
        "┌────────────────────────────────────────────────────────────┐\n"
        "│             API: TASK-BASED CAPTIONING REQUEST             │\n"
        "├────────────────────────────────────────────────────────────┤\n"
        f"│  • Target Image    : {p.name}\n"
        f"│  • Template Type   : {request.caption_type}\n"
        f"│  • Mood Seed       : {request.mood_seed}\n"
        f"│  • Temperature     : {request.temperature}\n"
        "└────────────────────────────────────────────────────────────┘\n"
    )
    logger.info(req_border_uncolored)
    sys.stdout.write(req_border_colored)
    sys.stdout.flush()

    try:
        engine, _ = get_engine_and_adapter()
        result = await engine.run(
            image_path=request.image_path,
            mood_seed=request.mood_seed,
            user_context=request.user_context,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            caption_type=request.caption_type,
        )
        return result
    except Exception as e:
        log.exception("Caption Engine failed task generation")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """OpenAI-compatible Chat Completion endpoint for Qwen2-VL vision model inference."""
    try:
        engine, adapter = get_engine_and_adapter()
        adapter._ensure_model()
        assert adapter._llm is not None

        # Build gorgeous completions request block
        req_border_colored = (
            "\n"
            f"{C_CYAN}┌────────────────────────────────────────────────────────────┐{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}           {C_BOLD}{C_GREEN}API: OPENAI-COMPATIBLE CHAT COMPLETION{C_RESET}           {C_CYAN}│{C_RESET}\n"
            f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Messages Count{C_RESET}  : {C_BOLD}{len(request.messages)}{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Max Gen Tokens{C_RESET}  : {request.max_tokens}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Temperature{C_RESET}     : {request.temperature}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Stream Mode{C_RESET}     : {C_YELLOW}{request.stream}{C_RESET}\n"
            f"{C_CYAN}└────────────────────────────────────────────────────────────┘{C_RESET}\n"
        )
        
        req_border_uncolored = (
            "\n"
            "┌────────────────────────────────────────────────────────────┐\n"
            "│           API: OPENAI-COMPATIBLE CHAT COMPLETION           │\n"
            "├────────────────────────────────────────────────────────────┤\n"
            f"│  • Messages Count  : {len(request.messages)}\n"
            f"│  • Max Gen Tokens  : {request.max_tokens}\n"
            f"│  • Temperature     : {request.temperature}\n"
            f"│  • Stream Mode     : {request.stream}\n"
            "└────────────────────────────────────────────────────────────┘\n"
        )
        logger.info(req_border_uncolored)
        sys.stdout.write(req_border_colored)
        sys.stdout.flush()

        # Format input messages for llama.cpp compatible structure
        formatted_messages = []
        for m in request.messages:
            msg_dict: dict[str, Any] = {"role": m.role}
            if isinstance(m.content, str):
                msg_dict["content"] = m.content
            else:
                msg_dict["content"] = []
                for part in m.content:
                    part_dict: dict[str, Any] = {"type": part.type}
                    if part.text is not None:
                        part_dict["text"] = part.text
                    if part.image_url is not None:
                        part_dict["image_url"] = part.image_url
                    msg_dict["content"].append(part_dict)
            formatted_messages.append(msg_dict)

        # Resolve any file:// image paths in messages to base64 representations
        for m in formatted_messages:
            if isinstance(m.get("content"), list):
                for part in m["content"]:
                    if part.get("type") == "image_url":
                        url = part["image_url"]["url"]
                        if url.startswith("file://"):
                            fp = url[7:]
                            from PIL import Image
                            from io import BytesIO
                            import base64
                            buf = BytesIO()
                            img = Image.open(fp)
                            img.convert("RGB").save(buf, format="JPEG", quality=85)
                            b64 = base64.b64encode(buf.getvalue()).decode()
                            part["image_url"]["url"] = f"data:image/jpeg;base64,{b64}"

        if not request.stream:
            # Sync completion executed on background thread pool
            import asyncio
            start_time = time.perf_counter()
            result = await asyncio.to_thread(
                adapter._llm.create_chat_completion,
                messages=formatted_messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=0.9,
                top_k=40,
                min_p=0.05,
                repeat_penalty=1.1,
            )
            duration = time.perf_counter() - start_time
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")

            # Single-shot beautiful completion report
            report_colored = (
                "\n"
                f"{C_CYAN}┌────────────────────────────────────────────────────────────┐{C_RESET}\n"
                f"{C_CYAN}│{C_RESET}               {C_BOLD}{C_GREEN}CHAT COMPLETIONS INFERENCE REPORT{C_RESET}            {C_CYAN}│{C_RESET}\n"
                f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
                f"{C_CYAN}│{C_RESET}  {C_BOLD}{C_YELLOW}[Execution Metrics]{C_RESET}                                       {C_CYAN}│{C_RESET}\n"
                f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Inference Time{C_RESET}      : {C_BOLD}{duration:.2f}s{C_RESET}\n"
                f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Output Length{C_RESET}       : {len(content)} chars\n"
                f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
                f"{C_CYAN}│{C_RESET}  {C_BOLD}{C_YELLOW}[Generated Content]{C_RESET}                                       {C_CYAN}│{C_RESET}\n"
                f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
                f"{content.strip()}\n"
                f"{C_CYAN}└────────────────────────────────────────────────────────────┘{C_RESET}\n"
            )
            
            report_uncolored = (
                "\n"
                "┌────────────────────────────────────────────────────────────┐\n"
                "│               CHAT COMPLETIONS INFERENCE REPORT            │\n"
                "├────────────────────────────────────────────────────────────┤\n"
                "│  [Execution Metrics]                                       │\n"
                f"│  • Inference Time      : {duration:.2f}s\n"
                f"│  • Output Length       : {len(content)} chars\n"
                "├────────────────────────────────────────────────────────────┤\n"
                "│  [Generated Content]                                       │\n"
                "├────────────────────────────────────────────────────────────┤\n"
                f"{content.strip()}\n"
                "└────────────────────────────────────────────────────────────┘\n"
            )
            logger.info(report_uncolored)
            sys.stdout.write(report_colored)
            sys.stdout.flush()
            
            return result

        else:
            # Async streaming generator sending chunk packets (OpenAI Server-Sent Events spec)
            async def event_generator() -> AsyncGenerator[str, None]:
                import asyncio
                response = await asyncio.to_thread(
                    adapter._llm.create_chat_completion,
                    messages=formatted_messages,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    top_p=0.9,
                    top_k=40,
                    min_p=0.05,
                    repeat_penalty=1.1,
                    stream=True,
                )
                for chunk in response:
                    yield f"data: {json.dumps(chunk)}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        log.exception("Error during chat completion execution")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # In production server script, listen on port 1234 by default
    port = int(os.getenv("TORIIGATE_PORT", "1234"))
    host = os.getenv("TORIIGATE_HOST", "127.0.0.1")
    
    # Configure beautiful server boot screen
    boot_screen = (
        "\n"
        f"{C_CYAN}┌────────────────────────────────────────────────────────────┐{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}                {C_BOLD}{C_GREEN}TORIIGATE API SERVER BOOTED{C_RESET}                 {C_CYAN}│{C_RESET}\n"
        f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Model Path{C_RESET}      : {C_BOLD}{MODEL_PATH}{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Vision Model{C_RESET}    : {MMPROJ_PATH}\n"
        f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• GPU Layers{C_RESET}      : {C_YELLOW}{NGL}{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Context size{C_RESET}    : {NCTX}\n"
        f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Server Address{C_RESET}  : {C_BLUE}http://{host}:{port}{C_RESET}\n"
        f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
        f"{C_CYAN}│{C_RESET}  {C_GREEN}✓ Production API Active & Listening for Requests...{C_RESET}      {C_CYAN}│{C_RESET}\n"
        f"{C_CYAN}└────────────────────────────────────────────────────────────┘{C_RESET}\n"
    )
    sys.stdout.write(boot_screen)
    sys.stdout.flush()

    uvicorn.run(app, host=host, port=port, log_level="warning")
