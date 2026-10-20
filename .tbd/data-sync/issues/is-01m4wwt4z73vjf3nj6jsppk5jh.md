---
type: is
id: is-01m4wwt4z73vjf3nj6jsppk5jh
title: Reject encoded userinfo in changelog HTTPS targets
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
created_at: 2026-10-14T09:45:03.706Z
updated_at: 2026-10-14T11:11:55.520Z
started_at: 2026-10-14T09:45:13.323Z
closed_at: 2026-10-14T11:11:55.520Z
close_reason: Delivered in PR590 final2ef11f49f36cd0b14c98823f3897078ac90043b8, merged287d9cba1d1777ec5531aa8eb73817e7faf82c2a. Senior/security/correctness A-G findings addressed; final Packing38548000279, Pages38548000229, mergeability38547992638 and exact-head full38548121070 passed. Actual merged Pages38552030866 publication/deployment/live verification succeeded; verifier115817992138 bound full287 and passed4182 checks. About launch index22entries/47deliveries/34noteworthyPRs/13explicitomissions; sharedsite/infographicsv0.6.0 and independentexplainer0.4.6 delivered. Subsequent new launches563/590 and independently tracked enforced main timing fix continue in PR599/think-h96x; storage and cost advisories remain separately owned.
resolution: null
duplicate_of: null
---
Dedicated security review found encoded delimiter URLs can pass the decoded-authority no-userinfo check while emitted original URL still contains credentials. Validate original and decoded authorities, retain no-script guarantees, and add both encoded-userinfo controls before PR590 delivery.
