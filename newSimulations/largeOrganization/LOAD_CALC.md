# 負荷値の計算ルール（Large Organization）

`large_simulation.py` は `newSimulations/afterInterview/task_rules.py` に定義されたルールをそのまま利用しており、SimLoad を以下のイベントで積み上げます。

## 用語・記号
- **`TaskWeight`**: `difficulty / stakeholders / coordination / ambiguity` の4成分から構成されるタスク固有の重み。
- **`weight.total()`**: 上記4成分の合計値。受信・送信コスト計算に直接使用します。
- **`LoadTracker`**: 各ノードの累積負荷（SimLoad）を記録するクラス。
- **`TaskState`**: `Created → Delegated → InProgress → Done → Reported → Escalated` の状態遷移を示す Enum。
- **`Score`**: `SimLoad` を最大値で正規化した値に betweenness centrality を掛け合わせた総合指標。`0.7 * normalized_sim_load + 0.3 * centrality`。

## 1. タスク受信（delegation/reporting）
- 子ノードへタスクを引き渡す際、受け取ったノードに **`+1.0 × weight.total()`** を付与します。
- ここでの `weight.total()` は `difficulty + stakeholders + coordination + ambiguity` の合計です。

## 2. タスク送信（delegation/escalation）
- タスクを渡したノードには調整・説明コストとして **`+0.3 × weight.total()`** を追加します。
- `TaskRulebook.select_next_node` は SimLoad が低いノードを 60% の確率で優先し、残り 40% はランダムに選びます。

## 3. プレイヤーの完了報告
- Player が `Done → Reported` に遷移すると、報告を受けた親（Manager）に **`+0.1 × weight.total()`** を加算します。
- これは報告対応の軽めな負担を表現しています。

## 4. 分割（Director / SeniorManager / Manager）
- `should_split` が true の役職はタスクを 60% 分を 3 つのサブタスクへ分割します。
- 分割時に元タスクを保持するノードへ **`split_cost = 0.2 × weight.total()`** が発生します。
- サブタスクは `weight.scale(delegated_fraction)` で元の重み構成を維持したまま子ノードへ渡されます。

## 5. エスカレーション
- `weight.total()` が 30 を超える、または 5% の確率イベントでタスクを上層へ戻します。
- 再度親ノードに渡す際は 1 と 2 のルール（受信/送信負荷）を適用します。

## 6. 集計とスコア
- 各ノードの SumLoad を `LoadTracker` が記録し、最終的に `node_sim_load / max_sim_load` で正規化した値と betweenness centrality を組み合わせて `Score = 0.7 * normalized_load + 0.3 * centrality` を算出しています。

これらのルールは afterInterview シナリオと共通で、Large Organization ではノード数 1000 のより大規模なグラフに対して適用しています。***
