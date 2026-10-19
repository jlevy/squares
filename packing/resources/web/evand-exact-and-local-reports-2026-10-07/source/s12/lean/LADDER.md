# The Lean lower-bound ladder

Goal: kernel-checked lower bounds `s(n) ≥ t` from point certificates — **kernel reduction only**
(`decide +kernel`; no `native_decide`, no new axioms), with **one generic verifier proved sound
once**, and per result only data plus a one-line theorem.

Status (2026-09-28): rung 1 (pilot) done — `SquarePacking.s12_ge_35_9 : (35/9 : ℝ) ≤ minSide 12`,
`#print axioms` = `[propext, Classical.choice, Quot.sound]`, no `sorry`.  The same verifier, unchanged,
also proves rung-3 results from our weighted certificates: `s12_ge_3920_997 : (3920/997 : ℝ) ≤
minSide 12` (`S12WLower.lean`, 224 points, in the default build) and `s11_ge_3040_797 :
(3040/797 : ℝ) ≤ minSide 11` (`S11Lower.lean`, 680 points; **opt-in**, not imported by
`Sqpack.lean`: `lake build Sqpack.S11Lower`, ~26 min on 3 cores).  All print the same three
axioms.

**The headline bound, `s(12) ≥ 15680/3951 = 3.968616`, done (2026-09-28):**
`SquarePacking.s12_ge_15680_3951 : (15680/3951 : ℝ) ≤ minSide 12` (`S12HLower.lean`), from
`certificates/s12_lower_3.9686.txt` (1736 points, total weight 11.9738036), with the same `BoxTree`
verifier, unchanged, and the same one-call proof as `S12WLower.lean` (the point set is
D4-invariant, so no new root lemma).  `#print axioms` = `[propext, Classical.choice, Quot.sound]`; no
`sorry`, no `native_decide`.  Opt-in, data gitignored: `lean/scripts/gen_data.sh S12H` (39 min, one
core), then `lean/scripts/build_parts.sh S12H Sqpack.S12HLower 1 14-15` (6 h 31 min wall / 7.3
CPU-h on 2 cores, ≤ 30.6 GB RSS).  Details in the measurements below.

**Rung 2, the first zero-margin rung, done (2026-09-27):** `SquarePacking.s13_ge_4 : (4 : ℝ) ≤
minSide 13` and `SquarePacking.s13_eq_4 : minSide 13 = 4` (`S13Lower.lean`), from the case-free
3,621-point cover `certificates/rung2/s13_closed_cover_4.txt` (`notes/s13-casefree.md`), `#print
axioms` = `[propext, Classical.choice, Quot.sound]`, no `sorry`, no `native_decide`.  At side 4 the
bound is sharp (the 4×4 tiling), so monotone witness leaves provably cannot do it (`search/RUNG2.md`
§2); the tree uses the zero-margin leaf types of the new sibling verifier `ZMTree.lean` (below),
proved sound once (`ZMTree.sound`, in the default build).  The data is **opt-in**: `lake build
Sqpack.S13Lower`, 538 s wall / 33 CPU-min on 4 cores, ≤ 13.2 GB RSS per process.

**Rung 2b, `s(32) = 6` with no hypothesis, done (2026-09-28):** `SquarePacking.s32_ge_6 : (6 : ℝ) ≤
minSide 32`, `SquarePacking.s32_eq_6 : minSide 32 = 6`, and `SquarePacking.s32_checkerCover :
S32CheckerCover` — the one computational hypothesis of `S32.lean` is now a theorem
(`S32Lower.lean`), from `certificates/s32/s32_closed_cover_6.txt` (13,085 points), with the same
`ZMTree` verifier, unchanged, and no new leaf type; the exact mirror rejected none of zeromargin's
leaves.  `#print axioms` = `[propext, Classical.choice, Quot.sound]`.  Opt-in, data gitignored:
`lean/scripts/gen_data.sh S32Z` (~70 min on 4 cores), then `lean/scripts/build_parts.sh S32Z
Sqpack.S32Lower 4 12-15` (3 h 36 min wall / 13.8 CPU-h, ≤ 15.2 GB RSS per process).  Details below.

**`s(k² − 3) = k` for all `k ≥ 6`, conditional on one finite statement (2026-09-29):**
`SquarePacking.Bentz.bentz_of_valid7 : Valid7 → ∀ k : ℕ, 6 ≤ k → minSide (k ^ 2 - 3) = k` (`Bentz.lean`, **default
build**, ~2 min).  `Valid7` = every closed unit square in `[0,7]²` has mass `≥ 1` under the box cover
`search/qx2_data/L4_k02_box7.txt` taken verbatim as a `MixedCover` (800 segments + the Lebesgue square `[9/5, 26/5]²`),
which is exactly what the Python certificate asserts (Lemma Z + `qx2_zm.py` run V3, `search/QUADRANT_EXACT.md`).  The
kernel checks the whole all-k reduction: the family measure `μ_k` for every `k`, `μ₇` = the box file, total mass
`k² − 4D < k² − 3`, and localisation by integer shifts.  `#print axioms` = `[propext, Classical.choice, Quot.sound]`.
Discharging `Valid7` in Lean needs polygon mass in `CovM`, Lemma Z, and Lemma E (`notes/lean-bentz-reduction.md`);
Lemma Z and the D4 reduction are now done (next paragraph but one).

**`s(k² − 4) = k` for all `k ≥ 8`, conditional on one finite statement (2026-10-03):**
`SquarePacking.Bentz4.bentz4_of_valid9 : Valid9 → ∀ k : ℕ, 8 ≤ k → minSide (k ^ 2 - 4) = k` (`Bentz4.lean`, **default
build**, ~35 s).  `Valid9` = every closed unit square in `[0,9]²` has mass `≥ 1` under the box cover
`search/qx2_data/K4_k008_box9.txt` taken verbatim as a `MixedCover` (2076 segments + the Lebesgue square
`[14/5, 31/5]²`), the statement of the Python certificate of record (`qx2_k4x_k008`, VERIFIED-D4).  Same argument as
`k² − 3`, now generic in the edge-zone width `R` (`BentzFam.lean`; `k² − 4` is `R = 3`, box `2R + 3 = 9`, threshold
`2R + 2 = 8`).  `#print axioms` = `[propext, Classical.choice, Quot.sound]`.  Section below and
`notes/lean-k2m4-reduction.md`.

**Only the tilted run's region left (2026-10-03):** `Bentz.bentz_of_validTilt7 : ValidTilt7 → ∀ k ≥ 6, minSide
(k ^ 2 - 3) = k` and `Bentz4.bentz4_of_validTilt9 : ValidTilt9 → ∀ k ≥ 8, minSide (k ^ 2 - 4) = k`
(`ValidSplit{,7,9}.lean`, **default build**, ~45 s).  `ValidTilt` = exactly the pose region `qx2_zm.py`'s box run
certifies (centres in `[0, m/2]²`, `0 < θ ≤ 45°` as `u = tan(θ/2)`, admissible squares); the D4 reduction and Lemma Z
(`θ = 0`, `validAxis7`, `validAxis9`, proved by a kernel check of all corner limits over the whole box) are in Lean.
Section below and `notes/lean-valid-split.md`.

**Lebesgue-square leaf primitives, Lemma U (LEB) and Lemma K (CAP), done (2026-10-03):** `LebMass.leb_sound`,
`LebMass.cap_sound` (`LebMass.lean`, **default build**): leaf tests on a rational pose box, proved sound for `CovT`, a
box predicate on the measure in exactly `ValidTilt`'s pose region; the smoke test `LebMass7.lean` checks **all** 689
LEB and 374 CAP leaves of run V3 in the kernel (`leb7_cov`, `cap7_cov`: `CovT` of each box for `box7Cover.measure`).
`#print axioms` = `[propext, Classical.choice, Quot.sound]`.  Section below and `notes/lean-leb-mass.md`.

## Files

