# SM_Reduced_Mgr_Increased_Step2

## 概要

SeniorManager の管理スパンを削減し、Manager の管理スパンを増加させる実験パターン2。

## InterviewBased からの変更点

### CHILD_RANGES 変更

| 役職 | InterviewBased | Step2 | 変化率 |
| --- | --- | --- | --- |
| CXO | (15, 20) 平均 17.5 | (15, 20) 平均 17.5 | 変更なし |
| Director | (10, 15) 平均 12.5 | (10, 15) 平均 12.5 | 変更なし |
| SeniorManager | (10, 15) 平均 12.5 | (6, 9) 平均 7.5 | **-40%** ⬇️ |
| Manager | (5, 10) 平均 7.5 | (10, 14) 平均 12 | **+60%** ⬆️ |
| Player | (0, 0) | (0, 0) | 変更なし |

## Step1 からの変更

| 役職 | Step1 | Step2 | 変化 |
| --- | --- | --- | --- |
| SeniorManager | (8, 11) 平均 9.5 | (6, 9) 平均 7.5 | -2.0 (-21%) |
| Manager | (8, 12) 平均 10 | (10, 14) 平均 12 | +2.0 (+20%) |

## 仮説

- SeniorManager の管理スパンをさらに削減することで、SeniorManager の負荷がより軽減される
- Manager の管理スパンをさらに増やすことで、Manager への負荷集中が観察される可能性
- Step1 との比較で、負荷遷移の傾向を把握

## 実行方法

```bash
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step2.graph_simulation
```

## 可視化

```bash
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step2.visualize_results
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step2.refresh_report
```

## 出力ファイル

- `RESULT.md`: シミュレーション結果の詳細テーブル
- `REPORT.md`: 役職別の SimLoad 極値レポート
- `plot_role_averages.png`: 役職別平均タスク数と SimLoad
- `plot_top_nodes_20.png`: SimLoad 上位 20 ノード
- `plot_role_extremes.png`: 役職別 SimLoad 極値
