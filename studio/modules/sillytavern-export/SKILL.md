---
name: sillytavern-export
description: "Build SillyTavern V3 character cards from Markdown files. Supports character export, lorebook embedding, and batch processing."
---

# 📤 SillyTavern Export Module

> **Purpose**: Build SillyTavern V3 character cards from structured Markdown files.

---

## Quick Start

```bash
# 1. Copy the template
cp studio/assets/templates/st_card_template.md my_character.md

# 2. Edit the markdown — fill in your character

# 3. Build the JSON card
python studio/modules/sillytavern-export/scripts/build_st_card.py my_character.md

# Output: my_character_v3.json
```

---

## On Activation (Agent Mode)

When invoked as an AI agent skill:

1. Load template from `{project-root}/studio/assets/templates/st_card_template.md`
2. Load V3 template reference from `{project-root}/studio/assets/templates/SillyTavern_V3_Template.json`
3. Load field mapping from `{project-root}/studio/modules/sillytavern-export/references/field_mapping.md`
4. Load character description example from `{project-root}/studio/assets/templates/char_desc_example.md`
5. Load expert knowledge from `{project-root}/studio/docs/sillytavern-expert-sidecar/knowledge/`

## Menu

| Trigger | Description |
|---------|-------------|
| `/st-export character <bible_path>` | Generate a filled markdown from a character bible, then build JSON |
| `/st-export build <markdown_path>` | Build JSON from an already-filled markdown |
| `/st-export worldinfo <world_path>` | Generate lorebook-only JSON from world info |
| `/st-export batch <folder>` | Export all `.md` files in folder to JSON cards |

---

## Markdown Template Format

The input file uses **YAML frontmatter** + **## sections**:

```yaml
---
name: "Rin"
creator: "LND Studio"
version: "1.0.0"
tags: [mesugaki, loli, tsundere]
talkativeness: 0.5
---
```

### Section → JSON Field Mapping

| Markdown Section | JSON Field | Notes |
|---|---|---|
| `## Description` | `description` | Main prompt block, always sent |
| `## Personality` | `personality` | Brief keyword summary |
| `## Scenario` | `scenario` | Current context |
| `## First Message` | `first_mes` | Opening greeting |
| `## Example Dialogues` | `mes_example` | Voice samples with `<START>` |
| `## System Prompt` | `system_prompt` | Behavioral rules |
| `## Post History Instructions` | `post_history_instructions` | End-of-context reinforcement |
| `## Alternate Greetings` | `alternate_greetings[]` | Separated by `---` |
| `## Lorebook` | `character_book.entries[]` | `###` sub-sections with `**keys:**` |

---

## Agent Workflow: Bible → Card

When asked to export a character bible:

### Step 1: Read the Bible
Read the character bible markdown (e.g., `_lnd-output/_bible/rin/char_rin.md`).

### Step 2: Generate the Filled Markdown
Copy the template and fill each section using the mapping in `references/field_mapping.md`:

- Bible **Thông tin cơ bản** → `## Description` → `<visual_appearance>` XML tags
- Bible **Tính cách** → `## Description` → `<behavioral_engine>` XML tags
- Bible **Voice Sample** → `## Example Dialogues` → `<START>` blocks
- Bible **Điểm yếu/Trigger** → `## Description` → `<sexual_mechanics>` XML tags
- Bible **Trạng thái theo Phase** → `## Lorebook` entries (keyword-triggered)

### Step 3: Apply Token Rules
- Replace character name with `{{char}}`
- Replace user name / POV name with `{{user}}`
- Apply primacy/recency: most important traits at START and END of description

### Step 4: Build the JSON
Run the build script:
```bash
python studio/modules/sillytavern-export/scripts/build_st_card.py <filled_card>.md <output>.json
```

### Step 5: Quality Gate
Verify:
- [ ] `name` is set (not placeholder)
- [ ] `description` is non-empty and under 4000 chars
- [ ] `first_mes` sets scene, action, and hook
- [ ] `mes_example` has at least 2 `<START>` blocks
- [ ] `{{char}}`/`{{user}}` tokens used consistently
- [ ] Lorebook entries have keyword triggers

---

## Output

- Characters: `{name}_v3.json`
- Default output: same directory as input
- Custom output: pass as second argument

## Knowledge References

| File | Purpose |
|------|---------|
| `studio/assets/templates/st_card_template.md` | Fillable MD template |
| `studio/assets/templates/SillyTavern_V3_Template.json` | V3 JSON reference |
| `studio/assets/templates/char_desc_example.md` | XML-tag description example (Grim Aloe) |
| `studio/docs/sillytavern-expert-sidecar/knowledge/` | Full ST expert guides |
| `studio/modules/sillytavern-export/references/field_mapping.md` | Bible → Card mapping |
