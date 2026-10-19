# Band lemma: local minimality of the integer-side records (10-07)

**Result.**  Every register record with integer side S = k (176 for n ≤ 324, 53 for n ≤ 82) is a local minimum
in the sense of `IsLocalMinPacking` (`lean/Sqpack/LocalMin.lean`).  One lemma covers all of them, with no contacts,
multipliers or field arithmetic.  All 53 with n ≤ 82 are kernel-checked in Lean (standard axioms).

## Statement

**Band lemma** (`le_side_of_band`).  Take a packing of unit squares in `[0, s]²` and a line `y = y₀`.  Let `k`
distinct squares each satisfy, with `δ` its angle mod 90° (`cos δ > 0`) and `b` its centre height,

    |y₀ − b| / cos δ + |sin δ| / 2 < 1/2.

Then `k ≤ s`.

**Local minimum** (`isLocalMin_of_band`).  Let a packing in `[0, k]²` contain `k` axis-parallel squares whose
centres lie within `1/2 − m` of one line `y = y₀`, with `0 < m ≤ 1/2`.  Then it is `IsLocalMinPacking` with
`ε = m/2`.  An aligned row (all centres at the same height) has `m = 1/2`, so `ε = 1/4`.  Only the `k` band squares
need to stay near their record poses: the other squares can be anywhere.

## Proof

1. **Chord.**  A square with centre `(a, b)` at angle `δ` satisfying the inequality above contains the closed unit
   segment of the line `y = y₀` centred at `x_m = a − (y₀ − b) tan δ`, and its interior contains the open segment.
   In the square's own coordinates the point `x_m + u` has coordinates `u cos δ` and `(y₀ − b)/cos δ − u sin δ`, both
   of absolute value `≤ 1/2` for `|u| ≤ 1/2` (and `< 1/2` for `|u| < 1/2`).  So tilting never shortens the chord
   below 1.  It only moves the chord, and the true chord `1/cos δ` is longer still.
2. **Separation.**  If two band squares had `|x_m − x_m'| < 1`, the midpoint of the two centres would lie in both
   open segments, so in both interiors.  Hence the `x_m` are pairwise at least 1 apart.
3. **Container.**  The endpoints `x_m ± 1/2` lie in the closed square, so in `[0, s]`: `x_m ∈ [1/2, s − 1/2]`.
4. **Counting** (`card_le_of_sep`).  `k` points of `[a, b]` pairwise at least 1 apart have distinct values of
   `⌊t − a⌋₊ ∈ {0, …, ⌊b − a⌋₊}`, so `k ≤ b − a + 1`.  Here that gives `k ≤ s`.
5. **Local minimum.**  Within `ε = m/2`: `|δ| < m/2 ≤ 1/4`, and `|y₀ − b'| < 1/2 − m/2`.  From
   `cos δ (1 − |sin δ|) ≥ (1 − δ²/2)(1 − |δ|) > 1 − m/2 − m²/8 ≥ 1 − m` we get
   `|y₀ − b'| < cos δ (1 − |sin δ|)/2`, which is the chord condition.

## Aligned rows, staggered chains, and tilted neighbours

* **What matters is a common line, not contacts.**  The band squares need not touch each other or the walls.  The
  hypothesis is that their open y-ranges share a point: vertical spread of the centres `< 1`.  An aligned row
  qualifies, and so does a staggered chain whose total vertical drift is `< 1`.
* **Interleaving corners do not help** a tilted neighbour.  Step 1 places a full unit segment in each square on the
  common line, whatever the tilts.  Disjointness on that one line is all the proof uses.
* **Staggered chains with drift ≥ 1: the lemma is false.**  Take a chain whose end squares differ in height by `D`
  and rotate it rigidly by a small `δ`.  Its horizontal extent becomes `k − δ(D − 1) + O(δ²)`.  Example: centres
  `(0.5, 0.5), (1.5, 1.2), (2.5, 1.9)`, `δ = 0.01`: width `2.9959 < 3`, height `2.43`.  Such a chain in isolation does
  not force `s ≥ k`.  Whether a record containing it is locally optimal depends on the other squares.  This is the
  staggered-chain trap that the packer avoids at n = 110 (PACKER.md).
