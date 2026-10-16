---
type: is
id: is-01m51jr81g6c5pgtsqrvtk5ch0
title: "Review: Greff's mixed covers for s(76) = 9 (T-184, #594) and s(95) = 10 (T-191, #610), stage 4 review lane"
kind: task
status: in_progress
priority: 1
version: 5
delegate: user-eb-review-76-95
labels:
  - validation
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T05:25:27.727Z
updated_at: 2026-10-16T06:14:14.304Z
started_at: 2026-10-16T05:25:32.352Z
---
Stage 4 review lane (W2) for T-184 (#594, Benjamin Greff, s(76) = 9) and T-191 (#610, s(95) = 10), the k = 9 and k = 10 cases of the k^2 - 5 series by mixed covers in Evan Daniel's format, registered at V0/C0. Their next_rung asks for "a review that reads the cover, the two checkers' composite over the D4 region and the wall segments". Model: docs/project/reviews/review-2026-10-02-wand125-s59-s77-mixed-covers.md (T-066's review). Deliverable: docs/project/reviews/review-2026-10-16-greff-k2m5-mixed-covers-76-95.md (or similar) on its own branch and draft PR; it moves no rung.

## Validation
- Claim: the lower halves s(76) >= 9 and s(95) >= 10 by the retained mixed covers (packets bengreff-s76-certificate-2026-10-14, bengreff-s95-certificate-2026-10-15), checked by zmx2 (D4 sweep) and zm_mixed.py.
- Run: read the covers and both checkers; reproduce samples or full sweeps as priced; mutated-input controls.
- Cost: estimate unknown until read; the reviewer prices before running anything above 1 CPU-h and stays under 4 CPU-h tonight.
- Budget status: runnable within the cap for samples.
- Depends on: nothing on main; the records slice think-ccjt runs in parallel.
- Done when: the review document is pushed with its PR, findings graded, verdict per entry.
- Machine note: one process, nice; the host is shared with two regularization lanes.

## Notes

2026-10-16 05:35Z user-eb-review-76-95: started. Read both briefs, AGENTS.md, result-import.md Stage 4, the two packet READMEs, T-184/T-191 entries, think-osvq/think-ribz (pins and claims). Worktree review-76-95 at e2e018f32 (branch claude/intake-2026-10-16-review-76-95). Next: read the source trees (verify.sh, tools, records, Lean) and the four pinned checkers; then write my own exact programs in scratch laneF/.

2026-10-16 05:56Z user-eb-review-76-95: read verify.sh, tools, records formats, Lean wrapper, and the checkers' relevant code (zmx2.rs parser/build_cover/check_d4/bounds/run_root/cmd_cert; zm_mixed.py main/keep/run_box/run_header; zeromargin d4_roots/clip_bin; mixed_cover load/validate) plus ZMX2.md. Wrote my own stdlib program (scratch laneF/prog/k2m5_review.py): cover audit (both covers: totals exact, D4 invariant under all 8 elements as a measure, FNV-1a = zmx2 log hash, no points on any line, 16/404 wall segments of one unit each) and composite audit (both packets: every root of the D4 grid present, census full-binary-tree, failing sets = failing_roots.txt, zm cells = exactly the aligned sub-cells, every cell decided, source = replay). My exact evaluator agrees to the last digit with zm_mixed.py pose at the triage control poses. Next: pose sampling, mutants, tiling controls of check_coverage.py, then the document. Branch head still e2e018f32 (nothing committed yet).

2026-10-16 06:17Z user-eb-review-76-95: spot checks done, all in scratch laneF/out (nothing committed yet): (1) exact mu at 9,326 (s76) and 17,319 (s95) sampled admissible poses (D4 region, every zmx2-failing root, every listed UNCERT box, tile and one-cut germs, coincidence angles u=1/3 and near sqrt26-5, 1,500 folded whole-container poses with mu equal before and after the fold): none below 1; lowest found by descent 1.000418 (s76, bottom-wall germ at (3.5,0.5)) and 1.003389 (s95). (2) six mutants (drop heaviest point orbit, drop heaviest segment orbit, scale 999/1000 resp. 249/250): exact mu < 1 at a pose, and zmx2 (6b7f0f79 built by devtools.replay_evand_zmx2 build, binary cba78a9e) refuses each at that pose's root while certifying the published cover there. (3) tiling controls: the author's check_coverage.py accepts 5 of 8 mutated record sets my check refuses (misaligned cell, other settings, other zm_mixed digest, headerless record, zmx2 log of another cover). No blocking defect so far. CPU so far about 7 CPU-min. Next: write the review document and the programs README; then commit, push, PR.
