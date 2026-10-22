---
type: is
id: is-01m50qjc49k5cwy2cw5dqgjj76
title: "Import mstrmg: n = 366 registration request (#624)"
kind: task
status: in_progress
priority: 1
version: 10
delegate: user-eb-intake-residue
labels:
  - result-import
dependencies: []
parent_id: is-01m50gnwbxd5kxbynyx9nd162p
hold: null
hold_until: null
created_at: 2026-10-15T21:30:23.753Z
updated_at: 2026-10-22T13:13:24.393Z
started_at: 2026-10-15T21:30:24.918Z
---
Opened 2026-10-15T20:02Z during this pass; labelled intake by lane D. Needs stage 0/1: an entry in result-requests.yaml (triage pending -> done), source pin, comparison against the beyond-horizon rows (n > 324) and #627's rows, and the report-order rule.

## Notes

2026-10-15 lane E (ecstatic-edison-lane-e): stage 0-1 triage of #624, on branch claude/ecstatic-edison-8en33t-intake-624 (base claude/ecstatic-edison-8en33t-records-1016, PR #627). Entry in packing/campaign/result-requests.yaml at cac85a60a.

Source pin: gist mstrmg/c3350a7e34fa344ae6a0c79293e6b2ab at 31e69614b69810afb91c99b9423c5deac3a5fe10, its only commit (2026-10-15T19:56:12Z). One file, n366.cert: 34,915 bytes, blob 09579a7e9d0e530796eb24a3aedb2f0809589468, SHA-256 9cd599bb759c9392a6baea8c305c64bec7e05bd5e5d2bd9db5649cb81e0853ae. No licence stated. Not retained in a packet, as #582 was not, because nothing is imported; the entry pins it by revision and digest.

Claim (the source's only one): s(366) <= 19.738804630679, as the issue prints it. The certificate's own side is 19738804240214197/1000000000000000 = 19.738804240214197, 3.90e-7 below the print. Rounded up at 12 places it is 19.738804240215, not the print, so the importer's admission rule (exact side rounds up to the print) would refuse it as stated; it proves slightly more than the issue says.

Exact check (triage, priced at minutes): from packing/, `python -m devtools.evand_exact_certificates check --certs SCRATCH --n 366 --workers 1 --receipt SCRATCH/receipt.json` on a copy named n-366.cert. exact_verify VALID and independent VALID: 66,795 pairs each, least pair gap 9.99e-13, least wall clearance 2.51e-12; 44.3 CPU-s (29.3 + 15.0), 45.8 s wall. The receipt stays in scratch and is not committed.

Comparison, exact (devtools.upper_bound_reports.relation; Göbel by the exact Q(sqrt 2) sign of couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py):
- Rows at 366 on this base: none among the 341 beyond_horizon_claims rows. The ledger's start is therefore the grid, ceil(sqrt 366) = 20; #624 is 0.2612 below it.
- The row at 369 (couzo-extended-range-reports-2026-10-08, 19.740417287556077) bounds 366 only by monotonicity; #624 is 1.613e-3 below it, the issue's "about 0.0016".
- franciscouzo/square-packing@4e4c8ce, first committed 2026-10-15T00:31:53Z, certificates/best/n366.cert: blob 8b30c1f7ba5ce265827096e5df5fd09722fa0faf, SHA-256 bfd83f906617a1a5ce6ac9c31fb57271c08f66d7a3037148c8d2c796d4948da4, equal to the digest its manifest.json states. Side 14 + 4 sqrt(2) scaled by 1 + 1e-24, 19.656854249493 rounded up. The manifest credits "PingYou Ltd (BuddenPing)", category "derived exact" from a parent n = 294 certificate (1 tile, 2 layers). #624 is 8.195e-2 above it. The file is unchanged at the head, 58a7833. It is one of think-yfoo's 341 rows.
- 4e4c8ce certificates/best/n369.cert (Francisco Couzo, local), 19.707106781187: #624 is 3.170e-2 above it (by monotonicity only).
- Göbel at 366: the Göbel strip for 369, 19 + sqrt(2)/2 = 19.707106781187 (Kingbird-Göbel-strips): #624 is 3.170e-2 above it (sign +1). The 4e4c8ce 366 certificate is below it.
- Other watched sources, at their heads: BuddenPing/square-packing-certificates 318ab94, BuddenPing/squares (a fork of this repository), TheSnakeFang/squarepack-certs 078789a and evand/square-packing 1038892 have no file for 366. Daniel's composition packets hold 364 and 365 only. No other issue on jlevy/squares reports 366 (gh search).

Report order and verdict: franciscouzo/square-packing@4e4c8ce (00:31:53Z) before #624 (20:02:39Z). By the owner's rule of 2026-10-14, with a publication in a watched repository counted from its first commit, #624 is NOT RECORDED: above, held by franciscouzo/square-packing@4e4c8ce. If publications were not counted, the start would be the grid and #624 would be recorded; if #613 makes Göbel's constructions the baseline, it is not recorded either way.

Method as the source gives it: started from Francisco Couzo's 369 packing, removed three squares, and optimized again with the author's own search (relax and basin hopping, then an exact check). The 19.740417287544 the issue quotes is Couzo's 02f9690 certificates/n369.cert (exact side 19.7404172875438...).

Credit as the source gives it: "Found by: @mstrmg"; "Fransico Couzo gets some credit because I based my find off of his 369 packing". Name: Miles Gray, from #582's "Credit name. Miles Gray".

AI assistance as the source gives it: "Claude code opus 5.5 was used to make the program used on my own device".

Price: no further replay; nothing is imported.

For think-yfoo: when the 4e4c8ce import writes its claims record, #624 is a later pending report at 366 (exact side above).

Draft reply, to post after the pull request carrying this entry merges, once main says what it says (stage 7). It names no id and links nothing outside main:

@mstrmg, thank you for the 366 packing in #624, and for the clear certificate, method and credits.

We pinned your gist at revision 31e69614b69810afb91c99b9423c5deac3a5fe10 (n366.cert, SHA-256 9cd599bb759c9392a6baea8c305c64bec7e05bd5e5d2bd9db5649cb81e0853ae). Both of this repository's exact checkers accept it, with every one of the 66,795 pairs separated, at the certificate's own side 19738804240214197/10^15 = 19.738804240214197. That is 3.9e-7 below the 19.738804630679 the issue prints, so the certificate proves a little more than the issue states.

We are not importing it. The project's rule for several reports at one count records a report only when its side is below every side reported before it, and a certificate published in a repository the project watches counts as reported from its first commit. `franciscouzo/square-packing@4e4c8ce`, first committed on 15 October at 00:31:53 UTC, before this issue, publishes a certificate at 366 with side 19.656854249493 (rounded up at 12 places; it is 14 + 4√2, scaled by 1 + 1e-24), 8.19e-2 below yours. Its index credits PingYou Ltd (BuddenPing), from whose 294 packing it is derived. Göbel's classical strip construction for 369 squares, of side 19 + √2/2 = 19.707106781187, also holds 366 squares once three are removed, and is 3.17e-2 below yours.

The 4e4c8ce certificates beyond 324 are awaiting import here.

If you have improvements at other counts, the fastest route is a new issue that points to an exact certificate in a repository, pinned at a commit. It helps to compare first with the smallest certificate that index lists at the count (`certificates/best/manifest.json` in `franciscouzo/square-packing`) and with Göbel's square and strip constructions.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-15 22:25Z lane E: draft PR https://github.com/jlevy/squares/pull/631 (stacked on #627's claude/ecstatic-edison-8en33t-records-1016; labels intake, S1; head cac85a60af82be78c9383add112d8f243f4d0d3c). Validation at cac85a60a: packing-validate --records 51/51 of its tier (105.8 s); --push 65 of 66 steps, its whole-suite step 18,768 passed and 3 failed (two process-group reaping tests, "worker process group remained alive after SIGKILL", and one site load budget, longestTaskMs 339 > 300), each failing again in isolation and none reading the requests record; 150 focused tests passed; hosted CI 15 passed, 42 skipped, 0 failed. Keep this bead open: it answers #624. After #627 and #631 merge, post the reply drafted above from main and record it under #624's replies; close this bead when the author has had the chance to answer.

