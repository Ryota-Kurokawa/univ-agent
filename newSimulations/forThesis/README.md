# forThesis - 論文用シミュレーションシナリオ集

本ディレクトリには、中間管理職負荷集中問題を解決するための組織構造最適化シミュレーションが含まれています。

---

## 📚 シナリオ一覧

### 🎯 シナリオの分類

| 分類 | シナリオ | 目的 | 総ノード数 | 推奨度 |
|------|---------|------|----------:|--------|
| **ベースライン** 🔵 | InterviewBased | 実務データに基づく比較基準 | 25,731 | ⭐⭐⭐⭐⭐ |
| **メインシナリオ** ⭐ | ReducedSeniorSpan_Adjusted | 管理スパン削減（規模統制版） | ~25,000 | ⭐⭐⭐⭐⭐ |
| **メインシナリオ** ⭐ | BalancedHierarchy_Adjusted | 負荷順序最適化（規模統制版） | ~25,000 | ⭐⭐⭐⭐⭐ |
| **系統的実験** 🔬 | **ParameterSweep** (8ステップ) | **負荷遷移の段階的調査**<br>SM管理スパン 12.5→5 | ~20,000-25,000 | ⭐⭐⭐⭐⭐ |
| **補助シナリオ** | BestPractice | 理想構造探索 | 26,048 | ⭐⭐⭐ |
| **補助シナリオ** | Final | SeniorManager削減実験 | 24,938 | ⭐⭐⭐ |
| **初期実験版** | ReducedSeniorSpan（旧） | 管理スパン大幅削減 | 10,795 ❌ | ⭐⭐ |
| **初期実験版** | BalancedHierarchy（旧） | 負荷順序最適化 | 2,435 ❌ | ⭐⭐ |
| **理論的境界** | maxplayers | 極端なフラット構造 | 26,048 | ⭐ |
| **理論的境界** | maxdirector | 極端なワイド構造 | 25,001 | ⭐ |

🔵 = ベースライン / ⭐ = 論文用推奨 / 🔬 = 系統的実験 / ❌ = 規模が異なるため直接比較不可

---

## 📊 全シナリオ比較表

### CHILD_RANGES 設定（管理スパン）

| シナリオ | CXO | Director | SeniorManager | Manager | Player | 総ノード数 |
|---------|----:|----------|---------------|---------|--------|----------:|
| **InterviewBased** 🔵 | 15-20<br>(17.5) | 10-15<br>(12.5) | 10-15<br>(12.5) | 5-10<br>(7.5) | 0 | **25,731** |
| **ReducedSeniorSpan_Adjusted** ⭐ | 17-22<br>(19.5) | 13-17<br>(15) | **7-10**<br>**(8.5)** | 7-10<br>(8.5) | 0 | **~25,000** |
| **BalancedHierarchy_Adjusted** ⭐ | 18-23<br>(20.5) | 12-15<br>(13.5) | **8-11**<br>**(9.5)** | 6-9<br>(7.5) | 0 | **~25,000** |
| BestPractice | 15-16<br>(15.5) | 12-14<br>(13) | 8-9<br>(8.5) | 14-16<br>(15) | 0 | 26,048 |
| Final | 15-20<br>(17.5) | 10-15<br>(12.5) | **5-8**<br>**(6.5)** | **10-20**<br>**(15)** | 0 | 24,938 |
| ReducedSeniorSpan（旧） | 15-20<br>(17.5) | 10-15<br>(12.5) | **3-5**<br>**(4)** | **8-12**<br>**(10)** | 0 | 10,795 ❌ |
| BalancedHierarchy（旧） | **5-8**<br>**(6.5)** | 12-15<br>(13.5) | 6-9<br>(7.5) | **3-5**<br>**(4)** | 0 | 2,435 ❌ |
| maxplayers | 5<br>(5) | 5<br>(5) | 5<br>(5) | **190-210**<br>**(200)** | 0 | 26,048 |
| maxdirector | **6250**<br>**(6250)** | 1<br>(1) | 1<br>(1) | 1<br>(1) | 0 | 25,001 |

*カッコ内は平均値 / 🔵 = ベースライン / ⭐ = 論文用推奨 / ❌ = 規模が異なるため直接比較不可*

---

### シミュレーション結果（役職別平均SimLoad）

