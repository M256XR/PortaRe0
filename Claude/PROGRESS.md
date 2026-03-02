# PortaRe0 進捗ログ

## 現在のフェーズ
**Phase 2: 回路設計 ✅ 完了 → Phase 3: PCBレイアウト 開始待ち**

## 現在の作業箇所
- フットプリント割り当て完了（session30）
  - 全シートのフットプリント割り当て完了（SW2・J7/J8のみTBD）
  - **次のタスク**: PCBレイアウト開始（KiCadボードアウトライン引き→部品配置→ルーティング）
  - SW2（キルスイッチ 5A+スルーホール）: 筐体設計後に確定
  - J7/J8（usb_adapter FPCエッジ）: PCBエッジ設計・コンポーネント不要
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
  - イヤホンジャックはPCBレイアウト時に型番・フットプリント確定予定（HP_L/HP_R/HP_DETはNet Label済み）
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
| キルスイッチ型番 | KiCad フットプリント決める時 |
| モーメンタリスイッチ型番 | KiCad フットプリント決める時 |
| LED C番号（緑・橙） | connectors/audioシート時 |
| イヤホンジャック型番 | PCBレイアウト時（HP_L/HP_R/HP_DETはNet Label済み） |
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
- フラットヒートパイプ 3mm厚 → AliExpress 注文済み ✅
- 3DSスライドパッド → 別途購入予定

## 購入待ちリスト

- 3DSスライドパッド（AliExpress or 中古）
- 秋月 マイクロスピーカー 8Ω 23×16×4.6mm（P-12494 or P-12495）
- FPCケーブル 30ピン 0.5mmピッチ（筐体CAD後に長さ確定）
- 小型ヒートシンク 14×9×4mm程度 × 4個

---

## 直近の決定事項ログ

### 2026-03-02（session30）
- フットプリント割り当て調査・確定:
  - easyeda2kicad取得: C115361(SKSCLBE010) / C115360(SKRPABE010) / C9006 / C70565 / C408335 / C3002557 / C19274352 / C157974 / C131337
  - 全シート316個のフットプリント割り当て完了（SW2・J7/J8のみTBD）
  - DNS問題(/etc/hostsにeasyeda.com追加で解決)
- コネクタ確定:
  - J4（バッテリー）: C157974（B8B-PH-K-S / JST PH 8pin / VBAT×4+GND×4）
  - J2/J3（スピーカー）・J6（FAN）: C131337（B2B-PH-K-S / JST PH 2pin）
  - J5（hdmi_adapter）: PinHeader_2x08_P2.00mm_Vertical（ジャンパワイヤー受けパッド）
- Claude.md冷却セクション更新: ファンはRP2040 #1 GP26→BSS138制御（A7Z内蔵コネクタ不使用）
- passive_parts.txtにコネクタセクション追加
- 4層基板の構造・差動ペアとキーマトリクスの干渉対策を検討

### 2026-03-02（session29）
- LED C番号確定（passive_parts.txtに追記）:
  - D1（赤/BQ25895 STAT直結）: **C2286**（KT-0603R / Basic）
  - D2（青/LED_ACT GP23）: **C19171394**（YLED0603B / Extended / 手はんだ）
  - D3（緑/LED_FULL GP22）: **C19273151**（YLED0603G / Extended / 手はんだ）
  - D4（橙/LED_CHG GP21）: **C19273153**（YLED0603O / Extended / 手はんだ）
- タクトスイッチ確定: 肩ボタン（Left/Right）・SW1（電源ボタン）すべて側面押しに変更
  - **C115361**（Alps SKSCLBE010 / 横押しSMD / 3.6×3.5mm / 2.24N）に統一
  - 旧: SKRPABE010（上押し）→ 新: SKSCLBE010（横押し）
  - KiCad要作業: keyboard.kicad_schの肩ボタン2個 + power.kicad_schのSW1 フットプリント変更
  - SW2（キルスイッチ / VSYS物理カット / 5A+スルーホール）: 筐体設計後に確定
