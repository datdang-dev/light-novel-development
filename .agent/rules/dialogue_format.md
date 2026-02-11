---
trigger: model_decision
description: Single source of truth for dialogue, thought, narrative, and SFX formatting
priority: 2
---

# Dialogue Format Rules

## LANGUAGE RULE (SINGLE SOURCE OF TRUTH)

| Element | Language | Example |
|---------|----------|---------|
| Prose/Narrative | Vietnamese | *Cô nàng ưỡn người...* |
| Dialogue | Vietnamese + occasional honorifics | 「Onii-chan~? Anh đến muộn quá đó~」 |
| Thoughts | Vietnamese | (Hắn ta nhìn có vẻ ngon lành quá...) |
| **SFX** | **Romanized Japanese ONLY** | guchu guchu, pan pan, zuchu~ |

> **CRITICAL**: SFX is always romanized Japanese. Never Vietnamese (bì bạch), never Kanji (ぐちゅ).

---

## FORMAT MARKERS

```text
Dialogue:   Character_Name: 「Content」
Thought:    (Internal thought content)
Narrative:  *Descriptive action*
SFX:        *Guchu guchu. Pan pan.*
```

### Complete Example

```text
Alice: 「Onii-chan~? Anh đến muộn quá đó~ Ehehe~」

(Hắn ta nhìn có vẻ ngon lành quá...)

*Guchu guchu. Tiếng nịt đùi thắt chặt vào da thịt vang lên.*
```

---

## MOANING PATTERNS

| Intensity | Pattern | Examples |
|-----------|---------|----------|
| Light | Soft gasps | "Ah...", "Nn...", "Hya!" |
| Medium | Rising | "Ahh~ Ahh~", "Kimochi~", "Nnn..." |
| High | Uncontrolled | "AHHH!", "Dame! Dame!" |
| Climax | Breaking | "IIIKUUUUU!!♡", "AHIII~!♡♡" |

### Heart Symbol Usage

- 1× ♡ = Building pleasure
- 2× ♡♡ = Peak/climax
- 3× ♡♡♡ = Mindbreak/ahegao

---

## ARCHETYPE QUICK REFERENCE

| Archetype | Normal | Climax |
|-----------|--------|--------|
| Mesugaki | "Hee~ Onii-chan yếu quá~" | "H-Hả?! AHIII~!♡♡" |
| Gyaru | "Ê~ Cứ thoải mái đi~" | "Đụ em mạnh lên Oji-san!♡♡" |
| Kuudere | "...Được." | "...!" *câm lặng, co giật* |
| Milf | "Ara ara~ Con trai ngoan~" | "MẸ... MẸ THUA RỒI~!♡♡" |

---

## DEGRADING DIALOGUE

### From Dominant

```text
"Con đĩ. Mày thích thế này hả?"
"Nhìn mày đi. Ướt nhẹp rồi."
```

### From Submissive (denial)

```text
"Không... đừng nói thế..."
"Em... em không thích đâu..." *nhưng không phản kháng*
```

---

## STACCATO RHYTHM (Climax Moments)

```text
❌ WRONG: "Hắn bắn ra nhiều và sâu."

✅ RIGHT:
*Sâu.*
*Sâu hơn.*
*NÓNG.*
*Đợt một—*
*Đợt hai—*
*Đầy.*
*Tràn.*
```

---

## SFX QUICK REFERENCE

| Action | Romanized SFX |
|--------|---------------|
| Penetration | guchu guchu, nuchu, zuchu~ |
| Oral | juru juru, gokkun, rero rero |
| Impact | pan pan!, pecchi pecchi |
| Cum | byuru, doku doku, pyu pyu |

**Full dictionary**: `{project-root}/studio/modules/sfx-lookup.md`
