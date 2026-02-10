---
name: 'step-01-gather-prose'
description: 'Collect all page prose files'
nextStepFile: './step-02-order-review.md'
---

# Step 1: Gather Prose

## STEP GOAL:

Collect all adapted prose files for the chapter.

## MANDATORY SEQUENCE

### 1. Request Chapter Info

```
"**📚 CHAPTER COMPOSER**

Cho mình:
1. **Project name:** 
2. **Chapter number:**
3. **Page range:** (hoặc 'all')"
```

### 2. Locate Prose Files

Search in `{output_folder}/_prose/{manga_name}/chapter_{ch}/`

### 3. List Found Files

```markdown
## Prose Files Found

| Page | File | Audit Score | Status |
|------|------|-------------|--------|
| 1 | page_001.md | 87 | ✅ |
| 2 | page_002.md | 85 | ✅ |
| ... | ... | ... | ... |
```

### 4. Present MENU

```
"✅ Prose gathered!

**Pages found:** {count}
**All passed audit:** {yes/no}

**Chọn:** [C] Continue to Order Review"
```

---
