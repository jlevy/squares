# BC-254: Control-Only Pair Separator Build

The pair separator and its file checker are implemented and have passed the declared
source and toy controls.
Instrument readiness remains pending separate independent review and coordinator
acceptance. **No exp-113 candidate pair geometry, target optimization, new row, or
support extension was evaluated.** H-099 remains unresolved.

This is the bounded W7 correctness commission `think-4ej5`, assigned for
`2026-09-06T21:20:01Z`–`2026-09-06T21:50:01Z`. The
[preceding design](bc-254-post-screen-next-discriminator.md) declared the pair test,
source/toy controls, candidate-only consequence, and proposed 30-second producer and
replay limits before this build.
The coordinator owns the session, records, experiment freeze, Git, and any research
verdict. No existing accepted source, solver, or packet file was edited.

## Implemented Contract

The reusable
[pair separator](../../../../../src/sqpack/full_size_density/pair_separator.py) accepts
contained exact unit squares in one number field, nonnegative rational weights, at most
60 raw placements, and at most 134 eligible pairs.
It canonicalizes placement keys and deduplicates identical geometry without adding its
weight. Inconsistent weights on duplicate keys are refused.
Noncyclic or nonunit geometry, containment failures, floating weights, and mixed fields
are outside the accepted input domain.

Eligible pairs have distinct canonical keys and weight sum strictly greater than one.
They are visited in canonical key order.
The existing exact separating-axis test is interpreted with `is None`: its zero result
is contact, not interior overlap.
For each separated or touching pair, the packet retains an exact unit separating axis
oriented from the first member toward the second.

At the first strict overlap, the producer collects all corners contained in the other
closed square and all edge-segment intersections.
Parallel edges are not divided by zero; their shared endpoints are already included by
closed membership. The collected set contains every vertex of the convex intersection.
Its exact average is tested against both squares’ eight strict projection inequalities
and the four container inequalities.
If any inequality or positive rational enclosure fails, the producer refuses instead of
retaining a witness.

For a positive rational lower bound $\gamma$ on every margin, it emits the rational
radius $r=\gamma/4$ and exact excess $w_i+w_j-1>0$. This certifies the whole open
$L^\infty$ box of radius $r$, not just a point.
An edge normal has unit Euclidean length and therefore $L^1$ norm at most $\sqrt2<2$, so
each defining form changes by less than $2r$ in that box.
Its area is $4r^2>0$.

The box may cross a third square’s boundary.
Other weights are nonnegative, so the selected pair alone proves depth greater than one
throughout the box. The certificate does not record a full-support incidence vector and
must not be reused as a necessary LP row without the separate off-boundary guards.

## File Replay and Its Independence

The [checker](../../../../../devtools/check_full_size_density_pair_separator.py)
reconstructs named control geometry or the fixed target source, and compares the full
canonical geometry/weight signature.
It independently enumerates eligible index pairs.
Every supplied separation must cover the next pair in that order.
Direct dot products at all corners prove the claimed separating halfplanes; this does
not call the producer’s SAT routine or select an axis for it.

For a witness, the checker uses orientation-corrected edge determinants rather than the
producer’s projection forms or intersection routine.
It requires every square and container margin to exceed $2r$ strictly, checks the exact
overweight, and verifies that the witness follows the complete separated prefix.
A no-hit packet must contain a valid axis certificate for every eligible pair.
Missing, duplicated, or reordered pairs are refused.

The checker shares the exact number-field implementation, canonical square key and
single-square validation, control definitions, and serialization contract.
For future target mode, producer D4 construction uses `bind_source`; checker
reconstruction uses the existing explicit-map `reconstruct_source`. The
toy/source-control constructors themselves are shared.
This is independent certificate reasoning, not a fully independent arithmetic kernel or
independent original-source transcription.
Source reconstruction still uses the accepted packing validator, including its SAT
checks on the original 11-square packing.
Independence here concerns replay of the new candidate-pair certificates, not
replacement of every source-validation primitive.

The existing bounded JSON reader rejects nonregular files, symbolic links, oversized
packets, duplicate object keys, floats, and nonfinite numbers.
Coefficients and radii reuse its bounded canonical rational lexical contract before
conversion, with normalization equality afterward.
A short large-exponent string is refused before `Fraction` construction.
Booleans cannot stand in for integer versions, counts, or indices.
Geometry and weight metadata are compared to the reconstructed signature, not trusted as
input coordinates.

The only successful replay verdicts are `candidate-refuted` and `no-pair-obstruction`. A
witness invalidates only the fixed weight assignment; absence of a witness is not
almost-everywhere feasibility and does not refute H-099. The executable triple control
has common-interior depth $6/5$ with no eligible pair.

## Frozen-Candidate Interface: Uninvoked

The [producer CLI](../../../../../devtools/run_full_size_density_pair_separator.py)
requires either `--control NAME` or explicit `--candidate PARENT_PACKET`; there is no
default mode. Candidate mode binds the retained exp-113 source, exact support metadata,
the eight per-member weights

$$
(1,0,2/5,1/10,0,1/10,3/10,0),
$$

and the accepted finite-row ceiling $56/5$. The
[accepted parent packet](../exp-113-h-099-trump-support-screen/packet.json) and the
design already supply those values.
Its four unit-weight members and 32 other positive members give $\binom42+4\cdot32=134$
eligible pairs; this is arithmetic on retained metadata, not a new geometric result.
Both target entry points require that count.

