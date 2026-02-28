---
description: "MOD Protocol — Suki's Enhanced Prose Modding System"
version: "1.0.0"
---

# MOD Protocol — Suki (lewd-writer)

> **Purpose:** Take existing canonical prose and create an enhanced "Director's Cut" version that is more compelling, more lewd, and more sensory-dense — without derailing the original plot.

---

## 1. Activation

The MOD system is triggered by Director K or the Boss with:

```
MOD page-XXX [, Tier N] [, FOCUS: TAG]
```

**Examples:**

- `MOD page-004` → Default Tier 2 (EXPAND), no specific focus
- `MOD page-006, Tier 3` → REIMAGINE level
- `MOD page-009, FOCUS: PSYCHOLOGY` → Focused on inner thoughts

---

## 2. MOD Tiers

| Tier | Name | Canon Retention | Allowed Additions |
|---|---|---|---|
| **Tier 1** | `ENHANCE` | ~95% | Expand sensory descriptions, add SFX, enrich existing dialogue. No new plot elements. |
| **Tier 2** | `EXPAND` | ~70% | Add new dialogue lines, internal thoughts, action beats, environmental reactions. Default tier if unspecified. |
| **Tier 3** | `REIMAGINE` | ~50% | Add sub-scenarios, new character reactions, extended aftermath, "what if" branches. Must preserve core plot direction. |

---

## 3. Focus Tags (Optional)

| Tag | Description |
|---|---|
| `DIALOGUE` | Add/upgrade dirty talk, power-dynamic lines, verbal degradation |
| `SENSORY` | Maximize smell, taste, touch, heat, moisture descriptions |
| `PSYCHOLOGY` | Inner monologue, rationalization, denial, gap moe, mental breakdown |
| `AFTERMATH` | Extend post-climax: residue, exhaustion, contamination, lingering effects |
| `SCENARIO` | Add situational elements (interruption, discovery, escalation trigger) |

If no focus tag is given, Suki applies her creative judgment to choose the most impactful enhancement.

---

## 4. Output Format

### 4.1 File Naming

```
page-XXX.mod.md      ← MOD version (separate file)
page-XXX.md          ← Original CANON (NEVER modified)
```

### 4.2 MOD Prologue Header

Every MOD file MUST start with this prologue block before the standard template:

```markdown
> **MODDED** page: XXX
> **Tier:** [ENHANCE | EXPAND | REIMAGINE]
> **Focus:** [Tag or "General"]
> **Changes:** [Summary of what was added/changed]
> **Canon Diff:** +N dialogue lines, +N action beats, +N SFX, +N internal thoughts
```

### 4.3 Body

After the prologue, the MOD file follows the same **Light Novel Standard** template as canonical prose:

- `---` YAML frontmatter
- `# 📖 Title` (can be different from original)
- Metadata block (Location, Time, POV)
- Vietnamese section headers `### [Name]`
- 「」 for dialogue, `()` for thoughts
- `*SFX: ...*` formatting
- Continuity State table at EOF

---

## 5. Creative Protocol — How Suki Thinks During MOD

### 5.1 Read Phase

1. Read the **original prose** (page-XXX.md) completely
2. Read the **forensic report** (page-XXX-forensic.md) for raw data
3. Identify the **Dialogue Anchor Matrix** — all original dialogue lines

### 5.2 Analysis Phase

4. Ask: *"What is the emotional/arousal peak of this page?"*
2. Ask: *"Where does the original prose feel thin or rushed?"*
3. Ask: *"What sensory channels are underrepresented?"* (Smell? Touch? Sound?)
4. Ask: *"What would a gooner reader WANT to see expanded?"*

### 5.3 Creation Phase

8. Write the MOD version using the tier-appropriate level of enhancement
2. **MANDATORY:** Preserve all original dialogue lines (can rephrase, but cannot delete)
3. **MANDATORY:** Do not introduce new characters not present in the source material
4. **MANDATORY:** Do not change the plot outcome or timeline
5. **ALLOWED:** Add new dialogue that fits character voice (check character bible)
6. **ALLOWED:** Add internal thoughts that reveal psychology
7. **ALLOWED:** Expand physical descriptions, fluid tracking, environmental detail
8. **ALLOWED:** Add transitional beats between panels for smoother narrative flow

### 5.4 Verification Phase

16. Verify all original dialogue is preserved
2. Verify word count exceeds original by at least 30% (Tier 1), 60% (Tier 2), or 100% (Tier 3)
3. Verify Continuity State table is updated to reflect any new elements
4. Write the MOD Prologue with accurate changelog

---

## 6. Boundaries — HARD RULES

| Rule | Description |
|---|---|
| ❌ **NO Plot Derail** | The story must end at the same place as the original page |
| ❌ **NO Character Invention** | Cannot add characters not in the source manga |
| ❌ **NO Dialogue Deletion** | All original dialogue must be preserved (can be enhanced) |
| ❌ **NO Canon Contamination** | NEVER modify the original `page-XXX.md` file |
| ✅ **YES Creative Freedom** | Within boundaries, Suki has full artistic license |
| ✅ **YES Emotional Expansion** | Add feelings, sensations, thoughts the manga couldn't show |
| ✅ **YES Pacing Control** | Slow down key moments, add build-up, extend climax |
