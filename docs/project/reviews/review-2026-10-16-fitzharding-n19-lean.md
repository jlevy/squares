# Fitzharding’s Lean Proof That s(19) = 3 + 4√2/3: Mathematical Review

**Verdict: as read, the proof establishes its statement modulo its trust boundary, and
this review found no blocking or major defect.** Oscar Fitzharding’s theorem
`Sq19.square19_optimality (L : ℝ) : Feasible19 L ↔ 3 + 4 * Real.sqrt 2 / 3 ≤ L`
([sq19](https://github.com/ofitzharding/sq19) v1.0.0 at `34fb2b7`) states the problem
this project poses: nineteen closed unit squares, each translated and rotated freely,
with pairwise disjoint interiors, inside $[0, L]^2$. Existence at the side is
Wainwright’s 1979 packing, which this review decided exactly in $\mathbb{Q}(\sqrt2)$.
Impossibility below it is a chain of six steps (a 25-cell cover with capacity one, a D4
orbit census, sub-pattern exclusions that leave seven survivors, four branch-tree
exclusions, three capture states that confine the packing to a tiny box H around
Wainwright’s configuration, and an exact local endgame on H), and the composition has no
gap: every case of every case split is covered by a theorem, the census is complete, and
no hypothesis remains in the assembly.

The trust boundary is stated once, in full, under The Trust Boundary: Lean’s kernel for
the proofs and, for 4,320 `native_decide` facts, Lean’s compiler and native evaluator,
the C toolchain and Lean core’s compiled runtime.
With programs written for it and none of the source’s checker code, this review
re-established the property each of the 2,328 native facts whose modules are in the Git
tree certifies (all 2,304 endgame cases, the orbit and routing checks, the nine
capture-to-hull checks, the twelve census-to-capture link checks; for the combinatorial
facts, the predicate itself), and the combinatorial content of the census theorem; all
pass. That supports the statement’s truth on those parts; for the endgame and region
facts it is not evidence about the native evaluator’s output (Independent Checks).
The 1,992 facts in the release archives are, apart from the census coverage check,
half-plane propagation traces with their tables, seeds and summaries, checked by the
s(17) proof’s checkers; they were scanned (digests, no `axiom` or other trust-widening
construct) but not re-run.

Nothing here built the proof.
Whether the modules compile, whether the kernel accepts them, and whether the native
facts evaluate to `true` are the author’s report, not this review’s observation.
Three findings are minor (credit for this project’s witness ordering, unpublished
generators and notes, and how the kernel-replay receipt can be stated) and four are
notes. On this review the result the entry PR #651 registers can take C1, by an accepted
adversarial AI review, as the s(17) proof (T-154) did; nothing higher without a build.

Reviewer: Claude, strong sub-agent tier, max reasoning (acting name
`user-eb-review-640`, bead `think-o40t`), the mathematical lane of the #640 import at
stage 4, in a worktree of its own.
It read the source as data and ran only code it wrote, kept in the packet under
[`review/`](../../../packing/resources/web/fitzharding-n19-lean-2026-10-16/review/README.md).
It did not read the two reviews of the s(17) proof until its own findings were written
(section Comparison).
After the pull request’s review A the record was revised in wording (what the
independent checks show, the trust boundary’s single statement, several counts and
paths), and `check_region.py` gained a check that every target polygon is bounded and
nonempty, which passes; no finding, grade or conclusion changed.
It is not a human oversight record.

## Summary for the Author

- The statement is the right one, and the bridge from your set-based `Feasible19` to the
  coordinate form the chain proves is sound (Statement, below).
- `endpoint_packing` is correct; an exact $\mathbb{Q}(\sqrt2)$ check written here
  agrees, with 31 pairs in contact (Endpoint).
- The chain re-derives cleanly.
  The only case splits are the orbit cover, the routing of census representatives, the
  piece split of owner 12’s angle window in each capture state, and the 4,096-case
  endgame encoding; each is complete, and each was re-checked here (Chain).
- Independent checks: the property each of the 2,328 native facts in the Git tree
  certifies holds under programs written here; the endgame’s inequalities hold with room
  (multipliers at least 0.70, $S_1 \ge 1.49$, slopes at least 0.038 over all of H), and
  the endpoint margin is exactly zero at Wainwright’s configuration, as it must be.
  The census theorem’s combinatorial content holds if each pattern’s roster is the mask
  its name encodes (question 4).
- Requests: say where `s19/data/packing_exact.json` came from and credit this project’s
  witness if it is the source (N19-1); publish `s19/tools/`, `s19/data/`,
  `LOCAL_THEOREM.md` and `ENDGAME.md`, or a written account of the argument (N19-2);
  publish the replay’s closure list and log and say which build it ran on (N19-3).

## Scope and Evidence

Read closely: `Basic.lean`, `SquareBase.lean`, `Assembly/` (all ten modules), `Cover/`
(statements and the finite data; the capacity lemmas at statement level), `Census/`,
`Survivors/`, `Capture/` (all hand-written modules and `Region.lean`’s data), `Endgame/`
(the reduction interface, the row and multiplier definitions, the derivative check),
`Milp/Problem.lean` and `SoundRows.lean`, the endgame certificate assembly, `scripts/`,
`expected/` and `verification/`. Read by structure and sample: the three large
`Wedge/Offset*.lean` identity files, `Cover/OrbitData.lean`, the 72 endgame shards and
64 assembly blocks, and from the release archives the S3435, S3438 and S3442 state data
(`Common.lean`, the piece tables and data files).

The source is the retained packet
[`fitzharding-n19-lean-2026-10-16`](../../../packing/resources/web/fitzharding-n19-lean-2026-10-16/README.md),
byte-identical to the pin.
The three capture-state archives were downloaded on 16 October 2026, each checked
against `SHA256SUMS` (whose digest the packet records), and their members against
`expected/generated-sources.sha256`; all five archives were then downloaded to scratch
one at a time, scanned and deleted (Independent Checks).

**Not done here:** no Lean toolchain is installed, and the full build is 190 to 420
CPU-hours and hundreds of gigabytes (held as `think-nqnl`). No module was compiled, no
`#print axioms` was run, and the kernel replay was not repeated.
The sq17-lean checker modules the proof compiles in place were not re-reviewed; their
soundness theorems are cited from the two s(17) reviews (Comparison).

## The Statement

`Feasible19 L` (`Sq19Lean/Assembly/PlainPacking.lean:11-15`) asks for
`S : Fin 19 → Set (ℝ × ℝ)` with each `S i` an `IsUnitSquare`, every point of `S i` in
$[0, L]^2$, and `Disjoint (interior (S i)) (interior (S j))` for $i \ne j$.
`IsUnitSquare S` (`SquareBase.lean:20-21`) is `S = sq cx cy ux uy` with
$u_x^2 + u_y^2 = 1$, and `sq` (`SquareBase.lean:16-17`) is the closed set
$\{p : |(p - c)\cdot u| \le 1/2,\ |(p - c)\cdot u^\perp| \le 1/2\}$, the closed unit
square with centre $c$ and side direction $u$. Rotations are arbitrary, touching is
allowed, and the container is axis-aligned.
`side19 = 3 + 4 * Real.sqrt 2 / 3` (`Basic.lean:7`) is the case record’s exact upper
bound $3 + (4/3)\sqrt2$ (`packing/frontier/n-019.md`). For $L < 0$ both sides are false,
so the equivalence has no degenerate reading.
`expected/statement.txt` and the logged `#print` of the four definitions
(`verification/Square19Optimality.log.gz`, first lines) agree with the sources.

`sq` and `IsUnitSquare` are textual copies of `Sq17Lean/SquareBase.lean:13-18` (compared
here), and the bridge `feasible19_iff_of_lower` (`PlainPacking.lean:25-47`) rewrites
`Sq19.sq` to `Sq17.sq` by unfolding (line 31) and the subset condition to
`containerBox L` (line 34, definitional).
Its forward direction needs exactly `CoordinateLowerBound19` (lines 17-23), which
`Assembly.side19_le` supplies with no hypothesis (`Assembly/Concrete.lean:31-47`); its
backward direction widens `endpoint_packing`’s container from `side19` to `L`.
`square19_optimality` (`Optimality.lean:9-11`) is that bridge applied.
The statement binding holds.

## The Endpoint Packing

`EndpointPacking.lean` defines S0 to S18 (lines 10-66): eleven axis-parallel squares and
eight at 45°, every coordinate in $\mathbb{Q}(\sqrt2)$, and proves containment (`cont*`)
and pairwise separation (`disj*`, one `halfplane_disjoint` per pair, with a separating
functional and the support bounds `axis_le` and `diag_le`), by `norm_num` and `linarith`
with $\sqrt2$ as an atom.
The file has no `native_decide`.
[`check_endpoint.py`](../../../packing/resources/web/fitzharding-n19-lean-2026-10-16/review/check_endpoint.py)
parses the nineteen definitions as data and decides, in exact $\mathbb{Q}(\sqrt2)$
arithmetic, that each direction is a unit vector, each square lies in
$[0, \mathrm{side19}]^2$ (clearance 0: squares touch the walls), and each of the 171
pairs is weakly separated by an edge normal; 31 pairs touch on their best axis.
The upper half of the theorem is correct, independently of the trust boundary.

## The Impossibility Chain Re-derived

Assume nineteen squares in $[0, L]^2$ with $L < \mathrm{side19}$; then
$L < 2443/500 = 4.886$ (`Assembly/Final.lean:13-17`).

**Step 1: an injective cell assignment** (`Cover/Reduction.lean:67-85`). The packing is
shifted concentrically into the frame $[0, U]^2$, $U = 2443/500$; every centre then lies
in the centre box $[1/2, 2193/500]^2$ (`shifted_centre_in_box`, from the support
$h = (|u_x| + |u_y|)/2 \ge 1/2$). The 25 cells cover that box (`CoverBox.lean:25-40`,
slab certificates checked by `decide +kernel`), and no cell holds two centres
(`Capacity.lean:189-205`): the nine interior cells have squared diameter at most
$15488/15625 < 1$, so two centres in one would be closer than 1 and the inscribed disks
would overlap; each of the sixteen wall cells, moved by a frame symmetry, fits the
window of `corner_capacity` or `side_capacity`, two lemmas proved in the kernel
(`CornerCapacity.lean`, `SideCapacity.lean`; read at statement level).
Choosing a cell per square is therefore injective.
Here, the 25 cells were shown to tile the box exactly (convex, inside it, pairwise
interior-disjoint, areas summing to $(1943/500)^2$), and the capacity data were
re-derived.

**Step 2: the orbit census** (`Cover/Orbit.lean:176-237`). One of the eight frame
symmetries maps the 19 occupied cells onto a mask in `censusMasks`, the 22,475 census
representatives (`orbit_check`, one native fact over all 177,100 nineteen-cell sets).
The symmetry tables are induced by the geometric action on cell vertices
(`vertex_action_checked`). Re-evaluated here: every set reaches a representative, and
the list holds exactly one mask per D4 orbit (22,475 orbits).

**Step 3: census exclusions** (`Census/Pattern.lean`, `Assembly/CensusRoute.lean`). A
census exclusion says that no assignment covering the cells of a mask packs in the
larger container $[0, 2443/500]^2$ (`Packs`, `Pattern.lean:18-25`): a stronger statement
than needed, since $2443/500 > \mathrm{side19}$. A certified pattern is an injective
cell list with `¬ Packs`, from a half-plane trace certificate (`not_packs_of_trace`);
its symmetry images and supersets inherit the exclusion (`not_packs_of_witness`, lines
111-119). The generated `Census.Complete.census_excluded` must have the type
`CensusExclusion` (`CensusRoute.lean:14-19`): every 19-cell mask other than the 38
symmetry images of seven survivors is excluded, with an empty exception list.
`Concrete.lean:15-16` applies it by definitional equality, so the count, survivor list
and exceptions cannot drift between the generator and the assembly.
`route_checked` (`CensusRouteData.lean:45-49`) routes each representative to an
exclusion, a tree mask or a capture mask.
Re-derived here: the 38 images are exactly the D4 orbits of the four tree masks and
three capture masks; the routing and capture-index facts hold; and, reading each of the
269 certified patterns’ cells from its name, every non-survivor mask (177,062 of them)
contains a symmetry image of a pattern while no survivor image does, so the census is
complete and tight.

**Step 4: four survivors by branch trees** (`Survivors/Dispatch.lean:11-61`). Census
indices 1, 2, 5423 and 5453 carry full nineteen-cell rosters with `¬ Packs`, proved by
generated branch trees (in the archives); `tree_excluded_perm` extends each to its eight
images.

**Step 5: three capture states into H** (`Capture/`). For census indices 3435, 3438 and
3442 (pinned by `captureIndex_checked` and `full_route`), and $L \le$ the capture side
$\mathrm{side19} + 10^{-12}$ (`Capture/Final.lean:97-101`), `census_capture`
(`CensusCapture.lean`) reflects the packing, relabels it in owner order and translates
it by $-\sigma$ into the state’s trace container (`StateFacts.lean`: the state’s cells
are the census cells shifted by $-\sigma$, and the reflected roster is the census mask).
Each state gives every square a pose with angle in a base window of width at least
$\pi/2$ (`width_checked`), splits owner 12’s window into pieces that tile it
(`tile_checked`; at 41.5°, 44.5° and 45.5° in 3435 and 3442, one piece in 3438), and for
each piece either excludes it by a propagation trace or captures every pose into its
targets (`S3442/State.lean`). The targets lie in the hull box H of `Hull.prob` after the
frame shift (`Region.lean`, `sqCheck` and `wallCheck`), and 3435’s piece P0 does so
through the anti-diagonal mirror (`ToHullMirror.lean`, `topCheck`). The output is
`Good Hull.prob θ dx dy L` (`Milp/SoundRows.lean:14-24`): nine squares (the witness’s
squares 1, 2, 5, 7, 8, 10, 11, 13 and 14) with angles and offsets in H, inside
$[0, L]^2$, pairwise disjoint.
Checked here: the property the nine region facts certify, the twelve link facts’
predicates, and that Wainwright’s configuration lies in H (margin $7.0 \times 10^{-5}$).

**Step 6: the endgame on H** (`Endgame/`, `s19/certificates/endgame_reduction/`). A
`Good` configuration matches one of 4,096 sign, owner and ordering cases
(`exists_matching_case`, `ReductionRows.lean:39`; the encoding is exhaustive by an
arithmetic proof, `ReductionEncodingPure.lean:18-47`). For the matching case three rows
P, Q, F hold; if their Farkas multipliers are nonnegative and $S_1 > 0$ on H
(`geometryCheck`), then $L \ge -S_0/S_1$ (`Combine.lean`), and $L \ge \mathrm{side19}$
follows from the endpoint margin $-S_0 - \mathrm{side19}\, S_1 \ge 0$
(`AngleReduction.lean:265-279`). The margin is nonnegative on the face where the five
moving angles are zero by exact identities in the kernel (`ReductionBase.lean:37`,
`ZeroRowIdentity.lean`, the `Wedge/` files), and nondecreasing along the case’s five
direction prefixes by the derivative check (`slopeCheck`), so it is nonnegative on the
case’s cone. The 2,304 canonical cases are native facts; the other 1,792 reduce to them
(`check_of_normalize`, `ReductionDedup.lean:42`). The property they certify was decided
here for all 4,096 cases (Independent Checks).

**Composition.** `side19_le_of_routes` (`Assembly/Final.lean:19-53`) splits on whether
the reached mask is excluded; if not, `full_route` puts its index among the three
capture states, and `hcap` (`Capture/Hcap.lean`) closes each.
`Concrete.lean` supplies every argument by a theorem.
Every split above is total: the orbit check covers all nineteen-cell sets, the routing
covers all representatives, the piece split tiles owner 12’s window and the base windows
give every square a pose, and the endgame encoding is onto.
No case is left to an unproved hypothesis.

## The Trust Boundary

This is the boundary everywhere this review refers to it.
The proofs rest on Lean’s kernel.
The 4,320 `native_decide` facts rest also on Lean’s compiler and native evaluator, on
the C toolchain that compiles the six checker modules into the library loaded with
`--load-dynlib`, and on Lean core’s compiled runtime routines, among them the `String`
routines that decode certificate data such as `censusMasks` at evaluation time, which
the kernel never sees.
The source states the kernel, compiler, native evaluator and C toolchain; the runtime
and `String` point is the first s(17) review’s, adopted here after the comparison
(Comparison).

`verification/Square19Optimality.log.gz` and `expected/axioms.txt.gz` list the same
4,323 axioms: `propext`, `Classical.choice`, `Quot.sound` and 4,320 facts named
`…_native.native_decide.ax_1_1`, and no `sorryAx` (counted here).

| Family | Facts | Where | Checker kind |
| --- | ---: | --- | --- |
| `Sq19.Endgame.Reduction.Shard*` | 2,304 | Git tree | Taylor-form interval checks (`Milp/`) |
| `Sq19.Census.P*`, `Census.Complete.all_ok` | 1,077 | archives | 269 patterns × (seed, table, owners, trace exclusion), and the coverage check |
| `Sq19.Capture.*` | 688 | 21 in the tree, 667 in archives | propagation runs, tables, seeds, summaries; region and link checks |
| `Sq19.Survivors.*` | 248 | archives | branch-tree traces, split covers, tables, seeds |
| `Sq19.Cover.orbit_check` | 1 | Git tree | combinatorial |
| `Sq19.Assembly.CensusRoute.*` | 2 | Git tree | combinatorial |

So 2,328 facts sit in the Git tree and 1,992 in the release archives, which
`expected/generated-sources.sha256` pins file by file.

`scripts/verify.py` compiles six checker modules to C and links them into one library
(lines 28-29, 131-140), and compiles every certificate-level module with `--load-dynlib`
(line 103), so `native_decide` runs that C code.
Its resume stamp binds each compiled module to the SHA-256 of its source and of the
library (line 101), and it refuses checker modules that depend on generated code.
The five sq17-lean `*Fast` modules (fetched here at `0a7167e`) and
`Capture/SummaryFast.lean` import only Lean core and contain ordinary definitions; none
of the sources read here, retained or archived, uses `implemented_by`, `extern`,
`unsafe`, `opaque` or an `axiom` declaration, so the compiled code implements the same
definitions the kernel sees, up to the compiler.
`#print axioms` reports names only, so a hand-written axiom with a native-looking name
would be indistinguishable in the log.
`scan_archives.py` streamed all five archives (2,112 members, 10.2 GB of Lean source):
each archive’s SHA-256 equals `SHA256SUMS`, every member equals its line of
`expected/generated-sources.sha256` and none is unlisted, and no member declares an
`axiom`, uses `sorry`, `admit`, `implemented_by`, `extern`, `unsafe`, `opaque`,
`skipKernelTC` or a `debug.` option, or defines a command, macro or elaborator.
`count_native.py` then finds each of the 4,320 logged facts as a theorem proved
`by native_decide`, none missing: 2,328 in the Git tree and 1,992 only in the archives.
Six of the tree facts are also in the archives, whose copies of the three capture
`State.lean` files are byte-identical to the tree’s. It also finds 170 native theorems
that the final theorem does not use (169 survivor-tree `owners_eq` facts and
`capture_indices`).

## Independent Checks

All programs are in
[`review/`](../../../packing/resources/web/fitzharding-n19-lean-2026-10-16/review/README.md),
standard library only, run with the project interpreter under `python -I`, reading the
sources as data.

| Program | What it decides | Result |
| --- | --- | --- |
| `check_endpoint.py` | the endpoint packing in exact $\mathbb{Q}(\sqrt2)$; order and values against this project’s witness | pass; 31 contacts; same order, $4.4 \times 10^{-16}$ |
| `check_cover_census.py` | tiling, symmetry tables, capacity data, `orbit_check`, `route_checked`, `captureIndex_checked`, survivor images, census coverage | 21 checks pass |
| `check_region.py` | the property the nine `Region.*` facts certify: the source’s `sqCheck` and `wallCheck` (`Capture/ToHull.lean:52-59`) transcribed, with `impliedOK` replaced by vertex enumeration of each target polygon, all 76 checked bounded and nonempty | 9 pass; 76 bounded; Wainwright in H |
| `check_capture_link.py` | `cells_ok`, `mask_ok`, `width_checked`, `tile_checked` for 3435, 3438, 3442, with their data from the archives | 12 pass; digests match |
| `check_endgame.py` | the property `geometryCheck` and `slopeCheck` certify, for all 4,096 cases, with its own first-order Taylor models | 4,096 pass |
| `scan_archives.py` | each archive’s digest and members, trust-widening constructs, native theorems | five archives, 2,112 members: digests match, none unlisted, no forbidden construct |
| `count_native.py` | where each of the 4,320 logged native facts is proved | 2,328 in the tree, 1,992 in the archives, none missing |

The endgame program transcribes the row definitions (`RowsH.lean`, `RowsAH.lean`,
`PhiExpr.lean`, `Combine.lean`, `ReductionCases.lean`) and evaluates them with its own
rigorous arithmetic: fixed-point outward rounding at $2^{-160}$, the quarter-turn values
exactly, $|\sin x - x| \le |x|^3/6$ and $1 - x^2/2 \le \cos x \le 1$, and forward-mode
differentiation for the slopes.
Over H the multipliers are at least 0.701147, 0.7009 and 0.999596, $S_1$ at least
1.49126, and every directional derivative at least 0.0383454 (the program’s printed
lower bounds); no `abs` operand moves along a direction, so the source’s `smoothAlong`
holds. The margin at $\theta = 0$ is zero to $10^{-46}$ in every case, which is the
tightness of Wainwright’s packing; on the axis-zero face a first-order bound is
$-0.0076$, which is why the source proves that face exactly rather than by intervals.
25,564 random points of the cases’ cones gave a smallest margin of $1.2 \times 10^{-4}$
in floating point. A natural interval extension (without Taylor forms) failed the slope
check in 3 of 10 trial cases, by dependency; the first-order models removed that.
`check_region.py` likewise transcribes the source’s `sqCheck` and `wallCheck` line for
line and replaces only `impliedOK`. Both programs are independent of the source in
evaluation, not in formulation.

**What a pass shows.** For the combinatorial facts (`orbit_check`, `route_checked`,
`captureIndex_checked`, `cells_ok`, `mask_ok`, `width_checked`, `tile_checked`) the
programs decide the same finite predicate the Boolean encodes, so a pass is close to a
re-evaluation of the fact.
For the 2,304 endgame facts and the nine region facts they decide the property the
Boolean certifies (multipliers nonnegative, $S_1 > 0$ and slopes nonnegative on H; each
target inside its box), not the Boolean itself, `checkNat n =
true` or `sqCheck … = true`. A pass there shows that the certified property holds, so a
wrong native result among those facts would not make the statement false.
It shows nothing about whether the native evaluator’s `true` is the kernel’s value: if
the source’s Taylor-form checks or its `impliedOK` evaluated to `false` in the kernel
while the compiled code returned `true`, the formal proof would rest on a false axiom
and both programs would still pass.

Not re-evaluated: the 1,992 archived facts, that is the census pattern traces, the
capture propagation runs and tables, and the survivor trees, which need a
reimplementation of the s(17) half-plane checker, and `Census.Complete.all_ok`, whose
content Step 3 re-derived from the pattern names.
The twelve link facts are tree facts (of the 21 capture facts in the tree); only their
data come from the archives.

## Provenance and Credit

`EndpointPacking.lean:4-6` says the packing was generated from
`s19/data/packing_exact.json` “(T1)”, and its docstrings number the squares “Square 1 of
the record” to “Square 19 of the record” (lines 9-66). The nineteen squares, in that
order, are this project’s known-best witness `W-known-best-n019`
(`packing/witnesses/known-best/n-019.yaml`), itself derived from the Kingbird
catalogue’s SVG; the hull problem’s record numbers 1, 2, 5, 7, 8, 10, 11, 13 and 14
(`Capture/ToHull.lean:7`, `Endgame/HullData.lean`) use the same numbering.
The README thanks the Squares Project generally.
No other use of this project’s $n = 19$ material was found: the record’s $n = 19$ work
is lower-bound grids and nets, and its cover constants (the frame $2443/500$, the 25
cells, the census) appear nowhere in this repository outside the packet.
This is a smaller debt than the s(17) proof’s use of the $n = 17$ plan (T-154), and it
is a credit question, not a correctness one.

## What the Record Can State

- **The theorem and its trust boundary:** as the source states them, confirmed here by
  reading.
- **The kernel replay** (README lines 18-19, `verification/kernel-replay.json`): only as
  the author’s report.
  The receipt says it ran on “compiled objects of the research build of 15 October 2026”
  (line 23), and the 16 October smoke test (line 25) does not say whether its build was
  fresh; the closure list is published only as a SHA-256 (line 6); 13,144 is the closure
  of `FinalReport`, 13,143 that of `Optimality`. A replay takes the native facts as
  axioms, so it rules out elaborator-level defects, not compiler ones.
- **Reproducibility:** the record can say the proof is reproducible from published
  sources by the published script, by the author’s account, and that a from-scratch run
  has not yet happened.
  It cannot say the certificates are regenerable: the generators are not published
  (N19-2).

## Findings

| Id | Grade | Where | Finding |
| --- | --- | --- | --- |
| N19-1 | minor | `EndpointPacking.lean:4-66`; `Capture/ToHull.lean:7` | The endpoint data and the square numbering are this project’s witness `W-known-best-n019` (from Kingbird’s SVG), in the same order; the source of `packing_exact.json` is not stated and the witness is not credited. |
| N19-2 | minor | comments in `Census/Cells.lean:3-4`, `Cover/OrbitData.lean:3-4`, `Capture/Region.lean:3-4`, `Endgame/HullData.lean:3`, `Combine.lean`, `Separations.lean` | The generators (`s19/tools/`: `census.c`, `milp_cert.c`, `produce19c.py`, `produce19k.py`, `gen_*`), their data (`s19/data/`) and the notes `LOCAL_THEOREM.md` and `ENDGAME.md` are cited but not published. Soundness does not depend on them; the certificates cannot be regenerated, and no written account of the argument exists. |
| N19-3 | minor | `verification/kernel-replay.json:4,6,23,25`; `README.md:18-19` | The replay receipt binds to an unpublished build; its closure list and per-module log are not published; the README states the replay without that qualifier. |
| N19-4 | note | `Optimality.lean:4-6`; `Assembly/Final.lean:8-9`; `Capture/Final.lean:105-151`; `CensusRouteData.lean:57-60` | Stale development text (“Do not describe this as verified until…”, “a separate file on the build machine”), an unused alternative assembly `lower_bound_from_capture`, and 170 native theorems the final theorem does not use (`capture_indices` and 169 survivor-tree `owners_eq` facts). Harmless. |
| N19-5 | note | `scripts/verify.py:101-103` | The native facts run compiled C loaded with `--load-dynlib`; the stamp scheme is sound, and the trusted base includes Lean’s IR-to-C compiler and the C toolchain, as the source says. |
| N19-6 | note | archives, `Census/Pat/` | Each census pattern’s name encodes a cell mask; this review’s coverage check assumes the roster is that mask (question 4). |
| N19-7 | note | `Census/Pattern.lean:18-25`; `Capture/Final.lean:97-101` | Census exclusions hold in $[0, 2443/500]^2$ and capture at $\mathrm{side19} + 10^{-12}$: margins in the right direction, worth one sentence in a write-up. |

No finding is blocking or major.

## Questions for the Author

1. Where does `s19/data/packing_exact.json` come from, and what is “T1”? If it is this
   project’s witness `W-known-best-n019` (or the Kingbird SVG it was taken from), would
   you credit it in the README and `CITATION.cff`?
2. Will you publish `s19/tools/` and `s19/data/`, with `LOCAL_THEOREM.md` and
   `ENDGAME.md`, or a short written account of the cover, census, capture and endgame?
3. Would you publish the replay’s closure list (SHA-256 `b301d93e…`), its per-module
   log, and the build stamps of the build it ran on, and say whether the 16 October
   smoke test started from a clean build?
4. Is each census pattern `P<hex>`’s roster exactly the cells of the mask `0x<hex>`?
5. Has the from-scratch `scripts/verify.py` run since the release?
   Its log would let the record cite a build that starts from the published bytes.

## What Depends on the Build

This review’s verdict is about what the sources say.
These conclusions rest on the author’s build and replay, not on anything observed here:
that every module compiles at Lean 4.34.1 against Mathlib `v4.34.1` and sq17-lean
`0a7167e`; that each kernel-checked lemma (the capacity lemmas, the slab cover, the
endgame identities, every soundness theorem) is accepted; that each of the 4,320 native
facts evaluates to `true`, including the 1,992 not re-evaluated here; and that the final
axiom set is the one logged.
The independent checks of the 2,328 tree-resident facts show that the property each
certifies holds, so a wrong native result among them would not make the statement false.
For the combinatorial facts they also show what the Boolean’s value is; for the 2,304
endgame facts and the nine region facts they say nothing about the native evaluator’s
output, and a formal proof resting on a false axiom there would still pass them
(Independent Checks).
They do not replace the build.

## Comparison with the Two s(17) Reviews

Written after the findings above, which were not changed by what follows, with two
exceptions stated here.
The comparison’s commit (`8cd4c2c2d`) also edited the opening’s description of the
archived facts, adding the census coverage check and the tables, seeds and summaries; it
brought the opening in line with the family table under The Trust Boundary, which
already listed them in the draft committed before the reading (`7ce9b69a8`), so it did
not come from the reading.
And after the pull request’s review A, The Trust Boundary took in the first s(17)
review’s runtime and `String` point described below, attributed there.
This review read the first s(17) review
([adversarial, 13 October](review-2026-10-13-fitzharding-n17-lean.md)) at its summary,
trust-boundary, lineage and findings sections, and the second
([mathematical correctness](review-2026-10-13-fitzharding-n17-mathematical-correctness.md))
at its summary, checker-soundness step, trust-boundary and defects sections, and only
after the findings and the re-evaluation above were committed.

**The reused checkers.** The s(19) proof’s census patterns, survivor trees and capture
states are checked by the s(17) half-plane checker, compiled in place from sq17-lean
`0a7167e`. The second review read its soundness modules in full and found them sound:
`run_sound`, `runAll_sound` and `excludes_sound` (`HalfPlaneStateSound`), the seeds
(`stateSeedOK_sound`, `windowSeedOK_sound`), checkpoints (`coverCheck_sound`), branch
trees (`tree_excluded`), chunk composition (`runToCheck_eq`, `CaptureTableSound`) and
the summary check (`summaryCheck_sound`), with the separating-axis collision test used
only in the sound direction and boundary contact not a collision.
This review relies on that reading for the 1,992 archived facts and did not repeat it.
Its MR-3, that `rowCheck` accepts a row whose entry index lies outside the table and
that the soundness lemma covers it, carries over unchanged, since
`Capture/SummaryFast.lean`’s `summaryCheckN` calls the same `rowCheck`.

**The trust boundary.** Both s(17) reviews state the boundary as the kernel, Lean’s
compiler and C toolchain for the `*Fast` modules loaded with `--load-dynlib`, and Lean
core’s compiled runtime routines; this review had stated all but the runtime.
The first review adds a point this review had not stated: certificate data decoded from
`String` literals at evaluation time are never seen by the kernel, so the compiled
`String` routines are trusted too.
That holds here: `censusMasks` is parsed from a hex string
(`Cover/OrbitData.lean:29-36`), and this review’s re-evaluation decoded it independently
and found 22,475 distinct nineteen-cell masks.
The second review’s question 4, whether the build checks that the loaded libraries were
compiled from the pinned sources, has a partial answer here: `verify.py` builds the
library in the same run and stamps every module compiled against it with the library’s
SHA-256 (line 101).

**Where the s(19) proof differs.** The local endgame is new: a Farkas combination of
three trigonometric rows with Taylor-form interval checks and a derivative check, and an
exact proof on the axis-zero face, where the s(17) proof had a 93-box dual certificate
proved by `decide +kernel`. Its 2,304 native facts are more than half the total, are
outside both s(17) reviews, and the property each certifies was checked here.
The capacity lemmas for wall and corner cells, the capture-to-hull step and the census
bridge are also new and were read here.
The second review replayed ten half-plane facts with its own re-implementation of the
compiled checker; this review replayed none of that kind, so the two reviews together
cover different checker kinds, and the archived half-plane facts of the s(19) proof
remain the least independently checked part of it.

**Credit and evidence.** The first review’s F-1 (major, attribution) found that the
s(17) proof ran on this project’s $n = 17$ plan and data; for $n = 19$ only the
witness’s square order is shared (N19-1, minor).
Its F-4 (unpublished generators), F-6 (a producer’s replay report) and F-3 with the
second review’s MR-1 and MR-2 (stale docstrings, unused modules) recur as N19-2, N19-3
and N19-4. The s(17) source carried a clean-build receipt (4,951 modules rebuilt, no
prebuilt project objects); the s(19) source has none, and says its from-scratch build
has not run, so the evidence for the build is weaker here than it was for s(17) when it
took C1. Its F-2 noted the misspelling of Manasseh Ahmed’s name; the s(19) README spells
it correctly and links the GitHub account `Queuingtheorydotcom`, which the records lane
may wish to check against the record’s credit for him.

## For the Records Lane

- **Confirmation:** this review is a qualifying adversarial AI read of the statement,
  the endpoint, the chain and the trust boundary, with independent checks of the
  properties the 2,328 tree-resident facts certify; it supports C1 for the result the
  entry PR #651 registers, as the s(17) proof took C1. Nothing higher: C3 and V3 need a
  complete build the record can rest on (`think-nqnl`).
- **Verification:** unchanged at V0; no build is retained.
- **Significance:** no reason found to change the draft S5.
- **Evidence and verifiers:** the seven programs are candidates for `verifiers.yaml`
  entries (independence: written here, sharing no code with the source; the endgame
  program transcribes the source’s row definitions and `check_region.py` its `sqCheck`
  and `wallCheck` by hand, so both are independent in evaluation, not in formulation),
  and their receipts for evidence entries on the source-report evidence entry PR #651
  registers. An evidence entry’s coverage should follow What a pass shows (Independent
  Checks): for the endgame and region facts, the certified property, not the native
  result.
- **Credit:** N19-1 is drafted to the author in question 1; it needs no record change.

## Verdict

As read, `Sq19.square19_optimality` proves that nineteen unit squares fit in a square of
side $L$ exactly when $L \ge 3 + 4\sqrt2/3$, with arbitrary rotations and touching
allowed, modulo the trust boundary stated under The Trust Boundary (the kernel, and for
4,320 finite facts Lean’s compiler and native evaluator, the C toolchain and Lean core’s
compiled runtime) and modulo the build and kernel replay the author reports.
No blocking or major defect was found; the record may take C1 on this review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
