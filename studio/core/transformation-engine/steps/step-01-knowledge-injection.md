---
name: 'step-01-knowledge-injection'
description: 'Phase 1: Knowledge Injection'
---

# Step 1: JIT Knowledge Injection

## STEP GOAL

Execute the `knowledge_injector.py` script to generate a contextual payload based on the `content_tags` found in the `forensic-state.json`.

## EXECUTION RULES

You MUST run the script from the terminal to generate `knowledge_payload.md` in the current working directory or the specific chapter output directory.

```bash
python3 {project-root}/studio/core/transformation-engine/knowledge_injector.py {forensic_state_path} {payload_output_path} {project-root}/studio/knowledge/
```

Once `knowledge_payload.md` is generated, update the virtual workflow state and proceed to Prose Generation with Suki.
