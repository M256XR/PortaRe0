# PortaRe0 進捗ログ

## 現在のフェーズ
**Phase 2: 回路設計 ← 進行中**

## 現在の作業箇所
- KiCad `kicad/PortaRe0/` power・usb_hub・keyboard・audioシート完成
- connectors.kicad_sch 空ファイル作成済み・PortaRe0.kicad_sch に Page6 として追加済み
- **次のタスク**:
  1. usb_hub シートに外部USB-C（J_EXT_C）・外部USB-A（J_EXT_A）を追加
  2. connectors シートにSBC接続コネクタ（J_SBC）・HDMIコントローラFPC（J_HDMI_CTRL）・ファン（J_FAN）を追加

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
- [ ] connectors シート（ファイル作成済み・Page6・コンポーネント未配置）
  - usb_hub: J_EXT_C（外部USB-C）・J_EXT_A（外部USB-A）追加待ち
  - connectors: J_SBC（サブ基板コネクタ）・J_HDMI_CTRL（HDMIコントローラFPC）・J_FAN 追加待ち

### Phase 3: PCBレイアウト ⏳ 未着手
### Phase 4: 試作・検証 ⏳ 未着手
### Phase 5: 筐体設計・組み立て ⏳ 未着手

---

## 未解決の TBD 事項

| 項目 | 解決タイミング |
|------|--------------|
| インダクタ値（BQ25895用 1.5µH / TPS61023用 1µH） | JLCPCB在庫確認後 |
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
