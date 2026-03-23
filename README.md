# PortaRe0

Cubie A7Z SBCベースのクラムシェル型ポータブルPC（Cyberdeck）自作プロジェクト。

## 概要

| 項目 | 内容 |
|------|------|
| SBC | Cubie A7Z (Allwinner A733 / 8コア / WiFi6 / BT5.4) |
| ディスプレイ | 5.5" Sharp LS055R1SX04 (1440×2560 / MIPI DSI) |
| キーボード | カスタムPCB + Alps SKRPABE010 × 64キー / RP2040 / QMK |
| 入力 | 3DSスライドパッド（アナログスティック） |
| 電源 | LiPo 606090 (4200mAh) + BQ25895 充電IC + TPS61023 昇圧DC-DC ×2 |
| USBハブ | VL812 (USB 3.0 / 4ポート) |
| ストレージ | M.2 2230 NVMe SSD（PCIe Gen3 x1 / Cubie A7Z F0506-16-BGR経由） |
| オーディオ | MAX98357A × 2 (スピーカー I2S) / PCM5102A + TPA6132A2 (イヤホン DAC+アンプ) |
| MCU | RP2040 × 2（キーボード専用 / オーディオ専用） |
| PCB | 6層基板 / JLCPCB PCBA |
| 筐体 | 3Dプリンター自作（クラムシェル / 139×81mm） |

## 現在のフェーズ

**Phase 3: PCBレイアウト完了 → 発注準備完了（資金準備待ち）**

- [x] power シート（BQ25895 / TPS61023 ×2 / AP2112K）
- [x] usb_hub シート（VL812 / W25Q32 / J_EXT_C / J_EXT_A）
- [x] keyboard シート（RP2040 #1 / キーマトリクス / アナログスティック / LED）
- [x] audio シート（RP2040 #2 / MAX98357A ×2 / PCM5102A / TPA6132A2）
- [x] connectors シート（J_HDMI_CTRL / J_FAN）
- [x] hdmi_adapter シート（別基板 / Micro HDMI → FFC変換）
- [x] usb_adapter シート（別基板 / FPCスティフナー + USB-Cオス ×2）
- [x] m2_ssd シート（M.2 2230 NVMe / PCIe Gen3 x1 / RT9080 LDO）
- [x] ERC（HP系のみ残存 / 想定内）
- [x] ガーバー生成済み / CPL生成済み
- [ ] JLCPCB発注（資金準備後）

## ドキュメント

- [Claude/PROGRESS.md](./Claude/PROGRESS.md) - 現在の進捗・次のタスク
- [Claude/CLAUDE.md](./Claude/CLAUDE.md) - 仕様サマリ・セッション開始手順
- [Claude/specs/](./Claude/specs/) - ハードウェア詳細仕様（電源・キーボード・オーディオ・M.2）
- [bom/cyberdeck_bom.xlsx](./bom/cyberdeck_bom.xlsx) - BOM (Excel)
- [bom/cyberdeck_bom.csv](./bom/cyberdeck_bom.csv) - BOM (CSV)
- [keyboard/matrix.md](./keyboard/matrix.md) - キーマトリクス割り当て表
- [keyboard/info.json](./keyboard/info.json) - QMKレイアウト定義

## リポジトリ構成

```
kicad/PortaRe0/        KiCadプロジェクト（回路図・PCB）
kicad/PortaRe0_lib/    カスタムシンボル・フットプリント・3Dモデル
keyboard/              キーレイアウト・マトリクス定義・QMK設定
cad/                   筐体 3Dデータ（進行中）
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
| MCU | RP2040 | C2040 |
| クリスタル（RP2040用 12MHz） | X322512MOB4SI | C70565 |
| クリスタル（VL812用 25MHz） | X322525MOB4SI | C9006 |
| I2Sアンプ | MAX98357AEWL+T | C2682619 |
| イヤホン用DAC | PCM5102APWR | C107671 |
| ヘッドフォンアンプ | TPA6132A2RTER | C69901 |
| USBパワースイッチ | TPS2042BDR | C138720 |
| USB ESD保護 | USBLC6-2SC6 | C7519 |
| キースイッチ | Alps SKRPABE010 | C115360 |
| ダイオード | 1N4148W | C2099 |
| MOSFET（レベル変換 / ファン制御） | BSS138 | C52895 |
| ショットキーダイオード（EN保護） | BAT54 | C466635 |
| FPCコネクタ（スティック用） | Molex 5034800440 | C3170007 |
| ZIF FPCコネクタ 24pin | FPC-05F-24PH20 | C2856805 |
| ZIF FPCコネクタ 16pin（PCIe） | FPC-05F-16PH20 | C2856801 |
| M.2ソケット（M-key 2230） | NASM0-S6701-TP40 | C367029 |
| LDO 3.3V（M.2用） | RT9080-33GJ5 | C841192 |
| USB-C レセプタクル（外部） | USB31-TYPE-C-FSABC | C2880583 |
| USB-A レセプタクル（外部） | HC-USB3.0-L168-WP | C7501850 |
| USB-C オス SMD（SBC接続） | 918-118A2021Y40000 | C168690 |
