---
type: is
id: is-01m4yd28hxb6m3ns2fbzws27ns
title: "Import Francisco Couzo: franciscouzo/square-packing 487b058 (no issue): s(211) 9.29e-6 below #586, and 296 certificates beyond 324"
kind: task
status: in_progress
priority: 2
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
child_order_hints:
  - is-01m4yst7ny3g52xgq8yr82r2az
hold: null
hold_until: null
created_at: 2026-10-14T23:48:21.180Z
updated_at: 2026-10-15T09:15:46.148Z
started_at: 2026-10-15T03:18:40.485Z
---
Found by the #607 lane (think-qik6) on 2026-10-14. franciscouzo/square-packing 487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d (2026-10-14T17:45:39Z, 'Land verified bounds through n=1024'), the parent of #607's pin 43ac7d2, is a watched-repository publication that no issue reports and no packet retains. Against b85dee2 (the issue-586 packet's pin) it adds 290 certificates under certificates/ (370 and 403 to 991), changes 7 (211, 339, 378, 379, 380, 381, 382) and deletes 22, and writes upper_bounds.json, the index #607 compares against.

Inside the corpus: certificates/n211.cert at 487b058 states s(211) <= 7496774813149710519467765230441/5*10^29 = 14.99354962629942..., 9.29e-6 below #586's 14.993558913975 (the ledger's best now at 211). Under the per-count rule it is a report at its first commit (17:45:39Z) and would be recorded.

Beyond the corpus: at 16 counts (339, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 757, 804, 812, 930) #607 (43ac7d2, 19:15:09Z) reports a smaller side, so 487b058's row there is recorded and then followed by #607's; the header of each of those 17 files (with 342, unchanged since 02f9690) states exactly the index's bound (read by the #607 lane, not retained). The other counts are unread.

Next: triage the whole commit (stage 1), retain a packet at 487b058 (stage 2), compare in report order, price the replay; add a franciscouzo read to intake-watch.yaml in the records PR.

## Notes

## 2026-10-15 reads lane (think-mq0k): mapping at the head 58a7833

