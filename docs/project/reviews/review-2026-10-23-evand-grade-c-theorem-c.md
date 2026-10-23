# Evan Daniel’s Grade-C Local Minima (Theorem C): Mathematical Review

**Verdict: Theorem C is true under its hypotheses as `gradec.py` checks them.
The paper proof has one gap, at the rows whose corner sits at a side end, which this
review repairs without changing a check, and hypothesis 2 should state a limit that the
certificate supplies (C-6).** With the repair, every one of the 233 VALID verdicts rests
on a complete argument.
A checker written here from the theorem, sharing no code with the source, decided all
233 configurations again in exact arithmetic, including that each record is a packing,
which `gradec.py` does not check, and it agrees with every published certificate on
every quantity that does not depend on a choice of basis or multipliers.

The source is Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing): Theorem C and its proof
in `tasks/exact-minpoly/grade-C.md` and the checker `search/exact/gradec.py`, both
retained at `ad86d42` in
[evand-exact-and-local-reports-2026-10-12](../../../packing/resources/web/evand-exact-and-local-reports-2026-10-12/README.md),
and the release `exact-data-2026-10-12` (tag commit `31523f8`) with the 233
certificates, retained in
[evand-exact-data-2026-10-12](../../../packing/resources/web/evand-exact-data-2026-10-12/README.md).
The claim is the source’s: 233 of the 250 roster configurations of field degree at most
4 are local minima of the side in the sense of `IsLocalMinPacking` (squares matched by
index, angles modulo 90 degrees), 231 with every load-bearing incidence as a row and 230
and 261 after 24 rows that carry no force are dropped.
No `T-NNN` on `main` holds this claim; the nearest is `T-124`, the same author’s
reported non-strict local minima for 178 configurations by a different route, Lean
proofs.

One finding is major (the gap, C-1), five are minor and seven are notes.
None is blocking.

Reviewer: Claude (Anthropic), strong sub-agent tier (`tbd-strong-max`), maximum
reasoning (acting name `c-review-thmc-1023`, bead `think-7scz`), the mathematical lane
of the #545 import at stage 4, in a worktree of its own.
It read the source as data and ran only code it wrote, kept in the packet under
[`review/`](../../../packing/resources/web/evand-exact-data-2026-10-12/review/README.md).
No earlier review of this result exists: a search of `docs/project/` by file name and by
the term `gradec` before writing found none (section Comparison).
It is not a human oversight record.

## Summary for the Author

- **The theorem holds.** Hypotheses 1 to 3, as `gradec.py` checks them, imply, for a
  record that is a packing, that it is a local minimum of the side (The Proof,
  Repaired).
- **The proof needs one more step at side-end rows (C-1).** The last line,
  $S(z) - S^\ast
  \ge (\kappa/4)|\Delta|^2 - O(|\Delta|^3)$, drops $\sum_r \lambda_r(m) h_r(z)$, which
  is nonnegative for interior and wall rows but only $\ge -K'\delta^2$ for side-end
  rows, the same order as the coercive term.
  And the bound $h_r \ge -K'|\Delta|^2$ the second bullet uses is measured from $m$,
  while the relaxation measures from $z^\ast$; where the flat family slides an aligned
  pair along its side, the slack the relaxation allows relative to $m$ is first order in
  $|\Delta|$. At n = 19, 16 of the 24 side-end rows slip along the family.
  The repair uses the pair: the edge argument you give shows that one row of a side-end
  pair is at least $-C\varepsilon$ times the other, and a bootstrap then makes every row
  $O(|\Delta|^2)$ and the slack $O(\varepsilon |\Delta|^2)$, which the Hessian absorbs.
- **Every hypothesis `gradec.py` assumes is listed below** (What gradec.py Checks).
  Two premises are outside it: that the record is a packing, which your
  `verify_exact.py` checks (C-2), and that the stated $t$ interval brackets a root of
  $f$ (C-3). Hypothesis 2 should also say that the multipliers tend to $\lambda^\ast$
  along the family: the coercivity step uses it, and your affine null vectors supply it
  (C-6).
- **The certificate files are summaries (C-4).** They give counts, dimensions and float
  values, not $\lambda^\ast$, the flat basis, the affine null vectors or $W$, so
  checking one means redoing the search.
- **Hypothesis 2 has a much smaller certificate.** Each $A_k$ acts on a contact row only
  through that row’s tangential slip and the angle of the square that owns the side, so
  the quadratic identities say that the lifts vanish at those angles, and the affine
  null vectors come from one linear system per null vector and flat direction (The Slip
  Form). With that and an $LDL^\mathsf{T}$ for the Hessian, our checker took a median of
  about one CPU-second per configuration and 24 CPU-minutes for all 233, the longest
  being n = 294 ($\dim W = 11$) at 369 seconds; both walls your 17 timeouts hit are
  algorithmic.
