# Adversarial review of PR 78: the `s(11) ≥ 381/100` claim

**Review date:** 2026-09-04\
**Pull request:** [#78](https://github.com/jlevy/squares/pull/78)\
**Original reviewed parent head:** `719c2a170a1ac8bbd4cddfd353645b6d70651c45`\
**Latest reconciled parent head:** `a159eb28fad4be00c2c522b572ac2aab4d564c33`\
**Base:** `9d5eae0f5ecfcf3cd417a345eb6c55b1f9ac4def` (`main`)\
**Remediation branch:** `codex/pr78-s11-adversarial-review`\
**Certificate SHA-256:**
`b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a`

## Verdict

**The concrete mathematical claim is accepted: the retained positive-weight certificate
proves `s(11) ≥ 381/100`. The reviewed parent should not merge without the soundness and
assurance repairs carried by this stacked branch.**

Those are different decisions:

| Question | Verdict | Reason |
| --- | --- | --- |
| Does this particular certificate prove `s(11) ≥ 381/100`? | **Accept** | Its 1,121 weights are strictly positive; every proof obligation holds; and source-distinct exact continuum checks obtain the declared minimum `4001/4000 > 1`. |
| Is the corrected reusable theorem and project verifier sound? | **Accept on this stack** | The parent omitted nonnegative weights and accepted an exact certificate for the false bound `s(1) ≥ 11/10`. This branch makes nonnegativity a shared precondition and retains that object as a must-refuse regression. |
| Does a method-distinct computation confirm **Condition 5**? | **Accept on this stack** | The interval branch-and-bound certifies all 361 directions with no stalled or budget-exhausted box and encloses the minimum exactly at `4001/4000`. Samples, unsafe integer magnitudes, and below-one enclosures cannot produce acceptance. |
| Is the historical claim established? | **Apparently novel, high confidence** | The search found no public lower bound after Stromquist 2003 that reaches `381/100`, but it cannot establish absolute priority over unindexed or unpublished work. |
| Are the upstream commit’s frozen-byte claims reliable? | **No; repaired here** | The retained file hashes to `b121…e6a`, not the `503c…7cd6` named in the introducing commit. Both full decisions were rerun against `b121…e6a`; the old attestation is discarded. |
| Is the reviewed parent ready to merge unchanged? | **Request changes** | Its generic and interval verifier boundaries, retained declarations, retention gate, falsification gate, provenance language, and validation classification all needed repairs. This stacked branch supplies them and records the result at epistemic `C5` after validation. |

The most important distinction is between the parent implementation and the concrete
instance. The generic implementation was unsound; the specific instance was sound.
Adding the missing premise does not change the retained certificate: all 1,121 of its
weights were already strictly positive.

## Scope and adversarial method

This review concentrates on T-018, not PR 78’s separate `n = 12` result.
It checked the mathematical implication, the exact bytes retained for `n = 11`, the
continuum-to-finite reduction, replay and validation boundaries, method provenance, and
the novelty claim. The PR advanced repeatedly during the audit, from `9b85236b` through
`bdf63b21`, `6fc71ce9`, `31775018`, `b77e78d2`, `9134ee41`, `430e7e09`, `6196480d`,
`44e9c4b4`, `10cf6479`, `fbe01c49`, `d1e873a0`, `4a0c213a`, `9d90aabe`, `d3d9c7cb`, and
`719c2a17`, ending at `719c2a17`. Commit `6fc71ce9` replaced the `19/5` target artifact
with a larger `381/100` certificate, so the concrete validation restarted on the new
bytes. The later commits strengthened the separate `n = 12` and `n = 17` results,
supplied the missing full-net `n = 17` interval control, added a finite-certificate
reach theorem and generated reach table, amended the project process document, and added
a general certificate-retention command; they did not change the reviewed `n = 11` bytes
or its core argument.
The reach theorem was in scope because its first prose interpretation overstated a
finite-certificate ceiling as a method-wide impossibility; F14 records the correction.
The self-contained verification package, interval-certified branch-and-bound checkpoint,
retained `n = 17` certificates, and late retention command were included before the
verdict was frozen. The final reconciliation also audited the moving parent’s new `4.59`
and `99/25` certificates and `4.68` run narrative for branch consistency; those claims
did not alter the T-018 proof, but F25-F33 record defects that would otherwise have
shipped beside it. F34 and F35 record the literature-source drift found while folding
this review back into the canonical resource and frontier tiers.
The other `n = 17`--`19` frontier movement was outside this review’s mathematical scope
except where the earlier published-value `n = 17` certificate served as a control.
The final reconciliation through `353998ac` additionally audited T-020, the integer and
parallel exact-sweep optimization, its timing claims, and its generated planning
records. Those changes do not alter the T-018 certificate or theorem.
They do alter the code path that replays T-018, so F36--F42 record the defects found and
repaired before accepting the optimized path as an equivalent implementation.
The last parent update through `a159eb28` closes Agenda 017, records session-085, and
updates the frontier-corpus tripwire.
It does not change the T-018 bytes or proof; this stack corrects the proof-condition
notation reintroduced by that retrospective record.

The audit was pre-registered under `think-tukn` with five falsifiable hypotheses.
Two proof-validation lanes were kept separate from the coordinator’s main review:

- a proof/minimal-checker lane challenged the short implication and current certificate,
  then ran the standalone exact verifier; and
- a formalization lane assessed the Lean boundary and independently reran the complete
  interval decision.

The coordinator separately searched the literature, replayed the project verifier,
reconciled the retained artifacts, and constructed negative controls.
Later blind-priority and parent-integration lanes independently challenged the
literature scope and the final `n = 12` reconciliation without using the review’s
conclusions. Runtime agreement alone was not an acceptance rule: the proof implication
and every implicit premise had to survive as well.

## Findings

### F1: Blocker in the parent, fixed here: signed weights make the theorem false

At the reviewed parent, the proof in
[`certificate.py`](../../../packing/src/sqpack/fractional/certificate.py) says that no
atom is counted twice and concludes that the mass in the disjoint inner squares is at
most the total atom mass.
That step also needs every weight to be nonnegative.
Neither [`Atom`](../../../packing/src/sqpack/fractional/model.py) nor the parent
`Certificate.__post_init__` checked it, and `verify()` had no corresponding condition.

This is a false theorem as encoded, not merely a missing explanation.
The following five-atom certificate satisfies the stated **Conditions 1–5**:

| Datum | Value |
| --- | --- |
| `n`, `L`, `B` | `1`, `11/10`, `3/5` |
| half-angle tangents | `(0, 1/2)` |
| atoms | weight `+2` at `(11/20, 11/20)`; weight `-1` at each corner of `[0, 11/10]²` |
| total mass | `-2 < 1` |
| **Condition 3** slack | `1/4` |
| **Condition 4** product | `(3/5)(1 + 1/2) = 9/10 < 1` |

**Condition 1** holds by symmetry.
At angle zero, every admissible `3/5`-square contains the centre atom and at most one
corner, so its mass is at least one.
At the other net angle, `cos θ = 3/5` and `sin θ = 4/5`; every admissible square
contains the centre atom and no corner, so its mass is two.
Thus mathematical **Condition 5** holds as well.
But `s(1) = 1 < 11/10`, contradicting the claimed conclusion.

The parent project verifier accepted this object:

```text
accepted: True
failures: ()
total: -2
minimum: 2
```

It reports two rather than the true boundary minimum one because the event sweep checks
open two-dimensional cells.
Omitting boundaries is safe for nonnegative weights: membership in a closed square can
only add nonnegative mass on a boundary.
It is not safe for signed weights, where adding a boundary atom can lower the mass.

The parent’s new
[`thirdparty/README.md`](../../../packing/cases/n11_fractional_certificate/thirdparty/README.md)
correctly adds `w_i ≥ 0`, and its verifier rejects negative weights at
[`verify.py`](../../../packing/cases/n11_fractional_certificate/thirdparty/verify.py).
That local premise did not protect callers of `sqpack.fractional.Certificate`, including
the primary replay path.

**Resolution:** this stacked branch makes nonnegative weight an explicit theorem premise
and checked core precondition, applies the guard to direct sweep calls, documents that
the boundary reduction depends on monotonicity, and retains the exact five-atom false
certificate as a must-refuse regression.
D-441 records the defect.

### F2: High in the parent, fixed here: the validation surface was not clean

At `34d19470`, `.venv/bin/basedpyright` reports **26 errors**:

- 13 in the retained `n = 12` independent verifier;
- 12 in the newly added `n = 11` standalone verifier and falsifier; and
- one optional-value error in `tests/test_fractional_certificate.py:159`.

The latest configuration change excludes the standalone package from Ruff only.
[`pyproject.toml`](../../../packing/pyproject.toml) still includes all of `cases` in
BasedPyright. The PR description’s statement that BasedPyright is clean, and its earlier
claim that the hosted failure is only the inherited D-422 snapshot limit, are therefore
stale for the reviewed head.
The previous hosted validation also timed out after thirty minutes in the fast
behavioural suite; the exact certificate tests are long-running and currently
participate in that surface.

This does not weaken the exact arithmetic, but it does defeat the repository’s merge
contract and makes a red result easy to misclassify as unrelated infrastructure noise.

**Resolution:** this branch excludes the source-distinct retained programs from
BasedPyright under the same explicit evidence-preservation rationale already used for
Ruff, fixes the project-owned optional-value error, and moves every measured full
certificate decision into the existing `exhaustive_exact` tier.
Fast sub-net and must-refuse controls remain in the ordinary gate.
D-438 records the classification failure; the final gate results appear below.

### F3: Medium in the parent, fixed here: “third-party check” overstated independence

The new package is titled “Third-Party Check,” and the evidence register says it permits
checking without trusting the repository.
Its own provenance section correctly says that the claiming project wrote it on the day
the result was found and that nobody outside the project has reviewed the result.
Running a self-contained copy under an empty environment demonstrates portability and
absence of hidden repository imports; it does not create author or reviewer
independence.

The `n = 17` control is also a project reconstruction in a new JSON schema from
Massaccesi’s publicly posted constants, not an artifact shipped by Massaccesi.
It is a useful known-answer and scaling-semantics test, but not external validation of
the `n = 11` certificate.

The method attribution should preserve the historical layers.
Göbel’s 1979 unavoidable points are the integral precursor.
Nagamochi’s 2005 weighted-resource argument already assigns nonnegative resources to
points, segments, and area and compares the amount every unit square consumes with the
total available; Bentz’s 2016 account supplies the “resource starvation” label.
Burns’s August 2026 post and proof note supply the recent pure-atomic, rational
direction-net implementation; Massaccesi’s August 2026 work supplies the LP-generated
`n = 17` instance and parameters.
The apparently novel contribution here is the `n = 11` atomic instance, not the general
weighted-cover principle.

**Resolution:** the package is now described as self-contained and intended for
third-party checking, not as third-party work.
The README and evidence entry distinguish portability from independent authorship,
describe the control as a reconstruction, and record the Göbel–Nagamochi–Bentz resource
lineage before the Burns/ChatGPT and Massaccesi implementation line.

### F4: Medium in the parent, fixed here: retained declarations did not govern acceptance

The primary `n = 11` replay checks the declared `total_mass`, but not the declared
`least_cell_mass`, at
[`__main__.py:34-37`](../../../packing/cases/n11_fractional_certificate/__main__.py).
The `n = 11` test checks only that the computed minimum is at least one and that the
claim string matches; it does not require the exact declared minimum.
The neighbouring `n = 12` test does make that exact comparison
([`test_fractional_certificate.py:161-164`](../../../packing/tests/test_fractional_certificate.py)).

The standalone verifier improves visibility by recomputing both fields, but a mismatch
is printed as `NOTE` and the process can still end in `VERIFIED`
([`verify.py:465-481`](../../../packing/cases/n11_fractional_certificate/thirdparty/verify.py)).
The full independent `n = 11` replay is also manual rather than a retained automated
gate. The values happen to agree in every review run; the problem is that future drift
would not necessarily be refused by the paths that claim to bind the record.

**Resolution:** the primary replay now refuses claim, total, or least-mass drift; the
standalone verifier treats every present declaration as verdict-bearing; exact mutation
tests cover both paths; and the complete source-distinct `n = 11` decision is a named
`exhaustive_exact` test.
D-444 records the defect.

### F5: Low in the parent, fixed here: one scope disclaimer was false by monotonicity

The standalone README said the result was “not a bound for any other `n`.” Since `s(n)`
is nondecreasing, `s(11) ≥ 381/100` also implies `s(n) ≥ 381/100` for every `n ≥ 11`.
The intended and defensible statement is that it improves no currently recorded
higher-`n` bound.

The standalone README and T-018’s composition record now say exactly that.

### F6: Blocker in the interval checkpoint, fixed here: a direction sample could accept

The later `interval.py` checkpoint added a valuable method-distinct decision: directed-
rounding interval arithmetic and branch and bound over centre boxes, on a doubled net
that does not rely on D4 symmetry.
Its public `directions=` argument was documented as a control-only restriction, but the
implementation marked **Condition 5** as holding whenever every selected direction
certified. The resulting `IntervalVerdict.accepted` was true even if 358 of 361
directions had not been searched, and the tests explicitly required this outcome.

This is a direct sampled-to-universal soundness failure.
It did not affect T-018 because the checkpoint was not yet cited by any evidence entry,
but a future caller could have promoted a diagnostic to a false theorem verdict.

**Resolution:** a restricted run still reports per-direction certificates, enclosures,
and decisive refutations, but an all-certified sample is `undecided`; only the complete
doubled net can establish **Condition 5**. The tests require both sides of this
contract. D-445 records the defect.

### F7: Blocker in the interval checkpoint, fixed here: integer mass could overflow

The checkpoint scaled rational weights into `numpy.int64`, summed them there for
**Condition 2**, and used them in Boolean-matrix products for **Condition 5**. It
bounded `n × scale`, but a candidate is allowed to carry an arbitrarily large
nonnegative total before **Condition 2** rejects it.
A large weight, total, or subset sum could therefore wrap before the rejection and
corrupt both conditions.

**Resolution:** weights are now scaled and summed first as Python integers.
Negative values are refused defensively, and totals at or above `2^62` are refused
before any NumPy array is constructed.
Every later matrix product is a nonnegative subset sum below that exact total.
A positive-weight `2^63 + 1` regression exercises the public path.
D-446 records the defect.

### F8: High and medium package gaps, fixed here: falsification and hostile inputs

The standalone falsifier originally had no expected verdicts: it printed a convincing
mutation table and returned success regardless of whether a mutation was accepted or a
condition changed. The package’s original one-command check did not run it.
Separately, the verifier silently coerced JSON decimals, strings, and Booleans through
`int(...)`, accepted duplicate keys, indexed malformed atom records before validating
them, and raised on both empty and singleton feasible domains.

None changes the shipped certificate’s arithmetic.
They do matter to the package’s claim to be a compact trust boundary.

**Resolution:** every full mutation now has an exact oracle for its verdict, conditions,
and minimum, and a quick signed-weight refusal runs in `check.py`. The loader is strict
and duplicate-free, malformed input becomes a clean refusal, an empty placement domain
is treated as vacuous, and a singleton closed placement is evaluated directly.
D-436, D-442, and D-443 record these defects; focused tests cover each case.

### F9: Blocker in the interval checkpoint, fixed here: enclosure mode could certify failure

The interval verifier has two modes.
Its ordinary mode stops once each direction has a lower bound of one; `enclose=True`
continues until lower and sampled upper bounds meet so it can report the exact minimum.
The checkpoint classified any completed enclosure search with no stalled box as
certified. It never checked that the enclosure’s lower endpoint reached one.
A small rational grid certificate therefore returned `accepted=True` beside the exact
enclosure `[0,0]`.

This did not flatter the retained `n = 11` object—its enclosure is strictly above
one—but it made the stronger-looking public mode logically weaker than the ordinary one.

**Resolution:** every direction is certified only when all boxes close and its lower
bound reaches the exact unit mass scale.
A sampled upper bound below one refutes **Condition 5** in either mode, and
whole-certificate acceptance rechecks every direction.
The former `[0,0]` acceptance is a must-refuse regression.
D-435 records the defect.

### F10: High in the interval checkpoint, fixed here: an exact seam made refusal infeasible

Outward-rounded boxes cannot close a coverage seam where one atom region’s leave-edge is
exactly another’s enter-edge.
The search correctly intended to return `undecided` at its resolution floor, but it
tiled the whole seam down to that floor.
Measurements grew from 4,631 boxes at `10⁻²`, to 274,303 at `10⁻⁴`, to 33,583,223 at
`10⁻⁶`; the production `10⁻¹²` test was not operationally finite.

**Resolution:** each direction has a conservative 100,000-box work budget.
Exhaustion returns lower bound zero and an explicit non-acceptance unless an admissible
sampled point already refutes **Condition 5**. The exact-seam regression now finishes in
under a second. None of the three full retained controls stalls or exhausts the budget.
D-447 records the defect.

### F11: Medium in the shared sweep, fixed here: a reported minimum centre could be infeasible

The exact sweep correctly includes an open event cell when it intersects the rotated
feasible-centre polygon, but it returned the midpoint of the whole cell.
At a polygon corner that midpoint need not be feasible.
An exact one-atom fixture at direction `(3/5,4/5)`, `L = 2`, and `B = 1` returned
rotated centre `(1,−1/5)`, which maps to `(19/25,17/25)`; its y-coordinate is below the
exact feasible margin `7/10`.

The minimum value and all retained bounds were unaffected: mass is constant on the open
cell, and the inclusion test already proved that some feasible point exists there.
The bug made the displayed witness untrustworthy.

**Resolution:** the sweep now clips the exact feasible polygon to the minimizing cell,
returns the average of that convex polygon’s vertices, and checks strict membership in
the open cell. The fixture now maps to the feasible centre `(13/18,43/60)`. D-448 and a
focused regression record the repair.

### F12: High provenance defect, fixed here: the new commit names the wrong certificate hash

Commit `6fc71ce9` says its exact and interval decisions read frozen certificate bytes
with SHA-256 `503c7d154d36ae1e16d3002ab3c5b003316fc47c14718cf65b3dbc43af4d7cd6`. The
`certificate.json` blob in that commit and at the reviewed head instead hashes to
`b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a`. The advertised
digest occurs nowhere in the tree.

This discrepancy is not a mathematical counterexample, but it severs the commit
message’s claimed link between transcript and artifact.
The original exact/interval run cannot establish which bytes it read merely because its
reported rational values agree.

**Resolution:** this review discards the old attestation, binds the actual retained hash
in a fast test and the theorem-specific checker, and reruns both full decisions from the
retained path. D-449 preserves the mismatch rather than rewriting history.

### F13: High in the full gate, fixed here: the exhaustive suite could not finish under its timeout

D-438 correctly moved complete finite certificate decisions out of the fast test tier.
The full validator then collected all 36 marked tests in one pytest step, but left that
step on the shared 900-second timeout.
During this review it was still running after 4,100 seconds under an explicit two-hour
measurement override.
The default full command would therefore kill a healthy exact-decision suite long before
completion.

**Resolution:** only the exhaustive exact step now has a 7,200-second declared ceiling.
The shared 900-second hang guard remains in force for short checks, and a tighter
timeout typed by an operator still takes precedence.
D-451 records the mismatch and the budget registry test fixes the complete three-step
exception set.
The late full-net `n = 17` control and the retention gate’s full two-route
replay raise the current inventory to 38; the same explicit budget covers them.

### F14: Medium in the late parent, fixed here: a finite-certificate ceiling became a method-impossibility claim

The late parent correctly proves that a certificate with `m = ceil(sqrt(n))` must
satisfy `L ≤ mB < m`: if `L > mB`, the container holds `m²` pairwise disjoint closed
axis-parallel `B`-squares, and **Condition 2** contradicts the mass that **Condition 5**
assigns them. It then says the method can never settle a case such as `n = 12` whose
value is the grid bound `m = 4`.

That last inference is too strong.
For the uniform half-tangent net with endpoint `T` and `K` gaps, `D = T/K` and the
ceiling is `m/(1+T/K)`, which tends to `m`. A proved family of valid certificates with
sides tending to `m` would establish the weak lower bound `s(n) ≥ m` even though no
finite member attained `m`. The ceiling rules out one finite certificate at the grid
bound; by itself it does not rule out a certified family plus a limit argument.

**Resolution:** the affected prose now states the finite scope and names the separate
limiting-family possibility.
An exact regression pins that the uniform-net ceilings are strictly below, but
arbitrarily approach, the grid bound.
D-452 records the distinction.

### F15: Low in the late parent, fixed here: the net endpoint was described as rounded down

The new certificate-reach renderer says `207107/500000` rounds `tan(π/8)` down.
Its exact **Condition 3** slack is `T² + 2T − 1 = 309449/250000000000 > 0`, so `T` is
strictly above the positive root `sqrt(2) − 1 = tan(π/8)`. Rounding it down would make
the direction net stop short of `π/4` and fail the theorem’s endpoint premise.

**Resolution:** the comment now says that `T` is the rational endpoint just above
`tan(π/8)`. The existing exact **Condition 3** regression pins the direction of the
inequality; D-453 records the prose error.
No certificate value or computation changed.

### F16: High integration defect, fixed here: the moving parent reused D-441

The parent added a candidate-retention defect as D-441 after this stack had already
accepted D-441 through D-453. A literal merge produced two meanings for one stable
identifier and incompatible generated counts.

**Resolution:** the older stack identifiers remain stable and the newer parent entry is
D-454, as [`conventions.md`](../../../conventions.md) requires for a merge collision.
The source and generated views were regenerated from the combined 468-entry log.
D-455 records the collision itself.

### F17: Blocker in the late parent, fixed here: RETAINABLE did not bind the declared theorem

The new `decide_certificate` command recomputed the certificate geometry, but it never
inspected `claim`, allowed `total_mass` and `least_cell_mass` to be absent, and parsed
`n` and `direction_steps` with `int(...)`. A file whose only change was
`"claim": "s(11) >= 4"`, one with deleted summaries, or one containing values such as
`11.9` and `180.9` could reach `RETAINABLE`. Malformed input escaped by traceback and
stopped the remaining paths in the batch.

This is verdict-bearing declaration drift: the two expensive computations can decide one
certificate while the retained bytes tell a reader they prove another theorem.

**Resolution:** the loader now rejects duplicate keys, JSON decimals, non-string or
overlong rationals, coercive integer types, malformed atom rows, unsupported direction
or atom counts, and missing required fields.
Before formatting exact mass it bounds the common denominator and integer total at the
interval verifier’s arithmetic limit.
It requires the canonical claim and total mass to match the reconstructed object,
requires the least mass in full mode, and converts each malformed or unsupported path
into a refusal without aborting later paths.
D-456 and the hostile loader matrix record the repair.

### F18: High in the late parent, fixed here: known preflight failures still ran both sweeps

The command accumulated an impossible-side or excessive-mass failure, then ran the exact
event sweep and interval branch-and-bound before printing the refusal.
Two small known failures each took about eight seconds; the exact route on larger
candidates can take hours.
The test named “before any sweep runs” asserted only output text.

**Resolution:** every preflight problem now returns before either route.
A full decision runs the interval rejection route first and starts the exact sweep only
after receiving an accepted, unstalled, point enclosure.
The regressions replace both route functions with exceptions on preflight and replace
the exact route with an exception on interval refusal or an unusable enclosure.
D-457 records the cost defect.

### F19: Medium in the late parent, fixed here: the two-route conjunction lacked negative controls

The only full-mode test was a positive retained certificate.
Deleting the interval refusal, exact refusal, missing-enclosure, nonzero-width,
route-disagreement, declared-minimum, or multi-path exit-status branches left that test
green.

**Resolution:** injected negative verdicts now exercise every core conjunction branch,
including stalled interval boxes, a missing exact minimum, an interval refusal that must
prevent the exact route from starting, a failed final reread, and a malformed first path
that must not hide a second refusal.
D-458 records the control gap.

### F20: Medium record contradiction, fixed here: the retention defect claimed a loss it disproved

The corrected parent narrative explains that the solver processes survived a container
restart, yet its title still said a kill “lost the candidate” and its fix still referred
to “the two drivers that lost candidates.”
It also claimed corrected scratchpad-driver wiring that is not retained in the
repository.

**Resolution:** D-454 now describes the loss conditionally.
The repository’s `generate_adaptive` entry point defaults to returning before any exact
decision, so its caller can freeze the candidate first; a regression fails if the
default invokes the in-memory verifier.
Retained work must then write a file and pass that path to the retention command.
D-459 records the narrative correction.

### F21: Low assurance overstatement, fixed here: the retention routes were called model-independent

The retention-command docstring said the exact and interval routes “share no modelling
assumption.” Both consume the same `Certificate` representation and implement
**Conditions 2–4**. Their valuable independence is narrower: event-cell enumeration and
interval branch-and-bound make method-distinct **Condition 5** decisions with different
failure modes.

**Resolution:** the docstring now states both the shared contract and the distinct
**Condition 5** methods, and a regression pins that boundary.
D-460 records the overstatement.

### F22: Low robustness defect, fixed here: two long phase results were still buffered

The final parent commit added `flush=True` to most progress output but missed the exact
and interval result lines.
Under captured stdout a finished phase could therefore remain invisible throughout the
next multi-minute computation, contrary to the commit’s claim that every decision-path
print flushed.

**Resolution:** every status and verdict print now flushes, and a fake positive full run
records every print call and requires the flag.
D-461 records the repair.

### F23: Medium robustness defect, fixed here: an interval input refusal could abort a batch

The interval route intentionally refuses an unsafe integer scale, an angle outside its
certified domain, or certificate geometry outside safe finite-float arithmetic.
Those input-domain non-decisions previously escaped as built-in exceptions, so one
unusable path could prevent all later paths from receiving a verdict.
Inputs at the largest finite float exposed a second boundary: conversion succeeded,
later arithmetic produced infinities or NaNs, and one zero-weight orbit emitted more
than a thousand NumPy warnings.

**Resolution:** documented input-domain failures now have the narrow
`IntervalInputError` type and become labeled per-path refusals.
Exact conversion, scalar enclosure arithmetic, and rotated-atom setup translate or
detect nonfinite results at that boundary, while expected overflow warnings are
contained. Unexpected `ValueError` and `OverflowError` exceptions from either verifier
remain visible as implementation bugs.
A real huge-coordinate record proves the batch continues; D-462 records the boundary.

### F24: Blocker soundness defect, fixed here: RETAINABLE named mutable, possibly replaced bytes

The command read a certificate path once, then spent minutes or hours deciding the
in-memory object. Another process could replace the path during either sweep and the
command would still print `RETAINABLE`, apparently approving bytes it had never read.
This is the same generator-rewrite boundary the command was introduced to close.

**Resolution:** the gate freezes the initial bytes, checks that the path still contains
them after the interval decision (before paying for the exact sweep), checks again after
the exact decision, and prints their SHA-256 in the positive verdict.
Regressions rewrite the path during each route and require refusal; D-463 records the
defect.

### F25: Medium robustness defect, fixed here: stderr refusals lost candidate attribution

The retention command sent candidate headers to stdout but post-load refusals to stderr
as bare indented messages.
A normal automation that captures streams separately could not tell which input failed;
equal basenames made the earlier load-error form ambiguous as well.

**Resolution:** every refusal now carries the full path on stderr, positive progress
stays on stdout, and duplicate path arguments are skipped before a second decision.
Two-valid-file and malformed-file regressions use equal basenames in different
directories; D-464 records the repair.

### F26: Medium evidence defect, fixed here: the reach table called unretained reports measured optima

The generated reach table and synopsis called four, then five, restricted program values
measured optima. The latest parent added a sixth report at side `4.68`, including exact
run counts and elapsed time, but retained no raw log, checkpoint, or candidate.
The same evidence gap applies to the displayed objectives at `3.82`, `3.96`, `4.58`, and
`4.59`. Only the displayed `3.95` value is recomputable from a tracked artifact, and
that artifact establishes a feasible mass, not optimality.
Frozen certificates at `4.58` and `4.59` have nearby but different masses.

**Resolution:** the renderer now places the evidence status beside every value.
The synopsis, agenda, and T-019 narrative distinguish operator reports, retained
feasible masses, and proved optima; the proposed quadratic is labeled an unverified
planning conjecture.
D-465 records the correction.

### F27: High detector gap, fixed here: the live rung-drift check missed the next live rung

When T-019 moved from `4.58` to `4.59`, its source still said “this certificate’s
16.965735” rather than the new mass `16.933080`. The dedicated rung-figure detector
passed because it recognized phrases such as “total mass” but not this possessive bare
mass. Thus the first subsequent live update reproduced the class the detector claimed to
close.

**Resolution:** the parser recognizes the narrowly anchored “certificate’s DECIMAL
reaching” form, its own examples name the current top rung, and the exact stale phrase
is a must-fail regression.
D-466 records the recurrence of D-439.

### F28: High record drift, fixed here: T-019’s case pages and evidence stayed on its predecessor

The latest parent changed the structured lower bounds for `n = 17`, `18`, and `19` to
`459/100` while leaving all three case bodies at Massaccesi’s `4.5058`, with obsolete
gaps and monotonicity composition.
The `n = 18` and `n = 19` bound fields also cited historical evidence that proves only
`4.5058`. Related successor notes, test prose, and evidence said `451/100` or said the
current certificate did not reach `n = 20`, although its mass below 17 makes it directly
valid there—it simply does not improve Nagamochi’s stronger bound.

**Resolution:** the case bodies now state the current first-party certificate, direct
**Condition 2** composition, and correct gaps.
Current bound fields cite only the exact and interval certificate evidence; historical
results remain labeled as predecessors.
A cross-page regression binds all three frontmatter records and bodies; D-467 records
the repair.

### F29: Medium robustness recurrence, fixed here: restricted interval search leaked overflow warnings

D-462 gave interval input failures a typed refusal and contained overflow while
constructing each direction search.
The public verifier then called the search itself outside that containment boundary.
A finite certificate with side `10^308`, no atoms, and one restricted near-diagonal
direction emitted sixteen NumPy overflow warnings while tightening its first box.
It did not produce a false acceptance, but it contradicted the documented quiet-refusal
boundary and allowed an infinite intermediate to be intersected away before the existing
final-result guard saw it.

**Resolution:** vector interval operations now refuse nonfinite intermediate or final
results with `IntervalInputError`; tightened search bounds have their own guard; and the
complete direction search contains expected NumPy overflow warnings.
The regression uses the public `verify_by_intervals` API with the exact finite
reproducer and requires a quiet, typed refusal.
D-468 records the recurrence.

### F30: High gate-performance recurrence, fixed here: the pre-push suite lost its measured timeout

The validator initially gave the complete ordinary behavioral suite a 1,800-second
budget, based on a 1,209-second clean run.
The `--push` entry point constructs a separate reachable-test step dynamically.
When conservative selection expanded that step to the complete ordinary suite, it still
inherited the shared 900-second cap and was killed at 88% completion.
Three failures printed earlier in that run were separately reduced to the local
sandbox’s refusal to bind loopback ports; all three passed together outside the sandbox
in 2.90 s. They do not explain the timeout.

**Resolution:** a whole-suite `--push` decision now reuses the same measured budget as
`fast behavioral tests`; a genuinely reachable subset keeps the 900-second hang guard,
and an explicit operator timeout still wins.
The final 1,810-test pass took 1,788.95 seconds and the validator measured its step at
1,791.00 seconds, leaving about nine seconds under 1,800. The shared whole-suite ceiling
is therefore 2,700 seconds, 50% above the observed step time, rather than a cap already
at 99.5% utilization.
A regression exercises both selector outcomes.
D-469 records the recurrence of D-438.

### F31: High parent-integration drift, fixed here: the new `n = 12` rung inherited old evidence

Commit `9d90aabe` advanced the moving `n = 12` certificate to `99/25` and 2,097 atoms;
the parent then advanced through `719c2a17` with agenda and README edits.
Its result and case still cited the source-distinct independent verifier even though
that program and its review decide only the historical `19/5` and `77/20` files.
The primary evidence entry still described an intermediate `197/50`, 681-atom
certificate, while the case body described `77/20` and 113 atoms.
The README and replay prose likewise stopped before the eighth rung.
Replay also bound its VERIFIED result only to total mass, so stale claim and
least-cell-mass declarations could survive, and moving the live pointer silently removed
the former `79/20` rung’s complete interval control.

**Resolution:** all reader, frontier, evidence, and replay surfaces now bind to the
current `99/25` certificate and its exact and interval decisions.
The independent exact verifier is pinned to `certificate-77-20.json`, retained as
historical evidence, and explicitly excluded from support for the current bytes.
A cross-record regression pins the current certificate figures, evidence pair, case,
README, and replay orientation together.
Declaration-mutation tests bind all three replay fields, the archived `79/20` full
interval decision is restored, and the ladder-wide coarse test is labeled as sampled
coverage rather than verification.
D-470 records the recurrence of D-467.

### F32: High gate-performance recurrence, fixed here: the new exact decision outgrew the exhaustive budget

The pre-parent exhaustive suite took 4,826.82 seconds for 37 tests.
The introducing commit reports 4,866 seconds for the new current `n = 12` exact
decision, replacing a predecessor whose recorded ceiling was 1,500 seconds.
Even conservative replacement arithmetic puts the current suite above 8,192 seconds, so
its 7,200-second declared ceiling could no longer contain the assigned work.

**Resolution:** the exhaustive exact step now has a separately justified 14,400-second
ceiling, while ordinary and short steps keep their tighter guards.
The validation registry pins the exceptional step and its budget.
Another approach to this ceiling requires redesign rather than an unexplained increase.
D-471 records the recurrence of D-451.

### F33: High quantitative record defects, fixed here: two measurements became complexity laws

The same parent called a `0.001040` margin twenty-eight times tighter than every
retained rung, although the previous-smallest margin is `0.007175`, a factor of about
6.9. It called 2,097 atoms three times every other retained certificate, although the
next largest has 1,184 atoms, a factor of about 1.77. It also projected rationalisation
loss across a twentyfold scale without labeling ceiling effects, and promoted effective
exponents from two certificate sizes to general quadratic and linear complexity.
Agenda 019 retained the superseded contended estimate `13,000/167 s` after the parent
reported `4,866/110 s`, while saying every figure had a retained log.

**Resolution:** the comparison arithmetic is corrected; the rationalisation passage
states both its inverse-scale estimate and worst-case bound; the 2.09 and 0.92 exponents
are labeled two-point effective slopes; and the 4,866/110 pair is preserved as an
operator-reported planning baseline without a raw timing transcript, hardware
description, or load trace.
Agenda 019 now begins by reproducing it.
D-473 records the defect.

### F34: Medium literature-record recurrence, fixed here: a recovered source remained unavailable in prose

The resource archive recovered Trump’s 2023 author note on 2026-08-27. The tutorial and
six evidence-gap statements nevertheless continued to say that the writeup or Trump’s
personal site was not retained.
That conflated the available 2023 paper with the still-unretained original 1979
communication.

**Resolution:** those surfaces now distinguish the two, and the complete `s(11)`
priority and method search is retained as a resource receipt, indexed from the resource
page and linked from the `n = 11` case, T-018 artifacts, evidence entry, and historical
survey addendum. D-472 records the recurrence of D-332.

### F35: Medium literature-provenance drift, fixed here: priority and archive claims outran the sources

The archive retained Göbel’s 1979 PDF but omitted it from the paper index and said every
paper had a cleaned and raw transcription, although that source is PDF-only.
The `n = 11` case and historical survey called Gensane and Ryckelynck’s 2005 elimination
the first exact algebraic characterization even though Trump’s retained 2023 note
reproduces an implicit equation he says he sent to Gardner in 1979; the original
communication is unavailable, so the repository cannot settle that computational
priority. Two canonical records also dated Stromquist’s unrestricted lower bound to 1979
rather than its unsupported 1984 memo assertion and published 2003 proof.
Several reader surfaces described T-018 as an absolute first instead of the first public
improvement located by the recorded search.

**Resolution:** the archive indexes Göbel and documents its PDF-only status; the survey
calls the 2005 work the first located published polynomial elimination and separates it
from Trump’s retrospective account; the Stromquist chronology is corrected; and every
T-018 priority statement carries the public-search boundary.
The method catalogue and tutorial now name Göbel, Kearney--Shiu, Nagamochi, Bentz,
Burns, and Massaccesi in their distinct historical roles.
A blind search also found a refereed 2024 paper that still calls the eleven-square
optimum unknown; the durable receipt records it as status corroboration, not theorem
evidence. D-474 records the finding.

### F36: Blocker in the optimized sweep, fixed here: its equivalence check compared one implementation with itself

The final parent replaced the exact verifier’s expanded cell list with one reachable
span per event-grid column.
That is the right optimization, but it also redefined the supposedly retained
`reduce_to_cells` reference as `reduce_to_spans` followed by tuple expansion.
The test that said the two reductions agreed therefore held by construction.
A shared off-by-one error in span construction would have passed every claimed
cell-for-cell equivalence check.

**Resolution:** the pre-optimization cell reducer is restored as an independent
implementation. It clips each slab and computes its reachable row indices directly; the
optimized span reducer shares neither that reachability loop nor the Fraction arithmetic
used after it.
Retained-rung tests compare the two event sets, cell sets, minimum values,
and witnesses. D-483 records the collapsed oracle.

### F37: Blocker in the optimized sweep, fixed here: its public integer entry point could bypass the overflow proof

The ordinary dispatcher proved that the scaled total mass was below its signed `int64`
limit before calling the integer sweep.
The integer function itself was public, however, and accepted a caller-supplied scale
without repeating that proof.
Individual weights could fit in `int64` while their coincident prefix sum overflowed, or
a non-integral scaled weight could reach NumPy through an unsupported call path.

**Resolution:** the public integer entry point now independently requires nonnegative
weights, a positive integer scale, integral scaled weights, and an exact scaled total
below the conservative limit before allocating its grid.
A direct-call regression with two coincident `2^62` weights must refuse.
D-484 records the trust-boundary gap.

### F38: High resource-safety defect, fixed here: parallel replay scaled memory with the host’s CPU count

The optimized verifier defaulted to `os.cpu_count()` workers and allocated one dense
event grid per worker.
On a high-core host that can turn a valid replay into tens of gigabytes of transient
memory. The Linux path also forced `fork` to make stdin callers work, which is unsafe as
a library default in a threaded host and does not address the same importability problem
on other platforms.

**Resolution:** worker selection uses the process-available CPU count and is capped by
four workers, the number of directions, and a conservative 512 MiB concurrent-grid
budget. A certificate whose one supported grid exceeds that parallelism budget runs in
one process rather than multiplying the allocation.
Non-importable `__main__` contexts, including missing paths, `<stdin>`, and `<string>`,
use the serial path; no platform forces `fork`. D-485 and focused scheduling controls
record the boundary.

### F39: Medium witness recurrence, fixed here: the integer route restored an infeasible midpoint

F11 and D-448 had already established that the midpoint of a reachable event cell need
not lie in the rotated feasible-centre polygon.
The new integer route returned exactly that midpoint, even though the Fraction route had
been repaired to return a point from the clipped intersection.
Its minimum remained correct, but its displayed witness could again fail its own
placement constraints.

**Resolution:** both routes use the exact clipped-cell witness constructor.
Their agreement tests therefore bind a feasible witness as well as the minimum.
D-486 records the recurrence.

### F40: High evidence drift, fixed here: operator timings became current benchmarks and complexity laws

The optimization commit reported substantial speedups, but the retained numbers were
operator observations without raw timing receipts; some were taken while the old
Fraction replay was still consuming the same machine.
They also precede the worker and memory caps added here.
Agenda and handoff prose nevertheless promoted them to current measurements, treated two
or three sizes as a settled cost law, and concluded that the retention gate no longer
bound the workflow.

**Resolution:** the record preserves the observations as pre-cap operator reports and
does not call them benchmarks for the corrected implementation.
Agenda 019 first measures the current exact and interval routes before retargeting;
Agenda 020 no longer infers a general complexity law or current gate ranking from the
old points. The duplicate full-certificate test was removed from the ordinary tier
because the existing exhaustive node already owns that decision.
D-487 records the evidence promotion.

### F41: High drift-detector regression, fixed here: a missing live certificate could silently select history

The rung-figure checker defined the current artifact as the file literally named
`certificate.json`, but the final parent fell back to the first resolved historical
certificate when that pointer was absent.
A result could therefore lose its live artifact and still have unqualified prose checked
against whichever old rung happened to be listed first.
The same change redefined every unqualified `margin` as distance to `floor(mass) + 1`,
even when the certificate’s declared target was larger; for T-020 that silently changed
“margin” from the recorded `n = 20` target to `n = 19`.

**Resolution:** a certificate-bearing result must resolve exactly one live
`certificate.json`; no historical fallback exists.
Unqualified margin means the certificate’s declared target, while prose such as “margin
below nineteen” is parsed and checked against that explicit integer.
Missing, duplicate, and swapped-target controls all fail.
D-488 records the detector regression.

### F42: Medium terminology defect, fixed here: proof conditions reused the confirmation ladder

The fractional-certificate proof, portable checkers, Lean report, and several historical
records called their five local hypotheses C₀ through C₄. Elsewhere the repository uses
`C0` through `C5` exclusively for epistemic confirmation levels, so a sentence such as
“the interval route decides C₄” was genuinely ambiguous: it could mean the fifth proof
condition or distinct-method confirmation.

**Resolution:** the proof contract and every maintained output now say **Condition 1**
through **Condition 5**. Adversarial tests use **Control 1**, **Control 2**, and so on;
external mathematical labels use typographic subscripts where they must be preserved.
`conventions.md` makes the reservation explicit.
D-489 records the collision.

## Frozen hypotheses and outcomes

| ID | Pre-registered hypothesis | Outcome |
| --- | --- | --- |
| H1 | **Conditions 1–5**, exactly as first stated, imply that eleven unit squares cannot fit at the certificate’s side (originally `19/5`, repeated at `381/100`). | **Refuted as stated.** Signed weights are a counterexample. **Pass after repair:** require `w_i ≥ 0`; the implication then applies unchanged to the new rung. |
| H2 | The retained bytes satisfy every explicit and implicit proof premise. | **Pass.** All 1,121 current weights are strictly positive, in addition to **Conditions 1–5**. |
| H3 | A source-distinct exact checker obtains mass at least one over all centres and all 181 net directions. | **Pass.** It obtains `4001/4000` exactly on the current bytes. |
| H4 | The declared literature search finds no lower bound after Stromquist 2003 that reaches the proposed value. | **Pass at apparent-novelty scope.** Searches for both `19/5` and `381/100` located no stronger public result; absolute priority remains unproved. |
| H5 | Replay and validation gates bind the retained claims and refuse targeted corruptions. | **Fail on the parent; pass after remediation.** The stack refuses signed weights and partial-net or below-one interval verdicts, bounds interval work and integer arithmetic, binds all retained and retention-command declarations to unchanged bytes and a printed digest, gives falsifications executable oracles, strictly parses portable records, and separates exhaustive decisions from the fast tier. |

The mathematical claim met the acceptance rule only after the missing nonnegative
premise was made explicit and checked against the concrete bytes.
H5 is why the parent does not pass unchanged and why the repaired stack, rather than the
original replay output, is the review’s final trust boundary.

## Proof audit

### The corrected implication

Let `K = [0,L]²` and let `μ` be a finite **nonnegative** atomic measure on `K`. Suppose
its weighted atoms are invariant under reflection in the diagonal, their total mass is
less than `n`, the direction net reaches `π/4`, the angular shrink condition is strict,
and every admissible shrunken square at a net direction has mass at least one.

Assume that `n` closed unit squares with pairwise disjoint interiors fit in `K`.

1. A square’s orientation may be reduced to `[0,π/4]`; reflect an individual square in
   the diagonal when its reduced orientation lies above `π/4`.
2. For the reduced orientation `φ`, choose the nearest net angle `θ`. If `d = |φ-θ|`,
   the half-angle parametrisation gives `tan d ≤ D`, where
   `D = max (t_{k+1}-t_k)/(1+t_k t_{k+1})`.
3. A concentric square of side `B` at angle `θ` has support radius `(B/2)(cos d+sin d)`
   in every normal direction of the unit square.
   Since `cos d+sin d ≤ 1+tan d ≤ 1+D` and `B(1+D)<1`, the closed `B`-square lies
   strictly inside the unit square’s interior.
4. **Condition 5** assigns that inner square mass at least one.
   Pull it back through any reflection; atom-measure invariance preserves its mass.
5. The pulled-back inner squares are pairwise disjoint.
   Nonnegativity now gives `n ≤ Σ_j μ(P_j) ≤ μ(K) < n`, a contradiction.

No packing exists at side `L`, and any packing at a smaller side would embed in
`[0,L]²`; hence `s(n) ≥ L`. Compactness is needed only for the optional stronger
statement `s(n) > L`, not for the claimed weak inequality.

### Obligation-by-obligation disposition

| Obligation | Result | Evidence |
| --- | --- | --- |
| Finite nonnegative atomic measure | **Parent fail; stack pass** | 1,121 finite, strictly positive weights; this stack adds the missing shared guard as well as the standalone theorem premise. |
| Atoms and exact arithmetic | **Pass** | 1,121 distinct rational sites; all deciding quantities are rational. The fast regression and minimal checker bind the actual digest; every complete run named that same retained path. |
| Symmetry used for orientation reduction | **Pass** | Exact D4 closure; the proof needs only diagonal reflection. |
| **Condition 2** total mass below 11 | **Pass** | `434547/40000 = 10.863675`; slack `5453/40000`. |
| Net starts at zero, increases, and reaches `π/4` | **Pass** | Uniform `t_k = (207107/500000)k/180`; **Condition 3** slack `309449/250000000000`. |
| Nearest-net containment | **Pass** | `D = 207107/90000000`; `B(1+D) = 899996306539/900000000000 < 1`. |
| Every net-direction placement has mass at least one | **Pass** | Source-distinct exact minima agree at `4001/4000`; no sampling or floating-point decision. |
| Closed-boundary convention | **Pass for this certificate** | With nonnegative weights, event-cell boundaries can only add mass; strict **Condition 4** puts every closed inner square inside one packed square’s open interior. |
| Pullback and disjoint-mass sum | **Pass after explicit nonnegativity** | D4 invariance preserves mass; inner squares lie in disjoint interiors; monotonicity is then valid. |
| Conclusion `s(11) ≥ 381/100` | **Pass** | No-fit at `L` also rules out every smaller container by embedding. |

## Minimal distillation

The shortest honest presentation is the one-minute implication in
[`t-018-proof.md`](../../../packing/cases/n11_fractional_certificate/t-018-proof.md),
followed by four exact facts about the retained data.
Its mathematical core is:

```text
positive symmetric mass < 11
  + a net angle whose closed B-square lies strictly inside each unit square
  + every such B-square has mass > 1
  => eleven disjoint inner squares have mass > 11, contradiction.
```

Only coordinate-swap invariance, not full D4 invariance, is needed.
The endpoint, gap, containment, total, and symmetry facts reduce to a few rational
equalities and inequalities.
The continuum coverage fact does not.
An honest proof must either rerun an exhaustive finite reduction or carry a
proof-producing partition receipt; a table of 181 reported minima is not enough.

The smallest practical audit surface is therefore a combination: the one-minute proof,
the exact **Condition 5** formula printed in `t-018-proof.md`, the immutable certificate
hash, and a theorem-specific standard-library checker.
Its proof-critical **Condition 5** geometry, scoring, and driver occupy about 156 lines;
the whole executable is 346 lines including strict input, declaration, checksum,
symmetry, arithmetic, output, and mutation checks.
It recomputes 567,130,649 cells and the exact minimum, then demonstrates a **Condition
5** failure after multiplying every weight by `3999/4001`. This is materially smaller
than the general 650-line portable verifier without hiding the continuum step in an
assertion.

The companion
[`t-018-proof-visual.svg`](../../../packing/cases/n11_fractional_certificate/t-018-proof-visual.svg)
is derived from the same frozen bytes.
It plots every atom, makes colored disk area proportional to weight, and outlines the
exact direction-zero witness: 84 atoms centered at `(27/50,27/50)` with mass
`4001/4000`. Its second panel magnifies the angle and clearance so they are visible
while printing the exact containment values underneath.
It is an explanation, not another proof route; the deterministic renderer recomputes the
displayed witness and refuses declaration drift.

## Lean feasibility spike

The bounded spike used Elan 4.2.1, Lean 4.32.1, and Mathlib 4.32.1 at commit
`520045ab14e26149ee970e2e617ca04b09bde5d6`. Its 149-line kernel proves:

- finite nonnegative weighted counting through a unique atom owner;
- the set-based wrapper that derives uniqueness from disjoint membership;
- mass preservation under an involutive reflection represented by an atom permutation;
- the exact `n = 11` **Conditions 2–4** rational inequalities; and
- the abstract support-radius inequality used for strict containment.

The source has no `sorry`, custom axiom, or `native_decide`. `#print axioms` reports
only Mathlib’s standard `propext`, `Classical.choice`, and `Quot.sound`; warm kernel
checks and builds take about four seconds.
The vendor-free
[`lean-spike`](../../../packing/cases/n11_fractional_certificate/lean-spike/README.md)
pins both direct and transitive dependencies and states its non-goals beside the source.

This is a successful feasibility result, not a formal proof of `s(11) ≥ 381/100`. It
does not yet define oriented squares or `s(n)`, prove the nearest-angle geometry, load
the 1,121 atoms, or prove **Condition 5**. The remaining ordinary geometry is plausibly
several focused days.
Formalizing arrangement correctness and the full **Condition 5** computation is the
largest remaining task, plausibly one to three or more weeks.
Direct kernel reduction of 567,130,649 rational cells would be a poor design.

The promising full-formalization route is a proof-producing per-direction certificate:
record exact feasible row intervals and range minima—at most roughly 181 × 2,243 rows
for this data—and prove a small Lean checker sound.
That would shrink the trusted computation without asking the kernel to repeat the
search.
`native_decide` would make a direct replay shorter, but Lean implements it with a
compiler-trusting axiom, which defeats the strongest third-party-verification goal.

**Disposition:** full Lean formalization is feasible, but the one-minute proof plus the
346-line exact checker is presently simpler and more compelling.
Keep the compiled Lean kernel as a formal audit of the load-bearing inequality and as
the starting point for a future proof-producing **Condition 5** receipt; do not present
it as validation of the headline claim.

## Exact certificate facts

| Quantity | Exact value | Margin or note |
| --- | --- | --- |
| `n` | `11` | — |
| `L` | `381/100` | `3.81` |
| `B` | `9977/10000` | `0.9977` |
| atoms | `1,121` | 1,121 distinct coordinates; every weight `> 0`; minimum `3/40000` |
| total mass | `434547/40000` | **Condition 2** slack `5453/40000` |
| terminal half-tangent | `207107/500000` | **Condition 3** slack `309449/250000000000` |
| largest half-gap tangent | `207107/90000000` | 180 uniform gaps |
| containment product | `899996306539/900000000000` | **Condition 4** slack `3693461/900000000000` |
| global covered-mass minimum | `4001/4000` | **Condition 5** slack `1/4000`; first attained at direction zero and centre `(27/50,27/50)` |

The small **Condition 4** and **Condition 5** margins do not create a numerical problem
because every deciding operation is exact.
They do make decimal transcription or floating-point reimplementation an inappropriate
trust path.

## Independent validation

Four complete decisions were reconciled against the retained `b121…e6a` bytes.
Three use exact event arrangements; the fourth covers centre boxes by directed-rounding
intervals and does not use the certificate’s symmetry premise for **Condition 5**.

| Lane | Independence boundary | Result |
| --- | --- | --- |
| Project replay | Primary `sqpack.fractional` prefix-sum implementation | **Conditions 1–5** pass over all 181 directions and 567,130,649 feasible event cells; minimum `4001/4000`. All three retained `n = 11` rungs replay. |
| Standalone general verifier | A standard-library implementation with its own strict loader and exact event sweep, pointed explicitly at the current JSON | All 181 directions pass at `4001/4000`; three minimizing cells per direction are re-summed directly; runtime 88.47 s in the independent review lane. |
| Minimal theorem-specific checker | A 346-line standard-library program with no project imports, bound to the actual certificate SHA-256 | All 567,130,649 feasible event cells pass at minimum `4001/4000`; direct summation confirms the witness at `(27/50,27/50)`; uniform weight scaling produces a genuine below-one refusal. |
| Interval branch and bound | NumPy implementation using outward-rounded region and domain boxes, direct centre-box coverage bounds, and the reflected half of the net instead of D4 reduction | All 361 directions certify in 1,570,831 boxes; no stalled or budget-exhausted box; global enclosure `[4001/4000,4001/4000]`. The same code obtains one-point enclosures for the retained `n = 12` certificate and the published-value `n = 17` reconstruction. |

The different cell counts reflect different conservative feasibility and boundary
enumerations; they do not represent skipped directions.
Every complete path agrees on the exact minimum and a direct witness.
Every path reads the same repository file; the fast test and minimal checker require its
actual SHA-256 before interpreting it.

A further run of the NumPy verifier originally written independently for `n = 12` was
stopped after 3,848 seconds without reaching a verdict on the larger 1,121-atom
instance; an earlier attempt was stopped after 501 seconds.
Its dense direct-summation matrix product is not a practical permanent gate.
That is a performance result, not mathematical evidence either way, and it is not
counted among the complete decisions above.
The complete standalone general verifier, which finishes in under two minutes, is the
retained source-distinct exhaustive test instead.
D-450 records that gate repair.

Negative controls included broken D4 orbits, reduced weights, removed atoms, an enlarged
container, a too-short angular net, non-strict containment, declared-value mutations,
the signed-weight theorem counterexample, a partial interval net, integer overflow, a
below-one interval enclosure, and an exact unresolvable interval seam.
The repaired shared and standalone entry points refuse the signed object before
verification.

The interval lane supplies decision-method diversity for **Condition 5**, but not
outside authorship or proof-assistant verification.
Every positive decision still relies on the rational direction-net containment lemma,
and every checker was produced within the project.
The frozen `19/5` third-party bundle separately reproduces Massaccesi’s `n = 17` result
as a known-answer scaling control.
It raises confidence in the shared theorem and the older verifier, but it does not
validate the extra `1/100` in the current certificate.

## Literature and novelty audit

### Established record

Stromquist’s 2003 paper
[*Packing 10 or 11 Unit Squares in a Square*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8)
states the unrestricted lower bound

```text
s(11) ≥ 2 + 2√(4/5) = 2 + 4/√5 = 3.7888543819… .
```

The new rational value exceeds it exactly because `5(381/100-2)² = 32761/2000 > 16`. The
improvement is about `0.021145618`, or `0.558%` of the old lower bound.
Against Trump’s best-known packing at approximately `3.877083590022814`, it closes about
`23.97%` of the previously open interval.
It does not determine `s(11)`.

The current
[Leaps in Bounds entry](https://leapsinbounds.org/constants/square-packing-in-square-11/)
and Friedman’s
[*Packing Unit Squares in Squares* survey page](https://erich-friedman.github.io/papers/squares/squares.html)
still report the Stromquist lower bound.
Trump’s page identifies his 1979 construction as the
[best-known packing](https://trump.de/square-packing/index.htm).
Nagamochi’s published general theorem in
[*Packing Unit Squares in a Rectangle*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v12i1r37)
gives only `1 + √6 ≈ 3.449` when specialized to `n = 11`.

### Search performed

The clean literature lane searched through 2026-09-04 for “unit,” “equal,” and
“congruent” squares packed in a square; `s(11)` and `s_11`; eleven-square lower bounds;
the exact constants `381/100`, `100/381`, and `110000/145161`, as well as the earlier
`19/5`, `5/19`, and `275/361`; and weighted, fractional, resource, and unavoidable-set
formulations. It checked the local source corpus, arXiv title and full-text results,
Crossref, OpenAlex, Semantic Scholar citation chains, author pages, public packing
catalogues, and recent fixed-`n` and asymptotic papers.
No later public lower bound above Stromquist’s value was found.

The search is not a proof of priority.
It did not exhaust subscription-only MathSciNet or zbMATH full text, every thesis or
proceedings volume, non-English and unindexed pages, private correspondence, or
unpublished work. The appropriate label remains **apparently novel**. A precise public
claim would be: “the first located public improvement to the `s(11)` lower bound since
Stromquist 2003, as of 2026-09-04.”

### Method lineage

The proof is an instance of fractional hitting-set weak duality:

- Göbel’s 1979 unavoidable points supply the integral hitting-set precursor.
- Kearney and Shiu’s 2002 dual-lattice proof counts two unavoidable point systems
  simultaneously, an integral multi-cover precursor.
- Nagamochi 2005 uses nonnegative point, segment, and area resources—the substantive
  weighted-resource antecedent.
- Bentz 2016 names this family “resource starvation” and summarizes the point, segment,
  area, and continuously moving resource variants.
- Burns’s
  [August 2026 post](https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/)
  and linked proof note give the recent pure-atomic rational orientation-net form.
- Massaccesi’s
  [August 2026 post](https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html)
  introduces the LP-generated `n = 17` certificate and parameters used as the control.

“Burns–Massaccesi certificate” is reasonable shorthand for that recent implementation
line. It should not imply that weighted resource counting itself began in 2026.

### Reconciliation into the source and frontier records

The bounded search is now retained at
[`s11-lower-bound-literature-audit-2026`](../../../packing/resources/web/s11-lower-bound-literature-audit-2026/README.md),
not only narrated in this review.
The resource index lists it; the `n = 11` case names it as context and carries a
2026-09-04 source-review date; T-018 lists it among its artifacts; and
`E-n011-fractional-certificate` points to it as the receipt behind the novelty scope.
The 2026-08-22 `s(11)` survey now has a dated addendum for `381/100`, preserving its
older historical snapshot instead of silently rewriting it.

No source found in this reconciliation changes another frontier endpoint.
The current public catalogues still carry Stromquist’s lower value and Trump’s upper
construction; they corroborate the search result but are not evidence for the new
theorem. The recovered Trump 2023 author note strengthens upper-bound provenance only.
The method sources change attribution, not the validity or priority of the concrete
`n = 11` certificate.

## Further formalities, in assurance order

### Completed on this stack

1. The shared theorem boundary now requires nonnegative weights and retains the exact
   signed counterexample as a must-refuse test.
2. Exact declarations govern replay acceptance, hostile portable records are refused,
   and the falsification table has executable oracles.
3. Full exact and interval decisions are named `exhaustive_exact` tests rather than
   hidden work in the fast tier.
4. The interval verifier cannot accept a sampled net, a wrapped mass, a below-one
   enclosure, or an unresolved seam; the complete `n = 11` run still certifies.
5. Independence, control provenance, method lineage, monotonicity, and apparent-novelty
   language now match the evidence.
6. A one-minute implication and the exact finite **Condition 5** lemma are isolated in
   [`t-018-proof.md`](../../../packing/cases/n11_fractional_certificate/t-018-proof.md).
7. [`TUTORIAL.md`](../../../TUTORIAL.md) now introduces atoms, weighted mass, the
   counting contradiction, both finite reductions, and the two places nonnegativity is
   essential before sending a reader to the proof and checker.
8. The late parent’s general retention command now binds exact JSON types and every
   declared theorem value, refuses before expensive work where possible, requires both
   **Condition 5** routes in full mode, and has negative controls for every decision
   edge.

### Stronger evidence after this review

1. **Freeze an archival release.** Publish the proof, certificate, minimal verifier,
   checksums, machine-readable receipt, and precise provenance under a DOI. A release
   prevents a moving branch from being the object of mathematical citation.
2. **Obtain an outside audit.** Give only the theorem and data to a square-packing
   researcher or formal-methods reviewer; ask them to publish the commit and certificate
   hashes they checked.
   This would turn code-level diversity into reviewer independence.
3. **Formalize the stable kernel, selectively.** The Lean spike above shows that the
   nonnegative finite-measure counting lemma and rational **Conditions 1–4** arithmetic
   are small. Formalizing rotated-square containment and the full 567-million-cell
   **Condition 5** decision is feasible in principle but is not currently the simplest
   audit surface.
4. **Use proof-producing verification for Condition 5.** Have the enumerator emit a
   compact, versioned arrangement certificate and let a much smaller checker validate
   every feasibility interval and cell lower bound.
   The goal is to reduce trust in a 500-line search program, not to add another copy of
   it.
5. **Add a second proof-producing method if assurance must rise further.** The interval-
   certified branch-and-bound now tests the event-cell reduction by a distinct method.
   An exact SMT/MILP decomposition or a compact partition receipt checked in another
   language would be the next computational escalation.
6. **Close the priority search.** Search MathSciNet and zbMATH, check citing works and
   theses, and contact the survey/catalogue maintainers and recent `n = 17` authors
   before using language stronger than “apparently novel.”

## Validation record

All project commands used the repository’s Python 3.14 environment from `packing/`.

| Command or check | Result |
| --- | --- |
| `.venv/bin/python3 -m cases.n11_fractional_certificate` | Accepted all three retained rungs: `189/50`, `19/5`, and the current `381/100`; the current exact minimum is `4001/4000`. |
| `thirdparty/verify.py` on the current certificate, `--audit 3` | Accepted all 181 directions and 567,130,649 regions at minimum `4001/4000`; three cells per direction were directly re-summed; **Condition 5** took 88.3 s. |
| `minimal_verify.py` on the current certificate | Hash, **Conditions 1–5**, 567,130,649 cells, minimum `4001/4000`, and the `3999/4001` scaling refusal all passed; the final merged-parent rerun took 88.253 s. |
| final blind proof-only audit and minimal-checker reruns | **Accepted with no finding** in a lane that did not read this review or the PR discussion; two fresh runs passed in 87.42 s and 90.72 s, and a direct re-sum found 84 atoms of total mass `4001/4000` at `(27/50,27/50)`. |
| deterministic T-018 proof visual | The certificate-driven renderer’s `--check` passed; the repository SVG checker passed all **86 controls**, including byte determinism and artifact ownership. |
| `thirdparty/check.py` | All four frozen-package steps passed: reconstruct the published-value `n = 17` control, verify the `19/5` rung, verify the control, and require a labeled negative-weight refusal. |
| complete current T-018 interval confirmation | **1 passed** in 22.23 s; all 361 directions certified, with enclosure `[4001/4000, 4001/4000]`. |
| pre-latest-parent exhaustive exact suite at the repaired timeout (`0883f28e`) | **37 passed**, 1,744 ordinary tests deselected, in 4,826.82 s. The later parent adds one exhaustive `n = 17` control, which was run separately below. |
| current T-019 full-net `n = 17` interval control | **1 passed** in 44.64 s; all 361 directions certified in 3,683,951 boxes, with enclosure `[200009/200000, 200009/200000]`. |
| final-parent T-017 interval rerun | The current `99/25` bytes passed all 361 directions in 4,448,751 boxes with no stalls and enclosure `[12501/12500, 12501/12500]`. |
| restored historical T-017 interval control | **1 passed** in 31.37 s; the archived `79/20` bytes passed all 361 directions in 2,666,151 boxes with no stalls and enclosure `[20001/20000, 20001/20000]`. |
| current exhaustive collection | **1,849 tests collected:** 1,810 ordinary and 39 `exhaustive_exact`; collection took 4.65 s. |
| pre-final focused parent-integration matrix | **155 passed**, 11 exhaustive tests deselected, in 218.90 s across the retention gate, generator, exact and interval certificate, module-boundary, and rung-figure suites. |
| final moving-pointer regressions | **8 passed** in 70.04 s: declaration mutations, sampled ladder coverage, marker registration, ambiguous-rung handling, and timeout provenance. |
| current positive full two-route retention gate | **1 passed** in 170.83 s; the gate required both complete decision routes on unchanged `n = 11` bytes. |
| full integrated `packing-validate --push` | **35 of 60 selected steps passed** in 1,794.95 s; the whole reachable suite reported **1,810 passed, 39 exhaustive tests deselected** in 1,788.95 s. The validator measured the step at 1,791.00 s, prompting the budget-only 2,700-second headroom correction recorded in F30. |
| post-measurement budget regressions | **3 passed** in 0.11 s; the whole-suite entry points receive 2,700 seconds, subsets stay on the 900-second guard, and an explicit operator limit still overrides either. |
| final `packing-validate --edit` | **34 of 60 selected steps passed**; Ruff checked and formatted 801 files, BasedPyright reported zero errors and warnings, and all schema, generated-record, provenance, and edit-tier checks passed. |
| earlier integrated `packing-validate --push` at `0883f28e` | **34 of 59 selected steps passed**; the then-current behavioral suite reported **1,724 passed, 36 exhaustive tests deselected** in 879.26 s; the complete gate took 882.61 s. This receipt predates F23-F30 and is retained only as provenance for that snapshot. |
| exact five-atom signed certificate through `sqpack.fractional.verify` | **Incorrectly accepted**, proving F1. |
| `.venv/bin/basedpyright` at finding head `34d19470` | **Failed: 26 errors**, proving F2. |
| fresh-copy Lean build and axiom audit | `lake build Kernel` passed in 9.38 s; the audit passed in 2.55 s and reported only `propext`, `Classical.choice`, and `Quot.sound`. |

## Residual risk

After the repairs on this stack, the remaining mathematical risk is concentrated in the
written orientation-net argument and the continuum coverage decisions.
The argument was read from first principles.
The exact decision was independently reimplemented, checked on a published-value
control, and attacked with mutations; a method-distinct interval search covers a doubled
net and agrees exactly.
The review found no contradiction or remaining identified boundary gap in the concrete
positive-weight instance.

That is strong evidence for a computer-assisted result, but not formal verification or
external peer review.
The responsible conclusion is therefore specific: **the certificate establishes
`s(11) ≥ 381/100`; the result appears to improve the public record; and the repaired
stacked branch, not the reviewed parent alone, is the finished local research artifact.
External mathematical review and an archival release remain the most valuable next
formalities.**

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
