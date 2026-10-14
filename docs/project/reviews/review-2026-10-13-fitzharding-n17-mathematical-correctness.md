# Fitzharding’s Lean Proof of s(17) = L: Mathematical-Correctness Review

**Verdict: accepted.** No blocking or major defect was found in what was read, and
nothing read was found false.
The theorem
`Sq17.square17_optimality (L : ℝ) : PlainPacking L ↔ EndpointGeometry.side ≤ L` states
the right thing: seventeen closed unit squares, each with its own direction, pairwise
disjoint interiors, boundary contact allowed, inside the closed box $[0, L]^2$, and
`side` is the exact algebraic endpoint $(6 + 4t)/(1 + 2t - t^2)$ at a root certified by
a kernel-checked contraction, not a decimal.
The proof establishes it up to the one trust boundary the author declares: 13,343
Boolean facts proved by `native_decide`, each of which the kernel takes as its own axiom
and the compiled Lean evaluator vouches for.
Everything from those facts upward, the geometry of the half-plane trace checker
included, is kernel-checked on `propext`, `Classical.choice` and `Quot.sound`, with no
`sorry`, and no `implemented_by`, `extern`, `unsafe`, `opaque`, `partial` or `axiom`
declaration anywhere in the project sources.

This review read the whole hand-written part of the development (about 140 modules, the
checker-soundness modules in full) and sampled the generated certificate sources from
the release archive, and it re-derived with its own code what the claims turn on: the
endpoint root and the frame margins; the D4 action, the 43,593 orbit representatives,
the 346,104 census rows, the 35 patterns and 2,781 full rosters and the classifier tree
that routes them; the cell cover, the interior-cell diameters and the wall-cell
capacities; the 93-box dual certificate of the 52-row local model, exactly; and the
compiled checker itself, re-implemented from the Lean text and replayed on one branch
node (14,851 steps), six chunk runs of the thin-margin neighbour and the capture (27,905
steps, final states equal to the declared ones to the bit), two degree-44 table checks
and the terminal summary check.
Every replay agreed with the recorded fact, and corrupted inputs were rejected.

Six findings are recorded, none blocking and none major: stale docstrings that still
call the development conditional, modules in the build that the theorem does not use, a
summary checker that accepts a malformed row by design (the soundness lemma covers it),
a provenance note on three artefacts that coincide with this project’s, and two
clarifications. What was not reached is listed below: no Lean was run here, 2,775 of the
2,776 ordinary traces and all but six of the 273 chunk runs were not replayed, and the
compiled shared libraries were not compared with their sources.

Reviewer: an AI agent, the mathematical-correctness lane of the sq17-lean intake, a
Claude model at the tbd-strong-max tier, reasoning max, prompted separately from the
first review lane and blind to its document and to the register entries until its own
findings were written; the comparison section at the end was added afterwards.

It registers nothing and moves no rung.
It is not a human oversight record.

## Scope and Evidence

The subject is the repository `sq17-lean` at its head commit `e6ee548`, cloned read-only
into the scratch directory, together with the release archive
`certificates/generated-sources.tar.gz` (718,897,665 bytes, SHA-256
`5e0f823f9853b18509f2001e94dab9fea200eaa88bef2dd0b9200c97bd16f029`, equal to the digest
in `manifest.json` and to the GitHub release digest), and the project’s retained packet
`packing/resources/web/fitzharding-n17-lean-2026-10-13/README.md`. The toolchain is Lean
4.34.1 with Mathlib at `d13f23b7`; the author’s `verification/clean-build-receipt.json`
and `verification/Square17Optimality.log` were read as data.
Nothing of the author’s was executed: no `lake`, no Lean, none of the scripts.
Lean is not installed here and the brief forbids installing it.
Every check below is a script written for this review, run with the project interpreter
(`python3 -I`, Python 3.14) on copies of the source files passed as arguments.

