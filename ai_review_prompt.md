# Prompt Review Framework LND Studio

You can copy the entire content below and send it to an AI (along with the source code or important files of the project) to ask for a review:

---

**[COPY FROM HERE]**

You are a Senior System Architect and AI Prompt Engineer specializing in Agentic Frameworks (especially in the Multi-Agent Orchestration model).

I am building a framework called "LND Studio" based on the BMAD standard. This framework is used to automate a workflow (e.g., converting manga into a light novel) through a Pipeline featuring an Orchestrator (Director K) and various Specialist Agents handling each phase (Forensics, Writer, QA Editor, etc.). The Agents are defined using YAML files (`.agent.yaml`) and communicate via JSON state files.

Please analyze this entire repository and evaluate the system based on the following 3 pillars:

### 1. Architecture (System Architecture)

*Goal: Evaluate extensibility, complexity, and maintainability.*

- **Extensibility:** Is it easy to add a new Agent or a new Pipeline step to the current system? Are the couplings between the Orchestrator and the Agents "hardcoded" or flexible?
- **Maintainability:** Is the state management via file I/O (Context saved on disk) well-decoupled? Are there any bottlenecks regarding data flow or directory structures?
- **Cognitive Load for AI:** Does this architecture create context bloat for the AI Model when reading configuration files and running workflows? Is the system's method of loading Context (e.g., via `pipeline-context.md`) optimal for the LLM's context window?

### 2. Implementation (Prompting Techniques & Execution)

*Goal: Evaluate the quality of prompts and constraint mechanisms.*

- **Prompt Engineering:** Please evaluate my use of Persona framing, Role-playing, and Constraint Injection in the `.agent.yaml` files. Are they robust enough for the AI to follow reliably?
- **Wording & Context:** Is the wording used in the Rules and Critical Actions at risk of being misleading or creating loopholes for the LLM to "bypass rules" or experience hallucinations?
- **Fallback & Audit Mechanism (Error-Contract):** Is the QA cycle (e.g., Agent Audit failing an output and demanding a rewrite) meticulously designed via the prompts with a high degree of determinism?

### 3. Recommendations & Other Insights

*Goal: Provide breakthrough perspectives.*

- Point out any "Blind spots" in the current design that I haven't recognized.
- Suggest new Design Patterns in Agentic AI (such as Reflexion, ReAct, Plan-and-Solve) that could be applied to LND Studio to enhance automation quality.
- If you have any clean quick wins that can create a significant impact, please list them.

Please return a structured evaluation report using Markdown, focusing on technical aspects and providing specific examples from the source code where applicable.

---
**[END COPY]**
