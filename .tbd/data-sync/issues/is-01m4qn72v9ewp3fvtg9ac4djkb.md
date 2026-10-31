---
type: is
id: is-01m4qn72v9ewp3fvtg9ac4djkb
title: "Import Evan Daniel: grade-C local minima at 233 configurations of field degree <= 4, 53 current-record counts beyond T-124 (#545)"
kind: task
status: in_progress
priority: 3
version: 11
delegate: bold-ritchie-l8
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T08:56:06.761Z
updated_at: 2026-10-31T13:07:23.450Z
started_at: 2026-10-12T14:33:44.161Z
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

**2026-10-12 update: the certificates are published** (issue comment https://github.com/jlevy/squares/issues/545#issuecomment-6126076974). Release exact-data-2026-10-12 of evand/square-packing at 31523f87316bdfda00f5459dd9077928e264f133. Asset gradec-233.tar.zst: 238,231 bytes, SHA-256 c71633f3850eb8b06c40ba04f824e9b6262b27b7996f62f69c6ad014a4ea9fa3, verified against the download, the release SHA256SUMS, GitHub's digest and the comment. 723 files, 15,787,809 bytes unpacked: 233 n-N.contacts.json, 233 n-N.gradec.json, 250 run logs, 3 GRADEC_DROPZERO logs (10, 230, 261), _status.txt, _dropzero_status.txt, README, SHA256SUMS; all 722 listed files match after unpacking in scratch.

**Retained** (branch intake-552, packet packing/resources/web/evand-exact-data-2026-10-12/): the archive itself as published (every member is one-line JSON or a short log, so 238 KB compressed against 15.8 MB raw; Python 3.14 tarfile r:zst reads it), plus its README and the two status files unpacked; the n = 10 exact form search/exact/minpoly/data/n-10.minpoly.json.gz as upstream gzip; gradec.py and its imports pinned identical to the ad86d42 packet.

**Recomputed n = 10.** The source's gradec.py (blob 93374b5a, read first; run from a scratch copy, CPython 3.13.16 with env.sh's pinned numpy 2.4.2, scipy 1.17.0, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0, no nix) on the committed n-10.minpoly.json and the archive's n-10.contacts.json: VALID, output byte-identical to the archive's n-10.gradec.json (SHA-256 ffc0c1ee...208f); 9.2 s wall, 2.5 s CPU. Receipt receipts/gradec-n10-recompute.json. Same-implementation: it shows the published certificate is what gradec.py computes from the published inputs, not that Theorem C or gradec.py is sound.