- TPA6132A2 EMIフィルタ 2.2nFキャップ追加: **audio.kicad_sch完了**（R8/R54出力→GND / C番号C1604）
- BQ25895 C6（PMID）電圧変更: **power.kicad_sch完了**（10µF 25V / C番号C91606 / Murata GRM188R61E106MA73D）
  - C19702（10V品）は他の10µFに引き続き使用、C6のみC91606

### 2026-02-28（session28）
- パッシブ部品C番号を全確定 → `Claude/checklists/passive_parts.txt` 作成
  - 抵抗15種類（0603 ±1% 100mW）/ コンデンサ8種類（0603）/ 150µFタンタル1種類
  - Extended Parts: 5種類（27Ω/6.04kΩ/22kΩ/750kΩ/150µFタンタル）→ 追加料金$15
- usb_hub 10pFキャップ削除（KiCad済み）:
  - C27,C29,C31,C33,C35,C37,C39,C40,C43,C45（10本）削除
  - 3V3_HUB/1V2_HUBに100nFが同一ネットに既存のため不要と判断
- インダクタ3種類C番号確定（passive_parts.txtに記録）:
  - L1 (BQ25895 2.2µH): **C408335**（Sunlord MWSA0402S-2R2MT / Idc=4.5A / DCR=58mΩ / 4.4×4.2mm）
  - L2,L4 (TPS61023 1µH ×2): **C3002557**（CENKER CKST322512 / Idc=5A / DCR=30mΩ / 1210）
  - L3 (VL812 10µH): **C19274352**（SHOU HAN CYA0420 / Idc=1.6A / DCR=294mΩ / 4.7×4.2mm）
- 未対応確認事項（次セッションへ）:
  - TPA6132A2 EMIフィルタ 2.2nFキャップ: audio.kicad_sch に未追加（C1604 / INL−/INR−→GND 計2本）
  - BQ25895 C6（PMID）: 10V品 → 25V品への変更要検討
  - LED C番号（D1〜D4）・スイッチ型番（SW1/SW2）未確定

### 2026-02-27（session24）
- IC設計レビュー用チェックシート作成（`Claude/checklists/` 01〜10）
- BQ25895 修正（KiCad済み）:
  - C5: 4.7nF → **4.7µF**（REGN バイパス / 1000倍違いを修正）
  - CE: 3V3 → **GND**（常時充電許可 / I2C制御で無効化可能）
  - QON: GND → **NC**（内部プルアップでHIGH維持・GNDだとシップモードループ）
- TPS61023 修正（KiCad済み）:
  - VREF = 0.6V と判明（チェックシートの0.5Vは誤り）
  - R_TOP: 910kΩ → **750kΩ**（VOUT = 5.1V / VREF=0.6V × (1+7.5) = 5.1V）
  - SW2: ENピン制御 → **VSYS直列物理カット**（5A定格スイッチ必要）
  - usb_hub シートの SW4（#2用キルスイッチ）削除（VSYS共通カットで両方止まる）
- AP2112K: 全ピン問題なし / バイパスキャップ 1µF → **10µF**

### 2026-02-28（session27）
- チェックシート照合 09_TPA6132A2 完了（修正多数）:
  - 入力ピン接続が逆だった → INL−/INR−が信号入力（データシート明記）/ INL+/INR+→GND
  - ACカップリングコンデンサ追加: 2.2µF（ポップノイズ防止）
  - EMIフィルタ追加: 470Ω直列 + 2.2nF(INL−/INR−→GND) → fc≈154kHz
  - G0: GND→+3V3（ゲイン: −6dB→0dB）
  - HPVDD: チャージポンプ出力ピン（VDD接続NG）→ 2.2µFのみ（100nFから変更）
  - VDD: 100nF→100nF+2.2µF追加
  - EP（露出パッド）: GNDPWR接続（VDDへの接続はデータシートで明示NG）
- チェックシート照合 10_TPS2042BDR_USBLC6 完了: 全ピン問題なし
- **IC設計レビュー（チェックシート照合）全10IC完了 → Phase 3 PCBレイアウトへ**

