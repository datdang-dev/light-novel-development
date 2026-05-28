# Erotic Image Captioner Pipeline (Unified Caption Engine)

## Overview

The Erotic Image Captioner (EC) has been refactored from a multi-agent manual prompting sequence and complex MCP tool structure into a **unified, high-performance local Caption Engine** (`studio/core/caption_engine/caption_engine.py`). 

Instead of prompting multiple text-only agents (Kana, Luna, Suki) in-session with large system files or invoking fragmented MCP tools, LND Studio now leverages a single optimized multimodal execution pass using the Qwen2-VL local vision engine. Prompts reside as independent templates in `studio/prompts/` and are loaded dynamically on-demand based on the specified `--type`.

This architecture ensures:
1. **Low VRAM footprint**: Visual inference runs in clean, dedicated local processes without multiple client-server context duplications.
2. **Beautiful Observability**: Color-coded, dashboard-style execution logging with real-time terminal output and log files (`_lnd-output/caption_engine.log`) suitable for `tail -f`.
3. **Toggleable Streaming**: CLI option (`--no-stream`) to switch between instant single-shot generation and real-time chunk streaming.

**Unified Architecture:**
```
[User Image] ──> [CaptionEngine (caption_engine.py)]
                        │
                        ├──► Loads: studio/prompts/{type}.txt (e.g., long_thoughts_v2, manga, etc.)
                        ├──► Resolves base64/local files
                        └──► Executes local InProcessQwen2VLAdapter
```

---

## 🛠️ CAPTION ENGINE CLI SET

The engine can be invoked directly from the CLI or via automated workflows using the following syntax:

```bash
python3 studio/core/caption_engine/caption_engine.py \
    --image "/path/to/image.png" \
    --type "long_thoughts_v2" \
    --mood "AUTO" \
    --temp 0.5 \
    --max-tokens 4096
```

### Parameter Map:
*   `--image`: Absolute path to the target image file (mandatory).
*   `--type`: Prompt style from `studio/prompts/` (e.g., `long_thoughts_v2`, `manga`, `json`, `md_comic`).
*   `--mood`: Mood setting seeds (e.g., `AUTO`, `MANIC`, `COLD`, `BRATTY`, `BROKEN`, `MASO`).
*   `--context`: Optional backstory or descriptive user context to inject.
*   `--temp`: Generation temperature (default: `0.5`).
*   `--max-tokens`: Max output generation length (default: `4096`).
*   `--no-stream`: Disables real-time streaming, running in clean single-shot mode.

---

## 📋 PIPELINE EXECUTION STEPS

When executing the pipeline, the active agent (typically Nova) or the orchestrator invokes the Caption Engine directly:

### Step 1 — Ingest & Validate
1. Verify the input image path exists.
2. Read the `mood_seed` parameter (default: `AUTO`).
3. Capture optional `user_context` (backstory/constraints).

### Step 2 — Direct Multimodal Generation
1. The engine dynamically compiles the prompt using `StudioPromptLoader` from the target template in `studio/prompts/{type}.txt`.
2. The engine initializes the local in-process model wrapper (`InProcessQwen2VLAdapter`) referencing `models/ToriiGate-0.5_Q4_K_L.gguf` and `mmproj_Q8_0.gguf`.
3. **Inference with Streaming/Single-Shot**: Depending on `--no-stream`, tokens are either streamed back in real-time with an ANSI colored dashboard or processed in a single fast block.
4. Output is verified and persisted in `_lnd-output/_captions/` as well as color-logged in `_lnd-output/caption_engine.log`.

---

## 📦 OUTPUT DIRECTORY STRUCTURE

For each processed image, the pipeline writes:

```
_lnd-output/_captions/
└── {image_name}_{timestamp}_{type}.md   # Output markdown/JSON formatted report
```

And appends live execution monitoring data to:
```
_lnd-output/caption_engine.log           # Structured color logs (viewable with tail -f)
```

---

## 🚀 ADVANTAGES OF THE NEW UNIFIED CONCEPT

1. **Deterministic Environment**: Bypasses unstable fastmcp/client-server connections. The execution is in-process and fast.
2. **Flexible Templates**: Switch prompt engineering templates on-the-fly by dropping new txt/md files into `studio/prompts/` and calling `--type {filename}`.
3. **Production Observability**: Full execution telemetry (token count, generation speed, temperature, and visual parameters) are beautiful, colored, and persisted.
