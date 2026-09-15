---
type: is
id: is-01m2heywfbtnapjrvzgya42m66
title: "PR #160 review D53: the ascent's Open phase does nothing"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:56.392Z
updated_at: 2026-09-15T02:40:56.016Z
closed_at: 2026-09-15T02:40:56.015Z
close_reason: "Fixed on #160 at e90187c8: the no-op Open phase is removed and the settle declares the record side; a test requires no phase to be one repeated picture."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

The ascent's Open phase did nothing: a `container` phase at factor 1.0 of the new side for 18 identical frames. The identity swap at the end was fixed in #160.

Source: #125 F18 (Open item). Related: think-cttv.

Files: `packages/workbench/tools/workbench_tools/ascent.py:54-59`.
