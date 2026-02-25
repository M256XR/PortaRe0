# PortaRe0 原文チャットログ索引

> 参照形式: SセッションNN LおよそN行目（例: S07 L180）
> ファイル: chat_logs/原文/YYYY-MM-DD_SessionNN.txt
> Session08・Session09は原文ファイルなし（session10内・要約_archive内で内容確認可能）

---

## セッション別索引

### Session01 (2026-02-19) - 2026-02-19_Session01.txt
- L1: プロジェクト概要・クラムシェル型Cyberdeckの構想開始
- L50: Cubie A7Z SBC選定・スペック確認
- L100: ディスプレイ選定（LS055R1SX04 5.5インチ）
- L200: 電源設計・BQ25895充電IC選定
- L300: USBポート割り当て（USB-C USB3.0→ハブ、USB-C USB2.0→充電、Micro HDMI→ディスプレイ）
- L400: VL812 USBハブチップ選定
- L500: 筐体フォームファクタ検討（クラムシェル・ボトム139×81mm）
- L700: キーボードスイッチ選定（Alps SKRPABE010）・アナログスティック検討
- L900: RP2040選定（QMK対応）
- L1100: PCB構成（4層・JLCPCB PCBA）
- L1300: バッテリー選定（LiPo 6060100 / 3500mAh）
- L1500: サブ基板設計（メイン基板スロット穴への垂直挿入方式）
- L1647: コの字構造・PCB to PCB接続方式の確定
- L1800: パッシブ冷却方針（ヒートパイプ＋小型ヒートシンク）

### Session02 (2026-02-19) - 2026-02-19_Session02.txt
- L1: スピーカー選定（秋月 23×16mm 8Ω）・MAX98357Aモノラル→ステレオ変更
- L90: MAX98357A × 2（ステレオ構成）確定
- L150: I2S SD_MODEピンのL/R切り替え方法最初の議論
- L350: AliExpress購入リスト整理（Cubie A7Z・LiPo・ヒートパイプ等）
- L500: 冷却設計（ヒートパイプ経路・ヒートシンク配置）
- L600: BQ25895周辺回路の設計開始・datasheet確認

### Session03 (2026-02-19) - 2026-02-19_Session03.txt
- L1: 前セッション継続確認・KiCad BQ25895配置から再開
- L26: BQ25895ピン配置・全ピン接続指示（VBUS/D+/D-/SCL/SDA/INT/OTG/CE/ILIM/TS/QON）
- L64: STATピン・LEDおよびプルアップ接続
- L87: TS（Pin11）→ REGN分圧方式（10kΩ×2）に修正
- L109: KiCadネットラベル・グローバルラベルの使い分け説明
- L165: TS処理の最終確定：REGN→R6(10kΩ)→TS→R7(10kΩ)→GND
- L198: BQ25895 TSピン接続方法の最終決定

### Session04 (2026-02-19) - 2026-02-19_Session04.txt
- L1: プロジェクト計画書（PROJECT_PLAN.md）保存・電源フロー確定
- L85: BQ25895右側ピン（BAT/SYS/PGND/PAD）接続
- L133: BQ25895上側ピン（SW/BTST/REGN/PMID/DSEL）接続・インダクタ1.5µH
- L165: BQ25895 インダクタ値1.5µH（スイッチング周波数1.5MHz時）確定
- L190: TS分圧接続の最終確定（REGN→R6→TS→R7→GND）
- L260: BQ25895完成・グローバルラベル（I2C_SCL/I2C_SDA）確定
- L400: I2CバスはRP2040経由でBQ25895を読む設計確認
- L500: GNDPWRと通常GNDの使い分け・一点接続

