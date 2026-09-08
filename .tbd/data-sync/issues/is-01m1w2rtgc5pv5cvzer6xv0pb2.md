---
type: is
id: is-01m1w2rtgc5pv5cvzer6xv0pb2
title: "W5: reduce T-022 replay cost on the PR fast path"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T19:22:51.787Z
updated_at: 2026-09-06T19:22:51.787Z
---
Current-base PR98 run34054383672 passed but took3m03, above the W5 investigation threshold and2–2.5minute target. Artifact9995547704 attributes52.133s to the newly landed serial dilation_corollary T-022 replay; exact verification was the last step to finish at90.230s versus50.929s on the priorbase. Validate job173s versus119s is a descriptive comparison, not causal: remaining exact subcommands and setup varied. Profile redundant immutable certificate work and scheduling before changing coverage. Preserve complete Conditions1–5 replay, record equivalence, actual changed-contract regressions and failure propagation. Measure interleaved runs under the W5 plan criterion; do not defer this check or claim a percentage speedup from one hosted observation. Evidence /tmp/pr98-newbase-fast-artifact-audit.json and PR98 validation record.