Read in full, in the hand-written tree: the statement and assembly (`SquareBase`,
`PackingStatement`, `Square17Optimality`, `HalfPlaneAssemblySkeleton`,
`HalfPlaneFinalAssembly`, `HalfPlaneLastTwo`, `HalfPlaneLastCase`, `HalfPlaneFullRoute`,
`HalfPlaneNeighbourDispatch`, `HalfPlanePatternDispatch`, `HalfPlaneDispatch`,
`HalfPlaneCases/Ordinary` head, `OrdinaryIndices`); the endpoint (`EndpointRoot`,
`EndpointRootData`, `PolynomialNewtonRoot`, `PolynomialBoxContraction`,
`EndpointSideSharp`, `EndpointRootSharp`, `RationalExpression`, `EndpointIntervals`,
`EndpointGeometry`, `EndpointPacking`, `EndpointContacts`, `EndpointSupport`,
`EndpointAngles`, `EndpointAngleBounds`, `ArctanCheck`); the reduction
(`PropagationWall`, `CenteredOrbitFrame`, `OrbitCellAssignment`,
`OrbitPackingReduction`, `PackingCellReduction`, `PackingSubfamily`, `ExactCellCover`,
`CellCoverCertificate`, `CellCoverGeometry`, `InteriorCellCapacity`,
`ExactWallCapacity`, `WallCapacityRectangle`, `WallCapacityBounds`,
`WallCapacityObstructions`, `WallMixedSupport`, `WallSquareSupport`,
`WallSquareSymmetry`, `SquareSupportSeparation`, `SquareSeparationGeometry`,
`SquareSeparationFinite`, `SquareSeparationAxes`, `CoreSeparationGeometry`,
`CoreSeparationAxes`, `FiniteOrbitCoverCheck`, `FiniteAffineBounds`, `CellPermutation`,
`CellSymmetry`, `CellSymmetryBridge`, `OrbitCensus/Complete`, `RepresentativeCaseData`,
`RepresentativeCaseCheck`, `RepresentativeCaseParts/All`); the checker and its soundness
(`HalfPlaneInt`, `HalfPlaneState`, `HalfPlaneStateSound`, `HalfPlaneFast`,
`HalfPlaneTable`, `HalfPlaneTree`, `HalfPlaneCells`, `HalfPlaneCover`,
`HalfPlaneCoverFast`, `HalfPlaneSeed`, `HalfPlaneWindowSeed`, `HalfPlaneRosterSeed`,
`HalfPlaneFrameBounds`, `HalfPlaneBranchComposition`, `HalfPlaneChunkComposition`,
`HalfPlanePrototype`, `HalfPlanePositiveControl`, `HalfPlaneBoundaryControl`,
`PropagationSupportInt`, `PropagationWallBaseline`, `PropagationWallReplace`,
`PropagationWallAngle`, `PropagationWallSupport`, `PropagationCoreCheck`,
`PropagationRational`, `PropagationTrig`, `PropagationAngleNormalize`,
`PropagationGeometry`, `PropagationEndpoint`, `PropagationAngleRow`,
`PropagationInvariant`, `PropagationState`, `PropagationStateTrace`,
`PropagationStateSeed`, `PropagationCollision`, `PropagationSupportCollision`,
`PropagationHullTriangle`); the capture (`CaptureClassifierBinding`, `CaptureRunFast`,
`CaptureRunSound`, `CaptureTableFast`, `CaptureTableSound`, `CaptureSummaryFast`,
`CaptureSummarySound`, `CaptureSummaryTargetsFast`, `CaptureSummaryTargets`,
`CaptureOpen/Optimality`, `CaptureOpen/Seed`, `CaptureOpen/Chain` (parts),
`CaptureOpenBridge`, `CaptureWindowBridge`, `CaptureFamily`,
`CaptureTerminalOptimality`, `CaptureTerminalLocalChart`, `CaptureLocalOptimality`,
`CapturePointOptimality`, `CapturePointBounds`, `CaptureChartFrame`,
`CaptureChartBounds`, `CaptureChartPacking`, `CaptureProjectionCheck`); and the local
rigidity (`LocalRigidityCertified`, `LocalRigidityGeometric`, `LocalRigidityBox`,
`LocalRigidityDual`, `LocalRigidityFiniteMax`, `LocalRigidityRatio`,
`LocalRigidityUniversalMass`, `LocalRigidityWeightGlobal`, `LocalRigidityWeightCheck`,
`LocalRigidityWeightCover`, `LocalRigidityWeightCoverData`,
`LocalPerturbationCoordinates`, `LocalPerturbationAxes`, `LocalChartCoordinates`,
`LocalChartGeometry`, `LocalChartBounds`, `LocalPackingSpan`, `LocalGeometricRows`,
`LocalGeometricRowsLower`, `LocalPairFeasibility`, `LocalWallFeasibility`,
`LocalWallRows`, `LocalPairRows`, `LocalSliderGeometry`, `LocalSliderCorner`,
`LocalSliderDistances`, `LocalSliderOffsetBounds`, `LocalRigidityMatrixRows`,
`LocalRigidityResidual`, `LocalRigidityResidualSupport`, `LocalRigiditySparseResidual`,
`LocalRigidityResidualCheck`, `LocalRigidityResidualGlobal`, `LocalRigidityIntervalSum`,
`LocalRigidityAffineExpansion`, `LocalRigidityTaylor`, `LocalRigidityCurvature`,
`LocalRigidityGapCurvature`, `LocalRigidityGapGeometry`, `LocalRigidityGapStability`,
`LocalRigidityCornerFeasibility`, `LocalRigidityParallelRows`, `LocalRigidityWallRows`).

Sampled from the archive, by shape and by replay: `HalfPlanePatterns/Dispatch.lean`
(13.9 MB, all 35 patterns), `Pattern01Data`, `Pattern03Data`; the three branch trees’
dispatchers and `T1528/Root`, `Tree`, `Node0`–`Node6` and their covers; `T1563/Common`,
`Tree` parts, `Cover_Node0_Node1`, `RootAlt`; `Neighbour329/Binding`, `Chain` parts,
`Seed`, chunks 0000, 0050 and 0107; `CaptureOpen` chunks 0000, 0080 and 0164 with their
`Checks` files; `OrbitRepresentativeFiniteData` (all 511 parts),
`RepresentativeCaseParts/Part000`, one `OrbitCensus` chunk; `LocalRigidityMatrixData`
(430 values), `LocalRigidityWeightData` (93 certificates), `LocalSliderUnwanted`,
`CaptureTerminalBoundsData`, `RowsData00` and `RowsData16`, `EndpointStrictGaps`.

The project artefacts compared with the Lean data:
`packing/campaign/series/series-000-smoke-and-calibration/results/exp-237-n17-polynomial-root/run-001/certificate.json`
(the endpoint polynomials and root box),
`.../exp-247-n17-unique-state-cover/run-001/receipt.json` (the 24-cell cover and the D4
permutation tables) and `.../exp-248-n17-local-half-composition/` (the 52-row local
model).

## The Statement and Its Scope

The final theorem is `Sq17.square17_optimality` (`Square17Optimality.lean:16`):

```lean
theorem square17_optimality (L : ℝ) :
    HalfPlaneAssembly.PlainPacking L ↔ EndpointGeometry.side ≤ L
```

`PlainPacking L` (`PackingStatement.lean:7`) asks for seventeen sets, each
`IsUnitSquare`, each inside `containerBox L`, with pairwise disjoint interiors.
`IsUnitSquare S` (`SquareBase.lean:18`) is `∃ cx cy ux uy, ux² + uy² = 1 ∧ S = sq cx cy
ux uy`, and `sq` (`SquareBase.lean:14`) is the closed set of points whose two
coordinates in the frame `(ux, uy)`, `(-uy, ux)` are at most $1/2$ in absolute value: a
closed square of side 1, translated and rotated independently of the others, with no
restriction on the angle.
`containerBox L` (`PropagationWall.lean:10`) is the closed box $0 \le x, y \le L$.
Disjointness is of interiors only, so two squares may share an edge or a corner, and a
square may touch the container’s boundary; `square_disjoint_unit_separator`
(`WallSquareSupport.lean`) derives weak separation from disjoint interiors, which is the
direction that keeps touching configurations covered, and `HalfPlaneBoundaryControl`
exhibits two touching squares that are not a collision.
`Feasible L` (`HalfPlaneAssemblySkeleton.lean:102`), the form the case analysis works
with, is the same statement in terms of centres and directions;
`feasible_iff_plainPacking` (`PackingStatement.lean:13`) proves the two equivalent.

`side` (`EndpointGeometry.lean:17`) is $(6 + 4t)/(1 + 2t - t^2)$ where $(t, \beta)$ is
`EndpointRoot.coordinates`, the common root of two integer polynomials inside a box
whose Newton contraction certificate is checked by the kernel
(`EndpointRootData.lean:105`, `decide +kernel`). So the endpoint is an exact algebraic
number; its decimal value $L = 4.67553009360455095163\ldots$ is a consequence
(`side_decimal_bounds`, `side_sharp_bounds`, enclosure width $2.1 \times 10^{-18}$), not
the definition. The reverse direction of the theorem is a construction:
`endpoint_packing` (`EndpointPacking.lean:60`) gives seventeen squares in
$[0, \mathrm{side}]^2$, which fit every larger box.
The set of feasible $L$ is therefore exactly $[\mathrm{side}, \infty)$: the infimum is
attained, and $s(17) = \mathrm{side}$ in the usual sense.

