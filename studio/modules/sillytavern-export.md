# 📤 SillyTavern Export Module

> **Purpose**: Export characters, world-info, và scenarios sang SillyTavern V3 format.

---

## Knowledge References

| File | Location | Purpose |
|------|----------|---------|
| ST Expert Knowledge | `studio/docs/sillytavern-expert-sidecar/knowledge/` | Full ST guide |
| V3 Template | `studio/assets/templates/SillyTavern_V3_Template.json` | Card structure |
| Character Example | `studio/assets/templates/char_desc_example.md` | Description format |
| Prompt Engineering | `studio/docs/sillytavern-expert-sidecar/knowledge/prompt-engineering.md` | Best practices |
| World Info Guide | `studio/docs/sillytavern-expert-sidecar/knowledge/world-info.md` | Lorebook format |
| Personas Guide | `studio/docs/sillytavern-expert-sidecar/knowledge/personas.md` | User personas |

---

## SillyTavern V3 Card Structure

```json
{
  "spec": "chara_card_v3",
  "spec_version": "3.0",
  "data": {
    "name": "Character Name",
    "description": "Appearance + Personality",
    "first_mes": "Opening message",
    "mes_example": "Example dialogues",
    "scenario": "Current situation",
    "personality": "Core traits",
    "system_prompt": "Behavioral instructions",
    "post_history_instructions": "",
    "creator_notes": "",
    "character_book": {
      "entries": []
    },
    "tags": [],
    "creator": "",
    "character_version": ""
  }
}
```

---

## Capabilities

### 1. Character Export

Convert Character Bible → ST V3 Card:

```
Input: character_bible/mimi.md
Output: mimi_v3.json

Mapping:
  Bible.identity → Card.name
  Bible.appearance → Card.description (portion)
  Bible.personality → Card.description + Card.personality
  Bible.speech_patterns → Card.mes_example
  Bible.erotic_profile → Card.system_prompt (hidden)
```

### 2. World Info Export

Convert scene/world documents → ST Lorebook:

```
Input: world_setting.md
Output: lorebook.json

Structure:
  entries: [
    {
      "key": ["location_name", "aliases"],
      "content": "Description",
      "extensions": {
        "position": "before_char"
      }
    }
  ]
```

### 3. Scenario Export

Format completed scenes as ST greeting:

```
Input: scene_prose.md
Output: scenario block for first_mes

Format:
  [Setting description]
  [Current situation]
  [Character's opening action/dialogue]
```

### 4. Prompt Optimization

Apply best practices from prompt-engineering.md:

```
Rules Applied:
  - Use "{{char}}" and "{{user}}" tokens
  - Place important info at start/end (primacy/recency)
  - Keep system prompt under 2000 tokens
  - Use clear section markers
```

---

## Export Templates

### Character Description Format

```markdown
{{char}} is [NAME], a [AGE/TYPE] [ROLE].

**APPEARANCE:**
[Height, body type, distinctive features]
[Hair, eyes, skin]
[Usual clothing/state of dress]

**PERSONALITY:**
[Core traits - 3-5 key characteristics]
[Speech patterns]
[Quirks and habits]

**BACKGROUND:**
[Relevant history that affects roleplay]
```

### System Prompt Format

```markdown
[Character name] must:
- [Behavior rule 1]
- [Behavior rule 2]
- [Speech pattern rule]

[Character name] will never:
- [Prohibited action 1]
- [Prohibited action 2]

During erotic scenes:
- [R18 specific rules]
- [Preferred SFX]
- [Reaction patterns]
```

---

## Integration Points

- **character-architect**: Export completed character bibles
- **world-weaver**: Export world settings as lorebooks
- **release-compiler**: Final export step for distribution

---

## Usage Examples

### Full Character Export
```
/st-export character [bible_path]
→ Generates: character_v3.json
→ Includes: description, examples, system prompt
→ Optional: embedded lorebook
```

### World Info Export
```
/st-export worldinfo [world_path]
→ Generates: lorebook_v3.json
→ Entries with keywords
→ Position settings
```

### Batch Export
```
/st-export batch [project_folder]
→ Exports all characters
→ Exports world info
→ Creates combined pack
```

---

## Quality Checklist

Before export, verify:

- [ ] Character name is clear and searchable
- [ ] Description under 4000 characters
- [ ] First message sets scene effectively
- [ ] Example messages show speech patterns
- [ ] System prompt is concise and actionable
- [ ] Lorebook entries have multiple keywords
- [ ] Tags are relevant for discoverability

---

## Technical Details

### Source Template
`{project-root}/studio/assets/templates/SillyTavern_V3_Template.json`

### Output Location
`{output_folder}/exports/sillytavern/`

### File Naming
- Characters: `{char_name}_v3.json`
- Lorebooks: `{world_name}_lorebook.json`
- Bundles: `{project_name}_pack.zip`

---

_Module for LND Studio | Export integration for character-architect, release-compiler_