* **No record needs a staggered band.**  Every integer-side record has an *aligned* row of `k` squares
  (`m = 1/2`).  167 of the 176 also have an aligned column.  The Lean lemma still accepts any `m > 0`.

## Coverage (`python3 search/exact/chain_lean.py --survey`)

| range | integer-side records | with a horizontal band | none |
|---|---|---|---|
| n ≤ 82 | 53 | 53 | 0 |
| n ≤ 324 | 176 | 176 | 0 |

n ≤ 82: 1 2 3 4 6 7 8 9 12 13 14 15 16 20 21 22 23 24 25 30 31 32 33 34 35 36 42 43 44 45 46 47 48 49 56 57 58 59 60
61 62 63 64 72 73 74 75 76 77 78 79 80 81.

These are exactly the `n` with `k(k−1) ≤ n ≤ k²` (k = 1…18).  n ≤ 324 adds 90–100, 111–121, 133–144, 157–169, 183–196,
212–225, 242–256, 274–289 and 308–324.  The records come from `batch/certs/n-N.cert`.  Coordinates are snapped from
the 1e-20-scaled certificate back to side `k` (small denominators, within 1e-12).  Each snapped record is then
re-checked exactly (Python `axis_ok`, then Lean `axisOK`).

## Lean

* `lean/Sqpack/ChainLocalMin.lean`: `band_chord`, `card_le_of_sep`, `le_side_of_band`, `isLocalMin_of_band`, and the
  certificate layer `axisOK` / `bandOK` / `isLocalMin_of_axisCert`:

  ```lean
  theorem isLocalMin_of_axisCert {n k : ℕ} (P : List (ℚ × ℚ)) (band : List ℕ) (y0 m : ℚ) (hn : P.length = n)
      (hP : axisOK k P = true) (hB : bandOK P n k band y0 m = true) :
      IsLocalMinPacking n k (fun i => cenOf P i) (fun _ => 0)
  ```

  `axisOK`: every square is in `[0, k]²`, and every pair is separated by at least 1 along `x` or along `y`.
  `bandOK`: `k` distinct indices `< n`, `|y_j − y₀| ≤ 1/2 − m`, `0 < m ≤ 1/2`.  Both are checked by
  `decide +kernel` over ℚ.
* `Exact/N8Chain.lean`: `UnitSquarePacking.Chain.N8.localMin : IsLocalMinPacking 8 3 (fun i => cenOf P i) (fun _ => 0)`.
  In the default build (about 4 s) and in `Axioms.lean`.
* `Exact/ChainUpTo82.lean`: all 53 integer-side records with n ≤ 82, as `UnitSquarePacking.ChainUpTo82.N<n>.localMin`.
  It takes about 92 s, the largest being n = 80 at about 6 s, so it is **outside the default build**
  (`lake build Sqpack.Exact.ChainUpTo82`).  All 53 theorems depend only on `propext, Classical.choice, Quot.sound`.
* Regenerate: `python3 search/exact/chain_lean.py 8` and `python3 search/exact/chain_lean.py --upto 82`.  `--upto 324`
  would give all 176 records.  The cost is mostly the O(n²) pair check, roughly 0.1–6 s per record at these sizes.

## Not covered

* **Every non-integer record** (tilted squares, field degree ≥ 2) still needs the grade A/B/C machinery
  (`grade-C.md`).  This lemma is only for side `k ∈ ℕ`.
* **Rotation by 90°.**  Records whose only band is vertical would need a transposed lemma.  None occur: all 176
  have a horizontal band in the register's orientation.
* **Scope.**  This is local optimality only.  `s(n) = k` itself is proved only for some of these n (`k²`, and
  `k² − 1`, `k² − 2` by Nagamochi); it is open for others, for example n = 12.  As in `grade-C.md`, the `IsLocalMinPacking` notion does not exclude a far-away
  descent.
