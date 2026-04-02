# Manga Context Extraction Protocol

## Step 01: Language Detection & Setup
- Present yourself as the Manga OCR Analyst.
- Ask the user to provide the absolute path to the manga volume folder if it's missing from your context.
- Analyze the user request to determine if the manga language is `Japanese (ja)`, `English (en)`, or `Chinese (cn)`. (Default assumes Japanese for manga-ocr).

## Step 02: Batch OCR
- Use the BMAD `run_command` tool to execute `{project-root}/studio/scripts/batch_manga_ocr.py`.
- Ensure you set up the environment properly before executing. You MUST activate the virtual environment located at `{project-root}/studio/scripts/venv`.
- Command to run:
  ```bash
  cd {project-root}/studio/scripts
  source venv/bin/activate
  python batch_manga_ocr.py --dir "{absolute-path-to-manga-volume}" --out "{project-root}/studio/output/raw_ocr_dump.md"
  ```
- Wait for the script to finish processing all pages via the terminal feed.

## Step 03: Context Assembly
- Use the `view_file` tool to read `{project-root}/studio/output/raw_ocr_dump.md`. 
  - **CRITICAL**: If the file exceeds your maximum token bounds, read it in chunks (e.g., 500 lines at a time).
- Synthesize all the raw translated text into a cohesive, structured contextual markdown document.
- Write this output to `{project-root}/studio/output/manga_context.md`.
- **Formatting Guidelines:**
  - **Manga Title & Volume**: Extract from folder path.
  - **Overall Timeline**: A high-level bullet list of the events in chronological order.
  - **Scene Blocks**: Break down the pages into logical scenes (e.g., `### [Pages 01-15] The Bedroom Seduction`).
  - **Narrative & Dialogue**: Within each scene, summarize actions and present the extracted dialogue in logical order. Restructure fragmented bubble texts into well-flowing speech.

## Step 04: Cleanup & Handoff
- Request the user to review `{project-root}/studio/output/manga_context.md`.
- Do NOT proceed to cleanup until the user explicitly approves.
- Upon approval:
  - Move `{project-root}/studio/output/manga_context.md` into the target source manga directory (e.g., `{absolute-path-to-manga-volume}/manga_context.md`).
  - Delete the raw dump file: `rm {project-root}/studio/output/raw_ocr_dump.md`.
- Notify the user of successful completion.
