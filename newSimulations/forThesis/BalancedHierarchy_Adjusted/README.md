# BalancedHierarchy_Adjusted シナリオ

## 目的

**負荷順序を最適化（SM > Dir > CXO ≈ Mgr）しつつ、InterviewBasedと同規模（約2.5万ノード）の組織で比較**

## 元のBalancedHierarchyとの違い

| 項目 | BalancedHierarchy | BalancedHierarchy_Adjusted |
|------|------------------:|---------------------------:|
| 総ノード数 | 2,435 | **~25,000** ✅ |
| CXO子数 | **5-8** | **18-23** |
| Director子数 | 12-15 | **12-15** (維持) |
| SeniorManager子数 | 6-9 | **8-11** |
| Manager子数 | 3-5 | **6-9** |

---

## CHILD_RANGES 設定

```python
CHILD_RANGES = {
    "CXO": (18, 23),         # 平均20.5（大幅増加）
    "Director": (12, 15),    # 平均13.5（維持）
    "SeniorManager": (8, 11), # 平均9.5（増加）
    "Manager": (6, 9),        # 平均7.5（増加）
    "Player": (0, 0),
}
```

---

## 設計の根拠

### 負荷順序の最適化を維持

元のBalancedHierarchyの設計思想を継承：

| 役職 | 子ノード数 | 狙い |
|------|----------:|------|
| **SeniorManager** | **8-11** | **中程度** → 挟まれ効果で最高負荷 |
| **Director** | **12-15** | **多い** → 2番目の負荷 |
| **Manager** | **6-9** | **少ない** → 低負荷 |
| **CXO** | **18-23** | 組織規模確保のため増加 |

### InterviewBasedとの比較

| 役職 | InterviewBased | BalancedHierarchy_Adjusted | 変化 |
|------|---------------:|---------------------------:|------|
| CXO | 15-20 (17.5) | 18-23 (20.5) | +17% |
| Director | 10-15 (12.5) | 12-15 (13.5) | +8% |
| SeniorManager | 10-15 (12.5) | 8-11 (9.5) | **-24%** |
| Manager | 5-10 (7.5) | 6-9 (7.5) | 0% |

---

## 推定ノード数

```
CXO: 1
Director: 20.5 × 1 ≈ 21
SeniorManager: 13.5 × 21 ≈ 284
Manager: 9.5 × 284 ≈ 2,698
Player: 7.5 × 2,698 ≈ 20,235
Total: 約 23,000-25,000 ✅
```

---

## 期待される結果

### 目標負荷順序
```
SeniorManager (最高)
    ↓
Director (2番目)
    ↓
Manager ≈ CXO (低く抑える)
```

### 予想される負荷値

| 役職 | InterviewBased | BalancedHierarchy_Adjusted（予想） |
|------|---------------:|----------------------------------:|
| SeniorManager | 94,420 | **75,000-85,000** (-10~-20%) |
| Director | 70,990 | **68,000-78,000** (-4~+10%) |
| Manager | 64,903 | **55,000-65,000** (-15~0%) |
| CXO | 47,789 | **45,000-55,000** (-6~+15%) |

---

## 設計のポイント

### 1. 挟まれ効果の活用（SeniorManager）

```
Director (13.5人)
  ↓ タスク流入
SeniorManager (9.5人管理) ← 上下から挟まれる
  ↓ タスク分割・報告受信
Manager (7.5人)
```

- 上層からタスクを受け取る
- 9.5人のManagerへ配分
- 9.5人から報告を受け取る
- **3重の負荷** → 最高値

### 2. Directorが2番目になる理由

- **多くのSeniorManager**（13.5人）を管理
- 報告受信負荷が大きい
- しかし上流なので、タスク流入は少ない

### 3. CXOとManagerを低く抑える

- **Manager**: 子数が少ない（7.5人）→ 報告受信負荷が小さい
- **CXO**: 最上層で上からのタスクがない（組織規模のため子数は多いが、報告受信のみ）

---

## 実行方法

```bash
# シミュレーション実行
python -m newSimulations.forThesis.BalancedHierarchy_Adjusted.graph_simulation

# 結果の可視化
python -m newSimulations.forThesis.BalancedHierarchy_Adjusted.visualize_results

# レポート更新
python -m newSimulations.forThesis.BalancedHierarchy_Adjusted.refresh_report
```

---

## 比較シナリオ

| シナリオ | 総ノード数 | 負荷順序（予想） |
|---------|----------:|-----------------|
| **InterviewBased** | 25,731 | SM > Dir > Mgr > CXO |
| **BalancedHierarchy_Adjusted** | ~25,000 | **SM > Dir > Mgr ≈ CXO** ✅ |
| BalancedHierarchy（旧） | 2,435 | SM > Mgr > Dir > CXO |

---

## 成功基準

1. **総ノード数**: 23,000-27,000（±10%以内）
2. **負荷順序**: SeniorManager > Director > (CXO ≈ Manager)
3. **SeniorManager削減**: InterviewBasedから **10-20%削減**
4. **ManagerとDirectorの順序**: Directorが2番目（またはManagerと同程度）

---

## 研究上の意義

### 負荷順序の最適化

> 「本研究では、SeniorManagerへの負荷集中を軽減しつつ、組織全体の
> 負荷分布を最適化する組織構造を提案する。具体的には、各階層の
> 管理スパンを調整することで、目標とする負荷順序（SeniorManager >
> Director > CXO ≈ Manager）の実現を目指す。」

### 公平な比較の実現

- ✅ InterviewBasedと同規模の組織
- ✅ 構造変更の純粋な効果を測定
- ✅ 負荷順序の制御可能性を実証

---

## 元のBalancedHierarchyとの関係

| 項目 | BalancedHierarchy（旧） | Adjusted（新） |
|------|------------------------|----------------|
| **目的** | 負荷順序の最適化 | 負荷順序の最適化 + 規模統制 |
| **ノード数** | 2,435 | ~25,000 |
| **比較可能性** | 低い（規模が異なる） | **高い（規模が同じ）** ✅ |
| **用途** | コンセプト実証 | **論文用比較実験** ✅ |

---

## 次のステップ

1. シミュレーション実行
2. 総ノード数の確認（目標: 23,000-27,000）
3. 負荷順序の確認（目標: SM > Dir > CXO ≈ Mgr）
4. InterviewBasedとの詳細比較
5. 論文用の比較表・グラフ作成
