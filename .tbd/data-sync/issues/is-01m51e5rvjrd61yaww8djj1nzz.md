---
type: is
id: is-01m51e5rvjrd61yaww8djj1nzz
title: "Import evand: exact algebraic sides for 22 current best-known packings (#639)"
kind: task
status: open
priority: 1
version: 31
delegate: null
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
updated_at: 2026-10-23T06:16:53.249Z
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

2026-10-20: #690 (merged 4b8aec9a6) recorded the posted 19 October replies on #639 (final, issue closed) and #640 (import). The posted #639 final reply dropped the drafts' 207 question ('does the unverified pair (73, 74) on your re-solve of the register's witness point at anything in that witness, or only at the re-solve?'); whether to ask it as a follow-up on #639 is an open owner decision. #640's s(19) questions remain held under think-a4x3.