| file | what |
|---|---|
| `Sqpack/BoxTree.lean` | the generic verifier `BoxTree.check` (natural-number arithmetic only), its soundness `BoxTree.sound`, the gluing lemmas `Cov.splitX/Y/U`, the tree decoder `BoxTree.dec`, and the end-to-end `BoxTree.le_minSide` |
| `scripts/gen_boxtree.py` | builds a box tree for a certificate (exact mirror of `check`) and writes the Lean data |
| `Sqpack/S12U/{Pts,Part0..3,Cov}.lean` | generated: the 81 points; 124 chunk theorems; `cov_root` |
| `Sqpack/S12Lower.lean` | `s12_ge_35_9` (hand-written, one `le_minSide` call) |
| `Sqpack/S12W/*`, `Sqpack/S12WLower.lean` | `s(12) ≥ 3920/997` from `certificates/s12_lower_3.931795_sparse.txt` |
| `Sqpack/S11/*`, `Sqpack/S11Lower.lean` | `s(11) ≥ 3040/797` from `certificates/s11_lower_3.8143.txt` (opt-in) |
| `Sqpack/S12H/{Pts,Part0..319,Cov}.lean`, `Sqpack/S12HLower.lean` | generated (gitignored): the 1736 points; 1,235 chunk theorems; `cov_root`.  `s12_ge_15680_3951` from `certificates/s12_lower_3.9686.txt` (opt-in) |
| `Sqpack/ZMTree.lean` | the zero-margin verifier `ZMTree.check` (tree type `ZT`: leaves `Z`, `E`; nodes `X/Y/U`, `XM/YM/UM`, `F`, `C`), its soundness `ZMTree.sound` (for the same `BoxTree.Cov`, so `BoxTree.le_minSide` is reused), the decoder `ZMTree.dec` |
| `scripts/gen_zmtree.py` | zero-margin tree search (`search/zeromargin.py` as a read-only oracle) + exact integer mirror of `ZMTree.check` + leaf pruning + Lean emission |
| `Sqpack/S13/{Pts,Part0..3,Cov}.lean`, `Sqpack/S13Lower.lean` | generated: the 3,621 points (a `PTree` and the literal `ptsL`); 209 chunk theorems; `cov_root`.  `s13_ge_4`, `s13_eq_4` (opt-in) |
| `Sqpack/S32Z/{Pts,Part0..95,Cov}.lean`, `Sqpack/S32Lower.lean` | generated (gitignored): the 13,085 points; 5,990 chunk theorems; `cov_root`.  `s32_ge_6`, `s32_checkerCover` (the hypothesis of `S32.lean`, proved), `s32_eq_6` (opt-in) |
| `Sqpack/BentzData.lean`, `Sqpack/Bentz.lean` | generated data (the box file verbatim + the family table, input sha256s in the header) and `bentz_of_valid7` |
| `scripts/gen_bentz_data.py` | writes `BentzData.lean` from `search/qx2_data/` (deterministic, byte for byte) |
| `Sqpack/BentzFam.lean` | the all-`k` reduction for a fixed-profile family of any edge-zone width `R` (two-layer code tables, box-file check by sorted keys, localisation, accounting, `minSide_eq`) |
| `Sqpack/Bentz4Data.lean`, `Sqpack/Bentz4.lean` | generated data (the `k² − 4` box file verbatim, the two family tables, the entry keys; input sha256s in the header) and `bentz4_of_valid9` |
| `scripts/gen_bentzfam_data.py` | writes `Bentz4Data.lean` from `search/qx2_data/K4_k008_*` (generic in `R`; deterministic, byte for byte) |
| `Sqpack/ValidSplit.lean` | `ValidTilt`, `ValidAxis`, `valid_of_tilt_axis` (the D4 split); grid covers (`gridCover`), their D4 invariance (`d4InvM_gridCover`) and Lemma Z (`validAxis_gridCover`); packed weight tables and the kernel checks `fitOK`, `symOKP`, `axisOKP` |
| `Sqpack/ValidSplitData.lean`, `Sqpack/ValidSplit7.lean`, `Sqpack/ValidSplit9.lean` | generated data (the two box files' weights packed, 48 bits per grid segment; input sha256s in the header) and the instances `validAxis7`, `valid7_of_tilt`, `bentz_of_validTilt7`, `validAxis9`, `valid9_of_tilt`, `bentz4_of_validTilt9` |
| `scripts/gen_validsplit_data.py` | writes `ValidSplitData.lean` from the two box files, with a Python mirror of `symOKP` / `axisOKP` (deterministic) |
| `Sqpack/LebMass.lean` | `CovT` (box predicate on a measure, `ValidTilt`'s region), `PBox`, `whi`; `volume_sq`; Lemma U (`lebOK`, `leb_sound`, `leb_sound_grid`); width lemma (`vol_hsl_le`, `vol_below_le`, `sq_below_le`, `sq_left_le`); segments on the boundary lines (`segMeasure_h/v`, `line_mass_ge`); tangent cap (`cone_BL/TL`, `chordY/X`); Lemma K (`capOK`, `cap_sound`) |
| `Sqpack/LebMass7Data.lean`, `Sqpack/LebMass7.lean` | generated: run V3's LEB / CAP leaf boxes; the kernel checks `leb7_ok`, `cap7_ok` and `leb7_cov`, `cap7_cov` |
| `scripts/gen_lebmass_data.py` | writes `LebMass7Data.lean` from the V3 leaf dump, with an exact mirror of `lebOK` / `capOK` (deterministic) |
| `scripts/build_parts.sh` | builds a data set's part files a few at a time (plain `lake build` starts them all at once) |

Regenerate: `python3 lean/scripts/gen_boxtree.py certificates/s12_uniform_7of81_3.888.txt --n 12
--name S12U --outdir lean/Sqpack/S12U` (25 s; deterministic).  The others:
`… s12_lower_3.931795_sparse.txt --n 12 --name S12W --outdir lean/Sqpack/S12W` (60 s) and
`… s11_lower_3.8143.txt --n 11 --look 0 --parts 24 --name S11 --outdir lean/Sqpack/S11` (4 min) and
`… s12_lower_3.9686.txt --n 12 --look 0 --parts 320 --balance digits --name S12H --outdir
lean/Sqpack/S12H` (39 min; `gen_data.sh S12H`).
Rung 2: `python3 lean/scripts/gen_zmtree.py certificates/rung2/s13_closed_cover_4.txt --n 13
--name S13 --outdir lean/Sqpack/S13 --nproc 4` (156 s wall / 580 s CPU on 4 cores; deterministic —
a fresh run reproduces the files byte for byte; gitignored, `lean/scripts/gen_data.sh S13`).
Rung 2b: `python3 lean/scripts/gen_zmtree.py certificates/s32/s32_closed_cover_6.txt --n 32 --name
S32Z --outdir lean/Sqpack/S32Z --nproc 4 --parts 96` (~70 min wall on 4 cores; `gen_data.sh S32Z`),
then `lean/scripts/build_parts.sh S32Z Sqpack.S32Lower 4 12-15` (not a plain `lake build`, below).
Large data sets (`S11`, `S13`, `S32Z`, `S12H` today, all future big ones) are **gitignored**: run `lean/scripts/gen_data.sh` before
`lake build Sqpack.S11Lower`.  Small ones (`S12U`, `S12W`) stay committed; both regenerate byte-identically.

## What is proved, and how

`BoxTree.le_minSide`: let `pts` be entries `(X, Y, w)` (point `(X/D, Y/D)`, weight `w/W`) with

* no repeated entry (`PTree.chainB`, kernel), invariant under `x ↦ Mq − x` and `x ↔ y`
  (`d4Check`, kernel), total `Σw < n·W` (kernel);
* `Cov … root`: every closed unit square inside `[0, Mq/D]²` with centre in `[0, Mq/(2D)]²` and
  angle `θ = 2 arctan u`, `u ∈ [0, 29/70]` (`29/70 > tan 22.5°`), contains entries of weight `≥ W`.

Then `Mq/D ≤ minSide n`.  The D4 reduction (`D4.lean`: `d4_reduction`), the cover-to-packing
argument (`S32.lean`: `not_packs_of_cover`, `packs_grid`, `Packs`, `minSide`) and the aggregation
of entries (`Cover.lean`: `coverA`, `coverW`, `D4Inv_cover`, `sum_filter_coverA`) are reused
unchanged.

`Cov` is established by `BoxTree.sound`: `check … t box c = true → Cov … box` for every tree `t`.
A tree splits the pose box `[x0,x1]×[y0,y1]×[u0,u1]` (centre over `Q = D·S`, `u` over `R`) at
midpoints (`X`, `Y`, `U` nodes), prunes the candidate list (`F` nodes: `near`, a pure speed
device), and ends in leaves `L sel`.  A leaf is accepted iff `u1 ≤ R` and

1. **walls**: `WL = ⌊Q(R² + 2U0R − U1²) / (2(R² + U1²))⌋` is a lower bound for `w(θ)/2 = (|cos θ| +
   |sin θ|)/2` on the bin (`wlo_le`; `w = (1 − u² + 2u)/(1 + u²)` by `wid_two_arctan`); the
   admissible centres of the box lie in the clipped rectangle `[max(x0,WL), min(x1, M−WL)] × …`
   (`sq_subset_box_iff`).  If it is empty the leaf holds vacuously;
2. **containment**: otherwise the selected candidates (`sel` = gaps into the candidate list) must
   each pass `ptOk` and weigh `≥ W` (`capSel`).  `ptOk` certifies `p ∈ sq c θ 1` for every
   admissible pose of the box: `p ∈ sq c (2 arctan u) 1 ⟺ G_k ≤ 0, k = 0..3`
   (`mem_sq_iff_gval`); `G_k` is affine in the centre with signs fixed on `u ∈ [0,1]`, so the
   worst centre is a corner of the clipped rectangle (Lemma A); and quadratic in `u`, so on
   `[U0, U1]` it is bounded by its Bernstein coefficients `G(U0)`, `G(U1)`, `G(U0,U1)` (polar
   form) — `lin3`, from the identity
   `(U1−U0)² G(v) = (U1−v)² G(U0) + 2(v−U0)(U1−v) G(U0,U1) + (v−U0)² G(U1)`.
   The 3 × 4 tests are linear in the point with all negative terms moved across (`triOk`), so
   everything is `Nat.add/mul/ble` — kernel-GMP operations, no `Int`, no `ℚ`.

**Trigonometry** is handled by the tan-half-angle parametrisation: `cos θ = (1−u²)/(1+u²)`,
`sin θ = 2u/(1+u²)` exactly, so no trig bounds, no approximation of `π`, and every test is a
polynomial inequality in rational `u`.  The only real-analytic facts used are `cos/sin (2 arctan
u)` (`ZeroMargin.lean`) and `θ ∈ [0, π/4] ⇒ tan(θ/2) ≤ 29/70` (`exists_u_of_theta'`).

**Nothing about the tree is trusted.**  `sound` holds for every tree, so the generator, the
chunking and the decoder `dec` (a tree ships as one hex numeral, a base-`B` digit stream) need no
proofs; a wrong tree only makes `decide` fail.  The certified statement is `Cov` of the root box,
glued from the chunk theorems by `Cov.splitX/Y/U` (a proof term the generator writes out).

## Engineering notes (what it took to make the kernel fast enough)

* **`Nat` only.**  The first version used `ℤ` with `decide (a ≤ b)`: 40 leaves/s and 25 GB.
  Rewriting every test as `Nat.ble (Σ positive terms) (Σ negative terms)` gave ~12×.
* **One declaration per chunk** (≤ 600 leaves).  The kernel's whnf cache lives per declaration;
  one 33k-leaf `decide` needed 32 GB and 167 s, the same tree in 144 declarations 7 GB.  Chunks
  are also the unit of parallelism: the generator splits them over `--parts` files that `lake`
  builds concurrently.
* **Leaves carry their selection.**  Testing every candidate at every leaf (and pruning the
  candidate list at every node) cost ~2×; now a leaf names its ≥ 7 points and only those are
  tested, and pruning happens only where it shrinks the list by ≥ 15 %.
* **Trees as numerals.**  Elaborating a 600-leaf nested constructor term cost about as much as
  its kernel check (~1 ms/leaf, mostly `OfNat` numerals in the leaf lists); one hex numeral per
  chunk, decoded in the kernel, costs ~13 % of the kernel time instead.
* Hand-writing the recursion with `BT.rec` instead of structural recursion: < 5 %, not kept.
  Pre-scaling the points (dropping `X·S`): 3 %, not kept.

## Measurements (2026-09-27, 16-core machine, pinned to physical cores 12–15)

Timings are CPU time on one core unless stated; "kernel" is the `decide +kernel` time, measured
as the difference against the same file with the decisions replaced by an axiom.  RSS includes
~6.6 GB for importing Mathlib.

| certificate | points | tree leaves (splits) | depth | points claimed / leaf | kernel throughput | build |
|---|---|---|---|---|---|---|
| `s12_uniform_7of81` (35/9) | 81, uniform | 29,529 (29,528) | 34 | 7 | **430 leaves/s** (7,594 leaves: 17.6 s) | clean `lake build` 41 s wall / 99 s CPU on 4 cores; 8.2 GB RSS per file |
| `s12_lower_3.931795_sparse` | 224, weighted | 25,127 (25,126) | 35 | ~21 | 170 leaves/s (6,459 leaves: 38 s) | 96 s wall / 251 s CPU on 4 cores; 10 GB RSS |
| `s11_lower_3.8143` | 680, weighted | 89,689 (89,688) | 37 | ~85 | 47 leaves/s (11,412 leaves: 240 s) | 26 min wall / 64 min CPU on 3 cores (oversubscribed); 17.6 GB RSS for an 11k-leaf file |
| **`s12_lower_3.9686`** (15680/3951) | 1736, weighted | 328,275 (328,274) | 39 | ~184 | **12.5 leaves/s** (whole build, CPU) | **6 h 31 min wall / 7.3 CPU-h** on 2 cores, one part at a time; 320 files; ≤ 30.6 GB RSS per file |

Tree generation (Python, one core): 25 s, 60 s, 3.5 min, 24 min (+ 15 min emission).

**The 1736-point run (2026-09-28, cores 14–15).**  The tree is exactly the predicted one (328,275
leaves, depth 39, 525 candidates per leaf on average); 1,235 chunks, 2,032 `F` nodes, 61.2 M
base-B digits (~184 claimed points per leaf).  The kernel cost came in at ~2× the model's estimate
(≈ 80 ms CPU per leaf against 1.0 + 0.23 × 184 ≈ 43 ms), and **memory, not time, set the layout**:
at 96 leaf-balanced files the parts covering the dense centre of the certificate (twice the digits
of the others) peaked at 47.6 GB and took 6–7 min, the others ~20 GB and 2.5–3.5 min.  Memory grows
through a file (per-declaration kernel work is not released), roughly with its digit count, so the
generator now has `--balance digits` (parts balanced by digit count; the default `leaves` keeps the
older data sets byte-identical — `S12W` was re-emitted and is unchanged).  At 320 digit-balanced
files: 26–181 s per part, peak 30.6 GB (`Part103`, the largest file, 0.63 MB),
most ≤ 15 GB; Lean ran ~1.1 cores per part process, so one part at a time on 2 cores costs little
against two (which would exceed a 35 GB budget when two heavy parts coincide).  `Pts` 7 s, `Cov`
6 s, `S12HLower` 4 s.  Elaboration of the data is now
negligible (one numeral per chunk); the kernel is > 85 % of a data file's build time.

**What dominates.**  The kernel does roughly 10⁶ `Nat` operations per second (GMP-backed; the
numbers here are 60–110 bits: `Q ≈ 3·10⁷`, `R ≈ 7·10⁷`, products of three or four of them).  Rational
sizes are not the issue (everything is scaled to integers once; no gcds, no `ℚ`), and there are no
trigonometric bounds at all (tan-half-angle, see above).  A leaf costs about

  `1.0 ms` (decode, walls, clipping, tree traversal) `+ 0.23 ms × (points claimed)`

— a claimed point is 3 Bernstein coefficients × 4 violation polynomials = 12 linear tests.  This
fits all three rows (2.6, 5.8, 20.6 ms predicted vs 2.3, 5.9, 21 ms measured).  So cost scales with
*leaves × points per leaf*, and points per leaf is `1 / (typical weight)`: uniform certificates
are cheap, dense weighted covers expensive.  Memory grows with the file (the 24-file split of
S11 kept each process under ~12 GB); keep ≲ 5k leaves of dense certificates per file.

**Extrapolation to the zero-margin rungs** (made before rung 2, with `BoxTree`'s leaf test; superseded
by the measurements in the rung-2 section below — s(13) took 33 CPU-min with the zero-margin leaves):

| target | boxes | points per leaf (≈ 1/avg weight) | est. kernel CPU | on 4 cores |
|---|---|---|---|---|
| s(13) = 4, 3621-point cover, avg weight 0.0036 | 16,872 | ~280 | 16,872 × 65 ms ≈ 18 min | ~5 min |
| s(32) = 6, 13,085 points, avg 0.0024 | 164k | ~410 | 164k × 95 ms ≈ 4.3 h | ~1.1 h |
| s(21) = 5, 7,536 points + 1,872 segments | 10⁵–10⁶ | ~250 + segment terms | 2–20 h | 0.5–5 h |

These are feasible, but the per-leaf point count is the lever: a leaf only needs *some* certified
subset of weight ≥ 1, and claiming the heaviest points first (as the generator now does) helps
little on these covers (6 % fewer digits on S12W).  Bigger wins, in order: (1) aggregate points
into clusters that a leaf can claim as one unit (a precomputed "sub-cover" whose points all lie in
a small disc: one containment test per cluster via the disc's bounding box); (2) a Mathlib-free
data layer, so each chunk file imports only the `Nat` checker (import time and the 6.6 GB baseline
disappear; soundness stays in the Mathlib file); (3) larger `F` pruning thresholds for dense
certificates (the candidate walk is ~5 % now).

## Rung 2: zero-margin leaves (`ZMTree.lean`), `s(13) = 4`

**Why new leaves.**  `BoxTree`'s only leaf is a *monotone witness set* (points in every admissible
square of the box).  At a sharp container side that is provably insufficient: any finite closed
subdivision certified that way forces total weight `≥ m²` (`search/RUNG2.md` §2, Theorem 2).  So
`ZMTree` adds the leaf types of `search/zeromargin.py`, each an exact integer test with its own
soundness lemma (reusing `ZeroMargin.lean`: `mem_sq_iff_gval`, `gval_eq`, `le_maxQuad`,
`condPoly_eq_gval`, `qeval4_le_maxBern`, `xnR_spec`/`xnW_spec`, `widU`), and states its result as the
same `BoxTree.Cov`, so the final step (`le_minSide`, D4, cover ⇒ packing) is unchanged.

| node / leaf | what the kernel checks | soundness |
|---|---|---|
| `E` | `c₁ < w(θ)/2` (in `x` or `y`) at both ends of the bin (`wgt`); `w` is quasi-concave on `u ≥ 0` | `E_cov` (`widU_ge_min`) |
| `C us` (`clip_bin`) | `w(us)/2 ≥ min(x₁,y₁)/Q` and `(R+us)(R+U₁) < 2R²` (`w` increasing on `[us,U₁]`): poses with `u > us` are inadmissible; child box `[U₀, us]` (often the degenerate bin `us = U₀`) | `C_cov` |
| `Z` | claimed entries (gaps into the candidate list), each with a tag; chains A, B of pivots `(X, Y, kind)`; an emptiness staircase | `Z_cov` |
| `X/Y/U`, `XM/YM/UM`, `F` | midpoint splits, splits at an explicit coordinate (the non-dyadic `1/10` root grid), candidate pruning | `Cov.split*` |

**Inside a `Z` leaf** (signed integers are pairs of naturals `(p, n)`; every test is `Nat.ble`):

* `ADM` (Lemma A with the walls, `_adm_cond_ok_int`): condition `k` of a point at its own centre
  corner, the lower centre bound being the box side (`'R'`: exact quadratic maximum `qOk`, i.e.
  `maxQuad`) or the wall `w(θ)/2` (`'W'`: a quartic `cpoly` = `Q R⁴ condPoly`, degree-4 Bernstein
  `bOk`).  An entry with tag `4` has all four conditions by `ADM` — the witness set `T`.
* `CHAIN` (Lemmas E–H): `pairOk l p q` = `λ_a G_p + λ_b G_q ≤ 0` on the whole box (four corners,
  exact quadratic maximum), `(λ_a, λ_b) = (1,−1)` (chain comparison / down reason), `(1,1), (2,1),
  (1,2)` (up reason, empty product region).  A chain's consecutive pivots are checked monotone; at
  any pose the pivots then cut the box into regions `r = 0..k` (`regions`).  An entry with swing kind
  `kp < 4` has the other three conditions by `ADM` and condition `kp` from a *down* reason
  `G_p ≤ G_{q_d}` (counts in regions `r ≥ d`) and/or an *up* reason (counts in `r < u`), in chain
  A and/or chain B.  Regions `(r, s)` of the product with `r < ka`, `s < e_r` are certified empty by
  `pairOk` between `A_{r+1}` and `B_{e_r}`; every other region must reach `W`.  One chain is the
  special case `kb = 0`, pure `ADM` the case `ka = kb = 0`.

The generator uses `zeromargin.py` (read-only) as the oracle for which leaf and which witnesses,
recomputing `T` without `P1` and without inherited points (the Lean leaf has neither), and checks
every leaf with an exact integer mirror of `ZMTree.check`; on s(13) the mirror accepts every leaf
zeromargin proposes, so the Lean tree is essentially zeromargin's own D4 tree (8,434 boxes against
its 8,452; `ADM` 1,416 and `EMPTY` 1,738 identical, `CHAIN` 2,663 against 2,672 — the clip value is
rounded to the `2⁻³²` grid).  It then prunes each chain leaf: pivots are dropped greedily while all regions still reach `W` (reasons remapped by
transitivity, `λ` unchanged), then unneeded entries and reasons.  That takes the chains from 94
pivots (one chain) / 76 × 65 (product) on average to about 3 / 3 × 5, and the claimed entries from
2.23 M to 1.33 M.

**The s(13) tree.**  400 root cells (`1/10` pitch, D4 region `[0,2]²`) × 8 `u`-bins of `[0, ½]`;
10,024 search boxes, max depth 13.  Leaves: **`E` 1,738; `Z` 4,079 = `ADM` only 1,416 + one chain
1,133 + two chains 1,530**; 1,590 `C` nodes, 2,617 midpoint splits in the cells, 374 `F` nodes.
Claimed entries 1,325,532 (1,122,165 `ADM` witnesses, 203,367 chain entries, 16,717 pivots), 325 per
`Z` leaf; 1.80 M base-2²⁰ digits in 209 chunks, 4 files.  Scale `Q = 1000·4096`, `R = 2³²`.

**Kernel cost** (cores 12–15): `lake build Sqpack.S13Lower` **538 s wall, 1,995 s CPU**, the four
part files 491–505 s each in parallel, **13.2 GB max RSS** per process (6.6 GB of it the Mathlib
import); `Pts` 23 s, `Cov` 3 s.  The kernel is ~98 % of a part file (elaboration alone: 7.8 s).
That is ~0.47 s CPU per `Z` leaf, or ~1.4 ms per claimed entry.
Measured on the heaviest chunk (32 `Z` leaves, 8,914 `ADM` entries, 825 chain entries): an `ADM`
entry costs ~0.5 ms (0.2 ms of it the test itself), a chain entry ~2.5 ms, the region count ~1.5 s
per chunk.  What it took (same chunk, 27.4 s → 7.6 s kernel):

* **Fast paths** that imply the exact tests, so every verdict is the exact one: `ADM` first by
  `ptOkK` (`BoxTree.ptOk` with one kind skipped: 12 linear tests on shared products; 0.2 ms against
  0.45 ms for four `qOk`), pair tests first by degree-2 Bernstein on per-box triples (`cornFast`),
  and a *single* corner when the combination does not depend on the centre (`cfree`: `G_p − G_q`
  of equal kinds, `G_p + G_q` of opposite kinds — most down/up reasons).
* **One numeral per `Z` leaf** instead of one per chunk: digit extraction from a 300-kbit numeral
  cost 85 µs per digit (2.1 s per chunk); now negligible.
* **The point list as a literal** (`ptsL`, `pts_toList : pts.toList = ptsL` proved once):
  evaluating `pts.toList` cost 0.75 s in *every* chunk declaration.
* The `ADM` weight is summed once per leaf; regions iterate the chain entries only.
* `lake` builds files concurrently only with `LEAN_NUM_THREADS > 1` (with `=1` it serialised the
  four parts).

**Extrapolation** (per-`Z`-leaf cost × leaf count × entries per leaf ∝ 1/average weight):

| target | `Z` leaves (zeromargin D4 census) | entries/leaf vs s(13) | est. kernel CPU | on 4 cores |
|---|---|---|---|---|
| s(13) = 4 (measured) | 4,079 (ADM 1,416, CHAIN 2,663) | 1 | 33 min | 9 min |
| s(32) = 6, 13,085 points | 82,208 (ADM 12,201, CHAIN 70,007) | ~1.5 | ~17 h | ~4–5 h (16 files) |
| **s(32) = 6 (measured, rung 2b)** | 89,473 in the Lean tree (ADM 16,747, CHAIN 72,726) | 1.6 | **13.8 h** | **3.6 h** (96 files, 4 at a time) |
| s(21) = 5, 7,536 points + 1,872 segments | — | — | needs segment entries (below) | — |

s(32) needs no new leaf type (same `ZMTree`, `m = 6`, root grid `[0,3]²` by `XM/YM` at pitch
`1/10`), only the generator run (zeromargin's own D4 sweep was 2.8 CPU-h; with the mirror and the
pruning expect ~3×) and the build; the remaining levers are the per-entry overhead in context
(0.5 ms against 0.2 ms for the bare test) and a Mathlib-free data layer.  (Done since: rung 2b
below — the mirror accepted every zeromargin leaf on s(32) too.)  s(21)
additionally needs segment entries (`MixedMeasure.lean`) in `Cov` and in the `Z` count.

## Rung 2b: `s(32) = 6` with no hypothesis (`S32Lower.lean`)

**What is proved.**  `SquarePacking.s32_ge_6 : (6 : ℝ) ≤ minSide 32` (by `le_minSide`, exactly as
`s13_ge_4`), `SquarePacking.s32_checkerCover : S32CheckerCover` — the one computational hypothesis of
`S32.lean` is now a theorem — and `SquarePacking.s32_eq_6 : minSide 32 = 6` (=
`s32_eq_six_of_checker s32_checkerCover`, so `S32.lean`'s own chain from the hypothesis is reused
unchanged).  The bridge is `S32CheckerCover.of_cov` (20 lines: `Cov` of the root box for
`S32Data.tree.toList` is literally `S32CheckerCover` after unfolding `pt = ptR 1000` and scaling
the weights by `10¹¹`) plus `s32_tree_toList : S32Data.tree.toList = ptsL` (kernel), i.e. the
generator's point list is the committed transcription of the certificate, entry for entry.
`#print axioms` for all three: `[propext, Classical.choice, Quot.sound]`; no `sorry`, no
`native_decide`.  `S32.lean` is untouched and still in the default build.  Same `ZMTree`, no new leaf type, nothing changed in
the verifier.

**Mirror rejections: none.**  As on s(13), every leaf zeromargin's logic proposes (with `T` recomputed
without `P1` and without inherited points) passes the exact mirror of `ZMTree.check` (`zm_only = 0`
over all 900 cells), and every leaf is re-checked by the mirror again at emission.

