---
description: "Step 01b: Generate Context Hypothesis (POC)"
---

# Generative Context Hypothesis (POC)

**Goal:** Analyze the previous page's state and the Bible to predict what *should* be on the current page. This hypothesis eliminates hallucination by telling the Forensic engine what to verify.

## 1. Trigger POC Generator

```bash
# Execute the POC Generator Script (or LLM Prompt)
# Input: State JSON, Bible JSON
# Output: {output_folder}/{chapter}/{page}/poc.md
python3 {project-root}/studio/services/gooner-alchemist/tools/generate_poc.py \
  --state "{output_folder}/_pipeline/{project}/state.yaml" \
  --bible "{project-root}/studio/database/bible.json" \
  --page "{current_page}"
```

## 2. Verify Output

Check that `poc.md` exists. It should contain:

- **Scene Context:** Where are we?
- **Character Expectations:** Who is here? What are they wearing?
- **Action Hypothesis:** What likely happens next based on previous flow?

## 3. Human Review (Optional)

Display the POC to the user for quick verification.
"Hypothesis: Asuka is angry. Correct? [Y/N]"

## 4. Proceed

Move to **Step 02: Forensic Analysis** with the `{poc_path}` argument.
