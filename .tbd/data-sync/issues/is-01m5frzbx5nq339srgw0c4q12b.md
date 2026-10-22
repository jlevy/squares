---
type: is
id: is-01m5frzbx5nq339srgw0c4q12b
title: "intake_sweep: say a read at a pinned head can be removed only when no commit it covers is left unretained"
kind: bug
status: closed
priority: 3
version: 6
delegate: coord-intake-1021b
labels:
  - tooling
  - packing
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T17:43:34.564Z
updated_at: 2026-10-22T19:43:45.632Z
started_at: 2026-10-21T17:43:35.876Z
closed_at: 2026-10-22T19:43:45.632Z
close_reason: "Merged in #723 (4432f51b5, 22 Oct 19:43Z) with review A dispositioned (A1 fail-closed load guard, A2 comment count, A3 held-commit pass only when a packet pins the head)."
resolution: null
duplicate_of: null
---
repositories_section in packing/devtools/intake_sweep.py prints "<url>: a packet now pins <head>, so intake-watch.yaml's read of it can be removed." for every read through the head whenever the head is among the repository's pins. It never asks whether that packet's declared scope retains the paths of the commits the read covers.

Measured on 21 October 2026 by the read-only triage c-triage-sweep-1021b with the sweep's own read_history. franciscouzo/square-packing's read through 7b6c87e is the head; couzo-issue678-2026-10-18 pins it but retains 90 of its 543 changed paths. With the read removed, _unretained lists 7b6c87e again ("7b6c87e Land 85 verified packing bounds and source provenance"). Following the note turns a clean sweep red, and a pass that trusts it removes a read the record needs.

Fix: derive the hint from what _unretained already computes. Say a read can be removed only when the history read without it finds no unretained commit; otherwise print nothing, or say the read stays because N commits it covers change paths no packet retains. Add tests beside the existing intake_sweep tests: a pinned head whose packet scope omits one changed path keeps its read and gets no removal note, and one whose packet retains the whole tree gets the note.

Done when the franciscouzo case prints no removal note and the tests run in --fast. Price: 1 to 2 agent-hours, no CPU.
blocked_on: none

## Notes

2026-10-22 c-triage-1022b: a second case of the same defect, measured by the read-only
triage of the 12:20Z sweep.

- franciscouzo/square-packing's head `6b7391de` is pinned by `couzo-issue715-2026-10-21`,
  which has 359 paths in scope.
- The commits under it, `d09edd7`, `5a299b4` and `6b7391d`, change 11, 2,650 and 1,975
  paths; 5, 2,339 and 1,788 of them are unretained (tools/unretained.py, reusing
  `intake_sweep.watched_repositories` and `Packet.retains`).
- The planned Couzo history records PR adds a packet at `5a299b4` that retains 20 of
  those paths. Its read through `6b7391d` must stay after that packet lands, and any
  "can be removed" hint for it would be wrong.

2026-10-22 c-lane-tooling-1022: done in jlevy/squares#723 (draft, head de5179c76), awaiting hosted CI and merge; for the coordinator to close.

- `read_history` computes, with `_unretained`, the commits listed without a read through the head (`RepoHistory.held_by_head_read`). `repositories_section` says "can be removed" only when there are none. Otherwise it says "a packet pins <head>, but intake-watch.yaml's read of it stays: N commits it covers change paths no packet retains: ...". With an unreadable history it says neither.
- Test: `test_a_read_through_a_pinned_head_goes_only_when_nothing_it_covers_is_left_unretained`, over a real repository via `file://`, through `repositories_section`. A head packet omitting one changed path keeps the read; one retaining the whole tree gets the note; main's code fails the first. It runs in the ordinary suite (`--fast`).
- Live (read-only network). At 7b6c87e taken as the head, the read stays, holding 4 commits, 7b6c87e first. The second case above, with a read added at today's head 6b7391d (pinned by couzo-issue715-2026-10-21): the read stays, holding 6b7391d, 5a299b4 and d09edd7. Today's head has no read, so no note prints. The sweep separately reports those 3 commits as unretained, which is record work.

2026-10-22 c-lane-tooling-1022, #723 review A3 (`e35898d58`): the held-commits pass now runs only when a packet pins the head, and a read through an unpinned head holds nothing, which a test asserts. Head `09e3ba373`, hosted CI green. For the coordinator to close after merge.
