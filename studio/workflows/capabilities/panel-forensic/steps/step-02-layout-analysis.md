---
name: 'step-02-layout-analysis'
description: 'Analyze page layout, panel arrangement, and reading flow'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/panel-forensic'
thisStepFile: './step-02-layout-analysis.md'
nextStepFile: './step-03-panel-breakdown.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
---

# Step 2: Layout Analysis

## STEP GOAL:

Perform complete panel segmentation and layout analysis for the validated page, establishing the structural foundation for per-panel forensic breakdown.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip any panel in layout analysis
- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Role Reinforcement:

- ✅ You are a layout analyst examining visual structure
- ✅ Use precise positional terminology
- ✅ Document everything systematically

### Step-Specific Rules:

- 🎯 Focus only on layout and panel arrangement
- 🚫 FORBIDDEN to analyze panel content (that's step 3)
- 💬 Create complete panel index before proceeding

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly.

### 1. Use Sequential Thinking for Layout

**MANDATORY:** Call `mcp_sequential-thinking_sequentialthinking` with minimum 3 thoughts:

```
Thought 1: PAGE LAYOUT TYPE
- Is this standard grid, irregular, or splash?
- How many distinct panels?
- Any overlapping or borderless panels?

Thought 2: PANEL ARRANGEMENT
- Describe exact positions (top-right, center, etc.)
- Note gutters and bleeds
- Identify reading flow direction

Thought 3: VERIFY PANEL COUNT
- Count panels again
- Confirm no missed panels
- Note any unusual panel shapes
```

### 2. Document Page Layout

Add to output file:

```markdown
## Layout Analysis

### Page Structure
- **Layout Type:** {grid / irregular / splash / double-page}
- **Total Panels:** {exact count}
- **Panel Arrangement:** {describe}
- **Gutters:** {present / minimal / none}
- **Bleed:** {art extending to page edge: yes / no}
- **Reading Flow:** {right-to-left / left-to-right}

### Unusual Features
{Note any special layout elements: overlapping panels, borderless art, etc.}
```

### 3. Create Panel Index

Create numbered index of ALL panels:

```markdown
### Panel Index

| Panel ID | Position | Size | Border Type |
|----------|----------|------|-------------|
| P1 | top-right | half-page | rectangular |
| P2 | top-left | quarter | irregular |
| P3 | center | full-width | borderless |
| ... | ... | ... | ... |

**Position Legend:**
- top-right, top-left, top-center
- mid-right, mid-left, mid-center  
- bottom-right, bottom-left, bottom-center
- full-page (splash), full-width (horizontal strip)

**Size Categories:**
- full-page, half-page, quarter, small, strip
```

### 4. Verify Zero-Skip Compliance

Checklist before proceeding:

- [ ] Every panel numbered and indexed
- [ ] No panels missed in count
- [ ] Reading order confirmed
- [ ] All unusual features noted

### 5. Update Output File

Append layout analysis section to `{outputFile}`:
- Update frontmatter: `stepsCompleted: ['step-01-input-validation', 'step-02-layout-analysis']`

### 6. Present MENU OPTIONS

Display:

```
"✅ Layout analysis hoàn thành!

**Kết quả:**
- Panels: {total_count}
- Layout: {layout_type}
- Reading: {direction}

**Panel Index đã tạo.** Tiếp theo: Per-panel forensic breakdown

**Chọn:** [C] Continue to Panel Breakdown"
```

#### Menu Handling Logic:

- IF C: Save to output file, update frontmatter, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN all panels are indexed and layout is fully documented will you load and execute `{nextStepFile}`.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Sequential thinking used for layout
- All panels counted and indexed
- Layout type correctly identified
- Reading order confirmed
- Panel index table created
- Output file updated with layout section

### ❌ SYSTEM FAILURE:

- Missing panels in count
- No panel index created
- Skipping unusual panel features
- Not using sequential thinking
- Proceeding without complete layout documentation

**Master Rule:** Count everything. Index everything. Miss nothing.
