#!/usr/bin/env python3
"""
Dir_Increased_SM_Reduced シリーズの役職別SimLoad推移を折れ線グラフで作成
- 最高SimLoad
- 正規化SimLoad（平均SimLoad / 平均タスク数）
"""

import matplotlib.pyplot as plt
import matplotlib
import re
from pathlib import Path
from collections import defaultdict

# 日本語フォント設定
matplotlib.rcParams['font.family'] = 'Hiragino Sans'

# シナリオのパスと表示名
SCENARIOS = [
    ("InterviewBased", "newSimulations/forThesis/InterviewBased/RESULT.md"),
    ("Dir_Step1", "newSimulations/forThesis/Dir_Increased_SM_Reduced_Step1/RESULT.md"),
    ("Dir_Step2", "newSimulations/forThesis/Dir_Increased_SM_Reduced_Step2/RESULT.md"),
    ("Dir_Step3", "newSimulations/forThesis/Dir_Increased_SM_Reduced_Step3/RESULT.md"),
    ("Dir_Step4", "newSimulations/forThesis/Dir_Increased_SM_Reduced_Step4/RESULT.md"),
]

ROLES = ["CXO", "Director", "SeniorManager", "Manager", "Player"]

def parse_result_md(filepath: str) -> tuple:
    """RESULT.mdから各役職の統計を抽出"""
    max_loads = defaultdict(float)
    avg_loads = defaultdict(float)
    avg_tasks = defaultdict(float)

    base_path = Path(__file__).parent.parent
    full_path = base_path / filepath

    if not full_path.exists():
        print(f"Warning: {full_path} not found")
        return max_loads, avg_loads, avg_tasks

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # Role統計セクションから平均値を抽出
    in_role_section = False
    for line in lines:
        if "| Role | Nodes | Avg Tasks | Avg SimLoad |" in line:
            in_role_section = True
            continue
        if in_role_section and line.startswith("|") and "---" not in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                role = parts[1]
                try:
                    avg_task = float(parts[3])
                    avg_load = float(parts[4])
                    if role in ROLES:
                        avg_tasks[role] = avg_task
                        avg_loads[role] = avg_load
                except (ValueError, IndexError):
                    continue
        elif in_role_section and not line.startswith("|"):
            in_role_section = False

    # Node Detailsセクションから最高値を抽出
    in_node_details = False
    for line in lines:
        if "| Node | Role |" in line:
            in_node_details = True
            continue
        if in_node_details and line.startswith("|") and "---" not in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 6:
                role = parts[2]
                try:
                    sim_load = float(parts[5])
                    if role in ROLES:
                        max_loads[role] = max(max_loads[role], sim_load)
                except (ValueError, IndexError):
                    continue

    return max_loads, avg_loads, avg_tasks


def main():
    # データ収集
    max_data = {role: [] for role in ROLES}
    normalized_data = {role: [] for role in ROLES}
    avg_tasks_data = {role: [] for role in ROLES}
    scenario_names = []

    for name, path in SCENARIOS:
        scenario_names.append(name)
        max_loads, avg_loads, avg_tasks = parse_result_md(path)

        for role in ROLES:
            max_data[role].append(max_loads.get(role, 0))

        for role in ROLES:
            avg_task = avg_tasks.get(role, 1)
            avg_load = avg_loads.get(role, 0)
            normalized = avg_load / avg_task if avg_task > 0 else 0
            normalized_data[role].append(normalized)
            avg_tasks_data[role].append(avg_task)

    # 2つのグラフを作成
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # グラフ1: 最高SimLoadの推移
    ax1 = axes[0]
    markers = ['o', 's', '^', 'D', 'v']
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']

    for i, role in enumerate(ROLES):
        ax1.plot(scenario_names, max_data[role],
                marker=markers[i],
                color=colors[i],
                linewidth=2,
                markersize=8,
                label=role)

    ax1.set_xlabel("シナリオ", fontsize=12)
    ax1.set_ylabel("最高 SimLoad", fontsize=12)
    ax1.set_title("(a) 役職別最高 SimLoad の推移\n(Director増加・SM削減)", fontsize=14)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, max(max(max_data[role]) for role in ROLES) * 1.1)
    ax1.tick_params(axis='x', rotation=15)

    # グラフ2: 正規化SimLoadの推移（全役職）
    ax2 = axes[1]

    for i, role in enumerate(ROLES):
        ax2.plot(scenario_names, normalized_data[role],
                marker=markers[i],
                color=colors[i],
                linewidth=2,
                markersize=8,
                label=role)

    ax2.set_xlabel("シナリオ", fontsize=12)
    ax2.set_ylabel("正規化 SimLoad (SimLoad/タスク数)", fontsize=12)
    ax2.set_title("(b) 役職別正規化 SimLoad の推移\n(Director増加・SM削減)", fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=15)

    plt.tight_layout()

    # 保存
    output_path = Path(__file__).parent / "figures"
    output_path.mkdir(exist_ok=True)
    plt.savefig(output_path / "dir_step_load_transition.png", dpi=150)
    print(f"Graph saved to {output_path / 'dir_step_load_transition.png'}")

    # データも表示
    print("\n=== 各シナリオの役職別最高SimLoad ===")
    print(f"{'シナリオ':<15}", end="")
    for role in ROLES:
        print(f"{role:<15}", end="")
    print()
    for i, name in enumerate(scenario_names):
        print(f"{name:<15}", end="")
        for role in ROLES:
            print(f"{max_data[role][i]:<15.2f}", end="")
        print()

    print("\n=== 各シナリオの役職別正規化SimLoad ===")
    print(f"{'シナリオ':<15}", end="")
    for role in ROLES:
        print(f"{role:<15}", end="")
    print()
    for i, name in enumerate(scenario_names):
        print(f"{name:<15}", end="")
        for role in ROLES:
            print(f"{normalized_data[role][i]:<15.2f}", end="")
        print()


if __name__ == "__main__":
    main()
