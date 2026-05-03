# ✍️ Style Enforcer Module

> **Purpose**: Enforce writing style rules và archetype patterns during prose generation.

---

## Knowledge References

| File | Location | Purpose |
|------|----------|---------|
| R18 LN Culture Guide | `studio/knowledge/style-guides/R18_LIGHTNOVEL_CULTURE_GUIDE.md` | Genre conventions |
| Mesugaki Dialogue Style | `studio/knowledge/style-guides/MESUGAKI_DIALOGUE_STYLE.md` | Bratty patterns |
| Mesugaki Research | `studio/knowledge/fetish-db/mesugaki_research.md` | Deep patterns |
| Mesugaki Variations | `studio/knowledge/fetish-db/mesugaki_variations.md` | Sub-types |
| Gyaru Research | `studio/knowledge/fetish-db/gyaru_research.md` | Gyaru speech |
| MILF Research | `studio/knowledge/fetish-db/milf_research.md` | Mature patterns |

---

## Style Rules

### ⚠️ Critical Format Rules

> [!IMPORTANT]
> **Light Novel prose MUST NOT contain Kanji.**
>
> - ❌ NO Kanji in prose, dialogue, or SFX
> - ✅ Use romanized Japanese for SFX only (guchu guchu, an~♡)
> - ✅ Use Vietnamese for all prose and dialogue

### R18 Light Novel Conventions

| Rule | Description | Example |
|------|-------------|---------|
| Non-judgmental narrator | No moral commentary | ❌ "dơ bẩn" ✅ "đầy tinh dịch" |
| Sensory-first | Show through senses | ❌ "felt good" ✅ "warm, wet, pulsing" |
| Third-person camera | Observer perspective | Describe as if filming |
| Extended aftermath | Don't cut away | Show residue, exhaustion |
| Power explicit | State dynamics | Who controls, who submits |

### Banned Words List

```
JUDGMENTAL TERMS (always replace):
❌ hôi thối → mùi nồng
❌ dơ bẩn → nhớp nháp
❌ ghê tởm → (omit or use neutral)
❌ đáng xấu hổ → (omit)
❌ tội lỗi → (omit)
❌ ghê → cảm giác lạ
```

---

## Archetype Enforcement

### Mesugaki (Bratty Girl)

**Speech Patterns:**
```
Prefixes: ねぇねぇ, あのさぁ, ちょっとぉ
Suffixes: ~なんだけど?, ~ってば!, ~でしょ♡
Attitude: Condescending, teasing, superior
```

**Vietnamese Adaptation:**
```
- "Ơ kìa~" / "Này này~"
- "...đấy thôi♡" / "...mà, sao hả?"
- Giggling: "Fufufu~" / "Ahahaha~♡"
```

**Escalation (if being dominated):**
```
Phase 1: "Làm được không đấy? 🙄"
Phase 2: "Ư-ừm... chờ đã..."
Phase 3: "Đ-đừng... n-nhìn như vậy..."
Phase 4: "Dạ... xin lỗi ạ... 🥺"
```

### Gyaru (Gal)

**Speech Patterns:**
```
- Heavy slang: まじやば, ちょーうけるw
- Elongated: えーーー, うそーーー
- Casual rudeness: お前, てめー
```

**Key Traits:**
```
- Shameless about body
- Uses appearance as weapon
- Group dynamics important
```

### MILF (Mature Woman)

**Speech Patterns:**
```
- Polite forms: です/ます even in arousal
- Terms: あなた, 旦那さん
- Self-reference: おばさん, 私のような歳で
```

**Key Dynamics:**
```
- Experience vs youth
- Guilt about enjoying
- "This is wrong but..."
```

---

## Capabilities

### 1. Style Validation

```
Input: [prose text] + archetype:mesugaki
Output:
  ✅ Speech pattern match: 8/10
  ⚠️ Missing condescending suffix at line 23
  ❌ Out-of-character line at 45: "Xin lỗi" (too polite for Phase 1)
```

### 2. Banned Words Scan

```
Input: [prose text]
Output:
  Line 12: "dơ bẩn" → Replace with "nhớp nháp"
  Line 67: "hôi thối" → Replace with "mùi nồng đặc trưng"
  Line 89: "ghê tởm" → DELETE or rephrase
```

### 3. Dialogue Pattern Check

```
Input: [dialogue] + archetype:gyaru
Output:
  Missing elements:
  - No えー elongation
  - No casual insults
  - Too formal for gyaru
  
  Suggestions:
  - Add "まじで?" / "ありえなくない?"
  - Use bolder language
```

### 4. Archetype Consistency

```
Input: character_bible + [prose]
Output:
  Character: Mimi (mesugaki)
  Consistency Score: 85%
  
  Inconsistencies:
  - Line 34: Uses polite form (should be condescending)
  - Line 78: Apologizes sincerely (breaks bratty persona)
```

---

## Integration Points

- **dialogue-crafter**: Apply archetype patterns during generation
- **lewd-writer**: Validate prose against style guide
- **gooner-editor**: Include style check in QA pass

---

## Usage Examples

### Full Style Check
```
/style-check [file.md] archetype:mesugaki
→ Complete validation report
→ Line-by-line issues
→ Archetype consistency score
```

### Banned Words Only
```
/style-banned [file.md]
→ Quick scan for judgmental terms
→ Replacement suggestions
```

### Archetype Reference
```
/style-ref gyaru
→ Speech patterns
→ Example dialogues
→ Do's and Don'ts
```

---

## Technical Details

### Source Files
- `{{project_root}}/studio/knowledge/style-guides/R18_LIGHTNOVEL_CULTURE_GUIDE.md`
- `{{project_root}}/studio/knowledge/style-guides/MESUGAKI_DIALOGUE_STYLE.md`
- `{{project_root}}/studio/knowledge/fetish-db/gyaru_research.md`
- `{{project_root}}/studio/knowledge/fetish-db/milf_research.md`

### Pattern Matching
Uses regex + keyword lists from style guides

---

_Module for LND Studio | Consistency enforcement for dialogue-crafter, lewd-writer_
