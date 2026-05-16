
## hermes [dev-architect] Architecture Review

[Error] Upstream account hit a rate limit and returned empty output.

## claude [dev-implementer] Code Review

# Review: `.agents/skills/axel-cowork/SKILL.md`

---

## Test Strategy & Coverage

**[MINOR]** No test strategy is documented. For a skill that orchestrates multi-agent sessions, consider:
- **Unit tests**: Argument parsing logic (e.g., `--agents` parsing, default fallback).
- **Integration tests**: End-to-end run with mock agents (verify `context.md` creation, agent invocation order).
- **Edge cases**: Missing `--task`, invalid `--mode`, malformed `--agents` string, empty `--prompt`.
- **Negative cases**: Non-existent agent ID, permission errors on `_out/`, concurrent task ID collision.

**Coverage criteria**: If this skill has a `run.sh` script, test coverage should include:
- All argument parsing branches.
- Agent registry lookup (valid/invalid IDs).
- File I/O (context.md creation, append logic).
- Error handling (missing dependencies, agent CLI failures).

**ASPICE alignment**: For SWE.4 (Software Unit Verification), unit tests should exist for the argument parser and agent dispatcher. For SWE.5 (Software Integration Test), integration tests should verify the full pipeline (task creation → agent invocation → result storage).

---

## Implementation Verification

**[CRITICAL]** **Missing error handling documentation**: The SKILL.md does not describe what happens if:
- An agent CLI fails (e.g., Hermes returns non-zero exit code).
- The `_out/agent-sessions/<task-id>/` directory cannot be created (permission error).
- The `--agents` string is malformed (e.g., `hermes:` with no role, or `unknown-agent:role`).

**Test that would catch this**: Integration test that:
1. Invokes `run.sh` with an invalid agent ID (e.g., `--agents "nonexistent:role"`).
2. Asserts the script exits with a non-zero code and prints a clear error message.
3. Verifies no partial state is left in `_out/`.

**[MAJOR]** **Concurrency risk**: If two users run the same `--task <id>` simultaneously, they will write to the same `context.md` file. This could cause:
- Interleaved writes (corrupted log).
- Race condition in file creation.

**Test that would catch this**: Stress test that:
1. Spawns 10 parallel invocations of `run.sh` with the same `--task` ID.
2. Asserts `context.md` is not corrupted (e.g., valid markdown, no interleaved lines).
3. Verifies each agent's output is correctly attributed.

**[MAJOR]** **Unquoted variables in bash**: If `run.sh` uses unquoted variables (e.g., `$prompt` instead of `"$prompt"`), word splitting will break multi-word prompts.

**Test that would catch this**: Unit test that:
1. Invokes `run.sh --prompt "multi word prompt"`.
2. Asserts the agent receives the full prompt string (not just `"multi"`).

**[MINOR]** **No validation of `--mode`**: If an invalid mode (e.g., `--mode invalid`) is passed, the script should fail fast with a clear error. The SKILL.md does not document this behavior.

**Test that would catch this**: Unit test that:
1. Invokes `run.sh --mode invalid`.
2. Asserts the script exits with code 1 and prints: `Error: Invalid mode 'invalid'. Valid modes: arch, code, review, cross`.

---

## Testability Assessment

**[MAJOR]** **Agent CLI dependencies are not mockable**: The SKILL.md does not describe how to test this skill without invoking real Hermes/Claude CLIs. For CI/CD, you need:
- A mock agent CLI (e.g., `mock-hermes.sh`) that accepts the same arguments and returns canned output.
- An environment variable (e.g., `AXEL_AGENT_REGISTRY_PATH`) to override the agent registry for testing.

**Test isolation**: Without mocks, every test invocation will:
- Hit real LLM APIs (slow, expensive, non-deterministic).
- Depend on external services (Hermes CLI availability).

**Observability**: The SKILL.md does not mention logging. For debugging, `run.sh` should:
- Log each agent invocation (command, exit code, duration).
- Log file I/O operations (context.md creation, append).
- Support a `--verbose` flag for detailed output.

**Regression risk**: If the agent registry format changes (e.g., new fields in `studio/developers/*.yaml`), existing tests may break. The SKILL.md should document the registry schema and version it.

