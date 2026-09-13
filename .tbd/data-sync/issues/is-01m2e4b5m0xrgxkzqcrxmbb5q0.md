---
type: is
id: is-01m2e4b5m0xrgxkzqcrxmbb5q0
title: Wire BC329 run sheet to the maintained run-set verifier
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2b884n0ms50xp93q6aaps1g
created_at: 2026-09-13T19:36:41.343Z
updated_at: 2026-09-13T19:36:41.343Z
---
Independent integrated-head review at PR156 source fbd915fc found the draft run sheet still invokes the reader directly and hand-copies evidence; it never calls the maintained verifier snapshot/read/join/retain/source-closure entry points. Wire the frozen target-free sheet to the accepted verifier blobs, preserve exact argv/status/proof copies, 22-file coordinator root and status inventory, source and candidate-index checks, and later evidence-commit OID check. Run Bash parse and synthetic operational controls, then independent rereview on one clean head. Do not execute positive calibration or BC329 until every gate accepts.
