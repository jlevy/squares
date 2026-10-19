---
type: is
id: is-01m51e5rvjrd61yaww8djj1nzz
title: "Import evand: exact algebraic sides for 22 current best-known packings (#639)"
kind: task
status: in_progress
priority: 1
version: 25
delegate: lane-658
labels:
  - result-import
dependencies: []
parent_id: is-01m51e5r3sg4h1wcrh7c826v7b
child_order_hints:
  - is-01m51fayepg6n4wt17qynt441n
  - is-01m5249k5jzwfh92yjb8qe5mbp
hold: null
hold_until: null
created_at: 2026-10-16T04:05:28.050Z
updated_at: 2026-10-19T20:37:11.755Z
started_at: 2026-10-16T04:05:36.125Z
---
Stage 1 triage of jlevy/squares#639 (evand, Evan Daniel, "Exact algebraic sides for 22 current best-known packings (minimal polynomial, isolating interval, exact configuration): registration request", opened 2026-10-16T03:37:13Z, labelled `intake`, no comments when read at about 04:20Z). Intake pass 2026-10-16 (epic think-mdnn), read-only: nothing was run but exact sign evaluations of the source's polynomials at the record's rationals (seconds), and nothing of the source is retained yet.

## Pin

- evand/square-packing at 7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1 (committed 2026-10-16T03:33:01Z, the head when read, the commit the issue names), directory search/exact/cur/, added by 058b67133f4130ce36bf43ee1c13b53948289343 (03:30:10Z) and annotated by 7d1407a (register comparison, 153 and 207 re-run on the register's witnesses). The checker the replay needs is search/exact/verify_exact.py (stdlib only, Fraction; SHA-256 a0f38ca87c13c7e1b1d6ca99d69adea47df6008a645e3b4dbb79e8e0af35bab4), unchanged by these commits.
- SHA-256 at the pin: README.md fef88307..., RESULTS.md 35c5b358..., results.json 732bab3b..., crosscheck.json 353e4558..., crosscheck.py 04cdf734..., run.py e8250aff..., table.py c1443891..., verify_data.sh 1de470c7..., data/verify.txt 6ec62056... (23 lines, 23 VALID). The 23 data files data/n-N.minpoly.json.gz are 21,474,827 bytes together; four are 20.75 MB of it (204 3,534,100 B; 263 8,960,033 B; 267 1,545,171 B; 297 6,714,645 B), so stage 2 pins them by digest under OR-18. Digests: 51 d5c90fb3..., 70 ebcdfbe8..., 88 a2994e3e..., 102 f18300ab..., 123 891d9aa5..., 126 ca327d76..., 153 0e87edab..., 172 e1fdda84..., 175 c612cbbe..., 199 9374939e..., 204 59cd30fc..., 207 f39fedbf..., 232 7386edf3..., 258 e0656208..., 259 5e9ffafc..., 263 d07bda8a..., 266 e5221442..., 267 09a7ca61..., 292 1e6c03a9..., 295 40ef2669..., 297 6037de6d..., 301 5d262ea2..., 302 8da6f8b0... (full digests in the pass's scratch read; stage 2's manifest records them).
- Licence: MIT (the repository's LICENSE, with credits in CREDITS.md, as the evand-n146-2026-10-14 packet records; neither changed in these commits). The issue adds: "Register data: CC BY 4.0, Joshua Levy, the squares project."
- Credit and AI, as the issue states them: "The packings are their finders' (the register's credits in the table). Method and code as in #419." "The solver, checkers and this batch were written and run with Claude (Anthropic) as a coding and research agent, directed and reviewed by me." Both commits carry a Claude co-author trailer. The issue's finder column names one finder per count; the case records also name improvers (Gupta at 88 and 199, Polkovskyi at 153, 207 and 258, Couzo at 267 and 302, Daniel at 70, 102, 123, 126, 172, 258, 263, 292, 295, 297 and 301).

## Every claim

For each n in {51, 70, 88, 102, 123, 126, 153, 172, 175, 199, 204, 207, 232, 258, 259, 263, 266, 267, 292, 295, 297, 301, 302}: s(n) <= S*, S* the unique root of an integer polynomial p (degree 2 to 41) in a rational isolating interval of width 2e-25, realised by an exact configuration over K = Q[t]/f (every square's x, y and u = tan(theta/2) in K; field degree = deg p at every count). Three are quadratic: s(51) <= (16 + 5 sqrt 2)/3, s(126) <= 15/2 + 3 sqrt 2, s(295) <= 22(1 + sqrt 2)/3. The issue says p is irreducible; no program in search/exact/cur or verify_exact.py checks irreducibility, so minimality is source-asserted, as for T-120 to T-123. Checked at the source by verify_exact.py (23/23 VALID, about 4 min on 8 processes) and crosscheck.py (64-digit Newton S in p's interval; mpmath.findpoly returns p at 51, 102, 126, 295). Not claimed: Lean Packs (20 of 23 have field degree <= 20), anything at s(29), any lower bound. The issue's 52 open counts are a list, not a claim.

## Map to the register (exact, here)

Method: the sign of p at each rational the record holds, against p's signs at the ends of the source's interval (a sign change at every count), refined by bisection; the record's decimals by check_standing's spans; #574's (T-174's) sides from pingyou-pr574-certificates-2026-10-13/acquisition/claims.json and algebraic-claims.json. Scratch programs: decide639.py, t174rat_vs_639.py, t174_vs_639.py (not committed; a triage read, OR-1 noted).

- 51: S* = (16 + 5 sqrt 2)/3, the case's exact form in both lanes (Ryan Xu, #432). A tie: not recorded. A second derivation of a value the record holds.
- 70, 153, 207: S* agrees to the 40 places #574 printed, at the same degree (5, 7, 5), with T-174's algebraic sides (PingYou Ltd, first committed 2026-10-13), which are 8.88e-20, 1.57e-14 and 2.42e-12 below the case lanes (T-146 at 70; T-173 at 153 and 207) and whose adoption is the owner's decision RP-3 ("the smallest sides known but rest on one route"). A tie with an earlier report: not recorded. It is a second exact configuration and a second checker for those values, which bears on RP-3. At 207 the source says its re-solve of the register's witness (store id 291579) did not verify pair (73, 74) and that the committed form is from a tying copy (store id 1044231); a statement about its re-solve, not about T-173's rational certificate, which three exact routes here decided.
- 172, 263, 297: #574's rational certificates (T-174, V3/C3, houses held by the owner's hold) are below S* by 1.18e-62, 9.23e-63 and 6.62e-63 (S* to 85 places against #574's exact side). #639 is weaker than an earlier report: not recorded. S* is then not the least side of those packings; the data files pin 14 free coordinates at 172 (stats n_free 14), a question for the author.
- Below every side the record holds or has pending (case lanes, T-136, T-146, T-158, T-162, T-173, T-174, T-181, T-186, T-139 and the rest), so recorded by the report-order rule: 88 (5.92e-95 below T-174), 102 (3.69e-88, T-174), 123 (8.95e-95, T-174), 126 (7.77e-35, T-174), 175 (1.00e-76, T-186), 199 (4.48e-88, T-174), 204 (1.48e-99, T-186), 232 (1.58e-99, T-186), 258 (1.51e-94, T-174), 259 (1.43e-94, T-174), 266 (1.49e-94, T-174), 267 (1.18e-64, T-174), 292 (1.66e-79, T-174), 295 (1.86e-94, T-174), 301 (1.97e-94, T-174), 302 (1.79e-39, T-186). Against the case lanes alone the margins are 9.9e-20 to 1.8e-19, and 1.56e-31 at 259. 16 counts.
- #574 and #593 are open reports at these counts, so stage 3 runs devtools.intake_ledger before registering. Its start reads a pending entry's bound from the entry's claim text (check_standing.improvements), and T-174's claim prints only its algebraic sides, so the ledger's start omits T-174's rationals at 172, 263 and 297 and would record #639 there; stage 3 transcribes those comparisons as record_relations, or the start is fixed first.
- Register action at stage 3: one new upper-bound entry over the 16 counts (exact algebraic sides; each value by its decimals cut where certain and an ellipsis, with the closed forms at 126 and 295), reported (V0/C0), credited to Evan Daniel after each packing's finder as the case records credit them, as a refinement; minimality source-asserted. Draft significance S2, as T-120 to T-123 (an exact algebraic form of a packing the record credits). The case lanes stay until adoption.

## Price

- Replay: the source's verify_exact.py on all 23 data files from the retained copy, plus a mutated-input control per checker (a moved square, an enlarged side): about 4 min wall on 8 processes at the source, so at most about 0.6 CPU-h; 263 and 297 (9 MB and 7 MB) dominate. Within the 40 CPU-h cap; runnable once stage 2 retains the source. Validation bead under this one.
- Irreducibility of each p over Q: seconds to minutes with FLINT or sympy (unmeasured); decides the minimality the source asserts.
- A second route here: sqpack.witness.exact_verify decides number-field witnesses (devtools.algebraic_witness_reports, #574's format, degrees 2 to 8 so far); evand's minpoly format needs a converter, a W7 slice; cost at field degree 12 to 41 unmeasured.
- Lean Packs n S* for the 20 counts of field degree <= 20 is not offered; nothing to price.

## Disposition (proposed)

Import. Stage 2: a packet evand-exact-cur-2026-10-16 at 7d1407a, scope search/exact/cur/ and search/exact/verify_exact.py, the 23 data files pinned by digest (or hosted), with its bibliography key. Not done in the triage pull request: the key would make the site a release-impact candidate, which the stage 3 pull request carries anyway. Stage 3: the ledger, then one entry at the 16 counts; 51, 70, 153, 207, 172, 263 and 297 not recorded, with the reasons above. RP-3 (owner) gains a second configuration and checker at 70, 153 and 207.

## Draft acknowledgement (not posted; stage 7 posts it after the pull request carrying this triage merges)

@evand, thank you for the batch. We have pinned evand/square-packing at 7d1407a, search/exact/cur/ with its 23 data files (21,474,827 bytes, each by SHA-256), and the checker search/exact/verify_exact.py, and compared each S* exactly, by the sign of p at every rational the record holds or has pending at its count. At 16 counts (88, 102, 123, 126, 175, 199, 204, 232, 258, 259, 266, 267, 292, 295, 301 and 302) S* is below all of them, by 1.5e-99 (204) to 7.8e-35 (126). At 51 it is the (16+5√2)/3 the record already holds from #432. At 70, 153 and 207 it agrees to 40 places, at the same degree, with the algebraic sides PingYou Ltd reported in #574 on 13 October, whose adoption is an open decision for the owner; your configurations and checker are a second route to those values. At 172, 263 and 297, #574's rational certificates, which three exact routes here decided, are below your S* by 1.2e-62, 9.2e-63 and 6.6e-63, so by the order rule those three are not recorded. Next we retain the directory in a source packet, replay verify_exact.py from it with mutated controls (about half a CPU-hour), and record the 16 counts as reported. We will reply here when that is on main.

Three questions for the record:
1. At 172, 263 and 297, S* is above a valid packing's side by about 1e-62. Is S* there a stationary point of the contact system with the pinned free coordinates (14 at 172) rather than the least side of the packing?
2. Which program checks that each p is irreducible? verify_exact.py checks p(S(t)) = 0 mod f and the isolating interval.
3. At 207, does the unverified pair (73, 74) on your re-solve of the register's witness point at anything in that witness, or only at the re-solve?

blocked_on: none

## Notes

2026-10-16 ~05:05Z, ecstatic-edison-intake-1016, state for recovery: stage 1 triage is done and in this bead's description (claim map, pin and digests, price, disposition, draft acknowledgement). Pushed on origin claude/ecstatic-edison-8en33t-intake-1016 at bd1f40425 (no PR yet): 09463a2af adds #639's and #640's entries to packing/campaign/result-requests.yaml (triage: done, results queued with beads, no reply posted), moves #622's read_through to its author's AI answer, and adds two evand reads to intake-watch.yaml (44a105e, bead think-0ayk; 7d1407a, bead think-phyb); bd1f40425 adds the methods survey's no-change record in release.py (render at e2e018f3 byte-identical in 42 files). Validation at bd1f40425: check_requests exit 0 (#639 and #640 reply due), --github 0 differences, packing-validate --records exit 0 (52/110 steps, 134 s), check_release_impact OK, release_pin --check OK (no re-pin), pytest of the requests, sweep and release tests 145 passed; packing-validate --push was running. New beads: think-g59l (#639 replay, <= 0.6 CPU-h), think-nqnl (#640 full build, held), think-o40t (#640 review), think-ve84 (backlog). Next: the owner's think-xik9 (the X announcement as a source on #640, sq19 watched), then the draft PR (labels intake, S1).

2026-10-16 ~05:25Z, ecstatic-edison-intake-1016: draft PR https://github.com/jlevy/squares/pull/642 (labels intake, S2) at 71f6a413e on claude/ecstatic-edison-8en33t-intake-1016. 71f6a413e adds the #640 stage 2 packet packing/resources/web/fitzharding-n19-lean-2026-10-16 (sq19 whole at 34fb2b7, release archives pinned by digest, the X announcement retained; acquire_source --check prints PACKET_MATCHES_ITS_CONTRACT), a resources README row and section for [Fitzharding n19 Lean 2026] (its bibliography.yaml entry waits for stage 3), and #640's entry records the announcement as a source and names think-xik9. At 71f6a413e the records tier exits 0, the survey render is byte-identical again, and the sweep on the branch watches sq19 (44 repositories, 18 heads pinned). packing-validate --push at bd1f40425 timed out in its reachable tests (285 files, 900 s) with one failure it did not name; a separate run of those files was in progress. Hosted CI was pending at opening.

2026-10-16 ~05:58Z OWNERSHIP TRANSFER by the owner's word to the overnight coordinator user-eb (epic think-hg5s): "We have some changes with the regularization and a couple other things from another agent that you should take over and incorporate into your work." The ecstatic-edison lanes should stop work on this bead and its branch, and record any unpushed state in a note here. user-eb's lanes fetch before every push and stop if the branch moved.

2026-10-16 ~06:45Z user-eb-intake-1016: stage 2 done and stage 3 ledger run on claude/intake-2026-10-16-records-639-640 (stacked on #642's 71f6a413e), head 24415a012, pushed. Packet packing/resources/web/evand-exact-cur-2026-10-16 (acquire_source --check PACKET_MATCHES_ITS_CONTRACT; 19 forms retained as upstream gzip, 204/263/267/297 pinned by size+SHA-256; verify_exact.py pinned identical_to the ad86d42 copy). Ledger packing/campaign/issue-intake/upper-bounds-20261016 (read_at_main e2e018f3): #639 recorded at the triage's 16 counts; ties at 51 (T-126) and 70/153/207 (T-174), decided exactly by review/exact_sides.py; not recorded at 172/263/297 (PR #574 rationals walked as a report there). Agrees with the triage. Next: register entry (T-NNN last), bibliography key, #640 entry, views, replay.

2026-10-16 ~07:15Z user-eb-intake-1016: draft PR https://github.com/jlevy/squares/pull/651 (base claude/ecstatic-edison-8en33t-intake-1016, head f5c4105cc on claude/intake-2026-10-16-records-639-640). a2167a03a registers T-193 (#639, 16 counts, draft S2) and T-194 (#640); f5c4105cc adds the papers' no-change records and tests/test_evand_exact_cur.py. Replay (think-g59l) running in scratch with a resumable cache. Next: replay evidence, re-pin, site edition last, PR body, announcement, reply drafts.

2026-10-16 ~08:12Z user-eb-intake-1016: stages 2-4 done on PR #651 (head 523d8c14f, base #642's 71f6a413e). T-193 = #639 at the 16 counts the 16 Oct ledger records, V3/C3 after the replay (think-g59l), draft S2; evidence E-evand-639-exact-sides-report and E-evand-639-verify-exact-replay, cited also in the 16 case records' evidence lists (no lane/status change; check_certificate_citations requires it); regularizations of T-174 (12 counts) or T-186 (175, 204, 232, 302), identity basis source-claim; bibliography [Daniel exact current records 2026-10-16] credit 'Daniel after Xu, Chaoweeraprasit, Ostashev, Couzo, PingYou Ltd, Gupta, Polkovskyi, Levy'. Ledger verdicts: recorded 88, 102, 123, 126, 175, 199, 204, 232, 258, 259, 266, 267, 292, 295, 301, 302; ties 51 (T-126), 70, 153, 207 (T-174, exact by resultant); not recorded 172, 263, 297 (PR #574 rationals smaller by ~1e-62). #639's request entry maps exact-sides-below-record to T-193. Verdict comment drafted by devtools.intake_comments from packing/campaign/issue-intake/upper-bounds-20261016/comments.yaml (records_pr #651), not posted; it names no T-NNN and may go out by stage 7's verdict-comment rule. Import reply drafted below, posts after #651 and #642 merge. Can close only after the reply is posted (answer bead).

2026-10-16 user-eb-intake-1016: DRAFT import reply for #639 (not posted; stage 7 posts it after PR #651 and #642 merge, rendered from main with check_requests --draft 639, the id and rungs checked against main and the deployed site first; it replaces the triage acknowledgement above, which was never posted). The report-order verdict comment is drafted separately by devtools.intake_comments from packing/campaign/issue-intake/upper-bounds-20261016/comments.yaml; it names no id and may go out first, by stage 7's rule.

@evand, thank you for the batch. It is imported and registered as T-193 at sixteen counts, confirmed: V3/C3, reproduced with your own checker (re-run, not re-implemented), not yet reviewed.

What we did: retained search/exact/cur/ at 7d1407a in a source packet, with 19 of the 23 data files kept as published and the four largest (204, 263, 267, 297) pinned by size and SHA-256, and your verify_exact.py pinned against the identical copy we already hold. We then ran verify_exact.py, read first and unchanged, from that copy on all 23 files: 23 of 23 VALID with the statements your data/verify.txt prints (about 21 CPU-minutes over two processes), and 76 of 76 mutated controls refused, four at each of the 19 retained forms (a square moved 1e-6 through the wall it touches, the side raised by 1e-6 in K, the side's interval moved below its root, a duplicate square). SymPy factors every p as irreducible over Q, which settles the minimality your issue asserts.

By the report-order rule (the owner's, of 14 October), T-193 records 88, 102, 123, 126, 175, 199, 204, 232, 258, 259, 266, 267, 292, 295, 301 and 302, each below every earlier report there, credited to you as an exact form of each packing after its finder. At 51 your side is the (16 + 5√2)/3 the record already holds from #432; at 70, 153 and 207 it is exactly #574's algebraic side (the resultant of #574's witness is your p), a tie with the earlier report, and your configurations and checker are now a second route for the owner's open decision on those three; at 172, 263 and 297 #574's rational certificates are below your sides by about 1e-62, so those three are not recorded. The case pages keep their houses until adoption, which is the owner's, with #574's.

Two questions, if you have a moment:
1. At 172, 263 and 297, S* is about 1e-62 above a valid packing of the same contact graph. The data files pin free coordinates (14 at 172); is S* there the solve with those pins rather than the least side of the packing?
2. At 207, does the unverified pair (73, 74) on your re-solve of the register's witness point at anything in that witness, or only at the re-solve?

2026-10-16 ~09:55Z user-eb-intake-1016: final head ef43dd02f on PR #651, hosted CI all green (08:29Z). 2ba1d9b0a replaced the hand-added case citations (which tests/test_house_adoption.py refused at n = 102) by a deferral in packing/devtools/certificate-citation-deferrals.yaml naming THIS bead (think-phyb) for E-evand-639-verify-exact-replay, blocked on RP-3 and T-174's held houses: this bead must stay open (or the deferral gets a new owner) until a house adopts a T-193 side or the owner rules, or check_bead_tree fails the next change to a deferral record.

2026-10-16 ~11:00Z user-eb-addr-642-651: #642 review A addressed at ae64ab461 (A1 fixed, A2 declined/handled by #651, A3 fixed in description, A4 fixed in the chain by a2167a03a); reply https://github.com/jlevy/squares/pull/642#pullrequestreview-5546756684. #651 in progress: merged ae64ab461 (1f954b060), T-193 held at V0/C0 pending think-7qxm, replay re-running with the fixed driver (A5/A6).

2026-10-16 ~11:05Z user-eb-addr-642-651 (PR #651 review A, A2): the DRAFT import reply for #639 above is SUPERSEDED in its first paragraph. T-193 is now held at V0/C0 (reported) until the stage 4 review lane think-7qxm returns, so the reply must not say confirmed or V3/C3; check_requests --report shows #639 at 3 of 4 settled, closeable no. Replace the first paragraph with: '@evand, thank you for the batch. It is imported and registered as T-193 at sixteen counts, as reported (V0/C0). We replayed your own verify_exact.py on all 23 files (re-run, not re-implemented), and our review of that replay is under way; until it is done the result is reported and replayed, not confirmed.' In 'What we did', take the CPU time and the irreducibility line from the refreshed receipt at PR #651's head (every polynomial squarefree and irreducible: one factor of multiplicity 1). Render from main with check_requests --draft 639 as before; it states V0/C0 until the review's exit raises the rung, and a follow-up reply then reports the raise.

2026-10-16 ~11:30Z user-eb-addr-642-651: PR #651 pushed at e45883525 (2bcd0a7c8 replay driver A5/A6 + refreshed receipt, 23/23 VALID, 76/76 refused, 23/23 squarefree+irreducible, 1484.5 CPU s; c86682367 T-193 held at V0/C0 pending think-7qxm, E-evand-639-verify-exact-replay and its case-citation deferral removed until the stage 4 exit (draft text at ef43dd02f), A3/A4 claim fixes; e45883525 re-pin). Next: records tier, focused tests, description, disposition reply, CI.

2026-10-16 ~11:55Z user-eb-addr-642-651: #651 review A addressed at 3a230d30f (CI green, runs 38895014466 / 38895014273); reply https://github.com/jlevy/squares/pull/651#pullrequestreview-5547382157. T-193 held at V0/C0 pending think-7qxm; the stage 4 exit must restore E-evand-639-verify-exact-replay (draft at ef43dd02f, numbers from the refreshed receipt: 1,427 CPU s positives, 58 s controls, 23/23 squarefree+irreducible) and cite it, and re-add a case-citation deferral if houses still cannot adopt. Deferrals opened: think-e1u5 (formal stack, A1), think-v860 (ledger start, A7).

2026-10-16 ~12:25Z coordinator user-eb: PR #651 MERGE-READY at b33ce8ffd (senior+correctness Review A 0/2/1/5 and follow-up Review B 0/0/0/2 addressed: T-193 held at V0/C0 until think-7qxm; T-194 registered V0/C0, S5 draft; A1 informal chain deferred think-e1u5; A7 think-v860; B1 cache key fixed; B2 noted on think-7qxm). CI green. Merge after #642, retargeted to main. The T-193 exit and the T-194 C1 mapping are lane K's PR (think-9e3w), stacked on #655.

Replacement stage 7 reply draft from #660's addressing pass: see the #639 section of the file attached below. Not posted.

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

2026-10-18 W1 intake (think-xmxb): New evidence at evand/square-packing 5ca0dc3ae7a4eebce16838bf41bedc2ce7e98241: exact three-angle witness at232 over degree14 K(sqrt2), same side as degree7 exact form, verify_exact.py claimed VALID and Lean Sqpack.Exact.Packs.N232R3.packs standard axioms; tasks/reg-cert-232/README.md. Retain/review and classify evidence update versus separate formalization. No build/replay here; T-193 underlying result keeps identity.

2026-10-19 lane-658: taken over by the 19 October handoff (issue #684) to land PR #658. Worktree branch lane-658/records-193-194: fast-forwarded #658 head 3022eb984 to checkpoint codex/handoff-20261019/658 d0b9ec2f9, merged origin/main 14fd9e27f (#685, v0.7.32) cleanly as c41eb33ec. Next: paper decision (AM1), re-pin, review round D, edition last, merge; then stage 7 replies.
