# s(95) = 10

Benjamin Greff, October 2026.

Let s(n) be the least side of a square that holds n non-overlapping unit squares with
arbitrary orientations. This repository contains a computer-assisted proof of

```
s(95) >= 10,   hence   s(95) = 10   (the 10 x 10 grid holds 100 >= 95 squares).
```

This is the case k = 10 of the k² − 5 series. It comes after wand125's s(59) = 8 (k = 8) and our
s(76) = 9 (k = 9, [bengreff/s76-certificate](https://github.com/bengreff/s76-certificate)). The
previous best lower bound was 9.965 (wand125). The proof is computer-assisted and has not been
peer reviewed.

## The argument

`cover/s95_cover_v2.txt.gz` defines a finite measure μ ≥ 0 on the closed square [0, 10]². It is
in Evan Daniel's "mixed 1" format: point masses, plus mass spread uniformly along axis-parallel
segments. Two facts give the lower bound:

1. **Total mass.** μ([0,10]²) = 3791753447/40000000 = 94.793836175 < 95.
2. **Covering.** Every closed unit square Q ⊂ [0,10]², at any position and orientation, has
   μ(Q) ≥ 1. A point on the boundary, or a segment along an edge, counts.

Suppose 95 unit squares fit in a square of side L < 10. Scale the packing up to side 10. Each
enlarged square contains a concentric closed unit square, and these are pairwise disjoint. They
would capture mass ≥ 95, which is a contradiction.

The cover file:

- `s95_cover_v2.txt`, sha256 `8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c`
- 48,352 points and 11,438 segments
- coordinates X/8000, weights w/(4·10⁸)

## How fact 2 is certified

- **Symmetry.** μ is exactly invariant under the dihedral group D4 of the container (`zmx2 d4`).
  It suffices to cover the fundamental region: centres in [0, 5]², angle 2·arctan u with
  u ∈ [0, 1/2].
- **Checkers.** Both are Evan Daniel's, used unchanged from evand/square-packing@b91d70b and
  pinned by sha256.

  | file | sha256 prefix |
  |---|---|
  | zmx2.rs | 6b7f0f79 |
  | zm_mixed.py | ee3e2915 |
  | zeromargin.py | 640fe453 |
  | mixed_cover.py | bb89de15 |

| step | checker | region | result |
|---|---|---|---|
| exact total, format, μ ≥ 0 | `tools/check_total.py` (exact rationals) | whole file | 3791753447/40000000 < 95 |
| D4 invariance | `zmx2 d4` (exact) | whole file | invariant |
| covering | `zmx2 cert --d4` (outward-rounded binary64) | 10,000 roots of 1/10 × 1/10 × 1/8 | 15,065,314 boxes; 9,981 roots certified; 8,263 boxes uncertified in 19 roots; no root capped |
| covering | `zm_mixed.py cert --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24` (exact rationals) | the 19 remaining roots, split into 304 roots of 1/20 × 1/20 × 1/32 | 9,614 boxes, max depth 13, 0 uncertified |
| coverage | `tools/check_coverage.py` | — | the zmx2 roots tile the region; the 304 zm_mixed roots tile the 19 remaining ones |

Records:

- `records/zmx2/zmx2_s95_v2.log.gz` has one `ROOT` line per root; the summary is
  `zmx2_s95_v2.out`. The 19 roots are listed in `failing_roots.txt`.
- `records/zm_mixed/j*.jsonl` has one record per root, including the census. Each header carries
  the cover's sha256. `jobs.txt` lists the 304 sub-roots, and `log_tails/` holds the end of each log.
- `records/toolchain.txt` gives the compiler, the zmx2 binary hash and the Python version.

## Lean

`lean/S95Lower.lean` builds against Evan Daniel's `Sqpack` library at commit 1718a58 (Lean
v4.33.1 and its Mathlib). It proves

```lean
theorem s95_eq_10 (hcov : S95Cover) : minSide 95 = 10
-- 'SquarePacking.s95_eq_10' depends on axioms: [propext, Classical.choice, Quot.sound]
```

- **Kernel-checked:** the data facts in `S95T/Pts.lean`. These are no duplicate atoms, exact D4
  invariance, and total < 95. The file is generated from the cover by `lean/mk_lean.py`. The
  reduction `le_minSide_mixed` and the 10 × 10 grid are also checked.
- **Hypothesis:** `S95Cover`, the covering statement on the D4 fundamental region (`CovM`). That
  is what the checkers above certify. It is not proved in Lean.

## Reproduce

```sh
sh verify.sh /tmp/s95-check 8
```

It needs git, Python 3 with numpy, and Rust ≥ 1.86. The checkers are fetched from upstream at
the pinned commit; they are not bundled.

A clean run from a fresh clone took 5 min 8 s wall on 8 threads of an i7-14700K under WSL2 (39
CPU-minutes). Each zm_mixed job prints `VERIFIED-D4 (PARTIAL)` because it covers only its own
sub-root; `tools/check_coverage.py` then checks that the pieces tile the whole region.

## How the cover was found (not part of the proof)

The construction is the same as for s(76), one size up.

- **Corners.** The four corner regions [0, 2.5)² and their images are wand125's certified
  s(59) = 8 cover, unchanged. The band of width 2 is inserted at x = 4 and y = 4.
- **Cross.** The cross {x or y ∈ [2.5, 7.5]} was re-optimized by linear programming over
  D4-orbit weights. Candidates:
  - a 1/20 lattice;
  - the base's own positions;
  - 1/16 segments on integer lines;
  - 2/1000 segments for lattice points on integer lines.
- **LP settings.** Free points are capped at 0.004 and the row margin is 0.006. Bottom-wall tile
  germs get margin 0.012.
- **Excluded points.** 70 point orbits are excluded to break exact coincidences of many atoms with
  the edges of one square. Two kinds occurred:
  - the 3-4-5 angle 2·arctan(1/3), where all four edges can hit the lattice;
  - the angle arctan(1/5), where the edge directions (5, 1) and (−1, 5) are lattice directions,
    so two adjacent edges can each pass through several lattice atoms.

  zm_mixed cannot close either kind at any depth. `construction/find_coinc.py` and
  `find_near_edge.py` locate the atoms from zm_mixed's uncertified boxes.
- **Speed.** The LP has 6,867 columns and up to about 480,000 rows. It was solved with
  `construction/gpu_ipm.py`, a mixed-precision interior-point method on the GPU. It forms the
  normal matrix by a float32 GEMM, factors it in float32, and refines each Newton direction by
  preconditioned CG with exact float64 sparse products. Per LP round it took 6–12 minutes,
  where HiGHS's single-threaded IPM took up to 7 hours (one round: 485 s against 25,523 s).
- **Rounds.** With it, the cutting-plane loop converged in 7 rounds (4 h). After the exclusions,
  3 more rounds (32 min) gave the final cover. The loop is `construction/run18.py`.

These scripts are research code; they are not needed to check the proof.

## Credits

- **Evan Daniel** ([evand/square-packing](https://github.com/evand/square-packing), MIT): the
  weighted-cover method at margin zero, the mixed format, the checkers `zmx2`, `zm_mixed.py`
  and `zeromargin.py`, and the Lean library.
- **wand125** ([wand125/square-packing](https://github.com/wand125/square-packing), MIT): the
  s(59) = 8 cover reused for the corners, and the band-insertion construction.
- **Benjamin Greff** directed the work. The search, LP and verification pipeline were built and run
  with Claude (Anthropic) as an AI assistant.
