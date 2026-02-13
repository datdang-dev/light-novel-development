---
name: step-01-gather-prose
description: Collect all page prose files
nextStepFile: ./step-02-order-review.md
projectRoot: {project-root}
---

# Step 1: Gather Prose 📚

## STEP GOAL

Collect all adapted prose files for the target chapter.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Request Chapter Info

Ask the user for the Project, Chapter Number, and Page Range.

**Format:**
`Project: [Manga Name] | Chapter: [01] | Pages: [001-020]`

### 2. Locate Prose Files

Scan `{output_folder}/_prose/{manga_name}/chapter_{ch}/` (or equivalent structure).

### 3. Verification Table

Generate a status table:

```markdown
## Prose Files Found

| Page | File | Audit Score | Status |
|------|------|-------------|--------|
| 1 | page_001.md | 87 | ✅ |
| 2 | page_002.md | 85 | ✅ |
| ... | ... | ... | ... |
```

### 4. Present MENU OPTIONS

```
"✅ Prose gathered!

**Pages found:** {count}
**All passed audit:** {yes/no}

**Tiếp theo:** Review Order & Continuity

**Chọn:** [C] Continue to Order Review"
```

#### Menu Handling Logic

- IF C: Load `{nextStepFile}`
- IF other: Redisplay menu
