---
title: H-135 — full effective dual support exposes a 32-row pointwise miss
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-135
  kind: hypothesis
  claim: Solving the unit-square transport of the retained BC-232 cutting state once and pricing its full
    positive dual support finds at least one new site orbit, absent from the transported state, whose
    exact depth under the first 32 positive rationalised dual rows is at most one and whose exact depth
    under the full positive rationalised support is greater than one.
  lane: proof
  derived_from:
  - X-022
  strategy_refs:
  - proof:15
  criterion:
    shape: determination
    metric: exact same-orbit paired32 and full depth under one LP solve and one rationalised dual sequence
    direction: an absent-from-state full witness has paired32 depth <= 1 < full depth
    threshold: paired32 depth <= 1 < full depth
  instrument: packing/devtools/price_cutting_state_dual.py on the exact unit-square transport of packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json;
    controls passed in the continuation checkout; exp-134 will bind the published instrument commit before
    target execution.
  instrument_ready: true
  regime: n = 11, container side 96/25, square side one, retained BC-232 sites, rows and 181-direction
    net transported exactly by factor 10000/9977 and centred in the target container; one scipy linprog
    solve in float64, with every raw dual preserved in hexadecimal, entries selected only when the raw
    dual is strictly greater than 1e-9, and selected weights rationalised once as Fraction(round(raw_dual
    * 10^9), 10^9) using Python's nearest rounding; paired32 is exactly the first 32 entries of that sequence
    and full retains every selected entry.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One 30-minute pricing process with a two-second TERM grace and one LP solve on the
    ten-logical-CPU host. Solver threading uses its default; no four-core allocation is enforced. The dense LP matrix is 346.6 MiB; its negated copy and solver workspace
    raise peak memory materially above 700 MiB. The line-pair guard bounds candidate construction separately.
    No candidate or cutting iterations.
  prereqs:
  - reviewed paired-pricing instrument and controls published on the stacked continuation branch
  - retained BC-232 state and exact unit-square transport receipt
  - five-million candidate line-pair guard evaluated before pair intersections are materialised
  replication: true
  registered: '2026-09-08'
  notes: This is a pointwise mechanism test. Both arms use the same raw LP dual and the same rationalised
    support ordering. Acceptance requires an exact rational membership replay at the same full-arm witness
    and exact proof that its complete D4 orbit is absent from the transported state. The float LP and
    arrangement screen only propose that witness. The claim does not reconstruct the lost historical BC-232
    dual, does not say the 32-row arm has no new site anywhere, and does not establish a global covering
    or packing certificate. A line-pair guard refusal, timeout, missing output or execution error leaves
    the hypothesis unresolved.
---
# H-135 — Paired Full-Support Pricing

BC-232 retained a cutting state, not its historical LP dual.
The proposed round solves that transported state once and records the new dual before
expensive arrangement work.
It then compares nested rational supports from that one solve: `paired32` uses
`full_entries[:32]`, while `full` uses every positive entry.

The mechanism succeeds only on a full-arm witness whose complete orbit is absent from
the state and whose membership is replayed exactly in both families with
`depth₃₂ ≤ 1 < depth_full`. Empty `paired32.chosen` output is not evidence of the
inequality. The same witness must be checked in both arms.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
