"""
LND Studio Developers Layer

Multi-agent review system with:
- Auto-summarizing context management (XML-wrapped)
- Schema-validated agent outputs (Pydantic)
- Lazy knowledge loading (namespace-based)
- Extensible mode system
- Optional Ruflo MCP orchestration
"""

from .ruflo_adapter import RufloMCPAdapter, RufloConfig, run_panel_with_ruflo
from .orchestrator import run_panel, MODE_REGISTRY, SCHEMA_MAP

__all__ = [
    "RufloMCPAdapter",
    "RufloConfig",
    "run_panel_with_ruflo",
    "run_panel",
    "MODE_REGISTRY",
    "SCHEMA_MAP",
]
