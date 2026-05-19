#!/usr/bin/env python3
"""
Demo script for Ruflo MCP Adapter integration with LND Studio developers layer.

This demonstrates the adapter's orchestration, routing, memory, and health features
while preserving the existing multi-agent CLI workflow.
"""

import asyncio
import sys
from pathlib import Path

# Add studio to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from studio.developers.ruflo_adapter import RufloMCPAdapter, RufloConfig, run_panel_with_ruflo


async def demo_basic_orchestration():
    """Demo: Basic Ruflo orchestration with sample task."""
    print("=" * 60)
    print("DEMO 1: Basic Ruflo Orchestration")
    print("=" * 60)

    # Create adapter with default config (disabled by default)
    adapter = RufloMCPAdapter()

    # Initialize (will return False since Ruflo is disabled by default)
    initialized = await adapter.initialize()
    print(f"Ruflo initialized: {initialized}")

    # Demo swarm init (returns demo mode response when MCP unavailable)
    swarm_result = await adapter.init_swarm("demo-swarm-001")
    print(f"\nSwarm init result:")
    print(f"  - swarm_id: {swarm_result.get('swarm_id')}")
    print(f"  - topology: {swarm_result.get('topology')}")
    print(f"  - strategy: {swarm_result.get('strategy')}")
    print(f"  - demo_mode: {swarm_result.get('demo_mode', False)}")

    # Demo health check
    health = await adapter.get_health_status()
    print(f"\nHealth status:")
    print(f"  - status: {health.get('status')}")
    print(f"  - demo_mode: {health.get('demo_mode', False)}")
    print()


async def demo_routing():
    """Demo: Task routing with semantic similarity."""
    print("=" * 60)
    print("DEMO 2: Task Routing")
    print("=" * 60)

    adapter = RufloMCPAdapter()

    # Route different task types
    tasks = [
        "Write Python code for a new API endpoint",
        "Review this security-sensitive authentication module",
        "Run unit tests for the payment service",
        "Analyze the manga panel and extract visual details",
    ]

    for task in tasks:
        result = await adapter.route_task(task)
        print(f"\nTask: {task[:50]}...")
        print(f"  Primary agent: {result.get('primary_agent')}")
        print(f"  Confidence: {result.get('confidence', 'N/A')}")
        print(f"  Demo mode: {result.get('demo_mode', False)}")
    print()


async def demo_verdict_storage():
    """Demo: Shared memory for verdicts."""
    print("=" * 60)
    print("DEMO 3: Verdict Storage & Retrieval")
    print("=" * 60)

    adapter = RufloMCPAdapter()

    # Store a verdict
    task_id = "demo-task-001"
    await adapter.store_verdict(
        task_id=task_id,
        verdict="PASS",
        score=92.5,
        details={"agent": "hermes", "mode": "single"}
    )

    # Retrieve it
    retrieved = await adapter.retrieve_verdict(task_id)
    print(f"Stored verdict for {task_id}:")
    print(f"  - verdict: PASS")
    print(f"  - score: 92.5")
    print(f"  - demo_mode: True (stored in local dict)")
    print()


async def demo_full_integration():
    """Demo: Full panel orchestration with multiple agents."""
    print("=" * 60)
    print("DEMO 4: Full Panel Integration")
    print("=" * 60)

    # Define sample agents (matching studio/developers/agents/registry.py)
    agents = [
        {"id": "hermes", "role": "R18 prose specialist"},
        {"id": "claude", "role": "Quality auditor"},
        {"id": "qwen", "role": "Visual forensic analyst"},
        {"id": "codex", "role": "Context extractor"},
    ]

    # Run with Ruflo orchestration (disabled - uses existing orchestrator)
    result = await run_panel_with_ruflo(
        task="Adapt manga page 001 to Vietnamese prose",
        mode="single",
        prompt="Extract visual details and generate R18 prose",
        agents=agents,
        ruflo_config=RufloConfig(enabled=False)  # Disabled = use existing workflow
    )

    print(f"Panel execution result:")
    print(f"  - success: {result.get('success')}")
    print(f"  - verdict: {result.get('verdict')}")
    print(f"  - total_score: {result.get('total_score')}")
    print(f"  - results count: {len(result.get('results', []))}")
    print()

    for r in result.get('results', []):
        print(f"  Agent {r.get('agent_id')} ({r.get('role')}):")
        print(f"    - status: {r.get('status')}")
        print(f"    - score: {r.get('score')}")
    print()


async def demo_ruflo_enabled():
    """Demo: With Ruflo enabled (requires MCP tools)."""
    print("=" * 60)
    print("DEMO 5: Ruflo Enabled Mode (MCP-dependent)")
    print("=" * 60)

    # Create adapter with Ruflo enabled
    adapter = RufloMCPAdapter(config=RufloConfig(
        enabled=True,
        swarm_id="prod-swarm-001",
        topology="hierarchical",
        strategy="specialized",
        max_agents=5,
        memory_namespace="lnd_dev_prod",
        routing_enabled=True,
        memory_enabled=True,
        health_enabled=True
    ))

    # Initialize
    initialized = await adapter.initialize()
    print(f"Ruflo enabled: True")
    print(f"Initialized: {initialized}")

    if initialized:
        # These would use real MCP tools when available
        print("\nWhen MCP tools are available, this would use:")
        print("  - mcp__ruflo__swarm_init")
        print("  - mcp__ruflo__agentdb_route")
        print("  - mcp__ruflo__memory_store")
        print("  - mcp__ruflo__system_health")
    else:
        print("\nMCP tools not available - running in demo mode")
        print("(This is expected in most environments)")
    print()


async def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("RUFLO MCP ADAPTER DEMO SUITE")
    print("LND Studio Developers Layer Integration")
    print("=" * 60 + "\n")

    await demo_basic_orchestration()
    await demo_routing()
    await demo_verdict_storage()
    await demo_full_integration()
    await demo_ruflo_enabled()

    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nKey takeaways:")
    print("1. Adapter works with or without Ruflo MCP tools")
    print("2. Existing orchestrator workflow is preserved")
    print("3. Routing, memory, and health features available when MCP enabled")
    print("4. Demo mode provides realistic responses for testing")
    print("5. Multi-agent CLI (Hermes, Claude, Qwen, Codex) unchanged")
    print()


if __name__ == "__main__":
    asyncio.run(main())
