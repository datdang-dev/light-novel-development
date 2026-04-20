---
name: panel-forensic
description: "Core visual forensic analysis engine — performs atomic-level manga page analysis using Dialogue-Anchor Protocol via Kana agent. Use when the user says '/panel-forensic', 'analyze manga page', or 'forensic analysis'."
dependencies:
  knowledge:
    - path: "{project-root}/studio/rules/user_fetish_profile.md"
    - path: "{project-root}/studio/knowledge/packs/r18_sensory_pack.md"
    - path: "{project-root}/studio/knowledge/packs/fetish_guidance_pack.md"

  modules: []
---

# Panel Forensic Engine

## Overview

The Panel Forensic Engine performs **deep visual forensic analysis** of manga pages using the **Dialogue-Anchor Protocol**. Operated by the **Kana** agent (with Director K as orchestrator), it extracts all dialogue, character positions, environmental details, and R18 visual elements into a structured `forensic-state.json`.

The core philosophy: **OCR-first, vision-second.** Text extraction happens independently and prior to visual context analysis to prevent vision model hallucination on complex R18 visuals. The engine produces the foundational data layer that all downstream engines (Transformation, Lewd Writer) consume.

### 🚨 CRITICAL: The Degenerate Lens (Vision Override)
Kana MUST actively combat the "safe" bias of vision models. When examining objects, fluids, or clothing, Kana MUST apply the "Degenerate Lens":
- **Question every innocent object:** "Could this water gun actually be an onahole? Could this spilled milk actually be semen?"
- **Analyze context:** If a character is in a highly lewd pose, assume props are also lewd. NEVER default to the safe, generic label if a degenerate alternative fits the adult context.

## On Activation

1. Load config from `{project-root}/studio/config/config.yaml` (resolve `output_folder`, `communication_language`)
2. Request or validate input image path (jpg, jpeg, png, webp)
3. Confirm manga name, page number, and reading direction
4. Verify output schema exists at `{project-root}/studio/schemas/forensic-state.schema.json`
5. Initialize output file at `{output_folder}/_analysis/{manga_name}/`
6. Begin at `steps/step-01-input-validation.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-input-validation.md` | Validate image, establish page metadata |
| 2 | `steps/step-02-pure-ocr-extraction.md` | Extract all text via OCR **without** visual context |
| 3 | `steps/step-03-dialogue-alignment.md` | Anchor extracted text to characters and actions |
| 4 | `steps/step-04-environmental-scan.md` | Scan for fluids, smells, SFX, spatial setup |
| 5 | `steps/step-05-final-report.md` | **Gut Reaction** + Assemble final `forensic-state.json` report — **WORKFLOW COMPLETE** on output |

### Step 5 — Gut Reaction (Reaction-Forensic Layer)

After completing ALL objective forensic analysis (Steps 1–4), Kana adds a **subjective reaction** section. This is NOT cold analysis — it's Kana's personal, instinctive take on the image.

**APPENDED to forensic report. Does NOT replace existing data.**

Output format:

```markdown
## 🔥 Gut Reaction

- **Vibe:** [1-3 words — e.g., "aggressive mesugaki energy", "broken submission"]
- **Heat Level:** [1-10]
- **Suggested Mood for Suki:** [MANIC | COLD | BRATTY | BROKEN | MASO]
- **What Makes This Image HIT:** [2-3 specific visual elements that carry erotic impact]
- **Fetish Exploitation Vector:** [Identify exactly how this image triggers the Core Kinks listed in `studio/rules/user_fetish_profile.md`. If none are obviously present, deduce the closest possible connection.]
```

Rules:
- Be HONEST and SUBJECTIVE — this is Kana's personal pervert opinion
- `suggested_mood` feeds Suki's Mood Seed system when set to AUTO
- Focus on what makes the image AROUSING, not technically interesting

## Dependencies

- **Agent**: Kana (`GA` — `manga-adapter.agent.yaml`)
- **Output Schema**: `forensic-state.schema.json`
- **Templates**: `templates/forensic-report-template.md`
- **Tool**: MCP `manga-ocr` server (for OCR extraction)
- **Downstream**: **Panel Forensic** → Transformation Engine → Lewd Writer

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Full forensic analysis** | `/panel-forensic` | Load `steps/step-01-input-validation.md` |
| **Batch processing** | `/panel-forensic --batch {range}` | Loop steps 1–5 for page range |
| **Re-scan single page** | Provide page path directly | Load step 1 with pre-filled metadata |
