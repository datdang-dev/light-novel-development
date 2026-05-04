# WHY

The core promise of the LND Studio framework is that once a workflow (e.g., the forensic → prose → audit pipeline) is **activated**, every subsequent turn—whether processing a new image, continuing a roleplay session, or running a quality audit—will execute **exactly the same logic** that was loaded at activation time.  

In practice, there is **no reliable mechanism** to guarantee that the AI agent has actually loaded the intended version of the workflow, nor any automatic detection when the loaded version becomes stale or diverges from the source files on disk. This uncertainty constitutes a **technical debt** that erodes trust, introduces silent correctness bugs, and forces users to constantly re‑verify state manually.

---

## Problem Statement

When a user issues a command such as:

```
/panel-forensic   # or "test Kana"
write prose       # or "draft prose"
audit             # or "run audit"
```

the expected behavior is:

1. The relevant agent (Kana, Suki, Riko, …) reads its defining YAML/SKILL files **exactly as they exist on disk at that moment**.
2. All downstream agents (e.g., Suki consuming Kana’s forensic output) see a **consistent, version‑locked context**.
3. If the source files are edited between turns, the next activation should **pick up the changes** (or at least signal that a reload is required).

Currently, none of these guarantees hold:

- **No version stamp** is attached to the loaded skills/YAML.
- **No checksum or timestamp comparison** is performed before execution.
- **No explicit reload trigger** exists; the agent relies on the context window retaining the previously loaded content, which may be stale, incomplete, or corrupted.
- **No automated smoke‑test** validates that the loaded logic produces the expected output (e.g., that Kana’s V_affordance vector fires on a known test image).
- **No persistent state** records which version of the framework was last successfully used, making cross‑session consistency impossible to verify without manual inspection.

As a result, users must **manually verify** each turn (e.g., by re‑reading files, checking outputs, or re‑issuing activation commands) to feel confident that the workflow is behaving as intended.

---

## Symptoms

| Symptom | Observable Effect |
|---------|-------------------|
| **Silent drift** | After editing `studio/agents/manga-adapter.agent.yaml` to tighten V_affordance checks, subsequent Kana runs still produce the old "gun" label because the agent is still using the cached version from context. |
| **Inconsistent outputs** | Two consecutive runs on the same image yield different forensic reports (e.g., one includes "Onahole Gun", the next reverts to "Gun") without any user‑visible trigger. |
| **Forgotten configuration** | Changing `user_name` or `communication_language` in `config.yaml` does not take effect until the agent is explicitly reloaded via `skill_view` or a new session. |
| **Verification overhead** | Users must prepend every request with a manual “load and check” step (e.g., `skill_view("lnd-dev-studio")` + `read_file` of critical files) to feel safe. |
| **Cross‑session amnesia** | After closing and reopening the chat, the agent has no record of which workflow version was last used, forcing a full re‑onboarding. |
| **Error masking** | If a YAML file becomes malformed (e.g., missing `---`), the agent may silently fall back to a previously cached good version, hiding the corruption until much later. |

---

## Root Causes

| Cause | Explanation |
|-------|-------------|
| **Stateless turn‑based execution** | Hermes agents are designed to be stateless per turn; they rely on the context window to carry over loaded skills. No built‑in persistence layer exists for framework metadata. |
| **Immutable context window** | Once a skill/YAML is loaded into the context, subsequent tool calls do not automatically re‑read the file unless explicitly instructed (`skill_view`, `read_file`). |
| **Lack of versioning metadata** | Neither SKILL.md nor agent YAML files contain a version, checksum, or timestamp field that agents can introspect. |
| **No automatic reload policy** | The framework does not define a rule like “reload if file mtime > last_loaded_time”. |
| **Missing integration tests / smoke tests** | There is no canonical test image or script that validates the core behavior (e.g., V_affordance detection) after each load. |
| **Siloed verification** | Verification is left to the user; there is no centralized “framework health check” tool that can be called from a pre‑flight hook. |
| **Memory tool used for user preferences, not framework state** | The persistent `memory` store is currently used for user‑profile facts, not for recording which framework revision was loaded. |

---

## Impact

- **Correctness risk**: Silent propagation of outdated or incorrect logic leads to wrong forensic analysis, misguided prose, and failed audits—directly undermining the studio’s value proposition.
- **User friction**: Users spend cognitive load on verification instead of creative work, reducing throughput and increasing frustration.
- **Maintenance brittleness**: Refactoring or improving a skill becomes risky because there is no guarantee the change will be observed.
- **Scalability limitation**: As the number of agents and workflows grows, the manual verification burden grows linearly, making the framework unsuitable for automated or batch processing.
- **Trust erosion**: Repeatedly observing inconsistent outputs damages confidence in the system, prompting users to fall back to external tools or manual processes.

---

## Proposed Solutions (Defense in Depth)

### 1. Version & Checksum Metadata in Skill/YAML Files
Add a small, standardized frontmatter block (or YAML annotation) to every critical file:

```yaml
# Example for manga-adapter.agent.yaml
metadata:
  version: "2026-05-04-v1.3"
  checksum: "sha256:3a7f4e1b9c2d..."
  last_modified: "2026-05-04T14:30:00Z"
  source: "studio/agents/manga-adapter.agent.yaml"
```

- Agents, upon loading, compute the SHA‑256 of the file (or read the declared checksum) and compare it to a persisted record.
- Mismatch triggers an **auto‑reload** and logs a warning.

### 2. Persistent Framework State Ledger
Create a file `_pipeline/framework_state.yaml` (or use Hermes `memory` with a dedicated key) that records:

