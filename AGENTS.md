# Repository Guidelines

## プロジェクト構成とモジュール整理
- `research_simulation.py`: 組織モビリティの標準シミュレーション実行用エントリーポイント。グラフ生成、エージェント移動、画像出力の全体を統括します。
- `simulations/`: `branches_comparison/` や `loop_edges_comparison/` などのシナリオ別フォルダ。新しい検証を追加する際は既存構成を踏襲し、説明用の `README.md` とスクリプトをセットで配置してください。
- `docs/`: リサーチノートや方針メモ。アルゴリズムや仮説を更新したら本文を同期させ、差分が生まれないよう管理します。
- `experiments/legacy/`: アーカイブ化された試行版。再検証が必要な場合は `experiments/` 直下に新しいブランチフォルダを作成し、元データは残す方針です。

## ビルド・テスト・開発コマンド
- `python -m venv .venv && source .venv/bin/activate`: 仮想環境の標準セットアップ。依存関係を入れる前に必ず実行します。
- `pip install -r requirements.txt` （または `pip install networkx matplotlib pydot`）: ネットワーク可視化に必要なライブラリを導入。新規依存を追加したら `requirements.txt` を更新します。
- `python research_simulation.py`: ベースラインシミュレーションを実行し、リポジトリ直下に PNG を再生成します。
- `python simulations/branches_comparison/simulation_branches_5.py`: 代替シナリオ実行例。リポジトリ直下で `python path/to/script.py` 形式を用いてインポートエラーを防いでください。

## コーディングスタイルと命名規約
- PEP 8 に従いインデントは 4 スペース。モジュール・変数・関数は snake_case、クラス（例: `MovingAgent`）のみ UpperCamelCase を使用します。
- 関数は可能な限り副作用を避け、描画やファイル書き出しはヘルパー関数へ分離。引数と戻り値が複雑な場合は短い docstring を添えます。
- Python 3.8 以降との互換性が不明な変更を行った際は、`python -m compileall path/to/file.py` で構文チェックを行ってからプッシュします。

## テスト方針
- 自動テスト基盤は未整備のため、`python research_simulation.py` と影響のあるシナリオスクリプトを再実行し、生成画像が期待通りかを確認します。
- 複雑なロジックを追加する場合は `tests/` ディレクトリを作成し、`pytest` 形式のテスト（例: `test_weighted_move.py`）を用意して将来の CI 導入に備えます。
- シナリオスクリプトは `random` と `numpy.random` にシードを設定し、再現性を確保してください。

## コミットとプルリクエストのガイドライン
- コミットメッセージは `type: summary` 形式で簡潔に記述し、`type` には `feat`、`fix`、`refactor`、`docs` などを使用。履歴の一貫性確保のため、言語は英語を推奨します。
- プルリクエストには変更概要、生成物が変わった場合のパスやスクリーンショット、実行したテストコマンド（例: `Ran python research_simulation.py`）を明記してください。
- 重要なシミュレーションロジック更新時は、関連する `docs/` の議事や Issue を参照に追記し、少なくとも 1 名のレビューを得てからマージします。
