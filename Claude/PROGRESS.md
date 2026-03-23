# PortaRe0 進捗ログ

## 現在のフェーズ
**Phase 3: PCBレイアウト完了 → 発注準備完了（資金準備待ち）**

## 現在の作業箇所
- **次のタスク**: JLCPCBにてPCBA見積もり確認（サーバーエラーで未確認）→ 発注
  - hdmi_adapter・usb_adapterのガーバー生成はまだ
  - Session41現在: 肩ボタン配置・配線・DRC完了 / ガーバー・CPL生成完了 / BOM確定
  - Session40現在: メインPCB完了・hdmi_adapter完了・usb_adapter（FPC基板）完了
  - Session39現在: MAX98357A I2S・BOOTSELスイッチ・M.2 PCIe配線完了
  - Session38現在: 電源幹線・HUB系・HDMI・USB・SPI Flash・RP2040 Flash・TPS2042・LED配線完了
  - J7/J8（usb_adapter FPCエッジ）: PCBエッジ設計・コンポーネント不要（変更なし）
  - Session33での主な確定事項:
    - J4（バッテリー）: BM06B-ACHFKS-GACN-ETF（JST ACH 6pin）/ 実装高1.43mm / 幅9.1mm / VBAT×3+GND×3 / 7.5A容量
      - DigiKey別途購入・手はんだ / シンボル+フットプリントをPortaRe0ライブラリに追加済み
      - バッテリー側: ACHFR-06V-H + SACHF-003GAC-P0.2×6 / リード線AWG #28に交換必要
      - KiCad J4シンボル差し替え・Pin1-3=VBAT / Pin4-6=GND
    - pcb_layout_notes.txt 新規作成（配置方針・発熱量・近接配置ペア・電源フロー）
    - specs/index.md PCB層数を6層に更新
  - Session32での主な作業: ドキュメント構成整理（下記参照）
  - Session31での主な確定事項:
    - SW2（キルスイッチ）: MSK12C02（C431540）EN制御方式 / KiCad配線完了
    - J9（ヘッドフォンジャック）: PJ-307C（C16684）/ KiCad配線完了 / 100kΩ pull-up追加
    - BOM Y4フットプリント修正: CONN-TH_B2B-PH-K-S → CRYSTAL-SMD_4P-L3.2-W2.5-BL
- KiCad 修正済み（session24-27で実施）:
  - BQ25895: C5(4.7nF→4.7µF) / CE(3V3→GND) / QON(GND→NC)
  - TPS61023: R_TOP(910kΩ→750kΩ, 5.1V出力) / SW2をVSYS直列に移動 / usb_hubのSW4削除
  - AP2112K: バイパスキャップ1µF→10µF
  - VL812: W25Q32 /CS GNDプルダウン→3V3_HUBプルアップ修正
  - RP2040 #1/#2: クリスタルシンボル GND23→GND24 修正 / GP24・GP25接続追加
  - PCM5102A: バイパスキャップ全修正（CAPP/CAPM→2.2µF / VNEG/AVDD/DVDD/CPVDD/LDOO→10µF）
  - TPA6132A2: 入力ピン接続逆転修正（INL+/INR+→GND / INL−/INR−へ信号） / ACカップリング2.2µF+470Ω+2.2nF追加 / G0=+3V3(0dBゲイン) / HPVDD→2.2µF / VDD→100nF+2.2µF

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
- [x] BQ25895 powerシート完成・修正済み（TS分圧固定 / インダクタ1.5µH / 全ピン配線済み）
- [x] TPS61023 回路（EN回路・モーメンタリボタン含む）・修正済み
- [x] AP2112K 回路（5V→3.3V / 常時ON）
- [x] VL812 usb_hub シート（W25Q32 SPI Flash / 25MHz水晶 / デカップリング全完）
- [x] RP2040 keyboard シート完成
  - RP2040本体・電源デカップリング・クリスタル・QSPI Flash・USB・SWD
  - キーマトリクス 63キー（9COL×8ROW / Net Label）
  - 3DSスライドパッド（Molex 5034800440 FPCコネクタ / GP27,GP28）
  - LED × 3（GP21=CHG橙 / GP22=FULL緑 / GP23=ACT緑 / 330Ω）