### 2026-02-27（session26）
- チェックシート照合 08_PCM5102A 完了
  - SCK(Pin12): GND接続確認（SCK-lessモード）
  - バイパスキャップ値修正（KiCad済み）:
    - CAPP/CAPM(Pin2/4): 1µF → **2.2µF**（TI example準拠）
    - VNEG(Pin5): 1µF → **10µF** (MLCC)
    - AVDD(Pin8): 100nF+1µF → 100nF+**10µF** (MLCC)
    - DVDD(Pin20): 100nF → 100nF+**10µF** (MLCC) 追加
    - CPVDD(Pin1): 100nF → 100nF+**10µF** (MLCC) 追加
    - LDOO(Pin18): 1µF → 100nF+**10µF** (MLCC)
  - 音質劣化への影響: ほぼ聴こえない範囲（SNR差5〜10dB程度・聴覚限界以下）

### 2026-02-27（session25）
- チェックシート照合 04〜07 完了
  - 04_VL812: W25Q32 /CS GNDプルダウン→3V3_HUBプルアップ修正 / RESET# DragonBoard準拠確認 / LX 10µH確認 / SSTX 100nF ACカップリング正常
  - 05_RP2040_kbd: クリスタルシンボル GND23→GND24修正 / GP24・GP25接続追加 / USB 27Ω外付け正しい（データシート「必須」と明記）/ 3DS VCC 3.3V OK確認
  - 06_RP2040_audio: #1と同じ修正適用 / GPIO GP0〜GP6全OK
  - 07_MAX98357A: SD_MODE回路正常確認（U9=直結=Left / U15=220kΩ直列=Right/RSMALL）/ GAIN_SLOT浮き=9dB OK
- 3DSサークルパッド実物ピン配置確認: Pin1=GND / Pin2=X / Pin3=VCC(1.8V→3.3V使用) / Pin4=Y

### 2026-02-26（session23）
- usb_adapterシート新設（hdmi_adapterと同じ方針）
  - J_SBC_USB1/J_SBC_USB2をconnectorsシートから移動
  - FPCテール直挿し方式採用（中間コネクタなし → スティフナー側にコネクタ不要）
  - FPC 24pinピン割り当て確定（差動ペア間GND配置）
    - USB3.0用: GND/TX+/TX-/GND/RX+/RX-/GND/D+/D-/GND/VBUS/CC1/CC2/GND×11
    - USB2.0用: GND/VBUS/GND/CC1/CC2/GND×19
  - connectorsシートにC2856805（24pin ZIF）×2追加
  - CC抵抗（USB3用5.1kΩ・USB2用22kΩ）はメインPCB側に実装
  - ERC再実行: HP系のみ残存（想定内・イヤホンジャック未確定）
- BQ25895インダクタ値: TI System Examples参考に2.2µHへ変更検討中（C番号はJLCPCB確認後）
- データシート照合は次回セッション（大画面環境）で実施予定

### 2026-02-25（session21）
- J_SBC_HDMI方針最終確定: Micro HDMIベアコネクタ → ジャンパワイヤー → 自作変換基板（hdmi_adapter）→ FFC → ZIF（メインPCB）
  - FFC: C2856805（24pin 0.5mm）をJ_HDMI_CTRLと共通化
  - J_MICROHDMI: Conn_02x08（20pin / GNDまとめて2pin / NC×4）
  - hdmi_adapterを別基板として独立シート新設
- J_FAN: F16FB（SUNON 16×16×4.5mm 5V 0.04A ブロワー型 $8.76）選定確定
  - 回路: GP26(FAN_PWM) → 1kΩ → BSS138 gate / 10kΩプルダウン / 1N4148Wフライバック
  - connectorsシートに配置完了
- GP26割り当て: FAN_PWMとしてGlobal Label追加（keyboardシート・connectorsシート）
- 全シートERC実施・対処完了（詳細はフェーズ完了状況参照）

### 2026-02-25（session20）
- 別PCからgit pull（session19の変更取得）・Claude.mdロール追加コミット
- J_HDMI_CTRL 配置・配線完了
  - ピン順修正: Pin20-21=GND×2（バッファ）/ Pin22-24=5V_SYS×3（EMI低減のためGNDをHDMI信号と電源の間に配置）
