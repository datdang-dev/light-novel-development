---
name: release-compiler
description: Final delivery packaging — compiles QA-approved pages into chapter files
injection:
  always:
    - '{{project_root}}/studio/config/canon-rules.md'
    - '{{project_root}}/studio/boot/canon-preamble.md'
dependencies:
  knowledge: []
  modules: []
---

# Release Compiler

## Overview

The Release Compiler takes QA-approved prose pages and compiles them into final chapter-level deliverables. It is invoked by the Orchestrator after all pages in a chapter have passed Quality Audit.

## On Activation

1. Scan `{{run_dir}}/_prose/` for all audit-passed pages
2. Verify each page has a corresponding PASS audit report
3. Compile pages in order into a single chapter file
4. Apply final formatting (prose_structure rules)
5. Output to `_lnd-output/_novels/{project}/novel_chapter_{XX}.md`

## Steps

| Step | Purpose |
|------|---------|
| 1 | Gather all PASS-audited prose files for the chapter |
| 2 | Order by page number |
| 3 | Merge with section breaks |
| 4 | Apply final formatting & continuity check |
| 5 | Output to release directory |
