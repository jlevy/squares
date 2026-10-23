---
type: is
id: is-01m4pan44x8vekhh54vsb2vhan
title: Review the verification and confirmation rungs of the recent register entries (T-120 to T-146) against their retained evidence
kind: task
status: open
priority: 1
version: 5
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T20:32:18.076Z
updated_at: 2026-10-23T06:15:47.005Z
started_at: 2026-10-11T20:32:21.487Z
---
Owner request 2026-10-11: review the verification levels on recent items. For each of T-120..T-146: does the derived V/C rung match the evidence actually retained (certificate, replay command, passing replay, control path, confirming origin, relationship_to_generator, reviews), is anything over- or under-rated, which next_rung is quick (minutes) and which needs a long run or a human record, and is the adoption state (case record vs register) stated consistently. Findings go to a mapped review; corrections to the records lane.

## Notes

2026-10-11, lane R1 (sub-agent, Claude Opus 5.5 at xhigh), commit ce6e7a8e8 on worktree-agent-a3d3681a4b18ca3ed (from main 3a5a91a90). Not pushed.

Review: docs/project/reviews/review-2026-10-11-recent-register-rungs.md, mapped in docs/project/document-map.yaml (SYNOPSIS.md not re-rendered). It reviews ratings, not mathematics: no entry should list it in `reviews`.

Verdict: all 27 entries T-120..T-146 declared = derived (ten V0/C0: T-120..T-124, T-129, T-132, T-142..T-144; seventeen V3/C3). No over- or under-rating. Every V3/C3 predicate checked in retained files: 48 evidence certificates resolve (41 repo-relative, 7 n40 ones packing-relative); acquire_source --check PACKET_MATCHES_ITS_CONTRACT on all 17 declared packets; ryxu/ryxu_radical_n51/gupta/couzo_refinement/couzo_followup admissions pass; 6 other importer packets check + check-claims pass (91 certs, 273 jobs); relations agree with deciding programs; controls exist; 11 reviews mapped and accepting.

Spot replays (one process, load 4-15): T-137 3/3 equal 12.8 s; T-139 3/3 44.1 s; T-131 6/6 96.5 s; T-141 15/15 1,319 s (309 s alone on 10-10); check-claims rebuilt equal for all four; third route decide 15 certs/90 controls 69.0 s and decide-imports '#483' trio126 '#489' regularized 21 certs/126 controls 574.3 s, no problem; #483 --upstream against certificate.json fetched at 24221d5 (sha256 eeebf55c... = pin) 7.3 s; T-133 and T-145 audits check + check-replay byte-identical to retained receipts. T-146 kernel replay not run (load).

Findings, none blocking a current rung: RR-1 (blocks any V4/C4) next_rung of T-128, T-130, T-131, T-133..T-141, T-145, T-146 asserts the two AI reviews are by distinct reviewers; the final upper review leaves that to the owner; checker counts reviewer strings. RR-2 check_results treats `certificate` as a non-empty string, not a resolved path (388 packing-relative register-wide). RR-3 sharp third-route controls unretained; later upper entries' controls name tests, not receipts. RR-4 T-127's replay (gupta certify) overwrites its receipt; no compare mode. RR-5 T-133 significance rationale stale (superseded by T-145); next_rung offers work that moves no bound. RR-6 T-132/T-142/T-143/T-144: tooling only on unmerged claude/wand125-confirmations-2026-10-11 (44eb6a017), owner questions open (check2 candidate retention; T-142 AXIS_ROUNDING), smoke receipts unretained; propose activity waiting/owner. RR-7 T-120..T-124 unfinished confirmations unlinked, unpriced; T-120 superseded at 102. RR-8 deferrals fail from 2026-11-10 (T-146's 2026-11-11), PR #403 open; E-fang-484, E-deleeuw-483, E-mishapolk-470 (and E-evand-465 unless n-155 cites it) are housed at no count and must be cited in case rosters at adoption. RR-9 T-125 notes and T-136 next_rung list later replacements in part.

Adoption: 39 counts pending (houses T-146 x15, T-128 x6, T-136 x6, T-140 x5, T-130 x3, T-141 x2, T-134 x1, T-139 x1); all next_rung house recommendations agree with exact smallest sides; 7 of 8 houses still need private-worker custody (T-128 has it).

Checks: packing-validate --records exit 1 only on "synopsis agrees with the artifacts" (stale SYNOPSIS document map, expected); check_results and check_certificate_citations pass.

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): the RR-1 owner decision is on https://github.com/jlevy/squares/issues/543; the review's proposed record and tool changes (RR-1..RR-7, RR-9) are https://github.com/jlevy/squares/issues/542 (bead think-npvi). Tracker https://github.com/jlevy/squares/issues/544.
