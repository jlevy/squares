---
type: is
id: is-01m4kraefdygkg3wkdwegf6vfw
title: "check_requests --draft: fix the seven defects the 2026-10-10 reply drafts had to rewrite"
kind: bug
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
child_order_hints:
  - is-01m59f4zkye3agw7a31k3a885t
created_at: 2026-10-10T20:33:24.973Z
updated_at: 2026-10-19T06:56:26.238Z
---
`python -m devtools.check_requests --draft N` produces stage 7 status comments that the 2026-10-10 reply lanes had to rewrite every time. Defects found (think-mtwe's notes record the first three; lane L27 of the 2026-10-10 pass found the rest):

1. The RECORDED wording ("nothing has been read or replayed here yet") is printed for entries that were replayed (T-128, T-130).
2. Numbers are glued to words where result-requests.yaml claims are interpolated.
3. `.:` appears where a claim's full stop meets the template's colon.
4. Its "how confirmed" text names `devtools.upper_bound_reports` and `evand_arrangement_reports` as independent re-verifiers. For #470 `upper_bound_reports` generated the witness (review RK-4), and the review says the adapter decides nothing.
5. For #476 and #488 it says "independent implementation" and drops RI-4/RL-5: one maintained route is the producer's own copied checker (the evidence entries' limitations record this).
6. It never says the case records are unchanged pending house adoption (PR #403, think-fvz4), never reports a case lane that did move (n-040 under T-145), and does not report superseded beyond-horizon rows (#484's 343/344).
7. `--draft N` refuses with exit 2 ("HEAD is not contained in origin/main") on an unmerged intake branch, so a lane cannot see the ledger's view of a reply it is drafting for after the merge; L27 called `check_requests.draft()` from a scratch script instead.

Done when `--draft` output for the ten 2026-10-10 issues (#470, #471, #476, #481, #483, #484, #485, #486, #488, #489) needs no factual rewrite, with tests for each defect, and `--draft` has a way to render against a named branch head.

## Notes

2026-10-15, evening intake pass (think-wnsv), lane D (think-ykg6): the sweep read item 6, "the case records are unchanged pending house adoption (PR #403, think-fvz4) ... (#484's 343/344)", as a wait, and reported #484 (closed 2026-10-12) as resolved. Those are context, not waits: nothing blocks this bead, and it can be worked now. Which of the seven defects `check_requests --draft` still has was not re-checked here.

blocked_on: none
