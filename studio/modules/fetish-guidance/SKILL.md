---
name: fetish-guidance
description: "Fetish pattern and escalation guidance module — provides research-backed fetish-specific writing patterns, do's/don'ts, and combination strategies from 30+ research files."
---

# 🔞 Fetish Guidance Module

> **Purpose**: Cung cấp guidance chi tiết khi xử lý specific fetishes trong prose.

---

## On Activation

1. Detect fetish tags from forensic state or user request
2. Load relevant research files from `{project-root}/studio/knowledge/fetish-db/`
3. Load style guides from `{project-root}/studio/knowledge/style-guides/`
4. Ready to serve pattern lookups, escalation guides, and combination strategies

## Knowledge References

### Fetish Database (30 Files)

| File | Topic | Key Elements |
|------|-------|--------------|
| `mesugaki_research.md` | Bratty dialogue | Teasing patterns, ugly bastard pairing |
| `ntr_research.md` | Netorare | Comparison lines, cuckold triggers |
| `mindbreak_research.md` | 5-phase mindbreak | Psychological descent, ahegao |
| `public_use_research.md` | 便所/Free Use | Objectification, convenience |
| `filming_research.md` | ハメ撮り | POV, blackmail, streaming |
| `paizuri_research.md` | Titfuck | Visual angles, dialogue |
| `blowjob_research.md` | Oral | Techniques, SFX |
| `gangbang_research.md` | Multi-partner | Rotation, stamina |
| `hypnosis_research.md` | Mind control | Trigger phrases |
| `creampie_research.md` | 中出し | Aftermath, overflow |
| *(+20 more in fetish-db/)* | | |

### Style Guides

| File | Content |
|------|---------|
| `MESUGAKI_DIALOGUE_STYLE.md` | Bratty speech patterns |
| `R18_LIGHTNOVEL_CULTURE_GUIDE.md` | Genre conventions |

---

## Capabilities

### 1. Fetish Detection

Parse scene tags and identify relevant fetishes with primary/secondary/tertiary ranking.

### 2. Pattern Library

Retrieve escalation patterns (e.g., mindbreak's 5 phases: Resistance → Confusion → Crack → Fall → Completion).

### 3. Do's and Don'ts

Fetish-specific writing rules (what to emphasize, what to avoid, pacing).

### 4. Combination Guidance

How to blend multiple fetishes effectively (e.g., mesugaki + mindbreak = confident start → satisfying break).

---

## Integration Points

- **lewd-writer**: Fetch fetish-specific patterns during prose generation
- **character-architect**: Reference fetish psychology for character design
- **gooner-editor**: Validate fetish execution against research

## Quick Reference

| Intent | Trigger | Action |
|--------|---------|--------|
| **Single lookup** | `/fetish {name}` | Full research + quick tips |
| **Multi-fetish** | `/fetish-combo [{list}]` | Combined approach guide |
| **Phase check** | `/fetish {name} current:{phase}` | Phase requirements + next triggers |
