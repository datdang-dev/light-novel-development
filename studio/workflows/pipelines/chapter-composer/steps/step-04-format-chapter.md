---
name: 'step-04-format-chapter'
description: 'Apply chapter formatting'
nextStepFile: './step-05-final-polish.md'
---

# Step 4: Format Chapter

## STEP GOAL:

Apply consistent chapter formatting.

## CHAPTER TEMPLATE

```markdown
# Chương {N}: {Title}

{opening paragraph}

---

{page 1 prose}

{transition}

{page 2 prose}

...

---

{chapter end/cliffhanger}
```

## MANDATORY SEQUENCE

### 1. Generate Title

Create evocative chapter title from content.

### 2. Add Chapter Header

```markdown
---
chapter: {num}
title: "{title}"
pages: [{range}]
word_count: {count}
---
```

### 3. Assemble Content

Combine all prose with transitions.

### 4. Present MENU

```
"✅ Chapter formatted!

**Title:** Chương {N}: {Title}
**Word count:** ~{count}

**Chọn:** [C] Continue to Polish"
```

---
