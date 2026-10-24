# Fang's gluing theorem: formalize, generalize, improve (started 2026-10-17)

Evan's pick (10-17).  Source: K. Fang, *Packing n² − n + 1 unit squares in a square of side less than n, for every
n ≥ 15* (draft v0.6, 2026-10-13; the note itself is unpublished), certificates at `TheSnakeFang/squarepack-certs@078789a`
(no Lean there).  jlevy/squares#603, registered as T-163 (V2/C1, S4).  Credit line there: *Fang after Arslanov,
Mustafin, Shangitbayev, Ellsworth, Stead, de Winter, Daniel, Couzo*.

* **Theorem 1.** s(n² − n + 1) < n for n ≥ 15.
* **Theorem 2.** n ≥ 15, 16p + 21q ≤ n − 15 ⇒ n² − n + 1 + p + 2q squares pack in side < n.

## The proof in one paragraph

Lemma 3 (Arslanov–Mustafin–Shangitbayev's decomposition): squeezable A (box a × b) top left, squeezable B (box a' × b')
bottom right, two aligned blocks in the other corners, side n − d with n = b + b'.  Every row and column meets A or B,
so the blocks slide by d.  Wastes add: waste(n) = waste(A) + waste(B).  A 17 × 16 rectangle with 257 squares (waste 15)
adds +16 to the side and +1 to the excess; a 22 × 21 with 443 (waste 19) adds +21 and +2.  Bases: r² − r + 1 in side
< r for r = 15..26 (de Winter 211; Daniel's certs of Ellsworth/Stead 241, 273; Fang's 308, 343, ..., 651), and for
r = 27..30, R glued to m² − m (m = 11..14: Ellsworth's 110, AMS21's 132, 156, 182).

## Status

| step | state |
|---|---|
| 1. Lean reduction | **done 10-17**: `lean/Sqpack/FangGlue.lean` (`glue`: Lemma 3 on `PacksIn`, any real d ≥ 0), `lean/Sqpack/FangTheorem.lean` (`Squeezable`, `Excess`, `Squeezable.glue/step`, `FangPieces` structure, `FangPieces.theorem1/2`).  Axioms: propext, Classical.choice, Quot.sound. |
| 2. Base certificates in Lean | **done 10-17**: all 18 pieces (`certificates/fang-gluing/`, `search/exact/fang_pieces.py`, rectangle checker `lean/Sqpack/ExactRect.lean`), 30-136 s each, ~19 min total; `lean/Sqpack/FangFinal.lean`: `theorem1`, `theorem2` unconditional, standard axioms. Earlier note: square pieces: existing `lean_cert.py` + `ExactCheck` (decide +kernel) works with K = Q (converter `f = T, t = 0`).  Rectangle pieces (257, 443) need a rectangle container: not started. |
| 3. Better linear pieces | not started (packer target: squeezable a × b with gain/height > 2/21). |
| 4. Explicit power law | already done by Ryu (c*(k) ≤ 8⌈√(k−4)⌉ − 1, k ≥ 6; jlevy #471/#486, registered as reported). Next: formalize his L-shaped family (closed form, all k), then the subagent's end-fill variant R1′ (~5.66√k, unproved for all k). `literature/waste-constructions-2026-10-17.md`. |

## Cost of step 2 (measured 10-17)

Trial: Fang's n0651 (CC0) → `lean_cert.py --split 25` (2.7 s; shadows leave 36 exact conditions, 1 exact pair,
2 exact boxes) → 27 chunk modules + Data.  The heaviest chunk (C0, rows 0-24, ~16k pairs) alone: ~2 min, **peak RSS
20.6 GB**.  Light chunks: 30 s-1 min.  So n = 651 is ~0.5 CPU-h; the whole square base set (~1.18M pairs, vs 212k for
651) ~2-3 CPU-h.  **Memory is the constraint**: a plain `lake build` ran 20 chunks at once and hit 120 / 125 GB
(stopped).  Build with few jobs (≤ 5) or smaller chunks.

**Sweep-line pruning (done 10-17)**: `lean/Sqpack/ExactCheckCut.lean` (`sortedOK`, `cutOK`, `rowOKc`,
`packs_exact_cut`; `Cert` and `packs_exact` unchanged) + `lean_cert.py --cut` (needs `--split`).  Squares sorted by
the enclosure's x lower bound; row i visits only j < cut i, the first j with x_lo(j) ≥ x_hi(i) + 3/2; every later j
passes `farOK` (x gap ≥ 3/2 ⇒ gap² ≥ 2).  It also kills the n³ term: `![…]` lookups of `encl j` are linear in j.
n = 651: 23,554 pairs visited instead of 211,575 (max 49 per row); worst chunk 16 s / 8 GB (was ~120 s / 20.6 GB);
**whole certificate 110 s wall at 8 chunks in parallel** (`xargs -P 8` over per-chunk `lake build`; a bare `lake
build` runs every chunk at once).  `#print axioms` on `N651.packs`: standard three.  The old (non-cut) output is
byte-identical to before (N100 regenerated and diffed).

Rectangle container: `ExactPack.InBox S` → an `InRect W H` variant plus `packsIn_of_cert` into `rect W H`; in
`ShadowCheck.inBoxOK` / `ExactCheck.boxN` the upper wall splits into W (x) and H (y).  A small separate rational-only
checker may be simpler than touching the field checker.

## Generalization (10-17 discussion)

* Gluing is additive: side and waste both add, widening a rectangle with aligned columns is free, and stacking adds
  heights and wastes.  So the closure of a piece library has slope = the best single piece's (b − w)/b.  Better
  linear constants need better pieces, never more gluing.
* Power law needs pieces whose gain grows faster than their height: the waste-bound constructions (Erdős–Graham 7/11,
  ..., ~0.6) recurse on non-integer regions (tilted-column strips, triangles).  Lean target: "if region T(ℓ, θ)
  holds ≥ X(ℓ, θ) squares then the square of side n − ε holds n² − W(n)", with every piece given by a formula, so no
  per-n certificates are needed.
* Pareto frontier: "linear, explicit constants and constructions" (Fang) vs "power law, no constants" (literature);
  the target is an explicit power law with an explicit threshold.

## Piece table and slopes (10-17)

Best excess j(m) = (max n with s(n) < m) − (m² − m), from the store (`search/packer/runs/store.sqlite`, all sources):

| m | 11–14 | 15–17 | 18–22 | 23–25 | 26–28 | 29–31 | 32 | 33 | 34–36 | 37–39 | 40 | 41–64 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| j | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 5 | 6 | 7 | **8** | 3–6 (Fang's composites, gap 1/20000) |

23–40 are de Winter's (jlevy#666, exact certificates; search results, heavily tilted: 983 / 1568 tilted at 40, no
evident family).  Beyond 40 nothing direct is known: only gluing.  j/m rises from 0.13 (m = 23) to 0.2 (m = 40).

* Gluing a *square* piece as A costs one square: widen it by a column of m − 1 aligned squares to an (m + 1) × m
  rectangle of gain j − 1 (equivalently: the two aligned blocks would overlap in a d × d corner).  [checked on paper]
* DP (rectangles R, R' plus widened squares of the table; bases = the table): best slope 7/40 = 0.175 (the 40 piece).
  E(n) vs Fang's F(n): n = 64: 11 vs 5; 100: 16 vs 9; 324: 54 vs 29; 1000: 176 vs 94; 2000: 351 vs 189.  So roughly
  **s(n² − n + 0.17 n) < n** for large n, about double Fang, given exact checks of the pieces.
* Every m ≥ 41 would be a new beyond-horizon record (store: j = 3–6 there).
* A lossless (m + 1) × m rectangle from the 40 piece (as Fang cut his rectangles from n² − n + 1 packings) would give 8/40.

## Comparison with Ryu (10-17)

Upper bounds on c*(k): Fang k − 1 − F(k); gluing with de Winter's pieces k − 1 − E(k); Ryu 8⌈√(k−4)⌉ − 1.
k = 40: 36 / 31 / 47; 80: 72 / 64 / 71; 100: 90 / 83 / 79; 150: 136 / 123 / 103.  Gluing beats Ryu only up to k = 94
(Fang: 86).  So better linear pieces are a small win; order (Evan 10-17): finish Fang in Lean (done), then Ryu's family.

## Ryu's Theorem 1.4 in Lean (done 10-17)

`lean/Sqpack/RyuBand.lean` (geometry: same-angle separation `sep_U`/`sep_V`, `unitSq_subset_box`,
`PacksIn.transpose`, `band`, `lshape`, `lpacking`) and `lean/Sqpack/RyuBound.lean` (angle and counts):
`packs_sub_8sqrt : ∀ k ≥ 6, ∃ s < k, Packs (k·k − 8(⌊√(k−5)⌋ + 1)) s`, i.e. c*(k) ≤ 8⌈√(k−4)⌉ − 1, and
`packs_sub_8b` (any b ≥ 2 with b + 4 ≤ k ≤ b² + 4).  Standard axioms, no certificates, ~400 lines.
Simplification over Ryu: rows R₁ = k − 4, R₂ = k − b − 4 directly (no ceilings; k² − N = 8b exactly), slack 4/D at
t₀ = 1/b, tilt t = 1/b + 1/(D(6k + 4b)) with three one-variable perturbation bounds instead of his mean-value
argument and M = 14kb² + 1.
Next: the end fills (R1′, ~4√(2k)); `literature/waste-constructions-2026-10-17.md` §3.
