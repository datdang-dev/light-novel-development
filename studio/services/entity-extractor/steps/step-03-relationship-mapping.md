---
name: 'step-03-relationship-mapping'
description: 'Identify character relationships'

thisStepFile: './step-03-relationship-mapping.md'
nextStepFile: './step-04-state-compilation.md'
---

# Step 3: Relationship Mapping

## STEP GOAL:

Map relationships between characters based on observed interactions.

## RELATIONSHIP TYPES

```
POWER DYNAMICS:
- dominant / submissive
- initiator / receiver
- aggressor / victim

SOCIAL:
- stranger / acquaintance / intimate
- authority / subordinate

EMOTIONAL:
- consenting / coerced
- eager / reluctant
```

## MANDATORY SEQUENCE

### 1. Analyze Interactions

For each character pair with interactions:
- Document interaction type
- Note power indicators
- Record dialogue evidence

### 2. Build Relationship Matrix

```markdown
## Relationship Mapping

### char_001 ↔ char_002

**Observed Interactions:**
| Panel | Interaction | Power Dynamic |
|-------|-------------|---------------|
| {X} | {description} | {who dominant} |

**Evidence:**
- Dialogue: "{quote}" - Panel {X}
- Action: {description} - Panel {X}

**Relationship Type:** {type}
**Confidence:** HIGH / MEDIUM / LOW
```

### 3. Flag Uncertain

```
IF relationship unclear:
  → Mark as UNCERTAIN
  → List conflicting evidence
  → Note for future resolution
```

### 4. Present MENU

```
"✅ Relationships mapped!

**Pairs analyzed:** {count}
**Dynamics identified:**
- char_001 → char_002: {type}

**Chọn:** [C] Continue to State Compilation"
```

---
