---
name: 'step-07-final-profile'
description: 'Compile and validate complete character profile'

thisStepFile: './step-07-final-profile.md'
profileOutput: '{output_folder}/_bible/{project}/characters/{char_id}.md'
---

# Step 7: Final Profile

## STEP GOAL:

Compile all sections into final character profile file.

## MANDATORY SEQUENCE

### 1. Compile Full Profile

Generate complete profile at `{profileOutput}`:

```markdown
---
id: "{char_id}"
name: "{name}"
role: "{role}"
archetype: "{archetype}"
created: "{timestamp}"
status: COMPLETE
---

# Character: {Name}

## Quick Reference
- **Age:** {age}
- **Archetype:** {archetype}
- **Key Trait:** {defining}
- **Fetish Focus:** {primary}

## Physical Description
{full physical description}

### Signature Features
- {feature 1}
- {feature 2}

## Psychological Profile

### Core Wound
{trauma}

### Desires
**Surface:** {stated}
**Deep:** {actual}

### Fears
**Primary:** {fear}
**Triggers:** {triggers}

## Sexual Profile

### Psychology-Fetish Link
{connection explanation}

### Preferences
{fetish table}

### Role Tendency
{dom/sub/switch with reason}

## Voice & Speech

### Speech Patterns
{patterns}

### Sample Dialogue
{examples}

## Relationships
{relationship entries}

## Writer's Notes
- {guidance 1}
- {guidance 2}
- {do's and don'ts}
```

### 2. Validation Checklist

```markdown
## Profile Validation

| Section | Status | Notes |
|---------|--------|-------|
| Core Identity | ✅ | {check} |
| Physical Description | ✅ | {check} |
| Psychological Profile | ✅ | {check} |
| Fetish Integration | ✅ | {check} |
| Voice & Speech | ✅ | {check} |
| Relationships | ✅ | {check} |
```

### 3. Workflow Completion

```
"✅ CHARACTER BIBLE COMPLETE!

**Profile:** {profileOutput}

**{Name}** is ready for:
- prose-adapter context
- gooner-alchemist pipeline
- scene development

**Summary:**
{one-paragraph character summary}

**WORKFLOW COMPLETE**"
```

---

## WORKFLOW END

Character profile complete and saved to bible.
