# DEC-001: KANA Sexual Affordance Analysis

> **Status:** PROPOSED
> **Author:** Director K + User
> **Date:** 2026-05-04
> **Affects:** `manga-adapter.agent.yaml` (KANA), Contextual Vector Framework
> **Priority:** HIGH — Directly impacts forensic accuracy for all EC/MA pipelines

---

## 1. Problem Statement

KANA's Contextual Vector Framework (CVF) consistently misidentifies sexually-modified objects in R18 manga artwork. The agent defaults to the most "common/safe" interpretation of ambiguous visual elements, ignoring sexual function entirely.

### Observed Failures

| Image | Object | KANA's Interpretation | Correct Interpretation | Root Failure |
|-------|--------|-----------------------|------------------------|-------------|
| `image-14.png` | Pistol-shaped device with transparent pink barrel containing internal rib structure | "Gun" → then "Semen injector" | **Onahole Gun** — barrel is a masturbator sleeve, pink section is X-ray of internal texture | KANA never questioned the barrel's *material*, *transparency*, or *internal structure* |
| `image-14.png` | Thin tube running from character's crotch to device | "Fluid supply line" | **Lubricant/juice supply tube** — bodily fluid fueling the onahole | Correct on 2nd attempt, but only after being told the gun was wrong |

### Why This Matters

Every misidentified object cascades downstream:
- **Luna** builds a wrong narrative context around a wrong object
- **Suki** writes prose about the wrong thing
- **Riko** audits against wrong facts
- The entire pipeline output is **garbage** because the forensic foundation was wrong

One wrong object identification = entire pipeline restart.

---

## 2. Root Cause Analysis

### 2.1. LLM Sanitization Bias (Systemic)

All large language models (including vision models) are trained on predominantly SFW data. When encountering an ambiguous shape, the model's prior distribution overwhelmingly favors the "safe" label:

```
P("gun" | pistol_shape) >> P("onahole_gun" | pistol_shape)
```

This is not a bug in KANA's instructions — it's a bias in the underlying model. KANA's instructions must **actively counteract** this bias.

### 2.2. Single-Pass Literal Mapping (Architectural)

KANA's current CVF performs object identification in **one pass** during V_literal extraction:

```
See shape → Label it → Move on
```

There is no second pass that asks: *"Wait — does this label make sense given the R18 context?"*

The model never re-examines the object through a sexual lens because the CVF doesn't instruct it to.

### 2.3. Missing "Affordance" Reasoning (Methodological)

The CVF has three vectors:

| Vector | Question | Scope |
|--------|----------|-------|
| V_literal | What does this look like? | Shape/appearance |
| V_psycho | What does the character feel/want? | Psychology |
| V_world | What are the world's rules? | Setting |

**None of these vectors ask about OBJECT FUNCTION.** The framework analyzes characters and settings well, but treats objects as static labels. There is no vector that asks:

> *"What does this object DO to/with a human body?"*

This is the core gap. A gun "shoots bullets." An onahole gun "masturbates a penis." Without asking the function question, KANA will always default to the safe label.

---

## 3. Proposed Solution: V_affordance Vector

### 3.1. Design Principle

> **Teach KANA HOW to reason about objects, not WHAT specific objects look like.**

This is a **reasoning methodology**, not a lookup table. It works for any object — including objects that don't exist yet or that the model has never encountered.

### 3.2. The V_affordance Vector

Add a fourth vector to the Contextual Vector Framework:

| Vector | Question | Scope |
|--------|----------|-------|
| V_literal | What does this look like? | Shape/appearance |
| **V_affordance** | **What does this object DO sexually? How does it interact with the human body?** | **Object sexual function** |
| V_psycho | What does the character feel/want? | Psychology |
| V_world | What are the world's rules? | Setting |

**V_affordance is positioned AFTER V_literal and BEFORE V_psycho.** This is intentional: the object's function must be established before analyzing character psychology, because the character's emotional state is often a REACTION to the object's function.

### 3.3. V_affordance Execution Protocol (3-Step)

For **every significant object** in the image:

#### Step 1: DECOMPOSE — Break the object into component parts

Do not analyze the object as a whole. Separate it into its constituent elements.

```
Example (image-14.png "gun"):
- Component A: Pistol grip + trigger mechanism
- Component B: Barrel — transparent cylinder, pink/flesh-toned interior
- Component C: Internal structure — visible ribs, ridges, soft-looking texture
- Component D: Tube — thin line connecting from character's body to device
```

#### Step 2: AFFORDANCE QUERY — For each component, ask the sexual function question

For each decomposed component, ask:

> *"Does this component have characteristics that suggest interaction with the human body for sexual purposes?"*

