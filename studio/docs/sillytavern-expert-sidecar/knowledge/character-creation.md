# Character Creation Guide

## Character Card Fields

### Core Fields (Always in Prompt)

| Field | Purpose | Token Impact |
|-------|---------|--------------|
| **Name** | Character identifier (REQUIRED) | Minimal |
| **Description** | Physical, personality, background | Always included |
| **Personality** | Brief personality summary | Always included |
| **Scenario** | Current circumstances/context | Always included |

### Optional Fields

| Field | Purpose | When Used |
|-------|---------|-----------|
| **First Message** | Sets style/tone | Only at chat start |
| **Example Dialogues** | Shows speaking style | Pushed out as context fills |
| **Main Prompt Override** | Custom system prompt | If "Prefer Char. Prompt" enabled |
| **Post-History Instructions** | Custom jailbreak | If "Prefer Char. Instructions" enabled |
| **Character's Note** | Reinforcement injection | At specified depth |

## Token Management

### Context Limits by Model
- **LLaMA 3**: 8192 tokens
- **Claude 3**: 200k tokens  
- **GPT-4**: up to 128k tokens
- **NovelAI Erato/Kayra**: 8192 (Opus tier)

### Red Token Counter Warning
When character definition exceeds 50% of model's context:
- Less "memory" for chat history
- May get only 3-4 exchanges of context
- Not broken, just reduced AI awareness

## Writing Description

### What to Include
- Physical appearance
- Personality traits
- Background/history
- Current situation
- World information
- Speech patterns

### Formatting Methods

#### PLists (Attribute Lists)
```
[Personality: curious, playful, tsundere]
[Appearance: long black hair, amber eyes, petite build]
[Likes: cats, reading, making tea]
```

#### Ali:Chat (Examples with Context)
```
{{char}} loves reading fantasy novels, often staying up late.
When {{char}} sees a cat, she can't resist petting it.
{{char}} speaks formally but slips into casual speech when flustered.
```

#### Prose Style
```
Seraphina is a forest guardian with flowing pink hair and amber eyes.
She carries herself with ethereal grace, her form radiating soft light.
Despite her ancient wisdom, she maintains a gentle, nurturing demeanor.
```

## First Message Best Practices

### Sets the Standard
- AI mimics length and style from first message
- If you want long responses, write long first message
- If you want *actions*, use *asterisks*

### Essential Elements
1. **Scene setting** - Where/when is this?
2. **Character introduction** - How does char appear?
3. **Action/dialogue** - What is char doing/saying?
4. **Hook** - Something for user to respond to

### Example
```
*The forest clearing glows with ethereal light as you awaken. 
A woman with flowing pink hair kneels beside you, her amber eyes 
filled with concern.* 

"Ah, you're finally awake." *She clasps your hands in hers, 
warmth radiating from her touch.* "I found you wounded in my 
forest. The name's Seraphina - I've healed you as best I could."

*She offers a steaming cup of herbal tea.* "How are you feeling?"
```

## Example Dialogues

### Format
```
<START>
{{user}}: "What's your favorite thing about this forest?"
{{char}}: *Seraphina's eyes light up as she spins slowly, gesturing 
at the ancient trees.* "Every living thing here is connected by 
threads of magic. Can you feel it?" *She places your hand on a 
gnarled trunk, and warmth pulses beneath the bark.*
```

### Key Points
- Use `<START>` between example blocks
- Use `{{char}}:` and `{{user}}:` prefixes
- Show desired response style/length
- Demonstrate personality traits in action

## Advanced Definitions

### Character's Note
- Injected at specific depth in chat
- Reinforces traits that fade
- Example use: "{{char}} always speaks with formal politeness"

### Talkativeness (Group Chats)
- 0-100% probability to speak
- Default: 50%
- Set lower for shy characters
- Set higher for chatty characters

## Alternate Greetings

- Multiple first messages as "swipes"
- Randomized in group chats
- Use for different scenarios/moods

## Creator's Metadata
- Not sent to AI
- For organization:
  - Created by
  - Character Version
  - Creator's Notes
  - Tags

## Quick Reference: Character Card V2 Spec

```json
{
  "name": "Seraphina",
  "description": "...",
  "personality": "...",
  "scenario": "...",
  "first_mes": "...",
  "mes_example": "...",
  "creator_notes": "...",
  "system_prompt": "...",
  "post_history_instructions": "...",
  "tags": ["fantasy", "healer"],
  "creator": "username",
  "character_version": "1.0"
}
```
