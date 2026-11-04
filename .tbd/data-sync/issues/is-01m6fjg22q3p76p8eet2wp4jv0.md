---
type: is
id: is-01m6fjg22q3p76p8eet2wp4jv0
title: "Stage 4 review: Özden's s(94) >= 1993/200 certificate (#890)"
kind: task
status: closed
priority: 1
version: 6
delegate: bold-ritchie-r222
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m6fj2mwfwwncghn4hv6qdhhg
hold: null
hold_until: null
created_at: 2026-11-03T02:06:03.350Z
updated_at: 2026-11-04T04:59:55.356Z
started_at: 2026-11-03T05:05:13.008Z
closed_at: 2026-11-04T04:59:55.356Z
close_reason: Stage-4 review of T-262 accepted, no defect (docs/project/reviews/review-2026-11-03-ozden-s94-dilated-measure.md); recorded in https://github.com/jlevy/squares/pull/891 (merged ca3a171bb).
resolution: null
duplicate_of: null
---
Stage 4 mathematical review of #890's certificate (Doğa Özden, s(94) >= 1993/200), by a separately prompted tbd-strong-max lane at maximum reasoning in its own worktree, as packing/campaign/result-import.md "Who reviews, and when" asks. It is what moves n-094's verified lower lane (frontier README: a complete replay here and a review of its mathematics; the 6 October declared-net soundness review's records-lane item 7: "A review under docs/project/reviews/ read this certificate and accepted it"; check_results verified_lane_review_problems).