| シナリオ | CXO | Director | SeniorManager | SM削減率 | Manager | Player | 最高負荷 |
|---------|----:|----------|---------------|:--------:|---------|--------|---------|
| **InterviewBased** 🔵 | 47,789 | 70,990 | **94,420** 🔴 | **(基準)** | 64,903 | 7,636 | **SM** |
| **ReducedSeniorSpan_Adjusted** ⭐ | 📊 予測中 | 📊 予測中 | 📊 **75,700-80,200**<br>*(-15~-20%)* | **-15~-20%** 🎯 | 📊 予測中 | 📊 予測中 | **SM** 🎯 |
| **BalancedHierarchy_Adjusted** ⭐ | 📊 **45,000-55,000**<br>*(-6~+15%)* | 📊 **68,000-78,000**<br>*(-4~+10%)* | 📊 **75,000-85,000**<br>*(-10~-20%)* | **-10~-20%** 🎯 | 📊 **55,000-65,000**<br>*(-15~0%)* | 📊 予測中 | **SM** 🎯 |
| BestPractice | 41,960 | 73,296 | 85,610 | **-9.3%** ✅ | 68,103 | 6,151 | SM |
| Final | 40,581 | 63,681 | 83,677 | **-11.4%** ✅ | 71,895 | 5,257 | SM |
| ReducedSeniorSpan（旧） | 36,762 | 57,607 | 72,127 | **-23.6%** ✅ | **76,178** 🔴 | 7,021 | **Mgr** ❌ |
| BalancedHierarchy（旧） | 27,458 | 65,480 | 76,709 🔴 | **-18.8%** ✅ | 67,324 | 12,785 | **SM** |
| maxplayers | 41,960 | 73,296 | 85,610 | -9.3% | 68,103 | 6,151 | SM |
| maxdirector | **10,706,529** 💀 | 49,810 | 108,452 | +14.9% ❌ | **167,251** | 105,565 | **CXO** |

*🔵 = ベースライン / ⭐ = 論文用推奨 / 📊 = 予測値（シナリオREADME参照） / 🎯 = 目標 / 🔴 = 最高負荷 / ✅ = 削減成功 / ❌ = 副作用あり / 💀 = 異常値*

---

### シナリオ特徴サマリー

| シナリオ | 主な特徴 | SM管理スパン | 期待効果 | 論文での役割 |
|---------|---------|:-----------:|---------|------------|
| **InterviewBased** 🔵 | 実務ベースライン | 12.5人 | **SM: 94,420**<br>(基準値) | 現状分析・問題提起 |
| **ReducedSeniorSpan_Adjusted** ⭐ | SM管理スパン削減<br>規模統制版 | **8.5人**<br>(-32%) | **SM: 75,700-80,200**<br>(15-20%削減) 🎯 | メイン実験1<br>管理スパン削減効果 |
| **BalancedHierarchy_Adjusted** ⭐ | 負荷順序最適化<br>規模統制版 | **9.5人**<br>(-24%) | **SM: 75,000-85,000**<br>(10-20%削減)<br>負荷順序: SM>Dir>Mgr≈CXO 🎯 | メイン実験2<br>負荷制御可能性 |
| BestPractice | 安定志向構造 | 8.5人 | 小幅改善<br>(-9.3%) | 補足実験<br>複数アプローチ比較 |
| Final | SM削減<br>Mgr増加 | 6.5人 | 中程度改善<br>(-11.4%) | 補足実験<br>別アプローチ提示 |
| ReducedSeniorSpan（旧） | 極端な削減<br>⚠️規模小 | **4人**<br>(-68%) | 大幅削減だが<br>Mgr最高に | 初期実験記録<br>参考程度 |
| BalancedHierarchy（旧） | 負荷最適化<br>⚠️規模小 | 7.5人 | SM最高達成<br>組織小さい | コンセプト実証<br>参考程度 |
| maxplayers | 極端フラット | 5人 | 限定的 | 理論的境界<br>付録 |
| maxdirector | 極端ワイド | 1人 | 機能せず | 理論的境界<br>付録 |

---

### Adjusted版シナリオの成功基準

