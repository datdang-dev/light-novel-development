---
trigger: model_decision
description: Enforce 1:1 mapping between source pages and output files + forensic gate
priority: 1
---

# ONE PAGE = ONE FILE + FORENSIC GATE

## RULE 1: File Mapping

Every source page MUST produce exactly ONE output file at each pipeline stage.

| Stage | Pattern | Example |
|-------|---------|---------|
| Forensic | `{page}_forensics.md` | `003_forensics.md` |
| Dialogue | `{page}_dialogue.md` | `003_dialogue.md` |

**ILLEGAL filename patterns:** Any file containing a page range in forensic/dialogue stages:

- ❌ `003-004_forensics.md`
- ❌ `005-006_dialogue.md`

**ALLOWED multi-page output** (these stages are cross-page by design):

- ✅ `pages_{range}_entities.md`
- ✅ `pages_{range}_prose.md`
- ✅ `pages_{range}_audit.md`
- ✅ `active_character_context.md`

### Validation

Before completing any forensic/dialogue step:

```
output_file_count MUST == source_page_count
```

---

## RULE 2: Forensic Gate

Prose generation is **BLOCKED** until a per-page forensic report exists.

### Gate Check

Before writing prose for ANY page:

1. Verify `{output_folder}/_forensics/{page}_forensics.md` exists
2. If missing → **STOP** → delegate to panel-forensic first
3. Only after forensic exists → proceed

### Required Forensic Sections

Each forensic report MUST contain:

| Section | Required |
|---------|----------|
| Panel Layout | ✅ |
| Character ID | ✅ |
| ATOMIC Analysis | ✅ |
| Dialogue Extraction | ✅ |
| SFX Extraction | ✅ |
| R18 Tags | ✅ |

If any section missing → report is INVALID → re-run forensic.
