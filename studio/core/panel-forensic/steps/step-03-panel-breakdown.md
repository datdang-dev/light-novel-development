---
name: 'step-03-panel-breakdown'
description: 'Per-panel forensic analysis with Zero-Skip Protocol'

# Path Definitions
workflow_path: '{project-root}/studio/core/panel-forensic'
thisStepFile: './step-03-panel-breakdown.md'
nextStepFile: './step-04-dialogue-extraction.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
analysisElements: '{workflow_path}/data/analysis-elements.csv'
---

# Step 3: Panel Breakdown

## STEP GOAL

Perform comprehensive forensic analysis of EACH panel identified in step 2, documenting every visual element with Zero-Skip Protocol compliance.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 NEVER skip any panel from the index
- 📖 CRITICAL: Read the complete step file before taking any action
- 📖 READ RESOURCE: `{project-root}/studio/config/knowledge/hentai_lexicon.md` NOW
- ✅ YOU MUST speak in Vietnamese

### ZERO-SKIP PROTOCOL (CRITICAL)

```
FOR EACH PANEL:
- Every visible element MUST be documented
- If unclear, mark as **UNCLEAR** and provide 2 hypotheses
- Residue check is MANDATORY (hair, fluids, condoms)
```

### Step-Specific Rules

- 🎯 Analyze ONE panel at a time, in order
- 🚫 FORBIDDEN to skip panels or summarize multiple together
- 💬 Use clinical terminology, pervert eye perspective

## MANDATORY SEQUENCE

**CRITICAL:** Repeat this for EACH panel from the index.

### 1. Use Sequential Thinking for Each Panel - ATOMIC PROTOCOL

**MANDATORY:** Call `mcp_sequential-thinking_sequentialthinking` with minimum 8 thoughts PER PANEL:

```
Thought 1: VISUAL COMPOSITION
- Camera angle, shot type, focal point
- Depth layers (foreground, midground, background)
- Lighting, shadows, atmosphere

Thought 2: CHARACTER IDENTIFICATION
- Who is present, exact body positioning
- Pose analysis (submissive, dominant, neutral)
- Eye direction vs Head orientation

Thought 3: CLOTHING & ACCESSORIES FORENSIC (FAN SERVICE)
- Clothing state (% nude, specific items)
- Fabric texture/tension (thigh highs cutting into skin?)
- Disarray indicators (pulled down, shifted, torn)
- Accessories (glasses, ribbons, jewelry)

Thought 4: BODY STATE SCAN (ATOMIC)
- Skin texture: sweating zones, flushed areas, goosebumps
- Muscle tension: flexed/relaxed areas
- Body hair: pubic, armpit, visible hair anywhere

Thought 5: GENITAL/EROGENOUS SCAN (ATOMIC)
- Nipple state: visible? erect? wet?
- Genital visibility: visible? position? wetness?
- Arousal indicators: vein visibility, swelling

Thought 6: MICRO-EXPRESSION SCAN
- Eye direction, dilation, tears
- Mouth state (open, drooling, moaning)
- Facial muscles (pleasure, pain, anticipation)

Thought 7: HAND/FINGER ANALYSIS
- Exact hand positions on both characters
- What are fingers doing specifically?
- Grip strength indicators

Thought 8: FLUID TRACKING (ATOMIC)
- Saliva: where? strings? dripping?
- Sweat: droplets location, sheen?
- Sexual fluids: cum, arousal, where exactly?

Thought 9: RESIDUE & DEBRIS CHECKLIST (MANDATORY - REFER TO HENTAI LEXICON)
- **Check Category 1 (Protection):** Any condoms (wrapper/used)? WHERE?
- **Check Category 2 (Fluids):** Any white/clear/yellow patches on skin/floor/bed?
- **Check Category 5 (Environment):** Tissues? Trash? Stains on sheets?
- **Check Category 5 (Hair):** Any STRAY PUBIC HAIR (curly/black)? Check thighs/face.
- **Hypothesis Test:** For each category, ask: "Is it *really* empty, or am I missing a small detail?"
- **Conclusion:** List found items or state "None" explicitly.

Thought 10: NARRATIVE SEED & PSYCHO-ANALYSIS (NEW CORE PROTOCOL)
- **Initiative Check:** Who started this action? (Dominance/Submission/Training)
- **Hesitation Check:** Any sweat drops/trembling indicating fear vs eagerness?
- **Continuity Buffer:** How does this compare to the previous panel? (Corruption Arc?)
- **Psychological Beat:** "She is [Action] because she feels [Emotion] and wants [Goal]."
- **Drafting Seed:** Write a raw, vivid sentence capturing the *feeling* of this panel.
```

