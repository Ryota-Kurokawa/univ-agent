"""
Baseline load profile simulation.

The script models a simple CXO -> Director -> Manager -> Player hierarchy and
tracks the total workload each role experiences while tasks flow down the
organization and completion reports travel upward.
"""
from __future__ import annotations

import random
import statistics
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

# Simulation knobs
RANDOM_SEED = 42
TIME_STEPS = 200
TASKS_PER_CXO = (1, 3)  # inclusive min/max
SENDER_COST_FACTOR = 0.3
ESCALATION_RATE = 0.05  # Manager -> Director escalation probability

# Organizational structure definition
NODES = [
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

NODE_ORDER = [node for node, _ in NODES]
ROLE_BY_NODE = {node: role for node, role in NODES}
ROLE_DEPTH = {"CXO": 0, "Director": 1, "Manager": 2, "Player": 3}

# Adjacency matrix with downward (execution) and upward (reporting) edges
ADJACENCY_MATRIX = [
    # CXO, DirS, DirD, MProd, MPlat, MField, MServ, P_A1, P_A2, P_B1, P_B2, P_C1, P_C2, P_D1, P_D2
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # CXO_A
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Director_Strategy
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Director_Delivery
    [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # Manager_Product
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # Manager_Platform
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],  # Manager_Field
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # Manager_Services
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Player_A1
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Player_A2
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Player_B1
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Player_B2
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Player_C1
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Player_C2
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Player_D1
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Player_D2
]


@dataclass
class Task:
    task_id: int
    weight: float
    phase: str  # "down" or "report"


class LoadTracker:
    def __init__(self, nodes: List[str]):
        self.load: Dict[str, float] = defaultdict(float)
        self.nodes = nodes

    def record_transfer(self, sender: str, receiver: str, weight: float) -> None:
        self.load[sender] += SENDER_COST_FACTOR * weight
        self.load[receiver] += weight

    def get_node_loads(self) -> Dict[str, float]:
        return {node: self.load.get(node, 0.0) for node in self.nodes}


def build_adjacency() -> Dict[str, List[str]]:
    adjacency: Dict[str, List[str]] = {node: [] for node in NODE_ORDER}
    for row_idx, row in enumerate(ADJACENCY_MATRIX):
        for col_idx, value in enumerate(row):
            if value:
                adjacency[NODE_ORDER[row_idx]].append(NODE_ORDER[col_idx])
    return adjacency


def split_neighbours(adjacency: Dict[str, List[str]]) -> tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    downward = defaultdict(list)
    upward = defaultdict(list)

    for node, neighbours in adjacency.items():
        for neighbour in neighbours:
            if ROLE_DEPTH[ROLE_BY_NODE[node]] < ROLE_DEPTH[ROLE_BY_NODE[neighbour]]:
                downward[node].append(neighbour)
            elif ROLE_DEPTH[ROLE_BY_NODE[node]] > ROLE_DEPTH[ROLE_BY_NODE[neighbour]]:
                upward[node].append(neighbour)

    return downward, upward


def generate_task(task_id: int) -> Task:
    difficulty = random.randint(3, 10)
    stakeholders = random.randint(1, 5)
    coordination = random.randint(0, 3)

    weight = (
        difficulty * 1.2
        + stakeholders * 0.8
        + coordination * 0.5
    )

    return Task(task_id=task_id, weight=weight, phase="down")


def process_task_queues(
    task_queues: Dict[str, List[Task]],
    downward: Dict[str, List[str]],
    upward: Dict[str, List[str]],
    load_tracker: LoadTracker,
) -> None:
    for node in NODE_ORDER:
        queue = task_queues[node]
        if not queue:
            continue

        task_queues[node] = []
        role = ROLE_BY_NODE[node]

        for task in queue:
            if task.phase == "down":
                children = downward.get(node, [])
                if not children or role == "Player":
                    task.phase = "report"
                    parents = upward.get(node, [])
                    if parents:
                        target = random.choice(parents)
                        load_tracker.record_transfer(node, target, task.weight)
                        task_queues[target].append(task)
                    continue

                target = random.choice(children)
                load_tracker.record_transfer(node, target, task.weight)
                task_queues[target].append(task)
            else:
                if role == "Manager":
                    parents = upward.get(node, [])
                    if parents and random.random() < ESCALATION_RATE:
                        target = random.choice(parents)
                        load_tracker.record_transfer(node, target, task.weight)
                        task_queues[target].append(task)
                elif role in {"Director", "CXO"}:
                    continue


def run_simulation() -> tuple[Dict[str, float], Dict[str, Dict[str, float]]]:
    random.seed(RANDOM_SEED)

    adjacency = build_adjacency()
    downward, upward = split_neighbours(adjacency)
    load_tracker = LoadTracker(NODE_ORDER)

    task_queues: Dict[str, List[Task]] = {node: [] for node in NODE_ORDER}
    cxo_nodes = [node for node, role in NODES if role == "CXO"]
    task_counter = 0

    for _ in range(TIME_STEPS):
        # Generate new work at the top
        for cxo in cxo_nodes:
            new_tasks = random.randint(*TASKS_PER_CXO)
            for _ in range(new_tasks):
                task_queues[cxo].append(generate_task(task_counter))
                task_counter += 1

        process_task_queues(task_queues, downward, upward, load_tracker)

    # Flush any in-flight work after the time horizon
    while any(task_queues[node] for node in NODE_ORDER):
        process_task_queues(task_queues, downward, upward, load_tracker)

    node_loads = load_tracker.get_node_loads()
    role_stats: Dict[str, Dict[str, float]] = {}

    for role in ("CXO", "Director", "Manager", "Player"):
        role_nodes = [node for node, node_role in NODES if node_role == role]
        loads = [node_loads.get(node, 0.0) for node in role_nodes]
        if not loads:
            continue
        role_stats[role] = {
            "average": round(statistics.mean(loads), 2),
            "variance": round(statistics.pvariance(loads), 2),
        }

    return node_loads, role_stats


def render_bar(value: float, max_value: float, width: int = 32) -> str:
    if max_value <= 0:
        return ""
    filled = int(round((value / max_value) * width))
    filled = min(width, max(filled, 0))
    return "#" * filled + "-" * (width - filled)


def main() -> None:
    node_loads, role_stats = run_simulation()

    print("=== Total load per node ===")
    sorted_nodes = sorted(
        node_loads.items(),
        key=lambda item: (ROLE_DEPTH[ROLE_BY_NODE[item[0]]], NODE_ORDER.index(item[0])),
    )
    max_node_load = max((load for _, load in sorted_nodes), default=0.0)

    for node, load_value in sorted_nodes:
        bar = render_bar(load_value, max_node_load)
        print(f"{node:20s} {load_value:8.2f} |{bar}|")

    print("\n=== Role-level averages ===")
    max_role_avg = max((role_stats[role]["average"] for role in ("CXO", "Director", "Manager", "Player") if role in role_stats), default=0.0)
    for role in ("CXO", "Director", "Manager", "Player"):
        stats = role_stats.get(role)
        if not stats:
            continue
        bar = render_bar(stats["average"], max_role_avg)
        print(
            f"{role:8s} avg={stats['average']:6.2f} var={stats['variance']:7.2f} |{bar}|"
        )


if __name__ == "__main__":
    main()
