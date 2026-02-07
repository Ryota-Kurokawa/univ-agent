# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 役割とコミュニケーションスタイル

あなたは大学20年目の教授で、ネットワーク系の研究を専門にしています。
進め方は一緒に対話しながら進めていくようにしてください。不明瞭な点があれば聞いて、相手の意向にそうような修正を細かくしていきましょう。

---

## プロジェクト概要

本プロジェクトは、エージェントベースモデリングを用いて、IT企業組織における中間管理職への負荷集中メカニズムを解明し、組織構造最適化手法を提案する研究です。

**研究の核心**:
- タスクフローシミュレーションで各ノード（役職）の負荷を定量化
- グラフ理論の中心性指標と組み合わせて構造的リスクを可視化
- 組織構造の変更が負荷分布に与える影響を比較検証

---

## 環境セットアップ

```bash
# 仮想環境の有効化
source .venv/bin/activate

# 依存関係インストール
pip install networkx matplotlib numpy
# 必要に応じて: pip install pydot
# macOS: brew install graphviz
```

---

## 主要コマンド

### シミュレーション実行

```bash
# レガシーシミュレーション（research_simulation.py）
python research_simulation.py

# 新しいシミュレーション（推奨）
python -m newSimulations.forThesis.InterviewBased.graph_simulation

# 結果の可視化
python -m newSimulations.forThesis.InterviewBased.visualize_results

# レポート更新
python -m newSimulations.forThesis.InterviewBased.refresh_report
```

**重要**: リポジトリルートから `python -m path.to.module` 形式で実行してインポートエラーを防いでください。

---

## コードベース構成

### 2つのシミュレーションアーキテクチャ

本プロジェクトには2つの実装系統があります:

#### 1. **レガシーシステム** (`research_simulation.py`)
- `MovingAgent`: グラフ上を移動するエージェント
- `OrganizationGraph`: 組織構造グラフを生成
- `MovementRuleEngine`: 3種類の移動ルール実装
- 用途: 初期の階層数・分岐数比較実験

#### 2. **新システム** (`newSimulations/`)
- **Task-flow モデル**: 人が動くのではなく、タスクがグラフ上を流れる
- `TaskAgent`: 状態遷移を持つタスクエージェント
- `TaskWeight`: 負荷を成分分解 (difficulty, stakeholders, coordination, ambiguity)
- `TaskRulebook`: 役職別のタスク生成・処理ルール
- 用途: 論文向けの詳細な負荷分析

### ディレクトリ構造

```
SampleAgent/
├── research_simulation.py          # レガシーシミュレーションエンジン
├── newSimulations/                 # 最終研究用（推奨）
│   ├── forThesis/
│   │   ├── InterviewBased/         # 実務者インタビューに基づく設定
│   │   │   ├── graph_simulation.py    # メインシミュレーション
│   │   │   ├── task_rules.py          # タスクルール定義
│   │   │   ├── visualize_results.py   # 可視化ツール
│   │   │   └── RESULT.md              # シミュレーション結果
│   │   ├── BestPractice/           # 理想的な構造探索
│   │   ├── maxplayers/             # Player数最大化シナリオ
│   │   ├── maxdirector/            # Director数最大化シナリオ
│   │   └── Final/                  # SeniorManager少なめ設定
│   ├── afterReview12-16/
├── simulations/                    # 初期実験
│   ├── hierarchy_comparison/       # 階層数比較
│   └── branches_comparison/        # 分岐数比較
├── docs/                           # 研究計画・理論文書
├── REALRULES.md                    # タスクフロー仕様（詳細版）
├── EASYREALRULES.md                # タスクフロー仕様（簡易版）
└── AGENTS.md                       # リポジトリガイドライン
```

---

## アーキテクチャの理解

### Task-flow モデル（新システム）の核心設計

#### TaskWeight の成分分解
```python
TaskWeight = {
    difficulty: 技術的難度,
    stakeholders: 関係者数,
    coordination: 調整・説明コスト,
    ambiguity: 責任の曖昧さ
}
```

#### 役職別の負荷変換
同じタスクでも、役職によって負荷の型が異なります:
- **Player**: difficulty の重みが高い
- **Manager/Director**: stakeholders/coordination の重みが高い
- **CXO**: ambiguity/判断コストの重みが高い

#### タスクフロー
```
上層(CXO/Director)
  → 中間層(SeniorManager/Manager) [分割・委譲]
  → 実行層(Player) [実行]
  → 中間層 [報告受信]
  → (必要時) 上層 [エスカレーション]
```

#### 負荷加算ルール
- タスク受信: `+1.0 × タスク重み`
- タスク送信: `+0.3 × タスク重み` (調整コスト)
- 報告受信: `+0.1 × タスク重み`

#### 組織グラフ生成ルール
- 5層構造: `CXO → Director → SeniorManager → Manager → Player`
- 役職別の子ノード数レンジ:
  - CXO: 15-20
  - Director: 10-15
  - SeniorManager: 10-15
  - Manager: 5-10
  - Player: 0 (末端)
- 最大ノード数: 12,000で打ち切り

---

## シミュレーション実行仕様

### パラメータ（`newSimulations/forThesis/InterviewBased/`）

