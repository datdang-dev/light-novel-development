---
name: "forensic-gate"
description: "Hard gate: Block prose generation without forensic report"
priority: 0
applies_to: ["lewd-writer", "prose-adapter", "gooner-alchemist"]
---

# Forensic Gate Rule

> **PRIORITY 0** - This rule overrides all other rules.

## Rule Statement

```
🚫 PROSE GENERATION IS BLOCKED UNTIL FORENSIC REPORT EXISTS 🚫
```

## Gate Check Sequence

Before writing ANY prose for a page, you MUST:

### 1. Check for Forensic Report

```
REQUIRED: {output_folder}/_analysis/{manga_name}/page-{XXX}-forensic.md
```

### 2. Validation Logic

```python
def can_generate_prose(page_number: str) -> bool:
    forensic_path = f"_lnd-output/_analysis/{manga}/page-{page_number}-forensic.md"
    
    if not file_exists(forensic_path):
        return False  # BLOCKED
    
    return True  # ALLOWED
```

### 3. If Forensic Missing

**STOP IMMEDIATELY** and output:

```
─────────────────────────────────────────────
🚫 FORENSIC GATE BLOCKED
📋 Missing: {expected_forensic_path}
📤 ACTION: Delegate to /panel-forensic first
─────────────────────────────────────────────
```

Then invoke `/panel-forensic` workflow for that page.

### 4. Only After Forensic Exists

Proceed to prose generation using forensic report as source material.

---

## Per-Page Enforcement

When processing multiple pages:

```
FOR EACH page in page_range:
    1. CHECK forensic exists for this page
    2. IF NOT: invoke /panel-forensic, WAIT
    3. READ forensic report
    4. THEN generate prose
    5. NEXT page
```

**NO BATCHING**: Process pages ONE BY ONE with forensic → prose → next.

---

## Zero-Skip Verification

Each forensic report MUST contain:

| Section | Required |
|---------|----------|
| Panel Layout | ✅ |
| Character ID | ✅ |
| Body Scan | ✅ |
| Fluid Scan | ✅ |
| SFX Extraction | ✅ |
| Dialogue | ✅ |
| Psychological Scan | ✅ |
| Smell Matrix | ✅ |
| Sound Matrix | ✅ |
| Continuity Notes | ✅ |

If ANY section missing → forensic report is INVALID → re-run forensic.

---

## Violation Consequences

If prose is generated without forensic:

1. **Prose is INVALID** - must be regenerated
2. **User should be notified** of protocol breach
3. **Forensic must be generated** retroactively
4. **Prose must be rewritten** using forensic data

---

*This gate ensures no visual details are missed in adaptation.*
