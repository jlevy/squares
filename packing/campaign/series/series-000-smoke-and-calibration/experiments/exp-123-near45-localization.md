---
title: exp-123 — four-guard continuous near45 localization
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-123
  series: series-000
  title: Certify the complete H123 near45 localization through four sufficient guards
  date: '2026-09-07'
  hypotheses: [H-123]
  tier: confirmatory
  subject:
    label: Original P10 at q=1939/500, both full near45 angle signs and closed center domains
    engine: Exact four-guard producer and independent polynomial/Bernstein reader
    engine_commit: 3ea8e346
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python3.14.7, GNU coreutils timeout9.9
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Eighteen producer and ten independent reader source-free tests passed,
      with independent analytic review of the complete geometric implication and
      swapped instrument reviews completed by07:08:11UTC. Controls forbid frozen
      target constructors and direct frozen-width evaluation. No target signs
      have been evaluated at registration.
    candidate: >-
      Fixed q=1939/500 and W=q/2-1; DF and D-squared-G on the two closed half-angle
      slabs [-T,0] and [0,T], T=110880/50803079. Four obligations ordered
      (0,F),(0,G),(1,F),(1,G), sixteen exact Bernstein coefficients total.
      Unsplit Bernstein degree2 and degree4 certificates only; no subdivision.
    runs_per_condition: 1
    interleaved: false
    operator: Session091 coordinator, BC255, max mathematical judgment
    commit: 3ea8e346
    dirty: false
    entry_point: packing/devtools/near45_localization.py
    command: >-
      /usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 15s
      env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.near45_localization --target-h123
    budget: >-
      One fifteen-second whole-process producer cap, including startup and output,
      with its internal ten-second alarm unchanged. Only actual exit zero and a
      complete proved four-obligation packet permit one ten-second whole-process
      independent reader. No retry, subdivision or coefficient/domain change.
      Launch before07:24UTC or retain non-invocation; no implicit extension.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-123-near45-localization/packet.json
  effort:
    timebox: One fifteen-second producer and one ten-second independent reader, each invoked once
    wall_seconds: 0.21
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Do all four sufficient polynomial guards hold over both closed angle slabs?
    outcome: criterion_met
    checked_by: Source-independent reader reconstructs exact polynomials and all sixteen Bernstein coefficients; actual exit zero, proved and complete, four obligations checked, no unresolved entries. The separate analytic reduction passed independent review.
  verdict:
    decision: accepted
    primary_criterion: Independent complete four-guard certificate plus the independently reviewed full-domain geometric implication.
    reason: The independent exact four-guard certificate and reviewed geometric reduction prove complete H123 localization on the actual near45 domain.
    commit: 881a786a
---
# exp-123 — Complete Near45 Localization

H-123 is accepted. The prospective protocol was committed as `881a786a` after all 31
record checks passed in 26.63 seconds.
The sole producer launched at the observed 07:17:17 UTC boundary and completed with
actual exit zero, all four guards proved and the ordered obligation inventory complete.
It used 0.09 seconds wall and 0.08 CPU.

The independent reader launched once at 07:17:35 UTC and completed with actual exit
zero, `status=proved`, `complete=true`, four obligations and sixteen recomputed
Bernstein coefficients, exact identity agreement and no unresolved entries.
It used 0.12 seconds wall and 0.08 CPU. Total scientific process cost is 0.21 seconds
wall and 0.16 CPU, separate from author, review and coordination time.

Both JSON receipts and stderr/timing logs are retained.
No subdivision, alternate frame, coefficient change or repeated invocation occurred.
Combined with the independently reviewed geometric reduction, this completes the full
localization lemma, including closed boundaries and the actual near45 angle band.
It does not establish H-036 or change the packing bound.

## Retained Prospective Protocol

Commit this protocol and pass record checks before either scientific invocation.
Use the clean detached source at `3ea8e346`, with its `packing/` as the working
directory and the existing project Python3.14 environment.
The exact producer and source-distinct reader share number-field arithmetic, not
coefficient or geometric reconstruction.
Do not reuse an earlier target receipt.

The [H-123 proof reduction](../../../hypotheses/H-123-near45-coordinate-localization.md)
was independently reviewed through its closed center-domain cover, exact P10 marks,
overlapping height intervals, K4 symmetry, actual-angle outer enclosure and symbolic F/G
formulas.
Acceptance of the sufficient polynomial certificate completes that implication.
No center mesh, missing boundary seam or angle sample substitutes for it.

## Frozen Invocation and Admission

Check that the result directory and all output paths are absent.
Retain producer stdout as `packet.json`, stderr/external timing as `producer.log` and
its actual exit. The internal alarm does not cover imports and final serialization, so
the external fifteen-second cap is mandatory.
A timeout, exception, incomplete inventory or failed sign certificate is unresolved and
does not authorize another invocation.

Only actual exit zero and complete `proved` output with all four prescribed obligations
authorize this command once:

```bash
/usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_near45_localization --input ABSOLUTE_PACKET_PATH
```

Retain its stdout as `replay.json`, stderr/external timing as `replay.log` and actual
exit. The reader has no internal alarm.
It independently reconstructs both cleared polynomials by exact operations, recomputes
Bernstein coefficients, and binds the positive sqrt(2) field, q/W/T, both closed slabs
and ordered four-entry inventory.

Accept H-123 only with actual reader exit zero, `status=proved`, `complete=true`,
`obligations_checked=4`, `bernstein_coefficients_checked=16`, exact identity agreement
and all recomputed coefficients nonnegative.
Combine this with the separately accepted analytic reduction, rather than treating the
numerical tool as its proof.
Zero coefficients are allowed because all clauses are closed and non-strict.

A failed sufficient polynomial/Bernstein guard is unresolved, not a localization
counterexample. Errors, timeout, missing evidence, identity mismatch and insufficient
receipts are likewise unresolved.
There is no automatic refinement or retry.

H-123 localizes a P10-avoiding near45 square under the global coordinate-reflection
group. It is an auxiliary lemma, not H-036 or a new packing bound.
H-122’s verified negative already rules out the small fixed-diamond shortcut; complete
compatibility with an actual distinguished square is a separate, unlaunched obligation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
