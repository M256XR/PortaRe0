# PortaRe0 ソフトウェア開発 セッションログ索引

## セッション別索引

| セッション | 日付 | ファイル | 主な内容 |
|-----------|------|---------|---------|
| Session00 | 2026-03-16 | （このセッションはログなし） | software/ フォルダ構成作成 |
| Session01 | 2026-03-17〜18 | 2026-03-16_Session01.txt | フレームワーク選定・任意ディストリ・Windows ARM調査・Cubie A7Z システム調査・EDK2ポート計画 |

### Session01 主要トピック行番号（2026-03-16_Session01.txt）
| トピック | 行番号 |
|---------|--------|
| キーボード QMK 選定理由 | L40 |
| オーディオ TinyUSB 選定理由 | L57 |
| Armbian / 任意ディストリ方式 | L146 |
| Windows ARM ロードマップ | L304 |
| Allwinner A733 調査結果（SoCスペック・TF-A・EDK2状況） | L343 |
| Cubie A7Z システム調査（lsusb/lsblk/lscpu等） | L750頃 |
| ブートチェーン確認（extlinux、UEFI無効） | L950頃 |
| U-Boot mainline A733パッチ状況 | L1100頃 |
| EDK2 移植構成・参考リポジトリ分析 | L1300頃 |

---

## トピック別索引

| トピック | セッション | 備考 |
|---------|-----------|------|
| フォルダ構成 | session00 | software/Claude/ 整備 |
| RP2040 #1 フレームワーク（QMK） | session01 | specs/dev_plan.md |
| RP2040 #2 フレームワーク（TinyUSB UAC2） | session01 | specs/dev_plan.md |
| 任意ディストリ戦略（rootfs差し替え / DistroBox） | session01 | - |
| Windows ARM ロードマップ | session01 | specs/windows_arm.md |
| Cubie A7Z ブートチェーン | session01 | extlinux / UEFI無効 |
| EDK2 移植計画（RPi4参考・awwiniot流用） | session01 | specs/windows_arm.md |
| U-Boot A733 mainlineパッチ状況 | session01 | v3投稿済み・未マージ |
