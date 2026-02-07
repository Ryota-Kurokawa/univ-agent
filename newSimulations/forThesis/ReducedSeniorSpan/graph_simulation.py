"""
ReducedSeniorSpan Scenario - Strategy to reduce SeniorManager load.

This scenario reduces the management span of SeniorManagers (3-5 children)
while increasing Manager child counts (8-12) to distribute workload more evenly.
The goal is to minimize reporting bottlenecks at the SeniorManager level.
"""
from __future__ import annotations

import random
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List

import networkx as nx

from newSimulations.afterInterview.task_rules import (
    TaskAgent,
    TaskRulebook,
    TaskState,
)

TIME_STEPS = 2000
SENDER_COST_FACTOR = 0.3
REPORT_RECEIVER_FACTOR = 0.1
ALPHA = 0.7
BETA = 0.3
ROLE_SEQUENCE = ["CXO", "Director", "SeniorManager", "Manager", "Player"]
CHILD_RANGES = {
    "CXO": (15, 20),
    "Director": (10, 15),
    "SeniorManager": (3, 5),    # ★ Reduced management span
    "Manager": (8, 12),          # ★ Increased to compensate
    "Player": (0, 0),
}


def build_graph(seed: int | None = None) -> nx.DiGraph:
    rng = random.Random(seed)
    graph = nx.DiGraph()

    root = "CXO_0"
    graph.add_node(root, role="CXO")

    queue: deque[tuple[str, str]] = deque()
    queue.append((root, "CXO"))

    global_index = 1

    while queue:
        parent, role = queue.popleft()
        role_index = ROLE_SEQUENCE.index(role)
        if role_index >= len(ROLE_SEQUENCE) - 1:
            continue

        child_role = ROLE_SEQUENCE[role_index + 1]
        min_children, max_children = CHILD_RANGES.get(role, (0, 0))

        if max_children == 0:
            continue

        child_count = rng.randint(min_children, max_children)

        new_children = []
        for _ in range(child_count):
            node_name = f"{child_role}_{global_index}"
            global_index += 1
            graph.add_node(node_name, role=child_role)
            graph.add_edge(parent, node_name)
            new_children.append((node_name, child_role))
        if child_role != "Player":
            queue.extend(new_children)

    return graph


class LoadTracker:
    def __init__(self):
        self.values: Dict[str, float] = defaultdict(float)

    def add(self, node: str, amount: float) -> None:
        self.values[node] += amount

    def get(self, node: str) -> float:
        return self.values.get(node, 0.0)


