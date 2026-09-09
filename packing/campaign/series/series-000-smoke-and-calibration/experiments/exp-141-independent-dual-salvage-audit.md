---
title: "exp-141 \u2014 independent conditional dualscreen replay"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-141
  series: series-000
  title: Independent replay of the retained conditional dualscreen
  date: '2026-09-09'
  hypotheses:
  - H-137
  tier: confirmatory
  subject:
    label: Published exact owner-footprint screen receipt and unchanged BC232 source family
    engine: devtools.audit_corner_dual_salvage; independent receipt reconstruction without producer invocation
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python3.14.7; one process
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Source Gitblob8a0bf1a264a1361649bc0acd0f70907ba8125f2f and exp137 receipt Gitblobdef74a3693f7fd4c0dbe434078df00786505b7d0;
      exact point/triangle/endpoint source identities and complete case sets.
    candidate: Independently reconstruct361directions, translation,192component masks and all3times65536joint
      classes; verify source indices, unchanged weights, strictSAT witness gaps, cardinality, masks, exact
      masses and summaries. Reassess the original H137 claim from audited data; original H138 record also
      receives review status from the full audit.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra,max; session113 coordinator
    entry_point: packing/devtools/audit_corner_dual_salvage.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.audit_corner_dual_salvage campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-137-corner-dual-salvage.json.gz
      campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json --expect-receipt-blob
      def74a3693f7fd4c0dbe434078df00786505b7d0 --expect-source-blob 8a0bf1a264a1361649bc0acd0f70907ba8125f2f
      --max-compressed-bytes 20000000 --max-uncompressed-bytes 200000000 --max-source-placements 1000
      --max-component-screens 1000 --max-joint-classes 100000 --out campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-141-corner-dual-salvage-audit.json
    budget: One five-minute externally bounded audit plus2secondTERM grace. Refuse oversized compressed/expandedinput
      before decoding;1000sources,1000component screens,100000jointclasses perkind. No producer replay,
      arrangement-depth recomputation, LP or retry.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-141-corner-dual-salvage-audit.json
  lease:
    expires: '2026-09-09T04:55:00Z'
  results: []
  verdict:
    decision: in-progress
    primary_criterion: 'Original H137 claim: the audited maximum endpoint one-corner survivor mass is
      at least10. Audit success by itself does not make this mathematical claim true.'
    reason: Prospective independent receipt audit. Exp137 already reports a negative; this confirmation
      must retain that verdict if all exact checks pass, and stay unresolved if the audit fails.
---
# Exp141: Independent Dualscreen Replay

Exp137 reports a negative result on H137, with its needs_review flag still set.
This confirmatory experiment audits that immutable receipt; it is not a new unobserved
discovery sample. Its mathematical verdict remains tied to H137’s original threshold.
Passing the audit and confirming a subthreshold mass rejects H137; it does not accept
the opposite claim by relabeling the hypothesis.

The separate auditor reconstructs source poses and finite direction membership, checks
every recorded strict separating witness, and independently validates every joint case
and aggregate. Mutation controls cover wrong source identities, weights, gaps, masks,
class counts and summaries.
It never calls the producer or its depth arrangement routine.
The original source’s exact depth-one receipt remains an explicit inherited assumption,
with its published provenance preserved.

The same complete audit also discharges the pending review on exp138’s H138 verdict.
The53.38second producer cost remains charged once to exp137; this audit records its own
actual runtime. Guard failure or incomplete evidence leaves review pending.
Commit and push this protocol and the controlled auditor before invoking the target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
