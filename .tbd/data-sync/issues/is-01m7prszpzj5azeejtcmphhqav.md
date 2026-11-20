---
type: is
id: is-01m7prszpzj5azeejtcmphhqav
title: "Import #1031: Joost de Winter's s(299) <= 17.793636991744 (0.0074 below the house), JoostdeWinter/square-packing n299/ at 497eb478"
kind: task
status: in_progress
priority: 1
version: 10
delegate: c2-imports
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-18T07:26:42.911Z
updated_at: 2026-11-20T08:59:19.010Z
started_at: 2026-11-18T07:33:41.966Z
---

## Notes

2026-11-18T07:36Z w6r2-dewinter-1118: claimed. Triage, read-only (issue read 07:32:46Z, no comment, intake label): #1031 (06:44:45Z) names 497eb478 (06:34:51Z, 'Add the packing for n = 299'; 3293038d at the same second adds REGISTRATION.md and SHA256SUMS; 72323289/aae089c3 at 07:30-07:31Z touch n109 only, #1012's). n299/ at the pin: README.md, n299_exact.json (blob 0a8e8120, SHA-256 199e6132...4a9c), n299_witness.yaml (Witness/v2, corners), n299_record.png, verify_exact.py, check_area.py; MIT per the repository. Exact side 17793636991743040580325825384225613703947282755372586749208848013397/10^66 = 17.79363699174304058, 12-place ceiling 17.793636991744 = the issue's print. Measured against main (86284ec20), not the issue's T-277: the house is T-325 (#1009, Polkovskyi's re-solve of Daniel after Ozden), 2225125554281470853018439796251/125000000000000000000000000000 = 17.8010044342517669; the claim is 7.3674e-3 below it (the issue's T-277 print 17.801004434255294 is 3.53e-12 above T-325). Kaggle: the issue says Nick Sarris reported 17.793636991746555 at 01:07:56Z on 18 Nov with no coordinates found; that is 3.51e-12 above this side, a score with no packing, so not a result here (priority question for the review/owner only if coordinates surface). Lineage per the issue: diagonal slices from Panoras's compilation v17 packings of 372 (prvsiyan 'A Square Deal') and 335 (areebbb, jazivxt, alexchilton, prvsiyan), then local optimization and a diagonal reflection. AI: GPT-6.2 Sol (OpenAI) and Claude (Anthropic), under his direction. Path: upper bound below the house, the house rule; stages 2-3 on claude/intake-2026-11-18-import-1031 after #1029, #1024 and #1021/#1022's PRs; blind review (tbd-strong-max) requested from the coordinator now. Nothing retained yet (scratch download only).

2026-11-18T08:20Z w6r2-dewinter-1118: R-1031 writes on think-r3tn (coordinator); this lane does not read think-r3tn, nor any R-1031 section here, until #1031's review merges. Nothing measured yet for #1031 beyond the triage's side and gains (scratch download at 07:33Z).

2026-11-18T08:33Z w6r2-dewinter-1118: for #1031's PR Limits: at about 08:30Z the coordinator's message relayed R-1031's summary verdict (accept; 7.37e-3 below T-325, about 2e24 times T-325's margin; a new arrangement; S3), before this lane ran any measurement of #1031 beyond the triage's side and gain (07:33Z). The import's replay, controls, identity and margin measurements will be its own programs' outputs under a controls plan hashed before they run.

2026-11-18T09:00Z w6r2-dewinter-1118: for #1031's PR Limits (coordinator): the 08:30Z relay of R-1031's verdict included its S3 reading before this lane scored #1031, so the import's significance score is not blind to the review; and at about 08:58Z the coordinator relayed that R-1031's senior review found 210 of 299 squares coinciding with T-325 under one rigid motion (the review lane is measuring whether generic or a continuation). The credit at 299 is not settled until #1036 merges with that answer; the import's own identity measurement (measure_identity against T-325 and T-277) will be run and reported as its own.

2026-11-20T07:05Z c2-imports (coordinator bold-ritchie-coord1120): claimed from w6r2. Controls plan for 299, written before any program of this lane read the certificate: packing/campaign/issue-intake/upper-bounds-1031-20261120/controls-plan-299.txt, SHA-256 b8a816b21af8d6b6346791170c82f925197d30b35d4d047c344019f0a3ea247f, hashed 2026-11-20T07:04:05Z; worktree scratchpad/c2-imports, branch claude/intake-2026-11-20-import-1021 (from main 1015fc175f), one PR for #1021, #1022 and #1031. Watched repo read at 21d944c (19 Nov 18:44:48Z): n299/ last touched by 3293038 (REGISTRATION.md, SHA256SUMS); pin 497eb47 as the issue names. This lane has read this bead's earlier notes (the 08:30Z and 08:58Z relays of R-1031) and will say so in the PR's Limits; it does not read #1036 or think-r3tn until the coordinator says #1036 merged.

2026-11-20T07:27Z c2-imports: packet de-winter-s299-upper-bound-2026-11-18 (licence, root README, n299/ at 497eb47; checkers pinned against byte-identical copies, never run; figure by digest; the certificate and witness digests equal 3293038's SHA256SUMS), claims against main 1015fc175: 7.3674e-3 below T-325. Replay at a203f4a752 (07:07-07:10Z): both routes accept, duplicate and outside refused, check --replay admits 3 jobs; sharp controls 11/11 as_expected (branches W1: far-wall clearance 6.42e-67; P1: least gap 1.05e-74, squares 175/137; N0: a square touches a near wall; E0). Difference from the plan's letter: the E0 wall enlargement (square 129) is not clean, so past contact both routes name overlap as well as container and shape; the module predicts that exactly for a square that cannot grow without closing a pair (every pair gap here is far below 1e-30), and the plan's E0 line names wall and shape only. Recorded here, in the packet README and the PR. Margins (devtools.contraction_margin): T-325 3.5612e-27 (squares 71, 140), T-277 3.4040e-12 (179, 194), own 6.4244e-67 (137, 175); option D: new. Identity (measure_identity vs T-325, T-277): no box symmetry pairs it one to one; under symmetry 3 the optimal assignment moves 127 squares beyond 0.1 (largest 1.074), 18 of its 114 tilted squares pair with tilted squares of the same sign. The relayed rigid-motion finding (210 of 299) is not a box symmetry and this tool does not measure it; credit at 299 waits on #1036. L-step scan: main's consequences unchanged.

2026-11-20T09:00Z c2-imports: T-333 registered at 07:36Z (5b2adb973f), after the replay (a203f4a752, 07:23Z) and ledger (647d806b21, 07:24Z). Coordinator reported #1036 merged (4443f7f90) at about 08:12Z; this lane read docs/project/reviews/review-2026-11-18-de-winter-1031.md from origin/main at 08:12:33Z, after all its own 299 work was committed. Mapped: V-de-winter-1031-review-check, E-de-winter-1031-review-exact-feasibility (rv1031_check ACCEPT, 44,551 pairs, 36 controls: 34 as stated, 2 as the side rule gives, F3), external_review on the report evidence, T-333 reviews block (accepted, covers T-333), novelty previously-published per After the Freeze A1 (not the frozen N5 line), credit Joost de Winter after the compilation's packings: a new arrangement relative to every packing at 299; the 210-square T-325 motion is a generic upright lattice plus the T-248 band (A2), not a continuation. Significance S3 confirmed by the review. Adopted at 299 in the pass of 20 November (adopt_houses 08:57Z); strong runs on 299 next.
