---
name: 'step-07-quality-check'
description: 'Pre-audit quality verification before sending to gooner-audit'

# Path Definitions
workflow_path: '{project-root}/studio/core/lewd-writer'
thisStepFile: './step-07-quality-check.md'
nextStepFile: './step-08-wiki-update.md'
outputFile: '{output_folder}/_prose/{manga_name}/chapter_{ch}/page_{page_num}_prose.md'
---

# Step 7: Quality Self-Check

## STEP GOAL

Perform self-audit against gooner-audit criteria and PREPARE FOR RECURSIVE UPDATE.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 📖 CRITICAL: This is the pre-final step
- ✅ Be honest in self-assessment

### Step-Specific Rules

- 🎯 Score against gooner-audit rubric
- 🚫 FORBIDDEN to submit prose that self-scores <70
- 💬 Fix issues before completing

## MANDATORY SEQUENCE

### 1. Sensory Immersion Check (25 points)

```markdown
## Quality Self-Check

### A: Sensory Immersion (25 pts)

| Check | Points | Self-Score | Evidence |
|-------|--------|------------|----------|
| A1: Smell ≥3 | 0-5 | {score} | {count} mentions |
| A2: Touch ≥5 | 0-5 | {score} | {count} textures |
| A3: Sound ≥3 | 0-5 | {score} | {count} sounds |
| A4: Visual density | 0-5 | {score} | Integrated |
| A5: Taste (if oral) | 0-5 | {score} | {count} or N/A |

**Subtotal A:** {score}/25
```

### 2. Edging Rhythm Check (20 points)

```markdown
### B: Edging Rhythm (20 pts)

| Check | Points | Self-Score | Evidence |
|-------|--------|------------|----------|
| B1: Setup exists | 0-4 | {score} | Environment section |
| B2: Build tension | 0-4 | {score} | Escalation present |
| B3: Peak intensity | 0-4 | {score} | Climax section |
| B4: Aftermath complete | 0-4 | {score} | Not truncated |
| B5: Pacing variation | 0-4 | {score} | Rhythm changes |

**Subtotal B:** {score}/20
```

### 3. Fetish Exploitation Check (20 points)

```markdown
### C: Fetish Exploitation (20 pts)

| Check | Points | Self-Score | Evidence |
|-------|--------|------------|----------|
| C1: Power dynamic clear | 0-5 | {score} | Dom/sub visible |
| C2: Fetish elements | 0-5 | {score} | Tags represented |
| C3: Degrading dialogue | 0-5 | {score} | Explicit speech |
| C4: Psychological elements | 0-5 | {score} | Character states |

**Subtotal C:** {score}/20
```

### 4. Psychological Depth Check (25 points)

```markdown
### D: Psychological Depth (25 pts)

| Check | Points | Self-Score | Evidence |
|-------|--------|------------|----------|
| D1: Character voices | 0-5 | {score} | Distinct speech |
| D2: Reactions realistic | 0-5 | {score} | Body language |
| D3: Progression shown | 0-5 | {score} | State changes |
| D4: Observer perspective | 0-5 | {score} | Camera maintained |
| D5: No moral judgment | 0-5 | {score} | Clean of judgment |

**Subtotal D:** {score}/25
```

### 5. Technical Check (10 points)

```markdown
### E: Technical (10 pts)

| Check | Points | Self-Score | Evidence |
|-------|--------|------------|----------|
| E1: Zero-Skip | 0-3 | {score} | All panels covered |
| E2: Dialogue integrated | 0-3 | {score} | All lines used |
| E3: Grammar/flow | 0-2 | {score} | Smooth prose |
| E4: Format compliance | 0-2 | {score} | Proper structure |

**Subtotal E:** {score}/10
```

### 6. Calculate Total

```markdown
### TOTAL SCORE

| Category | Score |
|----------|-------|
| A: Sensory | /25 |
| B: Rhythm | /20 |
| C: Fetish | /20 |
| D: Psychological | /25 |
| E: Technical | /10 |
| **TOTAL** | **{score}/100** |

**STATUS:** {PASS ≥85 / REVIEW 70-84 / FAIL <70}
```

### 7. Fix Issues if Below 85

If score <85:

- Identify weakest categories
- Make targeted improvements
- Re-score after fixes

### 8. Finalize Output

Update `{outputFile}` frontmatter:

```yaml
---
stepsCompleted: ['step-01-context-loading', 'step-02-scene-planning', 'step-03-environment-prose', 'step-04-action-prose', 'step-05-dialogue-integration', 'step-06-aftermath-polish', 'step-07-quality-check']
status: READY_FOR_AUDIT
self_audit_score: {score}
---
```

### 9. Continue to Recursive Update

```
"✅ PROSE ADAPTATION AUDIT COMPLETE!

**Self-Audit Score:** {score}/100 ({status})
**Output:** {outputFile}

**Tiếp theo:** Recursive Universe Update (Extract Facts)

**Chọn:** [C] Continue to Wiki Update"
```

#### Menu Handling Logic

- IF C: Save output, load `{nextStepFile}`
- IF other: Redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- Self-audit completed honestly
- Score ≥70 achieved
- Issues fixed before completion
- Output file properly formatted
- Ready for recursive update

### ❌ SYSTEM FAILURE

- Submitting prose <70 score
- Dishonest self-assessment
- Not fixing identified issues
- Missing frontmatter updates

**Master Rule:** Honest self-check. Fix before submit. Quality first.
