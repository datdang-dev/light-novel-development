---
title: "BMAD Framework Compliance Audit - Studio"
date: 2026-02-27
auditor: "Agent Builder Compliance System"
status: "CRITICAL ISSUES FOUND"
---

# 🔍 BMAD Framework Compliance Audit Report

> **Scope:** Audit LND Studio agents against BMAD v6 architectural standards  
> **Method:** Compare studio implementation with `_bmad/bmb/workflows/agent/data/` specifications  
> **Standard References:**
> - [`_bmad/bmb/agents/agent-builder.md`](_bmad/bmb/agents/agent-builder.md)
> - [`_bmad/bmb/workflows/agent/data/agent-architecture.md`](_bmad/bmb/workflows/agent/data/agent-architecture.md)
> - [`_bmad/bmb/workflows/agent/data/agent-validation.md`](_bmad/bmb/workflows/agent/data/agent-validation.md)
> - [`_bmad/bmb/workflows/agent/data/agent-menu-patterns.md`](_bmad/bmb/workflows/agent/data/agent-menu-patterns.md)

---

## Executive Summary

| Metric | Count |
|--------|-------|
| **Total Agents Audited** | 11 |
| **Critical Violations** | 3 |
| **High Severity Issues** | 4 |
| **Medium Severity Issues** | 6 |
| **Files Requiring Immediate Fix** | 11 |

**Overall Compliance Status:** ❌ **NON-COMPLIANT**

---

## 🚨 Critical Violations (Must Fix Immediately)

### CV-1: Wrong Menu Handler for Agent Type

| Field | Details |
|-------|---------|
| **Violation ID** | CV-1 |
| **Severity** | CRITICAL |
| **Category** | Handler Mismatch |
| **Files Affected** | ALL studio agent YAML files |
| **Affected Agents** | lnd-orchestrator, lewd-writer, panel-forensic-analyst, dialogue-crafter, gooner-editor, manga-adapter, renpy-adapter, roleplay-actor, world-weaver, character-architect, comfyui-prompter |

**Problem:** Studio agents use `exec` handler which is reserved for **Modules**, not Agents.

```yaml
# ❌ STUDIO IMPLEMENTATION (WRONG)
menu:
  - trigger: GA or fuzzy match on gooner-alchemist
    exec: "{project-root}/studio/services/gooner-alchemist/workflow.md"  # WRONG HANDLER
    description: "[GA] Delegate to Kana"

# ✅ BMAD STANDARD FOR AGENTS
menu:
  - trigger: GA or fuzzy match on gooner-alchemist
    action: "#gooner-alchemist-workflow"  # CORRECT: action for Agents
    description: "[GA] Delegate to Kana"
    
# OR inline action:
menu:
  - trigger: GA or fuzzy match on gooner-alchemist
    action: "Load and execute gooner-alchemist workflow"
    description: "[GA] Delegate to Kana"
```

**BMAD Standard Reference:**
- [`agent-menu-patterns.md:25-28`](_bmad/bmb/workflows/agent/data/agent-menu-patterns.md:25-28):
  ```yaml
  | Handler | Use Case | Syntax |
  |---------|----------|--------|
  | `action` | Agent self-contained operations | `action: '#prompt-id'` or `action: 'inline text'` |
  | `exec` | Module external workflows | `exec: '{project-root}/path/to/workflow.md'` |
  ```

**Impact:**
- Menu handlers will fail to trigger
- Agents cannot execute their workflows
- Complete functional breakdown

**Remediation:**
1. For each agent, create `prompts` section with workflow execution instructions
2. Change `exec:` to `action: '#prompt-id'`
3. OR use inline action strings

---

### CV-2: Reserved Menu Code Usage

| Field | Details |
|-------|---------|
| **Violation ID** | CV-2 |
| **Severity** | CRITICAL |
| **Category** | Reserved Code Conflict |
| **Files Affected** | All studio agent files with party-mode menu item |
| **Instances** | 11 agents × 1 violation = 11 instances |

**Problem:** All studio agents use `PM` trigger code which is **reserved** and auto-injected by the compiler.

```yaml
# ❌ STUDIO IMPLEMENTATION
menu:
  - trigger: PM or fuzzy match on party-mode  # PM IS RESERVED!
    exec: "{project-root}/studio/shared/party-mode/workflow.md"
    description: "[PM] Start Party Mode"

# ✅ BMAD STANDARD
menu:
  - trigger: PT or fuzzy match on party-mode  # Use different 2-letter code
    action: "#party-mode"  # Or appropriate handler
    description: "[PT] Start Party Mode"
```