The theorem does not say the optimal packing is unique or that Bidwell’s is the only
one, and it says nothing about other $n$. The axis-parallel container is no loss of
generality for the packing problem as usually posed.

## Findings by Step

### Step 1: The Endpoint and the Construction

The two polynomials, the root box and the Newton certificate were read
(`EndpointRootData`, `PolynomialNewtonRoot`, `PolynomialBoxContraction`), and the kernel
checks `contraction_checked` and the mass and slope bounds that make the box a
contraction, so the root exists and is unique in the box.
An 80-digit Newton solve written here, started from a crude guess, converges to the same
root and agrees with the declared box midpoint to 61 digits:
$L = 4.675530093604550951634111270483146648767$, $U - L = 0.000469906395449$ for the box
side $U = 1169/250$. The polynomials and the box are identical to the project’s
`exp-237` certificate (see MR-4). `side_decimal_bounds` and `side_sharp_bounds` hold at
these digits. The interval evaluator for rational expressions in $(t, \beta)$
(`RationalExpression`, `Cert.check_sound` at `RationalExpression.lean:120`) is
kernel-checked and is what every later enclosure of a coordinate of the packing rests
on.

The construction `endpoint_packing` places seventeen squares at centres and angles that
are rational expressions in $(t, \beta)$ (`EndpointGeometry`: `h`, `X`, `Y`, `A`, `B`),
inside $[0, \mathrm{side}]^2$, with pairwise separation by support functions
(`EndpointSupport`, `EndpointContacts`; `EndpointStrictGaps` carries the 136 pair gaps)
and the angle enclosures of `EndpointAngleBounds` and `ArctanCheck`. It was read, not
recomputed; the first review lane’s remit covers it, and nothing in it looked wrong.

### Step 2: Reduction to Cells and Orbits

`square_packing_cell_subset` (`PackingCellReduction.lean:31`) proves that for a box of
side at most $1169/250$ every centre lies in one of 24 closed cells, from the cover
certificate of `ExactCellCover` and `CellCoverCertificate` (22 slabs, 114 trapezoids
with triangle-hull witnesses, `decide +kernel`). The 24 cells and the D4 permutation
tables are the project’s `exp-247` “ring-3-voronoi-8-tabbed-unique” cover, vertex for
vertex. Capacity is one centre per cell: interior cells by squared diameter at most
$29377/31250$ (`InteriorCellCapacity`; recomputed here, $0.742527$ for the corner type
and $0.940064$ for the side cells, where the bound is tight), since centres of unit
squares with disjoint interiors are at distance at least 1; wall cells by
`wall_rectangle_capacity` (`WallCapacityRectangle.lean:61`) for the three rectangle
classes $79/100 \times 79/100$, $529/750 \times 911/1000$ and $257/375 \times 93/100$,
proved through the positivity of the quartic `wallPoly` on $[0, 1]$ by Bernstein
coefficients (`WallCapacityBounds`), the mixed support bound `mixed_support_normal`
(`WallMixedSupport`) and the finite-axis theorem `support_implies_axis`
(`SquareSeparationAxes`). An adversarial search written here over two squares in each
class never found a separable pair; the largest separation gap reached was $-0.018163$,
$-0.017181$ and $-0.013399$ for the three classes.
A grid of $401 \times 401$ points, 20,000 random points and every vertex of the box were
all covered by the 24 cells.

With one centre per cell, a packing occupies seventeen cells and leaves seven holes.
`OrbitCensus.Complete.exhaustive` (`OrbitCensus/Complete.lean:11`) proves that every
seventeen-subset of `Fin 24` is sent by some element of D4 (`CellPermutation.perm`) to a
representative in the tree of 43,593 nodes (`OrbitRepresentativeFiniteData`), through
346,104 rows in 338 chunks and `GoodBlock.exhaustive`
(`FiniteOrbitCoverCheck.lean:126`), all by `decide +kernel`. Recomputed here from
scratch: the eight permutation tables are the geometric action of D4 on the cells’
vertices, with consistent composition and inverse tables; the orbit count by Burnside is
43,593 and equals the number of distinct representative hole-sets; the 346,104 rows are
all distinct, are all of $\binom{24}{7}$, carry strictly increasing tags and each maps
to its representative; the search-tree keys increase.
`CellSymmetry` and `CellSymmetryBridge` carry a packing across the symmetry, and
`CenteredOrbitFrame` recentres it: with $\delta = (U - L)/2$ the packing of side $L$ is
translated into the $U$-box, and `packing_reaches_trace_table_exact`
(`OrbitPackingReduction.lean:10`) delivers a `RepresentativePacking holes L` whose
centres lie in the representative’s cells, shifted by $-\sigma$.

### Step 3: The Trace Checker and Its Soundness

This is the part of the proof the first review did not read, and it was read in full.

A state (`HalfPlaneState`) holds, for each owner, a list of rows: a list of integer
half-planes $ax + by \le q$ on the centre, a cached box of four support bounds (`mkBox`,
always computed from the half-planes by the pair scan of `HalfPlaneInt`; nothing ever
writes a box by hand), and an index into a table of angle rows.
A table entry carries a rational angle interval of width at most 1, a rational core
direction and core half-width, and a wall span; `TableValid T 44` (`HalfPlaneTable`,
`tableOK`) checks each entry against degree-44 Taylor enclosures of cosine and sine at
the interval’s endpoints (`PropagationTrig`, remainder $|x|^{45}/45!$), the endpoint
cone and the harmonic monotonicity on intervals of width at most 1
(`PropagationAngleRow`), so that a unit square at any angle of the row contains the core
square (`PropagationCoreCheck`). The meaning of a state is `Rep T S p`
(`HalfPlaneStateSound`): every pose of owner $i$ in the packing lies in some row of
owner $i$, centre in the row’s domain and angle in the row’s interval.

