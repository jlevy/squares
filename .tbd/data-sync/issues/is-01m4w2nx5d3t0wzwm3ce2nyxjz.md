---
type: is
id: is-01m4w2nx5d3t0wzwm3ce2nyxjz
title: Preserve changelog entry fragments in website aliases
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
hold: null
hold_until: null
created_at: 2026-10-14T02:08:21.659Z
updated_at: 2026-10-14T11:11:55.500Z
started_at: 2026-10-14T02:08:55.730Z
closed_at: 2026-10-14T11:11:55.500Z
close_reason: Delivered in PR590 final2ef11f49f36cd0b14c98823f3897078ac90043b8, merged287d9cba1d1777ec5531aa8eb73817e7faf82c2a. Senior/security/correctness A-G findings addressed; final Packing38548000279, Pages38548000229, mergeability38547992638 and exact-head full38548121070 passed. Actual merged Pages38552030866 publication/deployment/live verification succeeded; verifier115817992138 bound full287 and passed4182 checks. About launch index22entries/47deliveries/34noteworthyPRs/13explicitomissions; sharedsite/infographicsv0.6.0 and independentexplainer0.4.6 delivered. Subsequent new launches563/590 and independently tracked enforced main timing fix continue in PR599/think-h96x; storage and cost advisories remain separately owned.
resolution: null
duplicate_of: null
---
Candidate correctness C2: CHANGELOG.md#regularization-foundations currently maps to About top changelog anchor. Preserve and validate entry fragments while mapping an unfragmented changelog to About changelog.
