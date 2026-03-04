#!/usr/bin/env python3
"""
PortaRe0 キーボードレイアウト自動配置スクリプト

KiCad Scripting Console で実行:
  exec(open(r'D:\Projects\PortaRe0\kicad\place_keyboard.py').read())
"""

import json
import re
import pcbnew

# ===== 設定 =====
KLE_PATH    = r'D:\Projects\PortaRe0\keyboard\keyboard-layout.json'
PITCH_MM    = 8.5    # キーピッチ (mm)
MARGIN_X_MM = 4.0    # ボード左端からのマージン (mm)
MARGIN_Y_MM = 2.0    # ボード上端からのマージン (mm)
SW_ROTATION = 0      # スイッチ回転角 (度) — 必要なら 90 / 180 / 270 に変更
DIODE_DX    = 3.5    # ダイオードのスイッチ中心からの X オフセット (mm)
DIODE_DY    = 0.0    # ダイオードのスイッチ中心からの Y オフセット (mm)
# ================


def parse_kle(data):
    """KLE JSON をパースしてキー位置リストを返す"""
    keys = []
    y = 0
    for row in data:
        if isinstance(row, dict):
            y += row.get('y', 0)
            continue
        x, w, h = 0.0, 1.0, 1.0
        for item in row:
            if isinstance(item, dict):
                x += item.get('x', 0)
                y += item.get('y', 0)
                if 'w' in item: w = item['w']
                if 'h' in item: h = item['h']
            elif isinstance(item, str):
                keys.append({
                    'label': item if item else 'Enter',
                    'cx': x + w / 2,
                    'cy': y + h / 2,
                })
                x += w
                w, h = 1.0, 1.0
        y += 1
    return keys


def move_fp(fp, x_mm, y_mm, rot_deg=0):
    """フットプリントを指定位置に移動"""
    try:
        fp.SetPosition(pcbnew.VECTOR2I(
            int(pcbnew.FromMM(x_mm)),
            int(pcbnew.FromMM(y_mm))
        ))
    except Exception:
        fp.SetPosition(pcbnew.wxPointMM(x_mm, y_mm))
    try:
        fp.SetOrientationDegrees(rot_deg)
    except Exception:
        fp.SetOrientation(int(rot_deg * 10))


# ---- メイン ----
board = pcbnew.GetBoard()

# ボード左上座標を取得（Edge.Cuts のバウンディングボックス）
bbox = board.GetBoardEdgesBoundingBox()
bx = pcbnew.ToMM(bbox.GetLeft())
by = pcbnew.ToMM(bbox.GetTop())
print(f"ボード左上: ({bx:.2f}, {by:.2f}) mm")

# KLE 読み込み・パース
with open(KLE_PATH, 'r', encoding='utf-8') as f:
    keys = parse_kle(json.load(f))

print(f"KLE から {len(keys)} キーを読み込みました")
for i, k in enumerate(keys):
    print(f"  [{i+1:2d}] {k['label']:10s}  cx={k['cx']:.2f}  cy={k['cy']:.2f}")

# スイッチ (SW*) フットプリント収集
switches = sorted(
    [(int(re.search(r'\d+', fp.GetReference()).group()), fp)
     for fp in board.GetFootprints()
     if re.match(r'^SW\d+$', fp.GetReference())],
    key=lambda t: t[0]
)
print(f"\nSW フットプリント: {len(switches)} 個")

# ダイオード (1N4148W のみ) フットプリント収集
# FAN フライバック用 1N4148W も含まれる可能性があるため末尾1個は除外しない
# → スクリプトは keys の数だけ配置し、余りは放置
diodes = sorted(
    [(int(re.search(r'\d+', fp.GetReference()).group()), fp)
     for fp in board.GetFootprints()
     if re.match(r'^D\d+$', fp.GetReference()) and '1N4148' in fp.GetValue()],
    key=lambda t: t[0]
)
print(f"1N4148W フットプリント: {len(diodes)} 個")

# ---- スイッチ配置 ----
print("\n--- スイッチ配置 ---")
for i, (num, fp) in enumerate(switches):
    if i >= len(keys):
        print(f"SW{num} に対応するキーがありません（スキップ）")
        break
    k = keys[i]
    x = bx + MARGIN_X_MM + k['cx'] * PITCH_MM
    y = by + MARGIN_Y_MM + k['cy'] * PITCH_MM
    move_fp(fp, x, y, SW_ROTATION)
    print(f"  SW{num:2d} [{k['label']:10s}]  ({x:.1f}, {y:.1f}) mm")

# ---- ダイオード配置（キー順に最大 len(keys) 個）----
print("\n--- ダイオード配置 ---")
for i, (num, fp) in enumerate(diodes):
    if i >= len(keys):
        print(f"D{num} 以降はキー数を超えるためスキップ（FAN用等を手動移動してください）")
        break
    k = keys[i]
    x = bx + MARGIN_X_MM + k['cx'] * PITCH_MM + DIODE_DX
    y = by + MARGIN_Y_MM + k['cy'] * PITCH_MM + DIODE_DY
    move_fp(fp, x, y, 0)
    print(f"  D{num:2d}  ({x:.1f}, {y:.1f}) mm")

pcbnew.Refresh()
print("\n完了！PCB ビューを確認してください。")