The five step kinds and their soundness lemmas were checked one by one.
`cut i k j keep m` adds the half-plane `keep` to row $k$ of owner $i$ after
`collideRows` shows that its complement collides with every row of owner $j \ne i$;
`kill i k j` deletes row $k$ when every row of $j$ collides with it; `wall i k w m` adds
container half-planes justified by the row’s span (`wallOK_sound`, line 138, with
`halfSpan` never below $1/2$); `split i k e₁ e₂` replaces a row by two rows whose angle
intervals together cover its interval (children may be wider, which only weakens the
state); `dead i k` deletes a row whose domain is empty (`emptyOK_sound`, line 170).
`run_sound` (`HalfPlaneStateSound.lean:188`) proves that every accepted step preserves
`Rep` for every packing, given `TableValid T 44`; `runAll_sound` (line 318) and
`excludes_sound` (line 338) conclude that an owner with no rows means no packing is
represented. The collision test `collide` is the separating-axis test on the two cores
over the rows’ boxes and half-planes; `collideRows_sound` (line 122) rests on
`PropagationCollision` and `CoreSeparationGeometry`: disjoint core interiors give a
support separator (Hahn–Banach, `geometric_hahn_banach_of_nonempty_interior`) and
`CoreSeparationAxes` reduces it to one of eight directed edge normals.
The test is used only in the sound direction: an accepted collision means the two cores,
hence the two squares, overlap for every pair of poses in the two rows.
Boundary contact is not a collision (`touching_cores_not_collision`).

Seeds: `stateSeedOK_sound` (`HalfPlaneSeed.lean:68`) proves that a checked initial state
represents every packing whose centres lie in the roster’s cells, shifted by $\sigma$,
with angles in $[-r, r]$ for `initialAngleRadius` $r = 884279719004579/2^{50} =
\pi/4 + 9.1 \times 10^{-13}$; the quarter-turn symmetry of the square
(`PropagationAngleNormalize`) is what allows the restriction.
`windowSeedOK_sound` does the same for the capture’s per-owner angle windows.
Checkpoints: `coverCheck_sound` (`HalfPlaneCover.lean:112`) lets a branch reload a
parent’s state when every child row’s domain and angle interval are covered, with the
child boxes again from `mkBox`. Branch trees: `tree_excluded` (`HalfPlaneTree.lean:130`)
with leaf, split and reload nodes (`HalfPlaneBranchComposition`). Chunks: `runToCheck`
(`CaptureRunFast.lean:10`) runs a chunk’s steps and requires the result to equal the
declared end state `E` by structural equality (rows, boxes and entry indices,
`deriving DecidableEq`); `runToCheck_eq` (`CaptureRunSound.lean:6`) and
`excluded_of_runToCheck` (`HalfPlaneChunkComposition.lean:24`) compose chunks, and the
next chunk’s table extends the previous one under `inheritedCheck` (entry-wise equality
of the inherited prefix) and `freshCheck` (degree-44 checks of the fresh suffix), so
`TableValid` is inherited (`CaptureTableSound`).

The decoders are inside the chain.
`decodeInit`, `decodeSteps`, `decodeEntries` and `decodeBounds` read string literals
through `parseInts`, which drops any token `String.toInt?` rejects.
The decoded terms are the same terms in the seed fact, the table fact and the exclusion
fact, and every soundness lemma quantifies over whatever state and table those terms
denote; so a decoding error can only produce a certificate that fails to check, never a
false exclusion.
The seed check binds the decoded state to the cells and the angle range,
and the table check binds the decoded entries to the trigonometry.

No decidability instance or computable definition can turn a false proposition into
`true` here except through the evaluator: every native fact has the form `f args = true`
for a `Bool`-valued function defined by structural recursion over lists and arrays with
`Int` and `Rat` arithmetic and `decide` on decidable propositions over $\mathbb{Z}$,
$\mathbb{N}$ and $\mathbb{Q}$, and the project sources contain no `implemented_by`,
`@[extern]`, `unsafe`, `opaque`, `partial def`, `axiom` or `sorry` (grep over
`Sq17Lean/`, the tree and the sampled generated files).
The two controls, `HalfPlanePositiveControl` and `HalfPlaneBoundaryControl`, run the
same definitions through `decide +kernel`: a feasible two-square configuration cannot be
excluded by any step list (`no_false_exclusion`) or any branch tree (`no_false_tree`),
forged cached boxes and missing entries are rejected at the seed, and touching squares
are not a collision.
They test the definitions in the kernel, not the compiled evaluator; the replays below
test the evaluator.

### Step 4: Dispatch of the 43,593 Representatives

For $L < \mathrm{side}$, a `RepresentativePacking holes L` is routed by the classifier
tree (`RepresentativeCaseData`, `RepresentativeCaseCheck`), which mirrors the orbit tree
and labels each representative either with one of 35 patterns or with one of 2,781 full
rosters. Recomputed here: the mirror holds at every node (0 violations), 40,812
representatives are pattern-covered and 2,781 are full, $40{,}812 + 2{,}781 = 43{,}593$;
the pattern list has no duplicates and the full-roster keys are exactly
$0, \ldots, 2780$.

A pattern $p$ names a sub-roster of cells that the occupied cells contain under the
recorded symmetry; `pattern_dispatch_of_case` (`HalfPlanePatternDispatch.lean:22`) and
`PackingSubfamily` restrict the packing to the pattern’s squares, and
`Pattern<p>.no_packing` (one trace each in `HalfPlanePatterns/Dispatch.lean`, ordinary
frame, `roster_excluded` at `HalfPlaneCells.lean:49`) excludes them.
A full roster $k$ is routed by `full_route` (`HalfPlaneFullRoute.lean:53`): the 2,776
ordinary indices to `HalfPlaneCases/Ordinary` (`Case<k>.no_packing`, four native facts
each: `table_ok`, `seed_ok`, `owners_eq`, `excluded`), and the four neighbours of the
Bidwell state to their own modules: roster 209 to `Neighbour329` (108 chunks,
`Neighbour329.full_dispatch`), 1158 to the branch tree `T1528`, 1161 to `T1531` and 1193
to `T1563` (`neighbours_of_two`, `HalfPlaneLastTwo.lean:14`; `feasible_iff_of_1563`,
`HalfPlaneLastCase.lean:8`; `T1563.full_dispatch`,
`HalfPlaneTrees/T1563/Dispatch.lean:14`). The capture roster 204 goes to `CaptureOpen`
(Step 5). The rosters of 209, 1158, 1161, 1193 and 204 were recomputed from the census
here and equal the rosters bound in the Lean dispatchers (`roster_eq`,
`decide +kernel`): $209 = \{0, 1, 2, 3, 6, \ldots, 15, 18, 19, 20\}$,
$1158 = \{0, \ldots, 11, 13, 18, \ldots, 21\}$,
$1161 = \{0, \ldots, 7, 9, \ldots, 13, 18, \ldots, 21\}$,
$1193 = \{0, \ldots, 7, 9, 11, 12, 13, 14, 18, \ldots, 21\}$,
$204 = \{0, 1, 2, 3, 5, 6, 7, 8, 10, \ldots, 15, 18, 19, 20\}$.

