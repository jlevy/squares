---
type: is
id: is-01m4xmr0fhhynbfzj5vj0sh358
title: "Import Mishapolk 70a033f (no issue): 12 KKT refinements below best now at n = 129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304; 207 undecided"
kind: task
status: open
priority: 1
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
child_order_hints:
  - is-01m4xpwd1rtgx6ht2cqfm4qbm7
created_at: 2026-10-14T16:43:19.409Z
updated_at: 2026-10-14T17:21:12.762Z
---
Mishapolk/square-packing-records 70a033f (2026-10-14T16:11:31Z), 7 commits past #593's pin 46f638c. No issue reports it. Commit message: 'Refine 14 contested certificates to ultra-precision KKT endpoints'. census.json credits 14 counts to Mykhailo Polkovskyi and 10 re-cut counts to 'Antigravity'.

Exact comparison against ledger.json best now (triage 2026-10-14, scratchpad triage2/scripts/misha.py):
- Below best now: 129 (1.1e-21 below PR #574), 154 (1.29e-19 below #586), 156 (1.19e-34), 175 (7.2e-75), 176 (1.3e-94), 204 (1.8e-21), 232 (1.5e-74), 264 (1.8e-74), 271 (2.1e-34), 302 (1.79e-19 below #583), 303 (2.4e-74), 304 (1.79e-19 below #575). Each is a refinement of the packing named in the ledger.
- Undecided: 207, 1.46e-41 over PR #574's 40-place print. Deciding it needs PR #574's degree-5 root past 41 places.
- Not below best now (read note only): 153, 155, 181, 209, 267, 270, 272, 305-308.

Owner decided 2026-10-14: counts from first commit. It enters in report order at its first commit, after every report already in the ledger, so it changes no existing verdict, only adds rows. Validation: think-j7f1 (24 certificates, ~0.8 CPU-h, runnable).
