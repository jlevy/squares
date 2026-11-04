---
type: is
id: is-01m6jqkyrwaxf85nz7bytdv6t9
title: "T-262 to V3/C3: rerun mixed_n94_L9965's whole-net control under think-4uun's enclosure rule, enter the replay evidence, adopt 1993/200 in n-094's verified lane (#890, intake lane L37)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: bold-ritchie-l37
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-04T07:33:17.211Z
updated_at: 2026-11-04T08:56:05.729Z
started_at: 2026-11-04T07:33:23.700Z
---
Intake lane L37 (bold-ritchie-l37). #892 (merged 0bc5a08c5, think-4uun) replaced AXIS_ROUNDING with axis_captures_agree. Rerun sqverify_fast_census --family mixed --control --only mixed_n94_L9965; enter E-ozden-890-n94-9965-sqverify-fast-replay with the 3 November stage 4 review as its audit_record; T-262's rung as check_results derives it; n-094's verified lower lane to 1993/200, T-091 superseded at n = 94; #890's result-requests entry no longer blocked on think-4uun; generated views; DATA_REVISION re-pinned. Also the nits of #892's confirming review (sqverify_fast_axis docstring and pins, the fine-net auditor's derived_from refusal, the n68 complete-indices mismatch, the packet README, float(bound)). One draft PR; the coordinator posts #890's reply.

## Notes

2026-11-04 (bold-ritchie-l37): PR #898 (draft, labels intake and S2), branch claude/bold-ritchie-xo28us-l37, head 1118ab04e.

- Control: `sqverify_fast_census --family mixed --binary sqverify_fast/target/release/sqverify-fast --out benchmarks/measure-verifier/census-mixed --control --threads 2 --only mixed_n94_L9965` (binary 567a0fd5, source d97758bb, 07:35:14Z to 07:37:44Z, nice -n 19): CONTROLS_REFUSED r=277; 99/100 mutant refused at 600 of 600; near-threshold refused; axis capture in [0.9930860126842824, 0.9930860149308234]. Receipt mixed_n94_L9965.control.json, sha256 be73798aca4a369f195b3d2ec1d7754aae2bebc57cc2bf0d537a265fab813616 (commit 103bf530c).
- Records (d2924a31e): E-ozden-890-n94-9965-sqverify-fast-replay; T-262 V3/C3 (check_results derives it); n-094 verified lower 1993/200; #890 s94-dilation validation dropped (think-4uun no longer named).
- Nits of #892's confirming review: (a) 714788ded, s(94) pinned to an instrumented scratch build (original upper 1.0031171867987096); (b) 7aa242739, auditor admits derived_from and --candidate, full n94 run PASS 37.5 s; (c) filed think-swu4; (d) READMEs refreshed (records commit and 6ddb9047b); (e) 714788ded.
- Release: no-public-change record 3f08f6455 (four papers byte-identical, 69 files x3); DATA_REVISION re-pinned to d2924a31 (1118ab04e).
- Local validation: --records --jobs 2 55/55; --edit --jobs 2 70/71 with the type floor passing through uv run (0 errors).

Remaining: hosted CI on the head; coordinator's merge; #890's reply from main. think-2agl's claim was skipped (held by bold-ritchie-l33), so its revised notes are staged below for the coordinator to apply once it transfers the bead (`tbd update think-2agl --notes-file <this block>`).