### Session05 (2026-02-20) - 2026-02-20_Session05.txt
- L1: 別PCからpull・power/usb_hubシート完成の状態から継続
- L65: BQ25895 SCL/SDA・USB_DP/USB_DM のグローバルラベル化
- L100: connectors.kicad_schシート新設の決定
- L168: パワーシンボル名（5V_SYS/VSYS）カスタム作成
- L264: +3V3パワーシンボル統一（AP2112K VOUT = +3V3）
- L308: キルスイッチ設計（BQ25895とTPS61023の間・SPDT・充電継続可能）
- L345: 電源フロー確定：+BATT→BQ25895→VSYS→キルスイッチ→TPS61023/AP2112K
- L435: powerシート完了確認・TPS61023 ENピン（モーメンタリ起動）設計
- L500: TPS61023 FB分圧（R9=910kΩ/R10=100kΩ → 5.05V）・インダクタ1µH
- L660: GPIO足りるか確認開始
- L688: KLEレイアウト初回（60キー版）・9×8マトリクス（17本）確定
- L772: ショルダーボタン・Back/Next/RShift追加（66キー版）
- L838: RP2040 GPIO割り当て確定版（GP0-GP28、29本使用）
- L875: keyboard-layout.json保存

### Session06 (2026-02-20) - 2026-02-20_Session06.txt
※Session05と同内容・別デバイスから同じ状態で開始した重複セッション
- L65: BQ25895 SCL/SDA グローバルラベル化
- L168: 5V_SYS/VSYS カスタムパワーシンボル作成
- L308: キルスイッチ設計（SPDT・VSYS後段配置）
- L500: Geminiによる回路図レビュー（TPS61023/AP2112K/BQ25895）
- L549: キルスイッチ位置・AP2112K VIN接続先の確認
- L906: VL812 usb_hubシート作業開始
- L1013: VL812 電源ピン・デカップリング・SPI Flash・ストラップ全配線手順
- L1049: SSREXT→200Ω(1%)確定
- L1051: VBUSDET当初設計（5V_SYS直結・後に修正）
- L1059: EXTPWRON分圧値（22kΩ+47kΩ → 3.41V・後に簡略化）
- L1086: カスタムパワーシンボル（+3V3_HUB/+1V2_HUB）作成
- L1187: Pin40 NC確定

### Session07 (2026-02-21) - 2026-02-21_Session07.txt
- L1: pull・BOM更新・session08の作業内容確認
- L36: session08での作業（RP2040外部QSPI Flash/水晶確定）
- L65: キースイッチ＆ダイオードマトリクスの配線方向（ROW→[>|]→[SW]→COL）
- L220: SKRPABE010 C番号（C115360）在庫54,355個確定
- L286: アナログスティック選定比較（PSP互換/秋月JT8P/3DSスライドパッド）
- L325: 3DSスライドパッド採用決定
- L400: 3DS FPCコネクタ探索（4P 1.0mm ZIF）
- L435: FPCコネクタ確定（Molex 5034800440 / C3170007）
- L460: 3DS VCC 1.8V問題 → 3.3V直結でOKの結論
- L544: keyboard シート設計仕様まとめ（マトリクス/スティック/LED）
- L593: 物理配置ベースのマトリクス割り当て検討
- L680: ROW0〜7 × COL0〜8 の全割り当て表確定
- L720: QMK info.json保存
- L752: GP0〜GP8=COL / GP9〜GP16=ROW 確定
- L795: COL/ROWはローカルネットラベルで完結（シート内）
- L830: アナログスティック接続再確認（GP27/GP28・ADC・100nF）
- L842: ダイオード配置（ROW→[>|]→[SW]→COL）確定
- L1044: JSONパース→63キーに修正確定

