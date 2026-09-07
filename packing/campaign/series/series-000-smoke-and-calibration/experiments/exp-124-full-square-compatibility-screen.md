---
title: exp-124 — fixed-square full compatibility discriminator
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-124
  series: series-000
  title: Test one exact45 distinguished square against the fixed exp122 square
  date: '2026-09-07'
  hypotheses: [H-124]
  tier: exploratory
  subject:
    label: Fixed exp122 square S and canonical exact45 Q at q=1939/500 with all original marks
    engine: Exact clipped event-cell producer and independent source-bound corner/SAT reader
    engine_commit: a75d751a
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python3.14.7, GNU coreutils timeout9.9
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Thirteen producer and fourteen independently authored reader source-free
      controls passed, followed by separate independent reviews completed by
      08:09:33UTC. Controls forbid scientific constructors and retained-source
      access. Canonical clipping, open strata, closed seams, all-mark identity,
      actual angles and strict disjointness are reviewed. No target has run.
    candidate: >-
      Preserve S verbatim from the exp122 packet in the engine commit, including
      its ordered corners and axis-negative offset -1/500. Q uses exactly the
      positive45 frame and canonical center [1,q/2] times [0,1]. Enumerate its
      exact event strata against all ten P10 marks, searching eight signed
      Q/S edge-normal axes for a strict separating witness. No second frame or S.
    runs_per_condition: 1
    interleaved: false
    operator: Session093 coordinator, BC255, max mathematical judgment
    commit: a75d751a
    dirty: false
    entry_point: packing/devtools/full_square_compatibility.py
    command: >-
      /usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 30s
      env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.full_square_compatibility --target-h124
    budget: >-
      One thirty-second whole-process producer cap, including startup and output.
      Only actual exit zero and a well-formed witness packet authorize one
      independent ten-second whole-process reader. No retry, second frame,
      changed fixed square, obstacle substitution or budget extension.
      Launch before08:28UTC or retain non-invocation for a fresh future allocation.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-124-full-square-compatibility-screen/packet.json
  lease:
    expires: '2026-09-07T08:28:00Z'
    host: Session093 coordinator; prospective, no scientific process invoked
  results: []
  verdict:
    decision: in-progress
    primary_criterion: One independently verified closed-disjoint Q/S pair satisfies the complete H124 premises.
    reason: Prospective bounded fixed-S discriminator; independently reviewed instruments are ready but no target has run.
---
# exp-124 — Full-square Compatibility, One Fixed Slice

Commit this protocol and pass the record checks before either scientific invocation.
The reviewed engine is frozen at `a75d751a`; use that clean detached checkout with its
`packing/` as the working directory.
The retained exp122 square is an input to this new question, not a repeated
diamond-cover run.

The current independent PR110 inventory at `daedeb9f` contains Session092 but no new
hypothesis or experiment IDs.
This line allocates exp124 sequentially after that fresh check; no further experiment is
reserved.

## Frozen Invocation and Admission

Q is a contained closed unit square at exactly45 degrees.
Its center lies in [1,q/2] x [0,1], with q=1939/500, and it avoids all ten original P10
marks. The fixed S retains every source field from exp122 and avoids all nine B–J marks.
The source’s half-angle offset -1/500 obeys the reader’s strict guard1/480, which
implies actual-angle membership because2atan(|t|)<1/240<pi/720. The independent reader
checks both square geometries and the complete input identity.

Check that the result directory and all four output paths are absent before launch.
Retain producer stdout as `packet.json`, stderr and external timing as `producer.log`,
and the actual process exit.
A complete finite `no_witness` output is unresolved for H124 and does not authorize a
reader. Timeout, error or incomplete evidence is also unresolved.
Never create an inferred reader receipt.

Only actual producer exit zero and a well-formed `witness` authorize this command once:

```bash
/usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_full_square_compatibility --input ABSOLUTE_PACKET_PATH
```

Retain stdout as `replay.json`, stderr and timing as `replay.log`, and actual exit.
Neither instrument has an internal timeout; both external whole-process caps are
mandatory. They cover imports, source loading, checking and serialization.

## Scientific Disposition

Reject H124 only with actual reader exit zero, `status=verified_pair`, complete
evidence, passed guards, all76 mark-edge determinants checked,16 coordinate containment
checks and32 scalar wall inequalities, canonical Q, actual angle membership, unchanged
source identity, strict disjointness and no unresolved obligations.
A positive claimed gap is checked exactly, and a separate corner-based SAT calculation
must find strict separation.
Tangency is intersection, not a counterexample.

No result from this finite screen accepts continuous H124. Even exhaustive no-witness
output concerns only this fixed S and Q frame; it leaves every other S and Q angle open,
and its search coverage is not independently certified by the witness reader.
A valid pair refutes this sufficient compatibility route, not H036, an eleven-square
packing theorem or the global lower bound.

After disposition, reprice the strongest remaining route alongside the independently
funded graph-certificate component.
Do not turn the result into an automatic second frame, modified S, larger cap or
unbounded continuous proof build.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