**The s(32) tree.**  900 root cells (`1/10` pitch, D4 region `[0,3]²`) × 8 `u`-bins of `[0, ½]`;
186,888 search boxes, max depth 20 (zeromargin's own run needed depth 27 at the wall germ
`[1.5,1.6]×[0.5,0.6]`; here that cell closes at depth 18 — the mirror-side chain search and
clipping differ in detail).  Leaves: **`E` 5,127; `Z` 89,473 = `ADM` only 16,747 + one chain
25,152 + two chains 47,574** (zeromargin: `ADM` 12,201, `CHAIN` 70,007, `EMPTY` 3,457); 4,876 `C`
nodes, 87,400 midpoint splits, 8,005 `F` nodes.  Claimed entries 47.1 M (43.8 M `ADM` witnesses,
3.32 M chain entries, 358 k pivots), **526 per `Z` leaf** (s(13): 325); 55.1 M base-2²⁰ digits in
5,990 chunks, 96 files (267 MB of Lean, gitignored).  Scale `Q = 1000·4096`, `R = 2³²`, as for s(13).

**Generation.**  3,992 s wall on 4 cores (cores 12–15; 15,440 s CPU in the workers, 1.55× zeromargin's
own 9,958 s), plus 5 min emission.  (The search ran the generator's own per-cell worker from a
checkpointing wrapper, then `gen_zmtree.py --load`; the one-shot `lean/scripts/gen_data.sh S32Z`
command runs the same code but was not itself timed end to end.)  Deterministic: four cells
re-searched in a fresh process gave identical trees, and a second emission is byte-identical.