- J_SBC_USB1（C168690 USB3.0）配置・配線完了
  - A7Z直結のためTX/RX逆転: A2/B2→USB3_UP_RX_P / A10/B10→USB3_UP_TX_N等
  - CC1/CC2: 5.1kΩ→GND（Rd / UFP識別）
  - VBUS（A4/B4/A9/B9）→USB2_UP_VBUS（VBUSDET分圧へ）
- J_SBC_USB2（C168690 USB2.0）配置・配線完了
  - VBUS→5V_SYS（A7Zへ給電）/ CC1/CC2: 22kΩ→5V_SYS（Rp 3A / DFP/SRC）
  - D+/D- = NC（データ不要 / USB_DP/USB_DMはBQ25895の充電検出用であり無関係）
- J_FAN設計方針確定: RP2040 #1 GP26 → BSS138 gate → ファンGND / 5V_SYS→ファンVCC
- J_SBC_HDMI方針転換: FPVケーブル水平型（出っ張り2cm）は14mmスペースに収まらず断念
  → Micro HDMIケーブル自作用端子（オス+20pin FFC変換）手はんだ方式に決定

### 2026-02-24（session19）
- バッテリー変更: 6060100(5000mAh) → **606090(4200mAh)**
  - サイズ: 6×60×100mm → 6×60×90mm（10mm短縮）
  - SBCポート周辺の空き: 4.3mm → +10mm = 約14mmに改善
  - 稼働時間: 通常使用(8W)で約1.6時間（差分24分・許容範囲）
- J_SBC接続方針確定（FPC2本構成）
  - J_SBC_HDMI: 市販FPVケーブル（Micro HDMIオス+FFC）→テスターでPIN調査→ZIFコネクタ
  - J_SBC_USB: FPCスティフナー + USB-Cオス Vertical SMD（C168690）×2
  - ストラドルコネクタ: PCB厚制約あり・今回は不採用
  - USB-Cオス Vertical SMD（918-118A2021Y40000 / C168690 / USB3.1 / 24P）採用確定
    - Clamping plate不要・スティフナー厚自由・USB 3.0 SuperSpeed対応
    - KiCadライブラリ取得済み（シンボル: TYPE-C 3.1_C168690 / フットプリント: USB-C-SMD_TYPE-C-USB-3）
- extract_session.py のJSONLパスをLinux環境に対応（自動検出に修正）
- 調査待ち: 手持ちFPVケーブルの出っ張り寸法実測・Micro HDMI ZIFコネクタ選定

### 2026-02-24（session18）
- connectors シート設計方針確定
  - J_HDMI_CTRL: 24pin FPC 0.5mm（C2856805 XUNPU FPC-05F-24PH20）に決定
    - Pin1-19: HDMI Type A 19信号（Pin18=+5V for HPD）
    - Pin20-22: 5V_SYS×3（並列 / HDMIコントローラメイン電源）
    - Pin23-24: GND×2
    - HDMIコントローラ基板のHDMI端子（標準タイプ）・Micro-USB端子を外してFPC変換
    - easyeda2kicadでC2856805ライブラリ取得済み
  - SBC接続方式: サブ基板→FPCに変更
    - Cubie A7Zの全ポート（Micro HDMI・USB3.0・USB2.0）は同じ面に集中していることを確認
    - FPCスティフナーにMicro HDMIオス + USB-Cオス×2を直付けする方針
    - 信号構成: Micro HDMI 19本 + USB3.0 SS + USB2.0 + CC + GND = 約40pin FPC
    - PCBマウントオス型コネクタ（Micro HDMI男/USB-C男）はLCSCになし
    - AliExpress/Alibaba経由で調達・手はんだ実装の方針
  - J_SBC_PWR/J_SBC_USB3: USB-C女（USB31-TYPE-C-FSABC）は内部接続に不適と判明
  - J_FAN: Cubie A7Z直結のためメインPCBには不要の可能性あり