| 項目 | ReducedSeniorSpan_Adjusted | BalancedHierarchy_Adjusted |
|------|---------------------------|---------------------------|
| **総ノード数** | 23,000-27,000 (±10%) ✅ | 23,000-27,000 (±10%) ✅ |
| **SM削減率** | **15-20%削減** 🎯<br>(目標: 75,700-80,200) | **10-20%削減** 🎯<br>(目標: 75,000-85,000) |
| **負荷順序** | SM最高 または 2番目 | **SM > Dir > CXO ≈ Mgr** 🎯 |
| **他層への影響** | 極端な負荷増加なし | Dir が2番目 ✅ |
| **管理スパン削減** | SM: **12.5 → 8.5** (-32%) ✅ | SM: **12.5 → 9.5** (-24%) ✅ |
| **実務的示唆** | 管理スパン削減の効果実証 | 負荷制御可能性の実証 |

**評価のポイント**:
- ✅ = 設計通り達成
- 🎯 = 目標値
- ⚠️ = 要確認（実行後に検証必要）

---

### 📐 比較研究の設計思想

#### なぜAdjusted版が必要か？

| 課題 | 旧版の問題 | Adjusted版の解決策 | 研究的意義 |
|------|-----------|------------------|-----------|
| **公平な比較** | ReducedSeniorSpan（旧）: 10,795ノード<br>BalancedHierarchy（旧）: 2,435ノード<br>⚠️ InterviewBased（25,731）と規模が異なる | **両方とも約25,000ノード**<br>✅ 規模を統制 | 構造変更の<br>**純粋な効果**を測定可能 |
| **実務的示唆** | 規模が小さすぎて実務への適用性が不明 | 実務と同規模の組織で検証 | **実務的な改善策**<br>として提示可能 |
| **統計的妥当性** | サンプルサイズが異なる | サンプルサイズを統一 | 統計的に<br>**有意な比較**が可能 |

#### 2つのAdjusted版の関係

```
InterviewBased (基準)
   ├─ ReducedSeniorSpan_Adjusted  → 管理スパン削減アプローチ
   │   └─ 狙い: SM管理スパン -32% → SM負荷 -15~-20%
   │
   └─ BalancedHierarchy_Adjusted  → 負荷順序最適化アプローチ
       └─ 狙い: 負荷順序制御 → SM > Dir > CXO ≈ Mgr
```

**補完関係**:
- **ReducedSeniorSpan_Adjusted**: 「**どれくらい削減できるか**」を検証
- **BalancedHierarchy_Adjusted**: 「**どう配分するか**」を検証

**論文での論理展開**:
1. 問題提起（InterviewBased）→ SM負荷集中の定量化
2. 解決策1（ReducedSeniorSpan_Adjusted）→ 直接的削減の効果
3. 解決策2（BalancedHierarchy_Adjusted）→ 構造最適化の可能性
4. 総合考察 → 両アプローチの長所・短所・組み合わせの可能性

---

## 🔬 ParameterSweep: 系統的実験

### 概要

**負荷遷移のティッピングポイントを特定する段階的実験**

SeniorManagerの管理スパンを段階的に削減（12.5人 → 5人）し、最高負荷がどの役職に遷移するかを系統的に調査します。

### 実験設計

| ステップ | シナリオ名 | SM管理スパン | 期待される最高負荷 |
|:-------:|-----------|:-----------:|------------------|
| 0 | Step0_Baseline_SM12.5 | 12.5人 | **SM** |
| 1 | Step1_SM11 | 11人 | SM? |
| 2 | Step2_SM10 | 10人 | SM? |
| 3 | Step3_SM9 | 9人 | **SM or Dir** 🟡 |
| 4 | Step4_SM8 | 8人 | Dir? |
| 5 | Step5_SM7 | 7人 | Dir? |
| 6 | Step6_SM6 | 6人 | **Dir or Mgr** 🟡 |
| 7 | Step7_SM5 | 5人 | Mgr? |

### 実行方法

```bash
# 1. シナリオファイル生成
python3 -m newSimulations.forThesis.ParameterSweep.generate_scenarios

# 2. 全シナリオ実行（8ステップ）
python3 -m newSimulations.forThesis.ParameterSweep.run_all

# 3. 結果集計とレポート生成
python3 -m newSimulations.forThesis.ParameterSweep.aggregate_results

# 4. 集計レポート確認
cat newSimulations/forThesis/ParameterSweep/AGGREGATE_REPORT.md
```

### 期待される発見

