---
name: step-03-summarize
description: Compile Discussion Summary
---

# Step 3: Conclusion & Action Items 📝

## STEP GOAL

Compile discussion outcomes into an actionable summary.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Synthesize Results

Review the discussion log from Step 2.
Identify:

- **Key Decisions:** (Agreed upon direction)
- **Open Questions:** (Needs more research)
- **Action Items:** (Tasks assigned to specific workflows)

### 2. Generate Artifact

Create a new file: `{project-root}/studio/novels/_discussions/party_summary_{topic_slug}.md`

**Content:**

```markdown
# Party Mode Summary: {topic}
**Date:** {today_date}
**Participants:** {config.agents}

## 1. Executive Summary
{brief_overview}

## 2. Key Insights
- **Character (Aria):** {insight}
- **Prose (Suki):** {insight}
- **Dialogue (Miki):** {insight}
- **Other:** {insight}

## 3. Action Items
- [ ] {Task 1}
- [ ] {Task 2}
```

### 3. Present MENU OPTIONS

```
"✅ Summary Generated: file://{summary_path}

**Decisions:** {count}
**Action Items:** {action_item_count}

**Chọn:** [E] Exit Party Mode"
```

#### Menu Handling Logic

- IF [E]:
  - Notify User: "🎉 Discussion Concluded."
  - BREAK CHARACTER (Return to Default Handler).
