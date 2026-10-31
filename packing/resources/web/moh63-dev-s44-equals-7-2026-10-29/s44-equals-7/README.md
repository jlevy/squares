# s(44) = 7: forty-four unit squares need a square of side 7

**Claim.** No 44 unit squares (free rotation, pairwise disjoint interiors) fit in a square of side less than 7.
Since the 7 × 7 grid holds 49, **s(44) = 7**.  Before this, the record was 6.9725 ≤ s(44) ≤ 7
([squaremath.org/cases/44](https://squaremath.org/cases/44.html)).

Authors: **Mohsen Khalili** and **Sara Gharabaghi** (independent researchers), with AI assistance (see below).
Computer-assisted; not yet peer reviewed or formalized.

## The proof in one paragraph

`certificate/s44_cover_7.txt` describes a measure μ on [0, 7]²: 15,525 weighted points and 3,912 uniformly
weighted pieces of the grid lines x, y ∈ {1, …, 6}, with exact rational masses of total
**2199755099/50000000 = 43.99510198 < 44**.  The claim checked by computer is that **every closed unit square
in [0, 7]², at every position and angle, has μ-mass at least 1**.  If 44 unit squares fit in a square of side
s < 7, enlarging the whole configuration by the factor 7/s > 1 and then shrinking each square back to unit size
about its own center gives 44 unit squares in [0, 7]² that are pairwise disjoint as closed sets.  Each has mass
≥ 1, and disjoint sets share no mass, so the total mass would be ≥ 44, a contradiction.  These two steps are
standard (Göbel, Stromquist); in this closed form they are proved in Lean in Daniel's repository
(`packing_le_measure`, `not_packs_of_measure` in `lean/Sqpack/MixedMeasure.lean`).  The paper gives full proofs.
Format: `certificate/FORMAT_mixed_v1.md` (Evan Daniel's mixed-cover format).

## What checked it

| check | what it does | result | cost |
|---|---|---|---|
| `zmx2 --d4` (Rust, E. Daniel) | exact rational subdivision of all poses in the D4 fundamental region | **VERIFIED-D4**, all roots, 0 uncertified | 191 s, 1 thread |
| `zmx2 --full` (same program) | the same with no symmetry reduction: every center and angle | **VERIFIED**, all roots, 0 uncertified | 27.6 min, 1 thread |
| `zm_mixed.py --d4` (Python, E. Daniel, separately written) | exact `Fraction` subdivision with its own primitives | VERIFIED-D4: all 9,800 roots at depth 24; the 27 roots with uncertified boxes there (1,265 boxes) re-run in full at depth 30, 0 uncertified (max depth 29) | ≈143 CPU-h |
| `verification/sanity.py` (this repo) | exact total < 44, file well-formed, measure D4-invariant | OK | < 1 s |
| `verification/stress.py` (this repo, float) | mass of 675,000 random / near-tile / near-45° squares | min 1.0031 | seconds |
| `search/tilesep.py` (this repo, float) | targeted search for near-wall low-mass valleys | min 1.0034, none below 1 | 2 min |

Rerun: `bash verification/verify.sh`.  `--fast` (about 5 minutes) runs the exact sanity check, the zmx2 D4 sweep
and an audit of our recorded zm_mixed logs (every one of the 9,800 roots finished, and every root left with
uncertified boxes at depth 24 has a depth-30 run with none).  The default also runs the full zmx2 sweep and the
complete zm_mixed check, `verification/zm_mixed_check.py run`, which repeats our two-stage procedure (depth 24
everywhere, then depth 30 where needed) in parallel and resumably; it takes about 140 CPU-hours.  The checkers are used **unmodified**
from [evand/square-packing@659ee62](https://github.com/evand/square-packing/tree/659ee62e4a9d39542a1146e8b011cc3ab6407ede)
(`verify2/` = zmx2, `search/zm_mixed.py`).

**What the checkers share.**  Both exact checkers were written by the same author (Evan Daniel) and share the
closed-semantics conventions and the D4 reduction (zmx2 `--full` removes the latter).  The float checks and the
sanity script in this repository share no code with either.

**Not done.**  No Lean formalization; no external review yet.  Note: at the pinned commit `zm_mixed.py` prints
`zeromargin.py sha256 … DIFFERS FROM PINNED` because the upstream `zeromargin.py` changed after `zm_mixed.py`'s
pin was last updated; we used both files exactly as they are at that commit.

## How it was found (not part of the proof)

`search/cover_loop.py`: a cutting-plane loop on the linear program "minimize total mass subject to every sampled
square having mass ≥ 1" (Daniel's `line_cover.py` model, D4 orbits, segment pieces of length 1/50), alternating
LP solves, float separation, and zmx2 runs on the cover scaled to total 43.995; uncertified boxes become new
constraints.  The new ingredient, `search/tilesep.py`, searches for low-mass *valleys* of nearly axis-parallel
squares resting on a wall next to a corner, tilted 0.01°–3°, which the standard lattice separation (pitch 0.01,
0.5° steps) and the θ = 10⁻⁵ germ family both miss.  With only ≈ 0.4 % slack (LP 43.82 vs. 44) these valleys
were what blocked verification.  Round history: `search/ROUNDS.md`.

## Lineage and credit

- Unavoidable sets: Göbel, Stromquist, Friedman (DS7); weighted points, segments and areas: Nagamochi.
- Weights found by linear programming and checked in exact rational arithmetic: **Sam Burns**, **Gustavo Massaccesi**.
- Closed mixed covers (points plus grid-line segments), the mixed format, the exact checkers `zmx2` and
  `zm_mixed.py`, the `line_cover` model, and the s(45) = 7 cover used as the starting point: **Evan Daniel**
  ([evand/square-packing](https://github.com/evand/square-packing/tree/659ee62e4a9d39542a1146e8b011cc3ab6407ede), MIT).
- Public mixed-cover certificates, including s(59) = 8: **Hiroaki Hosono** (wand125).

## AI assistance

The search, the certificate, the new valley-separation tool and the verification runs were produced with
Claude (Anthropic) under our direction; we reviewed the method, the checks and this write-up.

## License

Scripts in this repository: MIT (see `LICENSE`).  The certificate is released into the public domain (CC0).
