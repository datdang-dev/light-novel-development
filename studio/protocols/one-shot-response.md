# One-Shot Response Protocol

# `studio/protocols/one-shot-response.md`

---

version: "1.0.0"
applies_to: [EC, PA]
---

## Purpose

The One-Shot Response Protocol defines how **lightweight pipelines** (EC, PA) execute inside a single LLM response without intermediate file writes.

This protocol eliminates the "multi-LLM simulation tax" — the pattern of writing intermediate artifacts (forensic.md, prelude.md) to disk and re-reading them, which adds 3-4 unnecessary tool calls per pipeline run.

## When to Use

Use this protocol when the pipeline manifest includes `execution_mode: ONE_SHOT`.

Currently enabled for:

- **EC** (Erotic Image Captioner): Kana → Luna → Suki
- **PA** (Prose Adapter): Suki only

Do NOT use for:

- **MA** (Manga-to-Novel): Too complex; intermediate artifacts required for Riko's audit
- **ND** (Novel Development): Multi-session state needed

## Execution Rules

### Rule 1: All intermediate work lives in `<think>` blocks

Kana's forensic analysis and Luna's prelude are computed internally. They are NOT written to disk.

```xml
<think>
  <!-- KANA FORENSIC ANALYSIS -->
  OCR: ...
  Characters: ...
  Explicit: ...
  Gut Reaction: ...

  <!-- LUNA SCENE PRELUDE -->
  Setting: ...
  The Why: ...
  Sensory Anchors: ...

  <!-- SUKI COT SCRATCHPAD -->
  Deep Forensic Application: ...
  Voice Derivation: ...
  Self-Audit: ...
</think>
```

### Rule 2: Only the FINAL artifact is written to disk

One `write_to_file` call only: `caption.json`.

### Rule 3: Handoff declarations are still required

Even in ONE_SHOT mode, the AI MUST follow the `PASS / DROP` handoff protocol embedded in the pipeline manifest. This prevents context bleeding between persona stages.

### Rule 4: Quality gates are self-enforced in the COT block

Each agent's quality gate checklist must be evaluated inside `<think>` before output is generated.

## Comparison: Standard Mode vs One-Shot Mode

| Metric | Standard Mode | ONE_SHOT Mode |
|---|---|---|
| Config reads | 5 (5× SKILL/agent files) | 1 (manifest only) |
| Intermediate writes | 3 (forensic/prelude/caption.md) | 0 |
| Intermediate reads | 2 (agent re-reads prior outputs) | 0 |
| Final writes | 1 (caption.json) | 1 (caption.json) |
| Task tracking | 3 updates | 1 update |
| **Total tool calls** | **~15** | **~5** |
