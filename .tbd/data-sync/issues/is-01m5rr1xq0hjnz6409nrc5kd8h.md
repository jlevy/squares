---
type: is
id: is-01m5rr1xq0hjnz6409nrc5kd8h
title: "Import #804: Hyukdong Kim's exact minimal polynomials of the record sides at 88, 126, 172, 199, 263"
kind: task
status: in_progress
priority: 2
version: 16
delegate: c-import-804-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5s72s7x05kxkyzxjkfqf2wh
  - is-01m5sas1vt59d996xv22h14rr7
hold: null
hold_until: null
created_at: 2026-10-25T05:20:39.648Z
updated_at: 2026-10-25T11:44:44.880Z
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

2026-10-25 coord-intake-1024 on c-triage-9vai-1025's report: decided by stated rules (stage 1 table; T-120..T-123 and T-193 precedent), not owner questions. 88, 126, 199: no entry (a second derivation of T-193's values, #639 exact-side-51 precedent). 172, 263: one new reported upper-bound entry, V0/C0, S2, phrased 's(n) <= <root>' never 's(n) =', credited to Hyukdong Kim after T-174's finders; nothing recorded on T-193. The configuration builder (W7-style, 10-100 CPU-h at 172) is a later bead, priced against the 40 CPU-h item cap before it runs. Records lane c-import-804-1025 (wt-804).
2026-10-25 c-import-804-1025 (wt-804, branch claude/intake-2026-10-25-issue804-exact-sides): import done as decided. Packet hyukdongkim-exact-forms-2026-10-25 (derived fact + digests, no archive byte; attachment re-downloaded with gh, SHA-256 matches). Ledger campaign/issue-intake/upper-bounds-issue804-20261025 (walks 172, 263; records both). T-244 upper bound V0/C0 S2 at 172 and 263, claim cut at 100 places (a 40-place cut reads as equal to T-174, which agrees to 88/93 places, and check_standing fails), regularizations of T-174 with identity source-claim; unfinished C3 links think-4rzl. 88/126/199: no entry, T-193 unchanged. Builder bead think-4rzl opened under think-ezt8, deferred to 2026-11-08. Requests entry #804 triage done. Question rule: Q1 (configurations at 172 and 263) goes under awaiting_author with changes: file once the acknowledgement is posted and has a URL; Q2 (licence) and Q3 (297) are informational.

ACKNOWLEDGEMENT DRAFT, revised after review A of #813 (post after #813 merges; T-244 is on the branch with contiguous ids; it drops the configurations question, answered at 09:06:23Z):
@HyukdongKim, thank you for these exact sides, for your correction of 07:22Z, and for the exact configurations you attached at 09:06Z.

**What we received.** We have the issue and its attachment `squares-exact-forms.zip` (14,112 bytes, SHA-256 `c770f9c37dee6b248543f3e661318630a0f279bc6a8c7663cb2efc53e2814ee7`, the digest you state), with `exact_forms.json` among its seven files. We also have `t244-exact-configurations.zip` (96,347 bytes, SHA-256 `16e6ad9d04f1def897478e59260880320bc7c06ae89e41fa83837c7dc29c9a2d`, the digest your comment states), and its `n172.minpoly.json` and `n263.minpoly.json` match the digests you give. We pinned the atlas files you read, `evand/square-packing@659ee62` `site/www/data/p/best-<n>.json`, by their digests as well.

**What we checked.** We did not run either bundle's code, and we wrote our own checks:

- Each of the five polynomials is primitive and irreducible over Q, by SymPy's `factor_list` and again by this repository's number-field code.
- Each root you name is the one we isolate exactly: the 4th of five real roots at 88, the larger of two at 126, the least of four at 172, the 2nd of two at 199, and the only one at 263. Your 100-digit values lie within 1e-99 of those roots.
- At 172 and 263 the atlas files you read are the record's witnesses at those counts, to binary64 at every square.

**88, 126 and 199.** Thank you for your comment of 07:22Z. As you say, your polynomials there are Evan Daniel's, from #639, registered as T-193 with exact configurations, so the record keeps no new entry for them; your values are an independent second derivation. We note that you withdrew the paragraph about 126 (the gap is 1.174e-19, and T-193 already holds 15/2 + 3√2).

