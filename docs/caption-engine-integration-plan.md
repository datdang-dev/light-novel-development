# Caption-Engine Integration Plan

## Objective
Create a SOLID/CLEAN architecture component `caption-engine` in `studio/core/` that encapsulates the erotic captioning logic, separating concerns and eliminating design smells from the current implementation.

## Current State Analysis
The erotic image captioning functionality is currently distributed across:
- `studio/services/erotic-image-captioner/` (service layer)
- `studio/agents/erotic-captioner.agent.yaml` (agent configuration)
- `studio/config/pipelines/erotic-captioner.yaml` (pipeline definition)
- MCP tools in `playground/toriigate/` (experimental)
- Prompts in `studio/prompts/` (decoupled but not encapsulated)

This distribution creates:
- Tight coupling between agent, service, and pipeline layers
- Diffusion of responsibility (no single owner of captioning logic)
- Difficulty in testing and maintaining business rules
- Violation of Single Responsibility Principle

## Target Architecture
The `caption-engine` will reside in `studio/core/caption-engine/` and follow CLEAN architecture principles:

```
studio/core/caption-engine/
├── entities/                # Enterprise-wide business objects
│   ├── caption.pydantic.py  # CaptionOutput schema
│   ├── forensic.pydantic.py # ForensicOutput schema
│   └── prelude.pydantic.py  # ScenePrelude schema
├── use_cases/               # Application-specific business rules
│   ├── generate_caption.py  # Main use case: orchestrates pipeline
│   ├── validate_caption.py  # Quality gate enforcement
│   └── apply_fetish_rules.py # Fetish exploitation logic
├── interfaces/              # Gateways (interfaces to outer layers)
│   ├── mcp_client.py        # Abstract MCP tool interface
│   ├── prompt_loader.py     # Abstract prompt loading interface
│   └── output_repository.py # Abstract output storage interface
├── adapters/                # Implementations of interfaces
│   ├── toriigate_mcp_adapter.py  # Concrete MCP client
│   ├── studio_prompt_loader.py   # Loads from studio/prompts/
│   └── filesystem_output_repo.py # Saves to _lnd-output/
└── caption_engine.py        # Facade / entry point (optional)
```

## Integration Plan: What TO Do

### 1. Create the Component Structure
- [ ] Create `studio/core/caption-engine/` directory
- [ ] Implement the CLEAN architecture structure above
- [ ] Move captioning-specific business logic from services/agents into appropriate layers

### 2. Apply SOLID Principles
**Single Responsibility (S):**
- [ ] Each class/module has exactly one responsibility
- [ ] Example: `generate_caption.py` only orchestrates the pipeline
- [ ] Example: `validate_caption.py` only enforces quality gates
- [ ] Example: `toriigate_mcp_adapter.py` only handles MCP communication

**Open/Closed (O):**
- [ ] Design for extension without modification
- [ ] Example: New MCP backends can be added by implementing `MCPClient` interface
- [ ] Example: New output formats can be added via `OutputRepository` implementations
- [ ] Use dependency injection to allow swapping implementations

**Liskov Substitution (L):**
- [ ] Ensure subclasses can substitute parents without breaking functionality
- [ ] Example: Any `MCPClient` implementation must work with `generate_caption.py`
- [ ] Example: Test with mock implementations to verify substitutability

**Interface Segregation (I):**
- [ ] Clients depend only on methods they use
- [ ] Example: `generate_caption.py` depends only on `MCPClient.analyze_forensic()` not on unrelated methods
- [ ] Example: Split large interfaces into smaller, specific ones

**Dependency Inversion (D):**
- [ ] High-level modules depend on abstractions, not concretions
- [ ] Example: `generate_caption.py` depends on `MCPClient` interface, not `ToriigateMCPAdapter`
- [ ] Example: Inject dependencies via constructor or setter

### 3. Move Business Logic Appropriately
- [ ] **Entities (`studio/core/caption-engine/entities/`)**: 
  - Pure data structures with validation (using pydantic)
  - No business logic, only data validation and transformation
  - Examples: `CaptionOutput`, `ForensicOutput`, `ScenePrelude`
  
- [ ] **Use Cases (`studio/core/caption-engine/use_cases/`)**:
  - Application-specific business rules
  - Orchestrate flow between entities and interfaces
  - Examples:
    - `generate_caption.py`: Main orchestrator (forensic → prelude → caption)
    - `validate_caption.py`: Applies Gooner audit rules, sensory density checks
    - `apply_fetish_rules.py`: Integrates user fetish profile with caption generation
    - `check_anti_slop.py`: Enforces anti-slop directives
    
