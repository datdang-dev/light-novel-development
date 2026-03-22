---
name: style-enforcer
description: "Writing style validation module — enforces R18 light novel conventions, character archetype speech patterns, and banned word scanning."
---

# ✍️ Style Enforcer Module

> **Purpose**: Enforce writing style rules và archetype patterns during prose generation.

---

## On Activation

1. Load R18 culture guide from `{project-root}/studio/knowledge/style-guides/R18_LIGHTNOVEL_CULTURE_GUIDE.md`
2. Load archetype-specific guides (Mesugaki, Gyaru, MILF, etc.)
3. Load banned words list
4. Ready to validate prose against style rules and archetype consistency

## Knowledge References

| File | Location | Purpose |
|------|----------|---------|
| R18 LN Culture Guide | `studio/knowledge/style-guides/R18_LIGHTNOVEL_CULTURE_GUIDE.md` | Genre conventions |
| Mesugaki Dialogue Style | `studio/knowledge/style-guides/MESUGAKI_DIALOGUE_STYLE.md` | Bratty patterns |
| Fetish Research Files | `studio/knowledge/fetish-db/` | Archetype deep-dives |

---

## Style Rules

### Critical Format Rules

- ❌ NO Kanji in prose, dialogue, or SFX
- ✅ Romanized Japanese for SFX only
- ✅ Vietnamese for all prose and dialogue

### R18 Light Novel Conventions

- Non-judgmental narrator (no moral commentary)
- Sensory-first (show through senses)
- Third-person camera (observer perspective)
- Extended aftermath (don't cut away)
- Power explicit (state dynamics)

### Banned Words

`hôi thối`, `dơ bẩn`, `ghê tởm`, `đáng xấu hổ`, `tội lỗi`, `ghê`

---

## Archetype Enforcement

Supports validation for: **Mesugaki**, **Gyaru**, **MILF** — with speech pattern templates, Vietnamese adaptations, and escalation phases per archetype.

## Capabilities

1. **Style Validation** — Check prose against archetype patterns with consistency scoring
2. **Banned Words Scan** — Line-by-line scan with replacement suggestions
3. **Dialogue Pattern Check** — Verify character dialogue matches archetype
4. **Archetype Consistency** — Score character behavior vs bible definition

## Integration Points

- **dialogue-crafter**: Apply archetype patterns during generation
- **lewd-writer**: Validate prose against style guide
- **gooner-editor**: Include style check in QA pass

## Quick Reference

| Intent | Trigger | Action |
|--------|---------|--------|
| **Full check** | `/style-check {file} archetype:{name}` | Complete validation report |
| **Banned words** | `/style-banned {file}` | Quick judgmental term scan |
| **Archetype ref** | `/style-ref {archetype}` | Speech patterns + examples |
