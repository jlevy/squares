# Search log

Model: `qx2_lp.py lp --R 4 --w 4 --hc 0.1 --hp 0.1 --hca 0 --hpa 0 --no-points --kappa 0.02 --th0 3 --germs`
(lines only, element pitch 0.1, tilt margin κ = 0.02 up to 3°, exact germ-limit rows). LP runs on an Apple M1 Pro.
From iteration k05-1 on: `--kappa 0.05 --th0 1` (larger tilt margin, so fewer roots are left for the exact checker).

Loop: LP (40 rounds) → exact projection (`qx2_exact.py projectf`) → exact checks (axis, mass, D4) → 11 × 11 cover →
`zmx2` oracle sweep (`--first-order --depth 24 --node-cap 2e6`, 55 columns) → uncertified poses become LP rows.

## Exact projections

| it | after LP round | exact D | tight rows | 11 × 11 total | cover sha256 (first 16) |
|---|---|---|---|---|---|
| 0 | 80 | 1.346452057 | 37,704 | 115.6142 | cbbe217ad65cc8ce |
| 1 | 120 | 1.346305638 | 37,695 | 115.6148 | 643a5ce78d51ed03 |
| 2 | 160 (+ sweep-1 rows) | 1.344837437 | 37,643 | 115.6207 | 1d54d3e005dfd467 |
| 3 | 200 (+ sweep-2 rows, denser oracle) | 1.342065170 | 37,564 | 115.6317 | 224430fb71c3a184 |
| 4 | 240 (+ sweep-3 rows) | 1.341657919 | 38,409 | 115.6334 | cd907089c367e8e3 |
| k05-1 | 40 at κ = 0.05 (warm from it 4) | 1.340785046 | 37,487 | 115.6369 | e81dbcdf195b60fb |
| k05-2 | 80 at κ = 0.05 (+ 304 zmx2 rows from k05-1) | 1.340578196 | 37,461 | 115.6377 | 06645e690fc14fc8 |
| k05-4 | warm from k05-2, + rows around the k05-2 violation (`k05it3/viol_rows`) | 1.340567374 | 37,451 | 115.6377 | 94c97a4a4207c05d |
| **k05-5** | warm from k05-4, + rows from its zmx2 refusals (`k05it5/viol_rows`) | **1.340566928** | 37,451 | 115.6377 | **d259fed5c9d5eb02** |

(k05-3 was an attempt with a second, steeper tilt margin; it was dropped.) Every projection: all tight rows exactly satisfied, σ = 0, no negative weights, axis face min exactly 1, D4-invariant.
Needed: D > 1.25.

## Oracle sweeps (zmx2, capped depth)

| sweep | cover | float-min < 1 (real weak spots) | worst | uncertified at depth 24 | rows added |
|---|---|---|---|---|---|
| 1 | it 1 | 123 | 0.99924 | 128,296 | 23,632 |
| 2 | it 2 | 58 | 0.99946 | 117,757 | 22,413 |
| 3 | it 3 | 7 | 0.99985 | 98,963 | 19,238 |
| 4 | it 4 | (uncapped) | | 97 roots left at depth 40 | |
| k05-1 | k05-1 | (uncapped, depth 40, node cap 2e7) | | 84 roots left | 304 |
| k05-2 | k05-2 | (uncapped, depth 40, node cap 2e7) | | **78 roots left**, all at u ∈ [0, 1/8] | final candidate |

Untilted squares and tilts below 0.05° had no weak spots in any sweep.

## Notes

- Daniel (K2M4_MARGIN.md, Oct 1) found w = 4 capped near 1.25 at element pitch 0.2 ("no-go"), and a conditional go at
  R = w = 5 (D ≈ 1.30). Pitch 0.1 is what lifts w = 4 to about 1.34.
- `qx2_exact.py projectf` (ours) replaces `project` for large tight sets: it removes duplicate rows, picks
  independent rows and pivot columns by QR, solves exactly with FLINT, then checks every tight row exactly.

## Final measure (k05-5)

- 11 × 11 board: 13,244 segments + Lebesgue square [19/5, 36/5]², masses w/(2·10¹²), sha256 `d259fed5…12099`.
- Exact: D = 1340566927759/10¹²; all 37,451 tight rows satisfied exactly; no negative weights; axis face min exactly
  1 (7,717 corners); Lemma Z min exactly 1 (10,000 corners); D4-invariant; total = 121 − 4D.
- zmx2 (first-order, depth 40, node cap 2·10⁷): 12,024 of 12,100 D4 roots certified; the 76 left are the 75
  tight-tile roots and root 9632. How they are closed: `docs/CHECKING.md` and the paper.
- k05-2, an earlier candidate, was not valid: zmx2 found a pose of exact mass 0.99998777 (θ ≈ 0.89°) in root 7536.
