---
name: 'step-04-prose-generation'
description: 'Invoke prose-adapter for prose generation'

nextStepFile: './step-05-quality-audit.md'
proseAdapterWorkflow: '{{project_root}}/studio/core/lewd-writer/references/workflow.md'
stateFile: '{{run_dir}}/_pipeline/{{project_name}}/state.yaml'
analysisFolder: '{{run_dir}}/_analysis/{{project_name}}'
proseFolder: '{{run_dir}}/_prose/{{project_name}}'
templateFile: '{{project_root}}/studio/context/mandatory/03-prose-template.md'
dialogueRulesFile: '{{project_root}}/studio/context/mandatory/02-dialogue-format.md'
contextManifest: '{{project_root}}/studio/context/mandatory/_MANIFEST.md'
---

# Step 4: Prose Generation

**Progress: Step 4 of 7** - Next: Quality Audit

## RULES

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- MUST check forensic gate BEFORE any prose work.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in Vietnamese

## CONTEXT

- Requires forensic report from Step 2.
- Requires context loaded from Step 3.
- Focus: Invoke /prose-adapter for prose generation.
- Output: Prose at {{proseFolder}}/page-{{XXX}}.md

---

## 0. PRE-EXECUTION GATE (MANDATORY)

### a) Load Pipeline State

Read `{{stateFile}}` and extract:

- `current_page`
- `forensics_completed`
- `context_loaded`

### b) FORENSIC GATE CHECK

```
🚫 GATE CHECK: FORENSIC REQUIRED

Expected: {{analysisFolder}}/page-{{current_page}}-forensic.md

IF FILE NOT EXISTS:
  ─────────────────────────────────────────────
  🚫 FORENSIC GATE BLOCKED
  📋 Missing: {{analysisFolder}}/page-{{current_page}}-forensic.md
  📤 ACTION: Return to Step 2 (Forensic Analysis)
  ─────────────────────────────────────────────
  
  HALT - DO NOT PROCEED
  Load step-02-forensic-analysis.md

IF FILE EXISTS:
  ✅ Forensic gate passed
  PROCEED
```

### c) CONTEXT GATE CHECK

```
IF current_page NOT IN context_loaded:
  ⚠️ Context not loaded for this page
  Recommend: Return to Step 3
  [C] Continue anyway | [B] Back to Context Loading
  
  HALT and wait
```

---

## GATE -1: MANDATORY CONTEXT STACK LOAD

**BEFORE any delegation to Suki, you MUST load the entire mandatory context stack:**

```text
1. READ {{contextManifest}} → Extract the strict load order
2. READ 00-anti-slop.md
3. READ 01-writing-mechanics.md
4. READ 02-dialogue-format.md
5. READ 03-prose-template.md
6. READ 04-language.md
7. READ 05-quality-criteria.md
8. PASS ALL AS CONTEXT to prose-adapter invocation
```

```text
🚫 GATE -1 CHECK:

IF the 6 mandatory context files are NOT loaded:
  ─────────────────────────────────────────────
  🚫 CONTEXT STACK GATE BLOCKED
  📋 Missing: One or more mandatory context files
  📤 ACTION: Load all 6 files before proceeding
  ─────────────────────────────────────────────
  
  HALT — DO NOT DELEGATE WITHOUT FULL CONTEXT STACK

IF context stack loaded:
  ✅ Context stack gate passed — rules are active
  PROCEED to delegation
```

**WHY THIS EXISTS:** Suki cannot enforce rules she was never given. This gate ensures the Anti-Slop directive and all core mechanics are always injected into the prose-adapter call.

---

## GATE -2: IMAGE CROSS-REFERENCE (RECOMMENDED — RETRO FIX 2026-04-25)

> [!TIP]
> Added after the Page 004 Incident. Suki can now cross-reference the original image
> via `image_path` in the forensic report frontmatter.

