---
type: is
id: is-01m4v6r1jm45jcx80wqastveke
title: "Re-run regularized_drawings after #578 or #585, whichever lands second, and state question 16 in attribution.md"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-13T18:00:11.601Z
updated_at: 2026-10-13T18:00:11.601Z
---
Follow-up from Review A (round 1) on jlevy/squares#585, finding A8.

#578 is open against main and edits packing/devtools/render_case_pages.py and packing/devtools/result_credit.py, both of which #585 (the credit layer, top of formal stack 498) also edits: #585 adds the case page's regularization line (_regularization, labelled "Regularized drawing" or "Regularization") and makes result_credit.regularization_sentence name `modifications` and `modifications_unrecorded`.

Whichever of #578 and #585 lands second:
- resolves the overlap in those two files, keeping both changes;
- re-runs `python -m devtools.regularized_drawings` (writes results.yaml's regularized_drawings block, the `modifications` of T-154's own regularizations, and the `regularization` field of the 133 case records) and `python -m devtools.render_results --update`, then confirms `regularized_drawings --check` and `render_results --check` hold;
- states the owner's rule of 13 October 2026 (docs/project/policies/regularization-policy.md, section 9, question 16) in attribution.md: a pure regularization, one that proves no new bound, is never a result but is a credited part of the frontier record; a regularization whose exact side proves a new upper bound is registered as a result; this project's modifications to Evan Daniel's regularizer are named wherever his regularizer made the view.

Done when the second PR merges with both checks green and attribution.md carries the rule.
