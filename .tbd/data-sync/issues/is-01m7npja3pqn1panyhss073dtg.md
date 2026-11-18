---
type: is
id: is-01m7npja3pqn1panyhss073dtg
title: "Apply option D (think-b0w5) at every count it settles: measure each re-certification against its predecessor shrunk to first contact (devtools.contraction_margin), record new result or restatement, and lift blocked:owner-decision on #939, #946 and #846 (think-ruu2, think-ikku, think-oqjd, think-5c9z; T-253, T-260, T-280, T-281, T-285, T-286; candidates at 130/293/307; regularizer optima)"
kind: task
status: in_progress
priority: 1
version: 8
delegate: w7r-optd-1118
labels:
  - intake
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-17T21:28:19.830Z
updated_at: 2026-11-18T05:13:03.298Z
started_at: 2026-11-18T02:28:47.344Z
---

## Notes

2026-11-17T23:10Z coord-intake-1117r: scope addition from the w5 audit: measure T-173 at 207 against T-147 shrunk to first contact (think-g0o4); 153 stays with the owner.

2026-11-18T03:05Z w7-optd-1118: branch claude/intake-2026-11-18-option-d (worktree /home/user/wt/w7-optd), WIP 7aa8012f8 pushed: schema field restatements + check_standing.restated (no improvement, no profile credit) + check_results.restatements_problems + RESULTS.md section + runbook/attribution/guide text + tests/test_restatements.py; receipts retained. Measured (devtools.contraction_margin, both routes): T-253 at 154,155,183,211,227,236,237,241,271 all 1.0000 within margin (restatements); T-260 at 105 0.0093, 146 0.0079, 156 0.0077, 229 0.0064, 308 0.0056 (restatements); candidates 130 1.1453 of T-259 (1.0297 of T-254, NEW), 293 0.0510 of T-257 (restatement), 307 1.0631 of T-256 (new, but T-279/T-326 lower: no candidate); T-173 at 207 0.9984 of T-147 and 0.1966 of T-167 (restatement, credit PingYou; identity one to one, max move 2.83e-4); existing: T-280 299 0.3472/303 0.9674, T-281 0.0896 (restatements), T-285/T-286 1.0399 (NEW). Coordinator rulings 18 Nov: keep restated entries as records of the report (no tombstone); apply D only to what think-b0w5 lists (T-259 etc. -> think-7k8p); T-285/T-286 new, adopt at 172/199 with regularization, S1 by #1023 precedent (rule -> think-mu3t); 130/303 classification only, registration to think-4z8z. Register/requests edits wait for #1023 (it changes results.yaml, evidence.yaml, result-requests.yaml, adopt_houses, select_houses, upper_bound_houses). Running: 631 (#719, #732 vs Couzo 4e4c8ce) for think-oqjd.

2026-11-18T03:52Z w7-optd-1118: pushed 7aa8012f8, 89fb6c547, 65951de3c (tooling: restatements field, check_standing.restated, check_results.restatements_problems, RESULTS.md section; contraction_margin through k L layers + dilation (measure_identity.read_l_layers) with tests; runbook/attribution/guide text; receipts). think-oqjd: Couzo 4e4c8ce 631 = 490 + 3 L layers dilated 1+1e-24, base margin 2.604763e-11; #719's 631 0.0105 (restatement), #732's 631 0.1318 (measured only, row stands; owner bead think-1ell; walks bead think-cwo0 blocked on it; take-out bead think-wtdz). 303 KKT (Daniel, regenerated) 1.0234 of T-278's margin: new, below the house -> think-4z8z with 130 (1.1453). Local branch w7-optd-prep (NOT pushed; waits for #1023, which changes results.yaml/evidence.yaml/result-requests.yaml/adopt_houses/upper_bound_houses): commit b76dbfef7 applies the register (T-173 207, T-253, T-260, T-280, T-281 restatements; T-285/T-286 V3/C3 with 4 evidence entries), requests (#846/#939/#946 unblocked, #573 153-only), check_requests RESTATED state, adoption at 172/199 (adopt_houses written). Scripts in scratchpad w7/tools/apply_{register,evidence,requests}.py. Running: atlas redraw for 172/199, then strong generators. Reply drafts in scratchpad w7/replies/.

2026-11-18T04:46Z w7r-optd-1118 (resumes w7-optd-1118 after the restart): committed the uncommitted SYNOPSIS/VERIFIERS renders (39c2a26da), case verifier sections at 172/199 + synopsis document map (ef868818f), merged origin/main 3ac78a55f into w7-optd-prep (3ceb5ce81; one conflict, test_check_requests docstring), pushed to claude/intake-2026-11-18-option-d-prep. #1023 still open (head ff07d4e69, validate red); option-d branch not yet folded. Next: trial merge with #1023's head to pre-resolve (SYNOPSIS, regularized/index.json, house-adoption-prior-state-2026-11-18.json.xz add/add, upper_bound_houses.py, INVENTORY, RESULTS, VERIFIERS, source-coverage.yaml, test_check_requests).

2026-11-18T05:12Z w7r-optd-1118: prep 30512e98d pushed to -option-d-prep (adds no-change record 2026-11-18-w7r-optd-1118-option-d.yaml, compare_paper_renders vs main 3ac78a55f: 55/43/43/43 byte-identical). Trial merge with #1023 head 0db1e5b4f resolved by scratchpad w7/tools/resolve_1023.py (index.json via carried_index, prior-state union, upper_bound_houses, source-coverage union, generated MDs theirs then render_evidence_inventory/verifiers/case_verifiers/results --update, render_results_headline, render_document_map); adopt_houses --check and atlas check pass. Still owed after the real merge: tests/test_house_adoption.py expectations at 172 (T-286) and 199 (T-285) (OVERTAKEN, the lifted-hold dict, 'later' in the custody-history test) and re-run 'python -m devtools.upper_bound_houses custody' (receipt houses); then records tier, stamp_landed, release_pin. PR body draft: scratchpad w7/pr-body2.md.
