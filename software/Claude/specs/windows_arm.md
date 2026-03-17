# Windows ARM on Cubie A7Z（Allwinner A733）

> 調査日: 2026-03-17（session01）
> ステータス: Linux公式イメージ動作確認済み / 環境整備待ち

---

## 目標

Cubie A7Z（Allwinner A733）上で Windows ARM を起動させる。
ロマン枠・時間無制限。実用性より「動いた」がゴール。

---

## SoC スペック（Allwinner A733）

| 項目 | 詳細 |
|------|------|
| CPU | Cortex-A76 × 2 + Cortex-A55 × 6（big.LITTLE、最大2.0GHz）|
| GPU | Imagination BXM-4-64 |
| NPU | 3 TOPS |
| プロセス | 12nm |
| メモリ | LPDDR4/4X/5、最大16GiB |
| ストレージ | UFS 3.0、eMMC 5.1 |
| 発売 | 2024年 |

---

## 利用可能なリソース

| リソース | URL | 備考 |
|---------|-----|------|
| Radxa 公式ドキュメント | https://docs.radxa.com/en/cubie/a7z | |
| Radxa BSP カーネル（Linux 5.15） | https://github.com/radxa/kernel `allwinner-aiot-linux-5.15` | |
| Radxa U-Boot | https://github.com/radxa/u-boot `cubie-aiot-v1.4.6` | |
| Allwinner 公式 SDK（Tina5.0） | https://gitlab.com/tina5.0_aiot | NDA不要・A733データシート含む |
| U-Boot mainline パッチ（v2） | https://lists.denx.de/pipermail/u-boot/2025-November/603430.html | [PATCH 00/11] 未マージ |
| Armbian 対応議論 | https://forum.armbian.com/topic/56130-radxa-cubie-a7aa7z-allwinner-a733/ | |
| Arch Linux ARM for A733 | https://github.com/hqu-little-boy/archlinuxarm-a733 | A7A向けだがA7Zも近い |
| radxa-build（ビルドシステム） | https://github.com/radxa-build/radxa-a733 | |
| linux-sunxi.org A733 | https://linux-sunxi.org/A733 | |

---

## ブートロードマップ

```
現在のブートチェーン（BSP）:
  SPL → [TF-A BL31？] → U-Boot → Linux

目標のブートチェーン:
  SPL → TF-A BL31 → EDK2（UEFI） → Windows ARM
```

---

## 作業ステップ

### Step 1: Linux 起動確認 ✅
- Radxa 公式 Debian イメージで動作確認済み

### Step 2: 現在のブートチェーン確認 ⏳
TF-A BL31 がすでに使われているか確認する。

```bash
# U-Boot起動ログを確認（BL31の文字があればTF-A使用中）
# または
cat /sys/firmware/devicetree/base/firmware/arm-trusted-firmware/compatible 2>/dev/null
strings /dev/mmcblk0 | grep -i "bl31\|trusted" | head -20
```

- **BL31あり** → Step 4（EDK2移植）へ直接進める
- **BL31なし** → Step 3（TF-A移植）が必要

### Step 3: TF-A BL31 を A733 に移植
- 参考: TF-A mainline の H616/A100 実装（`plat/allwinner/`）
- Allwinner SDK（Tina5.0）のデータシートでレジスタマップを確認
- EL3セキュアモニタが動けばOK

### Step 4: EDK2 を A733 向けに移植
- 参考1: RPi4 向け EDK2（https://github.com/pftf/RPi4）
- 参考2: 2017年の A64 向け断片実装（https://github.com/awwiniot/UEFI-aw1689）
- UEFI Shell 起動が最初のマイルストーン

### Step 5: Windows ARM インストール
- WoA Installer（https://worproject.com/）または DISM で展開
- この時点では「起動する」だけが目標

### Step 6: ドライバ対応（長期）
- USB / eMMC → 起動に必須
- GPU（Imagination BXM）→ Windows ドライバ要確認、長期戦

---

## 注意事項

- **GPU ドライバ**: Imagination BXM-4-64 の Windows ドライバが存在しない可能性が高い。「起動する」と「実用的に動く」は別問題。
- **Allwinner SDK は主に中国語ドキュメント**
- BSP U-Boot は 2018.07 ベースと古い。mainline U-Boot パッチ（v2）のマージを待つか自力適用を検討。
