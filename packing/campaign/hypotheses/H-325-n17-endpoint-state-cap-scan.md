---
title: H-325 — the endpoint's own occupancy state is excluded at a cap one hundredth below S*
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-325
  kind: hypothesis
  claim: >-
    In the centred container at cap V = S* - 1/100 (walls at (U - V)/2 and (U + V)/2
    with the H-266 cells kept in the U frame), the whole-state ownership-induction
    kernel under the SW9 adaptive-row recipe, or the interval branch and bound within
    10^6 nodes, certifies that no packing of 17 unit squares of side at most V has the
    family's own occupancy state; and the certificate passes the standing verifier in
    full mode.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      For each cap in the scan, S* - V in {2, 5, 10, 15} x 10^-3, the producer outcome
      (closed, stalled, time cap), the finest live row, the number of rows live at the
      end, and the standing verifier's full-mode verdict; for the branch and bound, the
      node count and the leaf outcomes.
    direction: >-
      Confirm when the family's state closes at S* - V = 1/100 under either engine and
      the standing verifier passes the certificate in full. A closure only at wider
      margins records the measured reach V_max and refutes the stated cap. A stall at
      every cap, including 1.5e-2, refutes the claim and would suggest that the
      per-state engines need a side margin above 1.5e-2 to act. It would not show that
      the hard tail cannot close at caps at least S*: a distance-2 state's margin there
      is its own minimal side minus the cap, which is unmeasured.
    threshold: >-
      Closure at S* - V <= 1/100 with a full-mode verifier pass; the kernel recipe is
      64 bins, octagon core, adaptive rows with floor 1/512 and cap 2,304 rows, 48
      rounds, 7,000 s; the branch and bound stops at 10^6 nodes.
  instrument: >-
    The centred-cap producer path of devtools/pilot_n17_capture.py (the exp-280 standing
    control ran the family's state at cap V' = 935106018721/200000000000 with centred
    walls and hull allowance 48) with the cap set below the root enclosure, or
    devtools/check_n17_subpattern.py on all 17 cells once it takes a centred cap; the
    branch and bound through devtools/pilot_n17_subpattern_bb.py at the same cap;
    closures re-proved by devtools/verify_n17_kernel_certificate.py and
    devtools/verify_n17_bb_certificate.py in full mode.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 unique-state cover at U = 1169/250 in the U frame; the family's
    state only; caps V = S* - delta with delta in {2, 5, 10, 15} x 10^-3, each as an exact
    rational below the H-255 root box; one run per cap and engine, frozen before the
    first launch; the endpoint's exact pose is not retained at any of these caps, which
    is the point.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    At most eight runs of at most 7,000 s producer plus about 4,000 s verification each;
    4 to 8 CPU-hours on two workers; about four agent-hours to confirm that the producer
    accepts a cap below the root and to register the frozen caps.
  prereqs: [H-266, H-288]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's first selection. The scan measures the one quantity the record never
    measured: the side margin at which pure exclusion stops reaching the endpoint's own
    state, which is the hardest state for every engine because it is feasible at every
    cap at least S*. The result prices the cap ladder (H-326) and sets the inner edge of
    the no-man's-land that capture must bridge (H-330). Certificates at these caps do not
    enter the optimality proof, whose exclusions need caps at least S*.
---
# H-325: The Endpoint State at Caps Below the Root

**Mechanism.** Below $S^\ast$ the family’s own state is infeasible, with a side margin
$S^\ast-V$ spread along its wall-to-wall contact chains.
The kernel’s first-order losses at its finest rows are about $10^{-3}$ per square
(envelope core $0.00097$ at $1/512$, wall rows up to $0.00195$), and the branch and
bound closes nodes whose outward-rounded dual bound exceeds the cap.
Whether either engine sees a margin of $10^{-2}$ in side on this state is unknown; the
per-state closures of 5 October had float penetrations of $0.012$ to $0.055$ and the
distance-2 states, at $0.0115$ to $0.012$, stalled.

**Falsifier.** A stall at every cap in the scan, including $S^\ast-V=1.5\times10^{-2}$,
under the 2,304-row recipe and $10^6$ nodes.

**Expected information.** The exclusion-reach margin $V_{\max}$. Closure at $10^{-2}$
makes the cap ladder worth a verified bound.
A stall at $1.5\times10^{-2}$ would suggest that the per-state engines need a larger
side margin than that to act.
It would not show that the hard tail cannot close at $U'$, because a distance-2 state’s
margin at $U'$ is its own minimal side minus $U'$, which nobody has measured and which
may exceed $1.5\times10^{-2}$.

**Limits.** One state.
Reach on the family’s state bounds the reach on the distance-2 states from above only if
their margins at a common cap are no larger, which the scan does not establish; a
control on the tail states themselves, such as H-326’s stratified pilot, is needed
before a stall here routes effort away from per-state methods.
The producer’s acceptance of a cap below the root box is a one-line condition to confirm
before registration of the frozen caps; no run is launched by this record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
