---
type: is
id: is-01m6na2ne3zs2jq13j0b5n3a7x
title: "Stage 4 review: Özden's s(94) >= 2493/250 certificate (#910)"
kind: task
status: open
priority: 1
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m6n86trbv1javs88wtdd2j24
created_at: 2026-11-05T07:34:22.402Z
updated_at: 2026-11-05T07:34:22.402Z
---
Stage 4 mathematical review of #910's certificate (Doğa Özden, s(94) >= 2493/250 = 9.972), by a separately prompted tbd-strong-max lane at maximum reasoning in its own worktree, as packing/campaign/result-import.md "Who reviews, and when" asks. With the complete replay (think-qcms) it is what moves n-094's verified lower lane (frontier README: a complete replay here and a review of its mathematics; the 6 October declared-net soundness review's records-lane item 7; check_results verified_lane_review_problems).

## Validation
- Claim: s(94) >= 2493/250 by certificate/n94-L9972.json.gz (format M; 853 rectangle orbits, mass 9399999/100000; B = 24872661/24875000; proof_net step 1/12000, last 4971, 4,972 half-angle directions, last tangent 1657/4000), Hosono's mixed_n94_L995 dilated by 4986/4975, kenaznia-doga/s94-lower-bound-9972@7d21f9bdf707102dd4ebf47e52f81b502a01004d, retained as packing/resources/web/ozden-s94-lower-bound-9972-2026-11-05; checker sqverify-fast (census route), whose census run is think-qcms.
- Run: read the certificate and the argument; recompute premises apart from the crate and the import lane's tool; decide sampled directions and poses exactly with code of its own; read the lab's receipt archive and two-direction control as data; say what the dilation does and does not carry.
- Cost: tokens at strong-max; CPU minutes for sampled exact decisions (well under 1 CPU-hour).
- Budget status: runnable (no CPU-hour item); gated on the coordinator launching a separately prompted lane.
- Possible subset under the cap: not needed.
- Depends on: the intake branch claude/bold-ritchie-xo28us-l49 (draft PR for #910), which the reviewer reads as its input. Not on think-qcms: the census may run after the review, and the review says what its row and control must show.
- Done when: a mapped review under docs/project/reviews/ with a verdict, recorded as external_review on E-ozden-910-n94-9972-report and under T-266's reviews; the draft significance S3 confirmed or changed.
- Machine note: shares the machine with gates; exact sampling is light; at most two cores at nice -n 19.

## Notes

2026-11-05 (bold-ritchie-l49): brief for the stage 4 reviewer, to be launched by the coordinator (not by the import lane, which may not review its own import).

- Tier: tbd-strong-max at maximum reasoning, in a worktree of its own, prompted separately from lane L49; it reads the source as data and runs only code it writes (result-import.md, "Who reviews, and when"). Python 3.14 only, via packing/'s uv environment.
- Inputs: branch claude/bold-ritchie-xo28us-l49. Packet packing/resources/web/ozden-s94-lower-bound-9972-2026-11-05/: the certificate source/certificate/n94-L9972.json.gz (and its text n94-L9972.json); the README; source/README.md; tools/rescale.py; receipts/native/{A..F}.jsonl.gz with their summaries, receipts/INDEX.json.gz, selection.csv and directions.jsonl.gz; controls/mass-99-100.json.gz, native-mutant.jsonl and control.json; verifier/ (the lab's copy of packing/sqverify_fast at e6e8d577). The import lane's receipts receipts/dilation-audit.json, receipts/native-receipt-audit.json and receipts/sample-diagnostic.json. Base measure: packing/resources/web/wand125-mixed-bounds-evening-2026-10-04/square-packing-bounds/certificates/mixed_n94_L995/candidate.json.gz. Crate theory: packing/sqverify_fast/SOUNDNESS.md (The Claim; lemma N0; lemma D, the per-bin domain; lemma C1, the quarter turn; N2's per-square fold; N4).
- Do not read before writing findings: the 3 November review of #890's certificate (docs/project/reviews/review-2026-11-03-ozden-s94-dilated-measure.md) and its programs under packing/resources/web/ozden-s94-lower-bound-2026-11-03/review/, which reviewed the same measure on the same route at 1993/200 and so count as an earlier review of a closely related result; the lab's own audit, tools/audit.py and checks/; and exploratory/SOUNDNESS.md. After the findings, add a section comparing with the #890 review, and disclose anything seen first.
- Re-derive: s(94) >= 2493/250 from the certificate under the net-and-shrink measure-capture theorem on the declared net: lemma N0 (a)-(e) exactly (the import lane found B(1 + D) = 99498934887/99500000000, t_max^2 + 2 t_max - 1 = 1649/16000000 and the tangent form 14327846598855339/14327999975125000 < 1; recompute them, do not copy them), the per-bin centre domain, the D4/quarter-turn reduction to the quadrant [L/2, U_r]^2 (the lab's README now says the quadrant stands for the whole domain through that symmetry; check that it is so for this measure), and the counting step with M = 9399999/100000 < 94. Say what the dilation of mixed_n94_L995 does and does not carry: 4,952 of the 4,972 directions are new; the centre domain grows at the 20 shared nodes by m_0(t) - m(t)/lambda, 1.93e-4 to 1.52e-3 in Hosono's coordinates by the import lane's tool, 11/9972 at the axis; Hosono's net does not admit the dilated core.
- Decide with code of its own, exactly: direction 0 (the axis) in full; the least-bound direction 3663 and its least-bound box; direction 4971; direction 1198; new directions near the walls; and several directions of each compacted stream B, C and D, whose rows keep only the proof fields. Hold the 99/100 control's two refusals and the lab's exact rational witness at 1198 (capture 0.991109005346039...) exactly.
- Read the receipt archive against the claim: is a union of six partial native runs, each selected line byte-identical to its run's, equivalent to one complete run (per-direction independence of the crate's decision; what in a summary depends on scope; what PARTIAL means); what the compaction of B, C and D removed and whether any removed field bears on soundness; whether stream E's declared sample and stream F's positive control are honest as described. The import lane's receipts audit (receipts/native-receipt-audit.json) is data for this, not a finding.
- Say what the census row and its whole-net control (think-qcms) must show, by the 6 October declared-net soundness review's "For the Records Lane" checklist, items 1-8 (docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md): the lab's control is two directions only, and the census's runs the 99/100 mutant at every direction.
- Grade the source's statements about independence and review (no human review, no formalization, no independent institution's replay; the exploratory C checker not interval arithmetic) as data, not evidence. Read the lab's answers to #890's notes F3 to F5 and say whether they are right.
- Output: docs/project/reviews/review-2026-11-05-ozden-s94-9972.md (or the day it lands), written to be shared with the author: summary first, findings graded blocking/major/minor/note with file and line, questions; no T-NNN not yet on main (T-266 is provisional until the intake PR merges); reviewer line names system family, tier and reasoning setting, not a model id. Confirm or change the draft significance S3 (T-262, T-091 and T-178 are S3 on the same route).
- Code: kept in the packet's review/ directory with a README (what each program does, what it read, how to run it, what it printed); each deciding program registered in packing/frontier/verifiers.yaml with its independence record; an evidence entry with coverage for each thing a run decides or samples.
- After it returns (records lane): map the review in docs/project/document-map.yaml; the external_review on E-ozden-910-n94-9972-report and the review under T-266's reviews; then think-qcms (runnable, about 19.4 CPU-h) and E-ozden-910-n94-9972-sqverify-fast-replay from `sqverify_fast_census --family mixed --evidence --only mixed_n94_L9972 --audit-record <review>`; check_results then derives the rungs; move n-094's verified lower lane to 2493/250, T-262 then superseded at n = 94; follow up on #910.
