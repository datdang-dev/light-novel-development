---
trigger: model_decision
description: Enforce light-novel-prose.md template structure for all prose output
priority: 3
---

# Prose Structure

## TEMPLATE ENFORCEMENT

All prose output MUST follow `studio/_templates/light-novel-prose.md`.

## Required Structure

```markdown
# 📖 [Scene Title in Vietnamese]

> **📍 Location:** [Location]
> **⏰ Time:** [Time]
> **👤 POV:** [Camera/Character]

---

### [Section Title]

[Prose content]

---

## Continuity State
[State table at end of file]
```

## Section Rules

1. **Scene title** — Vietnamese, evocative, not a page number
2. **Metadata block** — Location, Time, POV — always present
3. **Section headers** — Vietnamese titles per narrative beat
4. **Continuity table** — MUST be the final element in every prose file

## Anti-Patterns

| ❌ Wrong | ✅ Right |
|----------|---------|
| `## Page 003` | `### Mùi Hương Cấm Kỵ` |
| No metadata block | Full 📍⏰👤 block |
| Missing continuity table | State table at EOF |
| Numbered sections (I, II, III) without titles | Vietnamese titles required |
