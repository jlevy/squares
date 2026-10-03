---
title: "exp-250 — two n17 kernel certificates admitted by the standing verifier"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-250
  series: series-000
  title: Flag 3 at arity 9 and the residue state N1 certified infeasible at cap 1169/250 by the kernel, and
    admitted on the standing verifier's full pass
  date: '2026-10-03'
  hypotheses:
  - H-267
  tier: confirmatory
  subject:
    label: Flag 3, named SW9 (corner-SW, side-S0, side-N0, side-W0, side-W1, side-W2, interior-SW,
      interior-NW, interior-S), and the whole 17-cell residue state N1, each closed by the ownership-induction
      kernel, on the unique-state 24-cell cover at U = 1169/250.
    engine: devtools.verify_n17_kernel_certificate in full mode (the standing kernel verifier, its file as at
      25c1cdef6), on certificates written by devtools.check_n17_subpattern
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker per run
    selftest_passed: true
    engine_commit: fd2c9602eb4e96e1dcdfd2ac8ac8a637a3ab2b44
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: The same checker reports a certified stall, not a closure, on flag 3 from the same seed with
      uniform rows and a 12-round cap (receipts/kernel-flag3-a9-bins64.json, f4642c051), and on N1 under a
      45-minute ceiling (handoff/k2/h-N1.json). The endpoint's state survives every admitted entry, which the
      census checks. The verifier's 47 tests, the review's five condition tests among them, pass at
      ae4f5fb43.
    candidate: SW9's adaptive-row seed and node (93954a4d, 19cb9681) and N1's (f5aef923, 27050bae), each
      re-proved in full by the standing kernel verifier.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 168; lane K2 produced both certificates and ran both full verifications, lane A3
      admitted them and wrote this record
    entry_point: packing/devtools/verify_n17_kernel_certificate.py
    command: 'From packing: .venv/bin/python3 -m devtools.verify_n17_kernel_certificate --output FILE
      campaign/explorations/X048-session-168-pilots/certificates/flag3-a9-pending (at fd2c9602e), the same on
      certificates/N1-state-pending (at ae4f5fb43), then .venv/bin/python3 -m devtools.census_n17_certified
      --output campaign/series/series-000-smoke-and-calibration/results/exp-250-n17-standing-verifier-admissions/census.json.
      The producer and checker receipts are retained runs; none was repeated.'
    budget: 7,000 seconds per verification on one worker; the producer runs are retained, not re-run.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-250-n17-standing-verifier-admissions
    dirty: true
    commit: ae4f5fb43671a5ba77e2e4187b77502e54ce6862
  results:
  - shape: determination
    role: outcome
    question: Is flag 3 (SW9) infeasible at U, by a certificate the kernel's checker accepts and the standing
      verifier re-proves in full?
    outcome: criterion_met
    checked_by: The adaptive-row run (receipts/kernel-split-flag3-a9-bins64.json, 155abe8a2) returns
      PASS_CERTIFIED_CLOSED on 102 steps and 7,279 rows, closure all_parent_poses_forbidden for side-N0 at
      step 101. The standing verifier at fd2c9602e passes it in full mode in 351 s, checking all 3,359 live rows in full,
      8,575 collision regions by 28,321,424 exact facet checks, the closure re-derived. Alone it
      excludes 43,772 states and 5,499 orbits.
  - shape: determination
    role: outcome
    question: Is the residue state N1 infeasible at U, by a certificate the kernel's checker accepts and the
      standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run under a two-hour ceiling (handoff/k2/h-N1-2h.json) returns PASS_CERTIFIED_CLOSED in
      3,723 s on 82 steps and 2,624 rows, closure all_parent_poses_forbidden for interior-W at step 81, and the
      checker alone in a fresh process returns PASS_SAVED_CLOSED (certificates/N1-state-pending/check-saved.json).
      The standing verifier at ae4f5fb43 passes it in full mode in 482 s, checking all 2,611 live rows in full,
      8,470 collision regions by 16,709,184 exact facet checks. It excludes N1's 4 states, one orbit.
  - shape: determination
    role: guard
    question: Do the certified exclusions leave at most 10^4 orbits, H-267's threshold?
    outcome: criterion_missed
    checked_by: With W7, A, SW9 and N1 admitted, census_n17_certified counts 126,168 states and 15,953 orbits,
      the endpoint surviving, down from exp-249's 139,976 and 17,690. Neither new certificate is of arity at
      most seven, so this is the census of record, not H-267's arity-seven measurement.
  verdict:
    decision: unresolved
    primary_criterion: The certified residue is at most 10^4 orbits with every certificate independently
      checked; rejected if it exceeds 10^4 at arity seven or a certificate excludes the endpoint state.
    reason: Both certificates pass the standing verifier in full and are admitted, and the endpoint survives,
      but 15,953 orbits remain, and an arity-9 class and a whole state bear on H-267's arity-seven criterion
      only as progress on the census.
    needs_review: false
    commit: ae4f5fb43671a5ba77e2e4187b77502e54ce6862
  effort:
    timebox: 7000 seconds per verification; one worker
    wall_seconds: 836.0
    stopped_by: criterion
