---
name: volume-context-extractor
description: Extracts volume-level narrative context from manga, preferring manga-ocr MCP and falling back to Vision.
---
# Volume Context Extractor 

This skill is responsible for scanning an entire volume of manga or a batch of images to extract the general narrative context, character appearances, and timeline. 
It operates under the philosophy that "Blind" AI is "Hallucinating" AI, thus establishing a global baseline of truth before atomic panel processing begins.

## 1. Input Validation
Identify the target volume directory (e.g., `sources/mangas/{Title}/Volume_{N}`). 
Ensure the directory exists and contains images.
Look at the `pipeline-context.md` if the target is defined there globally.

## 2. OCR Strategy (Try MCP First)
Your first priority is to use formal OCR. To determine if MCP OCR is viable:
1. Select 1-2 random pages (e.g., page 003 or 004) from the target volume.
2. Use the `mcp_manga-ocr_ocr_full_page` tool to extract text. (Manga-OCR is highly tuned for Japanese).
3. Evaluate the output:
   - IF the output is coherent Japanese text: The strategy is **MCP_BATCH**.
   - IF the output is gibberish, hallucinated, missing much text, or incorrectly parsed (e.g. Traditional Chinese vertical text which the MCP tool fails on): The strategy is **VISION_FALLBACK**.

## 3. Execution Based on Strategy

### Strategy A: MCP_BATCH (For Japanese / Supported Languages)
1. Iterate through all image pages.
2. For each page, call `mcp_manga-ocr_ocr_full_page` to get the text.
3. Save the raw stitched text to a temporary scratchpad.
4. Run a synthesis step to generate a structured timeline mapping character dialogues, actions, and key plot points into `{project-root}/studio/output/volume_context.md`.

### Strategy B: VISION_FALLBACK (For CJK Complex Layouts like Chinese)
1. Since standard OCR failed, you must use your native Vision-Language capabilities.
2. Iterate through the pages using the `view_file` tool to visually read the text directly from the images. 
3. You may process them sequentially or in batches (e.g. read 5 pages, synthesize, repeat).
4. Extract the speech bubbles, character interactions, and setting details.
5. Synthesize your observations directly into `{project-root}/studio/output/volume_context.md`.

## 4. Final Output Construction
The final artifact MUST be saved to `{project-root}/studio/output/volume_context.md` containing:
- **Global Synopsis**: The overall plot spanning the pages.
- **Character Registry**: Who appears, their visual traits, and their psychological intent.
- **Narrative Timeline (Acts)**: Sequential breakdown of events to serve as the context anchor for atomic panel extraction.
- **Extraction Diagnostic**: A brief note on whether MCP or Vision strategy was used and the confidence level.

## 5. Handoff
Notify the user once `volume_context.md` has been generated and ask if they would like to proceed with atomic `panel-forensic` scans using Kana.
