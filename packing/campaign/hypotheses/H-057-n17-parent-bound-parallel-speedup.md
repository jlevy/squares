---
title: H-057 — parent-bound parallel execution makes the n = 17 residue admissible
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-057
  kind: hypothesis
  claim: >-
    On the same host and the fixed exp-052 inputs at ordinals 33, 107 and 180, a
    three-process parent-bound direction runner with deterministic single-writer merge
    attains at least 2.8x median wall-time speedup over the unchanged serial runner while
    producing byte-identical exact rows in three paired AB/BA/AB repetitions, with no
    paired trial at or below 1x.
  lane: proof
  derived_from: [X-011]
  strategy_refs: ['proof:21']
  criterion:
    shape: paired
    metric: >-
      paired monotonic wall time for the unchanged serial and candidate runners on fixed
      ordinals 33, 107 and 180; exact row bytes, event hashes, parent bindings and merged
      chain bytes; normal/optimized and interrupted/resumed assembly receipts
    direction: >-
      accepted only if the median paired speedup is at least 2.8x, every candidate row
      and merged chain is byte-identical to the serial control, no paired trial is at or
      below 1x, and all corruption and interruption mutations reject; rejected if the
      complete paired design is exact but misses either speed threshold; unresolved if
      profiling, equivalence, parent binding, deterministic merge or review is incomplete
    threshold: median paired speedup >= 2.8x and minimum paired speedup > 1x
  instrument: >-
    Agenda-014 BC-123's independently admitted external profiler wraps the unchanged
    exp-052 kernels in disjoint, exact-root-bound worker fragments and a deterministic
    single-writer merger. Its 30 target-blind controls validate every row, event hash and
    final three-pair statistic; reject gaps, duplicates, reordering, foreign parents,
    partial fragments, path escapes, missing or corrupt pairs and result overwrite; and
    compare normal, optimized and interrupted assembly receipts without making an
    exp-052 claim.
  instrument_ready: true
  regime: >-
    One fixed host, three process workers, fixed ordinals 33, 107 and 180, three paired
    repetitions in AB/BA/AB order, cold process starts recorded separately, and exp-052
    checkpoint/progress read-only. The three ordinals are an admission discriminator;
    they do not establish that all remaining 148 directions have equal cost.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    one 150-minute build, independent-admission and paired-profile block in 15--25-minute
    cells; no completion attempt is included
  prereqs:
  - independently reviewed exp-052 record and immutable checkpoint/progress
  - unchanged source-faithful and direct exact kernels
  - frozen parent hash, fragment schema, merge order and corruption mutations
  replication: false
  registered: '2026-09-01'
  notes: >-
    Acceptance makes a later 120-minute target wall arithmetically admissible; it does
    not decide H-052, predict every remaining direction, adopt the n = 17 lower bound or
    move n = 18 or n = 19.
---
# H-057 — Parent-Bound `n = 17` Parallel Speedup

The 33-row checkpoint solved retention, not runtime.
This claim asks whether an exact, deterministic process boundary is fast enough to
justify a later continuation without changing the certificate algorithms under
comparison.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
