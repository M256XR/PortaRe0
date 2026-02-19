# PortaRe0 Claude コンテキストファイル

Cowork / Claude がこのプロジェクトを引き継ぐ際に最初に読むファイル。

---

## このフォルダの読み込み順

1. **このファイル（CONTEXT.md）** - 全体像の把握
2. **PROGRESS.md** - 現在どこまで進んでいるか・次のタスク
3. **PROJECT_PLAN.md** - 確定済み仕様・部品型番・C番号
4. **chat_logs/** - 過去のチャット要約（詳細な経緯・議論が必要な時）

---

## プロジェクト概要

Cubie A7Z SBCベースのクラムシェル型ポータブルPC（Cyberdeck）自作プロジェクト。

- オーナー：M256XR
- GitHubリポジトリ：https://github.com/M256XR/PortaRe0
- ローカルパス：D:\Projects\PortaRe0\
- KiCadプロジェクト：D:\Projects\PortaRe0\kicad\PortaRe0\

---

## 作業スタイルの注意点

- KiCadの回路図作業はCoworkでの直接操作不可。コマンドや手順を示す形でサポートする
- easyeda2kicadはコマンドラインで動く（Coworkから実行可能）
- BOM更新・計算・ドキュメント生成はCoworkで自動化できる
- チャット内容は手動でchat_logs/に保存する運用

---

## 各フェーズの担当ツール目安

| 作業 | ツール |
|------|--------|
| 回路図作成・PCBレイアウト | KiCad（手動） |
| ライブラリ取得（easyeda2kicad） | Cowork / ターミナル |
| BOM更新・整合チェック | Cowork |
| インダクタ値計算・電源計算 | Claude（チャット） |
| データシート調査 | Claude（チャット） |
| 筐体モデリング | Fusion 360 / OpenSCAD（手動） |
| docs/へのPDF整理 | Cowork |
| PROGRESS.md更新 | Cowork or 手動 |
