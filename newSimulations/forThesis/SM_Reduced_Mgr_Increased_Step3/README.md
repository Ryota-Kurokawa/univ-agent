# SM_Reduced_Mgr_Increased_Step3

## 概要

SeniorManager の管理スパンを削減し、Manager の管理スパンを増加させる実験パターン3。

## InterviewBased からの変更点

### CHILD_RANGES 変更

| 役職 | InterviewBased | Step3 | 変化率 |
| --- | --- | --- | --- |
| CXO | (15, 20) 平均 17.5 | (15, 20) 平均 17.5 | 変更なし |
| Director | (10, 15) 平均 12.5 | (10, 15) 平均 12.5 | 変更なし |
| SeniorManager | (10, 15) 平均 12.5 | (5, 7) 平均 6 | **-52%** ⬇️ |
| Manager | (5, 10) 平均 7.5 | (11, 15) 平均 13 | **+73%** ⬆️ |
| Player | (0, 0) | (0, 0) | 変更なし |

## Step2 からの変更

| 役職 | Step2 | Step3 | 変化 |
| --- | --- | --- | --- |
| SeniorManager | (6, 9) 平均 7.5 | (5, 7) 平均 6 | -1.5 (-20%) |
| Manager | (10, 14) 平均 12 | (11, 15) 平均 13 | +1.0 (+8%) |

## 仮説

- SeniorManager の管理スパンを大幅に削減することで、SeniorManager の負荷が大幅に軽減される
- Manager の管理スパンを大幅に増やすことで、Manager への負荷集中が顕著に観察される可能性
- 極端な設定での負荷遷移を観察

## 実行方法

```bash
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step3.graph_simulation
```

## 可視化

```bash
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step3.visualize_results
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step3.refresh_report
```

## 出力ファイル

- `RESULT.md`: シミュレーション結果の詳細テーブル
- `REPORT.md`: 役職別の SimLoad 極値レポート
- `plot_role_averages.png`: 役職別平均タスク数と SimLoad
- `plot_top_nodes_20.png`: SimLoad 上位 20 ノード
- `plot_role_extremes.png`: 役職別 SimLoad 極値