- **Independent check.** The checker written here decided all 233 VALID, with the same
  rows, ranks, flat families, dimensions of $W$ and moving squares as your certificates,
  margins equal to the last float digit and least multipliers within
  $2.1 \times 10^{-9}$ relative.

## Scope and Evidence

Read, as data, in this order: `grade-C.md` (138 lines), the definition
`IsLocalMinPacking` and the lemmas around it in `lean/Sqpack/LocalMin.lean` (retained in
the `evand-exact-and-local-reports-2026-10-07` packet), `gradec.py` with the three
modules it imports (`localmin.py`, `verify_exact.py`, `geom.py`), `env.sh`,
`gradec_runs/run.sh` and both status files, the release README, and from the archive
`gradec-233.tar.zst` the contacts, certificates and logs.
The archive is retained as published and was read in memory.
The 233 exact forms `gradec.py` reads, `search/exact/minpoly/data/n-N.minpoly.json.gz`,
were fetched by Git blob from the tag commit `31523f8`, each blob hash checked against
the commit’s tree, and are now retained in the exact-data packet as their upstream gzip
files; three of them (10, 230, 261) were already retained and match by SHA-256.

The claim reviewed is grade-C.md’s Theorem C and the batch’s 233 VALID verdicts.
Nothing here reviews `T-124`’s Lean proofs, the 17 timeouts, the configurations of field
degree above 4, or whether a configuration is the one its case record holds now.

## The Claim and the Notion

`IsLocalMinPacking n S c θ` (LocalMin.lean lines 30 to 34) holds when the record
$(c, \theta)$ is a packing in $[0, S]^2$ and some $\varepsilon > 0$ is such that every
packing $(s, c', \theta')$ with $|c'_i - c_i| < \varepsilon$ in each coordinate and
$\theta'_i$ within $\varepsilon$ of $\theta_i$ modulo $\pi/2$, square $i$ matched to
square $i$, has $S \le s$. It is non-strict, the side $s$ is not in the ball, and a
quarter turn leaves a unit square unchanged (lines 45 to 59), so each angle can be taken
in its representative within $\varepsilon$. The notion is weak in a way the source
states: a broad plateau with a far downhill exit satisfies it
(tasks/exact-minpoly/README.md, of s(7)’s arrangements).
At a count whose value is proved, it is implied by the value, since no packing has a
smaller side.

## Theorem C Re-derived

### Setting

Square $i$ has centre $c_i = (x_i, y_i)$, angle $\theta_i$, frame $u_i = (\cos\theta_i,
\sin\theta_i)$, $v_i = J u_i$ with $J(x, y) = (-y, x)$; corner $a$ is
$c_i + \frac12(\sigma_a
u_i + \rho_a v_i)$ with $(\sigma_a, \rho_a) = (1,1), (-1,1), (-1,-1), (1,-1)$, and side
$k$ has outward normal $n_{ik} = R(\theta_i) e_k$, $e_k = (1,0), (0,1), (-1,0), (0,-1)$.
The coordinates are $z = (x_i, y_i, \delta_i)_{i \in B}$ and $S$, for the load-bearing
squares $B$, with $\delta_i$ the change of angle; the source uses $w_i = \sin\delta_i$
(grade-C.md line 10), and the two give the same first and second derivatives on the flat
family, where $\delta = 0$ (note N-3). Removing the squares that carry no force is sound
(lines 8 and 9): a packing of the $n$ squares near the record restricts to a packing of
$B$ near the record’s restriction.

A row is a function $h_r$, tight at $z^\ast$ and affine in the centres at fixed angles:
a wall row, the coordinate of a corner of $j$ measured from a wall ($x$, $y$, $S - x$ or
$S - y$); or a contact row, $h_r = n_{ik} \cdot (P_{ja} - c_i) - \frac12$ for corner $a$
of $j$ on the line of side $k$ of $i$, with $\tau_r = n_{i,k+1} \cdot (P_{ja} - c_i)$
its position along the side.
$L = \nabla h(z^\ast)$, and $L(z)$ is the Jacobian at $z$.

### The three kinds of row and why each is valid

Let $z$ be a packing within $\varepsilon$ of $z^\ast$.

- **Wall rows.** $h_r(z) \ge 0$: the corner is inside the container.

