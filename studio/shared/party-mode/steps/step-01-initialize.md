---
name: step-01-initialize
description: Select agents and set discussion topic
nextStepFile: ./step-02-facilitate.md
---

# Step 1: Initialize Party Mode 🎉

## STEP GOAL

Select participating agents and define the discussion topic.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Show Welcome Screen

Display the available roster:

- [A] Aria (Character)
- [S] Suki (Prose)
- [M] Miki (Dialogue)
- [R] Riko (Audit)
- [L] Luna (World)
- [T] Tavvy (RenPy/ST)

### 2. Capture Input

Ask the user to select Agents and Topic.

**Format:**
`Agents: [A, S, M] | Topic: "Refining Asuka's Tsundere Arc"`

### 3. Configure Session

Store the configuration:

```yaml
party_config:
  agents: {user_selection}
  topic: {topic_input}
  goal: {desired_outcome}
```

### 4. Present MENU OPTIONS

```
"✅ Party Configured!

**Agents:** {list_selected_agents}
**Topic:** {topic}

**Tiếp theo:** Start Round-Robin Discussion

**Chọn:** [C] Begin Discussion"
```

#### Menu Handling Logic

- IF C: Load `{nextStepFile}`
- IF other: Redisplay menu
