---
type: is
id: is-01m52241azyymmdhk8bsfcfyak
title: "PR #650 A1: chain #641 -> #650 is not a formal stack; link it or retarget #650 at merge"
kind: task
status: closed
priority: 1
version: 3
delegate: user-eb-addr-641-650
labels:
  - regularization
dependencies: []
parent_id: is-01m51pj9kng0mjpdpsw877d6v4
hold: null
hold_until: null
created_at: 2026-10-16T09:54:02.719Z
updated_at: 2026-10-16T20:34:46.111Z
started_at: 2026-10-16T09:54:12.566Z
closed_at: 2026-10-16T20:34:46.110Z
close_reason: "#641 merged first (68cdbc614), #650 was retargeted to main and merged at 321d492c7; the informal chain is complete."
resolution: null
duplicate_of: null
---
PR #650 Review A, finding A1 (High): https://github.com/jlevy/squares/pull/650#pullrequestreview-5544639580

#650 (branch claude/intake-2026-10-16-sweep-regularization) is based on #641's feature branch (claude/ecstatic-edison-8en33t-regularization-intake), but the two are not a formal GitHub stack: `GET repos/jlevy/squares/stacks?pull_request=650` and `?pull_request=641` both return `[]`. Under `tbd shortcut stacked-prs`, an informal chain is a High finding.

Not fixable from the addressing session: linking a formal stack needs the gh-stack extension, and `.claude/scripts/ensure-gh-cli.sh --with-stack` fails because the session proxy refuses the pinned gh-stack release download (verified by the coordinator at about 08:00Z on 16 October 2026). The chain is declared in both PR descriptions instead.

For the owner, at merge, one of:
- link the two as a formal stack (`gh stack link`, under the `github-stacked-prs` grant), then verify both through `stacks?pull_request=…`; or
- merge #641 first, then retarget #650 to `main` (it merges #641's head already, so the diff against main is then its own layer), let CI run on the retargeted base, and merge it.

Waits on: #641's merge (or a session where the gh-stack download works). Close when #650 has merged into main by either route.
