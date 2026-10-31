---
type: is
id: is-01m685tapg46244xgj0cmsd3x2
title: "Import Khalili and Gharabaghi: s(44) = 7 by a closed mixed cover (#842)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l3
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m686jr88t8k44ka04rczse21
hold: null
hold_until: null
created_at: 2026-10-31T05:09:47.344Z
updated_at: 2026-10-31T06:01:35.702Z
started_at: 2026-10-31T05:09:55.099Z
---
Stage 1 triage and stage 2 retention of jlevy/squares#842 (moh63-dev, Mohsen Khalili and Sara Gharabaghi, opened 2026-10-26T23:46:23Z; one comment, 2026-10-29T15:58:14Z, announcing release v1.1; labelled `intake` on 2026-10-31 by this lane under the github-workflows grant): "s(44) = 7: registration request". Intake pass 2026-10-31 (epic think-3guf), lane L3 (bold-ritchie-l3, tbd-strong sub-agent), branch claude/bold-ritchie-xo28us-s44. Followed the #594/#610 imports (think-osvq, think-ribz) and T-066's zmx2 route (s(59) = 8).

## Source pin

https://github.com/moh63-dev/s44-equals-7 at b5b1bc9d7354a8f62efcb6b7abeb30d1eb576aaf (tag v1.1, committed 2026-10-29T15:20:35Z, the head of main when cloned at 2026-10-31T04:58Z, the revision the issue's comment names). Two commits: 063c4d6 (tag v1.0, 2026-10-26T23:30:49Z, the commit the issue body names and the first holding the certificate) and b5b1bc9, which adds verification/zm_mixed_check.py (two-stage driver and log audit), edits README.md and verify.sh, adds .gitignore, removes .DS_Store, and leaves certificate/s44_cover_7.txt byte for byte. Pinned at the head by stage 1 rule 1; the claim does not depend on v1.0. Certificate SHA-256 c9fde0f1e7013f3f61f4a8d673b6bcaf9c5e54c914b6462164d7326ba254cae0, equal to the issue's and to certificate/SHA256SUMS. MIT (scripts, Mohsen Khalili and Sara Gharabaghi); the certificate CC0 by README. Paper also at https://doi.org/10.5281/zenodo.23769766.

Checkers: evand/square-packing at 659ee62e4a9d39542a1146e8b011cc3ab6407ede (2026-10-23T23:01:33-06:00), which verify.sh clones. zmx2.rs there is e2bb84e9e05938db416940ad608d2583ca9a0c248d59820937c4ce59d607ead7, byte-identical to the evand-square-packing-2026-10-04 packet's copy (V-evand-zmx2's third version, "not run here" until now); Cargo.toml 4e0f078e and Cargo.lock e1daec4d equal the retained ones. src/main.rs differs (afd53143) and builds the separate zmcheck binary, not zmx2. zm_mixed.py there is 1fd20346 (retained in the evand 2026-10-01 packet); zeromargin.py 3cb95fb7 and mixed_cover.py at 659ee62 are not retained.

## Claim map (result-import.md register table)