The frames (`HalfPlaneFrameBounds.lean:33`, `:37`). The ordinary frame has side
$2632353982198055/2^{49} = 4.676000000000000156\ldots$ ($U + 1.6 \times 10^{-16}$),
padding $4951760157141521/2^{92} \approx 10^{-12}$ and $\sigma = 0$; `ordinary_bounds`
proves its `Lower` and `Upper` conditions for every $L \le \mathrm{side}$ through
`frame_mono` and `side_decimal_bounds`. The neighbour and capture frame
`captureNeighbour` has side $5264178896829249/2^{50} = L + 1.136 \times 10^{-17}$, the
same padding and $\sigma = 8668243015428611/2^{65} = \delta(L) - 5.2 \times 10^{-16}$.
The trace container is the frame’s side plus the padding on each side,
$L + 2.0 \times 10^{-12}$ in the neighbour cases, and the two frame conditions hold with
slack $1.0005 \times 10^{-12}$ and $0.9995 \times 10^{-12}$ (computed here from the
root). The thin margin of $1.1 \times 10^{-17}$ named in the brief is the frame constant
above $L$; the exclusions are proved for every $L \le \mathrm{side}$ and used for
$L < \mathrm{side}$, and no step depends on that constant (MR-5).

Replayed here, with a re-implementation of `HalfPlaneFast` written from the Lean text:
`T1528/Node3` (791 table entries, 17 owners of 256 rows, 14,851 steps: 11,762 cuts,
1,061 kills, 808 splits, 1,210 walls, 10 deads), every step accepted in the same order,
owner 12 left without rows, `excludes = true` as the recorded fact says.
The node’s table check (`tableOK 44`) was not replayed, because the node’s bounds were
not found in the tree file by the script; the same check was replayed on two capture
tables (Step 5).

### Step 5: Capture and Local Rigidity

The capture seeds owner-wise angle windows (`CaptureSeedWindows`, `windowSeedOK`) on
roster 204 in the `captureNeighbour` frame and runs 165 chunks (`CaptureOpen/Chain`),
each with `run_checked : runToCheck table side shift S0 steps E = true` and a `Checks`
module (`fresh_checked`, `initial_length`, `final_length`). The terminal state
`Chunk0164.E` has 1,024 rows per owner and passes `summary_checked`
(`CaptureOpen/Optimality.lean:7`) against 17 targets of eight half-planes and one angle
interval each (`CaptureSummaryTargetsFast`); `summaryCheck_pose` and
`summaryTargets_pose` (`CaptureSummaryTargets.lean:461`, `:403`) turn the Boolean into
bounds on each real pose, and `terminalSummary_pointBounds`
(`CapturePointBounds.lean:771`) into `TerminalPointBounds`: radius $10^{-7}$ around the
Bidwell pose for the in-plane coordinates of thirteen squares and the transverse
coordinates of squares 4, 10 and 12, and the slider boxes $a \in [-1, 1/4]$,
$b \in [-1/2500, 1/12]$, $z \in [-1/8, 1/16]$; `summary_angle_bounds` and
`summary_coordinate_bounds` (`CapturePointOptimality.lean:16`, `:38`) add the angles,
and `summary_pose_optimality` (line 82) hands over to the local chart.
`classifier_capture_excluded` (`CaptureWindowBridge`) is the version the theorem uses;
`CaptureOpenBridge.side_eq_of_open_run` is an earlier version that the theorem does not
depend on (MR-2).

Replayed here: chunk runs 0000 (825 entries; 8,897 steps), 0080 (9,559 entries, 8,021
inherited; 9,000 steps) and 0164 (15,399 entries; 2,820 steps), each accepted step by
step with a final state equal to the declared `E` to the bit, in 87, 141 and 127 seconds
of exact rational arithmetic; the three `Neighbour329` chunks 0000, 0050 and 0107
(3,894, 2,493 and 801 steps) likewise, chunk 0107 ending with owner 15 empty, which is
the exclusion; `freshCheck 44` on the 825 fresh entries of chunk 0000 and the 1,538
fresh entries of chunk 0080; and `summaryCheck` on all $17 \times 1{,}024$ rows of the
terminal state. Two controls: one integer of chunk 0000’s declared `E` changed by one
makes the run disagree (`R = E` false), and one cut offset lowered by $10^{30}$ is
rejected at step 868; lowering one target’s angle bound by $10^{-12}$ makes the summary
check fail at owner 3, row 1023. The capture tables carry angle rows outside
$[-\pi/4, \pi/4]$ (chunk 0000 spans $[-1.4246, 1.4801]$); this is harmless, since a
split may widen (MR-6).

