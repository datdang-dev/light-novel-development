# MCP Erotic Caption Pipeline Template

## Purpose
Execute the full erotic caption pipeline via MCP tools instead of legacy delegation.

## Instructions
1. Use the `run_ec_pipeline` MCP tool from the `toriigate` server
2. Pass required parameters: image_path, manga_name, page_number, mood_seed, user_context
3. The tool automatically loads all required prompts:
   - `studio/prompts/forensic_analysis.txt` for Kana
   - `studio/prompts/scene_prelude.txt` for Luna
   - `studio/prompts/erotic_caption.txt` for Suki
4. Saves output to `_lnd-output/{basename}/`:
   - `forensic.json` (Kana's visual forensic analysis)
   - `prelude.json` (Luna's narrative scenario blueprint)
   - `caption.json` (Suki's erotic Vietnamese caption)

## Workflow
- This replaces the legacy delegation sequence: Kana -> Luna -> Suki -> Riko
- Executes in ONE_SHOT mode for VRAM efficiency on 6GB GPUs
- All processing happens within isolated MCP tool calls
- Output files conform to their respective schemas