- [ ] **Interfaces (`studio/core/caption-engine/interfaces/`)**:
  - Abstract base classes defining contracts
  - Examples:
    - `MCPClient`: `analyze_forensic()`, `generate_prelude()`, `generate_caption()`
    - `PromptLoader`: `load_forensic_prompt()`, `load_prelude_prompt()`, `load_caption_prompt()`
    - `OutputRepository`: `save_forensic()`, `save_prelude()`, `save_caption()`
  
- [ ] **Adapters (`studio/core/caption-engine/adapters/`)**:
  - Concrete implementations of interfaces
  - Examples:
    - `ToriigateMCPAdapter`: Implements `MCPClient` using the actual MCP server
    - `StudioPromptLoader`: Implements `PromptLoader` by reading from `studio/prompts/`
    - `FilesystemOutputRepository`: Implements `OutputRepository` by writing to `_lnd-output/`
  
- [ ] **Facade (Optional)**:
  - `caption_engine.py`: Simple entry point that wires everything together
  - Example: `CaptionEngine(mcp_client, prompt_loader, output_repo).process_image(image_path)`

### 4. Maintain Compatibility with Existing Systems
- [ ] Ensure the new component integrates with:
  - Existing agent YAML files (update to use caption-engine instead of direct service calls)
  - Existing pipeline YAML files (update to use caption-engine as a service)
  - Existing MCP server (no changes needed; it remains the backend)
  - Existing prompts in `studio/prompts/` (still used by StudioPromptLoader)
  - Existing output directory structure (`_lnd-output/`)
  
- [ ] Update agent configurations to depend on caption-engine:
  - `erotic-captioner.agent.yaml`: Change `skill:` to point to caption-engine facade
  - Or remove skill dependency entirely if agent now directly uses caption-engine

### 5. Implement Comprehensive Testing Strategy
- [ ] Unit tests for each use case (mock interfaces)
- [ ] Integration tests for adapter implementations
- [ ] Contract tests to ensure adapters satisfy interfaces
- [ ] End-to-end tests using the full stack (but keep these minimal/fast)
- [ ] Property-based testing for business rules (e.g., sensory density requirements)

### 6. Documentation and Knowledge Transfer
- [ ] Update `studio/docs/caption-engine-architecture.md` with CLEAN architecture details
- [ ] Create ADR (Architecture Decision Record) for this refactor
- [ ] Update onboarding documentation for new developers
- [ ] Create diagrams showing the dependency flow

## Integration Plan: What NOT to Do

### 1. Avoid Leaking Abstractions
- [ ] **DO NOT** let outer layers (agents, services, pipelines) know about CLEAN architecture internals
- [ ] **DO NOT** expose `use_cases/` or `entities/` directly to outer layers
- [ ] **DO NOT** allow agents to import and use `studio/core/caption-engine/use_cases/generate_caption.py` directly
- [ ] **INSTEAD**: Outer layers should depend only on stable interfaces (if any) or go through the established service/agent contracts

### 2. Avoid Breaking Dependency Rule
- [ ] **DO NOT** let inner layers (entities, use_cases) depend on outer layers
- [ ] **DO NOT** have `generate_caption.py` import anything from `studio/services/` or `studio/agents/`
- [ ] **DO NOT** have entities know about MCP, file systems, or prompts
- [ ] **INSTEAD**: Dependencies point inward only; outer layers depend on inner layers

### 3. Avoid Creating God Objects
- [ ] **DO NOT** put all captioning logic in one monolithic class
- [ ] **DO NOT** have a single `CaptionEngine` that does forensic analysis, prelude generation, captioning, validation, and output
- [ ] **INSTEAD**: Follow the principle: "Classes should be small, and methods should be smaller"

### 4. Avoid Tight Coupling to Specific Implementations
- [ ] **DO NOT** have use cases instantiate concrete adapters directly (e.g., `ToriigateMCPAdapter()`)
- [ ] **DO NOT** have use cases know about specific MCP servers or prompt locations
- [ ] **INSTEAD**: Use dependency injection - pass implementations via constructor

### 5. Avoid Leaking Framework Details
- [ ] **DO NOT** let use cases know about Claude Code, MCP, or LND Studio-specific framework details
- [ ] **DO NOT** have business logic that references `studio/config/`, `studio/agents/`, etc.
- [ ] **INSTEAD**: Keep use cases focused purely on captioning domain logic
- [ ] Framework details belong in adapters (outer layer)

