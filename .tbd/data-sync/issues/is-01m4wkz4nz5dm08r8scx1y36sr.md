---
type: is
id: is-01m4wkz4nz5dm08r8scx1y36sr
title: "Import Mishapolk: exact certificates at n = 103, 153, 207, 209, 258, 270 (#573)"
kind: task
status: open
priority: 1
version: 8
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T07:10:30.078Z
updated_at: 2026-10-23T06:16:18.117Z
started_at: 2026-10-14T07:10:40.964Z
---
Stage 1-2 and stage 4 replay of issue #573 (Mishapolk/square-packing-records at 336bdf5efab4784e54e0ac32edf3ed12f9c8af7e), lane mishapolk of the 2026-10-14 intake pass, branch claude/wizardly-meitner-wqn4x3-intake-1014-mishapolk. Claim map, comparison and priced plan in notes.

## Notes

## Stage 1 triage (2026-10-14, lane mishapolk, branch claude/wizardly-meitner-wqn4x3-intake-1014-mishapolk)

**Pin.** Mishapolk/square-packing-records at 336bdf5efab4784e54e0ac32edf3ed12f9c8af7e
(tree fd1ce3da, committed 2026-10-12T23:52:23Z), the issue's pin. All 19 certificates
are unchanged at 46f638c (#593's pin) and at head ec87dc6. Issue #573 opened
2026-10-12T23:58Z as "Exact rational certificates for 19 packings below register
(n = 103-306)", renamed by its author at 00:06Z to the six it names; no comments.

**Every claim.** Requested, rounded up at 12 places, all admitted: s(103) <= 10.679232047362,
s(153) <= 12.870013850405, s(207) <= 14.880960371558, s(209) <= 14.946223226448,
s(258) <= 16.563448002138, s(270) <= 16.929775353544; all six digests match. The release
holds 13 more certificates the renamed issue dropped (108, 127, 131, 154, 175, 180, 236,
237, 263, 267, 302, 303, 306), each admitted at the README's exact fraction. Author checks:
sqpack/verify.py at 562fdbd and evand verify_cert.py at 31523f8; the README credits five
engines to "David Ellsworth", three of them this repository's devtools. Lineage: Ryan Xu
at 103, Nate Chaoweeraprasit (SQUISH) at 258, new arrangements at 153/207/209/270.
AI: "The search implementation, verification orchestration, and issue preparation used
Gemini. I directed the work."

**Claim map against main aeef99ef0, re-read at b8c930338 and every open report (frozen claims.json).** No count
is the smallest known.
- 153, 207: below the case (T-148, T-147) by 2.56e-12, 1.49e-09 and below PingYou's #504/#503
  refinements by 2.55e-12, 5.56e-13; PR #574 smaller by 1.57e-14, 2.42e-12. Same bytes as
  #593's n153/n207 (owned by think-2ep3).
- 103, 258: above the case (T-146 regularizations of Mishapolk's #470) by 4.36e-14, 3.38e-12.
- 209: above the case (Couzo T-140) by 1.55e-12; #593's 209 is that case certificate byte
  for byte. 270: above the case (SQUISH T-151) by 1.58e-3; #593's 270 is smaller.
- Unrequested: 154, 175 below the case by 5.04e-4, 2.95e-3 (Couzo #586 smaller at 154 by
  1.36e-3; PR #574 at 175 by 1.40e-12); the other 11 above the case by 1.7e-12 to 7.2e-3.
- Map: no new entry recommended for #573 itself; 153 and 207 are carried by #593's
  identical files and are not the smallest.

**Priced validation plan.** Both maintained exact routes. Replayed the four below the case:
153, 154, 175, 207. Certify: 12 jobs, all as required, 359,730 pair decisions, 205.66 job
wall s, 4 m 17 s wall (07:35:08Z-07:39:25Z). Not run: the other 15, 18-31 min certify +
as much replay.

**Draft acknowledgement (not posted).**
> @Mishapolk, thank you. We have retained the 19 certificates of 336bdf5 (the six digests
> you list match) as derived exact facts; the repository states no licence. Against the
> register on main and the other open reports, none of the six is the smallest known side:
> 153 and 207 are below the register, but PR #574 states smaller sides at both; 103 and
> 258 are above Evan Daniel's regularizations of your #470 packings, now in the register;
> 209 and 270 are above the register, and your #593 holds the register's 209 certificate
> and a smaller 270. We replayed 153, 154, 175 and 207 with both of our exact checkers;
> both accepted the positives and refused the controls. We track your 46f638c release
> under #593.

## Stage 2 and stage 4 (2026-10-14)

Packet packing/resources/web/mishapolk-exact-certificates-2026-10-12 (derived facts, 19
certificates), branch claude/wizardly-meitner-wqn4x3-intake-1014-mishapolk at d4c198d0d.
Replay of 153, 154, 175, 207: certify 12 jobs, 4 positives accepted and 8 controls refused
on both routes, 359,730 pair decisions, 205.66 job wall s, 4 m 17 s wall; check --replay
equal, 1 m 49 s. Register plan: scratchpad mishapolk/register-plan-573.yaml; its template
calls all six requested sides improvements, which holds only at 153 and 207 against the
case, and neither is the smallest open report. Not run: 15 counts, 18-31 min certify plus
as much replay.


## Acknowledgement posted (2026-10-14)

https://github.com/jlevy/squares/issues/573#issuecomment-6163850092 (revised from the draft above; text in scratchpad mishapolk/ack573.md).

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): T-172 at 153 and 207, V0/C0 (the ledger records #573 there, before PR 574); 103, 209, 258, 270 not recorded.

Renumbered on 14 October at review A3 of #602 (records PR, branch claude/wizardly-meitner-wqn4x3-records-1014): Kevin Fang's theorem, T-178 above, is now T-163, at Theorem 1's first commit (6028f31, 12 October); T-163 to T-177 above are now T-164 to T-178. T-179 to T-184 keep their ids.