**Kernel cost** (cores 12–15, 4 part files at a time): the 96 part files **49,766 s CPU = 13.8
CPU-h** (499–549 s each, 502–582 s wall), **3 h 33 min wall**; `Pts` 144 s (the 13k-entry literal
and `pts_toList`), `Cov` 21 s, `S32Lower` 9 s.  **Peak RSS 13.7–15.2 GB per part process** (6.6 GB
of it Mathlib), ≤ ~55 GB for the four together.  That is **0.56 s CPU per `Z` leaf, 1.06 ms per
claimed entry** (s(13): 0.47 s, 1.4 ms) — the estimate before the run was ~17 CPU-h.

**Build note.**  `lake build` starts every ready module at once — one job per hardware thread,
ignoring `taskset` — so a plain `lake build Sqpack.S32Lower` started 32 part files together
(8 GB each within minutes, heading for 14 GB; killed at 94 GB used).  `lean/scripts/build_parts.sh
S32Z Sqpack.S32Lower 4 12-15` builds the parts 4 at a time (one `lake build` per part via `xargs
-P`), then the top.  The 13,085-entry `ptsL` literal also needs `maxRecDepth`/`maxHeartbeats`
raised in `Pts.lean` (the generator now emits them; `pts_toList`'s kernel list comparison recurses
13k deep).