### Session10 (2026-02-21) - 2026-02-21_Session10.txt
※session09継続作業（S09原文なし）
- L1: audio.kicad_sch作業継続・session09決定事項まとめ
- L115: イヤホン用IC検討（PCM5102A + TPA6132A2構成）
- L134: PCM5102APWR（C107671）在庫確認
- L139: TPA6132A2RTER（C69901）在庫確認
- L160: オーディオ構成確定（MAX98357A×2 + PCM5102A + TPA6132A2）
- L180: RP2040 2個構成の決定（#1キーボード/#2オーディオ）
- L213: RP2040 #1/#2 GPIO割り当て最終版
- L244: WS2812B廃止・個別LED×3（GP21/22/23）に戻す
- L265: LED GPIO確定（GP21=LED_CHG/GP22=LED_FULL/GP23=LED_ACT）
- L304: GPIO割り当て最終確定
- L351: MAX98357A SD_MODE確定（GP3共通 / LRCLK自動L/R振り分け）
- L375: PCM5102A全ピン接続方針
- L396: XSMT（PCM5102Aミュート）→RP2040 GP4制御
- L406: TPA6132A2全ピン接続方針
- L508: TESTEN→GND / RP2040 #1/#2のUSBラベル確定
- L554: Geminiによるusb_hubシートレビュー（ESD対策/過電流保護の必要性指摘）
- L642: TPS2042BDR採用決定（Active-Low確認・TPS2052Bは使えない）
- L679: TPS2042BDR全ピン確認・接続方針
- L690: 外部USBポート電力問題・TPS61023 #2追加の検討
- L711: TPS61023 #2（USB専用昇圧）追加決定
- L716: TPS61023 #2 ENピン→RP2040 #1 GP24制御
- L757: TPS61023 #2・TPS2042BDR・USBLC6-2SC6をusb_hubシートに配置
- L790: USBLC6-2SC6接続・VBUSDET分圧修正（56kΩ+100kΩ → 3.2V）
- L806: EXTPWRON簡略化（3V3_HUBへ10kΩプルアップのみ）
- L862: connectorシート構成の最終決定

### Session15 (2026-02-22) - 2026-02-22_Session15.txt
- L1: powerシートのGemini AI評価9点を実スキーマと照合・検証
- L50: Point1(TS→REGN)=誤報・Point5(TPS61023 FB)=誤報・Point9(L1→BAT)=正当と確認
- L120: L1接続修正（+BATT→VSYS / NVDC正しいトポロジー）
- L150: D1極性修正（rotation 0°）・R3 10kΩ→330Ω
- L200: SW1/RP2040_EN保護: BAT54ダイオード(C466635)をGP20→ENノード間に挿入
- L250: ENノードに10µFラッチキャップ追加（起動後のSW1離し対策）
- L300: SW_DET回路追加（SW1出力→10kΩ分圧→GP25 / 短押し=スリープ・長押し=シャットダウン）
- L350: C5 100nF→4.7µF（REGN cap）・C6 4.7µF→10µF（PMID cap）・SYS cap +10µF

### Session21 (2026-02-25) - 2026-02-25_Session21.txt
- L1: session20の続き・J_SBC_HDMI方針最終確定（ベアコネクタ+ジャンパワイヤー+自作変換基板）
- L20: hdmi_adapterシート新設（別基板）・J_MICROHDMI(Conn_02x08) + C2856805配置
- L50: FFC 24pin C2856805共通化（J_HDMI_CTRLと同型番）
- L70: J_FAN: F16FB選定（SUNON 16×16×4.5mm 5V 0.04A $8.76）
- L90: J_FAN回路確定（BSS138 + 1kΩ + 10kΩ + 1N4148W / FAN_PWM GlobalLabel）
- L110: connectorsシート・hdmi_adapterシート完成
- L120: 全シートERC実施・対処（SWD NC / VL812未接続ピン / DC10FB追加 / HP系NC）

### Session20 (2026-02-25) - 2026-02-24_Session20.txt
- L1: 別PCからgit pull・stash→pull→stash popでClaude.md自動マージ
- L20: J_HDMI_CTRL 配線方針確定（Pin20-21=GND×2バッファ / Pin22-24=5V_SYS×3）・配置完了
- L40: J_SBC_USB1（C168690）接続方針・配置完了（TX/RX逆転・CC=Rd 5.1kΩ）
- L60: J_SBC_USB2（C168690）接続方針・配置完了（VBUS=5V_SYS / CC=Rp 22kΩ / D+=NC）
- L80: J_FAN方針確定（RP2040 GP26→BSS138→ファン）
- L90: J_SBC_HDMI: 水平FPVケーブル断念（2cm出っ張りで14mmスペースに収まらず）
- L100: Micro HDMI自作用端子（オス+20pin FFC変換）手はんだ方式に決定

