---
name: 'step-02-scene-planning'
description: 'Plan escalation loops and scene structure'

# Path Definitions
workflow_path: '{project-root}/studio/core/lewd-writer'
thisStepFile: './step-02-scene-planning.md'
nextStepFile: './step-03-environment-prose.md'
---

# Step 2: Scene Planning

## STEP GOAL

Create a structured scene plan with clear escalation loops and beat tracking before writing prose.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Step-Specific Rules

- 🎯 Focus on PLANNING only, no prose writing
- 🚫 FORBIDDEN to skip the escalation loop structure
- 💬 Map each panel to a scene beat

## MANDATORY SEQUENCE

### 1. Map Panels to Narrative Beats (SKEPTIC PROTOCOL ACTIVE)

**SKEPTIC CHECK:** Before mapping, ask: "Does the Forensic Data match the Corruption Arc?"

- If Forensic says "Smiling" but context is "Pain", TRUST CONTEXT.
- If Forensic says "No fluids" but action is "Ejaculation", INFER FLUIDS.

**DIRECTOR ALIGNMENT:** Review "Director Vision" from Context Summary.

- Does the mapping serve the Director's request? (e.g. "More aggressive" -> Ensure aggressive beats).
- If Vision contradicts Forensic data, PRIORITIZE VISION for tone/style.

Create a beat map from forensic panel data:

```markdown
## Scene Structure

### Panel-to-Beat Mapping

| Panel | Beat Type | Escalation Level | Purpose |
|-------|-----------|------------------|---------|
| P1 | SETUP | 1/10 | Environment establishment |
| P2 | BUILD | 3/10 | Tension introduction |
| P3 | BUILD | 5/10 | Physical approach |
| P4 | ACTION | 7/10 | First contact moment |
| P5 | CLIMAX | 10/10 | Peak intensity |
| P6 | AFTERMATH | 4/10 | Recovery/consequence |
```

### 2. Define Escalation Loops

Identify escalation patterns:

```markdown
### Escalation Loop Structure

**Loop 1: Setup → First Peak**
- Panels: P1-P3
- Build from: {state}
- Peak at: P3
- Sensory focus: {dominant sense}

**Loop 2: Main Action → Climax**
- Panels: P4-P5
- Build from: {state}
- Peak at: P5
- Sensory focus: {dominant sense}

**Aftermath Section**
- Panels: P6+
- Focus: {residue, consequence, continuation setup}
```

### 3. Plan Sensory Distribution AND Palette

**Define the SENSORY PALETTE for this scene:**

- **Smell:** {e.g., Sweat, Semen, Cheap Perfume}
- **Sound:** {e.g., Wet slapping, Heavy breathing, Bed creaking}
- **Taste:** {e.g., Salty skin, Metallic blood, Sweet saliva}
- **Temperature:** {e.g., Stifling heat, Cold floor, Burning friction}

Pre-plan where sensory elements will go:

```markdown
### Sensory Planning

**Palette:** [Smell: {smell}] [Sound: {sound}] [Touch: {touch}]

| Sense | Target Count | Planned Locations |
|-------|--------------|-------------------|
| Smell | ≥3 | P2: initial, P4: intense, P6: aftermath |
| Sound | ≥3 | P3: SFX, P4: dialogue, P5: climax sounds |
| Texture | ≥5 | P1: fabric, P2: skin, P3: moisture, P4+: action |
```

### 4. Character Voice Planning

From bible or forensics, establish:

```markdown
### Character Voices

**{Character A}:**
- Speech pattern: {formal/crude/etc}
- Dialogue style: {demanding/pleading/etc}
- Key phrases: {established}

**{Character B}:**
- Speech pattern: {description}
- Dialogue style: {description}
- Key phrases: {established}
```

### 5. Update Output File

Append scene structure to output file:

- Update frontmatter: `stepsCompleted: [..., 'step-02-scene-planning']`

### 6. Present MENU OPTIONS

```
"✅ Scene planning hoàn thành!

**Escalation Loops:** {count}
**Peak Panel:** P{X}
**Sensory Distribution:** Planned

**Tiếp theo:** Environment prose writing

**Chọn:** [C] Continue to Environment Prose"
```

#### Menu Handling Logic

- IF C: Save/update output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- All panels mapped to beats
- Escalation loops defined
- Sensory distribution planned
- Character voices noted
- Structure documented

### ❌ SYSTEM FAILURE

- Skipping panel mapping
- No escalation planning
- Starting prose without structure
- Missing sensory pre-planning

**Master Rule:** Structure before prose. Plan the escalation.
