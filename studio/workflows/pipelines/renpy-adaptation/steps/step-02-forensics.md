---
name: 'step-02-forensics'
description: 'Activate Panel Forensic for visual analysis'
nextStepFile: './step-03-production.md'
---

# Step 2: Visual Forensics (The Eye)

## STEP GOAL

Analyze the extracted context for visual details, sensory information, and character psychology.

## EXECUTION

1. **Activate Agent:** Load and activate `studio/agents/L2_developers/panel-forensic.md`.
2. **Input:** Load the `studio/generated/{scene}_context.txt` file from Step 1.
3. **Execute Analysis:**
    * Identify Character States (Emotions, Clothing).
    * Identify Environment (Lighting, Sound).
    * Identify Key Assets (Image tags like `d31_helenoff01`).
4. **Output:** Generate `studio/generated/scene_analysis_{scene}.md`.
    * *Format:* Standard Forensic Report (Metadata, Narrative Arc, Sensory Details).
5. **Proceed:** Once complete, load `step-03-production.md`.
