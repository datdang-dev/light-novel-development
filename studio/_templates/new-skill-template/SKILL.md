---
name: new-skill-name
description: "Brief one-line description of what this skill does."
---

# Skill Display Name

## Overview

Describe what this skill does, who uses it, and what it produces. Keep to 1-2 paragraphs.

## On Activation

1. Load required context or configuration
2. Verify dependencies exist
3. Route to appropriate sub-file or capability

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-initialize.md` | First step description |

## Dependencies

- **Agent**: Agent Name (`CODE` — `agent-file.yaml`)
- **Schemas**: List relevant schemas
- **Modules**: List dependent modules
- **Upstream**: What feeds into this skill
- **Downstream**: What consumes this skill's output

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Primary action** | `/command` | Load first step |
| **Alternative** | Description | Route |
