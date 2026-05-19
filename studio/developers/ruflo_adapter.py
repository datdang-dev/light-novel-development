"""
Ruflo MCP Adapter for LND Studio developers layer.

This adapter provides optional Ruflo orchestration, shared memory, and routing
while preserving the existing orchestrator interface.

Usage:
    from studio.developers.ruflo_adapter import RufloMCPAdapter

    # Wrap your orchestrator calls
    adapter = RufloMCPAdapter()
    result = await adapter.run_with_orchestration(task, mode, prompt, agents)
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

# Check for MCP availability - handle both import styles
HAS_MCP = False
MCP_IMPORT_ERROR = None

try:
    import mcp
    HAS_MCP = True
except ImportError as e:
    MCP_IMPORT_ERROR = f"mcp package: {e}"

# Try alternative import paths for Ruflo MCP tools
RUFLO_TOOLS_AVAILABLE = False
try:
    # Check if Ruflo MCP tools are available via direct attribute access
    import mcp
    if hasattr(mcp, 'mcp__ruflo__swarm_init'):
        RUFLO_TOOLS_AVAILABLE = True
except Exception:
    pass


@dataclass
class RufloConfig:
    """Configuration for Ruflo MCP integration."""
    enabled: bool = False
    swarm_id: Optional[str] = None
    topology: str = "hierarchical"
    strategy: str = "specialized"
    max_agents: int = 5
    memory_namespace: str = "lnd_dev"
    routing_enabled: bool = True
    memory_enabled: bool = True
    health_enabled: bool = True


@dataclass
class AgentTask:
    """Represents a task assigned to an agent."""
    task_id: str
    description: str
    agent_id: str
    role: str
    status: str = "pending"
    result: Optional[str] = None
    score: Optional[float] = None


class RufloMCPAdapter:
    """
    Adapter layer for Ruflo MCP tools.

    Provides:
    - Swarm orchestration (hierarchical, queen-led)
    - Shared memory for cross-session state
    - Task routing with semantic similarity
    - Agent health monitoring
    """

    def __init__(self, config: Optional[RufloConfig] = None):
        self.config = config or RufloConfig()
        self._session = None
        self._initialized = False

    async def initialize(self) -> bool:
        """Initialize Ruflo MCP connection."""
        if not self.config.enabled:
            return False

        if not HAS_MCP:
            print("[!] Ruflo MCP not available (mcp package missing)")
            return False

        try:
            # In a real implementation, this would establish an MCP connection
            # For now, we'll mark as initialized for demo purposes
            self._initialized = True
            return True
        except Exception as e:
            print(f"[!] Ruflo initialization failed: {e}")
            return False

    async def ensure_initialized(self) -> bool:
        """Ensure adapter is initialized, initialize if needed."""
        if not self._initialized:
            return await self.initialize()
        return True

    async def init_swarm(self, swarm_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Initialize a Ruflo swarm for orchestration.

        Returns swarm configuration including swarm_id.
        """
        if not await self.ensure_initialized():
            return {"error": "Ruflo not enabled"}

        # Check if Ruflo MCP tools are available
        if not RUFLO_TOOLS_AVAILABLE:
            # Demo mode: simulate swarm initialization
            return {
                "swarm_id": swarm_id or "swarm-lnd-dev-001",
                "topology": self.config.topology,
                "strategy": self.config.strategy,
                "max_agents": self.config.max_agents,
                "status": "initialized",
                "demo_mode": True,
                "note": "Ruflo MCP tools not available - running in demo mode"
            }

        try:
            from mcp import mcp__ruflo__swarm_init

            result = await mcp__ruflo__swarm_init(
                topology=self.config.topology,
                strategy=self.config.strategy,
                maxAgents=self.config.max_agents,
                config={"swarmId": swarm_id}
            )

            return result
        except Exception as e:
            return {
                "error": str(e),
                "swarm_id": swarm_id or "swarm-lnd-dev-001",
                "status": "fallback"
            }

    async def route_task(self, task: str, context: str = "") -> Dict[str, Any]:
        """
        Route a task to the optimal agent using Ruflo's semantic router.

        Returns:
            {
                "primary_agent": str,
                "alternatives": List[str],
                "recommended_topology": str,
                "confidence": float
            }
        """
        if not self.config.routing_enabled:
            return {"error": "Routing disabled"}

        if not await self.ensure_initialized():
            return {"error": "Ruflo not initialized"}

        # Check if Ruflo MCP tools are available
        if not RUFLO_TOOLS_AVAILABLE:
            # Demo mode: simulate routing based on task content
            return self._route_task_demo(task, context)

        try:
            from mcp import mcp__ruflo__agentdb_route

            result = await mcp__ruflo__agentdb_route(
                task=task,
                context=context
            )

            return result
        except Exception as e:
            return {"error": str(e), "demo_fallback": True}

    def _route_task_demo(self, task: str, context: str) -> Dict[str, Any]:
        """Demo routing logic when MCP unavailable."""
        task_lower = task.lower()

        # Simple keyword-based routing for demo
        if "code" in task_lower or "write" in task_lower:
            primary = "coder"
        elif "review" in task_lower or "audit" in task_lower:
            primary = "code-reviewer"
        elif "security" in task_lower:
            primary = "security-reviewer"
        elif "test" in task_lower:
            primary = "tester"
        else:
            primary = "general-purpose"

        return {
            "primary_agent": primary,
            "alternatives": ["planner", "architect"],
            "recommended_topology": "hierarchical",
            "confidence": 0.85,
            "demo_mode": True
        }

    async def store_verdict(
        self,
        task_id: str,
        verdict: str,
        score: float,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Store a verdict in Ruflo shared memory for cross-session recall.

        Args:
            task_id: Unique task identifier
            verdict: PASS/FAIL/REWRITE
            score: Quality score (0-100)
            details: Additional metadata

        Returns:
            True if stored successfully
        """
        if not self.config.memory_enabled:
            return False

        if not await self.ensure_initialized():
            return False

        # Check if Ruflo MCP tools are available
        if not RUFLO_TOOLS_AVAILABLE:
            # Demo mode: store in local dict
            print(f"[Demo] Would store verdict for {task_id}: {verdict} (score: {score})")
            return True

        try:
            from mcp import mcp__ruflo__memory_store

            memory_key = f"verdict:{task_id}"
            memory_value = {
                "task_id": task_id,
                "verdict": verdict,
                "score": score,
                "details": details or {},
                "timestamp": __import__("time").time()
            }

            await mcp__ruflo__memory_store(
                key=memory_key,
                value=json.dumps(memory_value),
                namespace=self.config.memory_namespace
            )
            return True
        except Exception as e:
            print(f"[!] Failed to store verdict: {e}")
            return False

    async def retrieve_verdict(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a previously stored verdict."""
        if not self.config.memory_enabled:
            return None

        if not await self.ensure_initialized():
            return None

        # Check if Ruflo MCP tools are available
        if not RUFLO_TOOLS_AVAILABLE:
            # Demo mode: return None (not found in demo storage)
            print(f"[Demo] Would retrieve verdict for {task_id}")
            return None

        try:
            from mcp import mcp__ruflo__memory_retrieve

            memory_key = f"verdict:{task_id}"

            result = await mcp__ruflo__memory_retrieve(
                key=memory_key,
                namespace=self.config.memory_namespace
            )
            return json.loads(result) if result else None
        except Exception as e:
            print(f"[!] Failed to retrieve verdict: {e}")
            return None

    async def run_with_orchestration(
        self,
        task: str,
        mode: str,
        prompt: str,
        agents: List[Dict[str, Any]],
        files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run a panel with optional Ruflo orchestration.

        This method wraps the existing orchestrator behavior,
        adding Ruflo features when enabled.

        Args:
            task: Task description
            mode: Mode name from mode_registry.yaml
            prompt: User prompt
            agents: List of agent configurations
            files: Optional list of file paths to include

        Returns:
            {
                "success": bool,
                "results": List[Dict],
                "verdict": str,
                "total_score": float,
                "ruflo_metadata": Dict
            }
        """
        results = []
        scores = []
        ruflo_metadata = {}

        # 1. Optional: Route task to optimal agents
        if self.config.routing_enabled:
            route_result = await self.route_task(
                task=f"{mode}: {task}",
                context=f"Mode: {mode}, Agents: {[a.get('id') for a in agents]}"
            )
            ruflo_metadata["routing"] = route_result

        # 2. Execute using existing orchestrator logic
        # (In a real implementation, this would call the actual orchestrator)
        for agent_cfg in agents:
            agent_id = agent_cfg.get("id", "unknown")
            role = agent_cfg.get("role", "unknown")

            # 3. Optional: Store task start
            if self.config.memory_enabled and RUFLO_TOOLS_AVAILABLE:
                try:
                    from mcp import mcp__ruflo__task_create
                    task_id = f"task-{agent_id}-{mode}"
                    await mcp__ruflo__task_create(
                        type="review",
                        description=f"{mode} review by {agent_id}",
                        tags=[role, mode]
                    )
                except Exception:
                    task_id = f"task-{agent_id}-{mode}"
            else:
                task_id = f"task-{agent_id}-{mode}"

            # Simulate agent execution (replace with actual call in production)
            result = {
                "agent_id": agent_id,
                "role": role,
                "status": "completed",
                "output": f"[Simulated output from {agent_id}]",
                "score": 85.0
            }
            results.append(result)
            scores.append(result.get("score", 0))

            # 4. Optional: Store verdict
            if self.config.memory_enabled:
                verdict = "PASS" if result.get("score", 0) >= 70 else "REWRITE"
                await self.store_verdict(
                    task_id=f"task-{agent_id}-{mode}",
                    verdict=verdict,
                    score=result.get("score", 0),
                    details={"agent": agent_id, "mode": mode}
                )

        # 5. Calculate aggregate verdict
        avg_score = sum(scores) / len(scores) if scores else 0
        overall_verdict = "PASS" if avg_score >= 70 else "REWRITE"

        return {
            "success": True,
            "results": results,
            "verdict": overall_verdict,
            "total_score": avg_score,
            "ruflo_metadata": ruflo_metadata
        }

    async def get_health_status(self) -> Dict[str, Any]:
        """Get health status of Ruflo system."""
        if not self.config.health_enabled:
            return {"error": "Health monitoring disabled"}

        if not await self.ensure_initialized():
            return {"error": "Ruflo not initialized"}

        # Check if Ruflo MCP tools are available
        if not RUFLO_TOOLS_AVAILABLE:
            # Demo mode: return simulated health status
            return {
                "status": "healthy",
                "components": {
                    "mcp": {"status": "available", "demo_mode": True},
                    "memory": {"status": "available", "demo_mode": True},
                    "routing": {"status": "available", "demo_mode": True},
                    "swarm": {"status": "available", "demo_mode": True}
                },
                "timestamp": __import__("time").time(),
                "demo_mode": True
            }

        try:
            from mcp import mcp__ruflo__system_health

            return await mcp__ruflo__system_health()
        except Exception as e:
            return {"error": str(e), "demo_fallback": True}


# Convenience function for easy integration
async def run_panel_with_ruflo(
    task: str,
    mode: str,
    prompt: str,
    agents: List[Dict[str, Any]],
    files: Optional[List[str]] = None,
    ruflo_config: Optional[RufloConfig] = None
) -> Dict[str, Any]:
    """
    Convenience wrapper for run_panel with optional Ruflo orchestration.

    Args:
        task: Task description
        mode: Mode name from mode_registry.yaml
        prompt: User prompt
        agents: List of agent configurations
        files: Optional list of file paths
        ruflo_config: Optional RufloConfig (defaults to disabled)

    Returns:
        Same structure as run_with_orchestration
    """
    adapter = RufloMCPAdapter(config=ruflo_config or RufloConfig())
    return await adapter.run_with_orchestration(task, mode, prompt, agents, files)
