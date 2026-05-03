---
name: style-enforcer
description: "Writing style validation module — enforces R18 light novel conventions, Vietnamese prose rules, character archetype speech patterns, and banned word scanning. Acts as a pre-commit gate for all prose output."
owner: "datdang"
version: "1.0.0"
tags: [style, validation, r18, conventions, quality-gate]
injection:
  always:
    - "{{project_root}}/studio/rules/canon-rules.md"
    - "{{project_root}}/studio/rules/anti_slop.md"
  triggers:
    - scene_tag: "explicit|r18|prose|adaptation"
      loads:
        - "{{project_root}}/studio/knowledge/style-guides/R18_LIGHTNOVEL_CULTURE_GUIDE.md"
        - "{{project_root}}/studio/knowledge/style-guides/MESUGAKI_DIALOGUE_STYLE.md"
dependencies:
  knowledge:
    - path: "{{project_root}}/studio/knowledge/style-guides/R18_LIGHTNOVEL_CULTURE_GUIDE.md"
    - path: "{{project_root}}/studio/knowledge/style-guides/MESUGAKI_DIALOGUE_STYLE.md"
    - path: "{{project_root}}/studio/knowledge/glossaries/hentai_lexicon.md"
  modules: []
---

# Style Enforcer

## Role

Pre-commit gate that validates all prose output against R18 light novel conventions. Rejects output that violates format rules, uses banned language, or deviates from established character voice.

## On Activation

1. **Load canon rules:** `canon-rules.md`
2. **Load anti-slop rules:** `anti_slop.md`
3. **Load style guides:** `R18_LIGHTNOVEL_CULTURE_GUIDE.md`, `MESUGAKI_DIALOGUE_STYLE.md`
4. **Receive text** to validate (file path or raw string)
5. **Scan against all rules** in sequence
6. **Return pass/fail** with specific violation lines

## Validation Sequence

### Phase 1 — Format Rules

| Rule | Action |
|------|--------|
| No Kanji in prose/dialogue | ❌ REJECT |
| Romanized SFX only | ❌ REJECT if Kanji found |
| Vietnamese prose + dialogue | ✅ ENFORCE |
| Scene tags present | ⚠️ WARN if missing |
| No HTML/markdown in output | ❌ REJECT |

### Phase 2 — Language Quality

| Check | Threshold |
|-------|-----------|
| Banned words | 0 tolerance |
| Boilerplate ratio | < 10% |
| Sentence repetition | < 3 consecutive |
| Entropy | > 3.5 |

### Phase 3 — Character Voice

- Dialogue matches archetype (from `character-builder`)
- Speech register consistent (cậu-tớ vs mày-tao vs anata-kimi)
- No sudden register shifts mid-scene
- Dialogue ≠ narration (show don't tell in dialogue too)

### Phase 4 — R18 Conventions

- Non-judgmental narrator (no moralizing)
- Sensory-first descriptions (no abstract emotional summaries)
- Power dynamics explicit (who controls, who submits)
- Aftermath present (don't cut away at climax)
- No fourth-wall breaking (unless archetype calls for it)

## Banned Words (Hard Reject)

```
hôi thối, dơ bẩn, ghê tởm, đáng xấu hổ, tội lỗi, ghê
ửng hồng, ánh lên, trắng nõi, khuôn chậu, môi anh đào
```

## Violation Response

- **Hard reject:** Exit immediately, output violation report
- **Soft warn:** Flag but continue (format hints, missing scene tags)
- **Auto-fix:** None — enforcer validates, does not correct

## Integration

- **Upstream:** Any prose generation skill (lewd-writer, scene-expansion)
- **Downstream:** quality-audit (gooner-audit-engine) for final pass
- **Trigger:** Run before writing output to `_lnd-output/`