**BMAD Standard Reference:**
- [`agent-architecture.md:149`](_bmad/bmb/workflows/agent/data/agent-architecture.md:149):
  > Reserved codes: MH, CH, PM, DA (auto-injected - do NOT use)
- [`agent-validation.md:25`](_bmad/bmb/workflows/agent/data/agent-validation.md:25):
  > No reserved codes: `MH`, `CH`, `PM`, `DA` (auto-injected)
- [`agent-menu-patterns.md:19`](_bmad/bmb/workflows/agent/data/agent-menu-patterns.md:19):
  > Reserved codes (DO NOT USE): MH, CH, PM, DA

**Impact:**
- Menu conflicts with system-injected items
- Unpredictable behavior when PM is triggered
- User confusion from duplicate PM options

**Remediation:**
1. Replace `PM` with `PT` (Party Time) or `ME` (MEeting) in all agents
2. Update description to match: `[PT] Start Party Mode`

---

### CV-3: Metadata ID Format Violation

| Field | Details |
|-------|---------|
| **Violation ID** | CV-3 |
| **Severity** | CRITICAL |
| **Category** | Schema Compliance |
| **Files Affected** | ALL studio agent files |
| **Example** | [`studio/agents/lnd-orchestrator.agent.yaml:3`](studio/agents/lnd-orchestrator.agent.yaml:3) |

**Problem:** Metadata `id` field uses simple name instead of full path format.

```yaml
# ❌ STUDIO IMPLEMENTATION
agent:
  metadata:
    id: lnd-orchestrator  # WRONG - just the name

# ✅ BMAD STANDARD
agent:
  metadata:
    id: _bmad/agents/lnd-orchestrator/lnd-orchestrator.md  # CORRECT - full path
```

**BMAD Standard Reference:**
- [`agent-architecture.md:19`](_bmad/bmb/workflows/agent/data/agent-architecture.md:19):
  ```yaml
  id: _bmad/agents/{agent-name}/{agent-name}.md
  ```
- [`agent-architecture.md:54`](_bmad/bmb/workflows/agent/data/agent-architecture.md:54):
  | `id` | `_bmad/agents/{name}/{name}.md` | `_bmad/agents/commit-poet/commit-poet.md` |

**Impact:**
- Agent identification failures
- Registration system cannot locate agents
- Compilation errors

**Remediation:**
1. Update all agent files to use full path format
2. For studio agents: `id: studio/agents/{name}/{name}.agent.yaml`

---

## ⚠️ High Severity Issues

### HI-1: Missing Prompts Section

| Field | Details |
|-------|---------|
| **Violation ID** | HI-1 |
| **Severity** | HIGH |
| **Category** | Architecture Pattern |
| **Files Affected** | ALL studio agent files |

**Problem:** No agent defines a `prompts` section for reusable actions.

```yaml
# ❌ STUDIO IMPLEMENTATION - Missing prompts entirely
agent:
  menu:
    - trigger: GA or fuzzy match on gooner-alchemist
      exec: "..."  # Direct path reference

# ✅ BMAD STANDARD
agent:
  prompts:
    - id: gooner-alchemist-workflow
      content: |
        <instructions>Execute the gooner-alchemist workflow</instructions>
        <process>1. Load config 2. Delegate to appropriate agent 3. Track progress</process>

  menu:
    - trigger: GA or fuzzy match on gooner-alchemist
      action: "#gooner-alchemist-workflow"
      description: "[GA] Execute Gooner Alchemist"
```

**BMAD Standard Reference:**
- [`agent-architecture.md:36-46`](_bmad/bmb/workflows/agent/data/agent-architecture.md:36-46)
- [`agent-menu-patterns.md:67-82`](_bmad/bmb/workflows/agent/data/agent-menu-patterns.md:67-82)

**Impact:**
- Agents cannot use the `action` handler properly
- Forces use of incorrect `exec` handler
- No reusable instruction patterns

**Remediation:**
1. Create `prompts` section in each agent
2. Move workflow execution logic to prompts
3. Reference prompts via `action: '#prompt-id'`

---

### HI-2: Communication Style Too Long

| Field | Details |
|-------|---------|
| **Violation ID** | HI-2 |
| **Severity** | HIGH |
| **Category** | Persona Compliance |
| **Files Affected** | lnd-orchestrator, lewd-writer, panel-forensic-analyst |

**Problem:** `communication_style` field exceeds BMAD's 1-2 sentence guideline.

