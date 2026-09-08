---
type: is
id: is-01m1t2x178q8r8addrbexnvfx3
title: "Reconcile launch-packet prose: BC-240 duration and fresh-worktree submodule init"
kind: chore
status: closed
priority: 3
version: 2
labels:
  - planning
dependencies: []
parent_id: is-01m1t2sgqmantgyx59knjxqheg
created_at: 2026-09-06T00:46:40.871Z
updated_at: 2026-09-06T01:02:20.082Z
closed_at: 2026-09-06T01:02:20.082Z
close_reason: "Recorded on PR 89 in commit c0db25cf: the inset-1/2 screen converged in 191 s wall on the reviewer's host (receipt in agenda-025), the BC-240 duration reads 105 minutes, and agenda-024 tells a fresh worktree to init vendor/kpress before uv runs."
resolution: null
duplicate_of: null
---
Agenda-025 says the floating worker returns from 'that 90-minute theorem packet' while BC-240's budget in agenda-026 is 105 elapsed minutes and both schedule tables hand it back at 1:45. Also, an isolated worktree (a transport the plan explicitly allows) cannot run 'uv run --frozen' until 'git submodule update --init vendor/kpress' has run, because the dev group depends on the vendored kpress; neither agenda's launch sequence says so.
