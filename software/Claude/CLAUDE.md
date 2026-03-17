# PortaRe0 ソフトウェア開発 仕様書

> **このファイルはソフトウェア開発用コンテキストのサマリ。** 変更時は PROGRESS.md の決定事項ログにも必ず記録すること。

## セッション開始手順

1. `git fetch && git status` で差分確認
2. **PROGRESS.md** を読む（現在地・次のタスク・直近の決定事項）
3. このファイル（CLAUDE.md）でコンテキスト確認
4. 疑問があれば `chat_logs/原文/index.md` で原文の場所を特定
5. 終了処理は **CLOSING.md** を参照

> 仕様の信頼優先順位: 原文ログ > specs/* > CLAUDE.md > PROGRESS.md

---

## プロジェクト概要

Cubie A7Z SBCベースのクラムシェル型ポータブルPC（Cyberdeckスタイル）のソフトウェア開発。

**ハードウェア仕様 → [../../Claude/CLAUDE.md](../../Claude/CLAUDE.md)**

---

## ハードウェア構成（ソフト開発に関係する部分）

| コンポーネント | 詳細 |
|--------------|------|
| SBC | Cubie A7Z（OS: Linux） |
| キーボードMCU | RP2040 × 2（keyboard / audio シート） |
| キーマトリクス | 63キー（9COL × 8ROW）+ 1N4148Wダイオード |
| スライドパッド | 3DSスライドパッド（Molex FPC / GP27,GP28） |
| オーディオ | MAX98357A（I2S スピーカー） + PCM5102A（DAC） + TPA6132A2（ヘッドフォンアンプ） |
| ディスプレイ | LS055R1SX04（5.5インチ MIPI DSI）+ HDMIコントローラ基板 |
| USB HUB | VL812-Q7（USB3.0 4ポート） |
| M.2 SSD | PCIe接続（FPC経由） |

---

## Claudeの役割と作業方針

**Claudeはソフトウェア開発のアシスタント。コードの直接編集・生成を行う。**

### やること
- **ファームウェア開発**: RP2040 キーボードファームウェア（QMK / カスタム）
- **ドライバ・設定**: Linux側のデバイス設定・カーネルモジュール等
- **スクリプト・ツール**: 自動化スクリプト・ユーティリティ
- **デバッグサポート**: エラー解析・ログ読み込み・修正提案
- **コードレビュー**: 接続の妥当性・ロジック検証・最適化提案

### やらないこと
- ユーザーが自分でやると言っている作業の代行
- ハードウェア回路図の直接編集（ハードウェア作業は `Claude/` 配下を参照）

---

## ディレクトリ構成

```
software/
  src/               ← ソースコード
    keyboard/        ← RP2040 キーボードファームウェア
    audio/           ← オーディオ設定・スクリプト
    system/          ← Linux側 設定・スクリプト
  Claude/
    CLAUDE.md        ← このファイル
    PROGRESS.md      ← 進捗・決定事項
    CLOSING.md       ← 終了処理手順
    specs/           ← 詳細仕様
    chat_logs/原文/  ← セッションログ
    archive/         ← 古いログ
    checklists/      ← 作業チェックリスト
    extract_session.py
    session_close.py
```

---

## 開発環境

| 用途 | ツール |
|------|--------|
| RP2040 ファームウェア | TBD（QMK / Pico SDK / KMK等） |
| ビルド | TBD |
| 書き込み | BOOTSEL（UF2ドラッグ&ドロップ）|
| Linux側 | SSH or 直接操作 |

---

## よく使うコマンド

```bash
# セッション原文抽出
python software/Claude/extract_session.py

# セッション終了処理（commit + push）
python software/Claude/session_close.py "コミットメッセージ"
```
