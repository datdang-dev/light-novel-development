---
name: manga-context-extractor
description: "Batch manga volume orchestrator — runs OCR across entire manga volume, parses translated output, and synthesizes into manga_context.md timeline files. Upstream to Kana's panel-forensic for atomic processing."
owner: "datdang"
version: "1.0.0"
tags: [manga, batch, ocr, context, pipeline]
validateWorkflow: "./references/workflow.md"
injection:
  always:
    - "{{project_root}}/studio/rules/canon-rules.md"
  triggers:
    - scene_tag: "manga|volume|batch|ocr"
      loads:
        - "{{project_root}}/studio/core/volume-context-extractor/SKILL.md"
dependencies:
  knowledge:
    - path: "{{project_root}}/studio/knowledge/packs/narrative_style_pack.md"
    - path: "{{project_root}}/studio/knowledge/glossaries/hentai_lexicon.md"
  modules: []
---

# Manga Context Extractor

## Overview
This skill orchestrates the batch OCR scanning of entire manga volumes, parsing the raw translated output, and synthesizing it into properly formatted `manga_context.md` files describing the timelines, sequences, and conversations.

## On Activation
1. Check that you have the path to the target manga volume inside `sources/mangas/...`. If the user did not provide it, ask the user before proceeding.
2. Read the workflow protocol at `{{project_root}}/studio/services/manga-context-extractor/references/workflow.md`.
3. Inform the user what volume you are working on, then proceed with the steps defined in the workflow.

## Steps
Review `workflow.md` for exact execution technicalities.
| Step | Action | Description |
|------|--------|-------------|
| 01 | Language Detect | Verify target folder structure |
| 02 | Batch OCR | Execute `batch_manga_ocr.py` to generate `raw_ocr_dump.md` |
| 03 | Context Assembly| Parse dump, group into scenes, output timeline |
| 04 | Cleanup & Handoff| Move context file to source folder, delete dump |

## Dependencies
- script: `{{project_root}}/studio/scripts/batch_manga_ocr.py`
- agent: `{{project_root}}/studio/agents/manga-context-extractor.agent.yaml`
