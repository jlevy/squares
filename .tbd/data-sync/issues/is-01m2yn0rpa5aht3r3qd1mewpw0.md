---
type: is
id: is-01m2yn0rpa5aht3r3qd1mewpw0
title: "PR 202: reconcile the restacked corrections and certify every landing layer"
kind: task
status: open
priority: 1
version: 2
labels:
  - correctness
dependencies: []
parent_id: is-01m2ymyd4zef0ckcx8gvq3p5dx
created_at: 2026-09-20T05:35:57.129Z
updated_at: 2026-09-20T05:43:48.565Z
---
After PR199–201 repairs, restack PR202 on the new PR201 head. Remove only correction patches now supplied by lower layers, preserve remaining test-fixture and performance fixes, and retain the Session142 review and cost/provenance history. Compare the cumulative implementation with reviewed 8dbc1068 and closure 8cab8309 using Git range-diff/tree diffs; account for every difference, with no lost guard, test, certificate, record or atlas export. Historical original-head failures remain true; add current readiness evidence rather than rewriting those observations. Obtain fresh evidence for any changed source/base, auditing actual receipt checkout identities and the complete selected-step union; skipped jobs are not passes. Done when a readiness table names every PR199–202 current head/base, review verdict, substantive fast/deferred runs and mergeability, with all four individually green and no unresolved correctness finding. Make stack relationships and PR bodies agree and leave all PRs ready for review. No merge is authorized by this bead-creation request.
