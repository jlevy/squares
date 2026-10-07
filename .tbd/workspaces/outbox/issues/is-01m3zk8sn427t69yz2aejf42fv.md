---
type: is
id: is-01m3zk8sn427t69yz2aejf42fv
title: Independent review of the kernel and branch-and-bound verifier rewrites (lane R6)
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T00:40:19.363Z
updated_at: 2026-10-03T01:42:34.287Z
closed_at: 2026-10-03T01:42:34.286Z
close_reason: Both verifier rewrites admitted; digests listed (0c56fb627)
resolution: null
duplicate_of: null
---
Gates adding digests 5c550f7c (kernel, e0b66f07b) and the ff5471e89 branch-and-bound
verifier to the ledger’s reviewed verifiers.
Deliverable: docs/project/reviews/review-2026-10-03-n17-verifier-rewrites.md with an
admission verdict per verifier, mutation results, and old/new agreement on W7 and an N1
sample. Started 2026-10-03 00:00 UTC.

## Notes

DONE. Review 1c870efe2, conditions met 0c56fb627: four tests added by R6, each of five
mutants fails at least one; unmutated 27 pass.
Ledger lists kernel 5c550f7c and branch-and-bound 9ca8df6f as reviewed verifiers.
Next: N1 admission batched with the south-wall class in an experiment record
(clean-worktree --check-saved at a fixed commit, full verification by a listed digest).
