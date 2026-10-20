---
type: is
id: is-01m4w2nt19c83ngs7xswsa8vhs
title: Isolate disposable release-impact Git fixtures from inherited Git environment
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
created_at: 2026-10-14T02:08:18.456Z
updated_at: 2026-10-14T11:11:55.468Z
started_at: 2026-10-14T02:08:55.696Z
closed_at: 2026-10-14T11:11:55.468Z
close_reason: Delivered in PR590 final2ef11f49f36cd0b14c98823f3897078ac90043b8, merged287d9cba1d1777ec5531aa8eb73817e7faf82c2a. Senior/security/correctness A-G findings addressed; final Packing38548000279, Pages38548000229, mergeability38547992638 and exact-head full38548121070 passed. Actual merged Pages38552030866 publication/deployment/live verification succeeded; verifier115817992138 bound full287 and passed4182 checks. About launch index22entries/47deliveries/34noteworthyPRs/13explicitomissions; sharedsite/infographicsv0.6.0 and independentexplainer0.4.6 delivered. Subsequent new launches563/590 and independently tracked enforced main timing fix continue in PR599/think-h96x; storage and cost advisories remain separately owned.
resolution: null
duplicate_of: null
---
Candidate security B2: tests/test_release_impact.py Repository.git inherits Git redirection and can commit/update refs in an unrelated repository. Scrub Git routing variables, disable inherited hooks before init, and test an unchanged external sentinel.
