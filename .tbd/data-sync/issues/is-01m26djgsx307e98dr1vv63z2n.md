---
type: is
id: is-01m26djgsx307e98dr1vv63z2n
title: Lapsed session-099 deadlines are failing every pull request now
kind: bug
status: open
priority: 0
version: 1
labels: []
dependencies: []
created_at: 2026-09-10T19:44:03.901Z
updated_at: 2026-09-10T19:44:03.901Z
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
