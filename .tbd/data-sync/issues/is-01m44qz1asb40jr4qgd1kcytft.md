---
type: is
id: is-01m44qz1asb40jr4qgd1kcytft
title: "Import David Ellsworth / Allen Chang via the Kingbird catalogue: s(69) <= 8.82719465572973, s(83) <= 9.63475764863108, s(87) <= 9.83881526994826 (no issue)"
kind: task
status: closed
priority: 1
version: 8
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:38:34.584Z
updated_at: 2026-10-05T07:51:14.743Z
started_at: 2026-10-05T00:40:48.766Z
closed_at: 2026-10-05T07:19:47.755Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---
source-coverage.yaml pending_catalogue_intake lists n = 69, 83, 87: the 2026-09-30 Kingbird capture prints sides below the record. Register (T-088 n=69 Ellsworth; T-089 n=83, 87 Allen Chang), take the sides into the case records, remove the pending entries, witness from evand's parse of the SVGs at evand/square-packing 7ff3b21 site/www/data/p/ (kingbird.myphotos.cc is blocked by this session's egress policy). Stage 4 witness check if cheap.

## Notes

2026-10-05 lane kingbird, branch claude/ecstatic-pascal-pothtx-kingbird (not pushed): c023a08f9 tools; a79980ef0 records (T-088 n=69 Ellsworth, T-089 n=83,87 Chang, V0/C0, S2 draft); 326cd66f7 fixes found by the reachable tests (AI quotation vs formatter curled quotes; coverage wrap; chunk coverage pin); d21084b38 data pin. records tier green. Witnesses from evand/square-packing@7ff3b21 site/www/data/p parse (source.revision); --compare-parse: 90/90 agree to 1 ulp now (before intake 90/92, the two differing were 83/87 whose pictures had changed). Open: stage 4 for T-088/T-089 (rational promotion of the retained witnesses, which a scratch trial found within ~1e-12 of each printed side; independent check; receipts; verifiers; negative controls; review under docs/project/reviews/), re-derive from the SVGs when kingbird.myphotos.cc is reachable (and retain n=83's degree-672 polynomial); agenda-005 BC-050 (precise n=68/69 witnesses) is moot for n=69.