### 2026-02-23（session17）
- usb_hub シート完成
  - J_EXT_C: USB31-TYPE-C-FSABC（C2880583）配置・接続完了
    - VBUS×4 → USB1_VBUS / CC1/CC2 → 56kΩ Rp → USB1_VBUS（ホスト側）
    - DP1/DP2・DN1/DN2 A/B両側束ね → USBLC6経由 → USB2_DP1_DP/DM
    - SS A/B両サイド直結（muxなし）→ USB3_DP1_TX/RX
    - SBU=NC / SHELL=GND
  - J_EXT_A: HC-USB3.0-L168-WP（C7501850）配置・接続完了
    - Vbus→USB2_VBUS / D+/D-→USBLC6経由 / SS→USB3_DP2_TX/RX / SHELL=GND
  - コネクタ選定変更: 在庫なし(C319140)→C2880583 / 横向き(C7501850)に変更
  - CC Rp 56kΩ × 2 追加（Default Current / ~900mA アドバタイズ）

### 2026-02-23（session15）
- powerシートのGemini AI評価9点を実スキーマと照合して検証
  - 正真の問題: Point4(D1極性逆)・Point6(SW1→GPIO電圧)・Point9(L1→BAT→SYS誤り)・C5/C6/SYS cap不足
  - Gemini誤報: Point1(TS→REGN正しい)・Point3(ILIM誤認)・Point5(TPS61023 FB計算誤り)・Point8(誤認)
- **powerシート修正完了:**
  - L1接続変更: +BATT → VSYS（NVDC正しいトポロジー）
  - D1極性修正: rotation 180° → 0°（アノード→+3V3/R3、カソード→STAT）
  - R3変更: 10kΩ → 330Ω（LED輝度改善）
  - SW1/RP2040_EN保護回路追加: BAT54ダイオード(C466635)をGP20→ENノード間に挿入
  - ENノードに10µFキャップ追加（起動ラッチ用 τ=1s）
  - SW_DET回路追加: SW1出力→10kΩ分圧→GP25（電源ボタン長押し/短押し検出用）
  - C5変更: 100nF → 4.7µF（REGN cap）
  - C6変更: 4.7µF → 10µF（PMID cap）
  - SYS capに10µF追加（合計20µF / TI推奨値）
- GP25割り当て変更: 予備 → SW_DET（10kΩ分圧でVSYS→2.1V変換）
- BAT54（C466635, SOT-23）をBOMに追加
- ファームウェア設計方針: 短押し=スリープ、長押し=シャットダウン、超長押し=緊急停止

### 2026-02-22（session14）
- Claude Code CLI移行後の最初の動作確認セッション
- PowerShell `Start-Transcript` は Claude Code TUI の出力を取れないことを確認・廃止
- `launch_claude_utf16.ps1` / `chat_logs/raw/` を `.gitignore` に追加
- `Claude/extract_session.py` を新規作成: `~/.claude/projects/` の JSONL → 読みやすい原文テキストに変換
  - ユーザー発言（str）と Claude テキスト応答のみ抽出、tool_result / thinking / tool_use は除外
  - `chat_logs/原文/SessionNN.txt` に自動採番して保存
  - Windows / Linux 両対応
- セッション終了処理の手順1に `python Claude/extract_session.py` を追加（Claude.md 更新済み）
- 今後はターミナルで `claude` を直接起動するだけでOK（ラッパースクリプト不要）

### 2026-02-22（session13）
- Claude Desktop → Claude Code CLI移行の検討・方針決定
- launch_claude.ps1（Windows用）作成: セッション番号自動採番＋Start-Transcriptでチャット原文を自動保存
- launch_claude.sh（Linux用）作成: scriptコマンドで同様のログ取得
- launch_claude.ps1 / launch_claude.sh を .gitignore に追加（git push対象外）
- Claude.mdに「終了処理して」コマンドのセクションを追加（PROGRESS.md更新→index.md更新→git commitを自動化）
- index.mdにSession13を追記・ファイル名 `New session.txt` → `2026-02-22_Session13.txt` にリネーム

