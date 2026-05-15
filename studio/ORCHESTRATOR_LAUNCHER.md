# 🎬 LND Studio Orchestrator — Architecture Guide

## Correct 6-Layer Execution Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 1: ORCHESTRATOR (lnd-orchestrator.agent.yaml)               │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ Director K receives: /gooner-alchemist                         ││
│  │ - Reads hierarchy.owns[] → knows agents                         ││
│  │ - menu: defines delegation FLOW                                ││
│  │ - Delegates to AGENT, NOT directly to SKILL.md                 ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
                                ↓ Orch DELEGATES to AGENT
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 2: AGENT (e.g., manga-adapter.agent.yaml)                    │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ Kana agent activates                                            ││
│  │ - Defines persona, communication_style                          ││
│  │ - Has skill reference: core/panel-forensic/SKILL.md            ││
│  │ - Loads its SKILL.md                                            ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
                                ↓ Agent LOADS its SKILL.md
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 3: SKILL.md (workflow) (e.g., core/panel-forensic/SKILL.md)  │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ SKILL.md contains:                                               ││
│  │ - injection: always[], triggers[] (knowledge loading)           ││
│  │ - steps/: step files with execution logic                      ││
│  │ - references/: supporting docs                                 ││
│  │ - Output: forensic-state.json                                   ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 4: RESOURCE LAYER (steps/, resources/, tools/)              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Menu Triggers (Orch → Agent → SKILL.md)

| Trigger | Orch Delegates to → | Agent Loads → | Output |
|---------|---------------------|---------------|--------|
| **MA** | Kana → Aria → Suki → Riko | panel-forensic → lewd-writer → quality-audit | draft-prose.json |
| **EC** | Kana → Suki | panel-forensic → lewd-writer | caption.json |
| **ND** | Luna → Kana → Suki | novel-development → panel-forensic → lewd-writer | novel-outline.md |
| **VC** | Kana | manga-context-extractor/SKILL.md | volume_context.md |
| **PA** | Suki | lewd-writer/SKILL.md | draft-prose.json |
| **QA** | Riko | quality-audit/SKILL.md | audit-report.json |
| **CB** | Aria | character-builder/SKILL.md | character-bible.json |
| **RC** | Orchestrator → Riko | chapter-composer → quality-audit | chapter.md |
| **BS** | Aria | bible-sync/SKILL.md | bible-sync.json |
| **DC** | Miki | dialogue-scripting/SKILL.md | dialogue.json |
| **SE** | Suki | scene-expansion/SKILL.md | expanded-prose.md |
| **PT** | (multi-agent) | party-mode/SKILL.md | discussion-log.md |
| **PR** | (report) | — | performance-report.md |

---

## Example Flow: MA (Manga-to-Novel)

```
USER: "MA"

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: Orchestrator receives MA                                      │
│ lnd-orchestrator.agent.yaml                                          │
│ menu.MA → "DELEGATE TO KANA (manga-adapter.agent.yaml)"              │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Kana activates                                                │
│ manga-adapter.agent.yaml                                             │
│ → Loads: core/panel-forensic/SKILL.md                                │
│ → injection triggers: "explicit" → loads r18_sensory_pack.md        │
│ → Output: forensic-state.json                                        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: Aria activates (if character updates needed)                  │
│ character-architect.agent.yaml                                       │
│ → Loads: services/character-builder/SKILL.md                        │
│ → Output: character-bible.json                                        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 4: Suki activates                                               │
│ lewd-writer.agent.yaml                                              │
│ → Loads: core/lewd-writer/SKILL.md                                  │
│ → injection triggers: "bedroom" → loads sensory_density.md          │
│ → Input: forensic-state.json + character-bible.json                  │
│ → Output: draft-prose.json                                          │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 5: Riko activates                                               │
│ gooner-editor.agent.yaml                                            │
│ → Loads: services/quality-audit/SKILL.md                            │
│ → Input: draft-prose.json                                           │
│ → Output: audit-report.json (PASS/FAIL)                             │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ COMPLETE: Orchestrator compiles results → User                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Key Architecture Rules

### ✅ DO (Correct)

```
Orch → Agent → SKILL.md → steps/
```

### ❌ DON'T (Violation)

```
Orch → SKILL.md (bypass Agent layer)
```

---

## Hierarchy Reference

```
lnd-orchestrator (Layer 1)
  ├── OWNS (Layer 2):
  │   ├── manga-adapter (Kana)
  │   ├── lewd-writer (Suki)
  │   ├── gooner-editor (Riko)
  │   ├── character-architect (Aria)
  │   ├── dialogue-crafter (Miki)
  │   └── world-weaver (Luna)
  │
  └── DELEGATES TO:
      ├── services/gooner-alchemist (pipeline)
      ├── services/quality-audit
      ├── services/bible-sync
      └── services/character-builder
```

---

*Refactored: 2026-05-02 — v1.0.0 (Correct Architecture)*
*Orchestrator now follows Layer 1 → 2 → 3 flow*
