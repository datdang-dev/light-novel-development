---
name: step-06b-r18-audit
description: "R18 scene completeness audit — ensure no erotic scene is missed in novel adaptation"
---

# Step 6b: R18 Scene Completeness Audit

## Purpose

Cross-reference the R18 Scene Catalog (from quest flow extraction) with the novel timeline to ensure **every erotic scene in the game** is accounted for in the novel adaptation.

## 🔄 [Self-Executed by Director K]

## Prerequisites

- `quest_flow_report.md` generated (Step 6)
- `timeline.md` drafted (Step 6)

## Actions

### 6b.1 Build R18 Scene Checklist

From `quest_flow_report.md` → R18 Scene Catalog section:

1. Extract all unique CG names
2. Group by location and event
3. Classify each scene:
   - **Type**: oral, vaginal, anal, group, masturbation, voyeur, other
   - **Characters**: who participates
   - **Context**: main quest, side quest, or free-roam

### 6b.2 Cross-Reference with Timeline

For each R18 scene in the catalog:

| Status | Meaning |
|--------|---------|
| ✅ Mapped | Scene assigned to a specific chapter |
| ⏳ Planned | Scene identified but not yet written |
| ❌ Missing | Scene not in timeline — needs chapter assignment |
| ⬜ Skipped | Intentionally excluded (with reason) |

### 6b.3 Gap Analysis

Identify scenes marked ❌ Missing:

1. Determine which timeline window they belong to
2. Check if they require specific quest conditions
3. Propose chapter placement
4. Flag any scenes that may need new chapters

### 6b.4 Generate Audit Report

Create `r18_audit.md` with:

```markdown
# R18 Scene Audit — {game_name} / {heroine_name}

## Coverage Summary
- Total R18 CGs in game: X
- Mapped to chapters: Y
- Planned: Z
- Missing: W

## Scene Checklist
| # | CG Reference | Location | Characters | Type | Chapter | Status |
|---|-------------|----------|------------|------|---------|--------|
```

## Outputs

- `_lnd-output/_rpg/{game_name}/novels/{heroine_name}/r18_audit.md`

## Progression

- ✅ All scenes mapped or acknowledged → Load `./steps/step-07-prose-generation.md`
- ❌ Missing scenes found → Update timeline, then re-audit
