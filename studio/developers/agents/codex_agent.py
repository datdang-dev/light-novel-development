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

        # Fallback: help dump
        try:
            proc = await asyncio.create_subprocess_exec("codex", "exec", "--help", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env)
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10.0)
            help_text = stdout.decode(errors="replace") + "\n" + stderr.decode(errors="replace")
        except Exception as e:
            help_text = f"(Failed to run codex exec --help: {e})"

        return f"[ERROR codex] No successful invocation. Help:\n{help_text}"
