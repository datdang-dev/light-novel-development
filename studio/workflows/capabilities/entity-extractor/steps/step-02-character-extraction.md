---
name: 'step-02-character-extraction'
description: 'Extract character appearances and traits'

thisStepFile: './step-02-character-extraction.md'
nextStepFile: './step-03-relationship-mapping.md'
---

# Step 2: Character Extraction

## STEP GOAL:

Extract all character appearances, physical traits, and identifiers from forensic data.

## MANDATORY RULES

- **Evidence required**: Every trait must cite source panel
- **No invention**: Only document what's observed
- **Consistent IDs**: Use char_001, char_002 etc. until named

## MANDATORY SEQUENCE

### 1. Scan All Panels

For each panel in forensic report:
- Identify distinct characters
- Note physical descriptions
- Track clothing states
- Record positions/actions

### 2. Build Character Profiles

```markdown
## Character Extraction

### Character 1 (char_001)

**First Seen:** Panel {X}
**Panels:** {list}

**Physical Traits:**
| Trait | Description | Source |
|-------|-------------|--------|
| Hair | {desc} | Panel {X} |
| Body | {desc} | Panel {X} |
| Features | {desc} | Panel {X} |

**Clothing States:**
| Panel | State |
|-------|-------|
| {X} | {description} |

**Actions Observed:**
- Panel {X}: {action}
```

### 3. Handle Naming

```
IF character is named in dialogue:
  → Use name as identifier
  → Note alias if different from name

IF unnamed:
  → Keep as char_XXX
  → Add descriptive alias (e.g., "blonde_woman")
```

### 4. Present MENU

```
"✅ Characters extracted!

**Total:** {count} characters

**Identified:**
- char_001: {brief descriptor}
- char_002: {brief descriptor}

**Chọn:** [C] Continue to Relationship Mapping"
```

---