### Session19 (2026-02-24) - 2026-02-24_Session19.txt
- L1: J_SBC接続コネクタ調査継続（Micro HDMIオスPCBマウント品の入手性）
- L30: ストラドルコネクタのPCB厚制約問題 → 非ストラドル方向に方針転換
- L60: バッテリー変更: 606090(4200mAh)でSBCポート周辺に+10mm確保
- L80: FPVケーブル(Micro HDMI+FFC)市販品でPIN調査する方針確定
- L100: USB-Cオス Vertical SMD（C168690 / USB3.1）採用確定・ライブラリ取得
- L120: J_SBC FPC2本構成確定（HDMI用・USB用分離）
- L130: extract_session.pyをLinuxパス対応に修正

### Session18 (2026-02-24) - 2026-02-23_Session18.txt
- L1: connectors シート設計方針の検討開始
- L20: J_HDMI_CTRL: 24pin FPC 0.5mm（C2856805）に決定・ライブラリ取得
- L40: HDMIコントローラ基板はHDMI端子（標準）+Micro-USB → FPCに置換方針確定
- L60: 5V供給: HDMI Pin18(55mA・HPD用) + FPC Pin20-22(5V_SYS×3並列・メイン電源)
- L80: SBC接続: サブ基板→FPCに変更（ずれたとき修正可能なため）
- L100: Cubie A7Z全ポートが同じ面に集中していることを確認
- L120: FPCスティフナーにMicro HDMIオス+USB-Cオス×2直付け方針
- L140: PCBマウントオス型コネクタはLCSCになし → AliExpress調達+手はんだ方針
- L160: SBC接続FPC全信号: Micro HDMI 19本+USB3.0 SS+USB2.0+CC+GND = 約40pin

### Session17 (2026-02-23) - 2026-02-23_Session17.txt
- L1: usb_hub シートの続き（J_EXT_C / J_EXT_A 追加）
- L20: USB-C コネクタ在庫なし(C319140) → SB31-TYPE-C-FSABC(C2880583)に変更
- L30: USB-A コネクタ向き確認 → 横向き HC-USB3.0-L168-WP(C7501850) に変更
- L40: CC1/CC2 Rp 56kΩ（Default Current / ホスト DFP）確定
- L60: easyeda2kicad で C2880583・C7501850 取得
- L80: J_EXT_C / J_EXT_A 接続リスト確認・配置完了 → usb_hub シート完成

### Session16 (2026-02-23) - 2026-02-23_Session16.txt
- L1: Claudeの役割方針確認（回路設計アシスタント・kicad_sch直接編集しない）・CLAUDE.md更新済み確認
- L30: powerシート残作業の整理（J_BAT・J_USB_PWR・ENノード修正）
- L50: バッテリーコネクタ検討（JST SH / Molex Picoblade → いったん汎用2pinで保留）
- L80: TPS61023 ENノード回路レビュー（現状: EN→100kΩ/10μF/BAT54/分圧/SW→VSYS）
- L110: PW_SW_DET問題発見: RP2040_EN=HIGHのときENノード経由で常時1.5V→検出不能
- L130: 修正案: SW→EN間にBAT54(D1)追加 / PW_SW_DET分圧をD1のSW側に移動
- L150: D1追加でτも167ms→1秒に改善（ブート時間問題も同時解決）
- L170: J_USB_PWR（TYPE-C-31-M-12）接続方針確認・配置完了
- L190: ENノード修正・J_BAT・J_USB_PWR配置完了 → powerシート完成