franciscouzo/square-packing is at 58a783368d4b7e70bb800f0009ea9ca03e578739 (2026-10-15T01:25:11Z): 487b058 (this bead), 43ac7d2 (#607, think-qik6), 4e4c8ce (00:31:53Z, the index for n < 1024) and 58a7833 (Göbel bounds). This bead's in-corpus claim is unchanged: certificates/n211.cert has the same blob c079cb6b at 487b058 and the head, and the head's certificates/best/n211.cert is the same bytes; side 7496774813149710519467765230441/5e29 = 14.99354962629942, 9.29e-6 below #586's dostashev-merged-bands pending side (the smallest earlier exact side here), 2.79e-3 below PR #574/T-149. First committed 2026-10-14T17:45:39Z. No packet retains it yet; a packet at 487b058 or at the head pins the same bytes.

4e4c8ce supersedes much of 487b058's beyond-horizon set: at 341 counts (325 to 1023) its index side is smaller than 487b058's verified lane and #607's, equal at 358 (333 grid). Triaged read-only as think-yfoo; deciding with this bead whether one beyond-horizon import at the head replaces a 487b058 packet is the next step (report order still dates each certificate by its first commit).

The eight commits 337078c..b85dee2 the sweep flags (a7067d7, eee88d3, 0fa0e0d, e9eb44b, 93570ef, 4596670, 06d8db2, b85dee2): every certificate they change is retained by the packets at 0fa0e0d (couzo-certificates-2026-10-12, #561), 4596670 (couzo-issue583-2026-10-13) or b85dee2 (couzo-certificates-2026-10-13, #586), or superseded within the day by those pins; the unretained paths are prose (README, reviews REVIEW_20261012*.md, SEARCH_TO_400.md), the #561 publication drafts e9eb44b added and 06d8db2 removed, search code (accept_candidates.py, Cargo, search_forever.py, notify.py), found/ logs, known_best.json and the decimal poses and drawings. Nothing to import; a read through b85dee2 records it.

## 2026-10-15 stages 1, 2 and 4 (reads lane, on the coordinator's word; branch claude/wizardly-meitner-wqn4x3-reads-1015)

**Precedent read** (packing/campaign/issue-intake/upper-bounds-20261014/): the 14 October ledger walked Couzo's successive watched-repository commits as separate reports at their first commits and recorded a row a later report superseded: at 375 franciscouzo@4596670 "recorded (below by 7.71e-03)" and then #584 recorded; at 176 franciscouzo@93570ef recorded and then PR #574. So 487b058's rows are kept: recorded at 487b058, then superseded by #607 and 4e4c8ce.

**Packet** packing/resources/web/couzo-verified-bounds-2026-10-14/ at 487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d (tree f8f9ee10, 2026-10-14T17:45:39Z): 599 files, 34,106,389 bytes in scope; retained certificates/n211.cert (35,784 bytes) as factual data. The 296 certificates beyond 324 total 33,074,931 bytes, so under OR-18 ("a set totalling tens of megabytes is hosted outside the repository") they are pinned by SHA-256 and not retained; their metadata, both READMEs, upper_bounds.json and n211's decimal packing and drawing are pinned too. acquire_source --check: PACKET_MATCHES_ITS_CONTRACT. Proposal for the coordinator: keep the beyond-horizon bytes out of Git, and host them (owner) only if a replay is wanted.

**211.** s(211) <= 7496774813149710519467765230441/5e29 = 14.9935496262994211, printed 14.993549626300 (certificates/README.md at the pin); exact optimum seeded from Ostashev's #501 per certificates/n211.json. check-claims --write (main 6964362b5): smallest at 211; below #586/T-182 and #593/T-183 (same bytes) by 9.2877e-6, #583/T-181 by 9.2878e-6, #575/T-175 by 1.4456e-4, T-149 and PR #574/T-174 by 2.7871e-3, T-098 by 4.4111e-3, Fang's T-163 inventory by 6.4004e-3. Recorded under the per-count rule at 17:45:39Z; no later report is smaller (4e4c8ce restates the bytes). Replay: certify --workers 1, 03:24:21Z to 03:25:34Z: positive passes both routes, duplicate-square and outside-container controls refused by both; 132,930 pair decisions, 50.2 route CPU-s, 69.0 job wall-s; clearance 1/(2e20), least gap just under 1e-20 on both routes; check --replay again 70 s, equal; receipts/exact-certification.json.xz.

**Beyond 324** (review/compare_beyond_horizon.py from a checkout at the pin, each file held to its manifest digest and to the README's 12-place print; review/beyond-horizon-comparison.json, review/beyond-horizon-claims.json): 294 recorded (263 against the grid only, 31 against a report: #586 at 339 and 378-382, #596 at 370, Fang's direct certificates and composites 420-871, Daniel's tiling at 964; margins 9.3e-6 to 3.0e-1), 2 not recorded (812 and 930, above Fang's bef5c42 composites by 4.2e-3 and 1.3e-3); all 296 later superseded (#607 at 16 counts, 4e4c8ce at all). Owner question: 42 recorded counts (408-974) are rational witnesses 2.8e-11 to 5.7e-10 above Göbel's classical constructions, which the record holds nowhere beyond 324; 58a7833 itself corrects them to the closed forms.

**Replay price, beyond 324:** 456,922,338 pair decisions, 38 to 48 CPU-h at 0.30-0.38 ms a decision: HELD in think-2d7f with commands, the custody route and two subsets (the 31 report-beaten counts, 2.8-3.5 CPU-h).

**Register plan:** register-plan.yaml in the packet: the 211 entry (T-NNN, V0/C0, draft S1, evidence E-couzo-487b058-certificate-report, source key [Couzo verified bounds 2026-10-14]) as register-plan prints it, then a drafted beyond-horizon part: 294 rows (tracked-outside-case-corpus, bead think-nj7h), the 18 current rows they supersede (339, 370, 378-382, 421, 422, 463, 464, 507, 508, 553, 601, 651, 758, 814), the source's claims_record (review/beyond-horizon-claims.json, which check_source_coverage.load_claims reads), the 2 not recorded, and the Göbel question. No record edited.

**Tests:** packing/tests/test_upper_bound_reports_487b058.py (5) and test_upper_bound_reports_4e4c8ce.py (4) admitted with suite_files admit-local (report devtools/suite-file-cost-admissions/reads-1015-2026-10-15.json).

**Commit** 1c08cf97757d24203f08800dfa463dea6ce37937 on claude/wizardly-meitner-wqn4x3-reads-1015 (pushed; no PR), through the hooks (make hooks-install; flowmark reflowed main's SYNOPSIS.md, restored unstaged). packing-validate --records: exit 0 (03:33:43Z to 03:36:07Z). Focused tests: 349 passed (retained data, acquire_source, retained JSON, suite_files, source_coverage, both new modules). Validation bead: think-2d7f (HELD).

## 2026-10-15 records-1016 lane (think-mq0k), branch claude/wizardly-meitner-wqn4x3-records-1016, https://github.com/jlevy/squares/pull/616

Registered as T-188 (V0/C0, draft S1) at 211, 9.29e-6 below #586 (T-182). The declaration now lists T-057 at 211 and no longer labels #593's 211 as T-183 (scope 237 only); claims refrozen at main c4c690a3e. The source register holds 252 of the 296 beyond-horizon rows (source scope 211 + 252, claims record review/beyond-horizon-claims.json), superseding 18 current rows; #607's rows supersede 14 of them. Not recorded: 812, 930 (Fang composites smaller) and the 42 undecided-goebel rows (owner, #613, think-8krd). Replay held in think-2d7f (child of this bead), so this bead stays open while it is.
