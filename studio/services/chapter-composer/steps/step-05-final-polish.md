---
name: step-05-final-polish
description: Review and output final chapter file
chapterOutput: '{output_folder}/_chapters/{manga_name}/chapter_{ch}.md'
---

# Step 5: Final Review & Output ✨

## STEP GOAL

Perform final quality audit and save the compiled chapter.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Pre-Flight Checklist

- [ ] Continuity verified (Step 2)
- [ ] Transitions smooth (Step 3)
- [ ] Formatting consistent (Step 4)
- [ ] No placeholder text found

### 2. Generate Output File

Save the compiled content to: `{chapterOutput}`

### 3. Present MENU OPTIONS

```
"✅ CHAPTER COMPOSER COMPLETE!

**Output File:** {chapterOutput}
**Title:** {title}
**Words:** ~{count}

**Tiếp theo:** Distribution / Release

**Chọn:** [E] Exit Workflow"
```

#### Menu Handling Logic

- IF [E]:
  - Notify User: "🎉 Chapter {ch} Compiled Successfully!"
  - BREAK CHARACTER (Return to Default Handler).