- **Interior incidences** ($|\tau_r^\ast| < \frac12$). The corner of $j$ is not in the
  open square $i$, and near $z^\ast$ the values of sides $k+1$, $k+2$ and $k+3$ of $i$
  at it stay below $\frac12$, so $h_r(z) \ge 0$ (grade-C.md lines 18 and 19;
  LocalMin.lean’s `sideVal_ge_of_disjoint`).

- **Side-end pairs.** Two adjacent corners $a_1, a_2$ of $j$ on side $k$ of $i$, both
  tight and at $\tau^\ast = \mp \frac12$, so that the edge of $j$ is the side of $i$.
  `gradec.py` keeps a side-end incidence only as such a pair (lines 176 to 190); a lone
  one is dropped, which only relaxes.
  For $s \in [0, 1]$ let $P(s) = (1-s) P_{a_1} + s P_{a_2}$ and $v(s) = n_{ik} \cdot
  (P(s) - c_i) - \frac12$. Then $v$ is affine, $v(0) = h_{r_1}$ and $v(1) = h_{r_2}$,
  and $\tau(s)$, also affine, stays within $C\varepsilon$ of $s - \frac12$. For $s \in
  (C\varepsilon, 1 - C\varepsilon)$ the point $P(s)$ projects strictly inside the side,
  so $v(s) \ge 0$ (lines 20 to 23). Taking $s_1 = 2C\varepsilon$:

  $$
  (1 - s_1) h_{r_1}(z) + s_1 h_{r_2}(z) \ge 0, \quad\text{so}\quad
  h_{r_1}(z) \ge -4C\varepsilon\, |h_{r_2}(z)|,
  $$

  and likewise $h_{r_2}(z) \ge -4C\varepsilon\, |h_{r_1}(z)|$ for $\varepsilon$ small.
  This is the **pair form** of the relaxation.
  It is what the second-order argument needs; the source states the weaker
  $h_r \ge -K'\delta^2$ (line 23).

### The flat family

$F$ is the set of position directions $\varphi$ with $L_r \varphi = 0$ for every row
(grade-C.md lines 35 to 37). Because each $h_r$ is affine in the centres at fixed
angles, $h_r(z^\ast + \varphi) = 0$ exactly, and $S$ does not change: $M = z^\ast + F$
is an exact family of points with every row tight.
Only the lever arms change along $M$, so the Jacobian at $z^\ast + \varphi$ is
$L_0 + \sum_k \varphi_k A_k$, with $A_k$ supported on the angle columns.
Hypothesis 3 needs all of $F$: a flat direction left out of it would lie in $W$, where
the Hessian vanishes on it, since rows are affine in the centres.

### Theorem C

Hypotheses (grade-C.md lines 42 to 48), with the record a packing (C-2):

1. every row is a wall row, an interior incidence or one of a side-end pair, tight at
   $z^\ast$;
2. for every $m \in M$ near $z^\ast$ there are multipliers
   $\lambda(m) \ge \lambda_0 > 0$, $\sum_r \lambda_r(m) \le \Lambda$, with
   $\sum_r \lambda_r(m) L_r(m) = e_S$ and $\lambda(m) \to \lambda^\ast$ as
   $m \to z^\ast$, which the source leaves implicit (C-6);
3. with $W = \operatorname{null} L \cap F^\perp$, the reduced Hessian $Q =
   \nabla^2\mathcal{L}^\ast(z^\ast)|_W$, $\mathcal{L}^\ast = S - \sum_r \lambda^\ast_r
   h_r$, is positive definite, $\zeta^\mathsf{T} Q \zeta \ge \kappa |\zeta|^2$.

Then the record is a local minimum of the side in the sense of `IsLocalMinPacking`.

### The proof, repaired

Let $z$ be a packing within $\varepsilon$ of $z^\ast$ with $S(z) < S^\ast$; nothing is
lost by bounding $s$, since a right or top wall row exists ($e_S$ lies in the cone of
the rows) and so $s \ge S^\ast - C\varepsilon$ (note N-4). Let $m$ be the point of $M$
nearest $z$ and $\Delta = z - m \perp F$, $|\Delta| < \varepsilon$.

(i) **Expansion at $m$** (grade-C.md lines 55 and 56). With $\mathcal{L}_m = S - \sum_r
\lambda_r(m) h_r$, stationary at $m$ by hypothesis 2, and
$H_m = \nabla^2 \mathcal{L}_m(m)$:

$$
S(z) - S^\ast = \sum_r \lambda_r(m)\, h_r(z) + \tfrac12 \Delta^\mathsf{T} H_m \Delta + R,
\qquad |R| \le C_3 |\Delta|^3 .
$$