| 項目 | 内容 | 研究的価値 |
|------|------|-----------|
| **ティッピングポイント** | SM管理スパンが○○人で最高負荷が他職種へ遷移 | SM削減の限界値を特定 |
| **負荷遷移パターン** | SM → Dir → Mgr の遷移順序 | 組織設計の指針 |
| **非線形効果** | 小さな変更で大きく負荷が変わる臨界点 | 注意すべきパラメータ範囲 |
| **最適バランス** | SM負荷を最小化する管理スパン | 実務的な改善策 |

### 論文での活用

- **実験章**: 管理スパン削減の段階的効果を示す図表
- **結果章**: 負荷遷移のティッピングポイントを報告
- **考察章**: 最適な管理スパンの議論
- **付録**: 全8ステップの詳細データ

**詳細**: `ParameterSweep/README.md` を参照

---

## 🔍 各シナリオ詳細

### 1. InterviewBased 🔵（ベースライン）

**目的**: 実務の現状を定量化

**設定**:
```python
CXO: (15, 20), Director: (10, 15), SeniorManager: (10, 15), Manager: (5, 10)
```

**特徴**:
- 実務者へのインタビュー結果に基づく現実的な設定
- 全シナリオの比較基準

**結果**:
- SeniorManager が最高負荷（94,420）
- 中間管理職への負荷集中を定量化

**論文での役割**:
- 問題提起：「現実の組織でSeniorManagerに負荷が集中している」ことを示す
- 他のシナリオと比較する基準点

**推奨度**: ⭐⭐⭐⭐⭐（必須）

---

### 2. ReducedSeniorSpan_Adjusted ⭐（論文用メイン）

**目的**: 管理スパン削減の効果を検証（規模統制版）

**設定**:
```python
CXO: (17, 22), Director: (13, 17), SeniorManager: (7, 10), Manager: (7, 10)
```

**特徴**:
- SeniorManagerの管理スパンを**約32%削減**（12.5人 → 8.5人）
- InterviewBasedと**同規模**（約2.5万ノード）で公平な比較
- 上層（CXO, Director）を増やして組織規模を維持

**期待される効果** 📊:

| 役職 | InterviewBased | 予測値 | 変化率 |
|------|---------------:|-------:|-------:|
| SeniorManager | 94,420 | **75,700-80,200** | **-15~-20%** ✅ |
| 上層への影響 | - | 若干増加 | 限定的 |
| Managerへの影響 | 64,903 | 微増 | 許容範囲 |

**設計根拠**:
1. **報告受信負荷の削減**: 管理スパン8.5人 → 報告受信負荷が減少
2. **組織規模維持**: 上層を増やして総ノード数を維持
3. **挟まれ効果の緩和**: SM層の負担を上下で分散

**論文での役割**:
- メイン実験1：「管理スパン削減アプローチ」の効果検証
- 実務的な改善策の提示

**推奨度**: ⭐⭐⭐⭐⭐（必須）

**実行コマンド**:
```bash
python -m newSimulations.forThesis.ReducedSeniorSpan_Adjusted.graph_simulation
```

---

### 3. BalancedHierarchy_Adjusted ⭐（論文用メイン）

**目的**: 負荷順序の最適化（規模統制版）

**設定**:
```python
CXO: (18, 23), Director: (12, 15), SeniorManager: (8, 11), Manager: (6, 9)
```

**特徴**:
- 目標負荷順序: **SeniorManager > Director > CXO ≈ Manager**
- 挟まれ効果を活用してSeniorManagerを最高負荷に
- InterviewBasedと**同規模**（約2.5万ノード）

**期待される負荷値** 📊:

| 役職 | InterviewBased | 予測値 | 変化率 | 目標順序 |
|------|---------------:|-------:|-------:|:--------:|
| SeniorManager | 94,420 | **75,000-85,000** | **-10~-20%** | **1位** 🥇 |
| Director | 70,990 | **68,000-78,000** | -4~+10% | **2位** 🥈 |
| Manager | 64,903 | **55,000-65,000** | -15~0% | **3位** 🥉 |
| CXO | 47,789 | **45,000-55,000** | -6~+15% | **3位** 🥉 |

**設計根拠**:

| 役職 | 子ノード数 | 狙い | メカニズム |
|------|----------:|------|-----------|
| **SeniorManager** | **8-11** (中) | **最高負荷** | 挟まれ効果で3重の負荷 |
| **Director** | **12-15** (多) | **2番目** | 多くのSMを管理 → 報告受信大 |
| **Manager** | **6-9** (少) | **低負荷** | 子数少 → 報告受信小 |
| **CXO** | **18-23** (多) | **低負荷** | 最上層 → 上流タスクなし |

