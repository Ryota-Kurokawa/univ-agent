"""
Refresh REPORT.md with richer information (top & min SimLoad per role).

Usage:
    python refresh_report.py
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

RESULT_PATH = Path(__file__).with_name("RESULT.md")
REPORT_PATH = Path(__file__).with_name("REPORT.md")
ROLE_ORDER = ["CXO", "Director", "SeniorManager", "Manager", "Player"]


@dataclass
class NodeRow:
    node: str
    role: str
    tasks: int
    children: int
    simload: float
    degree: float
    score: float
    normalized: float = 0.0


def parse_result(path: Path) -> List[NodeRow]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.startswith("| Node "):
            start = idx + 2
            break
    if start is None:
        raise SystemExit("Node table not found in RESULT.md")

    rows: List[NodeRow] = []
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        parts = [p.strip() for p in line.strip("|").split("|")]
        rows.append(
            NodeRow(
                node=parts[0],
                role=parts[1],
                tasks=int(parts[2]),
                children=int(parts[3]),
                simload=float(parts[4]),
                degree=float(parts[5]),
                score=float(parts[6]),
            )
        )
    return rows


def build_report(rows: List[NodeRow]) -> str:
    max_simload = max((row.simload for row in rows), default=1.0)
    for row in rows:
        row.normalized = row.simload / max_simload if max_simload else 0.0
    by_role: Dict[str, Dict[str, NodeRow]] = {}
    role_stats: Dict[str, Dict[str, float]] = {}
    for row in rows:
        role_bucket = by_role.setdefault(row.role, {})
        top = role_bucket.get("top")
        if top is None or row.simload > top.simload:
            role_bucket["top"] = row
        low = role_bucket.get("min")
        if low is None or row.simload < low.simload:
            role_bucket["min"] = row
        stats = role_stats.setdefault(
            row.role,
            {"count": 0, "sim": 0.0, "tasks": 0.0, "children": 0.0, "score": 0.0, "norm": 0.0},
        )
        stats["count"] += 1
        stats["sim"] += row.simload
        stats["tasks"] += row.tasks
        stats["children"] += row.children
        stats["score"] += row.score
        stats["norm"] += row.normalized

    lines = [
        "# BestPractice SimLoad Extremes",
        "",
        "組織全体で負荷がどこに集中しているかを把握しやすいよう、"
        "各役職の Top / Average / Min を一覧化し、SimLoad（正規化含む）を比較します。",
        "",
        "## 概要テーブル",
        "",
        "| Role | Type | Node | SimLoad | Normalized | Score | Tasks | Children |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for role in ROLE_ORDER:
        info = by_role.get(role)
        if not info:
            continue
        top = info["top"]
        low = info["min"]
        stats = role_stats.get(role, {"count": 1})
        count = stats["count"]
        avg_sim = stats["sim"] / count
        avg_norm = stats["norm"] / count
        avg_score = stats["score"] / count
        avg_tasks = stats["tasks"] / count
        avg_children = stats["children"] / count

        lines.append(
            f"| {role} | Top | {top.node} | {top.simload:.2f} | {top.normalized:.3f} | "
            f"{top.score:.5f} | {top.tasks} | {top.children} |"
        )
        lines.append(
            f"| {role} | Average | - | {avg_sim:.2f} | {avg_norm:.3f} | "
            f"{avg_score:.5f} | {avg_tasks:.2f} | {avg_children:.2f} |"
        )
        lines.append(
            f"| {role} | Min | {low.node} | {low.simload:.2f} | {low.normalized:.3f} | "
            f"{low.score:.5f} | {low.tasks} | {low.children} |"
        )

    for role in ROLE_ORDER:
        info = by_role.get(role)
        if not info:
            continue
        top = info["top"]
        low = info["min"]
        stats = role_stats.get(role, {"count": 1})
        count = stats["count"]
        avg_sim = stats["sim"] / count
        avg_norm = stats["norm"] / count
        avg_score = stats["score"] / count
        avg_tasks = stats["tasks"] / count
        avg_children = stats["children"] / count
        lines.extend(
            [
                "",
                f"### {role}",
                "",
                "| 指標 | Top | Average | Min |",
                "| --- | --- | --- | --- |",
                f"| Node | {top.node} | - | {low.node} |",
                f"| SimLoad | {top.simload:.2f} | {avg_sim:.2f} | {low.simload:.2f} |",
                f"| Normalized | {top.normalized:.3f} | {avg_norm:.3f} | {low.normalized:.3f} |",
                f"| Score | {top.score:.5f} | {avg_score:.5f} | {low.score:.5f} |",
                f"| Tasks | {top.tasks} | {avg_tasks:.2f} | {low.tasks} |",
                f"| Children | {top.children} | {avg_children:.2f} | {low.children} |",
            ]
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    rows = parse_result(RESULT_PATH)
    report_text = build_report(rows)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(f"Updated {REPORT_PATH}")


if __name__ == "__main__":
    main()
