# PortaRe0 進捗ログ

## 現在のフェーズ
**Phase 2: 回路設計 ← 進行中**

## 現在の作業箇所
- KiCad `kicad/PortaRe0/` power・usb_hubシート完成
- **次のタスク**:
  1. RP2040 keyboard シート
  2. MAX98357A × 2 audio シート
  3. connectors シート（新規作成）

---

## フェーズ完了状況

### Phase 1: 部品選定 ✅ 完了
- 主要IC 全部の JLCPCB 在庫確認済み
- BOMファイル確定: `bom/cyberdeck_bom.xlsx`
- GitHubリポジトリ作成: https://github.com/M256XR/PortaRe0
- KiCadプロジェクト・ライブラリ設定済み
- easyeda2kicad で全ICのシンボル/フットプリント取得済み（`kicad/PortaRe0_lib/`）

### Phase 2: 回路設計 🔄 進行中
- [x] KiCadプロジェクト作成、階層シート構成（power / usb_hub / keyboard / audio）
- [x] BQ25895 powerシート: 左側ピン配線済み
- [x] BQ25895 powerシート: TS修正 + 右側・上側ピン完成
- [x] TPS61023 回路（EN回路含む）
- [x] AP2112K 回路
- [x] VL812 usb_hub シート（W25Q32 SPI Flash含む）
- [ ] RP2040 keyboard シート
- [ ] MAX98357A × 2 audio シート
- [ ] connectors シート（新規作成）

### Phase 3: PCBレイアウト ⏳ 未着手
### Phase 4: 試作・検証 ⏳ 未着手
### Phase 5: 筐体設計・組み立て ⏳ 未着手

---

## 未解決の TBD 事項

| 項目 | 解決タイミング |
|------|--------------|
| インダクタ値（BQ25895用・TPS61023用） | Phase 2 回路設計中に計算 |
| FPCケーブル長さ（30ピン 0.5mmピッチ確定済み） | 筐体CAD後 |
| キルスイッチ型番 | KiCad フットプリント決める時 |
| キーキャップ型番 | スイッチ嵌合確認後 |
| ヒンジ機構 | 筐体CAD後 |
| RTCバッテリー有無 | A7Z実機届いたら確認 |
| ヒートパイプ取り回し経路 | 筐体CAD後 |
| WiFiアンテナ配置 | 筐体CAD後 |

---

## 購入待ちリスト

- Cubie A7Z（在庫不安定、要確認）
- LS055R1SX04 + HDMIコントローラ基板セット（AliExpress）
- LiPo 6060100（AliExpress）
- PSP互換アナログスティック（AliExpress）
- 秋月 マイクロスピーカー 8Ω 23×16×4.6mm × 2個（P-12494 or P-12495）
- FPCケーブル 30ピン 0.5mmピッチ 複数長さ（筐体CAD後に長さ確定）
- フラットヒートパイプ 3mm厚（曲げ練習用含め 2〜3本）
- 小型ヒートシンク 14×9×4mm 程度 × 4個

---

## 直近の決定事項ログ

### 2026-02-21（session08）
- RP2040外部SPI Flash（W25Q32）必須と確認・BOM追加（VL812用と合わせて計2個）
- RP2040用W25Q32接続方法確定（QSPI 4ビット / /CS 10kΩプルアップのみ）
- LED割り当て詳細確定：GP24=LED_CHG(橙) / GP25=LED_FULL(緑) / GP26=LED_ACT（ADC0兼用）
- ダイオード数訂正：62個→66個
- クリスタル確定：X322512MOB4SI（C70565）/ 12MHz / 12pF / SMD3225-4P / 外付けC 15pF×2

### 2026-02-21（session07）
- キルスイッチ：VSYSラインではなくBQ25895出力後（VSYS→SW→TPS61023/AP2112K VIN）に配置確定
- キーレイアウト確定（66キー / 9×8マトリクス）
- RP2040 GPIO割り当て確定（29本/30本）
- パワーシンボル：VSYS / 5V_SYS / +BATT をカスタムパワーシンボルで作成確定
- connectors シートを新規作成する方針確定
- VL812 usb_hub シート完成

### 2026-02-19
- オーディオ：MAX98357AEWL+T × 2（ステレオ）/ スピーカーはモノラル1個 / 3.5mmジャックはステレオ
- I2S配線：Cubie A7Z GPIO からジャンパ3本（BCLK / LRCLK / SDIN）
- 冷却：パッシブ（ヒートパイプ + 小型ヒートシンク）/ ファン用スペース確保のみ
- USB-C ポートは PWR / DATA 刻印で区別
- 電源スイッチ：モーメンタリ起動 + ロック式キルスイッチ
- LED制御：RP2040 I2C 経由で BQ25895 を読んで制御
- アナログスティック：PSP互換品（カーソル操作用）
- GitHubリポジトリ: PortaRe0 (Public) / D:\Projects\PortaRe0
- KiCadライブラリ取得済み（easyeda2kicad）
- JLCPCB パーツ C番号確定:
  - BQ25895RTWR: C80200
  - VL812: C69417
  - RP2040: C2040
  - TPS61023DRLR: C919459
  - AP2112K-3.3TRG1: C51118
  - MAX98357AEWL+T: C2682619
  - W25Q32JVSSIQ: C82344
  - BSS138: C52895
  - 1N4148W: C2099
  - Alps SKRPABE010: C115360
