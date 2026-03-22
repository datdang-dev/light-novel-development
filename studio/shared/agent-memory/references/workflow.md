---
name: 'agent-memory'
description: 'Persistent learning layer for specialist agents — records what works and what fails across pipeline runs.'
---

# Agent Memory Layer (Optimization #7)

**Purpose:** Give specialist agents (primarily Suki and Riko) persistent memory across pipeline runs, so they learn from past successes and failures instead of starting cold every time.

## RULES

- ✅ Memory files are APPEND-ONLY (never delete past learnings)
- Memory is READ during Step 3 (Context Loading) as part of JIT payload
- Memory is WRITTEN during Step 6 (State Persistence) after successful audit

---

## MEMORY FILE STRUCTURE

Each agent's memory is stored at:

```text
{output_folder}/_pipeline/{project}/agent-memory/
├── suki-memory.md        # Suki's learned preferences
├── riko-memory.md         # Riko's scoring patterns
└── kana-memory.md         # Kana's recurring forensic notes
```

---

## WHEN TO WRITE (Step 6 — After Audit PASS)

After a page passes audit, extract and append learnings:

```text
FOR suki-memory.md:
  - IF audit score ≥ 90:
    → Record: "Page {X}: Vibes {scene_tags}. Từ vựng hiệu quả: {top_3_words}. Sensory ratio: {smell}/{sound}/{texture}."
  - IF revision was needed:
    → Record: "Page {X}: Riko flagged {category}. Fixed by {fix_description}. Avoid: {bad_pattern}."

FOR riko-memory.md:
  - Record: "Page {X}: Score {score}. Weakest: {category} ({score}). Strongest: {category} ({score})."

FOR kana-memory.md:
  - IF Forensic Cache was used:
    → Record: "Page {X}: Reused baseline from page {X-1}. Delta items: {count}."
```

---

## WHEN TO READ (Step 3 — Context Loading)

During JIT Context Sharding, check if agent memory exists:

```text
IF {output_folder}/_pipeline/{project}/agent-memory/suki-memory.md EXISTS:
  → Append to Suki's context payload:
    "## PAST LEARNINGS (from previous pages in this chapter):\n{file_content}"
  → This gives Suki 'experience' without loading full rules

IF memory file exceeds 2000 tokens:
  → Summarize: Keep only the last 10 entries + a 3-line summary of all-time patterns
```

---

## VERIFICATION CHECKLIST

- [ ] Memory directory created during pipeline init
- [ ] Memory files written after each audit PASS
- [ ] Memory files read during context loading
- [ ] Memory files capped at reasonable token count
