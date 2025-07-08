# エージェントシミュレーション

このプロジェクトは、平衡木グラフ上でエージェントが移動するシミュレーションを行うPythonプログラムです。

## 必要な環境

- Python 3.7以上
- pip（Pythonパッケージマネージャー）

## セットアップ手順

### 1. 仮想環境の作成と有効化

```bash
# 仮想環境の作成
python3 -m venv venv

# 仮想環境の有効化（macOS/Linux）
source .venv/bin/activate.fish

# 仮想環境の有効化（Windows）
# venv\Scripts\activate
```

### 2. 必要なパッケージのインストール

```bash
# 基本パッケージのインストール
pip install networkx matplotlib

# より綺麗な階層レイアウトを使用したい場合（オプション）
pip install pydot

# Graphvizのインストール（macOS）
brew install graphviz

# Graphvizのインストール（Ubuntu/Debian）
# sudo apt-get install graphviz

# Graphvizのインストール（Windows）
# https://graphviz.org/download/ からダウンロードしてインストール
```

### 3. 依存関係ファイルの作成（オプション）

```bash
# 現在インストールされているパッケージを記録
pip freeze > requirements.txt
```

## 実行方法

### 基本実行

```bash
# 仮想環境を有効化した状態で
python main.py
```

### 実行結果

プログラムを実行すると、以下のファイルが生成されます：

- `initial_state_tree.png` - 初期状態のグラフ
- `simulation_steps_part_1.png` - シミュレーション結果（ステップ1-6）
- `simulation_steps_part_2.png` - シミュレーション結果（ステップ7-10）

## プログラムの機能

### 現在の設定

- **エージェント生成・削除**: 無効化済み
- **初期エージェント**: A1（ルートノード）、B2（リーフノード）
- **シミュレーションステップ**: 10ステップ
- **グラフ構造**: 分岐数2、高さ3の平衡木

### エージェントの動作

1. 各ステップで、エージェントは隣接するノードにランダムに移動
2. エージェントの新規生成・消失は現在無効化されています
3. シミュレーション結果は画像ファイルとして保存されます

## カスタマイズ

### パラメータの変更

`main.py`の以下の部分を編集することで設定を変更できます：

```python
# グラフの構造
env = Environment(branches=2, height=3)

# シミュレーションステップ数
simulation_steps = 10

# エージェントの生成・削除確率（現在は無効化）
new_agent_probability = 0.08
agent_disappearance_rate = 0.05
```

## 仮想環境の終了

作業が終わったら、仮想環境を無効化します：

```bash
deactivate
```

## トラブルシューティング

### pydotに関する警告が表示される場合

```
警告: 'pydot'またはGraphviz本体が見つかりません。代替のspring_layoutで描画します。
```

この警告が表示されても、プログラムは正常に動作します。より綺麗な階層レイアウトを使用したい場合は、上記のセットアップ手順に従ってpydotとGraphvizをインストールしてください。

### モジュールが見つからないエラー

```
ModuleNotFoundError: No module named 'networkx'
```

このエラーが表示される場合は、仮想環境が正しく有効化されているか確認し、必要なパッケージがインストールされているか確認してください。

## プロジェクト構造

```
SampleAgent/
├── main.py                          # メインプログラム
├── README.md                        # このファイル
├── requirements.txt                 # 依存関係（生成される）
├── venv/                           # 仮想環境（生成される）
├── initial_state_tree.png          # 初期状態（生成される）
├── simulation_steps_part_1.png     # シミュレーション結果1（生成される）
└── simulation_steps_part_2.png     # シミュレーション結果2（生成される）
```
