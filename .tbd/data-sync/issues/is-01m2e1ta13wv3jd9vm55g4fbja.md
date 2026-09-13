---
type: is
id: is-01m2e1ta13wv3jd9vm55g4fbja
title: "Run-set verifier: report oversized JSON integer as refusal code 2"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2b884n0ms50xp93q6aaps1g
created_at: 2026-09-13T18:52:31.651Z
updated_at: 2026-09-13T18:52:31.651Z
---
Exact-head verifier review at 878e18d0 found a 5000-digit JSON integer raises uncaught ValueError rather than the declared refusal code 2. Add a bounded parse or catch with a focused mutation control.
