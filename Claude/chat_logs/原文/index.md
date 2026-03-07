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

### Session31 (2026-03-03) - 2026-03-03_Session31.txt
- L1: セッション継続・MSK12C02キルスイッチ確定（前回session確定済み）
- L30: P-ch MOSFET（DMP3010LK3-13 / C154730）発熱問題分析（1.6W@8A → TO-252で過熱）
- L60: キルスイッチ案B採用: MSK12C02でTPS61023 ENピン直接制御（COM→EN / NO→GND）
- L80: バッテリーコネクタ: B8B-PH-K-S(垂直)→S8B-PH-K-S（C157915 / 水平）確定
- L100: ヘッドフォンジャック: PJ-393-8P(SMD Extended)→PJ-307C(C16684 TH)に変更
- L130: PJ-307C ピン配置確定（データシートGemini確認）:
  - Pin1=GND / Pin2=L Tip / Pin3=L SW(Pin2ペア) / Pin4=R SW(Pin5ペア) / Pin5=R Ring
- L160: HP_DET回路: Pin4→HP_DET(GP6)/ 100kΩ pull-up / プラグ挿入でHIGH検出
- L190: KiCad audio.kicad_sch: PJ-307C配線完了・pull-up追加
- L220: BOMレビュー: Y4フットプリント誤り修正 / J7/J8空欄=意図的（PCBエッジ）
- L240: **Phase 2 回路設計 全シート完了**
- L383: M.2 SSD追加設計開始
  - Cubie A7Z PCIe Gen3 x1 / F0506-16-BGR（16pin 0.5mm FPC / RPi5互換）確認
  - M.2 2230 NVMe採用 / ソケット: NASM0-S6701-TP40（C367029）
  - FPCコネクタ: FPC-05F-16PH20（C2856801）/ LDO: RT9080-33GJ5（C841192）
  - m2_ssdシート新設・FPC→M.2全ピン接続確定
  - 注意: M.2 Pin42/44/46/48/56 = NC（SATAピン / PCIe x1では未使用）
  - ライブラリ取得済み: C2856801 / C841192 / C367029

### Session30 (2026-03-02) - 2026-03-02_Session30.txt
- L1: フットプリント割り当て状況を全シート調査（316個未割り当てと判明）
- L30: easyeda2kicad 7部品取得（DNS問題→/etc/hosts対応で解決）
  - C115361(SKSCLBE010) / C115360(SKRPABE010) / C9006 / C70565 / C408335 / C3002557 / C19274352
- L60: フットプリント割り当て表作成（全シート）
  - 0603R/C→標準KiCadライブラリ / 1N4148W→SOD-123既存 / IC類→PortaRe0ライブラリ
  - K_SW1/K_SW2（肩ボタン）→KEY-SMD_4P-SKSCLXX010 / K_SW3~K_SW65→KEY-SMD_4P-L4.2-W3.2
- L80: コネクタ検討・決定
  - バッテリー: JST PH 8pin（C157974 B8B-PH-K-S）→ VBAT×4+GND×4 / 8A
  - スピーカー・FAN: JST PH 2pin（C131337 B2B-PH-K-S）
  - J5(hdmi_adapter): PinHeader_2x08_P2.00mm_Vertical（ジャンパワイヤー受けパッド）
  - J7/J8(usb_adapter): PCBエッジFPCテール・コンポーネント不要
- L110: KiCadでフットプリント一括割り当て完了（SW2・J7/J8のみTBD）
- L130: 4層基板構造・キーマトリクスと差動ペアの干渉対策を検討
  - L1=COL/高速信号 / L2=GND面（シールド） / L3=電源 / L4=ROW
  - キーマトリクスエリアと高速信号エリアを物理的に分離する方針確定

### Session29 (2026-03-02) - 2026-03-02_Session29.txt
- L1: セッション開始・git状態確認（最新）
- L20: LED C番号確定（D1赤=C2286 / D2青=C19171394 / D3緑=C19273151 / D4橙=C19273153）
- L60: Vf問題確認（青緑は330Ωで~1.5mA→暗めだが許容）・Extended=手はんだ方針確定
- L80: SW1（電源ボタン）・肩ボタン（Left/Right）→ 側面押し（横押し）に変更
  - Alps SKSCLBE010（C115361）に統一 / SKRPABE010から変更
  - SW2（キルスイッチ / VSYS物理カット / 5A+）は筐体設計後
- L120: TPA6132A2 2.2nFキャップ: audio.kicad_sch追加済みと確認（C1604）
- L130: C6（PMID）10µF 25V品に変更: power.kicad_sch完了（C91606 Murata）

### Session28 (2026-02-28) - 2026-02-28_Session28.txt
- L1: git pull・PROGRESS.md確認・次タスク把握
- L30: PCBレイアウト前の部品確定作業開始（パッケージ0603方針）
- L60: 全シートのパッシブ部品を一覧化 → passive_parts.txt 作成
- L100: usb_hub 10pFキャップ（10本）が100nFと同一ネット → 不要と判断・KiCad削除
- L150: インダクタ要件確認（L1=Idc≥4A / L2,L4=Idc≥2A / L3=DragonBoard実績値）
- L200: インダクタC番号確定（L1=C408335 / L2,L4=C3002557 / L3=C19274352）

