import os
from pathlib import Path
from studio.core.caption_engine.interfaces.prompt_loader import PromptLoader


class StudioPromptLoader(PromptLoader):
    """Loads prompt templates dynamically from the studio folder."""

    def __init__(self, workspace_root: str | None = None):
        if workspace_root:
            self.root = Path(workspace_root)
        else:
            self.root = self._find_workspace_root()

        if self.root.name == "studio":
            self.prompts_dir = self.root / "prompts"
        else:
            self.prompts_dir = self.root / "studio" / "prompts"

    def _find_workspace_root(self) -> Path:
        # Traverse upwards from current file to find the root containing studio/
        curr = Path(__file__).resolve().parent
        for _ in range(7):
            if (curr / "studio").exists() or (curr / "module.yaml").exists() or (curr / ".git").exists():
                return curr
            curr = curr.parent
        return Path("/home/datdang/working/lnd_dev")  # fallback

    def _read_file(self, filename: str) -> str:
        filepath = self.prompts_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Required prompt template not found at {filepath}")
        return filepath.read_text(encoding="utf-8").strip()

    def load_direct_prompt(self, mood_seed: str, user_context: str = "", prompt_name: str = "direct_caption") -> str:
        if not prompt_name.endswith(".txt") and not prompt_name.endswith(".md"):
            filename = f"{prompt_name}.txt"
        else:
            filename = prompt_name

        template = self._read_file(filename)
        if user_context:
            template += f"\n\nContext to incorporate:\n{user_context}"
        return template