(ii) **Every row is $O(|\Delta|^2)$.** This is the step the source takes from $h_r \ge
-K'|\Delta|^2$ (line 57), a bound the relaxation does not give (C-1). Let $X = \max_r
|h_r(z)|$. The negative part of every row is at most $4C\varepsilon X$: zero for wall
and interior rows, and by the pair form for side-end rows.
From (i) and $S(z) < S^\ast$, $\sum_r \lambda_r h_r(z) < C_2 |\Delta|^2$, so for each
row $\lambda_0 h_r^+ \le
4\Lambda C\varepsilon X + C_2 |\Delta|^2$. For
$\varepsilon \le \lambda_0 / (8 \Lambda C)$ and $4 C \varepsilon \le \frac12$ this gives
$X \le 2 C_2 |\Delta|^2 / \lambda_0$.

(iii) **The normal part is small** (lines 57 to 60, unchanged).
Since $h_r(m) = 0$, $|L(m)\Delta| \le X + C_4|\Delta|^2 = O(|\Delta|^2)$, and
$\|L(m) - L\| = O(\varepsilon)$, so $|L\Delta| \le C(|\Delta| + \varepsilon)|\Delta|$.
Splitting $\Delta = \zeta + \eta$ with $\zeta \in \operatorname{null} L$,
$\eta \perp \operatorname{null} L$: $|\eta| \le \sigma^{-1}
|L\Delta| \le \tau |\Delta|$, $\tau = O(\varepsilon)$, and since $\Delta \perp F \subset
\operatorname{null} L$, $\zeta = \zeta_W + \zeta_F$ with $|\zeta_F| \le |\eta|$.

(iv) **Coercivity** (line 61). $H_m = \nabla^2\mathcal{L}^\ast(z^\ast) + o(1)$, since
$\lambda(m) \to \lambda^\ast$ (hypothesis 2, C-6) and the rows’ second derivatives are
continuous, so $\Delta^\mathsf{T} H_m \Delta \ge \kappa |\zeta_W|^2 -
O(\tau + \varepsilon)|\Delta|^2 \ge \frac{\kappa}{2} |\Delta|^2$ for $\varepsilon$
small.

(v) **Conclusion.** The step the source omits: $\sum_r \lambda_r(m) h_r(z) \ge -\sum_r
\lambda_r h_r^- \ge -4\Lambda C\varepsilon X \ge -C_5 \varepsilon |\Delta|^2$ by (ii).
Hence

$$
S(z) - S^\ast \ge \left(\tfrac{\kappa}{4} - C_5 \varepsilon - C_3 |\Delta|\right) |\Delta|^2
> 0
$$

for $\varepsilon$ small and $\Delta \ne 0$, and $\Delta = 0$ gives $z = m$ and $S(z) =
S^\ast$; either way $S(z) < S^\ast$ is impossible.
When $W = 0$ the Hessian is not needed: (iii) gives
$|\Delta| \le |\zeta_F| + |\eta| \le 2\tau|\Delta|$, so $\Delta = 0$. ∎

The source’s key point (lines 64 to 66), expanding at the nearest point of the family
with its own multipliers, is right and is what makes (iii) work.
What it does not address is that the side-end slack is of the same order as the term it
must be dominated by; the pair structure, which `gradec.py` already enforces, is exactly
what controls it.

### Hypothesis 2 by affine null vectors

The source’s certificate (lines 103 to 118) is affine vectors $w_j(\varphi) = w_{j0} +
\sum_k \varphi_k w_{jk}$ with $L(\varphi) w_j(\varphi) \equiv 0$, that is
$L_0 w_{j0} = 0$, $L_0 w_{jk} + A_k w_{j0} = 0$ and $A_k w_{jl} + A_l w_{jk} = 0$, with
zero $S$-components, whose $w_{j0}$ together with $F$ span $\operatorname{null} L_0$.
The lemma is correct: $F \subset \operatorname{null} L(\varphi)$ always ($A_k$ vanishes
on position directions), the $w_j(\varphi)$ stay independent near 0, the rank cannot
drop near 0, so $\operatorname{null} L(\varphi) = \operatorname{span}(F, w_j(\varphi))$;
then $e_S \perp \operatorname{null} L(\varphi)$, the rank is constant, and
$\lambda(\varphi) =
\lambda^\ast + L(\varphi)^{\mathsf{T}+}(e_S - L(\varphi)^\mathsf{T} \lambda^\ast)$ is
continuous with $\lambda(0) = \lambda^\ast > 0$, which is the convergence to
$\lambda^\ast$ that hypothesis 2 needs (C-6). The remark that the identities make the
$F \times W$ block of $\nabla^2 \mathcal{L}^\ast$ vanish is also correct: for $f \in F$
and $w \in \operatorname{null} L_0$, $f^\mathsf{T}
\nabla^2\mathcal{L}^\ast w = -\lambda^{\ast\mathsf{T}} A_f w = \lambda^{\ast\mathsf{T}}
L_0 w_f = (w_f)_S$, and with the $F \times F$ block zero (rows are affine in the
centres), positive definiteness on any complement of $F$ in $\operatorname{null} L_0$ is
equivalent to hypothesis 3.

