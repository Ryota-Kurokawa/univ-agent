# 追加検証：ベースラインモデル（管理スパン半分）

## 目的
元のInterviewBasedシナリオの管理スパンを半分にした場合の影響を検証する。

## 管理スパン設定

| 階層 | 元の管理スパン | 半分にした管理スパン |
|:---|:---:|:---:|
| CXO→Dir | 15-20 | 8-10 |
| Dir→SM | 10-15 | 5-8 |
| SM→Mgr | 10-15 | 5-8 |
| Mgr→Player | 5-10 | 3-5 |

## 実行方法

```bash
cd /Users/kurokawaryouta/Developer/Univ/SampleAgent
python -m newSimulations.forThesis.additionalStudy.Base.graph_simulation
```

## 期待される結果
- 総ノード数が大幅に減少
- 管理スパンが小さくなることで、各層の負荷がどう変化するかを確認
