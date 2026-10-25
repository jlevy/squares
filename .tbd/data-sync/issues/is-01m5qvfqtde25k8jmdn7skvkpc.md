---
type: is
id: is-01m5qvfqtde25k8jmdn7skvkpc
title: "W8: a maintained checker for the two-strip L-packing family (#799), with #799's packet and requests entry"
kind: task
status: in_progress
priority: 2
version: 2
delegate: c-w8-two-strip-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5qsa2jj6mf8cgemykzyy109
hold: null
hold_until: null
created_at: 2026-10-24T21:01:23.661Z
updated_at: 2026-10-25T04:16:26.130Z
started_at: 2026-10-25T04:16:26.129Z
---
Code slice from c-triage-799-1024's triage (scratch triage-799/: import-plan-799.md, scripts/, work/two-strip-decide.json). Decide a two-strip L-packing (Ryu's Theorem 1.3 shape: tilted rows on the bottom wall, tilted columns on the right wall, axis grid elsewhere, rational tan(a/2)) exactly from its parameters: strip lemma, region separation, capacity count; controls capacity+1, a side 1e-15 below the binding fit inequality, mH+1, tH=0 (W7's one-unit-below control does not carry over: slack >= 1.13e-8). Also stage 2: retain Zenodo 10.5281/zenodo.23624433 V1.0's 58,338 bytes (records.csv, README, regenerate.py as text) and the issue text as packet karimi-two-strip-2026-10-24, and add #799's result-requests entry (triage: pending). Rows wait for R1's walk above 1024 (think-llit). Price: checker < 0.1 CPU-h; exact replay of all positives on both routes plus six controls at one count per K about 0.8 CPU-h, run when the rows land.
