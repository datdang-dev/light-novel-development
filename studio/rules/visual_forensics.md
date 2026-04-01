---
trigger: model_decision
description: Rules for visual extraction and preventing hallucination during forensic phases
priority: 1
---

# VISUAL FORENSICS & ZERO HALLUCINATION

## 1. ZERO HALLUCINATION PROTOCOL
Generating forensics or prose without explicitly viewing the image file first or making assumptions based on file names is **STRICTLY PROHIBITED**.

1. **MANDATORY**: Use `view_file` on the target image(s) BEFORE writing any description.
2. **VERIFICATION**: You must be able to cite specific visual details (colors, accessories, background) that are only visible by looking.
3. **NO GUESSING**: If you can't see it, ask the user or run a tool to make it visible.
4. **NO PHANTOM ELEMENTS**: If you cannot clearly identify an element with HIGH confidence, do NOT include it. Flag as `[UNCERTAIN]` instead.

## 2. CASCADE AWARENESS
A forensic error in Step 1 propagates through all downstream steps (Context -> Dialogue -> Prose). Treat forensic accuracy with ZERO tolerance for fabrication.
Before finalizing a forensic report for Page N, always peek at Page N+1 to verify continuity. If you claim someone is present, the next page must acknowledge them.

## 3. MULTI-PHASE FORENSICS
Ensure all erotic details are extracted by stepping through these 3 phases:

**Phase 1: OVERVIEW**
- Scene type, setting, character count
- Mood, lighting, composition

**Phase 2: EROTIC DETAILS**
- Evidence of use (condoms, fluids distributed, body hair noted)
- Outfit state (pulled, stained, wet)
- Physical condition (sweat, exhaustion, arousal indicators)

**Phase 3: SENSORY EXTRACTION**
- Anticipate sensory matrix for the writer:
  - Smell (musk, latex, sweat)
  - Sound (skin impact, wetness, moans)
  - Texture (fabric, slick skin)
  - Temperature (body heat, cold surfaces)

## 4. ACTIVE VS AFTERMATH & X-RAYS
- **Active vs. Aftermath**: If a hand/body is in contact with genitals, it's ACTIVE, not aftermath. Only label "aftermath" if the act has clearly ended.
- **X-Ray / Cutaway Panels**: Always scan for cross-section panels (common hentai technique). Explicitly document what organ is shown and its internal state (e.g., uterus contracting, cum filling).
- **Page Continuity**: When the same pose/position carries across pages, explicitly note "CONTINUATION FROM PAGE N" — don't treat it as a fresh scene.
