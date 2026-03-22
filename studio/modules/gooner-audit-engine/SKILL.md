---
name: gooner-audit-engine
description: "Automated 100-point scoring engine for R18 prose — scores across 5 categories (Sensory, Edging, Fetish, Psychology, Technical) with keyword density detection and fix suggestions."
---

# 🔥 Gooner Audit Engine Module

> **Purpose**: Tự động hóa scoring và audit theo GOONER_AUDIT_FRAMEWORK.

---

## On Activation

1. Load audit framework from `{project-root}/studio/docs/GOONER_AUDIT_FRAMEWORK.md`
2. Load keyword lists (smell, banned words) from style guides
3. Load SFX glossaries for density checking
4. Ready to score prose across 5 categories

## Knowledge References

| File | Location | Purpose |
|------|----------|---------|
| GOONER_AUDIT_FRAMEWORK | `studio/docs/GOONER_AUDIT_FRAMEWORK.md` | 5-category scoring system |
| SFX Glossaries | `studio/knowledge/glossaries/*` | Keyword detection |
| Style Guides | `studio/knowledge/style-guides/*` | Banned words list |

---

## Scoring Categories (100 Points Total)

| Category | Points | Focus |
|----------|--------|-------|
| **A: Sensory Immersion** | 25 | Smell, touch, sound, temperature, taste density |
| **B: Edging Rhythm** | 25 | Tension, 60/40 rule, near-miss, staccato pacing |
| **C: Fetish Exploitation** | 25 | Power dynamics, humiliation, body focus, residue |
| **D: Psychological Depth** | 15 | Internal conflict, desire vs disgust, mental shift |
| **E: Technical Execution** | 10 | Coverage, banned words, hooks, dialogue ratio |

## Grade Thresholds

| Score | Grade | Action |
|-------|-------|--------|
| 95-100 | 🔥 GOONER PERFECTION | Ship immediately |
| 85-94 | ✅ APPROVED | Minor fixes optional |
| 70-84 | ⚠️ NEEDS REVISION | Fix before shipping |
| <70 | ❌ FAILED | Major rewrite required |

---

## Capabilities

1. **Automated Scoring** — Parse prose, generate per-category scores
2. **Keyword Density Check** — Count sensory words against minimums
3. **Banned Words Detection** — Scan for judgmental terms with line numbers
4. **Fix Suggestions** — Per-issue recommended additions/changes

## Integration Points

- **gooner-editor**: Primary consumer for QA scoring
- **lewd-writer**: Pre-check during prose generation
- **release-compiler**: Final validation before publish

## Quick Reference

| Intent | Trigger | Action |
|--------|---------|--------|
| **Full audit** | `/audit {prose_file}` | Complete 100-point scorecard |
| **Quick check** | `/audit-quick {prose_file}` | Pass/Fail per category |
| **Category focus** | `/audit-sensory {prose_file}` | Detailed Category A breakdown |
