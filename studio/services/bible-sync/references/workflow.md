# Bible Sync Workflow

## Overview

Bible Sync ensures character profiles are updated after each pipeline step, maintaining continuity across scenes and chapters.

## Operations

### LOAD (Before Prose)
1. Read `_lnd-output/_bible/{project}/active_character_context.md`
2. Extract current character states
3. Provide as context to prose generation

### SAVE (After Audit PASS)
1. Extract character state changes from approved prose
2. Update `active_character_context.md`
3. Update individual `char_desc_{name}.md` files if appearance changed

## Trigger
- Invoked by Orchestrator between forensic analysis and prose generation (LOAD)
- Invoked by Orchestrator after audit PASS (SAVE)
