---
trigger: model_decision
description: Pass/fail thresholds only - detailed scoring is in gooner-audit-engine module
priority: 4
---

# Quality Gates

## SCORE THRESHOLDS

| Score | Grade | Action |
|-------|-------|--------|
| 95-100 | 🔥 GOONER PERFECTION | Publish immediately |
| 85-94 | ✅ APPROVED | Publish ready |
| 70-84 | ⚠️ NEEDS REVISION | Target weak categories |
| <70 | ❌ FAILED | Major rewrite required |

**Minimum publish threshold: 85**

---

## CATEGORY OVERVIEW

| Category | Weight | Reference |
|----------|--------|-----------|
| A: Sensory | 25% | See `sensory_density.md` |
| B: Edging | 25% | 60/40 build-up ratio? |
| C: Fetish | 25% | Power dynamics clear? Residue tracked? |
| D: Psychological | 15% | Internal conflict shown? |
| E: Technical | 10% | Format per `dialogue_format.md`? No banned words? |

> **Detailed scoring**: `{project-root}/studio/modules/gooner-audit-engine.md`

---

## QUALITY GATES

### Gate 0: Anti-Contamination (CRITICAL)

Before ANY other gate, scan prose for context leaks:

- [ ] No internal file names in prose (`*_research.md`, `*_lexicon.md`, `workflow.md`)
- [ ] No agent names in prose (`lewd-writer`, `panel-forensic`, `gooner-audit`)
- [ ] No system/pipeline references (`state.yaml`, `forensic-gate`, `step-04`)
- [ ] No meta-commentary about rules (`sensory_density rule says...`)
- [ ] No English technical terms that break Vietnamese prose immersion

**If Gate 0 fails → AUTOMATIC REWRITE of contaminated lines before any other audit.**

### Gate 1: Per-Page

Before moving to next page:

- [ ] Sensory minimums met?
- [ ] Format correct (see `dialogue_format.md`)?
- [ ] No banned words (see `sensory_density.md`)?

### Gate 2: Per-Scene

Before ending scene:

- [ ] Build-up ratio ~60/40?
- [ ] Aftermath/residue included?
- [ ] Continuity tracked (see `continuity.md`)?

### Gate 3: Per-Chapter

Before publishing:

- [ ] Audit score ≥85?
- [ ] All scenes connected?
- [ ] Story bible updated?

---

## REVISION LOOP

If score < 85:

1. Run full audit via `gooner-audit-engine.md`
2. Identify lowest scoring category
3. Target specific deficiencies
4. Re-audit
5. Repeat until ≥85

**NEVER publish content scoring < 85**
