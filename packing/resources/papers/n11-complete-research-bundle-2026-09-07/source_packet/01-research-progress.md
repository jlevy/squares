# Research Progress and the Remaining n = 11 Problem

Snapshot: 2026-09-06, repository revision `4d305597a505ebfbe85f1851fa7148374661e622`.
This is context for a mathematical strategy review, not a new experiment or a decision
to continue the existing allocation.
The review should assess whether Agenda 024’s methods can produce substantial progress,
propose better alternatives where justified, and seek an argument that could determine
the exact value of `s(11)`.

## The Problem and the Exact Bracket

A packing consists of `n` closed unit squares contained in an axis-aligned square of
side `L`, with pairwise disjoint interiors.
Each small square may translate and rotate independently.
Boundary touching is allowed.
Write `s(n)` for the infimum of feasible container sides.
A construction proves an upper bound; a proof that no packing exists below a specified
side proves a lower bound.
Numerical failure to find a packing does not establish exclusion.

Eleven squares are the smallest unresolved case in the project’s source corpus.
The current bracket is

$$
\frac{38100\sqrt{8100042893309449}}{899996306539}
\le s(11)\le U,
$$

where

$$
3.810025723614703\ldots\le s(11)
\le3.87708359002281417730789706010096\ldots.
$$

The gap is approximately `0.067057866408`. The upper endpoint is Walter Trump’s 1979
construction: six axis-aligned squares surrounding five squares tilted by approximately
`40.1819372903°`. Its exact container side `U` is the root in `[3.87,3.88]` of

$$
U^8-20U^7+178U^6-842U^5+1923U^4-496U^3-6754U^2+12420U-6865=0.
$$

The repository verifies all 55 square pairs exactly, including 14 pairs at zero
separation, and 20 corner coordinates exactly on container walls.
This validates the construction.
It does not prove its optimality.
The algebraic degree eight distinguishes the endpoint from familiar low-degree bounds,
but no theorem in this corpus says that unavoidable-set methods cannot reach an endpoint
of that degree.

The principal first-party lower-bound result, **T-018**, is the simpler statement
`s(11) >= 381/100 = 3.81`. Its certificate has 1,121 positive weighted atoms, total mass
`434547/40000 = 10.863675`, and exact minimum covered mass `4001/4000`. An exact
event-cell sweep and a method-distinct interval calculation agree on that minimum.
The certificate’s shrunken witnesses lie strictly inside the actual unit squares,
allowing their masses to be counted without double counting touching boundaries.

**T-022** sharpens the containment estimate and uniformly dilates the retained
certificate. Every rational dilation satisfying a strict containment inequality gives a
no-fit side. Their supremum yields the displayed weak lower bound.
The containment inequality becomes equality at that endpoint, so the result supplies
neither an endpoint no-fit certificate nor a strict bound there.
Its gain above 3.81 is approximately `0.0000257236`; it is accepted mathematics, but a
small fraction of the remaining gap.

Sources: `SYNOPSIS.md`, “The Problem”; `packing/frontier/RESULTS.md`, T-011, T-018,
T-022; `packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md`;
`packing/cases/trump11/packing.py`.

## What the Larger Project Has Established

The square-packing package has produced results outside eleven squares and built methods
that expose difficulties a strategy must address.

| Result | Mathematical content and scope |
| --- | --- |
| T-017, twelve squares | `s(12) >= 99/25 = 3.96`, leaving a gap of 0.04 to the conjectured value 4. Together with Trump’s construction, this proves `s(12) > s(11)`. |
| T-019, seventeen and eighteen | A first-party fractional certificate gives `s(17), s(18) >= 4.59`; it also proves the weaker retained statement at nineteen. |
| T-020, nineteen | `s(19) >= 4.80`. The same certificate applies to twenty and twenty-one, where the next result is stronger. |
| T-021, twenty and twenty-one | `s(20), s(21) >= 4.85`. Its mass exceeds nineteen, so this certificate cannot move the nineteen-square bound. |
| T-014, five squares | Goebel’s optimum is locally isolated at fixed side, although its first-order cone contains a motion. Exact second-order stress calculations and an audited curve-selection argument close that motion. |
| T-008, forty-six squares | The audited published lower bound and the grid construction give `s(46) = 7`; this confirms an existing solved case. |
| T-009, twenty-nine squares | An interval certificate validates a relaxed witness with side about `5.933833462676929`; this is a slightly weaker bound than the reported record, not a better packing. |

