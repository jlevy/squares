---
type: is
id: is-01m2y0n1wa7ft8kfyf9a2wjmnx
title: "PR200-201 review R3: separate unfinished research from site-set refutations"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:40:01.800Z
updated_at: 2026-09-20T01:51:15.297Z
closed_at: 2026-09-20T01:51:15.297Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
H218 criterion:25-28, H220:25-27, H221 and X039:59-61 misclassify unconverged loops or stalled interval checks as site-set refutations. n20 restricted optima19.910044/19.939212 remain below20; adding rows need not cross20. Exact-only replay of exp171 n29 passes while interval stalls, confirming inconclusive is not refuted. Correct hypotheses, rankings and dispositions; budget-based retirement can remain as a scheduling decision without impossibility claims.
