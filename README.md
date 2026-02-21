# PortaRe0

Cubie A7Z SBCベースのクラムシェル型ポータブルPC（Cyberdeck）自作プロジェクト。

## 概要

| 項目 | 内容 |
|------|------|
| SBC | Cubie A7Z (Allwinner A733 / 8コア / WiFi6 / BT5.4) |
| ディスプレイ | 5.5" Sharp LS055R1SX04 (1440×2560 / MIPI DSI) |
| キーボード | カスタムPCB + Alps SKRPABE010 × 63キー / RP2040 / QMK |
| 入力 | 3DSスライドパッド（アナログスティック） |
| 電源 | LiPo 6060100 (3500mAh) + BQ25895 充電IC + TPS61023 昇圧DC-DC |
| USBハブ | VL812 (USB 3.0 / 4ポート) |
| オーディオ | MAX98357A × 2 (I2S / ステレオ) |
| PCB | 4層基板 / JLCPCB PCBA |
| 筐体 | 3Dプリンター自作（クラムシェル / 139×81mm） |

## 現在のフェーズ

**Phase 2: KiCad 回路設計中**

- [x] power シート（BQ25895 / TPS61023 / AP2112K）
- [x] usb_hub シート（VL812 / W25Q32）
- [x] keyboard シート（RP2040 / キーマトリクス / アナログスティック / LED）
- [ ] audio シート（MAX98357A × 2）
- [ ] connectors シート

## ドキュメント

- [Claude/PROGRESS.md](./Claude/PROGRESS.md) - 現在の進捗・次のタスク
- [Claude/PROJECT_PLAN.md](./Claude/PROJECT_PLAN.md) - 確定仕様・部品リスト
- [bom/cyberdeck_bom.xlsx](./bom/cyberdeck_bom.xlsx) - BOM (Excel)
- [bom/cyberdeck_bom.csv](./bom/cyberdeck_bom.csv) - BOM (CSV)
- [keyboard/matrix.md](./keyboard/matrix.md) - キーマトリクス割り当て表
- [keyboard/info.json](./keyboard/info.json) - QMKレイアウト定義

## リポジトリ構成

```
kicad/PortaRe0/        KiCadプロジェクト（回路図・PCB）
kicad/PortaRe0_lib/    カスタムシンボル・フットプリント・3Dモデル
keyboard/              キーレイアウト・マトリクス定義・QMK設定
cad/                   筐体 3Dデータ（未着手）
docs/                  データシート
bom/                   BOM（xlsx / csv）
Claude/                設計ドキュメント・進捗ログ・セッションログ
```

## 主要部品 C番号一覧

| 部品 | 型番 | C番号 |
|------|------|-------|
| 充電IC | BQ25895RTWR | C80200 |
| 昇圧DC-DC | TPS61023DRLR | C919459 |
| LDO 3.3V | AP2112K-3.3TRG1 | C51118 |
| USB HUBチップ | VL812-Q7 | C69417 |
| SPI Flash | W25Q32JVSSIQ | C82344 |
| キーボードMCU | RP2040 | C2040 |
| クリスタル（RP2040用） | X322512MOB4SI | C70565 |
| I2Sアンプ | MAX98357AEWL+T | C2682619 |
| キースイッチ | Alps SKRPABE010 | C115360 |
| ダイオード | 1N4148W | C2099 |
| MOSFET | BSS138 | C52895 |
| FPCコネクタ（スティック用） | Molex 5034800440 | C3170007 |