2026-10-15 23:45Z coordinator: merge plan updated after the restack: #631 is the top of stack #632 (#627 -> #628 -> #631), landed with gh stack merge 631 --yes --merge; the #624 reply posts from main after the stack merges.

2026-10-16 ~05:25Z, overnight coordinator user-eb (epic think-hg5s): ownership transferred to user-eb-intake-residue (bead think-mu5v) from ecstatic-edison-lane-e (last update 2026-10-15T23:44:00.869Z), because the sweep of 05:08Z reports this bead's blocker resolved and the owner asked tonight for the intake to continue. The lane resumes the work, closes the bead if it is done, or rewrites blocked_on.

2026-10-16 ~06:00Z user-eb-intake-residue (lane A, think-mu5v): resumed after the sweep of 05:08Z read #627 (merged in stack #632) as this bead's wait. Done since: the reply drafted above was posted from main as https://github.com/jlevy/squares/issues/624#issuecomment-6206054646 (2026-10-16T01:38:34Z) and is recorded under #624's replies on main (kind acknowledgement, via #637). No answer from the author yet (one comment on #624, ours). Not closed: #624 is open with this bead as its answer_bead in result-requests.yaml, and the owner's decision 4 in think-l3oo (whether a watched-repository publication counts as an earlier report; if not, #624 is recorded, and its printed side differs from its certificate by 3.9e-7) decides whether #624 closes as not recorded or is imported. check_requests --report marks #624 closeable; lane A does not close it (brief: decision 4). Next: the owner's ruling, then either the final comment and close, or the import with the author asked which side is meant.
blocked_on: think-l3oo

Correction (user-eb-intake-residue, 2026-10-16T05:47Z by date -u): the '~06:xxZ' times in this lane's notes of 16 October are about an hour late; they were written between 05:30Z and 05:47Z. The site pages were read at about 05:35Z. No condition changes: every last reply named is still more than a day old.

2026-10-22 c-triage-1022b (read-only): optional follow-up on #624.

- The posted reply cited `4e4c8ce`'s certificates/best/n366.cert (2026-10-15T00:31:53Z),
  8.19e-2 below #624.
- The Couzo history records PR (after #719's) records that certificate as the current
  row at 366, 0.343 below the grid, where `main` holds no row today.
- A one-line note linking the row is optional. The close condition is already met.
