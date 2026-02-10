# SillyTavern Expert Knowledge Base

## Documentation Source

Primary documentation: `SillyTavern-Docs/` in project root

## Documentation Structure

```
SillyTavern-Docs/
├── Installation/          # Setup guides per platform
├── Usage/
│   ├── API_Connections/   # Backend API setup
│   ├── Characters/        # Character creation guides
│   ├── Chatting/          # Chat features & commands
│   ├── Prompts/           # Advanced formatting & templates
│   ├── User_Settings/     # UI customization
│   ├── macros.md          # Variable macros reference
│   ├── personas.md        # User persona system
│   ├── worldinfo.md       # Lorebook/World Info guide
│   └── faq.md             # Common questions
└── extensions/            # Each extension has its own doc
    ├── TTS.md
    ├── Stable-Diffusion.md
    ├── Expression-Images.md
    └── ...
```

## Key Topics

### Installation
- Windows/Linux/Mac/Docker/Android setup
- Node.js requirements
- Branch selection (release vs staging)

### API Backends
- OpenAI, Claude, KoboldAI, Tabby, etc.
- Local models via various backends
- API key configuration

### Prompt Engineering
- **Context Template**: Overall prompt structure
- **Instruct Mode**: Format for instruction-tuned models
- **Advanced Formatting**: Token limits, depth, order
- **CFG/Mirostat**: Sampling configurations

### Character Creation
- V2 spec fields and purpose
- Description vs Personality distinction
- Example messages format
- Group chat considerations

### World Info/Lorebook
- Entry structure and keys
- Recursive scanning
- Insertion depth and order
- Token budget management

### Extensions
- Core: TTS, Image Gen, Expression Sprites
- Advanced: Summarize, Web Search, Translation
- Setup requirements (Extras API, etc.)

## Add Custom Knowledge

Place additional reference files in this folder:
- Character templates
- Preset collections
- Troubleshooting guides
- Best practice documents
