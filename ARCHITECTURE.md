# LND Studio Architecture

## Overview

LND Studio là framework chuyên biệt cho adaptation và generation R18 JP light novel + manga prose. Built trên nguyên tắc multi-agent orchestration với kiến trúc knowledge-centric, layered.

---

## Layered Architecture

```
┌─────────────────────────────────────────────┐
│  ENTRY POINTS (cli, party-mode, pipeline)   │
│  User-facing orchestration                   │
├─────────────────────────────────────────────┤
│  CORE ENGINE (studio/core/)                 │
│  Primary content generation agents          │
│  lewd-writer, panel-forensic,              │
│  scene-prelude, erotic-caption-writer,      │
│  transformation-engine, volume-context-ext  │
├─────────────────────────────────────────────┤
│  SERVICES (studio/services/)                 │
│  Adaptation, expansion, quality pipeline    │
│  scene-expansion, renpy-adaptation,        │
│  character-builder, quality-audit,        │
│  dialogue-scripting, manga-context-ext     │
├─────────────────────────────────────────────┤
│  MODULES (studio/modules/)                  │
│  Plug-in rule sets và specialized engines  │
│  fetish-guidance, gooner-audit-engine,     │
│  style-enforcer, lnd-re-specialist,        │
│  sfx-lookup, sillytavern-export           │
├─────────────────────────────────────────────┤
│  SHARED (studio/shared/)                    │
│  Cross-cutting concerns                     │
│  agent-memory, onboarding                  │
├─────────────────────────────────────────────┤
│  KNOWLEDGE (studio/knowledge/)             │
│  Domain knowledge packs — source of truth   │
│  packs/, fetish-db/, glossaries/,         │
│  sfx/, style-guides/, trope_beat_sheets/  │
├─────────────────────────────────────────────┤
│  RULES (studio/rules/)                     │
│  Global constraints và anti-slop guards    │
│  canon-rules, user_fetish_profile,         │
│  anti_slop, xcom_degenerate_style         │
├─────────────────────────────────────────────┤
│  CONFIG (studio/config/)                   │
│  Atmosphere thresholds, pipeline config    │
│  atmosphere_ledger.json                    │
└─────────────────────────────────────────────┘
```

---

## Knowledge Architecture

Knowledge files là nguồn tri thức nghiệp vụ. Mọi SKILL.md phải wire đến knowledge thông qua `dependencies.knowledge`.

### Index

- **File:** `studio/knowledge/knowledge-index.yaml`
- **Schema:**
  ```yaml
  index:
    - file: "packs/arousal_architecture.md"
      tags: [sensory, arousal, architecture]
      used_by: [lewd-writer, scene-expansion]
  scene_tags:
    explicit:
      loads: [...]
  ```

### Directory Layout

```
studio/knowledge/
├── packs/               # Core knowledge packs
│   ├── arousal_architecture.md
│   ├── fetish_guidance_pack.md
│   ├── narrative_style_pack.md
│   ├── japanese_reader_psychology.md
│   ├── r18_sensory_pack.md
│   └── roleplay_st_pack.md
├── fetish-db/          # Fetish-specific research
│   ├── anal_research.md
│   ├── mindbreak_research.md
│   ├── ntr_research.md
│   ├── creampie_research.md
│   └── ...
├── glossaries/
│   └── hentai_lexicon.md
├── sfx/
│   ├── japanese_sfx_dictionary.md
│   ├── moaning_sfx_research.md
│   └── r18_sfx_quickref.yaml
├── style-guides/
│   ├── MESUGAKI_DIALOGUE_STYLE.md
│   └── R18_LIGHTNOVEL_CULTURE_GUIDE.md
└── trope_beat_sheets/
    ├── corruption_beats.md
    ├── mindbreak_beats.md
    └── ...
```

### SKILL.md Frontmatter Schema

```yaml
---
name: skill-name
description: "One-line description"
injection:
  always:
    - "{{project_root}}/studio/rules/canon-rules.md"
  triggers:
    - scene_tag: "explicit|r18|sexual"
      loads:
        - "{{project_root}}/studio/knowledge/packs/arousal_architecture.md"
dependencies:
  knowledge:
    - path: "{{project_root}}/studio/knowledge/packs/arousal_architecture.md"
  modules:
    - module-name
```

---

## Agent Pipeline

### Primary Pipeline (Manga → Prose)

```
Raw Manga Page
    ↓
[Kana] Panel Forensic — dialogue extraction, character anchor
    ↓
[Luna] Scene Prelude — scenario seed, power dynamic
    ↓
[Suki] Erotic Caption Writer — R18 prose generation
    ↓
[Riko] Quality Audit — anti-slop, format gate
    ↓
Final Output
```

### Adaptation Pipelines

- **Novel Development:** raw text → structured R18 scene
- **RPG Adapter:** RPG Maker game data → chronological novel
- **Renpy Adaptation:** Ren'Py script → visual-novel format
- **Scene Expansion:** brief scenario → full prose chapter

---

## Quality Gates

Thresholds từ `atmosphere_ledger.json`:

| Metric | Threshold |
|--------|-----------|
| `min_sensory_density` | 0.20 |
| `max_boilerplate_ratio` | 0.10 |
| `min_entropy` | 3.5 |
| `max_ngram_repeat` | 0.05 |

Validator: `studio/scripts/anti_slop_validator.py`

---

## CI/CD

GitHub Actions: `.github/workflows/knowledge-quality.yml`

- **yaml-parse:** Mọi SKILL.md phải parse YAML frontmatter đúng
- **knowledge-sync:** `knowledge-index.yaml` phải đồng bộ với physical files
- **anti-slop:** Knowledge files phải pass entropy + ngram thresholds

---

## AI Slop Detection

### Signs

- Entropy < 3.5 (quá repetitive)
- N-gram repeat > 5% (copy-paste pattern)
- Sensory density < 0.20 (khô khan, thiếu hồn)
- 3+ câu liên tiếp cùng sentence starter
- Banned phrases: "ửng hồng", "ánh lên", "trắng nõi", "khuôn chậu"

### Anti-Slop Files

- `studio/rules/anti_slop.md` — banned phrase list
- `studio/rules/xcom_degenerate_style.md` — degenerate writing style
- `studio/scripts/anti_slop_validator.py` — automated scanner

---

## File Naming Conventions

| Type | Convention |
|------|-----------|
| Skill folder | `kebab-case` |
| Knowledge pack | `snake_case.md` |
| Research file | `*_research.md` |
| Glossary | `*_lexicon.md` |
| Beat sheet | `*_beats.md` |
| SFX reference | `*_sfx_*.md` |

---

## Anti-Patterns

1. **Orphan knowledge** — file tồn tại nhưng không có trong index hoặc không được reference bởi SKILL nào
2. **Broken wiring** — index nói `used_by: [lewd-writer]` nhưng lewd-writer không load file đó
3. **Multi-doc YAML** — SKILL.md frontmatter parse thành 2+ YAML document do `---` thừa
4. **Empty dependencies** — SKILL.md có `dependencies: []` nhưng engine cần knowledge
5. **Slop prose** — viết theo pattern generic, thiếu sensory detail, lặp vocabulary
