# PortaRe0 プロジェクト仕様書

> **このファイルは仕様のサマリ。** 変更時は PROGRESS.md の決定事項ログにも必ず記録すること。

## セッション開始手順

1. `git fetch && git status` で差分確認（別PCでの作業が入っている可能性あり）
2. **PROGRESS.md** を読む（現在地・次のタスク・直近の決定事項）
3. このファイル（CLAUDE.md）で仕様を確認
4. 疑問があれば `chat_logs/原文/index.md` で原文の場所を特定
5. 終了処理は **CLOSING.md** を参照

> 仕様の信頼優先順位: 原文ログ > specs/* > CLAUDE.md > PROGRESS.md

---

## コンセプト

Cubie A7Z SBCベースのクラムシェル型ポータブルPC（Cyberdeckスタイル）

**ハードウェア詳細仕様 → [specs/index.md](./specs/index.md)**

---

## Claudeの役割と作業方針

**Claudeは回路設計のアシスタント。KiCad回路図の直接編集は行わない。**

### やること
- **回路レビュー・確認**: 接続の妥当性、定数の検証、設計ミスの指摘
- **部品選定サポート**: データシート確認、代替品提案、C番号検索
- **シンボル/フットプリント取得**: `easyeda2kicad` コマンドの実行
- **設計判断のサポート**: ピン接続方針、抵抗値、配線ルール等の判断支援
- **KiCad操作手順の提示**: ユーザーが手動で行う操作のガイド

### やらないこと
- `.kicad_sch` ファイルの直接編集
- 複雑なPythonスクリプトによる回路図の自動生成
- ユーザーが自分でやると言っている作業の代行

---

## KiCad ライブラリ情報

- シンボル：`kicad/PortaRe0_lib/PortaRe0.kicad_sym`
- フットプリント：`kicad/PortaRe0_lib/PortaRe0.pretty/`
- 3Dモデル：`kicad/PortaRe0_lib/PortaRe0.3dshapes/`
- ライブラリ取得コマンド（easyeda2kicad）:
  ```
  python -m easyeda2kicad --full --lcsc_id C番号 --output kicad/PortaRe0_lib/PortaRe0 --overwrite
  ```

---

## 概算コスト

| カテゴリ | 概算（USD） |
|----------|------------|
| コンポーネント | $138〜$203 |
| PCB + PCBA（JLCPCB） | $70〜$130 |
| 筐体・機構 | $15〜$40 |
| 合計 | $223〜$373（約3.3〜5.6万円） |
