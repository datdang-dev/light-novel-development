# Personas Guide

## What is a Persona?

Your identity in chats - name, avatar, and optional description.
Allows switching roles without manual updates.

## Creating a Persona

1. Open Persona Management (😊 button in top menu)
2. Click "Create" button
3. Enter name
4. Add description (optional)
5. Set avatar (optional)

### Convert Character to Persona
Open character → More... → Convert to Persona
- Uses name and description only
- Swaps {{user}} and {{char}} if needed

## Persona Description

Your traits, appearance, background, etc.

### Insertion Positions
| Position | When Used |
|----------|-----------|
| None | Disabled |
| In Story String | With character info (default) |
| Top/Bottom of Author's Note | With AN |
| In Chat @ Depth X | At specific depth |

Position saved per persona.

## Persona Connections

### Chat Lock (🔒)
- Persona bound to specific chat
- Auto-selects when opening that chat

### Character Lock (🔗)
- Persona bound to character
- Auto-selects for all chats with that char

### Default Persona (👑)  
- Used when no other locks apply
- Yellow border indicator
- Only one can be default

### Temporary Persona
- Using different persona despite connection
- Resets on page reload or chat switch
- Can convert to chat lock

## Multiple Personas per Character

Enable in Global Persona Settings:
- "Allow multiple persona connections per character"
- Popup asks which persona when opening chat

## Slash Commands

```
/persona <name>        - Switch persona
/persona-lock type=chat on    - Lock to chat
/persona-lock type=character on   - Lock to character  
/persona-lock type=default   - Set as default
/persona-sync          - Re-attribute past messages
```

## Best Practices

1. **Use persona for immersion** - Let AI know about you
2. **Match persona to scenario** - Different personas for different settings
3. **Keep descriptions concise** - Token efficiency
4. **Use locks strategically** - Reduce switching overhead
5. **Backup personas** - Use backup button in management

## Example Persona Description

```
{{user}} is a 25-year-old adventurer with short brown hair and 
green eyes. They carry a worn leather satchel and a trusty sword. 
Known for their quick wit and kind heart, though they tend to 
get into trouble due to curiosity.
```