The local chart (`LocalChartCoordinates`, `LocalPerturbationCoordinates`) has 45
coordinates: the in-plane coordinates of thirteen squares, the transverse coordinates of
squares 4, 10 and 12, and sixteen angles; square 5 is left out, which is sound because a
sub-packing is a packing, and the three sliders $a, b, z$ along which squares 4, 10 and
12 may move are the model’s parameters.
The 52 rows are 25 wall rows and 27 pair rows for 19 contact pairs, chosen among 152
separating options, of which the 125 unwanted ones are excluded uniformly by
`rotatingCornerGap_stays_negative` (`LocalRigidityGapStability`) from the base gaps of
`LocalSliderUnwanted` with margin $51q$, and parallel faces give both rows without a
choice of owner (`parallel_face_rows`). Each row is a linearized contact inequality with
a curvature bound: along a perturbation of size $q$ the exact gap $g$ satisfies
$g(0) = 0$, $g(1) \ge 0$ (`rotatingCornerGap_feasible`, `fitted_wall_corner`) and
$g'' \le 100 q^2$ (`rotatingCornerGap_curvature`, Taylor on the segment), so the linear
row is at least $-50 q^2$ (`rotatingCornerGap_linear_lower`,
`movingWallGap_linear_lower`). The row coefficients (`LocalRigidityMatrixRows`, 430
values in `LocalRigidityMatrixData`) are `Cert` expressions in $(t, \beta)$ with
interval bounds through `Cert.check_sound`. The dual certificate
(`LocalRigidityWeightData`: 93 `AffineWeightCertificate 52 3`, weights affine in the
sliders and nonnegative on each of 93 boxes that cover the slider box, the direction
$-\omega_{11}$ split into four $z$-ranges) proves for each of the 90 signed coordinate
directions that $\pm q_j \le \rho \lVert q \rVert_\infty + M \cdot 50
\lVert q \rVert_\infty^2$ with residual $\rho \le 1/4$ and mass $M \le 12{,}000$
(`LocalRigidityWeightCheck`, `LocalRigiditySparseResidual`, `LocalRigidityRatio`,
`LocalRigidityUniversalMass`, `LocalRigidityFiniteMax`), hence $\lVert q \rVert_\infty
\le \lVert q \rVert_\infty / 4 + 6 \times 10^5 \lVert q \rVert_\infty^2$, which at
$\lVert q \rVert_\infty \le 10^{-7}$ forces $q = 0$. `pose_side_le_of_encoded_zero`
(`LocalChartGeometry.lean:61`) then pins the side with square 0 containing $(0, 1/2)$
and square 6 containing $(\mathrm{side}, 3/2)$, and `side_eq_of_local_capture`
(`CaptureLocalOptimality.lean:10`) concludes $L = \mathrm{side}$, against
$L < \mathrm{side}$.

Recomputed here, exactly, from the 93 certificates and the 430 coefficient intervals:
every weight check passes; the worst residual budget is $0.199543 \le 1/4$ (box 53,
direction $-u_{11}$); the largest mass is
$131499357511999117439/10995116277760000 \approx 11{,}958.9 \le 12{,}000$; the dense and
sparse residuals agree; the 93 boxes cover the slider box for all 90 directions; every
certificate’s target is the signed unit coordinate of its direction; and
$q/4 + 6 \times 10^5 q^2 = 0.310\, q$ at $q = 10^{-7}$. The model’s shape (45
coordinates, 52 rows, 19 pairs, 152 options) is that of the project’s `exp-248` (MR-4).

### Step 6: The Hand-Overs

Each hand-over is a kernel-checked theorem, and each was read: packing to cells,
`square_packing_cell_subset`; cells to a representative and a symmetry,
`OrbitCensus.Complete.exhaustive` with `CellSymmetryBridge` and `CenteredOrbitFrame`;
representative to a classifier leaf, `RepresentativeCaseCheck` and `full_route`; leaf to
a trace seed, `stateSeedOK_sound` or `windowSeedOK_sound` with the frame’s `Lower` and
`Upper`; trace to exclusion, `excludes_sound`, `tree_excluded` and
`excluded_of_runToCheck`; chunk to chunk, `runToCheck_eq` with `inheritedCheck` and
`freshCheck`; terminal state to real poses, `summaryCheck_pose`; poses to the chart,
`terminalSummary_pointBounds` and `summary_pose_optimality`; chart to the side,
`packing_local_rigidity` and `pose_side_le_of_encoded_zero`; and the four neighbour
cases and the capture back into `Feasible L ↔ side ≤ L` through `neighbours_of_two`,
`feasible_iff_of_1563` and `plainPacking_iff_of_1563`. Nothing in the chain takes a
Boolean fact as more than what its soundness lemma says.

## The Checkers’ Trust Boundaries

`#print axioms Sq17.square17_optimality` (`verification/Square17Optimality.log`) lists
`propext`, `Classical.choice`, `Quot.sound` and 13,343 axioms named
`<fact>._native.native_decide.ax_1_1`, one per `native_decide` fact in the theorem’s
dependency closure; `sorryAx` does not occur.
The count was confirmed by counting the log’s lines.
$2{,}776 \times 4$ of the facts are the ordinary cases’ and $35 \times 4$ the patterns’;
the rest are the 108 + 165 chunk runs with their table and length checks, the three
branch trees (760 facts carry the name `T1563`) and the capture summary.
The modules of MR-2 contribute no fact, which is how it is known that the theorem does
not use them. The kernel evaluates the rest: 2,091 `decide +kernel` proofs in the tree
and 862 in the sampled generated files, among them the census, the classifier, the cell
cover, the Newton contraction, the residual and weight checks and every `roster_eq`.

What `native_decide` trusts is the Lean compiler, the five `*Fast` modules compiled to
shared libraries and loaded with `--load-dynlib` by `scripts/reproduce.py`, and the
runtime’s `Int` and `Rat` arithmetic.
The receipt (`clean-build-receipt.json`: `CLEAN_SOURCE_BUILD_ACCEPTED`, Lean 4.34.1,
4,951 project modules rebuilt, no prebuilt project objects, pinned third-party cache,
`axiom_set_matches_local_build`) is the author’s own record of that build and was not
reproduced here. The replays of this review evaluate the same definitions with an
independent evaluator on ten of the facts and agree on all ten; they do not compare the
shared libraries with their sources, and they cover a sample.

## Defects

No blocking or major defect was found.
The table lists every candidate found, with its grade and resolution.

| Id | Grade | Location | Description | Blocking | Resolution |
| --- | --- | --- | --- | --- | --- |
| MR-1 | minor | `HalfPlaneAssemblySkeleton.lean:7`; `HalfPlaneFinalAssembly.lean:13`; `HalfPlaneLastTwo.lean:5-6`; `HalfPlaneLastCase.lean:4-5`; `PropagationCollision.lean:5`; `PropagationPolygonCollision.lean:8`; `WallCapacityBounds.lean:5` | Module docstrings still describe the development as “CONDITIONAL”, say a file “does NOT yet prove unconditional optimality”, that “optimality is still conditional”, or that a module “does not yet” formalize what a later module formalizes | No: the theorem has no premise, and its own docstring (`Square17Optimality.lean:3-8`) is right | Reword to the current state |
| MR-2 | note | `CaptureOpenBridge.lean:17`; `CaptureTerminalLocalChart.lean`; `CaptureTerminalStateData.lean`; `CaptureTerminalSummaryData.lean`; `HalfPlanePrototype.lean` | Modules in the build that the theorem’s dependency closure does not contain (the axiom report attributes no fact to them); a reader following the README’s module list can take the earlier route for the proof | No | Mark them as retained alternatives, or remove them |
| MR-3 | note | `CaptureSummaryFast.lean:14-18` | `rowCheck` returns `true` for a row whose entry index is outside the table | No: `summaryCheck_sound` (`CaptureSummarySound.lean:24`) carries it, since such a row represents no pose | Return `false`; the acceptance set shrinks and nothing in the data is affected |
| MR-4 | note | `README.md:102-126`; `EndpointRootData`; `ExactCellCoverData`; `CellPermutation`; `LocalRigidityMatrixRows` | The endpoint polynomials and root box, the 24-cell cover with its D4 tables, and the 45-coordinate, 52-row, 19-pair, 152-option local model coincide with this project’s `exp-237`, `exp-247` and `exp-248` artefacts; the README credits the Squares Project only as collecting “the wider research record” | No: provenance, not correctness | Name the artefacts reused, or state that the data were derived independently |
| MR-5 | note | `HalfPlaneFrameBounds.lean:37-39` | `captureNeighbour.side` exceeds $L$ by $1.1 \times 10^{-17}$, which reads as a thin margin; it is a frame constant, the container is $L + 2.0 \times 10^{-12}$, and the frame conditions hold for every $L \le \mathrm{side}$ with slack $10^{-12}$ | No | A comment at the definition |
| MR-6 | note | `CaptureOpen` chunk tables | Angle rows beyond $[-\pi/4, \pi/4]$ (chunk 0000 spans $[-1.4246, 1.4801]$) after splits | No: a wider child only weakens the state | None required; table hygiene |

