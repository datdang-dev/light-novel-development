---
name: sfx-lookup
description: "SFX lookup and suggestion module — provides romanized Japanese SFX categorized by type, intensity, and scene context for R18 prose generation."
---

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

## On Activation

1. Load SFX dictionary from `{project-root}/studio/knowledge/sfx/japanese_sfx_dictionary.md`
2. Load quick reference from `{project-root}/studio/knowledge/sfx/r18_sfx_quickref.yaml`
3. Optionally load moaning research from `{project-root}/studio/knowledge/sfx/moaning_sfx_research.md`
4. Ready to serve lookups by category, intensity, or scene context

## Knowledge References

| File | Location | Entries |
|------|----------|---------|
| Japanese SFX Dictionary | `studio/knowledge/sfx/japanese_sfx_dictionary.md` | 3000+ |
| R18 SFX Quick Reference | `studio/knowledge/sfx/r18_sfx_quickref.yaml` | 100+ |
| Moaning SFX Research | `studio/knowledge/sfx/moaning_sfx_research.md` | Detailed |

---

## Capabilities

### 1. Category Lookup

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

## Quick Reference

| Intent | Trigger | Action |
|--------|---------|--------|
| **Quick lookup** | `/sfx {category} {intensity}` | Return matching SFX |
| **Scene-based** | `/sfx scene:{type} phase:{phase}` | Context-aware suggestions |
| **Progression** | `/sfx progression:{type}` | Full escalation sequence |
