# PortaRe0 Claude コンテキストファイル

Claudeがこのプロジェクトを引き継ぐ際に最初に読むファイル。

---

## セッション開始時の手順

1. **GitHubから差分確認** - 別PCでの作業が入っている可能性があるため必ず確認
   ```
   git fetch && git status
   ```

2. **このファイル（CONTEXT.md）** - 全体像・読み込み順の把握

3. **PROGRESS.md** - 現在どこまで進んでいるか・次のタスク・最新の決定事項

4. **Claude.md** - 確定済み仕様の詳細（信頼の源泉）

5. **chat_logs/原文/index.md** - 疑問が生じたら索引で原文の場所を特定

6. **chat_logs/原文/SessionXX.txt** - 索引で場所を特定してから該当部分を読む

> **重要**: 仕様の正確性は Claude.md > PROGRESS.md > 原文 の順で信頼すること。
> PROJECT_PLAN.md は初期計画書（凍結）なので参照のみ・仕様変更の追跡には使わないこと。
> chat_logs/要約_archive/ は廃止済み。どうしても必要な場合のみ参照し、原文を優先すること。

---

## プロジェクト概要

Cubie A7Z SBCベースのクラムシェル型ポータブルPC（Cyberdeck）自作プロジェクト。

- オーナー：M256XR
- GitHubリポジトリ：https://github.com/M256XR/PortaRe0
- ローカルパス：D:\Projects\PortaRe0\
- KiCadプロジェクト：D:\Projects\PortaRe0\kicad\PortaRe0\

---

## ファイル構成と役割

| ファイル | 役割 | 更新タイミング |
|----------|------|---------------|
| Claude.md | 確定済み仕様の真実（最優先） | 仕様変更のたびに更新 |
| PROGRESS.md | 進捗・直近の決定事項ログ | セッションごとに更新 |
| CONTEXT.md | このファイル・案内のみ | 運用方式変更時のみ |
| PROJECT_PLAN.md | 初期計画書（凍結・参照のみ） | 更新しない |
| chat_logs/原文/index.md | 原文ログの索引 | 原文ファイル追加時に更新 |
| chat_logs/原文/SessionXX.txt | セッション原文ログ | セッション終了後に手動保存 |
| chat_logs/要約_archive/ | 旧要約（廃止） | 参照しない |

---

## 原文ログの保存ルール

- ファイル名形式：`YYYY-MM-DD_SessionNN.txt`
- 保存先：`chat_logs/原文/`
- 内容：チャットの原文をそのまま保存（要約・加工しない）
- 索引追記：`chat_logs/原文/index.md` のセッション別・トピック別に追記する

---

## 作業スタイルの注意点

- KiCadの回路図作業はClaude Codeでの直接操作不可。コマンドや手順を示す形でサポート
- easyeda2kicadはコマンドラインで動く（Claude Codeから実行可能）
- BOM更新・計算・ドキュメント生成はClaude Codeで自動化できる
- チャット内容は手動で chat_logs/原文/ に保存する運用

---

## 各フェーズの担当ツール目安

| 作業 | ツール |
|------|--------|
| 回路図作成・PCBレイアウト | KiCad（手動） |
| ライブラリ取得（easyeda2kicad） | Claude Code / ターミナル |
| BOM更新・整合チェック | 手動　Claude Code |
| インダクタ値計算・電源計算 | Claude（チャット） |
| データシート調査 | Claude（チャット）/ Gemini|
| 筐体モデリング | Fusion 360 |
| PROGRESS.md・Claude.md更新 | Claude Code or 手動 |
