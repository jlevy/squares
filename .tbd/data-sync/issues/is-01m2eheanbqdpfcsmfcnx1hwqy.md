---
type: is
id: is-01m2eheanbqdpfcsmfcnx1hwqy
title: Refresh PR125–PR155–PR160 onto current main
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-stack
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T23:25:36.296Z
updated_at: 2026-09-13T23:53:00.155Z
closed_at: 2026-09-13T23:53:00.152Z
close_reason: null
resolution: null
duplicate_of: null
---
PR #125 is behind current main and GitHub reports mergeable_state=dirty. Merge current main into #125, resolve the campaign ledger conflict with both histories intact, propagate the resulting parent heads into #155 and #160, run branch-appropriate validation, push all three PR branches, and record final heads and CI. Preserve clean worktrees with no local-only commits; cleanup proceeds only after pushed branch state is verified.

## Notes

2026-09-13 completion: current main f2e24e07be8c94fa3ac603c3534dce7c454da99b was merged into PR125; its pushed head is 7b06254cc610b06ce9d8e6c9fa47edf1f522af9e. The ledger was regenerated, records 32/75 and edit 46/75 passed. Its required code and Pages checks passed; Pages run 34790001091 first failed the existing D-490 PDF reproduction check, and attempt 2 passed after the diagnostic pair was downloaded and logged on think-ptit. PR155 pushed head a40d272c5c65bdb809f74fb3afbb932b61d497cc includes exact PR125 head, resolves the independent X-028 collision by renaming workbench physics to X-029, and passes the campaign ledger check. Local records/edit checks only hit sandbox Ruff-cache and missing-Node environmental errors; focused lint/browser rerun passed 3/75, and GitHub required and Pages checks passed. PR160 pushed head 4a1bf3b81ee24a8360424e87a9048c5f4aadc7c1 includes exact PR155 head, combines PDF source receipt and workbench deployed-revision/navigation checks, passes 25 focused Pages tests, records 32/76, and browser floor including 112 Node tests after pinned npm ci. GitHub frontend, packing-required, suite, geometry, sweeps, validate, Pages build, and mergeability checks pass. All three PR descriptions were updated with heads and evidence. Current PR160 worktree and existing PR155 worktree are clean and match pushed refs. The completed validation worktree and its stale Git metadata were moved to Trash, unemptied. PR160 remains draft because the workbench plan lists further Pack/Search/migration/release gates; this bead covers stack refresh only.
