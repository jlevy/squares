---
softschema:
  contract: squares.math-startup.hypothesis.v1
  schema: ../schemas/hypothesis.schema.yaml
  status: enforced
id: H-002
title: Prepared math and fewer startup dependencies reveal parameters sooner
derived_from: [X-001]
registered: "2026-09-08T16:09:33Z"
widths: [1280, 390]
metric: parameters_ready_ms
criterion: paired_latency
minimum_pairs: 12
maximum_ci95_change_pct: -10
---
# Prepared Math and Fewer Startup Dependencies Reveal Parameters Sooner

The combined change prepares initial math, waits only for the faces an expression uses,
reveals expressions independently, and schedules parameter values before heat maps.
It reduces normal first-visible parameter latency by at least ten percent on the fixed
local-file Chromium regime at both declared widths.

Use twelve interleaved control/candidate pairs per width.
Compute each pair’s relative change, then the median and a deterministic 2,000-resample
percentile bootstrap interval with seed `0x5EED`. The entire 95% interval must be at or
below minus ten percent at both widths.
Report each arm’s median and min–max range alongside the paired result.
Refuse invalid samples; never replace a failed run silently.

All correctness checks must pass before acceptance.
A result describes the combined change on this host and cache regime; it does not
allocate savings among individual changes or promise the same latency on a remote
network. The criterion was registered before any candidate run, without tuning to
candidate measurements.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
