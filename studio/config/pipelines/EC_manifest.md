---
name: EC_manifest
description: "MCP-driven single-session manifest for the [EC] Erotic Image Captioner pipeline. Uses toriigate MCP tools for forensic analysis, scene prelude, and caption generation."
execution_mode: ONE_SHOT
pipeline: MCP Forensic Analysis → MCP EC Pipeline
output: caption.json only (no intermediate file writes)
version: "2.0.0"
---

# EC Pipeline Manifest (MCP-Driven)

> **AI INSTRUCTION:** Read this file ONCE at pipeline start. It contains the essential configuration for the MCP-driven EC pipeline. The actual prompts are loaded dynamically from `studio/prompts/` by the toriigate MCP server.

## 🌐 GLOBAL RULES (Always Active)

**Language:** All narration and dialogue → 100% Vietnamese. SFX → Romaji/English only.

**Canon Override:** Never invent objects, acts, or characters not visible in the source image.

**Mandatory Vocabulary:** Tục tĩu, trần trụi, kích dục mạnh. Dứt khoát dùng: cặc, lồn, địt, đụ, tinh trùng. **CẤM:** âm đạo, dương vật, giao cấu, mọi từ lãng mạn sáo rỗng.

**User Fetish Priority (Core Kinks):** Mesugaki/Bratty slut, scent/fluid degradation (used condoms, sweat, armpit), nylon/foot worship, explicit-gesture tease, used garment defilement.

**Gooner Principles (Layer 0):** Internalize ALL 7 principles from `studio/rules/gooner_principles.md`. Most critical for EC: **P1 (Erection Test)**, **P2 (Zero Judgment)**, **P4 (Scent Over Sight)**, **P7 (Arousal Momentum)**.

## ⚙️ INITIALIZATION

1. Validate image path exists.
2. Extract image `basename` → output dir: `_lnd-output/_captions/{basename}/`
3. Read `mood_seed` param (default: `AUTO`). Valid: `AUTO | MANIC | COLD | BRATTY | BROKEN | MASO | EXHIBITIONIST`
4. Read optional `user_context` (backstory hint).

## 🔧 MCP TOOL USAGE

This manifest orchestrates the following MCP tool calls via the `toriigate` server:

1. **Forensic Analysis** - Uses `studio/prompts/forensic_analysis.txt`
   - Tool: `forensic_analysis`
   - Output: `_lnd-output/{basename}/forensic.json`

2. **Full EC Pipeline** - Uses all three prompt templates:
   - Tool: `run_ec_pipeline` 
   - Output: `_lnd-output/{basename}/` (forensic.json, prelude.json, caption.json)

**Note:** The `run_ec_pipeline` tool executes the complete pipeline in ONE_SHOT mode for optimal VRAM usage on 6GB GPUs.

## 📦 FINAL OUTPUT

Write ONE file: `_lnd-output/_captions/{basename}/caption.json`

```json
{
  "image": "{basename}.png",
  "pipeline_version": "v2.0.0",
  "execution_mode": "ONE_SHOT",
  "metadata": {
    "mood_seed": "{resolved_mood}",
    "theme": "{derived_theme}",
    "ocr_context": ["{extracted_text}"]
  },
  "content": {
    "caption": "{final_caption_text}"
  }
}
```
```