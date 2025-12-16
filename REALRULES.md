# REALRULES - スケーラブル現場ルール仕様

本研究のゴールは「中心性指標とシミュレーション結果を組み合わせ、中間層の負荷を軽減する最適な組織構成を見いだす」ことです。本ドキュメントでは、どのようなグラフ構造が入力されても同じアルゴリズムで負荷を算出できるよう、データ入力形式・タスク処理ルール・拡張方針を統合的に示します。

---

## 1. 入力データ仕様

### 1.1 グラフ構造

- **推奨フォーマット**: NetworkX がそのまま読み込める `node_link JSON` または `edge list CSV`。研究では隣接行列を併用しやすいので、`csv/adjacency_matrix.csv` のように `N×N` 行列を保存してもよい。
- **要素**:
  - `nodes`: `node_id`, `label`, `role`, `level`, `org_unit`（必須4属性）
  - `edges`: `source`, `target`, `weight`（遷移確率や業務頻度を重みとして持てる）
  - 隣接行列にする場合は行列とは別にノード順序と属性のマッピングファイルを用意する。
- **補足**: 入力グラフは木／DAG／一般グラフいずれも可。シミュレータ側で `DiGraph` として読み込み、REAL RULES に従って遷移を制限する。

### 1.2 タスクパラメータ

- `tasks.yaml` (例):
  ```yaml
  task_categories:
    - name: feature_dev
      complexity: 4
      stakeholders: 3
      comms_cost: 2
      escalation_threshold: 12
      allowed_roles: ["Director", "Manager", "TeamLead", "Senior"]
    - name: audit
      complexity: 2
      stakeholders: 5
      comms_cost: 4
      escalation_threshold: 10
      allowed_roles: ["CEO", "CTO", "Director"]
  escalation_probability: 0.05
  ```
- 1タスク = `weight`, `requires_escalation`, `current_node` を持つ。重みは `complexity * 0.4 + stakeholders * 0.4 + comms_cost * 0.2` をベースに、カテゴリーごとに係数調整可能。

### 1.3 シナリオ設定

- `scenario.yaml` で組織構造スケールを切り替え：
  ```yaml
  graph_source: data/org_chart_node_link.json
  adjacency_matrix: data/org_chart_adj_matrix.csv   # 任意
  task_config: configs/tasks.yaml
  simulation_steps: 100
  num_tasks: 500
  forest_subgraphs:
    - name: product_A
      node_ids: [0-150]
    - name: product_B
      node_ids: [151-320]
  cross_links:
    - from: product_A.Manager
      to: product_B.Manager
      weight: 0.1
  ```
- こうした設定を CLI から指定し、どのグラフでも同じ `ResearchSimulator` を動かす。

---

## 2. タスクフローと移動ルール

### 2.1 基本フロー

- **単方向が標準**: 上層 → 中間層 → 実行層で渡り、完了後は下層でクローズ。
- **報告/完了フロー**: 実行層 → 中間層 → （必要に応じて）上層。直接上層へ戻る経路は禁止。
- **エスカレーション**: `requires_escalation=True` or `weight >= escalation_threshold` の場合のみ、上層へ戻る特別ルートを開く。

### 2.2 役割別制約（遷移テーブル）

| 現在の役割 | 遷移可能な役割 | 備考 |
|------------|----------------|------|
| CEO/CTO | Director | 配賦専用。実装タスクには直接関与しない |
| Director/Manager | 上位(CEO/CTO)、同階層、下位(TeamLead, Senior) | エスカレーション判断と再配分を担う |
| TeamLead/Senior/Junior | 同階層または直上のみ | 上層との直接接続は持たせない |

REAL RULES では、グラフがどんな形でも役職属性を見て遷移を制御するため、入力データに `role` と `level` が必要。

### 2.3 重み付き負荷計測

- 負荷記録: `node_load[node_id] += task.weight`。訪問回数ではなく累積重みで評価。
- 追加要素:
  - `communication_penalty`: エスカレーションやクロスリンクを経由した際に加算。
  - `blocker_delay`: タスクが一定ステップ停滞すると、該当ノードに調整タスク（高 `comms_cost`）を生成。

---

## 3. 中心性指標との統合

- グラフ読み込み後に `betweenness`, `closeness`, `degree`, `eigenvector` などを算出し、各ノードの `role`, `level` と紐付ける。
- シミュレーション結果の `node_load` と中心性を結合し、階層ごとの「中心性×負荷」ヒートマップや回帰分析を実施。
- 任意グラフ入力で中心性計算が可能なよう、構造上の制約は設けない。ただし REAL RULES の遷移表は役職属性に依存するため、入力に役職情報を含めることが必須。

---

## 4. スケール対応とForest構造

- サブツリー（部門・プロダクトライン）を `forest_subgraphs` で定義し、複数グラフを合成しても REAL RULES が機能するようにする。
- `cross_links` を使い、部門間の調整ラインを疎な有向エッジとして追加。重みで連携頻度を表現し、負荷計測に `communication_penalty` を加算する。
- シナリオ比較は「構造パラメータ（ノード数・分岐パターン・クロスリンク数）」「タスク重み分布」「エスカレーション率」を共通指標で記録する。

---

## 5. 実装チェックリスト

1. **汎用グラフ読み込み**: node_link/edge list/隣接行列を読み込む IO 層を用意。ノード属性（role, level, org_unit）とタスク設定のバリデーションを行う。
2. **タスクエージェント化**: `RealTask` クラスを実装し、各タスクが重み・状態・カテゴリーを保持する。
3. **遷移エンジン**: 役職ベースの遷移テーブルを実装し、任意のグラフでも同じロジックで遷移を決める。エスカレーション時は特別ハンドラを呼び出す。
4. **負荷集計**: `node_load` を辞書で保持し、タスク移動時に重みを加算。分析フェーズで中心性指標と結合する。
5. **スケール設定**: CLI オプションまたは設定ファイルでシナリオを切り替えられるようにし、Forest構造・クロスリンクを含む複雑な入力でも処理できるようにする。
6. **レポートテンプレート**: 各階層の `平均負荷`, `最大負荷`, `中心性との相関`, `エスカレーション率` を標準アウトプットとしてまとめる。

これらを実装すれば、どのような組織グラフでも共通アルゴリズムで負荷を算出し、中心性分析と組み合わせて中間層の最適化方針を導き出せる「REAL RULES」仕様となります。
