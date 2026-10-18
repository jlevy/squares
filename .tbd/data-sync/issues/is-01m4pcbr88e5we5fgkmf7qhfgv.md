---
type: is
id: is-01m4pcbr88e5we5fgkmf7qhfgv
title: "Import wand125 via evand: Valid7 in the Lean kernel (evand PR #6, merged 060c1a1), a kernel route to T-064's finite premise (no issue)"
kind: task
status: in_progress
priority: 3
version: 4
delegate: codex@spud10.local
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T21:02:08.136Z
updated_at: 2026-10-18T08:51:41.794Z
started_at: 2026-10-18T08:47:55.993Z
---
Found in the 2026-10-11 intake read of evand/square-packing (think-q655); nothing on GitHub asked. Commit 060c1a1 (2026-10-11T02:36:49Z) merges wand125's PR #6 to evand/square-packing, "ValidTilt7 / Valid7 in the kernel, s(k^2 - 3) = k for all k >= 6": a Lean kernel checker for the V3 pose tree of L4_k02_box7.txt and a bridge to box7Cover (lean/Sqpack/V7/, LemmaE*, CapK, KBern and 25 other modules, lean/VALID7.md, generators under lean/scripts/), with 45d8c39 and 5b69ce0 (a kernel checker for covers by a mixed point/segment/area measure). The merge message says the root modules and Main are generated from wand125's release data/valid7-lean-certs-v1, not in the repository, and that evand reviewed it statically on 10 October and did not rebuild it. 7dfca4e makes the checker opt-in (Sqpack.Valid7Checker), adds a spot check (tasks/pr6-valid7-kernel/spotcheck-2026-10-10.md) and sets the k2m3 status to "no hypothesis".

This is new evidence for T-064 (s(k^2 - 3) = k for k >= 6, V3/C3): its lower half today is Valid7 decided by two exact checkers (E-k2m3-evand-valid7-qx2-replay, E-k2m3-wand125-valid7-independent) and the Lean reduction from Valid7 (E-k2m3-evand-bentz-lean-build); a kernel proof of Valid7 would make the whole theorem kernel-checked. Runbook row: new evidence about a registered entry, no new entry; retain the merged lean/ tree at 060c1a1 or later with wand125's release data/valid7-lean-certs-v1, read the statement binding, and price a kernel build before any rung moves.

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): https://github.com/jlevy/squares/issues/537 (the sample or rebuild decision is on https://github.com/jlevy/squares/issues/543). Tracker https://github.com/jlevy/squares/issues/544.

2026-10-18 W1 intake (think-xmxb): #537 new author comment https://github.com/jlevy/squares/issues/537#issuecomment-6247112302 (2026-10-18T07:25:01Z): Valid7 v2 at wand125/square-packing 649a92042b4b79dda1eca1749c34029aee60990e, release valid7-lean-v2, library evand c5c7f00. Same theorem/standard axioms; 62626 generated files; same9800 roots with re-certified leaves. Author reports798 CPU-h, peak37GB module/51GB Main,29.4h on48vCPU. The component CPU figures quoted in comment do not sum to798: reconcile source receipt before accepting new budget price. No build here. Retain and audit version2 instead of offering only stale v1 cost. Draft acknowledgement: Thank you for the version2 source and updated compute figures. This is queued as new evidence for T-064; no rebuild or new rung is claimed. A full build remains subject to the recorded budget and machine decision.
