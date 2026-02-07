# SM_Reduced_Mgr_Increased_Step4

## 概要

SeniorManager の管理スパンを削減し、Manager の管理スパンを増加させる実験パターン4。

## InterviewBased からの変更点

### CHILD_RANGES 変更

| 役職 | InterviewBased | Step4 | 変化率 |
| --- | --- | --- | --- |
| CXO | (15, 20) 平均 17.5 | (15, 20) 平均 17.5 | 変更なし |
| Director | (10, 15) 平均 12.5 | (10, 15) 平均 12.5 | 変更なし |
| SeniorManager | (10, 15) 平均 12.5 | (4, 6) 平均 5 | **-60%** ⬇️ |
| Manager | (5, 10) 平均 7.5 | (12, 16) 平均 14 | **+87%** ⬆️ |
| Player | (0, 0) | (0, 0) | 変更なし |

## Step3 からの変更

| 役職 | Step3 | Step4 | 変化 |
| --- | --- | --- | --- |
| SeniorManager | (5, 7) 平均 6 | (4, 6) 平均 5 | -1.0 (-17%) |
| Manager | (11, 15) 平均 13 | (12, 16) 平均 14 | +1.0 (+8%) |

## 仮説

- SeniorManager の管理スパンを極端に削減することで、SeniorManager の負荷が極めて軽減される
- Manager の管理スパンを極端に増やすことで、Manager への負荷集中が最大限に観察される可能性
- 極限的な設定での組織構造の安定性を検証

## 実行方法

```bash
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step4.graph_simulation
```

## 可視化

```bash
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step4.visualize_results
python3 -m newSimulations.forThesis.SM_Reduced_Mgr_Increased_Step4.refresh_report
```

## 出力ファイル

- `RESULT.md`: シミュレーション結果の詳細テーブル
- `REPORT.md`: 役職別の SimLoad 極値レポート
- `plot_role_averages.png`: 役職別平均タスク数と SimLoad
- `plot_top_nodes_20.png`: SimLoad 上位 20 ノード
- `plot_role_extremes.png`: 役職別 SimLoad 極値