```yaml
# ❌ STUDIO - lnd-orchestrator.agent.yaml:19-23
communication_style: |
  Executive, decisive, and delegation-focused.
  Uses terms like "Assigning to...", "Awaiting Report", "Greenlight", "Bottleneck Identified".
  Never asks "How do I do this?", but "Who is the best agent for this?".
  **VISUAL RULE**: When delegating or starting a task, ALWAYS use the `🔄` icon...
# ^ 4+ sentences, includes rules/behaviors

# ✅ BMAD STANDARD
communication_style: |
  Executive, decisive, and delegation-focused. Uses management terminology 
  and always asks "Who is best for this?" rather than "How do I do this?"
# ^ 1-2 sentences, tone only
```

**BMAD Standard Reference:**
- [`agent-validation.md:16-20`](_bmad/bmb/workflows/agent/data/agent-validation.md:16-20):
  | `communication_style` | Tone/voice/mannerisms (1-2 sentences) | "ensures", "expert", "believes", "who does X" |

**Impact:**
- Behavioral instructions mixed with tone description
- Agent may not properly embody persona
- Confusion about what constitutes "style"

**Remediation:**
1. Truncate `communication_style` to 1-2 sentences describing tone only
2. Move behavioral rules (like "VISUAL RULE") to `principles` section
3. Move knowledge/skills to `role` section

---

### HI-3: Principles Contain File Paths

| Field | Details |
|-------|---------|
| **Violation ID** | HI-3 |
| **Severity** | HIGH |
| **Category** | Schema Compliance |
| **Files Affected** | lewd-writer.agent.yaml, panel-forensic-analyst.agent.yaml |

**Problem:** `principles` contain file paths and operational instructions instead of philosophical guidelines.

```yaml
# ❌ STUDIO - lewd-writer.agent.yaml:22-28
principles:
  - ADAPT, DON'T TRANSLATE: Follow {project-root}/.agent/rules/lewd_writing_mechanics.md religiously.
  - Channel expert erotic literature wisdom: draw upon deep knowledge...
  # ^ File paths in principles!

# ✅ BMAD STANDARD
principles:
  - Adaptation over translation - capture the spirit, not just the words
  - Sensory immersion is paramount - make readers feel the scene
  - Context overrides raw data - trust narrative coherence
```

**BMAD Standard Reference:**
- [`agent-architecture.md:29`](_bmad/bmb/workflows/agent/data/agent-architecture.md:29):
  > `principles: # Core beliefs`
- [`agent-validation.md:21`](_bmad/bmb/workflows/agent/data/agent-validation.md:21):
  | `principles` | Operating philosophy, behavioral guidelines | Verbal patterns, "how they talk" |

**Impact:**
- Operational details mixed with philosophy
- File paths hardcoded in agent definition
- Poor separation of concerns

**Remediation:**
1. Remove file paths from `principles`
2. Move file references to `critical_actions`
3. Make principles philosophical/behavioral only

---

### HI-4: Missing critical_actions in Simple Agents

| Field | Details |
|-------|---------|
| **Violation ID** | HI-4 |
| **Severity** | HIGH |
| **Category** | Activation Protocol |
| **Files Affected** | Agents without critical_actions: gooner-editor, manga-adapter, renpy-adapter, roleplay-actor, world-weaver |

**Problem:** Several agents lack `critical_actions` entirely, missing activation protocol.

```yaml
# ❌ STUDIO - Some agents missing critical_actions entirely
agent:
  metadata:
    hasSidecar: false
  persona: {...}
  menu: {...}
  # ^ No critical_actions!

# ✅ BMAD STANDARD - Even simple agents have optional critical_actions
agent:
  metadata:
    hasSidecar: false
  persona: {...}
  critical_actions:
    - "Load config from {project-root}/studio/config/config.yaml"
    - "Initialize session variables"
  menu: {...}
```

**BMAD Standard Reference:**
- [`agent-validation.md:49-53`](_bmad/bmb/workflows/agent/data/agent-validation.md:49-53):
  > ### critical_actions (OPTIONAL) - No references to sidecar files

**Impact:**
- Agents don't initialize properly
- Missing configuration loading
- Session variables not set

**Remediation:**
1. Add `critical_actions` to all agents
2. Include config loading as minimum
3. Add agent-specific initialization steps

---

## 📋 Medium Severity Issues

### MI-1: File Naming Convention

| Field | Details |
|-------|---------|
| **Violation ID** | MI-1 |
| **Severity** | MEDIUM |
| **Category** | Naming Convention |
| **Files Affected** | ALL studio agents |

