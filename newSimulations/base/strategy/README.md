# Strategy Structure Visualization

NetworkX と Matplotlib を用いて、ベースライン戦略組織（CXO → Director → Manager → Player）の構造を1枚の PNG に出力するためのユーティリティです。

## 使い方
事前に仮想環境上で `pip install networkx matplotlib` を済ませてください（既存の `requirements.txt` に追記しても構いません）。

```bash
python3 newSimulations/base/strategy/generate_structure_image.py
```

実行すると同ディレクトリに `strategy_structure.png` が生成されます。ノード色は役職ごとに変えてあり、矢印で指揮系統（上→下）を表現します。

## カスタマイズ
- `NODES` / `EDGES`: ノードやエッジを差し替えることで別の階層構造を描画できます。
- `ROLE_LEVEL`: レイアウト時の縦位置。新しい役職を追加したい場合はここに深さを定義してください。
- `ROLE_COLORS`: 役職ごとのノード色。

`strategy_structure.png` はレポートや docs に貼り付けて、ベースライン構造の共有に活用できます。