- [x] audio シート（RP2040 #2 + MAX98357A×2 + PCM5102A + TPA6132A2構成）
  - PJ-307C（C16684 / TH）確定・KiCad配線完了（Pin1=GND / Pin2=HP_L / Pin4=HP_DET+100kΩpull-up / Pin5=HP_R）
- [x] power シートにJ_BAT（汎用2pin）・J_USB_PWR（TYPE-C-31-M-12）追加完了
  - J_BAT: Conn_01x02プレースホルダー / Pin1=+BATT / Pin2=GND
  - J_USB_PWR: VBUS/GND/CC1-CC2(5.1kΩ→GND)/DP1-DN1-DP2-DN2(USB_DP/USB_DM)/SBU=NC/EH=GND
  - ENノード修正: BAT54(D1)をSW→EN間に追加 / PW_SW_DET分圧をD1のSW側に移動（RP2040_EN干渉防止 + τ167ms→1秒改善）
- [x] usb_hub シートに J_EXT_C・J_EXT_A 追加完了 → usb_hub シート完成
  - J_EXT_C: USB31-TYPE-C-FSABC（C2880583）/ CC1/CC2=56kΩ Rp / SS両サイド直結
  - J_EXT_A: HC-USB3.0-L168-WP（C7501850）/ USB3.0 SS対応 / 右角TH
- [x] usb_adapter シート新設（session22）
  - [x] J_SBC_USB1/J_SBC_USB2をconnectorsから移動
  - [x] FPCテール直挿し方式採用（中間コネクタなし）
  - [x] FPC 24pin ピン割り当て確定（差動ペア間GND配置）
  - [x] connectorsシートにC2856805（ZIF）×2追加
  - [x] ERC再実行 → HP系のみ（想定内）
- [x] connectors シート完成（session21）
  - [x] J_HDMI_CTRL: C2856805（24pin 0.5mm FPC）配置・配線完了
  - [x] J_SBC_USB1: C168690（USB-Cオス Vertical SMD）配置・配線完了
  - [x] J_SBC_USB2: C168690（USB-Cオス Vertical SMD）配置・配線完了
  - [x] J_SBC_HDMI: C2856805（24pin / Pin1-19=HDMI信号 / Pin20-21=GND / Pin22-24=NC）配置完了
  - [x] J_FAN: Conn_01x02 + BSS138 + 1kΩ + 10kΩ + 1N4148W / FAN_PWM Global Label
- [x] hdmi_adapter シート新設（別基板・session21）
  - J_MICROHDMI: Conn_02x08（20pin / HDMI信号14本+GND×2+NC×4）
  - FFC側: C2856805（24pin / J_SBC_HDMIと同Net Label）
  - Micro HDMIベアコネクタ → ジャンパワイヤー → 変換基板 → FFC → メインPCB
- [x] m2_ssd シート新設（session31）
  - [x] FPC-05F-16PH20（C2856801）16pin ZIF + RT9080（C841192）LDO + NASM0-S6701-TP40（C367029）M.2ソケット
  - [x] FPC→M.2 全ピン接続確定（TX AC結合100nF / RX直結 / REFCLK直結 / PERST#/CLKREQ#/WAKE#）
  - [x] 3V3_M2レール（5V_SYS→RT9080→M.2 3.3Vピン群）
- [x] 全シートERC実施・主要エラー対処完了（session21）
  - SWCLK/SWDIO × 4 → No Connect（SWD未使用）
  - VL812: SSTX3/SSRX3/SSTX4/SSRX4 → No Connect（RP2040はUSB2.0のみ）
  - VL812: COREPWRDN/TESTEN → GND / SMDAT/SMCLK → 4.7kΩプルアップ→3V3_HUB / EP → GND / DC10FB → 10µF+100nF
  - HP_DET/HP_L/HP_R → No Connect（イヤホンジャック未確定）
  - USB2_DP1_DP 双方向誤報 → ERC除外

