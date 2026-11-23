---
type: is
id: is-01m7x48wpcz40ejzsmwj32p7m8
title: "Validation: phase-two replay of superseded #1039 and #1041 lower-bound claims (~6.6–15 CPU hours)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: codex-intake-1119-01a1fb
labels:
  - validation
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T18:42:32.268Z
updated_at: 2026-11-23T01:21:05.620Z
started_at: 2026-11-23T01:20:56.600Z
---
Phase 2 of think-fv42's replay plan (receipts/controls-plan.txt in packing/resources/web/de-winter-lower-bounds-2026-11-19, SHA-256 cc6a1bf4... on think-fv42): the superseded claims of issues 1039 and 1041, held off the 20 November session by the owner's coordinator (wall time on the shared box).

## Validation
- Claim: Issue #1041's 32 superseded counts (proof/nNNN of lower_bounds_2026_11_19 at JoostdeWinter/square-packing 21d944c, all but n105 and n111) and Issue #1039's superseded counts (the issue-1039 zip's rectangles/evidence sets with integer rows other than partial_n19/20/26/37_4144, refined_n90/92_400 and the n82 sets, and heterogeneous/ other than n66, n83, n110). Checker: the source's kernels (bmcheck.cpp, octagon.cpp, gram.cpp) via devtools.replay_rectangle_receipts --source 21d944c/proof.
- Run: K1 on those folders (--workers 2 per runner, nice 19), then control Q (--mutant quarter --first-per-level) on each; P1 `verify.py --n N` at the folder top for each 1041 count; P2 the zip's verify.py.
- Cost: 5,452 G node-rectangles in the archived receipts (1041: 118.6M nodes, 1,408 G; 1039 square kernel: 539.6M nodes, 3,467 G; heterogeneous: 98.5M nodes, 577 G). Measured here on 20 November: 5.6 ns per node-rectangle for the octagon kernels and 3.9 for the square kernel on a quiet box (n114: 199 CPU-s for 1,406,930 nodes), 12.3 ns under load 11-16 (n109 of issue 1042: 2,506 CPU-s for 7.33M nodes x 27,808 rectangles). Estimate 6.6 CPU-hours quiet, about 15 contended.
- Budget status: runnable, under the 40 CPU-hour item cap.
- Possible subset under the cap: not needed.
- Prerequisite satisfied: PR #1051 merged the replay tool and source packet. PRs #1059 and #1073 retain the subsequent partial independent review and custody results.
- Done when: every archived direction of those folders is verified and equal to the archive, control Q refused on coverage everywhere, the receipts committed in the packet, and both issues' replay evidence widened to their whole scopes. Assign result identifiers only when the registry admission decision is made.
- Machine note: CPU only, about 50 MB of scratch; can share the machine with a gate.