The finite-angle reduction is another useful fact: once every orientation and each
pair’s separating-axis choice are fixed, containment and nonoverlap become linear
inequalities in centers and container side.
Nonconvexity remains in the angles and the choice of separating branches.
Numerical experiments on Trump’s contact cell found a corner in the optimum as the
five-square block’s shared angle varies.
Smooth optimization models can therefore misrepresent even that restricted
one-dimensional problem.

The small cases also distinguish local rigidity from complete classification.
The project has complete quotient classifications for the `n=3,4` optimum spaces,
whereas the `n=5` theorem establishes local isolation of a particular pose.
They are different controls for a proposed global method.
At `n=40`, seven first-order motions have verified second-order obstructions, but the
recorded result does not establish full local rigidity.

Sources: `packing/frontier/RESULTS.md`, named result rows; `SYNOPSIS.md`, “Theoretical
Results” and “The Cell Decomposition”.
These are computer-assisted or audited results at their recorded assurance scopes.
“Apparently novel” describes the project’s retained source search, not external peer
review or proof-assistant formalization.

## How the Eleven-Square Work Reached This Point

The starting literature bound was Stromquist’s 2003 statement
`s(11) >= 2 + 4/sqrt(5) = 3.788854382...`. The repository found an exact strict box
avoiding every point in his printed Figure 14 set.
Thus that printed unavoidability argument is false as written.
A separately tested repair replaces `G=(0.8,1.85)` with `G'=(0.79,1.85)` and exactly
verifies the localization, forcing, cover, and counting chain.
**T-010** restores the same numerical bound through a source-distinct proof.
The repair is the project’s result, not a correction silently attributed to Stromquist.

The weighted fractional method then passed a below-record calibration at 3.78, reached
3.80, and established T-018 at 3.81. T-022 extracted the small additional dilation gain.
This moves the recorded lower endpoint by about `0.021171342` beyond Stromquist’s value.
The larger gap to Trump remains.

Experiments at 3.82 exposed limits of the tested models.
Two retained site sets reached covering objectives of eleven, with different convergence
states. A certificate needs strictly less than eleven after its coverage normalization.
These measurements obstruct those fixed choices; they do not prove an optimum of eleven
for unrestricted sites or all richer witnesses.
A separate exact check of one proposed fractional packing found maximum depth
`1925/1152`, much larger than its sampled estimate, reducing its feasible mass to
`1152/175`, approximately 6.58. Sampling had missed decisive arrangement events.

The later BC-232 attempt retained an exact packing-family lower endpoint near
`10.384212408` and a separate computational covering upper endpoint near `11.055616943`
at 3.82. Recovery produced no new row-converged covering below eleven.
Its scientific criterion remains unresolved.
The endpoints describe a fractional optimization problem; neither is a value of `s(11)`.
A stopped optimizer is not a certificate of that problem’s exact optimum.

Other negatives narrow particular mechanisms.
H-090 and H-091 obstruct core shrinking with retained sites, angle net, and relative
weights. The included assessment reports that a separately reviewed H-092 transport
bounds the refined mechanism’s possible improvement over T-022 by less than
`0.00000125`. That transport awaits integration and its evidence is absent from this
snapshot; treat this as reported context, not an independently supplied obstruction.
Even if confirmed, it would concern that fixed mechanism, not changed weights, new
sites, or richer witnesses.
The tested inset/release seed failed to improve its matched trajectory, and the simple
two-threshold angle-class program did not provide the desired reduction.
Neither experiment refutes all support priors or all conditional counting arguments.

