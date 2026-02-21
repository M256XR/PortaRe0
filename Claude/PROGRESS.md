# PortaRe0 進捗ログ

## 現在のフェーズ
**Phase 2: 回路設計 ← 進行中**

## 現在の作業箇所
- KiCad `kicad/PortaRe0/` power・usb_hub・keyboardシート完成
- **次のタスク**:
  1. MAX98357A × 2 audio シート
  2. connectors シート（新規作成）

---

## フェーズ完了状況

### Phase 1: 部品選定 ✅ 完了
- 主要IC 全部の JLCPCB 在庫確認済み
- BOMファイル確定: `bom/cyberdeck_bom.xlsx` / `bom/cyberdeck_bom.csv`
- GitHubリポジトリ作成: https://github.com/M256XR/PortaRe0
- KiCadプロジェクト・ライブラリ設定済み
- easyeda2kicad で全ICのシンボル/フットプリント取得済み（`kicad/PortaRe0_lib/`）

### Phase 2: 回路設計 🔄 進行中
- [x] KiCadプロジェクト作成、階層シート構成（power / usb_hub / keyboard / audio）
- [x] BQ25895 powerシート完成（TS分圧固定 / インダクタ1.5µH / 全ピン配線済み）
- [x] TPS61023 回路（EN回路・モーメンタリボタン含む）
- [x] AP2112K 回路（5V→3.3V / 常時ON）
- [x] VL812 usb_hub シート（W25Q32 SPI Flash / 25MHz水晶 / デカップリング全完）
- [x] RP2040 keyboard シート完成
  - RP2040本体・電源デカップリング・クリスタル・QSPI Flash・USB・SWD
  - キーマトリクス 63キー（9COL×8ROW / Net Label）
  - 3DSスライドパッド（Molex 5034800440 FPCコネクタ / GP27,GP28）
  - LED × 3（GP24=CHG橙 / GP25=FULL緑 / GP26=ACT緑 / 330Ω）
- [ ] MAX98357A × 2 audio シート
- [ ] connectors シート（新規作成）

### Phase 3: PCBレイアウト ⏳ 未着手
### Phase 4: 試作・検証 ⏳ 未着手
### Phase 5: 筐体設計・組み立て ⏳ 未着手

---

## 未解決の TBD 事項

| 項目 | 解決タイミング |
|------|--------------|
| インダクタ値（BQ25895用 1.5µH / TPS61023用 1µH） | JLCPCB在庫確認後 |
| VL812用 25MHz水晶 C番号 | JLCPCB在庫確認後 |
| FPCケーブル長さ（SBC接続用 30ピン 0.5mmピッチ） | 筐体CAD後 |
| キルスイッチ型番 | KiCad フットプリント決める時 |
| モーメンタリスイッチ型番 | KiCad フットプリント決める時 |
| LED C番号（緑・橙） | connectors/audioシート時 |
| イヤホンジャック型番 | audioシート時 |
| キーキャップ型番 | スイッチ嵌合確認後 |
| ヒンジ機構 | 筐体CAD後 |
| RTCバッテリー有無 | A7Z実機届いたら確認 |
| ヒートパイプ取り回し経路 | 筐体CAD後 |
| WiFiアンテナ配置 | 筐体CAD後 |

---

## 購入済み・発注済み

- Cubie A7Z 8GB → AliExpress 注文済み ✅
- LS055R1SX04 + HDMIコントローラ基板セット → AliExpress 注文済み ✅
- LiPo 6060100 → AliExpress 注文済み ✅
- フラットヒートパイプ 3mm厚 → AliExpress 注文済み ✅
- 3DSスライドパッド → 別途購入予定

## 購入待ちリスト

- 3DSスライドパッド（AliExpress or 中古）
- 秋月 マイクロスピーカー 8Ω 23×16×4.6mm（P-12494 or P-12495）
- FPCケーブル 30ピン 0.5mmピッチ（筐体CAD後に長さ確定）
- 小型ヒートシンク 14×9×4mm程度 × 4個

---

## 直近の決定事項ログ

### 2026-02-21（session09）
- キー数確定: 63キー（KLEパースにより確定 / 従来の66は誤り）
- ダイオード数確定: 63個
- アナログスティック確定: 3DSスライドパッド / FPC 4ピン 1.0mmピッチ
- FPCコネクタ確定: Molex 5034800440（C3170007）/ 4P 1.0mm ZIF / VCC=3.3V直結OK
- キーマトリクス物理配置ベース割り当て確定（keyboard/matrix.md）
- QMK info.json作成（keyboard/info.json）
- ダイオード向き: ROW→[>|]→SW→COL（カソードがSW側）
- keyboard.kicad_sch: RP2040完全完成

### 2026-02-21（session08）
- RP2040外部SPI Flash（W25Q32）必須と確認・BOM追加（VL812用と合わせて計2個）
- RP2040用W25Q32接続方法確定（QSPI 4ビット / /CS 10kΩプルアップのみ）
- LED割り当て詳細確定：GP24=LED_CHG(橙) / GP25=LED_FULL(緑) / GP26=LED_ACT
- クリスタル確定：X322512MOB4SI（C70565）/ 12MHz / 12pF / SMD3225-4P / 外付けC 15pF×2

### 2026-02-21（session07）
- キルスイッチ：VSYS→SW→TPS61023/AP2112K VIN に配置確定
- キーレイアウト確定（63キー / 9×8マトリクス）
- RP2040 GPIO割り当て確定（29本/30本）
- パワーシンボル：VSYS / 5V_SYS / +BATT をカスタムパワーシンボルで作成確定
- VL812 usb_hub シート完成

### 2026-02-19〜20
- 主要IC全部のJLCPCB C番号確定（下記参照）

---

## JLCPCB C番号確定リスト

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
