---
type: is
id: is-01m0w2p5c933yf0kcd8963rtnv
title: Do not pass generated views directly to Flowmark
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T09:05:42.792Z
updated_at: 2026-08-25T09:06:08.470Z
closed_at: 2026-08-25T09:06:08.469Z
close_reason: Recorded as D-259, recurrence of D-027. ledger.md regenerated; future formatting uses the repository-root target so .flowmarkignore remains effective.
resolution: null
duplicate_of: null
---
D-259, recurrence of D-027. During exp-038 landing, the coordinator explicitly passed campaign/ledger.md to Flowmark. Explicit file targets bypass .flowmarkignore, so Flowmark rewrapped the byte-generated view and packing-ledger check reported it stale. Acceptance: regenerate ledger.md, never explicitly format ledger.md or defects.md, run formatting from the repository root so exclusions apply, record the recurrence, and confirm ledger check plus the commit hook leave the generated view exact.
