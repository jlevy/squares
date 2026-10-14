# s(76) = 9

Benjamin Greff, October 2026.

Let s(n) be the least side of a square that holds n non-overlapping unit squares with
arbitrary orientations. This repository contains a computer-assisted proof of

```
s(76) >= 9,   hence   s(76) = 9   (the 9 x 9 grid holds 81 >= 76 squares).
```

This is the case k = 9 of the k² − 5 series. The previous best lower bound was 8.965 (wand125).
The proof is computer-assisted and has not been peer reviewed.

## The argument

`cover/s76_cover_v5.txt.gz` defines a finite measure μ ≥ 0 on the closed square [0, 9]². It is in
Evan Daniel's "mixed 1" format: point masses plus mass spread uniformly along axis-parallel
segments. Two facts give the lower bound:

1. **Total mass.** μ([0,9]²) = 3788361049/50000000 = 75.76722098 < 76.
2. **Covering.** Every closed unit square Q ⊂ [0,9]², at any position and orientation, has
   μ(Q) ≥ 1. A point on the boundary, or a segment along an edge, counts.

Suppose 76 unit squares fit in a square of side L < 9. Scale the packing up to side 9. Each
enlarged square contains a concentric closed unit square, and these are pairwise disjoint. They
would capture mass ≥ 76, which is a contradiction.

- File: `s76_cover_v5.txt`
- sha256 `b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2`
- Contents: 41,633 points and 9,744 segments, coordinates X/8000, weights w/(4·10⁸)

## How fact 2 is certified

- **Symmetry.** μ is exactly invariant under the dihedral group D4 of the container
  (`zmx2 d4`). It therefore suffices to cover the fundamental region: centres in [0, 9/2]²,
  angle 2·arctan u with u ∈ [0, 1/2].
- **Both checkers are Evan Daniel's**, used unchanged from evand/square-packing@b91d70b and pinned
  by sha256:

  | file | sha256 prefix |
  |---|---|
  | zmx2.rs | 6b7f0f79 |
  | zm_mixed.py | ee3e2915 |
  | zeromargin.py | 640fe453 |
  | mixed_cover.py | bb89de15 |

| step | checker | region | result |
|---|---|---|---|
| exact total, format, μ ≥ 0 | `tools/check_total.py` (exact rationals) | whole file | 3788361049/50000000 < 76 |
| D4 invariance | `zmx2 d4` (exact) | whole file | invariant |
| covering | `zmx2 cert --d4` (outward-rounded binary64) | 8,100 roots of 1/10 × 1/10 × 1/8 | 8,096 certified; 4 with uncertified boxes; no root capped |
| covering | `zm_mixed.py cert --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24` (exact rationals) | the 4 remaining roots, split into 64 roots of 1/20 × 1/20 × 1/32 | 64 certified, 0 uncertified boxes |
| coverage | `tools/check_coverage.py` | — | the zmx2 roots tile the region; the 64 zm_mixed roots tile the 4 remaining ones |

Records:

- `records/zmx2/zmx2_v5.log.gz` has one `ROOT` line per root; the summary is `zmx2_v5.out`.
- `records/zm_mixed/j*.jsonl` has one record per root, including the census. Each header carries
  the cover's sha256.
- `records/zm_mixed/jobs.txt` lists the 64 sub-roots.
- `records/toolchain.txt` gives the compiler, the zmx2 binary hash and the Python version of the
  clean replay.

## Lean

`lean/S76Lower.lean` builds against Evan Daniel's `Sqpack` library at commit 1718a58 (Lean
v4.33.1 and its Mathlib). It proves

```lean
theorem s76_eq_9 (hcov : S76Cover) : minSide 76 = 9
-- 'SquarePacking.s76_eq_9' depends on axioms: [propext, Classical.choice, Quot.sound]
```

- **Kernel-checked:** the data facts in `S76T/Pts.lean`, generated from the cover file by
  `lean/mk_s76_lean.py` (no duplicate atoms, exact D4 invariance, total < 76), and the reduction
  `le_minSide_mixed` with the 9 × 9 grid.
- **Hypothesis:** `S76Cover`, the covering statement on the D4 fundamental region (`CovM`). That is
  what the checkers above certify. It is not proved in Lean.

## Reproduce

```sh
sh verify.sh /tmp/s76-check 8          # checker hashes, exact total, zmx2 d4 and cert, zm_mixed on the 64 roots, coverage
sh verify.sh /tmp/s76-full 24 --full-zm  # also zm_mixed over all 129,600 roots of the D4 region (long)
```

It needs git, Python 3 with numpy, and Rust ≥ 1.86. The checkers are fetched from upstream at the
pinned commit and not bundled.

A clean run from a fresh clone took 9 min 13 s wall with 4 threads (35 CPU-minutes) on an
i7-14700K under WSL2: 75 s for the zmx2 sweep and the rest for zm_mixed on the 64 sub-roots. Each
zm_mixed job prints `VERIFIED-D4 (PARTIAL)` because it covers only its own sub-root;
`tools/check_coverage.py` then checks that the pieces tile the whole region.

## How the cover was found (not part of the proof)

- **Corners.** The four corner regions are taken from wand125's certified s(59) = 8 cover, with
  the central cross band inserted: cut at x = 4 and y = 4, far side shifted by 1. This is
  wand125's construction for s(77) = 9 from s(60) = 8.
- **Cross.** The cross {x or y in [2.5, 6.5]} was re-optimized by linear programming over D4-orbit
  weights. Candidates are:
  - the base's own positions;
  - a 1/20 lattice;
  - 1/16 segments on integer lines;
  - segments of length 2/1000 for lattice points that fall on integer lines.
- **LP settings.** Free point masses are capped at 0.004 and the margin is 0.005. Bottom-wall tile
  germs get margin 0.012. 28 point orbits are excluded to break exact coincidences of many atoms
  on the boundary of one square at the angle 2·arctan(1/3), which zm_mixed cannot resolve at any
  depth.
- **Cutting-plane loop.** HiGHS IPM; GPU screening; zmx2 sweeps; dense float64 scans of the
  zmx2-failing roots; exact zm_mixed `pose` checks of suspected violations. Scripts are in
  `construction/`. Inputs and settings are recorded there but they are research code, not needed
  to check the proof.

## Credits

- **Evan Daniel** ([evand/square-packing](https://github.com/evand/square-packing), MIT): the
  weighted-cover method at margin zero, the mixed format, the checkers `zmx2`, `zm_mixed.py` and
  `zeromargin.py`, and the Lean library.
- **wand125** ([wand125/square-packing](https://github.com/wand125/square-packing), MIT): the s(59) = 8
  cover reused for the corners, the band-insertion construction, and the pinned toolchain.
- **Benjamin Greff** directed the work. The search, LP and verification pipeline were built and run
  with Claude (Anthropic) as an AI assistant.
