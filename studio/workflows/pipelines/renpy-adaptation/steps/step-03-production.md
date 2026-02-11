---
name: 'step-03-production'
description: 'Activate Lewd Writer for prose drafting (Enforce Language)'
---

# Step 3: Production (The Craft)

## STEP GOAL

Draft the Light Novel Chapter in the configured language, strictly adhering to the project's formatting standards.

## 🚨 MANDATORY CONFIGURATION CHECK 🚨

1. **LOAD CONFIG:** Read `{project-root}/_bmad/bmb/config.yaml`.
2. **EXTRACT:** `communication_language` (Expected: Vietnamese).
3. **EXTRACT:** `user_name`.
4. **VERIFY:** If `communication_language` is NOT English, you **MUST** write the prose in that target language.

## EXECUTION

1. **Activate Agent:** Load and activate `studio/agents/L2_developers/lewd-writer.md`.
    * *Constraint:* You are SUKI. You must obey the "Prose in Vietnamese" rule if config dictates.
2. **Load Template:** Read `studio/_templates/light-novel-prose.md`.
3. **Input:** Load `studio/generated/scene_analysis_{scene}.md`.
4. **Drafting:** Write the chapter file `studio/novels/volume1/chapter_{scene}.md`.
    * **Dialogue:** `「...」` (Japanese/LN style) in **Vietnamese**.
    * **Thoughts:** `(...)` in **Vietnamese**.
    * **SFX:** Romanized Japanese (e.g. *Guchu*, *Pan*, *Hahn*).
    * **Narration:** **Vietnamese**.
5. **Review:** Check against the `hentai_lexicon.md` for proper terminology if needed. (Do not invent random words).

## COMPLETION

Once the file is successfully written:

1. **Notify User:** Present the path to the new chapter for review.
2. **Terminate Workflow:** The pipeline is complete.
