# PortaRe0 進捗ログ

## 現在のフェーズ
**Phase 2: 回路設計 ✅ 完了 → Phase 3: PCBレイアウト 開始待ち**

## 現在の作業箇所
- PCBレイアウト進行中（session32〜）
  - **次のタスク**: PCBレイアウト継続（部品配置・ルーティング）
  - J7/J8（usb_adapter FPCエッジ）: PCBエッジ設計・コンポーネント不要（変更なし）
  - Session32での主な作業: ドキュメント構成整理（下記参照）
  - Session31での主な確定事項:
    - SW2（キルスイッチ）: MSK12C02（C431540）EN制御方式 / KiCad配線完了
    - J4（バッテリー）: S8B-PH-K-S-LF-SN（C157915）水平型8pin JST PH / フットプリント確定
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
- フラットヒートパイプ 3mm厚 → AliExpress 注文済み ✅
- 3DSスライドパッド → 別途購入予定

## 購入待ちリスト

- 3DSスライドパッド（AliExpress or 中古）
- 秋月 マイクロスピーカー 8Ω 23×16×4.6mm（P-12494 or P-12495）
- FPCケーブル 30ピン 0.5mmピッチ（筐体CAD後に長さ確定）
- 小型ヒートシンク 14×9×4mm程度 × 4個

---

## 直近の決定事項ログ

### 2026-03-04（session32）
- ドキュメント構成を整理・スリム化:
  - CONTEXT.md → `archive/` に移動（廃止）
  - CLAUDE.md 冒頭にセッション開始手順を統合（CONTEXT.md参照不要に）
  - CLOSING.md 新規作成（終了処理手順を独立ファイルに）
  - CLAUDE.md のハードウェア仕様を `specs/` に分割
    - specs/index.md（コンポーネント一覧・筐体・PCB仕様）
    - specs/power.md / keyboard.md / audio.md / m2_ssd.md
  - CLAUDE.md: 10.4KB → 2.3KB に削減
  - 信頼優先順位変更: 原文ログ > specs/* > CLAUDE.md > PROGRESS.md
  - PROJECT_PLAN.md・要約_archive/ → `archive/` に移動（ユーザーが手動）
- session_close.py 新規作成（`Claude/session_close.py`）
  - PROGRESS.md の古いセッションログを `archive/PROGRESS_history.md` に自動移動（直近4件残す）
  - git add -A + commit + push を自動実行
  - 使い方: `python Claude/session_close.py "コミットメッセージ"`
- 終了処理フロー確定:
  1. `python Claude/extract_session.py`（原文保存）
  2. Claude: PROGRESS.md・index.md 更新
  3. Claude: README等確認・更新
  4. `python Claude/session_close.py "..."`（archive + git）

### 2026-03-03（session31）
- M.2 SSD追加設計:
  - Cubie A7Z PCIe Gen3 x1 / F0506-16-BGR（16pin 0.5mm FPC / RPi5互換）
  - M.2 2230 NVMe採用 / ソケット: NASM0-S6701-TP40（C367029）
  - FPCコネクタ: FPC-05F-16PH20（C2856801）/ LDO: RT9080-33GJ5（C841192）
  - m2_ssdシート新設・全ピン接続確定・ライブラリ取得済み
  - 注意: M.2 Pin42/44/46/48/56 = NC（SATAピン / PCIe x1では未使用）
- キルスイッチ確定: MSK12C02（C431540）EN制御方式
  - 当初: DMP3010LK3-13（TO-252 P-ch MOSFET）でVSYS直列カット → 発熱問題（1.6W@8A）で断念
  - 変更: MSK12C02でTPS61023 EN pin直接制御（COM→ENノード / NO→GND）
  - MOSFETは不要（ENピンはµA級 → 発熱ゼロ）
  - GP20→10kΩ→BAT54→ENノード の既存保護回路はそのまま流用
  - KiCad power.kicad_sch: SW2配線完了
- バッテリーコネクタ確定: S8B-PH-K-S-LF-SN（C157915）水平型8pin JST PH
  - B8B-PH-K-S（垂直）からS8B-PH-K-S（水平・サイドエントリー）に変更
  - フットプリント: PortaRe0:CONN-TH_S8B-PH-K-S-LF-SN
- ヘッドフォンジャック確定: PJ-307C（C16684）TH 5pin
  - PJ-393-8P（SMD Extended 8pin）から変更（ExtendedかつSMDで不利）
  - ピン配置（データシート確認）:
    - Pin1=GND(Sleeve) / Pin2=L Tip / Pin3=L SW(Pin2ペア) / Pin4=R SW(Pin5ペア) / Pin5=R Ring
  - 接続: Pin1→GND / Pin2→HP_L / Pin3→NC / Pin4→HP_DET(GP6+100kΩpull-up) / Pin5→HP_R
  - HP_DET動作: プラグ未挿入=Pin4-Pin5導通→LOW / 挿入=Pin4開放+pull-up→HIGH
  - KiCad audio.kicad_sch: 配線完了
- 新規ライブラリ取得（easyeda2kicad）:
  - C431540（MSK12C02 スライドスイッチ）/ C157915（S8B-PH-K-S-LF-SN）
  - C16684（PJ-307C）/ C154730（DMP3010LK3-13 / 未使用）
- BOM確認・修正:
  - Y4フットプリント誤り修正（CONN-TH_B2B-PH-K-S → CRYSTAL-SMD_4P-L3.2-W2.5-BL）
  - J7/J8フットプリント空欄: 意図的（PCBエッジ設計・コンポーネント不要）
- **Phase 2 回路設計 全シート完了 → Phase 3 PCBレイアウトへ**

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