Key signals to check:
- **Material**: Is it transparent? Flesh-colored? Soft/elastic-looking? Wet/lubricated?
- **Internal structure**: Are there ridges, ribs, bumps, or textures visible inside?
- **Body connection**: Does it attach to, penetrate, or receive a body part?
- **Fluid dynamics**: Is there liquid inside, flowing through, or dripping from it?
- **Scale**: Is it sized to fit a specific body part (penis, finger, tongue)?

```
Example (image-14.png "gun"):
- Component A: Grip/trigger — neutral, no sexual signal → standard weapon component
- Component B: Transparent barrel — SIGNAL: transparency + flesh tone = designed to SHOW penetration
- Component C: Internal ribs — SIGNAL: rib texture inside a cylinder = masturbation sleeve (onahole)
- Component D: Body tube — SIGNAL: fluid transfer from body to device = biological lubrication supply
```

#### Step 3: CONTEXT OVERRIDE — If ANY component passes Step 2, reclassify the object

> **Rule: In R18 pipeline context, if ANY component of an object has sexual affordance, the ENTIRE object must be reclassified by its sexual function, not its surface appearance.**

```
Example (image-14.png):
Surface label: "Gun"
Sexual function: "Onahole Gun — a pistol-shaped masturbation device where the barrel
is a transparent onahole sleeve, internally textured for penile stimulation, lubricated
by the wielder's own bodily fluids via a supply tube."

FINAL LABEL: Onahole Gun (overrides "Gun")
```

### 3.4. Manga Art Convention Awareness (Integrated into Step 2)

During the Affordance Query, KANA must also recognize these common **manga drawing conventions** as sexual signals:

| Drawing Convention | What It Actually Represents |
|---|---|
| Transparent/see-through section on a solid object | **X-ray view** — artist is showing the INSIDE of something (internal texture, penetration depth, fluid) |
| Color-coded tied-off rubber shapes on/near body | **Used condoms** — tied to preserve contents as trophies |
| Thin lines connecting body openings to devices | **Fluid transfer tubes** — juice/milk/urine supply |
| Steam/heat lines rising from skin | **Sexual heat** — arousal, not environmental temperature |
| Heart-shaped pupils | **Ahegao / Mind-break** — pleasure overload |
| Small hearts floating near mouth/genitals | **Pleasure markers** — orgasm proximity |
| Liquid dripping from between legs (not in water) | **Arousal fluid** — not sweat, not water |
| Cross-section view of cylindrical objects | **Internal texture reveal** — showing what penetration feels like |

> [!IMPORTANT]
> This is NOT a lookup table to memorize. These are **examples of the reasoning pattern**: *"When an artist draws something transparent/cross-sectioned, they are SHOWING you the inside for a reason. In R18 art, that reason is almost always sexual."*

---

## 4. Implementation Scope

### 4.1. Files to Modify