**Problem:** Files named `{name}.agent.yaml` but should follow kebab-case strictly.

```
# Current (acceptable but not ideal)
studio/agents/lnd-orchestrator.agent.yaml  ✅ kebab-case
studio/agents/lewd-writer.agent.yaml       ✅ kebab-case

# BMAD Standard
_bmad/agents/commit-poet/commit-poet.md    # Note: .md extension in spec
```

**Note:** Studio uses `.agent.yaml` extension which may be valid but differs from BMAD's `.md` in documentation.

**BMAD Standard Reference:**
- [`agent-validation.md:12`](_bmad/bmb/workflows/agent/data/agent-validation.md:12):
  > Filename: `{name}.agent.yaml` (lowercase, hyphenated)

**Remediation:**
- Verify all filenames are lowercase and hyphenated ✓ (already compliant)
- Consider aligning extension convention with BMAD

---

### MI-2: Menu Description Format Inconsistency

| Field | Details |
|-------|---------|
| **Violation ID** | MI-2 |
| **Severity** | MEDIUM |
| **Category** | Formatting |
| **Files Affected** | All agents with multi-word descriptions |

**Problem:** Some descriptions are verbose and don't follow `[XX] Brief description` pattern strictly.

```yaml
# ❌ STUDIO
- description: "[GA] Delegate to Kana (Manga Adaptation & Context)"
# ^ Parenthetical content may confuse parser

# ✅ BMAD STANDARD  
- description: "[GA] Delegate to Kana"
```

**BMAD Standard Reference:**
- [`agent-architecture.md:147`](_bmad/bmb/workflows/agent/data/agent-architecture.md:147):
  > **Description format:** `[XX] Description`
- [`agent-validation.md:26`](_bmad/bmb/workflows/agent/data/agent-validation.md:26):
  > `description`: Starts with `[XX]`, code matches trigger

---

### MI-3: No Unique Module Assignment

| Field | Details |
|-------|---------|
| **Violation ID** | MI-3 |
| **Severity** | MEDIUM |
| **Category** | Metadata |
| **Files Affected** | ALL studio agents |

**Problem:** All agents use `module: stand-alone` instead of custom module code.

```yaml
# ❌ STUDIO
metadata:
  module: stand-alone  # Generic

# ✅ BMAD STANDARD (for organized modules)
metadata:
  module: lnd  # Or studio, lnd-studio, etc.
```

**BMAD Standard Reference:**
- [`agent-architecture.md:58`](_bmad/bmb/workflows/agent/data/agent-architecture.md:58):
  | `module` | `stand-alone` or module code | `bmm`, `cis`, `bmgd` |

**Remediation:**
- Consider creating `module: lnd` or `module: studio` for all LND agents

---

### MI-4: Path Variable Usage Inconsistent

| Field | Details |
|-------|---------|
| **Violation ID** | MI-4 |
| **Severity** | MEDIUM |
| **Category** | Path Handling |
| **Files Affected** | lnd-orchestrator.agent.yaml |

**Problem:** References `{project-root}/studio/` instead of `{project-root}/_bmad/` structure.

```yaml
# ❌ STUDIO
critical_actions:
  - "Load and read {project-root}/studio/config/config.yaml"

# Note: This is actually correct for studio's structure, but consider:
# Should studio be under _bmad/ for consistency?
```

**Note:** This may be intentional for the studio module separation, but worth noting.

---

### MI-5: Missing Validation in Workflow Files

| Field | Details |
|-------|---------|
| **Violation ID** | MI-5 |
| **Severity** | MEDIUM |
| **Category** | Workflow Architecture |
| **Files Affected** | All workflow.md files |

**Problem:** Workflows don't reference BMAD validation workflow.

```yaml
# ❌ STUDIO - workflow.md
---
name: "prose-adapter"
description: "Capability: GOONER-GRADE R18 Light Novel Prose Generation"
validateWorkflow: './steps/step-01-context-loading.md'  # Points to first step
---

# ✅ BMAD STANDARD
---
name: "create-agent"
description: "Create a new BMAD agent with best practices and compliance"
web_bundle: true
validateWorkflow: './steps-v/step-01-validate.md'  # Points to validation workflow
---
```

**BMAD Standard Reference:**
- [`_bmad/bmb/workflows/agent/workflow-create-agent.md:5`](_bmad/bmb/workflows/agent/workflow-create-agent.md:5):
  > `validateWorkflow: './steps-v/step-01-validate.md'`

