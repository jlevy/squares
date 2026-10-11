---
type: is
id: is-01m0pnk0y4mh6tax6y71br6xb1
title: "Renumber PR #11's D-024 if that branch is revived"
kind: task
status: closed
priority: 3
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
created_at: 2026-08-23T06:40:36.292Z
updated_at: 2026-10-06T08:32:40.386Z
closed_at: 2026-10-06T08:32:40.386Z
close_reason: |
  Superseded (bead review 2026-10-06, origin/main eb43ffe9a): No-op by its own terms: PR #11 is CLOSED unmerged, and its finding is recorded on main as D-029
resolution: canceled
duplicate_of: null
---
PR #11 allocated D-024 for 'a partial quench was called the quench'. D-024 is taken on main by 'a strategy's enum and its prose said opposite things'. PR #11's finding is now recorded here as D-029 with a reproduction and a regression check, so if #11 is closed this is a no-op -- close it. If any part of #11 is revived, its defect entry must not reuse D-024.