### Session14 (2026-02-22) - 2026-02-22_Session14.txt
- L1: Claude Code CLI 移行後の最初の動作確認
- L10: PowerShell Start-Transcript が Claude Code TUI を取れない問題の調査
- L40: Git Bash に script コマンドなし / WSL は native install 必要と確認
- L70: Claude Code が ~/.claude/projects/ に JSONL を自動保存していることを発見
- L90: extract_session.py 作成・動作確認（JSONL → 読みやすい原文テキスト）
- L110: セッション終了処理に extract_session.py を組み込み（Claude.md 更新）
- L120: launch_claude_utf16.ps1 / chat_logs/raw/ を .gitignore に追加

### Session13 (2026-02-22) - 2026-02-22_Session13.txt
- L1: Claude Desktop落下によるセッション消失の問題整理
- L30: lucid-fermiワークツリー確認・session12の作業はコミット済みと確認
- L80: セッション原文ログが保存されていないことが本質的な問題と確認
- L120: Claude Desktop → Claude Code CLI移行の検討
- L150: Start-Transcript / scriptコマンドによる自動ログ取得方針決定
- L200: launch_claude.ps1（Windows用）作成・セッション番号自動採番機能付き
- L280: launch_claude.sh（Linux用）作成
- L310: launch_claude.ps1 / launch_claude.sh を .gitignore に追加
- L350: 「終了処理」コマンドをClaude.mdに追加・index.md更新の自動化

---

## トピック別索引

### 電源系

#### BQ25895
- 選定・概要: S01 L200
- TS処理（REGN分圧 R6/R7各10kΩ）: S03 L87, S03 L165, S04 L190
- プルアップ（+3V3）SCL/SDA/INT/QON: S03 L64
- ILIM抵抗（270Ω→2A制限）: S03 L86
- インダクタ値（1.5µH / スイッチング1.5MHz）: S04 L165
- BATおよびSYSデカップリング: S04 L85
- DSEL→GND（BC1.2無効）: S04 L133
- BTST(100nF→SW) / REGN(100nF→4.7µF修正) / PMID(4.7µF→10µF修正): S04 L133, S15 L350
- I2C SCL/SDA グローバルラベル化: S05 L65, S06 L65
- BQ_INT グローバルラベル: S03 L83
- 完成確認: S04 L260

#### TPS61023
- 選定: S01 L200
- FB分圧（R9=910kΩ / R10=100kΩ → 5.05V出力）: S05 L500, S06 L502
- EN制御（モーメンタリ起動・100kΩプルダウン）: S05 L435, S05 L504
- インダクタ値（1µH / 3A以上）: S05 L500
- 入出力コンデンサ（CIN=10µF / COUT=22µF+100nF）: S05 L500
- TPS61023 #2（USB用）追加: S10 L711
- TPS61023 #2 ENピン→RP2040 #1 GP24制御: S10 L716

#### AP2112K LDO
- 選定: S01 L200
- VIN→5V_SYS / EN→5V_SYS直結（常時ON）: S05 L513
- VOUT→+3V3: S05 L264
- デカップリング（1µF×2）: S05 L513

#### 電源スイッチ
- キルスイッチ位置確定（VSYS→SW→TPS61023/AP2112K VIN）: S05 L308, S05 L345
- SPDT・NC端未接続: S05 L466
- モーメンタリボタン（SW1）起動回路: S05 L504
- SW1保護回路修正: BAT54(C466635)をGP20→ENノード間に挿入 / 10µFラッチキャップ追加: S15 L200
- SW_DET追加: SW1→10kΩ分圧→GP25（電源ボタン短押し/長押し検出）: S15 L300
- ENノード修正(S16): BAT54(D1)をSW→EN間追加 / PW_SW_DET分圧をD1のSW側に移動（RP2040_EN干渉防止・τ1秒確保）: S16 L110
- 充電時もキルスイッチOFFで充電継続可能: S05 L354

