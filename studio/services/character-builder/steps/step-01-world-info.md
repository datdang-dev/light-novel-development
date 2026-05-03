# Step 01: Extract Lore & Construct World Info

**Goal:** Provide the necessary foundational lore contextualizing the characters. Web Chat AIs need explicitly stated world systems to avoid hallucinations.

## Instructions

1. **Analyze Corpus:** Review the provided story context, character bibles, or raw prose text.
2. **Identify World Systems:** Extract overarching organizations, magical/biological systems, power dynamics, or specific locations (E.g., "Libido-X", "SEED Organization", "Hypnosis Apps").
3. **Format World Info:** Synthesize this information into a compact file named `world_info_[system].md` formatted for easy ingestion by AI.

### Mandatory Template

```markdown
# [World Name / System Name]

## Core Concept
[2-3 sentences defining what this is]

## Rules & Mechanics
- [Rule 1]
- [Rule 2]

## Societal / Character Impact
[How does this affect the specific characters in the story?]
```

## Completion

Once the file is generated and saved cleanly to `_lnd-output/_roleplay/[project_name]/`, proceed to `./step-02-character-profile.md`.
