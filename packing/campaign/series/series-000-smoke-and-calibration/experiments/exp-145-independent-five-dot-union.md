---
title: "exp-145 \u2014 independent exact five-dot polygon-union audit"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-145
  series: series-000
  title: Independent exact five-dot polygon-union audit
  date: '2026-09-09'
  hypotheses:
  - H-143
  tier: confirmatory
  subject:
    label: Unchanged exp143 four endpoint patches and five equal atoms
    engine: Self-contained Fraction polygon clipping and inclusion-exclusion; no production geometry imports
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python 3.14; one process
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: 19 passing synthetic tests, including exact oblique area 7/8, corner completion, rational
      rotation, broken cover, and geometric direction-uniqueness guards; independent Astra Max mathematical
      review.
    candidate: Compute exact uncovered area in each complete contained-core center rectangle using the
      nine closed collision polygons and all 361 canonical directions.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra coordinator; instrument by GPT-5.6 Sol extra high; mathematical review by GPT-6
      Astra max
    entry_point: packing/cases/n11_five_dot_cover/independent_union.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m cases.n11_five_dot_cover.independent_union campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      --expect-receipt-blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19 --expect-directions 361 --max-subsets-per-direction
      511 --deadline-seconds 240 --output campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-145-independent-five-dot-union.json
    budget: One five-minute external process plus two-second termination grace, 240-second cooperative
      internal deadline, and at most 511 nonempty subset masks per direction. No tuning, retry or resume.
      The full allowance must fit in the launching session.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-145-independent-five-dot-union.json
  results: []
  lease:
    expires: '2026-09-09T15:00:00Z'
    host: local; prospective reservation, no process launched
  verdict:
    decision: in-progress
    primary_criterion: Complete exactly the 361 required unique directions with exact zero uncovered area
      at every direction and valid source provenance.
    reason: Prospective protocol only. Passing instrument and protocol must be committed and pushed before
      the one target invocation. No target has run.
---
# Exp145: Independent Five-Dot Union Audit

**Prospective; target unrun.** The instrument and this protocol must be committed and
pushed before invocation.
Record that exact launch commit, clean/dirty state, UTC start, exit status and process
duration in the launch receipt.
The input must retain Git blob `cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19`; the driver
refuses changed input or an existing output.
This publication commit is the source freeze, and its exact hash is captured at launch
rather than guessed in a self-referential protocol.

At q = 96/25 and B = 9977/10000, check the four unchanged owner patches and the five
unchanged dots from exp143. For each orientation, the legal-center rectangle must be
covered by the union of the four patch-collision polygons and five dot-collision
polygons. The [contract](../../../../cases/n11_five_dot_cover/union-contract.md) proves
why exact zero uncovered area gives pointwise coverage, including boundaries.

Accept only a complete all-361 result with every deficit exactly zero.
A positive exact deficit rejects this fixed coverage proposal.
A control failure, provenance mismatch, exception, timeout or partial manifest is
unresolved. No incomplete output is a cover, and no escaping residual core proves an
eleven-square packing exists.

The source uses its own rational parsing, direction generator, hull, clipper and
inclusion-exclusion.
The raw footprint coordinates and analytic transfer premises are shared with T-023.
Agreement adds independent finite geometric evidence; it does not automatically promote
confirmation to C4, certify an LP optimum, cover every owner class, or strengthen the
global n11 bound.

Session114 may launch only by 07:45:32 UTC, so the entire process allowance fits before
its research cutoff.
If publication misses that cutoff, retain this protocol unrun and allocate its unchanged
allowance prospectively in a successor session under Agenda033.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
