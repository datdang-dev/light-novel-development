# Step 2: Voiceprint Analysis

**Goal:** Distill 1000+ lines of raw dialogue into a dense "Psychological Profile" and "Style Guide".

## Input Required

- **`raw_{character_tag}_corpus.txt`**: The output from Step 1.

## Analysis Process (AI Task)

Analyze the corpus to identify the following 4 pillars of the character:

1. **Voice & Speech Patterns:**
    - Sentence structure (Short/Long? Formal/Slang?).
    - Verbal tics (Stutters, "Ugh", "Hmph").
    - Catchphrases or specific vocabulary.
    - Tone shifts (e.g., Haughty -> Flustered).

2. **Psychological Drivers:**
    - Core Motivations (Pride? Lust? Fear?).
    - Insecurities (What makes them defensive?).
    - Triggers (What specific words/actions set them off?).

3. **Kinks & Fetishes:**
    - Implicit desires revealed through dialogue/reactions.
    - Explicit preferences.

4. **Relationship Dynamics:**
    - How do they treat the Protagonist? (Hostile? Subservient? Tsundere?).
    - How does this evolve?

## Output Artifact

Create a new file: `analysis_{character_tag}.md`

```markdown
# Character Analysis: [Name]

## 1. Voiceprint
- **Tone:** [Adjectives]
- **Common Phrases:** [List]
- **Sentence Structure:** [Description]

## 2. Validation Checks (Golden Rules)
- Rule 1: [e.g., "Never admits she is wrong directly"]
- Rule 2: [e.g., "Stutters when complimented"]

## 3. Kink Profile
- [Tag 1]: [Context]
- [Tag 2]: [Context]
```

## Next Step

Proceed to **[Step 3: Profile Generation](./step-03-profile-generation.md)** to finalize the profile for the main studio.