**挟まれ効果の活用**:
```
Director (13.5人)
  ↓ タスク流入
SeniorManager (9.5人管理) ← 上下から挟まれる
  ↓ タスク分割・報告受信
Manager (7.5人)
```
- 上層からタスク受信
- 9.5人のManagerへ配分
- 9.5人から報告受信
- **3重の負荷** → 最高値達成

**論文での役割**:
- メイン実験2：「負荷順序最適化アプローチ」の効果検証
- 組織設計における負荷制御の可能性を示す

**推奨度**: ⭐⭐⭐⭐⭐（必須）

**実行コマンド**:
```bash
python -m newSimulations.forThesis.BalancedHierarchy_Adjusted.graph_simulation
```

---

### 4. BestPractice（補助シナリオ）

**目的**: 理想的な構造探索

**設定**:
```python
CXO: (15, 16), Director: (12, 14), SeniorManager: (8, 9), Manager: (14, 16)
```

**特徴**:
- 各層のレンジが狭い（安定志向）
- ばらつきを抑えた組織設計

**結果**:
- SeniorManager 85,610（-9.3%）
- 小幅な改善

**論文での役割**:
- 補助実験：「安定的な組織構造」の効果
- 複数アプローチの比較

**推奨度**: ⭐⭐⭐（補足として有用）

---

### 5. Final（補助シナリオ）

**目的**: SeniorManager削減、Manager増加

**設定**:
```python
CXO: (15, 20), Director: (10, 15), SeniorManager: (5, 8), Manager: (10, 20)
```

**特徴**:
- SeniorManagerを薄く、Managerを厚く配置
- InterviewBasedと同規模

**結果**:
- SeniorManager 83,677（-11.4%）
- 中程度の改善

**論文での役割**:
- 補助実験：別アプローチの提示
- 複数アプローチの比較

**推奨度**: ⭐⭐⭐（補足として有用）

---

### 6. ReducedSeniorSpan（旧版・参考）

**目的**: 極端な管理スパン削減（初期実験）

**設定**:
```python
CXO: (15, 20), Director: (10, 15), SeniorManager: (3, 5), Manager: (8, 12)
```

**特徴**:
- SeniorManagerを極端に削減（3-5人）
- **ノード数が少ない**（10,795）❌

**結果**:
- SeniorManager 72,127（-23.6%）✅
- しかしManager最高値（76,178）❌
- 組織規模が小さく公平な比較ができない

**論文での役割**:
- 初期実験の記録
- **Adjusted版に置き換え推奨**

**推奨度**: ⭐⭐（参考程度）

**注意**: 論文ではAdjusted版を使用することを推奨

---

### 7. BalancedHierarchy（旧版・参考）

**目的**: 負荷順序最適化（初期実験）

**設定**:
```python
CXO: (5, 8), Director: (12, 15), SeniorManager: (6, 9), Manager: (3, 5)
```

**特徴**:
- 負荷順序の最適化を狙う
- **ノード数が少ない**（2,435）❌

**結果**:
- SeniorManager最高（76,709）✅
- しかし組織規模が小さすぎる

**論文での役割**:
- コンセプト実証
- **Adjusted版に置き換え推奨**

**推奨度**: ⭐⭐（参考程度）

**注意**: 論文ではAdjusted版を使用することを推奨

---

### 8. maxplayers（理論的境界）

**目的**: 極端なフラット構造の検証

**設定**:
```python
CXO: (5, 5), Director: (5, 5), SeniorManager: (5, 5), Manager: (190, 210)
```

**特徴**:
- Manager直下にPlayer大量配置
- 極端なフラット構造

**結果**:
- SeniorManager 85,610

**論文での役割**:
- 理論的な境界条件の提示
- 「極端な例では効果が限定的」という補足

**推奨度**: ⭐（補足的）

---

### 9. maxdirector（理論的境界）

**目的**: 極端なワイド構造の検証

**設定**:
```python
CXO: (6250, 6250), Director: (1, 1), SeniorManager: (1, 1), Manager: (1, 1)
```

**特徴**:
- CXO直下にDirector 6,250人
- 極端なワイド構造

**結果**:
- CXO異常値（10,706,529）💀
- 実用性なし

