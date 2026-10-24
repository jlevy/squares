# Fang's theorems in Lean: the pieces

**Result** (`lean/Sqpack/FangFinal.lean`, axioms propext / Classical.choice / Quot.sound only):

* `theorem1 : ∀ n ≥ 15, ∃ s < n, Packs (n·n − n + 1) s`, i.e. s(n² − n + 1) < n;
* `theorem2 : ∀ n p q, 15 ≤ n → 16p + 21q ≤ n − 15 → ∃ s < n, Packs (n·n − n + 1 + p + 2q) s`.

Theorems: Kevin Fang, *Packing n² − n + 1 unit squares in a square of side less than n, for every n ≥ 15* (draft
v0.6, 2026-10-13; `TheSnakeFang/squarepack-certs@078789a`; jlevy/squares#603, T-163), after Arslanov, Mustafin and
Shangitbayev (Electron. J. Combin. 28(4) P4.22, 2021), whose decomposition is the gluing lemma.  Formalization
(gluing lemma, induction, checkers): this repository, 2026-10-17 (`tasks/fang-gluing/`).

## Inputs (`inputs/`, exact rational certificates; `SHA256SUMS`)

Line 1 `n S` (square) or `n W H` (rectangle), then `x y t` per square, t = tan(θ/2).  Packings are mathematical
facts; credit as follows.

| file | count, container | packing found by | certificate |
|---|---|---|---|
| `R257` | 257 in (17 − δ) × (16 − δ) | Kevin Fang (from Ellsworth–Stead's 241) | Fang, `rectangles/r17x16_n0257` |
| `R443` | 443 in (22 − δ) × (21 − δ) | Kevin Fang | Fang, `rectangles/r22x21_n0443` |
| `P110` | 110 in side < 11 | David Ellsworth | Evan Daniel |
| `P132`, `P156`, `P182` | m² − m in side < m, m = 12, 13, 14 | Arslanov, Mustafin, Shangitbayev (2021) | Evan Daniel |
| `P211` | 211 in side < 15 | Joost de Winter | Evan Daniel |
| `P241`, `P273` | 241 in < 16, 273 in < 17 | David Ellsworth, Peter Stead (Kingbird) | Evan Daniel |
| `P308`, `P343`, `P381`, `P421`, `P463`, `P507`, `P553`, `P601`, `P651` | m² − m + 1 in side < m, m = 19…26; 308 in < 18 | Kevin Fang | Fang, `n0NNN/` |

P110–P273 are `search/exact/minpoly/solve/n-N.cert` (our exact forms of the register records); Fang's files are
copied byte for byte from `078789a`.

## Rebuilding

```
python3 search/exact/fang_pieces.py                 # -> lean/Sqpack/Exact/Fang/ (gitignored, 6.4 MB, ~1 min)
for m in P110 P132 P156 P182 P211 P241 P273 P308 P343 P381 P421 P463 P507 P553 P601 P651 R257 R443; do
  lean/scripts/build_chunks.sh Sqpack.Exact.Fang.$m 8; done      # ~19 min wall, <= ~8 GB per chunk
cd lean && lake build Sqpack.FangFinal
```

Do not `lake build Sqpack.FangFinal` from scratch: it starts every chunk at once.
