---
name: 'step-03-environment-prose'
description: 'Write setting and atmosphere prose'

# Path Definitions
workflow_path: '{project-root}/studio/core/lewd-writer'
thisStepFile: './step-03-environment-prose.md'
nextStepFile: './step-04-action-prose.md'
---

# Step 3: Environment Prose

## STEP GOAL:

Write immersive setting and atmosphere prose that grounds the reader in the scene using the SETUP beats.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ Write prose in {document_output_language} (Vietnamese)

### OBSERVER-CAMERA Perspective:

```
Write as external observer:
- Describe environment like a camera panning
- Include ambient sensory details
- No character internal monologue yet
- Clinical but evocative
```

### Step-Specific Rules:

- 🎯 Focus on SETUP beats only (environment, initial positioning)
- 🚫 FORBIDDEN to jump to action content
- 💬 Establish atmosphere before any explicit content

## MANDATORY SEQUENCE

### 1. Write Setting Paragraph

From forensic environment data, create:

```markdown
## Prose Content

### Setting Establishment

[Write 1-2 paragraphs establishing:]
- Physical space (room, outdoor, vehicle, etc.)
- Lighting conditions
- Ambient sounds
- Ambient smells
- Temperature/atmosphere
- Time of day indicators
```

**Sensory Checklist for Setting:**
- [ ] At least 1 smell mention
- [ ] At least 1 ambient sound
- [ ] At least 1 texture/temperature feel

### 2. Write Character Entry/Positioning

From forensic character data:

```markdown
### Character Introduction

[Write character positioning prose:]
- Where each character is located
- What they're wearing (current state)
- Body language (from forensic pose data)
- Initial expressions
```

### 3. Write Tension Buildup

Bridge from SETUP to BUILD beats:

```markdown
### Tension Establishment

[Write transition prose:]
- Subtle shifts in atmosphere
- Eye contact moments
- Breathing changes
- Anticipation indicators
```

### 4. Verify Sensory Density

Check progress:

```
Environment Section Sensory Count:
- Smell: {count} (target: ≥1)
- Sound: {count} (target: ≥1)  
- Texture: {count} (target: ≥2)
```

### 5. Update Output File

Append environment prose to output:
- Update frontmatter: `stepsCompleted: [..., 'step-03-environment-prose']`

### 6. Present MENU OPTIONS

```
"✅ Environment prose hoàn thành!

**Paragraphs:** {count}
**Sensory elements:** {count}

**Sample:**
> {first 1-2 sentences}

**Tiếp theo:** Action prose writing

**Chọn:** [R] Revise environment [C] Continue to Action Prose"
```

#### Menu Handling Logic:

- IF R: Ask what to revise, make changes, redisplay menu
- IF C: Save/update output file, load `{nextStepFile}`

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Setting established with sensory detail
- Characters positioned
- Atmosphere created
- OBSERVER-CAMERA perspective maintained
- Smooth transition to action setup

### ❌ SYSTEM FAILURE:

- Jumping straight to explicit content
- No sensory details in setting
- Internal monologue instead of observation
- Missing environmental grounding

**Master Rule:** Ground the reader first. Atmosphere enables immersion.
