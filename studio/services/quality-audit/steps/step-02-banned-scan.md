---
name: 'step-02-banned-scan'
description: 'Scan for auto-fail banned words'

# Path Definitions
workflow_path: '{project-root}/studio/services/quality-audit'
thisStepFile: './step-02-banned-scan.md'
nextStepFile: './step-03-category-scoring.md'
bannedWordsFile: '{workflow_path}/data/banned-words.txt'
---

# Step 2: Banned Word Scan

## STEP GOAL:

Scan prose for banned words that trigger automatic failure before category scoring.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### AUTO-FAIL RULE:

```
ANY banned word present = AUTO-FAIL
Score becomes 0/100
Must revise before re-audit
```

### Step-Specific Rules:

- 🎯 Focus only on banned word detection
- 🚫 NO tolerance for banned words
- 💬 If found, immediately flag and stop scoring

## MANDATORY SEQUENCE

### 1. Load Banned Words List

```
BANNED WORDS (Moral Judgment):
- hôi thối
- dơ bẩn  
- bẩn thỉu
- ghê tởm
- đê tiện
- đáng khinh
- ô uế
- nhơ nhớp
- tởm lợm

BANNED PATTERNS (Judgment Context):
- "thật là [negative adjective]"
- "không thể chấp nhận"
- Any narrator moral commentary
```

### 2. Scan Prose

Systematically scan prose content for:

- Exact matches of banned words
- Variations/conjugations of banned words
- Banned patterns in narration
- Moral judgment phrases

### 3. Document Findings

```markdown
## Banned Word Scan

**Scan Status:** {CLEAN / VIOLATIONS FOUND}

### Violations (if any)

| Word/Phrase | Location | Context |
|-------------|----------|---------|
| {banned} | Line {X} | "...{context}..." |

**Total Violations:** {count}
```

### 4. Determine Outcome

```
IF violations == 0:
  - Status: CLEAN
  - Proceed to category scoring

IF violations > 0:
  - Status: AUTO-FAIL
  - Score: 0/100
  - Generate revision feedback
  - Return to prose-adapter
```

### 5. Update Audit Report

Add scan results to audit report:
- Update frontmatter: `stepsCompleted: [..., 'step-02-banned-scan']`
- Add banned word scan section

### 6. Present MENU OPTIONS

**IF CLEAN:**

```
"✅ Banned word scan: CLEAN

**Status:** No violations found
**Tiếp theo:** Category scoring

**Chọn:** [C] Continue to Category Scoring"
```

**IF VIOLATIONS:**

```
"❌ Banned word scan: AUTO-FAIL

**Violations Found:** {count}
{List violations}

**Required Action:** Return to prose-adapter for revision

**Chọn:** [F] Generate failure report and exit"
```

#### Menu Handling Logic:

- IF CLEAN + C: Save audit, load `{nextStepFile}`
- IF VIOLATIONS + F: Generate failure report, complete workflow with FAIL status

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Complete prose scanned
- All banned words checked
- Clear documentation of results
- Correct routing (continue or fail)

### ❌ SYSTEM FAILURE:

- Incomplete scan
- Missing banned word from check
- Proceeding despite violations

**Master Rule:** Zero tolerance. Full scan. No exceptions.
