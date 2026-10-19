---
type: is
id: is-01m4wq56t7qe7t64e8vx47jzns
title: "Import BuddenPing: 148 certificate refinements, 60 of them exact algebraic or tightened rational (#574)"
kind: task
status: in_progress
priority: 1
version: 13
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
child_order_hints:
  - is-01m5a96bxm53bfdgk9k3cefxhr
hold: null
hold_until: null
created_at: 2026-10-14T08:06:14.598Z
updated_at: 2026-10-19T14:31:34.579Z
started_at: 2026-10-14T08:06:19.172Z
---
Pull request jlevy/squares#574 (BuddenPing, PingYou Ltd), head 4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde of BuddenPing/squares (2026-10-13T01:58:38Z), treated as an intake report: never merged, approved or commented on here. Lane pr574 of the 2026-10-14 intake pass (think-mq0k), branch claude/wizardly-meitner-wqn4x3-intake-1014-pr574. Packet packing/resources/web/pingyou-pr574-certificates-2026-10-13/. Claim map, comparison, replay plan and draft acknowledgement in the notes.

## Notes

## Stage 1 triage (2026-10-14, lane pr574 of think-mq0k)

Source pinned: PR jlevy/squares#574 head 4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde of
BuddenPing/squares (branch codex/numerical-certificate-refinements, committed
2026-10-13T01:58:38Z, base e96e9ea). No comments or reviews when read (2026-10-14T07:37Z).
Geometry outside Git: three HostedData manifests at the pin bind four release assets of
BuddenPing/square-packing-certificates (tags all at 318ab94):
v2 pingyou-numerical-refinements-2026-10-13.zip 7,754,365 B sha256 ced04297...,
v2 pingyou-native-witnesses-2026-10-13.zip 21,737,024 B da66aa5f...,
pingyou-algebraic-refinements-2026-10-13.zip 2,815,986 B 26b31abe...,
pingyou-exact-153-302-2026-10-13.zip 235,073 B cea5e95d... All downloaded, digests match.
Packet: packing/resources/web/pingyou-pr574-certificates-2026-10-13/ (derived-only).

### Claims (148 counts, 5..308)

- 86 rational v2 certificates still current; 58 algebraic (48 Q(sqrt2); N18, N234, N299
  Q(sqrt7); N54, N107, N178 quartic; N151 biquadratic; N53 degree 8; N70, N207 degree 5);
  rational N146 and N261 (supplement); N153 (degree 7) and N302 (cubic) exact supplement.
- COVERAGE-147.json: 59 improved, 82 retained pending algebraic reconstruction, N50/N171
  exact rational, N153/N302 exact algebraic, N204/N264 radical candidates dominated.
- All are padding reductions or exact attainments of packings others found (and
  PingYou's own N153/N207/N302); the author claims no new constructions or optimality.

### Map to the register (stage 1 table)

- 16 algebraic counts equal the case's verified closed form (N5, 10, 18, 19, 26, 27, 38,
  40, 51, 52, 65, 66, 67, 82, 85, 89): second certificate of a held value; a
  `simplification` entry at most.
- 37 algebraic counts attain the reported lane's closed form and are below the verified
  rational ceiling by 7.2e-36..7.2e-15: verified lane would rise to the reported value.
  N54, N107, N178 quartic: below verified, reported lane a print.
- N70 (Xu's packing, 8.9e-20 below case), N153 (2.6e-12 below T-148), N207 (1.5e-9 below
  T-147) attain PingYou's/Xu's constructions exactly; N302 is 1.75e-3 below the case but
  2.6e-4 above Couzo's #583.
