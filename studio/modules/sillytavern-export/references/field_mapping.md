# Field Mapping: LND Bible → ST Card

## Character Bible → Markdown Template → V3 JSON

| LND Bible Section | Template Section | JSON Field | XML Tag (in Description) |
|---|---|---|---|
| **Thông tin cơ bản** (name, age, height) | `## Description` | `description` | `<visual_appearance>` → `<body_type>` |
| Tóc, Mắt, Thân hình | `## Description` | `description` | `<visual_appearance>` → `<body_type>` |
| Trang phục | `## Description` | `description` | `<visual_appearance>` → `<outfit_structure>` |
| Đặc điểm (kẹo mút, nốt ruồi) | `## Description` | `description` | `<visual_appearance>` → `<distinct_features>` |
| **Tính cách (3-Beat Arc)** | `## Description` | `description` | `<behavioral_engine>` → `<interaction_cycle>` |
| Beat 1/2/3 patterns | `## Description` | `description` | `<behavioral_engine>` → `<interaction_cycle>` |
| Speech patterns per beat | `## Description` | `description` | `<behavioral_engine>` → `<speech_patterns>` |
| **Cách xưng hô** | `## Description` | `description` | `<behavioral_engine>` → `<speech_patterns>` |
| **Voice Sample** (per state) | `## Example Dialogues` | `mes_example` | N/A (uses `<START>` blocks) |
| **Điểm yếu / Trigger** | `## Description` | `description` | `<sexual_mechanics>` → `<weakness>` |
| **Trạng thái theo Phase** | `## Lorebook` | `character_book.entries[]` | N/A (keyword-triggered entries) |
| — | `## Personality` | `personality` | N/A (keywords only) |
| — | `## Scenario` | `scenario` | N/A |
| — | `## First Message` | `first_mes` | N/A |

## World Info → Lorebook

| World Info Section | Lorebook Keys | Pattern Notes |
|---|---|---|
| **World/Location** (e.g. Setting) | location names | `constant: true`, `position: before_char` (Sets the stage) |
| **Mechanics** (onahole link, limits) | mechanic triggers | `constant: false`, `position: after_char` (Overwrites logic) |
| **Character History/Relationships**| character names | `constant: false`, `position: after_char`, `selective: true` |
| **Fetish / NSFW Events** | fetish terminology | `regex: true`, `sticky: 5`, `cooldown: 10` (Keeps effect alive) |

## Token Replacement Rules

| Original | Replace With | Context |
|---|---|---|
| Character's actual name | `{{char}}` | In description, scenario, examples |
| User/POV name (e.g., "Dat") | `{{user}}` | In scenario, examples, lorebook |
| Specific time references | Keep as-is or use `{{time}}` | In scenario |

## Description Format Priority

Place information in this order for best AI attention (primacy/recency effect):

1. **Identity** — Who is `{{char}}`? (name, role, archetype)
2. **Appearance** — Visual details (`<visual_appearance>`)
3. **Psychology** — Inner world (`<psychological_profile>`)
4. **Behavior** — How they act (`<behavioral_engine>`)
5. **R18 Mechanics** — Sexual traits (`<sexual_mechanics>`)
6. **Current Context** — Right now (`<current_context>`)
7. **System Instructions** — Rules for AI (`<system_instruction>`) ← recency
