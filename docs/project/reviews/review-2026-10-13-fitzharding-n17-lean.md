# Adversarial Review: Fitzharding’s Lean Proof That `s(17) = L`

Reviewed 2026-10-13 from the public source
[`ofitzharding/sq17-lean`](https://github.com/ofitzharding/sq17-lean) at head
`e6ee548090dc1dbf938ecf8590481de837a6a454` (13 October 2026), whose proof files are
those of release
[`v1.0.0`](https://github.com/ofitzharding/sq17-lean/releases/tag/v1.0.0) at
`0a7167efa8dcae7fa73855890630fb7e2de550ed` (the two later commits change only
`CITATION.cff`), by an AI agent: the adversarial review lane of the sq17-lean intake
(bead `think-xjb2`, a child of the import bead `think-hcqr`), prompted separately from
the lane that retains the source packet and sharing no context with it.
The model is `claude-opus-5-5` at the tbd-strong tier; the lane was not told its
reasoning setting.
The two reviews of `T-153` were read for their form and for Overbeck’s
statement; they are other lanes’ work.
The clone was read as untrusted data: no Lean, lake or script from it was executed, and
every Python program that read it ran under `-I`. One of the three release archives,
`generated-sources.tar.gz`, was downloaded to scratch, streamed and scanned (§3.2), and
deleted. Nothing upstream was modified, nothing was posted, and this lane proposes no
upstream bytes for retention; that is the packet lane’s decision.

This review registers nothing and moves no bound.
It is not a human formalization review, which `V5` needs, and not a human oversight
record.

**In one line:** `Sq17.square17_optimality` states this record’s `s(17) = L` exactly,
over closed unit squares with independent rotations, boundary contact allowed and
interiors disjoint, and its `EndpointGeometry.side` is the record’s $L$ by identity of
definitions (the same two polynomials, the same isolating box, the same side map); the
theorem takes no hypothesis but `L`, and by the source’s own axiom report its proof
rests on Lean’s three standard axioms and 13,343 `native_decide` facts, all in the case
exclusion and capture checks; the proof follows this project’s n = 17 plan (the 24-cell
cover, the census, sub-pattern exclusion, capture and the 52-row local half) and reuses
its data, which the source does not credit; it was published about six hours after
Overbeck’s candidate, which was the first public report, and it is the first report of a
complete proof, not a formalization of Overbeck’s.

**Verdict: accepted**, for what was read: the statement, the endpoint, the trust
boundary and the claim that no premise is left.
No mathematical defect was found.
Conditions: nothing was built here, so every “proved in Lean” below is the source’s
report together with this lane’s reading of the text; the 13,343 native checks were
neither replayed nor read; the soundness proofs of the half-plane checker were not read
(§0). Finding F-1, on credit, is for the owner and does not bear on the claim’s truth.

## 0. What Was Read, Skimmed, Scanned and Not Read

| Depth | Files |
| --- | --- |
| Read in full | `README.md`, `CITATION.cff` (both revisions), `lakefile.toml`, `lean-toolchain`, `lake-manifest.json`, `scripts/reproduce.py`, `verification/clean-build-receipt.json`, both control logs; `Square17Optimality.lean`, `SquareBase.lean`, `PropagationWall.lean`, `EndpointGeometry.lean`, `EndpointRoot.lean`, `EndpointRootData.lean` (definitions and proofs; the coefficient lines by script), `PolynomialBoxContraction.lean`, `PolynomialNewtonRoot.lean`, `PackingStatement.lean`, `HalfPlaneAssemblySkeleton.lean`, `HalfPlaneFinalAssembly.lean`, `HalfPlaneLastTwo.lean`, `HalfPlaneLastCase.lean`, `HalfPlaneFullRoute.lean`, `OrbitPackingReduction.lean`, `ExactCellCover.lean`, `ExactWallCapacity.lean`, `EndpointPacking.lean`, `RepresentativeCaseCheck.lean`, `HalfPlaneTree.lean`, `HalfPlaneBoundaryControl.lean`, `CaptureTerminalOptimality.lean`, `CaptureLocalOptimality.lean`, `LocalRigidityCertified.lean`, `CaptureOpen/Optimality.lean`, `OrbitCensus/Complete.lean` |
| Skimmed | `InteriorCellCapacity.lean` (lines 1–80), `HalfPlanePositiveControl.lean` (theorem list), `LocalRigidityDual.lean` (lines 1–40), `HalfPlaneFast.lean` (lines 1–40 and its definition list) and the definition lists of the other four `*Fast` modules, `ExactCellCoverData.lean` (the vertex block), `RepresentativeCaseData.lean` (the pattern table), `EndpointSideSharp.lean` and `EndpointIntervals.lean` (the side bounds), `CaptureFamily.lean`, `HalfPlaneTrees/T1563/Dispatch.lean`, `CaptureOpen/Chunk0161Checks.lean`, `OrbitCensus/Chunk0000.lean` (head), the heads of six archived data modules (§3.2) |
| Scanned by script | All 1,215 Lean files of the Git tree and all 526 members of `generated-sources.tar.gz`, for the keywords of §3.2; the 241-module closure of `PackingStatement.lean`, for `native_decide`; `manifest.json`, all 4,953 rows; the axiom report, all 13,346 entries |
| Not read | The proofs of the checker soundness theorems: `HalfPlaneInt`, `HalfPlaneStateSound`, `HalfPlaneCover`, `Propagation*`, `CaptureRunSound`, `CaptureTableSound`, `CaptureSummarySound`, `LocalSlider*`, `LocalGeometric*`, the `LocalRigidity*` modules other than `LocalRigidityCertified`, `CellSymmetry`, `CenteredOrbitFrame`, `WallCapacity*`, `WallSquareSupport` and the rest of the roughly 140 hand-written modules not named above; every generated certificate except as named; `scripts/unpack.py`; the archives `ordinary-generated-sources.tar.xz` (2,832 members) and `tree1563-sources.tar.gz` (380 members), not downloaded |

Words used below: *proved in Lean* means the source’s text proves it with tactics, `rfl`
or `decide +kernel`, and the published axiom report is consistent with that; nothing was
compiled here.
*Native-checked* means a `native_decide` fact, evaluated by compiled code.
*Checked here* means recomputed in this lane (§10). *Asserted* means stated by the
source and not checked.

## 1. Statement Fidelity

The theorem, `Sq17Lean/Square17Optimality.lean` lines 16–19:

```lean
theorem square17_optimality (L : ℝ) :
    HalfPlaneAssembly.PlainPacking L ↔ EndpointGeometry.side ≤ L
```

and its definitions:

```lean
-- SquareBase.lean lines 14–19
def sq (cx cy ux uy : ℝ) : Set (ℝ × ℝ) :=
  {p | |(p.1 - cx) * ux + (p.2 - cy) * uy| ≤ 1/2 ∧ |(p.2 - cy) * ux - (p.1 - cx) * uy| ≤ 1/2}
def IsUnitSquare (S : Set (ℝ × ℝ)) : Prop :=
  ∃ cx cy ux uy : ℝ, ux ^ 2 + uy ^ 2 = 1 ∧ S = sq cx cy ux uy
-- PropagationWall.lean lines 10–11
def containerBox (L : ℝ) : Set (ℝ × ℝ) := {p | 0 ≤ p.1 ∧ p.1 ≤ L ∧ 0 ≤ p.2 ∧ p.2 ≤ L}
-- PackingStatement.lean lines 7–11
def PlainPacking (L : ℝ) : Prop :=
  ∃ squares : Fin 17 → Set (ℝ × ℝ),
    (∀ i, Sq17.IsUnitSquare (squares i)) ∧
    (∀ i, squares i ⊆ Propagation.containerBox L) ∧
    (∀ i j, i ≠ j → Disjoint (interior (squares i)) (interior (squares j)))
```

| The record’s `s(17) = L` says | The formal statement says | Agrees |
| --- | --- | --- |
| $L$ is the least side of a square that holds seventeen unit squares, and it is attained | For every real `L`, a packing exists exactly when `side ≤ L`: the feasible sides are the closed ray from `side`, so `side` is the minimum, not only the infimum | Yes |
| Seventeen squares | `Fin 17 → Set (ℝ × ℝ)`. Two indices cannot name one square: its interior is nonempty, so it is not disjoint from itself. Fewer than seventeen cannot count | Yes |
| Unit squares, closed | `sq` is the set of points whose two coordinates in the frame `(u, u⊥)` are at most `1/2` in absolute value; `IsUnitSquare` requires `ux² + uy² = 1`, so the frame is orthonormal and the side is 1; the inequalities are weak, so the square is closed | Yes |
| Each square independently translated and rotated | Each square has its own existentially chosen centre and unit direction, with no constraint linking squares and no restriction on the angle | Yes |
| The container | `containerBox L` is the closed `[0, L]²`; axis-aligned at the origin without loss of generality | Yes |
| Boundary contact allowed | Closed squares in a closed container, and only interiors must be disjoint; the control `HalfPlaneBoundaryControl.lean` lines 19–27 proves two touching squares legal | Yes |
| Pairwise disjoint interiors | `Disjoint (interior …) (interior …)` for `i ≠ j`, with Mathlib’s `interior` for the product topology on `ℝ × ℝ`, which is the Euclidean one | Yes |
| $L$ | `EndpointGeometry.side`; §2 shows it is the record’s $L$ | Yes |
| Uniqueness of the packing | Not stated | Yes, none claimed |

**Objections tried.** (a) *A degenerate square.* `IsUnitSquare` forces a unit direction,
so no zero-area or non-square set qualifies.
(b) *Negative or small `L`.* For `L < 0` the container is empty and both sides are
false; for `0 ≤ L < side` the theorem is the lower bound.
(c) *A vacuous direction.* The existence direction has a witness,
`endpoint_plainPacking` (`PackingStatement.lean` line 34), the seventeen squares of
`EndpointGeometry.squares` proved inside `[0, side]²` and pairwise interior-disjoint
(`EndpointPacking.lean` lines 9–65); containment in `[0, L]²` for `L ≥ side` follows
(`HalfPlaneFinalAssembly.lean` lines 61–71). The impossibility direction is not vacuous
because `PlainPacking side` holds.
(d) *An ill-defined `side`.* `side` uses `Classical.choose` of an `∃!`
(`EndpointRoot.lean` lines 10–17), so the chosen point is pinned by the proved
uniqueness; the theorem itself also pins `side` as the minimum.
(e) *A second statement in disguise.* `PlainPacking` and the internal `Feasible`
(`HalfPlaneAssemblySkeleton.lean` line 102, centres and unit directions) are proved
equivalent in `PackingStatement.lean` lines 13–30, and the theorem is stated for
`PlainPacking`, the form with no parametrization.
(f) *Name resolution and elaboration.* The axiom report prints the type with fully
qualified names:
`Sq17.HalfPlaneAssembly.PlainPacking L ↔ Sq17.EndpointGeometry.side ≤ L` (last line of
`verification/Square17Optimality.log`). The only declarations named `PlainPacking`,
`containerBox`, `IsUnitSquare` and `sq` in the tree are those quoted; the other `side`
definitions are rationals in the namespaces of three trees, two pattern files and the
neighbour seed. Across the 1,215 tree files there are three `instance` lines, all
`DecidableEq` or `Decidable` (`CaptureRunFast.lean` lines 7–8,
`RepresentativeCaseCheck.lean` lines 22–24), one tactic macro (`EndpointContacts.lean`
line 13, which can only build proof terms), and no `notation`, `syntax`, `elab`,
`export`, `renaming` or `attribute` command (two `@[simp]` tags on the source’s own
lemmas in `ArctanCheck.lean` are the only attributes); the 526 members of
`generated-sources.tar.gz`, which include all 22 archived modules in
`PackingStatement`’s closure, have none of these at all.
The two archives not downloaded were not scanned; they are outside `PackingStatement`’s
closure, so they cannot change what `PlainPacking` means, and a later instance on `ℝ`’s
order that was not definitionally the standard one would break the Mathlib order lemmas
the assembly uses. A scan of those two archives is cheap (§6) and would close the point.

Verdict on §1: the statement is the record’s claim, with no wrong quantifier, frame or
symmetry restriction, open-closed slip, indexing gap or vacuous hypothesis.

## 2. The Endpoint Constant

**The Lean definition.** `EndpointGeometry.lean` lines 11–17:
`t := EndpointRoot.coordinates.1`, `beta := EndpointRoot.coordinates.2`,
`side := (6+4*t)/(1+2*t-t*t)`. `EndpointRoot.unique_root` (`EndpointRoot.lean` lines
10–15) proves that exactly one point of the closed box of radius `radius = 1/10^12`
about `midpoint` is a common zero of `polynomial0` and `polynomial1`, and `coordinates`
is that point.
The data are in `EndpointRootData.lean`: `midpoint` (line 9), two 60-place
decimals; `radius` (line 10); the polynomials (lines 11–43) as monomial lists
`⟨i, j, c⟩ = c tⁱ βʲ`. The proof is a Newton–Banach argument: a rational preconditioner
`c00 … c11` with nonzero determinant (line 107), two Newton-map polynomials whose
identities with the preconditioned system are proved by `norm_num` and `ring` (lines
111–122), and the coefficient test `check` (`PolynomialBoxContraction.lean` line 102:
absolute coefficient mass at most 1 and slope at most `1/2`) decided by `decide +kernel`
(line 105), from which Mathlib’s contraction mapping theorem gives a unique fixed point
(`PolynomialBoxContraction.lean` lines 104–132, `PolynomialNewtonRoot.lean` lines
20–57). The endpoint is proved in Lean with no native evaluation; the axiom report
confirms this indirectly, since the final theorem depends on `side` and lists no native
fact outside `Sq17.Propagation.HalfPlaneState`.

**The record’s definition.** `n-017.md` and `T-153` state $L = (6+4t_*)/(1+2t_*-t_*^2)$
with $(t_*, b_*)$ the unique common zero of H-255’s $F$ and $G$ in the radius-$10^{-12}$
box about the 60-place $(t_0, b_0)$ that the exp-237 certificate freezes; exp-245
identifies $L$ with the root of the catalogue’s degree-18 polynomial.

**Comparison, checked here** in exact rational arithmetic with the project interpreter
(§10, `endpoint_compare.py`):

| Item | Result |
| --- | --- |
| `polynomial0`, `polynomial1` against exp-237’s frozen `polynomials` | Equal, term for term |
| The same against H-255’s formulas rebuilt by `devtools.check_n17_root_certificate.n17_polynomials` | Equal, term for term |
| `midpoint` and `radius` against exp-237’s `box` | Equal |
| The side map | The same rational function as `check_n17_endpoint_feasibility._layout` and the record |
| The Lean contraction test, recomputed | Coefficient masses `1.295 × 10^-8` and `7.12 × 10^-9`, slopes `1.296 × 10^-8` and `7.13 × 10^-9`: the test passes by eight orders of magnitude |
| The Newton identities, recomputed by exact expansion of `P(m + r p)` | Both hold coefficient for coefficient |
| `side` to 60 places, by exact Newton refinement in the box | `4.675530093604550951634111270483146648767143855015879695416889` |
| Residuals of $F$, $G$ at the refined point | `6.4 × 10^-201`, `8.6 × 10^-201` |
| The degree-18 catalogue polynomial (`n-017.md`, `minimal_polynomial`) at that value | Residual `7.8 × 10^-191`; sign change across `±10^-40` |
| The record’s enclosure, exp-245 | `4.6755300936045509516341112704831466487671…` agrees to all 40 printed places |
| The record’s verified ceiling `23377650468022754758171074269267527/(5 × 10^33)` minus the value | `1.0358 × 10^-22` |

The Lean also proves its own decimal bounds,
`4.6755300936045509 ≤ side ≤ 4.6755300936045510` (`EndpointSideSharp.lean` lines 38–40),
which hold the value above.

**Same number, by method.** The two constants are the same algebraic number because they
have the same definition: the image under one side map of the unique common zero of the
same two polynomials in the same closed box.
The Lean proves uniqueness in that box and exp-237 proves it independently, so the two
zeros coincide; no numerical agreement is needed for the identity, and the 60-place
evaluation and the degree-18 sign change only confirm it.
The record’s $L$ and `EndpointGeometry.side` are one real number.

**Where the digits come from.** The 60-place `midpoint` is the tan-half pair of Marc
Leonard Overbeck’s rational reconstruction of Bidwell’s packing of 21 September 2026
(`packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/upper-packing-certificate.json`,
squares 9–14 and 16), which exp-237 took as its box centre; the Lean file says it was
“generated from the exact mathematical data in root_chart_data.json”, a file the release
does not include. The endpoint layout of `EndpointGeometry.lean` lines 18–40 (the
centres, the slider square 6 at `side − 3/2 − T/(3s)`, square 13 at `v11 − 1 − T/3`, the
directions `(1,0)`, `(c,s)`, `(d,−e)`) is H-256’s `_layout` in
`devtools/check_n17_endpoint_feasibility.py`, symbol for symbol, with the same label
convention.

## 3. Trust Boundary and Completeness

### 3.1 The axiom report

`verification/Square17Optimality.log` (SHA-256 `5e74c4af…8ac241`, which equals the
receipt’s `final_log_sha256`) lists 13,346 axioms for `Sq17.square17_optimality`, all
distinct:

| Kind | Count |
| --- | ---: |
| `propext`, `Classical.choice`, `Quot.sound` | 3 |
| `…._native.native_decide.ax_1_1`, all in `Sq17.Propagation.HalfPlaneState` | 13,343 |
| `sorryAx` | 0 |
| Any other axiom | 0 |

The native facts, by family: the 2,776 ordinary full cases, four each (`excluded`,
`owners_eq`, `seed_ok`, `table_ok`: 11,104); the 35 patterns, four each (140); the
capture trace `CaptureOpen` (825: `boundary_checked` 164, `fresh_checked` 165,
`inherited_checked` 164, `initial_length` 165, `run_checked` 165, `seed_checked` 1,
`summary_checked` 1); the neighbour chain `Neighbour329` (434); the three trees `T1528`,
`T1531`, `T1563` (840). The sum is 13,343, the number the README, the receipt and issue
#565 give.

### 3.2 The source scan

| Search | Git tree, 1,215 files | `generated-sources.tar.gz`, 526 members |
| --- | --- | --- |
| `axiom` declaration | 0 (three comment mentions) | 0 |
| `sorry`, `admit` | 0 (one comment mention each) | 0 |
| `opaque`, `implemented_by`, `@[extern]`, `@[csimp]`, `unsafe`, `partial def` | 0 | 0 |
| `instance` | 3, all `Decidable` or `DecidableEq` | 0 |
| `notation`, `macro`, `syntax`, `elab`, `export`, `renaming`, the `attribute` command | 1 tactic macro, `EndpointContacts.lean` line 13 | 0 |
| `ofReduceBool`, `trustCompiler`, `#eval`, `run_cmd`, `IO`, `Float` | 0 | 0 |
| `native_decide` | 714 lines in 313 files; 2 more are comments | 1,334 |
| `decide +kernel` | 2,091 | 877, all in the 22 statement-closure modules |
| `set_option` other than heartbeats and recursion depth | linters only | linters only, 3 files |

The archive’s 526 members are exactly the manifest’s 526 rows for it, each with the
manifest’s SHA-256 and size, with no link, duplicate, absolute or `..` path; the archive
itself has the SHA-256 the manifest and GitHub’s asset digest give.
The 1,215 tree files match their manifest rows.
The 241-module closure of `PackingStatement.lean` (219 tree modules and 22 archived
ones) and the 18-module closure of `EndpointPacking.lean` contain no `native_decide` use
(the one textual match is the comment at `InteriorCellCapacity.lean` line 134): the
statement and the upper bound are proved without native evaluation.

The one hand-written `Decidable` instance (`RepresentativeCaseCheck.lean` lines 22–24)
is `cases a <;> unfold Matches <;> infer_instance`, which builds the standard instance
for each branch; a native evaluation cannot read it differently from the kernel.

### 3.3 What a native check decides, and what it trusts

Every native fact is a decidable statement about concrete data: most have the form
`checker data = true` for a checker in one of five modules, `HalfPlaneFast`,
`CaptureRunFast`, `CaptureTableFast`, `HalfPlaneCoverFast` and `CaptureSummaryFast`,
which import only Lean core and each other (`HalfPlaneFast.lean` lines 1–6), and the
rest are length facts such as `S0.length = 17`. A theorem proved in Lean turns each
accepted run into geometry: for example `tree_excluded` (`HalfPlaneTree.lean` lines
130–156) says that an excluded seeded state admits no seventeen interior-disjoint unit
squares with centres in the roster’s cells.
The build driver compiles the five modules to C, then to shared libraries with
`leanc -O3`, and loads them into every later `lean` process with `--load-dynlib`
(`scripts/reproduce.py` lines 18–19, 82–92, 127–128), so the checkers run as native
code. The certificate data are mostly `String` literals decoded at evaluation time by
`parseInts` (`HalfPlaneFast.lean` line 243; for example
`CaptureOpen/Chunk0161Checks.lean`), so the kernel never sees the decoded certificates.
The trusted base is therefore: Lean’s kernel; Lean’s compiler and the bundled C compiler
for the five modules; the compiled runtime routines of Lean core that the checkers call
(`String.splitOn`, `String.toInt?`, `Array` access, `Int` and `Rat` arithmetic over
GMP); the agreement of the shared libraries with the `.olean` files they were built
beside; and Mathlib’s pinned cache.
The README says the compiler, native evaluator and C toolchain are trusted (lines 29–38,
50–52); this is the same boundary in more detail.
The source’s positive control documents one trap the soundness theorems guard against:
`excludes` with a wrong owner count returns `true` (`HalfPlanePositiveControl.lean`
lines 61–63), and the theorems require the state length as a hypothesis, which the
`owners_eq` and `*_length` native facts supply.

### 3.4 No premise is left

The README (lines 18–20) and the release notes say the statement has no
certificate-acceptance or case-exclusion premise.
The chain bears this out:

| Obligation of the conditional skeleton (`HalfPlaneAssemblySkeleton.lean` lines 35–60) | Discharged by | How |
| --- | --- | --- |
| Capacity one of the 16 wall cells (`ExactCellCover.lean` lines 85–91) | `ExactWallCapacity.lean` line 64, `wall_capacity` | Proved in Lean |
| Capacity one of the 8 interior cells; coverage of the centre box | `InteriorCellCapacity`, `ExactCellCover.lean` line 22 | Proved in Lean |
| The census: every 17-subset of the 24 cells reaches a representative | `OrbitCensus/Complete.lean` line 11, `exhaustive`, over 346,104 rows | Proved in Lean, `decide +kernel` |
| Every representative is a pattern image or a full case | `RepresentativeCaseParts/All.lean` line 1791 | Proved in Lean, `decide +kernel` |
| Every full case of length 17 is ordinary, a neighbour or the capture case | `HalfPlaneFullRoute.lean` lines 31–58 (2,781 indices) | Proved in Lean, `decide +kernel` |
| The 35 patterns excluded below `side` | `HalfPlanePatterns/Dispatch.lean` (archived) | Native-checked |
| The 2,776 ordinary cases | `HalfPlaneCases/Ordinary.lean` line 68 | Native-checked |
| Neighbours 1528 and 1531 | `HalfPlaneTrees/T1528/Dispatch.lean`, `T1531/Dispatch.lean`, line 14 each | Native-checked |
| Neighbour 329 | `Neighbour329/Dispatch.lean` line 4, used at `HalfPlaneLastCase.lean` lines 12–14 | Native-checked |
| Neighbour 1563 | `HalfPlaneTrees/T1563/Dispatch.lean` line 14, the argument at `Square17Optimality.lean` line 19 | Native-checked |
| The capture case reaches the local chart | `CaptureOpen/Optimality.lean` lines 7–9 | Native-checked |
| A packing in the local chart has side exactly `side` | `CaptureTerminalOptimality.lean` lines 16–31, `CaptureLocalOptimality.lean` lines 45–60, `LocalRigidityCertified.lean` lines 9–14 (93 boxes) | Proved in Lean, `decide +kernel` |
| The upper bound | `EndpointPacking.lean` lines 60–65 | Proved in Lean |

The final theorem’s only binder is `L`, as the printed type shows, and an unproved
premise left as an `axiom` would be in the axiom list.
Several module docstrings still describe the earlier conditional state (F-3); each is
true of its own file’s theorems, whose premises later files discharge.

### 3.5 The receipts

`verification/clean-build-receipt.json` records `CLEAN_SOURCE_BUILD_ACCEPTED`, 4,951
modules rebuilt with Lean 4.34.1, no prebuilt project `.olean`, the pinned Mathlib cache
reused, the three standard axioms, 13,343 native facts, the axiom set equal to the
author’s local build, and both controls with exit code 0 and log digests; the two
control logs it names are in the tree and match.
It carries no per-module log, no time, no machine description and no signature, and the
“independent checks” of the README (line 44) were distributed between two of the
author’s machines. It is the producer’s report of a replay, not a replay here.
The pins are consistent: `lean-toolchain` is `v4.34.1`, a Lean release of 24 September
2026, and Mathlib’s tag `v4.34.1` resolves to the `lake-manifest.json` revision
`d13f23b723b8…`, where `Mathlib/Basic/Real/Basic.lean`, which `SquareBase.lean` imports,
exists.

Verdict on §3: the trust boundary is what the source says it is, stated here in more
detail, and no premise is left as a hypothesis.

## 4. Architecture, Lineage and Independence

### 4.1 The architecture

Suppose seventeen unit squares pack in a square of side `L < side`. Translate the
packing to the centre of the square of side `U = 1169/250`; every centre then lies in
the closed centre box `[1/2, U − 1/2]²`, which 24 closed convex cells cover, each
holding at most one centre (eight interior cells by diameter, sixteen wall cells by a
depth-width wall lemma), so the packing occupies 17 distinct cells.
A census proved in the kernel reduces the 346,104 seven-hole sets under the cover’s
eight symmetries to representatives; each representative either contains a symmetry
image of one of 35 small occupied-cell patterns, or is one of 2,781 full cases.
Each pattern and each of 2,776 ordinary full cases is excluded at a cap a little above
`side` by a half-plane propagation trace (per square, polygonal centre domains and angle
rows, cut by pairwise collision and wall rules, split into branches) accepted by a
native-compiled checker whose soundness is proved in Lean.
The patterns and ordinary cases run in the `ordinary` frame, of side
`2632353982198055/2^49`, about `4.7 × 10^-4` above `side`; the four neighbouring cases
run in the `captureNeighbour` frame, of side `5264178896829249/2^50`, `1.1 × 10^-17`
above `side` (`HalfPlaneFrameBounds.lean` lines 33–40), three by branch trees and one by
a 108-chunk chain. The last case, the occupancy state of Bidwell’s packing, is captured:
a 165-chunk trace confines every packing in it to a chart within `10^-7` of the endpoint
family in 45 non-slider coordinates, with three sliders bounded, and there 52 contact
rows and a weighted dual certificate over 93 boxes force all 45 coordinates to zero, so
the side is exactly `side`, contradicting `L < side`.

### 4.2 What it shares with this project

Each item was checked here by exact comparison (§10) or by reading:

| Component | This project’s record | The Lean | Relation |
| --- | --- | --- | --- |
| The endpoint chart | H-255’s $F$, $G$ and exp-237’s box | `EndpointRootData.lean` lines 9–43 | Equal (§2) |
| The endpoint layout and labels | H-256, `check_n17_endpoint_feasibility._layout`, exp-238 | `EndpointGeometry.lean` lines 11–40 | Same formulas, same label order, square 6 the slider |
| The cap | `U = 1169/250` (H-266, explainer “The Cap”) | `ExactCellCover.lean` line 41 and throughout | Equal |
| The 24-cell cover | `ring-3-voronoi-8-tabbed-unique` (H-266, exp-247), `check_n17_capacity_one_cover.UNIQUE_24` | `ExactCellCoverData.lean` lines 9–57 | All 24 cells equal vertex for vertex, in the same order and under the same names (`corner-SW`, `side-S0`, `interior-SW`, …); none equal to the three earlier designs |
| The wall-cell parameters | Corners `79/100`; depth `911/1000`, width `529/750`; middle cells depth `93/100`, width `257/375`; the depth-width wall lemma (H-259, review of 2026-10-02) | `ExactWallCapacity.lean` lines 9–14, 50–62 | Equal parameters; the lemma reproved in Lean |
| The census | 346,104 states, 43,593 D4 orbits (exp-246) | `OrbitCensus/`, “the 43,593-orbit census” (`ExactCellCover.lean` line 14) | Same count |
| The excluded patterns | `X048-session-168-pilots/certified-sub-patterns.yaml`, 72 admitted entries | `RepresentativeCaseData.lean` lines 6–42, 35 patterns | 32 of the 35 equal an admitted entry up to the cover’s symmetry: A, W7 and SW9; 18 from Session 182; 11 closed by wand125 through issue #472 and admitted on 9 October. The other three are subsets of admitted entries. The Lean excludes them with its own certificates |
| The local half | The local-theorem recipe (review of 2026-10-02): 52 rows, rank 45 at the root, three sliders, positive dual weights; the X048 local-radius certificates | `LocalRigidity*`, `LocalPerturbationCoordinates.lean` (`Fin 45`), `AffineWeightCertificate 52 3` in the archived `LocalRigidityWeightData` | Same row count, coordinates and sliders; the first box, `[0, 1/4] × [−1/2500, 1/12] × [−1/8, 1/16]` for direction `+xi1`, is the first cell of `ratio-bwprime-1024-certificates.json`, with weights on the same `2^-44` grid; the arrays are not identical |
| Capture | The third part of the plan; undecided after pilot 2 (explainer, “Capture and Its Pilot”) | `CaptureOpen/` and `CaptureTerminal*` | The Lean’s own capture trace; nothing in this project completed it |

What is new in the Lean relative to this record is the exclusion of every residual case
(this project’s census still had 3,636 orbits open under its 72 entries), the capture,
and the formal proof of every bridge from certificates to geometry.
The overall plan, and much of the data it runs on, are this project’s.

### 4.3 Overbeck’s candidate edition

The Lean does not use Overbeck’s candidate proof.
None of its objects appears in the Lean (no class-row or charge certificate, no `KEY_W`,
`L9` frame, `JQ`/`JG`/`JPA` tree, `SPEC_v3.0`, `G20S` or `HW`), and the routes differ:
Overbeck’s is a charge-counting capture over eleven roots with thirteen
branch-and-contract trees; the Lean’s is a cell census with half-plane exclusion.
They share the endpoint chart (both take exp-237’s box, whose digits are Overbeck’s
September seed) and both build their local step on this project’s 52-row model.
The README (lines 119–122) and issue #565 say the Lean was developed independently; the
code bears that out, but the public history starts at the release (four commits from
20:42:00Z on 12 October), so the order of development cannot be checked, and the first
commit already cites Overbeck’s candidate.

### 4.4 Ahmed and MacIver

`lake-manifest.json` requires only Mathlib and its own dependencies; the Lean imports
nothing from Manasseh Ahmed’s `11SquaresFormalized` (the README spells his name
“Mannaseh”) or David MacIver’s `square-packing-research`, and no Lean file or scanned
archive member names either.
The trust model, `native_decide` behind kernel-proved soundness, is the one
`11SquaresFormalized` uses, as the README says (lines 35–37); the three-part shape
(finite exclusion, capture, local endpoint argument) is the n = 11 proof’s, which issue
#565 says and the README does not.

### 4.5 Credits given

| Where | Credit |
| --- | --- |
| `README.md` lines 104–105 | John Bidwell for the 1998 packing, improving Pertti Hämäläinen’s 1980 arrangement; Friedman’s survey |
| `README.md` lines 106–107 | The Squares Project “collects the wider research record” |
| `README.md` lines 107–110 | Ahmed “and collaborators’” eleven-square formalization, “a useful reference for computer-assisted formalization and its trust boundary” |
| `README.md` lines 110–111 | MacIver’s earlier Lean work, “a lower bound for seventeen squares” |
| `README.md` lines 119–122 | Overbeck’s independent candidate proof of 12 October 2026 |
| `README.md` line 124 | “substantial assistance from Claude and Codex” |
| `CITATION.cff` | Author Oscar Fitzharding; no references section |
| X post, 2026-10-13T00:06:56Z | “Built with @OpenAI Astra + @AnthropicAI Opus 5.5. Thanks to @ManassehA06 & @ojoshe for prior work.” |
| Issue #565 on this repository, 2026-10-12T22:23:37Z | Bidwell; Ahmed’s s(11) proof and formalization as “methodological references for finite exclusion, capture and the local endpoint argument”; “the Squares Project’s contributors and the Lean/Mathlib communities”; Claude and Codex; Overbeck’s candidate as related work |

### 4.6 Credits it should give and does not

- This project, for the 24-cell cover and its wall lemma, the cap and census, the
  selection of 32 of its 35 patterns, the endpoint chart and layout, and the local-half
  recipe (§4.2). “Collects the wider research record” and “prior work” do not say that
  the proof runs on these.
- wand125, whose eleven certified sub-patterns of issue #472 are among the 35, and the
  sessions whose entries the other 21 are.
- Overbeck, for the 60-place seed of 21 September that fixes the Lean’s box centre.
- Ahmed’s s(11) proof (`11SquaresOptimal`) for the proof shape, in the README and
  `CITATION.cff` as in issue #565.
- The identification of the Lean’s constant with “Bidwell’s packing” (README lines 3–5)
  as the catalogue’s degree-18 algebraic number rests on this project’s exp-245, which
  the README does not cite; the Lean proves nothing about that polynomial.

## 5. Chronology

All times UTC on 12 October 2026 unless stated.
Server-side times are GitHub’s or X’s; Git commit dates are set by the committer and are
listed only for completeness.

| Event | Time | Source |
| --- | --- | --- |
| `Kleddamag/the-seventeenth-square-candidate` created, public | 13:46:05 | Repository `created_at`; events API `PublicEvent` |
| Its branch `main` created | 14:21:17 | Events API `CreateEvent` |
| Its release `large-files-v1`: 12 assets uploaded, then published | 14:21:19–14:24:19; 14:24:20 | Release asset `created_at`/`updated_at`; release `published_at`; `ReleaseEvent` |
| Its only commit `653b9589d` | Authored 14:35:48, committed 14:40:59 | Git dates (committer-set) |
| That commit pushed | 14:41:30 | Events API `PushEvent`; repository `pushed_at` |
| Issue #557 opened here: “Tracking for @kleddamag ’s new announced proof” | 16:42:56 | Issues API |
| GitHub account `ofitzharding` created | 2026-07-31 02:50:36 | Users API |
| `sq17-lean` first commit `915afab` | 20:42:00 | Git date (committer-set) |
| `ofitzharding/sq17-lean` created, public | 20:42:08 | Repository `created_at`; events API `PublicEvent` |
| Its three release assets uploaded | 20:42:39–20:42:40 (updated to 20:52:16) | Release asset `created_at`/`updated_at` |
| Commit `0a7167e`, the receipts | 22:06:08 | Git date |
| Release `v1.0.0` published | 22:06:23 | Release `published_at`; `ReleaseEvent` |
| Issue #565 opened here: “Complete Lean proof of s(17) optimality: registration request” | 22:23:37 | Issues API |
| X post 2109798000008597616 | 2026-10-13 00:06:56 | Syndication JSON `created_at`; the post ID’s timestamp bits give 00:06:56.010 |
| Commits `dc67357`, `e6ee548` (citation only) | 2026-10-13 01:31:15, 01:59:58 | Git dates; repository `pushed_at` 02:00:01 |

Overbeck’s candidate was public first: its proof edition was pushed at 14:41:30 and its
large files published at 14:24:20, six hours before `sq17-lean` became public at
20:42:08 and seven hours 25 minutes before its release.
The Lean’s first commit already cites Overbeck’s candidate as published on 12 October.
Overbeck’s X announcement was not retrieved here; issue #557 shows it existed by
16:42:56.

The two reports are of different kinds.
Overbeck’s edition calls itself a “candidate proof, not an established theorem” that
holds if 210 obligations hold, 15 of them mathematical premises (`STATEMENT_STATUS.md`,
as the
[retained packet](../../../packing/resources/web/kleddamag-n17-candidate-2026-10-12/README.md)
records it); two reviews here read it and accepted what they read, and it is registered
as `T-153` at `V0/C1`. Fitzharding’s is a complete proof in the sense that its statement
carries no premise and every step is checked by Lean’s kernel or by native evaluation,
by its own receipt and not yet replayed here.
It is not a formalization of Overbeck’s proof: it proves the same statement by another
route. So Overbeck’s is the first public report of a proof of `s(17) = L`, and
Fitzharding’s the first public report of a complete machine-checked one.

## 6. Replay Price

**Full replay.** From the README (lines 54–86) and the manifest: download the three
archives, 1,962,867,415 bytes, which expand to 6,986,311,712 bytes of Lean source in
3,738 files beside the tree’s 1,215 files (22.5 MB); install Lean 4.34.1 by `elan` with
its C toolchain; `lake exe cache get` for Mathlib `v4.34.1`; run `scripts/unpack.py`
(hash checks), then `scripts/reproduce.py build`, which compiles the five checker
modules to native libraries and elaborates 4,951 modules, finishing with
`REPRODUCTION_ACCEPTED Sq17Lean.Square17Optimality` and the axiom report.
The README suggests `--jobs 40 --proof-jobs 8` and says the replay “requires substantial
CPU time and tens of gigabytes of disk and memory”; the author ran it across two Linux
machines. No CPU or wall time is published.
This host has 4 cores, 15 GB of memory and 18 GB of free disk, which does not hold the
archives, the expanded sources, the Mathlib cache and the build outputs together; the
replay needs a larger machine, and the record would then hold a `replayed-here`
proof-assistant entry with an axiom receipt.

**Cheaper checks that decide something**, in order of cost:

1. Stream-scan the two archives not downloaded here (1.24 GB) as §3.2 did the third: it
   closes the residual point of §1(f) and the keyword scan for the whole release.
   Minutes.
2. Elaborate the statement and the endpoint from the Git tree alone against the pinned
   Mathlib cache: the closures of `SquareBase`, `PropagationWall`, `EndpointRoot` and
   `EndpointGeometry` (at most 20 modules), with a probe that prints the four
   definitions and `#print axioms Sq17.EndpointRoot.unique_root`. It decides that the
   definitions read here are the ones that elaborate, and that the endpoint is proved on
   the standard axioms.
   Toolchain and cache download, then minutes.
3. Build the 18-module closure of `EndpointPacking` (one archived module) and the
   241-module closure of `PackingStatement` (22 archived modules, none using
   `native_decide`), then `lean4checker` over the outputs: a kernel-checked proof of the
   existence half that shares no code with exp-238, and the statement as built.
   Probably under an hour of CPU; not measured.
4. One ordinary case module with the five native libraries, as a pipeline check.
   It decides little about the whole.

The impossibility half is decided only by the full build.

## 7. Findings

None blocks the claim.

| ID | Severity | Where | What |
| --- | --- | --- | --- |
| F-1 | Major (attribution) | `README.md` lines 102–126; `CITATION.cff`; `ExactCellCoverData.lean` lines 1–57; `RepresentativeCaseData.lean` lines 6–42; `EndpointRootData.lean` lines 1–47; `EndpointGeometry.lean` lines 4–40; archived `LocalRigidityWeightData.lean` | The proof runs on this project’s 24-cell cover, cap, census, endpoint chart and layout and local-half recipe, and on 32 patterns of its certified ledger (§4.2), none of which the README or `CITATION.cff` credits; the Squares Project is credited only for collecting “the wider research record”, and wand125’s and Overbeck’s data contributions are not named (§4.6) |
| F-2 | Minor (attribution) | `README.md` lines 107–110 | Ahmed’s n = 11 proof is credited in issue #565 for the proof’s shape, but the README credits his formalization only for “formalization and its trust boundary”; his name is misspelled “Mannaseh” (his handle is ManassehA06) |
| F-3 | Minor (documentation) | `HalfPlaneAssemblySkeleton.lean` lines 7–9, 110; `HalfPlaneFinalAssembly.lean` lines 10–13; `HalfPlaneLastTwo.lean` lines 5–6; `HalfPlaneLastCase.lean` lines 4–5; `CaptureTerminalOptimality.lean` lines 10–12; `ExactCellCover.lean` lines 12–14 | Docstrings describe the earlier conditional state (“no unconditional optimality theorem”, “The only remaining exclusion premise is tree 1563”, the capture trace “is not a Lean theorem”); each is true of its own file, but a reader must follow the chain to `Square17Optimality.lean` and the axiom report to see every premise discharged |
| F-4 | Minor (provenance) | Generated-file headers naming `capture/engine/export_lean_cell_cover.py`, `capture/engine/halfplane_state/build_tree_dispatch.py`, `states/cells.txt`, `root_chart_data.json`, `full_cases.tsv`; `README.md` line 61 | The generators and their inputs are not published. Validity does not need them, since Lean checks every certificate, but the provenance of the data in F-1 cannot be traced from the release |
| F-5 | Note (trust boundary) | `scripts/reproduce.py` lines 18–19, 82–92, 127–128; `HalfPlaneFast.lean` line 243 | The native checks run five modules compiled with `leanc -O3` and loaded by `--load-dynlib`, on certificates decoded from `String` literals at evaluation time; the trusted base includes Lean core’s compiled `String`, `Array` and arithmetic routines and the C compiler (§3.3). Within the README’s stated boundary, but more specific than it |
| F-6 | Note (evidence) | `verification/clean-build-receipt.json`; `README.md` lines 40–48 | The clean rebuild is the author’s, on two of the author’s machines, with digests but no per-module logs, timing, machine description or signature; only the final log is published. It is a producer’s replay report |
| F-7 | Note (independence) | `README.md` lines 119–122; issue #565 | “Developed independently” of Overbeck is consistent with the code (§4.3) but not checkable from a history that begins at the release; the AI systems are named “Claude and Codex” in the README and “OpenAI Astra + Anthropic Opus 5.5” in the post |
| F-8 | Note (citation) | `CITATION.cff`, commits `dc67357` and `e6ee548` | A Zenodo DOI, `10.5281/zenodo.23329216`, was added and then removed “while Zenodo DOI awaits activation”; the record should cite the GitHub release at `0a7167e` until the DOI resolves |

## 8. The Record

These are recommendations; the coordinator registers and the owner decides.

- **Register the Lean proof as its own result**, not as evidence on `T-153`. It proves
  `T-153`’s claim by another route, with another author, so it is neither a replay nor a
  formalization of Overbeck’s proof.
  The two results should cross-reference each other: `T-153` keeps the first public
  report (Overbeck, candidate, 12 October 14:41Z); the new result is the first report of
  a complete machine-checked proof (Fitzharding, 12 October 20:42Z, release 22:06Z). The
  precedent of `E-n011-lean-formalization-report`, evidence on `T-060`, does not fit,
  because Ahmed formalized his own proof.
- **Its evidence now** is the source’s report: a proof-assistant result with a published
  axiom report and the author’s clean-build receipt, not replayed here.
  Under the n = 11 precedent it moves no rung until a replay this record can rest on is
  retained; the cheap checks of §6 are worth running first, and the full build is what
  reaches `C3`. `V5` and `C5` need human formalization reviews, which this is not.
- **The scope line** can use the source’s statement verbatim; §1 found it to be the
  record’s claim, and §2 found `EndpointGeometry.side` to be the record’s $L$.
- **Attribution**: Oscar Fitzharding (GitHub ofitzharding), as the owner directed, with
  the lineage of §4.2 and §4.6 on the credit line, and the AI assistance in the source’s
  words.
- **Case status**: the verified lower bound and `status` stay where they are until a
  replay passes; `reported_status` is already `proved` on `T-153`.

## 9. Questions for the Author

1. `ExactCellCoverData.lean` lines 1–4 and `RepresentativeCaseData.lean` lines 6–42: the
   24 cells are this project’s exp-247 cover vertex for vertex and under its cell names,
   and 32 of the 35 patterns are entries of its certified sub-pattern ledger.
   Were they taken from this repository, and will the README and `CITATION.cff` say so,
   with wand125’s certificates and Overbeck’s September seed?
2. `EndpointRootData.lean` line 3: what is `root_chart_data.json`, and where did its
   60-place midpoint come from?
3. Will the generators named in the generated files, and `states/cells.txt` and
   `full_cases.tsv`, be published, so the data can be traced?
4. `verification/clean-build-receipt.json`: what were the machines, the wall and CPU
   time, and the peak memory and disk, and can the per-module logs be published?
5. The README says the proof was developed independently of Overbeck’s candidate.
   Is there a dated record of the development before 12 October (a private history, a
   timestamp) that could be shared?
6. Will the module docstrings that still describe conditional states (F-3) be updated in
   a later release?

## 10. Checks Made Here

All Python ran under the project interpreter (`packing/.venv/bin/python3 -I`, Python
3.14.7, SymPy 1.14.0) from a scratch directory, reading the clone and the archive as
data; none took more than four minutes.
The programs named below are this lane’s scratch programs; none is retained in the
repository.

- `endpoint_compare.py`: $F$, $G$, midpoint and radius equal exp-237’s and H-255’s
  (`true` on all six comparisons); contraction masses `1.2954e-08`, `7.1236e-09`, slopes
  `1.2958e-08`, `7.1272e-09`; both Newton identities exact; `side` to 60 places
  `4.675530093604550951634111270483146648767143855015879695416889`; residuals
  `6.4e-201`, `8.6e-201`; degree-18 residual `7.8e-191` with a sign change across
  `±10^-40`; the record’s ceiling minus `side` `1.0358e-22`.
- `axioms.py` on the axiom report: 13,346 distinct entries, 3 standard, 13,343
  `._native.native_decide.ax_1_1`, no other, no `sorryAx`; family counts as in §3.1.
  `sha256sum` of the log: `5e74c4af…8ac241`, the receipt’s value.
- `manifest_check.py`: 4,953 sources (1,215 in the tree, 526, 2,832 and 380 in the
  archives), all `ready`; every tree file and top-level file matches its SHA-256; no
  unlisted Lean file.
- `closure.py`: import closures; `PackingStatement` 241 modules (22 archived),
  `EndpointPacking` 18 (one archived), `Square17Optimality` 4,951.
- `gh release download v1.0.0 -p generated-sources.tar.gz`: SHA-256
  `5e0f823f9853b18509f2001e94dab9fea200eaa88bef2dd0b9200c97bd16f029`, the manifest’s
  value and GitHub’s asset digest; `scan_archive.py`: 526 of 526 members, no problem,
  2,316,893,868 bytes; counts as in §3.2. `names_scan.py`: no occurrence of Ahmed,
  MacIver, Overbeck, Kleddamag, jlevy, Ellsworth, Gensane, Guzhou, wand125, Bidwell, an
  `exp-` or `H-` id in any member.
  The archive was then deleted.
- `cells_compare.py`: the 24 Lean cells equal `UNIQUE_24` exactly, 24 of 24, same order
  and names; 0 of 24 equal the three other designs.
- A pattern comparison with `check_n17_capacity_one_cover.d4_permutations`: 32 of 35
  Lean patterns equal admitted entries up to D4; three are subsets of admitted entries.
- GitHub API, with `NO_PROXY` set for `api.github.com`: repository, release, asset,
  commit and event timestamps for both repositories (§5); issues #557 and #565; the user
  records; Lean `v4.34.1` (published 2026-09-24T20:24:21Z) and Mathlib’s tag `v4.34.1` →
  `d13f23b723b8…`, with `Mathlib/Basic/Real/Basic.lean` present.
- The X post from the supplied syndication JSON; its ID’s timestamp decoded to
  2026-10-13T00:06:56.010Z.

Nothing from the clone or the archive was compiled or executed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
