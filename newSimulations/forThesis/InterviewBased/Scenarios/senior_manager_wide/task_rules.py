"""
Task rule definitions for the afterInterview simulation.

This module keeps the TaskAgent model, TaskWeight components, Poisson-based task
generation, deterministic random handling, and helper routines for delegation /
escalation logic.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Sequence, Tuple


class TaskType(str, Enum):
    TOP_DOWN = "top_down"
    DESIGN = "design"
    EXECUTION = "execution"
    INTERRUPT = "interrupt"


class TaskState(str, Enum):
    CREATED = "created"
    DELEGATED = "delegated"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    REPORTED = "reported"
    ESCALATED = "escalated"


@dataclass
class TaskWeight:
    difficulty: float
    stakeholders: float
    coordination: float
    ambiguity: float

    def total(self) -> float:
        return self.difficulty + self.stakeholders + self.coordination + self.ambiguity

    def scale(self, factor: float) -> TaskWeight:
        return TaskWeight(
            difficulty=self.difficulty * factor,
            stakeholders=self.stakeholders * factor,
            coordination=self.coordination * factor,
            ambiguity=self.ambiguity * factor,
        )


@dataclass
class TaskAgent:
    task_id: int
    task_type: TaskType
    weight: TaskWeight
    origin_node: str
    current_node: str
    state: TaskState = TaskState.CREATED
    history: List[str] = field(default_factory=list)

    def move_to(self, node: str, next_state: TaskState) -> None:
        self.current_node = node
        self.history.append(node)
        self.state = next_state


class TaskRulebook:
    LAMBDA = 2.0
    ROLE_GENERATION_PROB: Dict[str, float] = {
        "CXO": 0.20,
        "Director": 0.40,
        "Manager": 0.60,
        "Player": 0.05,
    }
    ROLE_TASK_TYPES: Dict[str, Sequence[Tuple[TaskType, float]]] = {
        "CXO": (
            (TaskType.TOP_DOWN, 0.7),
            (TaskType.DESIGN, 0.2),
            (TaskType.INTERRUPT, 0.1),
        ),
        "Director": (
            (TaskType.TOP_DOWN, 0.25),
            (TaskType.DESIGN, 0.45),
            (TaskType.EXECUTION, 0.2),
            (TaskType.INTERRUPT, 0.1),
        ),
        "Manager": (
            (TaskType.DESIGN, 0.3),
            (TaskType.EXECUTION, 0.5),
            (TaskType.INTERRUPT, 0.2),
        ),
        "Player": (
            (TaskType.EXECUTION, 0.8),
            (TaskType.INTERRUPT, 0.2),
        ),
    }

    TASK_COMPONENT_RANGES: Dict[TaskType, Dict[str, Tuple[int, int]]] = {
        TaskType.TOP_DOWN: {
            "difficulty": (6, 10),
            "stakeholders": (4, 8),
            "coordination": (4, 7),
            "ambiguity": (5, 9),
        },
        TaskType.DESIGN: {
            "difficulty": (5, 8),
            "stakeholders": (3, 6),
            "coordination": (3, 6),
            "ambiguity": (4, 7),
        },
        TaskType.EXECUTION: {
            "difficulty": (4, 7),
            "stakeholders": (1, 4),
            "coordination": (2, 4),
            "ambiguity": (1, 3),
        },
        TaskType.INTERRUPT: {
            "difficulty": (2, 5),
            "stakeholders": (0, 2),
            "coordination": (1, 3),
            "ambiguity": (2, 6),
        },
    }

    SPLIT_ELIGIBLE_ROLES = {"Director", "Manager"}
    SPLIT_COUNT = 3
    DELEGATE_RATIO = 0.6
    SPLIT_COST_FACTOR = 0.2

    ESCALATION_THRESHOLD = 30.0
    ESCALATION_PROBABILITY = 0.05

    def __init__(self, seed: int | None = None):
        self.random = random.Random(seed)

    def poisson_sample(self) -> int:
        # Knuth algorithm
        L = math.exp(-self.LAMBDA)
        k = 0
        p = 1.0
        while True:
            k += 1
            p *= self.random.random()
            if p <= L:
                break
        return k - 1

    def _sample_task_type(self, entries: Sequence[Tuple[TaskType, float]]) -> TaskType:
        total = sum(weight for _, weight in entries)
        pick = self.random.uniform(0, total)
        cumulative = 0.0
        for task_type, weight in entries:
            cumulative += weight
            if pick <= cumulative:
                return task_type
        return entries[-1][0]

    def _create_weight(self, task_type: TaskType) -> TaskWeight:
        ranges = self.TASK_COMPONENT_RANGES[task_type]
        return TaskWeight(
            difficulty=float(self.random.randint(*ranges["difficulty"])),
            stakeholders=float(self.random.randint(*ranges["stakeholders"])),
            coordination=float(self.random.randint(*ranges["coordination"])),
            ambiguity=float(self.random.randint(*ranges["ambiguity"])),
        )

    def generate_tasks(
        self,
        node_id: str,
        role: str,
        next_task_id: int,
    ) -> Tuple[List[TaskAgent], int]:
        probability = self.ROLE_GENERATION_PROB.get(role, 0.0)
        if self.random.random() > probability:
            return [], next_task_id

        task_types = self.ROLE_TASK_TYPES.get(role)
        if not task_types:
            return [], next_task_id

        task_count = self.poisson_sample()
        if task_count == 0:
            return [], next_task_id

        tasks: List[TaskAgent] = []
        for _ in range(task_count):
            task_type = self._sample_task_type(task_types)
            weight = self._create_weight(task_type)
            agent = TaskAgent(
                task_id=next_task_id,
                task_type=task_type,
                weight=weight,
                origin_node=node_id,
                current_node=node_id,
                state=TaskState.CREATED,
                history=[node_id],
            )
            tasks.append(agent)
            next_task_id += 1

        return tasks, next_task_id

    def should_split(self, role: str) -> bool:
        return role in self.SPLIT_ELIGIBLE_ROLES

    def split_task(self, agent: TaskAgent, next_task_id: int) -> Tuple[List[TaskAgent], int]:
        delegated_fraction = self.DELEGATE_RATIO / self.SPLIT_COUNT
        subtasks: List[TaskAgent] = []
        for _ in range(self.SPLIT_COUNT):
            new_weight = agent.weight.scale(delegated_fraction)
            new_agent = TaskAgent(
                task_id=next_task_id,
                task_type=agent.task_type,
                weight=new_weight,
                origin_node=agent.origin_node,
                current_node=agent.current_node,
                state=TaskState.DELEGATED,
                history=list(agent.history),
            )
            subtasks.append(new_agent)
            next_task_id += 1

        agent.weight = agent.weight.scale(1.0 - self.DELEGATE_RATIO)
        return subtasks, next_task_id

    def should_escalate(self, weight_total: float) -> bool:
        if weight_total >= self.ESCALATION_THRESHOLD:
            return True
        return self.random.random() < self.ESCALATION_PROBABILITY

    def select_next_node(self, candidates: List[str], node_loads: Dict[str, float]) -> str:
        if not candidates:
            raise ValueError("No candidates provided")

        if self.random.random() < 0.6:
            # pick lowest current load
            target = min(candidates, key=lambda node: node_loads.get(node, 0.0))
            return target

        return self.random.choice(candidates)