```yaml
loaded_at: "2026-05-04T15:00:00Z"
kana:
  version: "2026-05-04-v1.3"
  checksum: "sha256:..."
suki:
  version: "2026-05-04-v1.2"
  checksum: "sha256:..."
riko:
  version: "2026-05-04-v1.0"
  checksum: "sha256:..."
global:
  atmosphere_ledger_version: "2026-05-04-v1.0"
```

- Before each turn, the agent reads this ledger and validates that the on‑disk files match the recorded checksums.
- If any mismatch, the agent **reloads** the offending skill/YAML and updates the ledger.

### 3. Pre‑Flight Verification Hook (COT Scratchpad)
Extend the mandatory COT scratchpad (Module 1 of `roleplay-engine`) with a **Framework Verification** step:

```markdown
## 0. Framework Verification (MANDATORY mỗi turn)

- [ ] Confirm framework_state.yaml exists and is parseable.
- [ ] For each critical agent (Kana, Suki, Riko, Yua):
    - Verify that the agent’s YAML/SKILL file checksum matches the entry in framework_state.yaml.
    - If mismatch → auto‑reload via `skill_view` and update the ledger.
- [ ] Run a **smoke test** (e.g., process a 10 px test image with known V_affordance expectation) and assert the output contains the expected marker.
- [ ] If any check fails → halt and request user confirmation before proceeding.
```

This turns verification into an explicit, visible part of every turn’s reasoning trace.

### 4. Automated Smoke Test Script
Provide a lightweight script `scripts/smoke_test_framework.py` that:

1. Loads the current Kana YAML.
2. Runs a minimal vision inference on a bundled test image (e.g., a tiny PNG containing a transparent barrel with internal ribs).
3. Checks that the output contains the string `"Onahole Gun"` (or another version‑specific marker).
4. Returns exit code 0 on success, non‑zero on failure.

The script can be invoked from the COT verification step or from a CI‑like pre‑commit hook.

### 5. Explicit Reload Commands
Expose a simple, discoverable command for users and orchestrator agents:

```
/framework reload   # or "reload workflow"
```

Implementation: clears the relevant context, re‑loads all skills/YAML via `skill_view`, recomputes checksums, and writes a fresh `framework_state.yaml`.

### 6. CI/CD Gate for Skill Changes (Optional)
Even though the framework is prompt‑engineering focused, a lightweight CI step can be added to the repo:

- On any push to `studio/agents/` or `studio/skills/`, run the smoke test against a known image.
- Fail the CI if the test does not pass, preventing merges that break core behavior.

This turns the technical debt into a **detectable** issue early in the development lifecycle.

---

## Mitigation Strategies (Short‑Term, Zero‑Code)

While the above solutions require minor code/data changes, users can adopt these practices immediately to reduce risk:

1. **Always start a session with an explicit onboarding** (`/onboard` or `load context`) that calls `skill_view` on all critical skills and records the timestamps in a personal note.
2. **After editing any YAML/SKILL file, issue a `/framework reload`** before proceeding with further work.
3. **Maintain a personal checklist** in your notes:
   - [ ] Kana YAML version = X
   - [ ] SFX registry loaded
   - [ ] Atmosphere ledger version = Y
   - [ ] Smoke test passed
4. **Use the `memory` tool** to persist a hash of the last‑known‑good framework state:
   ```
   memory add user "framework_hash_$(date +%s): <sha256 of concat of all critical files>"
   ```
   Then compare on next session.
5. **Leverage the `session_search` tool** to recall the last successful run’s output and verify consistency manually.

---

## Open Questions & Trade‑offs

| Question | Considerations |
|----------|----------------|
| **Where to store the framework state ledger?** | Using a file (`_pipeline/framework_state.yaml`) makes it visible and version‑controllable but requires file‑system access. Using Hermes `memory` keeps it inside the agent’s session but is opaque and not directly inspectable. A hybrid approach (file for durability, memory for fast access) may be best. |
| **How granular should versioning be?** | Per‑file versioning gives the finest detection but increases metadata overhead. A single global framework version (incremented on any change) is simpler but may cause unnecessary reloads. |
| **Should the smoke test be mandatory?** | Making it mandatory guarantees correctness but adds latency (especially if vision model inference is slow). An opt‑in “strict mode” could be offered for users who need absolute certainty. |
| **How to handle partial failures?** | If only one agent’s file is out‑of‑date, should we reload the entire framework or just the offending piece? Reloading the whole framework is safer but may be wasteful. |
| **What about user‑provided custom overrides?** | Users may deliberately want to run with a patched version of a skill that is not yet committed. The verification system must allow an “override” flag that bypasses checksum checks for a specific file, with an explicit warning. |

---

## Conclusion

The inconsistency between **what the user believes is loaded** and **what the agent actually executes** is a classic technical debt that stems from the stateless, context‑window‑driven nature of the Hermes agent framework. By adding lightweight versioning, persistent state tracking, explicit verification steps, and an automated smoke test, we can transform this debt into a **managed, observable quality gate**—preserving the flexibility of prompt‑engineering while providing the reliability expected of a production‑grade workflow system.

Implementing the proposed layers will:

- Eliminate silent drift and ensure that every turn runs the exact logic the user intends.
- Reduce manual verification burden, freeing users to focus on creative work.
- Provide a clear, auditable trail of which framework version powered each run, enabling reproducibility and trust.
- Lay the groundwork for future automation (e.g., CI/CD pipelines, scheduled batch jobs) without requiring a wholesale redesign.

**Next step:** Draft the concrete file changes (add version frontmatter, create `framework_state.yaml` template, extend COT scratchpad, write smoke‑test script) and open a discussion with the team for review and implementation.
