# キーマトリクス割り当て

物理配置ベース。PCBレイアウト時にCOL線が縦方向に短くなるよう設計。
9COL × 8ROW = 72セル（使用66、空き6）

## マトリクス表

```
         COL0   COL1   COL2   COL3   COL4   COL5   COL6   COL7   COL8
GP:       GP0    GP1    GP2    GP3    GP4    GP5    GP6    GP7    GP8
         -----  -----  -----  -----  -----  -----  -----  -----  -----
ROW0 GP9: Left   ---    ---    ---    ---    ---    ---    ---   Right
ROW1 GP10: Esc    1      2      3      4      5      6      7      8
ROW2 GP11:  9     0      -      ^      ¥     BS    h/z     Q      W
ROW3 GP12:  E     R      T      Y      U      I      O      P      @
ROW4 GP13:  [   Enter   Tab     A      S      D      F      G      H
ROW5 GP14:  J     K      L      ;      :      ]    Shift    Z      X
ROW6 GP15:  C     V      B      N      M      ,      .      /      ¥2
ROW7 GP16: RSft  Spc   Back   Next   Ctrl    Fn    Alt    ---    ---
```

## キー一覧（ROW, COL順）

| ROW | COL | キー | GP_ROW | GP_COL |
|-----|-----|------|--------|--------|
| 0 | 0 | Left (ショルダー) | GP9 | GP0 |
| 0 | 8 | Right (ショルダー) | GP9 | GP8 |
| 1 | 0 | Esc | GP10 | GP0 |
| 1 | 1 | 1 | GP10 | GP1 |
| 1 | 2 | 2 | GP10 | GP2 |
| 1 | 3 | 3 | GP10 | GP3 |
| 1 | 4 | 4 | GP10 | GP4 |
| 1 | 5 | 5 | GP10 | GP5 |
| 1 | 6 | 6 | GP10 | GP6 |
| 1 | 7 | 7 | GP10 | GP7 |
| 1 | 8 | 8 | GP10 | GP8 |
| 2 | 0 | 9 | GP11 | GP0 |
| 2 | 1 | 0 | GP11 | GP1 |
| 2 | 2 | - | GP11 | GP2 |
| 2 | 3 | ^ | GP11 | GP3 |
| 2 | 4 | ¥ | GP11 | GP4 |
| 2 | 5 | BS | GP11 | GP5 |
| 2 | 6 | h/z | GP11 | GP6 |
| 2 | 7 | Q | GP11 | GP7 |
| 2 | 8 | W | GP11 | GP8 |
| 3 | 0 | E | GP12 | GP0 |
| 3 | 1 | R | GP12 | GP1 |
| 3 | 2 | T | GP12 | GP2 |
| 3 | 3 | Y | GP12 | GP3 |
| 3 | 4 | U | GP12 | GP4 |
| 3 | 5 | I | GP12 | GP5 |
| 3 | 6 | O | GP12 | GP6 |
| 3 | 7 | P | GP12 | GP7 |
| 3 | 8 | @ | GP12 | GP8 |
| 4 | 0 | [ | GP13 | GP0 |
| 4 | 1 | Enter (2u高) | GP13 | GP1 |
| 4 | 2 | Tab | GP13 | GP2 |
| 4 | 3 | A | GP13 | GP3 |
| 4 | 4 | S | GP13 | GP4 |
| 4 | 5 | D | GP13 | GP5 |
| 4 | 6 | F | GP13 | GP6 |
| 4 | 7 | G | GP13 | GP7 |
| 4 | 8 | H | GP13 | GP8 |
| 5 | 0 | J | GP14 | GP0 |
| 5 | 1 | K | GP14 | GP1 |
| 5 | 2 | L | GP14 | GP2 |
| 5 | 3 | ; | GP14 | GP3 |
| 5 | 4 | : | GP14 | GP4 |
| 5 | 5 | ] | GP14 | GP5 |
| 5 | 6 | Shift | GP14 | GP6 |
| 5 | 7 | Z | GP14 | GP7 |
| 5 | 8 | X | GP14 | GP8 |
| 6 | 0 | C | GP15 | GP0 |
| 6 | 1 | V | GP15 | GP1 |
| 6 | 2 | B | GP15 | GP2 |
| 6 | 3 | N | GP15 | GP3 |
| 6 | 4 | M | GP15 | GP4 |
| 6 | 5 | , | GP15 | GP5 |
| 6 | 6 | . | GP15 | GP6 |
| 6 | 7 | / | GP15 | GP7 |
| 6 | 8 | ¥2 | GP15 | GP8 |
| 7 | 0 | RShift (2u) | GP16 | GP0 |
| 7 | 1 | Space (4.5u) | GP16 | GP1 |
| 7 | 2 | Back | GP16 | GP2 |
| 7 | 3 | Next | GP16 | GP3 |
| 7 | 4 | Ctrl | GP16 | GP4 |
| 7 | 5 | Fn | GP16 | GP5 |
| 7 | 6 | Alt | GP16 | GP6 |

合計: 66キー（空きセル: ROW0×7 + ROW7×2 = 9セル）

## PCBレイアウト時の配線メモ

- COL線（GP0〜GP8）: 縦方向（上→下）に8キー分つなぐ
- ROW線（GP9〜GP16）: 横方向（左→右）に各行をつなぐ
- ダイオード向き: ROW→SW→[>|]→COL（カソードがCOL側）
- 空きセルはNC（ダイオードもSWも不要）
