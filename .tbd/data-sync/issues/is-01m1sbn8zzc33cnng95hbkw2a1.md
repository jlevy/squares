---
type: is
id: is-01m1sbn8zzc33cnng95hbkw2a1
title: The complete integration surface runs only on main, so no PR can catch a failure in it
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:00:29.439Z
updated_at: 2026-09-05T21:25:13.491Z
closed_at: 2026-09-05T21:25:13.490Z
close_reason: The fast tier goes 37 steps to 58, complete-only 24 to 3. Twenty-one promotions totalling 537.83s of step time; the three deferred steps argued by their own measurements above STEPS. Promoting 'deterministic SVG rendering' immediately caught the published Markdown embedding the renderer's own copy of the composite, which is what the promotion was for.
resolution: null
duplicate_of: null
---
packing-validation.yml runs 'packing-validate --fast' on pull_request and the complete surface only on push to main (plus weekly cron and workflow_dispatch). Steps outside the fast tier -- deterministic SVG rendering, the record and rendering controls, the exhaustive exact tier -- are therefore first exercised after merge, and D-455 plus the exhaustive budget overrun both reached main that way. Consider: dispatch the complete surface on the branch before merging, or move cheap record controls into the fast tier. Trade-off is the ~40 min the complete surface costs.