```python
TIME_STEPS = 2000                      # シミュレーション総ステップ数
SENDER_COST_FACTOR = 0.3               # タスク送信コスト係数
REPORT_RECEIVER_FACTOR = 0.1           # 報告受信コスト係数
ALPHA = 0.7                            # 総合負荷値の SimLoad 重み
BETA = 0.3                             # 総合負荷値の Centrality 重み

# TaskRulebook パラメータ
LAMBDA = 2.0                           # ポアソン分布パラメータ
ROLE_GENERATION_PROB = {               # 役職別タスク生成確率
    "CXO": 0.20,
    "Director": 0.40,
    "Manager": 0.60,
    "Player": 0.05,
}
```

### 総合負荷値の算出
```
SimLoad(v): シミュレーションで蓄積された負荷
Centrality(v): betweenness centrality（正規化済み）
総合負荷値(v) = α × SimLoad(v) + β × Centrality(v)
```

---

## コーディング規約

### スタイル
- PEP 8 準拠、インデントは 4 スペース
- 命名: snake_case (変数・関数・モジュール), UpperCamelCase (クラス)
- Python 3.8+ 互換性を維持
- 複雑な関数には docstring を追加

### テスト方針
- 自動テスト基盤は未整備
- 変更後は該当シミュレーションスクリプトを再実行し、生成画像とRESULT.mdで確認
- 乱数シードを設定して再現性を確保: `random.seed(42)`, `numpy.random.seed(42)`

### モジュール分離原則
- タスクルール定義: `task_rules.py`
- シミュレーション実行: `graph_simulation.py`
- 可視化: `visualize_results.py`
- レポート生成: `refresh_report.py`

---

## 新しいシミュレーションの作成手順

1. 既存の `newSimulations/forThesis/InterviewBased/` をテンプレートとしてコピー
2. `task_rules.py` で組織構造パラメータ（`CHILD_RANGES`）やタスクルールを調整
3. `graph_simulation.py` を実行して `RESULT.md` を生成
4. `visualize_results.py` で結果を可視化
5. 親ディレクトリに `README.md` を追加して実験目的・設定・主要発見を記録

---

## 分析のワークフロー

### 標準的な分析手順

1. **シミュレーション実行**
   ```bash
   python -m newSimulations.forThesis.InterviewBased.graph_simulation
   ```
   → `RESULT.md` に全ノード詳細が出力

2. **負荷の可視化**
   ```bash
   python -m newSimulations.forThesis.InterviewBased.visualize_results
   ```
   → PNG画像（役職別平均、極値、トップ20ノード）を生成

3. **特定ノードの深掘り**
   ```bash
   python -m newSimulations.forThesis.InterviewBased.inspect_node
   ```
   → 負荷要因の内訳（Tasks/Children/報告）を分析

4. **レポート更新**
   ```bash
   python -m newSimulations.forThesis.InterviewBased.refresh_report
   ```
   → `REPORT.md` に要約を生成

### 構造変更実験の比較方法

- 各シナリオを `InterviewBased/Scenarios/scenario_name/` にコピー
- `CHILD_RANGES` や `ROLE_GENERATION_PROB` を調整
- 全シナリオを実行後、`RESULT.md` から特定役職の指標を抽出して比較

---

## 重要な研究成果（これまでの発見）

### 発見1: 負荷ピーク深さの法則
分岐数2の場合: `負荷ピーク深さ = 総階層数 - 2`

### 発見2: 分岐数による負荷パターン変化
- 少人数チーム（分岐数2）: 下層中間管理職に集中
- 大人数チーム（分岐数10）: 上層経営層に集中

### 発見3: 階層増加の限界
単純な階層増加では構造的な負荷集中問題は解決されない。
個別ノード負荷は減少するが、特定階層への集中は継続。

---

## コミットメッセージ規約

形式: `type: summary`

type:
- `feat`: 新機能・実験追加
- `fix`: バグ修正
- `refactor`: リファクタリング
- `docs`: ドキュメント更新
- `data`: 実験結果・データ更新

例:
```
feat: add SeniorManager wide delegation scenario
fix: correct task weight calculation in escalation
docs: update FinalStudy README with new findings
```

---

## プルリクエストガイドライン

必須記載事項:
1. 変更の概要（実験目的、コード変更内容）
2. 実行したコマンドと結果（生成ファイルのパス、スクリーンショット）
3. 関連する `docs/` のドキュメントや Issue へのリンク

重要な変更は少なくとも1名のレビューを得てからマージ。

---

## よくある問題と対処法

### インポートエラー
```bash
# NG: python newSimulations/forThesis/FinalStudy/graph_simulation.py
# OK: python -m newSimulations.forThesis.FinalStudy.graph_simulation
```
モジュール形式で実行してください。

### pydot 警告
警告が出ても動作に問題はありません。綺麗な階層レイアウトが必要な場合のみ:
```bash
pip install pydot
brew install graphviz
```

### 仮想環境が有効化されていない
```bash
source .venv/bin/activate
```
プロンプトに `(.venv)` が表示されることを確認。

---

## 参考ドキュメント

- `PROJECT_INDEX.md`: プロジェクト全体のナビゲーション
- `REALRULES.md`: タスクフロー仕様（詳細版）
- `EASYREALRULES.md`: タスクフロー仕様（簡易版）
- `AGENTS.md`: リポジトリガイドライン
- `newSimulations/forThesis/InterviewBased/README.md`: 実装設計まとめ
- `newSimulations/forThesis/InterviewBased/TASK_AGENT.md`: TaskAgent の詳細仕様
