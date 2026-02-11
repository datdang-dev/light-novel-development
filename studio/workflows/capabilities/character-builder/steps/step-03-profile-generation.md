# Step 3: Profile Generation (System Prompt)

**Goal:** Convert the analysis into a "System Prompt" compatible artifact for the LND Orchestrator.

## Input Required

- **`analysis_{character_tag}.md`**: The detailed analysis from Step 2.

## Process

1. **Synthesize:** condense the analysis into the standard `studio/profiles/` format.
2. **Format:** Use the standard Frontmatter + Markdown structure.

## Output Template

File: `studio/profiles/{name}_profile.md`

```markdown
---
name: "{Name}"
tags: [tsundere, petite, rich_girl]
voice_model: "v2_high_haughty"
---

# {NAME} - Character Profile

## 🧠 Core Psychology
[Summary of drivers and insecurities]

## 🗣️ Voice & Dialogue Style
- **Tone:** [Adjectives]
- **Key Rules:**
    1. [Rule 1 from Step 2]
    2. [Rule 2 from Step 2]

## 💥 Triggers & Kinks
- **[Kink]:** [Description]

## 📝 Example Dialogue (Few-Shot)
**Context:** [Situation]
**{Name}:** "[Representative Quote]"

**Context:** [Situation]
**{Name}:** "[Representative Quote]"
```

## Integration

Once created, this file can be loaded by the Orchestrator for any scene involving this character using:
`view_file studio/profiles/{name}_profile.md`
