---
type: is
id: is-01m4pzx1eqrs8xrz662319ty8k
title: Narrow the negative-control copy-back to links a control checks (about 14.4 MB of archive files)
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-12T02:43:37.559Z
updated_at: 2026-10-15T04:29:09.738Z
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

## Notes

2026-10-15, PR #611 https://github.com/jlevy/squares/pull/611 (branch
claude/wizardly-meitner-wqn4x3-snapshot-b6ir, head 227c345eb).

Snapshot: 226,344,073 bytes on main 6964362b5 (148,343 headroom) -> 212,287,522 bytes on the
branch (14,204,894 headroom), under the unchanged 216 MiB cap. The selection saves 14,082,212
bytes; the branch's own files add 25,661.

Rule: the copy-back follows links only out of the documents a registered control link-checks
in a worker. Those are campaign Markdown (`ledger check`), README.md and SYNOPSIS.md
(`check_links`), listed as `LINK_CHECKED_DOCUMENTS`. Declared paths still return: the results
register, plus each defect's `recorded_in` (new, `defect_pruned_targets`).

Six readers reached workers only through dropped links, and each is a declared input now:
- the wall workflows (`wall_workflows()`, from gate-budgets.yaml);
- the n11 review (fragment links, think-wzmf);
- two `recorded_in` papers;
- the kingbird-29 provenance SVG (12 promote and witness-interval controls);
- three verifier-registry paths;
- two squish-401 normalized claim records (`squish_upper_bound_packets check`, run in
  `test_fn1_input_bindings`' worker).

New tool: `run_negative_controls --baseline FILE [--baseline-command CMD]`. Before and after,
all 50 distinct registered commands print the same unmutated in a worker, wall times and one
lease timestamp aside. `check_documentation` in a worker gains exactly the dead links of the
dropped files, since no control runs it. Controls: 174/174 fire at -j 3.

Release: `release.py` carries a reviewed no-public-change record for the four papers and the
site; the runner is in their import closure only via `upper_bound_houses.custody`.

Close on merge.

2026-10-15, review A of #611 (A1): Done-when amended for `check_documentation`.

As written, the criterion asked that unmutated `check_documentation` "print the same in a
worker before and after". It cannot, by the design of this bead. No registered control
runs `check_documentation`, and it is the one checker that follows the links of
reviews, research and guides. Those are exactly the links the narrowing stops carrying
into workers. They are still checked in the real checkout, where `check_documentation`
runs as a gate step.

The amended criterion: in a worker, unmutated `check_documentation` loses no line, and every
line it gains is a dead link to a dropped file or to a pruned directory that only a review
links.

Measured at the final selection (`--baseline-command`):
- 270 distinct lines before, and none lost after.
- 380 lines gained: 362 dead links to all 225 dropped files, and 18 links to pruned
  directories that were recreated empty before.

The other four commands (`check_readme`, `check_gate_budgets`, `ledger check` and
`validate_schemas`) print byte-identical output before and after.

Final figures at the review-A head: 212,294,894 bytes, 14,197,522 under the cap. The
selection saves 14,082,212; the branch adds 33,033.
