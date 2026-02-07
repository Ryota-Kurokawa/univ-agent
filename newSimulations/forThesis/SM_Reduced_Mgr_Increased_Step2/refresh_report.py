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
    by_role: Dict[str, Dict[str, NodeRow]] = {}
    for row in rows:
        role_bucket = by_role.setdefault(row.role, {})
        top = role_bucket.get("top")
        if top is None or row.simload > top.simload:
            role_bucket["top"] = row
        low = role_bucket.get("min")
        if low is None or row.simload < low.simload:
            role_bucket["min"] = row

    lines = [
        "# SM_Reduced_Mgr_Increased_Step2 SimLoad Extremes",
        "",
        "組織全体で負荷がどこに集中しているかを把握しやすいよう、"
        "各役職の最大・最小 SimLoad ノードを一覧化し、その差分も表示します。",
        "",
        "## 概要テーブル",
        "",
        "| Role | Top Node | Top SimLoad | Min Node | Min SimLoad | 差分 (Top-Min) |",
        "| --- | --- | ---: | --- | ---: | ---: |",
    ]

    for role in ROLE_ORDER:
        info = by_role.get(role)
        if not info:
            continue
        top = info["top"]
        low = info["min"]
        diff = top.simload - low.simload
        lines.append(
            f"| {role} | {top.node} | {top.simload:.2f} | {low.node} | {low.simload:.2f} | {diff:.2f} |"
        )

    for role in ROLE_ORDER:
        info = by_role.get(role)
        if not info:
            continue
        top = info["top"]
        low = info["min"]
        lines.extend(
            [
                "",
                f"### {role}",
                "",
                "| 指標 | Top | Min |",
                "| --- | --- | --- |",
                f"| Node | {top.node} | {low.node} |",
                f"| SimLoad | {top.simload:.2f} | {low.simload:.2f} |",
                f"| Score | {top.score:.5f} | {low.score:.5f} |",
                f"| Tasks | {top.tasks} | {low.tasks} |",
                f"| Children | {top.children} | {low.children} |",
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
