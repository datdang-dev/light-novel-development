---
name: 'step-07-final-report'
description: 'Compile and generate final forensic report'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/panel-forensic'
thisStepFile: './step-07-final-report.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
---

# Step 7: Final Report

## STEP GOAL:

Compile all analysis into a complete forensic report, verify Zero-Skip Protocol compliance, and prepare output for downstream workflows.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: This is the FINAL step - ensure everything is complete
- ✅ YOU MUST speak in Vietnamese

### Step-Specific Rules:

- 🎯 Focus on compilation and verification
- 🚫 FORBIDDEN to add new analysis (only compile existing)
- 💬 Verify all sections present and complete

## MANDATORY SEQUENCE

### 1. Verify All Sections Present

Check output file contains:

- [ ] Page Identification (from Step 1)
- [ ] Layout Analysis + Panel Index (from Step 2)
- [ ] Panel Breakdowns for ALL panels (from Step 3)
- [ ] Dialogue Table (from Step 4)
- [ ] SFX Table (from Step 4)
- [ ] Narrative Flow (from Step 5)
- [ ] R18 Documentation (from Step 6)

### 2. Zero-Skip Verification

```markdown
## Zero-Skip Compliance Check

**Panel Coverage:**
- Total panels in layout: {X}
- Panels documented: {X}
- Coverage: {100% / X%}

**Element Check:**
- [ ] Every panel analyzed
- [ ] Every character noted
- [ ] All fluids/residue catalogued
- [ ] All text extracted
- [ ] All SFX translated
- [ ] Fetish tags assigned

**Status:** {COMPLIANT / NON-COMPLIANT}

**Issues Found (if any):**
{List any gaps found}
```

### 3. Generate Page Summary

```markdown
## Executive Summary

**Page:** {manga_name} Page {page_num}
**Panels:** {count}
**Characters:** {list}
**Primary Action:** {1-2 sentence summary of what happens}
**Fetish Tags:** {primary tags}
**Mood/Tone:** {describe}

### Key Observations
1. {Important observation 1}
2. {Important observation 2}
3. {Important observation 3}

### Continuity Notes
- **Connects to previous:** {how this page flows from previous}
- **Sets up next:** {what is set up for following pages}
```

### 4. Create Quick Reference Table

```markdown
## Quick Reference

| Panel | Characters | Action | Key Details |
|-------|------------|--------|-------------|
| P1 | CharA | Setup | Context establishment |
| P2 | CharA, CharB | Approach | Tension building |
| P3 | CharA, CharB | Contact | First touch |
| ... | ... | ... | ... |
```

### 5. Finalize Output File

Update `{outputFile}` frontmatter:

```yaml
---
manga: "{manga_name}"
page: {page_num}
created: "{date}"
stepsCompleted: ['step-01-input-validation', 'step-02-layout-analysis', 'step-03-panel-breakdown', 'step-04-dialogue-extraction', 'step-05-narrative-flow', 'step-06-r18-documentation', 'step-07-final-report']
status: COMPLETE
zero_skip_compliant: true
total_panels: {count}
characters: [{list}]
primary_fetish_tags: [{tags}]
---
```

### 6. Workflow Completion

Display:

```
"✅ FORENSIC ANALYSIS HOÀN THÀNH!

**Report:** {outputFile}

**Summary:**
- Page: {manga_name} Page {page_num}
- Panels: {count}
- Zero-Skip: COMPLIANT ✓

**Output Ready For:**
- entity-extractor (structured data)
- prose-adapter (visual evidence)

**WORKFLOW COMPLETE**"
```

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 7 steps documented in frontmatter
- All sections present in output
- Zero-Skip verification passed
- Summary generated
- Quick reference table created
- Status set to COMPLETE

### ❌ SYSTEM FAILURE:

- Missing steps in completion record
- Missing sections in output
- Zero-Skip verification failed
- No summary generated
- Status not updated

**Master Rule:** Verify everything. Compile completely. Mark COMPLETE only when truly done.

---

## WORKFLOW END

This concludes the Panel Forensic workflow. The output file is ready for consumption by:
- `entity-extractor` workflow
- `prose-adapter` workflow
- Direct use in `gooner-alchemist` pipeline
