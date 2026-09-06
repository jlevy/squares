---
title: exp-111 — an interior witness excludes every ordinary-containment core gain
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-111
  series: series-000
  title: Replay the frozen T-018 measure above the lost corner event
  date: '2026-09-06'
  hypotheses: [H-091]
  tier: confirmatory
  subject:
    label: Exact minimum net-core mass on the fixed T-018 atomic measure
    engine: devtools.core_shrink using the exact event-cell sweep
    engine_commit: aeb683d5e02913504af663aa39e42f577e19a346
    assurance: verified
    method: exact-algebraic
    host_system: macOS 26.5.2 arm64, Python 3.14.7, two sweep workers
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: Full source replay at B=9977/10000 must reproduce minimum 4001/4000.
    candidate: Fixed atoms and weights at core side 997696/1000000, dilation 1000007/1000000.
    runs_per_condition: 1
    interleaved: false
    operator: Codex endpoint_epsilon_spike, max reasoning, coordinator satellite think-jthr
    commit: aeb683d5e02913504af663aa39e42f577e19a346
    dirty: false
    entry_point: packing/devtools/core_shrink.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
      VECLIB_MAXIMUM_THREADS=1 uv run --frozen --all-extras --group dev python
      -m devtools.core_shrink cases/n11_fractional_certificate/certificate.json
      --square-side 997696/1000000 --factor 1000007/1000000 --workers 2
      --output-dir campaign/series/series-000-smoke-and-calibration/results/exp-111-h-091-core-shrink
    budget: One frozen candidate, exact source and candidate replays, retention only on success.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-111-h-091-core-shrink/result.json
  effort:
    timebox: One source replay and one candidate replay
    wall_seconds: 30.584645
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Does m(997696/1000000) strictly exceed 434547/440000?
    outcome: criterion_missed
    checked_by: >-
      Exact minimum 96377/100000 over all 181 directions, at zero-based direction
      index 97. The raw receipt retains the admissible rational center and complete
      inclusion-event spectrum; direct closed-core atom summation reproduces the minimum.
  - shape: determination
    role: guard
    question: Does a fresh source replay reproduce the frozen T-018 declarations?
    outcome: criterion_met
    checked_by: >-
      Conditions 1 through 5 pass on the exact bytes whose SHA-256 is
      b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a;
      total mass 434547/40000 and minimum 4001/4000 agree with the declarations.
  verdict:
    decision: rejected
    primary_criterion: Exact minimum strictly greater than total mass divided by eleven.
    reason: >-
      The candidate minimum is below the threshold by 52441/2200000. Its interior
      witness also excludes every core side that could beat T-022 through ordinary
      containment while retaining these sites and relative weights.
    commit: aeb683d5e02913504af663aa39e42f577e19a346
    reopen_when: A separately registered refined-containment route or changed sites, net or relative weights.
---
# exp-111 — An Interior Witness Closes the Ordinary Shrink Route

The second fixed-atom core shrink fails.
The [frozen receipt](../results/exp-111-h-091-core-shrink/result.json) gives
$m(997696/1000000)=96377/100000=0.96377$, below $M/11=434547/440000$ by $52441/2200000$.
No candidate certificate was emitted, so there was no candidate for the production
retention gate or standalone verifier to decide.
Neither T-018 nor T-022 changes.

H-091 was committed as `210991ad` before this point was measured.
The run used clean commit `aeb683d5`, which adds only a synopsis wording correction.
It ran from 11:31:11.672807Z to 11:31:42.257452Z on 2026-09-06. The source replay took
15.128362 seconds; the smaller-core replay, including a repeated sweep of its worst
direction and direct atom sum, took 15.403501 seconds.
The raw receipt preserves the actual interpreter, checkout, command and tool digest.

## The Recovery Event

The worst placement uses zero-based net direction 97 and an interior center, not
exp-110’s corner center.
For this fixed center $(U,V)$ in coordinates rotated to that direction, atom $i$ enters
the closed core exactly at side $2\max(|u_i-U|,|v_i-V|)$. The receipt retains these
rational sides with their added masses and the exact center in both coordinate systems.

The first inclusion event at which this witness exceeds $M/11$ is

$$
e_{97}=\frac{1696802860582378979}{1700716629721128200}.
$$

Its mass immediately below this event is $96377/100000$. At the event, mass
$25257/200000$ enters, giving $218011/200000$. The center admits every positive core
side through

$$
a=\frac{17137540266205342633239451929256187973}
{8490057146508782661010155026357102600}>e_{97}.
$$

Thus every $0<b<e_{97}$ has an admissible core of mass at most $96377/100000$. No
normalization of these fixed weights can certify such a core side: its exact minimum
cannot exceed this witness mass, which is below $M/11$. This conclusion uses a single
placement and nonnegative weights; it does not require a sweep at any unmeasured side.

## Why This Excludes the Entire Ordinary-Containment Window

Write $B=9977/10000$ and $D=207107/90000000$ for the source core side and largest
half-gap tangent. T-022’s endpoint is $S_*=L\sqrt{1+D^2}/(B(1+D))$. For a smaller core
$b$ and dilation $q$ to improve it using ordinary containment, both $qL>S_*$ and
$qb(1+D)<1$ must hold.
Combining these strict inequalities requires

$$
b<\frac{B}{\sqrt{1+D^2}}.
$$

But the exact witness event satisfies

$$
e_{97}^2-\frac{B^2}{1+D^2}
=\frac{65196331602516217274491708275075416012593285009}
{23428864208538589123227153839724949707492304182760000}>0.
$$

Every core in the ordinary-containment improvement window is therefore below $e_{97}$
and rejected by this witness.
This is a whole-window obstruction for fixed sites, fixed net and fixed relative
weights, not just a negative result at two sampled points.
The proposed side $381002667/100000000$ does exceed T-022 algebraically; the failed
coverage premise prevents obtaining that bound.

## Replay and Disposition

The reusable witness-inspection mode hashes the frozen source, reconstructs every
inclusion event from its atoms, requires the entire spectrum and witness fields to match
the receipt, and computes the first mass-recovering event and the exact ordinary-window
comparison. It does not infer a global minimum from this one placement.
Run it without launching another sweep:

```bash
cd packing
uv run --frozen --all-extras --group dev python -m devtools.core_shrink \
  cases/n11_fractional_certificate/certificate.json \
  --inspect-witness campaign/series/series-000-smoke-and-calibration/results/exp-111-h-091-core-shrink/result.json
```

Seven focused tests pass, including both retained witnesses’ recovery events,
source-byte and witness-mass mutation refusals, and a small positive normalization that
passes both production routes with an original minimum below one.
Ruff and BasedPyright report zero findings.
The records tier passes all 31 selected steps in 15.15 seconds, including the experiment
schema, generated ledger, synopsis totals and mutation anchors.
This scoped checkpoint is not the full integration gate.

The two registered measurements are complete; no third experiment was run.
Refined containment on a smaller, successfully normalized source core is a distinct
route not excluded here.
It would need a new preregistration, an exact mass replay at a side above this
obstruction, and the refined-limit proof and retention checks.
Changing sites, the net or relative weights also falls outside this obstruction.
The coordinator can price those alternatives against the released research lanes without
repeating either frozen negative.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
