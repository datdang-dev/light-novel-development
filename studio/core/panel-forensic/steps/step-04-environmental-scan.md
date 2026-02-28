---
name: 'step-04-environmental-scan'
description: 'Phase 3: Environmental and Lewd Space Scanning'

nextStepFile: './step-05-final-report.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
---

# Step 4: Environmental & Lewd Scanning

## STEP GOAL

Now that the dialogue and character actions are strictly anchored from Phase 2, this phase evaluates the negative space: body details, fluid emissions, and environmental atmosphere necessary for R18 LND prose.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 Do NOT change the dialogue anchoring established in Step 03.
- 📖 CRITICAL: Read the complete step file before taking any action.
- ✅ YOU MUST speak in Vietnamese.
- 👁️ **GROUND TRUTH ONLY:** Only document fluids and bodily details that are *visibly drawn* on the page. Do not hallucinate based on tropes.

## MANDATORY SEQUENCE

### 1. Perform The Scans

Scan the image to fill out the following matrix templates. Be explicit and clinical.

```markdown
## Phase 3: Environmental & Lewd Matrix

### 3.1 Fluid & Excretion Scan
- **Fluids Present:** {Sweat / Tear / Drool / Semen / Pre-cum / Smegma / Dâm Thủy}
- **Locations Visually Confirmed:** {Detail exactly where the fluid is}
- **Viscosity/State:** {Dried, fresh, dripping, sticky}

### 3.2 Clinical Body Scan
- **Exposed Body Parts:** {Breasts, nipples, penis, vulva, anus}
- **Condition of Parts:** {Erect, flushed, bruised, covered in fluid}
- **Key Somatic Responses:** {Visible trembling, cross-legged squeeze (moji moji), pupil dilation, Ahegao}

### 3.3 Smell Matrix (Inferred from visuals)
- **Primary Odor Target:** {E.g., Smegma, sweat, unwashed cock, female arousal}
- **Visual Evidence for Smell:** {Text mentions of stench, visible stink/steam lines, character holding breath/sniffing}
```text

### 2. Update Output File

Append the "Phase 3: Environmental & Lewd Matrix" to the `{outputFile}`.
Update frontmatter: `stepsCompleted: [..., 'step-04-environmental-scan']`

### 3. Present MENU OPTIONS

Display:

```

"✅ Phase 3: Environmental & Lewd Scanning hoàn thành!

**Kết quả:**

- Môi trường và dịch tiết đã được đánh giá.

**Chọn:** [C] Continue to Phase 4: Final Report Assembly"

```

#### Menu Handling Logic

- IF C: Save/update output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

#### EXECUTION RULES

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.
