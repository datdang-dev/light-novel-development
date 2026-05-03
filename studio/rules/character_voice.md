---
trigger: model_decision
description: Check character bible before writing dialogue to prevent voice drift
priority: 4
---

# Character Voice Consistency

## RULE 1: ADAPT, NOT TRANSLATE

Source manga dialogue is **REFERENCE MATERIAL**, not a translation source.

```text
❌ WRONG: Source says "SERIOUSLY! SO RUDE!" → Output: 「Nghiêm túc đó! Thô lỗ quá!!」
✅ RIGHT: Source says "SERIOUSLY! SO RUDE!" → Character is bratty princess, insecure about height
   → Output: 「Ngươi dám?! Reira-chan đứng ở đây mà mắt ngươi để ở đâu hả, đồ ngốc!」
```

### Process

1. Read source dialogue → extract **INTENT** (what does the character want to communicate?)
2. Load character profile → understand **PERSONALITY** (archetype, verbal tics, pronoun tier)
3. Write new Vietnamese dialogue that captures intent through personality lens
4. Source wording is DISCARDED — only the meaning survives

## RULE 2: Bible Check

Before writing dialogue for ANY character, CHECK `_bible/` or `_entities/`.

- Voice profile is LAW — a tsundere stays tsundere, timid stays timid
- Drift requires narrative justification (mindbreak, power reversal, etc.)
- Unjustified drift = invalid output → rewrite

## RULE 3: Vietnamese Pronoun System

Pronouns carry **relationship weight** in Vietnamese. They are a **narrative device**, not just grammar.

### Pronoun Gradient Template

Each character should have a defined pronoun gradient that maps to their emotional arc. Pronoun shifts ARE plot points.

**Example — Tsundere/Bratty archetype:**

| Tier | Self | Other | Trigger | Example |
| :--- | :--- | :--- | :--- | :--- |
| 1. Bratty Princess | ta / [Name]-chan | ngươi | Default, angry, showing off | 「Reira-chan đã nói rồi! Ngươi im đi, đồ ngốc!」 |
| 2. Professional Shield | tôi | anh / [Name]-san | Trying to regain composure | 「Tôi là chuyên viên. Đây là quy trình.」 |
| 3. Tsundere Deflection | "người ta" | — | Flustered but denying | 「Người ta đâu có thích! Chỉ là kiểm tra!」 |
| 4. The Crack 💥 | ta→e-em (stutter) | ngươi→anh | Losing control, pronoun breaks mid-sentence | 「Ta... hnn... e-em... em không chịu nổi...」 |
| 5. Soft Surrender | em | anh | Corrupted stage 1, yielding | 「Em dọn cho anh nha... Đ-Đừng hiểu nhầm!」 |
| 6. Full Submission | em / [Name]-chan | ngài | Mindbreak, heart eyes | 「Ngài... Reira-chan là của ngài...」 |

### Pronoun Rules

| Pronoun Set | Tone | Restriction |
| :--- | :--- | :--- |
| ta - ngươi | Haughty/princess | Bratty archetypes, self-important characters |
| [Name]-chan self-refer | Peak bratty, 3rd person | Childish + cute, Gap Moe trigger |
| tôi - anh | Formal/professional | Defense mechanism, temporary composure |
| "người ta" | Tsundere deflection | Flustered denial — "people don't like this!" |
| em - anh | Intimate/yielding | Post-corruption, soft surrender |
| em - ngài | Full submission | Mindbreak, worship mode |
| anh - em | Older male default | Standard male → younger female |
| cậu - tớ | Casual friends | Same-age peers |
| **mày - tao** | **HOSTILE** | **ONLY combat, genuine hatred, extreme violence** |

> [!CAUTION]
> **mày - tao** is NOT bratty/annoyed speech. It signals REAL hostility.
> A bratty girl annoyed at someone uses **ta/ngươi**, not mày/tao.
> Reserve mày-tao for scenes with genuine violence or hatred.

## RULE 4: Verbal Tics

Each character archetype has signature speech patterns:

### Tsundere/Bratty Tics

| Tic | Usage | Example |
| :--- | :--- | :--- |
| "Đồ ngốc!" | Baka equivalent — when flustered | 「Đồ ngốc! Reira-chan không có đỏ mặt!」 |
| "Hứ!" | Dismissive hmph | 「Hứ! Ta không cần ngươi khen.」 |
| 「...đó!」 / 「...đấy!」 | Bratty sentence ender | 「Ta giận lắm đó!!」 |
| 「N-Không phải!」 | Tsundere denial stutter | 「N-Không phải! Đây là quy trình!」 |
| [Name]-chan 3rd person | Self-refer when showing off or seeking praise | 「Reira-chan làm tốt lắm chứ...?」 |
| Size-compensating titles | BIG words for small body | 「TA, ĐẠI DIỆN CHÍNH THỨC CỦA SEED...!」 |

## RULE 5: Gap Moe Technique

The gap between WORDS and BODY is where Gap Moe lives:

1. **Tsundere denial DURING explicit acts** — still denying while drooling
2. **Pronoun stutter at transition points** — old pronoun cracking into new one
3. **Professional framing of lewd moments** — 「Mẫu đạt tiêu chuẩn!」 while heart eyes active
4. **Body betrays words** — camera shows physical reactions contradicting verbal denial

## Quick Checks

| Check | Pass Criteria |
| :--- | :--- |
| Dialogue ≠ translation? | Vietnamese reimagined, not word-for-word |
| Pronoun tier correct for scene position? | Maps to character's emotional arc |
| Verbal tics present? | At least 2-3 signature tics per scene |
| Gap Moe visible? | Words say one thing, body say another |
| Pronoun shift is a PLOT POINT? | Reader can track the degradation |