### The slip form

For a contact row $r$, a corner of $j$ on a side of $i$ with outward normal $n_r$, and a
flat direction $b_p$, the only entry of $A_p$ in row $r$ is in the angle column of $i$,
the square that owns the side, and it equals the tangential slip $t_{rp} = (J n_r) \cdot
(b_p(j) - b_p(i))$: the normal component of $b_p(j) - b_p(i)$ is zero because $b_p$ is
flat. Wall rows have no entry.
So the quadratic part of row $r$ of $L(\varphi)
w(\varphi)$ is the product
$\left(\sum_p t_{rp} \varphi_p\right)\left(\sum_q w_q(\theta_i)
\varphi_q\right)$ of two linear forms, which vanishes identically only if one factor
does. Hence:

> The affine null vectors exist if and only if, for each $w$ in a complement of $F$ in
> $\operatorname{null} L_0$ and each flat direction $p$, the system $L_0 v = -A_p w$ has
> a solution $v$ that is zero at the $S$ coordinate and at the angle of every square
> owning a side that some flat direction slides along.

That is one sparse system per pair $(w, p)$, all with one matrix, instead of one system
in $N(1 + f)$ unknowns and $m(1 + f + f(f+1)/2)$ equations (gradec.py lines 338 to 358).
The $S$ condition is the vanishing of the $F \times W$ block, as above.

## What gradec.py Checks, and What It Assumes

| Hypothesis or premise | gradec.py | How |
| --- | --- | --- |
| The record is a packing in $[0, S]^2$ | not checked | `verify_exact.py`, separately; the roster’s status (C-2) |
| $t^\ast$ is a root of $f$ in the stated interval | assumed (lines 41 to 56) | bisection with no initial sign check (C-3) |
| Rows tight at $z^\ast$ | lines 290 to 293 | exact in $K$ |
| Class of each incidence | lines 170 to 184 | $\tau^2 - \frac14$ zero in $K$, else its sign by interval at $t^\ast$ |
| Side-end rows come as complete pairs | lines 186 to 190, 306 to 312 | two adjacent corners of $j$, both exactly at a side end |
| Interior margin $\mu > 0$ | lines 295 to 305 | interval lower bound |
| $F$, $\operatorname{null} L_0$, rank of $L_0$ | lines 315 to 329 | exact sparse elimination over $K$; the rank is the elimination’s (N-5) |
| Hypothesis 2 | lines 337 to 391 | affine null vectors solved exactly, identities re-verified by products |
| $\lambda^\ast > 0$, $\sum_r \lambda^\ast_r L_r = e_S$ | lines 394 to 432 | linear program proposes; basis solved exactly; identity exact; signs by interval |
| Hypothesis 3 | lines 433 to 457 | leading minors of $Q$ on $\operatorname{span}(w_{j0})$, each a sum over all $k!$ permutations, exact; signs by interval |
| Dropping rows that carry no force (230, 261) | lines 259 to 288 | a linear program selects; dropping relaxes, so the choice needs no proof |
| Every check runs | all of the above | Python `assert` (N-6) |

Everything the table marks as checked is checked exactly, and the floating-point steps
(the linear programs, the QR basis, the numerical values the log prints) only propose
candidates that exact arithmetic then accepts or refuses.
Which rows the contacts file lists is untrusted and does not matter for soundness: any
set of valid rows gives a relaxation of the true problem.

## The Trust Boundaries

**`gradec.py`, the source’s checker.** It trusts python-flint (FLINT, with GMP) for
arithmetic in $\mathbb{Q}[t]/(f)$, including the inverse by an extended gcd; Python’s
`Fraction` for interval endpoints (`verify_exact.I`, `rdn`, `rup`); its own sparse
elimination (`rref`) for the rank of $L_0$, on which the claim that $F$ and the $w_{j0}$
span $\operatorname{null} L_0$ rests (line 377 compares with the same elimination’s
count; lines 381 to 391 re-verify the identities but not the rank); the input’s $t$
interval; and Python running with assertions on.
numpy, scipy and mpmath only propose candidates.
It does not decide that the record is a packing.

