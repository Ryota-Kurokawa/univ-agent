# SM_Reduced_Mgr_Increased_Step1

## 概要

SeniorManager の管理スパンを削減し、Manager の管理スパンを増加させる実験パターン1。

## InterviewBased からの変更点

### CHILD_RANGES 変更

| 役職 | InterviewBased | Step1 | 変化率 |
| --- | --- | --- | --- |
| CXO | (15, 20) 平均 17.5 | (15, 20) 平均 17.5 | 変更なし |
| Director | (10, 15) 平均 12.5 | (10, 15) 平均 12.5 | 変更なし |
| SeniorManager | (10, 15) 平均 12.5 | (8, 11) 平均 9.5 | **-24%** ⬇️ |
| Manager | (5, 10) 平均 7.5 | (8, 12) 平均 10 | **+33%** ⬆️ |
| Player | (0, 0) | (0, 0) | 変更なし |

## 仮説

- SeniorManager の管理スパンを減らすことで、SeniorManager の負荷が軽減される
- Manager の管理スパンを増やすことで、組織全体のノード数バランスを調整
- 負荷がどの役職に遷移するかを観察

## 実行方法

```bash
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step1.graph_simulation
```

## 可視化

```bash
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step1.visualize_results
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step1.refresh_report
```

## 出力ファイル

- `RESULT.md`: シミュレーション結果の詳細テーブル
- `REPORT.md`: 役職別の SimLoad 極値レポート
- `plot_role_averages.png`: 役職別平均タスク数と SimLoad
- `plot_top_nodes_20.png`: SimLoad 上位 20 ノード
- `plot_role_extremes.png`: 役職別 SimLoad 極値