### 2026-02-22（session12）
- DragonBoard 820c公式回路図（VL812採用）との照合によりusb_hubシートを修正・検証完了
- SSREXT: 200Ω → **6.04kΩ ±1%**（DragonBoard/VL805/VL815/VL817全て6.04kΩ）
- VBUSDET分圧: 56kΩ+100kΩ → **4.7kΩ+10kΩ**（約3.4V）
- EXTPWRON: +3V3 → **3V3_HUB** に修正（キルスイッチ前の電源から取る）
- RESET#: 100nF → **1µF** に変更 / **100kΩ→GND** 追加
- LX インダクタ: 4.7µH → **10µH**（DragonBoard実績値）
- 水晶シンボル: Device:Crystal_Small（2端子）→ **Device:Crystal_GND24_Small**（4端子）に変更
- 以下はDragonBoardと一致確認済み ✅
  - 水晶負荷C 18pF×2 / DC33FB 4.7µF / DC12FB 10µF+100nF / USBHOC# 10kΩ→3V3_HUB

### 2026-02-22（session11）
- 外部USBポート電源・保護回路確定
  - TPS2042BDR（C138720）: VL812 /USBHPE制御のパワースイッチ（Active-Low）
  - USBLC6-2SC6（C7519）: Port1/2各1個ESD保護
  - TPS61023 #2追加: 外部USBポートVBUS専用昇圧（USB_5V_SYS）
  - RP2040 #1 GP24 → USB_VBUS_EN（TPS61023 #2 EN制御）
  - 注意: 外部USBポートは小型デバイス用（HDD等大電流機器非推奨）
  - 注意: BQ25895 SYSライン最大5〜6A → PCBパターン極太必須
- VL812 downstream割り当て確定
  - Port1 → USB-C外部（TPS2042BDR / USBLC6-2SC6）
  - Port2 → USB-A外部（TPS2042BDR / USBLC6-2SC6）
  - Port3 → RP2040 #1
  - Port4 → RP2040 #2
- VBUSDET修正方針: Upstream VBUSから56kΩ+100kΩ分圧（約3.2V）
- EXTPWRON修正方針: 3V3_HUBへ10kΩプルアップのみ
- MAX98357A SD_MODE修正: U8（Right ch）に220kΩ直列追加
- TPA6132A2 HPVSS修正: GND直結→1µFコンデンサ経由
- LED回路修正: 向きと接続方式修正済み
- RP2040 #1/#2 TESTEN→GND接続修正

### 2026-02-21（session10）
- RP2040を#1（キーボード）/ #2（オーディオ）の2個構成に変更
  - USB Audio + HID Compositeの実装難易度が高いため分離
  - VL812 DP4（空きポート）にRP2040 #2を接続
- LED：個別LED×3のまま変更なし（GP21=CHG橙 / GP22=FULL緑 / GP23=ACT緑 / 330Ω）
- イヤホン構成確定：PCM5102APWR（C107671）+ TPA6132A2RTER（C69901）
  - PCM5102A: I2S→ステレオアナログDAC
  - TPA6132A2: ヘッドフォンアンプ（Enable端子でRP2040制御）
- スピーカー変更：秋月品 → Nintendo Switch互換品 8Ω 20×14×4mm × 2個（L/R独立）
- GPIO再割り当て：
  - RP2040 #1: GP21=LED_CHG / GP22=LED_FULL / GP23=LED_ACT、GP24=USB_VBUS_EN、GP25〜26=予備
  - RP2040 #2: GP0=BCLK, GP1=LRCLK, GP2=SDIN, GP3=SD_MODE, GP4=XSMT, GP5=HP_EN, GP6=HP_DET

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
| イヤホン用DAC | PCM5102APWR | C107671 |
| ヘッドフォンアンプ | TPA6132A2RTER | C69901 |
| USBパワースイッチ | TPS2042BDR | C138720 |
| USB ESD保護 | USBLC6-2SC6 | C7519 |
| VL812用水晶 | X322525MOB4SI | C9006 |
