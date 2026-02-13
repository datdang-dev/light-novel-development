---
name: 'step-01-input'
description: 'Select chapters for release'
nextStepFile: './step-02-clean.md'
---

# Step 1: Input

## STEP GOAL:

Select source chapters for release compilation.

## MANDATORY SEQUENCE

### 1. Request Input

```
"**📦 RELEASE COMPILER**

Cho mình:
1. **Project:** 
2. **Chapters:** (e.g., '1-3' hoặc 'all')
3. **Output format:** md / html / txt"
```

### 2. Locate Chapters

Find compiled chapters in `{output_folder}/_chapters/{manga_name}/`

### 3. Present MENU

```
"✅ Chapters found!

**Chapters:** {list}
**Total words:** ~{count}

**Chọn:** [C] Continue to Clean"
```

---
