---
type: is
id: is-01m0thx4ty9zwzmw4bt2d7xmqk
title: Derive defect-direction and detector aggregates in SYNOPSIS
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: unknown@spud10.local
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
hold: null
hold_until: null
created_at: 2026-08-24T18:53:11.389Z
updated_at: 2026-08-24T18:58:35.499Z
started_at: 2026-08-24T18:56:46.514Z
closed_at: 2026-08-24T18:58:35.498Z
close_reason: "D-185 fixed in 29d99b1: SYNOPSIS now states the derived 50/61 soundness-direction and 7/185 gate-detector aggregates; both focused mutations fire."
resolution: null
duplicate_of: null
---
D-185. The living synopsis says 45/55 soundness defects were flattering and the gate caught 6/161, while defects.yaml currently derives 50/61 and 7/183 before the newly found D-184. Update the prose and extend check_synopsis.py plus focused mutations so both the soundness-direction fraction and gate-detector aggregate derive from defects.yaml. Acceptance: current 50/61 and 7/184 statements pass after D-184; either stale aggregate fails.
