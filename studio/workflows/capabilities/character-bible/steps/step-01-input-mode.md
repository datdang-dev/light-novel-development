---
name: 'step-01-input-mode'
description: 'Determine creation mode and gather initial input'

thisStepFile: './step-01-input-mode.md'
nextStepFile: './step-02-core-identity.md'
---

# Step 1: Input & Mode

## STEP GOAL:

Determine whether creating new character or enhancing existing stub, gather initial input.

## MANDATORY SEQUENCE

### 1. Aria Introduction

```
"**🎭 CHARACTER BIBLE - Aria speaking**

Xin chào! Mình là Aria, character architect của LND Studio.

Mình sẽ giúp bạn tạo character profile đầy đủ.

**Bạn muốn:**
[N] Tạo character MỚI từ ý tưởng
[E] Enhance character STUB có sẵn

**Hoặc:** Mô tả character của bạn"
```

### 2. Mode Detection

```
IF user provides character stub path:
  → MODE = ENHANCE
  → Load stub, identify gaps

IF user describes new character:
  → MODE = CREATE
  → Start from scratch

IF user selects [N]:
  → Ask for initial vision

IF user selects [E]:
  → Ask for stub path
```

### 3. Initialize Profile

```yaml
profile_state:
  mode: "{CREATE/ENHANCE}"
  stub_path: "{if enhance}"
  initial_vision: "{user description}"
  sections_complete: []
```

### 4. Present MENU

```
"✅ Mode: {CREATE/ENHANCE}

**Initial vision:** {brief}

**Tiếp theo:** Define core identity

**Chọn:** [C] Continue"
```

---
