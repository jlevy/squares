---
title: exp-110 — fixed T-018 atoms reject a core-side reduction of 1/100000
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-110
  series: series-000
  title: Replay the frozen T-018 measure at core side 99769/100000
  date: '2026-09-06'
  hypotheses: [H-090]
  tier: confirmatory
  subject:
    label: Exact minimum net-core mass on the fixed T-018 atomic measure
    engine: devtools.core_shrink using the exact event-cell sweep
    engine_commit: 48a161ba570d053d054eb1942f6e315929c6250b
    assurance: verified
    method: exact-algebraic
    host_system: macOS 26.5.2 arm64, Python 3.14.7, two sweep workers
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: Full source replay at B=9977/10000 must reproduce minimum 4001/4000.
    candidate: Fixed atoms and weights at core side 99769/100000, dilation 100001/100000.
    runs_per_condition: 1
    interleaved: false
    operator: Codex endpoint_epsilon_spike, max reasoning, coordinator satellite think-zq2u
    commit: 48a161ba570d053d054eb1942f6e315929c6250b
    dirty: false
    entry_point: packing/devtools/core_shrink.py
    command: >-
      cd packing && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
      VECLIB_MAXIMUM_THREADS=1 uv run --frozen --all-extras --group dev python
      -m devtools.core_shrink cases/n11_fractional_certificate/certificate.json
      --square-side 99769/100000 --factor 100001/100000 --workers 2
      --output-dir campaign/series/series-000-smoke-and-calibration/results/exp-110-h-090-core-shrink
    budget: One frozen candidate, exact source and candidate replays, retention only on success.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-110-h-090-core-shrink/result.json
  effort:
    timebox: One source replay and one candidate replay
    wall_seconds: 29.864937
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Does m(99769/100000) strictly exceed 434547/440000?
    outcome: criterion_missed
    checked_by: >-
      Exact minimum 85353/100000 over all 181 directions, at direction zero and
      center (1849127/3706800,1849127/3706800); a direct closed-core atom sum at
      that admissible center reproduces the minimum.
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
      The candidate minimum is below the required threshold by 294969/2200000,
      so rescaling these weights cannot certify the proposed side 3.8100381.
    commit: 48a161ba570d053d054eb1942f6e315929c6250b
    reopen_when: A separately registered smaller reduction, or a change of sites or relative weights.
---
# exp-110 — A Corner Event Rejects the First Core Shrink

The first core shrink fails.
The [raw receipt](../results/exp-110-h-090-core-shrink/result.json) records
$m(99769/100000)=85353/100000=0.85353$, below $M/11=434547/440000\approx0.98760681818$.
No candidate certificate was emitted, and the production retention gate and standalone
verifier had no candidate to decide.
T-022 remains the retained lower bound.

The exact source replay took 14.846608 seconds; the candidate replay, including a
separate sweep of the worst direction and direct atom summation at its witness, took
14.957827 seconds. The full invocation ran from 11:14:26.226943Z to 11:14:56.091880Z on
2026-09-06. The raw command records the actual interpreter and isolated checkout paths;
the command above uses the repository’s portable invocation.

## The Obstruction Is a Narrow Event, Not Every Smaller Core

The worst direction is axis aligned.
Put $e=1849127/1853400\approx0.9976945074$. The witness center is $(e/2,e/2)$, and a
core at this center is admissible for every positive side $b\le e$. The receipt gives
the complete sorted inclusion-event spectrum at this center.
Its last event below $e$ is $1565797464121/1570613788200$; the next event is exactly
$e$, where the covered mass increases by $917/6250$. The total mass from all preceding
events is $85353/100000$. Thus every $b<e$ has a concrete admissible placement of mass
at most $85353/100000$, which rejects normalization of these fixed weights throughout
that range. At $e$ the mass at this witness becomes exactly $4001/4000$.

The range $e\le b<9977/10000$ remains unresolved.
Its width is exactly $509/92670000$. The experiment therefore identifies a necessary
core size for this measure; it does not establish that the source side is critical or
rule out every positive shrink.

## Why the Acceptance Rule Allows Mass Below One

For fixed atoms and net, let $m(b)$ be the minimum mass over all admissible side-$b$
cores in the fixed container.
If $m(b)>M/n$, replacing each weight $w_i$ with $w_i/m(b)$ makes the minimum one and the
total strictly less than $n$. Any rational dilation $q$ satisfying $qb(1+D)<1$ then
gives an ordinary certificate at side $qL$. The proposed $q=100001/100000$ satisfies the
containment inequality, and $qL=38100381/10000000$ exceeds T-022’s endpoint by more than
$1/100000$. Coverage is the failed premise.

The function $m(b)$ is nondecreasing: if $b_1<b_2$, every center admissible for the
larger core also admits the smaller core, and the smaller core is contained in the
larger one. Taking minima gives $m(b_1)\le m(b_2)$. It need not be continuous.
Even an equally spaced one-dimensional atomic measure can cover every closed interval of
the lattice spacing with positive mass while slightly shorter intervals fit between
atoms and have zero mass.
A coverage margin alone supplies no geometric perturbation radius.

## Exact Critical Events for a Further Size Search

At a retained rational direction $(c,s)$, rotate centers to $(U,V)$ and atoms to
$(u_i,v_i)$. The coverage-event lines are $U=u_i\pm b/2$ and $V=v_i\pm b/2$. The
admissible-center lines are $cU-sV=b(c+s)/2$, $cU-sV=L-b(c+s)/2$, $sU+cV=b(c+s)/2$, and
$sU+cV=L-b(c+s)/2$. Each line has the form $aU+dV+f+gb=0$ with rational coefficients.

Changes in the arrangement occur only at parallel-line coincidences or vanishing
three-line determinants.
The determinant is affine in $b$, so every isolated critical value is rational.
The familiar event-order changes $b=|u_i-u_j|$ and $b=|v_i-v_j|$ are included.
Identically zero determinants represent persistent coincidences and do not supply
isolated critical values.
Between consecutive critical values, the cell incidence and its mass labels are
constant.

For a complete test immediately below a proposed side $B=p/r$, clear denominators on
every line and let $H\ge1$ bound the absolute integer coefficients.
The numerator and slope of each three-line determinant have magnitude at most $6H^3$;
the parallel-coincidence equations obey the same bound.
Every distinct critical value is at least $1/(6rH^3)$ from $B$. Consequently a replay at
$B-\min(B/2,1/(12rH^3))$ decides the immediate left-hand arrangement, including the case
where $B$ itself is critical.
This finite bound is a proof plan; this experiment implements the single-side replay and
the complete inclusion events at its witness, not that global arrangement search.

## Verification and Next Slice

Five focused tests pass, including normalization of a genuine below-one minimum through
both production decision routes, refusal of wrong-$n$, duplicate-key and
stale-declaration sources, failure-witness retention, containment refusal, and a direct
atom-sum regression of the exact corner obstruction.
Ruff and BasedPyright report zero findings.
The coordinator’s document-map correction has been integrated into the isolated
checkout. The synopsis carries the new hypothesis, round and cost totals.

A separate hypothesis should test a rational side above $e$ before investing in a
complete critical-arrangement enumerator.
The rejected point and its original acceptance rule remain frozen as H-090.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