```text
1. READ forensic report frontmatter
2. EXTRACT image_path field
3. IF image_path EXISTS:
   → Suki MAY call view_file(image_path) to verify visual accuracy
   → This is RECOMMENDED but not MANDATORY for Suki
   → Riko MUST use image_path for audit cross-reference in Step 5
4. IF image_path NOT EXISTS:
   → Log warning: "⚠️ Forensic report missing image_path — Riko audit will be limited"
   → PROCEED (non-blocking)
```

---

## GATE -3: VIETNAMESE PRONOUN VERIFICATION (MANDATORY — RETRO FIX 2026-04-25)

> [!CAUTION]
> Added after the Senpai Pronoun Incident (Batch 2).
> Suki used "cậu/tao" (hostile/equal) instead of "em/anh" (senior authority) for senpai→kouhai dialogue.
> Coercion ≠ Hostility. Power dynamic must be reflected in pronouns.

```text
BEFORE finalizing prose output, Suki MUST:

1. READ {{dialogueRulesFile}} → VIETNAMESE PRONOUN SYSTEM section
2. For EACH dialogue line, verify:
   - Speaker's relationship to listener (senpai/kouhai, teacher/student, etc.)
   - Correct pronoun pair from lookup table
3. PRONOUN RULE: Xưng hô reflects POWER DYNAMIC, not hostility
   - Coercive authority = "em/anh" (NOT "cậu/tao")
   - Only switch to "mày/tao" AFTER character is fully mindbroken/objectified
4. IF wrong pronoun detected:
   → AUTO-CORRECT before output
   → Log: "⚠️ Pronoun mismatch corrected: {old} → {new}"
```

---

## SEQUENCE OF INSTRUCTIONS

### 1. Load Required Inputs

**Read forensic report:**

```
forensic_content = READ {{analysisFolder}}/page-{{current_page}}-forensic.md
```

**Extract key data:**

- Panel count
- Character list
- SFX list
- Dialogue list
- Continuity notes

### 2. Announce Delegation

OUTPUT:

```
─────────────────────────────────────────────
📤 DELEGATING TO: Suki ✍️ (Lewd Writer)
📋 TASK: Generate R18 prose for page {{current_page}}
📁 INPUT: {{analysisFolder}}/page-{{current_page}}-forensic.md
📁 OUTPUT: {{proseFolder}}/page-{{current_page}}.md
─────────────────────────────────────────────
```

### 3. Invoke Prose-Adapter

**CRITICAL**: Load and execute `{{proseAdapterWorkflow}}` with:

- Forensic path: `{{analysisFolder}}/page-{{current_page}}-forensic.md` ( GROUND TRUTH )
- Context path: `{{run_dir}}/{{chapter}}/{{page}}/context_horizon.md` ( UPCOMING SCENE TRAJECTORY )
- Context: Story bible loaded in Step 3
- Action Deduplicator: Check `context_horizon.md` for merge recommendations. If flagged, MERGE redundant frames into a single, cohesive Action Beat.
- Output: `{{proseFolder}}/page-{{current_page}}.md`

**DO NOT write prose yourself. INVOKE the workflow.**

```
🚨 DIRECTOR K DOES NOT WRITE PROSE 🚨

You MUST invoke /prose-adapter (executed by /lewd-writer Suki)
You do NOT write prose yourself
```

### 4. Wait for Completion

Prose-adapter will:

1. ✅ Load context and forensic
2. ✅ Plan scene structure
3. ✅ Write environment (sensory density)
4. ✅ Write action (explicit detail)
5. ✅ Integrate dialogue (Vietnamese)
6. ✅ Add SFX (Romanized Japanese)
7. ✅ Polish aftermath
8. ✅ Self-check quality

### 5. Verify Prose Output

**GATE 0 - ANTI-CONTAMINATION (MANDATORY, RUN FIRST)**

Scan generated prose for context leaks. These patterns MUST NOT appear:

