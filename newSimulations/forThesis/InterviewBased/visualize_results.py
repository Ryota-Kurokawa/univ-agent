"""
Utility script that reads RESULT.md and creates simple visualizations.

- Role averages: bar charts for Avg Tasks / Avg SimLoad.
- Top nodes: SimLoad ranking (default top 20) with role coloring.

Usage:
    python visualize_results.py

Outputs PNG files next to RESULT.md.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
from matplotlib import font_manager

ROLE_SEQUENCE = ["CXO", "Director", "SeniorManager", "Manager", "Player"]


@dataclass
class RoleAverage:
    name: str
    nodes: int
    avg_tasks: float
    avg_simload: float


@dataclass
class NodeMetrics:
    name: str
    role: str
    tasks: int
    children: int
    simload: float
    degree: float
    score: float


def parse_tables(result_path: Path) -> tuple[list[RoleAverage], list[NodeMetrics]]:
    lines = result_path.read_text(encoding="utf-8").splitlines()
    role_averages: List[RoleAverage] = []
    node_metrics: List[NodeMetrics] = []

    def _parse_row(line: str) -> List[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    state = "search"
    for line in lines:
        if line.startswith("| Role |") and state == "search":
            state = "role_header"
            continue
        if line.startswith("| Node |"):
            state = "node_header"
            continue

        if state == "role_header":
            if line.startswith("| ---"):
                state = "role_rows"
                continue
            state = "search"
            continue

        if state == "role_rows":
            if not line.startswith("|"):
                state = "search"
                continue
            name, nodes, avg_tasks, avg_simload = _parse_row(line)
            role_averages.append(
                RoleAverage(
                    name=name,
                    nodes=int(nodes),
                    avg_tasks=float(avg_tasks),
                    avg_simload=float(avg_simload),
                )
            )
            continue

        if state == "node_header":
            if line.startswith("| ---"):
                state = "node_rows"
                continue
            state = "search"
            continue

        if state == "node_rows":
            if not line.startswith("|"):
                break
            name, role, tasks, children, simload, degree, score = _parse_row(line)
            node_metrics.append(
                NodeMetrics(
                    name=name,
                    role=role,
                    tasks=int(tasks),
                    children=int(children),
                    simload=float(simload),
                    degree=float(degree),
                    score=float(score),
                )
            )

    return role_averages, node_metrics


def plot_role_averages(role_averages: List[RoleAverage], out_dir: Path) -> None:
    roles = [ra.name for ra in role_averages]
    avg_tasks = [ra.avg_tasks for ra in role_averages]
    avg_simload = [ra.avg_simload for ra in role_averages]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].bar(roles, avg_tasks, color="#6baed6")
    axes[0].set_title("平均タスク数 (役職別)")
    axes[0].set_ylabel("タスク数")
    axes[0].tick_params(axis="x", rotation=45)

    axes[1].bar(roles, avg_simload, color="#fd8d3c")
    axes[1].set_title("平均SimLoad (役職別)")
    axes[1].set_ylabel("SimLoad")
    axes[1].tick_params(axis="x", rotation=45)

    fig.tight_layout()
    output_path = out_dir / "plot_role_averages.png"
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_top_nodes(node_metrics: List[NodeMetrics], out_dir: Path, top_n: int = 20) -> None:
    sorted_nodes = sorted(node_metrics, key=lambda m: m.simload, reverse=True)[:top_n]
    names = [m.name for m in sorted_nodes]
    simloads = [m.simload for m in sorted_nodes]
    colors: Dict[str, str] = {
        "CXO": "#08519c",
        "Director": "#3182bd",
        "SeniorManager": "#6baed6",
        "Manager": "#9ecae1",
        "Player": "#c6dbef",
    }
    node_colors = [colors.get(m.role, "#999999") for m in sorted_nodes]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(names, simloads, color=node_colors)
    ax.set_title(f"SimLoad 上位 {top_n} ノード")
    ax.set_ylabel("SimLoad")
    ax.tick_params(axis="x", rotation=75)

    # Create legend manually
    handled_roles = {}
    for m, bar in zip(sorted_nodes, bars):
        if m.role not in handled_roles:
            handled_roles[m.role] = bar
    ax.legend(
        handled_roles.values(),
        handled_roles.keys(),
        title="役職",
        loc="upper right",
    )


    fig.tight_layout()
    output_path = out_dir / f"plot_top_nodes_{top_n}.png"
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_role_extremes(node_metrics: List[NodeMetrics], out_dir: Path) -> None:
    roles = []
    top_values = []
    min_values = []
    for role in ROLE_SEQUENCE:
        role_nodes = [m for m in node_metrics if m.role == role]
        if not role_nodes:
            continue
        top = max(role_nodes, key=lambda m: m.simload)
        low = min(role_nodes, key=lambda m: m.simload)
        roles.append(role)
        top_values.append(top.simload)
        min_values.append(low.simload)

    if not roles:
        return

    x = range(len(roles))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar([i - width / 2 for i in x], top_values, width, label="Top SimLoad", color="#fb6a4a")
    ax.bar([i + width / 2 for i in x], min_values, width, label="Min SimLoad", color="#74c476")
    ax.set_xticks(list(x))
    ax.set_xticklabels(roles, rotation=45)
    ax.set_ylabel("SimLoad")
    ax.set_title("役職別 SimLoad 極値 (Top vs Min)")
    ax.legend()

    for i, (top_val, min_val) in enumerate(zip(top_values, min_values)):
        ax.text(i - width / 2, top_val, f"{top_val:.0f}", ha="center", va="bottom", fontsize=8)
        ax.text(i + width / 2, min_val, f"{min_val:.0f}", ha="center", va="bottom", fontsize=8)

    fig.tight_layout()
    output_path = out_dir / "plot_role_extremes.png"
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def _configure_font() -> None:
    """Try to use a Japanese-capable font to avoid square glyphs."""
    candidates = [
        "Hiragino Sans",
        "Hiragino Kaku Gothic ProN",
        "Yu Gothic",
        "YuGothic",
        "Noto Sans CJK JP",
        "IPAexGothic",
        "IPAGothic",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for font in candidates:
        if font in available:
            plt.rcParams["font.family"] = font
            break
    plt.rcParams["axes.unicode_minus"] = False


def main() -> None:
    _configure_font()
    parser = argparse.ArgumentParser(description="RESULT.md を読み込んで可視化します。")
    parser.add_argument(
        "--result",
        type=Path,
        default=Path(__file__).with_name("RESULT.md"),
        help="解析対象の RESULT.md パス",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="SimLoad上位ノードの表示数",
    )
    args = parser.parse_args()

    role_averages, node_metrics = parse_tables(args.result)
    if not role_averages or not node_metrics:
        raise SystemExit("RESULT.md から必要なデータを取得できませんでした。")

    out_dir = args.result.parent
    plot_role_averages(role_averages, out_dir)
    plot_top_nodes(node_metrics, out_dir, top_n=args.top_n)
    plot_role_extremes(node_metrics, out_dir)
    print(f"Saved plots to {out_dir}")


if __name__ == "__main__":
    main()
