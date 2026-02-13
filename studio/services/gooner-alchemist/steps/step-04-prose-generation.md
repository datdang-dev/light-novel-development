---
name: 'step-04-prose-generation'
description: 'Invoke prose-adapter for prose generation'

# Path Definitions
workflow_path: '{project-root}/studio/services/gooner-alchemist'
thisStepFile: './step-04-prose-generation.md'
nextStepFile: './step-05-quality-audit.md'
proseAdapterWorkflow: '{project-root}/studio/core/lewd-writer/workflow.md'
stateFile: '{output_folder}/_pipeline/{project}/state.yaml'
analysisFolder: '{output_folder}/_analysis/{project}'
proseFolder: '{output_folder}/_prose/{project}'
---

# Step 4: Prose Generation

**Progress: Step 4 of 7** - Next: Quality Audit

## RULES:

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- MUST check forensic gate BEFORE any prose work.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in Vietnamese

## CONTEXT:

- Requires forensic report from Step 2.
- Requires context loaded from Step 3.
- Focus: Invoke /prose-adapter for prose generation.
- Output: Prose at `{proseFolder}/page-{XXX}.md`

---

## 0. PRE-EXECUTION GATE (MANDATORY)

### a) Load Pipeline State

Read `{stateFile}` and extract:
- `current_page`
- `forensics_completed`
- `context_loaded`

### b) FORENSIC GATE CHECK

```
🚫 GATE CHECK: FORENSIC REQUIRED

Expected: {analysisFolder}/page-{current_page}-forensic.md

IF FILE NOT EXISTS:
  ─────────────────────────────────────────────
  🚫 FORENSIC GATE BLOCKED
  📋 Missing: {analysisFolder}/page-{current_page}-forensic.md
  📤 ACTION: Return to Step 2 (Forensic Analysis)
  ─────────────────────────────────────────────
  
  HALT - DO NOT PROCEED
  Load step-02-forensic-analysis.md

IF FILE EXISTS:
  ✅ Forensic gate passed
  PROCEED
```

### c) CONTEXT GATE CHECK

```
IF current_page NOT IN context_loaded:
  ⚠️ Context not loaded for this page
  Recommend: Return to Step 3
  [C] Continue anyway | [B] Back to Context Loading
  
  HALT and wait
```

---

## SEQUENCE OF INSTRUCTIONS

### 1. Load Required Inputs

**Read forensic report:**
```
forensic_content = READ {analysisFolder}/page-{current_page}-forensic.md
```

**Extract key data:**
- Panel count
- Character list
- SFX list
- Dialogue list
- Continuity notes

### 2. Announce Delegation

OUTPUT:
```
─────────────────────────────────────────────
📤 DELEGATING TO: Suki ✍️ (Lewd Writer)
📋 TASK: Generate R18 prose for page {current_page}
📁 INPUT: {analysisFolder}/page-{current_page}-forensic.md
📁 OUTPUT: {proseFolder}/page-{current_page}.md
─────────────────────────────────────────────
```

### 3. Invoke Prose-Adapter

**CRITICAL**: Load and execute `{proseAdapterWorkflow}` with:
- Forensic path: `{analysisFolder}/page-{current_page}-forensic.md`
- Context: Story bible loaded in Step 3
- Output: `{proseFolder}/page-{current_page}.md`

**DO NOT write prose yourself. INVOKE the workflow.**

```
🚨 DIRECTOR K DOES NOT WRITE PROSE 🚨

You MUST invoke /prose-adapter (executed by /lewd-writer Suki)
You do NOT write prose yourself
```

### 4. Wait for Completion

Prose-adapter will:
1. ✅ Load context and forensic
2. ✅ Plan scene structure
3. ✅ Write environment (sensory density)
4. ✅ Write action (explicit detail)
5. ✅ Integrate dialogue (Vietnamese)
6. ✅ Add SFX (Romanized Japanese)
7. ✅ Polish aftermath
8. ✅ Self-check quality

### 5. Verify Prose Output

**GATE CHECK - MANDATORY**

```markdown
## Prose Output Verification

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| File exists | {proseFolder}/page-{current_page}.md | ✓/✗ | |
| Word count | ≥500 | | |
| Sensory count | ≥8 | | |
| SFX present | ≥3 | | |
| Dialogue present | ≥1 | | |
| Self-audit score | ≥75 | | |
```

**IF ANY CHECK FAILS:**
```
⚠️ PROSE INCOMPLETE
Missing: {list_failed_checks}
ACTION: Re-invoke prose-adapter with feedback
```

### 6. Update Pipeline State

Update `{stateFile}`:
```yaml
prose_completed:
  - ... existing ...
  - {current_page}  # ADD this
```

### 7. Present Checkpoint Menu

OUTPUT:
```
✅ Prose generation complete for page {current_page}!

📄 Output: {proseFolder}/page-{current_page}.md
📊 Self-Score: {score}/100
🔢 Word Count: {count}
🔄 Attempt: {X}/3

**Select:** [C] Continue to Audit | [V] View Prose | [R] Regenerate
```

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF C:
  - VERIFY prose file exists (GATE CHECK)
  - IF EXISTS: Update state, load `{nextStepFile}`
  - IF NOT EXISTS: "🚫 Cannot proceed - prose missing" → Stay here
- IF V: Display prose contents, redisplay menu
- IF R: Re-invoke prose-adapter, return to Step 4
- IF Any other: Respond helpfully, redisplay menu

---

## REQUIRED OUTPUTS:

- MUST invoke /prose-adapter workflow (NOT write directly)
- MUST meet minimum quality thresholds
- MUST update pipeline state

## VERIFICATION CHECKLIST:

- [ ] Forensic gate checked FIRST
- [ ] Context gate checked
- [ ] Delegation banner displayed
- [ ] /prose-adapter invoked (NOT self-written)
- [ ] Prose verified with all checks passed
- [ ] `prose_completed` updated in state
- [ ] User selected [C] to continue

---

## 🚨 SYSTEM FAILURE CONDITIONS

Director K writing prose = **PROTOCOL VIOLATION**
Missing forensic file = **GATE BLOCKED - RETURN TO STEP 2**
Skipping to audit without prose = **PIPELINE FAILURE**

**Master Rule:** FORENSIC GATE. DELEGATE. VERIFY. Never write directly.
