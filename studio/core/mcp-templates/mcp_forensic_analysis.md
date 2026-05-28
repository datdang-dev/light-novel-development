# MCP Forensic Analysis Template

## Purpose
Execute forensic analysis via MCP tools instead of legacy delegation.

## Instructions
1. Use the `forensic_analysis` MCP tool from the `toriigate` server
2. Pass required parameters: image_path, manga_name, page_number, user_context
3. Save output to `_lnd-output/{basename}/forensic.json`
4. The tool automatically loads prompts from `studio/prompts/forensic_analysis.txt`

## Workflow
- This replaces the legacy delegation to Kana (manga-adapter.agent.yaml)
- No intermediate files are written to disk in ONE_SHOT mode
- All processing happens within the MCP tool call context