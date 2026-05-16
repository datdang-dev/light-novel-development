---
trigger: model_decision
description: Formatting and pattern rules for R18 dialogue
---

# Dialogue Format Rules

## FORMAT (STRICT LIGHT NOVEL STANDARD)

```
Dialogue: Character_Name: 「Content」
Thought: (Internal thought content)
Narrative/Action: *Descriptive action or sound effect*

Example:
Alice: 「Onii-chan~? Anh đến muộn quá đó~ Ehehe~」
(Hắn ta nhìn có vẻ ngon lành quá...)
*Tiếng nịt đùi thắt chặt vào da thịt vang lên sột soạt.*
```

---

## 🚨 VIETNAMESE PRONOUN SYSTEM (MANDATORY — RETRO FIX 2026-04-25)

> [!CAUTION]
> Sai xưng hô = phá vỡ power dynamic = PO reject. Đây là bảng tra BẮTBUỘC.

### Pronoun Lookup Table

| Relationship | Speaker→Listener | Xưng Hô | Tone | Ví Dụ |
|---|---|---|---|---|
| **Senpai → Kouhai** | Đàn anh → Đàn em | **anh/em** | Authority, dominance mượt mà | 「Em muốn cặc anh đến thế á?」 |
| **Senpai → Kouhai (group)** | Đàn anh → Nhiều đàn em | **anh/các em** | Commanding | 「Hôm nay anh sẽ vắt kiệt sức các em nhé.」 |
| **Teacher → Student** | Thầy → Trò | **thầy/em** hoặc **sensei/em** | Authority + grooming | 「Em ngoan lắm, thầy thưởng cho em nhé.」 |
| **Boss → Employee** | Sếp → Nhân viên | **anh/em** hoặc **tôi/cô** | Corporate power | 「Anh cần em OT tối nay.」 |
| **Older man → Young girl** | Oji-san → Gái trẻ | **chú/cháu** hoặc **oji-san/em** | Age gap, grooming | 「Cháu giỏi lắm~ Chú thích cháu quá~」 |
| **Equal rivals** | Ngang hàng thù hằn | **mày/tao** | Hostile, violent | 「Tao sẽ phá nát mày.」 |
| **True degradation** | Đã break xong | **mày/tao** hoặc **con/tao** | Post-mindbreak, vật hoá | 「Con đĩ. Mày thích thế này hả?」 |
| **Lovers (sweet)** | Người yêu | **anh/em** hoặc **cậu/tớ** | Romantic, intimate | 「Em tin cậu mà, Kazuki.」 |
| **Boyfriend → Girlfriend** | BF→GF (NTR context) | **cậu/tớ** hoặc **anh/em** | Innocent, pure | 「Tớ sẽ cố gắng, Haruka.」 |
| **Mother → Son** | Mẹ → Con | **mẹ/con** | Incest/Milf context | 「Con~ Mẹ thua rồi~♡♡」 |

### Decision Rules

```text
RULE 1: Xưng hô phản ánh POWER DYNAMIC, không phải HOSTILITY.
  → Cưỡng ép ≠ Thù hằn
  → Senpai ép em gái bú cặc vẫn gọi "em/anh" (authority)
  → CHỈ chuyển sang "mày/tao" khi nhân vật ĐÃ BỊ BREAK hoặc bị VẬT HOÁ

RULE 2: Xưng hô CÓ THỂ THAY ĐỔI theo progression:
  → Giai đoạn đầu (coercion): "em/anh" ← tôn trọng giả tạo
  → Giai đoạn giữa (escalation): "em/anh" hoặc "cưng/anh" ← thân mật cưỡng ép
  → Giai đoạn cuối (mindbreak): "mày/tao" hoặc "con/ông" ← vật hoá hoàn toàn

RULE 3: CONTEXT DECIDES, NOT CONTENT.
  → Dù nội dung tục tĩu đến đâu, xưng hô vẫn theo relationship.
  → "Em muốn cặc anh?" (authority coercion) ≠ "Mày muốn cặc tao?" (hostile)
```

---

## MOANING PATTERNS

### By Intensity Level

| Level | Pattern | Examples |
|-------|---------|----------|
| Light | Soft gasps | "Ah...", "Nn...", "Hya!" |
| Medium | Rising | "Ahh~ Ahh~", "Kimochi...", "Nnn..." |
| High | Uncontrolled | "AHHH!", "Dame! Dame!" |
| Climax | Breaking | "IIIKUUUUU!!♡", "AHIII~!♡♡" |

### Heart Symbols
Use ♡ at high arousal moments:
- 1x ♡ = building pleasure
- 2x ♡♡ = peak/climax
- 3x ♡♡♡ = mindbreak

---

## ARCHETYPE DIALOGUE

### Mesugaki (Bratty)
```
Teasing: "Hee~ Onii-chan không chịu nổi à? Yếu quá~"
Broken: "H-Hả?! Sao... sao lại...♡"
Climax: "CHẬM LẠI! EM... EM KHÔNG... AHIII~!♡♡"
```

### Gyaru (Flashy)
```
Casual: "Ê~ Cứ thoải mái đi~"
Pleasure: "Ugh~ Oji-san giỏi thiệt ha~♡"
Climax: "Cho em thêm đi oji-san!♡ Đụ em mạnh lên Oji-san!♡♡"
```

### Kuudere (Cold)
```
Normal: "...Được."
Aroused: "...Tốt." *hơi thở nặng*
Climax: "...!" *câm lặng, cơ thể co giật*
```

### Milf (Mature)
```
Gentle: "Ara ara~ Con trai ngoan quá~"
Aroused: "Mmm~ Mẹ thích thế này~♡"
Climax: "CON~! MẸ... MẸ THUA RỒI~!♡♡"
```

---

## DEGRADING LINES

### From Dominant
```
"Con đĩ. Mày thích thế này hả?"
"Nhìn mày đi. Ướt nhẹp rồi."
"Lồn mày đang kẹp chặt cặc tao kìa."
```

### From Submissive (in denial)
```
"Không... đừng nói thế..."
"Em... em không thích đâu..." *nhưng không phản kháng*
```

---

## STACCATO RHYTHM (climax moments)

```markdown
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

Short. Punchy. Impact.