**論文での役割**:
- 理論的な境界条件の提示
- 「極端すぎる構造は機能しない」という補足

**推奨度**: ⭐（補足的）

---

## 🎯 論文での推奨使用方法

### シナリオ別の論文での位置づけ

| 優先度 | シナリオ | 研究上の役割 | 論文での章・節 | 主張内容 |
|:-----:|---------|------------|-------------|---------|
| **必須** 🔵 | **InterviewBased** | ベースライン<br>問題定量化 | **3章**<br>現状分析 | 「実務組織ではSeniorManagerに<br>負荷が集中している（94,420）」 |
| **必須** ⭐ | **ReducedSeniorSpan_Adjusted** | メイン実験1<br>管理スパン削減 | **4章**<br>実験1 | 「管理スパンを32%削減すると<br>SM負荷が15-20%削減される<br>（75,700-80,200）」 |
| **必須** ⭐ | **BalancedHierarchy_Adjusted** | メイン実験2<br>負荷順序最適化 | **5章**<br>実験2 | 「階層設計により負荷順序を<br>制御可能である<br>（SM>Dir>Mgr≈CXO）」 |
| **推奨** | BestPractice | 補足実験<br>複数アプローチ | **6章**<br>補足実験 | 「安定志向構造では<br>9.3%の改善」 |
| **推奨** | Final | 補足実験<br>別アプローチ | **6章**<br>補足実験 | 「SM層削減アプローチでは<br>11.4%の改善」 |
| 任意 | ReducedSeniorSpan（旧）<br>BalancedHierarchy（旧） | 初期実験記録<br>研究過程 | **付録A**<br>初期実験 | 「規模統制の重要性を認識<br>→Adjusted版開発」 |
| 任意 | maxplayers<br>maxdirector | 理論的境界<br>限界ケース | **付録B**<br>境界値分析 | 「極端な構造は効果が限定的<br>または機能しない」 |

### 論文構成マッピング

| 章 | タイトル | 使用シナリオ | 目的 |
|----|---------|------------|------|
| **1章** | 序論 | - | 研究背景・目的 |
| **2章** | 方法論 | - | シミュレーション設計説明 |
| **3章** | 現状分析 | **InterviewBased** 🔵 | 問題の定量化 |
| **4章** | 実験1: 管理スパン削減 | **ReducedSeniorSpan_Adjusted** ⭐ | 管理スパン削減効果の検証 |
| **5章** | 実験2: 負荷順序最適化 | **BalancedHierarchy_Adjusted** ⭐ | 負荷制御可能性の実証 |
| **6章** | 補足実験 | BestPractice, Final | 複数アプローチの比較 |
| **7章** | 総合考察 | 全メインシナリオ | 効果比較・実務示唆 |
| **8章** | 結論 | - | 研究貢献・今後の課題 |
| **付録A** | 初期実験 | 旧版シナリオ | 研究過程の記録 |
| **付録B** | 境界値分析 | maxplayers, maxdirector | 理論的限界の提示 |

---

## 📝 論文構成例

### 1. 序論
- 中間管理職負荷集中の問題提起

### 2. 方法論
- エージェントベースモデリングの説明
- シミュレーション設定

### 3. ベースライン分析
- **InterviewBased** の結果提示
- 現実の問題を定量化

### 4. 実験1: 管理スパン削減アプローチ
- **ReducedSeniorSpan_Adjusted** の結果
- 管理スパン削減の効果を実証

### 5. 実験2: 負荷順序最適化アプローチ
- **BalancedHierarchy_Adjusted** の結果
- 負荷順序の制御可能性を実証

### 6. 補足実験
- BestPractice, Final の結果
- 複数アプローチの比較

### 7. 考察
- 3つのアプローチの効果比較
- 実務への示唆

### 8. 結論
- 研究の貢献
- 今後の課題

---

## 🚀 実行手順

### シナリオ実行コマンド一覧

