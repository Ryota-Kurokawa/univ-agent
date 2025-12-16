# Large Organization Simulation

1000 ノード規模の階層組織を自動生成し、`newSimulations/afterInterview/task_rules.py` のルールでタスクフローを 1 回シミュレートするスクリプトです。

## 構成
- ルート（CXO）から `Executive → Director → SeniorManager → Manager → Player` の 6 層構造を持つ有向木を生成します。
- Depth1～3（Executive / Director / SeniorManager）は各層 10～20 ノードになるよう幅を制御し、上層が過密にならないようにしています。
- 残りのノードは Manager / Player 層に割り当て、Manager 数に応じて 1 人あたり 4～6 名の Player を配分します（平均 5 人前後）。
- タスク生成や委譲・エスカレーションは afterInterview と同じルール（Poisson λ=2、分割率 60% など）を再利用しています。

## 使い方
1. 依存関係をインストール  
   ```bash
   pip install networkx
   ```
2. シミュレーションを実行  
   ```bash
   python3 newSimulations/largeOrganization/large_simulation.py
   ```

コンソールには最初の 30 ノード分の `SimLoad / Centrality / Score` が表示され、総ノード数も併記されます。あわせて同ディレクトリに `RESULT.md` を生成し、全ノード分の結果を Markdown テーブルで保存します（上書きされます）。

## カスタマイズ例
- `TARGET_NODES`: 1000 以外の規模を試す。
- `TIME_STEPS`: タスク発生期間を伸縮。
- `BRANCHING_SEQUENCE` や `ROLE_SEQUENCE`: 階層構成を別の業態に合わせて変更。
- `LargeOrganizationSimulation(seed=...)`: seed を変えて疑似乱数列を更新。
