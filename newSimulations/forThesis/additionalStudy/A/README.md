# 追加検証：実験A（管理スパン半分）

## 目的
実験A（SM人数固定、SM→Mgr削減、Mgr→Player増加）の管理スパンを半分にした場合の影響を検証する。

## 管理スパン設定

| 階層 | 元の管理スパン | 半分にした管理スパン |
|:---|:---:|:---:|
| CXO→Dir | 15-20 | 8-10 |
| Dir→SM | 10-15 | 5-8 |
| SM→Mgr | 4-6 | 2-3 |
| Mgr→Player | 18-22 | 9-11 |

## 実行方法

```bash
cd /Users/kurokawaryouta/Developer/Univ/SampleAgent
python -m newSimulations.forThesis.additionalStudy.A.graph_simulation
```

## 期待される結果
- SM→Mgrスパンが更に小さくなることで、SMの効率がさらに向上するか
- Mgrへの負荷遷移がどう変化するか