### Phase 3: PCBレイアウト ← 次のフェーズ
### Phase 4: 試作・検証 ⏳ 未着手
### Phase 5: 筐体設計・組み立て ⏳ 未着手

---

## 未解決の TBD 事項

| 項目 | 解決タイミング |
|------|--------------|
| インダクタ値 | ✅ 確定（L1=C408335 / L2,L4=C3002557 / L3=C19274352） |
| VL812用 25MHz水晶 C番号 | ✅ C9006確定（負荷C=18pF×2） |
| FPCケーブル長さ（SBC接続用 30ピン 0.5mmピッチ） | 筐体CAD後 |
| キルスイッチ型番 | ✅ 確定（C431540 MSK12C02 / EN制御方式・KiCad完了） |
| モーメンタリスイッチ型番 | ✅ 確定（C115361 SKSCLBE010 / session29確定） |
| LED C番号（緑・橙） | connectors/audioシート時 |
| イヤホンジャック型番 | ✅ 確定（C16684 PJ-307C / TH 5pin / KiCad完了） |
| キーキャップ型番 | スイッチ嵌合確認後 |
| ヒンジ機構 | 筐体CAD後 |
| RTCバッテリー有無 | A7Z実機届いたら確認 |
| ヒートパイプ取り回し経路 | 筐体CAD後 |
| WiFiアンテナ配置 | 筐体CAD後 |

---

## 参照回路図・リファレンス

| 用途 | 資料名 | URL |
|------|--------|-----|
| VL812 実装例（usb_hubシート検証に使用） | DragonBoard 820c Schematics | https://www.96boards.org/documentation/consumer/dragonboard/dragonboard820c/hardware-docs/files/db820c-schematics.pdf |

---

## 購入済み・発注済み

- Cubie A7Z 8GB → AliExpress 注文済み ✅
- LS055R1SX04 + HDMIコントローラ基板セット → AliExpress 注文済み ✅
- LiPo 606090（4200mAh）→ 要発注（6060100から変更）
- VS-CXMIPI-V1（D000118-VS-CXMIPI-V1-50Hz）→ AliExpress 注文済み ✅（5,731円 / UART輝度制御確認用）
- フラットヒートパイプ 3mm厚 → AliExpress 注文済み ✅
- 3DSスライドパッド → 別途購入予定

## 購入待ちリスト

- 3DSスライドパッド（AliExpress or 中古）
- 秋月 マイクロスピーカー 8Ω 23×16×4.6mm（P-12494 or P-12495）
- FPCケーブル 30ピン 0.5mmピッチ（筐体CAD後に長さ確定）
- 小型ヒートシンク 14×9×4mm程度 × 4個

---

## 直近の決定事項ログ

### 2026-03-23（session41）
- 肩ボタン（K_SW1/K_SW2）配置・配線・DRC完了（ROW0-COL0 / ROW0-COL8）
- キースイッチ変更: SKRPAKE010(C19724062) → **SKRPABE010(C115360)** / 62個 / 手はんだ
- 肩ボタン2種類購入して実機で選ぶ方針: SKSCLDE010(163gf・C115362) / SKSCLBE010(224gf・C115361)
- キー数確定: **64キー**（通常62 + 肩2 / Win=ROW7-COL7含む）/ ダイオード65個（64+FAN1）
- BOM更新: cyberdeck_bom.csv反映済み / specs/keyboard.md更新済み
- ガーバー生成完了: `gerber/`（6層・ENIG）
- CPL生成完了: `pos/PortaRe0-all-pos.csv`
- JLCPCB価格確認:
  - 基板単体5枚: **13,000円**（0.2/0.35mmビア・ENIG・6層）
  - デフォルト(0.3/0.4mm)なら7,000円だが0.2/0.35mmビアを526個中266個使用のため変更困難
  - PCBAはJLCPCBサーバーエラーで見積もり未確認（後日）
- Extended/在庫状況確認:
  - VL812(C69417) / M.2ソケット(C367029): 在庫ゼロ → プレオーダーで対応可
  - LED橙(C19273153): JLCPCBパーツライブラリ未確認 → 手はんだなので実害なし
  - BasicはAP2112K/RP2040/C9006/KT-0603Rの4点のみ・他全Extended
