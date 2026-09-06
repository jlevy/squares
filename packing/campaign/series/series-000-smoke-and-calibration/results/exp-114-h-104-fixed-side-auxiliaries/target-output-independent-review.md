# exp-114: Independent Target-Output Review

Disposition: **accept H-104 at its declared exact-angle auxiliary scope.** The single
independent file replay returned exit 0 and `decision: accepted`. The producer completed
all seven clauses at $q=1939/500$, with no unchecked clauses or returned obstructions.
[The replay](replay.json) leaves H-036 unresolved and explicitly disclaims a standalone
exhaustive certificate.

This is `think-jhs4`, W7 correctness, commissioned for 2026-09-06, 21:29:48–21:40:00
UTC. The coordinator accepted the
[source-only cold review](../agenda-026/bc-255-independent-reader-cold-review.md) and
opened the unused producer and replay allowances through the
[prospective exp-114 record](../../experiments/exp-114-h-104-fixed-side-auxiliaries.md).
The side, point formulas, seven-clause criterion, target count, and two separate
ten-second process caps were unchanged.

## Exact Input and Receipt Check

The reviewer used the coordinator-supplied frozen reader checkout `2153cb02` at
`/private/tmp/squares-h104-replay.cE1O1o/packing`. The coordinator dispatched the
retained [packet](packet.json), attesting one producer run from clean `e45c8a63` and its
actual exit code 0. The reader does not attest Git state or process history; those are
the coordinator’s recorded provenance responsibilities.

The independent reader bound the exact side and both point sets to its separate formula
transcription, including ten distinct points, the ordered twelve points, and their
first-three A labels.
It checked the completed angle order `0,45`, all seven Boolean outcomes, the
checked/unchecked inventories, the absence of failed clauses and witnesses, and
consistency with the supplied producer exit status.
The packet retains `perturbed_angles_evaluated: false` and `theorem_acceptance: false`.

The seven positive clauses are axis ten-cover, axis twelve-cover, 45-degree
localization, the three separate A-point forcing clauses in the canonical region, and
45-degree twelve-cover.
Closed-unit boundary placements and the four $K_4$ reflections retain the reviewed
algorithm’s semantics.
The packet reports event-product strata by dimensions 0, 1, and 2 as `[280, 526, 247]`
at 0° and `[668, 1397, 728]` at 45°. It reports six 45-degree ten-set-avoiding strata,
one in the canonical region.
These counts are diagnostics, not independent evidence of exhaustive coverage.

## Single Replay and Cost

The only replay started and completed within the observed clock second **21:35:35 UTC**.
It ran from the frozen reader’s `packing/` directory:

```bash
/usr/bin/time -p env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_restricted_orientation_discriminator /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-114-h-104-fixed-side-auxiliaries/packet.json --target-fixed-side --producer-exit-code 0
```

The fixed ten-second reader alarm did not fire.
Its stdout is retained verbatim in [replay.json](replay.json); it emitted no diagnostic
stderr. The standard process timer’s stderr is retained verbatim in
[replay.log](replay.log): **0.05 seconds wall, 0.04 seconds user, and 0.01 seconds
system**, or 0.05 seconds CPU. These are one-run costs at the timer’s displayed
precision, not a performance comparison or agent-time total.

For context, the separately owned [producer log](run.log) reports 2.41 seconds wall and
2.37 seconds CPU. The packet reports 2.280253915931098 seconds worker wall and 2.249838
seconds worker CPU. The reviewer did not repeat the producer or spend a second replay
allowance.

## Assurance and Next-Step Limit

This is computational verification of the seven fixed-formula, exact-angle auxiliaries
in [H-104](../../../../hypotheses/H-104-fixed-side-point-cover-auxiliaries.md).
Positive assurance combines the reviewed exhaustive center-stratum algorithm, its
recorded successful execution, and the independent exact input/receipt checks.
The reader imports neither producer geometry nor the producer’s exact-field
implementation, but it does not independently enumerate the target strata.
No negative witness needed replay because the producer returned none.

Acceptance permits pricing the continuous-angle extension; it does not commission that
work. No nearby angle, packing counterexample, full restricted-family theorem, or global
lower bound was established.
H-036’s original side threshold and quarter-degree neighborhoods are unchanged and
unresolved.

Only `replay.json`, `replay.log`, and this report were written.
No source, registry, shared view, bead, or Git state was changed.
Experiment-loop governed the frozen criterion and one-shot accounting; tbd review
guidance kept receipt checks separate from execution provenance.
Practical Prose and Flowmark guided the report.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
