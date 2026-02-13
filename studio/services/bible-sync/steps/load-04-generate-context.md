---
name: 'load-04-generate-context'
description: 'Generate context document for prose-adapter'

# Path Definitions
workflow_path: '{project-root}/studio/services/bible-sync'
thisStepFile: './load-04-generate-context.md'
contextOutput: '{output_folder}/_bible/{project_name}/prose-context.md'
---

# LOAD Step 4: Generate Context

## STEP GOAL:

Compile loaded information into a context document for prose-adapter consumption.

## MANDATORY SEQUENCE

### 1. Generate Context Document

Create `{contextOutput}`:

```markdown
---
project: "{project_name}"
chapter: {ch}
page: {page}
generated: "{timestamp}"
valid_for: "current_page_only"
---

# Prose Context: {project_name} Ch{ch} P{page}

## Character Quick Reference

### {Character Name}
- **Current clothing:** {state}
- **Physical condition:** {injuries, exhaustion, etc.}
- **Emotional state:** {mood}
- **Speech pattern:** {how they talk}
- **Relationship to others:** {dynamics}

### {Character 2}
...

## Carry-Forward Requirements

These MUST be reflected in prose:

1. **{Item 1}:** {description}
2. **{Item 2}:** {description}

## Recent Events Summary

From cumulative log, last relevant events:
- {event 1}
- {event 2}

## Continuity Notes

- {Any specific continuity requirements}
- {Established facts that cannot change}
```

### 2. Save Context Document

Write to `{contextOutput}`.

### 3. Workflow Completion

```
"✅ BIBLE-SYNC LOAD COMPLETE!

**Context generated:** {contextOutput}

**Ready for:** prose-adapter

**Characters loaded:** {count}
**Carry-forward items:** {count}

**WORKFLOW COMPLETE**"
```

---

## WORKFLOW END

LOAD mode complete. Context document ready for prose-adapter.
