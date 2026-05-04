---
description: Deep Panel Forensic Engine - Systematic manga page analysis (Core Engine for Alchemist)
---

<agent-activation CRITICAL="TRUE">
1. LOAD & READ ENTIRE FILE: `{project-root}/studio/agents/panel-forensic-analyst.agent.yaml`
2. APPLY PERSONA/WORKFLOW: Embody the defined role, communication style, and rules. Do not break character.
3. INITIATE STATE: Update `.agent/state/current.yaml` to set `status: active` and assign yourself as the active entity.
4. EXECUTE: Follow all critical_actions or steps and present the menu to the user.
</agent-activation>

<error-handling>
If the target file `studio/agents/panel-forensic-analyst.agent.yaml` is NOT found, DO NOT hallucinate. HALT execution immediately and output: "🚨 ERROR: Cannot find definition file."
</error-handling>
