# LND Step Template

This template provides the standard structure for LND Studio workflow step files.

<!-- TEMPLATE START -->

---
name: 'step-[N]-[short-name]'
description: '[Brief description of what this step accomplishes]'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/[category]/[workflow-name]'
thisStepFile: './step-[N]-[short-name].md'
nextStepFile: './step-[N+1]-[next-short-name].md'  # Remove for final step
outputFile: '{output_folder}/[output-file-name].md'
---

# Step [N]: [Step Name]

## STEP GOAL:

[State the goal in context of the overall workflow goal. Be specific about what this step accomplishes.]

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input when required
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST speak in {communication_language} (Vietnamese)

### Role Reinforcement:

- ✅ You are a [specific role] collaborating with the user
- ✅ Maintain your agent persona throughout
- ✅ We engage in collaborative dialogue

### Step-Specific Rules:

- 🎯 Focus only on [this step's task]
- 🚫 FORBIDDEN to [what not to do]
- 💬 Approach: [how to handle this task]

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly.

### 1. [First Action Title]

[Specific instructions]

### 2. [Second Action Title]

[Specific instructions]

### N. Present MENU OPTIONS

Display: "**Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue"

#### Menu Handling Logic:

- IF A: Execute advanced elicitation
- IF P: Execute party mode workflow
- IF C: Save content, update frontmatter, then load {nextStepFile}
- IF other: Help user respond, redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

---

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [completion requirements met] will you load and execute `{nextStepFile}`.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- [Success criteria 1]
- [Success criteria 2]
- Content properly saved
- Menu presented and user input handled

### ❌ SYSTEM FAILURE:

- [Failure mode 1]
- [Failure mode 2]
- Proceeding without user input
- Not updating frontmatter

**Master Rule:** Follow exact instructions. No skipping or optimizing.

<!-- TEMPLATE END -->
