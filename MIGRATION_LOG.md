# LND Studio Migration Log

## 2026-05-05: Wrapper Pattern Implementation

### Problem
Claude Code cannot read image files via Read tool (unlike other tools like Antigravity). The previous symlink approach (`lnd-core`, `lnd-services`) bypassed Claude Code-specific constraints and caused three critical issues:

1. **Image input handling** - Attempted to use Read tool on image paths (fails in Claude Code)
2. **Missing dialogue extraction** - No OCR/text bubble detection in forensic analysis
3. **Fetish over-enforcement** - Agents invented scenarios to force-fit user fetishes, causing hallucination

### Solution
Implemented wrapper pattern in `.claude/skills/` (similar to `.claude/agents/*` structure):

- Wrappers reference `studio/` files directly (no symlinks)
- Embed Claude Code-specific instructions
- Enforce fetish usage protocol (REFERENCE not ENFORCE)

### Files Created

1. **`studio/rules/fetish_usage_protocol.md`**
   - Defines REFERENCE vs ENFORCE distinction
   - Stage-specific guidelines (Kana/Luna/Suki)
   - Three-tier marking system (✅/⚠️/❌)
   - Quality gate checklist

2. **`.claude/skills/panel-forensic/SKILL.md`** (directory-based)
   - Image input handling protocol
   - Chat embedding requirement
   - Delegation instructions for Kana

3. **`.claude/skills/erotic-caption-writer/SKILL.md`** (directory-based)
   - Fetish usage enforcement
   - Quality gates
   - Delegation instructions for Suki

4. **`.claude/skills/scene-prelude/SKILL.md`** (directory-based)
   - Scenario grounding in forensics
   - Fetish expansion rules
   - Delegation instructions for Luna

5. **`.claude/skills/README.md`**
   - Documentation of wrapper pattern
   - Migration notes

### Structure Migration (2026-05-05)

**Problem:** Initial implementation used flat `.md` files, inconsistent with existing `lnd-orchestrator/` directory pattern.

**Solution:** Migrated to directory-based structure:
- `panel-forensic.md` → `panel-forensic/SKILL.md`
- `erotic-caption-writer.md` → `erotic-caption-writer/SKILL.md`
- `scene-prelude.md` → `scene-prelude/SKILL.md`

All wrappers now follow consistent pattern: `.claude/skills/{skill-name}/SKILL.md`

### Namespace Prefixing (2026-05-05)

**Problem:** LND Studio skills lacked namespace distinction from other Claude Code skills.

**Solution:** Added `lnd-` prefix to all LND Studio wrapper skills:
- `panel-forensic/` → `lnd-panel-forensic/`
- `erotic-caption-writer/` → `lnd-erotic-caption-writer/`
- `scene-prelude/` → `lnd-scene-prelude/`
- `lnd-orchestrator/` (already had prefix)

**Wrapper Conversion:** Converted `lnd-orchestrator/SKILL.md` from standalone implementation to proper wrapper pattern:
- Now references `studio/services/lnd-orchestrator/` as core implementation
- Added Claude Code-specific adaptations (image handling, agent delegation)
- Follows same wrapper pattern as other three skills

### Files Removed

- `.claude/skills/lnd-core` (symlink)
- `.claude/skills/lnd-services` (symlink)

### Validation

Tested with goblin suit exhibitionism image:
- ✅ Forensic analysis with actual image viewing
- ✅ Fetish matching without hallucination
- ✅ Vietnamese R18 caption generation (287 words)
- ✅ Sensory density compliance
- ✅ Pronoun consistency (ta-ngươi register)

### Next Steps

Additional wrappers may be needed for:
- `studio/core/lewd-writer/` (if used standalone)
- `studio/core/roleplay-engine/` (if used)
- `studio/services/gooner-alchemist/` (8-step pipeline)
- `studio/services/quality-audit/` (Riko's audit framework)

Create wrappers on-demand as pipelines are used.
