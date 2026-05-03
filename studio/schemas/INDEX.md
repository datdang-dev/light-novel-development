# LND Studio Schema Index

## Schemas

| Schema | Purpose | Agent | Status |
|--------|---------|-------|--------|
| `pipeline-state.schema.json` | Pipeline execution state | lnd-orchestrator | ✅ Active |
| `forensic-state.schema.json` | Visual forensic output | manga-adapter | ✅ Active |
| `draft-prose.schema.json` | Prose output | lewd-writer | ✅ Active |
| `character-bible.schema.json` | Character profiles | character-architect | ✅ Active |
| `audit-report.schema.json` | QA audit results | gooner-editor | ✅ Active |
| `continuity-ledger.schema.json` | Story continuity tracking | all agents | ✅ Active |

## Usage Rules

1. **ALL agents MUST validate output against their respective schema before handoff**
2. **IF schema validation FAILS: DO NOT output, inline fix and retry**
3. **Circuit breaker: If audit fails 3 times → HALT pipeline, report to orchestrator**

## Schema Validation Checklist

Before finalizing ANY output:
- [ ] Conforms to corresponding schema in this directory
- [ ] No BANNED_WORDS from `canon-rules.md`
- [ ] 100% Vietnamese prose (for narrative output)
- [ ] All required fields populated
- [ ] Optional fields null-checked

## Update Log

| Date | Change | By |
|------|--------|-----|
| 2026-05-02 | Added pipeline-state.schema.json | team-lead |
| 2026-05-02 | Created this INDEX.md | team-lead |