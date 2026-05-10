# Quality Gates (Gooner Audit Framework)

## Scoring Categories (100 Points Total)

| Category | Weight | Description |
|----------|--------|-------------|
| A: Sensory Density | 25 | Smell ≥3, Sound ≥3, Texture ≥5, Temperature on fluid |
| B: Anti-Slop | 20 | No banned words, entropy ≥3.5, no n-gram repeat >5% |
| C: Psychological Depth | 15 | Internal monologue, character-specific reactions |
| D: Dialogue Quality | 15 | SFX on every line, correct brackets, voice consistency |
| E: Continuity | 10 | Residue tracking, clothing state, position logic |
| F: Cultural Compliance | 15 | F1-F4 JP reader psychology gates |

## Thresholds

| Score | Verdict | Action |
|-------|---------|--------|
| ≥85 | PASS | Proceed to state persistence |
| 70-84 | REVIEW | Flag issues, allow minor fixes |
| <70 | FAIL | Rewrite required |

## Category F: Cultural Compliance (F1-F4)

| Gate | JP Concept | Check |
|------|-----------|-------|
| F1 | 納得感 (Nattoku-kan) | Does the scene make emotional/logical sense? |
| F2 | 背徳感 (Haitoku-kan) | Is the taboo thrill present? |
| F3 | ギャップ萌え (Gap Moe) | Is there contrast between appearance and action? |
| F4 | 征服感 (Seifuku-kan) | Is the power dynamic clear? |

**Rule**: If F-score < 10/15, draft FAILS regardless of total score.

## Auto-Fail Conditions

- ANY banned word from `studio/data/banned-words.txt` → instant FAIL
- Missing SFX on dialogue line → -5 per occurrence
- No smell in explicit scene → -10
- Clinical anatomy term used → -5 per occurrence
