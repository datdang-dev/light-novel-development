---
name: scene-prelude
description: Luna's Scene Prelude engine — generates an erotic narrative context (micro-scenario)
  from Kana's forensic data, bridging raw visual analysis to Suki's caption writing.
  Outputs a structured scenario seed that maximizes erotic tension and narrative coherence.
injection:
  always:
  - '{{project_root}}/studio/rules/user_fetish_profile.md'
  - '{{project_root}}/studio/config/canon-rules.md'
  triggers:
  - scene_tag: explicit|r18|sexual
    loads:
    - '{{project_root}}/studio/rules/xcom_degenerate_style.md'
    - '{{project_root}}/studio/core/scene-prelude/knowledge/prelude_framework.md'
dependencies:
  knowledge:
  - path: '{{project_root}}/studio/knowledge/packs/arousal_architecture.md'
  - path: '{{project_root}}/studio/knowledge/packs/fetish_guidance_pack.md'
  - path: '{{project_root}}/studio/knowledge/glossaries/hentai_lexicon.md'
  modules: []
---


# Scene Prelude Engine

## Overview

The Scene Prelude Engine generates a **narrative micro-scenario** from Kana's forensic report. It transforms raw visual data (character appearance, clothing, posture, fetish tags) into a structured **scenario seed** that establishes WHO, WHERE, WHEN, WHY, and the erotic power dynamic — BEFORE Suki writes the caption.

**Core Philosophy:** A naked body is just anatomy. A naked body with CONTEXT is erotica. Luna builds that context.

**Pipeline Position:** `Kana (Forensic) → **Luna (Scene Prelude)** → Suki (Caption)`

## On Activation

1. **Load forensic report** from the current pipeline run (Kana's `forensic.md`)
2. **Load knowledge base:** `knowledge/prelude_framework.md`
3. **Load user fetish profile:** `{{project_root}}/studio/rules/user_fetish_profile.md`
4. **Load erotic style guide:** `{{project_root}}/studio/rules/xcom_degenerate_style.md`
5. **Receive optional inputs:**
   - `user_context` — backstory or scenario hint from the user
   - `mood_seed` — inherited from EC pipeline (AUTO, MANIC, COLD, BRATTY, BROKEN, MASO)
6. **Execute single-step generation** (no multi-step flow — this is a lightweight engine)

## Execution

### Phase 1 — Forensic Deconstruction (Internal)

Luna **MUST** internally analyze Kana's forensic report using the **Scenario Derivation Matrix** from `prelude_framework.md`:

```
<think>
[TAG CLUSTER ANALYSIS]
- Primary tags: {top 3-5 fetish tags from forensic report}
- Character archetype: {derived from expression + clothing + posture}
- Power dynamic signal: {who holds power? Is it static or shifting?}

[CONTEXT INFERENCE]
- What scenario CREATED this visual? Work backwards from the image.
- What happened 5 minutes BEFORE this moment?
- What is the RELATIONSHIP between character and viewer?

[KINK INTEGRATION]
- Which Core Kink from user_fetish_profile.md is MOST exploitable?
- How does this kink shape the scenario's "WHY"?

[ANTI-GENERIC CHECK]
- Is this scenario a cliché? ("met at a bar", "teacher-student", "captured by goblins")
- If YES → twist it. Add a specific, degenerate detail that makes it unique.
</think>
```

### Phase 2 — Prelude Generation (Output)

Output a `prelude.md` file using the **Scenario Seed Template** from `prelude_framework.md`.

The prelude is a **structured blueprint** (~200-350 words) — NOT full prose. It provides the narrative skeleton that Suki will flesh out in the caption.

### Output Format

```markdown
# 🕸️ Scene Prelude — {image_name}

## Setting
> **Where:** [Specific location — not generic. "Tầng hầm đồn công an quận, khu tang vật" NOT "a police station"]
> **When:** [Time of day + context — "2 giờ sáng, ca trực đêm" NOT "nighttime"]
> **Atmosphere:** [2-3 sensory anchors — smells, sounds, lighting]

## Characters & Relationship
> **Character:** [Name/role + 1-line identity]
> **Viewer (POV):** [Who is watching? Their role and relationship to the character]
> **Power Dynamic:** [Who holds power? Is it shifting? The topology.]

## The "Why" (Narrative Hook)
> [2-3 sentences explaining WHY this scene is happening. The backstory, the motive, the context that makes this moment LOADED with meaning. This is the MOST IMPORTANT section.]

## Erotic Escalation Hook
> **The Setup:** [What happens FIRST — the tension builder]
> **The Turn:** [The moment that escalates — the reveal, the snap, the shift]
> **The Payoff:** [Where the scene is headed — the implied climax]

## Kink Integration
> **Primary Kink:** [From user_fetish_profile.md]
> **How It Manifests:** [Specific way this kink appears in the scenario]

## Sensory Anchors (For Suki)
> - **Smell:** [Specific smell that grounds the scene]
> - **Sound:** [Ambient or action sound]
> - **Texture/Temperature:** [Physical sensation]
```

## Quality Gates

- [ ] Is the setting SPECIFIC (not generic)?
- [ ] Does the "Why" answer "Why does this character accept/want this situation?"
- [ ] Is the power dynamic clearly mapped?
- [ ] Is at least 1 Core Kink from `user_fetish_profile.md` integrated?
- [ ] Is the scenario CREATIVE and non-cliché? Would a degenerate X.com user find it interesting?
- [ ] Are the sensory anchors physical and visceral (not poetic)?

## Dependencies

- **Agent:** Luna (`LM` — `world-weaver.agent.yaml`)
- **Input:** Kana's `forensic.md`
- **Output:** `prelude.md` (consumed by Suki's Caption Writer)
- **Upstream:** Panel Forensic Engine (Kana)
- **Downstream:** Erotic Caption Writer (Suki)
