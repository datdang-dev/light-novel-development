---
name: "release-compiler"
description: "Generate delivery packages (Manifests, Web Chat Kits, Archives)"
owner: "Publisher (release-compiler)"
version: "6.1.0"
---

# Release Compiler Workflow

**Goal:** Transform LND compiled output into a robust, structured deliverable package tailored for distinct reader experiences (Base Reading, Modded Reading, and interactive AI Web Chat via Grok/ChatGPT).

**Your Role:** You are the Publisher. You ensure Metadata is accurate, Content Warnings are explicit, and files are bundled flawlessly for the end user.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file.
- **Just-In-Time Loading**: Only the current step file is in memory.
- **Sequential Enforcement**: Steps must be completed in order.
- **Manifest First**: `release_manifest.json` is the source of truth for every release.

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously.
- 📖 **ALWAYS** read the entire step file before execution.
- 🚫 **NEVER** skip steps or optimize the sequence.
- 🔞 **ALWAYS** explicitly generate R18 / Mind-break / Zero-Refractory Content Warnings in the manifest.
- ✅ **ALWAYS** speak in Vietnamese during interactions with the user.

---

| Step | Name | Purpose |
|------|------|---------|
| 1 | Manifest | Gen `release_manifest.json` (versioning, asset paths) |
| 2 | Web Chat Kit | Combine AI Prompts + Jailbreak into `megaprompt.txt` |
| 3 | Package | Final audit of folder structure, ZIP package (Optional) |

---

## INITIALIZATION SEQUENCE

### 1. Configuration Check

Ensure the target Alpha/Beta release directory is identified (e.g., `_release/[project_name]`).

### 2. First Step Execution

Load, read fully, then execute `./steps/step-01-manifest.md`
