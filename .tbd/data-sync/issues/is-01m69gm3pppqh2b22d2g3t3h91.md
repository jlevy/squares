---
type: is
id: is-01m69gm3pppqh2b22d2g3t3h91
title: "Result status: does a defect-found read stay open after a review that ends defects-resolved? (T-261 reads incomplete; owner question)"
kind: task
status: open
priority: 3
version: 4
labels: []
dependencies: []
created_at: 2026-10-31T17:37:52.341Z
updated_at: 2026-11-02T00:11:58.929Z
---
Owner question on the result-status vocabulary (plan-2026-10-01-result-status, provisional), raised by review A of #861 (A4, https://github.com/jlevy/squares/pull/861#pullrequestreview-5724017016).

**The case.** T-261 (#545's grade-C local minima, registered by #861; T-264 on the branch before review A) is at V3/C1. Its report entry E-evand-gradec-local-minima-233-report carries `external_review.state: defect-found` from the 23 October review (C-1, a gap in grade-C.md's paper proof at side-end rows, which that review repaired with gradec.py's checks unchanged), and its register entry lists that review with verdict `defects-resolved`. `devtools.result_status.open_issues` rule 1 fires on any defect-found read while the result stands below C2, and does not read the review's verdict, so the results page shows T-261 as *incomplete*, beside T-007 (whose read has no review). T-261 is the only incomplete entry whose latest review ends `defects-resolved`.

**Why the status is wrong one way or the other.** C-1 is a proof gap, not a computation: think-mtah's replay of gradec.py over all 233 would raise T-261 to C3 and flip it to *confirmed* mechanically, without touching C-1. T-261's own next_rung says the author's adoption of the repaired step in grade-C.md closes C-1 at the source.

**Options (the owner's choice; no rule is changed until answered):**
1. **The record's repair counts.** A defect-found read is dispositioned by a later review of the same result that ends `defects-resolved` (or `accepted`), as rule 1 already lets a passing replay do. T-261 would read *reviewed* now; T-007 is unaffected.
2. **Only the source's adoption counts.** A defect-found read stays open until the source adopts the repair (or a later read of the source finds it fixed), whatever the rung. Then think-mtah's replay must not clear T-261's *incomplete*: rule 1 stops being rung-gated for defects a review repaired rather than a replay passed over, and the defect needs a recorded close (for example `external_review.state` moving on to a resolved state with its date and source).

## Validation
- Claim: result_status's rule 1 gives the status the owner chooses for a defect-found read whose latest review ends defects-resolved.
- Run: the owner's answer; then `devtools/result_status.py` rule 1 and its tests (tests/test_result_status.py, tests/test_site_result_filters.py's incomplete list), and epistemics.md's Status section.
- Cost: under an hour of agent time after the answer; no compute.
- Budget status: gated on decision (owner).
- Depends on: the owner's answer.
- Done when: rule 1 and epistemics.md say which of the two holds, and T-261's status follows it.

## Notes

2026-10-31 bold-ritchie-l8, from review A of #864 (A2, no change made): the #545 reply of 31 October (https://github.com/jlevy/squares/issues/545#issuecomment-6547240858) says "The replay would clear the label by moving T-261 to C3, not by settling the gap", true under today's rule 1, and the next bullet says the label will follow this bead's answer. **If the owner picks option 2** (the replay must not clear T-261's *incomplete*), T-261's status stops moving with C3, and the #545 follow-up that change owes must say that the replay no longer clears the label.

2026-11-01 bold-ritchie-l19 (think-mtah, PR #875, branch claude/bold-ritchie-xo28us-l19; **revised 2026-11-02 after review A of #875**: the entry's provenance sentence (A1), and apply steps 1 and 6 (A3)): **gradec.py's replay of all 233 has run, and its evidence waits on this bead's answer.** Lane L14's first driver ran it on 1 November, 15:48Z to 22:39Z. All 233 certificates are VALID and byte-identical to the published n-N.gradec.json, the 2 GRADEC_DROPZERO runs (230 and 261) among them. Every log matches the release's, paths and times aside, and the 3 GRADEC_MUTATE controls at n = 10 were refused. 39,646 CPU-seconds (11.0 CPU-hours). The receipt is packing/resources/web/evand-exact-data-2026-10-12/receipts/gradec-replay-233.json, stored plain. The tool on main adopted the ledger once with --adopt-unstamped, on a copy, and the receipt carries adopted_basis. It does not touch C-1. T-261 is unchanged: V3/C1, *incomplete*, same evidence and artifacts. Its next_rung opens "Held for the owner's question (think-xyek)", and its composition says C3 waits on entering the replay. Both follow T-253 and T-260 on think-ikku.

**To apply once answered** (think-mtah's done-when; about an hour, from packing/):
1. **frontier/evidence.yaml.**
   - Insert the entry below before `  - id: E-evand-gradec-n10-recompute`.
   - In **E-evand-gradec-local-minima-233-report**'s limitations, replace "C3 waits on entering gradec.py's replay of all 233, run on 1 November with its receipt retained (receipts/gradec-replay-233.json there) and held for think-xyek (think-mtah)" with "gradec.py's own replay of all 233 reproduced every certificate byte for byte (E-evand-gradec-local-minima-233-replay, think-mtah)".
   - In frontier/verifiers.yaml, drop "No evidence entry cites it until..." from V-evand-gradec-replay's note.
2. **frontier/results.yaml, T-261.**
   - Add the evidence id, and set confirmation C1 to C3.
   - Add the receipt and packing/devtools/evand_gradec_replay.py to artifacts, and the receipt and packing/tests/test_evand_gradec_replay.py to controls.
   - In composition, replace "C3 waits on entering gradec.py's replay of all 233, run on 1 November and held for think-xyek (think-mtah)" with: C3 rests on that same-implementation replay, and the review's checker stays a second route beside it (T-225/T-229, review A1 of #751).
   - Rewrite the claim's sentence "the C3 replay is gradec.py's own over all 233 (think-mtah)".
   - In next_rung, drop the hold and keep C-1's adoption. Drop the unfinished confirmation.
3. **devtools/certificate-citation-deferrals.yaml.** Add a deferral for the new id (results [T-261], bead and blocked_on think-8xy2), as for the review check.
4. **campaign/result-requests.yaml.** In #545's grade-C summary, replace "C3 waits on entering gradec.py's replay of all 233, run on 1 November (11.0 CPU-hours, think-mtah) with its receipt retained ... and held for the owner's question think-xyek" with the replay's result, and drop think-mtah from its validation list.
5. **site-urls.** The evidence ids and artifacts are part of T-261's identity binding, so add an `amendments` entry to result/t-261.html's row (development.md, Adding or Moving a URL). `devtools.site_urls --check` must report 0 failures.
6. **The rule.** The done-when is that rule 1 and epistemics.md say which option holds, and T-261's status follows it. Today seven other results cite a defect-found read at C3 and read *confirmed*, their defects passed over by replays: T-004, T-005, T-006 and T-008 (E-bentz-2010-proof, no reviews), T-058 (E-wand125-tools-ceiling-report), T-059 (E-wand125-tools-n11-row-report), and T-060 (E-n011-global-optimality-report, latest review `accepted`). T-007 (E-nagamochi-lower, C1, no reviews) and T-261 read *incomplete*.
   - **Option 1, the record's repair counts.** This is a rule change too.
     - Change devtools/result_status.py's open_issues rule 1: a defect-found read is dispositioned by a later review of the same result whose verdict is `defects-resolved` or `accepted`, dated on or after the read, as a passing replay already does.
     - Add a case to tests/test_result_status.py, beside test_a_defect_a_read_found_makes_a_result_incomplete_until_a_replay_passes.
     - Change tests/test_site_result_filters.py's incomplete list, and its comment near line 273, to [t-007].
     - Rewrite epistemics.md's Status section (line 398).
     - T-261 then reads *reviewed* at C1 even before step 1, and *confirmed* after it. Check that T-007 stays incomplete and the seven stay confirmed; T-060's `accepted` review changes nothing there.
   - **Option 2, only the source's adoption counts.** Rule 1 must not simply drop its C2 gate, which would turn all seven incomplete. Key it on the recorded close instead.
     - Add a close state to external_review.state in frontier/frontier-evidence.schema.yaml (the enum at line 325, for example `defect-resolved-at-source`), with the close's date and source, and say what it means in the schema's description.
     - Make rule 1 hold a defect-found read open, whatever the rung, while the result's latest review ends `defects-resolved` (a review repaired the defect, rather than a replay passing over it) and the read has not moved to the close state. Otherwise keep the C2 gate.
     - Add cases to tests/test_result_status.py: a defects-resolved review at C3 stays incomplete; the close state clears it; a defect-found read at C3 with no such review stays confirmed.
     - The incomplete list in test_site_result_filters.py stays [t-007, t-261]. epistemics.md's Status section says so.
     - Check that T-007 and T-261 read incomplete and the seven confirmed. The #545 follow-up in think-6gti must then say that the replay no longer clears the label.
7. **Views and release.** Regenerate the views (render_results, render_evidence_inventory, render_verifiers, the synopsis headline). Re-measure the four papers that read results.yaml, evidence.yaml and result-requests.yaml, and add a no-public-change record if they are unchanged. Re-pin DATA_REVISION.

The entry was checked against frontier-evidence.schema.yaml, and its scope against the receipt's and T-261's 233 counts:

```yaml
  - id: E-evand-gradec-local-minima-233-replay
    claim: derived-structure
    scope: {n_values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 35, 36, 38, 40, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 104, 107, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 124, 125, 127, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 147, 148, 149, 150, 151, 153, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 173, 175, 176, 178, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 200, 202, 203, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 229, 230, 232, 233, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 258, 260, 261, 264, 265, 267, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 293, 294, 298, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324]}
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    relationship_to_generator: same-implementation
    origin: replayed-here
    novelty: previously-published
    source_key: '[Daniel exact and local reports 2026-10-12]'
    certificate: packing/resources/web/evand-exact-data-2026-10-12/receipts/gradec-replay-233.json
    replay: >-
      From packing/, with VENV a fresh virtual environment holding env.sh's pins (numpy
      2.4.2, scipy 1.17.0, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0) under CPython
      3.13, run python -m devtools.evand_gradec_replay --python VENV/bin/python --work
      SCRATCH --jobs 2 --out OUT.json. It copies gradec.py and its three modules from the
      evand-exact-and-local-reports-2026-10-12 packet to SCRATCH, runs gradec.py on each of
      the 233 counts of review/counts.txt from the exact form this packet retains and the
      archive's contacts file (230 and 261 with GRADEC_DROPZERO=1), and runs the source's
      three GRADEC_MUTATE tests at n = 10. Every certificate must equal the archive's
      n-N.gradec.json byte for byte and every control must be refused (summary.all_passed
      true), as receipts/gradec-replay-233.json records.
    replay_status: passed
    verifiers: [V-evand-gradec-py, V-evand-gradec-replay]
    independence:
      coverage:
        extent: full
        unit: >-
          the 233 configurations the release's grade-C archive certifies, each certificate
          recomputed by the source's gradec.py and compared with the published one byte for
          byte
    limitations: >-
      Run here on 1 November 2026, 15:48Z to 22:39Z, by lane L14 of the 1 November intake
      (think-mtah) with the source's own checker, gradec.py at ad86d42 (byte-identical at
      31523f8), read first and run unchanged from a copy outside the repository under
      CPython 3.13.18 with env.sh's pinned packages and single-threaded BLAS, two runs at a
      time on a four-core host shared with other lanes. All 233 certificates are
      byte-identical to the published ones, every one VALID, 230 and 261 with
      GRADEC_DROPZERO=1 as the release ran them, and every run's log equals the release's
      line for line, paths and times aside. The source's three rejection tests at n = 10 (a
      square moved by 1e-30, the right-wall rows dropped, the Hessian negated) were each
      refused. 39,646 CPU-seconds for the 233 runs (11.0 CPU-hours, 1.04 times the build
      times the release's logs print), the longest n = 313 at 1,839; under the 40 CPU-hour
      cap. The 236 runs were made by L14's first driver, launched at 15:48:30Z from its
      working tree before 76d72c594 committed devtools.evand_gradec_replay (16:07:48Z), so
      Git does not hold the exact bytes that ran: it held each run to the wall timer only
      (no RLIMIT_CPU), counted only recorded CPU against the cap, and stamped no environment
      on its records. The tool on main adopted the 236 records once with --adopt-unstamped
      (lane L19) and wrote the receipt, whose cap_rule, platform, machine and ran_from
      describe that invocation, not the runs; the adopted environment is asserted
      (environment.adopted_basis), with the evidence in review A of #875: no file of the
      virtual environment is newer than the runs' start, and the interpreter probes at the
      runs' end and at the adoption agree.

      It shows that each published certificate is what gradec.py computes from the published
      inputs: a reproduction with the producer's code in full, not a check that Theorem C or
      gradec.py is sound. It does not touch C-1, the gap in grade-C.md's paper proof at
      side-end rows that the 23 October review repaired; the record's packing property is
      verify_exact.py's, not gradec.py's; and the 17 timeouts and field degrees above 4 stay
      outside the claim. The review's independent checker
      (E-evand-gradec-local-minima-233-review-check) decided the same 233 and is a second
      route beside this one.
    source_reviewed: '2026-11-01'
```
