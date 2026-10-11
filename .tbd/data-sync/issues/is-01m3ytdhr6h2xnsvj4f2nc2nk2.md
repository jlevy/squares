---
type: is
id: is-01m3ytdhr6h2xnsvj4f2nc2nk2
title: "Import squarepacker: s(12) >= 31360/7901, Daniel's s(12) certificate rescaled by 7902/7901 (#309)"
kind: task
status: closed
priority: 1
version: 6
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T17:26:00.710Z
updated_at: 2026-10-03T01:38:40.574Z
closed_at: 2026-10-03T01:38:40.574Z
close_reason: null
resolution: null
duplicate_of: null
---
Result import process, stages 1-4, lane AA. jlevy/squares#309 (squarepacker, Ryu Sungjoon, opened 2026-10-02) reports s(12) >= 31360/7901 = 3.96911783..., Evan Daniel's 1,736-point weighted certificate s12_lower_3.9686.txt (T-049, evand/square-packing at 7d6f46d) with every coordinate and the container multiplied by 7902/7901, weights unchanged (total 11.9738036 < 12), verified by Daniel's Rust verifier at N = 24000 (rejected at 6000 and 12000) and by the reporter's tools/indep_check.cpp. Source: github.com/squarepacker/s12-lower-bound; Zenodo 10.5281/zenodo.23106582; certificate sha256 6ad9b0e8...7578. Plan: retain the repository at a pinned commit (devtools.acquire_source), exact preflight against Daniel's retained certificate, the angle-net argument, replays (Daniel's verify at N = 24000, indep_check.cpp at 24000, the native parent-core checker if it decides this shape), two mutated controls per checker, review docs/project/reviews/review-2026-10-02-s12-rescaled-certificate.md, handoff of register and evidence entries to the records lane. Answer bead: think-5mkr.

## Notes

2026-10-02 lane AA, branch worktree-agent-a398285876beb6313 at b33e5b390 (local; push to claude/lane-aa-s12-309-wip was denied by the permission classifier). Stages 1-4 for #309 done: packet squarepacker-s12-lower-bound-2026-10-02 (pin 8c53049, Zenodo 10.5281/zenodo.23106582), preflight PASS 16/16, Daniel verify N=24000 VERIFIED (982 CPU-s), indep_check N=24000 VERIFIED, native parent-core PASS_COMPLETE 9,942 rows, controls refused by all three, review accepted (draft S2), packing-validate --edit clean. Credit squarepacker (Ryu Sungjoon) after Evan Daniel. Register/evidence entries handed to the records lane.

2026-10-02 handoff from lane AA (branch worktree-agent-a398285876beb6313 at b33e5b390, local only; to be merged into claude/zealous-gauss-jem7l9 by the records lane). Register entry and evidence entries follow verbatim.

Lane AA handoff for the records lane: jlevy/squares#309 (squarepacker), stages 1-4.
Branch: worktree-agent-a398285876beb6313 (local, not pushed). Bead think-gh2o; answer bead think-5mkr.

Done on the branch: packet packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/ (source at 8c53049, Zenodo record JSON, receipts), bibliography key [squarepacker s12 2026] (credit "squarepacker (Ryu Sungjoon) after Evan Daniel", lineage independent) and its row in packing/resources/README.md, devtools.audit_s12_rescaled_certificate (exact preflight + controls), verify_evand_angle_net_native case s12-rescaled at N = 24000, tests/test_s12_rescaled_certificate.py, review docs/project/reviews/review-2026-10-02-s12-rescaled-certificate.md mapped in docs/project/document-map.yaml, SYNOPSIS.md document-map block re-rendered.

