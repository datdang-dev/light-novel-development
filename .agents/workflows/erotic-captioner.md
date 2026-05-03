---
description: Erotic Image Captioner — Generate R18 erotic captions from manga/hentai images (Kana → Suki Caption Mode)
---
// turbo-all

# Erotic Image Captioner Pipeline

## Usage
```
EC <image_path>
```
or
```
EC <image_path_1> <image_path_2> ...
```
or 
```
erotic caption: <image_path> [user_context]
```

## Steps

1. Activate `@lnd-orchestrator` (Director K)
   *(Note: Target agent definition is handled directly by `studio/agents/lnd-orchestrator.agent.yaml`)*
2. Director K loads `studio/services/erotic-image-captioner/SKILL.md`
3. **Step 1 — Init:** Validate image, create output dir `_lnd-output/_captions/{basename}/`. Load `user_context` if provided in the prompt.
4. **Step 2 — Forensic (Kana):** Run `studio/core/panel-forensic/SKILL.md` on the image
   - *Error Handling:* If Kana fails to extract core details, prompt Kana to re-analyze or ask user for confirmation.
5. **Step 3 — Caption (Suki):** Run `studio/core/erotic-caption-writer/SKILL.md` using forensic data + `user_context`
   - *Quality Gate:* Suki must self-correct if the output violates `caption-rules.md`.
6. Output saved to `_lnd-output/_captions/{basename}/caption.md`
7. If multiple images are provided, loop Steps 1-6 for each image.
