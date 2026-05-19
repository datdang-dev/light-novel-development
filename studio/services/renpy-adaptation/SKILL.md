---
name: renpy-adaptation
description: Ren'Py game-to-prose adaptation pipeline — extracts semantic models from
  Ren'Py scripts via AST mining and delegates to the standard prose generation flow.
injection:
  always:
  - '{{project_root}}/studio/knowledge/packs/narrative_style_pack.md'
  triggers:
  - scene_tag: explicit|r18|sexual
    loads:
    - '{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md'
    - '{{project_root}}/studio/knowledge/packs/fetish_guidance_pack.md'
  - scene_tag: dialogue-heavy|visual-novel
    loads:
    - '{{project_root}}/studio/knowledge/packs/japanese_reader_psychology.md'
dependencies:
  knowledge:
  - path: '{{project_root}}/studio/knowledge/packs/narrative_style_pack.md'
  - path: '{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md'
  modules: []
---


# Ren'Py Playthrough Novelization Pipeline

## Overview

The Ren'Py Playthrough Novelization pipeline enables the **autonomous conversion of visual novel game scripts into high-fidelity, interactive R18 Light Novels**. Operated by the **Ren'Py Adapter** agent, it parses `.rpy` scripts, flattens branching dialogue trees based on a *Playthrough Choice Matrix*, maps multi-modal cues (sprites, backgrounds, sound effects) into stage directions, and compiles Suki's (`lewd-writer`) sensory-dense R18 Vietnamese prose with embedded game image illustrations.

This pipeline redefines game adaptation — transforming raw, complex game code into a beautiful, linear, or multi-route story book.

## On Activation

1. Load target Ren'Py script file(s) (`.rpy`)
2. Load or define the **Playthrough Choice Matrix** (e.g. `choices = {"day26_asuka": "slut"}`) to resolve narrative branching.
3. Verify extraction and index tools in the `tools/` directory.
4. Begin at `steps/step-01-ast-mining.md`

## Steps

| Step | File | Purpose |
| --- | --- | --- |
| 1 | `steps/step-01-ast-mining.md` | Parse `.rpy` files and discover characters, variables, and branches. |
| 2 | `steps/step-02-timeline-flattening.md` | Apply the Choice Matrix to resolve game flags and flatten the AST into a linear chronological script. |
| 3 | `steps/step-03-visual-audio-merging.md` | Map `scene`, `show`, `play music`, and transitions (e.g., `vpunch`) into multi-modal stage directions and visual anchors. |
| 4 | `steps/step-04-prose-drafting.md` | Suki (`lewd-writer`) rewrites the structured script into sensory-dense Vietnamese R18 prose, embedding images. |
| 5 | `steps/step-05-book-compilation.md` | Aggregate chapters and compile a self-contained, glassmorphic HTML/JS Web Book SPA. |

## Tools

| Path | Purpose |
| --- | --- |
| `tools/extract_renpy_ast.py` | Parses `.rpy` files into a structured AST JSON. |
| `tools/analyze_semantics.py` | Resolves positions, zooms, and environmental cues from the AST. |
| `tools/index_assets.py` | Indexes physical `.jpg`, `.png`, and `.webm` assets to link into the novel. |

## Dependencies

- **Agent**: Ren'Py Adapter (`renpy-adapter.agent.yaml`)
- **Output**: Beautiful, self-contained interactive Markdown/HTML Web Book chapters.
- **Downstream**: Suki (`lewd-writer`) → QA Audit (`riko`) → Web Book SPA Compiler.
