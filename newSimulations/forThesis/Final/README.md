
# Final シナリオ概要

本ディレクトリでは SeniorManager 層の子ノードを半分（5〜8人）に抑え、Manager 層は Player を倍の 10〜20 人抱える構造を試験します。  
これにより、Manager/Player 側にタスクを多めに割り振りつつ中間層の負荷を下げられるかを評価します。

- 実行方法
  ```bash
  source .venv/bin/activate
  cd newSimulations/Final
  python graph_simulation.py
  ```
  生成された `RESULT.md`, `REPORT.md`, `SORTEDRESULT.md` はこのフォルダに出力されます。`refresh_report.py` / `visualize_results.py` も利用可能です。

---

# 組織タスク負荷シミュレーション：実装設計まとめ（Draft）

本ドキュメントは、
**「組織内タスクの流れと負荷集中をシミュレーションし、役職別の総合負荷値を算出する」**
という目的に向けた、実装フェーズの共通理解をまとめたものです。

---

## 1. 実装のゴール（再確認）

### 目的

- 組織構造とタスクルールを入力として、
- 各ノード（人・役職）ごとの **総合負荷値** を出力する。

### 入力

- 組織構造（隣接行列 / 有向グラフ）
- ノード属性 
  - role: CXO / Director / Manager / Player など
  - subordinate_count など

### 出力

- 各ノードの 
  - シミュレーション由来の負荷（SimLoad）
  - 構造由来の指標（中心性など）
  - それらを統合した **総合負荷値**

---

## 2. 実装で意識すべき2つのコア要素

### ① Task に移動ルールを設定した Agent（モデル）

基本方針
- **人が動くのではなく、Task がグラフ上を流れる**
- ノード（人・役職）は Task を 
  - 受け取り
  - 分割し
  - 下に渡し
  - 報告・エスカレーションを行う

採用モデル
- **Task-flow（Token Passing）モデル**
  - 上層 → 中間層 → 実行層
  - 実行完了後は中間層へ報告
  - 一部は例外的に上層へエスカレーション

※ 立ち話・突発タスクは「通常ルート外の生成イベント」として扱う。

---

### ② TaskWeight（タスクの重さ）の定義

TaskWeightは1つの数値ではなく、成分分解して持つ

```text
TaskWeight = {
  difficulty: 難しさ,
  stakeholders: 関係者数（次数）,
  coordination: 調整・説明コスト,
  ambiguity: 責任の曖昧さ（隙間仕事）
}
```

インタビュー反映
- Player の難易度を 10 とすると
- 中間管理職は 20〜30 相当
- 「時間は短いが重い」「次数がきつい」を表現するため

---

## 3. TaskWeight → ノード負荷への変換

同じ Task でも、役職によって負荷の型が異なる。

```text
NodeLoad += RoleCost(role, task_components)
```

### 例

- Player 
  - difficulty の重みが高い
- Manager / Director 
  - stakeholders / coordination の重みが高い
- CXO 
  - ambiguity / 判断コストの重みが高い

---

## 4. タスクの種類（最低限）

インタビューから抽出されるタスクタイプ：
1. **Top-down Task**
   - CXO / 上層起点
   - 全社対応・方針・重要判断
2. **Design / Thinking Task**
   - 中間層起点
   - 理想設計・問題言語化
3. **Execution Task**
   - 実行層起点・担当
   - 実作業
4. **Random / Interrupt Task**
   - 立ち話・社長から突然・面接対応など
   - 非階層的に発生

---

## 5. タスク生成ルール（必須）

- 役職ごとにタスク生成確率が異なる
- タスクタイプも役職依存

```text
P(task発生 | CXO) = 低いが重い
P(task発生 | Manager) = 高い
P(task発生 | Player) = 低い（基本は受信専用）
```

---

## 6. タスクの移動・処理ルール

### 通常フロー

- 上層 → 中間層 → 実行層
- 実行完了後は中間層に報告

### 分割（Delegation）

- 中間管理職はタスクを 50〜70% 下に委譲
- 分割時に **分割コスト** が自分に発生

### 報告

- 実行層 → 中間層への報告は必須
- 軽いが数が多い負荷

### エスカレーション

- TaskWeight が閾値を超えた場合、 
  - 低確率（例：5%）で上層に戻す
- 「判断が必要」「難しすぎる」ケースに対応

---

## 7. 部下人数と負荷の関係

- 適正人数（例：10〜15人）を超えると
- 調整コストが **非線形に増加**

```text
if subordinate_count > threshold:
    CoordinationCost ∝ (subordinate_count - threshold)^2
```

---

## 8. タスクの状態遷移（実装安定化のため）

Task は状態を持つ：

```text
Created
→ Delegated
→ InProgress
→ Done
→ Reported
→ (optional) Escalated
```

---

## 9. 総合負荷値の定義（最終アウトプット）

```text
SimLoad(v): シミュレーションで蓄積された負荷
Centrality(v): グラフ構造由来の中心性（正規化）

総合負荷値(v) = α * SimLoad(v) + β * Centrality(v)
```

---

## 10. 実装フェーズの優先順

1. Task クラス（成分分解された TaskWeight）
2. Task の状態遷移とルーティングルール
3. ベースライン組織でのシミュレーション
4. ロール別負荷プロファイルの出力
5. 構造変更シナリオ（冗長化・ダウンサイジング）

---

この設計をベースに、
**「構造を変えると、誰の負荷がどう変わるか？」**
を定量的に検証していく。

---

## afterReview12-16 追加ルール