Sources: `packing/frontier/RESULTS.md`, T-010 and T-018 explanations;
`docs/project/specs/active/plan-2026-09-06-post-381-research-sequence.md`, “Evidence
That Changes the Allocation” and “Coverage of the Earlier Reviews”;
`docs/project/handoff-2026-09-06-post-381-t2-t10-continuation.md`, “Research Payoff and
Exposition”.

## The Local Trump Theorem and Its Missing Global Premise

The qualitative exp013 result covers all 128 derivative-distinct branches of Trump’s
local contact system.
Every branch has a zero first-order cone, certified through exact positive stresses and
rank. A finite-branch subsequence argument then proves local isolation.
This original result has no explicit radius.

BC-240 subsequently packages retained BC-199 modulus and curvature calculations into a
quantitative theorem.
Let `z` contain the eleven labeled centers and angles in an anchored 33-dimensional
chart; angles are measured in radians.
With container `[0,U]^2`, the preferred sup-norm radius is

$$
\rho=\frac{808514697}{200000000000}=0.004042573485.
$$

If a feasible pose satisfies `||z-z_*||_infinity < rho` at side `U`, it equals the
retained Trump pose.
A pose in the same ball fitting at side `s' <= U` must also equal that pose, with
`s'=U`. A further local estimate at side `U+sigma` is

$$
\sigma\ge-\frac{2574612531}{200000000}\|z-z_*\|_\infty^2.
$$

BC-241 accepted a source-distinct review of the exact tangent endpoint, aggregate
rational arithmetic, norm conversion, selected face calculations, and mutation controls.
The quantitative theorem remains **retained-record-dependent**: the radius artifact does
not retain every per-face primal and dual witness, and that review did not independently
rerun all radius face programs.
Its scope must survive any use in a final proof.

A global proof could use this neighborhood as its last step if it first proved that
every putative packing below `U`, after justified symmetry and label choices, enters
that ball. No such capture statement has been established.
The local chart does not exclude distant contact types, classify all minima, or show
global uniqueness.

Sources: `packing/cases/trump11/isolation-theorem.md`, “Theorem” and “Replay Boundary
and Refusals”;
`packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md`,
BC-240/241 outcomes;
`packing/campaign/series/series-000-smoke-and-calibration/results/bc-241-trump-local-theorem-review.json`.
The theorem document’s opening “awaiting review” is historical; the agenda records the
completed review. The frontier’s statement that the qualitative result has no quantified
radius remains correct for exp013, but does not describe this later extension.

## The Latest Density Evidence

An absolutely continuous covering density is a nonnegative integrable function `f` on
the container satisfying `integral_Q f >= 1` for every contained unit-square placement
`Q`. If its total mass is below eleven, eleven interior-disjoint squares cannot fit:
shared boundaries have area zero, and summing their required integrals exceeds the
available mass.

The weak dual assigns nonnegative weights `w_j` to full-size placements `Q_j`, with
weighted depth

$$
\sum_j w_j\mathbf1_{Q_j}(x)\le1
\quad\text{for Lebesgue-almost every }x.
$$

Every such dual family has mass `D=sum_j w_j` no larger than the total mass of any
covering density. This proves weak duality.
The accepted contract proves neither strong duality nor attainment.
The uniform average of the eight dihedral images of Trump’s packing is a feasible dual
family of mass eleven at side `U`.

**Exp113** asks whether arbitrary reweighting on that fixed support can exceed eleven.
The support consists of 60 distinct placements in eight orbits, of sizes
`(4,8,8,8,8,8,8,8)`. Twenty exact necessary depth rows yield a finite LP optimum
`56/5=11.2`, with matching exact primal and upper witnesses independently checked.
Together with the feasible uniform control, this places the true fixed-support supremum
in `[11,56/5]`. The finite-row optimizer is only a candidate for full a.e. feasibility.
Its per-member orbit weights are

