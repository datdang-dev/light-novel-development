---
name: manga-context-extractor
description: Batch process manga volumes through OCR and analyze the scenes and timeline
---

# Manga Context Extractor

## Overview
This skill orchestrates the batch OCR scanning of entire manga volumes, parsing the raw translated output, and synthesizing it into properly formatted `manga_context.md` files describing the timelines, sequences, and conversations.

## On Activation
1. Check that you have the path to the target manga volume inside `sources/mangas/...`. If the user did not provide it, ask the user before proceeding.
2. Read the workflow protocol at `{project-root}/studio/services/manga-context-extractor/references/workflow.md`.
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
- script: `{project-root}/studio/scripts/batch_manga_ocr.py`
- agent: `{project-root}/studio/agents/manga-context-extractor.agent.yaml`
