---
title: exp-121 — one exact fixed P12 escape test
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-121
  series: series-000
  title: Test the frozen near-axis P12 escape candidate
  date: '2026-09-07'
  hypotheses: [H-110]
  tier: confirmatory
  subject:
    label: One frozen rational unit square and all twelve unchanged points at q=1939/500
    engine: Exact projection producer and source-distinct oriented-corner reader
    engine_commit: 961d9923
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Python 3.14.7; GNU coreutils timeout 9.9
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Thirteen producer and twelve reader source-free controls pass, with swapped
      independent reviews completed by06:07:43UTC. Controls forbid the scientific
      constructors and cover exact frame identities, strip-gap signs/endpoints,
      closed boundaries, supporting-line nonmembership, full inventory, refusal
      and CLI exits. No target has run at registration.
    candidate: >-
      Exactly H-110: q=1939/500, t=1/1000, strip-midpoint center, unchanged
      source-ordered P12. No search, alternative parameter, point movement or symmetry.
    runs_per_condition: 1
    interleaved: false
    operator: Codex coordinator, max mathematical judgment, Session091 BC-255
    commit: 961d9923
    dirty: false
    entry_point: packing/devtools/p12_escape_candidate.py
    command: >-
      /usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s
      env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.p12_escape_candidate --target-h110
    budget: >-
      One ten-second whole-process producer cap, including startup and output.
      A complete packet and actual exit zero, whether escaped or not_escaped,
      permit one independent reader with its own ten-second whole-process cap.
      No retry, alternate candidate or second invocation. Launch before06:40UTC;
      otherwise retain non-invocation and select a fresh future allocation.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-121-h-110-fixed-p12-escape/packet.json
  effort:
    timebox: One ten-second producer and one independent ten-second reader, each invoked once
    wall_seconds: 0.11
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Does the frozen square fit in the actual domain and strictly avoid all twelve unchanged points?
    outcome: criterion_met
    checked_by: >-
      Independent reader returned actual exit zero, status escaped, complete true,
      exact unit CCW geometry, actual angle membership, sixteen wall slacks,
      twelve point checks and forty-eight edge determinants. Every point has a
      strictly negative edge determinant; no contained point or unresolved entry.
  verdict:
    decision: accepted
    primary_criterion: Independent exact validity and strict twelve-point avoidance of the frozen H-110 square.
    reason: The independently reconstructed frozen square is contained in the box and strictly avoids all twelve unchanged points.
    commit: 18e5a641
---
# exp-121 — Fixed P12 Escape

H-110 is accepted. The prospective protocol was committed as `18e5a641` after all 31
record checks passed in 20.2 seconds.
The sole producer launched at the observed 06:18:18 UTC boundary and returned actual
exit zero with a complete `escaped` packet.
The independent reader launched once at 06:18:49 UTC and returned actual exit zero,
`escaped`, all twelve strict avoidances and no unresolved entry.

Producer cost was 0.06 seconds wall and 0.04 CPU; replay cost was 0.05 seconds wall and
0.05 CPU. Total scientific process cost was 0.11 seconds wall and 0.09 CPU, separate
from author, review and coordinator time.
Neither allowance was repeated or extended.
The result directory retains `packet.json`, `producer.log`, `replay.json` and
`replay.log`.

This refutes the unchanged unconditional near-axis P12 clause.
It does not refute H-036 or establish a new packing bound.

## Retained Prospective Protocol

The following protocol was committed before either scientific process.
The source is the clean instrument commit `961d9923`; run from a detached checkout of
that commit, using its `packing/` directory and `PYTHONPATH=src`. The existing project
Python 3.14 environment supplies only standard-library dependencies for these two
instruments. No scientific result existed at registration.

## One Producer and One Independent Reader

Verify that the entire result directory and every output path are absent.
The producer command above writes stdout to `packet.json` and stderr, including external
timing, to `producer.log`. Retain the actual tool exit and never infer it from packet
status. Only an actual exit zero and a complete packet with status `escaped` or
`not_escaped` authorize the reader:

```bash
/usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_p12_escape_candidate --input ABSOLUTE_PACKET_PATH
```

Retain its stdout as `replay.json` and stderr/timing as `replay.log`. Its independent
reconstruction must agree exactly with the frozen candidate and all twelve marked
points. It verifies unit CCW geometry, the actual angle-domain proof, all sixteen wall
slacks and all forty-eight point-edge determinants.
Neither process has an internal timer; the two separately frozen external caps cover the
whole process.

The actual angle argument is `0<t<1/480`, implying `0<2 arctan(t)<2t<1/240<pi/720`
because `pi>3`. Failure of this sufficient guard is unresolved, not evidence that an
angle lies outside the actual band.

## Frozen Disposition

Accept H-110 only with actual reader exit zero, a complete `escaped` result, correct
identity, unit geometry, actual angle membership, box containment, all twelve points
strictly outside and no unresolved entry.
Reject only when the correctly reconstructed candidate is independently shown to violate
containment or contain at least one mark.
A completed negative also has exit zero; its mathematical status differs from process
failure. Malformed packets, wrong identity, disagreement, failed sufficient guards,
exceptions, timeouts and incomplete inventories are refused or unresolved, not
mathematical rejection.

No failure authorizes another invocation.
If the producer does not authorize replay, record that the reader was not invoked
instead of fabricating a receipt.
The `verified` assurance field describes the required exact decision route; it is not an
assertion that the unrun candidate already passes.

A verified one-square escape refutes only the unchanged unconditional near-axis P12
auxiliary construction.
It does not refute H-036 or H-102, does not invalidate the accepted H-106/H-108/H-109
lemmas, and is not an eleven-square packing.
The separately reviewed fixed-diamond counting reduction remains conditional on
localization and a complete both-band nine-point cover.
Select its next discriminator from this outcome; do not reinterpret this experiment as a
test of diamond compatibility.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
