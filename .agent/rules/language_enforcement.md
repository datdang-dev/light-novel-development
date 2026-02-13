---
trigger: model_decision
description: All output must be Vietnamese with specific exceptions for SFX and honorifics
priority: 1
---

# Language Enforcement

## OUTPUT LANGUAGE: VIETNAMESE

All prose, dialogue, thoughts, and narration MUST be in Vietnamese.

## Exceptions

| Element | Allowed Non-Vietnamese | Example |
|---------|----------------------|---------|
| SFX | Romanized Japanese | *guchu guchu*, *pan pan* |
| Honorifics | Romanized Japanese | -san, -sama, -chan, onii-chan |
| Character names | Original (romanized) | Reira Kurain, Kida |
| Moaning | Romanized patterns | "Ahh~", "Nnnn~", "Iku!" |

## BANNED in Output

| ❌ Banned | Why | ✅ Replace With |
|-----------|-----|----------------|
| Raw kanji/hiragana (ぐちゅ, パン) | Not romanized | guchu, pan |
| English prose sentences | Wrong language | Vietnamese equivalent |
| Vietnamese SFX (bì bạch, chát chát) | Must be JP romanized | pan pan, bachi bachi |
| Mixed EN-VI sentences | Inconsistent | Full Vietnamese |

## Validation

Before finalizing any output file, scan for:

1. Zero kanji/hiragana/katakana characters
2. Zero English prose paragraphs (English in metadata/frontmatter is OK)
3. All SFX are romanized Japanese
