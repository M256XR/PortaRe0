# PortaRe0 プロジェクト仕様書

> **このファイルが仕様の真実。** 変更時は PROGRESS.md の決定事項ログにも必ず記録すること。
> セッション開始手順・ファイル役割の詳細は **CONTEXT.md** を参照すること。
---

## コンセプト
Cubie A7Z SBCベースのクラムシェル型ポータブルPC（Cyberdeckスタイル）

---

## 筐体仕様
| 項目 | 仕様 |
|------|------|
| フォームファクタ | クラムシェル（ヒンジ構造） |
| ボトム外形 | 139 × 81 mm |
| 素材 | 3Dプリンター（FDM or SLA） |
| ヒンジ | 3Dプリント or 市販品（未確定） |
| ディスプレイ向き | 縦向きパネルを縦で使用 |

---

## 主要コンポーネント

### SBC
- **Cubie A7Z**（Radxa）Allwinner A733 / Cortex-A76×2 + A55×6 / 最大16GB LPDDR4X
- WiFi 6 + BT 5.4 内蔵（外部アンテナ必要、IPEX MHF4）
- USB-C (USB3.0) / USB-C (USB2.0) / Micro HDMI / GPIO 40pin / PCIe Gen3
- 内蔵ファンコネクタ（3ピン 0.8mm 5V）

### ディスプレイ
- **Sharp LS055R1SX04** 5.5" / 1440×2560 / MIPI DSI 4レーン
- **HDMI→MIPI DSIコントローラ基板**（汎用品）をリッド側に搭載

### 電源系

| 部品 | 型番 | JLCPCB C番号 | 役割 |
|------|------|-------------|------|
| 充電IC | BQ25895RTWR | C80200 | USB PD充電 / バッテリー保護内蔵 |
| 昇圧DC-DC #1 | TPS61023DRLR | C919459 | LiPo 3.7V → 5V / システム用（5V_SYS） |
| 昇圧DC-DC #2 | TPS61023DRLR | C919459 | LiPo 3.7V → 5V / 外部USBポートVBUS専用（USB_5V_SYS） |
| LDO | AP2112K-3.3TRG1 | C51118 | 5V → 3.3V（RP2040用） |
| バッテリー | LiPo 6060100 | — | 約3500mAh / 3.7V |

電源フロー:
```
USB-C (充電) → BQ25895 → LiPo 4.2V
LiPo SYS出力 (3.7〜4.2V) → TPS61023 #1 → 5V_SYS → Cubie A7Z / VL812本体 / HDMIコントローラ基板
LiPo SYS出力 (3.7〜4.2V) → TPS61023 #2 → USB_5V_SYS → 外部USBポートVBUS（RP2040 #1 GP24でEN制御）
5V_SYS → AP2112K → 3.3V（RP2040用）
```
注意: BQ25895 SYSラインは最大5〜6A流れる可能性あり → PCBパターン極太で引くこと

電源スイッチ:
- 起動：モーメンタリボタン → TPS61023 EN ピン High
- 通常OFF：SBC GPIO → EN Low（shutdown フック）
- 緊急キル：ロック式スイッチ → EN 強制 Low

### USBハブ

- **VL812**（QFN-76-EP 9x9）C69417
- 外付け：25MHz クリスタル X322525MOB4SI（C9006 / CL=12pF / 負荷C=18pF×2） / W25Q32JVSSIQ SPI Flash（C82344）/ 27Ω 抵抗（SSREXT）

USB 接続構成:
```
Cubie A7Z USB-C (USB3.0) → VL812 upstream
VL812 downstream 1 → 外部USB-C レセプタクル（TPS2042BDR経由 / ESD保護: USBLC6-2SC6）
VL812 downstream 2 → 外部USB-A レセプタクル（TPS2042BDR経由 / ESD保護: USBLC6-2SC6）
VL812 downstream 3 → RP2040 #1（キーボード）
VL812 downstream 4 → RP2040 #2（オーディオ）
Cubie A7Z USB-C (USB2.0) → BQ25895（充電入力 / 刻印:PWR）
Cubie A7Z Micro HDMI → HDMIコントローラ基板
```

外部USBポート電源構成:
- TPS2042BDR（C138720）: VL812 /USBHPE制御、/USBHOC過電流検知
- USBLC6-2SC6（C7519）: Port1/2各1個、ESD保護
- 外部VBUS専用TPS61023 #2（USB_5V_SYS）: RP2040 #1 GP24で制御
- 注意: 外部USBポートはデータ転送・小型デバイス用（HDD等大電流機器は非推奨）

### キーボード・入力

- **RP2040 #1**（キーボード専用）C2040 / QMK対応
- スイッチ：Alps SKRPABE010（SMD タクタイル 4.2×3.2mm）× 63キー（C115360）
- ダイオード：1N4148W（C2099）× 63個
- アナログスティック：3DSスライドパッド（カーソル操作用）/ FPC 4ピン 1.0mmピッチ / VCC=3.3V直結OK
- FPCコネクタ：Molex 5034800440（C3170007）/ 4P 1.0mm ZIF ヒンジ式 / JLCPCB PCBA対応

