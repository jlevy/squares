---
title: exp-122 — four-frame diamond-conditioned cover screen
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-122
  series: series-000
  title: Screen H122 at four exact frames for one independently verified escape
  date: '2026-09-07'
  hypotheses: [H-122]
  tier: exploratory
  subject:
    label: Fixed diamond and unchanged nine marks at q=1939/500, four prescribed frames
    engine: Exact event-cell and signed-axis producer with independent corner/SAT reader
    engine_commit: c4a69e3e
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python 3.14.7, GNU coreutils timeout 9.9
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Twelve producer and twelve source-distinct reader controls passed, followed
      by swapped independent reviews by06:49:01UTC. Controls forbid scientific
      constructors and cover exact signed frames, closed/open event strata,
      boundary tangency, positive-gap mixing, nine-point/corner identities,
      malformed input and no-witness refusal. No target has run at registration.
    candidate: >-
      One screen in the fixed order axis-negative, axis-positive, near45-negative,
      near45-positive, each half-angle offset t=-1/500 or +1/500 about its chart.
      Stop at the first witness. No new frame, alternate order, obstacle or mark.
    runs_per_condition: 1
    interleaved: false
    operator: Session091 coordinator, BC255, max mathematical judgment
    commit: c4a69e3e
    dirty: false
    entry_point: packing/devtools/diamond_cover_screen.py
    command: >-
      /usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 30s
      env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.diamond_cover_screen --target-h122
    budget: >-
      One thirty-second whole-process producer cap, including all four frames,
      startup and output; this is a bounded falsifier, not a completion estimate.
      Only an actual exit zero and a well-formed witness packet authorize one
      independent ten-second whole-process reader. No retry or additional frame.
      Launch before07:15UTC or retain non-invocation and a fresh future allocation.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-122-diamond-conditional-cover-screen/packet.json
  lease:
    expires: '2026-09-07T07:15:00Z'
    host: Session091 coordinator; prospective, no scientific process invoked
  results: []
  verdict:
    decision: in-progress
    primary_criterion: One actual contained both-band square strictly avoids all nine marks and the closed diamond.
    reason: Prospective bounded falsifier only; source-free readiness is reviewed but no target has run.
---
# exp-122 — Diamond-Conditioned Cover Screen

Commit this protocol and pass the record checks before either scientific process.
The exact instruments are frozen at `c4a69e3e`; use its clean detached checkout with
`packing/` as the working directory. The H-122 label was fixed before that commit.
This allocation is independent of the already completed H-110/exp-121 invocation.

## Frozen Scope and Caps

The producer examines the four frames in the order recorded above. Each actual angle
offset satisfies `abs(2 atan(t))<1/250<pi/720`. It searches all contained centers at
a frame through exact closed/open event strata until finding one witness, exhausting
the prescribed frames or reaching its thirty-second whole-process cap.
The cap is not a prediction that enumeration finishes. No result authorizes more time,
a rerun, a different frame or a larger obstacle.

Before launch, check that the result directory and every output path are absent.
Retain stdout as `packet.json`, stderr/external timing as `producer.log`, and the
actual process exit. A complete finite `no_witness` result remains unresolved for the
continuous claim and does not authorize a reader. A timeout, exception or incomplete
packet is likewise unresolved; do not fabricate a reader receipt.

Only a well-formed `witness` packet and actual exit zero authorize this command once:

```bash
/usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_diamond_cover_witness --input ABSOLUTE_PACKET_PATH
```

Retain its stdout as `replay.json`, stderr/timing as `replay.log` and actual exit.
The reader independently reconstructs the frame, q, exact diamond and nine source marks.
It verifies unit CCW corners, the actual angle, sixteen closed wall slacks, thirty-six
point-edge determinants and strict polygon separation. Tangency is intersection.

## Scientific Disposition

Reject H-122 only with an actual exit-zero reader result `verified_counterexample`,
passed guards, complete evidence, all nine points strictly outside and a strictly
positive exact separating gap from D. Exit zero alone is insufficient: it also permits
the reader's `not_a_counterexample` outcome, which leaves this universal claim unresolved.
Frame summaries are producer provenance, not independently checked continuous coverage.
Shared exact arithmetic is `sqpack.field`; geometric implementations are separate.

This screen cannot accept H-122. Even complete success at all four frames would not
cover either full angle band. A verified escape rejects only the sufficient
fixed-diamond cover: it need not be compatible with any actual distinguished square.
H-036, H-102 and the global packing bound remain unresolved or unchanged.
Choose the next allocation from the exact obstruction and independently reviewed
localization result; do not silently strengthen the obstacle in this round.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