### 2. Document Each Panel

For EACH panel, create section in output file:

```markdown
### Panel {P#}: [Brief descriptive title]

#### 3A. Visual Composition
- **Camera Angle:** {eye-level / low / high / bird's eye / worm's eye}
- **Shot Type:** {extreme close-up / close-up / medium / full body / wide}
- **Focal Point:** {what draws the eye first}
- **Depth Layers:** 
  - Foreground: {describe}
  - Midground: {describe}
  - Background: {describe}

#### 3B. Character Analysis
| Character | Position | Pose | Expression | Clothing | Physical State |
|-----------|----------|------|------------|----------|----------------|
| {name/desc} | {where} | {pose} | {facial} | {state} | {sweat/blush/etc} |

- **Eye Direction:** {where they're looking}
- **Gaze Target:** {what/who they're looking at}

#### 3C. Micro-Details
- **Hands:** {position, gesture, what they're doing}
- **Skin:** {sweat, flush, goosebumps}
- **Fabric:** {tension, transparency, wrinkles}
- **Other:** {any micro-details}

#### 3D. Residue Check (ZERO-SKIP)
- **Pubic Hair:** {none visible / present at: location}
- **Fluids:** {none / drool at: / sweat at: / cum at:}
- **Condoms:** {none / present: state/location}
- **Other Residue:** {describe}

#### 3E. Action/Motion
- **Current Action:** {what is happening}
- **Motion Indicators:** {speed lines, blur effects}
- **Implied Next:** {what seems about to happen}

#### 3F. Narrative Analysis (NARRATIVE SEED)
- **Initiative:** {Who initiated? Active/Passive?}
- **Psychological State:** {Internal monologue guess based on visuals}
- **Corruption Arc:** {Progress from previous panel? E.g., Hesitation -> Acceptance}
- **Narrative Seed:** "{A raw, evocative sentence describing the moment using sensory language}"
```

### 3. Zero-Skip Verification Checklist

After EACH panel, verify:

- [ ] All characters identified
- [ ] All body positions documented
- [ ] Clothing states tracked
- [ ] Residue check completed
- [ ] No visible elements skipped

### 4. Continue Until All Panels Done

Repeat steps 1-3 for EVERY panel in the index.

Track progress: "**Panel {X}/{total} complete**"

### 5. Update Output File

After ALL panels analyzed:

- Append all panel breakdowns to `{outputFile}`
- Update frontmatter: `stepsCompleted: [..., 'step-03-panel-breakdown']`

### 6. Present MENU OPTIONS

Display:

```
"✅ Panel breakdown hoàn thành!

**Kết quả:**
- {total} panels analyzed
- Zero-Skip Protocol: COMPLIANT

**Tiếp theo:** Dialogue và text extraction

**Chọn:** [C] Continue to Dialogue Extraction"
```

#### Menu Handling Logic

- IF C: Save/update output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN ALL panels from the index have been analyzed with Zero-Skip compliance will you load and execute `{nextStepFile}`.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- Sequential thinking used per panel
- All panels from index analyzed
- Zero-Skip Protocol followed
- Residue check completed for each panel
- All characters and positions documented
- Output file contains all panel breakdowns

### ❌ SYSTEM FAILURE

- Skipping panels
- Summarizing multiple panels together
- Not checking for residue
- Missing character documentation
- Not using sequential thinking
- Incomplete panel sections

**Master Rule:** Every panel. Every detail. Every residue. Zero-Skip.
