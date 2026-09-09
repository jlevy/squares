---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-009
title: Protected queued startup passes the registered timing rule
kind: comparison
hypotheses: [H-006]
measurements:
  - runs/ci-34283695063/startup-1280.json.gz
  - runs/ci-34283695063/startup-390.json.gz
correctness: passed
judgment: Both widths satisfy the fixed paired improvement and sampler bounds, and the same publication passes the complete geometry and rendering checks. Retain the combined repair; the observations establish its improvement over the frozen control without attributing the effect to one edit or certifying later integration changes.
---
# Protected Queued Startup Passes the Registered Timing Rule

[Pages dispatch 34283695063](https://github.com/jlevy/squares/actions/runs/34283695063)
tested clean source `dab2a3818f661311b130ca2f2360ffad5627db65` on its dedicated Linux
timing runner, after H-006 was registered.
The [candidate HTML](../fixtures/candidate-dab2a381.gz) preserves the exact measured
input and equals the prepared-page artifact used by the correctness jobs byte for byte.
The downloaded control equals the decompressed frozen
[`33cd4760` fixture](../fixtures/control-33cd4760.html.gz) byte for byte.
The [instrument controls](../runs/ci-34283695063/controls.json.gz) pass their positive
cases and reject missing math, the wrong active variant, missing instrumentation, and a
target added after sampling.

Each width has exactly twelve complete pairs, with arm order alternating by pair.
All forty-eight observations retain fourteen correct, exposed parameters and no validity
findings.
The instrument uses its registered parameter-only mode, Chromium 151.0.7922.34,
and a fresh browser process and context for every load.
Operating-system caches remain uncontrolled.
The
[generated ledger](../ledger.md#exp-009-protected-queued-startup-passes-the-registered-timing-rule)
derives the medians, ranges, paired changes, and fixed bootstrap intervals from the raw
reports.
Both intervals remain below minus ten percent; each arm’s median sampler cost is
below two percent of its median primary latency, within the registered ten-percent
bound. No pairs are added or replaced.

The complete H-004 result is retained in
[exp-010](exp-010-protected-hosted-font-geometry.md).
The [workflow receipt](../runs/ci-34283695063/pages-run.json.gz) and
[build log](../runs/ci-34283695063/pages-build.log.gz) establish that the same source
passed font exposure, early input, fallback, queue recovery, contextual typography,
reload, print layout, and PDF reproduction checks.
The workflow was dispatched for validation; its deploy job was skipped.
The [timing log](../runs/ci-34283695063/pages-timing.log.gz) preserves the executed
commands and their completion.

This result concerns the combined publication frozen at `dab2a381`, including its
loading, geometry, typography, and scrolling corrections.
It is not a causal estimate for any individual change.
The later integration of main’s Planetaire Mono adoption requires separate publication
correctness checks; it does not change this experiment’s input or verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