=== Revised think-2agl notes (to replace that bead's notes whole) ===

2026-11-03 (bold-ritchie-l33): DRAFT of #890's reply, revised after the stage 4 review and review A of #891; not posted. Post it only after #891 merges and the deploy is verified: render from main with `check_requests --draft 890`, check main and the site say what it says, adjust T-NNN if renumbered, post, then record it under #890's replies (kind: final, closing the issue) in the next change. #890 is closeable once T-262 is on main: its validation names think-4uun; the licence and n = 31 questions go in this closing comment and hold nothing open.

2026-11-04 (bold-ritchie-l37, think-qpq0): DRAFT revised for T-262 at V3/C3 (PR #898, intake lane L37); not posted; it replaces the draft of 3 November. Post it only after #898 merges and the deploy is verified: render from main with `check_requests --draft 890`, check that main and the site say T-262 is V3/C3 and that n-094's verified lower bound is 1993/200, post it, then record it under #890's replies (kind: final, closing the issue) in the next change. #890's `s94-dilation` result names no validation bead after #898, so nothing holds the issue open; the licence and n = 31 questions go in this closing comment.

---

Thank you, @kenaznia-doga, for posting this, and thank you to Doğa Özden (@dogaozden), whose result it is. This reply records what was done with #890 and closes the issue.

**Received and retained.** `kenaznia-doga/s94-lower-bound` at `9d76ad5`, kept whole but for `.gitignore` as the source packet [`ozden-s94-lower-bound-2026-11-03`](https://github.com/jlevy/squares/blob/main/packing/resources/web/ozden-s94-lower-bound-2026-11-03/README.md). Every digest the issue states holds: the certificate file (`116c8342…16f8`), its JSON text (`b8b03ee8…749c`), and Hosono's `candidate.json` at `797bdf6e` (`64d81953…0667a`), which equals the copy this repository already keeps for T-091.

**What was checked here.**

- **Premises and the dilation.** A new first-party tool, `devtools.audit_dilated_measure`, recomputes them in exact rationals from the retained bytes:
  - format M on the declared net, and lemma N0's five conditions, with B(1 + D) = 2387749705363/2388000000000 < 1;
  - the total 94 − 1/100000;
  - each of the 853 rows exactly λ = 1993/1990 times Hosono's, its mass unchanged;
  - the certificate's JSON text regenerated byte for byte from Hosono's candidate by the rule `tools/rescale.py` states.

  It decides no coverage.
- **A complete replay.** This repository's `sqverify-fast`, built from its reviewed source (`d97758bb…`), decided the retained certificate at all 600 directions on 3 November: VERIFIED, 296,805,699 nodes, least certified bound 1.0000000000314393 at direction 277, 8,139 CPU-seconds at two threads. Every direction's row equals both of the lab's receipts, timings aside. The lab ran the same checker, so this is reproduced with the producer's code; it is not a second implementation. The exact-integer second checker is retained and was not run here.
- **Controls.** Every mass scaled by 99/100 was refused at all 600 directions, each a coverage refusal at a centre in the domain where the mutant's exact capture is below 1. A mutant scaled to one part in a million below 1 at the least-bound leaf's centre was refused too. The first control receipt, of 3 November, failed closed on one bookkeeping rule of ours: at the axis, the vertex sweep's certified bound sits 1.12e-9 below the exact capture, more than the constant 1e-9 our census then allowed. We replaced that constant with the sweep's own enclosure (#892): the census now recomputes the interval the sweep held at that vertex, [0.9930860126842824, 0.9930860149308234], ties its lower end to the sweep's bound to the bit, and requires the capture to lie inside it. Written again under that rule on 4 November, the control passed.
- **A mathematical review.** A separately prompted review lane of this project, a Claude agent at the strong tier, [accepted the certificate](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-11-03-ozden-s94-dilated-measure.md) with no defect. It recomputed every premise exactly, decided direction 0 in full with code of its own, and held every other direction's least-bound box exactly. It also reproduced the lowest capture the Codex agent's review found, 1.0011230 at direction 144. It is an AI review, not a human one.

**What is recorded.**

- [T-262](https://squaremath.org/result/t-262.html), `s(94) ≥ 1993/200`, at **V3/C3**: confirmed, reproduced with the producer's code.
- n = 94's [verified and reported lower bounds](https://github.com/jlevy/squares/blob/main/packing/frontier/n-094.md) are now 1993/200, above Hosono's 199/20 (T-091), which keeps its claim and is superseded at n = 94. The gap to the 10 × 10 grid narrows from 0.05 to 0.035.

n = 95 and 96 are already proved equal to 10 (T-191), so the bound adds nothing there.

**Credit.** The record credits the certificate to Doğa Özden, after Hosono, Tokoharu and this project, as the repository's README does. It states the AI assistance as the issue does: Claude (Anthropic) agents in Doğa Özden's lab found the dilation, built the certificate, ran the checks and drafted the write-up, and an OpenAI Codex agent wrote the second checker and reviewed the argument (`GRADE.md`), under his direction.

**Notes from the review**, for the repository if you want them; none affects the bound:

- `notes/n31-negative/d529.jsonl` is a run on an input the repository does not keep: the retained `n31_L5978.json.gz` with every mass times 10000003/10000000. At the receipt's witness the retained file itself captures 0.99999969508, and the README's 0.99999999719 is in no retained receipt.
- The second checker checks the quadrant [L/2, U_r]², which covers each direction's whole centre domain only through the quarter turn and the measure's symmetry; the READMEs call it the full centre domain.
- `tools/rescale.py`'s growth formula ρ(1 − 1/λ) holds at r = 0 and on an unchanged net; on the finer net the growth at the shared nodes runs from 6.55e-5 to 1.062e-3.

**Two questions**, which hold nothing open; an answer is welcome here at any time:

1. The repository states no licence. Under which licence are the certificate, the receipts and the second checker's code published? They are kept on the presumption of permission that an author's own submission carries.
2. Did the lab try a side between 9.965 and the route's ceiling 99500/9977 ≈ 9.9729 on a finer net?