- **残り**: hdmi_adapter・usb_adapterのガーバー生成 / PCBAの見積もり → 発注（資金準備後）

### 2026-03-17〜18（session40）
- メインPCB DRC完了・各種制約値をJLCPCBスペックに合わせて修正
  - Defaultネットクラス: クリアランス0.1mm / ビアサイズ0.35mm / ビア穴0.2mm
  - 最小アニュラー幅0.075mm / 最小スルーホール0.2mm / 基板端クリアランス0.25mm
  - EPサーマルビア追加（各IC）/ スポーク最小数1に変更
- キーマトリクス（63キー）配線完了（肩ボタン2個のみ未配線・筐体CAD後）
  - 配線層: F.Cu/In2/In3混在（全体に広がるため層を選ばず使用）
- GNDベタ・Teardrops完了
- hdmi_adapter 新規プロジェクト作成・PCBレイアウト完了
  - 2層基板（Micro HDMIオス + 24pin FFCコネクタのみ）
- usb_adapter FPC基板 新規プロジェクト作成・PCBレイアウト完了
  - JLCPCBフレキシブル基板で発注予定
  - FPCエッジパッドフットプリント: mikeWShef/Kicad_FPC_board_ends から FPC-24P-0.5mm.kicad_mod を取得
  - スティフナー: USB-Cコネクタ部分・FPCエッジ挿入部分に必要（発注時に手動指定）
  - DRC設定: クリアランス0.1mm / アニュラー0.18mm / ビアドリル0.2mm・外径0.56mm / 基板端0.2mm
- software/ フォルダ作成（Claude/・スクリプト・PROGRESS.md等）
- **残り**: 肩ボタン（筐体CAD後）→ JLCPCB発注

### 2026-03-15（session39）
- MAX98357A I2S配線完了（BCLK/LRCLK/SDIN/SD_MODE）
  - B.CuはM.2 PCIeで塞がれており、In2経由（via→In2→via）でM.2エリアを通過
  - U15(R)→U9(L)のL字デイジーチェーン（RP2040 #2が右寄り・L/Rが下左右）
  - SD_MODE: U15エリアで220kΩ経由（Rch）とU9への直結（Lch）に分岐
- RP2040 BOOTSELスイッチ配置・配線完了（#1/#2両方）
  - QSPI_SS信号は低速なので30〜40mm離れた配置でも問題なし
  - #1はバッテリー裏を避けてアクセスしやすい場所に配置
- M.2 PCIe FPC配線完了
  - ACカップリング100nFはFPCコネクタ側（送信元近く）に配置
  - ペア内等長のみ必要・ペア間長さ違いはCDRで吸収されるためOK
- FPC全ピン逆順の懸念確認
  - PCIe FPC: 電源はPCB内（RT9080）生成のためピン逆順でも壊れない・最悪リンク不可のみ
  - HDMI FPC: 実機のHDMIコントローラ基板のHDMIコネクタを外してFPC化するため、はんだ付け時にピン順を合わせれば問題なし
- **残り**: キーマトリクス（63キー）・GNDベタ・Teardrops

### 2026-03-13（session38）
- ルーティング大幅進捗（電源幹線〜USB差動ペアまで完了）
- 電源ルーティング方針: 5V_SYS/VSYS/BATTはIn3ベタ+ビア / B.Cuトレース最小化
  - ビア6個並列でVSYS層間接続（6個×0.3mmドリル≒6A対応）
  - パッド根元0.3mm短区間は許容・Teardrops後で一括補強
- USB-C SS配線: TH側ピンが物理的障害で15mmスタブになるためSMD側のみ接続・TH側NC
  - USB3.0はケーブル挿し方向によりUSB2.0フォールバックあり（許容）
- HDMI（In2）・USB3.0 SS（In2）・USB2.0 HS差動ペアルーターで配線
  - SCL/SDAはI2C（差動ペアではない）→ 個別トレースで配線
  - ACカップリングキャップ前後でネット名変わる箇所は手動2本引き
