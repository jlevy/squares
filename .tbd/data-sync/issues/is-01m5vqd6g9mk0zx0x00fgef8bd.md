---
type: is
id: is-01m5vqd6g9mk0zx0x00fgef8bd
title: "Regularization gate: no count rests owed on main; flip + general regularization required with a house change; sweep owned() staleness"
kind: task
status: in_progress
priority: 2
version: 4
delegate: w-reg-gate-1026
labels:
  - regularization
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-26T09:07:03.817Z
updated_at: 2026-10-26T10:48:30.891Z
started_at: 2026-10-26T09:07:10.279Z
---
Owner, 26 Oct 2026: 'When something lands on our main rendered lists, the regularization should be done.' Gate: retire regularization-owed (fail validation); exemptions only on the owner's recorded word (OwnerWord: quote, date, file that holds it) with review_by <= 14 days; the four unratified Kingbird exemptions (39, 55, 290, 291; think-yk2h) stand until 2026-11-09; a change that moves a house must land it regularized/regular-as-published/decided-no-better (or owner-exempt, or a PENDING_ALLOWED correction) and its flip pose recorded (--check-state --base-ref). Sweep: owned() treats a bead with no update in 7 days, or an in_progress claim silent for 2 days, as STALLED (needs action). Runbook: result-import.md regularization step. Branch claude/friendly-einstein-gf9z0h-regularization-gate.

## Notes

PR #831 (draft), head 71d4225e, hosted CI green. Local: --records pass (fc96ad5e), --sweeps pass, --edit 67/70 (pyright timeout under load, site_urls vs moved main #825, local bead store). Release no-change record by render (69 files identical). Open: owner's word or runs for 39/55/290/291 by 2026-11-09 (think-yk2h).
