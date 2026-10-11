---
type: is
id: is-01m3vdmvbhzbzwn99p67asxgd1
title: "Standing: no 'current best' chip; 'superseded' marks every result that is no longer the best"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T09:45:05.134Z
updated_at: 2026-10-01T10:42:47.042Z
closed_at: 2026-10-01T10:42:46.991Z
close_reason: "See notes: chip removed, superseded audited and checked in the records tier, checkbox hides superseded rows; merged into claude/site-polish-3 (107abb466)."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: let's drop 'current best' altogether since it is kind of implicit, and instead make sure 'superseded' reflects when something is no longer best. (1) The result tables and popovers draw no 'current best' chip; a result that still stands shows no standing chip. (2) 'Superseded' is shown on every result that is no longer the best known for its case and direction, derived from the register (a later result with a better bound on the same quantity, or the entry's superseded_by), not hand-set; audit all 61 results and list any that are no longer best but not marked, and any marked that still stand. (3) The standing filter and the 'Current best only' checkbox keep working: the checkbox hides superseded rows. (4) paper-design.md and the Results page prose say what the absence of a chip means.

## Notes

Done on claude/site-polish-3: no 'current best' chip (c1442ae5d; 'current best, reported' draws only 'reported'); standing sits under the rungs. Superseded audit (c00969d99): standing is derived from the case records; a new value-based check, devtools.check_standing, found no mismatch either way across the 61 results, and is a records-tier step (d5fec6d56). The checkbox hides exactly the superseded rows and reads 'Hide superseded' (ca137cfde): homepage 6 of 61 by default (15 with the box clear), Results page 61 (34 with it checked). For the owner: partially superseded entries stay standing because each still holds a case: T-007 (holds 63 of 97 cases), T-020 (holds n=19; beaten at 20, 21), T-021 (holds 20; beaten at 21), T-044 (beaten at 26, 29), T-045 (beaten at 32), T-047 (beaten at 11, 27, 28, 31). Non-bounds (T-012, 013, 014, 023, 031, 035, 036, 058, 059) are never superseded; T-054 and T-055 are second certificates.
