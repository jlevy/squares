---
type: is
id: is-01m4jrxf9g47e2jbhvc39t0kbf
title: "Record fixes from the 2026-10-10 stage-5 audit: E-ryxu-432 limitations, the ry-xu credit name, stale next_rung clauses"
kind: task
status: closed
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T11:24:33.968Z
updated_at: 2026-10-23T06:12:20.169Z
closed_at: 2026-10-23T06:12:20.169Z
close_reason: "Tracker audit 2026-10-23 (c-audit-a-1023, think-s4ld), checked by coord-intake-1023: DONE. (1) 120fd32d5 and (3) 23e396d5c are ancestors of origin/main; (2) bibliography '[ry-xu square packing 2026]' has credit: Xu (owner 2026-10-14 credit decision); (4) #398 merged 2026-10-11"
resolution: null
duplicate_of: null
---
Found by the stage-5 check of the deployed main tree (think-mtwe, 2026-10-10). (1) packing/frontier/evidence.yaml E-ryxu-432-rational-feasibility: its limitations and review do not record that ry-xu's own checks ran this repository's sqpack (packing-witness verify at 84881f2); add that sentence (the rung is unaffected: the second route is independent of what the author ran). (2) packing/resources/bibliography.yaml '[ry-xu square packing 2026]' has no credit field, so the site credits 'ry-xu' while other records say 'Ryan Xu' or 'Xu': an owner decision on the name. (3) T-128 and T-130 next_rung still say 'Final exact-head CI remains required' though CI passed on main; rewrite with the review lane's next_rung (think-fvz4). (4) check_published_site's workbench_startup ignores SQPACK_CHROMIUM; jlevy/squares#398 (draft) already carries that fix.

## Notes

2026-10-10, records lane of the intake pass (sub-agent, Claude Opus 5.5), branch worktree-agent-af77bc1990859851b: (1) done in 120fd32d5: E-ryxu-432-rational-feasibility's limitations now say that issue 432 reports ry-xu's own checks ran this repository's sqpack at 84881f2 (packing-witness check, promote and verify, VERIFIED for all 25), so the sqpack exact_verify route reproduces with the producer's checker and the independent rational-corner checker decides apart from it; relation and rung unchanged. (2) the ry-xu credit name is left to the owner. (3) done in 23e396d5c: T-128 and T-130's next_rung no longer say "Final exact-head CI remains required"; both, with T-131, are at V3/C3 on the 10 October review. (4) not touched (jlevy/squares#398).