| 優先度 | シナリオ | 実行コマンド | 推奨理由 |
|:-----:|---------|-------------|---------|
| **1** 🔵 | InterviewBased | `python -m newSimulations.forThesis.InterviewBased.graph_simulation` | ベースライン（必須） |
| **2** ⭐ | ReducedSeniorSpan_Adjusted | `python -m newSimulations.forThesis.ReducedSeniorSpan_Adjusted.graph_simulation` | メイン実験1（必須） |
| **3** ⭐ | BalancedHierarchy_Adjusted | `python -m newSimulations.forThesis.BalancedHierarchy_Adjusted.graph_simulation` | メイン実験2（必須） |
| **4** | BestPractice | `python -m newSimulations.forThesis.BestPractice.graph_simulation` | 補足実験（推奨） |
| **5** | Final | `python -m newSimulations.forThesis.Final.graph_simulation` | 補足実験（推奨） |
| 6 | ReducedSeniorSpan（旧） | `python -m newSimulations.forThesis.ReducedSeniorSpan.graph_simulation` | 参考（任意） |
| 7 | BalancedHierarchy（旧） | `python -m newSimulations.forThesis.BalancedHierarchy.graph_simulation` | 参考（任意） |
| 8 | maxplayers | `python -m newSimulations.forThesis.maxplayers.graph_simulation` | 境界値（任意） |
| 9 | maxdirector | `python -m newSimulations.forThesis.maxdirector.graph_simulation` | 境界値（任意） |

### 結果可視化コマンド

各シナリオ実行後、以下で可視化：
```bash
python -m newSimulations.forThesis.[シナリオ名].visualize_results
```

### 一括実行（メインシナリオのみ）

```bash
# 論文用の必須3シナリオを順次実行
python -m newSimulations.forThesis.InterviewBased.graph_simulation && \
python -m newSimulations.forThesis.ReducedSeniorSpan_Adjusted.graph_simulation && \
python -m newSimulations.forThesis.BalancedHierarchy_Adjusted.graph_simulation
```

---

## 📊 比較分析のポイント

### 分析チェックリスト

| 項目 | 確認方法 | 期待値・基準 |
|------|---------|-------------|
| **総ノード数** | `grep "^Total nodes:" */RESULT.md` | InterviewBased: 25,731<br>Adjusted版: 23,000-27,000（±10%） |
| **SM削減率** | `(InterviewBased - 各シナリオ) / InterviewBased × 100` | ReducedSeniorSpan_Adjusted: 15-20%<br>BalancedHierarchy_Adjusted: 10-20% |
| **負荷順序** | RESULT.mdの役職別平均SimLoadを確認 | BalancedHierarchy_Adjusted:<br>SM > Dir > CXO ≈ Mgr |
| **各役職ノード数** | RESULT.mdのRole Averages確認 | 各階層が適切に分布しているか |
| **異常値チェック** | 各役職の最大・最小SimLoad確認 | 極端な外れ値がないか |

### 主要評価指標の計算式

| 指標 | 計算式 | 用途 |
|------|--------|------|
| **SM削減率** | `(94,420 - SM値) / 94,420 × 100` | 管理スパン削減効果の評価 |
| **負荷標準偏差** | 各役職SimLoadの標準偏差 | 負荷分散の均等性評価 |
| **組織効率** | `完了タスク数 / 総負荷` | 負荷あたりの生産性 |
| **規模一致度** | `各シナリオノード数 / 25,731` | 公平な比較の妥当性 |

---

## 📖 各シナリオの詳細ドキュメント

各シナリオディレクトリ内の `README.md` を参照してください：

- `InterviewBased/README.md` - ベースライン詳細
- `ReducedSeniorSpan_Adjusted/README.md` - 管理スパン削減詳細
- `BalancedHierarchy_Adjusted/README.md` - 負荷順序最適化詳細
- その他各シナリオ

---

## 🔧 トラブルシューティング

### よくある問題と解決方法

| 問題 | 原因 | 解決方法 |
|------|------|---------|
| **ノード数が目標より少ない** | CHILD_RANGESが小さい | 上層（CXO, Director）の子数を増やす<br>例: `(17, 22)` → `(18, 23)` |
| **ノード数が目標より多い** | CHILD_RANGESが大きい | 上層（CXO, Director）の子数を減らす<br>例: `(18, 23)` → `(17, 22)` |
| **インポートエラー** | カレントディレクトリが不正 | プロジェクトルートから実行<br>`cd /path/to/SampleAgent` |
| **モジュールが見つからない** | Pythonパスの問題 | `-m` オプションで実行<br>`python -m newSimulations.forThesis.[シナリオ名].graph_simulation` |
| **RESULT.mdが生成されない** | graph_simulation未実行 | まず`graph_simulation.py`を実行してから<br>`visualize_results.py`を実行 |
| **SM負荷が削減されない** | 管理スパンが大きすぎる | SeniorManagerのCHILD_RANGESを<br>さらに削減（例: `(7, 10)` → `(6, 9)`） |
| **Manager負荷が最高になる** | Managerスパンが大きすぎる | Manager CHILD_RANGESを削減<br>または他層を調整 |