## Segments (`s(21) = 5`, `s(45) = 7`) — batch 1 done (2026-09-28): S, T, L, P in the kernel

Details, statement ↔ code, and the zm_mixed.py audit: `notes/lean-segments.md`.  Done, in the
default build, all `#print axioms` = `[propext, Classical.choice, Quot.sound]`:

* `CovM.lean` — `CovM` (mixed mass), `CovM.split*`, `segD4Check`, **`le_minSide_mixed`**.
* `SegParts.lean` — parts of segments ≤ segment mass (`parts_le_segMass`); Lemma T in pair form
  (`pair_capture`, from `G_up(t) + G_down(t′) = 4u(t′ − t − u)`).
* `ZMTreeM.lean` — S-blocks (Lemma S: `admAll` at the two ends + convexity) and T-groups (a monotone
  coupling of the two germ lines' masses: the dual of Corollary T's `min_T f(T)`), `pc_sound`.
* `LemmaL.lean`, `LBlock.lean`, `LBlockSound.lean` — L-blocks (Lemma L, general ends, Corollary L at
  the four box corners, all corner inequalities quartic ⇒ `ZMTree.bOk`), **`lblk_sound`**.
* `ZMTreeX.lean` — the mixed tree `ZTM` (a `ZMTree` point leaf with target `W − Lp`: Lemma P),
  `checkM`, **`soundM`**, decoder `decM`.  `ZMTree.lean` is untouched.
