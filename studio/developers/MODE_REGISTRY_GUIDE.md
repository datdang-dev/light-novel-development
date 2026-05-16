# Mode Registry Quick Reference Guide

**Last Updated:** 2026-05-16  
**Version:** 1.0.0 (Phase 2)

---

## Overview

The Mode Registry is a YAML-based declarative configuration system that allows adding new orchestrator modes without modifying Python code.

**Key File:** `studio/developers/config/mode_registry.yaml`

---

## Adding a New Mode (Zero-Code)

### Example: Adding a "security" mode

Edit `studio/developers/config/mode_registry.yaml`:

```yaml
modes:
  security:
    description: "Security vulnerability scan"
    execution_type: "single"
    template: "security_scan.md"
    output_schema: "SecurityScanOutput"
    knowledge_namespaces: ["security"]
    knowledge_files:
      security:
        - "owasp_top_10.md"
        - "secure_coding.md"
    agents:
      required: 1
      roles:
        - "security/m-security-expert"
```

**That's it!** No Python code changes needed.

---

## Mode Configuration Fields

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `description` | string | Human-readable mode description | "Architecture review by single agent" |
| `execution_type` | enum | How mode executes | "single", "sequential", "debate" |
| `template` | string | Template filename | "arch_review.md" |
| `output_schema` | string | Pydantic schema name | "ArchReviewOutput" |
| `knowledge_namespaces` | list | Knowledge namespaces to load | ["se", "dev"] |

### Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `knowledge_files` | dict | Specific files per namespace | `se: ["system.md"]` |
| `agents` | dict | Agent requirements | `required: 1, roles: [...]` |
| `steps` | list | For sequential modes | See "review" mode |
| `passes` | list | For debate modes | See "cross" mode |

---

## Execution Types

### 1. Single Agent (`execution_type: "single"`)

One agent processes the task using a template.

**Example:** `arch` mode, `code` mode

**Required:**
- `template`
- `output_schema`
- `knowledge_namespaces`

### 2. Sequential (`execution_type: "sequential"`)

Multiple agents execute in sequence, each using a different mode.

**Example:** `review` mode (arch → code)

**Required:**
- `steps` (list of `{mode, agent_index}`)

**Structure:**
```yaml
review:
  execution_type: "sequential"
  steps:
    - mode: "arch"
      agent_index: 0
    - mode: "code"
      agent_index: 1
```

### 3. Debate (`execution_type: "debate"`)

Multi-agent debate with independent, challenge, and synthesis passes.

**Example:** `cross` mode

**Required:**
- `passes` (list of `{type, ...}`)

**Structure:**
```yaml
cross:
  execution_type: "debate"
  passes:
    - type: "independent"
    - type: "challenge"
      max_words: 200
    - type: "synthesis"
      synthesis_agent: 0
```

---

## Knowledge Loading

### Lazy Loading (Recommended)

Specify exact files to load per namespace:

```yaml
knowledge_files:
  se:
    - "global_rule_hub.md"
    - "delegation_protocol.md"
    - "system.md"
  dev:
    - "anti_slop.md"
    - "sensory_density.md"
```

**Benefits:**
- 80% token reduction (15,000 → 3,000 tokens)
- Faster loading
- More focused context

### Greedy Loading (Deprecated)

Omit `knowledge_files` to load all files in namespace:

```yaml
knowledge_namespaces: ["se"]
# No knowledge_files specified → loads all .md files in se/
```

**Not recommended** - loads unnecessary files.

---

## Global Settings

Configure in `mode_registry.yaml`:

```yaml
settings:
  timeout: 600.0              # Default timeout in seconds
  context_threshold: 120      # Context size threshold
```

Access in code:

```python
from studio.developers.mode_registry import MODE_REGISTRY

timeout = MODE_REGISTRY.get_setting("timeout", 600.0)
threshold = MODE_REGISTRY.get_setting("context_threshold", 120)
```

---

## Mode Registry API

### Python Usage

```python
from studio.developers.mode_registry import MODE_REGISTRY

# Validate mode
is_valid, error_msg = MODE_REGISTRY.validate_mode("arch")

# Get mode config
mode_config = MODE_REGISTRY.get_mode("arch")

# Get template
template = MODE_REGISTRY.get_template("arch")  # Returns "arch_review.md"

# Get schema
schema = MODE_REGISTRY.get_schema("arch")  # Returns "ArchReviewOutput"

# Get knowledge files
files = MODE_REGISTRY.get_knowledge_files("arch", "se")
# Returns: ["global_rule_hub.md", "delegation_protocol.md", "system.md"]

# Get namespaces
namespaces = MODE_REGISTRY.get_knowledge_namespaces("arch")
# Returns: ["se"]

# Get setting
timeout = MODE_REGISTRY.get_setting("timeout", 600.0)
```

---

## Template Requirements

Each mode requires a template file in `studio/developers/config/templates/`.

### Template Structure

```markdown
# {Title}

## Task
{task_description}

## Context
<system_context>
{context}
</system_context>

## Knowledge
<knowledge>
{knowledge}
</knowledge>

## Instructions
{instructions}

## Output Format
Return ONLY valid JSON matching this schema:
{schema}

## Forbidden Patterns
<forbidden_patterns>
{negative_prompts}
</forbidden_patterns>
```

