"""
Generate a visual organization chart for the baseline strategy hierarchy.

Uses NetworkX + Matplotlib to draw the CXO -> Director -> Manager -> Player
structure and saves it as PNG under the same directory.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import networkx as nx

try:
    import matplotlib.pyplot as plt
except ImportError as exc:  # pragma: no cover - graceful failure message
    raise SystemExit(
        "matplotlib が見つかりません。`pip install matplotlib` を実行してから再度試してください。"
    ) from exc

NODES: List[Tuple[str, str]] = [
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

EDGES = [
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

ROLE_LEVEL = {"CXO": 0, "Director": 1, "Manager": 2, "Player": 3}
ROLE_COLORS = {
    "CXO": "#d73027",
    "Director": "#fc8d59",
    "Manager": "#fee090",
    "Player": "#91bfdb",
}

OUTPUT_PATH = Path(__file__).with_name("strategy_structure.png")


def build_graph() -> nx.DiGraph:
    graph = nx.DiGraph()
    for node, role in NODES:
        graph.add_node(node, role=role)

    graph.add_edges_from(EDGES)
    return graph


def layout_tree(graph: nx.DiGraph) -> Dict[str, Tuple[float, float]]:
    child_map: Dict[str, List[str]] = defaultdict(list)
    child_nodes = set()
    for parent, child in EDGES:
        child_map[parent].append(child)
        child_nodes.add(child)

    roots = [node for node, _ in NODES if node not in child_nodes]
    root = roots[0] if roots else NODES[0][0]

    positions: Dict[str, Tuple[float, float]] = {}
    x_counter = 0

    def dfs(node: str, depth: int) -> float:
        nonlocal x_counter
        children = child_map.get(node, [])
        if not children:
            x = float(x_counter)
            x_counter += 1
        else:
            child_x = []
            for child in children:
                child_x.append(dfs(child, depth + 1))
            x = sum(child_x) / len(child_x)
        positions[node] = (x, -depth)
        return x

    dfs(root, 0)

    # Assign remaining nodes (in case of disconnected components)
    for node in graph.nodes():
        if node not in positions:
            positions[node] = (float(x_counter), -ROLE_LEVEL.get(graph.nodes[node]["role"], 0))
            x_counter += 1

    horizontal_spacing = 2.0
    vertical_spacing = 1.5
    return {node: (x * horizontal_spacing, y * vertical_spacing) for node, (x, y) in positions.items()}


def draw_graph(graph: nx.DiGraph, positions: Dict[str, Tuple[float, float]]) -> None:
    plt.figure(figsize=(10, 6))
    colors = [ROLE_COLORS[graph.nodes[node]["role"]] for node in graph.nodes()]

    nx.draw_networkx_nodes(graph, positions, node_size=1200, node_color=colors, linewidths=1.0, edgecolors="black")
    nx.draw_networkx_edges(graph, positions, arrows=True, arrowstyle="-|>", arrowsize=15, width=1.5)
    nx.draw_networkx_labels(graph, positions, font_size=8, font_color="black")

    legend_elements = [
        plt.Line2D([0], [0], marker="o", color="w", label=role, markerfacecolor=color, markersize=10, markeredgecolor="black")
        for role, color in ROLE_COLORS.items()
    ]
    plt.legend(handles=legend_elements, loc="upper center", ncol=4, frameon=False)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200)
    plt.close()


def main() -> None:
    graph = build_graph()
    positions = layout_tree(graph)
    draw_graph(graph, positions)
    print(f"Saved structure image to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
