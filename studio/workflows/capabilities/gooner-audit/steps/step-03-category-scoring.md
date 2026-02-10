---
name: 'step-03-category-scoring'
description: 'Score prose across all 5 quality categories'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/gooner-audit'
thisStepFile: './step-03-category-scoring.md'
nextStepFile: './step-04-generate-feedback.md'
---

# Step 3: Category Scoring

## STEP GOAL:

Score the prose across all 5 quality categories with specific evidence for each rating.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Scoring Rules:

```
SCORING PRINCIPLES:
- Be objective, not generous
- Require EVIDENCE for each score
- Count actual instances, don't estimate
- If in doubt, score lower
```

### Step-Specific Rules:

- 🎯 Score ALL categories, no skipping
- 🚫 FORBIDDEN to give points without evidence
- 💬 Document specific examples for each score

## MANDATORY SEQUENCE

### 1. Category A: Sensory Immersion (25 points)

```markdown
## Category Scoring

### A: Sensory Immersion (25 pts)

| ID | Check | Max | Score | Evidence |
|----|-------|-----|-------|----------|
| A1 | Smell (≥3 required) | 5 | {0-5} | Count: {X} - "{example}" |
| A2 | Touch (≥5 required) | 5 | {0-5} | Count: {X} - "{example}" |
| A3 | Sound (≥3 required) | 5 | {0-5} | Count: {X} - "{example}" |
| A4 | Visual density | 5 | {0-5} | {assessment} |
| A5 | Taste (if applicable) | 5 | {0-5} | Count: {X} or N/A |

**Scoring Guide:**
- 0: Not present
- 1-2: Below minimum
- 3: Meets minimum
- 4: Good variety
- 5: Exceptional density

**Subtotal A:** {X}/25
```

### 2. Category B: Edging Rhythm (20 points)

```markdown
### B: Edging Rhythm (20 pts)

| ID | Check | Max | Score | Evidence |
|----|-------|-----|-------|----------|
| B1 | Setup exists | 4 | {0-4} | {environment section present?} |
| B2 | Build tension | 4 | {0-4} | {escalation visible?} |
| B3 | Peak intensity | 4 | {0-4} | {climax section quality} |
| B4 | Aftermath complete | 4 | {0-4} | {post-climax not truncated?} |
| B5 | Pacing variation | 4 | {0-4} | {rhythm changes present?} |

**Scoring Guide:**
- 0: Missing entirely
- 1: Present but weak
- 2: Adequate
- 3: Good
- 4: Excellent

**Subtotal B:** {X}/20
```

### 3. Category C: Fetish Exploitation (20 points)

```markdown
### C: Fetish Exploitation (20 pts)

| ID | Check | Max | Score | Evidence |
|----|-------|-----|-------|----------|
| C1 | Power dynamic clear | 5 | {0-5} | {dom/sub visible?} |
| C2 | Fetish elements | 5 | {0-5} | {tags from forensics represented?} |
| C3 | Degrading dialogue | 5 | {0-5} | {explicit speech present?} |
| C4 | Psychological elements | 5 | {0-5} | {character states explored?} |

**Subtotal C:** {X}/20
```

### 4. Category D: Psychological Depth (25 points)

```markdown
### D: Psychological Depth (25 pts)

| ID | Check | Max | Score | Evidence |
|----|-------|-----|-------|----------|
| D1 | Character voices | 5 | {0-5} | {distinct speech patterns?} |
| D2 | Reactions realistic | 5 | {0-5} | {body language described?} |
| D3 | Progression shown | 5 | {0-5} | {state changes visible?} |
| D4 | Observer perspective | 5 | {0-5} | {camera maintained?} |
| D5 | No moral judgment | 5 | {0-5} | {clean of judgment?} |

**Subtotal D:** {X}/25
```

### 5. Category E: Technical (10 points)

```markdown
### E: Technical (10 pts)

| ID | Check | Max | Score | Evidence |
|----|-------|-----|-------|----------|
| E1 | Zero-Skip | 3 | {0-3} | {all panels covered?} |
| E2 | Dialogue integrated | 3 | {0-3} | {all lines used?} |
| E3 | Grammar/flow | 2 | {0-2} | {prose quality} |
| E4 | Format compliance | 2 | {0-2} | {proper structure?} |

**Subtotal E:** {X}/10
```

### 6. Calculate Total Score

```markdown
## Score Summary

| Category | Score | Max |
|----------|-------|-----|
| A: Sensory Immersion | {X} | 25 |
| B: Edging Rhythm | {X} | 20 |
| C: Fetish Exploitation | {X} | 20 |
| D: Psychological Depth | {X} | 25 |
| E: Technical | {X} | 10 |
| **TOTAL** | **{X}** | **100** |

**Threshold Status:**
- ≥85: PASS ✅
- 70-84: REVIEW ⚠️
- <70: FAIL ❌

**Current Status:** {PASS/REVIEW/FAIL}
```

### 7. Update Audit Report

Append all scoring to audit report:
- Update frontmatter: `stepsCompleted: [..., 'step-03-category-scoring']`

### 8. Present MENU OPTIONS

```
"✅ Category scoring hoàn thành!

**TOTAL SCORE:** {X}/100 ({status})

**Category Breakdown:**
- A: {X}/25
- B: {X}/20
- C: {X}/20
- D: {X}/25
- E: {X}/10

**Tiếp theo:** Generate feedback

**Chọn:** [C] Continue to Feedback"
```

#### Menu Handling Logic:

- IF C: Save audit, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 5 categories scored
- Evidence provided for each score
- Specific counts documented
- Total calculated correctly

### ❌ SYSTEM FAILURE:

- Skipping categories
- Scores without evidence
- Incorrect calculation
- Generous scoring without basis

**Master Rule:** Score everything. Evidence required. Be objective.