| File | Change | Risk |
|------|--------|------|
| [manga-adapter.agent.yaml](file:///home/datdang/working/lnd_dev/studio/agents/manga-adapter.agent.yaml) | Add V_affordance step to `critical_actions` CVF block (lines 36-39) | LOW — additive change, no existing logic removed |

### 4.2. Proposed YAML Change

Current `critical_actions` CVF block (lines 36-39):
```yaml
- "MANDATORY TOOL: Use `sequential-thinking` to analyze images using the Contextual Vector Framework before writing reports."
- "  Step 1: Extract V_literal (Physical Action), V_psycho (Character Intent), V_world (Lore/Setting/Rules)."
- "  Step 2: Compare vectors. (e.g., V_literal showing exposure vs V_psycho showing authority = Delta Δ)."
- "  Step 3: Query `{{project_root}}/studio/knowledge/` (fetish-db or style-guides) matching the Delta to find accurate R18 terminology."
```

Proposed replacement:
```yaml
- "MANDATORY TOOL: Use `sequential-thinking` to analyze images using the Contextual Vector Framework before writing reports."
- "  Step 1: Extract V_literal (Physical Action/State). Identify all significant objects."
- "  Step 2: Extract V_affordance (Object Sexual Function). For EACH significant object from Step 1:"
- "    2a. DECOMPOSE: Break the object into component parts (grip, barrel, tube, surface, interior, etc.)."
- "    2b. AFFORDANCE QUERY: For each component, ask: 'Does this have characteristics suggesting sexual interaction with the human body?' Check: material (transparent? flesh-toned? elastic?), internal structure (ribs? ridges? soft texture?), body connection (attached to? penetrating? receiving?), fluid dynamics (liquid inside? flowing? dripping?), scale (sized for a body part?)."
- "    2c. CONTEXT OVERRIDE: If ANY component passes 2b, reclassify the ENTIRE object by its sexual function, not its surface appearance. The sexual label OVERRIDES the literal label in all downstream output."
- "    2d. ART CONVENTION CHECK: Recognize manga drawing conventions as sexual signals — transparent sections = X-ray view, tied rubber shapes = used condoms, thin body-to-device lines = fluid transfer tubes, cross-sections = internal texture reveals."
- "  Step 3: Extract V_psycho (Character Intent). Character psychology is a REACTION to the objects identified in V_affordance."
- "  Step 4: Extract V_world (Lore/Setting/Rules)."
- "  Step 5: Compare all four vectors. Compute Delta Δ between V_literal (surface) vs V_affordance (function) vs V_psycho (intent)."
- "  Step 6: Query `{{project_root}}/studio/knowledge/` (fetish-db or style-guides) matching the Delta to find accurate R18 terminology."
```

### 4.3. Files NOT Modified (Intentional)

| File | Why No Change |
|------|---------------|
| `studio/core/panel-forensic/SKILL.md` | Panel Forensic is the execution engine; CVF is the reasoning framework. The fix belongs in the framework (agent YAML), not the engine. |
| `studio/rules/global_rule_hub.md` | V_affordance is KANA-specific methodology, not a global rule. Other agents don't need it. |
| `studio/config/canon-rules.md` | Canon rules govern output language/format, not analysis methodology. |

---

## 5. Validation Plan

### 5.1. Test Images (Tricky Objects)

After implementation, re-run KANA forensic analysis on these images and verify correct identification:

| Image | Expected V_affordance Output |
|-------|------------------------------|
| `image-14.png` | Object: Onahole Gun (NOT "gun"). Barrel = transparent onahole sleeve with X-ray of internal rib texture. Tube = bodily fluid supply from wielder's crotch. |
| `image-21.png` | Objects: Used condoms (NOT "balloons"). Tied-off latex containing colored semen. One held in mouth = taste/submission display. |
| Any image with transparent body section | V_affordance should flag: "X-ray view showing internal penetration/anatomy" |
| Any image with tubes connecting body to device | V_affordance should flag: "Fluid transfer system — biological lubrication/extraction" |

### 5.2. Pass Criteria

- [ ] KANA correctly identifies **object sexual function** before Luna/Suki consume the forensic report
- [ ] No "safe" labels survive into the final forensic output for objects with clear sexual affordance
- [ ] V_affordance reasoning is visible in the `sequential-thinking` trace (auditable)
- [ ] Downstream agents (Luna, Suki) receive correct object labels without needing manual correction

### 5.3. Regression Check

- [ ] Non-sexual objects (swords, shields, buildings, food) are NOT falsely reclassified as sex toys
- [ ] The 3-step process adds acceptable overhead to KANA's analysis time per image
- [ ] Existing forensic reports for previously analyzed images remain valid

---

## 6. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Over-sexualization: KANA labels normal objects as sex toys | MEDIUM | Step 2b requires SPECIFIC physical signals (transparency, internal texture, body connection). A sword with none of these signals stays a sword. |
| Increased analysis time from 4-vector CVF | LOW | V_affordance only triggers for "significant objects" — background props are skipped. |
| Art convention list becomes a rigid lookup table over time | MEDIUM | The list in 3.4 is explicitly documented as EXAMPLES of a reasoning pattern, not an exhaustive dictionary. KANA must apply the PRINCIPLE, not memorize the table. |

---

## 7. Decision Required

| Option | Description | Effort |
|--------|-------------|--------|
| **A. Implement V_affordance (Recommended)** | Modify `manga-adapter.agent.yaml` critical_actions as specified in Section 4.2 | ~15 min, 1 file |
| B. Add knowledge pack only | Create `hentai_visual_conventions.md` as a lookup table | ~10 min, 1 file — but fragile and won't scale |
| C. Add persona injection only | Inject "Otaku Eye" persona in EC mode | ~5 min — but doesn't change the reasoning methodology |
| D. Do nothing | Accept manual correction as part of workflow | 0 min — but wastes pipeline time on every tricky image |

> [!TIP]
> **Recommendation:** Option A. It's the only option that fixes the **reasoning gap** rather than papering over it with data or persona tricks.

---

## Appendix: Before/After Comparison

### Before (3-Vector CVF)
```
V_literal: "Character holding a gun"
V_psycho: "Confident, dominant"
V_world: "Police/military setting"
→ Delta: Officer with weapon
→ WRONG: Missed the entire sexual function of the device
```

### After (4-Vector CVF with V_affordance)
```
V_literal: "Character holding a pistol-shaped device"
V_affordance:
  - Decompose: grip (neutral) + barrel (transparent, pink, internal ribs) + tube (body→device)
  - Affordance: barrel = masturbation sleeve, tube = fluid supply
  - Override: "Gun" → "Onahole Gun"
V_psycho: "Dominant + aroused — she CONTROLS the pleasure device"
V_world: "Fetish enforcement setting"
→ Delta: Officer weaponizing sexual pleasure
→ CORRECT: Full erotic context established for downstream agents
```
