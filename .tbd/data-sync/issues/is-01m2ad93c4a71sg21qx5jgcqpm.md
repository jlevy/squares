---
type: is
id: is-01m2ad93c4a71sg21qx5jgcqpm
title: Combine PR149 geometry-probe fixes and correct D-491 evidence
kind: bug
status: closed
priority: 1
version: 4
delegate: root integration lane
labels: []
dependencies:
  - type: blocks
    target: is-01m2ad9avdatjwfznq7zwqjget
parent_id: is-01m26rygs7f0s76v147x0px4cd
created_at: 2026-09-12T08:55:52.963Z
updated_at: 2026-09-12T09:06:55.806Z
closed_at: 2026-09-12T09:06:55.805Z
close_reason: Combined author and local probe repairs at 7acbc809; focused, records, and live Chromium controls pass. Exact-head publication validation continues in dependent bead think-o96l.
resolution: null
duplicate_of: null
---
Integrate the author branch same-observation exposure predicate with the local root-watchdog pause and live-hook assertion. Preserve both regression sets and the independent queue-watchdog control. Rewrite D-491 and related code, test, PR, and bead language around the two demonstrated instrumentation defects: evidence drawn from different observations, and an artificial setup delay that can consume the page watchdog. Do not claim the carrier substitution reveals boxes or that unchanged reservation boxes prove final glyph metrics. Validate the combined revision from a fresh head.

## Notes

Combined at merge commit 7acbc809. The implementation keeps exposed_early and early_ready on one observation, pauses and records the root watchdog only in the artificial geometry probe, fails closed when the live hook is absent, and retains the separate real-expiry queue control. D-491 now records the retained WebKit timings, the 20.875 px intrinsic-width change, and the historical causal limit. Evidence: 17 focused tests, Ruff, BasedPyright, generated views, synopsis, schema and records gates, plus a live Chromium replay with 13 held font requests, 450 targets, 369 bases and no findings.
