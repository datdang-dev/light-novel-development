---
name: 'step-03-write-description'
description: 'Craft persona and description fields'
nextStepFile: './step-04-create-lorebook.md'
---

# Step 3: Write Description

## STEP GOAL:

Write the main description and personality fields for the ST card.

## MANDATORY SEQUENCE

### 1. Write Description

Format for ST description field:

```
[Character: {Name}]
[Age: {age}]
[Appearance: {physical summary}]
[Personality: {key traits}]
[Background: {brief history}]
[Likes: {preferences}]
[Dislikes: {aversions}]
[Sexual preferences: {if NSFW card}]
```

### 2. Write Personality

Concise personality summary:

```
{Name} is {archetype}. {Psychological core}. 
{Voice pattern description}. {Behavioral tendencies}.
```

### 3. Write First Message

In-character greeting:

```
*{action description}*

"{In-character dialogue matching voice profile}"

*{additional action/expression}*
```

### 4. Write Example Messages

Format 2-4 example exchanges:

```
<START>
{{user}}: {user message}
{{char}}: *{action}* "{dialogue}" *{reaction}*
<START>
...
```

### 5. Present MENU

```
"✅ Descriptions written!

**Description:** ~{word count} words
**First message:** Ready
**Examples:** {count}

**Chọn:** [C] Continue to Lorebook"
```

---
