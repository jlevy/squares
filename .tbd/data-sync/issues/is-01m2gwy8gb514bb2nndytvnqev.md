---
type: is
id: is-01m2gwy8gb514bb2nndytvnqev
title: Throw away the confused annealing material; keep only what survived checking
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-14T21:25:01.570Z
updated_at: 2026-09-14T21:25:15.346Z
---
Owner, 2026-09-14: "let's thoroughly edit and throw away the confused information, and make sure none of the code that was making that mistake about not checking the run arrangement as a packing is removed."

The 2026-09-13 reconciliation preserved every superseded claim under dated corrections, so X-029 and exp-207..210 each read as a correction, then an "original account", then a correction inside the account. A reader cannot tell what is true. The owner's direction replaces annotate-and-preserve with remove-and-point: each artifact now states only what survived checking, with one line pointing at `a40d272c` for the previous text.

Scope, all on claude/annealing-search-benchmark:
- X-029 rewritten from the ground up: blind is record-conditioned; the runs were not packings; what repaired runs are worth, from `resolved: true` cells only; what is not established.
- exp-207, exp-208, exp-209, exp-210 rewritten; frontmatter values corrected where they were mislabelled (exp-210's medians were the minimum and an endpoint; exp-208's control was level 3, which was never measured; exp-207's control median was seed 0's value).
- exp-207/208/209 slugs renamed with repren so filenames stop asserting withdrawn claims.
- H-206 retired (its premise was an overlap artefact), idea 164 noted as retired on the board; H-207..211 bodies stripped of unchecked numbers.
- Runbook's retained-record section rewritten.
- Ledger regenerated; `packing-ledger check` passes.

Code: nothing removed. summaries.json kept whole (PR #160's historical_summary_audit test reads it).
