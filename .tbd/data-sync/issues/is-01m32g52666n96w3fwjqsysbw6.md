---
type: is
id: is-01m32g52666n96w3fwjqsysbw6
title: "Encode a wall-clock ceiling on routine gates: no unselected delay beyond a few minutes"
kind: task
status: closed
priority: 0
version: 2
labels: []
dependencies: []
parent_id: is-01m32fgxn7yh0skf12a0zxnres
created_at: 2026-09-21T17:27:52.770Z
updated_at: 2026-10-06T08:45:10.348Z
closed_at: 2026-10-06T08:45:10.348Z
close_reason: "Done: OR-17 'Every routine gate has a wall ceiling, and anything above it is selected on purpose' is in operating-rules.md (and AGENTS.md) on origin/main via PR #212 (merged 2026-09-21), with ci_gates walls in packing/devtools/gate-budgets.yaml and devtools.check_pr_wall."
resolution: null
duplicate_of: null
---
Owner directive, 2026-09-21: 'We should never have routine delays of more than a few minutes that are not consciously selected as needed checks via a systematic process. Having routine 45-minute or even 10-minute runs is not acceptable. It delays all serious progress. That should be encoded in our systems.'

This is stronger than what the rules currently say and the gap is why today happened. OR-13 governs WHERE a check runs (every fast check in CI, only the unavoidably slow ones leave). OR-14 says a development cycle is never artificially slow and sets 2 to 2.5 minutes for the pull-request surface. Neither puts a ceiling on a gate that has already left the fast surface, so the deep gate grew to 2674s with nothing watching, and a label-gated 45-minute wall sat on the merge path unremarked.

What to encode, none of it done yet:
1. A wall-clock ceiling per routine gate, not only a step-time budget, with the deferred/deep surface inside it rather than exempt by virtue of being deferred.
2. Any gate above the ceiling must be CONSCIOUSLY SELECTED per invocation and the record says who selected it and why. A label that silently costs 45 minutes is not a conscious selection; it looks like a checkbox.
3. Drift enforcement on the CI jobs themselves, the way gate-budgets.yaml enforces local tiers. The exhaustive-tier job at 2674s against its own declared 1943.05s is 1.38x and no rule reads it.
4. A rule that a gate is never re-run on a tree already decided. Today's second deep gate ran 45 minutes on a byte-identical tree (91a2ed86...) that run 35579234418 had already passed; that alone was the whole wall of the merge.

Deliverable is an amendment to operating-rules.md, since AGENTS.md is generated from it, plus the enforcing control. OR-15 says process is revised on a cadence rather than on irritation, so this belongs in the efficiency block think-zmos rather than as an ad-hoc edit.