- 85 declared rational counts are all below their case ceilings: 73 by padding
  (4.6e-61..5.3e-16), 12 by relaying newer packings of open reports (N129 #562, N146 #566,
  N156 #561, N175, N176 #575, N204 #562, N232, N237 #561, N261 #567, N264, N271 #561, N303
  #562). Excluded from the declaration: N11 (above the proved optimum root(P_trump11)),
  N17 (1.04e-22 below a rounded verified print; no house reader), N29 (case record defect:
  verified value 5.43e-20 above its own exact form).
- Register action: bounds of one kind at several counts in one release -> one entry
  whose scope covers them, each count listed as a regularization of the packing it
  tightens (finder keeps credit). Significance drafted S1.

### Who else holds each value

Frozen in acquisition/claims.json and algebraic-claims.json (main b8c930338): case on
main, every register entry stating a bound at the count, #593/#573 (binary64 / 12-place
prints), #562/#575 (40-place), #561/#583 (12-place), PingYou #564/#566-#569 and the
#503/#504 comments. By prints: smallest only at N258, N261 (rational) and N207
(algebraic); above others at N211, N237, N241, N304, N302. With Mishapolk's exact sides
at 46f638c and the couzo/pingyou lane packets (diagnostic): strictly smallest at 60
rational counts and N70, N153, N207. vs PingYou's own issues: below #568/#566/#569 by
1.1e-79/1.3e-79/1.7e-99 (same packings), #567 by 2.0e-21.

### Priced validation plan

- Rational: both maintained exact routes via upper_bound_reports (custody extended to
  release-asset members). Priced (n129 probe, 2.6 ms CPU/decision under load) at ~6.1 h
  for all 85 on one worker; strictly-smallest 60 at ~5.4 h; replayed first (roster).
  Rest (25 counts) ~0.8 h, not run.
- Algebraic: one maintained route, sqpack exact_verify over the field
  (devtools.algebraic_witness_reports); probes n40 1.8 s, n70 27 s, n53 305 s per positive
  job. Roster N70, N153, N207. No second route over number fields exists; an independent
  number-field corner checker is a W7 slice (large); duck-typing the rational corner
  checker over sqpack.field would share field arithmetic with route 1.

### Draft acknowledgement (not posted)

Thank you for PR #574. We are reading it as an intake report and will not merge it as a
pull request. We retained its sources at 4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde with the
four release assets its manifests pin (digests checked), as derived exact facts. We are
checking each rational certificate on this project's two exact routes and the algebraic
certificates on the exact number-field route, comparing every count with the current
case records and the other open reports, and will register the results that the record
does not already hold, crediting each packing's finder and PingYou Ltd for the
certificate refinements. We will reply again with the outcome.

## Stage 2 and stage 4 results (2026-10-14, branch claude/wizardly-meitner-wqn4x3-intake-1014-pr574)

- Packet retained: pingyou-pr574-certificates-2026-10-13 (acquire_source --check passes;
  derive --check passes for 85 rational and 60 algebraic facts from the pin and assets).
- Rational replay, both routes, --workers 1 (one job at a time): 39 of the 60 counts
  below every report finished before the session's 2-hour background ceiling stopped
  the driver (08:11-10:13Z). 117 jobs, 39 positives pass both routes, 78 controls
  refused; 4,555,860 pair decisions, 4,836 route CPU s, 6,992 job wall s, longest 204 s.
  All positives are exact-contact certificates (wall clearance 0; pair gap 0 at 38).
  check --replay re-decided N129, N156, N175, N176, N258, N261, N271 (21 jobs, 21m43s),
  equal; all 117 admitted.
- Algebraic replay, one route (sqpack exact_verify in the field): N70, N153, N207; 9 jobs
  pass/refuse as required; 106,092 pair decisions, 699 CPU s, 787 wall s; check --replay
  equal (12m57s).
- Not run, priced: 21 remaining below-every-report rational counts ~2.8 h; other 25
  declared rational counts ~0.8 h; rational check --replay of the other 32 counts ~1.5 h;
  57 algebraic counts ~2.2 h on route 1; a second number-field route needs a W7 slice.
- register-plan (rational, 85 counts) run; T-NNN at V0/C0, S1 drafted, published
  2026-10-13; output kept at scratch register-plan.yaml (131 KB; claim states 85
  exact sides as long fractions).

