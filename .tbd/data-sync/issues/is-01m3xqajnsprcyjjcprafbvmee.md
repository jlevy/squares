---
type: is
id: is-01m3xqajnsprcyjjcprafbvmee
title: "W9: re-ground T-007's consumers per the 2026-10-02 Nagamochi review (287 floors, s(k^2-1), s(k^2-2))"
kind: task
status: closed
priority: 1
version: 3
labels:
  - research
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-02T07:12:43.192Z
updated_at: 2026-10-02T20:45:54.069Z
closed_at: 2026-10-02T20:45:54.068Z
close_reason: "Applied per the 2026-10-02 review with the pass branch (6200bcf23): T-007 V0/C1; T-066..T-069; 271 case records re-grounded; D-516; FRONTIER_COUNTS 0 Nagamochi-bounded. Departures recorded: n=54,57,73 on T-044's values; n=61 pending think-jkeu. Green on PR 305 at 730f4f2e1."
resolution: null
duplicate_of: null
---
The W2 review docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md concludes: Nagamochi 2005 Lemma 1 is false for every a > 3, b > 2 (Karakuš's family K_t, verified in exact arithmetic by devtools.check_nagamochi_lemma1_counterexample), Theorem 1 rests on it alone, and the gap reaches T-007 for every N >= 10. Recommended statuses: T-007 V0/C1 'incomplete'; E-nagamochi-lower external_review defect-found (2026-10-02); the general floors re-grounded on Karakuš Corollary 6.2, s(N) >= 1/2 + sqrt(N - floor(sqrt N) + 1/4), as new published-proof evidence V3/C1 (strictly weaker except at N = m^2-1); s(k^2-1) = k at V3/C1 on Karakuš Corollary 1.2; s(k^2-2) = k at V0/C0 until chelokot's Lean proof is replayed with an axiom receipt, the verified floor at N = 14, 23, 34, 47, 62, 79, 98, ... falling to Karakuš's value meanwhile; a correction result for Lemma 1. The inventory devtools.audit_t007_consumers (records tier) lists the 287 records whose operative floor cites Nagamochi (238 open, 49 proved; 224 outside T-007's registered 4-100 scope), the exposure class of each, and the documents that state the theorem as proved (SYNOPSIS, frontier README and RESULTS, results.yaml, evidence.yaml, generate_frontier_case.py, 291 case bodies, bound-citations.json, three research reports). Apply per conventions.md §7 (dated corrections, originals kept), add a defect entry for the register's V3 reliance, regenerate every view, and re-run the inventory. Owner decision pending: apply now, or after the Lean replay bead.
