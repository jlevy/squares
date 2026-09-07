# BC-259: Positive-Inclusion Adoption Instrument Review

Status: **GO for the frozen instrument and prospective protocol**, subject to the
coordinator completing engine and record admission before any scientific call.
The independent review found no launch blocker.
The actual source binding and seven scientific box inclusions remain untested; no
adoption result is claimed.

This is `think-9mql`, the second and final BC259 readiness slice in
[Session095](../../../../agent-sessions/session-095-collision-cover-and-support-ceiling.md).
Dispatch: 2026-09-07 at 12:27:00 UTC. Observed reviewer start: 12:27:52 UTC. The
original hard deadline is 12:57:00 UTC. The author froze both implementation files at
12:37:05 UTC. The mathematical and code review completed at 12:42:02 UTC, 14 minutes 10
seconds after the observed start; this note’s final formatting followed within the
original slice. The reviewer read both frozen source assessments, including
[the positive-only proposal](bc-259-support-adoption-review.md#cheaper-ceiling-only-row-predicate),
but did not inspect the new implementation before its author froze it.
Only this review note is in the reviewer’s write scope.

## Sufficient Contract

Let $\mathcal F$ be the complete deduplicated D4 support, with orbits $O_j$ of sizes
$d_j$. Average any nonnegative feasible weighting over D4, obtaining per-placement
weights $a_j$ without changing its mass or a.e. feasibility.
For each fixed positive-area box $B_i$, choose distinct placements $S_{ijk}\in O_j$,
with exactly $R_{ij}$ choices in orbit $j$, and prove

\[
B_i\subset\operatorname{int}(S_{ijk}).
\]

For every $x\in B_i$, the full depth is at least $\sum_j R_{ij}a_j$. Since the box
cannot be contained in a Lebesgue-null exceptional set, a.e. feasibility implies
$Ra\leq\mathbf1$. Thus $\lambda\geq0$, $\lambda^TR=d^T$ and $\sum_i\lambda_i=11$ imply
that the total mass is at most eleven.
The independently validated original packing supplies the matching feasible average.

This proof needs no information about unselected placements’ intersection with the
boxes. In particular, neither constant full incidence nor strict exclusion margins are
necessary. A failed attempt to supply a required inclusion is an unresolved certificate,
not evidence against the support claim.
The selected instrument must call its rows necessary lower-incidence rows, not a replay
of every archived membership sign.

The frozen seven rows request $3+3+7+6+6+8+8=41$ selected incidences, all with radius
$1/100000$ and the unchanged archived centers and multipliers.
Selection may inspect additional members to find these inclusions; 41 is the accepted
inclusion inventory, not a bound on all work performed.
One new history-free checker is sufficient: the archive already supplies the proposed
certificate. There is no need for a new search producer or another run of its LP.

## Verified Soundness Boundaries

| Boundary | Required behavior | Failure prevented |
| --- | --- | --- |
| Source and real embedding | Use the fixed current source through accepted public `reconstruct_source`; retain the exact side, eleven seeds and original packing validity | Certifying a different construction or an invalid baseline |
| Complete quotient | Retain all 88 labelled images, 60 distinct placements, eight complete orbits and every preimage label | Losing placements or confusing labels with distinct atoms |
| Orbit correspondence | Compare full orbit corner-key sets and obtain a bijective archive-to-current permutation | Counting the same geometric orbit under two columns |
| Selected members | Meet every row’s per-orbit quota using distinct deduplicated placement IDs within that row | Double-counting stabilizer aliases as extra coverage |
| Box inclusion | Validate cyclic unit-square geometry and all four strict inward affine minima on the whole closed box | Accepting a center sample, boundary contact or wrong orientation |
| Container and area | Require the unchanged positive radius and all four strict box-containment margins | A null or inadmissible box supplying a necessary row |
| Upper arithmetic | Check every integer count, nonnegative multiplier, column identity and total eleven exactly | A complete-looking but insufficient inequality |
| Completion | Emit a positive result only after source binding and all seven quotas and arithmetic checks finish | Partial work, timeout or a malformed input being accepted |

Member identities may repeat between different rows; they may not be counted twice
within one row.
Complete orbit disjointness and the bijective permutation ensure that two
different columns cannot hide the same placement.
The 88 labelled preimages are provenance for the baseline, not the membership IDs to
count toward quotas.

The accepted public source reconstruction, exact field arithmetic, exact signs and
original seed factory are shared foundations.
The new inclusion check is independent of the archived interval checker.
Reusing those foundations is appropriate, but it is not an independent derivation of
Trump’s construction.
The legacy history-bearing `replay_packet` and target-disabled toy `replay_upper` are
not the new interface.

The frozen [checker](../../../../../devtools/check_trump_support_adoption.py) satisfies
these boundaries. Its `_binding` independently enumerates all eight images of every
supplied seed, compares the complete sorted orbit keys and reconstructs every labelled
preimage.
It checks the original packing and each cyclic unit square before accepting the
source metadata. JSON serialization equality distinguishes Boolean labels from integer
labels.
`_specification` validates exact rational types and bit limits before certificate
arithmetic, then checks the multiplier identities.

`check_certificate` binds the archive representatives by a bijective full-orbit-key
permutation. It selects member IDs only from the validated deduplicated support and
checks distinctness within each row.
`contains_box` tests all sixteen inward corner-edge determinants for each selected
inclusion, using the square’s verified orientation.
Strict positivity at all four box corners implies strict positivity over their whole
convex hull.
The output’s positive flags are constructed only after every row, source and
arithmetic obligation succeeds.

Static inspection of `trump_specification` found the seven archived centers, radius,
representatives, sizes, original counts and multipliers unchanged.
The lazy `check_trump` entry point checks the current polynomial divided by its leading
coefficient five, the declared interval `[9/25,37/100]`, eleven seeds, sixty placements
and eight orbits. The interval is exactly the archived `(36/100,37/100)` interval in
canonical rational serialization.
The source constructor and this specification were not called during review.

## Prospective Once-Only Protocol

Before invocation, the coordinator must bind the reviewed immutable engine, the exact
explicit CLI selector and the unchanged seven-row data in a committed prospective
record.
Independent source-free readiness, push validation and the committed records gate
must be accepted before the launch cutoff.
This readiness slice does not allocate a scientific call.

The selected scientific operation is one independent archived-certificate checker call,
not a new producer followed by a second same-source run.
Run it from the isolated immutable `packing/` directory with the project Python 3.14
interpreter and the declared import path.
Require fresh output paths, retain stdout and stderr separately, and capture the exact
command, revision, observed UTC interval, actual external exit and outer wall/CPU.

The coordinator proposes an external 60-second TERM deadline followed by a two-second
KILL grace. That is not a strict 60-second completion cap; record both the deadline and
the grace. Imports, source reconstruction, membership checks, output and termination
belong to the same supervised child attempt.
Any timeout, nonzero exit, malformed or incomplete output, failed required predicate or
unmet inclusion quota leaves adoption unresolved.
No repeated call, changed row, changed radius, LP or arrangement extension follows
automatically.

Only an actual exit-zero complete result with every source and certificate predicate
verified can support a new H099 disposition.
Exact counts and status literals must be taken from the frozen implementation and
prospective record, not inferred from an exit code or a human-readable verdict alone.
The accepted scope would be optimum eleven on this fixed support at the exact Trump
side. It would not establish an unrestricted density equality, a below-side transport or
a global packing bound.

The reviewer read the coordinator’s complete prospective exp128 draft at 12:36:14 UTC,
before registration or commitment.
Its once-only `--target-trump` command, original 13:09 launch and 13:12 finish cutoffs,
timeout grace, fresh-output requirement and nonacceptance rules match this contract.
The pending engine pointers and false selftest flag are intentional pre-admission state,
not evidence of completed readiness.
The coordinator applied the requested wording correction: selected member identities are
discovered and source-bound by the checker; the archived data prescribes the per-orbit
quotas, not particular member identities.
The final frozen-code comparison confirmed the acceptance literals:
`status=verified_support_ceiling`, literal `ceiling_proved=true`,
`predicate=necessary-lower-incidence`, `source=trump11-v1`, `upper_bound="11"`,
`baseline_mass="11"` and literal `baseline_verified=true`. The full 88/60/8 quotient,
seven fixed rows, 41 selected incidences and every literal
`strict_inclusions_verified=true` remain required; exit zero alone is insufficient.
The result’s kind is `d4-positive-inclusion-support-ceiling`, with version `1`. The
protocol retains the whole-child timeout and does not invent a second producer or reader
invocation.

## Independent Checks and Remaining Premises

The reviewer read both frozen implementation files before running the focused controls.
The twelve [tests](../../../../../tests/test_trump_support_adoption.py) use an unrelated
rational nine-square packing and a nonrational square over the positive `sqrt(3)`
embedding. The latter distinguishes two placements with a common center and checks
reversed corner orientation.
Mutations exercise full-source labels and metadata, duplicate support members, the
nontrivial orbit permutation, quotas, box admission, foreign-field coordinates, invalid
packing or corner order, dimensions, rational types, multiplier signs and identities,
and the output byte cap.
Mocked CLI controls cover the required selector, complete success and a refusal
returning nonzero with unresolved status.
No separate operating-system timeout experiment was run; that cap belongs to the
prospective external supervisor.

The autouse guard forbids `check_trump`, `trump_specification`, the accepted scientific
seed builder and the old actual Trump-field test helper.
Calls to the public source reconstruction use only the injected unrelated fixtures.
The tests neither import the archived executable nor evaluate the fixed scientific
source or boxes.

All commands ran from `packing/` with the project Python 3.14 interpreter.
Each used `/usr/bin/time -p` and `PYTHONDONTWRITEBYTECODE=1`; pytest additionally used
`PYTHONPATH=src` and disabled its cache provider.
Ruff and its formatting check disabled their caches.
The three tool checks ran in parallel; their times below are individual outer-process
measurements, not a sequential elapsed total.

| Check | Outcome | Wall seconds | User seconds | System seconds |
| --- | --- | ---: | ---: | ---: |
| `pytest -q -p no:cacheprovider tests/test_trump_support_adoption.py` | 12 passed; pytest reported 0.50 seconds | 0.69 | 0.63 | 0.03 |
| Ruff check, both frozen files | Clean | 0.05 | 0.02 | 0.01 |
| Ruff format check, both frozen files | Already formatted | 0.04 | 0.02 | 0.01 |
| BasedPyright, both frozen files | Zero errors, warnings or notes | 0.84 | 1.47 | 0.10 |

The reviewed scientific CLI is
`.venv/bin/python3 -m devtools.check_trump_support_adoption --target-trump`, using the
exact project interpreter and external supervisor in the prospective record.
It is not an arbitrary-packet interface or a replay of screening history.
Readiness does not establish source adoption, quota success or execution cost on the
actual field. Those remain the sole prospective call’s obligations, after the frozen
engine, independent review, push gate and committed record gate are admitted.
No target, scientific field, archived checker or retained geometry was evaluated here;
the reviewer changed only this note.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
