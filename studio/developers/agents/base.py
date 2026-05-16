from abc import ABC, abstractmethod
from pathlib import Path

class BaseAgent(ABC):
    """Base interface for AI Developer agents in the Studio."""

    def __init__(self, role_name: str, config_dir: Path):
        self.role_name = role_name
        self.config_dir = config_dir
        self.role_content = self._load_role(role_name)

    def _load_role(self, role_name: str) -> str:
        roles_dir = self.config_dir / "roles"
        role_file = roles_dir / f"{role_name}.md"
        if not role_file.exists():
            return f"# Role: {role_name}\n(Role definition not found at {role_file})"
        return role_file.read_text(errors="replace")

    @abstractmethod
    async def call(self, prompt: str, session_dir: Path, **kwargs) -> str:
        """Call the agent CLI or API.
        
        Args:
            prompt: The full prompt string.
            session_dir: Path to the task's session directory for persistence.
        """
        pass
