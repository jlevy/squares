# Review: PR #14 and the Executable Square-Packing Research Program

**Date:** 2026-08-23

**Author:** Codex (agent)

**Status:** Current; deep mathematical-strategy delta complete

**Reviewed:** [PR #14](https://github.com/jlevy/thinking-scratchpad/pull/14), initially
at `fa538931b20fef0f51dffedb9e4d7071603b7790`, reassessed as its branch and description
advanced, and delta-reviewed through final source head
`f9f119a2a67e682607faf9d9f1623ea4ae1c83d6` and merge commit
`8926a7c04ba9e59cf988b6d00a28d3ad756a5d0f`, together with the full
`explorations/packing/` research, tooling, campaign, corpus, and source archive.

The initial findings and reproduction results below describe the first exact PR head.
The dated reassessments record the five later commits and give every affected finding an
explicit disposition.
The later section
[Changes applied on the stacked review branch](#changes-applied-on-the-stacked-review-branch)
records narrow repairs made after the review; it does not retroactively change the
reviewed evidence.

## Verdict

**PR #14 is merged as a useful prototype.
Do not run the proposed unattended census yet.**

The project has unusually strong raw material: a serious primary-source archive, an
honest distinction between upper bounds and proofs, a useful `n = 1…100` scalar corpus,
an exact verification of Trump’s `n = 11` construction, a defect log that records
negative results, and the right high-level decomposition

```
proposer -> quench -> canonicalize -> independently verify -> observation log -> atlas
```

PR #14 also points in the right direction.
A canonical identity, an atlas, a queue that can stop itself, and a morning report are
all necessary. The problem is that the new pieces do not yet implement the claims made
for them.
The current runner can promote an archive whose rows its own guard rejects; the
result contract trusts a proposer’s scalar `overlap: 0` without storing enough geometry
to check it; the criterion evaluator cannot evaluate the census, rarity, or equal-budget
hypotheses it is meant to run; the contact certificate is not invariant under
reflection; the atlas records non-converged stopping points as basins; and “fixed
angles” still has several cell-dependent answers.
These are trust-boundary defects, not polish defects.

The research program also overstates three premises.
The angle in Trump’s packing is not an algebraic number; rigidity does not imply a small
basin of attraction; and grid optimality for `m² - 3` is known only for the proved
finite cases, not as a general family.
Those errors are especially important because they determine which experiments the
current plan promotes.

The ambition should remain.
Each strategy needs a runnable proposer, an independent validity oracle, an exact budget
meter, a provenance-complete event archive, a criterion-specific evaluator, and an
explicit promotion path from floating candidate to exact certificate.
Once that spine exists, the best portfolio is broader than the current one: active-set
and contact-graph search, rare-event simulation, continuation with branch switching,
quality-diversity and packing surgery, and a proof-producing unavoidable-set
cutting-plane loop.

This review maps that repair and research program into epic
[`think-6sst`](#the-epic-and-its-bead-map), with four direct focus epics and 26 primary
work beads: five for Correctness, seven for Process, nine for Insight, and five for
Efficiency. Four narrower ambiguity beads remain nested under their owning work items.
Existing beads are referenced rather than silently duplicated.

Findings use the following severities:

- **P0 — blocker:** can make an invalid run look valid, change the scientific answer, or
  invalidate an unattended campaign.
- **P1 — high:** invalidates a subsystem, a reported interpretation, or a promised
  research capability.
- **P2 — material:** drift, performance, or reproducibility defect that must be
  corrected before scale-up.

## Scope and standard

This was a program review, not only a diff review.
It covered:

- every research report, review, active spec, handoff, postmortem, hypothesis,
  experiment artifact, and generated synopsis under `explorations/packing/`;
- the `n = 1…100` frontier artifacts, strategy catalogues, source-availability record,
  local paper archive, and the current public record catalogue;
- the exact field arithmetic and verifier, Rust annealer, LP quench, canonicalizer,
  atlas, runner, ledger, schema layer, regression checks, soundness perimeter, and full
  gate;
- the exact PR head, not the PR description: commit
  `fa538931b20fef0f51dffedb9e4d7071603b7790`;
- current primary sources, including the EJC survey and proofs, the live Squares in
  Squares catalogue, and the 2025–2026 asymptotic papers.

For this review, a strategy is **fully executable** only when all seven questions have
machine-checkable answers:

1. What command or API proposes configurations?
2. What exact counter limits the work, and can the command exceed it?
3. What complete artifact preserves every result needed to reproduce the conclusion?
4. What independent code rechecks containment and every pairwise separation from the
   stored pose?
5. What deterministic quench or certification relation defines the object being counted?
6. What evaluator implements this hypothesis’s declared metric, accept rule, and kill
   rule?
7. How is a promising float promoted to a rigorous upper bound or a failed promotion
   retained as evidence?

A prose answer, a scalar side length, or a visual plateau is not enough.

## Operating model: correctness, process, insight, and efficiency

The review and remediation program uses four independent dimensions.
The plain-language principle is the durable name; the parenthetical name is the
specialist role an agent takes while working in that lane.

| Principle | Specialist role | Owns | Authority boundary |
| --- | --- | --- | --- |
| **Correctness** | Soundness | Mathematical claims, primary-source coverage, rigorous proof and certification, numerical-to-exact promotion, independent validation | May veto claims and promotions that exceed the evidence |
| **Process** | Discipline | Preregistration, schemas, lifecycle, provenance, event and defect logbooks, reconciliation, and handoffs | May veto runs and records that cannot be reconstructed or whose acceptance rule moved |
| **Insight** | Creativity | Structural explanations, conjectures, diverse search and proof mechanisms, cross-`n` grammar, and selection of tractable questions | Proposes and prioritizes; cannot certify its own proposal |
| **Efficiency** | Infrastructure | Stable executors, profiling, batching, parallelism, caching, visualization systems, and measured agent-loop latency | May block unstable scale-up; cannot relax Correctness or Process controls |

An agent normally focuses on one dimension at a time.
The standard handoff is **Insight proposes → Process preregisters → Efficiency executes
→ Correctness validates → Process records**. This is not a claim that every small change
needs five owners; it is a prohibition on self-promoting an idea because the same agent
also wrote the code, produced the plot, or documented the run.

Basin visualization deliberately spans Insight and Efficiency.
`think-vcnx` owns the mathematical questions and honest encodings; `think-djvs` owns the
scalable explorer, deterministic snapshots, and traceability to source observations.
The views must distinguish certified facts, observed samples, and inferred relations.
In particular, graph layout, proximity in an embedding, and a sampled cluster do not
prove adjacency, metric distance, or connectedness in configuration space.

## What was verified by running it

| Check | Result |
| --- | --- |
| PR identity | Exact head is `fa538931…`; 11 changed files, +1,384/−12. No PR checks, reviews, or comments were present at review time. |
| `verify_trump11.py` and exact negative controls | Pass. The built-in Trump witness is exactly valid in its declared degree-8 field; all 55 pairs are decided and the published side polynomial vanishes. |
| `test.sh --strict` | Exits non-zero because `README.md` omits the new atlas from the layout tree. The gate runs `canonical_check.py`, but does not run `atlas_check.py` or `tools/regression_test.py`. Its unfrozen `uv run` calls also rewrite the tracked `uv.lock` under this environment. |
| `runner.py preflight` | Reports `PREFLIGHT PASSED`. An adversarial archive containing five rows with `overlap: 0.001` is nevertheless rebuilt by `cells_from` and receives `unresolved; clauses 1–4 pass`. `read_lines` also writes the invalid row before raising its guard. |
| Canonical checker | The shipped checker passes. A valid four-square configuration and its vertical reflection have the same geometric key but contact certificates `8dc5…` and `dd8f…`. |
| Angle-class stability | `[0, 0.75e-6, 1.5e-6]` groups as sizes `[2,1]`; the permutation `[0.75e-6,0,1.5e-6]` groups as `[3]`. |
| Canonical worst case | The empty, single-colour graph takes 0.098 s at `n = 7`, 0.818 s at `n = 8`, and 7.91 s at `n = 9`; the claim that exhaustive individualization is cheap through `n = 12` is false. |
| Atlas checker and invariants | The shipped `n = 5` census has only 1 of 12 quenches marked converged but records 12 basins and misses the known optimum. Independently, `Atlas(5)` accepts an `n = 1` key and atlases with `quantum = 1e-3` and `1e-6` merge without refusal. |
| Quantization boundary | Two one-square configurations 2e-12 apart, straddling a 1e-6 rounding boundary, report `same-arrangement-different-metric`; `Atlas.add` stores both as separate basins. |
| Fixed-angle objective | One fixed three-angle vector, evaluated from eight starting centre sets, returns four distinct sides: 2.473119696597, 2.484453371849, 2.614379463537, and 2.628899625295. Fixed angles alone do not define one objective value. |
| Generic exact field | `NumberField([1,-3,2], (0,7/5))` accepts the reducible polynomial whose isolated root is 1, but `(alpha - 1).is_zero()` returns false. The advertised equality and sign completeness needs the unverified minimal-polynomial precondition. |
| `n = 17` discrepancy | The stored degree-18 polynomial has root `4.6755300936045509516…`. The catalogue decimal is within 9.52e-16; the paper transcription `4.6755300960455` is 2.44e-9 away and gives polynomial residual 56.9. The corpus’s “unresolved” label can be narrowed to a source typo or different equation, not an equal ambiguity. |
| Frontier gap ordering | The three smallest open scalar gaps in the repository are `n = 97` (0.05573), `78` (0.06275), and `61` (0.07180); `n = 11` is fourth (0.08823). |

The Java-runtime warning printed by this machine’s environment was unrelated to the
Python checks and did not affect their results.

## Reassessment after PR #14 advanced

PR #14 added three commits after the initial review:

- `4310096` changes the bracket quench to narrow its angle window only after a failed
  sweep, raises the default sweep cap, and gives the atlas check a realistic wall
  budget;
- `f4d3031` adds the circular angle quantizer, closed-form recognizer, fixed-seed golden
  basin map, and a proved-case convergence ladder; and
- `5b1ae65` wires per-step timing into the gate.

The D-030 change is a substantive repair.
The same `n=5` atlas fixture that initially reported one convergence in twelve now
converges on all six current proposals at its declared budget.
The circular quantizer also closes the `0`/`π/2` seam.
Neither change repairs the atlas contract itself: the new golden contains one
non-converged `n=3` endpoint among four proposals, stores it as a basin, and passes
because the guard accepts any census with at least half its quenches marked converged.
The checker also printed ten proposals after a six-proposal census because its final
summary included four synthetic deduplication re-offers; that bookkeeping error is fixed
and recorded as D-037 on the stack.

The new golden exposed a second trust problem.
After rebuilding the checked-in Rust engine, its committed seed-7 `n=10` ladder did not
reproduce: annealing started `0.077126752369` above the proved value and the quench
ended at `(8 + 5√2)/4`, still `0.06066` high, rather than at `s(10)`. The `n=3` and
`n=5` map also drifted.
The tool nevertheless describes its fixed seeds as reproducible and, when run
standalone, consumed whichever pre-existing release binary happened to be present.
This is F-16, not evidence against the known `n=10` optimum.

Reviewing the new terminator found D-036: `_free_sweep` returned the same tuple after a
deadline break as after examining every coordinate, so `quench_bracket` could report
`converged=True` and `free pass clean` for an incomplete pass.
The stacked branch now propagates the timeout and has a named regression.
That repair makes the status honest; it does not upgrade coordinatewise stationarity
into local optimality.

The updated dispositions are therefore:

| Finding | Disposition at `5b1ae65` plus the stacked fixes |
| --- | --- |
| F-05 | Partially repaired: both keys are D4- and seam-invariant on the fixtures. Order-dependent angle clustering, exact two-hash equality, quantization splits, and factorial canonical labeling remain. |
| F-07 | The D-030 cause is fixed for the `n=5` fixture, but non-converged endpoints are still counted and event order is still absent. Remains P0. |
| F-10 | Deadline propagation is fixed as D-036. The result still certifies only finite coordinate probes, not a coupled local optimum. |
| F-15 | Atlas, golden, regression, and timing steps are now wired. The raw updated branch’s golden is red against its own source-built engine, the gate costs about eight minutes, and no PR CI exists. |
| F-16 | New P0: the golden mixes oracle checks with exact characterization data and was not hermetic or reproducible as committed. Partially repaired on the stack; the atlas promotion policy remains open. |

No research-remediation bead is closed by these changes.
The fix narrows the blocker from “the cold quench demonstrably cannot arrive at `n=5`”
to “the project still lacks a sound definition and provenance-complete record of what
may be counted as a basin.”

## Second reassessment at PR #14 head `c412b8c`

PR #14 advanced again during final validation:

- `64ade69` splits the golden into a millisecond stored-file audit and an explicit deep
  regeneration, and replaces the expensive atlas census with one real `n=4` smoke quench
  plus synthetic store keys; and
- `c412b8c` records the seam defect as D-031 and the previously fixed but unguarded
  claim/release defects as D-032 and D-033, then derives another synopsis count from the
  ledger.

The fast/deep split is useful, and recording D-031 through D-033 is the right correction
to the research history.
It also exposes a new enforcement error.
On the raw PR head, `./test.sh --strict` does **not** imply `--deep`, even though that
exact strict command is the handover checklist.
The fast golden reads stored side lengths and trusts stored `valid` and `converged`
booleans; it has no poses from which to re-run the independent verifier and does not
execute the quench. The shortened atlas check offered six entries all marked converged
and then called `non_converged == 0` proof that the counter works.
Consequently the default strict gate no longer carries an executable recurrence test for
D-030, the bug that motivated the validation suite.

The accompanying explanation also calls the seven single-seed convergence ladder
“census-scale evidence.”
It is not: those starts are deliberately selected to lie in the target basins.
The fixed-seed case maps are the census-shaped experiment, and they still admit and
count a non-converged `n=3` endpoint.
The stacked branch makes strict imply deep, source-builds the engine for every
deep/update run, checks stored count identities on the fast path, and feeds the atlas
one explicit `converged=False` offer so the counter’s false branch is exercised.
Those repairs restore the regression without pretending the open promotion policy is
solved.

Finally, D-033’s new ledger entry says timezone-aware leases are normalized to aware
UTC, but the implementation at `ledger.py:298–303` uses `.replace(tzinfo=None)`. That
drops an offset rather than converting it.
The runner currently emits UTC, so its own fixtures are safe; the generic contract and
the “fixed” claim are still too broad.
Both D-032 and D-033 remain explicitly without regressions, which confirms F-04 rather
than closing it.

| Finding | Disposition at `c412b8c` plus the stacked fixes |
| --- | --- |
| F-04 | D-032/D-033 are now recorded, but recovery is unguarded and non-UTC offsets are still mishandled. Remains P1. |
| F-07 | The structural atlas check is faster and clearer, but only the strict/deep golden runs a real multistart map; non-converged observations are still promoted. Remains P0. |
| F-15 | The routine gate is faster. The stacked strict handover remains deep and hermetic; GitHub still has no configured PR checks. |
| F-16 | Fast scalar-oracle audit and deep characterization are now distinct code paths. The fixture still has no stored poses and the policy still byte-compares discovery data. Remains P0. |
| F-17 | New P0: raw strict mode skipped the only producer-level golden regeneration and the atlas’s claimed non-convergence test never supplied a false value. Repaired on the stack; retain a negative control for the strict/deep implication. |

Our two initial review-found defects are D-036 and D-037 so the defect ledger retains
merged PR #14’s D-031 through D-035 without collision.
The same 17 epic children own the new work; F-17 belongs to the existing enforcement,
quench, and atlas beads.

## Third reassessment: the four ambiguities and final merged delta

The four questions added under “What is ambiguous” are not peripheral unknowns.
They expose missing definitions in the counted object, the numerical identity relation,
the endpoint-promotion policy, and the statistical estimand.
The earlier review covered pieces of all four in F-05, F-07, F-10, F-13, F-14, F-16,
O-03, A-02, and Q-04, but it did not give each ambiguity a complete disposition.
F-18 through F-21 below now do so.

| PR ambiguity | Answer | Consequence now | Executable resolution | Bead |
| --- | --- | --- | --- | --- |
| Is a basin well-defined at small `n`? | Not under the current two-hash endpoint definition. `n=3` gives an exact positive-dimensional counterexample. | Small-`n` “distinct basin” counts are quantization-dependent endpoint-cluster counts. | Detect rank deficiency, continue terminal stationary sets, and count connected components under a declared quench and quotient. | `think-0yo9` |
| What are the unrecognised singletons? | The stored evidence cannot decide. “Higher degree” and “not converged” are only two of at least six live classes. | They are unresolved endpoints, not established local optima or basins. | Preserve poses and active sets; run a precision/budget ladder, directional/KKT tests, component detection, and exact promotion. | `think-aans` |
| Does D-021’s `1e-11` floor merge basins? | D-021 bounds error in the scalar side, not distance between configurations or terminal components. | `closest_pair` cannot validate identity; equal-side rows may differ and one component may contain many keys. | Calibrate pose, topology, and interval separation across tolerance sweeps; carry an explicit ambiguity graph and count interval. | `think-3szr` |
| Is uniform multistart the right null? | It is one useful baseline, not a canonical or distribution-free null. | Every frequency and rarity statement is conditional on an incompletely recorded proposer/quench regime. | Benchmark several named proposal measures at equal pair tests and report each conditional probability with uncertainty. | `think-apwt` |

The description’s twelve-start `n=5` result is also not a durable result at the current
head.
No checked-in event or atlas artifact preserves those twelve poses, proposal order,
or regime. The current raw-head golden instead contains six `n=5` proposals, five rows,
and `found_optimum: false`; the source-built stacked golden contains six proposals, six
rows, and also misses the optimum.
Even if the historical `1/12` versus `4/12` counts are accepted, the point ratio is
`0.25`, not H-012’s registered “below `0.1`” threshold, and exact 95% binomial intervals
for the two marginal probabilities are approximately `[0.0021, 0.3848]` and
`[0.0992, 0.6511]`. That sample is a useful smoke observation, not evidence for the
rarity premise, and it does not test H-012’s registered `n=10,11` sweep.

The final `f9f119a` source delta correctly elevated terminal isolation into D-034 and
added the exact `n=3` sliding-family witness.
It also made one new rank-free claim: the two `n=5` rows were called one connected
five-dimensional family solely from 11 raw contacts versus 16 coordinates.
Fixed-cell LP degeneracy is measurable, but it does not alone determine the full
angle-moving terminal manifold.
The living docs now retain the exact `n=3` proof and mark `n=5` unresolved pending
active-matrix rank, full Jacobian, feasible-null-direction, and continuation evidence.

The ambiguity delta and its adjacent documentation errors are now durable logbook
entries:

| Defect | Review finding | State |
| --- | --- | --- |
| D-038 | F-10/F-16: scalar closed-form recognition was described as a convergence/local-optimum oracle | Documentation fixed; no regression yet |
| D-039 | F-20: D-021’s side floor was generalized into component resolution | Outstanding on `think-3szr` |
| D-040 | F-21: rarity lacked a durable, proposer-conditioned `P/Q/E` estimand | Outstanding on `think-apwt` |
| D-041 | F-13/F-18: contact counts and a one-angle kink were used as rank, rigidity, dimension, and connectivity proofs | Rank-free prose fixed; certification outstanding on `think-1s0h` |
| D-042, D-062 | F-14: the open `n=12` case was treated as a known-answer negative control, and the first correction missed the executable runner | Active docs and artifacts corrected; the not-below guard now uses proved `n=16`, with a mutation control for recurrence |

## Fourth reassessment: reset to the tight research loop

The first efficiency pass after the merge expanded D-035 into a hostile-isolation
design: repository snapshots, per-control worktrees, capability-style tokens, and a
general activity lease.
That was the wrong cost model for this project.
The workspace is cooperative, candidate mathematics can be checked after a run, and the
evidence policy reserves promotion for independent verification.
The useful operational objective is rapid detection, bounded loss, and cheap
recovery—not protection from an adversarial same-user process.
Worktrees and full repository copies would also add the disk and startup costs the
efficiency lane is supposed to remove.

All implementation from that detour was backed out of this branch and preserved only in
the local, nonportable stash named
`attic: overengineered D035 isolation prototype before autonomous-loop reset` for
possible pattern recovery.
Ten prototype beads were canceled as attic work rather than allowed to distort the
active plan. D-035 remains open with a narrow cooperative scope: preserve exact bytes
before an in-place mutation, bound each checker, stop its children on timeout or
interruption, restore before continuing, and make stale transaction state visible.
The existing gate marker, on-disk runner stubs and archives, subprocess timeboxes, and
generated reconciliation checks remain useful because they are small and directly tied
to observed failures.

The outer autonomous loop is correspondingly simple:

1. a persistent agent goal selects one focus and advances the ready `tbd` queue;
2. bounded work is delegated with a compact return contract—outcome, evidence, files,
   checks, uncertainty, next action, and elapsed wall time;
3. mathematical ideas and measurements continue to use the existing exploration,
   hypothesis, raw-result, and experiment artifacts;
4. implementation work updates beads and actual errors update the categorized defect
   log; and
5. one versioned agent-session artifact preserves the integration state and measured
   delegation loop.

The numerical runner remains a small executor for preregistered rounds, not a second
orchestrator. The README now names interactive, focused, checkpoint, deep-handoff, and
research-round latency envelopes from the measurements available so far.
The checkpoint timings are single-run observations; repeated warm/cold profiles and
per-stage attribution remain open work on `think-xzew`.

## What is sound and should be retained

- **The evidence tiers are the right backbone.** `f64_screen`, `polished`, and `exact`,
  with record claims reserved for the exact tier, is the correct policy.
  The repair is to enforce that policy at the artifact boundary.
- **Fixed angles plus a fixed separating cell is an LP.** The independent 1,056-row
  Trump reconstruction supports this.
  The error is the extra leap from “one cell is an LP” to “fixed angles define one LP
  objective.” The cell decomposition should become more explicit, not be discarded.
- **Proposer over one shared spine is the right architecture.** It makes equal-budget
  comparisons possible and prevents each strategy from redefining validity or basin
  identity.
- **The project records defects and negative results unusually well.** That practice
  should extend to invalid rows, non-convergence, algebraic-recognition failures, and
  disagreements between independent implementations.
- **`n = 5`, `10`, `16`, and `17` are a useful calibration ladder.** They test a
  non-trivial 45° mechanism, a larger proved 45° case, a proved grid that is a true
  not-below control, and an oblique-record mechanism.
  `n = 12` should remain a target.

## Technical findings

### F-01 (P0): the runner can record data that its own overlap guard rejects

[`read_lines`](../../../campaign/runner.py) writes each line to the archive at lines
315–322 *before* parsing or checking it.
`run` catches `GuardError` at lines 779–785 and then calls `record` unconditionally.
More seriously, `record` rebuilds cells through `cells_from`, lines 393–412, which reads
only `n`, `seed`, and `best_side`; it does not re-run any of the JSON, overlap,
membership, or completeness guards.

The counterexample is direct.
A five-seed H-017 archive with `overlap: 0.001` on every row is converted to a complete
`Cell`, and `decide` reports:

```
unresolved — Every cell came within 1e-04 ... Clauses 1-4 pass
```

`read_lines` refuses one of those rows, but only after placing it in the archive.
A user or recovery path invoking `record` on a changed archive bypasses the guard
entirely. This violates the runner’s main safety claim and makes unattended results
non-authoritative.

**Required repair:** create one validation function at the `record` trust boundary and
make every path use it.
Write to a temporary accepted archive and atomically rename only after the invocation
passes; retain rejected stdout in a separately named quarantine artifact with an invalid
verdict. `record` must refuse any non-`in-progress` round and must never derive
scientific result rows from guard-invalid data.

**Bead:** `think-ldq2`.

### F-02 (P0): validity is a proposer assertion, not an independent measurement

The command contract at [`campaign/runner.py:20–34`](../../../campaign/runner.py)
requires only a scalar `overlap` or `best_overlap`. No pose is required.
The harness then checks exact equality to the value zero *reported by the same code that
proposed the configuration*. It cannot recompute containment or separation.
The PR’s own quench driver illustrates the loss:
[`run_quench.py:78–120`](../../../run_quench.py) emits side, convergence, counts, and
timings but omits `x`, `y`, and `theta`.

The provenance fields repeat the same mistake.
The claim stub hardcodes `selftest_passed: true` at `runner.py:221–240`; the terminal
artifact hardcodes it again at lines 519–525. `preflight` never runs the declared
engine’s self-test. A command that prints a fabricated best side and `overlap: 0` passes
this boundary.

The project already states the correct rule: search energy is not validity.
It must now encode it.

**Required repair:** every result row must preserve a full pose or a content-addressed
pose reference. A separate `sqpack` process recomputes containment and pair separation
from that pose, records its own version and tolerance tier, and signs the accepted row’s
digest. `selftest_passed` must come from an executed test with binary hash and exit
status.
Exact zero is not required at the float screen; independently bounded non-overlap
is.

**Beads:** `think-ldq2`, `think-zcx4`, and `think-n4f6`.

### F-03 (P0): the generic evaluator cannot evaluate the hypotheses it is meant to queue

[`decide`](../../../campaign/runner.py) ignores `criterion.shape`, uses only a numeric
`criterion.threshold` at line 438, and reduces every outcome to
`best_side - standing_best` at lines 457–470. That implements H-016/H-017/H-020 only.
It does not implement:

- H-001’s `pair_tests_to_known_optimum`, whose threshold is a prose baseline and would
  fail `float(...)` if a runner recipe were added;
- H-011’s basin-discovery plateau;
- H-012’s record-to-modal probability ratio;
- H-018’s return fraction; or
- H-019’s ratio of one-sided derivatives.

The overnight spec plans to make H-011 runnable and then obtain an H-012 verdict from
the same system. As written, adding a recipe would silently evaluate the wrong metric or
crash on its threshold.
The schema’s determination outcome also has no typed plateau or coverage state.

**Required repair:** criterion shapes need registered evaluator implementations and
typed result schemas.
Preflight must instantiate every `instrument_ready: true` hypothesis, feed its evaluator
positive and negative fixtures, and refuse a hypothesis whose metric has no
implementation. A hypothesis does not enter the unattended queue merely because it has a
shell command.

**Beads:** `think-ldq2` and `think-rrht`.

### F-04 (P1): runner state, dependencies, deadlines, and git persistence are not a closed state machine

Several smaller defects combine at the overnight boundary:

- `queue` at `runner.py:181–216` never checks `prereqs`; `claim` checks only that a
  recipe exists. A dependent hypothesis can run before its evidence exists.
- `execute` and `record` do not require an `in-progress` verdict.
  A terminal round can be truncated, re-executed, and rewritten.
- `execute` creates one deadline for an entire multi-cell recipe at lines 343–359,
  although recipes and the spec describe per-cell timeboxes.
  It does not cap that deadline to the remaining session or lease.
- `run` computes the queue once.
  It neither re-screens after each verdict nor releases a failed claim.
  Only `GuardError` increments the “three failures” counter; process-level exceptions
  and persistence failures escape that policy.
- `git()` at lines 127–130 discards return codes.
  `record` stages all of `campaign/`, commits with `--no-verify`, ignores commit
  failure, and still returns a success decision at lines 589–615. The `dirty` flag is
  computed after the runner’s own files have been written, so it does not describe the
  engine’s starting tree.
- `release` regenerates the ledger but does not check regeneration or persist the
  release. The report can omit runnable-but-unrun work and does not implement the
  promised “what moved / what died” distinction.
- [`ledger.py:298–303`](../../../campaign/ledger.py) drops a parsed timezone with
  `.replace(tzinfo=None)` instead of converting it to UTC. A non-zero offset can make a
  fresh lease stale or an expired lease live.

**Required repair:** model claim, execution, validation, recording, persistence,
release, and terminal states explicitly.
Use checked git commands and narrow path staging; record pre-run engine dirtiness before
campaign writes; convert aware datetimes with `astimezone(UTC)`; recompute the queue
after every state transition; enforce prerequisites; and make persistence failure a
terminal error that cannot be reported as a scientific verdict.

**Bead:** `think-ldq2`.

### F-05 (P0): basin identity is neither fully invariant nor a stable equivalence relation

The geometric key does minimize over `D4`, and the shipped test checks that path.
The contact certificate does not.
At [`canonical.py:201–210`](../../../sqpack/canonical.py), angle classes are ranked by
their folded representative angle.
Reflection sends `a -> pi/2 - a`, which reverses those ranks; a contact graph whose
topology distinguishes the classes can therefore change certificate.
The shipped D4 test at [`canonical_check.py:100–122`](../../../tools/canonical_check.py)
compares only `.geometric`, so it misses this failure.

The angle classes used as node colours are themselves order-dependent.
The greedy representative algorithm at [`quench.py:349–368`](../../../sqpack/quench.py)
does not define a transitive equivalence relation near its tolerance.
A relabelling can therefore change both the contact certificate and angle signature.

Finally, the two-key policy is internally inconsistent.
The module says a matching contact certificate resolves a quantization split, and
`agrees_with` reports exactly that state.
[`Atlas.add`](../../../sqpack/atlas.py), however, deduplicates only when the exact tuple
`(geometric, contact)` matches.
The demonstrated 2e-12 perturbation is stored twice.
There is no disagreement ledger or later union operation.

**Required repair:** either canonicalize the attributed contact graph over every D4
image or use reflection-invariant angle relations.
Replace greedy tolerance grouping with a deterministic circular clustering rule whose
equivalence semantics are stated.
Represent uncertain equality explicitly—candidate equivalence edges plus deterministic
union, or a stable metric verification step—rather than pretending two hashes are an
equivalence proof. Test every D4 image and random permutation for **both** keys.

**Bead:** `think-siui`.

### F-06 (P1): the contact-graph canonicalizer has factorial worst-case behavior at the intended n

`_certificate` at `canonical.py:147–177` exhaustively individualizes ambiguous colour
classes without memoization, automorphism pruning, or a graph-canonicalization backend.
The docstring calls it cheap for `n <= 12`. The empty graph benchmark above grows from
0.098 seconds at `n = 7` to 7.91 seconds at `n = 9`. Sparse contact graphs and repeated
attributes are not pathological for early or non-converged packing endpoints; they are
exactly what the atlas will receive.

At census scale, this can dominate the quench, stall `n = 10`, and make a failure look
like landscape complexity.

**Required repair:** use a proven canonical-label implementation such as nauty/bliss or
an equivalent maintained backend, or implement automorphism-aware memoization with
special cases for empty and regular colour classes.
Publish adversarial timing floors through at least `n = 100`; the fast geometric key may
screen most cases, but the slow path must have a bounded operating envelope.

**Bead:** `think-siui`.

### F-07 (P0): the atlas counts stopping points as basins and cannot reconstruct its claimed discovery curve

The atlas class calls every row “one distinct local optimum,” but
[`Atlas.add:82–116`](../../../sqpack/atlas.py) stores the endpoint even when
`converged=False`. Its comments explicitly defend that choice.
The observed result at `n = 5`—11 sweep-limit stops, one convergence, 12 rows, and no
known optimum—is the consequence.
The result counts termination artifacts rather than basins.

At the updated PR head, D-030 repairs that particular cold-start failure: the revised
`n=5` fixture converges on all six proposals.
The contract still admits the same error.
The new golden’s `n=3` case has only three convergences in four proposals, stores the
fourth stopping point among its three reported basins, and passes a majority threshold.
A detector that permits up to half its sample to be the object it was introduced to
exclude does not make basin counts authoritative.

The append-only claim is also incomplete.
The file stores aggregate `proposals` and frequencies, not an event order or
`first_seen_proposal`. The transient Boolean returned by `add` is lost.
No saved atlas can reconstruct new-basins-versus-proposals, even though the overnight
plan makes that curve the kill criterion.

The updated checker demonstrated the same boundary problem in miniature.
It correctly snapshotted six census proposals for its convergence assertion, then
printed ten in its final summary after re-offering four basins to test deduplication.
D-037 records the historical line, but an actual atlas still lacks the immutable event
boundary needed to make this class of mix-up impossible.

Convergence itself is currently too weak for promotion (F-10), but the data model must
separate the states regardless.

**Required repair:** store immutable observations first.
An observation may be invalid, non-converged, coordinatewise-stationary, locally
certified, or exactly promoted.
A basin representative is a derived view over independently valid and sufficiently
certified observations.
Persist proposal order, first-seen order, failures, censoring, and promotion history so
the curve is regenerated—not remembered—from the event log.

**Beads:** `think-31k1` and `think-rrht`.

### F-08 (P1): atlas frequencies have no experimental regime or merge provenance

An atlas header contains `n`, quantization, contact tolerance, proposal count, and
aggregate rows. It omits proposer distribution and version, quench definition and
version, seed block, engine commit, budget, host or numeric backend, validity tier, run
ids, and shard identity.
Yet `merge` at `atlas.py:208–225` adds frequencies after checking only `n`. Incompatible
quantization regimes merge; self-merge doubles counts; the same shard can be merged
twice; `Atlas(5)` accepts a key whose own `n` is 1; and `load` trusts all counts and
identities without schema validation.

Frequency is meaningful only conditional on a proposal distribution and quench map.
Mixing regimes produces a number that is neither probability nor a reproducible count.

The saved `softschema.schema` is also the bare string `atlas.schema.yaml` at lines
138–145. Saving outside that directory produces metadata the CLI cannot resolve; the
checker manually points at the repository schema instead of validating through the
artifact’s declaration.

**Required repair:** give every observation a regime digest and shard id; enforce
schema, `n`, identity, count, and regime invariants on add/load/save/merge; make merge
an idempotent union of observation ids; and derive frequency tables by regime.
The saved schema reference must resolve from every supported output location.

**Bead:** `think-31k1`.

### F-09 (P0): “fixed angles define a function” remains false

The correct theorem in this repository is:

> Fixed angles **and one separating-axis cell** define a linear program.

[`solve_to_fixed_point`](../../../sqpack/quench.py) instead starts from the cell chosen
by the input centres, solves it, chooses another cell, and stops when a cell repeats or
when the next cell is worse or infeasible.
At lines 194–197 it returns the incumbent even though the re-read cell differs, so the
result need not be a fixed point.
Its docstring claims this removes path dependence; the same-theta counterexample proves
otherwise.

The D-015 regression at [`regression_test.py:80–105`](../../../tools/regression_test.py)
checks deterministic repetition and a pure translation of one start.
It never supplies distinct starting cells, so it cannot test the property it names.
The file is not wired into `test.sh` in any case.

This invalidates `s(theta)` as used by the one-dimensional golden search and by claims
that the quench has turned the landscape into one well-defined map.

**Required repair:** name the object honestly.
Either hold an explicit cell fixed; enumerate or globally optimize all cells reachable
at fixed angles; or define a trajectory-relative quench endpoint whose key includes the
transition rule and start regime.
Add same-theta, many-cell controls and retain all distinct endpoints.
Do not call the minimum over one path the fixed-angle objective.

**Bead:** `think-zcx4`.

### F-10 (P1): quench convergence does not certify a local optimum

The free-angle pass performs cyclic one-coordinate golden searches.
Stopping with no coordinate improvement proves, at best, stationarity under those
particular coordinate probes and finite brackets.
A coupled angle direction can still improve the packing.
The code nevertheless returns `converged=True`, and the atlas promotes that result to a
“local optimum.”

There are two further gaps:

- Golden section assumes a unimodal objective on its fixed interval.
  The multi-cell objective is nonsmooth and may have several minima; the code does not
  expand or verify a bracket.
- `_free_sweep` checks its deadline only before each coordinate.
  A single probe can run many LP/cell iterations and overrun the wall budget; the
  apparent out-of-time path cannot interrupt work inside the probe.

The updated head made this worse than an overrun: a deadline break returned the normal
five-field tuple, and the caller interpreted “no improvement in the partial pass” as
`converged=True`. D-036 on the stacked branch changes the helper to raise on timeout,
checks inside every probe, and returns a non-converged result.
That fixes the status bug, not the mathematical scope of the status.

The research reports also describe Powell and Nelder–Mead as smooth methods that cannot
converge to a corner.
Both are derivative-free and can optimize nonsmooth functions.
Their measured failures are evidence about these implementations and starts, not a
general impossibility result.

**Required repair:** use honest states such as `sweep_limit`,
`coordinatewise_stationary`, and `locally_certified`. Promote only after a nonsmooth
active-set/KKT or directional test, interval neighborhood check, or an explicitly scoped
empirical criterion.
Thread a cancellable deadline through every LP and objective evaluation.
Benchmark multiple brackets and coupled directions on proved controls.

**Beads:** `think-zcx4` and `think-rrht`.

### F-11 (P1): the generic exact-arithmetic API does not enforce its completeness preconditions

[`NumberField.__init__`](../../../sqpack/field.py) documents an irreducible minimal
polynomial and an interval containing exactly one real root.
The implementation checks only a sign change at the endpoints.
A reducible polynomial can pass, after which a non-zero reduced representative can
vanish at the selected root.
Equality is then wrong and sign refinement may not terminate.

The counterexample `P(x)=(x-1)(x-2)` on `(0,7/5)` selects the root 1, but the quotient
representation reports `alpha - 1 != 0`. The rational-root check in `_bisect` is too
late and does not establish irreducibility or root uniqueness.

This does **not** overturn the built-in Trump verification: `derive_field.py` separately
checks its polynomial and the exact negative controls pass.
It does mean the README’s “verifying another packing” API and the field module’s
completeness claim are unsound for untrusted certificate data.

**Required repair:** validate primitive/squarefree irreducibility and count exactly one
root in the interval with a Sturm sequence, or require proof-carrying field metadata
that an independent certificate checker verifies.
Negative controls must include reducible, repeated-root, zero-endpoint, and
multiple-root intervals, and every sign test must have a resource bound or proof of
termination.

**Beads:** `think-zcx4` and `think-n4f6`.

### F-12 (P1): the search record cannot support its budget and basin inferences

`run_chain` checks `moves < budget_moves` only between anneals, while `anneal` always
executes `p.steps` moves.
A run can exceed its declared move budget by nearly one full anneal.
The project’s preferred pair-test budget is not implemented, so “equal budget”
comparisons remain impossible.

The chain initializes its retained best to the trivial grid at
[`search.rs:197–224`](../../../sqsearch/src/search.rs) and stores only an improving
valid best. Therefore exp-011 returning exactly side 5 at `n = 17` means only that no
better valid candidate was retained.
It does **not** show that trajectories never left the grid basin, never visited oblique
configurations, or are structurally blind “at any n.” The event stream needed to
distinguish those statements was discarded.

Incremental overlap is recomputed for the final best, which correctly fixed D-009, but
its drift still affects which configurations are considered feasible and retained during
the run. An independent record-time verifier helps only if candidates near the threshold
are not discarded first.

**Required repair:** cap inner iterations to the remaining budget, implement an exact
pair-test counter, and archive trajectory or event summaries sufficient to recover
orientation classes, validity-screen transitions, basin candidates, and censored near
misses. Keep a separate candidate reservoir; do not infer a trajectory from the final
fallback best.

**Beads:** `think-rrht`, `think-ldq2`, and existing `think-b4jc`/`think-owm0`.

### F-13 (P0): three mathematical claims that shape the strategy are false or unproved

**The angle is not algebraic.**
[`research-2026-08-22-packing-11-unit-squares.md:200–207`](../research/research-2026-08-22-packing-11-unit-squares.md)
says algebraic `sec(a)` makes the angle itself algebraic of degree 8. In radians, a
non-zero algebraic `a` would make `exp(i a)` transcendental by Lindemann–Weierstrass;
algebraic `cos(a)` would make the same number a root of `z² - 2 cos(a) z + 1`, hence
algebraic. Therefore `a` is transcendental.
`cos(a)`, `sec(a)`, `tan(a/2)`, and `s` are algebraic; the angle is not.

**`m² - 3` is not a proved general grid family.**
[`search-strategies.yaml:11–17`](../../../frontier/search-strategies.yaml) and its
generated table say the grid is optimal for all `m²-3`. Nagamochi proves the general
families `m²`, `m²-1`, and `m²-2` in
[Packing Unit Squares in a Rectangle](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v12i1r37).
The repository’s own research correctly states that `m²-3` is known for `m=3…7`; Bentz’s
[2010 paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v17i1r126)
supplies `m=4,7`. The cases `m=8,9,10`, namely `n=61,78,97`, remain open in the corpus.

**Rigidity does not imply a rare attraction basin.** Rigidity is local isolation of a
feasible/contact structure.
A basin is the preimage of a specified algorithmic quench.
An isolated minimum may have a large, positive-measure basin, and a flexible family may
be difficult for a particular proposer to enter.
The search-philosophy report’s lines 92–100 briefly acknowledge this distinction, but
its heading and conclusions, the main research report at lines 1686–1691, H-012, H-018,
and the idea board turn the correlation into a consequence.
Exp-005 itself found return behavior out to perturbation `0.1`, contradicting “no
attracting neighbourhood.”

**Required repair:** correct the angle statement; qualify the grid table; and reframe
rarity as a proposer-, start-distribution-, and quench-specific empirical hypothesis.
Contact count, rigidity, algebraic degree, and measured entry probability may be tested
for association, with held-out `n`, but no causal implication should be presumed.

**Beads:** `think-zt29` and `think-3b3s`.

### F-14 (P1): the central hypotheses and controls are not yet statistically or logically executable

H-011 promises a “near-complete atlas” with “exact side lengths.”
A discovery curve that looks flat does not establish near-completeness when the support
is unknown, and the atlas stores polished floats, not exact reconstructions.
It also does not persist the curve.
The sweep is `n=5…10`.

H-012 says it is a query over H-011 but requires both `n=10` and `n=11`; H-011 produces
no `n=11` data. Frequencies from one finite sample need uncertainty and a definition of
the sampling measure.
Good–Turing coverage, Chao-style unseen-species estimates, or capture–recapture across
independent proposer/quench regimes are appropriate; “plateau by n=8” alone is not.

H-020’s artifact title says “cannot find an oblique record, at any n,” while its actual
claim is one method, one budget, five seeds, and `n=17`. Failure to reach the criterion
refutes that scoped positive claim.
It does not prove blindness at all `n` or at all budgets.
Canonicalizing 40 unquenched chain outputs into many float keys likewise does not
establish one funnel.

Finally, `n=12` is repeatedly encoded as a negative control even though `s(12)=4` is
open and merely believed.
A genuine sub-4 packing would be censored as a bug by `CONTROLS` and the schema.
The proved `n=16` grid is the correct not-below-4 control; `n=12` is an upper-bound and
lower-bound target.

**Required repair:** preregister estimators, confidence intervals, independent
replicates, and censoring; split exact reconstruction from float census; extend H-011 or
give H-012 its own `n=11` experiment; scope H-020’s conclusion; and replace `n=12` with
a proved grid control.

**Beads:** `think-rrht`, `think-zt29`, `think-iwlr`, and `think-3b3s`.

### F-15 (P1): the enforcement story and living documents have drifted from the code

The overnight plan says each Half-A component lands with a `test.sh` check and a watched
negative control.
The PR wires `canonical_check.py`, but not `atlas_check.py`; the latter
currently fails. `tools/regression_test.py` contains named regressions D-002/D-015/
D-016/D-019/D-029 and is also absent from the gate.
There is no pull-request CI.

The strict gate currently fails only on a README layout check because the new atlas is
not listed. That small failure matters: the handover spec requires strict exit zero, yet
the PR presents the handover as ready.

Other concrete drift found in the same pass:

- the overnight plan promises a check on “two genuinely distinct `n=5` optima,” but the
  canonical checker compares Trump’s `n=11` packing with an `n=16` grid and an archived
  wrong `n=11` basin;
- `SYNOPSIS.md` calls the `n=11` gap the smallest open gap at `n<=100`; it is fourth,
  after `n=97,78,61`;
- the handoff says ten rounds while exp-011 exists, and the synopsis still says the
  atlas is unbuilt;
- the strict gate invokes project tools through unfrozen `uv run` commands and rewrites
  the tracked lockfile under this environment;
- the overnight spec’s 16.4 “cpu-minutes” is a sum of artifact `wall_seconds`, not CPU
  time;
- the angle-kink prose reports positive “left” and right derivative magnitudes without
  preserving the actual derivative sign;
- the canonical/atlas docs claim cheap exact or ground-truth identity more strongly than
  their implementations support; and
- `frontier/n-017.md` calls the catalogue/paper decimal discrepancy unresolved even
  though the stored polynomial decisively supports the catalogue value.

The updated PR head wires the atlas and golden checks and prints step timings; the
stacked branch wires the historical regressions and freezes dependency resolution.
That resolves the missing-command portion of this finding.
It also makes the next failure visible: the source-built golden is red against its
committed `n=10` row, the full gate is reported at roughly 480 seconds, and GitHub still
reports no PR checks.
Wiring a red or impractically slow check is evidence, not completion.

**Required repair:** wire every named checker into the strict gate and CI only after it
passes adversarial controls; freeze dependency resolution during verification; make
doc/artifact reconciliation cover round counts, atlas existence, gap ordering, control
roles, derivative signs, and timing labels; and treat a red promised check as a handover
blocker.

**Bead:** `think-zt29`.

### F-16 (P0): the mathematical golden is not hermetic and asserts what it says it only records

[`tools/golden_basins.py`](../../../tools/golden_basins.py) combines two different
artifacts: an oracle-driven convergence ladder and an exact characterization snapshot of
a few multistart draws.
The prose says discovery is “measured, never asserted,” but the whole rebuilt
YAML—including which basins those draws found, their frequencies, and `found_optimum`—is
compared byte for byte.
A legitimate proposer or quench improvement therefore fails the gate in exactly the same
way as a mathematical regression.

The committed file did not reproduce from the checked-in engine.
After an explicit release build, fixed seed 7 at `n=10` annealed to gap
`+0.077126752369` and quenched to `(8 + 5√2)/4`, gap `+0.06066`; the committed row says
gap `+0.021003996488` followed by the proved optimum.
The standalone command did not build the engine, so an untracked stale binary could
supply its supposedly fixed inputs.
The current source is itself deterministic: two direct runs produced byte-identical
scientific rows, isolating the problem to the committed fixture/provenance rather than
scheduler randomness.

Four more details matter:

- the ladder records `converged` but did not add `converged=False` to its oracle
  failures, so `--update` could bless an incomplete result;
- `--update` wrote the replacement before inspecting its oracle failures, so a command
  that exited non-zero still left an invalid golden in the worktree;
- the census accepts 50% non-convergence and includes those endpoints in the exact map;
- the atlas keeps the lowest side for a repeated identity while `configs.setdefault`
  kept the first pose, so the independent verifier could check a different pose/side
  pair from the one reported; and
- 12 decimal places are finer than the declared `1e-11` numerical floor, while sub-floor
  gaps are serialized verbatim.
  Exact text comparison can therefore fail on differences the evidence tier says are
  meaningless.

Closed-form recognition is useful supporting evidence, but its coincidence heuristic
does not turn it into an oracle: optimizer outputs are not uniform random reals, and a
short quadratic surd neither proves local optimality nor excludes a censored point.

**Required repair:** build the source-locked engine before every standalone rebuild;
record the selected seed and full regime; use a preselected start known to lie in each
control basin; make validity and completed convergence non-waivable oracle conditions;
verify the pose that supplies the reported side; compare numeric fields at the tier
tolerance; and separate the deterministic characterization map from mathematical pass/
fail assertions. Refuse oracle-invalid updates before an atomic write.
Non-converged endpoints remain observations, never certified basins.

**Beads:** `think-zt29`, `think-zcx4`, and `think-31k1`.

### F-17 (P0): the fast gate removed the producer-level regression it claimed to preserve

At PR head `c412b8c`, [`test.sh`](../../../test.sh) makes `--deep` and `--strict`
independent flags. The handover specification invokes only `./test.sh --strict`, so its
golden step calls `verify_stored()` rather than annealing, quenching, rebuilding the
map, or independently checking a pose.
That function can derive mathematical constraints on stored scalars, but a YAML row
saying `valid: true` is not independent validation.
The file contains no pose with which the fast path could establish that claim.

At the same time, [`tools/atlas_check.py`](../../../tools/atlas_check.py) replaced its
real six-start `n=5` census with one cheap real `n=4` quench and five synthetic keys.
All six offers were passed with `converged=True`; the check then asserted that the
non-convergence counter was zero and described this as testing that the store did not
hide non-convergence.
A branch that deletes or ignores the false path can pass that fixture.
The text then points to the single-start ladder as census-scale coverage, although those
seeds are deliberately selected for membership in target basins.

The three changes together remove the executable recurrence test for D-030 from the raw
strict handover gate.
The faster default is reasonable for ordinary edits; the scientific handover cannot
substitute assertions about a committed file for executing its producer.

**Required repair:** strict must imply deep; deep/update must build the checked-in
engine; the cheap atlas check must offer at least one explicit non-converged observation
and assert its count; the real fixed-seed maps must remain the D-030 regression; and
comments must distinguish a selected convergence start from a census.
Add a negative control that mutates the strict/deep implication and observes the deep
marker disappear.

**Beads:** `think-zt29`, `think-zcx4`, and `think-31k1`.

### F-18 (P0): endpoint hashes do not define basins on non-isolated terminal sets

The PR description is right that the `n=3` optimum has slack, but the failure is already
constructive rather than merely possible.
For every `t` in `[1/2,3/2]`, the three axis-aligned squares with centres

```
(1/2, 1/2), (3/2, 1/2), (t, 3/2)
```

form a valid packing in a side-2 container.
The top square slides continuously while the optimum side remains fixed.
Running the current canonicalizer at `t = 0.50, 0.75, 1.00, 1.25, 1.50` produced one
contact certificate, `af4ca4659c8fc659a37907833f922899`, but three geometric keys; D4
identifies `t` with `2-t` and does not identify the remaining continuum.
Because [`Atlas.add`](../../../sqpack/atlas.py) merges only when both hashes agree, a
finer geometric quantum creates more rows from the same connected optimal family.

This is not repaired by choosing the contact key instead.
The family’s active contact graph is constant through its interior, but contact graphs
can also stay constant across genuinely different metric realizations and can change at
the boundary of one connected family.
Neither hash defines connectedness.
The module-level statement that a basin is “the preimage of one quench endpoint” assumes
the very discreteness that fails here.

The mathematical object has to be declared before it can be counted.
Let `P` be a proposal measure, `Q` a fully specified deterministic quench including
tie-breaking and termination, and `E` an equivalence on terminal states after
quotienting square relabelling, each square’s quarter-turn symmetry, and container D4.
An attraction probability is then the `P`-measure of the preimage under `Q` of one
`E`-class. For isolated minima, `E` may reduce to certified geometric equality.
For a non-isolated stationary set, it should identify a connected terminal component or
stratum, not each sampled point.

**Required repair:** compute the active-constraint Jacobian or rigidity matrix at every
candidate, report rank and nullity after removing the side and any modeled gauge
directions, and continue each certified null direction.
Use active-set continuation or a semialgebraic component method to join boundary strata
whose contact graphs change without leaving the terminal set.
Until that exists, label the output `endpoint clusters`; exclude non-isolated cases from
basin-count and saturation claims.
The exact `n=3` family above is the minimum regression: changing the geometric quantum
must not change the reported number of terminal components.

**Beads:** `think-0yo9`, under `think-siui`, and `think-31k1`.

### F-19 (P1): the unrecognised singleton question is not identifiable from the stored artifact

The PR offers two explanations for the unrecognised `n=5` singletons: legitimate
higher-degree optima or incomplete convergence.
Both are possible, but the dichotomy is incomplete.
An unrecognised row may also be:

- a coordinatewise stationary saddle or non-minimizing kink;
- one sampled point on a positive-dimensional terminal component;
- a quantization split or tolerance-induced duplicate of a recognised component;
- a valid isolated local minimum whose side lies outside the recognizer’s bounded
  quadratic-surd family; or
- a numerical artifact that changes active cell, pose, or side under tighter solving.

The checked-in golden stores a rounded side, contact count, angle-class sizes,
frequencies, and booleans.
The atlas stores hashes and the same coarse descriptors.
Neither artifact retains the pose, active constraints, termination reason, residuals, or
a content-addressed observation from which the alternatives can be tested.
Rediscovery is evidence about proposal mass, not a convergence certificate.
Conversely, [`closed_form.py`](../../../sqpack/closed_form.py) searches only a finite
family `(p + q sqrt(d))/r`; a match is a heuristic clue, and a miss says only that this
family did not match.

**Required repair:** preserve every pose and active set, then replay each singleton
through a preregistered precision and budget ladder.
Require independent validity, complete free sweeps, active-set stability, identity
stability, and a coupled directional or KKT residual before calling it stationary.
Detect nullity as in F-18. For isolated candidates, solve the active equations at high
precision, reconstruct the candidate field, and use interval Newton or a Krawczyk-style
test plus second-order or feasible-direction checks where available.
Emit one of `censored`, `unresolved duplicate`, `nonisolated stationary component`,
`isolated stationary candidate`, `certified local minimum`, or `exactly promoted`. Do
not promote “unrecognised singleton” itself to a scientific class.

**Beads:** `think-aans`, under `think-31k1`, plus `think-zcx4` and `think-n4f6`.

### F-20 (P0): D-021’s side-error floor is being used as a basin-resolution theorem

D-021 says the floating LP can perturb the reported **side** by roughly `1e-11`. It does
not say that two terminal configurations whose sides differ by more than that are
different, or that two configurations whose sides differ by less are the same.
The current system nevertheless makes that inference in three places:

- [`canonical.py`](../../../sqpack/canonical.py) says its `1e-6` pose quantum is far
  below every real basin distinction because real basins differ in side by `1e-3` or
  more;
- [`atlas.py`](../../../sqpack/atlas.py) calls the minimum scalar side gap the number
  that determines whether two rows are resolvable; and
- [`atlas.schema.yaml`](../../../atlas/atlas.schema.yaml) gives `closest_pair` the same
  interpretation.

The project’s own data refutes the premise.
The stacked `n=5` golden contains two distinct rows at the identical serialized side
`2.767766953`, while the `n=3` family in F-18 contains continuously many configurations
with side exactly `2`. Independently, the identity pipeline uses a `1e-6`
coordinate/angle quantum and a `1e-9` contact tolerance, neither derived from D-021. A
scalar objective gap therefore cannot calibrate a high-dimensional equivalence relation.

**Required repair:** keep the minimum side gap only as `closest_side_gap`, a descriptive
statistic with no identity authority.
Add quotient-space pose distance, active/contact-set comparison, repeat-run variation,
and interval enclosures for side and pose.
Sweep solver tolerances, quench budgets, contact tolerances, and geometric quantums;
look for a stable component partition rather than choosing one magic epsilon.
Represent unresolved pairwise equality as an ambiguity graph and publish lower and upper
component counts until interval separation or continuation resolves it.

**Bead:** `think-3szr`, under `think-siui`.

### F-21 (P0): “record-basin rarity” has no distribution-free estimand

A basin frequency is conditional on an entire measurement regime.
For proposal measure `P`, deterministic quench `Q`, and terminal equivalence `E`, the
frequency estimates the probability that `Q` maps a `P`-draw into one `E`-class.
Change the coordinate parameterization, initial container size, feasibility
conditioning, repair operator, annealing schedule, quench tie-break, or equivalence
relation and the probability changes.
There is no intrinsic “uniform over configurations” measure that makes these choices
disappear.

The current proposer samples centres uniformly from `[0.5, side-0.5]`, angles uniformly
from one quarter turn, and uses an initial side selected from the proved value plus
`0.6` or from `ceil(sqrt(n)) + 0.6`. It permits overlap and can place rotated squares
through the wall. That is a legitimate raw-coordinate baseline once versioned, but it is
not invariant to parameterization and is not the landscape’s unique null.
The atlas does not store its definition or digest, and H-012’s `regime` says only “same
multistart distribution and polish backend.”
Merging frequencies across a changed box or quench would silently change the estimand.

The PR description’s `n=5` sample cannot carry the stronger inference.
Its `1/12` record-to-`4/12` modal ratio is `0.25`, above H-012’s registered `0.1` accept
threshold; twelve draws give broad uncertainty; and H-012 is registered at `n=10,11`,
not `n=5`. More importantly, those twelve events are not preserved at the current head.

**Required repair:** retain raw uniform multistart as a named baseline arm, not “the
null.” Version the proposal density, initial-side rule, feasibility/repair rule,
random-number generator, `Q`, and `E` in every event and atlas shard.
At equal exact pair-test budgets, compare raw uniform, feasible-conditioned or repaired,
space-filling, record-neighbour, continuation/surgery, and annealer-endpoint measures.
Report per-regime frequencies, exact or weighted confidence intervals, censoring, and
effective sample size; use importance weights only when the proposal densities are
known. H-012 must be rewritten as a proposer-specific claim, and rigidity/contact
correlations must be a separate held-out model rather than inferred from the same
frequency ratio.

**Beads:** `think-apwt`, under `think-rrht`, plus `think-843f` and `think-3b3s`.

### F-22 (P1): living operator and hypothesis artifacts retained superseded campaign state

Two active entry points contradicted the corrected record.
`run_baseline.sh` still called open `n=12` a negative control and instructed an operator
to treat a side below 4 as a bug.
H-002 still said its quench instrument was unbuilt after exp-006 through exp-009 had
built and measured it.
Either error could make an arriving agent discard a discovery or repeat completed work.
The script now routes a valid sub-4 candidate to promotion, and H-002 preserves both the
refuted universal claim and the measured local success on the tested `n=5` and `n=10`
starts.

**Beads:** `think-xaa7` (D-066) and `think-lexp` (D-069).

### F-23 (P1): the campaign omitted a terminal round and mislabeled wall time as CPU time

The five retained exp-011 summaries total `397.474` seconds, but the terminal artifact
had no `effort.wall_seconds`. The generated total therefore covered ten of eleven
rounds. The ledger then called its sum of elapsed wall seconds CPU time, although no
processor time was measured.
Exp-011 now carries the raw-derived value, all eleven rounds total 23.0 wall-minutes,
terminal rounds require wall time, and living summaries use the measured unit.

**Beads:** `think-j9o9` (D-067) and `think-p418` (D-068).

### F-24 (P1): execution provenance was replaced by the later record revision

Exp-011 originally named runtime revision `60a50cc`; later cleanup changed its execution
fields to `6f94be6`, the revision that recorded the artifact.
Rebuilding the latter therefore would not reconstruct the code boundary that produced
the retained measurements.
The historical fields are restored, and `execute` now appends one elapsed-time,
execution-revision, and dirty-state receipt to the existing raw archive for `record` or
`release` to consume.
Producer stdout is forbidden from writing the runner’s reserved receipt key.
Git history continues to identify the later write-up commit.

**Bead:** `think-zknq` (D-070).

### F-25 (P1): unattended session reports overwrite their own history

`campaign/runner.py` writes every generated handoff to `campaign/session-report.md`, so
one unattended run replaces the previous report.
Before this checkpoint there was also no versioned outer-loop record connecting
delegations, evidence, elapsed time, integration status, and the exact next action.
A small soft-schema agent-session artifact now fills the outer-loop gap without turning
the numerical runner into a scheduler.
The runner report path itself remains open and must become append-only before unattended
scale-up.

**Bead:** `think-y37w` (D-071), still open.

### F-26 (P1): direct execute and release commands bypassed the cooperative gate marker

Status, claim, and record refused to overlap the mutation gate, but direct `execute` and
`release` calls omitted the same check despite the runner’s stated contract.
They could therefore consume a deliberately corrupted campaign input or rewrite a
recovery artifact during a negative control.
Both paths now use the existing marker refusal, and preflight exercises each against a
temporary active marker.
This is the needed cooperative repair; it does not require a lease, worktree, capability
token, or repository snapshot.

**Bead:** `think-ep8g` (D-072).

### F-27 (P2): agent sessions were omitted from the existing filename/id invariant

The new session artifacts were schema-validated and duplicate-checked, but
`ledger.naming()` still received only series, explorations, hypotheses, and experiments.
A schema-valid session could therefore claim an id different from its path while the
ledger stayed green.
Sessions now use the same filename/id and kebab-case check, with a mutation control that
changes `session-001` to `session-002`.

**Bead:** `think-tsck` (D-073).

### F-28 (P1): the provenance regression did not exercise artifact-field mapping

The first D-070 repair parsed a timing/provenance receipt in preflight, then described
that check as proof that `record` preserved execution provenance.
It never exercised the five assignments into the terminal artifact, so any one could
drift back to record-time state while the named regression stayed green.
Those fields now come from one mapping function; preflight compares the complete mapping
with the receipt fixture, and a mutation control changes `method_commit` away from that
receipt and requires the named assertion to fail.

**Bead:** `think-9ork` (D-074).

### F-29 (P1): PR #16’s portable-oracle conclusion exceeded its evidence

The response retained a report that seed 7 did not quench to the proved optimum in one
environment, then said every tested environment reached the proved optimum.
Its generic `ORACLE FAILURES` excerpt identifies a rendered-byte mismatch, not the
failed predicate. It also proposed dropping only `annealer_gap`, although the
byte-compared map contains other stochastic characterization fields.
The cross-environment mismatch is real evidence that source-build reproducibility is
insufficient; the portable mathematical surface, failed predicate, and cause remain
unresolved.

**Bead:** `think-v6n1` (D-075); continuing experiment `think-osyp` under D-059.

### F-30 (P1): six endpoint rows from six proposals did not identify the cause

PR #16 correctly observed six converged `n=5` terminators and six endpoint-key rows,
then concluded that identity was too fine rather than the landscape being rich.
The sample establishes only no observed saturation.
Terminal diversity, insufficient stationarity, quench sensitivity, identity instability,
and numerical splitting remain competing explanations for `think-1s0h`.

**Bead:** `think-dqhd` (D-076).

### F-31 (P1): the PR #16 handoff sent agents toward stale and rejected work

The handoff called `think-97pp` closed, recommended pushing a snapshot/worktree/lease
prototype that had been quarantined, and reported obsolete branch and defect state.
The integrated handoff now records D-035’s narrow cooperative interruption-recovery and
per-control-timeout scope.
`git status` before broad staging remains a temporary precaution after an interrupted
negative-control run.

**Bead:** `think-sk4a` (D-077).

### F-32 (P2): the corrected `n=5` rank explanation was still incomplete

The response correctly retracted the five-dimensional family claim, but said the
constraint subtraction would be valid if the contact gradients were independent.
Independence can establish equality-stratum rank; it does not establish a connected
feasible optimal family.
The objective level, unilateral constraints, feasible tangent cone, higher-order
obstruction, and continuation still matter.
The handoff also retained an implication from record rigidity to possible non-record
flexibility; the exact `n=3` witness supplies that fact, not the strategy premise.

**Bead:** `think-djru` (D-078, D-079).

### F-33 (P2): PR #16’s fixed-finding count contradicted its own table

The response said four of five cited findings were fixed while its table listed all five
as fixed. The correct accounting is four executable repairs plus one closed-form prose
repair. The original commits preserve the mistake; the status addendum and current
handoff reconcile it.

**Bead:** `think-hej7` (D-077).

### F-34 (P2): a priority sketch was presented as a dependency chain

The handoff serialized independent ready work behind terminal-flatness measurement.
Only `think-siui` and `think-jxx8` have the relevant blocker edge from `think-1s0h`;
portability, recovery, terminology, timing, and other infrastructure work can proceed in
parallel. The current handoff publishes lanes and explicitly defers to `tbd` for live
state.

**Bead:** `think-55m2` (D-077).

### F-35 (P1): the registered neighbor-transfer test was true before search began

The standing H-4 proposed `n=12` budget-to-side-`4+epsilon` as the outcome.
A cold grid already has side 4, so the control satisfies the target at initialization
and the test cannot measure transfer.
H-004 now makes a paired equal-budget comparison at `n=11`, using add-from-10 and
remove-from-12 seeds and a fixed median best-side improvement.

**Disposition:** fixed in the canonical registry artifact (D-080).

### F-36 (P0): a nonempty queue is not a priced unattended agenda

Preflight passes with one runnable recipe.
H-017’s declared eight-hour timebox projects to about 2.8 hours at the recorded local
throughput, and the runner has no second cell; the same green preflight therefore
precedes both an underfilled night and an almost idle day.
Queue state must be per unresolved cell and carry target-host p50/p95 cost, with a
reserve beyond the intended horizon.

**Bead:** `think-kmn2` (D-081).

### F-37 (P1): living summaries again exceeded two completed experiments

The synopsis repeated D-057’s generalization from one `n=17` method, budget and five-
seed block to oblique-record blindness as a class.
It also called Trump’s basin attracting through `epsilon=0.1` after H-018 observed zero
registered-threshold returns and a finite-quench residual.
The first result is scoped to its registered regime; the second diagnoses incomplete
convergence and establishes no component attraction.

**Disposition:** fixed with visible corrections in the synopsis and exp-005 (D-082,
D-083).

### F-38 (P1): the `n=11` frontier record promoted two unsupported facts

The structured artifact said `rigid: true` while its body admitted that no rank or
interval-local isolation certificate exists.
It also called the 0.0882 interval the smallest open gap although the corpus ranks it
fourth. Rigidity is now unknown, and the text distinguishes the smallest open instance
from the fourth-smallest numerical gap.

**Disposition:** fixed in `frontier/n-011.md` (D-084); H-022 carries the local-geometry
question.

### F-39 (P2): documented read-only commands could modify the lockfile

The campaign runbook and synopsis still used unfrozen `uv run`; invoking the documented
runner help path rewrote tracked `uv.lock`. Living commands now pass `--frozen`,
restoring the operator boundary D-058 said had been fixed.

**Disposition:** fixed (D-085, recurrence of D-058).

### F-40 (P1): the active overnight plan scheduled finished work and an inadmissible census

The plan retained the old ten-round, 16.4-wall-minute aggregate, scheduled landed
canonicalization and atlas blocks, and directed an H-011 launch before terminal identity
and independent runner validity.
The dated quench handoff made the same path current.
One rebuilt plan now separates autonomous agent work from numeric execution, records the
eleven-round/23.0-wall-minute baseline, and supplies exact scientific, lifecycle,
capacity and morning-artifact gates.

**Disposition:** fixed; overlapping overnight epics are superseded by `think-ydus`
(D-086).

### F-41 (P1): the angle-class registry combined different claims and an unmeasured sweep

H-001 used one assertion both for a corpus-wide few-angle law and for a proposer’s
performance. Neither implies the other.
H-019 named `n=5,10,11` as its sweep while its claim and measurement concern only
Trump’s `n=11` shared-tilt slice.
H-001 now owns the algorithm comparison, H-024 owns the corpus law, and H-019 declares
only its measured cell.

**Bead:** `think-w5rb` for H-024’s corpus evidence (D-087).

### Technical-finding to defect-logbook crosswalk

Every technical error in F-01 through F-41 now has a durable defect entry.
A finding can map to more than one entry when it combined independent failure modes;
prior entries are reused where the review reproduced an already known cause.

| Finding | Defect entries | Disposition |
| --- | --- | --- |
| F-01 | D-043 | Fixed with live-ingest and replay validation |
| F-02 | D-044 | Open: independent pose validity and executed self-test provenance |
| F-03 | D-045 | Open: typed criterion evaluators |
| F-04 | D-032, D-033, D-046 | Recovery subpaths fixed; full runner state machine open |
| F-05 | D-031, D-034, D-047, D-048 | Angle seam and reflection fixed; component/equivalence semantics open |
| F-06 | D-049 | Open: bounded canonical-label implementation |
| F-07 | D-030, D-037, D-050 | Cold convergence and checker summary fixed; promotion/event model open |
| F-08 | D-051 | Open: regime-safe, idempotent observation merge |
| F-09 | D-015, D-029 | Existing defects cover path-dependent fixed-angle semantics and the one-solve misdiagnosis |
| F-10 | D-036, D-052 | Timeout status fixed; local-certification scope open |
| F-11 | D-053 | Open: generic field-certificate preconditions |
| F-12 | D-002, D-009, D-054 | Earlier budget/overlap defects retained; exact work and event semantics open |
| F-13 | D-040, D-041, D-055, D-056, D-063 | False theorem and logic prose fixed; empirical rarity and rigidity certification open |
| F-14 | D-034, D-038–D-042, D-057, D-062 | Hypothesis/control errors separately recorded and scoped |
| F-15 | D-027, D-028, D-058, D-065 | Local handover and derived README claim reconciled; configured PR CI remains on the remediation bead |
| F-16 | D-038, D-050, D-059 | Hermetic safety fixes landed; oracle/characterization separation remains open |
| F-17 | D-060, D-064 | Fixed with strict-implies-deep, a firing mutation control, and a read-only preflight path that remains testable inside the gate |
| F-18 | D-034 | Open: terminal-component definition on the exact `n=3` control |
| F-19 | D-061 | Open: evidence-complete endpoint classification |
| F-20 | D-039 | Open: identity calibration independent of side precision |
| F-21 | D-040 | Open: durable proposer-conditioned `P/Q/E` estimand |
| F-22 | D-066, D-069 | Fixed: active operator and hypothesis artifacts match the measured campaign state |
| F-23 | D-067, D-068 | Fixed: all terminal rounds carry elapsed wall time and the generated unit is honest |
| F-24 | D-070 | Fixed: execution timing and revision survive the separate record step |
| F-25 | D-071 | Partially fixed: outer sessions are versioned; numerical runner reports still overwrite |
| F-26 | D-072 | Fixed: direct execute and release paths refuse the active gate marker |
| F-27 | D-073 | Fixed: session filenames and declared ids are reconciled |
| F-28 | D-074 | Fixed: receipt-to-artifact provenance mapping is directly mutation-tested |
| F-29 | D-059, D-075 | Response corrected; portable mathematical versus stochastic characterization surfaces remain open |
| F-30 | D-076 | Fixed: six-of-six is a no-saturation observation with competing explanations |
| F-31 | D-035, D-077 | Handoff fixed; narrow cooperative recovery remains open |
| F-32 | D-041, D-063, D-078, D-079 | Fixed: rank and logic corrections now state the actual conditions and witness |
| F-33 | D-077 | Fixed: five corrections are accounted for consistently |
| F-34 | D-077 | Fixed: current handoff uses parallel lanes and real blocker edges |
| F-35 | D-080 | Fixed: neighbor transfer now has a discriminating paired target |
| F-36 | D-081 | Open: unresolved-cell queue pricing and horizon readiness |
| F-37 | D-057, D-082, D-083 | Fixed: both results are scoped to their actual regimes and observables |
| F-38 | D-041, D-084 | Fixed structured facts; local rigidity certification remains open |
| F-39 | D-058, D-085 | Fixed: living uv commands preserve the lockfile |
| F-40 | D-071, D-086 | Plan fixed; append-only numerical morning reports remain open |
| F-41 | D-087 | Fixed: algorithm, corpus, and single-cell kink claims are separate |

## Key omissions

### O-01: there is no executable geometry corpus for the common values of n

The frontier’s 100 artifacts are valuable, but they are principally a scalar database:
best upper bound, lower bound, source, polynomial where known, a few tilt annotations,
and prose. They do not generally contain centres, angles, normalized SVG transforms,
contact topology, exact field elements, or independently checked certificates.
The README itself says tilt angles exist only for a handful of cases.

That omission blocks several advertised strategies at once:

- neighbor transfer has no machine-readable `n-1` or `n+1` pose to transfer;
- packing surgery and motif mining cannot operate on scalar bounds;
- the exact verifier cannot recheck the record corpus;
- the canonicalizer cannot be calibrated against known alternative packings;
- an improved public record page cannot be detected independently; and
- “common n” research cannot reproduce the pictures from which its claims were inferred.

The live
[Squares in Squares](https://kingbird.myphotos.cc/packing/squares_in_squares.html) page
provides SVG geometry and algebraic annotations for many entries.
Treating those as importable source data is a more useful foundation than another prose
strategy list.

**Required artifact:** one versioned `PackingPose` per obtainable record and meaningful
alternative, with `n`, side, normalized `x/y/theta`, source URL and retrieval date,
original content hash, import transform, independent float validity, canonical/contact
descriptors, claimed exact data, and verification tier.
Missing geometry remains an explicit row.
Start with `n=5,10,11,12,13,16,17,22,28,29,33,37,39,46,51,61,78,97`, then complete
`n<=100`.

**Bead:** `think-2o5w`, reconciled with `think-ezcx`, `think-0y0g`, and `think-kmwb`.

### O-02: no numerical candidate can be promoted automatically to an exact result

The exact verifier is a successful worked example for one hand-authored witness.
The README correctly says “the work is in the first line”: recovering the field is
manual. There is no command that accepts a high-quality float packing and performs:

1. high-precision independent validation;
2. stable active-contact and separating-axis extraction;
3. solution of the contact equations at increasing precision;
4. rational/algebraic recognition with PSLQ or minimal-polynomial recovery;
5. interval/Krawczyk proof that the numerical root is unique in a box;
6. exact reconstruction of every coordinate and side; and
7. emission and replay of a per-pair certificate.

Without that path, a successful search cannot become a publishable bound, and a failed
recognition disappears into human notebook work.
It also prevents the verifier from being tested on fields and topologies other than
Trump’s.

**Required artifact:** `sqpack promote candidate.json -> certificate.json`,
deterministic from pinned inputs, with separate `recognized`, `ambiguous`,
`nonisolated`, and `rejected` outcomes.
Reproduce rational/grid controls, `n=5`, `n=10`, Trump, and the degree-18 `n=17` side
before trusting a new candidate.

**Bead:** `think-n4f6`.

### O-03: the campaign lacks a scientific observation and uncertainty model

The current schemas are round-centric and winner-centric.
They do not preserve the event sequence required to answer the questions the project
asks: when a basin first appeared, what proposer weight produced it, which invalid
candidates were censored, whether the quench stopped or converged, what exact budget had
been consumed, and how often independent replicates captured the same unseen support.

This matters beyond bookkeeping.
A discovery curve without event order cannot be recomputed.
A basin frequency without a proposal distribution is not a probability.
A zero-hit record basin has an upper confidence bound, not probability zero.
A run that retains the grid has not proved that its trajectory stayed in the grid
funnel.

**Required artifact:** an append-only event schema covering proposal, screen, validity,
quench transition, endpoint, canonical ambiguity, promotion, and verdict.
It carries a content hash for the pose, exact pair-test and LP counters,
run/regime/proposer/quench digests, timestamps, censoring reason, and parent event.
Atlas tables, discovery curves, Good–Turing/Chao coverage, capture–recapture
comparisons, and confidence intervals are generated views.

**Bead:** `think-rrht`.

### O-04: independent oracles, source gaps, and proof controls are not closed

The project has a good independent LP reconstruction and a float-vs-exact negative
control, but the new identity and atlas layers are tested mainly against their own
implementations. There are no property-based or metamorphic suites for D4/permutation/
tolerance invariance, no second canonical-label backend, no differential atlas merge
implementation, and no generic certificate round trip.
The regression file that does exist is outside the gate.

The source archive is strong but its own availability record still names 11 missing
primary items.
The highest-value gaps remain Stromquist’s 1984 memoranda, El Moumni 1999,
Trump 2023, and Arslanov–Bui 2025. Those affect proof history, local-optimality claims,
and constructive families.
Their absence is correctly recorded, but the research program has no acquisition/retest
cadence tied to decisions that depend on them.

The lower-bound lane also lacks an end-to-end known-answer control.
The repository knows what that control should be: a falsifier must find a pose escaping
Stromquist’s ten-point set and must fail on the twelve-point set before interval proof
is trusted.

**Required artifact:** a property/differential suite and disagreement ledger; a dated
source-retest job with impact-ranked acquisition routes; and a proof-lane control suite
covering falsification, certified no-escape, and replay of at least one published
unavoidable set.

**Bead:** `think-thhk`, reconciled with `think-4o6l`, `think-leh0`, `think-ty3d`, and
`think-yrvm`.

## Creative executable strategies

The current program emphasizes uniform multistart, angle classes, continuation, neighbor
transfer, MAP-Elites, and billiard moves.
Those are worth keeping after the spine is repaired.
The following four programs attack different failure modes and can produce useful
artifacts even when they miss a record.

### A-01: active-set, separating-cell, and contact-graph search

This strategy makes the LP decomposition the search space instead of using it only as a
polisher.

**State.** A candidate consists of angle classes, a separating-axis assignment for every
non-contact pair, a contact/wall graph, and an LP basis.
Continuous centres and side are solved variables, not mutation coordinates.

**Operators.** Add or remove a contact; flip one pair’s separating axis; split or merge
an angle class; pivot to an adjacent LP basis; reflect or quotient a symmetry; insert or
delete a square for cross-`n` transfer.
Rigidity counts and graph automorphisms prune isomorphic states.

**Bounds.** For a fixed cell and angle box, solve LP relaxations with interval bounds on
trigonometric coefficients.
Use dual infeasibility or lower bounds to prune.
A SAT/SMT outer layer can encode the finite separating-axis disjunction, while interval
branch-and-bound handles the remaining angle boxes.
Every pruned node retains its dual or interval certificate.

**Calibration.** Enumerate the relevant cells at `n=5` and `10`; recover Trump’s cell
when seeded; measure topology count and pruning at `n=6…8`; then attack restricted
orientation/contact classes at `n=11` and `12`. Compare by exact node and pair-test
budgets, not only wall time.

**Accept rule.** Better exact side; a certified lower bound for a declared structural
class; or a tenfold reduction in certified search nodes against a fixed baseline.
A negative run still publishes topology counts, dual bounds, and the smallest unpruned
boxes.

**Bead:** `think-9vh7`.

### A-02: rare-event simulation rather than independent restarts

If a record basin is rare under a stated proposer, use methods designed to estimate and
enter rare sets.

**Arms.** Adaptive multilevel splitting or subset simulation on nested side thresholds;
cross-entropy adaptation of pose and move distributions; replica exchange/parallel
tempering; basin hopping; Wang–Landau or metadynamics over structural descriptors; and
plain independent restart as the control.

**Scores.** Side threshold is necessary but insufficient.
Preserve structural novelty using quantization-stable descriptors—angle-class spectrum,
contact topology, wall-contact pattern, LP basis, and oblique-core size—without
collapsing them into one hackable reward.
Rare event weights must survive selection so probability estimates remain meaningful.

**Calibration.** Require recovery of `n=5` and `10`, and non-violation of the proved
`n=16` control. Use `n=17` to test entry into an oblique-record class before `n=11` and
`12`. Run all arms through the same independent validator, quench, and event archive at
equal pair tests.

**Accept rule.** Predeclare time-to-certified-target and unique-certified-basin yield,
with confidence intervals.
For zero hits, report the binomial/weighted upper bound.
Retire an arm that cannot beat restart on controls at equal budget.

**Bead:** `think-843f`.

### A-03: continuation, branch switching, quality diversity, and packing surgery

The existing continuation ideas become much stronger when treated as a branch-discovery
system rather than a single homotopy.

**Parameters.** Continue in container inflation `delta`, aspect ratio, superdisk
exponent `p`, corner roundness, or a penalty that interpolates circles to squares.
Continue across `n` by inserting/deleting one square or duplicating a motif.
Track the active contact graph and LP basis at every step.

**Branch handling.** Detect contact changes, singular active sets, and basis degeneracy
as numerical branch events.
Launch branch-switching solves on each admissible new cell instead of following only the
locally smooth branch.
Archive valid continuation paths and their maximum required side as clearance upper
bounds. A branch merge or loss is not, without separate certification, a
feasible-component bifurcation or barrier.

**Diversity.** Store branches in a MAP-Elites or novelty archive keyed by versioned
structural descriptors.
Use an emitter portfolio—CMA-ES/DE for angles, cell pivots, billiard moves, neighbor
transfer, and explicit packing surgery.
Surgery operators come from the catalogue’s actual construction language:
add/remove/straighten an L, splice a strip, duplicate a subpacking, or replace a
boundary layer.

**LLM role.** Generate graph grammars, constructors, or checked code—not raw coordinates
or claims. Every proposal enters through the same typed proposer interface.

**Accept rule.** At equal pair tests, improve independently valid cell diversity,
declared branch coverage, or target-hitting time over restart; after terminal identity
exists, component diversity may be added as a separate metric.
A new active topology is an observation until its mathematical status is certified.
Hold out `n` values when evaluating learned surgery rules.

**Bead:** `think-g2ko`.

### A-04: proof-producing unavoidable-set synthesis

The lower-bound lane can be turned into a counterexample-guided optimization loop.

**Master problem.** Select a finite point set, weighted point measure, or fractional
transversal that makes every unit-square pose in a container expensive.
Optimize the number or total weight with LP/MIP and symmetry constraints.

**Separation oracle.** Given the current master solution, globally search the
three-parameter pose space `(x,y,theta)` for a unit square avoiding or underweighting
the points. A float optimizer proposes counterexamples; interval branch-and-bound
certifies whether a violating pose exists.
Each found pose becomes a new master constraint.

**Certificate.** When the oracle proves no violation, preserve the point set or weights,
the pose-space subdivision, interval bounds, and LP dual.
A small independent checker replays the certificate; a later Lean checker can verify the
same finite object.

**Calibration.** Find the known escape from Stromquist’s ten-point set, distinguish the
twelve-point set, and replay a published optimal case such as `n=10`, `13`, `22`, `33`,
or `46`. Then target `n=12` at side 4 and restricted `m²-3` boundary layers.

**Accept rule.** A new certified lower bound, a smaller published unavoidable set, or a
strictly stronger relaxation on a known case.
Counterexamples remain reusable poses and drive the next master iteration.

**Bead:** `think-6yni`.

## Tractable open questions

### Q-01: can n = 12 be moved from either side?

`n=12` is the best small target because both directions are meaningful.
The known grid gives `s(12)<=4`; the repository records a lower bound near 3.788854. A
construction below 4 is immediately a new upper bound.
A stronger unavoidable-set certificate is a new theorem even if the grid remains best.

Run the lanes in parallel:

- **Upper bound:** seed from Trump’s 11 plus a square, the 13-grid minus one, the best
  verified neighboring records, and continuation branches.
  Use the rare-event ensemble and packing-surgery archive; promote every side below 4
  exactly.
- **Lower bound:** synthesize weighted/unweighted unavoidable sets, use interval pose
  separation, and publish improvements even if they do not reach 4.
- **Restricted results:** certify that no packing below a chosen threshold exists within
  declared angle-class, boundary-contact, or cell families.
  Such results prune the upper-bound search and exercise the proof machinery.

A negative search result requires event-level coverage and uncertainty.
A proof result must state the exact restricted or global proposition.
`n=16`, not 12, is the not-below-4 control.

**Bead:** `think-iwlr`.

### Q-02: can the m² - 3 theorem be extended to n = 61, 78, or 97?

These are `8²-3`, `9²-3`, and `10²-3`, and they have the smallest open scalar gaps in
the `n<=100` corpus.
They offer asymmetric opportunities:

- **Construction:** any verified side below `8`, `9`, or `10` breaks the next grid case
  and is easy to recognize as progress.
- **Proof:** because only three cells are missing from a nearly full grid, a lower-bound
  proof may reduce to a boundary-layer or strip classification rather than a free
  `3n`-variable problem.
- **Computation:** use the proved `m=3…7` cases as a regression ladder for
  contact-graph, boundary-layer, and unavoidable-set generators before extrapolating.

The latest asymptotic work—Bui’s
[O(x^0.6) construction](https://arxiv.org/abs/2508.04603) and McClenagan’s
[independent O(x^(3/5)) construction](https://arxiv.org/abs/2602.01484)—does not settle
these finite cases, but its boundary trapezoids and surgery arguments may suggest finite
branch templates. A result that rules out one explicit strip/angle grammar is worthwhile
even without the full theorem.

**Bead:** `think-9m9x`.

### Q-03: what can be certified about Trump’s n = 11 packing short of global optimality?

Three propositions should be separated:

1. **Exact upper bound:** the published construction is valid.
   This repository already verifies it, but the witness should be regenerated through
   the general promotion pipeline.
2. **Local optimality/rigidity:** no sufficiently small perturbation within or across
   the adjacent active cells reduces the side.
   This is a tractable interval active-set or nonsmooth KKT certificate and would
   formalize Trump’s arrangement-specific claim.
3. **Global optimality:** every packing of 11 squares has at least that side.
   This remains far harder and must not be implied by the first two.

Useful intermediate theorems include: any packing below the optimal 45° bound must use
an oblique angle outside a stated neighborhood; any packing below a threshold must have
at least a stated number of boundary contacts or angle classes; or no packing in a
specified contact-graph family beats Trump.
Each theorem cuts a certified region from the global search.

**Bead:** `think-qv90`.

### Q-04: is there a small grammar of record packings, and what really predicts entry probability?

The catalogue repeatedly says “extends,” “removes,” “straightens,” “combines two
copies,” and “adds an L.” That suggests a finite constructor grammar across `n`. The
geometry corpus makes two separate questions testable:

- Can a small set of graph/surgery rules generate held-out record topologies or good
  seeds at neighboring `n`?
- Conditional on a named proposer, start distribution, and quench, do rigidity, contact
  count, algebraic degree, angle-class count, or wall-contact pattern predict
  basin-entry probability out of sample?

The second question must remain algorithm-specific.
Its payoff is practical even if no universal law exists: a calibrated predictor can
allocate emitters and budgets.
The first can produce constructive families or a negative classification of what local
surgeries cannot express.

**Bead:** `think-3b3s`.

### Additional results worth pursuing

| Question | Why it is tractable now | Useful stopping result |
| --- | --- | --- |
| Reconstruct and independently verify every obtainable upper bound at `n<=100` | The catalogue already exposes SVGs and many polynomials; the missing piece is the importer/promotion pipeline | A public verified corpus, plus corrected decimal/contact errors |
| Resolve the full small-n quench landscape at `n=5` and `6` | Cell/contact enumeration is still small enough for exhaustive or interval work | A quench-definition-specific complete list, or a certified count for restricted angles |
| Find the smallest n where the stock proposer enters an oblique record class | `n=17` is one failed cell, not a theorem; the geometry corpus supplies a mechanism ladder | A scoped success/failure curve by `n`, budget, and proposer |
| Certify local optimality for analytically optimized records beyond `n=11` | Their contact equations and polynomials are published; the general exact pipeline makes them repeatable | Interval active-set certificates and a catalogue of degeneracies |
| Detect whether the record corpus’s polynomial/decimal pairs are self-consistent | Polynomial evaluation and root isolation are cheap compared with search | A machine-generated discrepancy ledger; `n=17` is the first resolved example |
| Turn asymptotic boundary constructions into finite constructors | The 2025–2026 papers provide explicit geometric templates rather than only existence proofs | A finite-n improvement, or measured thresholds where the asymptotic construction loses to known records |
| Prove restricted-orientation lower bounds at `n=11` or `12` | Angle boxes plus separating-axis disjunctions fit interval/SAT methods sooner than the unrestricted problem | A certified exclusion of a broad angle family |

## Recommended executable program

The critical path is a trust and artifact path, not an overnight-compute path.

### Stage 0 — stop promotion, preserve evidence

Do not let PR #14 run an unattended census.
Keep its canonical/atlas code as a prototype, quarantine any guard-invalid output, and
require full poses on every new run.
Correct the factual claims and use `n=16` as the true grid control.

**Exit:** F-01 through F-05, F-09, F-16, and F-17 have failing regression fixtures
before their repairs, and no invalid or non-converged endpoint can appear as a basin.

### Stage 1 — build the reproducibility spine

Implement the geometry corpus, independent validator, event log, regime digest,
idempotent atlas derivation, pair-test meter, and float-to-exact promotion.
Add independent canonical labeling and certificate replay.

**Exit:** one command can import, validate, quench, canonicalize, promote, and replay
`n=5,10,11,16,17`, with every intermediate artifact content-addressed and every budget
exact.

### Stage 2 — calibrate the landscape machinery

Use `n=5,6,7,8,9,10` for small landscape work, but call it a statistical census unless
completeness is proved.
Use independent replicates, unseen-species estimators, and regime-specific frequencies.
Use `n=16` for false-record detection and `n=17` for an oblique mechanism.

**Exit:** discovery curves regenerate from events; coverage intervals and
non-convergence are visible; a held-out replicate reproduces the basin ranking within
declared uncertainty.

### Stage 3 — run a proposer portfolio, not one thesis

Compare restart, active-set/contact graph, rare-event methods, continuation/branch
switching, QD/surgery, and billiard emitters through one spine.
Use sequential elimination on controls so weak arms die cheaply.
Keep the best arm per mechanism rather than naming one universal winner.

**Exit:** each retained strategy has a runnable command, independent validation, exact
budget, event archive, predeclared accept/kill rule, and result on a mechanism-matched
control.

### Stage 4 — make the proof lane generate and replay certificates

Run the Stromquist falsifier controls, reproduce a published unavoidable-set result,
then launch the cutting-plane synthesis loop and restricted angle/cell branch-and-bound.

**Exit:** an independent small checker can replay both an exact upper-bound certificate
and a lower-bound/no-pose certificate without trusting the search code.

### Stage 5 — attack the targets in parallel

Allocate the upper-bound portfolio to `n=11`, `12`, and the `m²-3` cases; allocate the
proof portfolio to `n=12`, local/restricted `n=11`, and boundary-layer `m²-3`. Continue
corpus-wide reconstruction in the background because it supplies seeds and catches
source errors.

**Exit:** every null result states a scoped proposition or confidence bound; every
candidate is reproducible; every claimed bound has a replayable certificate.

### Instance portfolio

| n | Role |
| ---: | --- |
| 5, 10 | Proved non-trivial 45° controls; quench and promotion known answers |
| 16 | Proved side-4 grid; true not-below control |
| 6–9 | Small landscape and cell-enumeration calibration |
| 11 | Exact upper bound, local certification, restricted/global target |
| 12 | Open two-sided target; never a negative control |
| 13, 22, 33, 46 | Published optimal cases for lower-bound certificate replay |
| 17 | Oblique-record and degree-18 promotion control |
| 28, 29, 37, 39, 51 | Diverse record mechanisms and atlas/proposer calibration |
| 61, 78, 97 | Open `m²-3` frontier with the three smallest scalar gaps |

## The epic and its bead map

Epic **`think-6sst` — “Review remediation: executable square-packing research program
(PR #14)”** is a child of the standing square-packing epic `think-xkqu` and links to
this review as its spec.
Its direct children are the four focus epics below.
Their 31 direct work beads preserve the original technical-error, omission, creative-
alternative, and open-question labels while assigning exactly one primary owner.
The increase is the deep creativity review, its new exact-small-`n` and asymptotic
lanes, and the missing-primary correction.

| Focus epic | Primary authority | Direct work beads |
| --- | --- | ---: |
| `think-6awy` — Correctness (Soundness) | Mathematical truth and certification | 6 |
| `think-p76j` — Process (Discipline) | Reproducible research operations | 7 |
| `think-z3g5` — Insight (Creativity) | Mathematical strategy and discovery portfolio | 13 |
| `think-r1yl` — Efficiency (Infrastructure) | Trustworthy experimental throughput | 5 |

| Focus | Bead | Work item | Depends on in this review epic |
| --- | --- | --- | --- |
| Correctness | `think-siui` | Make canonical basin identity invariant, stable, and scalable | — |
| Correctness | `think-zcx4` | Correct fixed-angle quench and exact-verifier contracts | — |
| Correctness | `think-n4f6` | Implement float-candidate to exact-certificate promotion | `think-zcx4`, `think-2o5w` |
| Correctness | `think-thhk` | Close source, test-oracle, and independent-implementation gaps | — |
| Correctness | `think-zt29` | Correct false research claims and wire every enforcement gate | `think-ldq2`, `think-siui`, `think-31k1`, `think-zcx4` |
| Correctness | `think-vw06` | Archive and reconcile the direct 2018 piercing-number application | — |
| Process | `think-jmjn` | Publish the four-principle packing research charter | — |
| Process | `think-2w1a` | Maintain the review, defect logbook, and bead reconciliation map | — |
| Process | `think-m79h` | Define lane-specific agent handoffs and evidence contracts | `think-jmjn` |
| Process | `think-ldq2` | Repair the campaign trust boundary and run lifecycle | — |
| Process | `think-31k1` | Separate atlas observations from certified basins | `think-siui`, `think-zcx4` |
| Process | `think-2o5w` | Build a provenance-complete record-packing corpus through `n=100` | `think-zcx4` |
| Process | `think-rrht` | Add event-level measurement and a statistical census contract | `think-ldq2`, `think-siui`, `think-31k1`, `think-zcx4` |
| Insight | `think-vcnx` | Design basin-atlas views that expose mathematical structure | — |
| Insight | `think-9vh7` | Prototype active-set and contact-graph branch-and-bound search | `think-zcx4`, `think-2o5w`, `think-n4f6` |
| Insight | `think-843f` | Benchmark a rare-event proposer ensemble | `think-ldq2`, `think-31k1`, `think-rrht` |
| Insight | `think-g2ko` | Build continuation, quality-diversity, and packing-surgery emitters | `think-siui`, `think-31k1`, `think-2o5w`, `think-rrht` |
| Insight | `think-6yni` | Synthesize unavoidable-set lower bounds by cutting planes | `think-zcx4`, `think-n4f6`, `think-thhk` |
| Insight | `think-iwlr` | Attack `n=12` from certified upper- and lower-bound lanes | `think-n4f6`, `think-rrht`, `think-843f`, `think-6yni` |
| Insight | `think-9m9x` | Extend the `m²-3` frontier at `n=61,78,97` | `think-2o5w`, `think-9vh7`, `think-g2ko` |
| Insight | `think-qv90` | Certify and structurally constrain the `n=11` optimum | `think-2o5w`, `think-n4f6`, `think-9vh7` |
| Insight | `think-3b3s` | Determine cross-`n` packing grammar and proposer-specific basin laws | `think-2o5w`, `think-rrht`, `think-g2ko` |
| Insight | `think-7gu0` | Deep creativity and mathematical-frontier portfolio review | — |
| Insight | `think-w5rb` | Reconstruct and test the record angle-class corpus through `n=30` | — |
| Insight | `think-chbu` | Classify exact small-`n` optimal configuration spaces | — |
| Insight | `think-ykt7` | Advance the asymptotic waste and finite-transfer lane | — |
| Efficiency | `think-xzew` | Baseline and profile the end-to-end research loop | — |
| Efficiency | `think-rthe` | Profile and reduce negative-control latency; parallelize only if the measured simple design preserves serial results | `think-xzew` |
| Efficiency | `think-ba88` | Build a resumable sharded executor for packing campaigns | `think-xzew`, `think-ldq2` |
| Efficiency | `think-qk9w` | Cache reusable validation and build work with sound invalidation | `think-xzew` |
| Efficiency | `think-djvs` | Build a scalable interactive basin-atlas explorer | `think-vcnx`, `think-31k1`, `think-rrht`, `think-7z7y` |

Each bead contains evidence, scope, and an acceptance test.
Where an older bead already owns implementation—canonicalization, atlas, pair-test
meter, source acquisition, promotion, proposer work—the child explicitly requires
reconciliation rather than creating a second authoritative plan.

The prior agent’s open work remains in its original phase hierarchy and is assigned a
focus label rather than duplicated:

| Focus | Existing bead | Reconciliation |
| --- | --- | --- |
| Correctness | `think-1s0h` | Owns D-034 terminal flatness/rank/connectivity and blocks canonical identity |
| Correctness | `think-ouf0` | Owns proved engine anchors and prefix-valid budget checks |
| Process | `think-jxx8` | Defines a named proposal baseline, corrected from “the null” under D-040 |
| Process | `think-5zwm` | Owns the claim→ledger→release recovery rehearsal |
| Process | `think-o48b` | Closed after defect-id reconciliation and source-built golden regeneration |
| Efficiency | `think-97pp` | Owns D-035’s narrow cooperative interruption recovery and per-control timeout; worktrees and a general lease are explicitly out of scope |
| Efficiency | `think-l3ds` | Carries the earlier 480→152 second gate profile; `think-xzew` extends rather than repeats it |
| Efficiency | `think-7z7y` | Owns deferred atlas fields consumed by the visualization explorer |

The four questions added to the PR description are tracked as narrower children of the
relevant remediation beads, not as a second epic:

| PR-description ambiguity | Bead | Parent | Acceptance boundary |
| --- | --- | --- | --- |
| Non-isolated basin definition | `think-0yo9` | `think-siui` | Component count is invariant to quantum on the exact `n=3` sliding family |
| Unrecognised singleton classification | `think-aans` | `think-31k1` | Every endpoint receives an evidence-based promotion class from a retained pose |
| Numerical identity versus D-021 | `think-3szr` | `think-siui` | Counts carry calibrated ambiguity bounds; scalar side gap has no identity authority |
| Proposer-conditioned null | `think-apwt` | `think-rrht` | H-012 names `P`, `Q`, and `E`; multiple proposal measures are compared at equal budget |

Fourteen checkpoint defects are tracked separately from the 26 primary research-program
beads because they are concrete corrections, not new strategy lanes:

| Defect | Bead | State at this checkpoint |
| --- | --- | --- |
| D-066 | `think-xaa7` | Fixed: active `n=12` baseline instruction |
| D-067 | `think-j9o9` | Fixed: exp-011 wall time and terminal-round requirement |
| D-068 | `think-p418` | Fixed: wall/CPU measurement labels |
| D-069 | `think-lexp` | Fixed: H-002 reconciled with measured rounds |
| D-070 | `think-zknq` | Fixed: execution provenance across runner steps |
| D-071 | `think-y37w` | Open: numerical session-report archival |
| D-072 | `think-ep8g` | Fixed: direct runner commands honor the gate marker |
| D-073 | `think-tsck` | Fixed: session filename/id invariant |
| D-074 | `think-9ork` | Fixed: provenance regression covers artifact-field mapping |
| D-075 | `think-v6n1` | Fixed: cross-environment mismatch no longer proves a portable oracle |
| D-076 | `think-dqhd` | Fixed: `n=5` six-of-six is a no-saturation observation, not a causal result |
| D-077 | `think-sk4a`, `think-hej7`, `think-55m2` | Fixed: PR #16 handoff state, counts, and lanes reconciled |
| D-078, D-079 | `think-djru` | Fixed: rank conditions and rigidity logic completed |
| D-080 | `think-isa3` | Fixed: H-004 has a discriminating paired criterion |
| D-081 | `think-kmn2` | Open: price scientifically admissible unresolved cells for both launch horizons |
| D-082, D-083 | `think-1sxv` | Fixed: H-020 and H-018 summaries no longer exceed their measurements |
| D-084 | `think-1sxv` | Fixed structured `n=11` rigidity and gap-rank facts; H-022 remains open |
| D-085 | `think-1sxv` | Fixed: living uv commands are frozen |
| D-086 | `think-ydus` | Fixed: one current readiness agenda and superseded stale handoff |
| D-087 | `think-w5rb` | Claim split fixed; corpus evidence remains to be reconstructed |

Ten hostile-isolation prototype beads—`think-5zzb`, `think-xe5l`, `think-tg66`,
`think-1pyr`, `think-6wgw`, `think-06vo`, `think-v8ve`, `think-zh3m`, `think-om54`, and
`think-7gq9`—are canceled as attic work and are not part of this map.
`think-z4db` is also canceled: exact source inspection showed its alleged duplicate
README link was a tool-output false positive.

## Final creativity review: source and measurement corrections

The mathematical-frontier pass began by challenging the facts used to choose research
directions. It found 18 substantive defects before proposing new experiments.
They are recorded as D-088 through D-105 so the creative portfolio does not inherit a
false geometry, an irrelevant proof control, or an algorithm-conditioned landscape
claim.

| Finding | Defect | Disposition |
| --- | --- | --- |
| F-42 | D-088 | The 29 July 2026 UnitSquare release replaces the stored `n=68,69` upper bounds; the release validation is cited but not claimed as independently re-run here |
| F-43 | D-089 | `n=17` uses `0°`, `+39.8049589798°`, and `−36.6237863834°`, not symmetric `±40°` |
| F-44 | D-090 | The primary `n=29` SVG is a six-angle-class counterexample candidate to H-024; effective angular rank replaces the universal small-class prior |
| F-45 | D-091 | H-010 now reproduces Stromquist’s localization, forced-three-point cohabitation, and counting implications rather than a nonexistent standalone 12-point theorem |
| F-46 | D-092 | The structured asymptotic record no longer attributes an explicit `10^-100` constant to Roth and Vaughan |
| F-47 | D-093 | Contact canonicalization now preserves angle/wall/degree attributes through individualization, with a colored-`K3` regression |
| F-48 | D-094, D-095 | The idea board has the correct `n=11` gap rank and no longer schedules refuted H-018 as a fresh experiment |
| F-49 | D-096, D-097 | Algebraic degree is a warning rather than a proof-method ceiling, and the strategy catalogues are working maps rather than exhaustive histories |
| F-50 | D-098, D-104 | A finite stochastic return threshold and a local-refinement failure are no longer called an intrinsic basin radius or a proved wrong component |
| F-51 | D-099 | H-023 asks same-level terminal connectivity only for the equal-side pair; unequal-side rows get a minimax clearance question |
| F-52 | D-100 | H-013 now requires a fixed-side projection family, measures minimum required inflation, and separates observed branch events from certified connectivity |
| F-53 | D-101 | Exp-007/008 round wall times conflict with retained per-call durations and are quarantined from map pricing pending reconstruction |
| F-54 | D-102 | H-006 now uses dual hard poses to generate columns and primal support to propose piercing points |
| F-55 | D-103 | H-011 machine-readable prerequisites now include its declared H-021/H-023 identity gates |
| F-56 | D-105 | H-014 fixes unit area and requires explicit symmetry-breaking and branch-event rules |

The first normal-gate attempt then caught D-106: correcting the stale H-018 prose had
invalidated a mutation-control anchor.
The one-match guard stopped rather than silently dropping coverage; the anchor now
targets the corrected registry link and retains the same referential-integrity mutation.
The second attempt caught D-107 when the synopsis still carried old defect totals,
treated a prose-annotated H-024 status as an absent registry row, and scheduled
already-resolved work.
Its aggregates and next-work state now agree with the corrected sources.
A later stage of the same reconciliation defect caught the generated ledger stale after
source formatting; regeneration now follows formatting at this checkpoint.

### Second creativity delta: audit the attractive ideas before funding them

The independent
[mathematical-frontier review](review-2026-08-23-mathematical-frontier-strategy.md) then
re-read the first creativity draft as adversarially as the code.
Twelve additional defects were found before its proposals were promoted:

| Finding | Defect | Disposition |
| --- | --- | --- |
| F-57 | D-108 | Bašić–Slivková (2018) is now archived and restores the direct piercing-number precedent; its `n=61` bound is weaker than Nagamochi’s stored bound |
| F-58 | D-109 | The verifier’s 20 boundary count is corner coordinates, not wall equations; the false `14+20=34` isostatic argument is replaced by branchwise one-sided tangent cones |
| F-59 | D-110 | A fixed-cell LP dual is an equilibrium-load certificate against the container objective, not automatically a free-framework self-stress or angle certificate |
| F-60 | D-111 | A calibrated fixed-budget tail fit is a sensitivity analysis, never a proof about all future budgets or proposer support |
| F-61 | D-112 | H-028 maps one imported cell and class assignment; the global two-class landscape is a separate lower-envelope problem |
| F-62 | D-113 | A numerical branch merge is not feasible topology; verified paths give only upper bounds on minimax required-side clearance |
| F-63 | D-114 | Fractional piercing has asymmetric conclusions: `τ*>10` rules out ten points, while `τ*≤10` does not construct an integral set |
| F-64 | D-115 | Claims of “first,” “never,” and “unpublished” are scoped to a recorded retrieved corpus rather than asserted globally |
| F-65 | D-116 | The review now agrees with the 40-artifact registry and assigns algebraic metadata only to independently verified standing witnesses |
| F-66 | D-117 | The idea board no longer says H-018 answered an intrinsic basin-width question |
| F-67 | D-118 | H-017’s fixed-budget reachability and H-012’s `P/Q/E` attraction ratio are separate estimands; H-012 needs a new identified `n=11` sample |
| F-68 | D-119 | H-028 now tests for one refined local minimizer and a boundary margin; continuity makes uniqueness inside a fixed positive objective tolerance impossible |

The corrected portfolio registers H-025 through H-040. Its strongest independent fronts
are Trump’s nonsmooth local geometry, exact optimal configuration spaces at small `n`,
held-out construction surgery, pure-point piercing limits, robust restricted-angle
proofs, `s(12)`, the next `m²−3` case at `n=61`, exact record fields, and the asymptotic
waste exponent. The basin program now has a typed object hierarchy and visualization
ladder; a glyph gallery and exact `n=3` quotient precede any point-cloud atlas.

Three source checks materially changed the frontier.
The [UnitSquare machine-readable release](https://hmbelvedere.com/data/results.json)
gives strictly smaller construction-only bounds at `n=68` and `n=69`. The primary
Kingbird [`n=17` SVG](https://kingbird.myphotos.cc/packing/square-17.svg) corrects the
orientation data, while its
[`n=29` SVG](https://kingbird.myphotos.cc/packing/square-29.svg) declares five distinct
nonzero angle entities plus the axis-aligned class.
Exp-012 has now reconstructed the complete `n=29` pose, checked all 406 pairs at 160
decimal digits, replayed its defining equations, and found six disjoint orientation
classes. That refutes H-024’s universal upper bound of three while leaving H-001’s
algorithmic comparison and H-025’s quantitative compressibility question open.

The canonicalization witness was exact and local: before the repair,
`_certificate([0,0,0], K3)`, `_certificate([0,0,1], K3)`, and the fully distinguished
variant were equal. Individualization had replaced every original node color before the
leaf certificate was serialized.
Preserving the original color sequence in canonical node order fixes the collision
without weakening relabeling invariance.

The recurring conceptual correction is that a numerical pipeline defines an
**algorithm-conditioned observation**. A mathematical terminal component, feasible
clearance barrier, or local optimum needs additional path, active-system, tangent-cone,
or interval evidence.
This distinction drives the basin-map design in the companion creative-frontier review.

## Changes applied on the stacked review branch

The review branch fixes issues whose correct resolution does not depend on a research
choice:

- The branch is rebased onto merged `main` at `8926a7c`, including final PR #14 source
  head `f9f119a`. Conflicts across the README, timed gate, defect ledger, synopsis,
  handoff plan, atlas, golden, and negative-control catalogue were resolved
  semantically. Merged PR #14’s D-031 through D-035 remain intact; the review’s earlier
  fixes are D-036/D-037 and the final ambiguity delta is D-038 through D-042.
- `campaign/runner.py` now applies one result-line validator both before archival and
  during replay, rejects non-finite or malformed fields and undeclared cells or seeds,
  and releases a round instead of recording it after a guard refusal.
  Its preflight now watches invalid rows fail before reaching the archive and watches a
  tampered archive fail again at record time.
- `sqpack/canonical.py` now minimizes the attributed contact-graph certificate over all
  eight D4 images. The independent canonical check compares both the geometric and
  contact keys across all eight transforms and under a one-square quarter-turn.
- The README tree now includes both the top-level atlas schema and the `sqpack` atlas
  and canonical modules, removing the strict-gate drift.
- `tools/regression_test.py` now runs in the main gate instead of remaining a passing
  but optional command.
  D-036 adds deadline checks inside the free-angle pass and refuses to report a
  timed-out partial pass as convergence.
- The golden tool builds the source-locked Rust engine, records the selected ladder
  seed, uses a reproducible `n=10` control start, rejects non-converged ladder results,
  verifies the pose that supplied each stored minimum side, serializes no precision
  below the declared floor, and refuses oracle-invalid updates before an atomic write.
  Its fast path checks stored count/frequency consistency; strict mode implies deep
  regeneration rather than trusting the committed fixture.
- The golden map now records each basin’s converged frequency.
  The shortened atlas checker feeds an explicit false convergence status through the
  store and keeps its one real quench separate from synthetic offers.
  This also supersedes the mixed census/re-offer summary recorded as D-037.
- Every project `uv run` reached by `test.sh`, including negative-control commands, is
  frozen so a verification run no longer rewrites the dependency lock.
- The research report now distinguishes the transcendental angle from its algebraic
  trigonometric coordinates; the generated search-strategy table limits the `m²-3`
  theorem to `m=3…7`; the `n=17` note reports the polynomial evaluation that favours the
  catalogue decimal; and the synopsis and handoff carry the correct gap rank, round
  count, and hypothesis count.
- The final description-only delta now has four explicit dispositions, four executable
  ambiguity beads, and exact `n=3` evidence that the current endpoint hashes split a
  connected optimal family.
- Canonicalizer, atlas, schema, closed-form-recognition, census, and H-012 prose now
  distinguish endpoint clusters from terminal components, scalar side precision from
  identity resolution, recognition from convergence, and proposer-specific frequency
  from an intrinsic landscape probability.
- Living tier, rigidity, and campaign docs no longer call a floating-point LP endpoint
  exact, infer terminal dimension from raw contact counts, equate a one-angle kink with
  full rigidity, or use the open `n=12` instance as a known-answer negative control.
- The merged-head delta now has a line-by-line defect crosswalk through D-065. It
  corrects the executable `n=12` control in the runner, narrows angle-kink and
  oblique-record claims to what their experiments measured, removes a false
  contrapositive from the rigidity premise, and keeps the README’s qualitative defect
  summary reconciled to the defect source.
- The README and bead hierarchy now publish the four independent operating focuses:
  Correctness, Process, Insight, and Efficiency.
  Basin visualization is split between Insight’s view design and Efficiency’s
  reproducible implementation, with explicit Process and Correctness handoffs.
- The outer-loop contract is now explicit and deliberately small: a persistent goal and
  `tbd` select work; the existing campaign artifacts retain mathematical ideas and
  measurements; one versioned soft-schema agent-session artifact records delegation,
  elapsed time, integration evidence, stopping conditions, and the next action.
  The abandoned worktree/snapshot/lease prototype is not in this branch.
- Exp-011’s raw-derived `397.474` wall seconds and runtime revision `60a50cc` are
  restored; the eleven-round ledger now reports 23.0 wall-minutes.
  Future runner executions append one timing/provenance receipt to their existing raw
  archive, and terminal rounds without wall time fail the ledger.
  H-002 and the active `n=12` baseline instructions now agree with the measured record.
- Direct execute and release commands now honor the existing cooperative gate marker,
  and agent-session paths use the same filename/id invariant as the scientific
  artifacts. These repairs have named preflight and mutation checks and remain within the
  existing architecture.
- The execution receipt now feeds all five execution-owned artifact fields through one
  mapping that preflight and a mutation control exercise directly; receipt parsing alone
  is no longer misreported as end-to-end provenance coverage.

Before the second upstream advance, the source-locked golden passed its atomic update
path and a subsequent read-only rebuild.
Two full `./test.sh --strict` runs passed all exact, schema, generated-artifact, lint,
type, Rust, canonical, golden, atlas, negative-control, regression, soundness-perimeter,
bead, provenance, and campaign checks; the last took 298 seconds.
After the `c412b8c` rebase and second conflict resolution, the final strict/deep run
passed the same perimeter plus 21 negative controls and the 35-entry defect ledger in
291 seconds. The upstream D-030 repair changes the deep `n=5` fixture from one
convergence in twelve to six in six; strict mode now runs it.
`campaign/runner.py preflight` and the focused canonical and regression checks also
pass.

After PR #14 merged and this branch was rebased onto `8926a7c`, the first post-merge
checkpoint passed the full normal gate in 162 seconds: exact verification, the
independent LP reconstruction, source build and lint, canonical and atlas checks, all 21
negative controls, historical regressions, the soundness perimeter, all 42 defect
entries and generated views, bead-tree consistency, synopsis/README reconciliation,
search self-tests, differential validity, provenance, and campaign-ledger validation.
The two negative-control anchors initially drifted after the documentation corrections;
the gate failed by name, their stable anchors were repaired, and both were observed to
fire before the successful run.

The pushed `a7e7adc` process-lane checkpoint passed the full normal gate in 108 seconds
with 24 negative controls, 65 defect entries, and all generated-view, schema, lint,
type, canonical, atlas, soundness-perimeter, bead-tree, README/synopsis, provenance,
search, and campaign checks enabled.
An earlier integration run caught D-064 when runner preflight could not reach its
assertion from inside the gate.
The repaired read-only path then fired under mutation.
A post-gate read caught the D-065 README aggregate recurrence; its new reconciliation
check was also observed failing under mutation before this successful run.

The stabilized checkpoint then passed the full normal gate in 125 seconds with all 29
mutation controls firing and all 73 defect entries reconciled.
The exact verifier, independent fixed-cell LP, canonical and atlas checks, historical
regressions, soundness perimeter, schemas, generated views, bead tree, provenance,
search self-tests, differential validity, and campaign record all passed.
The three largest measured stages were the soundness perimeter at 37 seconds, negative
controls at 28 seconds, and historical regressions at 22 seconds.
The first attempt stopped at the lint floor on two Ruff-format diffs; the delegated
mechanical fix took about 1.5 seconds, and the complete rerun passed.
A final pre-commit review then found D-074: the D-070 regression parsed the receipt but
did not exercise its terminal artifact mapping.
After centralizing and mutation-testing that mapping, the final normal gate passed in
126 seconds with all 30 controls firing and all 74 defects reconciled.
Its largest stages were the soundness perimeter at 34 seconds, negative controls at 31
seconds, and historical regressions at 22 seconds.

PR #16 was then reviewed and absorbed through a merge parent so its five-commit
self-correction history remains visible.
F-29 through F-34 and D-075 through D-079 correct its unsupported portable-oracle and
`n=5` interpretations, incomplete rank and logic explanations, stale bead state, finding
count, and invented dependency chain.
A fresh deep golden run passed locally in about 91 seconds but does not rebut the
retained other-environment mismatch; `think-osyp` now requires per-predicate output and
complete environment provenance.
The final normal gate passed in 114 seconds with all 30 mutation controls firing, all 79
defects reconciled, and both agent sessions indexed.
Its largest stages were the soundness perimeter at 33 seconds, negative controls at 27
seconds, and historical regressions at 20 seconds.

After PR #15 merged, the unattended-readiness checkpoint rebuilt the active agenda,
codified the full 24-artifact portfolio, and recorded F-35 through F-41 as D-080 through
D-087. The normal gate passed in 132 seconds with all 30 mutation controls firing, all
87 defects reconciled, and three agent sessions indexed.
Its largest stages were the soundness perimeter at 40 seconds, negative controls at 31
seconds, and historical regressions at 23 seconds.
This is repository-checkpoint evidence, not authorization for an unattended numeric run;
the new plan’s scientific and lifecycle gate remains open.

## PR #17 Comment Disposition: 2026-08-24

Every comment surface on PR #17 was checked directly: four top-level comments, no formal
review submissions, no inline review threads, no linked issues, and no configured GitHub
checks. The four comments have the following durable disposition.

| Comment | Disposition | Durable record |
| --- | --- | --- |
| [First mathematical-frontier review](https://github.com/jlevy/thinking-scratchpad/pull/17#issuecomment-5389861146) | Superseded by its own later correction; all retained findings fixed or explicitly deferred | F-42 through F-56, D-088 through D-107, `think-f82b`, commit `5d772c6` |
| [Engineering and loop-efficiency review](https://github.com/jlevy/thinking-scratchpad/pull/17#issuecomment-5390037297) | Stacked PR #18 rebased and corrected before absorption; larger research-engine work remains open | D-120 through D-132, `think-9a7v` and children, engineering-review status addendum |
| [Deep mathematical delta checkpoint](https://github.com/jlevy/thinking-scratchpad/pull/17#issuecomment-5390373103) | Five false claims retracted; every retained finding logged and dispositioned | F-57 through F-68, D-108 through D-119, `think-vw06`, `think-0vt5`, `think-uyf4`, commit `7d019ab` |
| [Bead-count correction](https://github.com/jlevy/thinking-scratchpad/pull/17#issuecomment-5390382115) | Accepted; the creativity epic and all seven listed review children are closed | `think-7gu0` and its child beads |

The engineering absorption fixes the specific review-contract defects: selected checks
avoid unrelated Rust builds; partial runs expose skips; worker counts reject invalid
values; `--jobs 1` is serial at both layers; the documented worker limit matches the
implemented per-step cap; private negative-control snapshots are bounded and measured;
parallel snapshot assignment uses an explicit queue; the branch stack is current; and
the Python lint floor now means zero errors **and** zero warnings.
The defect-link mutation control itself failed once during integration when its anchor
became nonunique; D-130 records that gate-caught failure and the unique replacement.

The review did **not** justify closing every engineering research bead.
D-050/D-059 keep basin-count and golden semantics open; D-126 keeps scientific work
budgeting open; D-129 keeps per-control timeout and child reaping open; D-132 keeps the
fixed-cell termination contract open; the batch quench, cross-host CI, and target-CPU
policy remain named work under `think-9a7v`. This is the line between addressing every
review comment and pretending every broader recommendation has already been implemented.

A post-merge sweep of PR #18’s linked review document found one omitted, unnumbered
smaller finding: `solve_to_fixed_point` does not distinguish a settled cell from its
iteration cap or a rejected transition.
D-132 now records that deferred defect under `think-9qz0`. The sweep narrowed the
review’s exact-float-equality concern because fixed `theta` regenerates the same numeric
axis fields for the same discrete cell; no separate float-mismatch failure was
reproduced. The post-merge strict/deep gate then passed all 25 steps and 30 negative
controls with 132 defects reconciled in 55 wall seconds.

The corrected, rebased stack passed the 25-step normal gate in 26 wall seconds and the
strict/deep gate in 48 wall seconds.
Each run fired all 30 negative controls, reconciled all 131 defects, and enforced a
zero-error, zero-warning Python lint floor.
GitHub had no configured check runs on either PR, so these are retained local validation
results rather than a CI claim.

No primary mathematical or research-strategy remediation bead is closed by these
checkpoint repairs. The focused D-066 through D-070 and D-072 through D-074 incident
beads plus D-075 through D-079 are fixed; D-071 remains open for append-only numerical
runner reports.
In particular, the runner still trusts a producer-reported scalar overlap
rather than a stored pose checked independently; contact canonicalization still has
order-dependent angle clustering and factorial worst-case search; and the atlas,
fixed-angle semantics, criterion evaluators, exact-promotion path, event record, and
statistical contract remain open.

## Post-merge operating disposition

PR #14 has merged and is now the stable prototype base.
Treat its unattended census as blocked until this operational gate is satisfied:

1. F-01/F-02 fixed with an adversarial archive and fake-overlap control;
2. both canonical keys invariant under D4 and relabelling, with bounded runtime;
3. non-converged observations excluded from basin counts;
4. isolated endpoints distinguished from connected terminal components, with the exact
   `n=3` sliding family passing a quantum-invariance regression;
5. event order and full proposer/quench/equivalence regime provenance persisted;
6. unrecognised endpoints classified from retained poses rather than side strings;
7. numerical identity calibrated independently of D-021’s scalar side floor;
8. H-011/H-012 evaluators implemented with uncertainty, or the overnight claims removed;
9. fixed-angle semantics corrected;
10. `n=12` removed as a negative control;
11. atlas, golden, and regression checks hermetic, wired, and green under strict CI; and
12. the README, synopsis, handoff, and plan regenerated or corrected.

Until then, supervised exploratory runs are acceptable only if their raw stdout and full
poses are retained and their results are labelled untrusted screen data.

## False positives and limits of this review

- The built-in Trump exact witness passed; F-11 is about the generic field/certificate
  boundary, not a claim that Trump’s verified packing overlaps.
- The geometric key’s D4 minimization works on the tested fixtures.
  The counterexample is specifically the contact certificate and the combined identity
  policy.
- The LP formulation for a **fixed cell** is sound and independently reproduced.
  The counterexample concerns cell selection at fixed angles.
- The current live catalogue agrees with the repository on the examined common-n record
  values. The `n=17` polynomial supports the repository’s chosen decimal.
- The earlier primary-source search missed the UnitSquare Project’s 29 July 2026
  construction release.
  F-42 corrects the two affected `n<=100` cases and records the four additional cases
  beyond the current corpus.
  This remains a dated search result, not proof that no private or uncatalogued result
  exists.
- This review did not edit archived source transcriptions or claim new global packing
  theorems. Its mathematical corrections are standard deductions or direct checks of
  stored polynomials and code contracts.

## Primary references checked

- Erich Friedman,
  [Packing Unit Squares in Squares: A Survey and New Results](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS7).
- Walter Stromquist,
  [Packing 10 or 11 Unit Squares in a Square](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8).
- Hiroshi Nagamochi,
  [Packing Unit Squares in a Rectangle](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v12i1r37).
- Wolfram Bentz,
  [Optimal Packings of 13 and 46 Unit Squares in a Square](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v17i1r126).
- Bojan Bašić and Anna Slivková,
  [On optimal piercing of a square](https://doi.org/10.1016/j.dam.2018.03.048).
- M. Z. Arslanov and S. A. Mustafin,
  [Improved Packings of n(n-1) Unit Squares in a Square](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v28i4p22).
- David Ellsworth,
  [Squares in Squares](https://kingbird.myphotos.cc/packing/squares_in_squares.html),
  checked 2026-08-23.
- UnitSquare Project, [Six improved upper bounds](https://hmbelvedere.com/) and its
  [machine-readable release](https://hmbelvedere.com/data/results.json), published
  2026-07-29 and checked 2026-08-24.
- Hong Duc Bui,
  [Square Packing with Asymptotically Smallest Waste Only Needs Good Squares](https://arxiv.org/abs/2504.09489)
  and [Square Packing with O(x^0.6) Wasted Area](https://arxiv.org/abs/2508.04603).
- Rory McClenagan,
  [Optimally Packing a Large Square by Unit Squares](https://arxiv.org/abs/2602.01484).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