**Price of the rest.** The logs' build times for the VALID runs sum to 38,026 s = 10.6 CPU-h (author's machine, 8 jobs in parallel; may be slower here): 154 runs under 1 min (1,249 s total), 212 under 10 min (3.9 h), longest 1,741 s (n = 313). So the 232 other VALID counts by gradec.py cost about 10.6 CPU-h (owner budget); the sub-minute tranche, about 21 CPU-min, could run in a lane. The 17 timeouts will not finish under gradec.py as written: 10 (174, 201, 204, 231, 234, 257, 262, 295, 296, 299) stop in the reduced-Hessian step with dim W 12-16, while every finished run has dim W <= 11, and gradec.py sums each leading minor over all k! permutations; 7 (274, 275, 308-312) stop before the null vectors with dim F 210-274. A fraction-free determinant in K would remove the first wall (W7 slice, the source's or ours). Review of Theorem C: one W2 lane, a few agent-hours, unchanged. An independent checker of the certificate JSON: W7 slice.

**Draft reply (not posted).** "Thank you for publishing the grade-C data. The archive matches its digest and every file its SHA256SUMS lists; we keep the archive in the repository as published. Recomputing n = 10 from the committed exact form with gradec.py gave a byte-identical certificate here too. A full re-run is about 10.6 CPU-hours by your logs' times and waits for a budget; the review of Theorem C is queued. One observation: the ten runs that time out after the multipliers all have dim W of 12 or more, and every finished run has 11 or less, which matches the permutation sum for the Hessian minors."


**2026-10-23, stage 4 mathematical review (c-review-thmc-1023).** Review:
docs/project/reviews/review-2026-10-23-evand-grade-c-theorem-c.md, branch
claude/intake-2026-10-23-theorem-c-review (draft PR https://github.com/jlevy/squares/pull/751, head ea247d8e5 after merging main 7335d0098, #752). Theorem C is true under its hypotheses as gradec.py checks them. The paper proof has one gap (C-1, major): its last two steps do not control rows whose corner sits at a side end. The relaxation's slack, -K' delta^2 from the record, is of the order of the coercive term; measured from the family point it is first order where the flat family slides an aligned pair, which it does at 16 of the 24 side-end rows at n = 19 and at 206 of the 233 configurations. Repaired by the pair form (one row of a side-end pair is at least -C epsilon times the other) and a bootstrap, with no check changed. Minor: C-2 the record's packing property is outside gradec.py (verify_exact.py decides it); C-3 the t interval's bracket is not checked; C-4 the certificates are summaries; C-5 hypothesis 1 should name its row classes; C-6 hypothesis 2 should state that the multipliers tend to lambda* along the family, which the coercivity step uses and the source's lemma on affine null vectors supplies. Seven notes. A checker written here (review/check_theorem_c.py in evand-exact-data-2026-10-12, V-evand-gradec-review-check: Python fractions, the slip form of hypothesis 2, LDL^T for hypothesis 3, and the packing check) decided all 233 VALID in 24 CPU-minutes and agrees with every certificate on rows, ranks, dim F, dim W and moving squares (drafted below as E-evand-gradec-local-minima-233-review-check: full coverage, independently re-implemented after reading the producer's code, by a Claude agent, a system family the producer also used). The packet now retains the 233 exact forms. Records: E-evand-gradec-local-minima-233-report with external_review defect-found; V-evand-gradec-py and the three review programs; the key [Daniel exact and local reports 2026-10-12], defined in packing/resources/README.md, with its byline joined to evan-daniel in packing/contributors/occurrences.yaml. The evidence entries for the review's run and the 12 October n = 10 recomputation are drafted below and enter with the register entry. Significance S2 kept (as T-124); no S4/S5, no News. Not registered: no T-NNN allocated to this lane. On registration, C3 waits on a separate replay lane, gradec.py over all 233 (about 10.6 CPU-hours by the source's logs, think-mtah), which result-import.md Stage 4 accepts as the replay; the review's checker is that lane's own and no one else has reviewed its soundness, so its run is a second route beside the rung, as at T-225 and T-229 (review A1 of #751, settled by the coordinator).

**Draft reply on #545 (not posted; stage 7, on the owner's word).** "Thank you again for publishing the grade-C data. We have reviewed Theorem C and checked all 233 certificates again: https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-23-evand-grade-c-theorem-c.md. In short, the theorem holds and gradec.py checks what it needs, but the proof in grade-C.md has a gap at rows whose corner sits at a side end. The last step drops the sum of lambda_r(m) h_r(z), which for those rows is only at least -K' delta^2, the same order as the coercive term; and the bound h_r >= -K'|Delta|^2 is measured from the record rather than from m, so where the flat family slides an aligned pair (16 of the 24 side-end rows at n = 19 slip) the slack the relaxation allows is first order in |Delta|. It closes with the pair form of your edge argument, that one row of a side-end pair is at least -C epsilon times the other, and a bootstrap that makes every row O(|Delta|^2); the review writes it out. Hypothesis 2 should also say that the multipliers tend to lambda* along the family: the coercivity step uses it, and your lemma on affine null vectors supplies it. A checker written here from the theorem, sharing no code with yours (Python fractions, no python-flint), decided all 233 VALID, including that each record is a packing, which gradec.py leaves to verify_exact.py, and it agrees with your certificates on rows, ranks, dim F, dim W and moving squares. It took 24 CPU-minutes for all 233: the quadratic identities for the affine null vectors reduce, row by row, to the lifts vanishing at the angle of each square that owns a slipping side, so each lift is one linear solve, and an LDL^T replaces the permutation sums. Both walls your 17 timeouts hit should be avoidable this way, though none of the 17 was run here and most are larger than anything that was (dim F up to 274 against at most 212 here, dim W up to 16 against 11); if you publish their contacts files we can run them. Five questions are at the end of the review; the first is whether you would adopt the repaired step in grade-C.md."


**Evidence entries drafted for the registration (not in the register).** devtools.check_certificate_citations counts a verified, replayed certificate as cited only by a case record's packing block, method-limit evidence or beyond-horizon evidence, and no case record has a block for local minimality, so these two can enter evidence.yaml with the grade-C register entry only under a deferral in packing/devtools/certificate-citation-deferrals.yaml naming that entry, which lapses 30 days after the evidence register's last_reviewed; a citation that outlasts it is think-8xy2 (review A4 of #751). The claim's register entry needs a T-NNN from the coordinator. Paste after E-evand-gradec-local-minima-233-report and cite both from the new entry's evidence. The first is the second route beside the rung, as E-evand-regularized-1020-review-exact-feasibility is at T-225, and does not give the entry its C3, which waits on think-mtah's gradec.py replay: cite it beside that replay's entry, or hold the declared confirmation below what it derives with a composition note saying why. The second is a reproduction with the producer's code at n = 10:

```yaml
  - id: E-evand-gradec-local-minima-233-review-check
    claim: derived-structure
    scope: {n_values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 35, 36, 38, 40, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 104, 107, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 124, 125, 127, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 147, 148, 149, 150, 151, 153, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 173, 175, 176, 178, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 200, 202, 203, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 229, 230, 232, 233, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 258, 260, 261, 264, 265, 267, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 293, 294, 298, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324]}
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    relationship_to_generator: independent-implementation
    origin: replayed-here
    novelty: previously-published
    source_key: '[Daniel exact and local reports 2026-10-12]'
    certificate: packing/resources/web/evand-exact-data-2026-10-12/review/README.md
    replay: >-
      From packing/, with P = resources/web/evand-exact-data-2026-10-12, run
      OPENBLAS_NUM_THREADS=1 .venv/bin/python3 -I $P/review/check_theorem_c.py --minpoly-dir
      $P/source/search/exact/minpoly/data --archive
      $P/acquisition/release/gradec-233.tar.zst --dropzero 230,261 --out OUT.jsonl $(cat
      $P/review/counts.txt). Every one of the 233 lines must say valid true and the program
      must exit 0; then .venv/bin/python3 -I $P/review/compare_certificates.py --archive
      $P/acquisition/release/gradec-233.tar.zst OUT.jsonl must print agree true and exit 0,
      as receipts/review-theorem-c-233.jsonl and receipts/review-compare-233.json record.
    replay_status: passed
    verifiers: [V-evand-gradec-review-check, V-evand-gradec-review-compare, V-evand-gradec-review-derivatives]
    independence:
      coverage:
        extent: full
        unit: >-
          the 233 configurations the release's grade-C archive certifies, each decided in full:
          the record's packing property, every kept row, the multipliers, null L0 and the flat
          family, the affine null vectors and the reduced Hessian
    limitations: >-
      Run here on 23 October 2026 by the stage 4 mathematical review of the #545 import
      (think-7scz), under Python 3.14.7, numpy 2.5.2 and scipy 1.17.1, in niced processes,
      two for most of the run and three at once near its end, with single-threaded BLAS, on the 233 exact forms retained in the packet
      (each bound to its Git blob at 31523f8) and the archive's contacts files read in
      memory: all 233 valid, in 1,463 CPU-seconds, at most 369 for one count (n = 294). It
      decides the hypotheses of Theorem C in the form the review proves (the pair form of
      the side-end relaxation) and the record's packing property; that the hypotheses imply
      local minimality is the review's paper proof, not a mechanized one. It uses the
      contacts files' choice of rows, which any choice of valid rows makes sound, and at each of
      230 and 261 drops the 24 rows a linear program finds forced to zero, the same 24 as
      the source. numpy and scipy only propose multipliers and a basis order, and a numerical
      SVD agrees with the exact rank of L0 at every count; the identities, signs, lifts and
      Hessian are exact. It agrees with every published certificate on rows, ranks, dim F,
      dim W, the moving squares and the load-bearing squares. Independently re-implemented
      after reading the producer's code, by a Claude agent, a system family the producer
      also used. Not covered: the 17 timeouts, field degrees above 4, T-124's Lean proofs,
      and whether each configuration is its case's current packing.
    source_reviewed: '2026-10-23'

  - id: E-evand-gradec-n10-recompute
    claim: derived-structure
    scope: {n_values: [10]}
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    relationship_to_generator: same-implementation
    origin: replayed-here
    novelty: previously-published
    source_key: '[Daniel exact and local reports 2026-10-12]'
    certificate: packing/resources/web/evand-exact-data-2026-10-12/receipts/gradec-n10-recompute.json
    replay: >-
      Copy gradec.py with localmin.py, verify_exact.py and geom.py from
      packing/resources/web/evand-exact-and-local-reports-2026-10-12/source/search/exact/ to
      a directory outside the repository, install numpy 2.4.2, scipy 1.17.0, mpmath 1.3.0,
      sympy 1.14.0 and python-flint 0.9.0 (env.sh's versions) into a fresh virtual
      environment, put the unzipped n-10.minpoly.json from this packet's
      source/search/exact/minpoly/data/ beside the archive's n-10.contacts.json, and run
      PYTHONPATH=. python3 gradec.py DIR/n-10 with OPENBLAS_NUM_THREADS=1 and
      GRADEC_DROPZERO and GRADEC_MUTATE unset. The output must be byte-identical to the
      archive's n-10.gradec.json, SHA-256
      ffc0c1ee41b0c2037ab241806215b0df9d2a0111893256fa2a2116e3df02208f, as
      receipts/gradec-n10-recompute.json records.
    replay_status: passed
    verifiers: [V-evand-gradec-py]
    independence:
      coverage:
        extent: full
        unit: the n = 10 certificate, recomputed with the source's checker from the committed exact form and the published contacts
    limitations: >-
      Run on 12 October 2026 by the records lane of the #545 import with the source's own
      checker (gradec.py at 93374b5a, read first, run from a copy outside the repository
      under CPython 3.13.16 with env.sh's pinned packages and without nix): VALID, output
      byte-identical to the published n-10.gradec.json, 9.2 s of wall time and 2.5 CPU
      seconds. It shows that the published certificate at n = 10 is what gradec.py computes
      from the published inputs, not that Theorem C or gradec.py is sound; it is a
      reproduction with the producer's code at one count of 233 and sets no rung.
    source_reviewed: '2026-10-12'
```

**2026-10-23, review A of #751 addressed (c-review-thmc-1023, parent think-qa9c).** https://github.com/jlevy/squares/pull/751#issuecomment-6368595518. A1: C3 waits on the gradec.py replay (think-mtah), the review's run is the second route beside the rung; the request entry, the review's For the Records Lane, the evidence and verifier notes, this bead and the PR's Limits say so. A2: the key [Daniel exact and local reports 2026-10-12] is builds-on-project, credited Daniel after Schadt, Ellsworth, Levy, with its occurrence spans; the 7 October key is think-588u. A3: coverage entry evand-exact-and-local-reports-2026-10-12. A4: the citation wording, and think-8xy2. A5: the 23 October fetch dated in the packet. A6: the process count, 24 rows at each, and the timeouts reworded. A7: independence blocks for the two premise programs.