Branch head: 56cf868c617975eaada5b0c10dab953cc6fa2e37 (pushed). records tier: only failure is the URL-history step against the advanced origin/main (0 failures against base b8c930338).

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): T-174 at the ledger's 68 counts (64 rational, algebraic at 70, 153, 207 and 302), V0/C0, 67 regularizations; 39 rational counts replayed on both routes, the algebraic at 70, 153 and 207 on route 1; the other 25 rational counts and 302 are in unfinished_confirmations.

Replay with the owner budget (2026-10-14): all 64 recorded rational counts and the 4 recorded algebraic counts (incl. 302) now have receipts (head 7dc75a64b and later); check --replay of the remaining counts runs in chunks. T-id per the records lane after #602: T-174.

Budgeted replay done (2026-10-14, head e9eb6935a): 64 recorded rational counts, 192 jobs on both routes, 64 pass / 128 controls refused; 4 recorded algebraic counts, 12 jobs on route 1, 4 pass / 8 refused; check --replay of every recorded count equal. Unreplayed: 21 declared rational counts the ledger does not record, 56 algebraic counts.

2026-10-16 ~03:40Z ecstatic-edison-replies-stack, PR #637 review A4 (https://github.com/jlevy/squares/pull/637#pullrequestreview-5542558537). Held reply on #574: `check_requests --report` lists #574 as reply due (T-174 is V3/C3, confirmed, and E-pingyou-574-certificate-report and E-pingyou-574-algebraic-report reviewed, where the follow-up of 14 October stated V0/C0 and recorded). The coordinator held it out of the 16 October replies (think-py1e's brief: "Not on #574 ..."): deciding the pull request and adopting T-174 are the owner's, and the entry's close_when has the owner post the resulting state with T-174's id. What releases it: the owner's decision on PR #574, or the owner's instruction to post. Until then a pass that finds #574 due does not post it; #574's entry in packing/campaign/result-requests.yaml notes the same hold (PR #637).

Replacement stage 7 reply draft from #660's addressing pass (house rule; RP-3 and the T-174 hold end): see the #574 section of the file attached below. Not posted: stage 7 replies post only after the change merges and deploys.

# Stage 7 reply text after PR #660 (review A2), for the answer beads' holders

These are replacement lines for drafts that are already on the answer beads. Nothing here has been posted. Each reply still goes out on the trigger its bead names.

## think-9v2k (#574): the held note of 2026-10-16 ~03:40Z

Replace "deciding the pull request and adopting T-174 are the owner's" with:

> deciding the pull request is the owner's; adopting T-174 is not, since the owner's house rule of 16 October 2026 makes T-174 the house at 63 counts, staged in `select_houses.PENDING_ADOPTION` under think-3mry (60 rational counts, the next pull request) and think-ot5c (70, 153 and 207, once `adopt_houses` writes an algebraic side)

The release is unchanged: the owner's decision on PR #574, or the owner's instruction to post.

Add this sentence to the reply itself, after the V3/C3 state:

> Under the house rule the owner set on 16 October 2026, a validated packing smaller than a case's house becomes the house, whoever found it, and is regularized in the pull request that adopts it. T-174's packings are therefore the houses at 63 counts. The 60 rational ones are adopted in the next adoption pull request, and the algebraic ones at 70, 153 and 207 once the record's writer takes algebraic sides.

## think-phyb (#639): the DRAFT import reply

In its third paragraph, replace "and your configurations and checker are now a second route for the owner's open decision on those three" with:

> so #574 keeps the record there, and your configurations and checker are a second exact route to those three sides, which the owner's house rule of 16 October 2026 adopts as the houses once the record's writer takes algebraic sides

Replace "The case pages keep their houses until adoption, which is the owner's, with #574's." with:

> Under that rule each validated smaller side becomes the house in the pass that validates it. T-193's sixteen are adopted that way once T-193's stage 4 review is merged (#658), and the case pages keep their current houses until then.

The supersession note of ~11:05Z still applies: if T-193 is not yet at V3/C3 on main when this reply is posted, the reply must not say it is confirmed.
