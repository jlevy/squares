---
type: is
id: is-01m4pzx1eqrs8xrz662319ty8k
title: Narrow the negative-control copy-back to links a control checks (about 14.4 MB of archive files)
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-12T02:43:37.559Z
updated_at: 2026-10-15T01:36:13.902Z
started_at: 2026-10-15T01:36:13.902Z
---
On 2026-10-12 the owner raised `SNAPSHOT_MAX_BYTES` in
`packing/devtools/run_negative_controls.py` from 200 to 216 MiB, in the intake session,
after intake 2026-10-11 layer 2 (PR #516, 1e41643e8) measured 210,099,865 bytes, 384,665
over 200 MiB. The lane that looked found no safe prune: the new packets are
results-register artifacts that workers read, and the larger files of the walk are
linked, registered, or read by controls. The raise answers that breach; this bead is the
saving that was found and not taken.

The saving: `linked_pruned_targets` copies back every file under `LINKED_PRUNE_ROOTS`
that a scanned document links inline, including archive files under
`packing/resources/` linked only from root documents, `docs/` reviews and research that
no registered control link-checks. The 2026-10-12 lane measured about 14.4 MB of that
copy-back (the log above `SNAPSHOT_MAX_BYTES` recorded 16.6 MB copied back for this
reason on 2026-10-09, 12 MB of it from the archive). Narrowing the rule to links a
control actually checks would take those bytes out of every worker.

Two hidden readers have to be fixed first, because today they reach workers only
through that copy-back:

1. `check_gate_budgets` opens `.github/workflows/pages.yml` and
   `.github/workflows/packing-validation.yml`, the two workflows its wall register names.
   They reach workers only through the link in
   `docs/project/reviews/review-2026-09-12-workbench-stack-architecture.md` and through
   `defects.md`'s links. They need to be an explicit input (for example
   `COPY_SEPARATELY`), not a side effect of a review's links.
2. `ledger check` stats the original n11 review, which campaign Markdown reaches only
   through `#fragment` links that `INLINE_LINK` does not match. That is think-wzmf.

Done when: both readers are explicit inputs; the copy-back rescues only targets linked
from documents a registered control link-checks, plus registered evidence;
`packing/tests/test_snapshot_link_consumers.py` is updated to the narrower custody; all
registered controls fire (`run_negative_controls -j 3`); unmutated `check_readme`,
`check_gate_budgets`, `ledger check`, `validate_schemas` and `check_documentation` print
the same in a worker before and after; and the measured saving is recorded in the log
above `SNAPSHOT_MAX_BYTES`, with the cap left where the owner set it unless the owner
decides otherwise.
