# 追加検証：実験B（管理スパン半分）

## 目的
実験B（Dir→SM増加、SM人数増加、SM→Mgr削減）の管理スパンを半分にした場合の影響を検証する。

## 管理スパン設定

| 階層 | 元の管理スパン | 半分にした管理スパン |
|:---|:---:|:---:|
| CXO→Dir | 15-20 | 8-10 |
| Dir→SM | 18-23 | 9-12 |
| SM→Mgr | 4-6 | 2-3 |
| Mgr→Player | 10-13 | 5-7 |

## 実行方法

```bash
cd /Users/kurokawaryouta/Developer/Univ/SampleAgent
python -m newSimulations.forThesis.additionalStudy.B.graph_simulation
```

## 期待される結果
- SM人数が増加することで、総負荷の分散効果がどう変化するか
- 管理スパンを小さくしても分散効果は維持されるか
