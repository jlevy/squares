---
type: is
id: is-01m212vnnwz9d60e7yhsahx8qe
title: Measure parameter startup without pre-paint anchor overhead
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T18:00:37.307Z
updated_at: 2026-09-08T20:34:14.067Z
---
Exp004 met its numeric timing threshold but full-page anchor sampling cost differs by94–99ms and samples font-blocked prepaint geometry. A separate parameters mode preserves all14correct-visible checks with no all-page ranges. H003 repeats12pairs perwidth and requires recorded sampler overhead≤10%in eacharm. Fresh hosted runner required because unrelated Mac work was later found consuming CPU.
