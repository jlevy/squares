---
type: is
id: is-01m2chg0twsn4zvjg2jrxbztfp
title: "PR156: bind source bytes despite Git index flags"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2cgrxpkq2g6jryfp8sa74as
created_at: 2026-09-13T04:48:02.905Z
updated_at: 2026-09-13T04:55:02.459Z
closed_at: 2026-09-13T04:55:02.459Z
close_reason: Runner repair committed421c3445;128focused tests passed,Ruff andBasedPyrightclean. Independent AstraMax second review accepted all four fixes and reran11 final regressions. Full-stack integration remains open.
resolution: null
duplicate_of: null
---
Independent runner review found assume-unchanged/skip-worktree can hide loaded implementation drift. Require direct frozen Git-blob comparison and regression coverage.
