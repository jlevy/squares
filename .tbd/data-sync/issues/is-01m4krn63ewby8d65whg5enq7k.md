---
type: is
id: is-01m4krn63ewby8d65whg5enq7k
title: "Import Evan Daniel: exact-optimum certificates at 15 counts below the register (regularized lists, 122d0ba) (no issue)"
kind: task
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T20:39:16.846Z
updated_at: 2026-10-11T03:04:36.011Z
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

## Notes

2026-10-10, lane L29 (stages 2-3 groundwork and the stage 4 replay, no records edited):
commit 0b5aa6bb4 on worktree-agent-a717630f351063391, from claude/determined-rubin-yjfy2a
at 125b0340f.

- Pin: ea1a2f23678a13bd1d252f9f4c95ca5dd2ffd2b7, the head at retrieval (20:45Z; the head
  had moved past baf9143 by one commit of n17 Lean modules, lean_batch.py and TODO.md).
  search/regularize/ is unchanged since 122d0ba; the 15 certificates and their JSON are
  unchanged since 346c6ed (first_committed 2026-10-10T18:05:38Z).
- Packet packing/resources/web/evand-regularized-2026-10-10: the 15 n-NNN.cert.gz and
  n-NNN.json.gz retained as original gzip, REGULARIZE.md, LICENSE (MIT), CREDITS.md;
  best.csv, best.json, site/data/records2026.json and verify_cert*.py (identical to the
  issue-399 copies) pinned by digest. 38 manifest files, 33 retained. acquire_source
  --check: PACKET_MATCHES_ITS_CONTRACT.
- Declaration: offered = each JSON's S_cert (exact), houses per case record, pending
  reports T-137 (#483) at 70, T-138 (#470) at 103/258/302/303, T-136 (#481) at the seven
  SQUISH counts, T-134 (#476) at 263/303, #476 at 269 (equal to the case), #488 at 303
  (uncited). HOUSES gained exact readers for #483, #470 and this packet.
- check-claims: this certificate is the smallest at all 15; least gap 2.21e-17 (302,
  T-136) to 7.82e-10 (295, ry-xu case). Matches L26's triage exactly.
- certify --workers 2: 45 jobs, 302 s wall, 2,155,368 pair decisions, 413.8 route CPU s,
  566.29 job wall s, longest 39.16 s (295 outside control). check --replay (serial):
  15 certificates and 45 jobs admitted, 476 s.
- Third route: decide-imports --imports regularized --upstream (new roster group):
  15 pass, 90/90 controls, wall 5e-21, least distance 1.00e-20, 30 upstream checks
  (retained gzip bytes and S_cert prints), no disagreement, 111 s on two workers.
  arrangement_gap against the credited packing: 10-238 squares moved beyond 1e-6 under
  the lists' stated orientation; 123, 129, 292 match one to one under no symmetry.
- register-plan run; corrected entries (claim wording, significance rationale, notes,
  evidence limitations, coverage notes, README line) handed to the coordinator in the
  lane report. No T-NNN taken.
- Open for the owner: credit at 70 (the view is nearer Xu's poses than Deleeuw's; the
  source's site credits #432 only); the source's lists credit other finders (DeVincentis
  at 70, Couzo, Ellsworth, Cantrell); intake-watch needs a read at ea1a2f2.

2026-10-11, records lane (stage 4 exit, done on claude/determined-rubin-yjfy2a, not
pushed): commits 3ad82d5b6 "register: typed regularizations, and T-146's stage 4 exit at
V3/C3" and 5356edce9 "release: re-pin DATA_REVISION to 3ad82d5b".

- The stage 4 review is committed:
  docs/project/reviews/review-2026-10-10-evand-regularized-certificates.md (accepted for
  finite feasibility only, RG-1 to RG-11 non-blocking), mapped in document-map.yaml.
- T-146 at V3/C3 through E-evand-regularized-exact-feasibility (new) and the review's
  reviews entry; claim, notes, next_rung and significance are the review's texts, split
  into paragraphs under check_prose_ceremony's 800-character wall; activity removed; the
  review added to artifacts. E-evand-regularized-certificate-report carries the review as
  external_review and no longer says the review is pending.
- Credit at 70: Ryan Xu alone (owner), T-137 named only as the previous smallest side.
  [Daniel regularized lists 2026-10-10] credit is now "Daniel after Xu, Chaoweeraprasit,
  Mishapolk, Levy" (RG-2).
- T-146 carries 15 `regularizations` items (think-cgdv): of T-125 at 70, 102, 123, 129,
  146, 295; T-138 at 103, 258; T-136 at 153, 236, 263, 269, 292, 302, 303; by the
  bibliography key; side solved; identity source-claim with the review's measurements.
- RG-8: the pending-review sentences of T-125, T-136, T-137 and T-138 (notes and
  next_rung), the coverage entry, the resources README line and the intake-watch note
  are rewritten. verifiers.yaml notes of V-check-half-angle-area and V-upper-bound-reports
  name this review.
- Case adoption deferred in packing/devtools/certificate-citation-deferrals.yaml
  (E-evand-regularized-exact-feasibility, bead think-fvz4, blocked on
  jlevy/squares#403). T-146's site URL row records an amendment for its new evidence and
  artifacts.
- Validation: packing-validate --records and --edit pass (--jobs 2); the six targeted
  test modules pass (323 tests). Remaining for this bead: stages 5 to 7 (house adoption
  after #403 and private-worker custody, RG-7).
