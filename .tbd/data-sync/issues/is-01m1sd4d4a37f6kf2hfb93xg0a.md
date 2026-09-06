---
type: is
id: is-01m1sd4d4a37f6kf2hfb93xg0a
title: "BC-215: stop re-running expensive gate work whose inputs have not changed"
kind: task
status: open
priority: 0
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:26:13.770Z
updated_at: 2026-09-06T17:06:53.297Z
---

## Notes

W5 validation-efficiency review identified a concrete duplicate: exhaustive test_the_record_round_trips and the named n=40 assessor --check both recompute assess() and compare the full retained dict. Keep both until a follow-up explicitly moves this contract to the named full-gate step, adds cheap CLI equality/drift/missing/read-only checks, and tests aggregate coverage. No cached-result reuse is introduced by the current block. See docs/project/reviews/review-2026-09-06-validation-efficiency-implementation.md and think-i2gk for the exhaustive profile and scheduling follow-up.