```
BLOCKED_PATTERNS = [
  "*_research",      # Internal research file names
  "*_lexicon",       # Internal lexicon file names  
  "references/workflow.md",     # Workflow references
  "state.yaml",      # Pipeline references
  "forensic-gate",   # System gate references
  "step-0",          # Step file references
  "lewd-writer",     # Agent names
  "panel-forensic",  # Agent names
  "gooner-audit",    # Agent names
  "gooner-alchemist",# Service names
  "Director K",      # Agent personas
  "lnd-orchestrator", # System names
  "sensory_density", # Rule file names
  "quality_gates",   # Rule file names
  ".agent.yaml",     # Config files
  "hentai_lexicon",  # Knowledge base files
]
```

```
IF ANY BLOCKED_PATTERN found in prose:
  ─────────────────────────────────────────────
  🚫 GATE 0 FAILED: CONTEXT CONTAMINATION DETECTED
  📋 Found: {pattern} at line {line_number}
  📋 Content: "{contaminated_line}"
  📤 ACTION: Auto-rewrite contaminated lines, re-verify
  ─────────────────────────────────────────────
  
  DO NOT PROCEED TO QUALITY CHECKS
  FIX contaminated lines FIRST, then re-run Gate 0
```

**GATE 1 - QUALITY CHECK**

```markdown
## Prose Output Verification

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Gate 0 (contamination) | 0 matches | | |
| File exists | {{proseFolder}}/page-{{current_page}}.md | ✓/✗ | |
| Word count | ≥500 | | |
| Sensory count | ≥8 | | |
| SFX present | ≥3 | | |
| Dialogue present | ≥1 | | |
| Format compliance | Header + 「」Dialogue + *SFX:* | | |
| Self-audit score | ≥75 | | |
```

**IF ANY CHECK FAILS:**

```
⚠️ PROSE INCOMPLETE
Missing: {list_failed_checks}
ACTION: Re-invoke prose-adapter with feedback
```

### 6. Update Pipeline State

Update `{{stateFile}}`:

```yaml
prose_completed:
  - ... existing ...
  - {{current_page}}  # ADD this
```

### 7. Present Checkpoint Menu

OUTPUT:

```
✅ Prose generation complete for page {{current_page}}!

📄 Output: {{proseFolder}}/page-{{current_page}}.md
📊 Self-Score: {{score}}/100
🔢 Word Count: {{count}}
🔄 Attempt: {{X}}/3

**Select:** [C] Continue to Audit | [V] View Prose | [R] Regenerate
```

**HALT and wait for user selection.**

#### Menu Handling Logic

- IF C:
  - VERIFY prose file exists (GATE CHECK)
  - IF EXISTS: Update state, load `./step-05-quality-audit.md`
  - IF NOT EXISTS: "🚫 Cannot proceed - prose missing" → Stay here
- IF V: Display prose contents, redisplay menu
- IF R: Re-invoke prose-adapter, return to Step 4
- IF Any other: Respond helpfully, redisplay menu

#### EXECUTION RULES (Interactive Mode)

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.

#### EXECUTION RULES (Batch Mode — `--batch`)

- ✅ **AUTO-CONTINUE**: If batch mode is active, skip the HALT and auto-select `[C]`.
- ✅ Gate checks still apply — if prose file is missing, HALT even in batch mode.
- ✅ After prose is complete, automatically proceed to Step 5 (Quality Audit).

---

## REQUIRED OUTPUTS

- MUST invoke /prose-adapter workflow (NOT write directly)
- MUST meet minimum quality thresholds
- MUST update pipeline state

## VERIFICATION CHECKLIST

- [ ] Forensic gate checked FIRST
- [ ] Context gate checked
- [ ] Delegation banner displayed
- [ ] /prose-adapter invoked (NOT self-written)
- [ ] Prose verified with all checks passed
- [ ] `prose_completed` updated in state
- [ ] User selected [C] to continue

---

## 🚨 SYSTEM FAILURE CONDITIONS

Director K writing prose = **PROTOCOL VIOLATION**
Missing forensic file = **GATE BLOCKED - RETURN TO STEP 2**
Skipping to audit without prose = **PIPELINE FAILURE**
Internal file names in prose output = **GATE 0 CONTAMINATION - AUTO-REWRITE**

**Master Rule:** FORENSIC GATE. DELEGATE. GATE 0 SCAN. VERIFY. Never write directly.