#### パワーシンボル構成
- カスタムパワーシンボル（VSYS/5V_SYS）作成: S05 L168, S06 L207
- +BATT / VSYS / 5V_SYS / +3V3 の体系確定: S05 L345
- GNDPWR と GND の一点接続: S04 L500
- +3V3_HUB / +1V2_HUB（VL812用）カスタム作成: S06 L1086

---

### VL812 USBハブ

#### 電源構成
- VCC5I（Pin19,38）→5V_SYS: S06 L1013
- DC33FB（Pin18）→+3V3_HUB + 100nF: S06 L1014
- DC12FB（Pin37）→+1V2_HUB / LX（Pin39）→L(4.7µH)→+1V2_HUB: S06 L1016
- Pin40 NC確定: S06 L1187

#### デカップリング
- VDD×3ピン（30,48,58）各10µF+100nF: S06 L1020
- VSUS33×3ピン（36,41,49）各100nF: S06 L1021
- VCCA33系（2,8,27,71）各100nF+10pF: S06 L1022
- VCCA12系（5,13,24,61,68,74）各100nF+10pF: S06 L1023

#### SPI Flash（W25Q32）接続
- SPICS/SPISCLK/SPISI/SPISO（Pin32-35）接続・各100kΩプルダウン: S06 L1038, S10 L789
- /HOLD, /WP → 10kΩプルアップ（+3V3_HUB）: S10 L789

#### 水晶（25MHz）
- SSXI/SSXO（Pin75,76）→25MHz水晶 + 負荷C(15pF×2): S06 L1055

#### SSREXT抵抗値
- SSREXT（Pin1）→200Ω(1%)→GNDPWR: S06 L1049

#### VBUSDET / EXTPWRON
- VBUSDET当初（5V_SYS直結）→修正後（Upstream VBUSから56kΩ+100kΩ分圧→3.2V）: S06 L1051, S10 L800
- EXTPWRON当初（22kΩ+47kΩ分圧→3.41V）→簡略化（3V3_HUBへ10kΩプルアップ）: S06 L1059, S10 L806

#### USBHPE / USBHOC
- USBHOC1(45)/USBHOC2(44)→10kΩ→+3V3_HUB: S06 L1053
- USBHPE1(43)/USBHPE2B(42)→TPS2042BDRと接続: S10 L679

#### ACカップリング有無ルール
- Upstream TX（Pin22,23）→100nF ACカップリング挿入: S10 L789
- DP1/DP2 TX→100nF ACカップリング挿入: S10 L789
- RX側（Upstream/Downstream全て）→直結（ACカップリングなし）: S10 L789

#### ダウンストリームポート割り当て
- DP1（Pin64,65 D+/D- / Pin59-63 SS）→外部USB-C（TPS2042BDR/USBLC6-2SC6）: S06 L1033, S10 L789
- DP2（Pin72,73 D+/D- / Pin66-70 SS）→外部USB-A（TPS2042BDR/USBLC6-2SC6）: S06 L1034, S10 L789
- DP3（Pin9,10 D+/D-）→RP2040 #1（キーボード）: S06 L1035, S10 L201
- DP4（Pin16,17 D+/D-）→RP2040 #2（オーディオ）: S10 L201

---

### キーボード（RP2040 #1）

#### キーレイアウト
- KLEデータ初回（60キー）: S05 L688
- ショルダーボタン・Back/Next/RShift追加（66キー版）: S05 L772
- keyboard-layout.json保存: S05 L875
- JSONパース→63キーに修正確定: S07 L1044

#### ダイオード向き・接続方式
- Col2Row方式（ROW→スイッチ→ダイオード→COL / アノードがROW側）: S07 L65, S07 L842
- 1N4148W（カソード=COL側）: S07 L65

#### キーマトリクス割り当て
- 9COL × 8ROW（17本）確定: S05 L750
- 物理配置ベース割り当て表（ROW0〜7 × COL0〜8）: S07 L680
- QMK info.json保存: S07 L720
- COL/ROWはローカルネットラベル（シート内完結）: S07 L795

