import asyncio
from pathlib import Path
from .base import BaseAgent

class ClaudeAgent(BaseAgent):
    """Claude Code CLI wrapper for co-work panel."""

    async def call(self, prompt: str, session_dir: Path, **kwargs) -> str:
        # Use task name for session persistence
        task_name = session_dir.name
        safe_task = "".join(c if c.isalnum() else "-" for c in task_name)
        session_name = f"axel-{safe_task}-claude"

        session_marker = session_dir / "claude_session_active"
        is_resume = session_marker.exists()
        
        cmd = ["claude", "--print", "--dangerously-skip-permissions"]
        
        if is_resume:
            cmd += ["--resume", session_name]
        else:
            cmd += ["--name", session_name]
            session_marker.touch()
        
        cmd.append(prompt)

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.DEVNULL,
        )

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=kwargs.get("timeout", 180.0))
        output = stdout.decode(errors="replace").strip()

        if proc.returncode != 0:
            err = stderr.decode(errors="replace").strip()
            if not output:
                 output = f"[ERROR claude] exit code {proc.returncode}\n{err}"
            else:
                 output += f"\n[ERROR claude] {err}"

        return output if output else "(no output from claude)"