* Toys: `s3_ge_2` (pure segments, 178 leaves, 97 with L-blocks), `s3_ge_2_mixed` (points + segments,
  222 `ADM` point leaves with a piece phantom); opt-in `s16_ge_4` (T1 grid cover, 9,451 leaves).
* Generator `scripts/gen_zmmtree.py` (+ `scripts/lblock.py`, `scripts/mk_toys.py`): zm_mixed.py as
  oracle, exact mirror; M2 and the T1 germ cell (S+T) reproduce zm_mixed's census exactly.

Not done: Lemma L′/V, SPLIT (Lemma R), wall corners in Corollary L (the last two need a general-degree
Bernstein lemma).  Kernel cost per `Z` leaf: S 23 ms, T 27 ms, L 125 ms (≈ 40 ms per line).

### The original scope (for reference)

Both covers put most of their mass uniformly on grid-line segments (s(21): 7,536 points + 1,872
segments; s(45): 19,989 points + 3,912 segments, 32.8 of the 44.77 on lines), and their certificates
are `zm_mixed.py` runs (`search/ZM_MIXED.md`).  What exists in Lean: the measure-level reduction
(`MixedMeasure.lean`: `not_packs_of_measure`, `d4_reduction_measure_u`, `MixedCover.measure_apply`
giving the mass of a square as points inside + each segment's weight × the fraction of its
parameter interval inside), and `S21.lean` with its one hypothesis `S21CheckerCover` (no s(45) file
yet).  What a hypothesis-free rung needs:

1. **`CovM`** — `Cov` with the mixed mass (point sum + Σ segment weight × inside fraction), its
   `splitX/Y/U` gluing and an end-to-end `le_minSide_mixed` via `not_packs_of_measure` and
   `d4_reduction_measure_u` (≈ 150 lines, mechanical; plus a `SegTree` data layer like `PTree`).
2. **Segment terms in the `Z` leaf**, each an exact integer test with its own soundness lemma —
   this is the real work.  `zm_mixed.py`'s leaves are `PIECE` (piece mass alone ≥ 1) and zeromargin's
   `ADM`/`CHAIN` with a *phantom point* of weight `L` (Lemma P), where `L` comes from
   * **Lemma S** (certified core of a line): the Bernstein coefficients are affine in the point, so
     on a line they cut an interval with rational ends; nearest to what `ZMTree` already proves
     (`ADM` for every point of a segment at once).  Straightforward: ≈ 300–500 lines.
   * **Lemma T** (threshold lemma for a germ pair of lines one unit apart) and **Lemma L / L′**
     (linear chord ends on an axis line, hull form) — piecewise-linear lower bounds on the chord
     length as the pose varies; genuinely new real analysis (chord of a tilted unit square on a
     line, monotonicity in the pose), plus the rational-function bounds `rf_bound`.  In the s(21)
     census Lemma L raises `L` at 173 k of the leaves and T at 59 k, so neither can be skipped.
   * **Lemma R / `SPLIT`** (region-wise coupling of pieces and points, 54 k leaves in each run).
   Estimate: 1.5–3 k lines of Lean for the soundness side, several days; the generator is the
   analogue of `gen_zmtree.py` with `zm_mixed.py` as oracle and an exact mirror.
3. **Kernel cost.**  `zm_mixed.py`'s D4 censuses: s(21) 461 k boxes, leaves `PIECE` 9 k, `ADM` 146 k,
   `CHAIN` 23.5 k, `SPLIT` 54 k, `EMPTY` 18 k (46 k CPU-s in Python); s(45) 438 k boxes, `PIECE` 9.5 k,
   `ADM` 123 k, `CHAIN` 46 k, `SPLIT` 54 k, `EMPTY` 25 k (59 k CPU-s).  So ~2.5× s(32)'s leaf count,
   but the lines carry most of the mass, so a leaf claims far fewer points (the phantom `L` covers
   the rest): at s(32)'s measured 0.56 s per `Z` leaf, **~40 CPU-h each (≈ 10 h on 4 cores)** is a
   conservative upper estimate; with ~100–200 claimed points per leaf and a few dozen segment tests,
   more likely **15–25 CPU-h** each.  Memory per part file as for s(32) (split into ~200 parts).

## Common specification (`Spec.lean`, `SpecBridge.lean`, `SpecHeadline.lean`)

`Sqpack/Spec.lean` (namespace `UnitSquarePacking`, imports only Mathlib, ~100 lines) is a short
statement of the problem meant to be shared with other projects: `rot θ` (explicit, since `ℝ × ℝ`
has the sup metric), `unitSq c θ` = image of `[-1/2,1/2]²` under `p ↦ c + rot θ p`, `container s =
Icc 0 s ×ˢ Icc 0 s`, `Packs n s` (closed squares inside, `Pairwise` disjoint `interior`s), `minSide n =
sInf {s | Packs n s}`; canonical result shapes: exact `IsLeast {s | Packs n s} k`, lower `∀ s, Packs n
s → a ≤ s`, upper `Packs n b`.  Proved there: `unitSq_eq_setOf`, `interior_unitSq`.

`SpecBridge.lean` (default build): `sq_one_eq`, `sqInt_one_eq`, `box_eq`, hence `packs_iff :
SquarePacking.Packs n s ↔ UnitSquarePacking.Packs n s` and `minSide_eq`; `lower_of_le_minSide` /
`isLeast_of_le_minSide` (`n ≥ 1`, via `csInf_le`); restated: `s12_lower_3920_997`,
`s32_isLeast_of_checker`.  `SpecHeadline.lean` (opt-in: needs the `S11`, `S12H`, `S13` data):
`s13 : IsLeast {s | Packs 13 s} 4`, `s12_lower` (`15680/3951`), `s11_lower` (`3040/797`), and in a
comment the `s(32)` one-liner (data `S32Z`).  All print the three standard axioms.  Attainment
(`isLeast_minSide`, `Sqpack/Attain.lean`) transfers through `packs_iff`/`minSide_eq` unchanged.

Bridge to google-deepmind/formal-conjectures (`FormalConjectures/Wikipedia/SquarePacking.lean`):
their `Square`, `UnitSquare`, `Packing` are copied verbatim (Apache-2.0, attributed, namespace
`FCSquarePacking`) into `Sqpack/FCSquarePacking.lean`; `Sqpack/SpecFC.lean` proves
`packs_iff_nonempty_packing : Packs n x ↔ Nonempty (Packing n UnitSquare (Square x))` for all `n`,
`x` (open squares placed by isometries of `EuclideanSpace ℝ (Fin 2)` in the open box), hence
`setOf_packs_eq`, and `SpecHeadline.lean` has `s13_fc : IsLeast {x | Nonempty (Packing 13 UnitSquare
(Square x))} 4`, their `least_…` shape.  Ingredients: Mazur–Ulam (`toRealLinearIsometryEquiv`);
the image of the standard basis is orthonormal, so `u = (cos φ, sin φ)`, `v = ε(-sin φ, cos φ)`,
`ε = ±1` (`exists_frame`); either way `(0,1)²` maps onto the interior of a unit square
(`frame_image`); closure/interior between the open and closed formulations.

