---
type: is
id: is-01m70ga6b62h1z8an6d5ynxges
title: "Stage 4 blind review of #935, #936 (Özden's s(172), s(270))"
kind: task
status: closed
priority: 1
version: 10
delegate: bold-ritchie-l72-review
labels:
  - intake
  - review
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-09T15:54:59.302Z
updated_at: 2026-11-09T16:56:12.007Z
started_at: 2026-11-09T15:55:07.051Z
closed_at: 2026-11-09T16:56:12.007Z
close_reason: "Blind stage-4 review of #935/#936 done: both accepted (F15 minor on L71's wording, rest notes); clean-room checker ACCEPT; LANE_EQUALS_REVIEW; branch claude/bold-ritchie-xo28us-l72-review head 7f4301070, to be folded into L71's PR (think-he66)."
resolution: null
duplicate_of: null
---

## Notes

L72 (bold-ritchie-l72-review), stage 4 blind review of #935 (s(172)) and #936 (s(270)).

2026-11-09T15:56Z start. Branch claude/bold-ritchie-xo28us-l72-review cut from origin/main ef1af4933.
Clones (untrusted, nothing run from them): kenaznia-doga/s172-upper-bound @ 2ce1f7c7 (tree d9ae3f41),
kenaznia-doga/s270-upper-bound @ 78ab8cec (tree 5eaba28c); one parentless commit each.
Certificate SHA-256s equal the issues': 0df5ae79... (172), f2b62bf0... (270).
Houses read from main: T-257 at 172 (2723587139676283080823463207799/2e29), T-224 at 270
(16928162252196750114897964982713/1e30).
Read so far: precedent review-2026-11-09-ozden-927-931-five.md (document and packet README only,
not its programs), result-import.md stage 4, witness.schema.yaml, the issues, the author READMEs,
printed outputs and certificate/pose files as data.
Not read (clean room until the checker freeze): author verifier/sqcheck.py and verifier/README.md,
any sqpack witness/verifier/promotion code, devtools tools, the precedent's l64_* programs, L71.
Next: write the clean-room checker (reader; method A separating axes in Fraction; method B clipped
areas in gmpy2.mpq; self-test), freeze it by SHA-256.

2026-11-09T16:12:07Z CHECKER FROZEN. frozen/checker-frozen-digests.txt SHA-256
a77b067df7ff1e152c965ac33fc0289d082e606f1a8c93355728a3356ce3c411; six files:
l72_util.py 7815f7a5..., l72_reader.py 76eec736..., l72_sat.py a565ecf5..., l72_clip.py 4a450e32...,
l72_check.py a6c8edeb..., l72_selftest.py 5c7ba446.... Self-test PASSED (80 cases). One timing run on
172 before the freeze: ACCEPT, 9.9 s (contacts 46 left, 85 bottom, 161 right; least pair 2.008e-13 at 36,38).
Next: final self-test and checks of both files; then the controls plan, stated and hashed before the
controls program exists.

2026-11-09T16:14Z final runs: selftest PASSED (80); check-n172 ACCEPT (9.4 s); check-n270 ACCEPT (23.5 s).
172: contacts 46 left, 85 bottom, 161 right; 14,706 pairs apart by both; least 2.00833939294e-13 (36,38);
342 pairs below 1e-12. 270: contacts 104 left, 84 bottom, 227 top; 36,315 pairs apart by both; least
2.01624754215e-13 (220,234); 258 pairs below 1e-12. JSON twins equal the YAML; digests equal the READMEs'.
2026-11-09T16:17:18Z CONTROLS PLAN STATED: prog/controls-plan.json SHA-256
1826043aaa43b13652f8f9ab378b13a5ea61b225a137616e1af3126385d807cd (23 controls per count: G1-G6, G8, G9,
S1a-d, S3 L/R/D/U, S4c/p centre line, S5 centre line, S6, S7c/p, S8), stated from the check receipts and
l72_plan_facts.py (7ef3dcf7...), before l72_controls.py existed.

2026-11-09T16:50Z controls: EVERY_CONTROL_AS_STATED at both counts (23 of 23 each, no miss; G6 reversed
sense overlaps 66 pairs at 172, 98 at 270). Custody CUSTODY_HOLDS (LICENSE-evand-square-packing.txt is
blob 52cf89d2, byte-identical to the retained evand LICENSE at both house packets). Sides: claims are
12-place ceilings; gaps 3.24584509520e-03 (T-257) and 1.36488538957e-05 (T-224), rounded prints as issued.
Houses ACCEPT on the frozen checker; uniform-contraction margins S*1e-20 (1.3618e-19, 1.6928e-19); gains
are 2.38e16 and 8.06e13 times them (RV-3 does not reach them). Lineage: issue counts reproduce against the
house witnesses under the identity. 172: nearest centres miss one to one by one (14,18 share house 14),
15 beyond 0.1, tilts move between squares (further arrangement, as the 299 precedent). 270: one to one,
all ids kept, 1 beyond 0.1 (sq 59 straightens 32.3 deg). Pose vs certificate: no dilation, margins the
pose's own to 7e-37. Next: write the review, freeze findings, then reconcile with L71.

2026-11-09T16:42:21Z FINDINGS FROZEN, before anything of L71's, sqcheck.py, or this repository's verifier
and promotion code was opened. frozen/review-2026-11-09-ozden-935-936.frozen.md: 778 lines, 51,671 bytes,
SHA-256 26df28bbf7a6c452284fa11bebbc5018c581e9248f0ff13eb09188c086058d58.
Verdicts: accepted at both counts; F1-F14 all notes. S3 at 172; S2 at 270 (borderline, inside the
1.15e-5..1.88e-5 band; S3 alternative stated). Final run: ALL_RECEIPTS_MATCH, ~578 CPU-s.
Next: read L71's branch claude/bold-ritchie-xo28us-l71 and reconcile in a separate section.

2026-11-09T17:0xZ DONE. Branch claude/bold-ritchie-xo28us-l72-review pushed: 07bc1fc20 (review as frozen),
133a73572 (reconciliation with L71 @ 3e81f5d01, compare-lane.json LANE_EQUALS_REVIEW), 7f4301070 (F15 wording).
Reconciliation: L71's replays, identity counts, padding (house and own margins) and draft scores (S3 172,
S2 270) equal this review's. New F15 minor (records): L71's 172 draft "reverses 9 tilts" / "9 to the other
side of upright" / "36 one way and 13 the other" are near-45-degree sign conventions (9 squares turn
0.79-1.18 deg; 44 of 49 tilted squares within 1 deg of 45). Verdicts unchanged: accepted at both.
Packet names match L71's. No PR, no merge, no GitHub comments. Bead left in_progress for the coordinator.
