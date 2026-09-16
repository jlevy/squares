---
type: is
id: is-01m2mpez5qemp0vvh47wfbdq7p
title: "PR #180 hosted Motion Lab paint restoration is nondeterministic"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6y4gw224dgrwf37bgqnhd
created_at: 2026-09-16T08:48:46.769Z
updated_at: 2026-09-16T09:07:02.928Z
closed_at: 2026-09-16T09:07:02.927Z
close_reason: "Fixed at local commit d7c07bf7 on integrated head 3a9bb2f6: the Motion Lab checker now decodes PNGs to RGB int16, counts material pixel changes with explicit channel/paint/restoration boundaries, fails closed on dimension mismatch, and reports pixel counts. Tests cover alternate PNG encodings, exact delta 8/9 and 256/257 boundaries, zero-change mutants, and shape mismatch. Ten repeated installed-Chrome checks passed both pages and both live mutants; focused 100, browser floor, Ruff/Rust, BasedPyright, lock check, and independent senior review are green. Hosted Linux exact-head rerun remains publication verification."
resolution: null
duplicate_of: null
---
Hosted exact-head frontend run 35075455272 job 104726691290 fails only because the exact Motion Lab positive paint fixture compares restored PNG bytes for exact equality. Diagnose Linux Chromium screenshot nondeterminism and replace raw byte equality with a quantified, bounded pixel/stability invariant that preserves opacity-zero and transparent-paint negative-control sensitivity. Validate with repeated real Chrome/Playwright runs, focused tests, and the browser floor.
