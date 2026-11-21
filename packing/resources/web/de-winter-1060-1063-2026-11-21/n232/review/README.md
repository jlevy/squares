# Review of Issue 1062: Rational Feasibility at 232 Squares

**Finite feasibility passes.** The independent exact check verified 232 unit squares
inside the closed square `[0,S] × [0,S]`, with disjoint interiors, for the submitted
rational side.
Its upward rounding to 12 decimal places is **15.759531623541**. All 3,712
vertex-wall inequalities and 26,796 unordered pairs passed.
There are four wall equalities and one actual pair contact, `(123,124)` with zero-based
indices. The predeclared equality and inward/outward controls passed.
The [single mathematical receipt](results/independent-feasibility.json) holds the exact
side, contact margins, control values, and counts.

The source, implementation, and controls were frozen before execution at
`2026-11-21T18:31:30Z`. The initial run took 3.980607375 seconds under Python 3.14.7,
with worker and observe-only memory-guard exits 0. The portable replay took 1.297996708
seconds and reproduced every mathematical field.
The immutable [frozen source](frozen/verify.py.txt) and
[freeze record](frozen/freeze.json) preserve that review boundary.
The runnable [portable verifier](tools/verify.py.txt) changes input handling, annotations,
logging and formatting, while preserving the geometry and controls.
The independently written proof uses rational vertices and separating axes; no producer
or project geometry code, prior validator result, or other reviewer judgment informed
it. The assigned issue snapshot did include its owner comment about earlier side
comparisons, which did not determine feasibility.

## First-Contact Comparison and Credit

The coordinator supplied the exact
[Option D comparison](results/option-d-comparison.json) after freeze.
It compares the submitted side with each earlier rational certificate uniformly
contracted at fixed orientations until first contact, translated and reboxed:

| Earlier rational certificate | First-contact side minus submitted side |
| --- | ---: |
| T-307 | Approximately `4.00173175448769e-9` |
| JoeGun’s earlier rational recorded certificate | Approximately `2.0087986080703956e-34` |

Both differences are positive as exact fractions.
The JoeGun comparison is to his **earlier rational recorded certificate at first
contact**. It establishes no ordering against an unrounded optimal or local limit.
The independent finite check establishes no priority, local minimality, or global
minimality. Retain the prior Kodaj–JoeGun layout and local-solve credits when recording
Joost de Winter’s rational certificate.

The maintained `devtools.measure_identity` comparison to both certificates completed in
1.847264125 seconds under one observe-only guard and a 120-second ceiling, exit 0.
Neither comparison found a one-to-one nearest-center match under any box symmetry.
The best centered assignment had symmetry 0, largest move and bottleneck `0.76216`, and
RMS move `0.152247` for both; 27 squares moved more than `0.1` and 29 turned more than
one degree. [Pose measurements](results/pose-identity.json) support these limited
statements; similar side values alone do not establish pose identity or priority.

Two maintained Fraction routes timed out without a result after 300 wall seconds in the
coordinator’s run; those timeouts are not mathematical verdicts.
Source audit found that `sqpack.witness.exact_verify` performs unbucketed verification
followed by an exhaustive margin pass, while
`check_rational_witness_independent.check_squares` projects every pair.
`prepared_verify_packing` caches projections for the reference predicates and remains an
all-pair route by default; it is not another independent implementation.
The audit gave no measured basis for another exact run below 120 seconds, so no further
heavy route was run.

## Source and Replay

The [source acquisition record](source/acquisition.json) identifies the official
[issue](https://github.com/jlevy/squares/issues/1062), original
[archive](https://github.com/user-attachments/files/35205219/n232-rational.zip), and its
SHA256 `752b5efc0aaedfab63605b8c2f3112610a41164bfc31d843b629752cda4088c3`. The
coordinator supplied the archive; the reviewer checked its hash.
Only the two original factual gzip members are included.
No producer program is included or run.
The [predeclared controls](controls.md) explain the exact acceptance boundary.

From this directory, with Python 3.14.7 selected as `python`, run:

```bash
python -I -B tools/verify.py.txt source/232 replay.json
```

Use an external-volume scratch output in the host workflow.
`tools/identity.py.txt` is optional post-freeze tooling requiring the project’s existing
environment:

```bash
python -I -B tools/identity.py.txt REPOSITORY source/232/candidate.json.gz identity.json
```

[Validation metadata](results/validation.json) records replay agreement and lint/type
checks. Full historical launch scripts and telemetry remain in external evidence; the
portable overlay contains no absolute internal paths.
This reviewer performed no network publication, remote-service write, checkout edit, PR
action, or tracker change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
