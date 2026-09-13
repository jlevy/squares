---
type: is
id: is-01m2chknz8861931tannzahgvh
title: Reject invalid and nonfinite trials consistently in annealing reports and sweeps
kind: bug
status: closed
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels:
  - workbench-roadmap
  - workbench-phase-1
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2b7na7psnnn1j62g1yjdtta
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m2chr65cx0jhfd1gsmx3r31y
  - type: blocks
    target: is-01m2b80wcx8cm9vb2m97cx7s4s
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-13T04:50:02.851Z
updated_at: 2026-09-13T07:32:54.554Z
closed_at: 2026-09-13T07:32:54.551Z
close_reason: "Implemented at f9099096: canonical finite geometry/config/source admission, exact uint32 seeds, post-step returned-snapshot validation, authoritative typed API with negative shape/key controls. 78 package Python contract/admission tests and 31 Node tests passed; whole Python/type/browser floors passed. Further consumer migration and strict legacy graduation remain open under the package roadmap."
resolution: null
duplicate_of: null
---
Review R3: valid() uses not(overlap>tolerance), admitting NaN from missing resolved metrics; sweep() bypasses validity filtering and ranks resolved_closed for every row. Introduce one admission rule for trial counts, finite metrics, finite poses, pair/wall validity and raw/repaired provenance. Use it in replay, report and sweep; report rejected counts and refuse an empty admitted population. Add negative controls for NaN/missing fields and invalid high-scoring rows.
