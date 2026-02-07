"""
Inspect a specific node's metrics and connections based on RESULT.md.

Usage examples:
    python inspect_node.py --node SeniorManager_205
    python inspect_node.py --node Manager_2026 --seed 42

The script rebuilds the org graph using graph_simulation.build_graph (seed default 42),
parses RESULT.md for node metrics, and prints parents/children lists.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

from graph_simulation import build_graph, ROLE_SEQUENCE

RESULT_PATH = Path(__file__).with_name("RESULT.md")


def load_metrics(path: Path) -> Dict[str, Dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.startswith("| Node "):
            start = idx + 2
            break
    if start is None:
        raise SystemExit("Node table not found in RESULT.md")

    metrics: Dict[str, Dict[str, str]] = {}
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        parts = [p.strip() for p in line.strip("|").split("|")]
        metrics[parts[0]] = {
            "role": parts[1],
            "tasks": parts[2],
            "children": parts[3],
            "simload": parts[4],
            "degree": parts[5],
            "score": parts[6],
        }
    return metrics


def inspect(node_id: str, seed: int) -> None:
    metrics = load_metrics(RESULT_PATH)
    node_info = metrics.get(node_id)
    if not node_info:
        raise SystemExit(f"{node_id} was not found in RESULT.md")

    graph = build_graph(seed=seed)
    if node_id not in graph:
        raise SystemExit(f"{node_id} does not exist in generated graph. Check the seed.")

    parents = list(graph.predecessors(node_id))
    children = list(graph.successors(node_id))

    print(f"Node: {node_id}")
    print(f"Role: {node_info['role']}")
    print(f"Tasks processed: {node_info['tasks']}")
    print(f"SimLoad: {node_info['simload']}")
    print(f"Score: {node_info['score']}")
    print(f"Degree centrality: {node_info['degree']}")
    print(f"Child count (RESULT): {node_info['children']}")
    print()
    print(f"Parents ({len(parents)}): {', '.join(parents) if parents else 'None'}")
    print(f"Children ({len(children)}):")
    for child in children:
        child_metrics = metrics.get(child)
        summary = ""
        if child_metrics:
            summary = f" (role={child_metrics['role']}, tasks={child_metrics['tasks']}, simload={child_metrics['simload']})"
        print(f"  - {child}{summary}")


def main() -> None:
    parser = argparse.ArgumentParser(description="RESULT.md とグラフ構造からノード詳細を表示します。")
    parser.add_argument("--node", required=True, help="調査対象ノードID (例: SeniorManager_205)")
    parser.add_argument("--seed", type=int, default=42, help="build_graph の乱数シード")
    args = parser.parse_args()
    inspect(args.node, args.seed)


if __name__ == "__main__":
    main()
