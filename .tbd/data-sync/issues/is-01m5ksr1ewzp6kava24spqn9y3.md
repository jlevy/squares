---
type: is
id: is-01m5ksr1ewzp6kava24spqn9y3
title: "Validate: chelokot's and Daniel's Lean proofs of s(2) to s(5) (think-7l2j), receipt-bound builds (<1 CPU-h)"
kind: task
status: in_progress
priority: 3
version: 7
delegate: bold-ritchie-l29
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T07:14:00.796Z
updated_at: 2026-11-02T11:52:31.506Z
started_at: 2026-10-26T11:21:28.603Z
---
Validation part of think-7l2j (chelokot's and Evan Daniel's Lean proofs that s(2) = s(3) = s(4) = 2 and s(5) = 2 + 1/sqrt 2; no issue). Created by c-lean-1023 under the 23 October intake epic, as the lane rules allow; it serves think-7l2j.

## Validation
- Claim: chelokot/square-packing-archive at 753079eb37d8d16225a5dc1f56e493a3c3b243f4: Records.Square5.s5_eq_goebel, NearSquare.s2_eq_two, s3_eq_two, SquareNumbers.s4_eq_two (Lean v4.33.0, Mathlib db584cd6); evand/square-packing at 7051f4eabf7f9b2509ad1e7cc296f57d19482027: rect2_iff, rect3_iff, rect4_iff, rect5_pts_lower, rect5_upper (Lean v4.33.1, Mathlib 0df444a3). Packets: packing/resources/web/chelokot-small-n-lean-2026-09-05/ and evand-rect-small-n-lean-2026-10-22/.
- Run: (a) from the chelokot packet's retained bytes, `lake exe cache get`, `lake build` of the three Records modules and a probe printing the seven theorems' axioms, under a receipt that names them (devtools.replay_chelokot_lean's pattern; the 2 October build of the whole archive already logged these axioms, build.log lines 330 and 338 to 343, but its receipt names only T-086's theorem); (b) from the rectangle packet, `lake build` of Rect, Rect3, Rect4, Rect5Pts and Rect5Pack and a probe of their axioms. Accept only the three standard axioms.
- Cost: under 1 CPU-hour in all (eight modules each, no certificates; an estimate from size).
- Budget status: runnable within a lane's 2 CPU-hour single run; needs two toolchains and two Mathlib caches, about 20 GB of disk, which the lane's host lacked on 23 October (5.2 GB free).
- Possible subset: either route alone.
- Depends on: the packets; the stage 4 review, which also reads the square-case step from the rectangle theorems (Fried4 at w = h < 2, and five squares in a side below 2).
- Done when: receipts are committed on a branch this bead names and registered as `replayed-here` entries on the register entry that think-4o9c's decision makes (T-237 is allocated and held), or the owner dispositions them.
- Machine note: small; not alongside a validation gate.

blocked_on: none

## Notes

2026-10-26 ~11:25Z w-val-1026 (moderate-tier sub-agent of coord-n12-1025, the 26 October intake review's validation lane): NOT STARTED, disk. The run needs two Lean toolchains (v4.33.0 for chelokot's 753079eb, v4.33.1 for Daniel's 7051f4e) and two Mathlib caches (db584cd6 and 0df444a3), about 10 GB each by the two packets' READMEs (chelokot-small-n-lean-2026-09-05/README.md lines 155-159, evand-rect-small-n-lean-2026-10-22/README.md lines 137-139): about 20 GB for both routes, about 10 GB for either alone. This host (four cores, shared) had 5.1 GB free on / at 11:21Z on 26 October (`df -h /`: 252G size, 34G used, 5.1G avail), so neither route fits; no toolchain (~/.elan absent) or Mathlib cache is present to reuse. CPU price unchanged: under 1 CPU-hour for both (an estimate from size). Runnable on a host with at least 12 GB free for one route or 22 GB for both; nothing else blocks it. #786 stays open on it (review track: it closes only when T-238 is confirmed or refuted).

2026-11-02 ~11:50Z bold-ritchie-l29 (strong-tier lane L29 of the 31 October intake pass, think-3guf; claimed 11:13Z): NOT BUILT, network policy. Disk was no longer the bar (15 GB free on a four-core host). Two hosts are refused by this environment's proxy, each CONNECT answered 403:
- release.lean-lang.org:443, elan 4.2.4's origin for official toolchains (`elan toolchain install leanprover/lean4:v4.33.0` failed). The same release as a GitHub asset downloads: lean-4.33.0-linux.tar.zst, 574,882,764 bytes, SHA-256 4b3fb03c29a1e0a253fb1d11f9bae3725f19a0dc6fc09b3ea16d2c9df3349e2c, whose `lean --version` names commit d8b18978322de05a8f3dba51ef03cf5461676c17, the v4.33.0 tag's by `git ls-remote`; it was linked into elan as leanprover/lean4:v4.33.0, then removed.
- lakecache.blob.core.windows.net:443, Mathlib's prebuilt cache. `lake exe cache get` in chelokot's staged formal/ cloned Mathlib db584cd6 and its eight dependencies from GitHub, then downloaded 0 of 309 attempted files (of 8,690) before it was stopped.
Without the cache each route needs Mathlib built from source (Daniel's Basic.lean imports all of Mathlib; chelokot's closure imports its calculus modules), far above this bead's price, so nothing was built, per the brief (report the block, do not work around it).
What landed, on claude/bold-ritchie-xo28us-l29 (draft PR https://github.com/jlevy/squares/pull/887): devtools.replay_lean_packet, with routes chelokot-small-n and evand-rect-small-n. `stage` writes each project from the retained bytes (both ok: every module at the closure receipt's upstream Git blob, pins at the receipt's toolchain and package revisions, 0 kernel-escape tokens); `run` does lake exe cache get, lake build of the route's modules, a probe of the theorems' axioms (accepted only as propext, Classical.choice, Quot.sound) and three negative controls each (a mutated statement given the theorem's term; a module copy with one statement made false: s5_ge_goebel's side + 1/100, rect5_pts_lower's a + b < 4 + 2√2; the statement proved by sorry), under devtools.replay_receipt, with --cpus for taskset; `check` validates the receipt offline. The controls are written but have never run against Lean.
To finish, on a host that reaches the cache: from packing/, `.venv/bin/python3 -m devtools.replay_lean_packet stage chelokot-small-n --out W1`, then `run chelokot-small-n --out W1 --cpus 2,3` (receipts go to the packet's receipts/lean-build by default), and the same for evand-rect-small-n with W2; then the replayed-here proof-assistant-checked evidence entries on T-238 and a control path, and let check_results derive the rung. Price unchanged: under 1 CPU-hour for both, an estimate.
No reply is owed on #786: no rung moved. Draft, if the coordinator wants a status line there: "The receipt-bound builds of both routes are not yet run: Mathlib's prebuilt cache is outside the network policy of the host that tried on 2 November. The build tool is in #887; T-238 stays V0/C0."
blocked_on: network policy — lakecache.blob.core.windows.net:443 (Mathlib cache), release.lean-lang.org:443 (elan)