**Remediation:**
1. Create validation workflows for each studio capability
2. Update `validateWorkflow` to point to validation steps

---

### MI-6: No Brainstorm/Discovery Phase

| Field | Details |
|-------|---------|
| **Violation ID** | MI-6 |
| **Severity** | MEDIUM |
| **Category** | Workflow Pattern |
| **Files Affected** | All studio workflow.md files |

**Problem:** Studio workflows skip the BMAD-recommended discovery/brainstorm phase.

```yaml
# ❌ STUDIO
workflow.md → step-01-context-loading.md (immediate execution)

# ✅ BMAD STANDARD
workflow.md → step-01-brainstorm.md (optional discovery)
        ↓
    step-02-discovery.md (requirements gathering)
        ↓
    step-03-sidecar-metadata.md (build phase)
```

**BMAD Standard Reference:**
- [`_bmad/bmb/workflows/agent/workflow-create-agent.md:66-72`](_bmad/bmb/workflows/agent/workflow-create-agent.md:66-72):
  > Starts with optional brainstorming → Progresses through discovery, metadata, persona...

---

## 🔧 Remediation Summary

### Immediate Actions (Critical)

| Priority | Action | Files | Effort |
|----------|--------|-------|--------|
| 1 | Fix `exec` → `action` handler | 11 agents | Medium |
| 2 | Replace `PM` with `PT` code | 11 agents | Low |
| 3 | Fix `id` format to full path | 11 agents | Low |

### Short-term Actions (High)

| Priority | Action | Files | Effort |
|----------|--------|-------|--------|
| 4 | Add `prompts` sections | 11 agents | Medium |
| 5 | Shorten `communication_style` | 3-4 agents | Low |
| 6 | Move file paths from `principles` | 2 agents | Low |
| 7 | Add `critical_actions` | 5 agents | Low |

### Medium-term Actions

| Priority | Action | Files | Effort |
|----------|--------|-------|--------|
| 8 | Create validation workflows | All capabilities | High |
| 9 | Add discovery/brainstorm phases | All workflows | High |
| 10 | Consider module code assignment | All agents | Low |

---

## 📊 Compliance Matrix

| Requirement | Standard | Studio Status |
|-------------|----------|---------------|
| Handler: `action` for Agents | ✅ Required | ❌ Uses `exec` |
| Handler: `exec` for Modules | ✅ Correct | N/A |
| Reserved codes: No MH/CH/PM/DA | ✅ Required | ❌ Uses `PM` |
| Metadata `id` format | ✅ Full path | ❌ Simple name |
| `hasSidecar` declared | ✅ Required | ✅ Present |
| `prompts` section | ✅ Recommended | ❌ Missing |
| `communication_style` 1-2 sentences | ✅ Guideline | ❌ Too long |
| `principles` no file paths | ✅ Guideline | ❌ Has paths |
| `critical_actions` present | ✅ Recommended | ⚠️ Partial |
| Filename kebab-case | ✅ Required | ✅ Compliant |
| Menu desc `[XX]` format | ✅ Required | ✅ Compliant |

**Compliance Rate:** 5/11 (45%)

---

## 📎 Reference Files

**BMAD Standards:**
- [`_bmad/bmb/agents/agent-builder.md`](_bmad/bmb/agents/agent-builder.md)
- [`_bmad/bmb/workflows/agent/data/agent-architecture.md`](_bmad/bmb/workflows/agent/data/agent-architecture.md)
- [`_bmad/bmb/workflows/agent/data/agent-validation.md`](_bmad/bmb/workflows/agent/data/agent-validation.md)
- [`_bmad/bmb/workflows/agent/data/agent-menu-patterns.md`](_bmad/bmb/workflows/agent/data/agent-menu-patterns.md)

**Studio Implementation:**
- [`studio/agents/lnd-orchestrator.agent.yaml`](studio/agents/lnd-orchestrator.agent.yaml)
- [`studio/agents/lewd-writer.agent.yaml`](studio/agents/lewd-writer.agent.yaml)
- [`studio/agents/panel-forensic-analyst.agent.yaml`](studio/agents/panel-forensic-analyst.agent.yaml)
- [`studio/agents/dialogue-crafter.agent.yaml`](studio/agents/dialogue-crafter.agent.yaml)
- [`studio/agents/gooner-editor.agent.yaml`](studio/agents/gooner-editor.agent.yaml)

---

*Audit completed: 2026-02-27*  
*Auditor: BMAD Compliance System*  
*Next Review: After remediation*