## Questions for the Author

1. Were the endpoint polynomials and root box, the 24-cell cover with its D4 tables, and
   the 52-row local model taken from the Squares Project’s `exp-237`, `exp-247` and
   `exp-248` artefacts, and if so, can the README name them?
2. Will the docstrings of MR-1 be brought up to date in the next release, so that a
   reader of the module sees the same status as a reader of the theorem?
3. Are `CaptureOpenBridge`, `CaptureTerminalLocalChart`, `CaptureTerminalStateData`,
   `CaptureTerminalSummaryData` and `HalfPlanePrototype` kept on purpose, and can they
   be marked as outside the proof?
4. Does `scripts/reproduce.py` check, by digest, that the five shared libraries it loads
   with `--load-dynlib` were compiled from the pinned sources of the same build?
5. Why does square 5 not appear among the 45 chart coordinates: is it the square whose
   pose the contacts do not pin, and is this stated anywhere in the sources?
6. Is there a reason the capture tables keep angle rows outside $[-\pi/4, \pi/4]$ rather
   than clipping children at the parent’s interval?

## Checks Run Here

All checks are scripts written for this review, kept in the scratch directory under
`math-fitzharding/code/`, run with the project interpreter as `python3 -I`, reading the
cloned sources and the extracted archive members as data by path.
They import no code of the author’s and run no Lean.

```sh
python3 -I endpoint_check.py            # root, side, frames, margins
python3 -I census_check.py              # D4 tables, orbits, rows, patterns, rosters, routing
python3 -I geometry_checks.py           # cell diameters, cover, wall-class search
python3 -I rigidity_dual_check.py       # 93 weight certificates, residuals, masses, cover
python3 -I fast_replay.py T1528/Node3.lean T1528/Common.lean T1528/Tree.lean
python3 -I chunk_replay.py <Chunk>Data.lean          # six chunks, two controls
python3 -I table_check.py <Chunk>Data.lean <Chunk>Checks.lean   # two capture chunks
python3 -I summary_check.py CaptureOpen/Chunk0164Data.lean CaptureSummaryTargetsFast.lean
```

| # | Check | Result |
| --- | --- | --- |
| 1 | Root of the two polynomials by Newton at 80 digits from a crude start | agrees with the declared box midpoint to 61 digits; $L = 4.6755300936045509516341\ldots$; $U - L = 4.699 \times 10^{-4}$; `side_decimal_bounds` and `side_sharp_bounds` (width $2.1 \times 10^{-18}$) hold |
| 2 | Frames from the root | ordinary side $= U + 1.6 \times 10^{-16}$, padding $10^{-12}$; neighbour side $= L + 1.136 \times 10^{-17}$, $\sigma = \delta(L) - 5.2 \times 10^{-16}$; container $L + 2.0 \times 10^{-12}$; frame slacks $1.0005 \times 10^{-12}$, $0.9995 \times 10^{-12}$; `initialAngleRadius` $= \pi/4 + 9.1 \times 10^{-13}$ |
| 3 | D4 tables against the geometric action; composition and inverse tables | equal; consistent |
| 4 | Orbit census from scratch | 43,593 orbits by Burnside = 43,593 distinct representative hole-sets = 43,593 tree nodes; 346,104 distinct rows = $\binom{24}{7}$, tags strictly increasing, each to its representative; keys increasing |
| 5 | Classifier tree against the orbit tree | mirror exact, 0 violations; 40,812 pattern-covered + 2,781 full; 35 patterns without duplicates; full keys $0, \ldots, 2780$ |
| 6 | Rosters of 209, 1158, 1161, 1193, 204 from the census | equal to the Lean `roster_eq` rosters |
| 7 | Interior-cell squared diameters | corner type $0.742527$, side cells $0.940064 = 29377/31250$ (tight) |
| 8 | Cover of the $U$-box by the 24 cells | $401 \times 401$ grid, 20,000 random points, every vertex: 0 uncovered; cell area sum $13.6057$ against box area $13.5130$ |
| 9 | Wall-class two-square search (three classes) | never separable; largest gaps $-0.018163$, $-0.017181$, $-0.013399$ |
| 10 | `AffineWeightCertificate.check` and `sparseResidualCheck`, exact, 93 certificates | all pass; worst residual budget $0.199543 \le 1/4$ (box 53, $-u_{11}$); largest mass $\approx 11{,}958.9 \le 12{,}000$; dense = sparse; slider box covered for all 90 directions; targets correct; $q/4 + 6 \times 10^5 q^2 = 0.310\, q$ at $q = 10^{-7}$ |
| 11 | `T1528/Node3` replay | 791 entries; 14,851 steps all accepted (11,762 cut, 1,061 kill, 808 split, 1,210 wall, 10 dead); owner 12 emptied; `excludes = true` |
| 12 | `Neighbour329` chunks 0000, 0050, 0107 replay (`runToCheck`) | 3,894, 2,493, 801 steps accepted; `R = E` exactly; 0107 ends with owner 15 empty; 10 s, 102 s, 69 s |
| 13 | `CaptureOpen` chunks 0000, 0080, 0164 replay | 8,897, 9,000, 2,820 steps accepted; `R = E` exactly; 0164 ends with 1,024 rows per owner; 87 s, 141 s, 127 s |
| 14 | Controls on `Neighbour329` chunk 0000 | one integer of `E` changed by 1: `R = E` false; one cut offset lowered by $10^{30}$: rejected at step 868 |
| 15 | `freshCheck 44` on capture chunks 0000 and 0080 | 825 and 1,538 fresh entries, all pass; angle widths at most $2.45 \times 10^{-2}$ and $7.67 \times 10^{-4}$; core half-widths at least $0.98795$ and $0.99962$ |
| 16 | `summaryCheck` on `Chunk0164.E` against the 17 targets | all $17 \times 1{,}024$ rows pass; one target bound lowered by $10^{-12}$: fails at owner 3, row 1023 |
| 17 | Axiom report and escape hatches | 13,343 `native_decide` axioms counted in the log; `sorryAx` absent; no `implemented_by`, `extern`, `unsafe`, `opaque`, `partial def`, `axiom` or `sorry` in `Sq17Lean/`; 2,091 and 862 `decide +kernel` in the tree and the sample |

