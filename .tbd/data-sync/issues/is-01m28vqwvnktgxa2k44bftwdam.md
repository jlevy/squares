---
type: is
id: is-01m28vqwvnktgxa2k44bftwdam
title: Keep geometry exposure evidence within one controlled observation
kind: bug
status: closed
priority: 2
version: 5
labels: []
dependencies: []
created_at: 2026-09-11T18:30:09.012Z
updated_at: 2026-09-12T10:07:50.389Z
closed_at: 2026-09-12T10:07:50.388Z
close_reason: Published and independently reviewed the same-observation exposure rule and probe-only root-watchdog pause at 237c4023, preserved the independent queue-watchdog control, corrected D-491's causal scope, and obtained focused live plus exact-head Firefox/WebKit and hosted validation.
resolution: null
duplicate_of: null
---
The geometry probe previously combined visibility from its later before snapshot with readiness exemptions from an earlier observation. That mixed two states and made the exposure verdict internally inconsistent. The retained WebKit artifact also shows that artificial pre-release work lasted beyond the independent three-second page watchdog: early_visible was empty, the first KPress call arrived at 5339 ms, and 18 boxes were visible later. Their reservation boxes did not move, but their intrinsic glyph widths changed by as much as 20.875 px. Integrate the same-observation exposed_early predicate with a probe-only watchdog pause and live assertion. Preserve the separate queue-watchdog product control. Record the historical causal limit: the artifact supports this timing mechanism but does not timestamp watchdog expiry or prove it was the sole historical cause.

## Notes

Combined fix is published at PR149 head 237c4023. The exposure verdict uses exposed_early and early_ready from one observation; the geometry probe pauses and records only its artificial root-watchdog timer; the independent queue-watchdog product control retains the real timer and rejects its broken-queue mutation. Seventeen focused geometry tests, an exact live Chromium run with root_watchdog_paused true and zero findings, and exact-head hosted Firefox/WebKit, geometry, page build and packing validation all pass. D-491 states that the retained WebKit timing supports the mechanism but does not timestamp watchdog expiry or prove a sole historical cause.
