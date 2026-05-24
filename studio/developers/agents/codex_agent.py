import asyncio
import os
from pathlib import Path
from .base import BaseAgent

class CodexAgent(BaseAgent):
    """Wrapper for the Codex CLI."""

    async def call(self, prompt: str, session_dir: Path, **kwargs) -> str:
        timeout = kwargs.get("timeout", 180.0)
        # Codex exec mode
        candidates = [
            ["codex", "exec", prompt],
            ["codex", "-m", "o3", "exec", prompt],
        ]

        env = os.environ.copy()

        for cmd in candidates:
            try:
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env)
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
                out = stdout.decode(errors="replace").strip()
                if proc.returncode == 0 and out:
                    return out
            except Exception:
                continue

        # Fallback: call direct API
        return await self.call_api_direct(prompt)