**RP2040 #1 GPIO割り当て：**
| GPIO | 役割 |
|------|------|
| GP0〜GP8 | キーマトリクス COL（9本） |
| GP9〜GP16 | キーマトリクス ROW（8本） |
| GP17 | I2C_SCL（BQ25895） |
| GP18 | I2C_SDA（BQ25895） |
| GP19 | BQ_INT |
| GP20 | RP2040_EN（TPS61023 EN制御） |
| GP21 | LED_CHG（橙 / BQ25895 I2C読み） |
| GP22 | LED_FULL（緑 / BQ25895 I2C読み） |
| GP23 | LED_ACT（緑 / OS動作表示） |
| GP24 | USB_VBUS_EN（TPS61023 #2 EN制御） |
| GP25 | 予備 |
| GP26 | 予備 |
| GP27（ADC1） | アナログスティック X |
| GP28（ADC2） | アナログスティック Y |
| GP29 | 予備 |

### オーディオ

- **RP2040 #2**（オーディオ専用）C2040 / VL812 DP4経由
- **MAX98357AEWL+T × 2**（C2682619）スピーカー用ステレオI2Sアンプ
- **PCM5102APWR**（C107671）イヤホン用ステレオDAC / TSSOP-20
- **TPA6132A2RTER**（C69901）イヤホン用ヘッドフォンアンプ / WQFN-16
- スピーカー：Nintendo Switch互換品 8Ω 20×14×4mm × 2個（L/R）
- イヤホンジャック：3.5mm TRRS SMT（挿入時スピーカーミュート）
- I2S接続：RP2040 #2 → MAX98357A × 2（スピーカー）/ PCM5102A（DAC）→ TPA6132A2 → ジャック

**RP2040 #2 GPIO割り当て：**
| GPIO | 役割 |
|------|------|
| GP0 | I2S BCLK |
| GP1 | I2S LRCLK |
| GP2 | I2S SDIN |
| GP3 | SD_MODE制御（MAX98357A × 2 / U8は220kΩ直列でRight ch設定） |
| GP4 | XSMT（PCM5102A ミュート制御） |
| GP5 | HP_EN（TPA6132A2 Enable） |
| GP6 | HP_DET（イヤホン挿入検出） |
| GP7〜GP29 | 予備 |

**信号フロー：**
```
Cubie A7Z USB → VL812 DP4 → RP2040 #2（USB Audio）
RP2040 #2 I2S ─┬─→ MAX98357A × 2 → スピーカー L/R
                └─→ PCM5102A（DAC）→ TPA6132A2 → 3.5mmジャック
GP3: スピーカーON/OFF（SD_MODE）
GP4: イヤホンアンプON/OFF（Enable）
GP5: 挿入検出 → GP3/GP4をソフト制御
```

### LED

| LED | GPIO | 色 | 役割 |
|-----|------|----|------|
| 充電中LED | GP21 | 橙 | BQ25895 I2C読み → 充電中点灯 |
| 充電完了LED | GP22 | 緑 | BQ25895 I2C読み → 満充電点灯 |
| ACT LED | GP23 | 緑 | OS動作表示（USB経由でSBCから制御） |

- 各LED: 330Ω直列抵抗 → GND
- パッケージ: SMD（C番号: 未確定）

### 冷却

- 方式：パッシブ（ヒートパイプ + 小型ヒートシンク）
- ヒートパイプ：3mm厚フラット銅製、SoC → 90度曲げ → バッテリー上端の隙間（幅16mm）を通過
- ヒートシンク：14×9×4mm 程度 × 4個（サーマルパッドで密着）
- ファン：スペース確保のみ（Cubie A7Z 内蔵ファンコネクタ経由で後付け可）

---

## PCB 仕様

| 項目 | 仕様 |
|------|------|
| 層数 | 4層（信号 / GND / 電源 / 信号） |
| 製造 | JLCPCB（PCBA込み） |
| HDMI 差動ペア | 90Ω / 等長配線 |
| USB3.0 SS 差動ペア | 90Ω |
| サブ基板 | メインPCBのスロット穴に垂直挿入（SBC接続用） |

---

## KiCad ライブラリ情報

- シンボル：`kicad/PortaRe0_lib/PortaRe0.kicad_sym`
- フットプリント：`kicad/PortaRe0_lib/PortaRe0.pretty/`
- 3Dモデル：`kicad/PortaRe0_lib/PortaRe0.3dshapes/`
- ライブラリ取得コマンド（easyeda2kicad）:
  ```
  python -m easyeda2kicad --full --lcsc_id C番号 --output kicad/PortaRe0_lib/PortaRe0 --overwrite
  ```

---

## セッション終了処理

ユーザーが「終了処理して」と言ったら、以下を自動で実行すること：

1. **セッション原文を保存**
   - `python Claude/extract_session.py` を実行
   - 最新セッションの JSONL が `chat_logs/原文/YYYY-MM-DD_SessionNN.txt` に保存される

2. **PROGRESS.md更新**
   - 「現在の作業箇所」を今日の作業内容に合わせて更新
   - 「直近の決定事項ログ」に今日の日付とセッション番号で決定事項を追記

3. **index.md更新**
   - `chat_logs/原文/index.md` のセッション別索引に今回のセッションを追記
   - 主要トピックのL行番号はおおよその目安でOK
   - トピック別索引に新規トピックがあれば追記

4. **git commit & push**
   - 変更ファイルをまとめてコミット
   - メッセージ形式: `Docs: sessionNN終了処理・PROGRESS/index更新`
   - コミット後に `git push` まで実行する

---

## 概算コスト

| カテゴリ | 概算（USD） |
|----------|------------|
| コンポーネント | $138〜$203 |
| PCB + PCBA（JLCPCB） | $70〜$130 |
| 筐体・機構 | $15〜$40 |
| 合計 | $223〜$373（約3.3〜5.6万円） |