class OrganizationSimulation:
    def __init__(self, steps: int = TIME_STEPS, seed: int = 42):
        self.graph = build_graph(seed)
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
        self.task_counts: Dict[str, int] = defaultdict(int)
        self.task_counter = 0
        self.completed_tasks = 0

    def run(self) -> Dict[str, Dict[str, float]]:
        for _ in range(self.steps):
            self._spawn_tasks()
            self._process_step()

        degree_centrality = nx.degree_centrality(self.graph)
        max_load = max(self.load_tracker.values.values()) if self.load_tracker.values else 1.0

        summary: Dict[str, Dict[str, float]] = {}
        for node in self.graph.nodes():
            sim_load = self.load_tracker.get(node)
            normalized_load = sim_load / max_load if max_load else 0.0
            score = ALPHA * normalized_load + BETA * degree_centrality.get(node, 0.0)
            summary[node] = {
                "role": self.graph.nodes[node]["role"],
                "sim_load": round(sim_load, 2),
                "degree": round(degree_centrality.get(node, 0.0), 5),
                "tasks": self.task_counts.get(node, 0),
                "children": len(self.children[node]),
                "score": round(score, 5),
            }

        return summary

    def _spawn_tasks(self) -> None:
        for node in self.graph.nodes():
            role = self.graph.nodes[node]["role"]
            rule_role = self._map_role_for_rules(role)
            new_tasks, self.task_counter = self.rulebook.generate_tasks(
                node_id=node,
                role=rule_role,
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
            rule_role = self._map_role_for_rules(role)
            for agent in queue:
                self._advance_agent(agent, node, role, rule_role, next_queues)

        self.current_queues = next_queues

    def _advance_agent(
        self,
        agent: TaskAgent,
        node: str,
        role: str,
        rule_role: str,
        next_queues: Dict[str, List[TaskAgent]],
    ) -> None:
        children = self.children[node]
        parents = self.parents[node]

        if agent.state in (TaskState.CREATED, TaskState.DELEGATED):
            if children:
                if self.rulebook.should_split(rule_role):
                    self._split_to_all_children(agent, node, children, next_queues)
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
        self.task_counts[node] += 1

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
        self.task_counts[target] += 1

    def _split_to_all_children(
        self,
        agent: TaskAgent,
        node: str,
        children: List[str],
        next_queues: Dict[str, List[TaskAgent]],
    ) -> None:
        if not children:
            return

        original_weight = agent.weight.total()
        self.load_tracker.add(node, self.rulebook.SPLIT_COST_FACTOR * original_weight)

        shares = self._compute_child_shares(children)
        for child, share in shares.items():
            new_weight = agent.weight.scale(share)
            new_agent = TaskAgent(
                task_id=self.task_counter,
                task_type=agent.task_type,
                weight=new_weight,
                origin_node=agent.origin_node,
                current_node=node,
                state=TaskState.DELEGATED,
                history=list(agent.history),
            )
            self.task_counter += 1
            self._enqueue_next_step(
                target=child,
                agent=new_agent,
                next_state=TaskState.DELEGATED,
                receiver_factor=1.0,
                sender=node,
                sender_factor=SENDER_COST_FACTOR,
                next_queues=next_queues,
            )

    def _compute_child_shares(self, children: List[str]) -> Dict[str, float]:
        values: Dict[str, float] = {}
        for child in children:
            grand_children = self.children.get(child, [])
            values[child] = 1.0 + 0.5 * len(grand_children)

        total = sum(values.values())
        if total <= 0:
            equal_share = 1.0 / len(children)
            return {child: equal_share for child in children}

        return {child: value / total for child, value in values.items()}

    def _map_role_for_rules(self, role: str) -> str:
        if role == "SeniorManager":
            return "Manager"
        return role


def main() -> None:
    simulation = OrganizationSimulation()
    summary = simulation.run()

    role_totals: Dict[str, Dict[str, float]] = defaultdict(lambda: {"sum": 0.0, "count": 0, "tasks": 0.0})
    for metrics in summary.values():
        role = metrics["role"]
        role_totals[role]["sum"] += metrics["sim_load"]
        role_totals[role]["count"] += 1
        role_totals[role]["tasks"] += metrics["tasks"]

    role_order = ["CXO", "Director", "SeniorManager", "Manager", "Player"]
    sorted_roles = [role for role in role_order if role in role_totals] + [
        role for role in role_totals.keys() if role not in role_order
    ]
    sorted_items = sorted(
        summary.items(),
        key=lambda item: (
            sorted_roles.index(item[1]["role"]) if item[1]["role"] in sorted_roles else len(sorted_roles),
            -item[1]["sim_load"],
        ),
    )

    result_path = Path(__file__).with_name("RESULT.md")
    lines = [
        "# After Review Simulation Result",
        "",
        f"Total nodes: {len(summary)}",
        "",
        "## Role Averages",
        "",
        "| Role | Nodes | Avg Tasks | Avg SimLoad |",
        "| --- | ---: | ---: | ---: |",
    ]
    for role in sorted_roles:
        stats = role_totals.get(role)
        if not stats:
            continue
        avg_load = stats["sum"] / stats["count"] if stats["count"] else 0.0
        avg_tasks = stats["tasks"] / stats["count"] if stats["count"] else 0.0
        lines.append(f"| {role} | {int(stats['count'])} | {avg_tasks:.2f} | {avg_load:.2f} |")


    lines.extend([
        "",
        "## Node Details",
        "",
        "| Node | Role | Tasks | Children | SimLoad | DegreeCentrality | Score |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ])

    for node, metrics in sorted_items:
        lines.append(
            f"| {node} | {metrics['role']} | {metrics['tasks']} | {metrics['children']} | "
            f"{metrics['sim_load']:.2f} | {metrics['degree']:.5f} | {metrics['score']:.5f} |"
        )

    result_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
