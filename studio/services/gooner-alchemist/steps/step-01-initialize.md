---
name: 'step-01-initialize'
description: 'Initialize pipeline and validate input'

# Path Definitions
workflow_path: '{project-root}/studio/services/gooner-alchemist'
thisStepFile: './step-01-initialize.md'
nextStepFile: './step-02-forensic-analysis.md'
stateTemplate: '{workflow_path}/resources/pipeline-state-template.yaml'
stateFile: '{output_folder}/_pipeline/{project}/state.yaml'
---

# Step 1: Initialize Pipeline

**Progress: Step 1 of 7** - Next: Forensic Analysis

## RULES:

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- MUST NOT begin any analysis work.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in Vietnamese

## CONTEXT:

- Entry point for gooner-alchemist pipeline.
- Focus: Validate inputs and create pipeline state.
- Output: State file at `{stateFile}`
- Objective: Establish clear pipeline parameters for per-page processing.

---

## 0. CHECK FOR WORK IN PROGRESS

### a) Before anything else, check if `{stateFile}` exists:

### b) IF STATE FILE EXISTS:

1. Read the state and extract: `project`, `current_page`, `pages_pending`, `status`
2. Calculate progress: `completed = pages_processed.length / pages_total`
3. Present to user:

```
Chào {user_name}! Phát hiện pipeline đang chạy:

**{project}** - Page {current_page} đang xử lý
📊 Tiến độ: {completed}% ({pages_processed.length}/{pages_total})

Đây có phải là project bạn muốn tiếp tục?

[Y] Tiếp tục từ page {current_page}
[N] Lưu trữ và bắt đầu mới
```

4. **HALT and wait for user selection.**

#### Menu Handling:
- **[Y] Continue:** Jump to appropriate step based on current page state
- **[N] Archive:** Rename state file to `state-archived-{date}.yaml`, proceed to fresh init

---

## SEQUENCE OF INSTRUCTIONS

### 1. Welcome and Input Collection

OUTPUT:
```
**🎬 GOONER ALCHEMIST PIPELINE**

Xin chào {user_name}! Director K đây, điều phối pipeline adaptation.

Để bắt đầu, mình cần:

1. **Manga source folder:** (đường dẫn đến folder chứa images)
2. **Project name:** (tên manga/project)
3. **Chapter number:** 
4. **Page range:** (ví dụ: 10-15)

Vui lòng cung cấp hoặc xác nhận thông tin!
```

**IF user already provided info in command, extract and confirm:**
- Source folder
- Page range
- Project name

### 2. Validate Input Images

**CHECK each file in page range:**

```markdown
## Input Validation

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Folder exists | {source_folder} | ✓/✗ | |
| First page | {first_page}.webp | ✓/✗ | |
| Last page | {last_page}.webp | ✓/✗ | |
| Total pages | {count} | | |
| Format | .webp/.jpg/.png | | |
```

**IF ANY CHECK FAILS:**
```
❌ Input không hợp lệ!
Missing: {list_missing}
Vui lòng kiểm tra lại đường dẫn.
```
HALT - do not proceed.

### 3. Check First Chapter Protocol

```
IF chapter == 1 AND first_page == 1:
  → FIRST CHAPTER PROTOCOL active
  → Will create new story bible
  → Extra validation steps enabled
  → Set first_chapter: true in state
```

### 4. Create Pipeline State

**Create output directories:**
```bash
mkdir -p {output_folder}/_pipeline/{project}
mkdir -p {output_folder}/_analysis/{project}
mkdir -p {output_folder}/_prose/{project}
mkdir -p {output_folder}/_bible/{project}
```

**Copy state template and populate:**

Create `{stateFile}` with:
```yaml
project: "{project_name}"
chapter: {chapter}
source_folder: "{source_folder}"
started: "{timestamp}"
status: "IN_PROGRESS"

current_page: {first_page}
pages_total: {count}
pages_pending: [{page_list}]
pages_processed: []

forensics_completed: []
context_loaded: []
prose_completed: []
audits_passed: []
bible_synced: []

audit_scores: {}
revision_counts: {}
max_revisions: 3

first_chapter: {true/false}
```

### 5. Present Checkpoint Menu

OUTPUT:
```
✅ Pipeline initialized!

**Project:** {project}
**Chapter:** {chapter}
**Pages:** {first_page} → {last_page} ({count} pages)
**First Chapter:** {yes/no}
**State:** {stateFile}

⚠️ IMPORTANT: Pipeline sẽ xử lý TỪNG PAGE một:
  forensic → prose → audit → next page

**Select:** [C] Continue to Forensic Analysis (Page {first_page})
```

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF C: 
  - VERIFY state file created
  - Load `{nextStepFile}`
- IF Any other: Respond helpfully, redisplay menu

---

## REQUIRED OUTPUTS:

- MUST validate all input images exist
- MUST create pipeline state file
- MUST create output directories

## VERIFICATION CHECKLIST:

- [ ] WIP check performed FIRST
- [ ] All input images validated
- [ ] State file created at `{stateFile}`
- [ ] Output directories created
- [ ] `current_page` set to first page
- [ ] User selected [C] to continue

---

**Master Rule:** Validate everything. Track everything. Gate everything.
