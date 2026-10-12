---
type: is
id: is-01m4qn72v9ewp3fvtg9ac4djkb
title: "Import Evan Daniel: grade-C local minima at 233 configurations of field degree <= 4, 53 current-record counts beyond T-124 (#545)"
kind: task
status: open
priority: 3
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-12T08:56:06.761Z
updated_at: 2026-10-12T09:08:30.443Z
---
Found in lane W's read of evand/square-packing for the 2026-10-12 intake (think-mq0k); nothing on GitHub asked, so the record says: a watched-repository read, not an issue.

**Pin.** evand/square-packing ad86d42d0f743076d735036702ba04a41ce24a8c (2026-10-12T04:39:01Z). The claim is 0d0146e (2026-10-12T02:29:22Z), "gradec.py: exact grade-C local-min certificates for small field degree", and e493eea (02:38:47Z), "GRADEC_DROPZERO drops rows forced to zero force; n = 230, 261 VALID"; 7ea600b adds the batch runner. Retained: packing/resources/web/evand-exact-and-local-reports-2026-10-12/ (branch intake-watch-1012): gradec.py, gradec_explore.py, gradec_runs/ (_status.txt, _dropzero_status.txt, run.sh), the imported modules localmin.py, verify_exact.py, geom.py, the roster minpoly/results.json, the inputs at 230 and 261, tasks/exact-minpoly/grade-C.md.

**Claim (grade-C.md).** Theorem C (paper proof): a configuration with exact flat motions is a local minimum of the side (IsLocalMinPacking: no packing in a smaller square within a pose-space ball, squares matched by index, angles mod 90 degrees) if rows are valid with a margin, positive multipliers balance forces along the whole flat family, and the reduced Hessian is positive definite on a complement of the flat directions in null L. gradec.py checks these exactly in the number field (signs by intervals; force balance along the family by affine null vectors). Batch over the 250 roster configurations of field degree <= 4 (8 jobs, 30-minute cap): 231 VALID; 230 and 261 VALID with GRADEC_DROPZERO=1 (24 forced-zero rows dropped; dropping constraints only relaxes); 17 timeouts (174, 201, 204, 231, 234, 257, 262, 274, 275, 295, 296, 299, 308-312). Field degrees of the 233: 175 rational, 51 quadratic, 7 quartic. Mutation tests reported rejected. Not published: the certificates minpoly/solve/n-N.gradec.json, their n-N.contacts.json inputs, the logs.

**Map (stage 1 table).** A later release adding counts to a reported kind: a new entry. T-124 (restricted-optimality, V0/C0, Lean localMin proofs for 178 configurations) covers 169 of the 233; 64 are outside it. Measured against l4's case records: at 222 of the 233 counts the roster side equals the case's reported upper bound within 1e-9; at 11 (70, 84, 86, 127, 153, 175, 176, 232, 258, 261, 267) the roster (last changed 7 October, dbcb4c4) holds a superseded configuration, 7.1e-4 to 1.2e-2 above the case. So 53 counts gain a reported local-minimality claim for the case's current packing that T-124 lacks: 5, 10, 18, 19, 26, 27, 38, 40, 50, 52, 53, 54, 65, 66, 67, 82, 85, 89, 101, 104, 107, 109, 122, 124, 125, 145, 147, 148, 149, 150, 151, 170, 171, 173, 178, 197, 198, 200, 202, 203, 226, 227, 229, 230, 233, 260, 264, 265, 290, 291, 293, 294, 298 (5 and 10 are proved cases). The comparison is of sides; the configurations are not published. n = 261: the roster side is 684/41 = 16.682926829..., 4.15e-3 above T-150's 16.678779875343207747... (Robert Barnett, #505), so grade C says nothing about T-150's packing. n = 230: 643/41, the case ceiling. T-124 counts not grade-C VALID: 11, 28 (field degree > 4), 274, 275, 308-312 (timeouts).

**Draft register entry (records lane).** kind restricted-optimality; headline "Reported grade-C local minima for 233 source configurations of field degree at most 4"; claim "Evan Daniel reports that 233 source configurations of field degree at most 4 are local minima of the side under the source's matched-index convention (IsLocalMinPacking, angles modulo 90 degrees), by Theorem C of grade-C.md, a second-order sufficient condition that allows exact flat motions, checked exactly in each configuration's number field by gradec.py; at 230 and 261 after dropping rows that carry zero force. At eleven counts the configuration has since been superseded on its case. The certificates are not published. No global bound or rigidity is claimed."; scope n_values the 233; V0, C0; significance 2 (as T-124); novelty previously-published; attribution source key [Daniel exact and local reports 2026-10-12] (to be defined), published 2026-10-12; evidence E-evand-gradec-local-minima-233-report; artifacts the packet README, source/search/exact/gradec.py, source/tasks/exact-minpoly/grade-C.md, source/search/exact/gradec_runs/_status.txt; notes: name the 11 superseded counts and the 169 shared with T-124 (a second, Python route beside T-124's Lean one); next_rung "Obtain the certificates and contact inputs, review Theorem C, and re-run or re-implement the checks"; unfinished_confirmations: that, rung C3, this bead, estimated_cost below.

**Priced validation.** Nothing decidable from what is published. (1) Ask the author to publish minpoly/solve/n-N.contacts.json and n-N.gradec.json for the 233 (small JSON files) and the per-count run times. (2) W2 review of Theorem C's paper proof (the side-end relaxation h_r >= -K' delta^2, the projection onto the flat family, the null-vector lemma); one review lane, a few agent-hours; Lean is out of reach per the source. (3) Re-running gradec.py from the retained copy (python-flint, mpmath, numpy, scipy): the source's batch was 250 jobs at a 30-minute cap on 8 cores; 230 and 261 took about a minute each; worst case about 117 CPU-hours (233 x 30 min), likely far less, unmeasured since logs are not published; same-implementation. Needs an owner budget once timings are known. (4) An independent checker of the certificate JSON is a W7 slice. Nothing here was run.

**Credit.** Evan Daniel, MIT; CREDITS.md: produced by Claude (Anthropic) under human direction; both commits co-authored by Claude Opus 5.5. Each configuration keeps its case's finder credit.

**Draft acknowledgement** (no issue; for the owner if one is opened): "Thank you for the grade-C local-minimality checks (evand/square-packing 0d0146e and e493eea). We retained gradec.py, grade-C.md and the batch status at ad86d42. The certificates and contact inputs are gitignored; could you publish minpoly/solve/n-N.contacts.json and n-N.gradec.json for the 233 VALID runs, with their run times? We will review Theorem C and re-run the checks."

## Notes

GitHub issue: https://github.com/jlevy/squares/issues/545 (opened 2026-10-12 by the coordinator to track this watched-repository read).
