---
name: 'step-01-initialize'
description: 'Select agents and set discussion topic'
nextStepFile: './step-02-facilitate.md'
---

# Step 1: Initialize

## STEP GOAL:

Select participating agents and define discussion topic.

## MANDATORY SEQUENCE

### 1. Welcome

```
"**🎉 PARTY MODE - Team Discussion**

Agents available:
- [A] Aria - Character specialist
- [S] Suki - Prose writer
- [M] Miki - Dialogue crafter  
- [R] Riko - Quality auditor
- [L] Luna - World builder
- [T] Tavvy - ST export

**Chọn agents** (e.g., 'A, S, M') hoặc [ALL] for everyone:

**Discussion topic:**"
```

### 2. Set Parameters

```yaml
party_config:
  agents: [{selected}]
  topic: "{topic}"
  format: "round-robin" | "free-form"
  goal: "{desired outcome}"
```

### 3. Present MENU

```
"✅ Party configured!

**Agents:** {list}
**Topic:** {topic}

**Chọn:** [C] Start Discussion"
```

---
