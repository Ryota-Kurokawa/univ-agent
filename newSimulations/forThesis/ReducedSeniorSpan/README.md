# ReducedSeniorSpan シナリオ

## 目的

**SeniorManagerの管理スパンを削減し、負荷を分散する**

## 戦略

SeniorManagerへの負荷集中を解決するため、以下の構造変更を実施：

1. **SeniorManagerの子ノード数を削減**: 10-15人 → **3-5人**
2. **Managerの子ノード数を増加**: 5-10人 → **8-12人**

### 狙い

- SeniorManagerが管理する直属の部下を減らす
- 報告受信負荷を大幅に削減（+0.1 × タスク重み × 子ノード数）
- Managerが増えることでタスクが薄く分散
- 組織全体の階層が深くなり、負荷が平準化

---

## CHILD_RANGES 設定

```python
CHILD_RANGES = {
    "CXO": (15, 20),
    "Director": (10, 15),
    "SeniorManager": (3, 5),    # ★ 削減（InterviewBased: 10-15）
    "Manager": (8, 12),          # ★ 増加（InterviewBased: 5-10）
    "Player": (0, 0),
}
```

---

## 比較対象

### InterviewBased（実務者インタビューベース）

| 役職 | 子ノード数 | 平均SimLoad |
|------|----------:|------------:|
| CXO | 15-20 | 47,789 |
| Director | 10-15 | 70,990 |
| **SeniorManager** | **10-15** | **94,420** ⚠️ |
| Manager | 5-10 | 64,903 |
| Player | 0 | 7,636 |

**問題点**: SeniorManagerが最高負荷（94,420）

---

## 期待される効果

### 1. SeniorManagerの負荷削減
- 子ノード数が1/3に削減（10-15 → 3-5）
- 報告受信負荷が大幅減少
- **目標**: SimLoadを **60,000以下** に削減（約36%削減）

### 2. 組織全体の負荷分散
- Managerが増えてタスクが分散
- 極端な負荷集中点が消失
- 最高負荷値が全体的に低下

### 3. 構造的な改善
- 管理スパンが適正化（3-5人は理想的な範囲）
- 中間層の負担が軽減
- 報告経路が明確化

---

## 実行方法

```bash
# シミュレーション実行
python -m newSimulations.forThesis.ReducedSeniorSpan.graph_simulation

# 結果の可視化
python -m newSimulations.forThesis.ReducedSeniorSpan.visualize_results

# レポート更新
python -m newSimulations.forThesis.ReducedSeniorSpan.refresh_report
```

---

## 結果の確認

### 主要指標
- `RESULT.md`: 全ノードの詳細データ
- `REPORT.md`: 役職別サマリー
- `plot_role_averages.png`: 役職別平均負荷グラフ

### 成功基準
1. SeniorManagerの平均SimLoadが **70,000以下**
2. 全役職の最高SimLoadが **InterviewBasedより低い**
3. 負荷の標準偏差が小さくなる（負荷が平準化）

---

## 他シナリオとの比較

| シナリオ | SeniorManager子数 | Manager子数 | 狙い |
|---------|------------------:|------------:|------|
| **InterviewBased** | 10-15 | 5-10 | 実務データベース |
| **ReducedSeniorSpan** | **3-5** | **8-12** | SeniorManager負荷削減 |
| BestPractice | 8-9 | 14-16 | 理想的構造探索 |
| Final | 5-8 | 10-20 | SeniorManager削減実験 |

---

## 理論的背景

### 管理スパンの適正範囲

組織論では、効果的な管理スパン（1人の上司が管理する部下の数）は以下とされる：

- **上層管理職**: 3-7人（戦略的判断が必要）
- **中間管理職**: 5-10人（調整業務が多い）
- **下層管理職**: 10-15人（定型業務が中心）

InterviewBasedではSeniorManagerが10-15人を管理しており、調整コストが過大。
本シナリオでは **3-5人** に削減し、理論的な適正範囲に収める。

---

## 次のステップ

1. シミュレーション実行
2. InterviewBasedとの詳細比較
3. 負荷削減率の算出
4. 論文への結果反映
