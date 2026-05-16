---
trigger: model_decision
description: "Sensory density contract. Reference by name — do NOT restate inline."
priority: 1
---

# 🎯 Sensory Contract

> **RULE:** Every prose block (narration, caption, RP turn) MUST satisfy ALL 3 anchors below.
> Missing ANY anchor = REJECT.

## Required Anchors

| # | Anchor Type | What Qualifies | Examples |
|---|-------------|---------------|----------|
| 1 | **SMELL** | Any olfactory reference | mùi mồ hôi, nồng, tanh, hương dâu, mùi tinh trùng |
| 2 | **TEXTURE / TEMPERATURE** | Tactile or thermal | nóng hổi, trơn tuột, nhớt, da mịn, rát bỏng, lạnh ngắt |
| 3 | **SOUND** | SFX or described audio | *guchu guchu*, thở dốc, rên rỉ, lép nhép, tiếng bóp |

## Self-Check (run before output)

```
□ ≥1 SMELL word present?     → YES / NO (if NO → add before submit)
□ ≥1 TEXTURE/TEMP present?   → YES / NO (if NO → add before submit)
□ ≥1 SOUND present?          → YES / NO (if NO → add before submit)
```

## Anti-Pattern: Stacking

Do NOT stack all 3 anchors in one sentence. Distribute across the prose block for natural density.

❌ Bad: "Mùi mồ hôi nồng nặc, da trơn nhớt, tiếng rên rỉ vang lên."
✅ Good: Smell in paragraph 1, texture in paragraph 2, sound as SFX between dialogue.
