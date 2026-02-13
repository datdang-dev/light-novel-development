---
name: 'step-07-complete'
description: 'Finalize pipeline and generate summary'

# Path Definitions
workflow_path: '{project-root}/studio/services/gooner-alchemist'
thisStepFile: './step-07-complete.md'
---

# Step 7: Complete Pipeline

## STEP GOAL:

Finalize the pipeline, generate completion summary, and prepare for next page.

## MANDATORY SEQUENCE

### 1. Generate Completion Summary

```markdown
## Pipeline Completion Summary

### {project_name} Chapter {ch} Page {page}

**Started:** {timestamp}
**Completed:** {timestamp}
**Duration:** {time}

### Outputs Generated

| Output | Path | Status |
|--------|------|--------|
| Forensics | {path} | ✅ |
| Prose | {path} | ✅ |
| Audit | {path} | ✅ |
| Bible | {path} | ✅ |

### Quality Metrics

**Final Audit Score:** {score}/100
**Revision Attempts:** {count}
**Zero-Skip:** COMPLIANT

### Bible Updates

**Characters affected:** {list}
**Events logged:** {count}
```

### 2. Update Pipeline State

Finalize pipeline doc:

```yaml
---
status: COMPLETE
completed: "{timestamp}"
final_score: {score}
outputs:
  forensics: "{path}"
  prose: "{path}"
  audit: "{path}"
---
```

### 3. Check for Next Page

```
IF more pages in range:
  → Prepare for next page
  → Reset step counter
  → "Ready to process page {N+1}"

IF last page:
  → "Chapter adaptation complete"
  → Suggest chapter compilation
```

### 4. Workflow Completion

**IF MORE PAGES:**

```
"✅ **PAGE {page} COMPLETE!**

**Score:** {score}/100
**Outputs:** All generated ✓

**Next page ready:** Page {page+1}

**Chọn:** 
[N] Next Page (continue pipeline)
[E] Exit (end session)"
```

**IF LAST PAGE:**

```
"🎉 **CHAPTER {ch} COMPLETE!**

**Pages processed:** {count}
**Total prose:** ~{word_count} words

**All outputs in:** {output_folder}

**Suggested next:**
- Chapter compilation workflow
- Release preparation

**PIPELINE COMPLETE**"
```

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All outputs verified
- Pipeline state finalized
- Summary generated
- Next page prepared if applicable

### ❌ SYSTEM FAILURE:

- Missing outputs
- Incomplete summary
- Not finalizing state

**Master Rule:** Verify everything delivered. Clear summary. Ready for next.

---

## WORKFLOW END

This concludes the Gooner Alchemist pipeline for the current page.

**Outputs:**
- Forensic analysis
- Adapted prose (audit approved)
- Updated story bible
- Audit report
