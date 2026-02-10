# 📋 LND Team — Lessons Learned & Best Practices

> **CRITICAL**: All agents MUST read this file before starting any new project.
> Last Updated: 2026-02-04

> [!CAUTION]  
> **🚨 PROSE OUTPUT LANGUAGE RULE 🚨**
> - **ALL DIALOGUE = VIETNAMESE** (dirty talk style)
> - **SFX = English (Plap, Splurt) OR Romaji (kupaa~, biku!, siko siko)**
> - **NEVER use ideographic characters (ひらがな/カタカナ/漢字/中文) in prose**
> - Source language is for FORENSICS ANALYSIS ONLY

---

## 🛑 WHAT TO STOP (Anti-Patterns)

### 1. ❌ Default to First-Person POV
**Problem**: Assuming 1st person POV (ojisan POV, character POV) without confirmation.
**Rule**: Always confirm POV with user BEFORE writing.
**Default**: Use 3rd person camera POV unless specified otherwise.

### 2. ❌ Skip Erotic Detail Analysis
**Problem**: Missing visual elements like used condoms, pubic hair, fluid distribution.
**Rule**: Check "Evidence of Use" checklist before prose writing.

### 3. ❌ Assume Character Context
**Problem**: Not checking if character is recurring (Dat, etc.) or new.
**Rule**: Query character database or ask user about character history.

### 4. ❌ Surface-Level Forensics
**Problem**: Generic image analysis missing key erotic elements.
**Rule**: Use multi-phase forensics: Overview → Erotic Details → Sensory.

### 5. ❌ Rush to Deliver
**Problem**: Completing scene without verification, causing rewrites.
**Rule**: Use pre-flight checklist before writing prose.

### 6. ❌ Keep Source Language in Output
**Problem**: Manga source is Chinese/Japanese, but output includes raw 日本語 or 中文 dialogue.
**Example (WRONG)**: `「為什麼我會在做這種事...」` in prose output
**Example (CORRECT)**: `「Tại sao... em lại đang làm chuyện này...」`
**Rule**: 
- **Forensics stage**: May note original dialogue for reference
- **Prose output**: ALL dialogue MUST be Vietnamese + dirty talk

### 7. ❌ Keep Non-Latin SFX
**Problem**: Using Japanese katakana SFX (ビュルルッ) or Chinese onomatopoeia directly in prose.
**Rule**: Convert SFX to Latin/romanized form OR Vietnamese phonetic equivalent.

### 8. ❌ Use Awkward Vietnamese Onomatopoeia for Sex SFX
**Problem**: Vietnamese SFX like "bì bạch", "nhẹp nhẹp" sound awkward/cringe ("lỏ") to readers.
**Example (WRONG)**: `*Bì bạch. Bì bạch. Âm thanh da thịt đập vào nhau.*`
**Example (CORRECT)**: `*Plap. Plap. Plap.*`
**Rule**: Use **international lewd SFX** vocabulary:

| Action | SFX |
|--------|-----|
| Thrusting | Plap, Clap, Smack |
| Deepthroat | Glurk, Gluk |
| Wet pussy | Schlick, Squelch |
| Cum ejaculation | Splurt, Spurt |
| Impact/slap | Smack, Thwack |
| Impact/slap | Smack, Thwack |

**Rationale**: Gooner target audience is familiar with English/romanized hentai SFX from doujinshi translations.

### 9. ❌ Visual Hallucination (Guessing Content)
**Problem**: Generating forensics or prose without explicitly viewing the image file first.
**Root Cause**: Assuming content based on file names, context, or previous patterns (e.g., guessing "spanking" from a "punishment" file name).
**Rule**: **ZERO HALLUCINATION PROTOCOL**
1. **MANDATORY**: Use `view_file` on the target image(s) BEFORE writing any description.
2. **VERIFICATION**: You must be able to cite specific visual details (colors, accessories, background) that are only visible by looking.
3. **NO GUESSING**: If you can't see it, ask the user or run a tool to make it visible. 
4. **PENALTY**: Any hallucinated content is an immediate failure of the LND protocol.

### 10. ❌ Combine Multiple Pages Into Single File

**Problem**: Grouping pages like 006-007, 009-011, or 012-014 into single forensics/prose files.
**Root Cause**: LLM optimizing for "narrative continuity" over workflow compliance. Agent sees continuous scene → decides to batch for "better flow".
**Example (WRONG)**: `page_009-011.md` containing prose for 3 pages
**Example (CORRECT)**: `page_009.md`, `page_010.md`, `page_011.md` as separate files
**Rule**: **ATOMIC PAGE PROCESSING**

1. **1 Page = 1 Forensics file = 1 Prose file** (ZERO exceptions)
2. File naming: `page_XXX.md` where XXX is zero-padded (001, 002, etc.)
3. NEVER use ranges in filenames (page_005-008.md is PROHIBITED)
4. Even if pages belong to same scene, each page must be separate

