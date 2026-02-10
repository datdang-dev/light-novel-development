---
name: 'step-02-clean'
description: 'Remove development markup'
nextStepFile: './step-03-format.md'
---

# Step 2: Clean

## STEP GOAL:

Strip development-only content from chapters.

## REMOVE PATTERNS

```regex
# YAML frontmatter
/^---[\s\S]*?---\n/

# Developer comments
/<!--.*?-->/g
/\[DEV:.*?\]/g

# Panel references
/\(Panel \d+\)/g
/\[P\d+\]/g

# Audit scores
/Audit Score:.*$/gm
```

## MANDATORY SEQUENCE

### 1. Strip Dev Content

Remove all development markup.

### 2. Verify Content

Ensure no dev artifacts remain.

### 3. Present MENU

```
"✅ Dev content removed!

**Items cleaned:** {count}

**Chọn:** [C] Continue to Format"
```

---
