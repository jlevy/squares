---
type: is
id: is-01m4jrxf9g47e2jbhvc39t0kbf
title: "Record fixes from the 2026-10-10 stage-5 audit: E-ryxu-432 limitations, the ry-xu credit name, stale next_rung clauses"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T11:24:33.968Z
updated_at: 2026-10-10T11:24:33.968Z
---
Found by the stage-5 check of the deployed main tree (think-mtwe, 2026-10-10). (1) packing/frontier/evidence.yaml E-ryxu-432-rational-feasibility: its limitations and review do not record that ry-xu's own checks ran this repository's sqpack (packing-witness verify at 84881f2); add that sentence (the rung is unaffected: the second route is independent of what the author ran). (2) packing/resources/bibliography.yaml '[ry-xu square packing 2026]' has no credit field, so the site credits 'ry-xu' while other records say 'Ryan Xu' or 'Xu': an owner decision on the name. (3) T-128 and T-130 next_rung still say 'Final exact-head CI remains required' though CI passed on main; rewrite with the review lane's next_rung (think-fvz4). (4) check_published_site's workbench_startup ignores SQPACK_CHROMIUM; jlevy/squares#398 (draft) already carries that fix.
