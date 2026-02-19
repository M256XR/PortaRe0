# PortaRe0

Cubie A7Z SBCベースのクラムシェル型ポータブルPC（Cyberdeck）自作プロジェクト。

## 概要
- **SBC**: Radxa Cubie A7Z (Allwinner A733 / 8コア / WiFi6 / BT5.4)
- **ディスプレイ**: 5.5" Sharp LS055R1SX04 (1440×2560)
- **キーボード**: カスタムPCB + Alps SMDスイッチ 60キー / RP2040 / QMK
- **電源**: LiPo 6060100 + BQ25895 充電IC + TPS61023 昇圧DC-DC
- **PCB**: 4層基板 / JLCPCB PCBA
- **筐体**: 3Dプリンター自作

## ドキュメント
- [PROGRESS.md](./PROGRESS.md) - 現在の進捗・次のタスク
- [PROJECT_PLAN.md](./PROJECT_PLAN.md) - 確定仕様・部品リスト
- [bom/cyberdeck_bom.xlsx](./bom/cyberdeck_bom.xlsx) - BOM

## 現在のフェーズ
Phase 2: KiCad 回路設計中（BQ25895 powerシート作業中）

## リポジトリ構成
```
kicad/PortaRe0/        KiCadプロジェクト
kicad/PortaRe0_lib/    カスタムシンボル・フットプリント
cad/                   筐体 3Dデータ
docs/                  データシート
bom/                   BOM
```
