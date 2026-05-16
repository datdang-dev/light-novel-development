from pathlib import Path
from typing import Dict, Type
from .base import BaseAgent
from .hermes_agent import HermesAgent
from .claude_agent import ClaudeAgent

AGENT_MAP: Dict[str, Type[BaseAgent]] = {
    "hermes": HermesAgent,
    "claude": ClaudeAgent,
    # "codex": CodexAgent, # Placeholder for future restoration if needed
}

def get_agent_class(agent_id: str) -> Type[BaseAgent]:
    """Retrieve agent class by ID."""
    if agent_id not in AGENT_MAP:
        raise ValueError(f"Unknown agent ID: {agent_id}. Available: {list(AGENT_MAP.keys())}")
    return AGENT_MAP[agent_id]

def create_agent(agent_id: str, role_name: str, config_dir: Path) -> BaseAgent:
    """Factory to instantiate a developer agent."""
    cls = get_agent_class(agent_id)
    return cls(role_name, config_dir)
