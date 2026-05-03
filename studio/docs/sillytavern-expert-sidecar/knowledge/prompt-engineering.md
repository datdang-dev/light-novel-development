# Prompt Engineering Guide

## Prompt Structure Overview

### Text Completion APIs
```
[System Prompt / Story String]
[World Info - Before Char Defs]
[Character Description]
[Character Personality]
[Scenario]
[World Info - After Char Defs]
[Example Dialogues]
[Chat History]
[Character Name:]
```

### Chat Completion APIs
Uses Prompt Manager with role-based messages (system, user, assistant).

## Story String (Context Template)

### Handlebars Variables
| Variable | Content |
|----------|---------|
| `{{description}}` | Character description |
| `{{scenario}}` | Character scenario |
| `{{personality}}` | Character personality |
| `{{system}}` | System prompt |
| `{{persona}}` | User persona description |
| `{{char}}` | Character name |
| `{{user}}` | User/persona name |
| `{{wiBefore}}` / `{{loreBefore}}` | WI before char defs |
| `{{wiAfter}}` / `{{loreAfter}}` | WI after char defs |
| `{{mesExamples}}` | Formatted example dialogues |
| `{{mesExamplesRaw}}` | Raw example dialogues |
| `{{anchorBefore}}` | Extension prompts (before) |
| `{{anchorAfter}}` | Extension prompts (after) |

### Special: `{{trim}}`
Removes surrounding newlines. Use to prevent unwanted line breaks.

### Example Story String
```handlebars
{{system}}

{{wiBefore}}

# Character: {{char}}
{{description}}

## Personality
{{personality}}

## Current Scenario
{{scenario}}

{{wiAfter}}

{{persona}}
```

## Instruct Mode

For instruction-tuned models (Alpaca, ChatML, Llama2, Mistral, etc.)

### Key Settings

| Setting | Purpose |
|---------|---------|
| Wrap Sequences with Newline | Add \n around sequences |
| Replace Macro in Sequences | Enable {{macro}} in prefixes |
| Include Names | Add character names to messages |

### Sequence Types

**Story String Wrapping:**
- Story String Prefix: Before story string
- Story String Suffix: After story string

**Message Wrapping:**
- User Message Prefix/Suffix
- Assistant Message Prefix/Suffix  
- System Message Prefix/Suffix

**Misc:**
- First Assistant Prefix
- Last Assistant Prefix
- Stop Sequence

### Common Formats

**Alpaca:**
```
### Instruction:
{input}

### Response:
{output}
```

**ChatML:**
```
<|im_start|>system
{system}<|im_end|>
<|im_start|>user
{input}<|im_end|>
<|im_start|>assistant
{output}<|im_end|>
```

**Llama 2 Chat:**
```
[INST] <<SYS>>
{system}
<</SYS>>

{input} [/INST] {output}
```

**Llama 3:**
```
<|start_header_id|>system<|end_header_id|>
{system}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{input}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
{output}<|eot_id|>
```

## Macros Reference

### Basic Macros
| Macro | Returns |
|-------|---------|
| `{{user}}` | User/persona name |
| `{{char}}` | Character name |
| `{{time}}` | Current time |
| `{{date}}` | Current date |
| `{{weekday}}` | Day of week |
| `{{random::a::b::c}}` | Random pick (re-rolls each time) |
| `{{pick::a::b::c}}` | Stable random (consistent) |
| `{{roll::2d6}}` | Dice roll |

### Variable Macros
```
{{getvar::name}}         - Get local variable
{{setvar::name::value}}  - Set local variable
{{getglobalvar::name}}   - Get global variable
{{setglobalvar::name::value}} - Set global variable
```

### Message Macros
| Macro | Returns |
|-------|---------|
| `{{lastMessage}}` | Last message |
| `{{lastUserMessage}}` | Last user message |
| `{{lastCharMessage}}` | Last char message |
| `{{lastMessageId}}` | Index of last message |

### Conditional (Staging Branch)
```handlebars
{{if description}}
  {{description}}
{{else}}
  No description provided.
{{/if}}
```

### Variable Shorthands (Staging)
```
{{.myvar}}          - Get local
{{$myvar}}          - Get global
{{.myvar = value}}  - Set local
{{.counter++}}      - Increment
{{.score += 10}}    - Add
{{.name || Guest}}  - Fallback if falsy
```

## System Prompt Best Practices

### For Roleplay
```
You are {{char}}, a character in an interactive roleplay.
Stay in character at all times. Use *asterisks* for actions.
Never break character or reference being an AI.
Write in third person limited perspective.
```

### For NSFW
```
You are {{char}}. This is a mature (18+) roleplay scenario.
All characters are adults. Explicit content is permitted.
Focus on descriptive writing and atmosphere.
```

### Key Elements
1. **Establish identity** - Who is the AI playing?
2. **Set boundaries** - What can/can't happen?
3. **Define style** - How should responses look?
4. **Clarify perspective** - First/third person?

## Stopping Strings

JSON array format:
```json
["\n{{user}}:", "\n{{char}}:", "<END>", "\n\n\n"]
```

Use to prevent:
- Model impersonation
- Infinite generation
- Format leaking

## Model-Specific Tips

### Claude (Anthropic)
- Responds well to detailed character descriptions
- Roleplay improved with *action* formatting
- System prompt: Character-focused works best
- Good with long context

### GPT (OpenAI)
- Prefers concise system prompts
- May need jailbreak for adult content
- Chat completion format: auto
- Temperature 0.7-1.0 for creativity

### Local Models (GGUF/GPTQ)
- Instruct format MUST match training
- Common: Alpaca, ChatML, Llama2-Chat, Mistral
- Context varies by model/quantization
- Lower context = need shorter character cards

## Prompt Manager (Chat Completion)

For OpenAI/Claude APIs, use Prompt Manager instead of Story String.

### Role Messages
- **System**: Instructions, world, character
- **User**: User's messages
- **Assistant**: AI's responses

### Ordering
Drag and drop prompts to reorder. Higher = earlier in prompt.

### Enable/Disable
Toggle prompts without deleting them.

## Advanced Techniques

### Reinforcement at Depth
Use Character's Note to reinforce traits that fade:
- Depth 0: After last message (highest impact)
- Depth 2-4: Mid-context (moderate)
- Higher: Lower impact

### Author's Note
Real-time injection for scene direction:
```
[Scene: romantic candlelit dinner]
[Style: slow-paced, sensory descriptions]
```

### Post-History Instructions
Like system prompt but at END of context:
- Highest influence on response
- Good for jailbreaks/format reminders

## Troubleshooting Prompts

### Character Breaks
- Add reinforcement via Character's Note
- Increase personality detail
- Add explicit "never break character"

### Responses Too Short
- Lengthen first message
- Add "detailed, descriptive responses"
- Lower repetition penalty

### Responses Too Long
- Shorten first message  
- Add length guidance in system prompt
- Increase repetition penalty

### Wrong Format
- Check instruct mode matches model
- Verify stop strings
- Review example dialogues
