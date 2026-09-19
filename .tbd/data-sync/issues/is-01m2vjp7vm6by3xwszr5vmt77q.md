---
type: is
id: is-01m2vjp7vm6by3xwszr5vmt77q
title: "PR #199 review F-PY-3: G4 linprog failure reported as refused"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2vjmfpw370ygezsjr5xbn9z
created_at: 2026-09-19T00:57:31.764Z
updated_at: 2026-09-19T00:59:50.908Z
closed_at: 2026-09-19T00:59:50.908Z
close_reason: "Fixed in fc873d74: HiGHS status 1 from solve_covering is unresolved; produce writes status=unresolved. Test: test_covering_timeout_is_unresolved_never_refused. Scientific n=11/n=6 targets stay refused."
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/199#issuecomment-5734563940
packing/devtools/produce_threshold_certificate.py:194-204 and 405-406. HiGHS status 1 must be unresolved, not refused/infeasible. Scientific n=11 181-net and n=6 at 299/100 stay refused.
