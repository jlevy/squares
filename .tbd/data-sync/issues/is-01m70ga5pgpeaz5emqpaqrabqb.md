---
type: is
id: is-01m70ga5pgpeaz5emqpaqrabqb
title: "Import #935, #936: Doğa Özden's s(172) and s(270) upper bounds (kenaznia-doga, 9 November)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l71
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-09T15:54:58.640Z
updated_at: 2026-11-09T16:43:23.169Z
started_at: 2026-11-09T15:55:06.608Z
---
#935 s(172) <= 13.614689853287 (kenaznia-doga/s172-upper-bound @ 2ce1f7c7, n-172-candidate.yaml sha256 0df5ae79...), 3.246e-3 below T-257; #936 s(270) <= 16.928148603343 (s270-upper-bound @ 78ab8cec, sha256 f2b62bf0...), 1.365e-5 below T-224. Both opened 2026-11-09T15:28Z, promoted with packing-witness promote --strategy robust-rational @ ef1af493; repos carry LICENSE.md (CC BY 4.0 / MIT) and Daniel's MIT notice. Precedent: #927-#931 (think-463r, PR #932).

## Notes

L71 (bold-ritchie-l71), 2026-11-09, branch claude/bold-ritchie-xo28us-l71 from main ef1af4933.

Done so far:
- Packets ozden-s172-upper-bound-2026-11-09 (2ce1f7c, 11 files: 7 retained incl. n-172-decimal-pose.yaml, 4 pinned: diff png by digest, verifier/README.md and sqcheck.py identical_to earlier Özden packets, LICENSE-evand-square-packing.txt identical_to evand-issue845's LICENSE) and ozden-s270-upper-bound-2026-11-09 (78ab8ce, same shape, LICENSE pinned to evand-n270-sweep's). All digests match the issues/READMEs.
- check-claims: 172 exact side ceil16 13.6146898532862152, 3.246e-3 below T-257; 270 ceil16 16.9281486033428544, 1.365e-5 below T-224. Prints are the 12-place ceilings.
- certify + check --replay + sharp-controls: both routes accept, gross controls refused, 11 sharp controls each as expected. Pair gap >= 2.008e-13 (172), 2.016e-13 (270).
- measure_identity: 172 not one to one with T-257 by nearest centres (15 beyond 0.1, 9 tilts reversed); 270 one to one with T-224 (1 beyond 0.1, one square turned 32.3 deg).
- contraction_margin (from L65 branch, scratch copy): T-257 margin 1.36e-19, T-224 1.69e-19; gains are 2.4e16 and 8.1e13 times those. Özden's own margins 2.53e-12 and 3.21e-12.
- Ledger upper-bounds-935-936-20261109 records both.
- Registered T-282 (172, draft S3) and T-283 (270, draft S2) at V3/C3 on the replay, pending review think-qqyg. Requests, coverage, bibliography, resources, site cards, census, citation deferrals.
- Follow-ups owed on adoption: #845 (T-257 named current), #703 (T-224 confirmed/house).

Adoption is NOT done: select_houses.eligible needs an accepted review in `reviews`, and check_results refuses the verified lane without it. Mapping L72's review then adopting (adopt_houses, both strong regularizers, derived records) is the next step.

Update (16:55Z): draft PR #937 open (labels intake, S3), head 3e81f5d01. Commits: intake aa7cc6270, register ed8a71fc7, release record 5af3a8f9a, re-pin a6f21e975, records-tier fixes e6e1458ec, importer roster 3e81f5d01. Local --records: only check_results contiguity fails (T-280/T-281 not on main until #934). --edit: 70/71, same one. Hosted CI: suite-a and validate fail on the same contiguity only. A local preview merge of the L65 branch (branch l71-merge-preview, not pushed) passes --records fully and 1096 touched tests (test_house_adoption included). Waiting for #934 to land, then merge main, re-render SYNOPSIS row (283/251), site-urls, views, census; re-pin; retain contraction receipts with the module from main.
