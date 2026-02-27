---
name: 'step-05c-sensory-injection'
description: 'Mandatory secondary pass to inject Goonfy sensory details'

# Path Definitions
workflow_path: '{project-root}/studio/core/lewd-writer'
thisStepFile: './step-05c-sensory-injection.md'
nextStepFile: './step-06-aftermath-polish.md'
outputFile: '{output_folder}/_prose/{manga_name}/chapter_{ch}/page_{page_num}_prose.md'
---

# Step 5c: Sensory Injection Pass

## STEP GOAL

Perform a dedicated Secondary Pass over the drafted prose to strictly verify and inject extreme "Goonfy" sensory details (smells, wet sounds, textures, temperatures, and visceral bodily reactions) to ensure compliance with `sensory_density.md`.

## MANDATORY EXECUTION RULES (READ FIRST)

### The "AI Focus" Problem

When initially writing action choreography and dialogue, AI models often "forget" or drop sensory descriptors (smell, sound, temperature) to focus on the mechanical movements.
**This step forces you to artificially fix that drop-off.**

### Step-Specific Rules

- 🔍 Re-read the drafted prose so far.
- 📖 READ AND APPLY: `{project-root}/studio/rules/sensory_density.md`
- 🚫 FORBIDDEN to proceed if the page does not meet the minimum sensory counts.

## MANDATORY SEQUENCE

### 1. The Sensory Audit

Scan the current prose draft and count the explicit mentions of:

- **Smells** (Target: ≥3)
- **Wet Sounds** (Target: ≥3)
- **Textures** (Target: ≥5)
- **Temperatures** (Target: every bodily/fluid contact)
- **Visceral Bodily Reactions** (Target: ≥1 per climax/peak intensity)

### 2. The Injection Pass

If the prose falls short of ANY target, you MUST rewrite or inject new sentences into the existing draft to meet the quota.

**Injection Strategy (Gooner Lexicon):**

- **Inject Smells**: Add descriptions of *mùi nồng đặc trưng*, *mùi dâm thủy*, *mùi tinh dịch tanh mặn* into the breathing/panting moments.
- **Inject Sounds**: Add *bì bạch*, *chùn chụt*, *lép nhép* directly inside the action beats.
- **Inject Temperatures**: Add *nóng hổi*, *nóng rực*, *ấm nóng* whenever skin touches skin or fluid enters the body.
- **Inject Visceral Reactions**: Ensure characters have *mắt lờ đờ*, *ngón chân quắp chặt*, or *lưng ườn cong* during peak moments.

### 3. Update Frontmatter

Update `stepsCompleted` to include `step-05c-sensory-injection`.

```yaml
stepsCompleted: [..., 'step-05b-format-ensure', 'step-05c-sensory-injection']
```

---

## COMPLETION CHECK

- [ ] Have you successfully hit ≥3 smells, ≥3 wet sounds, and ≥5 textures?
- [ ] Are visceral bodily reactions explicitly described?
- [ ] Did you save the updated, sensory-dense prose?

If YES, proceed to `{nextStepFile}`.