- Director / Manager がタスクを子ノードへ委譲する際は、子ノードとその孫ノードの数に応じて**比率配分**します。
  - 子ノード自身を価値 1、孫ノードを価値 1/2 として合計値を計算し、全子ノードの値で正規化した割合をタスク重みに掛けます。
  - これにより **すべての子ノードが必ず一部のタスクを受け取る** 仕様になります。
- 生成された結果は `RESULT.md` に Markdown テーブル（役職平均 + ノード詳細）として書き出され、ターミナルには表示しません。
- 組織グラフは `CXO → Director → SeniorManager → Manager → Player` の 5 層構造を自動生成し、上司 1 人あたりの部下数は  
  `Director: 15〜20, SeniorManager: 10〜15, Manager: 10〜15, Player: 5〜10` のレンジから乱択されます（最大 12,000 ノードで打ち切り）。

---

## 実装ファイル一覧

- `task_rules.py`  
  TaskWeight のサンプリング、TaskAgent の状態遷移、役職別コスト変換をまとめたルールブック。外部から呼び出して Task を生成・評価できます。
- `graph_simulation.py`  
  NetworkX で組織グラフを構築し、TaskAgent を流しながら SimLoad と中心性を計測します。以下で実行してください。

  ```bash
  python3 -m newSimulations.afterInterview.graph_simulation
  ```

  単一シミュレーションで `SimLoad / Centrality / Score` を出力します。  
  （事前に `pip install networkx` を行ってください。）

- `TASK_AGENT.md`  
  TaskAgent の属性・状態遷移・負荷換算ロジックを詳説した補助ドキュメント。タスクのライフサイクルを把握する際に参照してください。

## 実装仕様（必須ルール）

- **グラフ**
  - 有向グラフを使用する
  - 隣接行列（0/1）を入力とする
  - 実装には NetworkX の `DiGraph` を用いる

- **役職レベル（role_level）**
  - CXO = 0  
  - Director = 1  
  - Manager = 2  
  - Player = 3  
  ※ 数値が小さいほど階層が高い

- **シミュレーション設定**
  - 総ステップ数: `T = 2000`
  - 1ステップあたりに生成されるタスク数は  
    ポアソン分布 `Poisson(λ = 2)` に従う

- **タスク生成ルール**
  - 各ノードは、各ステップごとに以下の確率でタスクを生成する  
    - CXO: 0.2  
    - Director: 0.4  
    - Manager: 0.6  
    - Player: 0.05  
  - 生成されるタスクの種類（Top-down / Design / Execution / Random など）は  
    役職に応じた分布テーブルで決定する（別途定義）

- **タスクの分割（Delegation）**
  - 現在の役職が `Director` または `Manager` の場合、タスクを分割する
  - 分割率（委譲率）: `delegate_ratio = 0.6`
  - タスクは `k = 3` 個のサブタスクに分割される
  - 各サブタスクの重さの合計は、元のタスクの重さと等しくなる
  - 分割時、委譲したノードには以下の分割コストが加算される  
    - `split_cost = 0.2 × 元タスクの重さ`

- **タスクのルーティング**
  - 通常ルート  
    - 上位層 → 中間層 → 実行層  
    - 実行完了後、タスクは中間層へ報告として戻る
  - エスカレーション  
    - タスクの総重量が閾値（`threshold = 30`）を超えた場合、  
      確率 `p = 0.05` で上位ノードへエスカレーションする
  - 遷移先ノードが複数ある場合  
    - 確率 0.6 で **現在の SimLoad が最も小さいノード** を選択  
    - それ以外（確率 0.4）はランダムに選択する

- **負荷の加算ルール（Load charging）**
  - タスクを **受け取ったノード** には  
    - `+1.0 × タスクの重さ`
  - タスクを **渡したノード** には  
    - 調整・説明コストとして `+0.3 × タスクの重さ`
  - 実行完了後の **報告** によって  
    - 中間層の受信ノードに `+0.1 × タスクの重さ` を加算する


- 負荷の分解: newSimulations/FinalStudy/RESULT.md の SeniorManager_205 行を起点に、Tasks・Children・W（SimLoad の各要因）の推移を確認し、負荷が上流/下流どちらのタスク流入で膨らんでいるのかを切り分ける。必要なら graph_simulation.py にログを入れて SeniorManager 層内のタスク分配比率を可視化する。
  
- 構造パラメータの調整: まずは最小限の構造改修で効果を見たいので、SeniorManager→Manager の CHILD_RANGES だけを局所的に調整してみる。例: SeniorManager の子数レンジを 10–15 から 12–16 に寄せる or Manager の子数を 5–10 から 8–12 に増やすなど、特定層の扇状度をコントロールしてタスクが薄く広がるか検証する。
  
- 再割り当て/再配線の実験: SeniorManager_205 にぶら下がる Manager をランダムに他の SeniorManager に付け替える “shuffle” スクリプトを導入し、各試行後にRESULT.md を比較。既存構造を大きく変えず、局所的な再配線が負荷を緩和するかを測れる。

- タスク生成ルールの微調整: SeniorManager 層の rulebook.should_split 判定やタスクのスプリットシェア（_compute_child_shares）を少し変え、現在の “子＋孫数” に基づく配分が SeniorManager_205 を偏らせていないかテスト。必要なら SeniorManager ごとに子ノード数に応じたウェイト上限を設ける。

- 比較レポートの自動化: 各シナリオ（構造変更案）を FinalStudy/scenario_x/ にコピーして実行し、RESULT.md から SeniorManager_205 の指標だけ抜き出す集計スクリプトを用意。これで少数の実験を回しても効果を一覧できる。
