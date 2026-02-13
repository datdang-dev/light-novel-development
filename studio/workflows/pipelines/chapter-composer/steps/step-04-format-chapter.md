---
name: step-04-format-chapter
description: Apply chapter-level formatting
nextStepFile: ./step-05-final-polish.md
---

# Step 4: Chapter Assembly & Formatting 📄

## STEP GOAL

Compile individual pages into a single cohesive document with chapter structure.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Construct Metadata

Identify or Generate:

- **Title:** From scene content or user input.
- **Chapter Number:** From step 1.
- **Word Count:** Total sum.

### 2. Apply Template

Combine pages and transitions in this structure:

```markdown
---
chapter: {num}
title: "{title}"
pages: [{range}]
word_count: {new_count}
---

# Chương {N}: {Title}

{opening_paragraph}

---

{page_1_content}

{transition_1}

{page_2_content}

...

---

{closing_scene}
```

### 3. Present MENU OPTIONS

```
"✅ Chapter formatted!

**Title:** Chương {N}: {Title}
**Word count:** ~{count}

**Tiếp theo:** Final Polish & Output

**Chọn:** [C] Continue to Final Polish"
```

#### Menu Handling Logic

- IF C: Load `{nextStepFile}`
- IF other: Redisplay menu
