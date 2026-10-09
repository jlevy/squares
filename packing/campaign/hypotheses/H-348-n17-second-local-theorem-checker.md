---
title: H-348 — a second, LP-free checker reproduces the local theorem's certificates and refuses mutants
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-348
  kind: hypothesis
  claim: >-
    An independent checker of the local family theorem's fixed certificate data (the
    52-row roster, 45 coordinate lifts, slider-cell cover, dyadic duals, root enclosure,
    curvature constants and radius vectors), written without importing the standing
    local-minimum or local-radius checkers and using exact rational arithmetic without
    LP, reproduces the four retained cases: uniform 1/5000 on B_W (93 cells, worst
    ratio 0.925818092269), uniform 1/5000 on B_W' (93, 0.925931049178), the anisotropic
    uniform-floor 1/1216 vector on B_c (109, 0.999316555505), and the distinct
    capture-form vector on B_c (117, 0.999368209930; ordinary angle radius 1/1024,
    minimum position radius 11/32768). It preserves whole-cell quadratic residual
    bounds and refuses at least 20 deliberately invalid certificates with named reasons.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      For each fixed replay case: its certificate data, exact radius vector and slider
      box, per-coordinate residual components, root-box allowance, dual nonnegativity,
      curvature mass, denominator and exact rational ratio; cell tiling and the four
      retained cell counts and displayed worst ratios. Record the refusal reason for
      each invalid mutant and exact agreement of every bound with the standing fixed
      replay, without generating replacement duals or cells.
    direction: >-
      Confirm when all four fixed replay cases agree in their exact rational bounds
      and retained displayed ratios and cell counts, all whole-cell residual and recipe
      obligations pass, and at least 20 predeclared invalid mutants are refused. A
      disagreement refutes parity until its cause is resolved; acceptance of an invalid
      mutant refutes the refusal claim. A fresh LP-generated proposal passing the
      standing tool is not an independent replay of the retained certificate data.
    threshold: 4 of 4 fixed cases exact; 93/93/109/117 cells; whole-cell residual bounds; at least 20 invalid mutants refused.
  instrument: >-
    Unbuilt: a separately written checker in another language or Python module sharing
    no implementation with the standing checkers, reading exp-244, exp-248 run-002,
    ratio-composition-1216-certificates.json and ratio-composition-capture-certificates.json
    with each case's receipt and exact vector. Reconstruct affine matrix and dual
    products, bound their quadratic residual throughout each cell including root-box
    error, check tiling and the remaining recipe obligations, and run a predeclared
    invalid-certificate mutation suite.
  instrument_ready: false
  regime: >-
    n = 17; fixed retained local certificate data, not regenerated proposals; B_W =
    [0, 1/4] x [0, 1/12] x [-1/8, 1/16], B_W' with the b floor widened to -1/2500,
    and B_c = [0, 4/25] x [-1/128, 11/100] x [-13/200, 1/30]; each exact radius vector
    from its own receipt; exact rational arithmetic; hand lemmas taken as given.
  instance: {axis: n, point: 17}
  priority: 3
  cost_estimate: 20 to 30 agent-hours to build and review; seconds to run.
  prereqs: [H-261, H-268, H-340]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 6, the local half of two-verifier parity (H-335 covers the kernel
    format). Correction of 9 October following review C9: the 109-cell vector has
    minimum radius 1/1216 and maximum 85/19456; the 117-cell capture-form vector has
    minimum radius 11/32768 and maximum 249/65536. Its position floor is the
    upward-rounded 1/3072 proposal, smaller than 1/1216. These are distinct replay
    cases. The review's fresh proposal runs and internal exact checks corroborate the
    standing recipe but are neither fixed-data replays nor second implementations.
    The independent checker must preserve the quadratic residual bound on the whole
    cell; an affine dual times an affine matrix is quadratic, so vertex checks alone
    do not suffice. This is a replication proposal and makes no new admission claim.
---
# H-348: Two Checkers for the Local Half

**Mechanism.** Replay four fixed certificate cases, binding each to its slider box and
radius vector:

| Case | Slider box | Radius vector | Cells | Retained worst ratio |
| --- | --- | --- | ---: | ---: |
| exp-244 | $B_W$ | uniform $1/5000$ | 93 | 0.925818092269 |
| exp-248 run-002 | $B_W'$ | uniform $1/5000$ | 93 | 0.925931049178 |
| uniform-floor composition | $B_c$ | minimum $1/1216$, maximum $85/19456$ | 109 | 0.999316555505 |
| capture-form composition | $B_c$ | ordinary angles $1/1024$, minimum positions $11/32768$, maximum $249/65536$ | 117 | 0.999368209930 |

The two composition vectors are the exact named-coordinate vectors in
[ratio-composition-1216.json](../explorations/X048-session-168-pilots/receipts/local-radius/ratio-composition-1216.json)
and
[ratio-composition-capture.json](../explorations/X048-session-168-pilots/receipts/local-radius/ratio-composition-capture.json).
The capture-form case cannot establish a uniform $1/1216$ floor.

For a cell centred at $c$, write $\delta=w-c$ with $|\delta_k|\le W_k$,
$A(w)=A_c+\sum_k\delta_k A_k$ and $\lambda(w)=\lambda_0+\sum_k\delta_k\mu_k$. The
residual for signed coordinate $j$ is

$$
\lambda(w)^{\mathsf T}A(w)+s e_j
=r_0+\sum_k\delta_k r_k+\sum_{k,l}\delta_k\delta_l q_{kl},
$$

where $r_0=\lambda_0^{\mathsf T}A_c+s e_j$,
$r_k=\mu_k^{\mathsf T}A_c+\lambda_0^{\mathsf T}A_k$ and $q_{kl}=\mu_k^{\mathsf T}A_l$.
Reproduce the whole-cell bound

$$
\varepsilon_j=\|r_0\|_1+\sum_k W_k\|r_k\|_1
+\sum_{k,l}W_kW_l\|q_{kl}\|_1+\varepsilon_{\rm root}.
$$

Vertex checks suffice for affine dual nonnegativity and affine curvature mass, with the
recipe’s root-box allowance added; they do not bound the quadratic residual by
themselves. The checker must verify rank, coordinate lifts, roster, sign branches, cell
tiling, curvature bounds and the ratio $M_j/(2(r_j-\varepsilon_j R))<1$ with a positive
denominator throughout the cell, where $R=\max_j r_j$. It reads the retained cells and
duals without solving a new LP.

**Falsifier.** A disagreement on any fixed exact replay bound or an accepted invalid
mutant.
Mutations must be chosen to violate a specified obligation, including an interior
residual failure that vertex-only checking would miss; merely changing data that remains
valid is not a refusal control.

**Expected information.** Whether the local half’s fixed certificates have matching
checks from two independent implementations.

**Limits.** The hand lemmas and curvature formula remain shared premises; H-333 is where
they stop being hand lemmas.
Replay parity validates these fixed instances and does not establish outer capture or
change the admitted bracket.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
