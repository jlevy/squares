---
title: exp-134 — paired 32-row and full-support pricing of the transported BC-232 state
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-134
  series: series-000
  title: Paired 32-row and full-support pricing of the transported BC-232 state
  date: '2026-09-08'
  hypotheses:
  - H-135
  tier: exploratory
  subject:
    label: one-solve paired pricing of the exact unit-square transport of BC-232's retained n = 11 cutting
      state at side 96/25
    engine: devtools.price_cutting_state_dual at 82df41bd7154903d4048fed0feef39b8bec794f8
    engine_commit: 82df41bd7154903d4048fed0feef39b8bec794f8
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 64
      rounding: scipy linprog float64 for the LP proposal; raw duals retained with float.hex; support
        weights rounded to nearest on common denominator 10^9 using Python round
    tolerance: a row is selected only when its raw dual is strictly greater than 1e-9; no float comparison
      accepts a witness or a certificate
    host_system: Darwin 25.5.0 arm64; ten logical CPUs, one compute process, default solver threading,
      Python 3.14.7
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: paired32, the first 32 positive entries of the single full rationalised support in identical
      order; no second LP solve and no independently rationalised dual
    candidate: every row of the same raw LP dual above 1e-9 after the one common rationalisation; accept
      only an orbit absent from the transported state whose same representative has exact paired32 depth
      <= 1 and exact full depth > 1
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra, max; coordinator of session-111
    commit: 82df41bd7154903d4048fed0feef39b8bec794f8
    entry_point: packing/devtools/price_cutting_state_dual.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 30m .venv/bin/python3
      -m devtools.price_cutting_state_dual campaign/series/series-000-smoke-and-calibration/results/agenda-031/bc-306-unit-state-at-q.json
      --solved campaign/series/series-000-smoke-and-calibration/results/agenda-031/exp-134-solved-support.json
      --priced campaign/series/series-000-smoke-and-calibration/results/agenda-031/exp-134-paired-pricing.json
      --max-line-pairs 5000000
    budget: One pricing process with a 30-minute timeout and a two-second TERM grace, one LP solve and
      no candidate iterations. The dense LP matrix is 346.6 MiB; its negated copy and HiGHS workspace
      raise peak memory materially above 700 MiB. The host has ten logical CPUs; solver threading is default,
      not an enforced four-core allocation. The five-million line-pair guard is applied before intersection
      construction. The exact launch clock and process timing will be retained; the lease is ownership
      metadata, not permission to extend the process timeout.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/exp-134-paired-pricing.json
  results:
  - shape: determination
    role: guard
    question: Was the registered target invoked under its original live allocation?
    outcome: criterion_missed
    checked_by: Session111 records no LP or pricing invocation. The owner reprioritized BC309, and the
      unused operational lease expired at 2026-09-09T02:40Z. Scientific wall time is zero; preparation,
      validation and coordination remain in session usage.
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes:
    - treating an empty paired32 chosen list as proof that the full witness has paired32 depth at most
      one
    - constructing line intersections before enforcing the five-million pair guard
    - reporting a numerical LP or screen witness as exact without rational membership replay at the same
      absent-from-state orbit
    notes: Prospective allocation; no LP solve or pricing target has run. The instrument commit is 82df41bd;
      the actual runtime HEAD and dirty state will be captured at launch. The solved-support record is
      written before arrangement construction and contains every raw dual hex value and the full positive
      rationalised support. Both arms share that one sequence.
  verdict:
    decision: blocked
    primary_criterion: at least one full-arm new-site orbit, absent from the input state, with exact same-point
      paired32 depth <= 1 < full depth
    reason: No target was invoked. The owner prioritized BC-309 before this launch, and the unused lease
      expired at 02:40Z. The scientific protocol is retained unchanged; execution needs a fresh forward
      allocation. This is an administrative unrun disposition, not negative evidence about H-135.
  effort:
    timebox: One thirty-minute process with two-second grace; scientific allowance unspent
    wall_seconds: 0
    stopped_by: dependency
---
# exp-134 — Prospective Paired Pricing Round

The original allocation ended without a scientific invocation.
The owner selected the conditional-cover pilot instead; this administrative block is not
negative evidence about full-support pricing.
The original scientific contract below is retained, with its full process allowance
unspent and a fresh forward launch allocation required.

The published instrument is commit `82df41bd7154903d4048fed0feef39b8bec794f8`. Its
integrated controls and the publication check passed.
The exact state transport was replayed before this allocation: maximum depth one over
2,702,488 vertices, with 19,335 exact decisions and mass `21342289572/2055263195`. That
mass is below eleven; the expected K3 failure means this is a retained fractional
control, not a packing obstruction.
The control used 135.91 seconds wall, 125.64 seconds user CPU and 1.91 seconds system
CPU, separately from the prospective LP/pricing effort.

The transport retains the 181-direction net, rows and sites, uses scale `10000/9977` and
translation `(1396/249425,1396/249425)`, and is contained at `q = 96/25`. The complete
state and raw control receipts are in `results/agenda-031/`.

No LP solve or pricing target has run.
Publish this protocol before opening the one-process target phase.
The solved-support artifact is written before arrangement work.
Acceptance requires exact rational membership at the same full-arm witness,
`paired32 depth <= 1 < full depth`, and absence of its whole D4 orbit from the state.
A guarded or exhausted execution stays unresolved.
The round supplies no global packing or covering certificate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