Not done (records lane): results.yaml, evidence.yaml, source-coverage.yaml, n-012.md, generated views, campaign/result-requests.yaml (link #309 to think-gh2o).

builds_on: check_results refuses builds_on on any entry with attribution ("a result by others takes its credit from the bibliography, not builds_on"), so T-049 is carried by the bibliography credit's "after Evan Daniel" and by the claim naming T-049. novelty previously-published.

=== results.yaml (take the T-NNN last) ===
  - id: T-NNN
    kind: lower-bound
    registered: '2026-10-02'
    headline: "`s(12) ≥ 31360/7901 = 3.9691178…`, Daniel's certificate rescaled by `7902/7901`"
    claim: >-
      s(12) >= 31360/7901 = 3.96911783..., by squarepacker (Ryu Sungjoon) after Evan
      Daniel, published on 2 October 2026 and reported on jlevy/squares#309. It raises
      the verified bound by 15680/31216851, about 0.000502, over T-049.

      The certificate is Daniel's 1,736-point weighted certificate of T-049 with every
      coordinate and the container multiplied by 7902/7901 and the weights unchanged,
      total 11.9738036 < 12. The rescaling and its verification on the finer angle net
      are squarepacker's; the certificate and the verifier that decides it are Daniel's.
      Every closed unit square in [0, 31360/7901]^2, at every angle, captures weight at
      least one, decided over the rational angle net 2 arctan(k/24000) with a per-bin
      shrink of 1/(cos d + sin d). The nets N = 6000 and 12000 refuse it, which a pass at
      one net does not need: each net's test is a complete sufficient condition.

      It was replayed here on 2 October 2026 by Daniel's verifier and by squarepacker's
      own indep_check.cpp at N = 24000, least captured weight 10000056/10^7 at bin 0 in
      both, as the source records, and decided completely by this repository's native
      parent-core interval branch and bound over all 9,942 rows, which shares nothing
      with the two sweeps and gives the strict s(12) > 31360/7901.

      squarepacker (Ryu Sungjoon),
      [s12-lower-bound](https://github.com/squarepacker/s12-lower-bound/tree/8c53049025b94bb589ed25a90203f0a34c2945e4),
      archived as [Zenodo 10.5281/zenodo.23106582](https://doi.org/10.5281/zenodo.23106582),
      after Evan Daniel's certificate and verifier (T-049). The source's README says the
      rescaling, the verification runs and its checker were prepared with the help of an
      AI assistant from Anthropic, which it names.
    scope: {n_values: [12]}
    verification: V3
    confirmation: C3
    significance:
      score: 2
      rationale: >-
        True and replayed in full by three checkers, and it raises the verified lower
        bound at n = 12, but by 0.000502, moving the gap to the grid's 4 from 0.0314 to
        0.0309. It rescales T-049's certificate until a finer angle net stops accepting
        it, which spends that certificate's slack and adds no technique, as the source
        says itself; T-061 is the precedent for scoring such a step by what it changes.
      scored: '2026-10-02'
      by: think-gh2o stage 1-4 lane (repository; draft, kept by its review)
    novelty: previously-published
    attribution:
      source_keys: ['[squarepacker s12 2026]']
      published: '2026-10-02'
    composition: >-
      Primary at n = 12: one certificate, no monotonicity. Two entries whose methods
      differ decide it: the producer's two arrangement sweeps, Daniel's verify and
      squarepacker's indep_check.cpp (exact-algebraic, replayed here, one method in two
      implementations), and this repository's directed-rounding interval coverage of
      every row (interval-certified); that is C3, with the two methods shown beside the
      rung. All three rest on the certificate, the counting theorem and the shrink lemma
      on the net N = 24000, and the native rows are Daniel's bins and sigma_k by design.
    reviews:
      - path: docs/project/reviews/review-2026-10-02-s12-rescaled-certificate.md
        kind: adversarial
        reviewer: an AI agent of this project, lane AA of the 2 October import effort, which also ran the replays
        reviewer_kind: ai
        relation: project
        date: '2026-10-02'
        scope: >-
          squarepacker's s(12) >= 31360/7901: the exact identity with Daniel's certificate
          times 7902/7901, the reduction, the angle-net shrink lemma and admissible centre
          box, why refusals at N = 6000 and 12000 and a pass at 24000 are consistent, a
          line-by-line read of indep_check.cpp, the three checkers' trust boundaries, the
          replays and controls, significance.
        verdict: accepted
    evidence:
      - E-n012-squarepacker-31360-7901-report
      - E-n012-squarepacker-31360-7901-source-replay
      - E-n012-squarepacker-31360-7901-native-parent-core
    artifacts:
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/README.md
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound/s12_lower_3.969118.txt.gz
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound/README.md
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound/tools/indep_check.cpp
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/preflight.json
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/daniel-verify-N24000.log
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/indep-check-N24000.log
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/native-parent-core-N24000.json
      - packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12/certificates/s12_lower_3.9686.txt.gz
      - packing/devtools/audit_s12_rescaled_certificate.py
      - packing/devtools/verify_evand_angle_net_native.py
      - docs/project/reviews/review-2026-10-02-s12-rescaled-certificate.md
    controls:
      - packing/tests/test_s12_rescaled_certificate.py
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/controls/native-scaled-7901-7900.json
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/controls/native-weights-minus-57.json
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/controls/indep-check-N24000-scaled-7901-7900.log
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/controls/indep-check-N24000-weights-minus-57.log
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/controls/daniel-verify-N24000-scaled-7901-7900-bins-3880-3910.log
      - packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/receipts/controls/daniel-verify-N24000-weights-minus-57-bins-0-15.log
    next_rung: >-
      V4 and C4 need two adversarial AI reviews by distinct reviewers and a human
      oversight record; the one retained review was written by the lane that ran the
      replays, so a separately prompted read is the next step. Rung 5 needs a
      proof-assistant formalization reviewed by human experts; the source notes that
      Daniel's Lean pose-box-tree checker, which kernel-checks T-049's certificate, could
      in principle take this one. The exact value remains open; the conjecture is
      s(12) = 4.

=== evidence.yaml ===
(see the three entries in the bead notes / below)

=== evidence.yaml ===
  - id: E-n012-squarepacker-31360-7901-report
    claim: lower-bound
    scope: {n_values: [12]}
    assurance: reported
    reported_method: exact-algebraic
    performed_by: source-author
    relationship_to_generator: same-implementation
    origin: external
    novelty: previously-published
    source_key: '[squarepacker s12 2026]'
    certificate: resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound/s12_lower_3.969118.txt.gz
    replay_status: not-attempted
    limitations: >-
      squarepacker/s12-lower-bound at 8c53049025b94bb589ed25a90203f0a34c2945e4 (Zenodo
      10.5281/zenodo.23106582, v1.0 = 7acf812c, same certificate) claims s(12) >=
      31360/7901 = 3.96911783 from Evan Daniel's s12_lower_3.9686.txt (T-049) with every
      coordinate and the container multiplied by 7902/7901, weights unchanged, total
      11.9738036 < 12, first committed at be1871bd on 2026-10-02. The source reports
      Daniel's verify refusing it at N = 6000 (least 9849809/10^7) and 12000
      (9867834/10^7) and accepting it at 24000 (10000056/10^7), also with overflow checks,
      and its own indep_check.cpp, which sweeps [0, 90] degrees with no symmetry, agreeing
      on every net and accepting at 48000 and 96000. This entry preserves the source
      claim; the local replays are recorded separately.
    source_reviewed: '2026-10-02'

  - id: E-n012-squarepacker-31360-7901-source-replay
    claim: lower-bound
    scope: {n_values: [12]}
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    relationship_to_generator: same-implementation
    origin: replayed-here
    novelty: previously-published
    source_key: '[squarepacker s12 2026]'
    certificate: resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound/s12_lower_3.969118.txt.gz
    replay: >-
      With the certificate restored from the packet's .gz: build Daniel's verifier from
      packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12/verify
      with cargo build --release (CARGO_TARGET_DIR outside the packet) and run verify
      s12_lower_3.969118.txt 12 24000 2 0, which must print VERIFIED; build the packet's
      tools/indep_check.cpp with g++ -O2 and run indep_check s12_lower_3.969118.txt 24000,
      which must print VERIFIED. The packet README (Replays Here, Reproduce) gives the
      commands; the receipts are its receipts/daniel-verify-N24000.log and
      receipts/indep-check-N24000.log.
    replay_status: passed
    proof:
      source: packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound/README.md
      theorem: Twelve unit squares do not fit in a square of side below 31360/7901.
      scope: Unrestricted square packing with independent rotations, disjoint interiors and boundary contact allowed.
      pinpoints: >-
        The source README, "Why the certificate proves the bound" and "Verification";
        tools/indep_check.cpp; Daniel's s12/verify/src/main.rs (26 September evand packet);
        devtools.audit_s12_rescaled_certificate and its receipt receipts/preflight.json.
      assumptions:
        - The certificate is Daniel's T-049 certificate with every coordinate and the side times 7902/7901, weights unchanged, nonnegative, D4-invariant, total 119738036/10^7 < 12 (decided exactly by devtools.audit_s12_rescaled_certificate).
        - A unit square at any angle in [2 arctan(k/N), 2 arctan((k+1)/N)] contains the concentric square of side 1/(cos d + sin d) at the left angle, and its admissible centres lie in the box for the smaller bounding width at the two ends.
        - Each sweep computes the least captured weight over every admissible centre at each net angle of N = 24000; a pass at one net is a complete check, and refusals at coarser nets are not counterexamples.
      audit_record: docs/project/reviews/review-2026-10-02-s12-rescaled-certificate.md
    external_review:
      state: informally-verified
      date: '2026-10-02'
      reviewed_by: An AI agent of this project, lane AA of the 2 October import effort, which also ran the replays (docs/project/reviews/review-2026-10-02-s12-rescaled-certificate.md).
      note: >-
        Sound as stated; no blocking defect. The rescaling identity was decided exactly,
        the angle-net argument re-derived, indep_check.cpp read line by line, and the
        refusals at N = 6000 and 12000 shown consistent with the pass at 24000.
    limitations: >-
      Replays the producer's two checkers on the retained bytes on 2026-10-02 on a shared
      four-core Linux host. Daniel's verify, built by cargo 1.97.0 from the retained
      sources (main.rs blob 0e8035a3, the same at 7d6f46d9, which the source names), at
      N = 24000 on two threads: VERIFIED, least 10000056/10^7 at bin 0, 982 CPU-s, every printed line equal to the source's log (a first run was killed by a container restart and rerun whole).
      squarepacker's indep_check.cpp, built by g++ 13.3.0 -O2, at N = 24000: VERIFIED,
      least 10000056/10^7 at bin 0, 67.7 CPU-s, every printed line equal to the source's
      log; at N = 6000 and 12000 it refuses with the source's values, and verify refuses
      at the same values over bin windows. The overflow-checked build of verify and the
      N = 48000 and 96000 runs were not repeated. Both are arrangement sweeps of one
      angle-net method and both are the producer's code (Daniel's verifier, which the
      source used, and squarepacker's own checker), so this entry supports V3/C3 by
      itself; the method-distinct decision is
      E-n012-squarepacker-31360-7901-native-parent-core. Two mutated certificates (side
      31360/7900; every weight lowered by 57/10^7) are refused by both
      (receipts/controls/). Advance over T-049: 15680/31216851, about 0.000502; gap to
      the grid's 4: 244/7901, about 0.0309.
    source_reviewed: '2026-10-02'

  - id: E-n012-squarepacker-31360-7901-native-parent-core
    claim: lower-bound
    scope: {n_values: [12]}
    assurance: verified
    method: interval-certified
    performed_by: repository
    relationship_to_generator: independent-implementation
    origin: audited-here
    novelty: previously-published
    source_key: '[squarepacker s12 2026]'
    certificate: resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound/s12_lower_3.969118.txt.gz
    replay: >-
      uv run --frozen --all-extras --group dev python -m devtools.verify_evand_angle_net_native
      --case s12-rescaled --all --workers 2 --output OUT.json, from packing/, which must
      print PASS_COMPLETE.
    replay_status: passed
    proof:
      source: packing/src/sqpack/fractional/parent_core.py
      theorem: Twelve independently rotated unit squares cannot fit in a square of side 31360/7901; the native theorem gives the strict s(12) > 31360/7901, which implies the source's s(12) >= 31360/7901.
      scope: Unrestricted square packing with disjoint interiors and boundary contact allowed.
      pinpoints: >-
        devtools/verify_evand_angle_net_native.py, case s12-rescaled, which reads the
        source's integer certificate into ParentCoreCertificate rows [k/N, (k+1)/N, k/N,
        sigma_k] at N = 24000 with parent side 1 and minimum charge 1; validate_parent_core
        and parent_core_interval.py verify_parent_core_rows; the receipt and row journal
        receipts/native-parent-core-N24000.json and .rows.jsonl in the squarepacker packet.
      assumptions:
        - The 1,736 point charges are exact, nonnegative and D4 invariant, and total 29934509/2500000 < 12, a counting gap of 65491/2500000.
        - The 9,942 contiguous half-tangent rows [k/24000, (k+1)/24000] cover the folded parent orientations up to tan(pi/8), and each row's closed core of side sigma_k at half-tangent k/24000 lies strictly inside every unit parent of the row, which validate_parent_core proves in exact rational arithmetic (least containment numerator 11625067/4095488160000000000).
        - Directed-rounding boxes cover each row's entire parent-centre domain and count only sites surely inside the closed core; every row certifies at the exact threshold of one unit with no stalled or exhausted box.
        - Disjoint parent interiors make their closed cores disjoint, so twelve parents would capture at least 12 from a total below 12.
      audit_record: docs/project/reviews/review-2026-09-22-native-n11-parent-core.md
    limitations: >-
      The complete native run of 2026-10-02 accepted all 9,942 rows at the one-unit threshold with 89,403,350 boxes, zero stalls, no exhausted budget and no refutation: 1,810 rows on clean commit 119d1bab, the rest resumed from that journal on clean commit 44cf3444 with the tool unchanged after a container restart (2,856 CPU-s for the resumed part). The coverage decision is this repository's interval branch and bound
      over centre boxes, which shares no code with Daniel's verify or squarepacker's
      indep_check.cpp; with E-n012-squarepacker-31360-7901-source-replay it gives two
      complete methods, shown beside C3. All three rest on the certificate, the counting
      theorem and the shrink lemma on the same net: the native rows are Daniel's bins and
      sigma_k by design. The transfer theorem and engine were reviewed for Kleddamag's
      n = 11 certificate (the audit record above) and applied to T-049; the reader's
      s12-rescaled case changes only the net and the pinned file. Both mutated
      certificates are refuted at the rows where the sweeps refuse them, with admissible
      witnesses of charge below one (receipts/controls/native-*.json). The exact value
      remains open.
    source_reviewed: '2026-10-02'
