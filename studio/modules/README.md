# 📦 LND Studio Modules

> **Location**: `studio/modules/`

Knowledge-backed modules that extend agent capabilities.

---

## Available Modules

| Module | Purpose | Knowledge Source |
|--------|---------|------------------|
| [🔊 sfx-lookup](./sfx-lookup.md) | SFX tra cứu, dịch, gợi ý | `glossaries/`, `fetish-db/moaning*` |
| [🔞 fetish-guidance](./fetish-guidance.md) | Fetish patterns & escalation | `fetish-db/` (30 files) |
| [🔥 gooner-audit-engine](./gooner-audit-engine.md) | 100-point QA scoring | `docs/GOONER_AUDIT_FRAMEWORK.md` |
| [✍️ style-enforcer](./style-enforcer.md) | Archetype & style validation | `style-guides/`, `fetish-db/*_research` |
| [📤 sillytavern-export](./sillytavern-export.md) | ST V3 card export | `docs/sillytavern-expert-sidecar/` |

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

## Usage

Modules are referenced by agents during workflow execution. To use manually:

```
# View module capabilities
cat studio/modules/sfx-lookup.md

# Reference in agent workflow
"Apply sfx-lookup module to suggest SFX for this scene"
```

---

## Adding New Modules

1. Create `{module-name}.md` in this directory
2. Include:
   - Purpose section
   - Knowledge References table
   - Capabilities list
   - Integration Points
   - Usage Examples
3. Update this README

---

_Managed by Director K 🎬_
