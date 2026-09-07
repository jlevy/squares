---
title: exp-125 — complete two-band H124 residual cover
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-125
  series: series-000
  title: Certify the complete H124 common-obstacle cover in both whole angle bands
  date: '2026-09-07'
  hypotheses: [H-124]
  tier: confirmatory
  subject:
    label: Fixed q=1939/500, reviewed E=conv(D union K1), unchanged P9 and complete closed center domains for both whole bands
    engine: Independently source-bound exact closed-polygon endpoint-chain certificates
    engine_commit: 7daa7c55
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python3.14.7
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Independent generic cover instruments passed21 producer and69 reader controls
      and separate reviews in Session093. Source constructors passed33 producer and
      22 independently authored reader controls, with mathematical reviews completed
      by10:14:46 UTC. The capped caller passed13 source-free controls and independent
      mechanical review. All controls forbid actual scientific construction.
    candidate: >-
      Exactly two obligations, frame axis followed by diagonal. Each uses the fixed
      reviewed whole-band inner kernel, complete center box, E plus kernel, all nine
      original mark translations and exactly the three B/D/F corner patches. No
      angle samples, changed kernel, mark, side, obstacle, subdivision or retry.
    runs_per_condition: 1
    interleaved: false
    operator: Session094 coordinator, BC255; max mathematical judgment
    commit: 7daa7c55
    dirty: false
    entry_point: packing/devtools/run_h124_cover.py
    command: >-
      /usr/bin/time -p env PYTHONPATH=src
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.run_h124_cover --frame axis --limit 5000 --timeout-seconds 120
    budget: >-
      One120-second complete-process producer for each of axis then diagonal.
      Only actual exit zero and a well-formed covered packet authorize one60-second
      independent reader for that frame. A valid unresolved first-band receipt with
      stop_reason no_chain, event_limit or slab_limit may
      be followed by the separately declared second-band producer, because their
      partial proof obligations differ. A timeout, malformed packet, nonzero exit
      or independent reader failure stops the entire sequence. No retry or cap
      extension. Begin by10:32 UTC, finish by10:38:06 UTC, or retain non-invocation.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-125-h124-complete-residual-cover
  lease:
    expires: '2026-09-07T10:38:06Z'
    host: Session094 coordinator
  results: []
  verdict:
    decision: in-progress
    primary_criterion: Both complete closed whole-band covers pass independent source reconstruction and endpoint-chain verification, together with the reviewed analytical reduction.
    reason: Prospectively registered; no scientific source constructor or cover invocation has run. Immutable push evidence, protocol review and committed record checks remain launch prerequisites.
---
# Complete H124 Residual Cover

This is a new complete sufficient-cover experiment, not a repeat of exp124’s fixed-S
screen. The exact source and its mathematical reduction are defined in
[H124](../../../hypotheses/H-124-full-distinguished-square-compatibility.md).
Source construction, actual producer-reader wire agreement and runtime are untested.

## Frozen Admission and Commands

Use clean immutable engine `7daa7c55`, with its `packing/` as the working directory.
The engine push tier, independent protocol review and committed prospective record
checks must pass before either scientific source is constructed.
The full checkpoint gate is tracked separately; its pending state is not a claimed pass.

Run the declared producer once for `axis`, then at most once for `diagonal`,
substituting only the frame argument.
Each has `--limit 5000 --timeout-seconds 120`. These frame names denote complete
continuous angle bands, not central-angle samples.
The static source bound is13 polygons, at most60 vertices and at most2,082 conservative
x-events.

For a frame, actual exit zero, exact source label `h124:axis` or `h124:diagonal`,
envelope kind `h124-closed-cover/v1`, and nested `status=covered` with
`stop_reason=complete` permit exactly one independent reader:

```bash
/usr/bin/time -p env PYTHONPATH=src \
  /Users/levy/wrk/github/squares/packing/.venv/bin/python3 \
  -m devtools.run_h124_cover --frame axis --limit 5000 --timeout-seconds 60 \
  --input /absolute/path/to/that-frame/packet.json
```

The replay must return actual exit zero, matching source, `status=verified_source_cover`
and literal `cover_proved=true`; its nested independent result must also report
`status=verified_cover` and literal `cover_proved=true`. One completed frame is only a
partial sufficient lemma.
Both accepted frames, together with the independently reviewed common-obstacle and
counting reductions, accept H124 and establish restricted H036. They do not improve the
unrestricted packing bound.

## Stop Conditions and Retention

A well-formed producer receipt with `status=unresolved` and `stop_reason` exactly
`no_chain`, `event_limit` or `slab_limit` is not a counterexample and does not authorize
a reader. It leaves that frame unresolved.
The other predeclared frame may still supply useful partial evidence, but no scientific
call is repeated. `arithmetic_error` or `deadline` stops all remaining calls even if the
producer exits zero.
Any other operational error, timeout, malformed receipt or failed reader also stops the
sequence; do not reinterpret that as a scientific negative.

Keep separate `axis/` and `diagonal/` subdirectories beneath the declared result path.
For each invoked process retain stdout and stderr with external wall/user/system timing
and the actual tool exit code in the experiment narrative.
Retain partial or empty output on failure, labeled as such.
A conditional process not invoked gets no invented receipt.
Remove the lease and record the scoped verdict when this sequence ends.

Fresh upstream/open-PR inspection at10:05 UTC found no exp125 or H125 in PR110 at
`57b85302`; this record allocates exp125 sequentially.
It allocates no new hypothesis, agenda, BC or exploration ID. Session094 and this
experiment remain on integrated PR109.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
