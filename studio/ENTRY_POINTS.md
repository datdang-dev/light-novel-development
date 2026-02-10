# studio Entry Points

## Main Pipeline

| Command | Workflow | Purpose |
|---------|----------|---------|
| `/gooner-alchemist` | Full pipeline | Complete manga→prose adaptation |

---

## Capability Workflows

| Command | Owner | Steps | Purpose |
|---------|-------|-------|---------|
| `/panel-forensic` | Director K | 7 | Visual forensic analysis |
| `/prose-adapter` | Suki | 7 | Prose generation |
| `/gooner-audit` | Riko | 5 | Quality scoring |
| `/bible-sync` | Director K | 8 | State management (LOAD/SAVE) |
| `/entity-extractor` | Director K | 5 | Character data extraction |
| `/character-bible` | Aria | 7 | Character creation |
| `/dialogue-generator` | Miki | 6 | R18 dialogue & SFX |
| `/scene-expansion` | Suki | 6 | Outline → full prose |
| `/st-card-export` | Tavvy | 5 | SillyTavern cards |

---

## Pipeline Workflows

| Command | Steps | Purpose |
|---------|-------|---------|
| `/party-mode` | 3 | Multi-agent discussion |
| `/chapter-composer` | 5 | Compile pages → chapter |
| `/release-compiler` | 4 | Dev → reader format |

---

## Quick Reference

```bash
# Full adaptation
/gooner-alchemist

# Just analyze
/panel-forensic

# Create character
/character-bible

# Team brainstorm
/party-mode
```