Bridge to chelokot/square-packing-archive (commit `753079e`, `formal/SquarePackingArchive/
Geometry.lean`; records such as `s6_eq_three : IsMinimumSide 6 3` in `Records/Square6Exact.lean`):
`Sqpack/SpecChelokot.lean` (default build, namespace `UnitSquarePacking.Chelokot`) restates their
`Point`/`Frame` (`(cos, sin)` with `cos² + sin² = 1`)/`PlacedSquare`/`Packing`/`HasPacking`/
`IsLowerBound`/`IsMinimumSide` in our own code (checked against their source by reading; nothing
imported, copied, or run) and proves `hasPacking_iff : HasPacking n s ↔ Packs n s ∧ 0 ≤ s`,
`hasPacking_iff_packs` (`n ≥ 1`), `isLowerBound_iff`, `isMinimumSide_iff_isLeast`, and
`isMinimumSide_iff_minSide_eq (hn : 1 ≤ n) : IsMinimumSide n s ↔ minSide n = s`.  So, as a remark,
their `s6_eq_three` gives `minSide 6 = 3` (likewise `s10_eq_goebel`, `s13_eq_four`, `s22_eq_five`,
`s33_eq_six`).  Only mismatch: their `Packing` requires `0 ≤ side`; irrelevant for `n ≥ 1`, but at
`n = 0` their `IsMinimumSide 0 0` holds while `{s | Packs 0 s} = univ` (`isMinimumSide_zero`).
Closed squares, closed box, interior-disjointness and the counterclockwise angle convention match.

## Attainment: `s(n)` is a minimum (`Attain.lean`, default build, 2026-10-01)

`minSide n` is defined as `sInf {s | Packs n s}`; `Attain.lean` proves the infimum is attained:

* **`isLeast_minSide (hn : 1 ≤ n) : IsLeast {s | Packs n s} (minSide n)`**, i.e. `packs_minSide :
  Packs n (minSide n)`;
* `packs_mono : Packs n s → s ≤ t → Packs n t`, `packs_nonempty n : Packs n n` (grid),
  `one_le_of_packs (hn : 1 ≤ n) : Packs n s → 1 ≤ s`, `bddBelow_packs`, `minSide_le`;
* `le_minSide_iff (hn) : a ≤ minSide n ↔ ∀ s, Packs n s → a ≤ s`,
  `packs_iff_minSide_le (hn) : Packs n s ↔ minSide n ≤ s`,
  `minSide_eq_iff_isLeast (hn) : minSide n = k ↔ IsLeast {s | Packs n s} k`.

Proof: a sequence of sides `s_m ↓ minSide n` with packings; angles reduced into `[0, 2π)` by
`toIcoMod` (the squares only see `cos θ`, `sin θ`), centres in `box s_0`, so the parameters lie in a
compact product and a subsequence converges (`IsCompact.tendsto_subseq`).  Containment passes to the
limit through the parametrisation `sqPt c θ a b` of the closed square and the closed set
`{(q, t) | q ∈ box t}`; disjoint interiors pass to the limit because `{(c, θ) | p ∈ sqInt c θ 1}` is
open.  ~190 lines, ~4 s to check.  Exports: `s3_eq_2`, `s3_isLeast` (`S3Lower.lean`, default build) and
`s13_isLeast` (`S13Lower.lean`, opt-in).  `#print axioms` = `[propext, Classical.choice, Quot.sound]`.

## Averaging: D4 symmetry is free (`Average.lean`, default build, 2026-10-02)

`search/FRIEDMAN.md` §9.1.1.  For any measure on the plane:

* `CoverValid C μ` (every closed unit square `⊆ C` has measure `≥ 1`), `SqGood C g` (`g` pulls closed unit
  squares of `C` back to closed unit squares of `C`; closed under `∘`), `avgMap g μ = |ι|⁻¹ • Σᵢ μ.map (g i)`;
* **`coverValid_avg`**: averaging a valid cover over finitely many square-good maps keeps it valid;
  `avgMap_apply_of_preimage`: same mass on `C` if every `g i` preserves `C`; `avgMap_preimage_eq`: invariance
  under `h` when `h ∘ g i = g (σ i)` for a permutation `σ`;
* `d4map m : Fin 8 → …`, the eight words in `reflX m`, `swapXY`, with `reflX_comp_d4map`, `swapXY_comp_d4map`
  (left multiplication as explicit involutions of `Fin 8`);
* **`exists_d4InvM_cover`**: every valid cover measure of `box m` has a D4-invariant (`D4InvM m`) valid cover
  measure of the same total mass.  So D4-invariant certificates lose nothing, and `d4_reduction_measure`
  applies to the average.

~200 lines, ~4 s to check.  `#print axioms` = `[propext, Classical.choice, Quot.sound]`.

## `s(k² − 4) = k` for `k ≥ 8` from `Valid9` (`BentzFam.lean`, `Bentz4.lean`, default build, 2026-10-03)

```lean
theorem SquarePacking.Bentz4.bentz4_of_valid9 (h : Valid9) : ∀ k : ℕ, 8 ≤ k → minSide (k ^ 2 - 4) = k
def Valid9 : Prop := ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box 9 → 1 ≤ box9Cover.measure (sq c θ 1)
```

`box9Cover = fileCover 2000000000000 boxSegs boxPolyVerts boxPolyW`: `K4_k008_box9.txt` verbatim (no points, 2076 unit
segments in file order with mass `w/(2·10¹²)` uniform by length, the polygon `[14/5, 31/5]²` with mass `11.56`
uniform by area).  The proof is `bentz_of_valid7`'s, written once for any `R` in `BentzFam.lean` (`Fam` = `R`,
Lebesgue corner `A/5`, mass denominator, two code tables); `Bentz4.lean` is the instance (`fam4`: `R = 3`, `A = 14`)
plus five `decide +kernel` data checks and the accounting constants.  Differences from `k² − 3`:

* **Two entries on one segment.**  The `k² − 4` corner module puts mass on the band's end lines `x = R`, `y = R`
  (`H 3 4/5 1`, `H 3 1 6/5` and their diagonal images), where the profile's phase-0 line also lies; the box file lists
  these 16 unit segments twice (corner entry + profile entry).  So the end lines get their own line code (offset
  `5R`, distinct from interior phase 0) and the family has a second table (`famTab2`, the corner part); a file entry's
  layer is "the layer-1 mass matches, else layer 2", checked.
