---
type: is
id: is-01m4ky8t55xs2vpah34mrpv8b9
title: Propose tbd claim diagnostics and measurable lifecycle audit
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-10-10T22:17:22.851Z
updated_at: 2026-10-10T22:50:20.914Z
---
Follow-up from think-qpm4. Build a reusable audit of current owner metadata and session events: creation/claim before first work, delegated task ownership acceptance, completion dispositions, and successful issue sync at session start, post-commit, handoff and end. Exclude this review baseline additions; snapshots cannot prove ordering or successful no-op syncs. Fix misleading last_sync_at producer already documented upstream as tbd-iwup; do not duplicate that upstream defect. Consider explicit claim-conflict exit status and ownership-transfer semantics. Test distinct and shared identities, same-clone contention, stale independent clones, interrupted handoffs and sync failures. These are proposals, not implemented.

## Notes

2026-10-10 reconciliation: metadata inventory and complete disposition coverage are implemented in packing/devtools/reconcile_work.py under think-p2z4. Remaining scope is execution-order/sync evidence, beginning with the ten-slice transcript sample in docs/project/reviews/review-2026-10-10-tbd-coordination.md. Preserve lightweight defaults: event receipts or enforcement must be opt-in. Current start exit behavior stays compatible; inspect claimed/skipped. Upstream last_sync_at defect remains tbd-iwup. Do not duplicate the metadata tool or the optional coordination shortcut under think-nx5z.