This binding checks the parent’s source and fixed candidate, not its LP proof, row
generation, multipliers, or pivot history.
The accepted parent must still be frozen by Git revision and repository-relative path in
the next experiment.
No parent LP replay is hidden inside this tool.
The target construction, pair test, and target binding roundtrip remain unexecuted in
this control-only commission.

Both CLIs enforce a selectable integer limit of 1–30 seconds.
Their outer subprocess deadline covers worker startup and computation, and the internal
worker also has an alarm so direct `--worker` use does not bypass the bound.
Failed or timed-out workers do not publish partial stdout as a valid packet.
A timeout is an unresolved refusal, not a no-pair result.
These limits do not promise the target will finish.

## Controls and Measured Cost

The retained [tests](../../../../../tests/test_full_size_density_pair_separator.py)
cover:

- Positive-area axis-aligned overlap; exact edge contact, corner contact, and positive
  separation; overlapping weights whose sum is exactly one.
- A common-interior triple with all weights $2/5$, demonstrating the pair limitation.
- Cyclic corner shifts, reversed traversal, a quarter turn, geometric deduplication,
  inconsistent duplicate weights, invalid squares, and placement/pair caps.
- Degree-eight non-target translated and rotated toys, without constructing exp-113’s
  candidate; a rational overlap of width $10^{-30}$; and a first witness after two
  separated pairs.
- Tampered witness points, radii, excesses, field dimensions, keys, weights, counts,
  pair order, axes, and packet syntax.
  A monkeypatched conversion proves exponent refusal occurs before allocation; another
  control forbids producer geometry and eligibility helpers during successful replay.
- Original exact Trump source at unit weights: 11 placements, 55 eligible pairs, no pair
  obstruction. Its retained D4 uniform average: 60 placements, six eligible pairs, no
  pair obstruction. Both have exact mass 11. Tests forbid the candidate loader in these
  source-control paths.
- Actual producer/file-checker subprocess roundtrips on two source controls and the
  rotated degree-eight toy; explicit mode/cap refusals; simulated timeout and failed
  worker suppression of partial stdout.

TDD began with a missing-module failure for the core, followed by the first passing
strict-overlap/contact control.
The packet test then failed for the missing checker before that interface was
implemented. The first full source-control run exposed an incorrect test expectation of
zero eligible uniform-average pairs: the four weight-$3/4$ placements yield six pairs.
The tool correctly returned six nonoverlapping pairs; the expectation was corrected.
No scientific accept criterion changed.

The timed command, run from `packing/` with the existing frozen Python 3.14 environment
and no dependency synchronization, was:

```bash
/usr/bin/time -p env PYTHONPATH=src .venv/bin/python3 -m pytest -q -s tests/test_full_size_density_pair_separator.py
```

At the 37-test checkpoint it passed in 4.38 seconds of pytest time, with process wall
4.58 seconds and CPU 4.53 seconds (`user 4.29`, `sys 0.24`). Its actual CLI worker
receipts were:

| Control | Producer wall / CPU (s) | Separate checker wall / CPU (s) |
| --- | --- | --- |
| Rotated degree-eight toy | 0.056554500 / 0.056338 | 0.010524375 / 0.010480 |
| Original exact Trump packing, unit weights | 0.293798917 / 0.292501 | 0.126424625 / 0.125797 |
| D4 uniform source average | 0.431884541 / 0.429838 | 0.434426584 / 0.432212 |

These are worker costs, excluding interpreter startup and the outer process wrapper; the
timed test command above includes its child processes.
They price source/control arithmetic only.
**Candidate producer and candidate replay costs remain unmeasured.**

After adding the narrow-overlap and ordered-prefix controls, the focused command with
`tests/test_module_boundaries.py` passed 54 tests in 7.98 seconds of pytest time, 8.21
seconds wall, and 7.88 seconds CPU (`user 6.72`, `sys 1.16`). A final replay after the
control-constructor cleanup passed the same 54 tests in 7.74 seconds of pytest time,
8.03 seconds wall, and 7.58 seconds CPU (`user 6.79`, `sys 0.79`). This is not the full
research or publication gate.
Ruff passed on all four new Python files, and BasedPyright reported zero errors,
warnings, and notes.

The reusable source-control command, from `packing/`, is:

```bash
PYTHONPATH=src .venv/bin/python3 -m devtools.run_full_size_density_pair_separator --control trump-original-control-v1 --timeout-seconds 30
```

The CLI roundtrip tests retain a temporary control packet and invoke
`devtools.check_full_size_density_pair_separator CONTROL_PACKET --timeout-seconds 30` in
a separate Python process.
A future target producer instead requires `--candidate PARENT_PACKET`; its separate
checker requires the emitted packet and `--parent PARENT_PACKET`. Those target modes
have not been run.

## Remaining Work and Stop Conditions

The smallest next prerequisite is separately commissioned independent review of these
four Python files, the exact-domain argument, and this report.
Target execution is not authorized by passing these controls.
The coordinator must accept readiness and freeze a new prospective experiment, including
immutable engine/source binding, retained output paths, and one 30-second producer plus
one separately dispatched 30-second file replay.
The target cap is a spending limit, not a runtime estimate.

The proposed target stops at the first checked strict-overlap pair, complete exhaustion
of all 134 eligible pairs, or guard/time refusal.
No unchanged retry, triple search, new point row, reweighting, larger support, or new LP
follows automatically.
A checked pair witness retires only exp-113’s candidate; no pair obstruction leaves its
a.e. feasibility and H-099 unresolved.
Complete positive-area-face checking remains a separate, unfunded obligation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
