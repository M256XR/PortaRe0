# オーディオ 詳細仕様

---

## 構成部品

- **RP2040 #2**（オーディオ専用）C2040 / VL812 DP4経由
- **MAX98357AEWL+T × 2**（C2682619）スピーカー用ステレオI2Sアンプ
- **PCM5102APWR**（C107671）イヤホン用ステレオDAC / TSSOP-20
- **TPA6132A2RTER**（C69901）イヤホン用ヘッドフォンアンプ / WQFN-16
- スピーカー：Nintendo Switch互換品 8Ω 20×14×4mm × 2個（L/R）
- イヤホンジャック：PJ-307C（C16684 / TH 5pin）

### イヤホンジャック ピン配置

| ピン | 接続 | 備考 |
|------|------|------|
| Pin1 | GND | Sleeve |
| Pin2 | HP_L | L Tip |
| Pin3 | NC | L SW（Pin2ペア） |
| Pin4 | HP_DET（GP6 + 100kΩ pull-up） | 未挿入=LOW / 挿入=HIGH |
| Pin5 | HP_R | R Ring |

---

## RP2040 #2 GPIO割り当て

| GPIO | 役割 |
|------|------|
| GP0 | I2S BCLK |
| GP1 | I2S LRCLK |
| GP2 | I2S SDIN |
| GP3 | SD_MODE制御（MAX98357A × 2 / U8=直結=Left / U15=220kΩ直列=Right） |
| GP4 | XSMT（PCM5102A ミュート制御） |
| GP5 | HP_EN（TPA6132A2 Enable） |
| GP6 | HP_DET（イヤホン挿入検出） |
| GP7〜GP29 | 予備 |

---

## 信号フロー

```
Cubie A7Z USB → VL812 DP4 → RP2040 #2（USB Audio）
RP2040 #2 I2S ─┬─→ MAX98357A × 2 → スピーカー L/R
                └─→ PCM5102A（DAC）→ TPA6132A2 → 3.5mmジャック
GP3: スピーカーON/OFF（SD_MODE）
GP4: DAC ミュート（XSMT）
GP5: HPアンプ Enable
GP6: 挿入検出 → GP3/GP4/GP5をソフト制御
```
