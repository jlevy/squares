---
type: is
id: is-01m44xye3rpvpb1gv26h4tvcbd
title: Require bead on every queued result and ask in result-requests.yaml once the 2026-10-05 lanes merge
kind: task
status: open
priority: 1
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
created_at: 2026-10-05T02:23:06.360Z
updated_at: 2026-10-05T02:23:06.360Z
---
The schema (packing/campaign/schemas/result-requests.schema.yaml) gained an optional bead and blocked_on on results and asks on 2026-10-05 (branch claude/ecstatic-pascal-pothtx-process, 52c4ddd39). They are optional only because the three queued items open that day (#282 oct3-oct4-mixed-14, #316's and #317's asks) were being imported by other lanes, which owned those entries. After the merge: give every remaining queued result and ask its bead (and blocked_on where it waits), then make bead required when queued is true (results) or state is queued (asks), so validate and check_bead_tree refuse an unowned queued item rather than only the sweep reporting it. Also drop the matching sentence in docs/project/postmortems/postmortem-2026-10-05-orphaned-catalogue-intake.md (The other lists that hold work back).
