---
type: is
id: is-01m0pjfzt5k0qy5nnrh9zr2phb
title: "SYNOPSIS.md: the technical root document, reconciled against its sources"
kind: task
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0nrh9z5aa3gc9fp6j0vgh05
created_at: 2026-08-23T05:46:31.109Z
updated_at: 2026-08-31T02:52:45.482Z
closed_at: 2026-08-31T02:52:45.470Z
close_reason: "Landed in PR #8: SYNOPSIS.md, tools/check_synopsis.py wired into test.sh as a gate step, and lp_cell.py brought to the lint floor and cross-checked against H-019's registered slopes."
---
The directory had six reports, two reviews, a plan spec, a runbook, a ledger and a defect log, and no single place saying what the project currently knows. explorations/packing/SYNOPSIS.md is that place: the problem from the ground up, a per-n account of where effort has gone, results by evidential tier, the registry read as confirmed/refuted/blocked, a roll-up of all ten rounds, and the defect record. It states results and points at the artifact carrying the detail.

It cannot be generated (most of it is judgement), so it is reconciled instead, the way ledger.py reconciles ideas.md. tools/check_synopsis.py checks six things: round verdicts against artifacts, hypothesis statuses against the ledger, effort totals and defect counts against their datasets, no artifact silently missing, and every relative link and heading anchor resolving. That last one closed a real gap: campaign/ledger.py walks links under campaign/ only, so the root document's ~45 references were unchecked. Verified against eight injected faults before wiring into test.sh.

Also on this change: lp_cell.py rebuilds the fixed-angle cell LP through constraint rows sqpack/quench.py does not share (sixteen per pair from corner pairs against the quench's one from half-extents), which is postmortem rule R1. Both agree on the cell optimum to 4.441e-16 and on H-019's one-sided slopes to three decimals.

PR #8.