### 6. Avoid Premature Optimization
- [ ] **DO NOT** add caching, async optimizations, or complex patterns until proven necessary
- [ ] **DO NOT** complicate the architecture with patterns that aren't currently needed
- [ ] **INSTEAD**: Start simple, follow YAGNI (You Aren't Gonna Need It)
- [ ] Optimize only when measurements show a bottleneck

### 7. Avoid Violating LND Studio Rules
- [ ] **DO NOT** let the architecture compromise any LND Studio canons or Gooner principles
- [ ] **DO NOT** allow output that violates sensory density rules, anti-slop directives, or fetish protocols
- [ ] **INSTEAD**: These rules belong in the use cases layer (specifically in validation and application use cases)

### 8. Avoid Creating Unnecessary Layers
- [ ] **DO NOT** add layers just for the sake of having layers
- [ ] **DO NOT** over-engineer for hypothetical future requirements
- [ ] **INSTEAD**: Follow the Rule of Three: if you need something twice, consider making it reusable; if you need it three times, make it reusable
- [ ] **INSTEAD**: Start with what you need now; refactor when duplication occurs

## Migration Steps

### Phase 1: Preparation (Zero Downtime)
- [ ] Create `studio/core/caption-engine/` directory structure
- [ ] Implement entities and interfaces without changing existing code
- [ ] Write unit tests for new components
- [ ] Verify no conflicts with existing implementation

### Phase 2: Strangler Fig Pattern
- [ ] Implement the first use case (e.g., `validate_caption.py`) 
- [ ] Route a small percentage of traffic through the new component (via feature flag)
- [ ] Compare outputs between old and new systems
- [ ] Gradually increase traffic percentage

### Phase 3: Full Cutover
- [ ] Once validation passes at 100%, update all agents/pipelines to use caption-engine
- [ ] Remove old implementation from `studio/services/erotic-image-captioner/`
- [ ] Remove obsolete agent and pipeline configurations
- [ ] Keep MCP server and prompts unchanged (they remain outer layer dependencies)

### Phase 4: Cleanup and Refinement
- [ ] Remove any temporary code or feature flags
- [ ] Perform final architecture review
- [ ] Update all documentation
- [ ] Conduct knowledge transfer session

## Success Criteria
- [ ] All existing tests pass (no regression in functionality)
- [ ] New component follows SOLID principles (verifiable via dependency analysis)
- [ ] CLEAN architecture boundaries are respected (no inward-pointing dependencies)
- [ ] Component is easily testable (high unit test coverage, low mocking complexity)
- [ ] Business logic is isolated from framework specifics
- [ ] Adding a new MCP backend requires only adding a new adapter (no use case changes)
- [ ] Changing output format requires only adding a new repository implementation
- [ ] All LND Studio rules (Goober, sensory density, anti-slop, etc.) are enforced in use cases layer

## Files to Create
```
studio/core/caption-engine/
├── __init__.py
├── entities/
│   ├── __init__.py
│   ├── caption.pydantic.py
│   ├── forensic.pydantic.py
│   └── prelude.pydantic.py
├── use_cases/
│   ├── __init__.py
│   ├── generate_caption.py
│   ├── validate_caption.py
│   ├── apply_fetish_rules.py
│   └── check_anti_slop.py
├── interfaces/
│   ├── __init__.py
│   ├── mcp_client.py
│   ├── prompt_loader.py
│   └── output_repository.py
├── adapters/
│   ├── __init__.py
│   ├── toriigate_mcp_adapter.py
│   ├── studio_prompt_loader.py
│   └── filesystem_output_repo.py
└── caption_engine.py  # Optional facade
```

## Related Files to Update
- `studio/agents/erotic-captioner.agent.yaml` (update skill/reference)
- `studio/config/pipelines/erotic-captioner.yaml` (update to use caption-engine)
- `studio/docs/architecture/` (add caption-engine architecture docs)
- `studio/config/EC_manifest.md` (update if needed to reflect new architecture)

## Estimated Effort
- **Analysis & Design**: 2 hours
- **Implementation**: 6-8 hours
- **Testing**: 2-3 hours
- **Migration & Validation**: 2 hours
- **Documentation**: 1 hour
- **Total**: ~13-16 hours

This plan ensures we create a maintainable, testable, and extensible captioning component that strictly adheres to SOLID and CLEAN architecture principles while preserving all existing functionality and compliance with LND Studio rules.