**`verify_exact.py`, the source’s packing checker.** Standard library only: exact
identities modulo $f$ for touching inequalities, rational interval arithmetic for strict
ones, and a separating side line or disjoint circumscribed discs for every pair.
It is the premise C-2 needs; `V-evand-verify-exact` registers it.

**`check_theorem_c.py`, written here.** It trusts CPython’s integers and `Fraction` for
all arithmetic (in $\mathbb{Q}$, or $\mathbb{Q}[t]/(f)$ for degree 2 and 4 with signs by
exact interval evaluation at $t^\ast$ and bisection of the interval), and its own sparse
elimination for ranks; the rank and nullity of $L_0$ were also computed by a numerical
singular value decomposition at every count and agree, with a ratio of at least
$2.1 \times 10^{13}$ between the last nonzero singular value and the first zero one.
numpy and scipy (HiGHS) propose the multipliers and a basis order; the identities,
signs, lifts and the Hessian are verified exactly.
Its derivative formulas were tested against finite differences of the row functions
written from their definitions (5,646 rows of 15 configurations, largest error
$1.3 \times 10^{-10}$ in a gradient and $2.7 \times 10^{-5}$ in a Hessian entry, the
rounding level of a second difference at that step).
It decides the record’s packing property itself.

**What any two share.** `gradec.py` imports `verify_exact.py`’s interval class and
rounding (line 29) and `localmin.py`’s field wrapper (line 30), so it shares that code
with both.
The checker written here shares no code with either; it shares the inputs (the
exact forms and the contacts files’ choice of rows), the certificate format’s numbering
of corners, sides and walls (read from `geom.py`’s docstring), CPython, and scipy’s
HiGHS as a proposer of multipliers in both.
Its authors read the source’s code before writing it, so it is independent after reading
the producer’s code, not clean-room; it was written by a Claude agent, a system family
the source’s `CREDITS.md` and commits also credit, from a prompt and in files of its
own. `T-124`’s Lean route is a different checker for 169 of the same counts and was not
examined here.

## Independent Checks

`check_theorem_c.py` (in the packet’s `review/`) decides, for each count, the record’s
packing property; each row’s class, tightness and margin; exact multipliers; $F$,
$\operatorname{null} L_0$ and a complement $W'$; the affine null vectors by the slip
form, verified by products from $A_k$ computed two ways; the $F \times W'$ block; and
positive definiteness on $W'$ by an exact $LDL^\mathsf{T}$. For 230 and 261 it drops the
rows a linear program finds forced to zero, a side-end pair as a whole.

It ran on 23 October 2026 on all 233 configurations, 175 of field degree 1, 51 of degree
2 and 7 of degree 4, and every one is valid.
The checks took 1,463 CPU-seconds in all, a median of 0.94 per configuration and at most
369, at n = 294 ($\dim W = 11$, $\dim F = 88$), as two processes under `nice` on the
shared four-core host (57 minutes of wall time at load averages of 17 to 38). Across the
233 it classified 202,010 rows, 184,412 of them side-end rows, present at 231 counts
(all but 1 and 5); at 206 counts, 58,988 side-end rows slip along the flat family, the
case the second step of C-1 concerns.
A flat family exists at 214 counts and $\dim W > 0$ at 47 (at most 11), where it solved
1,066 lifts; the $F \times W'$ block vanished at each of them.
The numerical SVD found the same nullity of $L_0$ at every count, with a ratio of at
least $2.1 \times 10^{13}$ between the last nonzero and the first zero singular value.
It dropped the 24 rows forced to zero at 230 and at 261, the same 24 as the source, the
lone side-end incidences there (36 and 40), and the corners beyond a side end at 66,
127, 150 and 175 (12, 6, 16 and 8). The least interior margin is $7.2 \times 10^{-17}$,
at n = 175, decided exactly, and the least multiplier is 0.0015.

`compare_certificates.py` compared the receipts with the 233 published
`n-N.gradec.json`: every row set, rank of $L_0$, $\dim F$, $\dim W$, set of moving
squares and number of load-bearing squares is the same; the interior margins agree to
the last digit of the floats the certificates print; and the least multipliers agree
within $2.1 \times 10^{-9}$ relative, both being a max-min linear program’s point,
rounded and then solved exactly.
The Hessian minors were not compared, because they depend on the basis of $W$.

