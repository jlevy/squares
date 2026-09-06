# BC-254 Support Controls: Independent Review

Verdict: **GO for the control-only implementation.** No Blocker, High, Medium, or Low
finding was identified within this commission.
This is not H-099 instrument readiness, target authorization, a retained support
verdict, or acceptance of a mathematical result.

## Scope and Evidence

W2 review for BC-254 / H-099 / `think-01q4`, against the author-confirmed stable
checkpoint on 2026-09-06. The observed review start was `19:41:31 UTC`, with a
ten-minute deadline of `19:51:31 UTC`. The coordinator owns session and active-time
accounting.

The review covered the complete [frozen design](bc-254-support-screen-spec.md),
[control report](bc-254-support-controls-slice-01.md), and three implementation files:

- [support_ceiling.py](../../../../../src/sqpack/full_size_density/support_ceiling.py),
  255 lines
- [check_full_size_density_support_ceiling.py](../../../../../devtools/check_full_size_density_support_ceiling.py),
  112 lines
- [test_full_size_density_support_ceiling.py](../../../../../tests/test_full_size_density_support_ceiling.py),
  89 lines

There is no `full_size_density/__init__.py` in the delivered tree.
The module imports and all focused checks succeed through the existing package layout;
the proposed empty file’s absence is not a finding for these controls.
Relevant exact-field and LP APIs were inspected, including their scalar domain,
minimization convention, feasible-basis contract, and multiplier equation.
No implementation file was changed.

## Mathematical and Engineering Checks

The support builder validates four cyclic corners, containment, unit lengths,
orthogonality, and closure in one exact field before generating the D4 images.
Its sorted reduced-coefficient keys identify physical squares without rounding and
without depending on corner traversal.
The orbit size counts distinct placements, not eight labelled transformations.
Selecting the least remaining key orders the orbits consistently with replay’s sorted
explicit orbit maps.

The projection producer and determinant replay use different incidence calculations.
Replay regenerates expected orbit keys from the declared seeds, compares the complete
support, and checks unit geometry and containment again.
It adjusts determinants by the square’s orientation, so reversed traversal and
reflections do not reverse inside and outside.
The row coefficient counts all containing members of an orbit; it is not a Boolean
orbit-coverage flag.

The radius argument is sound.
For each admitted point, the producer obtains a positive rational lower bound on every
absolute supporting-line form and container margin and divides their minimum by four.
Exact sign refinement precedes enclosure.
Replay checks strictly positive rational radius and strict margins greater than twice
that radius, using its independently computed edge determinants.
Unit edge length bounds each normal coordinate in absolute value by one, so a coordinate
change of at most the radius changes a form by at most twice the radius.
The resulting box lies inside the container, has positive area, and has constant
incidence.
Thus each row is necessary for almost-everywhere feasible weights; an isolated
sampled point is not being treated as a positive-area obstruction.

The LP adapter implements `min -mᵀa` with rows `A` and `-I`, right-hand sides one and
zero, and explicit `Fraction` zero and one.
The `-I` rows give an independent active basis at the feasible point zero.
Positive integer multiplicities and a positive coefficient somewhere in each column
imply finite coordinate bounds before solving.
The zero-budget refusal is preserved as an LP failure, not a research verdict.

The extracted incidence multipliers have the correct upper-bound sign.
The solver equation is `Aᵀy - z = m`; replay’s scalar check directly requires `y ≥ 0`
and `Aᵀy ≥ m`, and returns `sum(y)`. The adapter separately checks primal nonnegativity,
every row inequality, and equality of primal objective, upper bound, and negated solver
objective.
These arithmetic checks establish the reported toy LP optimum without trusting
solver status alone.

Replay does not invoke the optimizer or accept the producer’s incidence matrix.
It shares `check_upper` and `checked_rational` with the producer, as well as exact field
arithmetic and data types.
Consequently it is solver-independent with separately implemented geometry, not a fully
source-disjoint certificate implementation.
The report states the narrower claim correctly.
The scalar checker refuses Boolean or noninteger counts, nonpositive multiplicities,
negative multipliers, floats, malformed rationals, bad dimensions, and deficient column
inequalities.

## Controls and Remaining Scope

The four tests exercise the declared rational orbit, the two-variable fractional LP, the
degree-eight non-target orbit, and representation/mutation controls.
The fifteen expected refusals include a missing support member, changed incidence,
excessive radius, invalid multipliers, boundary equality, failed containment, an
uncovered LP column, exhausted pivot budget, and the disabled target side.
Both the support constructor and replay reject container sides other than two.
The algebraic test imports field constants; it does not construct the Trump packing.

The tests do not establish the full target instrument.
The deterministic initial-row fallback, fixed extension, source preimage receipt,
coalesced mass-eleven packing control, target loader and bounded command, and strict
serialized packet/file-checker boundary remain open as the author reports.
Typed in-memory inputs are not a replacement for that future parsing boundary.
In particular, these toy controls do not establish H-099’s runtime allowance or
authorize a target support, row, or LP. No additional code or documentation change is
requested for this slice.

## Independent Validation

The following focused commands ran from `packing/` through the frozen Python 3.14
environment in a non-login shell:

```bash
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache uv run --frozen --all-extras --group dev pytest -q tests/test_full_size_density_support_ceiling.py
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache uv run --frozen --all-extras --group dev ruff check src/sqpack/full_size_density/support_ceiling.py devtools/check_full_size_density_support_ceiling.py tests/test_full_size_density_support_ceiling.py
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache uv run --frozen --all-extras --group dev basedpyright src/sqpack/full_size_density/support_ceiling.py devtools/check_full_size_density_support_ceiling.py tests/test_full_size_density_support_ceiling.py
```

Results: `4 passed in 0.07s`; Ruff reported all checks passed; BasedPyright reported
zero errors, warnings, or notes.
All three checks had completed by the observed clock `19:45:17 UTC`. No separate CPU or
peak-memory measurement was made by this review.
No target calculation, broader integration gate, CI query, source-retention decision,
bead mutation, or Git operation was performed.
This review document is the only authored artifact; the coordinator owns integration
validation, instrument readiness, experiment freezing, and publication.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
