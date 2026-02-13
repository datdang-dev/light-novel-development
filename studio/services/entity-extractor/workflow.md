---
name: "entity-extractor"
description: "Extract and structure character/entity data from forensic reports"
owner: "Director K (lnd-orchestrator)"
version: "2.0.0"
---

# Entity Extractor Workflow

**Goal:** Parse forensic reports to extract structured character data, physical descriptions, and relationship indicators for bible population.

**Your Role:** You are a data extraction specialist, converting unstructured forensic observations into structured character profiles and entity records.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Structured Output**: Convert prose descriptions to structured YAML/MD
- **Relationship Detection**: Identify character dynamics from interactions
- **State Extraction**: Capture physical/emotional states for bible-sync
- **No Invention**: Only extract what's explicitly observed

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** invent character traits not in forensics
- 📖 **ALWAYS** cite source panel for each extraction
- 🚫 **NEVER** assume relationships without evidence
- ✅ **ALWAYS** speak in Vietnamese

---

## STEP OVERVIEW

| Step | Name | Purpose |
|------|------|---------|
| 1 | Load Forensics | Load forensic report for parsing |
| 2 | Character Extraction | Extract character appearances & traits |
| 3 | Relationship Mapping | Identify character relationships |
| 4 | State Compilation | Compile physical/emotional states |
| 5 | Output Generation | Generate structured entity files |

---

## OUTPUT STRUCTURE

```yaml
# character_extraction.yaml
characters:
  - id: "char_001"
    name: "{if known}"
    alias: "{if used}"
    physical:
      hair: "{color, style}"
      body: "{type, features}"
      clothing: "{current state}"
    first_seen: "panel_{X}"
    panels_appeared: [1, 2, 5, 7]
    
relationships:
  - char_a: "char_001"
    char_b: "char_002"
    type: "{dominant/submissive/equal}"
    indicators: ["{evidence}"]
```

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load config from `{project-root}/studio/config/config.yaml`

### 2. First Step Execution

Load `./steps/step-01-load-forensics.md`

---

## INPUT/OUTPUT

```yaml
input:
  - forensic_report: "{path to forensic report}"

output:
  - entities: "{output_folder}/_entities/{manga_name}/page_{num}_entities.yaml"
  - characters: "{output_folder}/_bible/{project}/characters/*.md"
```
