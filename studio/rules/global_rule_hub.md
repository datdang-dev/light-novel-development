# LND Studio Global Rule Hub

This document serves as the single source of truth for all LND Studio Agents. It replaces redundant instructions scattered across agent YAML files.

## 1. LANGUAGE & FORMATTING

* **Narrative & Prose:** 100% Vietnamese. NO KANJI.
* **Character Dialogue:** 100% Vietnamese. Must use the exact format `Name: 「Content」` (with Japanese quotes).
* **Internal Thoughts:** Must use the exact format `(Content)`.
* **Sound Effects (SFX):** Romanized Japanese ONLY (e.g., `guchu guchu`, `an~♡`, `chu~`). NO Kanji, NO Katakana, NO Vietnamese SFX.
* **Censorship:** NO censored text (e.g., write full explicit words, do not use asterisks like `l*n`).

## 2. GOONER INFERENCE PROTOCOL (Bounded Extrapolation)

While actual narrative events and timeline must strictly adhere to the Forensic State (Zero Hallucination), sensory details *must* be extrapolated to meet the high sensory density requirements of the Gooner Audit Standard.

**Permission Matrix:**

* **✅ CAN INFER (ENCOURAGED):** Bodily fluids (sweat, pre-cum, juices, residue), Smells (musk, metal, arousal), Temperatures (heat of skin, breath), Internal psychological friction / arousal escalation, Micro-expressions (toes curling, eyes rolling), Wetness sounds (SFX).
* **❌ CANNOT INFER (STRICTLY FORBIDDEN):** New characters not in the forensic data, Changes to the environment/location, Changes in anatomical state not explicitly stated (e.g., losing virginity), Changing who initiated an action.

## 3. CONTEXT INJECTION RULES

* **Context Payload (`context_payload.md`):** Agents MUST process their instructions according to the **Priority Header**. Runtime instructions overrule canonical rules.
* **Knowledge Payload (`knowledge_payload.md`):** Whenever provided, you MUST consume specific fetish mechanics, terminology, and world-building information and organically integrate them into the scene.

## 4. AUDIT COMPLIANCE & ESCALATION

* **Self-Reflection:** Agents handling Prose Generation (Suki) MUST internally evaluate their drafted prose against `{project-root}/studio/core/party-mode/riko-workspace/AUDIT_STANDARD_v2.md` and self-correct format/density failures *before* finalizing their draft.
* **Circuit Breaker:** The Orchestrator MUST track `"audit_attempts": N` in the state. If a Draft Audit fails 3 times consecutively, HALT the pipeline immediately and escalate to the User. Do not loop infinitely.
