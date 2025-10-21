# 分岐数比較実験

## 研究質問
1人の上長が管理する部下数（分岐数）が変わると、負荷分布はどう変化するか？

## 実験条件
- **分岐数**: 2、5、10
- **階層数**: 7階層（分岐数10は計算量制約で4階層）
- **試行回数**: 各1,000回
- **移動ルール**: 階層依存ルール

## 実験結果

### 負荷パターンの逆転現象

| 分岐数 | ノード数 | 最大負荷位置 | 最大負荷値 | パターン |
|--------|---------|-------------|-----------|---------|
| 2 | 127 | Senior (depth=5) | 28.95回 | 下層集中型 |
| 5 | 19,531 | CEO (depth=0) | 0.52回 | 極度分散型 |
| 10 | 1,111 | CEO (depth=0) | 42.09回 | 上層集中型 |

## 主要な発見

1. **負荷パターンの逆転**
   - 分岐数少ない: 下層中間管理職に負荷集中
   - 分岐数多い: 上層経営層に負荷集中

2. **最適分岐数の示唆**: 3-5程度が適切と推測

3. **組織規模の影響**: 極端に大きい組織は負荷が分散しすぎる

## 含まれるファイル

- `BRANCHES_COMPARISON_REPORT.md` - 詳細な比較レポート
- `simulation_branches_5.py` - 分岐数5のシミュレーション
- `simulation_branches_10_adjusted.py` - 分岐数10のシミュレーション

## 実行方法

### 分岐数5のシミュレーション
```bash
cd /path/to/SampleAgent
source .venv/bin/activate
python simulations/branches_comparison/simulation_branches_5.py
```

### 分岐数10のシミュレーション（階層調整版）
```bash
python simulations/branches_comparison/simulation_branches_10_adjusted.py
```

### カスタム分岐数で実行

`research_simulation.py`を直接編集：

```python
org = OrganizationGraph(branches=カスタム分岐数, height=階層-1, structure_type="baseline")
```

## 注意事項

- 分岐数が大きいと組織規模が指数的に増大
- 分岐数10×7階層は計算不可能（111万ノード）
- 現実的な組織サイズを考慮して設定すること