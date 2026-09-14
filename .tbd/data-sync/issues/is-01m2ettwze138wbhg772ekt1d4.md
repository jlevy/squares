---
type: is
id: is-01m2ettwze138wbhg772ekt1d4
title: "Land sibling PR #157 on main after the stack merge"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - pr
  - landing
dependencies: []
parent_id: is-01m2etr75jfh3t3ry7kj1ccqrb
created_at: 2026-09-14T02:09:45.451Z
updated_at: 2026-09-14T02:27:12.838Z
---
Land sibling #157 (weighted five-site threshold atoms, stages 1–2; head 382944dd) after the stack merge retargets it to main.

Remaining before merge:
- Post the result of #157's local 74-step checkpoint on 382944dd and the final disposition comment (think-zo70 notes say it waits on this).
- Close or re-scope think-6dca (MATH-05 accepted, awaiting final validation) and think-v38h ("resolve failing PDF build check": Pages is green at 382944dd; root cause stays under think-ptit); then think-zo70.
- The launch supplement still says "Status: draft for exact-head review under think-99bz" although think-99bz closed 2026-09-13 23:49Z; with BC329 calibration deferred (think-zwlf) it stays a retained, unexecuted procedure — correct the status line or say so in the #157 description.
- After retarget: fresh required CI on the new base, then dispatch `Deferred checkpoint` with pull_request: 157 against the new main.
- Reconcile SYNOPSIS "selected next entry": #157 names think-8c9e, the chain names BC329 admission (think-qw9w). Whichever lands second reconciles and re-runs fast CI; note the suite budget child.
- `git merge-tree` of #166 with #157 was clean at 2026-09-14 02:00Z; the only shared files are SYNOPSIS.md, docs/project/document-map.yaml, the active daytime plan, packing/campaign/ledger.md, and packing/devtools/controls.yaml.
