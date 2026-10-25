# Upper bounds on c\*(k), in Lean

`c*(k)` is the largest `c` with `s(k² − c) = k`: the most unit squares you can remove from a `k × k` grid and still
need a square of side `k`.  An upper bound `c*(k) ≤ c − 1` is a packing of `k² − c` unit squares in a square of
side less than `k`.  Every theorem below is of that form, `∃ s < k, Packs (k * k − c) s`, with `Packs` the plain
definition of `lean/Sqpack/Spec.lean` (closed unit squares, any angles, in `[0, s]²`, pairwise disjoint
interiors), and is checked by the Lean kernel with the standard axioms only (propext, Classical.choice,
Quot.sound).  Re-check: `certificates/k2-minus-c/verify.sh` (a few minutes; `--fang` adds Fang's pieces, ~20 min).
Write-up: [`docs/k2c.html`](../../docs/k2c.html).

| bound | for | Lean (`lean/Sqpack/`) | mathematics |
|---|---|---|---|
| `c*(n) ≤ n − 2`, i.e. `s(n² − n + 1) < n` | n ≥ 15 | `FangFinal.theorem1` (opt-in build) | Kevin Fang (jlevy/squares#603, T-163), after Arslanov–Mustafin–Shangitbayev |
| `n² − n + 1 + p + 2q` squares in side `< n` | n ≥ 15, 16p + 21q ≤ n − 15 | `FangFinal.theorem2` (opt-in) | Fang |
| `c*(k) ≤ 8⌈√(k − 4)⌉ − 1` | k ≥ 6 | `RyuBound.packs_sub_8sqrt` | S. Ryu, Theorem 1.4 (jlevy/squares#471, #486) |
| `c*(k) ≤ 4⌈√(2k − 7)⌉ + 5` | k ≥ 7 | `RyuFill.packs_sub_4sqrt2` | this repository (Ryu's L-shape, one axis layer at each band end) |
| **`c*(k) ≤ 4⌈√(2k − 7)⌉ − 1`** | **k ≥ 7** | `RyuLayers.packs_sub_4sqrt2_layers` | this repository (two top layers; `2b` end squares in all) |
| `c*(k) < 4k/b + 4(4.33 v² + 11 v + 30)` | v ≥ 10, v³/2 ≤ b ≤ v³, k ≥ b + 2v² + 10 | `RyuStairBound.packs_stair` | Ryu's staircase ends (his §6, after Bui), our count |
| **`c*(k) < 18.9 k^{2/5} + 35.7 k^{1/5} + 122`** | **k ≥ 3 · 10⁵** | `RyuStairBound.packs_stair_k25` | from `packs_stair` |
| `c*(k) < 20.668 k^{2/5} + 0.623` | k ≥ 8 · 10⁶ | `RyuStairBound.packs_ryu_thm12` | Ryu's Theorem 1.2 (he proves it for k ≥ 1.6 · 10⁷) |

Which is smallest: Fang's Theorem 2 for `15 ≤ k ≤ 39` (ties at 34 and 39; the register's packings are better still at
small `k`); `4⌈√(2k − 7)⌉ − 1` from `k = 40` to about `7.4 · 10⁵` (below Ryu's `8⌈√(k − 4)⌉ − 1` at every `k ≥ 7`); then
`packs_stair_k25` (below Ryu's Theorem 1.2 bound for every `k ≥ 6.7 · 10⁶`).  Ryu's three certificates are better at
their own `k` (`c*(10⁵) ≤ 1583`, `c*(10⁶) ≤ 3972`, `c*(10⁷) ≤ 10039`, against 1791, 5435, 12943 here), and his
`k^{3/8}` tiers (not formalized here) are better for `k ≳ 10¹²`.

| k | Fang | Ryu 8√ | **4⌈√(2k−7)⌉ − 1** | **two-term k^{2/5}** | Ryu Thm 1.2 |
|---|---|---|---|---|---|
| 15 | 13 | 31 | 19 | | |
| 100 | 90 | 79 | 55 | | |
| 10⁴ | 9048 | 799 | 567 | | |
| 10⁵ | 90476 | 2535 | 1791 | | |
| 10⁶ | 904762 | 7999 | 5659 | 5435 | |
| 10⁷ | | 25303 | 17891 | 12943 | 13041 |
| 10⁸ | | 79999 | 56571 | 31497 | 32757 |

(Each entry is the resulting bound on `c*(k)`; Fang's column uses Theorem 2 with the best `p, q`.)

## The constructions

All but Fang's are Ryu's L-shaped packing (his Theorem 1.3): an axis grid of `(k − b)²` squares and two bands of rows
of `b` squares tilted by `θ` just above `2 arctan(1/b)`, so that a row is slightly narrower than `b` and the side is
`k − b + w < k`.  What differs is the four band ends, the triangles below the first row and above the last
(`RyuEnds.band_ends`: Ryu's Lemma 5.1, any packings of the two end regions, with the rows lifted by `y₀`):

* **empty** (Ryu's Theorem 1.4): each end costs about `b`, total `≈ 4b + 4k/b`, best at `b ≈ √k`: `8√k`;
* **axis layers** (`RyuLayers`): about `b/2` axis squares fit under the first row and over the last, so an end costs
  about `b/2` and the total is `≈ 2b + 4k/b`, best at `b ≈ √(2k)`: `4√2 √k ≈ 5.66 √k`.  With `b = ⌈√(2k − 7)⌉`
  and `L − 3` rows per band of length `L`, the ends hold `⌊(b − 1)/2⌋` (twice), `⌊b/2⌋` and `⌊b/2⌋ + 1 + 1`: `2b`
  squares.  For `7 ≤ k ≤ 3 · 10⁵` no other `b` or axis layering of this construction does better
  (`search/ryu/r1prime.py`);
* **staircase** (Ryu's §6; the idea of replacing the lower squares of tilted columns by axis layers is Bui's): columns
  at one tilt `α`, layers under them, wedge rows at the left wall; end cost `O(b^{2/3})`, and with `b ≈ k^{3/5}` the
  exponent `2/5`.  Our version (`RyuStair`, `RyuStairCount`, `RyuStairEnd`) takes `tan(α/2) = (√2 + 1/v)/v` with
  `b ≈ v³` and a lift `y ∈ [3v²/4, 3v²/4 + 2]`, lets each layer run to the right wall when it fits, and bounds the
  number of squares from the floors directly (`EndP.count`: each floor loses at most `1`), with no area argument;
  the end cost is `≤ 4.33 v² + 11 v + 30` (`end_bound`; the leading `2√2 + 3/2` is Ryu's limit constant).

Fang's theorem is a gluing induction (Arslanov–Mustafin–Shangitbayev's decomposition) over 18 exact piece
certificates: `certificates/fang-gluing/`.

## Files

| file | content |
|---|---|
| `RyuBand.lean` | the band (Ryu's Lemmas 3.1–3.4), transposition, the L-shape (Lemma 4.1) |
| `RyuBound.lean` | Ryu's Theorems 1.3–1.4: the angle, the row counts, `packs_sub_8sqrt` |
| `RyuFill.lean` | one axis layer per end: `packs_sub_4sqrt2` |
| `RyuEnds.lean` | lifted bands and end regions (`band_ends`), half-plane separation, the rotation by π, axis layers |
| `RyuLayers.lean` | two top layers: `packs_sub_4sqrt2_layers` |
| `RyuStair.lean` | the staircase geometry (`staircase`), finite unions of closed regions |
| `RyuStairCount.lean` | the staircase parameters, `EndP.packs`, the closed-form count `EndP.count` |
| `RyuStairEnd.lean` | the end cost: `lb_identity`, the six term bounds, `tilt_ok`, `end_bound` |
| `RyuStairBound.lean` | the band facts, rows, the waste identity, `packs_stair`, the two closed forms |
| `FangGlue.lean`, `FangTheorem.lean`, `FangFinal.lean`, `ExactCheckCut.lean`, `ExactRect.lean` | Fang's theorems |

Numerical companions: `search/ryu/r1prime.py` (the axis-filled L-shape, exact rationals, pairwise check),
`search/ryu/endcost.py` (axis vs staircase end cost), `search/ryu/staircase.py` (our staircase end: exact-floor end
cost, the closed form `lb`, and the bound `Eub`).

## Status and credits

Not peer reviewed.  Novelty of the two bold bounds checked against jlevy's register
(`packing/frontier/asymptotic-waste-bounds.yaml`, 2026-10-18) and Ryu's paper (v1.1, including §12 "Other end
constructions"); a wider literature check has not been done.  Mathematics as credited in the table; S. Ryu's
preprint *k² − c upper bounds* (squarepacker/k2-minus-c-upper v1.1) for the L-shape, the waste identity and the
staircase, with H. D. Bui's construction behind the staircase, and Erdős–Graham behind the L-shape.  The axis-filled
ends were suggested by a literature-reading agent of this repository (2026-10-17,
`literature/waste-constructions-2026-10-17.md`).  Formalization: this repository (Evan Daniel, with Claude),
2026-10-17/18.
