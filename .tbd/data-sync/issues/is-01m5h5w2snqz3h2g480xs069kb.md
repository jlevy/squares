---
type: is
id: is-01m5h5w2snqz3h2g480xs069kb
title: "Stage 4 for #719's in-corpus entry at 105 and 204: replay, independent review, adoption and regularization"
kind: task
status: closed
priority: 2
version: 10
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
parent_id: is-01m5h3rxsgydmfjazs3vmw05wp
hold: null
hold_until: null
created_at: 2026-10-22T06:48:12.852Z
updated_at: 2026-10-23T00:47:27.648Z
started_at: 2026-10-22T06:48:15.575Z
closed_at: 2026-10-23T00:47:27.648Z
close_reason: "stage 4 merged in #725, replies posted"
resolution: null
duplicate_of: null
---
From the #719 triage (scratchpad triage-719/in-corpus.md): 105 is 5.18e-12 below T-174 (same arrangement re-solved); 204 is 1.006e-8 below T-225 (one to one, 6 squares moved > 0.1, one turned 25.6 deg). Replay ~1 CPU-min, one strong-max review, adoption and regularization 10-50 CPU-min; 105's grid-slack view and SETTLED[204] lapse; think-13e9 then superseded. After #719's records PR.
blocked_on: think-xyhn

## Notes

