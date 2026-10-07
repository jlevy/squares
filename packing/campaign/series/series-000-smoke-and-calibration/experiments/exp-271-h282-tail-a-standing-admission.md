---
title: "exp-271 \u2014 full standing admission verification for retained TailA"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-271
  series: series-000
  title: Full standing verification for the retained current-source TailA closure
  date: '2026-10-07'
  hypotheses:
  - H-282
  tier: confirmatory
  subject:
    label: Exact retained exp266 TailA seed/node, named17cells and canonical selector3096311.
    engine: devtools.verify_n17_kernel_certificate default full standing verifier, reviewed kernel-streamed
      listing
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Python 3.14.7, one process per invocation; external scratch.
    selftest_passed: true
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Existing reviewed kernel-streamed standing verifier; independent Sol validates exact saved-object/source/namedcell/Frame/selector
      custody before invocation. Fresh shared-kernel PASS_SAVED_CLOSED exp266 is necessary evidence, not
      this admission receipt.
    candidate: One fresh FULL standing replay of the unchanged retained TailA certificate; no producer
      retry.
    runs_per_condition: 1
    interleaved: false
    operator: Sol coordinator executes sole-Astra900-second admission contract; root alone mutates ledger/counts.
    entry_point: packing/devtools/verify_n17_kernel_certificate.py
    command: 'From packing/ with externalTMPDIR/UV_CACHE_DIR/CARGO_TARGET_DIR: /usr/bin/time -p /opt/homebrew/bin/gtimeout
      -k10s900s /Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3 -m devtools.verify_n17_kernel_certificate
      campaign/explorations/X048-session-168-pilots/certificates/s184-tail-a-m3096311 --output campaign/explorations/X048-session-168-pilots/certificates/s184-tail-a-m3096311/verification.json
      --progress. No --sample or --cells override.'
    budget: One900-second wall ceiling, TERM900/KILL910; root samples owned currentRSS4096MiB. Deliberate
      ceiling, not runtime forecast. Preserve all receipts/logs; no producer retry, parameter/source retuning
      or admission on missing/partial/sample receipt.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-271-tail-a-standing-admission
  results: []
  verdict:
    decision: in-progress
    primary_criterion: schema n17-certificate-verification/v1, verifier kernel, statusPASS, modefull,
      matching seed/node/frame/namedcells/canonicalselector/cap and closureowner11/step26; all27steps/1728rows
      full checked; reviewedkernel-streamed listing and ordinaryledger/census joins. Independent verifier
      eventcount equality is not required.
    reason: Registered before standing target; exp266 source65fc producer/selfcheck and freshfullreplay
      pass, independent custody clears. No ledger count changes yet.
  lease:
    expires: '2026-10-07T10:10:00Z'
    host: macOS arm64
---
# exp-271: Tail A Standing Admission

The successful fresh saved replay in exp-266 does not have the ordinary ledger’s
required standing-verifier schema.
This separately registered phase rechecks the same objects under the reviewed
`kernel-streamed` full verifier.
It authorizes no producer retry.
The scientific criterion and finite 900-second ceiling are frozen before launch.

Acceptance permits the separate ordinary admission of this single orbit only after all
source, certificate, canonical named-state and census joins.
Missing, sample-mode, incomplete or refused verification leaves the orbit pending.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
