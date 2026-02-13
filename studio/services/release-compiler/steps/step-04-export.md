---
name: 'step-04-export'
description: 'Generate final output'
releaseOutput: '{output_folder}/_releases/{manga_name}/'
---

# Step 4: Export

## STEP GOAL:

Generate final reader-ready output file(s).

## MANDATORY SEQUENCE

### 1. Generate Output

Based on selected format:

**Markdown:**
```
{releaseOutput}/{manga_name}_release.md
```

**HTML:**
```
{releaseOutput}/{manga_name}_release.html
```

### 2. Workflow Completion

```
"✅ RELEASE COMPILER COMPLETE!

**Output:** {releaseOutput}

**Files:**
- {filename}.{format}

**Word count:** ~{count}
**Chapters:** {range}

**Ready for distribution!**

**WORKFLOW COMPLETE**"
```

---

## WORKFLOW END

Reader-ready release generated.
