from abc import ABC, abstractmethod
from pathlib import Path
import json

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

    def _load_knowledge(self, namespace: str, specific_files: list[str] = None) -> str:
        """Load only requested knowledge files from a namespace.

        Args:
            namespace: Knowledge namespace (se, dev, qa)
            specific_files: List of filenames to load. If None, loads all files in namespace.

        Returns:
            XML-wrapped knowledge content
        """
        index_file = self.config_dir / "knowledge_index.json"
        if not index_file.exists():
            return f"<!-- Warning: knowledge_index.json not found at {index_file} -->"

        try:
            index = json.loads(index_file.read_text())
        except json.JSONDecodeError as e:
            return f"<!-- Error parsing knowledge_index.json: {e} -->"

        if namespace not in index["namespaces"]:
            return f"<!-- Warning: Unknown namespace '{namespace}' -->"

        ns = index["namespaces"][namespace]
        base_path = Path(ns["path"])

        # Load only specific files if provided, else load all
        files_to_load = specific_files or ns["files"]

        content = [f"<knowledge namespace='{namespace}' description='{ns['description']}'>"]

        for fname in files_to_load:
            fpath = base_path / fname
            if fpath.exists():
                file_content = fpath.read_text(errors="replace")
                content.append(f"<rule file='{fname}'>\n{file_content}\n</rule>")
            else:
                content.append(f"<!-- Warning: File not found: {fpath} -->")

        content.append("</knowledge>")

        return "\n".join(content)

    @abstractmethod
    async def call(self, prompt: str, session_dir: Path, **kwargs) -> str:
        """Call the agent CLI or API.

        Args:
            prompt: The full prompt string.
            session_dir: Path to the task's session directory for persistence.
        """
        pass
