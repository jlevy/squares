---
type: is
id: is-01m4fzyh9p9bz01rgq7wpx4vwr
title: "INLINE_LINK in run_negative_controls ignores #fragment links (latent worker-copy hole)"
kind: bug
status: in_progress
priority: 2
version: 4
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: claude-code@vm
labels:
  - n-17
dependencies:
  - type: blocks
    target: is-01m4pzx1eqrs8xrz662319ty8k
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-09T09:29:45.526Z
updated_at: 2026-10-15T03:20:02.863Z
started_at: 2026-10-15T01:36:13.093Z
---
INLINE_LINK (\]\(([^)#\s]+)\)) never matches links that carry a #fragment, so link rescue misses files reached only through fragment links. ledger check stats docs/.../n11_research_review.md, reachable from campaign Markdown only via #fragment links; it is in workers only because one review links it without a fragment. If that link changes, ~35 ledger-check controls go red. Found during #464 prune tracing (scratchpad 464-prep). Fix: match fragment links (strip the fragment) and add a control.

## Notes

2026-10-15, PR #611 (branch claude/wizardly-meitner-wqn4x3-snapshot-b6ir, commit c4a23fd80).

`INLINE_LINK` is now `\]\(([^)#\s]+)(?:#[^)\s]*)?\)`: it captures the path before a `#`, and a bare
`(#section)` still matches nothing. On main 6964362b5 it rescues no new file, because a `docs/`
review linked the n11 review bare. Under think-b6ir's narrowing, that review link no longer
counts, so X-017's fragment links are what keep the review in workers.

Control: `tests/test_snapshot_link_consumers.py::test_fragment_links_rescue_their_target` fails
on the old pattern. `test_every_pruned_target_the_ledger_resolves_reaches_a_worker` reads campaign
links the way `ledger check`'s `dead_links` does, and requires every pruned target it resolves to
reach a worker. `ledger check` is also held green in a worker by `GREEN_BASELINE_COMMANDS`.

Close on merge.
