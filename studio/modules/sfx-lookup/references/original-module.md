# 🔊 SFX Lookup Module

> **Purpose**: Tra cứu và gợi ý SFX phù hợp cho scenes.

---

## ⚠️ SFX Format Rules

> [!IMPORTANT]
> **SFX MUST be in ROMANIZED JAPANESE only.**
>
> - ❌ NO Vietnamese SFX (không dùng: nhẹp nhẹp, bì bạch)
> - ❌ NO Kanji (không dùng: 喘ぎ声, 濡れ音)
> - ✅ ONLY Romanized: guchu guchu, pachi pachi, nn~♡

---

## Knowledge References

| File | Location | Entries |
|------|----------|---------|
| Japanese SFX Dictionary | `studio/knowledge/glossaries/japanese_sfx_dictionary.md` | 3000+ |
| R18 SFX Quick Reference | `studio/knowledge/glossaries/r18_sfx_quickref.yaml` | 100+ |
| Moaning SFX Research | `studio/knowledge/fetish-db/moaning_sfx_research.md` | Detailed |

---

## Capabilities

### 1. Category Lookup

Find SFX by type (ALL examples in romanized form):

| Category | Romanized Examples | Use Case |
|----------|-------------------|----------|
| `wet` | guchu guchu, bicha bicha, nucha nucha | Penetration, oral |
| `impact` | pan pan, pashi, bachi bachi | Thrusting, slapping |
| `moaning` | an~♡, haa haa, nn... | Pleasure expressions |
| `slurping` | juru juru, rero rero, chu chu | Oral, licking |
| `breathing` | haa haa, zee zee, ha... ha... | Exhaustion, arousal |

### 2. Intensity Levels

| Level | Description | Romanized Example |
|-------|-------------|-------------------|
| 1-Soft | Gentle, teasing | chu, n... |
| 2-Medium | Building | an~♡, guchu |
| 3-Intense | Peak action | aaaa~♡♡, bicha bicha |
| 4-Extreme | Climax/aftermath | ikuuu~!, dopyu dopyu |

### 3. Context-Aware Suggestions

```
Input:  Scene type = "paizuri"
Output:
  - Primary: munyu munyu, nuchu
  - Secondary: haa haa, n~
  - Impact: pafu pafu
```

```
Input:  Scene type = "blowjob" phase = "climax"
Output:
  - Primary: goku, ngu~, gokkun
  - Secondary: nn~♡, juru~
```

### 4. Moaning Progression

```
Level 1: n...
Level 2: an~♡
Level 3: aaaa~♡♡
Level 4: ikuuu~♡♡♡
```

---

## Integration Points

- **dialogue-crafter**: Auto-suggest SFX during dialogue generation
- **lewd-writer**: Inject SFX into prose at appropriate moments
- **gooner-editor**: Validate SFX density meets audit requirements

---

## Usage Examples

### Quick Lookup

```
/sfx wet intense
→ gucho gucho, bicha bicha, jupu jupu
```

### Scene-Based Suggestion

```
/sfx scene:blowjob phase:climax
→ goku~, ngu~, gokkun
```

### Progression Pattern

```
/sfx progression:moaning
→ Level 1: n... → Level 2: an~♡ → Level 3: aaaa~♡♡ → Level 4: ikuuu~♡♡♡
```

---

## Technical Details

### Source Files (Absolute Paths)

- `{project-root}/studio/knowledge/glossaries/japanese_sfx_dictionary.md`
- `{project-root}/studio/knowledge/glossaries/r18_sfx_quickref.yaml`

### Data Format (YAML Quick Ref)

```yaml
wet_sounds:
  - romanized: guchu guchu
    intensity: 3
    context: [penetration, fingering]
```

---

_Module for LND Studio | Integrates with dialogue-crafter, lewd-writer_
