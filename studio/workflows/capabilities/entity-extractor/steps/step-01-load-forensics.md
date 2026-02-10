---
name: 'step-01-load-forensics'
description: 'Load forensic report for entity parsing'

thisStepFile: './step-01-load-forensics.md'
nextStepFile: './step-02-character-extraction.md'
---

# Step 1: Load Forensics

## STEP GOAL:

Load and validate the forensic report that will be parsed for entity extraction.

## MANDATORY SEQUENCE

### 1. Request Forensic Report

```
"**ENTITY EXTRACTOR**

Cần forensic report để extract entities.

Provide: Path to forensic report file"
```

### 2. Load and Validate

```markdown
## Forensic Loading

**Report:** {path}
**Panels:** {count}
**Characters detected:** {preliminary count}

### Validation
- [ ] Report is complete
- [ ] All panels documented
- [ ] R18 content tagged
```

### 3. Initialize Extraction State

```yaml
extraction_state:
  forensic_path: "{path}"
  panels_to_process: [{list}]
  characters_found: []
  relationships_found: []
```

### 4. Present MENU

```
"✅ Forensic report loaded!

**Panels:** {count}
**Ready for extraction**

**Chọn:** [C] Continue to Character Extraction"
```

---
