# ReducedSeniorSpan_Adjusted シナリオ

## 目的

**SeniorManagerの管理スパンを削減しつつ、InterviewBasedと同規模（約2.5万ノード）の組織で比較**

## 元のReducedSeniorSpanとの違い

| 項目 | ReducedSeniorSpan | ReducedSeniorSpan_Adjusted |
|------|------------------:|---------------------------:|
| 総ノード数 | 10,795 | **~25,000** ✅ |
| CXO子数 | 15-20 | **17-22** |
| Director子数 | 10-15 | **13-17** |
| SeniorManager子数 | **3-5** | **7-10** |
| Manager子数 | 8-12 | **7-10** |

---

## CHILD_RANGES 設定

```python
CHILD_RANGES = {
    "CXO": (17, 22),             # 平均19.5（増加）
    "Director": (13, 17),        # 平均15（増加）
    "SeniorManager": (7, 10),    # 平均8.5（InterviewBased比で削減）
    "Manager": (7, 10),          # 平均8.5
    "Player": (0, 0),
}
```

---

## 設計の根拠

### InterviewBasedとの比較

| 役職 | InterviewBased | ReducedSeniorSpan_Adjusted | 変化 |
|------|---------------:|---------------------------:|------|
| CXO | 15-20 (17.5) | 17-22 (19.5) | +11% |
| Director | 10-15 (12.5) | 13-17 (15) | +20% |
| **SeniorManager** | **10-15 (12.5)** | **7-10 (8.5)** | **-32%** ✅ |
| Manager | 5-10 (7.5) | 7-10 (8.5) | +13% |

### 狙い

1. **SeniorManagerの管理スパンを約32%削減**
   - InterviewBased: 12.5人 → 8.5人
   - 報告受信負荷の削減

2. **組織全体の規模を維持**
   - 上層（CXO, Director）の子数を増やして補完
   - 総ノード数 約2.5万を確保

3. **公平な比較を実現**
   - InterviewBasedと同規模の組織
   - 構造変更の効果を正確に測定

---

## 推定ノード数

```
CXO: 1
Director: 19.5 × 1 ≈ 20
SeniorManager: 15 × 20 ≈ 300
Manager: 8.5 × 300 ≈ 2,550
Player: 8.5 × 2,550 ≈ 21,675
Total: 約 24,000-26,000 ✅
```

---

## 期待される効果

### 1. SeniorManagerの負荷削減
- 管理スパン削減（-32%）により報告受信負荷が減少
- **目標**: InterviewBased（94,420）から **15-20%削減**

### 2. 上層への影響
- CXOとDirectorの負荷は若干増加する可能性
- しかし、SeniorManagerほど挟まれないため増加は限定的

### 3. Managerへの影響
- 子数が微増（7.5 → 8.5）
- 若干の負荷増加が予想されるが、許容範囲

---

## 実行方法

```bash
# シミュレーション実行
python -m newSimulations.forThesis.ReducedSeniorSpan_Adjusted.graph_simulation

# 結果の可視化
python -m newSimulations.forThesis.ReducedSeniorSpan_Adjusted.visualize_results

# レポート更新
python -m newSimulations.forThesis.ReducedSeniorSpan_Adjusted.refresh_report
```

---

## 比較シナリオ

| シナリオ | 総ノード数 | SM子数 | 比較目的 |
|---------|----------:|-------:|---------|
| **InterviewBased** | 25,731 | 10-15 | ベースライン |
| **ReducedSeniorSpan_Adjusted** | ~25,000 | **7-10** | **公平な比較** ✅ |
| ReducedSeniorSpan（旧） | 10,795 | 3-5 | 極端な削減例 |

---

## 成功基準

1. **総ノード数**: 23,000-27,000（±10%以内）
2. **SeniorManager負荷**: InterviewBasedから **15-20%削減**
3. **負荷順序**: SeniorManagerが最高または2番目
4. **他層への影響**: 極端な負荷増加がない

---

## 研究上の意義

### 公平な比較の実現

従来のReducedSeniorSpanは総ノード数が約42%しかなく、公平な比較が困難でした。
本シナリオでは：

- ✅ 同規模の組織で比較
- ✅ 構造変更の純粋な効果を測定
- ✅ 実務的な示唆を導出可能

### 論文での位置づけ

> 「管理スパン削減の効果を検証するため、組織規模を統制した実験を実施した。
> InterviewBased（25,731ノード）と同規模の組織において、SeniorManagerの
> 管理スパンを平均12.5人から8.5人（-32%）に削減した場合の負荷変化を分析する。」

---

## 次のステップ

1. シミュレーション実行
2. 総ノード数の確認（目標: 23,000-27,000）
3. InterviewBasedとの詳細比較
4. 論文用の比較表作成
