# A238 -- the k5 toolkit on the Trump-parent protected classes: geometry against A100's LP

Every row is ONE node of a protected class's tree at s0 with the SAME hypothesis A100 priced: M_S & YES(H),
delta_pin = 2e-2, H the A100/A84 level-1 cover cell (`attempts/A238-k4-benchmark/code/load238.py`).
A238's verdict is the k5 toolkit's (A211 coarse tree, A212 gate + Lemma TUBE-LEAF/S in the class direction,
A224 Rule SNAP with the k+1 hand-off, A230 Rule EPS, A220/A221); A100's is the case-LP's.

## corners4

| set | n | A238 DEAD | TUBE | ALIVE | A238 mean / median s | A100 PASS | A100 mean / median s | speed-up (median) |
|---|---|---|---|---|---|---|---|---|
| A100 head-to-head | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |
| + extrapolation set | 0 | 0 | 0 | 0 | None / None | - | - | - |
| all cover nodes | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |

root (A84-P1 node, H = the whole interior zone): {'verdict': 'ALIVE', 'seconds': 4.9, 'n_nodes': 3, 'gate': False}

kills by rule: `{}`; gate hits 0; TRUMP-TUBE leaves 0; SNAP kills 0, hand-offs 0; max depth {"0": 1}

## k3_02

| set | n | A238 DEAD | TUBE | ALIVE | A238 mean / median s | A100 PASS | A100 mean / median s | speed-up (median) |
|---|---|---|---|---|---|---|---|---|
| A100 head-to-head | 20 | 0 | 0 | 20 | 4.3 / 4.3 | 15 | 388.5 / 496.2 | 115.4x |
| + extrapolation set | 46 | 0 | 0 | 46 | 4.2 / 4.3 | - | - | - |
| all cover nodes | 66 | 0 | 0 | 66 | 4.2 / 4.3 | 15 | 117.7 / 0.0 | - |

root (A84-P1 node, H = the whole interior zone): {'verdict': 'ALIVE', 'seconds': 2.3, 'n_nodes': 1, 'gate': True}

kills by rule: `{}`; gate hits 7; TRUMP-TUBE leaves 0; SNAP kills 0, hand-offs 0; max depth {"0": 67}

### k3_02 — cell by cell (A100's own LP row against A238's geometry)

| cell | A100 verdict | A100 s | A238 verdict | A238 s | killed by | nodes | depth |
|---|---|---|---|---|---|---|---|
| `c0_Y0083` | PASS | 1014 | **ALIVE** | 4.7 | — | 3 | 0 |
| `c0_Y0179` | refused (tau 7.000000 >= budget 7) | 601 | **ALIVE** | 4.5 | — | 3 | 0 |
| `c0_Y0721` | PASS | 53 | **ALIVE** | 4.6 | — | 3 | 0 |
| `c0_Y0729` | PASS | 17 | **ALIVE** | 4.4 | — | 3 | 0 |
| `c0_Y0730` | PASS | 604 | **ALIVE** | 4.4 | — | 3 | 0 |
| `c0_Y0731` | PASS | 606 | **ALIVE** | 4.3 | — | 3 | 0 |
| `c0_Y0732` | PASS | 38 | **ALIVE** | 4.3 | — | 3 | 0 |
| `c0_Y0733` | PASS | 19 | **ALIVE** | 4.3 | — | 3 | 0 |
| `c0_Y0778` | refused (tau 7.000000 >= budget 7) | 77 | **ALIVE** | 4.7 | — | 3 | 0 |
| `c0_Y0779` | refused (tau 7.000000 >= budget 7) | 17 | **ALIVE** | 4.0 | — | 3 | 0 |
| `c0_Y1042` | FAIL(rc=3) | 157 | **ALIVE** | 4.3 | — | 3 | 0 |
| `c0_Y1050` | PASS | 691 | **ALIVE** | 4.4 | — | 3 | 0 |
| `c0_Y1051` | PASS | 604 | **ALIVE** | 4.3 | — | 3 | 0 |
| `c0_Y1111` | PASS | 762 | **ALIVE** | 4.4 | — | 3 | 0 |
| `c0_Y1119` | PASS | 737 | **ALIVE** | 4.0 | — | 3 | 0 |
| `c0_Y1127` | PASS | 85 | **ALIVE** | 4.1 | — | 3 | 0 |
| `c0_Y1135` | FAIL(rc=3) | 88 | **ALIVE** | 4.2 | — | 3 | 0 |
| `c0_Y1139` | PASS | 604 | **ALIVE** | 4.4 | — | 3 | 0 |
| `c0_Y1143` | PASS | 604 | **ALIVE** | 3.9 | — | 3 | 0 |
| `c0_Y1151` | PASS | 391 | **ALIVE** | 4.4 | — | 3 | 0 |

