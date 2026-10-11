---
type: is
id: is-01m3p6krj8zr6a0956x7de4xfv
title: Investigate unchanged frontend timing drift on PR 246
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
created_at: 2026-09-29T09:05:57.319Z
updated_at: 2026-09-29T15:40:36.788Z
closed_at: 2026-09-29T15:40:36.776Z
close_reason: "Resolved by c621b845f: bounded browser concurrency preserves all eight checks and unchanged thresholds. Same-host serial/two-worker comparison 67.331s/49.606s; 135 focused tests passed across runs; independent concurrency review found no blocker. Hosted frontend run 36590984972 passed in 101.68s. Required packing and certificate-page CI passed, and the hosted Git tree matches the pushed source."
resolution: null
duplicate_of: null
---
Hosted run36546217991 at45eaf8e75 passed all three frontend functional steps, but the tier took134.86s against recorded85.25s:1.58x exceeds the1.5x regression threshold while remaining below the150s absolute ceiling. Workbench browser behavior took134.85s; browser floor54.34s; liveness24.61s. The preceding run36544631396 passed frontend, and the intervening commit changed only the document scanner, its test and review prose. Preserve this failure and measure workload/runner variance before changing budgets or adding retries. This is separate from the inherited Session161 record blocker; all final-head functional checks passed.

## Notes

Hosted36546217991 vs36544631396: same frontend source, workbench117.829s vs79.287s and liveness24.613s vs15.208s; independent tsc commands similarly slower, indicating whole-runner variance. Eight isolated browser owners were serial. Same-host bounded2worker candidate49.606s versus serial67.331s (-26.3%), all8contracts preserved; build18.223vs19.053 and animate23.757vs24.539. Receipts in external taskroot frontend-serial-control.json and frontend-parallel-candidate.json. Gate caps browserworkers2 and falls back1 when available CPUs minus outerjobs leaves fewer2. Budgets unchanged. Atomic optionalreceipts carry sourcecommit/dirty/status. Hosted exact-head verification remains required.