## Validation
- Claim: s(94) >= 1993/200 by certificate/n94_L9965.json.gz (format M, proof_net step 83/120000, last 599; B = 19884161/19900000; Hosono's mixed_n94_L995 dilated by 1993/1990), kenaznia-doga/s94-lower-bound@9d76ad5, retained as packing/resources/web/ozden-s94-lower-bound-2026-11-03; checker sqverify-fast (census route).
- Run: read the certificate and the argument (net and shrink, lemma N0 on 600 directions, per-bin centre domain, D4 reduction, counting); recompute premises apart from the crate; decide sampled directions and poses exactly with code of its own; read the census row and control receipt against the candidate; say what the dilation does and does not carry (the 400 new directions, the centre domain grown by 3/3986 at r = 0); grade the author's second checker's independence claims only as data.
- Cost: tokens at strong-max; CPU minutes for sampled exact decisions.
- Budget status: runnable (no CPU-hour item).
- Possible subset under the cap: not needed.
- Depends on: the replay on branch claude/bold-ritchie-xo28us-l33 (think-2agl), which the reviewer may read after writing its own findings.
- Done when: a mapped review under docs/project/reviews/ with verdict, recorded as external_review / proof.audit_record and in the register entry's reviews; then the verified lower lane of n-094 moves to 1993/200 if accepted.
- Machine note: shares the machine with gates; exact sampling is light.

## Notes

2026-11-03 (bold-ritchie-l33): brief for the stage 4 reviewer, to be launched by the coordinator (not by the import lane).

- Tier: tbd-strong-max at maximum reasoning, in a worktree of its own, prompted separately from lane L33; reads the source as data and runs only code it writes (result-import.md, "Who reviews, and when").
- Inputs: branch claude/bold-ritchie-xo28us-l33 (draft PR for #890). Packet packing/resources/web/ozden-s94-lower-bound-2026-11-03/ (certificate source/certificate/n94_L9965.json.gz; README; receipts/dilation-audit.json). Base measure: packing/resources/web/wand125-mixed-bounds-evening-2026-10-04/square-packing-bounds/certificates/mixed_n94_L995/candidate.json.gz. Census capture and control: packing/benchmarks/measure-verifier/census-mixed/ozden-s94-lower-bound-2026-11-03/ (mixed_n94_L9965.jsonl.gz, .control.json), census.json row mixed_n94_L9965, comparison receipt receipts/replay-comparison.json. Crate theory: packing/sqverify_fast/SOUNDNESS.md (The Claim; lemma N0; lemma D per-bin domain; C1; N4).
- Do not read before writing findings: source/second-checker/GRADE.md and GRADE.json (the author's referee report is an earlier review of the same result), nor any later review of this certificate; after the findings, add a section comparing with GRADE.md, and disclose anything seen first.
- Re-derive: s(94) >= 1993/200 from the certificate under the net-and-shrink measure-capture theorem on the declared net (600 half-angles of step 83/120000, B = 19884161/19900000): lemma N0 (a)-(e) exactly, the per-bin centre domain, the D4/quarter-turn reduction, the counting step with M = 9399999/100000 < 94. Say what the dilation of mixed_n94_L995 does and does not carry (the 400 new directions; the centre domain grown by 3/3986 at r = 0 in base coordinates; why Hosono's net does not admit the dilated core).
- Recompute premises apart from the crate and the lane's tool; decide sampled directions and poses exactly with code of its own (at least the least-bound direction, 277 in the author's receipts and the census; r = 144, where the author's grader reports its lowest sampled capture; direction 599; and new directions near the walls).
- Read the census row and control receipt against the candidate by the 6 October declared-net soundness review's "For the Records Lane" checklist, items 1-8 (docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md).
- Grade the source's independence statements (second checker from SOUNDNESS.md prose only) as data, not as evidence.
- Output: docs/project/reviews/review-2026-11-03-ozden-s94-dilation.md (or the day it lands), written to be shared with the author: summary first, findings graded blocking/major/minor/note with file and line, questions; no T-NNN not yet on main (T-262 is provisional until the PR merges); reviewer line names system family, tier and reasoning setting, not a model id. Confirm or change the draft significance S3.
- Code: kept in the packet's review/ directory with a README (what each program does, what it read, how to run it, what it printed); each deciding program registered in packing/frontier/verifiers.yaml with its independence record; an evidence entry with coverage for each thing a run decides or samples.
- After it returns (records lane): map the review in docs/project/document-map.yaml; enter E-ozden-890-n94-9965-sqverify-fast-replay (printed by `sqverify_fast_census --family mixed --evidence --only mixed_n94_L9965 --audit-record <review> --date 2026-11-03`), the external_review on E-ozden-890-n94-9965-report, the review under T-262's reviews; check_results then derives V3/C3; move n-094's verified lower lane to 1993/200 (adoption), T-091 then superseded at n = 94; follow up on #890.

2026-11-03 (bold-ritchie-r222, the stage 4 reviewer): done; verdict accepted, no defect of the certificate.

- Review: docs/project/reviews/review-2026-11-03-ozden-s94-dilated-measure.md, mapped (document-map row; SYNOPSIS.md's generated map regenerated with it). Programs and receipts: packing/resources/web/ozden-s94-lower-bound-2026-11-03/review/dilated-measure-2026-11-03/. Commits on claude/bold-ritchie-xo28us-l33: 5ad487b72 (findings, pushed before GRADE.md was read), 985d4bee1 (comparison with GRADE.md), e9417a952 (wording).
- F1 (gap, records lane): the control receipt fails closed only on the census tool's AXIS_ROUNDING = 1e-9 (r = 0 gap 1.123e-9; the original's own sweep shows 1.134e-9), so declared-net checklist item 6 is not met; all 600 refusals hold exactly here. The verified lane should wait for think-4uun.
- F2 to F6 notes: SOUNDNESS.md N2's "whole configuration" fold must be per square; the n = 31 receipt d529.jsonl is for an unretained input (masses x 10000003/10000000); "full centre domain" means the quadrant; rescale.py's growth formula assumes the same net; checklist item 8's words must read "reproduced with the producer's code" for this row.
- Significance S3 confirmed. Not done here (records lane): verifiers.yaml registration of dm_premises.py and dm_axis.py (deciders) and the sampling programs, evidence entries, external_review / reviews entries. The README in the review directory states each program's independence record.
