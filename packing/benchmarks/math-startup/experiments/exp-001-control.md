---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-001
title: Frozen deployed page on the normal startup instrument
kind: baseline
hypotheses: [H-001, H-002]
measurements:
  - runs/control-desktop.json.gz
  - runs/control-mobile.json.gz
correctness: passed
judgment: The control is valid for the fixed local-file regime; its large absolute movement includes figures inserted after the first readable frame.
---
# Frozen Deployed Page on the Normal Startup Instrument

The six fresh Chromium navigations ran sequentially after all three delegates confirmed
their browsers and heavy checks were idle.
Each viewport has three valid observations.
The reports record the instrument commit, actual command, environment, source identity,
target completeness, timing, text anchors, and observer overhead.
The raw JSON is losslessly compressed with `gzip -n`; decompression restores the probe’s
original output.

This establishes the control distribution, not a speedup.
Local-file latency excludes network transfer and is therefore not directly comparable to
the earlier live-site first-any-math diagnostics.
The report’s all-parameter metric is also stricter than first-any-math.

Absolute movement includes the source-discovered figure insertion tracked as
`think-tpsi`. Local anchor displacement records reflow inside each containing block; it
can include prose-font changes as well as mathematics.
The independent prepared-box guard will determine whether math itself retains its
geometry while fonts are pending.

Before candidate timing, the instrument’s eligibility check was corrected to allow a
host that never calls the optional `ready()` warmup.
A new no-warmup fixture proves that path; observed render or hydration activity is still
required. Sampling, clocks, and the numerical baseline are unchanged.
These original receipts retain their original instrument revision.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
