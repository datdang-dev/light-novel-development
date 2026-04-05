---
trigger: model_decision
description: Quality thresholds and pass/fail criteria for R18 content
---

# Quality Gates

## AUDIT SCORING

### Category Breakdown (100 points total)

| Category | Max Points | Weight |
|----------|------------|--------|
| A: Sensory Immersion | 25 | 25% |
| B: Edging Rhythm | 25 | 25% |
| C: Fetish Exploitation | 25 | 25% |
| D: Psychological Depth | 15 | 15% |
| E: Technical Execution | 10 | 10% |

---

## 📊 CATEGORY A: Sensory Immersion (25 pts)

| ID | Requirement | Points | Pass Criteria |
|----|-------------|--------|---------------|
| A1 | Smell Density | 5 | ≥3 per page |
| A2 | Touch/Texture | 5 | ≥5 per page |
| A3 | Sound/Onomatopoeia | 5 | ≥3 per action |
| A4 | Temperature | 5 | Every fluid contact |
| A5 | Taste (when applicable) | 5 | Oral scenes only |

---

## 📊 CATEGORY B: Edging Rhythm (25 pts)

| ID | Requirement | Points | Pass Criteria |
|----|-------------|--------|---------------|
| B1 | Pre-Action Tension | 5 | 4-6 paragraphs before action |
| B2 | 60/40 Rule | 5 | Build-up vs action ratio |
| B3 | Near-Miss Moments | 5 | ≥1 per 3 pages |
| B4 | Edge Markers | 5 | 🔺BUILD → ⚡EDGE → 💥RELEASE |
| B5 | Staccato Pacing | 5 | Short sentences at climax |

---

## 📊 CATEGORY C: Fetish Exploitation (25 pts)

| ID | Requirement | Points | Pass Criteria |
|----|-------------|--------|---------------|
| C1 | Power Dynamics | 5 | Clear control/submission |
| C2 | Humiliation Elements | 5 | Explicit degradation |
| C3 | Body Part Focus | 5 | Detailed attention |
| C4 | Clothing State | 5 | Exact undress/contamination |
| C5 | Residue Tracking | 5 | Fluids across scenes |

---

## 📊 CATEGORY D: Psychological (15 pts)

| ID | Requirement | Points | Pass Criteria |
|----|-------------|--------|---------------|
| D1 | Internal Conflict | 5 | Mind vs body battle |
| D2 | Desire vs Disgust | 5 | Reluctance paradox |
| D3 | Mental Shift | 5 | Psychology evolution |

---

## 📊 CATEGORY E: Technical (10 pts)

| ID | Requirement | Points | Pass Criteria |
|----|-------------|--------|---------------|
| E1 | Zero-Skip Protocol | 3 | Every panel captured |
| E2 | Neutral Narrator | 3 | No judgmental words |
| E3 | Page Hook | 2 | Tension at endings |
| E4 | Dialogue Ratio | 2 | ≥50% dialogue/thoughts |

---

## 📊 CATEGORY F: Cultural Compliance — JP Reader Alignment (15 pts) — V8.0

> **Hard Gate Dependency:** This category cross-references `hentai_logic_gate.md`.
> If HENTAI LOGIC GATE fails → Category F auto-scores 0, regardless of individual item scores.

| ID | Requirement | Points | Pass Criteria |
|----|-------------|--------|---------------|
| F1 | 納得感 (Erotic Justification) | 4 | Every sexual escalation has narrative/psychological logic |
| F2 | 背徳感 (Taboo Element) | 4 | Scene explicitly identifies and leverages a taboo |
| F3 | ギャップ萌え (Gap Moe) | 4 | At least 1 visible persona contrast per featured character |
| F4 | SFX Authenticity | 3 | Japanese-phonetic SFX (パンパン, ぐちゅ, etc.) used correctly and consistently |

---

## 🎯 GRADE SCALE

> **Note (V8.0):** Total possible = 115 pts (A:25 + B:25 + C:25 + D:15 + E:10 + F:15). Normalize to 100 for grading: `final_score = (raw_score / 115) * 100`.

```
95-100: 🔥 GOONER PERFECTION (JP-aligned masterpiece)
85-94:  ✅ APPROVED (publish ready)
70-84:  ⚠️ NEEDS REVISION
<70:    ❌ FAILED (major rewrite)
```

---

## 🚦 QUALITY GATES

### Gate 0: Format Compliance (HARD FAIL)

**This gate runs BEFORE any scoring. If ANY item fails → score = 0, return to prose-adapter.**

- [ ] Header Banner present? (`# 📖`, `📍 Location:`, `⏰ Time:`, `👤 POV:`)
- [ ] All dialogue in `「」` brackets with `Name:` prefix?
- [ ] All SFX in `*SFX: ...*` format?
- [ ] Template structure matches `light-novel-prose.md`?
- [ ] Footer separator (`---` + `***`) present?

```
IF ANY FORMAT ITEM FAILS:
  Score = 0/100
  Verdict = FORMAT-FAIL
  Action = Return to Suki (step-05b-format-ensure)
  DO NOT proceed to category scoring
```

### Gate 1: Per-Page Check

Before moving to next page:

- [ ] Sensory minimums met?
- [ ] Format correct?
- [ ] No banned words?

### Gate 2: Per-Scene Check

Before ending scene:

- [ ] Build-up ratio correct?
- [ ] Aftermath included?
- [ ] Continuity tracked?

### Gate 3: Per-Chapter Check

Before publishing:

- [ ] Full audit score ≥85?
- [ ] All scenes connected?
- [ ] Story bible updated?

---

## 🔄 REVISION LOOP

If score < 85:

1. Identify lowest scoring categories
2. Target specific IDs (A1, B2, etc.)
3. Revise those sections
4. Re-audit
5. Repeat until ≥85

**NEVER publish content scoring < 85**
