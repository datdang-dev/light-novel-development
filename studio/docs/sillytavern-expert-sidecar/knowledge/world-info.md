# World Info (Lorebook) Guide

## Core Concept

World Info dynamically injects lore/context into prompts when keywords are detected.
Only relevant entries are included, saving tokens.

## Entry Structure

### Key (Trigger Keywords)
- Comma-separated list
- Case-insensitive by default
- Supports regex: `/pattern/flags`

**Example Keys:**
```
Seraphina, the guardian, forest spirit
```

**Regex Key Example:**
```js
/(?:{{char}}|she) (?:talks about|mentions) (?:the )?forest/i
```

### Optional Filter (Secondary Keys)
Logic options:
- **AND ANY**: Primary + any filter = activate
- **AND ALL**: Primary + all filters = activate  
- **NOT ANY**: Primary + none of filters = activate
- **NOT ALL**: Block if all filters present

### Entry Content
The actual lore text inserted when triggered.
- Keep concise for token efficiency
- Can reference other entries for recursion
- Supports macros like `{{char}}`, `{{user}}`

## Insertion Positions

| Position | Impact | Best For |
|----------|--------|----------|
| Before Char Defs | Moderate | World background |
| After Char Defs | Higher | Important lore |
| Before Example Messages | Variable | Example context |
| After Example Messages | Variable | Example context |
| Top of Author's Note | Variable | Reminders |
| Bottom of Author's Note | Variable | Reinforcement |
| @ Depth X | Precise control | Timed injection |
| Outlet | Manual control | Custom placement |

### @ Depth Roles
- ⚙️ System message
- 👤 User message
- 🤖 Assistant message

### Outlet System
```
{{outlet::YourOutletName}}
```
Place in Prompt Manager to manually insert entry content.

## Insertion Order

Numeric value - higher = closer to end of context = more impact.
- Entry with Order 100 appears before Order 250
- Constant entries inserted first
- Direct keyword mentions > recursive activation

## Entry Strategy (🔵🟢🔗)

| Icon | Name | Behavior |
|------|------|----------|
| 🔵 Blue | Constant | Always in prompt |
| 🟢 Green | Normal | Keyword-activated |
| 🔗 Chain | Vectorized | Embedding similarity match |

## Probability (Trigger %)

- 100% = Always when activated
- 50% = Coin flip
- 0% = Disabled
- Use for random events

## Inclusion Groups

When multiple entries share a group:
- Only ONE is inserted
- Selection by Group Weight (random)
- Or by Order (if Prioritize Inclusion enabled)

**Use Case:** Multiple outcomes for same trigger
```
Group: "weather_event" 
Entry 1: Sunny day (Weight: 70)
Entry 2: Rainy day (Weight: 30)
```

## Recursive Scanning

Entries can activate other entries via content keywords.

**Example:**
```
Entry #1
Key: Bessie
Content: Bessie is a cow and is friends with Rufus.

Entry #2  
Key: Rufus
Content: Rufus is a dog.
```
Mentioning "Bessie" also pulls in "Rufus" entry.

### Recursion Controls
- **Non-recursable**: Won't activate from other entries
- **Prevent further recursion**: Won't trigger more entries
- **Delay until recursion**: Only activates during recursive scans
- **Recursion Level**: Controls order of delayed entries

## Timed Effects

### Sticky
Entry stays active for N messages after triggering.
- Ignores probability on subsequent scans
- Good for ongoing conditions

### Cooldown
Entry can't reactivate for N messages.
- Prevents spam
- Good for one-time events

### Delay
Requires N messages before can activate.
- Delay=2 means needs at least 2 messages in chat
- Good for late-game reveals

**Combined Example:**
```
Sticky=3, Cooldown=2, Delay=2

Message 0: delay (can't trigger)
Message 1: ACTIVATES
Message 2: sticky (stays active)
Message 3: sticky  
Message 4: sticky
Message 5: cooldown (can't trigger)
Message 6: cooldown
Message 7: CAN trigger again
```

## Activation Settings

### Scan Depth
How many messages to scan for keywords.
- 0 = Only recursed entries + Author's Note
- 1 = Last message only
- Higher = More context, more activations

### Context Budget
- Context % or flat token Budget
- Limits total WI tokens
- Constant entries use budget first

### Min Activations
Ignores scan depth, keeps scanning until N entries activate.
- Still respects Max Depth
- Still respects Budget

### Case-Sensitive Keys
Disabled by default. Enable for common words.
- "rose" vs "Rose"

### Match Whole Words
Enabled by default. 
- "king" won't match "liking"
- Disable for CJK languages

## Character Lore

Bind World Info to specific characters:
1. Open Character Management
2. Click globe button
3. Select World Info file

### Insertion Strategies
- **Sorted Evenly**: All mixed by Order
- **Character Lore First**: Char WI, then Global
- **Global Lore First**: Global WI, then Char

## Best Practices

1. **Keep entries concise** - Token efficiency
2. **Use specific keywords** - Avoid false triggers
3. **Test recursion chains** - Prevent infinite loops
4. **Set appropriate depth** - Balance relevance vs budget
5. **Use inclusion groups** - Manage mutual exclusions
6. **Document with memos** - Organization
7. **Balance constant vs triggered** - Token budget
