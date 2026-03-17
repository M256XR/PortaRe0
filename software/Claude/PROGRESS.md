# PortaRe0 ソフトウェア開発 進捗ログ

## 現在のフェーズ
**Phase 3: PCBレイアウト完了待ち → ソフトウェア開発 準備中**

## 現在の作業箇所
- **筐体・PCB完成待ちのため QMK/TinyUSB は保留**
- **EDK2 移植（Windows ARM）を優先的に進行中**
- **次のタスク**: Cubie A7Z の GIC/TF-A 情報収集 → TF-A BL31 A733 ポート開始
- 参照: `specs/windows_arm.md`（ロードマップ・参考リポジトリ一覧）

---

## フェーズ完了状況

### RP2040 キーボードファームウェア ⏳ 未着手
- [ ] フレームワーク選定（QMK / KMK / Pico SDK）
- [ ] キーマトリクス 63キー定義
- [ ] スライドパッド（GP27/GP28）統合
- [ ] USB HID デバイス認識確認
- [ ] LED（CHG/FULL/ACT）制御

### オーディオ ⏳ 未着手
- [ ] MAX98357A I2S スピーカー動作確認
- [ ] PCM5102A DAC + TPA6132A2 ヘッドフォン動作確認
- [ ] ALSA / PipeWire 設定

### Linux システム設定 ⏳ 未着手
- [x] Cubie A7Z 初期セットアップ（公式Debianイメージ動作確認済み）
- [ ] ディスプレイ（LS055R1SX04）設定
- [ ] USB HUB（VL812）動作確認
- [ ] M.2 SSD 認識確認

### Windows ARM（ロマン枠） ⏳ 調査完了・環境整備待ち
- [x] リソース調査（specs/windows_arm.md に記録）
- [ ] 現在のブートチェーン確認（TF-A BL31使用有無）
- [ ] TF-A BL31 移植（必要な場合）
- [ ] EDK2 移植
- [ ] Windows ARM 起動

---

## 未解決の TBD 事項

| 項目 | 解決タイミング |
|------|--------------|
| ~~RP2040 ファームウェアフレームワーク~~ | ✅ session01で確定 |
| Linux OS ディストリビューション | Cubie A7Z 実機届いたら確認 |
| キーレイアウト（QMKレイヤー構成） | QMK開発開始時 |

---

## 直近の決定事項ログ

### 2026-03-17〜18（session01）
- フレームワーク確定: RP2040 #1 → **QMK**、RP2040 #2 → **Pico SDK + TinyUSB（UAC2）**
- 開発計画: `specs/dev_plan.md` に詳細まとめ
- **方針転換**: 筐体未完成のため QMK/TinyUSB は保留 → EDK2 移植を優先
- Cubie A7Z システム調査: ブートチェーン = SPL→U-Boot（UEFI無効）→extlinux→Linux
- U-Boot ビルド日: 2024-03-20 / カーネル: 5.15.147-7-a733 / RAM: 1GB
- アイドル消費電力: 3〜5W（ヒートシンクのみで触れないレベルに熱くなる）
- Windows ARM 調査完了: `specs/windows_arm.md` に知見・リソース・ロードマップ・EDK2構成を記録
- EDK2参考実装確認済み: RPi4 EDK2 / awwiniot/UEFI-aw1689（AXP PMICドライバ流用可）
- U-Boot A733 mainlineパッチ: v3投稿済み・未マージ（v2026.07以降見込み）→ 待たずにBSPで進める
- **次のアクション**: Cubie A7Z でGIC/TF-A情報収集（調査5.txt 未取得）→ TF-A BL31 ポート開始

### 2026-03-16（session00）
- software/ フォルダ・Claude サブディレクトリ構成を作成
- ハードウェア側 Claude/ と同様の管理体制をソフトウェア開発用に整備
