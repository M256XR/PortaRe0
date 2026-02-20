# PortaRe0

Cubie A7Z SBCベースのクラムシェル型ポータブルPC（Cyberdeck）自作プロジェクト。

## 概要
- **SBC**: Cubie A7Z (Allwinner A733 / 8コア / WiFi6 / BT5.4)
- **ディスプレイ**: 5.5" Sharp LS055R1SX04 (1440×2560)
- **キーボード**: カスタムPCB + Alps SMDスイッチ 66キー / RP2040 / QMK
- **電源**: LiPo 6060100 + BQ25895 充電IC + TPS61023 昇圧DC-DC
- **USBハブ**: VL812 (USB 3.0 / 4ポート)
- **オーディオ**: MAX98357A × 2 (I2S / ステレオ)
- **PCB**: 4層基板 / JLCPCB PCBA
- **筐体**: 3Dプリンター自作

## 現在のフェーズ
Phase 2: KiCad 回路設計中
- [x] power シート（BQ25895 / TPS61023 / AP2112K）
- [x] usb_hub シート（VL812 / W25Q32）
- [ ] keyboard シート（RP2040）
- [ ] audio シート（MAX98357A × 2）
- [ ] connectors シート

## ドキュメント
- [Claude/PROGRESS.md](./Claude/PROGRESS.md) - 現在の進捗・次のタスク
- [Claude/PROJECT_PLAN.md](./Claude/PROJECT_PLAN.md) - 確定仕様・部品リスト
- [bom/cyberdeck_bom.xlsx](./bom/cyberdeck_bom.xlsx) - BOM

## リポジトリ構成
```
kicad/PortaRe0/        KiCadプロジェクト
kicad/PortaRe0_lib/    カスタムシンボル・フットプリント
keyboard/              キーレイアウト
cad/                   筐体 3Dデータ
docs/                  データシート
bom/                   BOM
Claude/                設計ドキュメント・進捗ログ
```
