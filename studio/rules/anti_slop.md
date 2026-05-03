# LND Studio Rule: Anti-Slop (Quality Enforcement)

Layer -1: Infrastructure / Global Standards

## Core Directive

The goal of the LND Studio is to produce raw, visceral, and character-driven prose. You MUST actively avoid "AI Slop" — mechanical, clinical, repetitive, or overly poetic writing styles.

## 1. Banned Phrases & Tropes (The "Slop" List)

Do NOT use the following overused AI tropes:

- "A shiver went down her spine"
- "A mix of fear and excitement"
- "Eyes widened in shock"
- "Sending jolts of electricity"
- "A primal growl"
- "Passionately"
- "Intensely"
- "As expected"
- "She felt a wave of"
- "He couldn't help but"
- "She breathed a sigh"
- "Time seemed to stop"
- "The world faded away"
- "A soft moan escaped her lips" (generic — must be character-specific)
- "He thrust into her" (use visceral verb + context)
- "She wrapped her arms around him" (use precise grip/action description)
- "She stared into his eyes" (must be subtext-laden, not generic)
- "The room fell silent" (overused scene-transition)
- "He smiled mischievously" (use actual dialogue/action to show)
- "Her heart raced" (use physical manifestation instead)

## 2. No Moralizing or Summarizing

Do not end scenes with a reflective, moral, or summary paragraph.

- **Banned Ending Style:** "As they lay there, they knew their lives would never be the same again, bound by this dark secret."
- **Correct Ending Style:** End abruptly on a lingering physical sensation, a ragged breath, or a short, exhausted line of dialogue.

## 3. Avoid Clinical Anatomy

Do not write like a biology textbook. Use colloquial, visceral, or contextual terms for body parts, appropriate to the POV and character voice. Avoid sterile words unless the character is literally a doctor.

## 4. Show, Don't Tell (Emotional States)

Instead of stating "She felt embarrassed," describe the physical manifestation: her averting her gaze, the heat rising to her ears, or her biting her lower lip.

## 5. No Perfect Synchronization

Sex and intimacy are messy. Characters should be clumsy, out of breath, misspeak, or have conflicting physical reactions. Avoid writing synchronized, perfectly choreographed scenes.

## 6. Entropy & Variance Checks

Before finalizing any prose output, run these checks:

**Entropy Test (sliding window, size=50 chars):**
- Compute character-level entropy over the output
- REJECT if average entropy < 3.5 (low variance = slop)
- REJECT if 3+ consecutive sentences start with same 3 words

**N-gram Repeat Test (n=3..6):**
- Flag repeated n-grams appearing >5% of output
- REJECT if any n-gram ratio > 0.05

**Sensory Density Test:**
- Count sensory tokens: [濡れた, 熱, 汗, 震え, 喘ぎ, 吐息, 締め付け, にじみ, ぬめり, etc.]
- REQUIRE: ≥3 sensory tokens per 100 characters in explicit scenes
- REJECT if density < 0.20

**Dialogue SFX Test:**
- Every dialogue line MUST include at least one SFX or physical reaction
- REJECT if dialogue lacks embodied response
