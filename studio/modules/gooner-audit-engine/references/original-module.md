---
name: "gooner-audit-engine"
description: "Core logic for the Gooner Audit Framework - Automated scoring and feedback"
version: "1.0.0"
type: "module"
owner: "Riko (gooner-editor)"
---

# 🔥 Gooner Audit Engine Module

> **Purpose**: Tự động hóa scoring và audit theo GOONER_AUDIT_FRAMEWORK.

---

## Knowledge References

| File | Location | Purpose |
|------|----------|---------|
| GOONER_AUDIT_FRAMEWORK | `studio/docs/GOONER_AUDIT_FRAMEWORK.md` | 5-category scoring system |
| SFX Glossaries | `studio/knowledge/glossaries/*` | Keyword detection |
| Style Guides | `studio/knowledge/style-guides/*` | Banned words list |

---

## Scoring Categories (100 Points Total)

### Category A: Sensory Immersion (25 pts)

| ID | Requirement | Points | Detection Method |
|----|-------------|--------|------------------|
| A1 | Smell Density | 5 | Count: mùi, nồng, tanh, xộc, mặn |
| A2 | Touch/Texture | 5 | Count: ướt, nhớp, nóng, mềm, cứng |
| A3 | Sound/SFX | 5 | Count: onomatopoeia, SFX markers |
| A4 | Temperature | 5 | Count: nóng, lạnh, ấm, rực |
| A5 | Taste | 5 | Count: mặn, đắng, ngọt, tanh |

### Category B: Edging Rhythm (25 pts)

| ID | Requirement | Points | Detection Method |
|----|-------------|--------|------------------|
| B1 | Pre-Action Tension | 5 | Paragraph analysis before action |
| B2 | 60/40 Rule | 5 | Build-up vs action ratio |
| B3 | Near-Miss Moments | 5 | Detect "almost" patterns |
| B4 | Edge Point Markers | 5 | Look for 🔺⚡💥 or equivalents |
| B5 | Staccato Pacing | 5 | Short sentence density in climax |

### Category C: Fetish Exploitation (25 pts)

| ID | Requirement | Points | Detection Method |
|----|-------------|--------|------------------|
| C1 | Power Dynamics | 5 | Explicit dom/sub indicators |
| C2 | Humiliation Elements | 5 | Degradation keywords |
| C3 | Body Part Focus | 5 | Detailed body descriptions |
| C4 | Clothing State | 5 | Wardrobe tracking |
| C5 | Residue Tracking | 5 | Fluid continuity |

### Category D: Psychological Depth (15 pts)

| ID | Requirement | Points | Detection Method |
|----|-------------|--------|------------------|
| D1 | Internal Conflict | 5 | Mind vs body patterns |
| D2 | Desire vs Disgust | 5 | Paradox expressions |
| D3 | Mental Shift | 5 | Psychology evolution |

### Category E: Technical Execution (10 pts)

| ID | Requirement | Points | Detection Method |
|----|-------------|--------|------------------|
| E1 | Zero-Skip Protocol | 3 | Panel/moment coverage |
| E2 | Non-Judgmental | 3 | Banned words check |
| E3 | Page Ending Hook | 2 | Cliffhanger patterns |
| E4 | Dialogue Ratio | 2 | 50%+ dialogue check |

---

## Capabilities

### 1. Automated Scoring

Parse prose and generate scores:

```
Input: [prose text]
Output:
  Category A: 22/25 (Missing: taste)
  Category B: 20/25 (Missing: near-miss moment)
  Category C: 25/25 ✓
  Category D: 12/15 (Weak: desire/disgust)
  Category E: 8/10 (Missing: hook)
  
  TOTAL: 87/100 - ✅ APPROVED (minor fixes)
```

### 2. Keyword Density Check

```
Input: [prose text]
Output:
  Smell words: 4 (Required: ≥3) ✓
  Texture words: 6 (Required: ≥5) ✓
  SFX count: 2 (Required: ≥3) ⚠️ LOW
  Temperature: 1 (Required: per penetration) ⚠️ MISSING
```

### 3. Banned Words Detection

```
Input: [prose text]
Scan for: hôi thối, dơ bẩn, ghê tởm, đáng xấu hổ, tội lỗi
Output:
  ❌ Found "dơ bẩn" at line 47
  ❌ Found "ghê tởm" at line 89
  Recommendation: Replace with neutral descriptors
```

### 4. Fix Suggestions

```
Issue: A3 (Sound) score low
Suggestions:
  - Add wet SFX: nhẹp nhẹp, bì bạch
  - Add moaning: 「Ahh~♡」
  - Add impact: thịt vỗ vào thịt
  
Issue: B3 (Near-Miss) missing
Suggestions:
  - Add "Almost... not yet..." moment
  - Introduce interruption before climax
  - Build 2-3 paragraphs of denial
```

---

## Integration Points

- **gooner-editor**: Primary user of this module for QA
- **lewd-writer**: Pre-check during prose generation
- **release-compiler**: Final validation before publish

---

## Usage Examples

### Full Audit

```
/audit [prose_file.md]
→ Returns: Complete 100-point scorecard
→ Issues identified with line numbers
→ Fix recommendations prioritized
```

### Quick Check

```
/audit-quick [prose_file.md]
→ Returns: Pass/Fail per category
→ Critical issues only
```

### Category Focus

```
/audit-sensory [prose_file.md]
→ Returns: Category A detailed breakdown
→ Word counts by type
→ Missing sensory suggestions
```

---

## Grade Thresholds

| Score | Grade | Action |
|-------|-------|--------|
| 95-100 | 🔥 GOONER PERFECTION | Ship immediately |
| 85-94 | ✅ APPROVED | Minor fixes optional |
| 70-84 | ⚠️ NEEDS REVISION | Fix before shipping |
| <70 | ❌ FAILED | Major rewrite required |

---

## Technical Details

### Source Framework

`{project-root}/studio/docs/GOONER_AUDIT_FRAMEWORK.md`

### Keyword Lists

- Smell: `{project-root}/studio/docs/GOONER_AUDIT_FRAMEWORK.md#smell-words`
- Banned: `{project-root}/studio/docs/GOONER_AUDIT_FRAMEWORK.md#banned-words`

---

_Module for LND Studio | Primary QA automation for gooner-editor_
