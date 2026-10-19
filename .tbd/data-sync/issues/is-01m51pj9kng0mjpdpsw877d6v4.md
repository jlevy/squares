---
type: is
id: is-01m51pj9kng0mjpdpsw877d6v4
title: "Intake sweep: report regularization debt (pending counts and owed decisions with their beads), and make regularization a standard step for every new house"
kind: task
status: in_progress
priority: 1
version: 9
delegate: user-eb-reg-intake
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
child_order_hints:
  - is-01m52241azyymmdhk8bsfcfyak
hold: null
hold_until: null
created_at: 2026-10-16T06:32:07.029Z
updated_at: 2026-10-16T10:24:31.297Z
started_at: 2026-10-16T06:32:14.332Z
---
The owner, 2026-10-16 (overnight, to coordinator user-eb, epic think-hg5s): "The other agent had worked on regularization, but we should make sure all of the intake process covers the regularization and we update that for any other new packings we have. That should be part of our standard process to do the regularization."

Stacked on #641 (think-g3q7), on branch claude/intake-2026-10-16-sweep-regularization:

- packing/devtools/intake_sweep.py gains a regularization source/section reading packing/atlas/known-best/default-drawings.json and default_drawings.PENDING_ALLOWED / SETTLED / owed: each pending count with the bead that owns it (needs action when that bead is not open/in_progress/blocked, or the count is pending and not allowlisted); each decided-no-better count whose decision still owes work, with its bead; a summary line of counts by state. JSON output and tests (tests/test_intake_sweep*.py) as for the record-side queues.
- packing/campaign/result-import.md ("Running an Intake Pass" steps 1-3, "The Prompt", stage 0's list, stage 3/5): every new packing that becomes a house (an adoption from any import: register results such as T-174 or T-186..T-190 when adopted, Kingbird catalogue intake, exact re-solves) is regularized in the same PR or allowlisted with an open bead, and the sweep lists what is owed.

Done when: draft PR open with base = #641's branch, labels project + S2, CI green; `python -m devtools.intake_sweep --offline` lists today's 20 pending counts as owned by think-la7h/think-kpm3/think-3zi3 and nothing as needing action. Closes at merge.

## Notes

2026-10-16T06:40Z user-eb-reg-intake: branch claude/intake-2026-10-16-sweep-regularization pushed, head 5e432e0dc, stacked on #641's head 46562eab0: bdd215034 intake_sweep Regularization owed section + 5 tests; 5e432e0dc runbook (pass steps 1-3/8, Prompt 2-4/9, sources table, stage 0 bullet, stage 5). intake_sweep --offline: 20 pending owned by la7h/kpm3/3zi3, nothing needs action, exit 0. Next: draft PR (base #641 branch, labels project + S2), records tier, CI.

2026-10-16T06:53Z user-eb-reg-intake: draft PR https://github.com/jlevy/squares/pull/650 opened (base claude/ecstatic-edison-8en33t-regularization-intake = #641, head 226e2b0ef, labels project + S2). Local: 113 focused tests passed; records tier 52/52 (247 s); intake_sweep --offline exit 0, 20 pending owned by la7h 9/kpm3 8/3zi3 3, none needs action. Next: CI to green. Closes at #650's merge.

2026-10-16T07:24Z user-eb-reg-intake DONE for this lane: #650 (draft, base #641's branch, labels project + S2) head 89cc59e83, CI green (Packing validation run 38865724793; first run 38863767816 failed only on a frontend Chromium hang in overview_data.load, re-run by an empty commit). Closes at #650's merge, after #641.

2026-10-16T09:56Z user-eb-addr-641-650: addressing Review A on #650. Merged #641's head e9d5c01d8 (f517ede2a); pushed 67fb92456 (A2 tests: decisions, exemptions, missing bead; A4 broken record/index reported, not a traceback) and eb8dea201 (A3 one owning-bead label). A1 (not a formal stack) deferred to think-bb70. Next: PR bodies (#650 A5 and chain declaration, #641), CI, replies.

2026-10-16T10:15Z user-eb-addr-641-650: #650 addressed at a82415d23 (merges #641's 7aa4775ea). CI green (14 success, 43 skipped; Packing validation run 38883863154). Description and title updated (A5, chain declared). Disposition reply: https://github.com/jlevy/squares/pull/650#pullrequestreview-5546267959. A1 deferred to think-bb70 (open until #650 is in main).

2026-10-16 ~10:40Z coordinator: PR #650 MERGE-READY at a82415d23 except Review A's A1 (High: informal chain, not a formal GitHub stack), deferred to think-bb70 because the session cannot install gh-stack; merge after #641, retargeted to main. All other findings fixed; CI green.
