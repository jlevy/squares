---
type: is
id: is-01m5cm2y1myb3jwdvqjp1gt5af
title: "Added-blob guard: run on PR retarget (edited) and on pushes to main; main has no branch protection"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m5c0ftybryt8q817fj95axz8
created_at: 2026-10-20T12:20:25.266Z
updated_at: 2026-10-20T12:20:25.266Z
---
Review H of #406, finding H5 (Low), deferred: packing-validation.yml:14 and :74. Retargeting a PR (pull_request 'edited' with a base change) does not rerun the added-blob guard, a push to main never runs it, and main has no branch protection or rulesets. Not reproduced on GitHub. Decide the event set and whether the guard should be a required check.