### Session27 (2026-02-28) - 2026-02-27_Session27.txt
- L1: git pull（別PCからのpush取得）・前回セッション把握
- L30: 09_TPA6132A2チェックシート照合開始
- L50: HPVDD=チャージポンプ出力（VDD接続NG / 2.2µFのみ）確認
- L70: INL+/INR+→GND / INL−/INR−→信号 と判明（現状逆だった）
- L90: ACカップリング2.2µF + EMIフィルタ(470Ω+2.2nF) 追加決定
- L110: G0=+3V3（0dBゲイン）に変更・全修正KiCad適用
- L130: 09_TPA6132A2 完了 / 10_TPS2042BDR_USBLC6 全ピンOK
- L140: チェックシート照合 全10IC完了 → Phase 3 PCBレイアウトへ

### Session26 (2026-02-27) - 2026-02-27_Session26.txt
- L1: 08_PCM5102Aチェックシート照合開始
- L30: SCK(Pin12)=GND確認（SCK-lessモード・変更不要）
- L50: バイパスキャップ値をTI example準拠に修正（CAPP/CAPM→2.2µF / VNEG/AVDD/DVDD/CPVDD/LDOO→10µF MLCC）
- L80: 音質劣化の影響検討（聴覚上ほぼ問題なし）
- L90: 08_PCM5102A チェックシート完了

### Session25 (2026-02-27) - 2026-02-27_Session25.txt
- L1: git pull（session24の変更取得）
- L20: 04_VL812チェックシート: W25Q32 /CS修正・RESET#確認・LX 10µH確認・SSTX 100nF正常
- L80: 05_RP2040_kbdチェックシート: クリスタルGND23→GND24修正・GP24/GP25追加・USB 27Ω確認・3DS VCC確認
- L150: 06_RP2040_audioチェックシート: #1と同修正適用・全GPIO OK
- L180: 07_MAX98357Aチェックシート: SD_MODE動作確認（220kΩ=RSMALL/Right ch）・GAIN_SLOT浮き=9dB OK

### Session24 (2026-02-27) - 2026-02-26_Session24.txt
- L1: セッション継続（コンテキスト圧縮後）・TPS61023 FB抵抗の検討
- L30: TPS61023 VREF = 0.6V と判明（0.5Vは誤り） → R_TOP: 910kΩ → 750kΩ（5.1V出力）
- L60: キルスイッチ: ENピン制御 → VSYS直列物理カット（5A定格スイッチ必要）
- L80: KiCad修正完了（SW2移動 / usb_hub SW4削除 / R_TOP変更）
- L90: BQ25895修正確認（C5/CE/QONはすでに修正済み）
- L100: AP2112K チェック（全ok / バイパスキャップ1µF→10µF変更）

### Session23 (2026-02-26) - 2026-02-26_Session23.txt
- L1: session23開始・git状態確認（kicad/PDF/ を .gitignore に追加）
- L30: connectorsシートのJ_SBC_USB1/USB2がFPC分離点を持たない問題を指摘
- L60: usb_adapterシート新設方針決定（hdmi_adapterと同じ考え方）
- L100: FPCテール直挿し方式採用（中間コネクタなし / スティフナー直接ZIFへ）
- L130: FPC 24pinピン割り当て確定（差動ペア間GND配置 / USB3.0用・USB2.0用）
- L180: CC抵抗はメインPCB側に配置（FPC部品なし・シンプル化）
- L250: KiCad作業完了・ERC再実行（HP系のみ）
- L500: PROGRESS.md更新・index.md更新・git commit & push
- L600: データシート照合は次回（大画面環境）で実施予定
- L650: BQ25895インダクタ: TI System Examples参考に2.2µH候補（C番号TBD）

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

### Session34 (2026-03-06) - 2026-03-06_Session35.txt（完全版 / Session34は途中抽出）
- L1: セッション開始・PROGRESS.md確認・PCBレイアウト継続
- L57: 電源配線幅の目安（VSYS/5V_SYS/3V3別）・6層基板の基礎説明
- L182: RP2040↔VL812 USB2.0 HS 許容距離（100mm以内・ペア内等長優先）
- L236: L3↔VL812 最短必須（2mm以内・スイッチングループ最小化）
- L284: B.Cu高速差動ペアとIC密集の干渉問題 → USB3.0 SS・HDMIをIn2へ移動
- L510: LS055R1SX04 + MIP-1000 動作確認（PC正常 / スマホ不可）
- L600: MIP-1000特定・STM32 HID（VID_0483/PID_5750）確認・HIDでの制御断念
- L1280: MIP-1000 STM32 HIDドライバ認識・Monitorianで認識不可確認
- L1539: MIPI 60pin配置（LED_VOUT Pin51-53 / LED_1 Pin55 / LED_2 Pin56）
- L1624: LP3320B6F LEDドライバ特定（ENピンPWM調光1%〜100%対応）
- L1700: XIAO ESP32-S3でPWM実験開始・コンパイルエラー修正（ledcAttach新API）
- L1954: XIAO ESP32-S3破損（半田ショート）→ 実験断念
- L2044: 明るさ制御確定: 手動6段階・バウンス式・電源オフ後保持・RP2040制御不要
- L2127: 明るさ調整ボタン→下筐体へ信号線1本（GNDは下筐体から取る）
- L2165: SBC→VL812 USB3.0 距離 20cm以内安全
- L2226: 抵抗・コンデンサ 0402化方針（Basic品→0402 / Extended品→0603維持）
- L2300: 0402 C番号確認・passive_parts.txt大幅更新
- L2400: 10µF分類（3.3Vライン=C15525 0402 / 5V/VSYS/BATT=C96446 0603 25V）
- L終: C6(0402→0603)・C104(0402→0603) KiCad修正完了・CSV確認