price: 864 cover cells x 4.2 s = **1.0 CPU-h** of geometry; the 100 % geometry leaves over (at A100's 485 s/node LP) 116.4 CPU-h; total **117.4 CPU-h** against A100's measured 290.2 CPU-h (per node 115.43 x cheaper).

## k4_03

| set | n | A238 DEAD | TUBE | ALIVE | A238 mean / median s | A100 PASS | A100 mean / median s | speed-up (median) |
|---|---|---|---|---|---|---|---|---|
| A100 head-to-head | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |
| + extrapolation set | 0 | 0 | 0 | 0 | None / None | - | - | - |
| all cover nodes | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |

root (A84-P1 node, H = the whole interior zone): {'verdict': 'ALIVE', 'seconds': 338.1, 'n_nodes': 38, 'gate': True}

kills by rule: `{"REACH": 1, "NOROOM-CN": 2}`; gate hits 1; TRUMP-TUBE leaves 0; SNAP kills 0, hand-offs 0; max depth {"10": 1}

## k4_05

| set | n | A238 DEAD | TUBE | ALIVE | A238 mean / median s | A100 PASS | A100 mean / median s | speed-up (median) |
|---|---|---|---|---|---|---|---|---|
| A100 head-to-head | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |
| + extrapolation set | 0 | 0 | 0 | 0 | None / None | - | - | - |
| all cover nodes | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |

root (A84-P1 node, H = the whole interior zone): {'verdict': 'ALIVE', 'seconds': 340.3, 'n_nodes': 44, 'gate': False}

kills by rule: `{"REACH": 4, "FC+EPS": 2, "NOROOM-CN": 2, "NOROOM": 1}`; gate hits 0; TRUMP-TUBE leaves 0; SNAP kills 0, hand-offs 0; max depth {"6": 1}

## k4_06

| set | n | A238 DEAD | TUBE | ALIVE | A238 mean / median s | A100 PASS | A100 mean / median s | speed-up (median) |
|---|---|---|---|---|---|---|---|---|
| A100 head-to-head | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |
| + extrapolation set | 0 | 0 | 0 | 0 | None / None | - | - | - |
| all cover nodes | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |

root (A84-P1 node, H = the whole interior zone): {'verdict': 'ALIVE', 'seconds': 325.5, 'n_nodes': 66, 'gate': True}

kills by rule: `{"EmptyBox": 3, "REACH": 6}`; gate hits 1; TRUMP-TUBE leaves 0; SNAP kills 0, hand-offs 0; max depth {"6": 1}

## k4_08

| set | n | A238 DEAD | TUBE | ALIVE | A238 mean / median s | A100 PASS | A100 mean / median s | speed-up (median) |
|---|---|---|---|---|---|---|---|---|
| A100 head-to-head | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |
| + extrapolation set | 0 | 0 | 0 | 0 | None / None | - | - | - |
| all cover nodes | 0 | 0 | 0 | 0 | None / None | 0 | None / None | - |

root (A84-P1 node, H = the whole interior zone): {'verdict': 'ALIVE', 'seconds': 333.5, 'n_nodes': 31, 'gate': True}

kills by rule: `{"EmptyBox": 10, "S-CLIP": 2, "NOROOM-CN": 2, "NOROOM-POCKET": 1}`; gate hits 2; TRUMP-TUBE leaves 0; SNAP kills 0, hand-offs 0; max depth {"7": 1}

## k4_11

| set | n | A238 DEAD | TUBE | ALIVE | A238 mean / median s | A100 PASS | A100 mean / median s | speed-up (median) |
|---|---|---|---|---|---|---|---|---|
| A100 head-to-head | 39 | 17 | 0 | 22 | 245.9 / 315.0 | 15 | 337.9 / 219.0 | 0.7x |
| + extrapolation set | 43 | 15 | 0 | 28 | 260.8 / 318.6 | - | - | - |
| all cover nodes | 82 | 32 | 0 | 50 | 253.7 / 317.4 | 15 | 160.7 / 0.0 | - |

root (A84-P1 node, H = the whole interior zone): {'verdict': 'ALIVE', 'seconds': 337.0, 'n_nodes': 50, 'gate': True}

kills by rule: `{"EmptyBox": 1684, "FC": 252, "NOROOM": 212, "FC+EPS": 166, "NOROOM-CN": 229, "NOROOM-POCKET": 69, "REACH": 143, "COUNT": 37, "S-CLIP": 53, "MISS-CLIP": 1}`; gate hits 11; TRUMP-TUBE leaves 0; SNAP kills 0, hand-offs 0; max depth {"0": 7, "12": 2, "3": 5, "7": 6, "9": 1, "5": 19, "11": 2, "6": 19, "4": 15, "2": 4, "8": 1, "13": 1, "1": 1}

### k4_11 — cell by cell (A100's own LP row against A238's geometry)

| cell | A100 verdict | A100 s | A238 verdict | A238 s | killed by | nodes | depth |
|---|---|---|---|---|---|---|---|
| `c0_Y0074` | FAIL(rc=3) | 184 | **DEAD** | 16.3 | EmptyBox x1 | 1 | 0 |
| `c0_Y0075` | FAIL(rc=3) | 122 | **DEAD** | 14.2 | EmptyBox x1 | 1 | 0 |
| `c0_Y0076` | refused (tau 6.000000 >= budget 6) | 131 | **DEAD** | 13.1 | EmptyBox x1 | 1 | 0 |
| `c0_Y0401` | FAIL(rc=3) | 560 | **ALIVE** | 320.2 | COUNT x1, EmptyBox x31, FC x8, NOROOM x4, REACH x2 | 71 | 9 |
| `c0_Y0402` | refused (tau 6.000000 >= budget 6) | 185 | **ALIVE** | 316.7 | EmptyBox x35, FC+EPS x4, NOROOM x8, REACH x1, S-CLIP x1 | 78 | 5 |
| `c0_Y0403` | refused (tau 6.000000 >= budget 6) | 314 | **ALIVE** | 322.8 | EmptyBox x35, FC x2, FC+EPS x4, NOROOM x4, REACH x1, S-CLIP x1 | 78 | 7 |
| `c0_Y0404` | refused (tau 6.000000 >= budget 6) | 164 | **DEAD** | 214.4 | EmptyBox x12, FC+EPS x2, NOROOM-CN x4, NOROOM-POCKET x4, S-CLIP x1 | 36 | 3 |
| `c0_Y0405` | PASS | 182 | **ALIVE** | 318.1 | EmptyBox x19, FC+EPS x9, NOROOM x5, NOROOM-CN x11, NOROOM-POCKET x1, S-CLIP x2 | 76 | 5 |
| `c0_Y0497` | FAIL(rc=3) | 359 | **ALIVE** | 315.0 | EmptyBox x38, FC x6, FC+EPS x6, NOROOM x4, REACH x1 | 98 | 5 |
| `c0_Y0498` | FAIL(rc=3) | 214 | **ALIVE** | 318.1 | COUNT x3, EmptyBox x22, FC+EPS x2, NOROOM-CN x1, NOROOM-POCKET x1, S-CLIP x1 | 49 | 7 |
| `c0_Y0499` | PASS | 195 | **DEAD** | 272.7 | EmptyBox x11, FC+EPS x2, NOROOM x1, NOROOM-CN x5, NOROOM-POCKET x2, S-CLIP x2 | 37 | 4 |
| `c0_Y0500` | PASS | 237 | **DEAD** | 223.0 | COUNT x1, EmptyBox x11, FC+EPS x2, NOROOM x1, NOROOM-CN x3, NOROOM-POCKET x4, S-CLIP x1 | 36 | 3 |
| `c0_Y0501` | FAIL(rc=3) | 112 | **DEAD** | 251.7 | EmptyBox x18, FC x6, FC+EPS x2, NOROOM x1, NOROOM-CN x4, NOROOM-POCKET x3, S-CLIP x2 | 54 | 4 |
| `c0_Y0770` | PASS | 865 | **ALIVE** | 326.5 | EmptyBox x13, FC x7, FC+EPS x7, NOROOM x4, NOROOM-CN x2, REACH x2 | 60 | 5 |
| `c0_Y0771` | PASS | 112 | **DEAD** | 40.9 | EmptyBox x24 | 30 | 2 |
| `c0_Y0778` | FAIL(rc=3) | 102 | **ALIVE** | 331.2 | EmptyBox x37, FC+EPS x3, NOROOM x8, NOROOM-POCKET x3, REACH x2, S-CLIP x1 | 83 | 11 |
| `c0_Y0779` | refused (tau 6.000000 >= budget 6) | 97 | **ALIVE** | 323.6 | EmptyBox x44, FC x1, FC+EPS x3, REACH x2, S-CLIP x3 | 82 | 8 |
| `c0_Y0786` | FAIL(rc=3) | 670 | **ALIVE** | 323.5 | EmptyBox x36, NOROOM x8, NOROOM-POCKET x3, REACH x5, S-CLIP x1 | 80 | 13 |
| `c0_Y0787` | refused (tau 6.000000 >= budget 6) | 312 | **ALIVE** | 323.6 | EmptyBox x50, FC x2, NOROOM x13, NOROOM-POCKET x7, REACH x4, S-CLIP x3 | 93 | 4 |
| `c0_Y0850` | FAIL(rc=3) | 112 | **ALIVE** | 333.6 | EmptyBox x7, FC x2, FC+EPS x2, NOROOM x1, NOROOM-CN x11, NOROOM-POCKET x1, REACH x2, S-CLIP x1 | 48 | 6 |
| `c0_Y0851` | refused (tau 6.000000 >= budget 6) | 553 | **ALIVE** | 336.8 | EmptyBox x22, FC x4, NOROOM x1, NOROOM-CN x19, NOROOM-POCKET x3, REACH x2, S-CLIP x1 | 75 | 4 |
| `c0_Y0858` | FAIL(rc=3) | 786 | **ALIVE** | 326.4 | EmptyBox x47, FC+EPS x2, NOROOM x1, NOROOM-CN x6, REACH x2, S-CLIP x1 | 81 | 6 |
| `c0_Y0859` | refused (tau 6.000000 >= budget 6) | 601 | **ALIVE** | 328.1 | EmptyBox x25, FC x4, FC+EPS x2, NOROOM x4, NOROOM-CN x6, NOROOM-POCKET x1, REACH x2, S-CLIP x1 | 68 | 6 |
| `c0_Y0970` | refused (tau 6.000000 >= budget 6) | 690 | **ALIVE** | 318.5 | EmptyBox x34, FC x6, FC+EPS x3, NOROOM x8, NOROOM-POCKET x1, REACH x6, S-CLIP x3 | 93 | 6 |
| `c0_Y0971` | refused (tau 6.000000 >= budget 6) | 663 | **ALIVE** | 313.9 | EmptyBox x38, FC x2, FC+EPS x3, NOROOM x9, NOROOM-POCKET x3, REACH x3, S-CLIP x1 | 86 | 6 |
| `c0_Y1007` | PASS | 257 | **DEAD** | 80.7 | EmptyBox x3, FC x1, FC+EPS x2, NOROOM-CN x1 | 13 | 3 |
| `c0_Y1015` | PASS | 87 | **DEAD** | 51.2 | FC x1, NOROOM-CN x2 | 6 | 1 |
| `c0_Y1023` | PASS | 192 | **DEAD** | 63.0 | EmptyBox x1, FC+EPS x2, NOROOM-CN x2 | 10 | 2 |
| `c0_Y1031` | PASS | 643 | **DEAD** | 101.2 | EmptyBox x9, NOROOM x1, NOROOM-CN x4, NOROOM-POCKET x2 | 23 | 2 |
| `c0_Y1039` | FAIL(rc=3) | 192 | **ALIVE** | 327.1 | EmptyBox x36, FC x4, FC+EPS x4, NOROOM x1, NOROOM-CN x8 | 79 | 4 |
| `c0_Y1042` | FAIL(rc=3) | 643 | **ALIVE** | 504.1 | EmptyBox x13, FC+EPS x13, NOROOM-CN x7, NOROOM-POCKET x2, REACH x2 | 73 | 6 |
| `c0_Y1043` | refused (tau 6.000000 >= budget 6) | 603 | **ALIVE** | 313.1 | EmptyBox x14, FC x2, FC+EPS x10, NOROOM-CN x9, NOROOM-POCKET x1, REACH x3 | 65 | 5 |
| `c0_Y1079` | refused (tau 6.000000 >= budget 6) | 638 | **ALIVE** | 408.7 | EmptyBox x19, FC x9, NOROOM x1, NOROOM-CN x7, REACH x2 | 59 | 6 |
| `c0_Y1087` | PASS | 160 | **ALIVE** | 316.2 | COUNT x1, EmptyBox x20, FC x3, FC+EPS x4, NOROOM x4, NOROOM-CN x3, S-CLIP x1 | 61 | 5 |
| `c0_Y1095` | PASS | 545 | **DEAD** | 255.7 | EmptyBox x4, FC x1, FC+EPS x2 | 18 | 5 |
| `c0_Y1103` | PASS | 219 | **DEAD** | 184.4 | COUNT x1, EmptyBox x3, FC+EPS x3, REACH x1 | 18 | 5 |
| `c0_Y1111` | PASS | 138 | **DEAD** | 62.2 | FC x1, FC+EPS x2, NOROOM-CN x2 | 10 | 2 |
| `c0_Y1119` | PASS | 95 | **DEAD** | 92.7 | EmptyBox x4, FC x2, FC+EPS x3, NOROOM x2, NOROOM-CN x2, NOROOM-POCKET x1 | 23 | 5 |
| `c0_Y1127` | PASS | 246 | **DEAD** | 287.1 | EmptyBox x48, FC x7, FC+EPS x5, NOROOM-CN x11 | 108 | 4 |

price: 923 cover cells x 253.7 s = **65.0 CPU-h** of geometry; the 61 % geometry leaves over (at A100's 559 s/node LP) 87.4 CPU-h; total **152.4 CPU-h** against A100's measured 203.1 CPU-h (per node 2.2 x cheaper).

## Tier extrapolation

The measured per-class numbers are the two pilots; the extrapolation carries them by the ONE number that
predicts traction -- the class's USABLE forced cells (`results/forced238.md`), i.e. how many of its one-slot
extensions are closed on the window.

| block | classes | usable forced cells | geometry CPU-h | LP residue CPU-h | total (A238) | A100's price |
|---|---|---|---|---|---|---|
| k4 with traction (k4_03, k4_05, k4_06, k4_08, k4_11) | 5 | k4_03 3/5, k4_05 3/5, k4_06 3/5, k4_08 5/7, k4_11 5/7 | 325 | 437 | **762** | 203.1 each |
| k <= 3 (k3_01, k3_02, k3_03, k3_04, k3_05, k2_*, k1_00) | 9 | 0 for every one | 9 | 1048 | **1057** | 290.2 each |
| corners4 (shadow, no image) | 1 | 0/8 -- every extension is the OPEN k5_16 | 0 | not priced | - | not priced |

`corners4` is not run: with no usable forced cell the toolkit's rules have nothing to act on (A193 and
A84 s.7.1 independently), so a run would cost the stage-0 seconds and decide nothing -- exactly what the
k3_02 rows above measure.  For the same reason the k <= 3 row is NOT a saving: the geometry is cheap there
because it is blind, and the LP residue is A100's whole price.

**The lever the numbers point at**: five of the nine blocked k <= 3 extensions are k4 classes A55 already
killed exactly (k4_00 / 01 / 02 / 04 / 07 / 09 / 10 / 12) that simply have no full-window scoreboard row.
Emitting those rows would give each k3 class 2-5 usable forced cells and move it into the k4 row of this
table.

