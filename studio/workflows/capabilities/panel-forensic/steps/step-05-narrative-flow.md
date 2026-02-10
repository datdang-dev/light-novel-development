---
name: 'step-05-narrative-flow'
description: 'Analyze panel transitions and pacing structure'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/panel-forensic'
thisStepFile: './step-05-narrative-flow.md'
nextStepFile: './step-06-r18-documentation.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
---

# Step 5: Narrative Flow Analysis

## STEP GOAL:

Analyze page-level storytelling through panel transitions, pacing, and visual narrative techniques.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Step-Specific Rules:

- 🎯 Focus on transitions and pacing, not content
- 💬 Use Scott McCloud's transition terminology

## MANDATORY SEQUENCE

### 1. Classify Panel Transitions

For EACH transition between adjacent panels:

```markdown
## Narrative Flow

### Panel Transitions

| From → To | Transition Type | Description |
|-----------|-----------------|-------------|
| P1 → P2 | moment-to-moment | Small time gap, same action continues |
| P2 → P3 | action-to-action | Same subject, action progresses |
| P3 → P4 | subject-to-subject | Same scene, focus shifts to different character |
```

**Transition Type Reference:**
- **Moment-to-moment**: Very small time gap, same subject
- **Action-to-action**: Single subject, action progresses
- **Subject-to-subject**: Same scene, different subject focus
- **Scene-to-scene**: Significant time/space change
- **Aspect-to-aspect**: Different aspects of same moment (common in manga)
- **Non-sequitur**: No logical relationship

### 2. Analyze Pacing Structure

```markdown
### Pacing Analysis

**Time Compression/Expansion:**
- {Describe how time feels - compressed (fast action) or expanded (slow tension)}

**Tension Curve:**
```
P1 ●───── LOW (setup)
P2    ●── BUILDING
P3       ●── RISING
P4          ●── PEAK
P5       ●── RELEASE
```

**Information Reveal Order:**
- P1: {what information is revealed}
- P2: {what new info}
- P3: {progression}
```

### 3. Identify Climax Points

```markdown
### Climax Identification

**Primary Climax Panel:** P{X}
- **Why:** {What makes this the peak moment}
- **Build-up panels:** P{} → P{} → P{}
- **Release panels:** P{} → P{}

**Secondary peaks (if any):** P{Y}
```

### 4. Note Visual Storytelling Techniques

```markdown
### Visual Techniques

**Panel Size Variation:**
- Largest panel: P{X} - Purpose: {emphasis/impact}
- Smallest panels: P{Y}, P{Z} - Purpose: {quick action/transitions}

**Negative Space Usage:**
- {Where and why empty space is used}

**Eye Flow Direction:**
- {How the reader's eye is guided across the page}
```

### 5. Update Output File

Append narrative flow section to `{outputFile}`:
- Update frontmatter: `stepsCompleted: [..., 'step-05-narrative-flow']`

### 6. Present MENU OPTIONS

Display:

```
"✅ Narrative flow analysis hoàn thành!

**Kết quả:**
- Transitions identified: {count}
- Climax panel: P{X}
- Pacing: {compressed/expanded/balanced}

**Chọn:** [C] Continue to R18 Documentation"
```

#### Menu Handling Logic:

- IF C: Save/update output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All transitions classified
- Pacing structure identified
- Climax panel identified
- Visual techniques noted
- Output file updated

### ❌ SYSTEM FAILURE:

- Missing transitions
- No climax identification
- Ignoring pacing elements

**Master Rule:** Understand the story flow before documenting explicit content.
