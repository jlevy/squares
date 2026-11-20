---
type: is
id: is-01m7xkabvzsbkx3b33hj63ny9h
title: Audit F-2 after the frozen R1 rectangle-kernel review
kind: task
status: closed
priority: 2
version: 3
delegate: codex-intake-1119-01a1fb
labels: []
dependencies: []
parent_id: is-01m7x1bwanac148b7py63cahyx
hold: null
hold_until: null
created_at: 2026-11-20T23:05:29.214Z
updated_at: 2026-11-20T23:06:04.938Z
started_at: 2026-11-20T23:05:36.607Z
closed_at: 2026-11-20T23:06:04.936Z
close_reason: Verified F-2 source control flow at the pinned commit after the findings freeze. The full R1 review remains on think-dhjz.
resolution: null
duplicate_of: null
---
Read-only continuation of think-dhjz. A fresh reviewer audited the F-2 source obligation after verifying the R1 findings freeze at cf1ee8f713 (20 November 2026 at 21:20:28Z, SHA-256 dbe6ffb115a853b2a98971ceec90a1eb70a0e3d0bb1178fd7b59de704959e6e2). This was a handover of the post-freeze audit. The reviewer received only R1's freeze context and used the pinned source as text. No R2 materials, current frontier records or author programs were read or executed beyond that source-text scope.

At JoostdeWinter/square-packing 21d944c43098e2261ab7d713cd10f02a5eb13f3d, lower_bounds_2026_11_19/proof/octagon.cpp:111–115 skips a rectangle before any of four corner accumulators change if any of its corner masses is zero or less. gram.cpp:100–105 skips all diagonal and cross contributions for that rectangle in any triangle with a zero corner. gram.cpp:143–147 accumulates the four triangles separately, and :149–154 only accepts both triangles in one box-covering diagonal pair. One zero corner can leave a rectangle on the opposite triangle, where all three corner masses are positive. The independently checked conclusion is that F-2 holds per interpolation cell. gram.cpp:29–37 separately tests enclosure across the whole centre box before adding full mass. check.py:32 dispatches octagon and octagon-gram to those two kernels.

This closes the source-level F-2 audit conditional on valid corner masses and arithmetic. Keep the rest of R1 open for the other proof obligations, replay provenance, receipt linkage and the final mapped report. The audit supplies no executed-binary evidence and certifies no additional directions.