2026-10-22 c-lane-719-import: the entry is T-229 on branch claude/intake-2026-10-22 (records PR for #719; quote no id to the author until it is on main): s(105) <= 674331486483935962030285457609/62500000000000000000000000000 (5.18e-12 below T-174) and s(204) <= 882663895519250432/59604644775390625 (1.006e-8 below T-225), V0/C0, pending adoption at both, draft S2, regularizations of T-174 (105) and T-225 (204), identity measured (resources/web/mishapolk-issue719-2026-10-22/measure/identity.json). Its unfinished_confirmations names this bead at C3, priced 0.5 to 1 CPU-h. Inputs for stage 4: the facts facts/n-105.yaml.gz and n-204.yaml.gz (derived; no licence, so no upstream byte; derive --check from a checkout at 12fc466 rebuilds them), receipts/exact-certification.json.xz (both routes accept both, all 4 controls refused, 156,996 pairs, 22.55 CPU s; 105 clears walls by 5.00e-21 and pairs by 9.99e-21, 204 by 5.0e-13 and 9.98e-13), acquisition/claims.json (frozen at main 0281e7763). Not run here: the filtered six-control decision at 105 and 204 (beyond_horizon_replay decides only beyond the corpus); the triage measured it in scratch (4.2 CPU s, 6/6 refused on both). The judgment the review should look at: 204 is listed as a regularization of T-225 although one square is re-oriented by 25.64 deg (one to one; 67 beyond 1e-3, 6 beyond 0.1, at most 0.273; T-225 itself moves up to 0.442 from T-223). The release's second 204 file (certificates/n204.cert, 1.48e-11 lower, same packing) is pinned by digest only; if the author names it the entry states its side instead.

2026-10-22 13:25Z coord-intake-1021b: stage 4 mathematical review done by c-review-t229-math (tbd strong-max tier, Claude Opus 5.5; separate from the import lane and #722's reviewer). Both certificates accepted for finite feasibility. Clean-room stdlib checker (route Z integers / separating axes; route C Fraction clipped area), frozen and decided at 12:24:41Z before reading any maintained or source code (read the T-226-T-228 review document beforehand: disclosed as earlier-review). 105: 5,460 pairs, least wall 5e-21, least gap 1.0e-20; 204: 20,706 pairs, least wall 4.9998e-13, least gap 9.98e-13; equal field for field to both receipt routes. Sharp controls (contact accepted, -1e-30 refused) agree across all four deciders and run_sharp. Below every earlier report at each count (15 at 105, 13 at 204). Findings: RF-1 major (the issue names sqpack/verify.py as its second checker, so the replay entry is shared-components, as #678's); RF-2 minor (the issue's verify.py command decides nothing; the source README's verify_cert2.py unmentioned); RF-3 minor (square 38 at 204 is released, not just turned); RF-4 note (keeps #678's frame and tilts; of: T-225 vs T-223; credit #670 as first report); RF-5 minor (105 is S2 by T-190, not padding S1; S2 stands); RF-6 note (margins rounded up in README/notes: 4.99e-13, 1.536e-6/1.53e-6); RF-7 minor (gross controls only; no sharp test); RF-8 note (retain programs in the packet's review/review-2026-10-22/, register the checker in verifiers.yaml); RF-9 note (identity need not be re-measured for adoption). Proposed: V3/C3 at both (replay shared-components + clean-room independent-implementation), S2, adoption at both. Two author questions: how verify.py was invoked; how square 38 was released and from which file. Files: scratchpad/review-t229/ (review doc for docs/project/reviews/, README and programs/outputs for the packet; data/ NOT retained: holds a mutated copy of the certificate). Next: the stage 4 PR with think-0nse after #722 merges.

2026-10-22 c-lane-719-import (#722 review A, A3 and A6, data left for stage 4): three sentences in data files are stale, and the stage 4 PR that rewrites T-229 should take them (no re-pin was made for them in #722). (1) T-229's claim (packing/frontier/results.yaml, the "Credit ..." paragraph) says the issue gives Mikhail Polk: the author's 11:35:16Z edit of #719 changed only the two credit lines, to "Mishapolk (Mykhailo Polkovskyi)", the record's name, so say the issue credits Mykhailo Polkovskyi. (2) T-229's notes say the release's "second 105 file, 4.6e-12 above it ... pinned by digest only": certificates/n105.cert is not in upstream-subtree.sha256 and is pinned by the commit alone (4.64e-12 above n-105.cert, measured from the clone at 12fc466); n204.cert is the one pinned by digest. (3) The source register's mishapolk-issue719-2026-10-22 note (packing/frontier/source-coverage.yaml) says "the issue credits Mishapolk (Mikhail Polk)". The packet README, custody record, bibliography note and requests entry were fixed in #722 at 1eaa8624c.
2026-10-22 c-lane-stage4-1022: stage 4 applied in draft PR #725 (head 7a7ff3cc1, stacked on #722; merges on or after 2026-10-23T00:00Z). Review mapped as docs/project/reviews/review-2026-10-22-mishapolk-719.md; programs and outputs retained at packing/resources/web/mishapolk-issue719-2026-10-22/review/review-2026-10-22/ (data/ NOT retained). T-229 V3/C3, S2 confirmed; E-mishapolk-719-exact-feasibility (shared-components) and E-mishapolk-719-review-exact-feasibility (independent-implementation, clean room); verifiers V-mishapolk-719-review-check and -controls. RF-1..RF-9 applied, plus #722 review A3 (credit name) and A6 (n105.cert unpinned; 170 of 607 .cert files in scope). Adopted at 105 and 204 in the pass dated 2026-10-23 (LATER_PASSES['2026-10-23'] = {105, 204}; prior state house-adoption-prior-state-2026-10-23.json.xz), regularized: grid-slack 1-degree view drawn at 105, half-degree at 204; runs in packing/cases/regularized_drawings/think-4h23-2026-10-23/. At 204 Evan Daniel's regularizer solved T-229 to exactly n204.cert's header side (1.48e-11 below): the author's earlier publication, not registered or drawn (think-h01y). Reply draft: replies/stage4-1022/719-reply.md, not posted. Release held until #722 merges.

2026-10-22 20:45Z coord-intake-1021b: #725 (https://github.com/jlevy/squares/pull/725, retargeted to main after #722 merged): review A approve after A1-A4 (fixed, dispositions posted); main cacdafc1f merged (a666710ef), #722's stage 7 reply records added (3d43e15da). Release (DATA_REVISION re-pin + papers, NO site cut) held for #729 (think-yjkq); merges on or after 2026-10-23T00:00Z (adoption pass dated 23 Oct).

2026-10-23 00:25Z coord-intake-1021b: #725 merged as e929137a8 (head a623e7585, packing-required and pages-required green; review A dispositions plus coordinator delta check https://github.com/jlevy/squares/pull/725#issuecomment-6354340587). Stage 7 replies on #670/#672/#675/#719 follow the verified deploy.

2026-10-23 00:50Z coord-intake-1021b: deploy of e929137a8 verified (Certificate page run 39877818964; t-226..t-229 at V3/C3 live). Stage 7 replies posted: #670 6354654599, #672 6354654824, #675 6354655082, #719 6354655328 (v2 answering the 20:15Z comment); recorded in #739. Done.
