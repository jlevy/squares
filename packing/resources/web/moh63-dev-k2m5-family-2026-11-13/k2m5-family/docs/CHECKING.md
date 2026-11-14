# What is checked, how, and by what (final cover k05-5)

Board: `certificate/sol_exact_box11.txt`, sha256 `d259fed5c9d5eb02c6fed85f5d1070e86d48f5717305f9e056c9a88adbd12099`;
13,244 segments + Lebesgue on [19/5, 36/5]²; D = 1340566927759/10¹² ≈ 1.3405669; total 121 − 4D.

| # | claim | check | kind | result |
|---|---|---|---|---|
| 1 | total of μ_k is k² − 4D, D > 5/4 | `sanity_k2m5.py` (ours); boards k = 10, 11, 12, 13, 20 built and summed (`qx2_exact.py cover`) | exact | OK, all equal k² − 4D |
| 2 | the board file is μ₁₁ of the family | `lean/K2m5/scripts/gen_fam10_data.py` (Python mirror) and the Lean kernel (`box11Cover_measure`) | exact / kernel | OK |
| 3 | μ_k is D4-invariant | `sanity_k2m5.py` (k = 11); `zmx2 d4` (k = 10, 12, 13, 20) | exact | OK |
| 4 | locality: k ≥ 10 reduces to k = 11 | paper Lemma 7 (proof by hand); Lean `k2m5_of_valid11`; `locality_check.py` (ours) on k = 10, 12, 13, 20, which also catches a one-weight mutation of μ₁₂ (176 bad windows) | proof / kernel / exact | OK |
| 5 | untilted squares (θ = 0) | Lemma Z at 10,000 limit corners (exact, min exactly 1); our axis check at 7,717 corners (exact, min exactly 1); `zmx2 cert0` on 2,500 roots | exact / interval | OK |
| 6 | tilted squares, general position | `zmx2 cert --d4 --first-order --depth 40 --node-cap 2e7`, 55 columns, 12,100 roots; `audit_zmx2.py` | interval (outward-rounded binary64, exact integer masses) | 12,024 roots certified; 76 left |
| 7 | root 9632 | its 6,850 zmx2-uncertified boxes lie in one `qx2_zm.py` root (depth 18), which leaves 83 boxes, none meeting them; `check_9632.py` | exact | closed |
| 8 | the 75 tight-tile roots | Tight-Tile Lemma (`tight_tile/`): 308 jobs at u₀ = 1/4000 + 15 at 1/2000, every chart and corner zone certified; `cov_check.py`: all 1,255,023 zmx2 leftover boxes inside the certified region | exact + outward-rounded intervals | COVERAGE-OK |
| 9 | float stress test | `stress_family.py` (ours): 270,000 random, near-tile and near-45° poses | float, not part of the proof | min 1 − 9·10⁻¹⁵ (rounding, in the Lebesgue middle) |

## Controls (the checkers refuse what they must)

| checker | real cover | modified cover | result |
|---|---|---|---|
| `zmx2`, root (15, 36), depth 24 | 0 uncertified | every segment weight × 0.999 / × 0.993 | 209 / 217 uncertified: refused |
| `qx2_zm.py`, root-9632 window | 83 uncertified, none meeting zmx2's leftovers (closed) | every segment weight × 0.999 | 87 uncertified, 3 of them meeting zmx2's leftovers: `check_9632.py` says NOT-CLOSED (refused) |
| Tight-Tile checker | certified | weights × 0.99; line x = 2 −1%; one segment moved (same limit values, smaller first-order growth: a true violation, mass 1 − 1.34·10⁻⁷) | refused (1,190 refused cells in the last) |
| `locality_check.py` | OK | one weight of μ₁₂ changed | 176 windows fail: refused |

## Independent review

A separate agent reviewed the Tight-Tile proof and code adversarially (exact re-evaluation of μ − 1 at every
vertex of every certified cell in sample regions, 44,000 interval tests, exact sampling of the covering lemmas).
No mathematical flaw; two bookkeeping gaps in the coverage step were fixed and the affected job re-run.

## Notes

- `zmx2` is interval-certified (outward-rounded binary64 geometry, exact integer masses), not exact-rational.
- `qx2_zm.py` prints `zeromargin.py … DIFFERS FROM PINNED`; our `zeromargin.py` is Daniel's at the pin.
- `--cert-mode` of `zm_mixed.py` does not apply: the cover contains a Lebesgue polygon, which cert mode refuses;
  `qx2_zm.py` runs without it, as for Daniel's own k² − 3 and k² − 4 families.
- The `zmx2` coverage dumps used the one-line `ZMX2_PRINT_ALL` patch (output only); the numbers of uncertified
  boxes listed and reported agree (1,255,023), the dumps' cover hash (`a53f06f25d54b3df`, zmx2's FNV-1a hash of the board file) and settings line
(`mode=d4 atoms=grid+fo depth=40 node_cap=20000000`) equal the main sweep's (`audit_zmx2.py` checks both).