### Session33 (2026-03-06) - 2026-03-05_Session33.txt
- L1: セッション開始・PROGRESS.md C番号確定リスト更新
- L30: J4バッテリーコネクタ変更: S8B-PH-K-S → BM06B-ACHFKS-GACN-ETF（JST ACH 6pin）
  - 検討経緯: JST PH → AUH → ACH / 実装高1.43mm / 幅9.1mm / 7.5A
  - バッテリー電流計算（最大5.1A / 通常4.4A）
  - シンボル+フットプリントをPortaRe0ライブラリに追加
- L80: pcb_layout_notes.txt 新規作成（配置方針・発熱量・近接配置・電源フロー）
- L120: specs/index.md PCB層数 4層→6層に更新
- L150: バッテリー上配置可否・発熱量計算（インダクタDCR損失 P=I²×R）
- L200: バッテリー↔IC間の熱的クリアランス検討（3mm〜5mm）

### Session32 (2026-03-04) - 2026-03-04_Session32.txt
- L1: セッション開始・ドキュメント整理の検討
- L30: CONTEXT.md を archive/ に移動・CLAUDE.md 冒頭にセッション開始手順統合
- L60: CLOSING.md 新規作成（終了処理手順の独立ファイル化）
- L90: CLAUDE.md のハードウェア仕様を specs/ に分割（index/power/keyboard/audio/m2_ssd）
- L130: CLAUDE.md 10.4KB → 2.3KB に削減・信頼優先順位を変更
- L160: specs/index.md・CLOSING.md・MEMORY.md・README.md の記述を修正
- L200: session_close.py 新規作成（PROGRESS.mdアーカイブ + git自動化）
- L250: 終了処理フロー確定（extract → Claude更新 → session_close.py）

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

#### TPA6132A2 入力回路（session27）
- シングルエンド入力: INL−/INR−に信号 / INL+/INR+→GND（データシート明記）: S27 L70
- ACカップリング: 2.2µF直列（ポップノイズ防止）: S27 L90
- EMIフィルタ: 470Ω直列 + 2.2nF(→GND) / fc≈154kHz: S27 L90
- G0=+3V3, G1=GND → ゲイン0dB（当初GND/GND=-6dBから修正）: S27 L110
- HPVDD: チャージポンプ正電圧出力 → 2.2µFのみ / VDD接続NG: S27 L50
- EP: GNDPWRのみ（VDD接続はデータシートで明示NG）: S27 L130

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
- usb_adapterシート新設: J_SBC_USB1/USB2移動・FPCテール直挿し方式・24pinピン割り当て確定: S23 L100
- connectorsシートにC2856805（ZIF）×2追加・CC抵抗メインPCB側に配置: S23 L180
- BQ25895インダクタ2.2µH候補（TI System Examples参考）: S23 L650

#### TPS61023 #2（USB専用昇圧）
- 外部USBポートの電力不足問題の指摘: S10 L690
- TPS61023 #2追加決定（出力名USB_5V_SYS）: S10 L711
- usb_hubシートに配置・ENピン→GP24: S10 L757, S10 L716

---

### M.2 SSD / PCIe

- M.2追加決定・Cubie A7Z PCIe Gen3 x1確認: S31 L383
- F0506-16-BGR = 16pin 0.5mm FPC（RPi5互換）: S31 L409
- M.2 2230採用・ソケット選定（C367029 NASM0-S6701-TP40）: S31 L412
- m2_ssdシート設計案・部品リスト: S31 L542
- FPC→M.2全接続図（TX AC結合/RX直結/REFCLK/制御信号）: S31 L703
- FPC→M.2ピン番号対応表: S31 L811
- M.2 Pin42/44/46/48/56 = NC確定（SATAピン / PCIe x1未使用）: S31 L900
- ライブラリ取得: C2856801(FPC 16pin) / C841192(RT9080) / C367029(M.2ソケット): S31 L579

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
- パッシブ部品（抵抗/コンデンサ）全種類: S28 L60（passive_parts.txt参照）
- インダクタ（L1=C408335 / L2,L4=C3002557 / L3=C19274352）: S28 L200
