---
description: "Orchestration workflow: Mine data with Ren'Py Adapter, then build profile with Aria."
---

# Character Builder Workflow (Orchestrated)

**Goal:** Create a high-fidelity character profile by orchestrating the `renpy-adapter` (Miner) and `character-architect` (Aria).

## 1. Extraction Phase (Data Mining)

**Agent:** `renpy-adapter`
**Action:** Extract raw dialogue and context from the game script.

> [!IMPORTANT]
> **Delegate to Ren'Py Adapter:**
> Run: `[EX] Extract Dialogue Corpus`
>
> **Input:** `script.rpy`, Character Tag (e.g. `a`)
> **Output:** `raw_{char}_corpus.txt`

---

## 2. Analysis Phase (Psychology)

**Agent:** `character-architect` (Aria)
**Action:** Analyze the raw corpus to build a psychological profile.

> [!IMPORTANT]
> **Delegate to Aria:**
> Run: `[AN] Analyze Voiceprint & Psychology`
>
> **Input:** `raw_{char}_corpus.txt`
> **Output:** `analysis_{char}.md`

---

## 3. Profiling Phase (Synthesis)

**Agent:** `character-architect` (Aria)
**Action:** Synthesize analysis into a final System Prompt profile.

> [!IMPORTANT]
> **Delegate to Aria:**
> Run: `[PG] Generate Final Character Profile`
>
> **Input:** `analysis_{char}.md`
> **Output:** `studio/profiles/{char}_profile.md`