$$
(1,0,2/5,1/10,0,1/10,3/10,0).
$$

**Exp115** exhausts all 134 distinct pairs whose weights sum to more than one.
Every pair has an exact separating axis, independently checked.
Thus the proposed positive-area overweight-pair obstruction does not exist.
H-105 is rejected, while H-099 and the full candidate remain unresolved.
Three squares of weight `2/5` can have excessive common depth although no pair is
overweight; pair exclusion cannot certify full feasibility.

The next proposed discriminator is complete positive-area-face verification of the
unchanged candidate.
One route probes every open segment of its supporting-line arrangement on both sides;
another independently reconstructs every vertical slab and open depth band.
Both need completeness arguments and boundary controls.
Vertex-only closed-set depth is unsuitable because excessive depth confined to touching
boundaries is allowed in the a.e. formulation.

If the mass-11.2 candidate passes, weak duality rules out an equality density of mass
eleven at Trump’s side.
It would identify a limitation of this relaxation, not refute Trump’s optimality.
Failure of this candidate likewise says nothing decisive about other weights.
A fixed-support ceiling of eleven would close only that support.
None of these outcomes settles whether useful covering densities exist at smaller sides,
which is the separate below-Trump question.

Sources:
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-242-full-size-density-proof-contract.md`;
`packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-113-h-099-trump-support-screen.md`;
`packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-115-h-105-fixed-candidate-pair-obstruction.md`;
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-254-post-screen-next-discriminator.md`,
“Next Step: Complete Face Verification, 2026-09-06”.

## The Latest Restricted-Orientation Evidence

Stromquist’s existing restricted theorem bounds the exact 0°/45° class below by
`2+(4/3)sqrt(2)`, approximately 3.885618. Trump beats this value, proving that oblique
orientations matter.
H-036 asks for a more robust restriction: no packing below `q=1939/500=3.878` when every
square’s angle independently belongs, modulo quarter turns, to

$$
[-\pi/720,\pi/720]\cup[\pi/4-\pi/720,\pi/4+\pi/720].
$$

These are closed ±0.25° neighborhoods.
They leave intermediate orientations, including Trump’s tilt, outside the claim.

**Exp114** verifies seven fixed-formula auxiliary clauses at side 3.878, exactly at 0°
and 45°. They concern a ten-point cover, localization of its 45° avoiders, three
separate forced-point implications, and twelve-point coverage.
The positive result uses a reviewed exhaustive center-stratum algorithm and independent
exact input/receipt checks.
It is not a second exhaustive implementation or a standalone positive coverage
certificate. H-104 is accepted at this scope; H-036 remains unresolved, and no packing
bound changed.

The proposed continuous extension must include every allowed angle and center, including
wall contact and interval endpoints.
A uniform concentric-core transfer loses too much side to reach 3.878. The current
alternative maps a fixed center square into the true angle-dependent containment domain
and covers it by closed rational triangles.
Assigning one frozen point to each triangle reduces membership to polynomial
inequalities at its vertices.
Exact nonnegative Bernstein coefficients can certify a complete angle slab.
Mixed coefficients merely leave the sufficient certificate unresolved; they do not
supply a geometric counterexample.
Even a genuine one-square escape refutes only the auxiliary clause, whereas a packing
counterexample to H-036 needs eleven verified squares.

If all continuous auxiliaries hold, a scaling-and-counting argument excludes the whole
restricted family. One enlarged square avoiding the ten-set must contain three distinct
points of the twelve-set; the other ten squares require distinct remaining points, but
only nine remain. Reflection must apply to the whole configuration.
The continuous proof is still a proposal, and its first ten-set obligation would
complete only one of the required clauses.

