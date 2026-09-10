---
type: is
id: is-01m26djgsx307e98dr1vv63z2n
title: Lapsed session-099 deadlines are failing every pull request now
kind: bug
status: open
priority: 0
version: 2
labels: []
dependencies: []
created_at: 2026-09-10T19:44:03.901Z
updated_at: 2026-09-10T20:48:04.077Z
---
The lapsed session-099 deadlines are no longer a future problem; they are failing builds now.

Measured on 2026-09-10:

- PR #148's `Packing validation` run failed at its head committed 17:56:48Z with exactly
  `FAIL session-099-atlas-expansion-to-324.md: in-progress session deadline_at has passed`
  and the same line for workflow phase 4. Nothing else failed.
- `packing-ledger check` reproduces both locally at any HEAD committed after
  2026-09-10T13:50:00Z, and nothing else fails. At main's tip `3a18a05a`, committed
  01:10:02-07:00, it passes -- which is why main is currently green and why the next merge
  to main will not be.

So every contributor's pull request and the next push to main are red until one of the two
documented closeout routes lands. The ledger judges an in-progress deadline against HEAD's
committer date (D-468), so waiting does not help and no commit can avoid it honestly.

think-5hak records the terminal-unmeasured marker as designed and locally green, under the
name `resource_usage_unmeasured`. It is on no origin branch: `git log --all -S
resource_usage_unmeasured` hits only tbd-sync commits. This bead exists to carry the
observed impact and the evidence, not to duplicate that work -- a second implementation of
the same state would collide with it.

## Notes

Status at 2026-09-10T20:50Z: the repair is pushed and its own gate agrees, but it is not landed.

PR #150 (`codex/n11-daytime-strategy`, draft) carries it: session-099 is `status: stopped` with
`resource_usage_unmeasured: {reason: native_harness_data_unavailable, ...}`, plus 46 lines of
`agent-session.schema.yaml` and 124 of `check_session_rollups.py`.

- Its `validate` **passes**, which is the proof the design clears this block: `campaign record`
  is green on a commit stamped well after 13:50Z.
- Its `suite` **fails** on one test:
  `FAILED tests/test_session_rollups.py::test_agent_session_schema_allows_that_post_certification_state
  - KeyError: 'certification_pending'`, with `1 failed, 4899 passed`. The design note on
  think-5hak says the marker "no longer requires certification_pending", so the schema's
  conditional moved and that test still reads the old key. It is the last thing between the
  repair and a green PR.

So every other PR stays red until #150 lands. PR #149 is in that state now and says so.

Not ported into #149, deliberately. Porting the repair would clear `campaign record` there and
then fail `suite` on this same test, trading one red check that is demonstrably external for one
that #149 would own, and duplicating a governance change already in flight. When #150 lands, the
other branches need only merge main and re-run.

Two labelling risks worth settling while #150 is still open, both from reading the consumers
rather than guessing: nothing in the project counts a missing rollup as zero cost -- every
consumer refuses or skips, and `close_session.sum_rollups` totals receipts on disk rather than
summing sessions -- so the arithmetic is safe. What is not safe is the label.
`close_session.py` emits one `sessions_unmeasured` integer that would then carry three different
facts (44 pre-field, live-awaiting-receipt, terminal-unmeasured), and its generated reason falls
through to `"declares no rollups"` for a marker-bearing session, which is indistinguishable from
a silent omission -- the state the marker exists to make visible. The hand-written prose at
SYNOPSIS.md that explains the count names exactly two categories and would become false; that
same display defect was filed and closed once before (2026-09-06, PR 103) by fixing the prose
rather than splitting the count, which is why it recurs. Split the counter this time.
