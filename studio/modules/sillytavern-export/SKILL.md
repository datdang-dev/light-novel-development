---
name: sillytavern-export
description: "SillyTavern V3 export module — converts LND character bibles, world settings, and scenarios into SillyTavern-compatible cards, lorebooks, and scenario packs."
---

# 📤 SillyTavern Export Module

> **Purpose**: Export characters, world-info, và scenarios sang SillyTavern V3 format.

---

## On Activation

1. Load ST expert knowledge from `{project-root}/studio/docs/sillytavern-expert-sidecar/knowledge/`
2. Load V3 template from `{project-root}/studio/assets/templates/SillyTavern_V3_Template.json`
3. Load character description example from `{project-root}/studio/assets/templates/char_desc_example.md`
4. Ready to export characters, world info, or scenarios

## Knowledge References

| File | Location | Purpose |
|------|----------|---------|
| ST Expert Knowledge | `studio/docs/sillytavern-expert-sidecar/knowledge/` | Full ST guide |
| V3 Template | `studio/assets/templates/SillyTavern_V3_Template.json` | Card structure |
| Prompt Engineering | `studio/docs/sillytavern-expert-sidecar/knowledge/prompt-engineering.md` | Best practices |
| World Info Guide | `studio/docs/sillytavern-expert-sidecar/knowledge/world-info.md` | Lorebook format |

---

## Capabilities

1. **Character Export** — Bible → ST V3 Card (name, description, personality, examples, system prompt)
2. **World Info Export** — Scene/world docs → ST Lorebook (keyword-triggered entries)
3. **Scenario Export** — Completed scenes → ST greeting/first_mes format
4. **Prompt Optimization** — Apply {{char}}/{{user}} tokens, primacy/recency rules

## Output Formats

- Characters: `{char_name}_v3.json`
- Lorebooks: `{world_name}_lorebook.json`
- Bundles: `{project_name}_pack.zip`

## Integration Points

- **character-architect**: Export completed character bibles
- **world-weaver**: Export world settings as lorebooks
- **release-compiler**: Final export step for distribution

## Quick Reference

| Intent | Trigger | Action |
|--------|---------|--------|
| **Character** | `/st-export character {bible_path}` | Generate V3 card |
| **World info** | `/st-export worldinfo {world_path}` | Generate lorebook |
| **Batch** | `/st-export batch {project_folder}` | Export all assets |