- s(44) = 7 (a new exact value; n-044.md is open at 2789/400 = 6.9725 <= s(44) <= 7, T-090 Hosono, both lower lanes; T-177's 2799/400 is reported and pending adoption): one new entry, kind optimality, scope n = 44. Lower half: the closed mixed cover certificate/s44_cover_7.txt, 15,525 weighted points and 3,912 uniformly weighted pieces of the grid lines x, y in {1..6} of [0,7]^2, D = 1000, W = 10^8, total 2199755099/50000000 = 43.99510198 < 44, D4-invariant. Upper half: the 7 x 7 grid (E-basic-grid-upper). It is k = 7 of the s(k^2 - 5) = k series (T-066 k = 8, T-184 k = 9, T-191 k = 10).
- Consequences: s(44) >= 7 gives s(45..48) >= 7 by monotonicity, which the record already holds (s(45) = 7 is Daniel's); nothing new. The total is above 43, so nothing at n <= 43.
- Supersedes as a bound: T-090's s(44) >= 2789/400 and T-177's reported 2799/400, once the case adopts 7 (derived).
- Checking the source reports: zmx2 cert --d4, VERIFIED-D4, all 4,900 roots, 0 uncertified, 191 s one thread; zmx2 cert --full, VERIFIED, all 39,200 roots, 134,880,184 boxes, 0 uncertified, max depth 39 (depth limit 40), 1,658 s wall / 1,643 CPU-s; zm_mixed.py cert --d4 --depth 24 --disj --chain-from 0 over 9,800 roots, 1,265 boxes uncertified in 27 roots, each re-swept at depth 30 to none (max depth 29), about 143 CPU-h, records in verification/logs/zm_mixed/; sanity.py (exact) and stress.py (float, min 1.0031) of the authors'.
- Not done by the source: Lean, independent review.
- Search code (cover_loop.py, tilesep.py): research code, not part of the proof; no claim to register. The valley separation is a search method, not a proof step.

Credit read from the source: Mohsen Khalili and Sara Gharabaghi, after Evan Daniel (closed mixed covers, the format, zmx2 and zm_mixed.py, line_cover, the s(45) = 7 starting cover), Burns and Massaccesi (LP-weighted exact covers), Hosono (public mixed-cover certificates), Göbel, Stromquist, Friedman, Nagamochi. AI assistance: "The search, the certificate, the new valley-separation tool and the verification runs were produced with Claude (Anthropic) under our direction; we reviewed the method, the checks and this write-up." Lineage: independent (the source names no debt to this project; it cites squaremath.org/cases/44 for the standing bound). Credited names: Mohsen Khalili and Sara Gharabaghi.

Novelty: no s(44) >= 7 elsewhere in the record: n-044.md open at 2789/400; T-177 reports 2799/400. Previously-published (the source), apparently first.

## Validation plan, priced (cap: the owner's 40 CPU-h per item, think-3guf; at most 2 cores)

Run in this lane:
1. Packet and data facts: acquire_source --check; devtools.audit_evand_mixed_covers with a Case 44 (exact total, counts, D4 invariance as a measure). Seconds.
2. zmx2 --d4 replay, e2bb84e9 built from retained bytes by devtools.replay_evand_zmx2 (case 44 registered), 2 threads: about 191 CPU-s by the source. Same-implementation.
3. zmx2 --full replay, the same binary, 2 threads: about 1,650 CPU-s (0.46 CPU-h) by the source's 1,643 CPU-s.
4. Two mutated-cover controls (drop-heaviest-point, drop-heaviest-segment) refused by zmx2, held by tests/test_replay_controls.py: seconds each. This is stage 4's control rule; zmx2 decides every root here, so no zm_mixed.py composite is needed for C3 (T-066's route, unlike T-184/T-191).
5. Root-for-root comparison of the replay's root logs with the source's zmx2_d4.log and zmx2_full.log (published here, unlike T-066's): seconds.
6. Stage 4 review (W2), a distinct pass in this lane on the coordinator's instruction: reduction cover -> claim, zmx2 e2bb84e9 against the reviewed 6b7f0f79 (the diff), the full sweep's depth 39 of 40, wall-adjacent valleys, exact spot poses. Agent hours.

Priced and not run (over the cap):
7. zm_mixed.py's complete two-stage pass (depth 24 over 9,800 roots, depth 30 over the 27): about 143 CPU-h by the source (verification/zm_mixed_check.py run). A second route by the producer's code; it reaches no rung (epistemics: a second machine method is an attribute), so it is not an unfinished confirmation. Validation bead and backlog row. Possible subset: a sample of roots (about 52 CPU-s a root on average by the source's total), or the source's audit mode over its records (seconds), a premise read.

Draft ratings (registering lane's draft, for the reviewer): enters at V3/C3 if the replay and controls pass and the review finds no blocking defect (T-066's path), confirmation reproduced with the producer's code (zmx2, Daniel's, which the authors ran). V4/C4 needs two adversarial AI reviews by distinct reviewers and a human oversight record; V5 a Lean proof of the covering statement. S3, a substantive case result, as T-066, T-184 and T-191: an exact value for an open case by Daniel's recipe at a new count, no new technique in the proof.

## Acknowledgement draft (post after the PR merges, stage 7)

See the answer section added when the PR is open.

## Notes

2026-10-31, lane L3 (bold-ritchie-l3). Draft PR https://github.com/jlevy/squares/pull/851 (labels intake, S3). Claimed with tbd start --as bold-ritchie-l3 (claimed). Branch claude/bold-ritchie-xo28us-s44, pushed: 65b1f2d (packet, tools, D4 replay), 1994011 (full replay, controls, review programs), a2ee6db (register, case, requests, coverage, verifiers, views). A container restart at about 05:27Z stopped the --full sweep after 29,812 of 39,200 roots; resumed from its root log by the same command and finished at 05:35:45Z.

## Stage results

- Stage 1: entry #842 in campaign/result-requests.yaml (triage done, read_through the 29 Oct comment); issue labelled `intake` (no n-44 label exists; listed for the owner).
- Stage 2: packet packing/resources/web/moh63-dev-s44-equals-7-2026-10-29 at b5b1bc9 (v1.1, head; certificate identical to v1.0 063c4d6), 212 files, acquire_source --check PACKET_MATCHES_ITS_CONTRACT; bibliography [Khalili Gharabaghi s44 cover 2026-10-29]; coverage entry; resources README rows.
- Stage 3: T-252 (optimality, n = 44), landed 2026-10-31; E-khalili-842-cover-report, E-khalili-842-cover-replay.
- Stage 4 replay (zmx2.rs e2bb84e9 from retained bytes, binary d68a2e35..., 2 threads): --d4 VERIFIED-D4, 4,900 roots, 16,792,446 boxes, 0 uncertified, max depth 39, 131 s wall / 222 CPU-s; --full VERIFIED, 39,200 roots, 134,880,184 boxes, 0 uncertified, max depth 39 (first run ~1,004 s wall to the restart, resume 311 s / 430 CPU-s; zmx2's own count 2,601 CPU-s). Both root logs equal the source's root for root (audit_evand_mixed_covers compare-zmx2, check_whole_case clean). Controls refused: drop-heaviest-point at d4 x23 y17 (435 uncertified), drop-heaviest-segment at d4 x8 y9 (235); held by tests/test_replay_controls.py.
- Stage 4 review: docs/project/reviews/review-2026-10-31-khalili-gharabaghi-s44-mixed-cover.md, accepted, F1-F6 notes, written as a distinct pass of this lane (disclosed: not separately prompted). Cross-checks: zmx2 6b7f0f79 (binary cba78a9e) over the D4 region, identical census at all 4,900 roots; 2,880 exact poses + 25 descents, none below 1 (least 1.003837205 at the wall tile (1/2, 3/2), tilt 1e-6 deg); the source's printed float minima reproduced exactly; mutants below 1 exactly (0.993201, 0.819939); the source's zm_mixed.py records complete (9,800 roots at depth 24, 27 closed at depth 30, 495,545 CPU-s).
- Rating: V3/C3, confirmed, reproduced with the producer's code; S3 (review confirmed the draft). n-044 proved (reported and verified lower 7).
- Held: zm_mixed.py complete pass, think-qvp6 (~138 CPU-h, over the cap; a subset, the 27 depth-30 roots at ~25.7 CPU-h, fits); backlog row in think-j9kg.

## Reply draft for #842 (post after the merge, from main with check_requests --draft 842, checked against main and the site)

@moh63-dev, thank you for the registration request, and for v1.1 with the zm_mixed.py driver and the log audit.

Your result is on main (PR #851): **T-252, s(44) = 7, at V3/C3 — confirmed, reproduced with the producer's code**, and [n = 44](https://squaremath.org/cases/44.html) now reads proved. The packet retains moh63-dev/s44-equals-7 at b5b1bc9 (v1.1), whose certificate is byte for byte v1.0's (c9fde0f1…cae0).

What ran here: Evan Daniel's zmx2, zmx2.rs e2bb84e9 (the file at evand/square-packing 659ee62) built from this repository's retained copy, over all 4,900 D4 roots and all 39,200 unreduced roots, none uncertified; every root's census equals your published logs. Two mutated covers, each without one D4 orbit (the heaviest point orbit, the heaviest segment orbit), are refused. This is a reproduction with your checker, not a second implementation.

The stage 4 review ([review-2026-10-31-khalili-gharabaghi-s44-mixed-cover.md](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-31-khalili-gharabaghi-s44-mixed-cover.md)) found no mathematical defect and no blocking finding. Its notes: zmx2 is interval-certified (binary64 geometry widened outward, exact integer mass tests), not exact-rational as the README, the issue and the paper's section 4 say; for your cover zmx2.rs e2bb84e9 runs the same decision path as the 6b7f0f79 version earlier reviews derived, and that version gives the same census at every D4 root; both sweeps reach depth 39 of 40. Exact capture at 2,905 sampled poses was never below 1.

Not run here: zm_mixed.py's complete pass, about 138 CPU-hours by your records, over this pass's compute cap. It is owned by think-qvp6; it would add a second machine method beside the rung and raises no rung. Your zm_mixed.py records were read with the review's own code: every root at depth 24, and each of the 27 open roots closed whole at depth 30.

Two questions, neither holding anything open: were the zm_mixed.py runs without --cert-mode deliberate (for this cover nothing certificate mode disables is reachable), and is zeromargin.py 3cb95fb7, which zm_mixed.py flags as differing from its pin, the file at 659ee62?

V4/C4 would need a second, separately prompted adversarial review and a human oversight record. With the import answered, this issue is closed; an answer to the questions is still welcome.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