Sources:
`packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-114-h-104-fixed-side-auxiliaries.md`;
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-instrument-design.md`,
“Fixed Claim” and “2026-09-06: Next Allocation After H-104”;
`packing/campaign/hypotheses/H-036-robust-restricted-orientation.md`.

## From the Current Portfolio to a Global Proof

Agenda 024 currently recommends the unopened scalar probe, complete density
verification, and the first continuous-angle certificate.
Its priorities are reviewable choices.
The broader objective requires assessing several possible levels of progress:

| Level | Useful result | Additional premise needed to resolve eleven squares |
| --- | --- | --- |
| Improve the current scalar certificate | Certify `61/16=3.8125`, or identify a precise obstruction in the retained language. This would close about 3.69% of the remaining bound gap. | A mechanism that continues substantially beyond that rung; extrapolating two LP objectives is insufficient. |
| Change weights, sites, or witnesses | Remove a named limiting pose through new support, angle-dependent kernels, segments, or a finite existential witness menu. | Complete coverage over all poses, with containment and counting valid for the richer objects. |
| Solve the density question | Certify a useful primal below Trump, or establish an exact obstruction to a proposed equality route. | Continuum primal coverage and, for endpoint arguments that need them, justified limiting or attainment statements. |
| Prove restricted structure | Exclude angle compositions or wall-support cases with exact inequalities. | A complete reduction placing every possible competitor into covered cases or explicitly controlled residual cases. |
| Capture globally and close locally | Prove every competitor below `U` enters the Trump neighborhood. | Complete global case coverage, rigorous pruning, justified symmetry handling, and sufficient assurance for the invoked local theorem. |

BC-245 supplies a finite typed stationary language: a branch records which square owns a
separating axis, its direction and order, wall-support features, and angle charts.
Necessary Fritz–John conditions retain ordinary and abnormal branches, ties, zero
multipliers, and rattlers.
This is a representation theorem, not an enumerated atlas.
Discarding those cases without a proof would invalidate completeness.
A contact graph alone omits geometric data needed for exclusion.

A possible synthesis is to turn a valid nearly tight covering measure into restrictions
on which witnesses different squares can occupy, then prove matching, capacity, or
wall-to-wall inequalities that force a small family of geometric branches.
Such an argument would connect the productive lower-bound method to the existing local
endpoint. It is an open strategic possibility.
No retained result establishes that reduction, and conflict cuts added to a one-body LP
do not acquire multi-square meaning automatically.

Review should therefore ask which new lemma has a credible path to complete coverage,
which existing restriction is spending effort for too little information, and what
bounded test would distinguish the alternatives.
A creative direct geometric argument could bypass several steps in the current program.
Its value would lie in its stated hypotheses and complete treatment of arbitrary
orientations, rather than agreement with the agenda’s selected work.

Sources: `docs/project/specs/active/plan-2026-09-06-post-381-research-sequence.md`,
“Mathematical Discriminators” and “Coverage of the Earlier Reviews”;
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-245-typed-backbone-theorem-packet.md`;
`packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md`, “Current Allocation”.

## Reading the Source Record Without Changing Its Claims

The latest allocation and Session 089’s “Readiness and Follow-Up” supersede older launch
schedules retained inside the agendas and continuation handoff.
The scalar invocation has not run; the adaptive program’s two selected control slices
have completed; exp113, exp114, and exp115 must be read as completed results.
No packing bound moved in that session.
The density design document’s dated complete-face section supersedes its opening
pair-test recommendation.
The restricted design’s post-H-104 section supersedes its earlier proposal to run the
exact-angle discriminator.

Source documents sometimes retain older states intentionally.
The local theorem’s “awaiting review” label predates BC-241 acceptance.
The fixed-weight H-092 negative is reported as reviewed but remains pending integration;
its separate evidence is not available in this packet.
Some narrative passages call a result “newest” although later register entries exist.
The result register, specific experiment verdicts, and dated outcome amendments
determine the relevant mathematical scope; none justifies silently upgrading a candidate
or a partial computation.

Sources: `packing/campaign/agent-sessions/session-089-agenda024-next-phases.md`,
“Readiness and Follow-Up”; `SYNOPSIS.md`, “Current Handoff”;
`packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md`, “Current Allocation”.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
