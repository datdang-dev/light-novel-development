---
name: dialogue-scripting
description: "Miki's Dialogue Crafter — generates authentic R18 Japanese-influenced Vietnamese dialogue with SFX integration. 6-step workflow: context load → voice calibration → escalation mapping → dialogue generation → SFX integration → polish. Use when scene requires character speech or audio cues."
owner: "Miki (dialogue-crafter)"
version: "6.0.0"
tags: [dialogue, sfx, r18, voice, escalation]
validateWorkflow: "./references/workflow.md"
injection:
  always:
    - "{{project_root}}/studio/rules/canon-rules.md"
    - "{{project_root}}/studio/knowledge/glossaries/hentai_lexicon.md"
  triggers:
    - scene_tag: "explicit|r18|dialogue-heavy|intimate"
      loads:
        - "{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md"
        - "{{project_root}}/studio/knowledge/sfx/japanese_sfx_dictionary.md"
dependencies:
  knowledge:
    - path: "{{project_root}}/studio/knowledge/glossaries/hentai_lexicon.md"
    - path: "{{project_root}}/studio/knowledge/sfx/japanese_sfx_dictionary.md"
    - path: "{{project_root}}/studio/knowledge/sfx/moaning_sfx_research.md"
    - path: "{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md"
    - path: "{{project_root}}/studio/knowledge/packs/narrative_style_pack.md"
    - path: "{{project_root}}/studio/knowledge/style-guides/MESUGAKI_DIALOGUE_STYLE.md"
  modules: [sfx-lookup, style-enforcer]
---

# Dialogue Scripting (Miki)

## Role

Generates authentic R18 dialogue with proper voice archetypes and integrated SFX. 6-step workflow producing dialogue that sounds like real corrupted characters, not AI-generated text.

## Pipeline Position

```
[Character Builder] → [Dialogue Scripting] → [Scene Expansion]
                     ↓
              [SFX Lookup] → [SFx Integration]
```

## 6-Step Workflow

**CRITICAL:** LOAD and follow each step file exactly:

1. **Context Load** (`steps/step-01-context-load.md`) — Load character profile, scene tags, power dynamic
2. **Voice Calibration** (`steps/step-02-voice-calibration.md`) — Match archetype, set speech register
3. **Escalation Mapping** (`steps/step-03-escalation-mapping.md`) — Plan 3-beat arc (setup → turn → payoff)
4. **Dialogue Generation** (`steps/step-04-dialogue-generation.md`) — Write dialogue with embedded narration
5. **SFX Integration** (`steps/step-05-sfx-integration.md`) — Layer Japanese SFX in romaji
6. **Polish & Review** (`steps/step-06-polish-review.md`) — Anti-slop scan, banned word check

## Voice Archetypes

| Archetype | Register | Content Pattern |
|-----------|----------|----------------|
| Mesugaki | cậu-tớ → mày-tao | Confident → commanding |
| Mindbroken | cậu-tớ (frozen) | Confused, repetitive |
| Yandere | anata-kimi → mày | Sweet surface, possessive |
| Cold Authority | anata-kimi | Flat, commanding |
| Exhibitionist | varies | 4th-wall breaking |

## SFX Rules

- Japanese romaji only (no Kanji, no Katakana in-line)
- Format: `*shlick*`, `*gulp*`, `*squelch*`
- Catalog: `studio/knowledge/sfx/japanese_sfx_dictionary.md`
- Moaning patterns: `studio/knowledge/sfx/moaning_sfx_research.md`

## Anti-Patterns

- ❌ Character suddenly switches register mid-scene
- ❌ SFX in Kanji/Katakana
- ❌ Dialogue that narrates (tell don't show)
- ❌ Generic responses ("I love you", "It feels good")
- ❌ Morally judging narration ("ghê tởm", "tội lỗi")

## Integration

- **Upstream:** `character-builder` (profile), `scene-prelude` (scenario context)
- **Downstream:** `scene-expansion` (embed in prose), `sfx-lookup` (SFX catalog)
- **Related:** `style-enforcer` (voice consistency check)
