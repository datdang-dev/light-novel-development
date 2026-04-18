---
name: 'step-05b-format-ensure'
description: 'Enforce strict Light Novel formatting: header banner, dialogue, thoughts, SFX'

nextStepFile: './step-05c-sensory-injection.md'
outputFile: '{output_folder}/_prose/{manga_name}/chapter_{ch}/page_{page_num}_prose.md'
templateFile: '{project-root}/studio/_templates/light-novel-prose.md'
dialogueRulesFile: '{project-root}/studio/rules/dialogue_format.md'
---

# Step 5b: Ensure Format Compliance

## STEP GOAL

Strictly enforce ALL Light Novel formatting standards before polishing. This is a **HARD GATE** — prose CANNOT proceed to step-05c if any violation remains.

## ⚠️ CRITICAL: THIS IS A HARD GATE (ZERO TOLERANCE)

```
IF ANY FORMAT VIOLATION REMAINS AFTER FIXES:
  🚫 HALT — DO NOT PROCEED TO STEP-05c
  🔄 RE-SCAN until 100% clean
```

---

## SECTION 0: HEADER BANNER VALIDATION (MANDATORY)

### Required Structure

Every prose file MUST begin (after YAML frontmatter) with:

```markdown
# 📖 [Scene Title]

> **📍 Location:** [Location Name]
> **⏰ Time:** [Time of Day]
> **👤 POV:** [Character Name or "Ngôi thứ ba quan sát (Camera)"]

---
```

### Checks

- [ ] `# 📖` header present as first heading?
- [ ] `📍 Location:` line present?
- [ ] `⏰ Time:` line present?
- [ ] `👤 POV:` line present?
- [ ] `---` separator after header block?

### IF MISSING

Auto-inject the header from `{templateFile}`. Fill placeholders from forensic report context:

- Scene Title → derive from dominant action/setting
- Location → from forensic Section 1 (Panel Layout) or Section 10 (Continuity)
- Time → from forensic context or "Không xác định"
- POV → default to "Ngôi thứ ba quan sát (Camera)"

---

## SECTION 1: DIALOGUE BRACKETS (ZERO TOLERANCE)

### Rule

- **Spoken dialogue** MUST use `「...」` (Japanese corner brackets).
- **Character attribution** MUST precede dialogue: `Character_Name: 「Content」`
- **FORBIDDEN:** Standard quotation marks `""` or `""` for speech.

### Checks

- [ ] All spoken lines use `「...」`?
- [ ] All spoken lines have `Name:` prefix?
- [ ] No stray `"double quotes"` used for speech?

### Corrections

- ❌ `"Dừng lại!"` → ✅ `Character: 「Dừng lại!」`
- ❌ `Cô nói: "Content"` → ✅ `Character: 「Content」`

---

## SECTION 2: INTERNAL THOUGHTS

### Rule

- Internal monologues/thoughts MUST use parentheses `(...)`.
- **FORBIDDEN:** Italics `*text*` or quotes `""` for thoughts.

### Checks

- [ ] All thoughts in `(...)` format?
- [ ] No italics used for inner monologue?

### Corrections

- ❌ `*Hắn ta đang nhìn mình...*` → ✅ `(Hắn ta đang nhìn mình...)`
- ❌ `"Hắn ta đang nhìn mình..."` → ✅ `(Hắn ta đang nhìn mình...)`

---

## SECTION 3: SFX FORMAT VALIDATION

### Rule

- All sound effects MUST use italicized `*SFX: [Sound]*` format.
- SFX must be International Lewd SFX (English e.g., Plap, Splurt) OR Romaji (e.g., Guchu, Pan).
- **FORBIDDEN:** Do NOT use awkward Vietnamese onomatopoeia (e.g., bì bạch, nhẹp nhẹp).
- **FORBIDDEN:** Inline SFX without the `*SFX:` prefix.

### Checks

- [ ] All SFX lines start with `*SFX:`?
- [ ] No bare `*Pan Pan*` or `*Guchu*` without prefix?

### Corrections

- ❌ `*Basa... Basa...*` → ✅ `*SFX: Basa... Basa...*`
- ❌ `*Pan! Pan!*` → ✅ `*SFX: Pan! Pan!*`
- ❌ Inline `(*Bikun!*)` → ✅ Separate line: `*SFX: Bikun!*`

---

## SECTION 4: FOOTER SEPARATOR

### Rule

Every prose file MUST end with:

```markdown
---
***
```

### Check

- [ ] File ends with `---` followed by `***`?

---

## EXECUTION SEQUENCE

### 1. Load Content

Read the current state of `{outputFile}`.

### 2. Run All Checks (Sections 0-4)

Scan for ALL violations across all sections simultaneously.

### 3. Apply Fixes

For each violation found:

- Apply the documented correction
- Log what was fixed

### 4. Re-Scan (MANDATORY)

After all fixes applied, re-scan the entire file to confirm zero violations remain.

```
IF violations_remaining > 0:
  🚫 HALT — Re-apply fixes
  LOOP until clean

IF violations_remaining == 0:
  ✅ Format gate PASSED
  Proceed to step-05c
```

### 5. Update Frontmatter

```yaml
stepsCompleted: [..., 'step-05b-format-ensure']
```

---

## COMPLETION CHECKLIST

- [ ] Header Banner present and complete?
- [ ] All dialogue inside `「...」` with `Name:` prefix?
- [ ] All thoughts inside `(...)`?
- [ ] All SFX in `*SFX: ...*` format?
- [ ] Footer separator present?
- [ ] Re-scan confirms zero violations?
- [ ] File saved with corrections?

**ALL boxes must be checked. If ANY is unchecked → HALT.**

If ALL checked → proceed to `{nextStepFile}`.
