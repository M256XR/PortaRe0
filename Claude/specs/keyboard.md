# キーボード・入力・LED 詳細仕様

---

## キーボード・入力

- **RP2040 #1**（キーボード専用）C2040 / QMK対応
- スイッチ：Alps SKRPABE010（SMD タクタイル 4.2×3.2mm）× 63キー（C115360）
- ダイオード：1N4148W（C2099）× 63個
- アナログスティック：3DSスライドパッド / FPC 4ピン 1.0mmピッチ / VCC=3.3V直結OK
- FPCコネクタ：Molex 5034800440（C3170007）/ 4P 1.0mm ZIF ヒンジ式

### RP2040 #1 GPIO割り当て

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
| GP23 | LED_ACT（青 / OS動作表示） |
| GP24 | USB_VBUS_EN（TPS61023 #2 EN制御） |
| GP25 | SW_DET（電源ボタン検出 / 10kΩ分圧でVSYSを3.3V以下に変換） |
| GP26 | J_FAN PWM（BSS138 gate制御） |
| GP27（ADC1） | アナログスティック X |
| GP28（ADC2） | アナログスティック Y |
| GP29 | 予備 |

---

## LED

| LED | GPIO | C番号 | 色 | 役割 |
|-----|------|--------|----|------|
| D1 | STAT直結 | C2286（KT-0603R） | 赤 | BQ25895 STAT端子直結 |
| D2 | GP23 | C19171394（YLED0603B） | 青 | LED_ACT（OS動作表示） |
| D3 | GP22 | C19273151（YLED0603G） | 緑 | LED_FULL（満充電） |
| D4 | GP21 | C19273153（YLED0603O） | 橙 | LED_CHG（充電中） |

- D2〜D4: Extended / 手はんだ対象
- 各LED: 330Ω直列抵抗 → GND / パッケージ: 0603

---

## キーマトリクス

- 構成：9COL × 8ROW / 計72セル（使用63 / 空き9）
- COL方向：縦 / ROW方向：横
- ダイオード向き：ROW → [>|] → SW → COL（カソードがSW側）
- 詳細：`keyboard/matrix.md`
