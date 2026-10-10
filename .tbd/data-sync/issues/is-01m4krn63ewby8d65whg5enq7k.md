---
type: is
id: is-01m4krn63ewby8d65whg5enq7k
title: "Import Evan Daniel: exact-optimum certificates at 15 counts below the register (regularized lists, 122d0ba) (no issue)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T20:39:16.846Z
updated_at: 2026-10-10T20:39:16.846Z
---
Evan Daniel's display-regularized record lists (evand/square-packing `search/regularize/`, added 346c6ed on 2026-10-10 18:05Z, lists refreshed at 122d0ba666884b176b2e442056c4fd1afe5a634a; head baf9143 at 20:31Z) hold one exact rational certificate per count for n = 1..324 (`lists/certs/n-NNN.cert.gz` plus 50-digit JSON). Lane L26 of the 2026-10-10 pass parsed all 329 certificates with `devtools.evand_exact_certificates.parse` and compared each exactly with every value the register holds (case records, source-coverage overrides, superseded and beyond-horizon rows, packet claim records, results.yaml claims). At 15 counts the certificate is strictly below the register's least value:

| Counts | Register's least value | Gap |
|---|---|---|
| 70 | T-137 | 1.07e-11 |
| 102, 123, 129, 146, 295 | ry-xu's #432 ceilings | 7.90e-11 to 7.82e-10 |
| 103, 258 | T-138 | 6.94e-13, 4.21e-12 |
| 153, 236, 263, 269, 292, 302, 303 | T-136 | 2.21e-17 to 5.05e-13 |

All 15 (and n = 51, which equals the case's (16+5√2)/3) pass both maintained exact routes' `decide` in triage (pair gap 1e-20, wall clearance 5e-21; no controls; not a stage 4 replay). The author does not claim them as records: REGULARIZE.md says no refreshed side is below the store's best beyond rounding (2e-12 .. 8e-10, the exact optimum of the same packing). By the T-139 (unclaimed n126_xu) and T-137 precedents each is still a value the register does not hold. No issue reports them. The repository has a LICENSE (MIT).

Plan: a packet at 122d0ba retaining the 15 gzipped certificates (the evand-cert adapter needs gunzip, or derived facts) with `acquisition/report.json` for `devtools.upper_bound_reports` naming the houses and pending reports per count; `certify` with a positive and 2 controls per count (about 45 jobs, 5 to 10 CPU-minutes); the third exact route; one register entry scoped to the 15 counts, a coverage source and a bibliography key; credit to the original finders (ry-xu, SQUISH, Mishapolk at 103/258, Deleeuw at 70) improved by Evan Daniel, as T-098 did; a stage 4 review for V3/C3. n = 261's stated exactsolve optimum 16.6787798753429 is not certified and is not part of this import.