Controls: with a load-bearing square of n = 10 moved by $10^{-30}$, the checker refuses
(a row is no longer tight); with the right-wall rows removed, it refuses (no strictly
positive multipliers); and its Hessian test refuses an indefinite matrix.
`packing/tests/test_evand_gradec_review.py` holds these, the n = 10 and n = 19 outcomes,
and the program’s digest against the receipts.

## Findings

| Id | Grade | Where | Finding |
| --- | --- | --- | --- |
| C-1 | major | grade-C.md lines 20 to 24, 55 to 62 | The proof does not control side-end rows in its last two steps (below). Repaired here; the hypotheses and the checks stand |
| C-2 | minor | gradec.py lines 290 to 465; LocalMin.lean lines 32 to 34 | The certificate does not decide that the record is a packing, which `IsLocalMinPacking` requires; `verify_exact.py` does, separately |
| C-3 | minor | gradec.py lines 41 to 56 | The $t$ interval is narrowed without checking that $f$ changes sign on it, unlike verify_exact.py lines 207 to 210, and a root exactly at the lower end would be bisected away. No verdict is affected: 169 intervals are the point 0 for $f = t$ and the other 64 change sign |
| C-4 | minor | gradec.py lines 461 to 465 | `n-N.gradec.json` records summaries, not $\lambda^\ast$, $F$, the affine null vectors or $W$; a check must redo the search |
| C-5 | minor | grade-C.md lines 20 and 44 | Hypothesis 1 says “edge overlap for side-end corners” and the relaxation speaks of partially overlapping contacts; the rows `gradec.py` keeps are complete pairs where the edge of $j$ is the side of $i$, and the theorem should say so |
| C-6 | minor | grade-C.md lines 45, 46 and 61 | The coercivity step needs $\nabla^2\mathcal{L}_m(m) \to \nabla^2\mathcal{L}^\ast(z^\ast)$, that is $\lambda(m) \to \lambda^\ast$, and hypothesis 2 asserts only multipliers with uniform bounds. The affine null vectors make the rank of $L(m)$ constant near $z^\ast$, so the multipliers of the lemma at lines 103 to 118 tend to $\lambda^\ast$ and no verdict is affected; the theorem should state it |
| N-1 | note | grade-C.md lines 25 and 26 | $L_3 = L_1$ holds whenever the two corners coincide, not only in the axis-aligned case: $J$ is antisymmetric. The code does not rely on it |
| N-2 | note | grade-C.md lines 116 to 118 | The $F \times W$ block remark is right, and is the $S$ condition of the slip form |
| N-3 | note | grade-C.md line 10; gradec.py lines 243 to 257 | The theorem’s coordinate is $\sin\delta$ and the Hessian is computed in $\delta$; they agree on $M$, since $d^2\delta/dw^2 = 0$ at $w = 0$, which the write-up could say |
| N-4 | note | LocalMin.lean line 33 | The side is not in the pose ball; that a packing near the record has $s \ge S^\ast - C\varepsilon$ is one line the proof omits |
| N-5 | note | gradec.py lines 326 to 329, 377 | The rank of $L_0$ is its own elimination’s; ours and a singular value decomposition agree at all 233 |
| N-6 | note | gradec.py, every check; gradec_runs/run.sh line 7 | All checks are `assert` statements, so under `python -O` or `PYTHONOPTIMIZE` the program would print VALID having checked nothing; run.sh does not set either |
| N-7 | note | gradec.py line 439; grade-C.md line 134 | The `neghess` mutation tests nothing where $\dim W = 0$, which holds at 186 of the 233, 230 and 261 among them |

**C-1 in full.** The relaxation (grade-C.md lines 20 to 23) gives, for a corner at a
side end, $h_r \ge -(\text{overhang}) \cdot |v'|$, which is $-K'\delta^2$ with
$\delta = |z -
z^\ast|$. Two steps of the proof need more than that.

1. The last line (61) concludes $S(z) - S^\ast \ge (\kappa/4)|\Delta|^2 - O(|\Delta|^3)$
   from line 56, which needs $\sum_r \lambda_r(m) h_r(z) \ge -o(|\Delta|^2)$; side-end
   rows give only $-\Lambda K' \delta^2$, the same order as $(\kappa/4)|\Delta|^2$. Line
   24’s “the rigidity argument only needs $h_r \ge -K'\delta^2$” is true of the
   first-order argument of grade A (LocalMin.lean’s `rigidity`) and not of this
   second-order one.
