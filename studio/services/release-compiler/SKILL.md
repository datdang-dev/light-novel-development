---
name: release-compiler
description: "Release packaging service — transforms compiled output into delivery packages including manifests, web chat kits, and distribution archives."
dependencies:
  knowledge: []
  modules: []
---

# Release Compiler Service

## Overview

The Release Compiler transforms LND Studio output into **structured delivery packages** tailored for distinct reader experiences. Operated by the **Publisher** agent (Release Compiler), it generates manifests, web chat kits (for Grok/ChatGPT integration), and archive packages.

Three output formats: Base Reading (clean prose), Modded Reading (with annotations), and interactive AI Web Chat (SillyTavern-compatible cards + lorebooks).

## On Activation

1. Verify compiled chapter output exists
2. Load character profiles for web chat kit generation
3. Begin at `steps/step-01-manifest.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-manifest.md` | Generate release manifest with metadata |
| 2 | `steps/step-02-web-chat-kit.md` | Build web chat integration kit |
| 3 | `steps/step-03-package.md` | Package and archive deliverables |

## Dependencies

- **Agent**: Publisher (`CC` — `release-compiler.agent.yaml`)
- **Input**: Compiled chapters (from Chapter Composer)
- **Modules**: `sillytavern-export`
- **Upstream**: Chapter Composer

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Compile release** | `/release-compiler` | Load `steps/step-01-manifest.md` |
| **Web chat kit only** | Specify chat-kit mode | Skip to step 2 |