**Rationale**:

- Atomic units enable precise progress tracking
- Individual page revision without affecting others
- Proper evidence chain in handover schemas
- Consistent QA audit per page

---

## 🚀 WHAT TO START (New Practices)

### 1. ✅ Visual Detail Checklist

Before writing prose, ALWAYS check for:
- [ ] Condoms (used, scattered, color, quantity)
- [ ] Body hair (pubic hair on thighs, source identification)
- [ ] Fluid distribution (fresh/dried, layers, locations)
- [ ] Outfit state (pulled aside, bunched, stained)

### 2. ✅ POV Confirmation

Ask user BEFORE writing:
```
「Anh muốn POV nào~?
1. 3rd person camera (default)
2. Specific character POV
3. Other」
```

### 3. ✅ Character Database Lookup
Check if character exists in:
- `bible/characters.md` in project folder
- Previous scenes in same project
- `studio/docs/` for global characters

### 4. ✅ Multi-Phase Forensics
```
Phase 1: OVERVIEW
├── Scene type, setting, character count
└── Mood, lighting, composition

Phase 2: EROTIC DETAILS
├── Evidence of use (condoms, fluids, hair)
├── Outfit state (pulled, stained, wet)
└── Physical condition (sweat, exhaustion)

Phase 3: SENSORY EXTRACTION
├── Smell (minimum 5 sources)
├── Sound (minimum 4 sources)
├── Texture (minimum 4 surfaces)
└── Temperature mentions
```

### 5. ✅ Pre-Flight Checklist
MANDATORY before writing:

```markdown
## Pre-Flight Checklist

### Context ✅
- [ ] POV confirmed? (3rd camera / 1st person / specific character)
- [ ] Main character identified? (New or recurring?)
- [ ] Setting established? (Location, time, atmosphere)

### Forensics Complete ✅
- [ ] Character appearance detailed?
- [ ] Outfit state described? (Normal, disheveled, removed)
- [ ] Evidence of use? (Condoms, fluids, body hair)
- [ ] Sensory matrix filled?

### Erotic Elements ✅
- [ ] Cum distribution mapped?
- [ ] Used protection noted?
- [ ] Physical evidence (hair, stains) noted?
- [ ] Smell profile complete?

### Ready to Write ✅
- [ ] All above checked
- [ ] User requirements clear
- [ ] No ambiguity remaining
```

---

## ✨ WHAT TO CONTINUE (Good Practices)

### 1. ✅ Forensic Table Format
Keep using tables for structured analysis:
```markdown
| Element | Description |
|---------|-------------|
| **Item** | Detail |
```

### 2. ✅ Sensory Density Targets
- Smell: ≥5 sources
- Sound: ≥4 sources
- Texture: ≥4 surfaces
- Temperature: ≥2 mentions

### 3. ✅ Dialogue Format
Continue using:
- 「」for Japanese-style dialogue
- Vietnamese + Wibu mix
- SFX in *italics*

### 4. ✅ Project Organization
```
project_name/
├── README.md
├── source_images/
├── forensics/
├── prose/
└── bible/
```

### 5. ✅ Master README Updates
Always update `standalone_lnd/README.md` when creating new project.

---

## 📊 Quality Metrics

### Acceptable Thresholds
| Metric | Target | Minimum |
|--------|--------|---------|
| Rewrite Rate | <20% | <30% |
| Sensory Count (Smell) | ≥5 | ≥3 |
| Sensory Count (Sound) | ≥4 | ≥3 |
| Audit Score | ≥85/100 | ≥80/100 |

### Red Flags (Immediate Action)
- Rewrite requested due to POV mismatch → POV confirmation skipped
- User corrects erotic details → Forensics incomplete
- Scene lacks continuity → Character database not checked

---

## 🔗 Agent-Specific Notes

### For Suki (Lewd Writer)
- ALWAYS check forensics first
- Verify POV BEFORE writing
- Reference character database for voice consistency

### For Riko (QA Editor)
- Check "Evidence of Use" section exists
- Verify sensory density meets targets
- Flag missing erotic elements

### For Aria (Character Architect)
- Update character database after creating profiles
- Note recurring character traits
- Track physical state changes between scenes

### For Director K (Orchestrator)
- Run pre-flight checklist before delegating to Suki
- Verify forensics complete before prose phase
- Ask clarifying questions if ambiguous

---

## 📝 Retrospective History

### Sprint 2026-02-01
**Issues Found:**
- 50% rewrite rate (2/4 scenes)
- Root cause: Insufficient initial requirement gathering

**Actions Taken:**
- Created this lessons-learned document
- Defined pre-flight checklist
- Mandated POV confirmation

---

> **Next Agent**: If you learn something new, ADD IT HERE.
> This is a living document.