2. Line 57 uses $h_r \ge -K'|\Delta|^2$ with $\Delta = z - m$. The overhang is measured
   from the record, not from $m$: where a flat direction slides $j$ along the side of
   $i$, at $m$ one corner of $j$ already overhangs the end by $O(|m - z^\ast|)$, and for
   the two squares alone a rotation of size $|\Delta|$ about the end of the side makes
   that row about $-|m - z^\ast| \cdot |\Delta|$, first order in $|\Delta|$; so the
   bound does not follow from the relaxation.
   This is not a corner case: our checker counts the side-end rows whose slip along $F$
   is nonzero, and they occur at 206 of the 233 configurations (58,988 rows), n = 19
   among them.

The two-square picture shows why the theorem survives: when one row of a pair is
negative by $t\alpha$ (overhang $t$, rotation $\alpha$), the other row is about
$+\alpha$, first order and positive, and a descent cannot afford that.
The pair form and step (ii) of The Proof, Repaired turn this into the argument.

## Questions for the Author

1. Would you adopt the pair form and the bootstrap of step (ii) in grade-C.md, and say
   in hypothesis 2 that the multipliers tend to $\lambda^\ast$, or do you have a route
   to $h_r \ge -K'|\Delta|^2$ relative to $m$ that we missed?
2. Could the certificate files carry the exact objects, $\lambda^\ast$ in $K$, the basis
   of $F$, the affine null vectors and the basis of $W$, so that a checker needs only
   products and signs?
3. Is `verify_exact.py`’s VALID in `minpoly/results.json` the intended premise that the
   record is a packing, and could `gradec.json` record it?
4. With the slip form and an $LDL^\mathsf{T}$, both walls of the 17 timeouts go away in
   our checker. Would you publish `n-N.contacts.json` for those 17 so that they can be
   run?
5. At 230 and 261, where $\dim W = 0$, which mutations does “still rejected” (line 134)
   refer to?

## Significance

The draft score is S2, as for `T-124`, and this review keeps it.
The claim is local structure of named configurations under a non-strict, index-matched
notion, with no bound and no rigidity; it is weaker at every count than the rigidity
results `T-012` to `T-014` and the optimality statements the register scores S3. Theorem
C is a second-order sufficient condition adapted to an exact flat family, a sound and
useful method, but the claim scored is the 233 local minima, not the method.
No result here reaches S4 or S5, and no News item is owed.

## For the Records Lane

- No `T-NNN` holds the claim, so the review covers no register entry.
  Registering it needs an id.
  On this review and the full run here, an entry of kind `restricted-optimality` can
  derive V3 and C3 from the replay evidence; its composition note should say that the
  theorem is the source’s paper proof as repaired here (C-1); C4 needs a second
  adversarial review and a human oversight record.
- The report’s evidence entry, `E-evand-gradec-local-minima-233-report`, carries this
  review as its `external_review` (`defect-found`, for C-1, with the repair).
  The run here and the n = 10 recomputation of 12 October are verified certificates,
  which a record must cite (`devtools.check_certificate_citations`), and no case record
  has a block for local minimality; their evidence entries are drafted in `think-7scz`
  and enter the register with the claim’s entry, which cites them.
  Until then their receipts in the exact-data packet are the record of both runs.
- The wording “confirmed” must say which confirmation: independently re-implemented
  after reading the producer’s code, by a Claude agent, a system family the producer
  also used.
- The claim is about the source’s configurations: measured on 12 October, at 11 counts
  (70, 84, 86, 127, 153, 175, 176, 232, 258, 261, 267) the side was above the case’s
  record, and at 230 the side is 643/41, the case’s ceiling; registration should measure
  again. Whether the other 222 configurations are the case records’ packings, as poses
  and not only as sides, was not checked.
- The 17 timeouts and the configurations of field degree above 4 are outside the claim.

## Comparison

No earlier review of Theorem C or of the grade-C batch exists.
Before writing, this review had read the bead’s notes of 12 October and the packet
READMEs, which record the read at `ad86d42`, the price of a re-run, and that
`gradec.py`, run here once, reproduced the n = 10 certificate byte for byte; that run
used the producer’s own code and decided nothing about the theorem.
Those notes observe that the ten Hessian-step timeouts all have $\dim W \ge 12$ against
$\dim W \le 11$ for every finished run; the permutation sum explains it, and the
$LDL^\mathsf{T}$ used here removes it.

## Verdict

Theorem C holds, `gradec.py` checks what it needs, and the 233 VALID verdicts stand on
the proof as repaired here, with the record’s packing property supplied by the source’s
`verify_exact.py` and decided again here.
The gap in the paper proof is major for the write-up and does not change a verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