#### GPIO割り当て（RP2040 #1）
- GP0〜GP8=COL / GP9〜GP16=ROW 確定: S07 L752
- GP17=I2C_SCL / GP18=I2C_SDA / GP19=BQ_INT / GP20=RP2040_EN: S05 L838, S10 L304
- GP21=LED_CHG / GP22=LED_FULL / GP23=LED_ACT: S10 L265
- GP24=USB_VBUS_EN（TPS61023 #2 EN制御）: S10 L716, S10 L304
- GP25=SW_DET（電源ボタン検出 / 10kΩ分圧）: S15 L300
- GP27=スティックX(ADC1) / GP28=スティックY(ADC2): S07 L752, S10 L304

#### アナログスティック（3DSスライドパッド）
- 選定比較（PSP互換/秋月JT8P/3DS）: S07 L286
- 3DSスライドパッド採用決定（感触◎・薄型）: S07 L325
- FPCコネクタ確定（Molex 5034800440 / C3170007 / 4P 1.0mm ZIF）: S07 L435
- ピンアサイン（GND/X軸/VCC=3.3V直結/Y軸）: S07 L456, S07 L497
- 接続回路（GP27=X ADC / GP28=Y ADC / 100nFデカップリング）: S07 L830

#### LED回路
- 当初設計（GP24〜GP26 + 330Ω）: S05 L849
- WS2812B採用→レベルシフト問題で廃止: S10 L244
- 個別LED×3 確定（GP21/22/23 / 330Ω / アクティブHigh）: S10 L265

#### 外部SPI Flash（W25Q32）
- QSPI Flash必須確認・4ビット接続: S07 L38
- 水晶: X322512MOB4SI（C70565 / 12MHz）: S07 L38（session08からの引用）

---

### オーディオ（RP2040 #2）

#### MAX98357A SD_MODE設定
- 当初（R35 210kΩ → +3V3固定でL/R切り替え）: S02 L150
- 変更後（GP3共通 → LRCLK自動L/R振り分け / U8に220kΩ直列追加）: S10 L351, S10 L363

#### PCM5102A / TPA6132A2 追加の経緯
- USB Audio + HID Composite実装困難 → RP2040を2個に分割: S10 L180
- イヤホン用PCM5102A（DAC）+ TPA6132A2（HPアンプ）追加決定: S10 L160
- PCM5102APWR C番号（C107671）: S10 L134
- TPA6132A2RTER C番号（C69901）: S10 L139
- PCM5102A接続方針（AVDD/DVDD=+3V3/I2S/XSMT→GP4）: S10 L375, S10 L396
- TPA6132A2接続方針（チャージポンプ/ゲイン0dB/EN=GP5）: S10 L406

#### スピーカー選定
- 秋月 23×16×4.6mm 8Ω確定（当初）: S02 L1
- Nintendo Switch互換品 8Ω×2（20×14×4mm）に変更: S10 L488

#### GPIO割り当て（RP2040 #2）
- GP0=BCLK / GP1=LRCLK / GP2=SDIN: S10 L213
- GP3=SD_MODE / GP4=XSMT / GP5=HP_DET / GP6=HP_EN: S10 L213, S10 L396

#### connectorシート構成
- 最終決定（USB外部→usb_hub / 充電・バッテリー→power / SBC接続→connectors）: S10 L862

---

### 外部USBポート

#### TPS2042BDR採用
- VL812 UBSHPEがActive-Low → TPS2052B不可 → TPS2042BDR採用: S10 L642, S10 L794
- TPS2042BDR全ピン確認・接続方針: S10 L679
- C番号: C138720（LCSC）: S10 L642

#### USBLC6-2SC6 ESD保護
- GeminiレビューによるESD対策の必要性指摘: S10 L554
- USBLC6-2SC6採用（Port1/Port2それぞれ1個ずつ / C7519）: S10 L764, S10 L828