**172 and 263.** Daniel's #639 forms have degree 12 there, and their roots lie 1.18e-62 and 9.23e-63 above yours. PingYou Ltd's rational certificates from #574 are smaller than those, and your roots are smaller still: below them by 3.90e-89 at 172 and 2.13e-94 at 263, decided exactly. These sides are registered as [T-244](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), recorded as reported (V0/C0): s(172) ≤ 13.6189889568993984288635016293504898995040… and s(263) ≤ 16.7331660078993789705122814839596734462471…, cut at 100 places in the entry. They are credited to you, after the packings' finders: Francisco Couzo's at 172 and Nate Chaoweeraprasit's at 263, as Evan Daniel and PingYou Ltd improved them. They are upper bounds, the sides of those packings, not values of s(n). Daniel's `exactsolve.py` also solves the KKT system on the load-bearing contacts and searches for an integer relation, so we credit you with the values, not with a new method. We record no local minimality: the least multiplier is about −6·10⁻¹⁶, and no second-order condition was checked.

**Your configurations.** They are kept here, and they will be decided exactly in a following change: on this repository's exact verifier over number fields, which reads Daniel's `minpoly.json` format, and on the retained `verify_exact.py` as a second route, with controls. Until then T-244 stays reported. Because neither bundle states a licence, we keep the polynomials, the printed sides and the configurations' content as facts, with the attachments' digests, and not the files themselves. We did not run `check_field_packing.py` or `controls.py`.

Two questions, neither of which holds anything open:

1. Would you dedicate the two bundles to the public domain (CC0 1.0) or license them (CC BY 4.0)? Then we can keep the files themselves.
2. At 297, Daniel's degree-12 form is also above #574's certificate, by 6.62e-63. Does your method give the stationary side there? This one is for interest only.

We will reply here as each step lands.

---
_Generated by [Claude Code](https://claude.ai/code)_

PR: https://github.com/jlevy/squares/pull/813 (draft, labels intake and S2), head 37e0f43a6. Hosted check_results fails on the T-243 gap until #806 merges; then merge main, re-cut the explainer at the next patch, re-pin.

Update 07:30Z: merged main 886dddce6 (#808) at 77c978716; fixed the first hosted run (download allowlist, issue 804 card, headline by surname) at 0ed9f670d; recorded #799 acknowledgement (issuecomment-6394514727) at 5e08f28c9; papers re-measured; re-pinned DATA_REVISION to 0ed9f670 at head dae3e3835. Hosted at dae3e3835: only check_results and the 7 tests calling it fail, on the T-243 gap; clears when #814 merges and main is merged here (re-cut the explainer at v0.4.29 then, since #814 also takes v0.4.28).

Update 09:50Z: merged main 46e355582 (#814) at 20c2a2fe4 (T-243 before T-244, ids contiguous); explainer re-cut v0.4.29 (dd5fc01db); #806 final comment recorded and entry closed (9d8bed3dd); #814 News landed (4c8f83bd1); hosted findings fixed (1b75d2f78: explainer PDF 25 pages, T-174 page test reads its 350,000-byte registered budget); papers re-measured at 1b75d2f7; DATA_REVISION 20c2a2fe4. Head 63de0bc6a: every hosted check passes (Packing validation 40180900830, Certificate page 40180900864, Branch mergeability 40180896050). The acknowledgement draft above names T-244, now on the branch with contiguous ids; still post only after the merge.

Update 10:40Z (review A of #813, issuecomment-6396307905): A1 to A5 fixed at 6997281dd; both author comments read (07:22:16Z concession at 88/126/199 and withdrawn 126 paragraph; 09:06:23Z configurations zip 16e6ad9d...9a2d), kept in packet hyukdongkim-t244-configurations-2026-10-25 as derived facts (no licence); #804 read_through 09:06:23Z, queued result configurations-172-263 on think-4rzl; think-4rzl re-scoped to deciding them on both routes, not deferred, builder only as fallback. Acknowledgement draft above rewritten: two informational questions (licence, 297), no awaiting_author item.
Update 11:55Z (review B, issuecomment-6396781432): B1 to B5 fixed at d5dcd2d0e; dispositions issuecomment-6396944532; head 3bf9b6455, every hosted check passes (Packing validation 40188144019, Certificate page 40188143967). think-4rzl step 1 is now the reader of the configurations packet facts (about half an agent-day).

2026-10-25 coord-intake-1024: #813 MERGED as 01e2b5295 at 11:32:19Z (review A issuecomment-6396307905 / dispositions issuecomment-6396537425; follow-up B issuecomment-6396781432 / dispositions issuecomment-6396944532; head 3bf9b6455, CI green). T-244 reported at 172/263; configurations received (think-4rzl, not deferred). The acknowledgement above is posted after the deploy verifies.

2026-10-25 coord-intake-1024: #813 deployed (Pages 40189291622 verified; live result/t-244.html 200). #804 acknowledgement posted https://github.com/jlevy/squares/issues/804#issuecomment-6397201800; recorded by think-4rzl's PR (c-decide-4rzl-1025, wt-4rzl), which decides the configurations.