* **The box-file check is `O(n log n)`.**  The pairwise `Nodup` / `contains` checks of `Bentz.lean` cost ~100 µs per
  comparison in the kernel (400 entries: 32 s; the full 2076: > 5 min and 26 GB before it was stopped).  Now the
  generator also writes the entries' natural-number keys (`boxKeys`) and their sorted list (`boxGridKeys`); the kernel
  checks `keys = map key file` (3 s), a fuel-based merge sort (`msort`, proved a permutation) of them `= boxGridKeys` (3 s),
  `boxGridKeys` strictly increasing, and `boxGridKeys` = the keys of the non-zero (segment, layer)s of `[0,9]²`
  enumerated in order (`gridKeys`, 11 s); the per-entry check `segOK` (unit grid segment, mass = the family's) takes 5 s.  Strictly increasing ⇒ no entry twice; equality ⇒ every non-zero
  (segment, layer) is an entry (`keyN` is injective on the grid).
* Threshold `k₀ = 2R + 2 = 8` (localisation: a range of width `< 2` cannot touch both `x ≤ R` and `x ≥ k − R`); the
  accounting holds for `k ≥ 2R + 1 = 7`, total `= k² − 4D`, `D = 214770225571/200000000000`; segment mass
  `22.4·10¹² m + 85489190977160` (units `1/(2·10¹²)`, `k = m + 7`).

Build (cores 12–15, `LEAN_NUM_THREADS=4`): `Bentz4Data` 5.8 s, `BentzFam` 10 s, `Bentz4` 22 s.  `Bentz.lean` is
unchanged (the `k² − 3` data also passes `gen_bentzfam_data.py`'s mirror with an empty layer 2, so it could be
re-expressed as a `BentzFam` instance).

## `Valid7` / `Valid9` split: D4 and Lemma Z in Lean (`ValidSplit*.lean`, default build, 2026-10-03)

```lean
def ValidTilt (m : ℝ) (μ : Measure (ℝ × ℝ)) : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ), c.1 ∈ Set.Icc 0 (m / 2) → c.2 ∈ Set.Icc 0 (m / 2) → 0 < u →
    u ^ 2 + 2 * u ≤ 1 → sq c (2 * Real.arctan u) 1 ⊆ box m → 1 ≤ μ (sq c (2 * Real.arctan u) 1)
def ValidAxis (m : ℝ) (μ : Measure (ℝ × ℝ)) : Prop := ∀ c, sq c 0 1 ⊆ box m → 1 ≤ μ (sq c 0 1)
theorem ValidSplit.valid_of_tilt_axis (hinv : D4InvM m μ) (ht : ValidTilt m μ) (ha : ValidAxis m μ) :
    ∀ c θ, sq c θ 1 ⊆ box m → 1 ≤ μ (sq c θ 1)
theorem Bentz.validAxis7 : ValidAxis7          -- ValidAxis 7 box7Cover.measure
theorem Bentz.valid7_of_tilt (ht : ValidTilt7) : Valid7
theorem Bentz4.validAxis9 : ValidAxis9         -- ValidAxis 9 box9Cover.measure
theorem Bentz4.valid9_of_tilt (ht : ValidTilt9) : Valid9
```

`ValidTilt` is the domain of `qx2_zm.py`'s box run read off the code: `d4_roots` (centres `[0, m/2]²`, `u ∈ [0, 1/2]`),
minus what its leaves delegate (`AXIS`: `θ = 0`, Lemma Z; `SYM`: `θ ≥ 45°`, the diagonal symmetry; `EMPTY` /
`clip_bin`: no admissible pose).  No mismatch with what the reduction needs (`θ ∈ [0, π/4]`).

* **Grid covers.**  Both box files are `gridCover K A den w` (unit segments of the `1/5`-grid in `[0,K]²` with mass
  `w/den`, Lebesgue on `[A/5, K − A/5]²`), via `box7Cover_measure` / `box9Cover_measure` and the families.
* **D4** from invariance of the weight table under the index maps of `x ↦ K − x`, `x ↔ y` (`MixedCover.d4InvM`).
* **Lemma Z** as "every cell of lower-left corners, every closed corner": per cell `(p, q)` of `(1/5)ℤ²` and corner
  `(a, b)`, the inside limit is an integer sum over 50 unit segments plus `lov·lov/25`; on the closed cell the mass is
  at least the bilinear interpolation of the four corner values (segment fractions by sub-intervals, line indicators
  by closedness, Lebesgue overlaps exactly), so `≥ 1`.  3,600 corners (`K = 7`) / 6,400 (`K = 9`), the whole box.
  Agrees with `qx2_zm.py axis` (tight corners 4·188 / 4·208).
* **Kernel speed.**  `Finset` sums in a `decide` cost ~3 s per corner; a family weight (`ℤ` codes) ~1.2 ms per
  evaluation.  The weights are packed into one `ℕ` literal per file (48-bit fields, read by GMP `>>>`/`%`), tied to the
  family by one `fitOK` pass.  Checks: `fitOK` 4.3 s / 8.0 s, `axisOKP` 4.4 s / 9.0 s, `symOKP`, `outOK` < 0.5 s.
  Build: `ValidSplit` 10 s, `ValidSplit7` 12 s, `ValidSplit9` 20 s (cores 8–15).

Left: `ValidTilt7`, `ValidTilt9` (Lemmas S/T/L/R, U, K, E of the leaf primitives, with the Lebesgue polygon).  U and K:
next section.

## Lemma U (LEB) and Lemma K (CAP): `LebMass.lean`, default build, 2026-10-03

```lean
def LebMass.CovT (m : ℝ) (μ : Measure (ℝ × ℝ)) (x0 x1 y0 y1 u0 u1 : ℝ) : Prop :=
  ∀ c u, x0 ≤ c.1 → c.1 ≤ x1 → y0 ≤ c.2 → c.2 ≤ y1 → u0 ≤ u → u ≤ u1 → 0 < u → u ^ 2 + 2 * u ≤ 1 →
    sq c (2 * Real.arctan u) 1 ⊆ box m → 1 ≤ μ (sq c (2 * Real.arctan u) 1)
theorem LebMass.validTilt_of_covT (h : CovT m μ 0 (m / 2) 0 (m / 2) 0 (1 / 2)) : ValidTilt m μ
theorem LebMass.leb_sound {a b : ℚ} (hμ : ∀ S, MeasurableSet S → volume (S ∩ lsq a b) ≤ μ S)
    {B : PBox} (h : lebOK a b B = true) : B.Cov m μ
theorem LebMass.cap_sound (hA : 2 * A < 5 * K) (hden : 0 < den) {B : PBox}
    (h : capOK K A den w B = true) : B.Cov K (gridCover K A den w).measure
theorem Bentz.leb7_cov : ∀ B ∈ lebLeaves7, B.Cov 7 box7Cover.measure
theorem Bentz.cap7_cov : ∀ B ∈ capLeaves7, B.Cov 7 box7Cover.measure
```

* **Box and bin.**  A leaf is a `PBox` of six rationals (the dump's `Fraction`s); tests are `ℚ` comparisons by
  `decide +kernel` (only ~1,000 such leaves per run, so `ℚ` costs nothing).  `ŵ = whi u1` (`w(u1)` below 45°, else
  `14143/10000`), sound on `ValidTilt`'s region by monotonicity of `widU` (`widU_le_whi`).
* **Lemma U.**  `λ(sq c θ 1) = 1` (`volume_sq`: preimage of `[−½,½]²` under a translation and a linear map of
  determinant 1); a grid cover is `≥ λ` on its Lebesgue square (`gridCover_vol_le`).
* **Lemma K.**  Width lemma for compact convex centrally symmetric sets (slices below the centre are no longer than
  the slice at `a`), Fubini (`Measure.prod_apply_symm`) for `λ(Q ∩ {y < a}) ≤ d·λ₁(Q_a)`, a unit grid segment
  captures `5 λ₁(slice ∩ cell)`, the chord range from the box (crude, and the tangent cap from the cone at the lowest
  / leftmost vertex), cell indices by floor/ceil; the final inequality entirely in `ℝ≥0∞`.
* **Smoke test.**  All 689 LEB and 374 CAP leaves of run V3 pass (`decide +kernel`, a few seconds); the mirror in
  `gen_lebmass_data.py` agrees (0 rejections).  Without the tangent refinement 124 CAP leaves fail; with zero weights
  all 374 fail.  Build: `LebMass` 12 s, `LebMass7Data` 6 s, `LebMass7` 10 s (`LEAN_NUM_THREADS=4`).

Left for `ValidTilt7` / `ValidTilt9` (`notes/lean-leb-mass.md` §7): the `CovT` tree layer, PIECE with the polygon
(Lemma S(b), plus the existing S/T/L), and Lemma E (11 k leaves, the large part): ~5–8 k lines, several weeks.

## Remaining gaps / next steps

* No `sorry`; nothing is assumed about the tree, the generator or the decoder.
* `BoxTree`'s leaf test is sound everywhere but a tree can only terminate where the certificate
  has slack; the zero-margin leaves are in `ZMTree` (rung 2: `s(13) = 4`; rung 2b: `s(32) = 6`,
  both done, hypothesis-free).  Next: segments (`s(21)`, `s(45)`), scoped in the section above.
* D4 symmetry is assumed (`d4Check`); a certificate without symmetry needs a second root lemma
  (centre in `[0,m]²`, `u ∈ [0,1]`, via `θ ↦ θ + π/2`), about 30 lines on top of `d4_reduce`'s
  step D.  All certificates in `certificates/` checked so far are D4-invariant (including the
  1736-point `s12_lower_3.9686.txt`, checked by `pts_d4`).
* Others' certificates (rung 2) only need a file in this format (`certificates/FORMAT.md`).

