---
type: is
id: is-01m5rr1xq0hjnz6409nrc5kd8h
title: "Import #804: Hyukdong Kim's exact minimal polynomials of the record sides at 88, 126, 172, 199, 263"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-triage-9vai-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-25T05:20:39.648Z
updated_at: 2026-10-25T05:41:16.813Z
started_at: 2026-10-25T05:21:00.185Z
---
New 2026-10-25 issue https://github.com/jlevy/squares/issues/804 (HyukdongKim, 01:57:25Z): the record side at each of 88, 126, 172, 199 and 263 is a root of a stated irreducible polynomial (degrees 7, 2, 24, 16, 17; 126 = 15/2 + 3 sqrt 2), the register having minimal_polynomial: null there; exact_forms.json. Claude-assisted. Stage 1 triage read-only first: which houses the polynomials describe today (the record has moved since 2ec489d1e at some counts?), how to verify (exact KKT/rigidity system, PSLQ is not a proof), and the register action (new exact-value entries, or evidence on the houses).

## Notes

Triage of #804 (c-triage-9vai-1025, 2026-10-25, main bb756e193; read-only, author code not run).

Pin: attachment squares-exact-forms.zip (https://github.com/user-attachments/files/33917140/squares-exact-forms.zip), 14,112 bytes, SHA-256 c770f9c37dee6b248543f3e661318630a0f279bc6a8c7663cb2efc53e2814ee7 = issue's digest; exact_forms.json SHA-256 531e7077b3242aa56e959031824fb435693deaf8d73f7e33016d49c9e1709202. No licence. Inputs: evand/square-packing@659ee62 site/www/data/p/best-<n>.json (last changed 122d0ba, 10-10). Daniel's head d99925d: EXACT_FORMS.md unchanged since 1b7e2cb (10-07 table); search/exact/cur unchanged since 7d1407a (#639).

Per count (exact, own Fraction bisection + devtools.exact_sides):
- 88: house T-127 (Gupta), root 9.882e-20 below (house = root(1+1e-20)); polynomial identical to #639 = T-193 (V3/C3, staged house, waits think-8ido). 4th of 5 real roots. Irreducible.
- 126: house T-139, root 1.174e-19 below (issue's 1.2e-22 is wrong); identical to T-193 (15/2+3sqrt2). 2nd of 2. Irreducible.
- 172: house T-174, root 3.898e-89 below; #639 deg-12 side 1.185e-62 above root (not recorded in T-193). 1st of 4. Irreducible, deg 24, gcd with #639 poly = 1.
- 199: house T-127, root 1.462e-19 below; identical to T-193. 2nd of 2. Irreducible.
- 263: house T-174, root 2.126e-94 below; #639 deg-12 side 9.234e-63 above. Only real root. Irreducible, deg 17.
No house/case record moved since 2ec489d1e. Atlas input = T-174 witness to binary64 at 172/263; at 88/126/199 other poses (max move 0.150/0.137/0.611 under best box symmetry), same side.

Action proposed: 88/126/199 not registered (second derivation of T-193's values; #639 exact-side-51 precedent). 172/263 one new upper-bound entry V0/C0 S2 as reported (T-121/T-193 precedent); validation needs an exact number-field configuration (ask author; else W7 KKT builder, priced ~1 agent-day + 10-100 CPU-h at 172 without python-flint). Decision of a supplied config ~2 CPU-h (up to ~8) for both counts on two routes.

Drafts: scratchpad triage-804/drafts/{result-requests-804.yaml (triage: pending, schema-valid), result-requests-804-results-after-triage.yaml (schema-valid), register-entry-172-263.yaml (schema-valid), import-plan-804.md, ack-804.md}.