---

## Schema Requirements

Each mode requires a Pydantic schema in `studio/developers/schemas.py`.

### Example Schema

```python
from pydantic import BaseModel

class SecurityScanOutput(BaseModel):
    """Output schema for security scan mode."""
    vulnerabilities: list[str]
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    recommendations: list[str]
    scan_summary: str
```

---

## Testing New Modes

### 1. Validate Registry

```bash
python3 tests/test_mode_registry.py
```

### 2. Test Mode Execution

```bash
python3 -m studio.developers.orchestrator \
  --task test-security \
  --mode security \
  --prompt "Scan this file for vulnerabilities" \
  --agents scanner:security/m-security-expert \
  --files path/to/file.py
```

### 3. Verify Output

Check `_out/agent-sessions/test-security/` for:
- `scanner_last.md` (agent output)
- `context.md` (updated context)

---

## Common Patterns

### Single-Agent Review Mode

```yaml
mymode:
  description: "Custom review mode"
  execution_type: "single"
  template: "my_review.md"
  output_schema: "MyReviewOutput"
  knowledge_namespaces: ["custom"]
  knowledge_files:
    custom:
      - "rules.md"
      - "guidelines.md"
```

### Multi-Step Sequential Mode

```yaml
fullreview:
  description: "Architecture + Code + Security review"
  execution_type: "sequential"
  steps:
    - mode: "arch"
      agent_index: 0
    - mode: "code"
      agent_index: 1
    - mode: "security"
      agent_index: 2
```

### Debate Mode with Synthesis

```yaml
consensus:
  description: "Multi-agent consensus building"
  execution_type: "debate"
  passes:
    - type: "independent"
    - type: "challenge"
      max_words: 150
    - type: "synthesis"
      synthesis_agent: 0
```

---

## Troubleshooting

### Mode Not Found

**Error:** `Unknown mode: mymode`

**Fix:** Check spelling in `mode_registry.yaml` and ensure mode is defined under `modes:` key.

### Template Not Found

**Error:** `Template not found: my_template.md`

**Fix:** Create template file in `studio/developers/config/templates/my_template.md`

### Schema Not Found

**Error:** `Schema not found: MyOutput`

**Fix:** Add schema class to `studio/developers/schemas.py`

### Knowledge Files Not Loading

**Error:** Files not found in namespace

**Fix:** Verify files exist in `studio/developers/config/roles/{namespace}/rules/`

### Validation Errors

**Error:** `Invalid mode configuration`

**Fix:** Run `python3 tests/test_mode_registry.py` to see detailed validation errors

---

## Best Practices

### 1. Use Lazy Loading

Always specify `knowledge_files` to avoid loading unnecessary content:

```yaml
# ✅ GOOD: Lazy loading
knowledge_files:
  se: ["system.md", "delegation_protocol.md"]

# ❌ BAD: Greedy loading
knowledge_namespaces: ["se"]
# (no knowledge_files specified)
```

### 2. Keep Templates Focused

Each template should serve one clear purpose. Don't create "kitchen sink" templates.

### 3. Use Descriptive Mode Names

```yaml
# ✅ GOOD
security-scan:
  description: "OWASP Top 10 vulnerability scan"

# ❌ BAD
mode1:
  description: "Does stuff"
```

### 4. Document Custom Modes

Add comments in `mode_registry.yaml`:

```yaml
# Custom mode for project X - scans for SQL injection
sql-scan:
  description: "SQL injection vulnerability scan"
  ...
```

### 5. Test Before Deploying

Always run tests after adding a new mode:

```bash
python3 tests/test_mode_registry.py
python3 tests/run_all_tests.py
```

---

## Migration from Hardcoded Modes

### Before (Hardcoded)

```python
if mode == "arch":
    template = "arch_review.md"
    schema = "ArchReviewOutput"
    # ... hardcoded logic
elif mode == "code":
    template = "code_review.md"
    schema = "CodeReviewOutput"
    # ... hardcoded logic
```

### After (Registry)

```python
is_valid, error = MODE_REGISTRY.validate_mode(mode)
if not is_valid:
    raise ValueError(error)

mode_config = MODE_REGISTRY.get_mode(mode)
template = MODE_REGISTRY.get_template(mode)
schema = MODE_REGISTRY.get_schema(mode)
```

**Benefits:**
- No code changes to add modes
- Centralized configuration
- Easier to maintain
- Self-documenting

---

## Resources

| Resource | Location |
|----------|----------|
| Mode Registry YAML | `studio/developers/config/mode_registry.yaml` |
| Registry Loader | `studio/developers/mode_registry.py` |
| Templates | `studio/developers/config/templates/` |
| Schemas | `studio/developers/schemas.py` |
| Tests | `tests/test_mode_registry.py` |
| Orchestrator | `studio/developers/orchestrator.py` |

---

## Support

For issues or questions:
1. Check this guide first
2. Run `python3 tests/test_mode_registry.py` for validation errors
3. Review `PHASE_2_COMPLETE.md` for implementation details
4. Check `studio/developers/orchestrator.py` for usage examples

---

**Version History:**
- 1.0.0 (2026-05-16): Initial release with Phase 2
