---
name: 'step-06-polish-review'
description: 'Final refinement and voice check'

thisStepFile: './step-06-polish-review.md'
dialogueOutput: '{output_folder}/_dialogue/{scene_id}_dialogue.md'
---

# Step 6: Polish & Review

## STEP GOAL:

Final review, refinement, and output of dialogue package.

## MANDATORY SEQUENCE

### 1. Voice Consistency Check

For each character, verify:
- [ ] All lines sound like them
- [ ] Speech quirks present
- [ ] Crude level appropriate
- [ ] R18 voice matches profile

### 2. Escalation Flow Check

- [ ] Intensity builds properly
- [ ] No jarring drops
- [ ] Climax is peak
- [ ] Aftermath is coherent

### 3. SFX Balance Check

- [ ] Not overused
- [ ] Appropriate types
- [ ] Well placed
- [ ] Romanized correctly

### 4. Final Polish

Make refinements:
- Vary sentence starters
- Ensure dialogue isn't repetitive
- Check pacing

### 5. Generate Output

Write to `{dialogueOutput}`:

```markdown
---
scene_id: "{id}"
characters: [{list}]
beats: {count}
generated: "{timestamp}"
---

# Dialogue Package: {scene_id}

## Voice Reference
{char}: {brief voice notes}

## Dialogue by Beat

### Beat 1: {name}
{dialogue with SFX}

### Beat 2: {name}
...
```

### 6. Workflow Completion

```
"✅ DIALOGUE PACKAGE COMPLETE!

**Output:** {dialogueOutput}

**Summary:**
- Characters: {list}
- Lines: {count}
- SFX instances: {count}

**Ready for:** prose-adapter integration

**WORKFLOW COMPLETE**"
```

---

## WORKFLOW END

Dialogue package ready for prose integration.
