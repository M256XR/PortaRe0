# PortaRe0 プロジェクト仕様書

> 確定済みの仕様のみ記載。変更時は PROGRESS.md の決定事項ログにも記録すること。
> 最初にGithub側で別PCの作業による変更があるか確認すること
> セッション開始時の読み込み順: CONTEXT.md → PROGRESS.md → PROJECT_PLAN.md → chat_logs/（最新セッションログを必ず読む）→ 必要に応じて過去ログ
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
| 昇圧DC-DC | TPS61023DRLR | C919459 | LiPo 3.7V → 5V / 最大3.7A |
| LDO | AP2112K-3.3TRG1 | C51118 | 5V → 3.3V（RP2040用） |
| バッテリー | LiPo 6060100 | — | 約3500mAh / 3.7V |

電源フロー:
```
USB-C (充電) → BQ25895 → LiPo 4.2V
LiPo SYS出力 (3.7〜4.2V) → TPS61023 → 5V
5V → AP2112K → 3.3V（RP2040用）
5V → Cubie A7Z / VL812 / HDMIコントローラ基板
```

電源スイッチ:
- 起動：モーメンタリボタン → TPS61023 EN ピン High
- 通常OFF：SBC GPIO → EN Low（shutdown フック）
- 緊急キル：ロック式スイッチ → EN 強制 Low

### USBハブ

- **VL812**（QFN-76-EP 9x9）C69417
- 外付け：25MHz クリスタル / W25Q32JVSSIQ SPI Flash（C82344）/ 27Ω 抵抗（SSREXT）

USB 接続構成:
```
Cubie A7Z USB-C (USB3.0) → VL812 upstream
VL812 downstream 1 → 外部USB-C レセプタクル（刻印:DATA）
VL812 downstream 2 → 外部USB-A レセプタクル
VL812 downstream 3 → RP2040（キーボード）
Cubie A7Z USB-C (USB2.0) → BQ25895（充電入力 / 刻印:PWR）
Cubie A7Z Micro HDMI → HDMIコントローラ基板
```

### キーボード・入力

- **RP2040** C2040 / QMK対応
- スイッチ：Alps SKRPABE010（SMD タクタイル 4.2×3.2mm）× 66キー + ショルダー2個（C115360）
- ダイオード：1N4148W（C2099）× 66個
- アナログスティック：PSP互換品（カーソル操作用）

### オーディオ

- **MAX98357AEWL+T × 2**（C2682619）ステレオ構成
- スピーカー：秋月 マイクロスピーカー 8Ω 23×16×4.6mm × 1個（片チャンネル）
- イヤホンジャック：3.5mm TRRS SMT（挿入時スピーカーミュート）
- I2S 接続：Cubie A7Z GPIO → ジャンパ3本（BCLK / LRCLK / SDIN）

### LED

| LED | 制御 | 役割 |
|-----|------|------|
| 電源LED（緑） | TPS61023 出力（5V） | 電源ON中点灯 |
| 充電中LED（橙） | RP2040（BQ25895 I2C読み） | 充電中点灯 |
| 充電完了LED（緑） | RP2040（BQ25895 I2C読み） | 満充電点灯 |
| ACT LED | RP2040（USB経由でSBCから制御） | OS動作表示 |

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

## 概算コスト

| カテゴリ | 概算（USD） |
|----------|------------|
| コンポーネント | $138〜$203 |
| PCB + PCBA（JLCPCB） | $70〜$130 |
| 筐体・機構 | $15〜$40 |
| 合計 | $223〜$373（約3.3〜5.6万円） |
