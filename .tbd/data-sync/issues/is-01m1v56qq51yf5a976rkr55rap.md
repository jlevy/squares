---
type: is
id: is-01m1v56qq51yf5a976rkr55rap
title: Correct the cold-review audited-head provenance
kind: bug
status: closed
priority: 0
version: 4
spec_path: packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md
labels:
  - release-blocker
  - provenance
dependencies:
  - type: blocks
    target: is-01m1v2yhy02qmka8ez4d2f5bde
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T10:46:10.405Z
updated_at: 2026-09-06T17:57:54.053Z
closed_at: 2026-09-06T10:50:28.339Z
close_reason: "Integrated e893d164: the protocol now identifies 0660f02b as the cold review's shared input, ca188bd2 only as the fourth transport's parent/prior transport head, and lists think-hvze in the release graph and umbrella prerequisites. The isolated transport passed Flowmark, documentation, and edit-tier checks."
resolution: null
duplicate_of: null
---
The integrated Cold Senior Review Protocol names ca188bd2 as the audited input, but that is the isolated transport parent; the cold senior reviewer explicitly audited shared head 0660f02bc41f49d90e6cc763afb9fe926c2858c6. Distinguish the cold-audit input from transport lineage and keep later exact-candidate review requirements intact. Acceptance: handoff carries both roles without conflation, live document checks pass, and the current release umbrella blocks on this bead.
