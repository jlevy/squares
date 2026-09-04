# Adversarial review of PR 78: the `s(11) ≥ 381/100` claim

**Review date:** 2026-09-04\
**Pull request:** [#78](https://github.com/jlevy/squares/pull/78)\
**Reviewed parent head:** `b77e78d2bcfcfa06cccfaac91110140edac1758d`\
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
| Does a method-distinct computation confirm C4? | **Accept on this stack** | The interval branch-and-bound certifies all 361 directions with no stalled or budget-exhausted box and encloses the minimum exactly at `4001/4000`. Samples, unsafe integer magnitudes, and below-one enclosures cannot produce acceptance. |
| Is the historical claim established? | **Apparently novel, high confidence** | The search found no public lower bound after Stromquist 2003 that reaches `381/100`, but it cannot establish absolute priority over unindexed or unpublished work. |
| Are the upstream commit’s frozen-byte claims reliable? | **No; repaired here** | The retained file hashes to `b121…e6a`, not the `503c…7cd6` named in the introducing commit. Both full decisions were rerun against `b121…e6a`; the old attestation is discarded. |
| Is the reviewed parent ready to merge unchanged? | **Request changes** | Its generic and interval verifier boundaries, retained declarations, falsification gate, provenance language, and validation classification all needed repairs. This stacked branch supplies them and records the result at C5 after validation. |

The most important distinction is between the parent implementation and the concrete
instance. The generic implementation was unsound; the specific instance was sound.
Adding the missing premise does not change the retained certificate: all 1,121 of its
weights were already strictly positive.

## Scope and adversarial method

This review concentrates on T-018, not PR 78’s separate `n = 12` result.
It checked the mathematical implication, the exact bytes retained for `n = 11`, the
continuum-to-finite reduction, replay and validation boundaries, method provenance, and
the novelty claim. The PR advanced repeatedly during the audit, from `9b85236b` through
`bdf63b21`, `6fc71ce9`, `31775018`, and finally `b77e78d2`. Commit `6fc71ce9` replaced
the `19/5` target artifact with a larger `381/100` certificate, so the concrete
validation restarted on the new bytes.
The later commits strengthened the separate `n = 12` and `n = 17` results and amended
the project process document; they did not change the reviewed `n = 11` bytes or
argument. The self-contained verification package, interval-certified branch-and-bound
checkpoint, and later retained `n = 17` certificates were included before the verdict
was frozen. The later `n = 17`--`19` frontier movement was outside this review’s
mathematical scope except where the earlier published-value `n = 17` certificate served
as a control.

The audit was pre-registered under `think-tukn` with five falsifiable hypotheses.
Two delegated lanes were kept separate from the coordinator’s main review:

- a proof/minimal-checker lane challenged the short implication and current certificate,
  then ran the standalone exact verifier; and
- a formalization lane assessed the Lean boundary and independently reran the complete
  interval decision.

The coordinator separately searched the literature, replayed the project verifier,
reconciled the retained artifacts, and constructed negative controls.
Runtime agreement alone was not an acceptance rule: the proof implication and every
implicit premise had to survive as well.

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
The following five-atom certificate satisfies the stated C0-C4 conditions:

| Datum | Value |
| --- | --- |
| `n`, `L`, `B` | `1`, `11/10`, `3/5` |
| half-angle tangents | `(0, 1/2)` |
| atoms | weight `+2` at `(11/20, 11/20)`; weight `-1` at each corner of `[0, 11/10]²` |
| total mass | `-2 < 1` |
| C2 slack | `1/4` |
| C3 product | `(3/5)(1 + 1/2) = 9/10 < 1` |

C0 holds by symmetry.
At angle zero, every admissible `3/5`-square contains the centre atom and at most one
corner, so its mass is at least one.
At the other net angle, `cos θ = 3/5` and `sin θ = 4/5`; every admissible square
contains the centre atom and no corner, so its mass is two.
Thus mathematical C4 holds as well.
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
D-435 records the defect.

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
D-441 records the classification failure; the final gate results appear below.

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
Nagamochi’s 2005 “resource starvation” argument already assigns nonnegative resources to
points, segments, and area and compares the amount every unit square consumes with the
total available. Burns’s August 2026 post and proof note supply the recent pure-atomic,
rational direction-net implementation; Massaccesi’s August 2026 work supplies the
LP-generated `n = 17` instance and parameters.
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
The neighbouring `n =
12` test does make that exact comparison
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
D-438 records the defect.

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
implementation marked C4 as holding whenever every selected direction certified.
The resulting `IntervalVerdict.accepted` was true even if 358 of 361 directions had not
been searched, and the tests explicitly required this outcome.

This is a direct sampled-to-universal soundness failure.
It did not affect T-018 because the checkpoint was not yet cited by any evidence entry,
but a future caller could have promoted a diagnostic to a false theorem verdict.

**Resolution:** a restricted run still reports per-direction certificates, enclosures,
and decisive refutations, but an all-certified sample is `undecided`; only the complete
doubled net can establish C4. The tests require both sides of this contract.
D-439 records the defect.

### F7: Blocker in the interval checkpoint, fixed here: integer mass could overflow

The checkpoint scaled rational weights into `numpy.int64`, summed them there for C1, and
used them in Boolean-matrix products for C4. It bounded `n × scale`, but a candidate is
allowed to carry an arbitrarily large nonnegative total before C1 rejects it.
A large weight, total, or subset sum could therefore wrap before the rejection and
corrupt both conditions.

**Resolution:** weights are now scaled and summed first as Python integers.
Negative values are refused defensively, and totals at or above `2^62` are refused
before any NumPy array is constructed.
Every later matrix product is a nonnegative subset sum below that exact total.
A positive-weight `2^63 + 1` regression exercises the public path.
D-440 records the defect.

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
D-436 and D-437 record these defects; focused tests cover each case.

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
A sampled upper bound below one refutes C4 in either mode, and whole-certificate
acceptance rechecks every direction.
The former `[0,0]` acceptance is a must-refuse regression.
D-442 records the defect.

### F10: High in the interval checkpoint, fixed here: an exact seam made refusal infeasible

Outward-rounded boxes cannot close a coverage seam where one atom region’s leave-edge is
exactly another’s enter-edge.
The search correctly intended to return `undecided` at its resolution floor, but it
tiled the whole seam down to that floor.
Measurements grew from 4,631 boxes at `10⁻²`, to 274,303 at `10⁻⁴`, to 33,583,223 at
`10⁻⁶`; the production `10⁻¹²` test was not operationally finite.

**Resolution:** each direction has a conservative 100,000-box work budget.
Exhaustion returns lower bound zero and an explicit non-acceptance unless an admissible
sampled point already refutes C4. The exact-seam regression now finishes in under a
second. None of the three full retained controls stalls or exhausts the budget.
D-443 records the defect.

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
the open cell. The fixture now maps to the feasible centre `(13/18,43/60)`. D-444 and a
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
retained path. D-445 preserves the mismatch rather than rewriting history.

## Frozen hypotheses and outcomes

| ID | Pre-registered hypothesis | Outcome |
| --- | --- | --- |
| H1 | C0-C4, exactly as first stated, imply that eleven unit squares cannot fit at the certificate’s side (originally `19/5`, repeated at `381/100`). | **Refuted as stated.** Signed weights are a counterexample. **Pass after repair:** require `w_i ≥ 0`; the implication then applies unchanged to the new rung. |
| H2 | The retained bytes satisfy every explicit and implicit proof premise. | **Pass.** All 1,121 current weights are strictly positive, in addition to C0-C4. |
| H3 | A source-distinct exact checker obtains mass at least one over all centres and all 181 net directions. | **Pass.** It obtains `4001/4000` exactly on the current bytes. |
| H4 | The declared literature search finds no lower bound after Stromquist 2003 that reaches the proposed value. | **Pass at apparent-novelty scope.** Searches for both `19/5` and `381/100` located no stronger public result; absolute priority remains unproved. |
| H5 | Replay and validation gates bind the retained claims and refuse targeted corruptions. | **Fail on the parent; pass after remediation.** The stack refuses signed weights and partial-net or below-one interval verdicts, bounds interval work and integer arithmetic, binds all retained declarations, gives falsifications executable oracles, strictly parses the portable record, and separates exhaustive decisions from the fast tier. |

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
4. C4 assigns that inner square mass at least one.
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
| C1 total mass below 11 | **Pass** | `434547/40000 = 10.863675`; slack `5453/40000`. |
| Net starts at zero, increases, and reaches `π/4` | **Pass** | Uniform `t_k = (207107/500000)k/180`; C2 slack `309449/250000000000`. |
| Nearest-net containment | **Pass** | `D = 207107/90000000`; `B(1+D) = 899996306539/900000000000 < 1`. |
| Every net-direction placement has mass at least one | **Pass** | Source-distinct exact minima agree at `4001/4000`; no sampling or floating-point decision. |
| Closed-boundary convention | **Pass for this certificate** | With nonnegative weights, event-cell boundaries can only add mass; strict C3 puts every closed inner square inside one packed square’s open interior. |
| Pullback and disjoint-mass sum | **Pass after explicit nonnegativity** | D4 invariance preserves mass; inner squares lie in disjoint interiors; monotonicity is then valid. |
| Conclusion `s(11) ≥ 381/100` | **Pass** | No-fit at `L` also rules out every smaller container by embedding. |

## Minimal distillation

The shortest honest presentation is the one-minute implication in
[`PROOF.md`](../../../packing/cases/n11_fractional_certificate/PROOF.md), followed by
four exact facts about the retained data.
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
the exact C4 formula printed in `PROOF.md`, the immutable certificate hash, and a
theorem-specific standard-library checker.
Its event-cell geometry and scoring core is about 140 lines; the whole executable is 346
lines including strict input, declaration, checksum, symmetry, arithmetic, output, and
mutation checks.
It recomputes 567,130,649 cells and the exact minimum, then demonstrates
a C4 failure after multiplying every weight by `3999/4001`. This is materially smaller
than the general 645-line portable verifier without hiding the continuum step in an
assertion.

## Lean feasibility spike

The bounded spike used Elan 4.2.1, Lean 4.32.1, and Mathlib 4.32.1 at commit
`520045ab14e26149ee970e2e617ca04b09bde5d6`. Its 149-line kernel proves:

- finite nonnegative weighted counting through a unique atom owner;
- the set-based wrapper that derives uniqueness from disjoint membership;
- mass preservation under an involutive reflection represented by an atom permutation;
- the exact `n = 11` C1-C3 rational inequalities; and
- the abstract support-radius inequality used for strict containment.

The source has no `sorry`, custom axiom, or `native_decide`. `#print axioms` reports
only Mathlib’s standard `propext`, `Classical.choice`, and `Quot.sound`; warm kernel
checks and builds take about four seconds.
The vendor-free
[`lean-spike`](../../../packing/cases/n11_fractional_certificate/lean-spike/README.md)
pins both direct and transitive dependencies and states its non-goals beside the source.

This is a successful feasibility result, not a formal proof of `s(11) ≥ 381/100`. It
does not yet define oriented squares or `s(n)`, prove the nearest-angle geometry, load
the 1,121 atoms, or prove C4. The remaining ordinary geometry is plausibly several
focused days. Formalizing arrangement correctness and the full C4 computation is the
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
the starting point for a future proof-producing C4 receipt; do not present it as
validation of the headline claim.

## Exact certificate facts

| Quantity | Exact value | Margin or note |
| --- | --- | --- |
| `n` | `11` | — |
| `L` | `381/100` | `3.81` |
| `B` | `9977/10000` | `0.9977` |
| atoms | `1,121` | 1,121 distinct coordinates; every weight `> 0`; minimum `3/40000` |
| total mass | `434547/40000` | C1 slack `5453/40000` |
| terminal half-tangent | `207107/500000` | C2 slack `309449/250000000000` |
| largest half-gap tangent | `207107/90000000` | 180 uniform gaps |
| containment product | `899996306539/900000000000` | C3 slack `3693461/900000000000` |
| global covered-mass minimum | `4001/4000` | C4 slack `1/4000`; first attained at direction zero and centre `(27/50,27/50)` |

The small C3 and C4 margins do not create a numerical problem because every deciding
operation is exact.
They do make decimal transcription or floating-point reimplementation
an inappropriate trust path.

## Independent validation

Four complete decisions were reconciled against the retained `b121…e6a` bytes.
Three use exact event arrangements; the fourth covers centre boxes by directed-rounding
intervals and does not use the certificate’s symmetry premise for C4.

| Lane | Independence boundary | Result |
| --- | --- | --- |
| Project replay | Primary `sqpack.fractional` prefix-sum implementation | C0-C4 pass over all 181 directions and 567,130,649 feasible event cells; minimum `4001/4000`. All three retained `n = 11` rungs replay. |
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
D-446 records that gate repair.

Negative controls included broken D4 orbits, reduced weights, removed atoms, an enlarged
container, a too-short angular net, non-strict containment, declared-value mutations,
the signed-weight theorem counterexample, a partial interval net, integer overflow, a
below-one interval enclosure, and an exact unresolvable interval seam.
The repaired shared and standalone entry points refuse the signed object before
verification.

The interval lane supplies decision-method diversity for C4, but not outside authorship
or proof-assistant verification.
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
- Nagamochi 2005 uses nonnegative point, segment, and area resources—the substantive
  weighted-resource antecedent.
- Burns’s
  [August 2026 post](https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/)
  and linked proof note give the recent pure-atomic rational orientation-net form.
- Massaccesi’s
  [August 2026 post](https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html)
  introduces the LP-generated `n = 17` certificate and parameters used as the control.

“Burns–Massaccesi certificate” is reasonable shorthand for that recent implementation
line. It should not imply that weighted resource counting itself began in 2026.

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
6. A one-minute implication and the exact finite C4 lemma are isolated in
   [`PROOF.md`](../../../packing/cases/n11_fractional_certificate/PROOF.md).

### Stronger evidence after this review

1. **Freeze an archival release.** Publish the proof, certificate, minimal verifier,
   checksums, machine-readable receipt, and precise provenance under a DOI. A release
   prevents a moving branch from being the object of mathematical citation.
2. **Obtain an outside audit.** Give only the theorem and data to a square-packing
   researcher or formal-methods reviewer; ask them to publish the commit and certificate
   hashes they checked.
   This would turn code-level diversity into reviewer independence.
3. **Formalize the stable kernel, selectively.** The Lean spike above shows that the
   nonnegative finite-measure counting lemma and rational C0-C3 arithmetic are small.
   Formalizing rotated-square containment and the full 567-million-cell C4 decision is
   feasible in principle but is not currently the simplest audit surface.
4. **Use proof-producing C4 verification.** Have the enumerator emit a compact,
   versioned arrangement certificate and let a much smaller checker validate every
   feasibility interval and cell lower bound.
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
| `thirdparty/verify.py` on the current certificate, `--audit 3` | Accepted all 181 directions and 567,130,649 regions at minimum `4001/4000`; three cells per direction were directly re-summed; C4 took 88.3 s. |
| `minimal_verify.py` on the current certificate | Hash, C0-C4, 567,130,649 cells, minimum `4001/4000`, and the `3999/4001` scaling refusal all passed in 83.522 s. |
| `thirdparty/check.py` | All four frozen-package steps passed: reconstruct the published-value `n = 17` control, verify the `19/5` rung, verify the control, and require a labeled negative-weight refusal. |
| complete current interval confirmation | **1 passed** in 19.14 s; all 361 directions certified, with enclosure `[4001/4000, 4001/4000]`. |
| repaired focused regressions | **56 passed**, 5 exhaustive tests deselected, in 6.01 s. |
| `packing-validate --edit` on the integrated stack | **33 of 59 steps passed**; Ruff checked and formatted 793 files, BasedPyright reported zero errors, and all schema, generated-record, provenance, and edit-tier checks passed in 29.16 s. |
| `packing-validate --push` on the integrated stack | **34 of 59 steps passed**; the reachable behavioral suite reported **1,724 passed, 36 exhaustive tests deselected** in 879.26 s; the complete gate took 882.61 s. |
| exact five-atom signed certificate through `sqpack.fractional.verify` | **Incorrectly accepted**, proving F1. |
| `.venv/bin/basedpyright` at the reviewed head | **Failed: 26 errors**, proving F2. |
| fresh-copy Lean build and axiom audit | `lake build Kernel` passed in 9.38 s; the audit passed in 2.55 s and reported only `propext`, `Classical.choice`, and `Quot.sound`. |

## Residual risk

After the repairs on this stack, the remaining mathematical risk is concentrated in the
written orientation-net argument and the continuum coverage decisions.
The argument was read from first principles.
The exact decision was independently reimplemented, checked on a published-value
control, and attacked with mutations; a method-distinct interval search covers a doubled
net and agrees exactly.
No contradiction or unexamined boundary case remains in the concrete positive-weight
instance.

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
