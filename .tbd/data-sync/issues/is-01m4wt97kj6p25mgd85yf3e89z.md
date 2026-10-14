---
type: is
id: is-01m4wt97kj6p25mgd85yf3e89z
title: Keep unpublished infographic candidate editions stable through review corrections
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
hold: null
hold_until: null
created_at: 2026-10-14T09:00:52.209Z
updated_at: 2026-10-14T11:11:55.481Z
started_at: 2026-10-14T09:02:36.912Z
closed_at: 2026-10-14T11:11:55.481Z
close_reason: Delivered in PR590 final2ef11f49f36cd0b14c98823f3897078ac90043b8, merged287d9cba1d1777ec5531aa8eb73817e7faf82c2a. Senior/security/correctness A-G findings addressed; final Packing38548000279, Pages38548000229, mergeability38547992638 and exact-head full38548121070 passed. Actual merged Pages38552030866 publication/deployment/live verification succeeded; verifier115817992138 bound full287 and passed4182 checks. About launch index22entries/47deliveries/34noteworthyPRs/13explicitomissions; sharedsite/infographicsv0.6.0 and independentexplainer0.4.6 delivered. Subsequent new launches563/590 and independently tracked enforced main timing fix continue in PR599/think-h96x; storage and cost advisories remain separately owned.
resolution: null
duplicate_of: null
---
PR590 guards compare selected version with local retained output, so a correction after the first unpublished redraw wrongly demands another version bump. Compare against the authoritative published/main baseline, allow same successor version across review revisions, preserve refusal to alter an already published edition and atomic full-pair promotion, and add first-redraw/correction/rebuild controls.
