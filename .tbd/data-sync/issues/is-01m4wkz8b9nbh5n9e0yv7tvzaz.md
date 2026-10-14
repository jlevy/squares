---
type: is
id: is-01m4wkz8b9nbh5n9e0yv7tvzaz
title: "Import Mishapolk: 73 upper bounds across n = 51 to 308 (#593)"
kind: task
status: in_progress
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T07:10:33.832Z
updated_at: 2026-10-14T14:50:30.342Z
started_at: 2026-10-14T07:10:42.633Z
---
Stage 1-2 and stage 4 replay of issue #593 (Mishapolk/square-packing-records at 46f638ce0537beeb1bad24242c6a3d357eecd9ee), lane mishapolk of the 2026-10-14 intake pass, branch claude/wizardly-meitner-wqn4x3-intake-1014-mishapolk. Claim map, comparison and priced plan in notes.

## Notes

## Stage 1 triage (2026-10-14, lane mishapolk, branch claude/wizardly-meitner-wqn4x3-intake-1014-mishapolk)

**Pin.** Mishapolk/square-packing-records at 46f638ce0537beeb1bad24242c6a3d357eecd9ee
(tree a3d2236c, committed 2026-10-14T01:24:10Z), the issue's pin. Head at retrieval
(2026-10-14T07:09Z) was ec87dc6; its six later commits add and edit ISSUE_REGISTRATION.md
only. Issue #593 opened 2026-10-14T01:40Z; no comments, no renames, labelled intake.
Cross-referenced from evand's #596 (beyond-horizon, no shared count).

**Every claim.** 73 exact certificates certificates/n<n>.cert, n = 51..308. The issue's
16-place sides are binary64 prints (census side_float) and do not admit; census.json
states each exact side_fraction, which every header equals (admitted there). All 73
digests the issue lists match the pinned files. The tree also holds #573's 19
square-<n>.cert (same blobs as 336bdf5), decimal poses/drawings of #470/#573, and
LEGAL_VICTORIES.jsonl. Author-reported checks: evand verify_cert.py, verify_cert2.py and
sqpack/verify.py from the author's own copies (not in the tree), 73/73. No optimality
claimed. Credit name given two ways: "Mishapolk (Mykhailo Polkovskyi)" and "Mishapolk
(Mikhail Polk)". AI: "Gemini 3.8 assisted with solver scripting, precision checks, and
formatting."

**Provenance facts.** 13 files are byte for byte certificates already retained here:
Evan Daniel's regularized lists (T-146) at 70, 102, 123, 269, 292, 295; Couzo's at 105,
108, 127, 209, 267, 305, 306. The pin's commit message: "Absorb latest pending issue/PR
submissions: update 12 certificates (108, 127, 146, 181, 209, 236, 261, 267, 270, 272,
305, 306)". 103/153/207/258 are #573's bytes (first committed 336bdf5, 2026-10-12T23:52Z).

**Claim map against main aeef99ef0, re-read at b8c930338 and every open report (frozen claims.json).**
- Equal to the case's exact side, 40: 70 84 86 88 102 105 106 108 110 123 126 127 130 132
  152 172 177 179 180 182 199 206 208 209 210 228 240 263 266 267 268 269 273 292 295 297
  301 305 306 308. Map: a request for a value already registered; no new entry.
- Above the case, 15 (+51 vs Ryan Xu's radical (16+5sqrt2)/3, by 7.69e-20): 68 103 131 146
  155 181 236 238 239 258 259 261 270 272 307. Map: none; stays in the packet.
- Below the case, 17. Smallest known only at 237 (2.45e-4 below T-140; 2.43e-4 below
  Couzo #561 and PR #574). 211, 241: exact side equal to Couzo's #586 certificates at
  b85dee2 (17:30:53Z on 10-13; Mishapolk's 8bb41af 15:51:54Z) - priority/credit question,
  both continue Ostashev #575. Others smaller: PR #574 by ~1e-19 (guard) at 129 175 176
  204 232 264 303, by 1.57e-14 at 153, 2.42e-12 at 207; Ostashev #562/#575 (earlier) by
  <1e-30 at 129 176 204 303 304; Couzo #583 at 302 by 2.62e-4; Couzo #586 at 154 by
  1.29e-3; 156, 271 undecided with Couzo #561's 12-place print, PR #574 smaller by ~1e-19.
  Map: 237 is a new entry; the rest are the records lane's call, pending the other open
  imports.
- Open PRs #585, #587, #591 state no side at these counts.

**Priced validation plan.** Both maintained exact routes (devtools.upper_bound_reports
certify, check --replay); nothing needs the source's code. Whole batch priced ~5.5 h one
worker (certify + replay), above the 3 h line, so group 1 only: 211, 237, 241.
Certify: 9 jobs, all pass/refuse as required, 474,246 pair decisions, 227.80 job wall s,
4 m 47 s wall (07:29:54Z-07:34:41Z), load 7-9. Not run: the other 69 declared counts,
75-125 min certify + as much replay (the 14 other below-case counts: 17-28 min of that);
51 not derived (algebraic house).

**Draft acknowledgement (not posted).**
> @Mishapolk, thank you. We have retained the 73 certificates of 46f638c (all 73 digests
> match) as derived exact facts; the repository states no licence. Your 16-place sides
> are binary64 prints, so we admitted each certificate at census.json's exact fraction.
> Compared with the register on main and with the other open reports, the release holds
> the smallest known side at 237. At 211 and 241 its sides equal Francisco Couzo's #586
> certificates exactly. At 40 counts the certificate has the register's exact side
> (13 files are byte for byte certificates already registered from Evan Daniel and
> Francisco Couzo), at 16 it is above the register, and at the other 14 counts below the
> register another open report (Daniil Ostashev's #562/#575, Couzo's #583/#586, PR #574)
> is smaller or equal. We replayed 211, 237 and 241 with both of our exact checkers; both
> accepted the positives and refused the controls. Could you tell us which credit name
> to use (Mykhailo Polkovskyi or Mikhail Polk), and how the 129, 176, 303 and 304
> packings relate to Ostashev's #562 and #575, whose sides agree to 30 places?

## Stage 2 and stage 4 (2026-10-14)

Packet packing/resources/web/mishapolk-records-2026-10-14 (derived facts, 72 certificates),
branch claude/wizardly-meitner-wqn4x3-intake-1014-mishapolk at d4c198d0d. Replay of 211,
237, 241: certify 9 jobs, 3 positives accepted and 6 controls refused on both routes,
474,246 pair decisions, 227.80 job wall s, 4 m 47 s wall; check --replay equal, 4 m 33 s.
Least wall clearance 5e-21 and pair gap 1.00e-20 in each positive (1e-20 dilation).
Register plan: scratchpad mishapolk/register-plan-593.yaml (regenerate with
`upper_bound_reports mishapolk-records-2026-10-14 register-plan`); its template claims
"improvements" at all 72 requested counts, so the records lane must restrict any entry
to 237 (and decide 211/241 with Couzo #586). Not run: 69 counts, 75-125 min certify plus
as much replay. Open questions: credit name; Ostashev priority at 129/176/204/303/304;
Couzo priority at 211/241 and 156/271; 51 needs an algebraic house to compare in-tool.


## Acknowledgement posted (2026-10-14)

https://github.com/jlevy/squares/issues/593#issuecomment-6163849805 (revised from the draft above; text in scratchpad mishapolk/ack593.md).

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): T-183 at 237, V0/C0; the ties at 211 and 241 and the other 70 counts not recorded.
