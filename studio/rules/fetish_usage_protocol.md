# Fetish Usage Protocol

## PURPOSE

Define how `user_fetish_profile.md` should be used across all LND Studio agents to prevent over-enforcement and hallucination.

## CRITICAL RULE: REFERENCE, NOT ENFORCE

`user_fetish_profile.md` is a **REFERENCE GUIDE**, not a **MANDATE**.

---

## Correct Usage

### ✅ DO:

1. **Read fetish profile** to understand user preferences
2. **Identify matches** between source material and fetish list
3. **Highlight existing elements** that align with fetishes
4. **Use appropriate vocabulary** from fetish lexicon when describing what's actually present
5. **Note fetish matches in metadata** for transparency

### ❌ DON'T:

1. **Invent scenarios** to force-fit fetishes
2. **Add elements** not visible in source material (image, manga panel, forensic report)
3. **Exaggerate** minor details into major fetish elements
4. **Ignore** what's actually in the source to write what user "might want"
5. **Assume** user wants every fetish applied to every scene

---

## Stage-Specific Guidelines

### Forensic Stage (Kana)

**Job:** Describe what IS in the image, then note which fetishes it matches.

**Output Format:**

```markdown
## Fetish Profile Matches

- ✅ FETISH 2 (Sweat/Fluid): Visible perspiration on forehead, neck, and chest
- ⚠️ FETISH 1 (Bratty): Expression suggests defiance but archetype not confirmed
- ❌ FETISH 3 (Nylon): No stockings or tight clothing visible
- ❌ FETISH 5 (Used Garments): No garment sniffing or wearing depicted
```

**Rules:**
- Only mark ✅ if element is CLEARLY VISIBLE
- Use ⚠️ for ambiguous/partial matches
- Use ❌ for fetishes NOT present (helps prevent downstream hallucination)

### Prelude Stage (Luna)

**Job:** Build narrative context from forensic facts, reference fetishes where they naturally fit.

**Rules:**
- Base scenario on forensic visual evidence
- If a fetish element exists in forensics, you MAY expand on it narratively
- If a fetish element does NOT exist in forensics, do NOT invent it
- Scenario creativity is allowed, but must be grounded in visual evidence

**Example:**

**Forensic shows:** Girl with slight sweat, annoyed expression, exposed breasts

**❌ WRONG Prelude:**
> "She's been wearing her classmate's stolen panties all day, the crotch soaked with her juices..."
> (FETISH 5 invented - not in forensics)

**✅ RIGHT Prelude:**
> "Forced to expose herself in public as punishment, her body betrays her with visible sweat despite her defiant expression..."
> (Based on forensic facts, expands naturally)

### Caption Stage (Suki)

**Job:** Write prose based on forensic facts and prelude context, using fetish vocabulary where appropriate.

**Rules:**
- Describe what forensics documented
- Use sensory language from fetish lexicon when it fits
- DO NOT add new fetish elements beyond forensics + prelude
- If prelude invented something not in forensics, you MAY include it (Luna's job to stay grounded)

**Example:**

**Forensic shows:** Sweat on forehead only

**❌ WRONG Caption:**
> "Mồ hôi chảy ròng ròng từ nách, mùi tanh nồng xộc vào mũi, vệt ướt dọc sườn..."
> (Inventing armpit sweat, smell, side wetness - not in forensics)

**✅ RIGHT Caption:**
> "Giọt mồ hôi lăn từ trán xuống thái dương, nóng bỏng dưới ánh nắng..."
> (Describing only what's visible, using sensory language appropriately)

---

## Fetish Vocabulary vs Fetish Invention

### ✅ Using Fetish Vocabulary (ALLOWED)

When forensics show sweat, you CAN use rich vocabulary:
- "mồ hôi" → "mồ hôi mặn"
- "wet" → "ướt nhớp", "dính dấp"
- "smell" → "mùi mồ hôi", "tanh"

This is **descriptive enhancement**, not invention.

### ❌ Fetish Invention (FORBIDDEN)

When forensics show NO armpit exposure, you CANNOT write:
- "mùi nách nồng nặc"
- "mồ hôi từ nách chảy xuống"
- "kẹp nách"

This is **hallucination** to fit FETISH 2.

---

## Quality Gate Checklist

Before finalizing any output, verify:

- [ ] Every fetish element mentioned exists in forensic report
- [ ] No scenarios invented solely to fit fetish profile
- [ ] Vocabulary enhances existing elements, doesn't create new ones
- [ ] Fetish matches documented in metadata (transparency)
- [ ] If forensics say ❌ for a fetish, output doesn't include it

---

## Integration with Canon Rules

This protocol is an **extension** of Canon Rule #2 (Zero Hallucination Protocol).

**Canon Rule #2 states:**
> You MUST NOT invent objects, characters, or actions that are not present in the source material.

**This protocol adds:**
> You MUST NOT invent fetish elements to fit user_fetish_profile.md that are not present in the source material.

---

## Related Files

- `studio/config/canon-rules.md` - Global hard rules
- `studio/rules/user_fetish_profile.md` - User preferences (reference only)
- `studio/rules/visual_forensics.md` - Zero hallucination protocol
- `.claude/skills/panel-forensic.md` - Claude Code forensic wrapper
- `.claude/skills/erotic-caption-writer.md` - Claude Code caption wrapper
