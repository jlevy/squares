---
type: is
id: is-01m1sbn8zzc33cnng95hbkw2a1
title: The complete integration surface runs only on main, so no PR can catch a failure in it
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T18:00:29.439Z
updated_at: 2026-09-05T18:00:29.439Z
---
packing-validation.yml runs 'packing-validate --fast' on pull_request and the complete surface only on push to main (plus weekly cron and workflow_dispatch). Steps outside the fast tier -- deterministic SVG rendering, the record and rendering controls, the exhaustive exact tier -- are therefore first exercised after merge, and D-455 plus the exhaustive budget overrun both reached main that way. Consider: dispatch the complete surface on the branch before merging, or move cheap record controls into the fast tier. Trade-off is the ~40 min the complete surface costs.
