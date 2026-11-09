---
type: is
id: is-01m70ga6b62h1z8an6d5ynxges
title: "Stage 4 blind review of #935, #936 (Özden's s(172), s(270))"
kind: task
status: in_progress
priority: 1
version: 6
delegate: bold-ritchie-l72-review
labels:
  - intake
  - review
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-09T15:54:59.302Z
updated_at: 2026-11-09T16:17:38.756Z
started_at: 2026-11-09T15:55:07.051Z
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