---
# exp-250: Two Kernel Certificates Admitted by the Standing Verifier

[H-267](../../../hypotheses/H-267-n17-isolated-sub-pattern-residue.md) counts the n17
states that survive certified sub-pattern exclusions on the unique-state cover.
This round admits two more kernel certificates to that census: flag 3, a nine-cell class
named SW9 here, and N1, a whole 17-cell residue state.
N1 is also the first exclusion of a whole state, the kind whose cost
[H-264](../../../hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md) asks about.

## What Is Certified

No 9 unit squares with centres in SW9’s cells, and no 17 with centres in N1’s, fit
inside $[0,1169/250]^2$ with disjoint interiors.
Both were closed by the ownership-induction kernel, and in both the last owner loses
every parent pose: side-N0 at step 101 for SW9, interior-W at step 81 for N1.

SW9 closed with adaptive rows (split floor 1/512, at most 1,152 rows, 24 rounds).
With uniform rows and a 12-round cap the same class, from the same seed, is a certified
stall. N1 closed in 3,723 s under a two-hour ceiling and stalled under a 45-minute one.

## How They Were Admitted

Under [OR-16](../../../../../operating-rules.md) as amended on 2026-10-03, the full pass
of a reviewed standing verifier is the admission check: there is no clean-worktree
re-run and no review of each certificate.
The kernel verifier is the one the
[verifier-rewrites review](../../../../../docs/project/reviews/review-2026-10-03-n17-verifier-rewrites.md)
admitted at `575795e02`. Since then `25c1cdef6` changed only its input and recording: it
no longer reads file names back as a check, and its receipt records provenance instead
of a module digest. The
[ledger](../../../explorations/X048-session-168-pilots/certified-sub-patterns.yaml) now
lists it at `25c1cdef6`, and both verifications ran with that file.

No run was repeated.
The [results directory](../results/exp-250-n17-standing-verifier-admissions/) holds only
the census; the run records are the retained receipts under
[X048](../../../explorations/X048-session-168-pilots/README.md):

| Record | What it shows | Wall |
| --- | --- | ---: |
| `receipts/kernel-split-flag3-a9-bins64.json` | SW9 with adaptive rows: producer closed, checker `PASS_CERTIFIED_CLOSED` | 1,521 s |
| `receipts/kernel-flag3-a9-bins64.json` | SW9 with uniform rows: certified stall, the control | 1,562 s |
| `certificates/flag3-a9-pending/verification.json` | standing verifier, full mode, at `fd2c9602e`: PASS | 351 s |
| `handoff/k2/h-N1-2h.json` | N1 under a two-hour ceiling: `PASS_CERTIFIED_CLOSED` | 3,723 s |
| `handoff/k2/h-N1.json` | N1 under a 45-minute ceiling: certified stall | 2,694 s |
| `certificates/N1-state-pending/check-saved.json` | N1’s checker alone in a fresh process: `PASS_SAVED_CLOSED` | 3,767 s |
| `certificates/N1-state-pending/verification.json` | standing verifier, full mode, at `ae4f5fb43`: PASS | 482 s |

N1’s earlier full pass, by an earlier version of the verifier, stays beside it as
`verification-5c550f7c.json`, with the same counts.
Both certificate directories keep their `-pending` names, because each verification
receipt names its directory and the census requires that name.

## What It Changes

The [census](../results/exp-250-n17-standing-verifier-admissions/census.json) now counts
126,168 surviving states and 15,953 orbits, down from exp-249’s 139,976 and 17,690, with
the endpoint’s state surviving.
At the margin SW9 removes 13,804 states and 1,736 orbits, and N1 its own 4 states, one
orbit.

H-267 stays undecided.
Its criterion is about classes of arity at most seven, and neither new certificate is
one, so the drop is progress on the census rather than evidence on the threshold.
For H-264, N1 is one sampled state closed within two CPU-hours, of the 10 to 20 its
falsifier needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
