---
type: is
id: is-01m1vs0edeyqrwptpsptt58v5g
title: "W5: measure and optimize the exhaustive checkpoint with bounded workers"
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T16:32:15.789Z
updated_at: 2026-09-06T20:41:54.762Z
closed_at: 2026-09-06T20:41:54.761Z
close_reason: Completed bounded worker allocation and source-bound exhaustive profiling in PR98, with all 55 final cases and timing records verified. No causal whole-CI speedup claim. Scheduling, dependency selection/reuse and n=40 duplicate work continue under think-xejq; post-merge CI remains tracked under think-rwte.
resolution: null
duplicate_of: null
---

## Notes

Bounded profiling/allocation first slice is complete in merged PR98. The isolated exhaustive job uses one outer worker and up to four inner workers under actual CPU and memory limits; concurrent jobs retain their two-by-two budget. Worker and workflow contract tests passed.

Two old-base observations retained the same 55 case identities: run 34050662740 at fb1a987d/edccf294 used two inner workers and took 26m56s job / 1598.45s pytest; run 34052836364 at bc65e779/edccf294 used four and took 20m56s / 1234.35s. Serial n=40 also changed from 236.30s to 169.59s, so the six-minute difference is descriptive, not a causal worker-speedup estimate.

The final PR checkpoint 34056585319 at b3b7275f/c14451f5 passed all 55 unchanged case identities with complete 165 phase records, source and receipt joins, four actual CPUs, and one outer/four inner workers. Job time was 21m14s; pytest 1251.16s; command 1252.129337s; step 1252.130959s. Dominant cases were n=40 round trip 192.639s, retained witnesses 168.094s, and n=12 interval verification 84.473s. Artifact: https://github.com/jlevy/squares/actions/runs/34056585319/artifacts/9996467997.

Disposition: finish this bounded measurement/allocation slice; continue scheduling, n=40 duplicate elimination and dependency-based selection/reuse under think-xejq. The separately combined landed main 8743cb0d includes PR100 and still awaits main run 34057826143, tracked under think-rwte.