## Not Reached

No Lean was run, so the kernel-checked part is trusted as the author’s log and receipt
report it; the receipt was not reproduced and the shared libraries were not compared
with their sources. Of the 2,776 ordinary traces none was replayed and of the 35 pattern
traces none; of the 273 chunk runs six were replayed; of the three branch trees one node
of one tree. The degree-44 table check was replayed on two capture tables and not on the
branch trees’ tables.
The endpoint construction (`EndpointPacking`, `EndpointContacts`, the 136 pair gaps) was
read, not recomputed.
The 430 coefficient expressions of the local model were read in shape and their interval
bounds were used as given; the row derivation from the geometry was read theorem by
theorem and not re-derived numerically.
The generated modules were sampled, not read in full; `#print axioms` at the end of each
module is the evidence that the sample is representative.

## Verdict

Accepted.
The statement is the one the record wants, the endpoint is exact, and the proof
is a kernel-checked chain from 13,343 compiled Boolean facts whose soundness lemmas were
read and found to say what the geometry needs.
The facts are the declared trust boundary; an independent evaluator agreed with ten of
them and rejected corrupted inputs, and the exact re-derivations of the census, the
cover, the frames, the routing and the dual certificate found no discrepancy.
The six findings ask for prose, hygiene and attribution, not for a change to the
mathematics.

## Comparison with the First Review

Written after the findings above, on reading
[`review-2026-10-13-fitzharding-n17-lean.md`](review-2026-10-13-fitzharding-n17-lean.md)
(the adversarial lane, a Claude model at the tbd-strong tier) and the register entry
`T-154` in `packing/frontier/results.yaml`.

**Confirmed.** Every row of the first review’s statement table (§1) and every objection
it tried agree with the reading here: the closed `sq`, the independent unit direction,
the closed container, interiors only, the attained minimum, no uniqueness claimed.
Its endpoint section (§2) is confirmed and goes further: it compared the polynomials,
the box and the side map with `exp-237` and H-255 term for term and refined `side` to 60
places, `4.675530093604550951634111270483146648767143855015879695416889`, which the
80-digit solve here reproduces to every digit both carry.
Its axiom accounting (§3.1: 3 standard axioms, 13,343 native facts, none elsewhere than
`Sq17.Propagation.HalfPlaneState`, no `sorryAx`) is the count made here, and its family
decomposition (11,104 ordinary, 140 pattern, 825 capture, 434 neighbour, 840 tree) sums
to it, which the probe here only approximated; its keyword scan (§3.2) agrees with the
grep here on every keyword, and its “no premise is left” table (§3.4) is the chain read
here theorem by theorem.
Its F-3 is MR-1: the two location lists overlap and together are the complete list (the
first review adds `CaptureTerminalOptimality.lean:10-12` and
`ExactCellCover.lean:12-14`; this one adds the three `Propagation*` and `WallCapacity*`
docstrings). Its F-5 and F-6 are the trust-boundary section and the “not reached” list
here, in other words.
Its remark that `excludes` with a wrong owner count returns `true` and that the
`owners_eq` and `*_length` facts supply the length premise is right; the positive
control’s `raw_wrong_owner_count` shows the trap, and `excludes_sound` takes
`S.length = n` as a hypothesis.

**Nothing contradicted.** No statement of the first review or of `T-154` was found
wrong. The register entry’s claim text describes the theorem, the route and the trust
boundary as this review read them; its note that the first review “did not read the
checkers’ soundness proofs or the certificates” names exactly the part this review
covers.

**What it found that this review did not.** The first review’s remit was the record and
its lineage, and it reached things outside this review’s scope: the manifest and all 526
archive members checked by digest; the import closures (the 241-module closure of
`PackingStatement` and the 18-module closure of `EndpointPacking` hold no
`native_decide`, so the statement and the upper bound are proved without native
evaluation, which this review stated for the endpoint but did not compute); the
enumeration of every `instance` (three, all `Decidable` or `DecidableEq`, the
hand-written one built by `infer_instance`) and the one tactic macro, which closes the
question of a rogue instance more completely than the grep here; the lineage in detail
(32 of the 35 patterns are entries of this project’s certified sub-pattern ledger,
eleven of them wand125’s; the endpoint layout is H-256’s; the 60-place box centre is
Overbeck’s seed of 21 September; the cap and the census are H-266’s and `exp-246`’s),
which is why its F-1 grades attribution as major where MR-4 here, written from a
correctness remit with three artefact comparisons, is a note; the chronology against
Overbeck’s candidate; and the credits findings F-2, F-4, F-7 and F-8. MR-4 should be
read with F-1 as the fuller statement.

**What this review adds.** The first review did not read the soundness proofs of the
checker and did not replay or read the native facts; those are Steps 3 to 5 here: every
step kind’s soundness lemma, the collision direction, the seeds, covers, branch trees
and chunk composition, the decoders inside the chain, and ten native facts re-evaluated
with an independent implementation (one branch node, six chunk runs, two degree-44
tables, the terminal summary) with corrupted inputs rejected.
It also recomputed the census and the classifier tree from scratch rather than comparing
counts, re-derived the cell geometry and wall capacities, computed the frame margins
behind the $1.1 \times 10^{-17}$ constant, and recomputed the 93-box dual certificate
exactly. MR-2, MR-3, MR-5 and MR-6 are new.
Neither review built the proof; `T-154`’s rung is unchanged by this one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
