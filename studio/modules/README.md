# 📦 LND Studio Modules

> **Location**: `studio/modules/`

Knowledge-backed modules that extend agent capabilities. Each module follows the SKILL.md convention with a standardized entry point, activation protocol, and composable structure.

---

## Available Modules

| Module | Directory | Purpose |
|--------|-----------|---------|
| [🔊 sfx-lookup](./sfx-lookup/SKILL.md) | `sfx-lookup/` | SFX tra cứu, dịch, gợi ý |
| [🔞 fetish-guidance](./fetish-guidance/SKILL.md) | `fetish-guidance/` | Fetish patterns & escalation |
| [🔥 gooner-audit-engine](./gooner-audit-engine/SKILL.md) | `gooner-audit-engine/` | 100-point QA scoring |
| [✍️ style-enforcer](./style-enforcer/SKILL.md) | `style-enforcer/` | Archetype & style validation |
| [📤 sillytavern-export](./sillytavern-export/SKILL.md) | `sillytavern-export/` | ST V3 card export |

---

## Module Structure (SKILL.md Convention)

Each module follows this standard layout:

```
module-name/
├── SKILL.md          # Entry point: YAML frontmatter + Overview + Activation
└── references/       # Static knowledge refs and original documentation
```

### SKILL.md Requirements

- **YAML frontmatter** with `name` and `description`
- **On Activation** section with numbered setup steps
- **Quick Reference** table mapping intents to triggers

---

## Integration Map

```
┌─────────────────────────────────────────────────────────────┐
│                      AGENT LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  dialogue-crafter ←→ sfx-lookup, style-enforcer            │
│  lewd-writer      ←→ fetish-guidance, sfx-lookup, style    │
│  character-arch   ←→ fetish-guidance, sillytavern-export   │
│  gooner-editor    ←→ gooner-audit-engine, style-enforcer   │
│  world-weaver     ←→ sillytavern-export                    │
├─────────────────────────────────────────────────────────────┤
│                      MODULE LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  sfx-lookup │ fetish-guidance │ audit-engine │ style │ ST  │
├─────────────────────────────────────────────────────────────┤
│                    KNOWLEDGE LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  glossaries/ │ fetish-db/ │ style-guides/ │ docs/          │
└─────────────────────────────────────────────────────────────┘
```

---

## Adding New Modules

1. Create a new directory: `modules/{module-name}/`
2. Copy the template from `_templates/new-skill-template/`
3. Write a proper `SKILL.md` with:
   - YAML frontmatter (`name`, `description`)
   - `## Overview` — what the module does
   - `## On Activation` — setup steps
   - `## Capabilities` — what it provides
   - `## Integration Points` — which agents use it
   - `## Quick Reference` — trigger table
4. Add a `references/` directory for knowledge sources
5. Update `module.yaml` with the new module entry
6. Update this README

---

_Managed by Director K 🎬_
