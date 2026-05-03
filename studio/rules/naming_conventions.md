---
trigger: model_decision
description: Standardize output file and folder naming conventions
priority: 7
---

# Naming Conventions

## Folder Names

| Type | Convention | Example |
|------|-----------|---------|
| Manga output | kebab-case, short | `semen-collector-4` |
| Pipeline subdirs | underscore prefix | `_forensics`, `_prose`, `_dialogue` |

## File Names

| Stage | Pattern | Example |
|-------|---------|---------|
| Forensic | `{page}_forensics.md` | `003_forensics.md` |
| Dialogue (per-page) | `{page}_dialogue.md` | `003_dialogue.md` |
| Dialogue (batch) | `pages_{range}_dialogue.md` | `pages_001-007_dialogue.md` |
| Entities | `pages_{range}_entities.md` | `pages_001-007_entities.md` |
| Prose | `pages_{range}_prose.md` | `pages_001-007_prose.md` |
| Audit | `pages_{range}_audit.md` | `pages_001-007_audit.md` |
| Bible | `active_character_context.md` | — |

## Page Numbers

- Always 3 digits, zero-padded: `001`, `012`, `100`
- Range separator: hyphen (`001-007`), never tilde or "to"
