---
name: 'save-04-log-events'
description: 'Add events to cumulative log'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/bible-sync'
thisStepFile: './save-04-log-events.md'
logPath: '{output_folder}/_bible/{project_name}/state/cumulative-log.md'
---

# SAVE Step 4: Log Events

## STEP GOAL:

Add significant events from this scene to the cumulative event log.

## MANDATORY SEQUENCE

### 1. Format Log Entry

```markdown
## Ch{ch} Page {page} - {timestamp}

**Participants:** {characters}
**Location:** {setting}

### Events
- {Event 1}: {description}
- {Event 2}: {description}

### State Changes Summary
- {Character}: {from} → {to}

### Continuity Notes
- {Any facts established}
- {Details to remember}

---
```

### 2. Append to Cumulative Log

Add entry to `{logPath}`.

### 3. Workflow Completion

```
"✅ BIBLE-SYNC SAVE COMPLETE!

**Events logged:** {count}
**State updated:** ✓

**Bible synchronized for:** {project_name}

**WORKFLOW COMPLETE**"
```

---

## WORKFLOW END

SAVE mode complete. Bible is now synchronized with latest prose.
