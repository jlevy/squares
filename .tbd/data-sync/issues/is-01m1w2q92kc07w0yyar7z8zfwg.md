---
type: is
id: is-01m1w2q92kc07w0yyar7z8zfwg
title: Restore scalar readiness after fractional depth corrections
kind: task
status: open
priority: 0
version: 1
spec_path: packing/campaign/hypotheses/H-093-n11-scalar-61-16-certificate.md
labels: []
dependencies: []
parent_id: is-01m1vvtvrvn3h40brmksg8jvyh
created_at: 2026-09-06T19:22:01.170Z
updated_at: 2026-09-06T19:22:01.170Z
---
BC251/H093 may launch once only after its cutting and ceiling decision path is sound and fresh seed/bridge controls pass. PR100 at237d9386 reports exact false-depth regressions in those paths and supplies corrections; read it as evidence, do not import the open head. Integrate only landed origin/main, run the relevant counterexample/control checks, then restore instrument_ready and freeze the new experiment before starting the unchanged150-minute scalar recipe in an isolated checkout. No time or failed guard is an H093 verdict; other research lanes proceed independently.