- VL812 SPI Flash: In3電源ベタ隙間を通して配線・等長11〜12mm・誤差1mm
- RP2040 QSPI Flash: 等長11〜12mm・誤差1mm以内
- TPS2042配線: HUB_1V2をベタ化してIn3スペース確保→大回りルートで完了
- ビアサイズ: JLCPCBスペック確認（最小ドリル0.15mm/外径0.25mm・推奨ドリル0.2mm/外径0.35mm）
- 信号線トレース幅: 0.2mm（JLCPCBルール最小0.1mm）
- **残り**: 電源系IC細かい配線・オーディオ系・RP2040信号線・キーマトリクス・GNDベタ・Teardrops

## JLCPCB C番号確定リスト

### IC・半導体

| 部品 | 型番 | C番号 |
|------|------|-------|
| 充電IC | BQ25895RTWR | C80200 |
| 昇圧DC-DC | TPS61023DRLR | C919459 |
| LDO 3.3V | AP2112K-3.3TRG1 | C51118 |
| M.2 LDO | RT9080-33GJ5 | C841192 |
| USB HUBチップ | VL812-Q7 | C69417 |
| SPI Flash | W25Q32JVSSIQ | C82344 |
| キーボードMCU | RP2040 | C2040 |
| I2Sアンプ | MAX98357AEWL+T | C2682619 |
| イヤホン用DAC | PCM5102APWR | C107671 |
| ヘッドフォンアンプ | TPA6132A2RTER | C69901 |
| USBパワースイッチ | TPS2042BDR | C138720 |
| USB ESD保護 | USBLC6-2SC6 | C7519 |
| MOSFET（FAN/audio） | BSS138 | C52895 |
| Schottkyダイオード（電源保護） | BAT54 | C466635 |
| ダイオード（キーマトリクス） | 1N4148W | C2099 |

### 水晶・インダクタ

| 部品 | 型番 | C番号 |
|------|------|-------|
| クリスタル（RP2040用） | X322512MOB4SI | C70565 |
| クリスタル（VL812用） | X322525MOB4SI | C9006 |
| インダクタ L1（BQ25895 2.2µH） | MWSA0402S-2R2MT | C408335 |
| インダクタ L2/L4（TPS61023 1µH） | CKST322512 | C3002557 |
| インダクタ L3（VL812 10µH） | CYA0420 | C19274352 |

### スイッチ・LED

| 部品 | 型番 | C番号 |
|------|------|-------|
| キースイッチ（63キー） | Alps SKRPAKE010 | C19724062 |
| タクトSW（電源ボタン/肩ボタン×2） | Alps SKSCLDE010 | C115362 |
| キルスイッチ | MSK12C02 | C431540 |
| LED 赤（STAT直結） | KT-0603R | C2286 |
| LED 青（LED_ACT） | YLED0603B | C19171394 |
| LED 緑（LED_FULL） | YLED0603G | C19273151 |
| LED 橙（LED_CHG） | YLED0603O | C19273153 |

### コネクタ

| 部品 | 型番 | C番号 |
|------|------|-------|
| バッテリーコネクタ J4（JST ACH 6pin / VBAT×3+GND×3） | BM06B-ACHFKS-GACN-ETF | DigiKey別途購入 |
| スピーカー/FAN J2/J3/J6（2pin JST PH） | B2B-PH-K-S | C131337 |
| イヤホンジャック J9 | PJ-307C | C16684 |
| M.2ソケット | NASM0-S6701-TP40 | C367029 |
| FPCコネクタ 24pin ZIF（HDMI/SBC用） | FPC-05F-24PH20 | C2856805 |
| FPCコネクタ 16pin ZIF（M.2用） | FPC-05F-16PH20 | C2856801 |
| FPCコネクタ 4pin ZIF（スティック用） | Molex 5034800440 | C3170007 |
| USB-Cオス Vertical（SBC接続） | 918-118A2021Y40000 | C168690 |
| 外部USB-C レセプタクル | USB31-TYPE-C-FSABC | C2880583 |
| 外部USB-A レセプタクル | HC-USB3.0-L168-WP | C7501850 |
