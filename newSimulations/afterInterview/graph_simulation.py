"""
Graph simulation that follows the afterInterview task rules.

Tasks are generated per role using a Poisson process, flow down the CXO →
Director → Manager → Player hierarchy, split at middle layers, and bubble back
up for reporting / escalation. Node-level SimLoad is combined with betweenness
centrality to expose overall risk.
"""
from __future__ import annotations

import random
from collections import defaultdict
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


def build_graph() -> nx.DiGraph:
    graph = nx.DiGraph()

    nodes = [
        ("CXO_A", "CXO"),
        ("Director_Strategy", "Director"),
        ("Director_Delivery", "Director"),
        ("Manager_Product", "Manager"),
        ("Manager_Platform", "Manager"),
        ("Manager_Field", "Manager"),
        ("Manager_Services", "Manager"),
        ("Player_A1", "Player"),
        ("Player_A2", "Player"),
        ("Player_B1", "Player"),
        ("Player_B2", "Player"),
        ("Player_C1", "Player"),
        ("Player_C2", "Player"),
        ("Player_D1", "Player"),
        ("Player_D2", "Player"),
    ]
    graph.add_nodes_from((node, {"role": role}) for node, role in nodes)

    edges = [
        ("CXO_A", "Director_Strategy"),
        ("CXO_A", "Director_Delivery"),
        ("Director_Strategy", "Manager_Product"),
        ("Director_Strategy", "Manager_Platform"),
        ("Director_Delivery", "Manager_Field"),
        ("Director_Delivery", "Manager_Services"),
        ("Manager_Product", "Player_A1"),
        ("Manager_Product", "Player_A2"),
        ("Manager_Platform", "Player_B1"),
        ("Manager_Platform", "Player_B2"),
        ("Manager_Field", "Player_C1"),
        ("Manager_Field", "Player_C2"),
        ("Manager_Services", "Player_D1"),
        ("Manager_Services", "Player_D2"),
    ]
    graph.add_edges_from(edges)

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
        self.graph = build_graph()
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

        summary: Dict[str, Dict[str, float]] = {}
        for node in self.graph.nodes():
            sim_load = self.load_tracker.get(node)
            normalized_load = sim_load / max_load if max_load else 0.0
            score = ALPHA * normalized_load + BETA * centrality.get(node, 0.0)
            summary[node] = {
                "role": self.graph.nodes[node]["role"],
                "sim_load": round(sim_load, 2),
                "centrality": round(centrality.get(node, 0.0), 3),
                "score": round(score, 3),
            }

        return summary

    def _spawn_tasks(self) -> None:
        for node in self.graph.nodes():
            role = self.graph.nodes[node]["role"]
            new_tasks, self.task_counter = self.rulebook.generate_tasks(
                node_id=node,
                role=role,
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

        if agent.state in (TaskState.CREATED, TaskState.DELEGATED):
            if children:
                if self.rulebook.should_split(role):
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
    simulation = OrganizationSimulation()
    summary = simulation.run()

    print("Node                       Role      SimLoad  Centrality  Score")
    print("-" * 65)
    for node, metrics in summary.items():
        print(
            f"{node:24s} {metrics['role']:9s} "
            f"{metrics['sim_load']:8.2f} {metrics['centrality']:10.3f} {metrics['score']:7.3f}"
        )


if __name__ == "__main__":
    main()
