# LND Studio v7.0 — Auditor Briefing

**For:** Human Auditor
**From:** Opus 4.5 (AI Refactoring)
**Date:** 2026-05-02

---

## TL;DR

This is a **prompt engineering framework** for R18 light novel writing. The refactoring:

1. Fixed the Orchestrator (was bypassing Agent layer)
2. Added knowledge injection via scene_tags
3. Cleaned legacy files
4. Created 3 new agents for game adaptation

---

## Key Questions for Auditor

### 1. Architecture
- Is the 6-layer model correct and maintainable?
- Should `services/` vs `core/` boundary be clearer?
- Is Layer -1 (Infrastructure) naming appropriate?

### 2. Orchestrator Flow
- **Before:** Orch → SKILL.md (direct)
- **After:** Orch → Agent → SKILL.md

Is the new flow correct? Any edge cases where direct SKILL.md load is needed?

### 3. Knowledge Injection
- `injection.always:` — always loaded
- `injection.triggers:` — loaded based on scene_tag

Is this pattern sustainable? Should triggers be validated automatically?

### 4. Agent Coverage
- All 10 services now have corresponding agents
- 3 new agents: Ren (Ren'Py), Rex (RPG Maker), Nova (Caption)

Is the agent count appropriate? Too many? Too few?

### 5. Testability
- No automated tests exist
- Manual trigger testing required

What test strategy would you recommend?

---

## File Locations

| Document | Path |
|----------|------|
| **Full Report** | `studio/REFACTORING_REPORT.md` |
| **Orchestrator** | `studio/agents/lnd-orchestrator.agent.yaml` |
| **Agent Registry** | `studio/agents/agent-registry.yaml` |
| **Architecture Doc** | `studio/docs/ARCHITECTURE.md` |
| **Knowledge Index** | `studio/knowledge/knowledge-index.yaml` |
| **Sample SKILL.md** | `studio/core/lewd-writer/SKILL.md` |

---

## What Changed (Summary)

| Change | Before | After |
|--------|--------|-------|
| Orchestrator flow | Direct to SKILL.md | Via Agent |
| Knowledge injection | Manual in step files | YAML triggers in SKILL.md |
| Agent registry | CSV (static) | YAML (single source) |
| Invalid services | 3 active (bible-sync, etc.) | Deleted |
| Legacy files | Scattered | Archived |
| Agent count | 9 | 12 (added Ren, Rex, Nova) |

---

## Next Steps

1. **Auditor reviews** REFACTORING_REPORT.md
2. **Test flow:** Trigger `/MA` and verify Orch → Kana → Suki → Riko
3. **Validate injection:** Check if scene_tags load correct knowledge
4. **Report findings:** Any architectural issues, missing pieces, cleanup suggestions

---

*Questions? Start with `studio/REFACTORING_REPORT.md` for full details.*