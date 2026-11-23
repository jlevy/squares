# Frozen Tiny Graph-Enumeration Pilot Plan

This is a plan only.
No graph-enumeration checker has been written, imported, syntax-checked or executed for
this pilot. The completed covariance and clause-census evidence is packaged separately
for the next n20 PR.

## Fixed Selection and Inputs

Select exactly sixteen canonical case indices by `floor(i*3670/15)` for `i=0,...,15`:

`0, 244, 489, 734, 978, 1223, 1468, 1712, 1957, 2202, 2446, 2691, 2936, 3180, 3425, 3670`.

This fixed spread replaces the earlier tentative first-sixteen proposal before any graph
pilot has run. It samples the full canonical ordering without using graph outcomes or
selecting easy cases.
It is not asserted representative enough to price the complete theorem by linear
extrapolation.

The sole mathematical enumeration input is the complete case-to-clause receipt:

- Original bytes: 24,888,016.
- Original SHA-256: `d7dd3ba492405d5b9a61dbd6a18a21164dc9c18b9b1b64d6d4633de6c9f40237`.
- Stored gzip SHA-256:
  `916f3c5692170312257d014126b6f64a4154648f0b474040ca7c771a97785808`.

Its exact source cases, edge counts, clause masks and path-origin binding are already
accepted finite evidence.
No contributor program or solver may be imported.
The reviewer has read the producer’s solver; the new implementation must disclose that
exposure and be written independently.

Verify the full raw receipt identity with a 64 KiB decompression stream before accepting
selected rows. Parse the cases with bounded incremental JSON decoding: maximum one case
at a time, maximum 1 MiB parser buffer, retain only the sixteen selected cases.
Check all 3,671 case indices are consecutive and unique and require the completed
receipt summary.
The source writer caps a single case at 256 KiB. Do not load the 24.9 MB
expanded receipt into an unrestricted object tree.

## Exact Enumeration Condition

For every selected case, enumerate every bit mask satisfying its complete retained
clause list. Bit one means horizontal separation.
A pair `(P,N)` is satisfied when `mask & P` or `(~mask) & N` is nonzero.
Reject bits outside the case’s declared edge count.
Keep the original clauses; introduce no subsumption or other optimization in the first
pilot.

Use deterministic depth-first branching on the lowest unset bit and fixed-point unit
propagation. Contradictory units or an unsatisfied empty clause close a branch.
If all clauses are satisfied, enumerate every assignment of the remaining free bits.

Document the finite induction: unit propagation preserves all completions; a conflict
has none; branching partitions completions into two disjoint values of one unset bit;
and satisfied clauses permit all free-bit completions.
Every emitted complete mask must independently satisfy every original clause.
Reject duplicate emissions.

Retain every selected case’s full model roster and counts, input row identity, edge
count, original clause identity, search nodes and timing.
A zero-model case is a completed result if its entire search was exhausted.
A cap or interrupted search is incomplete even if the count happens to match a producer
number. No count is prescribed for these sixteen cases.

## Controls Before the Pilot

Compare complete model sets, not only counts, against an independent direct truth table
on at most eight variables.
Freeze at least these three-variable formulas and expected counts with the eventual
checker:

| Formula | Models |
| --- | ---: |
| No clauses | 8 |
| x0 | 4 |
| not x0 | 4 |
| x0 and not x0 | 0 |
| Empty clause | 0 |
| x0 or x1 | 6 |
| (x0 or x1) and (not x0 or not x1) | 4 |
| x0 and not x1 | 2 |
| Duplicate copies of x0 or x1 | 6 |
| x0 and (x0 or x1) | 4 |
| (x0 or not x1) and (not x0 or x1) | 4 |
| x0 and (not x0 or x1) and (not x1 or x2) | 1 |

Add deliberate faults for reversed literal polarity, a skipped child, a duplicated
model, a mask outside the edge domain, and a forced tiny emission cap.
Each must be detected by the independent truth table or a declared refusal.
The exact fixture list and checker bytes must be frozen before execution; this plan does
not claim controls have passed.

## Measured Budget and Acceptance

Use one isolated project Python 3.14 worker under the coordinator’s serial memory guard.
Admission pressure must be 1; stop at pressure 2. Target under 20 seconds and 0.15 GiB
RSS. Hard ceilings: 60 supervised seconds, 55 internal seconds, 0.25 GiB owned process
tree, one million search nodes in total, 100,000 emitted models in total and 50,000 per
case. Raw output is capped at 16 MiB and compressed output at 4 MiB. All temporary
storage and evidence remain external.

The accepted case-to-clause run’s 7.199 supervised seconds measures a different
algorithm and is not a graph-search runtime estimate.
The pilot’s actual per-case node counts, elapsed times, model counts and memory will
price subsequent chunks.
If a cap fires, retain the exact incomplete case and choose a new bounded plan before
continuing.

Acceptance requires all sixteen selected cases complete, all controls passed, all
emitted masks satisfying the original clauses, no duplicates and guard/worker
completion. This supports only the pilot’s sixteen finite model sets.
It does not establish the complete 3,671-case graph roster, the source’s 273,584 graph
total, bank-rule applicability or Stage 4 acceptance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
