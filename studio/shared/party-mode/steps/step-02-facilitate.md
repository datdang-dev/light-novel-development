---
name: step-02-facilitate
description: Facilitate Discussion Rounds
nextStepFile: ./step-03-summarize.md
---

# Step 2: Discussion Facilitation 🎤

## STEP GOAL

Manage the discussion flow, ensuring each selected agent contributes according to their persona.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Execute Discussion Round

For each selected **Agent** (e.g., Aria, Suki, Miki):

- **Invoke Persona:** Speak in character about the `{topic}`.
- **Offer Insight:** Provide specialized feedback based on their domain (Character, Prose, Dialogue, etc.).
- **Debate:** Respond to previous agents if conflicting views arise.

### 2. Moderator Intervention (Director K)

Briefly summarize points of agreement/conflict.
Ask clarifying questions if the discussion drifts.

### 3. Present ACTIVE MENU

```
"🔄 **Round Complete.**

**Key Points:** {bullet_points_of_round}

**Options:**
[N] Start Next Round (New sub-topic or rebuttal)
[Q] Ask Specific Question to Agent
[S] Conclude & Summarize (Finish Session)"
```

#### Menu Handling Logic

- IF [N]: REPEAT Step 1 (New Round).
- IF [Q]: Ask user for question -> Agent answers -> Redisplay Menu.
- IF [S]: Load `{nextStepFile}`.
