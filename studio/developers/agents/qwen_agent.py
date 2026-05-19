import asyncio
import os
from pathlib import Path
from .base import BaseAgent

class QwenAgent(BaseAgent):
    """Wrapper for the Qwen CLI."""

    async def call(self, prompt: str, session_dir: Path, **kwargs) -> str:
        timeout = kwargs.get("timeout", 180.0)
        # Candidate command patterns. We try each until one returns successfully.
        candidates = [
            ["qwen", "-p", prompt],
            ["qwen", "--prompt", prompt],
            ["qwen", prompt],
        ]

        # Also support piping prompt to stdin
        stdin_candidates = [["qwen"]]

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

        # fallback: pipe prompt to qwen stdin
        for cmd in stdin_candidates:
            try:
                proc = await asyncio.create_subprocess_exec(*cmd, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env)
                stdout, stderr = await asyncio.wait_for(proc.communicate(input=prompt.encode()), timeout=timeout)
                out = stdout.decode(errors="replace").strip()
                if proc.returncode == 0 and out:
                    return out
            except Exception:
                continue

        # If all failed, attempt a help dump to surface errors
        try:
            proc = await asyncio.create_subprocess_exec("qwen", "--help", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env)
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10.0)
            help_text = stdout.decode(errors="replace") + "\n" + stderr.decode(errors="replace")
        except Exception as e:
            help_text = f"(Failed to run qwen --help: {e})"

        return f"[ERROR qwen] No successful invocation. Help:\n{help_text}"