---

## Summary

### Top 3 Actionable Findings

1. **[CRITICAL] Missing error handling documentation**  
   - **Issue**: SKILL.md does not describe failure modes (invalid agent ID, permission errors, CLI failures).  
   - **Fix**: Add an "Error Handling" section documenting:
     - Exit codes (0 = success, 1 = invalid args, 2 = agent failure, 3 = I/O error).
     - Error messages for each failure mode.
     - Cleanup behavior (e.g., delete partial `context.md` on failure).
   - **Test**: Integration test that asserts correct exit codes and error messages for each failure mode.

2. **[MAJOR] Concurrency risk in `context.md` writes**  
   - **Issue**: Parallel invocations with the same `--task` ID will corrupt `context.md`.  
   - **Fix**: Use file locking (e.g., `flock` in bash) or atomic append (e.g., `>>` with `O_APPEND`).  
   - **Test**: Stress test with 10 parallel invocations, assert no interleaved lines in `context.md`.

3. **[MAJOR] Agent CLI dependencies are not mockable**  
   - **Issue**: Tests cannot run without real Hermes/Claude CLIs (slow, expensive, non-deterministic).  
   - **Fix**: Add `AXEL_AGENT_REGISTRY_PATH` env var to override agent registry. Provide `mock-hermes.sh` and `mock-claude.sh` for testing.  
   - **Test**: Unit test that sets `AXEL_AGENT_REGISTRY_PATH` to a mock registry and asserts correct agent invocation.

---

## Additional Suggestions for Newcomers

### Missing Information

1. **Prerequisites**: What must be installed before using this skill?
   - Hermes CLI (link to installation guide).
   - Claude Code (version requirement).
   - Python/bash version requirements.

2. **Example walkthrough**: Add a "Quick Start" section with a concrete example:
   ```bash
   # Review architecture for task "auth-refactor"
   bash .agents/skills/axel-cowork/run.sh \
     --task auth-refactor \
     --mode arch \
     --prompt "Review the new JWT auth flow for security issues"
   
   # Check results
   cat _out/agent-sessions/auth-refactor/context.md
   ```

3. **Agent registry format**: Document the schema for `studio/developers/*.yaml`:
   ```yaml
   id: hermes
   engine: hermes-cli
   role: dev-architect
   command: hermes --mode {mode} --prompt "{prompt}"
   ```

4. **Mode descriptions**: Expand the mode table:
   | Mode | Purpose | Example Use Case |
   |---|---|---|
   | `arch` | High-level design review | "Is this microservice split correct?" |
   | `code` | Implementation review | "Check this Python async code for race conditions" |
   | `review` | Post-implementation audit | "Does this PR meet our security standards?" |
   | `cross` | Multi-agent debate | "Hermes proposes, Claude critiques" |

5. **Troubleshooting**: Add a section for common errors:
   - `Error: Agent 'hermes' not found` → Check `studio/developers/hermes.yaml` exists.
   - `Permission denied: _out/agent-sessions/` → Run `mkdir -p _out/agent-sessions`.
   - `Hermes CLI not found` → Install Hermes: `pip install hermes-cli`.

6. **Output format**: Describe the structure of `context.md`:
   ```markdown
   # Task: auth-refactor
   ## [2026-05-16 08:45] hermes [dev-architect]
   <hermes output>
   
   ## [2026-05-16 08:46] claude [dev-implementer]
   <claude output>
   ```

7. **Integration with Studio pipeline**: How does this skill fit into the larger LND Studio workflow? Add a diagram or reference to `studio/docs/architecture/`.

---

## Clarity & Structure Assessment

**Strengths**:
- Concise overview.
- Clear table of developers.
- Storage location is documented.

**Weaknesses**:
- No error handling documentation.
- No example walkthrough.
- No prerequisites section.
- No troubleshooting guide.
- No description of output format.
- No integration context (how does this fit into the Studio pipeline?).

**Recommendation**: Expand the SKILL.md to ~2x its current length by adding the missing sections above. Prioritize the "Quick Start" example and "Error Handling" sections for immediate clarity.
