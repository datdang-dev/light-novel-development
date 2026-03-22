---
name: "character-builder"
description: "Capability: Build High-Fidelity Character Profiles & Bios (V6.1)"
owner: "Aria (character-architect)"
version: "6.1.0"
---

# Character Builder Workflow (V6.1)

**Goal:** Create high-fidelity psychological character profiles and foundational World Lore contexts. These files will be ingested by the Release Manager [RC] later to build Web Chat Kits.

**Architecture:**

- **Step 1:** World Lore & Systems (Aria) - `step-01-world-info.md`
- **Step 2:** Profile Synthesis (Aria) - `step-02-character-profile.md`

IT IS CRITICAL THAT YOU LOAD FULLY EACH STEP WHEN DELEGATED AND DO NOT SKIP.

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load config from `{project-root}/studio/config/config.yaml`.

### 2. First Step Execution

If the user triggered `[CC] Run Full Context Workflow`, load and fully read `./steps/step-01-world-info.md`.
