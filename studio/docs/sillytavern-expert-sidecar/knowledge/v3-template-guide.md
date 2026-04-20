# SillyTavern Character Card V3 Template

This folder contains the official V3 Character Card template for SillyTavern.

## File

- `SillyTavern_V3_Template.json` - Complete V3 spec template with all fields

## V3 Spec Overview

The V3 Character Card specification is the latest format supported by SillyTavern.

### Root Fields

| Field | Purpose | AI Visible |
|-------|---------|------------|
| `spec` | Format identifier ("chara_card_v3") | No |
| `spec_version` | Version string ("3.0") | No |
| `name` | Character name | Yes |
| `description` | Main character definition | Yes (always) |
| `personality` | Brief personality summary | Yes (always) |
| `scenario` | Current situation/context | Yes (always) |
| `first_mes` | Opening message | Yes (once) |
| `mes_example` | Example dialogues with `<START>` tags | Yes (context permitting) |
| `creator_notes` | Notes for users | No |
| `tags` | Category tags | No |
| `talkativeness` | Group chat response probability (0-1) | No |
| `alternate_greetings` | Additional first messages | Yes (selected) |
| `group_only_greetings` | Greetings for group chats only | Yes (in groups) |
| `creator` | Author name | No |
| `character_version` | Version string | No |

### Extensions Block

```json
"extensions": {
    "world": "Linked World Info name",
    "depth_prompt": {
        "prompt": "Injection text",
        "depth": 4,
        "role": "system"
    }
}
```

- `world` - Name of linked World Info file
- `depth_prompt` - Character's Note injection settings

### Embedded Character Book (Lorebook)

V3 supports embedding lorebook entries directly in the card:

```json
"character_book": {
    "name": "Book name",
    "scan_depth": 3000,
    "token_budget": 500,
    "recursive_scanning": true,
    "entries": [...]
}
```

#### Full Entry Fields Schema

| Core Field | Purpose |
|------------|---------|
| `keys` | Array of primary trigger keywords (e.g. `["school", "classroom"]`) |
| `secondary_keys` | Array of optional filter keys |
| `content` | Text to inject, can use macros `{{char}}` / `{{user}}` |
| `enabled` | Active toggle (`true`/`false`) |
| `position` | Insertion block (`"before_char"` / `"after_char"`) |
| `constant` | Always include, ignoring keys (`true`/`false`) |
| `selective` | Requires secondary keys logic to pass (`true`/`false`) |
| `insertion_order` | Priority (higher = placed later in prompt) |
| `use_regex` | Are the keys regex patterns? (`true`/`false`) |

#### Full Extensions Schema (inside `extensions: {}`)

| Extension Field | Description | Type / Default |
|-----------------|-------------|----------------|
| `position` | Enum equivalent for placement (`0`=before, `1`=after, `2`=before_example...) | Integer |
| `selectiveLogic` | Logic for secondary keys (`0`=AND ANY, `1`=AND ALL, `2`=NOT ANY, `3`=NOT ALL) | Integer |
| `role` | @ Depth Role (`0`=system, `1`=user, `2`=assistant) | Integer |
| `vectorized` | Use semantic matching instead of keyword matching? | Boolean |
| `sticky` | Stays active for X messages after trigger | Integer |
| `cooldown` | Cannot trigger for X messages after triggering | Integer |
| `delay` | Must wait X messages from chat start to be eligible | Integer |
| `group` | Inclusion group name for mutual exclusion | String |
| `group_weight` | Lottery weight when choosing from group | Integer (100) |
| `prevent_recursion`| Prevents this entry from activating other entries | Boolean |
| `delay_until_recursion`| Only triggers via another entry, not directly | Boolean |
| `automation_id` | Identifier for external script/API hooks | String |
| `triggers` | Array of trigger conditions / generation filters | Array of Strings |

1. Copy `SillyTavern_V3_Template.json`
2. Rename to your character name
3. Fill in all required fields
4. Import into SillyTavern

## Best Practices

1. **Description** - Use structured format (PLists, Ali:Chat, or prose)
2. **First Message** - Set the tone/length you want responses to match
3. **Examples** - Use `<START>` to separate examples, show speech patterns
4. **Lorebook** - Embed related lore entries for self-contained cards
5. **Tags** - Help with organization and filtering
