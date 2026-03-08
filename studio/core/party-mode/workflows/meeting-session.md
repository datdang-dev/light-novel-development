    ---

name: "meeting-session"
description: "Workflow for collaborative multi-agent studio meetings"
owner: "Antigravity (meeting-chair)"
version: "1.0.0"
---

# 🥂 LND Studio Meeting Session

**Goal:** Facilitate structured, collaborative discussions between multiple specialized agents (Party Mode) to solve complex architectural or creative problems.

## Phase 1: Preparation

1. **Define Agenda:** The Chair (Antigravity) identifies the core topic and goals of the meeting.
2. **Invite Participants:** List the specialized agents required for the discussion (e.g., Ren for technical, Kana for forensic, Suki for creative).
3. **Context Loading:** Read the relevant project files or history to establish the baseline for all participants.

## Phase 2: Discussion

1. **Opening Statement:** The Chair presents the problem/opportunity.
2. **Agent Round-Table:**
    - Each invited agent provides a perspective based on their `persona` and `rules`.
    - Participants should build on each other's ideas rather than just auditing (unless explicitly requested).
3. **Synthesis & Debate:** The Chair identifies conflict points or synergies and facilitates focused discussion.

## Phase 3: Conclusion

1. **Action Items:** Summarize the decisions made and assign tasks to specific agents.
2. **Meeting Minutes:** Save a log of the discussion in `{project-root}/studio/core/party-mode/logs/{date}_{topic}.md`.
3. **Drafting (Optional):** If the meeting results in a new workflow or code change, initiate the implementation phase.

---
**CRITICAL:** The Chair MUST maintain the specialized voice of each guest agent. Do NOT flatten different personas into a single generic tone. Invoke Cursor CLI (`agent`) if a formal, unbiased audit is required during the meeting.
