---
type: is
id: is-01m2chknz8861931tannzahgvh
title: Reject invalid and nonfinite trials consistently in annealing reports and sweeps
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2b7na7psnnn1j62g1yjdtta
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-13T04:50:02.851Z
updated_at: 2026-09-13T04:52:35.238Z
---
Review R3: valid() uses not(overlap>tolerance), admitting NaN from missing resolved metrics; sweep() bypasses validity filtering and ranks resolved_closed for every row. Introduce one admission rule for trial counts, finite metrics, finite poses, pair/wall validity and raw/repaired provenance. Use it in replay, report and sweep; report rejected counts and refuse an empty admitted population. Add negative controls for NaN/missing fields and invalid high-scoring rows.
