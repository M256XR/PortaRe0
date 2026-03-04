# 電源・USBハブ 詳細仕様

---

## 電源系

| 部品 | 型番 | C番号 | 役割 |
|------|------|--------|------|
| 充電IC | BQ25895RTWR | C80200 | USB PD充電 / バッテリー保護内蔵 |
| 昇圧DC-DC #1 | TPS61023DRLR | C919459 | LiPo → 5V_SYS（システム用） |
| 昇圧DC-DC #2 | TPS61023DRLR | C919459 | LiPo → USB_5V_SYS（外部USBポートVBUS専用） |
| LDO | AP2112K-3.3TRG1 | C51118 | 5V → 3.3V（RP2040用） |
| バッテリー | LiPo 606090 | — | 4200mAh / 3.7V |

### 電源フロー

```
USB-C (充電) → BQ25895 → LiPo 4.2V
LiPo SYS出力 → TPS61023 #1 → 5V_SYS → Cubie A7Z / VL812 / HDMIコントローラ基板
LiPo SYS出力 → TPS61023 #2 → USB_5V_SYS → 外部USBポートVBUS（RP2040 #1 GP24でEN制御）
5V_SYS → AP2112K → 3.3V（RP2040用）
5V_SYS → RT9080 → 3V3_M2（M.2 SSD用）
```

> 注意: BQ25895 SYSラインは最大5〜6A → PCBパターン極太必須

### 電源スイッチ

- 起動：モーメンタリボタン（SKSCLBE010 C115361）→ TPS61023 EN ピン High
- 通常OFF：SBC GPIO → EN Low（shutdown フック）
- 緊急キル：MSK12C02（C431540）スライドSW → EN 強制 Low

---

## USBハブ（VL812）

- **VL812-Q7**（QFN-76-EP 9x9）C69417
- 外付け：W25Q32JVSSIQ SPI Flash（C82344）/ 25MHz水晶 X322525MOB4SI（C9006）/ SSREXT 6.04kΩ

### USB接続構成

```
Cubie A7Z USB-C (USB3.0) → VL812 upstream
VL812 downstream 1 → 外部USB-C レセプタクル（TPS2042BDR / USBLC6-2SC6）
VL812 downstream 2 → 外部USB-A レセプタクル（TPS2042BDR / USBLC6-2SC6）
VL812 downstream 3 → RP2040 #1（キーボード）
VL812 downstream 4 → RP2040 #2（オーディオ）
Cubie A7Z USB-C (USB2.0) → BQ25895（充電入力 / 刻印:PWR）
Cubie A7Z Micro HDMI → HDMIコントローラ基板
```

### 外部USBポート電源構成

- TPS2042BDR（C138720）: VL812 /USBHPE制御 / /USBHOC過電流検知
- USBLC6-2SC6（C7519）: Port1/2各1個 ESD保護
- 外部VBUS専用 TPS61023 #2（USB_5V_SYS）: RP2040 #1 GP24で制御
- 注意: 外部USBポートはデータ転送・小型デバイス用（HDD等大電流機器は非推奨）
