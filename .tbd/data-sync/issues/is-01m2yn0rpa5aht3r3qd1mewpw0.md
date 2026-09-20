---
type: is
id: is-01m2yn0rpa5aht3r3qd1mewpw0
title: "PR 202: reconcile the restacked corrections and certify every landing layer"
kind: task
status: open
priority: 1
version: 4
labels:
  - correctness
dependencies: []
parent_id: is-01m2ymyd4zef0ckcx8gvq3p5dx
created_at: 2026-09-20T05:35:57.129Z
updated_at: 2026-09-20T06:35:17.727Z
---
After PR199–201 repairs, restack PR202 on the new PR201 head. Remove only correction patches now supplied by lower layers, preserve remaining test-fixture and performance fixes, and retain the Session142 review and cost/provenance history. Compare the cumulative implementation with reviewed 8dbc1068 and closure 8cab8309 using Git range-diff/tree diffs; account for every difference, with no lost guard, test, certificate, record or atlas export. Historical original-head failures remain true; add current readiness evidence rather than rewriting those observations. Obtain fresh evidence for any changed source/base, auditing actual receipt checkout identities and the complete selected-step union; skipped jobs are not passes. Done when a readiness table names every PR199–202 current head/base, review verdict, substantive fast/deferred runs and mergeability, with all four individually green and no unresolved correctness finding. Make stack relationships and PR bodies agree and leave all PRs ready for review. No merge is authorized by this bead-creation request.

## Notes

Additional reviewed correction commit to preserve during restack: 93e88a3f on PR202, publication audit think-kq00 plus validation fixture race think-fpwp. It adds missing README result summaries, updates frontier bound/gap prose, adds the new-result publication sequence and registered-result omission guard, and moves TypeScript API compilation fixtures outside checkout. Retain these changes or account for their move into earlier appropriate layers; atlas payloads and mathematical claims are unchanged. Fresh CI is pending at this note.

Completion evidence: PR202 commit 93e88a3ff59a6fbe383aa59592b74793e6a79472 on base 2aaa296de815e5048b013ea268cc72d0c273b7ac passed packing validation https://github.com/jlevy/squares/actions/runs/35494422161 (all eight substantive fast jobs plus required aggregator, including macOS portability) and page/PDF checks https://github.com/jlevy/squares/actions/runs/35494422156. Branch mergeability also passed. Deferred run 35494422158 skipped and is not full-checkpoint evidence. The prior complete mathematical checkpoint is historical evidence for unchanged mathematics. The correction checkout and original checkout are clean. Publication audit and fixture correction complete; PR199–202 per-layer readiness and W7 improvements remain open, with H216 blocked behind both epics. No PR merged or new research started.