#### 外部コネクタ（J_EXT_C / J_EXT_A）
- J_EXT_C: USB31-TYPE-C-FSABC(C2880583) / CC 56kΩ Rp / SS両サイド直結: S17 L80
- J_EXT_A: HC-USB3.0-L168-WP(C7501850) / USB3.0 SS対応 / 横向きTH: S17 L80
- usb_hub シート完成: S17 L80

#### SBC接続・connectors シート（session18-19）
- J_HDMI_CTRL: 24pin FPC 0.5mm (C2856805 XUNPU FPC-05F-24PH20): S18 L20
  - Pin1-19=HDMI Type A / Pin20-22=5V_SYS×3 / Pin23-24=GND×2
  - HDMIコントローラのHDMI端子+Micro-USB外してFPC変換
- J_SBC FPC2本構成確定（S19）
  - J_SBC_HDMI: 市販FPVケーブル（Micro HDMIオス+FFC）→テスターでPIN調査→ZIFコネクタ: S19 L80
  - J_SBC_USB: FPCスティフナー + USB-Cオス Vertical SMD（C168690）×2: S19 L100
  - ストラドルコネクタ廃案（PCB厚制約・非ストラドルに変更）: S19 L30
- バッテリー変更: 6060100(5000mAh) → 606090(4200mAh) / SBCポート周辺+10mm確保: S19 L60
- USB-Cオス Vertical SMD: 918-118A2021Y40000 / C168690 / USB3.1 / KiCadライブラリ取得済: S19 L100
- J_HDMI_CTRL配置完了（Pin順修正: GND×2バッファ→5V_SYS×3）: S20 L20
- J_SBC_USB1/USB2（C168690）配置完了: S20 L40, L60
- J_SBC_HDMI: FPVケーブル断念→Micro HDMI自作端子+20pin FFC方式: S20 L90
- J_SBC_HDMI最終確定: ベアコネクタ+ジャンパワイヤー+自作変換基板(hdmi_adapter)+FFC(C2856805 24pin): S21 L1
- hdmi_adapterシート新設（別基板）: J_MICROHDMI(Conn_02x08) + C2856805: S21 L20
- J_FAN: F16FB(SUNON 16×16×4.5mm 5V 0.04A)選定・回路完成(BSS138/FAN_PWM): S21 L70
- connectorsシート・hdmi_adapterシート完成・ERC対処完了: S21 L110

#### TPS61023 #2（USB専用昇圧）
- 外部USBポートの電力不足問題の指摘: S10 L690
- TPS61023 #2追加決定（出力名USB_5V_SYS）: S10 L711
- usb_hubシートに配置・ENピン→GP24: S10 L757, S10 L716

---

### 全体設計

#### 筐体フォームファクタ
- クラムシェル型・ボトム139×81mm: S01 L500
- サブ基板（メイン基板スロット穴・垂直挿入・カードエッジ方式）: S01 L1647

#### 採用しなかった案
- アナログスティック: PSP互換・秋月JT8P → 3DS採用: S07 L286
- LED: WS2812B（レベルシフト問題）→ 個別LED採用: S10 L244
- オーディオ: モノラル→ステレオ→RP2040×2構成: S02 L90, S10 L180
- 過電流保護: TPS2052B（Active-High・不適）→ TPS2042BDR採用: S10 L642

#### C番号確定タイミング
- SKRPABE010: C115360: S07 L220
- X322512MOB4SI（RP2040用水晶）: C70565: S07 L38（session08引用）
- Molex 5034800440: C3170007: S07 L485
- PCM5102APWR: C107671: S10 L134
- TPA6132A2RTER: C69901: S10 L139
- TPS2042BDR: C138720: S10 L642
- USBLC6-2SC6: C7519: S10 L764
- BAT54（Schottky / SW1保護用）: C466635: S15 L200
