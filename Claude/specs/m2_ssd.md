# M.2 SSD 詳細仕様

---

## 構成

- **M.2ソケット**: NASM0-S6701-TP40（C367029）M-key / 2230対応
- **PCIeインターフェース**: Cubie A7Z F0506-16-BGR（16pin 0.5mm FPC / RPi5互換）→ PCIe Gen3 x1
- **FPCコネクタ**: FPC-05F-16PH20（C2856801）16pin 0.5mm ZIF
- **電源**: RT9080-33GJ5（C841192）600mA LDO / 5V_SYS → 3V3_M2（AP2112K とは別レール）

---

## FPC → M.2 ピン接続

| FPC Pin | 信号 | 接続 | M.2 Pin |
|---------|------|------|---------|
| Pin2 | PCIE_TX_P | → 100nF → | Pin43 (PERp0) |
| Pin3 | PCIE_TX_N | → 100nF → | Pin41 (PERn0) |
| Pin5 | PCIE_RX_P | 直結 | Pin49 (PETp0) |
| Pin6 | PCIE_RX_N | 直結 | Pin47 (PETn0) |
| Pin8 | PCIE_REFCLK_P | 直結 | Pin55 (REFCLKP) |
| Pin9 | PCIE_REFCLK_N | 直結 | Pin53 (REFCLKN) |
| Pin11 | PCIE_PERST_N | 直結 | Pin50 (PERST#) |
| Pin12 | PCIE_CLKREQ_N | + 10kΩ → 3V3_M2 | Pin52 (CLKREQ#) |
| Pin13 | PCIE_WAKE_N | + 10kΩ → 3V3_M2 | Pin54 (PEWAKE#) |

- 3V3_M2 → M.2 Pin: 2, 4, 12, 14, 16, 18, 70, 72, 74
- M.2 Pin 42/44/46/48/56 = NC（SATAピン / PCIe x1では未使用）
