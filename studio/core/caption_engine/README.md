# 🔬 LND Studio Caption Engine

A highly optimized, production-ready multimodal vision & prose captioning engine. This engine runs **entirely in-process** as a single FastMCP server, executing high-fidelity visual description and direct R18/hentai panel captioning via a fine-tuned vision model.

---

## 📂 Directory Structure

The engine is completely decoupled from UI frameworks and maintains a flat, simplified structure:

```
studio/core/caption_engine/
├── README.md               # This documentation
├── caption_engine.py       # Flat unified domain orchestrator (Direct Visual Captioning Facade)
├── adapters/               # Infrastructure adapters (MCP clients, file repositories)
│   ├── filesystem_output_repo.py
│   ├── in_process_qwen2vl_adapter.py  # In-process llama_cpp model executor
│   ├── studio_prompt_loader.py       # Decoupled dynamic prompt loader
│   └── toriigate_mcp_adapter.py      # Backwards-compatible HTTP API adapter
├── interfaces/             # Core abstract interface contracts
│   └── mcp_client.py
├── models/                 # Model assets folder (GGUF checkpoints & vision projectors)
└── server/                 # Headless FastMCP bridge
    ├── chat_handler_qwen2vl.py   # High-efficiency custom KV-cache Qwen2-VL sampler
    └── mcp_server.py             # Single in-process FastMCP server exposing tools
```

---

## 🧠 Multimodal Vision Models

The server leverages a highly optimized quantized fine-tune of **Qwen2-VL-7B** for structural understanding, localized character parsing, and high-fidelity erotic visual recognition.

### Model Requirements
Download the GGUF checkpoints and save them directly in the `studio/core/caption_engine/models/` directory:

1. **Vision Model**: `ToriiGate-0.5_Q4_K_L.gguf` (Quantized 7B Qwen2-VL fine-tune)
   - Source: [mradermacher/ToriiGate-v0.5-7B-GGUF](https://huggingface.co/mradermacher/ToriiGate-v0.5-7B-GGUF)
2. **Vision Projector**: `mmproj_Q8_0.gguf`
   - Source: [Qwen/Qwen2-VL-7B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct-GGUF)

---

## ⚡ Operation

### Single In-Process Server (Prism Design)
Unlike traditional configurations that split the execution into a separate model service and a tool server (leading to double-server overhead, open sockets, and base64 transmission delays), the LND Studio Caption Engine uses a **unified, in-process architecture**:

1. When Claude Code or another agent starts the FastMCP server (`mcp_server.py`), the process launches.
2. Upon receiving the first tool invocation, the GGUF model and its multimodal projector are loaded directly **in-process** via Python bindings (`llama_cpp`) using hardware-accelerated thread pools.
3. Subsequent visual descriptions and panel steps are executed in-memory.

This eliminates all uvicorn processes, subprocess spawning, local port conflicts, and HTTP connection errors, boosting inference response times significantly.

---

## 🛠️ MCP Tools Exposed

The MCP server (`mcp_server.py`) registers the following tools for agents to query:

1. **`run_ec_pipeline`**
   - Orchestrates the direct, single-pass visual captioning of the target image using the fine-tuned vision model. Saves output to `caption.json`.
2. **`describe_image`**
   - Exposes a free-form vision-QA prompt interface to query the model about characters, text, poses, or objects.
3. **`check_backend_status`**
   - Checks the health and hardware configuration of the loaded in-process Qwen2-VL model.
