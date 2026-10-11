---
type: is
id: is-01m4d97gn20a9nddee9p1ka2sz
title: Profile and shorten eight quick-lane calls measured above the 12s wall
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-10-08T08:14:13.665Z
updated_at: 2026-10-08T08:14:13.665Z
---
PR410 integration run37743244050 at98f476dd/base7a8d9c16 took1906.79s; all shard assertions passed but eight quick calls measured12.19–27.03s against hard12s. Seven also exceeded12s on same-tree PR run37743213463 under declared advisory45s hang policy, and six PR readings were slower than full; topology alone is not demonstrated cause. Preserve full FAIL and paired durations at attic/n17-six-hour-engineering/pr410-integration/ci-fast-98-paired-test-durations.json and run URL https://github.com/jlevy/squares/actions/runs/37743244050. Profile actual repeated verifier/build work before optimizing. Do not raise ceilings, remove checks, or mark slow without matched measured-registry evidence. Behavioral-only worker reservation max(1, available_cpus/inner_jobs) is a source-based candidate, preserving explicit PACK_JOBS, but not established cure. Use documented fast plus deep complement for current proof-work iteration; this optimization debt stays open.