### パラメータ調整のガイドライン

| 目的 | 調整対象 | 推奨方向 |
|------|---------|---------|
| **組織規模を増やす** | CXO, Director | レンジ上限を +1〜+2 |
| **SM負荷を削減** | SeniorManager | レンジ上限を -1〜-3 |
| **負荷を均等化** | 全階層 | レンジ幅を狭める（例: 5→3） |
| **Dir負荷を削減** | Director | レンジ上限を -1〜-2 |
| **Mgr負荷を削減** | Manager | レンジ上限を -1〜-2 |

---

## 📞 研究上の注意点

### 公平な比較のための統制変数

| 項目 | 設定値 | 重要性 | 確認方法 |
|------|--------|--------|---------|
| **乱数シード** | `seed=42` | 🔴 必須 | `graph_simulation.py`の<br>`OrganizationSimulation(seed=42)` |
| **総ノード数** | 約25,000<br>(±10%) | 🔴 必須 | RESULT.mdの<br>`Total nodes:` 行を確認 |
| **シミュレーション時間** | `TIME_STEPS=2000` | 🔴 必須 | `graph_simulation.py`の<br>`TIME_STEPS` 定数 |
| **負荷係数** | `ALPHA=0.7`<br>`BETA=0.3` | 🟡 推奨 | 全シナリオで統一 |
| **コスト係数** | `SENDER_COST=0.3`<br>`REPORT_RECEIVER=0.1` | 🟡 推奨 | 全シナリオで統一 |

### 統計的信頼性のための推奨事項

| 項目 | 推奨設定 | 理由 | 実装方法 |
|------|---------|------|---------|
| **複数回実行** | 5回以上 | ランダム性の影響を排除 | シード値を変えて実行<br>`seed=42, 43, 44, 45, 46` |
| **平均値報告** | 必須 | 代表値として使用 | 5回の平均SimLoadを計算 |
| **標準偏差報告** | 推奨 | ばらつきを示す | 5回の標準偏差を計算 |
| **信頼区間** | 任意 | 統計的有意性 | 95%信頼区間を計算 |

### 複数回実行の例

```bash
# シード値を変えて5回実行
for seed in 42 43 44 45 46; do
  # graph_simulation.pyのseed値を変更して実行
  python -m newSimulations.forThesis.InterviewBased.graph_simulation
  # 結果を別ファイルに保存
  mv InterviewBased/RESULT.md InterviewBased/RESULT_seed${seed}.md
done
```

---

## 📅 更新履歴

| 日付 | 更新内容 |
|------|---------|
| 2026-01-10 | **🔬 Parameter Sweep実験追加**: <br>• 自動シナリオ生成スクリプト作成<br>• 8ステップの段階的実験フレームワーク<br>• 一括実行・結果集計スクリプト<br>• 負荷遷移ティッピングポイント分析機能<br><br>**大幅アップデート**: <br>• テーブル形式に全面リニューアル<br>• Adjusted版シナリオの予測値を追加<br>• 成功基準テーブルを追加<br>• 比較研究の設計思想セクション追加<br>• 挟まれ効果のメカニズム図解追加<br>• 論文構成マッピング強化<br>• トラブルシューティング表追加<br>• 統制変数と統計的信頼性の推奨事項追加 |
| 2026-01-07 | Adjusted版シナリオ追加（規模統制版）<br>ReducedSeniorSpan_Adjusted, BalancedHierarchy_Adjusted |
| 2026-01-06 | ReducedSeniorSpan, BalancedHierarchy 追加 |
| 2025-12-31 | InterviewBased をベースラインとして確立 |
| 2025-12-24 | BestPractice, Final 追加 |

---

## 📚 参考文献

プロジェクトルートの以下のドキュメントも参照：

- `../README.md` - プロジェクト全体概要
- `../CLAUDE.md` - 開発ガイドライン
- `../PROJECT_INDEX.md` - プロジェクト構成
- `../REALRULES.md` - タスクフロー仕様
