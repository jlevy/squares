---
type: is
id: is-01m44xye3rpvpb1gv26h4tvcbd
title: Require bead on every queued result and ask in result-requests.yaml once the 2026-10-05 lanes merge
kind: task
status: closed
priority: 1
version: 4
delegate: c-gates-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T02:23:06.360Z
updated_at: 2026-10-23T09:08:15.125Z
started_at: 2026-10-23T06:19:02.986Z
closed_at: 2026-10-23T09:08:15.125Z
close_reason: "Delivered: result-requests schema requires bead on queued results and asks, check_bead_tree fails an unowned one, postmortem sentence dropped (91b1067eb). All 124 queued items already named one. PR #748 head 417ba331b, CI green (Packing validation run 39927824318, Certificate page 39927824335)."
resolution: null
duplicate_of: null
---
The schema (packing/campaign/schemas/result-requests.schema.yaml) gained an optional bead and blocked_on on results and asks on 2026-10-05 (branch claude/ecstatic-pascal-pothtx-process, 52c4ddd39). They are optional only because the three queued items open that day (#282 oct3-oct4-mixed-14, #316's and #317's asks) were being imported by other lanes, which owned those entries. After the merge: give every remaining queued result and ask its bead (and blocked_on where it waits), then make bead required when queued is true (results) or state is queued (asks), so validate and check_bead_tree refuse an unowned queued item rather than only the sweep reporting it. Also drop the matching sentence in docs/project/postmortems/postmortem-2026-10-05-orphaned-catalogue-intake.md (The other lists that hold work back).

## Notes

2026-10-23 c-gates-1023 (PR #748): result-requests.schema.yaml requires `bead` on a result with queued: true and an ask with state: queued; check_bead_tree collects an unowned queued item as a deferral to no bead and fails it as unowned; the postmortem sentence is dropped. Commit 91b1067eb; tests in test_check_requests.py (two schema cases) and test_bead_tree.py. All 124 queued items on main 44df28b07 named a bead; none unowned on #742's head or the claude/intake-2026-10-23* heads.
