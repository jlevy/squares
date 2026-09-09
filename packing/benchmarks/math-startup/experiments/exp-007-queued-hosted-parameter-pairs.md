---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-007
title: Queued startup passes the timing rule but fails correctness
kind: comparison
hypotheses: [H-005]
measurements:
  - runs/ci-34274946315/startup-1280.json.gz
  - runs/ci-34274946315/startup-390.json.gz
correctness: failed
judgment: Both registered widths pass the numerical improvement and sampler bounds, but the same candidate fails print geometry and WebKit first-exposure checks. Preserve the valid timing result separately from failed correctness; the repair requires a newly registered comparison.
---
# Queued Startup Passes the Timing Rule but Fails Correctness

[Pages dispatch 34274946315](https://github.com/jlevy/squares/actions/runs/34274946315)
tested clean source `d122d19cffb1b59c86ce57a02838f0c70438e978` on the dedicated Linux
runner.
The [candidate HTML](../fixtures/candidate-d122d19c.html.gz) is byte-identical to
the prepared-page artifact consumed by the correctness jobs.
The downloaded control matches the decompressed frozen `33cd4760` fixture exactly.
The retained [controls](../runs/ci-34274946315/controls.json.gz) pass, including
rejection of missing math, wrong active variants, missing instrumentation and targets
added after sampling.

Each width contains exactly twelve complete pairs, with arm order alternating by pair.
All forty-eight observations retain fourteen correct, exposed parameters, no measurement
findings and the registered parameter-only mode.
Chromium 151.0.7922.34 runs in a fresh process and context for every load;
operating-system caches remain uncontrolled.
Both bootstrap intervals satisfy the unchanged minus-ten-percent rule, and all four
arm/width sampler fractions remain below two percent.

This does not establish correctness of the candidate.
The independent geometry experiment, exp-008, preserves three failing print settings and
missing WebKit coverage.
The [WebKit failure log](../runs/ci-34274946315/pages-webkit-failed.log.gz) records math
exposed before font readiness.
No observations are replaced, and no extra pairs are added.
The next repaired candidate belongs to H-006, registered before its dispatch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
