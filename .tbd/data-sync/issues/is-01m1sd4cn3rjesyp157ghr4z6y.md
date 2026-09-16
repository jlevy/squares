---
type: is
id: is-01m1sd4cn3rjesyp157ghr4z6y
title: "BC-214: split the CI surface -- PR tier under four minutes, deep validation its own workflow"
kind: task
status: closed
priority: 0
version: 4
labels: []
dependencies: []
created_at: 2026-09-05T18:26:13.282Z
updated_at: 2026-09-16T00:20:06.221Z
closed_at: 2026-09-16T00:20:06.219Z
close_reason: |
  Landed. The CI surface split shipped on 2026-09-05/06 in PRs #87 and #93: five concurrent pull-request jobs in .github/workflows/packing-validation.yml, deep validation in its own deferred workflow. The four-minute goal is superseded by OR-14's 120-150 s target and the 180 s budget packing/devtools/check_pr_wall.py enforces (think-z121); the current wall regression is tracked under think-xfqk.
resolution: null
duplicate_of: null
---

## Notes

PR 94 repair retrospectively stopped session-087 with partial efficiency results and selects BC-214 as the next handoff. PR 83 is merged; current PR checks cost 264.51 s in run 34018965403, above 150 s goal. Reconcile retained split and BC-215/BC-217 dispositions before another prospective efficiency phase; no efficiency campaign executed in this repair.


2026-09-15 (think-xfqk, think-z121): closing as landed. BC-214's CI surface split shipped on 2026-09-05/06 in PRs #87 and #93. The pull-request tier is now `--checks`, `--frontend`, `--geometry`, `--suite` and `--sweeps` running as five concurrent jobs in `.github/workflows/packing-validation.yml` with `packing-required` waiting on all five, and deep validation moved to its own deferred workflow. The four-minute goal in the title is superseded by OR-14's 120-150 s and the 180 s budget `packing/devtools/check_pr_wall.py` now enforces on every pull request; the standing regression -- 154 s median on 2026-09-06 against 288 s across 21 runs on 2026-09-15 -- is tracked under think-xfqk, not here.
