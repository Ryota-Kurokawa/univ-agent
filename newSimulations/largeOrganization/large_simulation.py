"""
Large-organization task simulation with ~1000 nodes.

Builds a multi-level hierarchy using the afterInterview task rules and
executes a single simulation run to highlight load concentration.
"""
from __future__ import annotations

import random
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import networkx as nx

from newSimulations.afterInterview.task_rules import TaskAgent, TaskRulebook, TaskState

TARGET_NODES = 1000
TIME_STEPS = 1500
SENDER_COST_FACTOR = 0.3
REPORT_RECEIVER_FACTOR = 0.1
ALPHA = 0.7
BETA = 0.3

ROLE_SEQUENCE = [
    "CXO",
    "Executive",
    "Director",
    "SeniorManager",
    "Manager",
    "Player",
]

TOP_LEVEL_WIDTH = {
    1: (10, 20),  # Executives
    2: (10, 20),  # Directors
    3: (10, 20),  # Senior Managers
}


def determine_level_counts(target_nodes: int, rng: random.Random) -> List[int]:
    counts = [1]  # CXO

    # Depth 1-3: keep each layer around 10-20 nodes
    for depth in range(1, 4):
        low, high = TOP_LEVEL_WIDTH[depth]
        counts.append(rng.randint(low, high))

    remaining = target_nodes - sum(counts)
    if remaining <= 0:
        raise ValueError("Target nodes must exceed top-level allocation")

    avg_players = rng.randint(4, 6)
    manager_count = max(1, remaining // (avg_players + 1))
    player_count = remaining - manager_count
    if player_count <= 0:
        player_count = 1
        manager_count = max(1, remaining - player_count)

    counts.append(manager_count)
    counts.append(player_count)
    return counts


def build_large_graph(target_nodes: int = TARGET_NODES, seed: int | None = None) -> nx.DiGraph:
    rng = random.Random(seed)
    graph = nx.DiGraph()
    level_counts = determine_level_counts(target_nodes, rng)
    level_nodes: List[List[str]] = []
    node_index = 0

    for depth, count in enumerate(level_counts):
        nodes: List[str] = []
        for _ in range(count):
            node_name = f"N{node_index:04d}"
            node_index += 1
            role = ROLE_SEQUENCE[min(depth, len(ROLE_SEQUENCE) - 1)]
            graph.add_node(node_name, role=role)
            nodes.append(node_name)
        level_nodes.append(nodes)

    for depth in range(len(level_nodes) - 1):
        parents = level_nodes[depth]
        children = level_nodes[depth + 1]
        if not parents or not children:
            continue
        for idx, child in enumerate(children):
            parent = parents[idx % len(parents)]
            graph.add_edge(parent, child)

    return graph


class LoadTracker:
    def __init__(self):
        self.values: Dict[str, float] = defaultdict(float)

    def add(self, node: str, amount: float) -> None:
        self.values[node] += amount

    def get(self, node: str) -> float:
        return self.values.get(node, 0.0)


class LargeOrganizationSimulation:
    def __init__(self, steps: int = TIME_STEPS, seed: int = 2024):
        self.graph = build_large_graph(seed=seed)
        self.rulebook = TaskRulebook(seed=seed)
        self.random = random.Random(seed)
        self.steps = steps

        self.parents: Dict[str, List[str]] = {
            node: list(self.graph.predecessors(node)) for node in self.graph.nodes()
        }
        self.children: Dict[str, List[str]] = {
            node: list(self.graph.successors(node)) for node in self.graph.nodes()
        }

        self.current_queues: Dict[str, List[TaskAgent]] = {node: [] for node in self.graph.nodes()}
        self.load_tracker = LoadTracker()
        self.task_counter = 0
        self.completed_tasks = 0

    def run(self) -> Dict[str, Dict[str, float]]:
        for _ in range(self.steps):
            self._spawn_tasks()
            self._process_step()

        centrality = nx.betweenness_centrality(self.graph, normalized=True)
        max_load = max(self.load_tracker.values.values()) if self.load_tracker.values else 1.0

        results: Dict[str, Dict[str, float]] = {}
        for node in self.graph.nodes():
            sim_load = self.load_tracker.get(node)
            normalized = sim_load / max_load if max_load else 0.0
            score = ALPHA * normalized + BETA * centrality.get(node, 0.0)
            results[node] = {
                "role": self.graph.nodes[node]["role"],
                "sim_load": round(sim_load, 2),
                "centrality": round(centrality.get(node, 0.0), 4),
                "score": round(score, 4),
            }

        return results

    def _spawn_tasks(self) -> None:
        for node in self.graph.nodes():
            role = self.graph.nodes[node]["role"]
            new_tasks, self.task_counter = self.rulebook.generate_tasks(
                node_id=node,
                role=role if role in TaskRulebook.ROLE_TASK_TYPES else "Player",
                next_task_id=self.task_counter,
            )
            for task in new_tasks:
                task.move_to(node, TaskState.CREATED)
                self._receive_now(node, task)

    def _process_step(self) -> None:
        next_queues: Dict[str, List[TaskAgent]] = {node: [] for node in self.graph.nodes()}

        for node in self.graph.nodes():
            queue = self.current_queues[node]
            if not queue:
                continue

            role = self.graph.nodes[node]["role"]
            for agent in queue:
                self._advance_agent(agent, node, role, next_queues)

        self.current_queues = next_queues

    def _advance_agent(
        self,
        agent: TaskAgent,
        node: str,
        role: str,
        next_queues: Dict[str, List[TaskAgent]],
    ) -> None:
        children = self.children[node]
        parents = self.parents[node]

        role_for_rules = role if role in TaskRulebook.ROLE_TASK_TYPES else "Player"

        if agent.state in (TaskState.CREATED, TaskState.DELEGATED):
            if children:
                if self.rulebook.should_split(role_for_rules):
                    original_weight = agent.weight.total()
                    subtasks, self.task_counter = self.rulebook.split_task(agent, self.task_counter)
                    self.load_tracker.add(node, self.rulebook.SPLIT_COST_FACTOR * original_weight)
                    for subtask in subtasks:
                        target = self.rulebook.select_next_node(children, self.load_tracker.values)
                        self._enqueue_next_step(
                            target=target,
                            agent=subtask,
                            next_state=TaskState.DELEGATED,
                            receiver_factor=1.0,
                            sender=node,
                            sender_factor=SENDER_COST_FACTOR,
                            next_queues=next_queues,
                        )
                    if agent.weight.total() <= 0.01:
                        return
                else:
                    target = self.rulebook.select_next_node(children, self.load_tracker.values)
                    self._enqueue_next_step(
                        target=target,
                        agent=agent,
                        next_state=TaskState.DELEGATED,
                        receiver_factor=1.0,
                        sender=node,
                        sender_factor=SENDER_COST_FACTOR,
                        next_queues=next_queues,
                    )
                    return
            agent.move_to(node, TaskState.IN_PROGRESS)

        if agent.state == TaskState.IN_PROGRESS:
            agent.move_to(node, TaskState.DONE)

        if agent.state == TaskState.DONE:
            if parents:
                target = self.rulebook.select_next_node(parents, self.load_tracker.values)
                self._enqueue_next_step(
                    target=target,
                    agent=agent,
                    next_state=TaskState.REPORTED,
                    receiver_factor=REPORT_RECEIVER_FACTOR,
                    sender=None,
                    sender_factor=0.0,
                    next_queues=next_queues,
                )
            else:
                self.completed_tasks += 1
            return

        if agent.state == TaskState.REPORTED:
            if parents and self.rulebook.should_escalate(agent.weight.total()):
                target = self.rulebook.select_next_node(parents, self.load_tracker.values)
                self._enqueue_next_step(
                    target=target,
                    agent=agent,
                    next_state=TaskState.ESCALATED,
                    receiver_factor=1.0,
                    sender=node,
                    sender_factor=SENDER_COST_FACTOR,
                    next_queues=next_queues,
                )
            else:
                self.completed_tasks += 1
            return

        if agent.state == TaskState.ESCALATED:
            if parents and self.rulebook.should_escalate(agent.weight.total()):
                target = self.rulebook.select_next_node(parents, self.load_tracker.values)
                self._enqueue_next_step(
                    target=target,
                    agent=agent,
                    next_state=TaskState.ESCALATED,
                    receiver_factor=1.0,
                    sender=node,
                    sender_factor=SENDER_COST_FACTOR,
                    next_queues=next_queues,
                )
            else:
                self.completed_tasks += 1

    def _receive_now(self, node: str, agent: TaskAgent) -> None:
        self.current_queues[node].append(agent)
        self.load_tracker.add(node, agent.weight.total())

    def _enqueue_next_step(
        self,
        target: str,
        agent: TaskAgent,
        next_state: TaskState,
        receiver_factor: float,
        sender: str | None,
        sender_factor: float,
        next_queues: Dict[str, List[TaskAgent]],
    ) -> None:
        agent.move_to(target, next_state)
        next_queues[target].append(agent)
        self.load_tracker.add(target, receiver_factor * agent.weight.total())
        if sender is not None and sender_factor > 0:
            self.load_tracker.add(sender, sender_factor * agent.weight.total())


def main() -> None:
    simulation = LargeOrganizationSimulation()
    summary = simulation.run()

    print("Node       Role            SimLoad    Centrality    Score")
    print("-" * 70)
    sample_nodes = list(summary.items())[:30]
    for node, metrics in sample_nodes:
        print(
            f"{node:8s} {metrics['role']:15s} "
            f"{metrics['sim_load']:10.2f} {metrics['centrality']:8.4f} {metrics['score']:7.4f}"
        )
    print(f"... total nodes: {len(summary)} (showing first 30)")

    result_path = Path(__file__).with_name("RESULT.md")
    role_totals: Dict[str, Dict[str, float]] = defaultdict(lambda: {"sum": 0.0, "count": 0})
    for metrics in summary.values():
        role = metrics["role"]
        role_totals[role]["sum"] += metrics["sim_load"]
        role_totals[role]["count"] += 1

    role_order = sorted(role_totals.keys(), key=lambda role: ROLE_SEQUENCE.index(role) if role in ROLE_SEQUENCE else len(ROLE_SEQUENCE))
    sorted_items = sorted(
        summary.items(),
        key=lambda item: (role_order.index(item[1]["role"]), -item[1]["sim_load"]),
    )

    lines = [
        "# Large Organization Simulation Result",
        "",
        f"Total nodes: {len(summary)}",
        "",
        "## Role Averages",
        "",
        "| Role | Nodes | Avg SimLoad |",
        "| --- | ---: | ---: |",
    ]
    for role in role_order:
        stats = role_totals[role]
        avg = stats["sum"] / stats["count"] if stats["count"] else 0.0
        lines.append(f"| {role} | {int(stats['count'])} | {avg:.2f} |")

    lines.extend([
        "",
        "## Node Details",
        "",
        "| Node | Role | SimLoad | Centrality | Score |",
        "| --- | --- | ---: | ---: | ---: |",
    ])
    for node, metrics in sorted_items:
        lines.append(
            f"| {node} | {metrics['role']} | {metrics['sim_load']:.2f} | "
            f"{metrics['centrality']:.4f} | {metrics['score']:.4f} |"
        )

    result_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote full table to {result_path}")


if __name__ == "__main__":
    main()
