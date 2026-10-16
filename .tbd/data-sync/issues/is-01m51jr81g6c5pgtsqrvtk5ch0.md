---
type: is
id: is-01m51jr81g6c5pgtsqrvtk5ch0
title: "Review: Greff's mixed covers for s(76) = 9 (T-184, #594) and s(95) = 10 (T-191, #610), stage 4 review lane"
kind: task
status: in_progress
priority: 1
version: 13
delegate: user-eb-review-76-95
labels:
  - validation
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T05:25:27.727Z
updated_at: 2026-10-16T10:34:51.078Z
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

2026-10-16 06:59Z user-eb-review-76-95: review written (docs/project/reviews/review-2026-10-16-greff-k2m5-mixed-covers-76-95.md, mapped in document-map.yaml); programs, run scripts and outputs regenerated from the final program (k2m5_review.py 4fa7ed60) and staged under packing/resources/web/bengreff-s76-certificate-2026-10-14/review/ (s95 packet review/README.md points there). zm_mixed.py controls on the s(76) cell j054: the 199/200 mutant ran 15 min at depth 24 with no verdict; at depth 12 the published cell certifies (121 boxes, record j054's census) and the mutant is refused (44 uncertified, one holding the hole's pose). A local mutant (one 1/16 segment orbit removed) is running at depth 24 under a 10-min limit. Verdicts so far: T-184 and T-191 no mathematical defect, nothing blocking. Next: commit, push, validate, draft PR.

2026-10-16 07:32Z user-eb-review-76-95: branch claude/intake-2026-10-16-review-76-95 at 7ae526246 pushed: review + programs (afdc297d8), synopsis row (4510ca9df), section 12 compute wording (baf6454a6), site cut v0.7.15 as last commit (7ae526246; v0.7.15 is also cut on four other branches, so a re-cut at merge is likely). packing-validate --records exit 0 (52/110 named-tier steps); check_release_impact --baseline-ref origin/main: every publication candidate dispositioned. Next: draft PR (S2), final note.

2026-10-16 07:42Z user-eb-review-76-95: review pushed and in a draft PR. Branch claude/intake-2026-10-16-review-76-95, head 7ae526246; PR https://github.com/jlevy/squares/pull/652 (#652, draft; labels S2, intake).

Deliverable: docs/project/reviews/review-2026-10-16-greff-k2m5-mixed-covers-76-95.md (mapped in docs/project/document-map.yaml, with its generated SYNOPSIS.md row), with the reviewer's programs and outputs in packing/resources/web/bengreff-s76-certificate-2026-10-14/review/ (README there; the s95 packet's review/README.md points to it).

Per-entry verdict:
- T-184, s(76) = 9: no mathematical defect found; no blocking finding.
- T-191, s(95) = 10: no mathematical defect found; no blocking finding.

Findings (none blocking): F1 minor, in the source: tools/check_coverage.py accepts 5 of 8 malformed record sets (a cell shifted by 1/40, other settings, another zm_mixed.py digest, a headerless record, a zmx2 log of another cover); the published and replayed records pass this review's stricter check. Notes F2 to F8: verify.sh sound only as a whole; each cover's line 2 calls it a candidate; S95Lower.lean line 11 names S76Cover; two checkers, one per cell (the trust base is the union; the confirmation is reproduced with the producer's code); zmx2's float-min is not evidence (seen on two scaled mutants); CovM read at f58a017, not the wrappers' 1718a58; zm_mixed.py refusal of a mutant shown at depth 12 only (199/200 mutant, cell j054), more owed for the replay lane's control.

For the records lane (think-ccjt, PR #649): this review may be recorded as external_review (informally-verified) on E-bengreff-594-cover-report and E-bengreff-610-cover-report and in each entry's reviews (adversarial, ai, accepted): C1. V3/C3 follow once the retained reproduction is recorded as evidence through the registered tools; nothing in the review stands in the way. Rung 4 needs a second distinct adversarial review and a human oversight record. Significance S3 confirmed for both.

Site edition: v0.7.15 cut as the last commit, since the synopsis row is a site output and the cut tool admits only the patch successor of main's v0.7.14. #646 and three other branches of this pass also cut v0.7.15, so it may need re-cutting at merge. Validation: packing-validate --records exit 0 (52 of 110 steps, the named tier); check_release_impact --baseline-ref origin/main: every candidate dispositioned; --fast left to hosted CI. Compute: about an hour of wall time for the programs and controls, one process at a time under nice -n 10 (CPU time less), plus two records-tier runs of about 3 min each, which ran with their default 4 jobs. This bead stays open (the coordinator's).

2026-10-16 07:48Z user-eb-review-76-95: hosted CI at 7ae526246 (PR #652) green: Packing validation run 38868173215 passed (07:35Z to 07:47Z), Certificate page run 38868173165 passed, Branch mergeability passed; 31 checks succeeded, 52 deferred/deep-gate skipped, none failed. PR body updated with it. Correction: the note stamped 07:42Z above was appended at 07:36Z. Bead stays open: lane E's #649 names think-l8wi (blocked_on in packing/devtools/certificate-citation-deferrals.yaml, and the next_rung links of T-184 and T-191), so it closes with the records PR that records this review and drops those references. Lane F done.

2026-10-16T10:04Z user-eb-addr-652: addressing review A on #652. Pushed 0b341ce71 (review text: A2 sec 12, A3, A4, A6, A7, A9, A10) and 0bd64c107 (A11 packet README pointers); records tier exit 0 at 0bd64c107. Next: run scripts made to run from the repository (A5, rerun of run_all_final.sh in progress), PR body (A1, A8), disposition reply.

2026-10-16T10:16Z user-eb-addr-652: pushed d930504c7 (A5 run scripts run from the repository via programs/common.sh; README A2/A5); run_all_final.sh re-run from the repo: all exit 0, outputs equal to kept apart from timings and absolute paths; records tier exit 0 at d930504c7. PR #652 body updated (A1 collision and merge order, A8). Next: hosted CI at d930504c7, then the disposition reply.

2026-10-16T10:32Z user-eb-addr-652: review A on #652 addressed, 11 of 11 fixed, none deferred or declined. Head a4d48feb7 (commits 0b341ce71, 0bd64c107, d930504c7, a4d48feb7, plain on top of 7ae52624). Hosted CI green at a4d48feb7 (Packing validation 38886161628, Certificate page 38886161378, Branch mergeability 38886154739). Disposition reply: https://github.com/jlevy/squares/pull/652#pullrequestreview-5546493950. PR body updated (A1 collision and merge order, A8). Lane E can merge a4d48feb7 into #649.

2026-10-16 ~10:35Z coordinator user-eb: PR #652 MERGE-READY at a4d48feb7 (senior Review A 0/0/1/7 + 3 suggestions, all fixed by user-eb-addr-652; reply https://github.com/jlevy/squares/pull/652#pullrequestreview-5546493950; CI green). Site v0.7.15: whichever of #644/#646/#648/#652 lands first keeps it, the rest re-cut (PR body section 'Site Edition Collision and Merge Order'). #649 carries this review; lane E merges a4d48feb7.
