# TaskAgent モデル解説

`TaskAgent` は「組織グラフ上を流れるタスク」を抽象化した最小単位です。実体は `task_rules.py` で定義されたデータクラスで、以下の属性・振る舞いを持ちます。

## 主な属性
- `task_id`: シミュレーション内で一意な ID。
- `task_type`: `TopDown / Design / Execution / Interrupt` のいずれか。役職ごとの分布に従って Poisson(λ=2) のタスク生成イベントから決まります。
- `weight`: `difficulty / stakeholders / coordination / ambiguity` で構成される `TaskWeight`。各要素はインタビューで得たレンジに基づきランダムにサンプリングされます。`scale(factor)` により分割後も比率を保ったまま再利用できます。
- `origin_node`: タスクを発生させたノード ID。
- `current_node`: 直近で滞在しているノード。
- `state`: 進行状況。`Created → Delegated → InProgress → Done → Reported → Escalated` の順序で推移します（Escalated は必要時のみ）。
- `history`: これまでに訪れたノードのリスト。`move_to` を呼ぶたびに追記されます。

## 状態遷移
1. **Created**: 発生直後。生成ノードのキューに置かれます。
2. **Delegated**: 管理職が子ノードへ委譲する際の状態。`should_delegate` で決まる確率に従います。
3. **InProgress**: ノード自身が処理を引き受けた状態。
4. **Done**: 実行完了。親ノードへ報告する準備が整います。
5. **Reported**: 実行層→中間層の報告。受信側には `0.1 × weight.total()` の軽い負荷を加算します。
6. **Escalated**: TaskWeight が閾値（30.0）を超える、または 5% の確率イベントで上層へ再委譲された状態。上層ノードは再度 `should_escalate` を評価し、必要ならさらに上へ渡します。

`TaskAgent.move_to(node, next_state)` は遷移を 1 箇所にまとめたヘルパーです。移動先ノードを履歴に保存し、状態を更新します。

## 負荷計算との関係
- タスクを受け取ったノード: `+1.0 × weight.total()`
- タスクを渡したノード: `+0.3 × weight.total()`（調整・説明コスト）
- 実行完了後の報告を受けたノード: `+0.1 × weight.total()`
- Director / Manager が分割した際: `+0.2 × weight.total()` の分割コスト

これらのルールが `graph_simulation.py` の `LoadTracker` に記録され、SimLoad（シミュレーション負荷）として出力されます。

## 代表的な動き
1. CXO が TopDown タスクを生成（Created）。
2. CXO から Director へ `select_next_node` で SimLoad が小さい枝を優先しつつ委譲。受け渡し時に送信側へ `+0.3w`、受信側へ `+1.0w`。
3. Director / Manager はタスクを 60% 下に割り振り（3 サブタスク）つつ、自身には `split_cost = 0.2w` が入る。残り 40% は自分で保持して InProgress。
4. Player が InProgress → Done → Reported と進み、Manager へ軽い報告負荷を与える。
5. Manager/Director は `should_escalate`（閾値 30 または 5%）を満たしたタスクだけを Escalated として上層へ再送。Escalation も調整コスト + 受信負荷を発生させる。
6. Escalation が収束するとタスクは完了し、`completed_tasks` が増加する。

このように TaskAgent は「タスクの実体 + 状態 + 軌跡」を保持することで、グラフ上の流れと負荷計算をシンプルな API に閉じ込めています。
