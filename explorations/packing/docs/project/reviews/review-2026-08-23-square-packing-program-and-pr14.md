# Review: PR #14 and the Executable Square-Packing Research Program

**Date:** 2026-08-23

**Author:** Codex (agent)

**Status:** Complete

**Reviewed:** [PR #14](https://github.com/jlevy/thinking-scratchpad/pull/14),
`fa538931b20fef0f51dffedb9e4d7071603b7790`, together with the full
`explorations/packing/` research, tooling, campaign, corpus, and source archive.

The findings and reproduction results below describe that exact PR head.
The later section
[Changes applied on the stacked review branch](#changes-applied-on-the-stacked-review-branch)
records narrow repairs made after the review; it does not retroactively change the
reviewed evidence.

## Verdict

**Request changes. Do not run the proposed unattended census yet.**

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
[`think-6sst`](#the-epic-and-its-bead-map), with **17 direct children**: five technical
repairs and four each for omissions, creative alternatives, and tractable open
questions. Existing beads are referenced rather than silently duplicated.

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

The append-only claim is also incomplete.
The file stores aggregate `proposals` and frequencies, not an event order or
`first_seen_proposal`. The transient Boolean returned by `add` is lost.
No saved atlas can reconstruct new-basins-versus-proposals, even though the overnight
plan makes that curve the kill criterion.

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

**Required repair:** wire every named checker into the strict gate and CI only after it
passes adversarial controls; freeze dependency resolution during verification; make
doc/artifact reconciliation cover round counts, atlas existence, gap ordering, control
roles, derivative signs, and timing labels; and treat a red promised check as a handover
blocker.

**Bead:** `think-zt29`.

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
as bifurcations. Launch branch-switching solves on each admissible new topology instead
of following only the locally smooth branch.
Archive merge `delta` and barrier estimates.

**Diversity.** Store branches in a MAP-Elites or novelty archive keyed by versioned
structural descriptors.
Use an emitter portfolio—CMA-ES/DE for angles, cell pivots, billiard moves, neighbor
transfer, and explicit packing surgery.
Surgery operators come from the catalogue’s actual construction language:
add/remove/straighten an L, splice a strip, duplicate a subpacking, or replace a
boundary layer.

**LLM role.** Generate graph grammars, constructors, or checked code—not raw coordinates
or claims. Every proposal enters through the same typed proposer interface.

**Accept rule.** At equal pair tests, improve certified basin diversity, branch
coverage, or target-hitting time over restart; or discover a reproducible topology
absent from the record corpus.
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

**Exit:** F-01 through F-05 and F-09 have failing regression fixtures before their
repairs, and no invalid or non-converged endpoint can appear as a basin.

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
All 17 items below are direct children, so category coverage is visible in the issue
tree.

| Category | Bead | Work item | Depends on in this review epic |
| --- | --- | --- | --- |
| Technical error | `think-ldq2` | Repair the campaign trust boundary and run lifecycle | — |
| Technical error | `think-siui` | Make canonical basin identity invariant, stable, and scalable | — |
| Technical error | `think-31k1` | Separate atlas observations from certified basins | `think-siui`, `think-zcx4` |
| Technical error | `think-zcx4` | Correct fixed-angle quench and exact-verifier contracts | — |
| Technical error | `think-zt29` | Correct false research claims and wire every enforcement gate | the four technical beads above |
| Omission | `think-2o5w` | Build a provenance-complete record-packing corpus through `n=100` | `think-zcx4` |
| Omission | `think-n4f6` | Implement float-candidate to exact-certificate promotion | `think-zcx4`, `think-2o5w` |
| Omission | `think-rrht` | Add event-level measurement and a statistical census contract | the four foundational technical beads |
| Omission | `think-thhk` | Close source, test-oracle, and independent-implementation gaps | — |
| Creative alternative | `think-9vh7` | Prototype active-set and contact-graph branch-and-bound search | `think-zcx4`, `think-2o5w`, `think-n4f6` |
| Creative alternative | `think-843f` | Benchmark a rare-event proposer ensemble | `think-ldq2`, `think-31k1`, `think-rrht` |
| Creative alternative | `think-g2ko` | Build continuation, quality-diversity, and packing-surgery emitters | `think-siui`, `think-31k1`, `think-2o5w`, `think-rrht` |
| Creative alternative | `think-6yni` | Synthesize unavoidable-set lower bounds by cutting planes | `think-zcx4`, `think-n4f6`, `think-thhk` |
| Open question | `think-iwlr` | Attack `n=12` from certified upper- and lower-bound lanes | `think-n4f6`, `think-rrht`, `think-843f`, `think-6yni` |
| Open question | `think-9m9x` | Extend the `m²-3` frontier at `n=61,78,97` | `think-2o5w`, `think-9vh7`, `think-g2ko` |
| Open question | `think-qv90` | Certify and structurally constrain the `n=11` optimum | `think-2o5w`, `think-n4f6`, `think-9vh7` |
| Open question | `think-3b3s` | Determine cross-`n` packing grammar and proposer-specific basin laws | `think-2o5w`, `think-rrht`, `think-g2ko` |

Each bead contains evidence, scope, and an acceptance test.
Where an older bead already owns implementation—canonicalization, atlas, pair-test
meter, source acquisition, promotion, proposer work—the child explicitly requires
reconciliation rather than creating a second authoritative plan.

## Changes applied on the stacked review branch

The review branch fixes issues whose correct resolution does not depend on a research
choice:

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
- Every project `uv run` reached by `test.sh`, including negative-control commands, is
  frozen so a verification run no longer rewrites the dependency lock.
- The research report now distinguishes the transcendental angle from its algebraic
  trigonometric coordinates; the generated search-strategy table limits the `m²-3`
  theorem to `m=3…7`; the `n=17` note reports the polynomial evaluation that favours the
  catalogue decimal; and the synopsis and handoff carry the correct gap rank, round
  count, and hypothesis count.

After those changes, `./test.sh --strict`—including `tools/regression_test.py`—plus
`campaign/runner.py preflight`, the canonical checker, and the table drift check pass.
The separately invoked `tools/atlas_check.py` still fails because only 1 of 12 quenches
converges; it is still not wired into the main gate.

No remediation bead is closed by these partial fixes.
In particular, the runner still trusts a producer-reported scalar overlap rather than a
stored pose checked independently; contact canonicalization still has order-dependent
angle clustering and factorial worst-case search; and the atlas, fixed-angle semantics,
criterion evaluators, exact-promotion path, event record, and statistical contract
remain open.

## Recommended disposition of PR #14

Keep the PR open as a prototype branch, but do not merge it as an unattended-run
capability. The minimum merge gate is:

1. F-01/F-02 fixed with an adversarial archive and fake-overlap control;
2. both canonical keys invariant under D4 and relabelling, with bounded runtime;
3. non-converged observations excluded from basin counts;
4. event order and regime provenance persisted;
5. H-011/H-012 evaluators implemented or the overnight claims removed;
6. fixed-angle semantics corrected;
7. `n=12` removed as a negative control;
8. atlas and regression checks wired and green under strict CI; and
9. the README, synopsis, handoff, and plan regenerated or corrected.

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
- The latest primary-source search found active asymptotic work in 2025–2026, but no
  newer finite-`n<=100` proof or record paper that obviously supersedes the corpus.
  That is a dated search result, not proof that no private or uncatalogued result
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
- M. Z. Arslanov and S. A. Mustafin,
  [Improved Packings of n(n-1) Unit Squares in a Square](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v28i4p22).
- David Ellsworth,
  [Squares in Squares](https://kingbird.myphotos.cc/packing/squares_in_squares.html),
  checked 2026-08-23.
- Hong Duc Bui,
  [Square Packing with Asymptotically Smallest Waste Only Needs Good Squares](https://arxiv.org/abs/2504.09489)
  and [Square Packing with O(x^0.6) Wasted Area](https://arxiv.org/abs/2508.04603).
- Rory McClenagan,
  [Optimally Packing a Large Square by Unit Squares](https://arxiv.org/abs/2602.01484).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
