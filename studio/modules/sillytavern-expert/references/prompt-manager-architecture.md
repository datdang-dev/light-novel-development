# SillyTavern Prompt Manager Architecture

> Internal context assembly logic inferred from ST source behavior and raw API request analysis.
> Source: Celia V5.4 preset analysis + raw_request samples + ST documentation.

## Core Mechanics

### How Prompts Become Context

```
Prompt Manager State (UI)
    │
    ├── enabled: true      → ALWAYS included in system message
    ├── enabled: false     → Toggleable module (library), NOT included
    ├── marker: true       → Dynamic content injection (resolved at request time)
    └── role: system       → Placed in system message
        role: user         → Placed in user message slot
```

**Final Message Assembly:**

```
messages: [
  { role: "system", content: "<all enabled prompts concatenated in injection_order>" },
  { role: "user",   content: "<current user input>" },
  { role: "assistant", content: "<chat history / generation>" }
]
```

### Injection Order Logic

All `enabled: true` prompts are concatenated in **ascending `injection_order`** value into a single system message string.

```
injection_order: 0     → First in system message (primacy slot)
injection_order: 500   → Middle
injection_order: 1000  → Last (recency slot)
```

**Rule of thumb:**
- `0-100`: Core identity, language, safety — things the model MUST see first
- `101-500`: Context and world-building
- `501-800`: Behavior and formatting directives (recency-sensitive)
- `801-1000`: Post-instructions and reinforcement

### Marker Resolution

When `marker: true` is set on a prompt, the system replaces the marker tag with dynamic content at request time:

| Marker | Resolves To | Source |
|--------|-------------|--------|
| `{{description}}` / `{{charDescription}}` | Character description field | V3 card `data.description` |
| `{{personality}}` / `{{charPersonality}}` | Character personality field | V3 card `data.personality` |
| `{{scenario}}` | Scenario field | V3 card `data.scenario` |
| `{{persona}}` / `{{userPersona}}` | User persona description | Persona manager |
| `{{wiBefore}}` / `{{worldInfoBefore}}` | World info (before char) | World Info entries with position:before |
| `{{wiAfter}}` / `{{worldInfoAfter}}` | World info (after char) | World Info entries with position:after |
| `{{examples}}` / `{{exampleDialogue}}` | Example messages | V3 card `data.mes_example` |
| `{{history}}` / `{{chatHistory}}` | Recent chat turns | Chat log |
| `{{ujb}}` / `{{userJailbreak}}` | User jailbreak prompt | User settings |
| `{{cjb}}` / `{{charJailbreak}}` | Character jailbreak prompt | Character settings |
| `{{sysPromptOverride}}` | Override system prompt | Advanced settings |
| `{{currentSnippet}}` / `{{currentSc}}` | Active lorebook entries | World Info resolved by keys |

**Critical:** Markers in `role: user` slots are resolved too. Some presets use user-role prompts to inject character context — ST supports this, but it changes the `alternate_roles` composition.

### The "Enabled + Marker" Interaction

```
marker: false  →  Static text prompt (content is literal)
marker: true   →  Content is a single marker tag like {{description}}
                  ST replaces it with the actual field content at request time
```

**In Celia V5.4 pattern:**

```yaml
# Static rule prompt (always the same text)
- content: "Write in Vietnamese..."
  enabled: true
  marker: false
  injection_order: 100

# Dynamic content prompt (changes with character card)
- content: "{{description}}"
  enabled: true
  marker: true
  injection_order: 300
```

## Context Window Assembly Priority

When ST builds the full context window (not just system message), the order is:

1. **System Message** (all enabled prompts concatenated)
2. **Instruct Mode Pre-Query** (if configured)
3. **Chat History** (most recent N messages, trimmed to fit context)
4. **Depth Prompt** (if configured — Claude-specific post-context anchoring)

### Context Budget (Token Accounting)

ST uses a "story string" / context template to allocate the context window:
```
context: <system prompts> + <world info before> + <description> +
         <personality> + <scenario> + <world info after> +
         <persona> + <examples> + <chat history> + <depth prompt>
```

Each section has a configured token limit. When limit is exceeded, content is **truncated from the middle** (not the end).

## Module Library Pattern (enabled: false)

Modules with `enabled: false` act as a **toggleable library**. They don't appear in context by default but can be enabled:
- Per-chat via the ST UI toggle
- Via slash commands
- In specific character cards (override at card level)

**This is the pattern used in Celia V5.4 for:**
- POV selectors (1st/2nd/3rd person)
- RP type modules (Immersive, Internet Chat, TableRPG)
- Pacing controls
- Language toggles

## Vietnamese Roleplay Implications

### What Happens With Bad Prompt Ordering

```
[WRONG]
injection_order: 500 → Character description (marker: true)
injection_order: 100 → "Write in Vietnamese" (static)
injection_order: 50  → NSFW permissions
injection_order: 10  → Persona description

Result: NSFW permission comes BEFORE persona. Model sees "pacing" instructions
in the primacy slot instead of identity. Character description is in the MIDDLE
of rules. Wasted primacy.
```

```
[OPTIMAL for VN R18]
injection_order: 0   → Core identity + Vietnamese language directive
injection_order: 50  → NSFW permission + banned word list
injection_order: 100 → Format rules (novel format, pronoun gradient)
injection_order: 200 → Character description (marker: true)
injection_order: 300 → Scenario (marker: true)
injection_order: 400 → World info before
injection_order: 500 → Behavioral rules (sensory density, COT, anti-slop)
injection_order: 600 → World info after
injection_order: 700 → Persona (marker: true)
injection_order: 800 → Example dialogues
injection_order: 900 → Post-instructions / reinforcement
```

### Model-Specific Assembly Notes

| Model | System Message Behavior | Context Sensitivity |
|-------|------------------------|---------------------|
| **Claude** | Reads entire system msg carefully. Sensitive to primacy/recency. Supports `depth_prompt` for post-context anchoring. | Strong adherence to system instructions. Long descriptions OK. |
| **GPT (3.5/4)** | Reads system msg but optimized models (4o) are less sensitive to ordering. Concise > verbose. | Good but can "forget" mid-context instructions. Recency matters more. |
| **Local (Llama/Mistral)** | Instruct format alignment critical. Needs explicit format tokens. More sensitive to prompt injection from examples. | Heavily recency-biased. Key instructions should be near end too. |
| **OpenRouter** | Varies by model. Use generic instruct format with tiered safety. Fallback chain might change behavior. | Unpredictable across model fallbacks. Keep core instructions model-agnostic. |

## Raw Request Verification

To simulate what the model sees:

```
1. Collect all prompts where enabled: true
2. Sort by injection_order ascending
3. For each prompt:
   - If marker: false → literal content
   - If marker: true → resolve marker to actual field content
4. Concatenate into single system message string
5. Build messages array
6. Estimate token count (approx 1 token/4 chars for English, variable for Vietnamese)
```

This is the single most important debugging technique. Never trust what the UI shows — trace the actual request.
