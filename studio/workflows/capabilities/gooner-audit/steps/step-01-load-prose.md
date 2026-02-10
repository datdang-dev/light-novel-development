---
name: 'step-01-load-prose'
description: 'Load prose file and initialize audit document'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/gooner-audit'
thisStepFile: './step-01-load-prose.md'
nextStepFile: './step-02-banned-scan.md'
---

# Step 1: Load Prose

## STEP GOAL:

Load the prose file to be audited and initialize the audit report document.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER begin audit without fully loading prose
- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Step-Specific Rules:

- 🎯 Focus only on loading and initialization
- 🚫 FORBIDDEN to begin scoring before load complete
- 💬 Verify prose is from prose-adapter workflow

## MANDATORY SEQUENCE

### 1. Request Prose Path

If not provided:

```
"Xin chào! Mình là Riko, QA specialist cho R18 prose. 📋

Để bắt đầu audit, mình cần:

1. **Đường dẫn prose file** (output từ prose-adapter)
2. **Page/chapter info** (để tracking)

Vui lòng cung cấp đường dẫn prose!"
```

### 2. Load and Read Prose

Use `view_file` to load the complete prose file.

Extract from frontmatter:
- manga name
- page number
- chapter number
- self_audit_score (if available)
- stepsCompleted (verify prose-adapter complete)

### 3. Verify Prose Source

```
CHECK: stepsCompleted contains prose-adapter steps
- [ ] step-01-context-loading
- [ ] step-02-scene-planning  
- [ ] step-03-environment-prose
- [ ] step-04-action-prose
- [ ] step-05-dialogue-integration
- [ ] step-06-aftermath-polish
- [ ] step-07-quality-check

IF incomplete: Reject and return to prose-adapter
```

### 4. Initialize Audit Report

Create audit report file:

```markdown
---
manga: "{manga_name}"
page: {page_num}
chapter: {ch}
created: "{date}"
stepsCompleted: ['step-01-load-prose']
status: AUDIT_IN_PROGRESS
prose_source: "{prose_path}"
---

# Gooner Audit Report: {manga_name} Ch{ch} P{page_num}

## Audit Info

**Prose File:** {path}
**Self-Audit Score:** {score or 'N/A'}
**Audit Start:** {timestamp}

---
```

### 5. Present MENU OPTIONS

```
"✅ Prose loaded thành công!

**File:** {prose_path}
**Self-score:** {score}
**Word count:** ~{estimate}

**Tiếp theo:** Banned word scan

**Chọn:** [C] Continue to Banned Scan"
```

#### Menu Handling Logic:

- IF C: Save audit file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Prose file fully loaded
- Source verified as prose-adapter output
- Audit report initialized
- Metadata extracted

### ❌ SYSTEM FAILURE:

- Not loading full prose
- Auditing non-prose-adapter output
- Not creating audit report

**Master Rule:** Full load. Verify source. Initialize report.
