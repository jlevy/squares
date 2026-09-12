---
type: is
id: is-01m28vqwvnktgxa2k44bftwdam
title: Keep geometry exposure evidence within one controlled observation
kind: bug
status: in_progress
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-11T18:30:09.012Z
updated_at: 2026-09-12T08:56:10.525Z
closed_at: 2026-09-11T18:30:15.242Z
close_reason: Fixed in 15959d44; recorded as D-491
resolution: null
duplicate_of: null
---
The geometry probe previously combined visibility from its later before snapshot with readiness exemptions from an earlier observation. That mixed two states and made the exposure verdict internally inconsistent. The retained WebKit artifact also shows that artificial pre-release work lasted beyond the independent three-second page watchdog: early_visible was empty, the first KPress call arrived at 5339 ms, and 18 boxes were visible later. Their reservation boxes did not move, but their intrinsic glyph widths changed by as much as 20.875 px. Integrate the same-observation exposed_early predicate with a probe-only watchdog pause and live assertion. Preserve the separate queue-watchdog product control. Record the historical causal limit: the artifact supports this timing mechanism but does not timestamp watchdog expiry or prove it was the sole historical cause.

## Notes

Reopened during PR149 reconciliation because the original closed description attributed visibility to carrier CSS, which changes font family but not visibility. Child implementation bead think-6ogd owns the combined correction and fresh validation.
