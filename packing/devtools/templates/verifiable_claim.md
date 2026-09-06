# Verifiable Claim: $s(11) \ge {{L_FRAC}}$

Everything needed to check, with your own tools and without trusting this repository,
that eleven unit squares do not fit in a square of side ${{L_FRAC}} = {{L_DEC}}$: the
claim, the theorem it instantiates, its proof, a verifier in Python’s standard library
alone, and the certificate the verifier decides.
Paste this one file into any coding agent, or read it yourself.
{{STANDING}}

## The Claim

Let $s(n)$ be the side of the smallest square that contains $n$ unit squares with
pairwise disjoint interiors, the unit squares free to rotate.
(Formally $s(n)$ is the infimum of the sides that admit such a packing.)

**Claim.** $s(11) \ge {{L_FRAC}}$.

The witness is the certificate `{{CERT_NAME}}`, {{N_ATOMS}} weighted points and a net of
{{N_DIRECTIONS}} rational directions, carried in full at the end of this file and kept
in the repository as [`{{CERT_NAME}}`]({{CERT_URL}}). The verifier below decides five
conditions on it in exact rational arithmetic, and the theorem below shows that the five
conditions imply the claim.
[`{{OTHER_FILE_NAME}}`]({{OTHER_CLAIM_URL}}) does the same for
$s(11) \ge {{OTHER_L_FRAC}}$.

## The Theorem

The argument is a weighted, fractional form of the classical unavoidable-set argument
for square packing, in the shape Gustavo Massaccesi used for $n = 17$ in August 2026
after Sam Burns proposed the weighted form.
Neither the theorem nor the certificate shape is this project’s; the $n = 11$ instance
is.

**Data.** An integer $n \ge 1$; rationals $L > 0$ (the container side) and $B > 0$ (the
shrunken side); a direction net of rationals $0 = t_0 < t_1 < \cdots < t_K$, standing
for the angles $\theta_k = 2 \arctan t_k$; and finitely many atoms $(x_i, y_i, w_i)$
with rational coordinates and rational weights $w_i \ge 0$. For a set $Q$ in the plane
write $\operatorname{mass}(Q) = \sum \{\, w_i : (x_i, y_i) \in Q \,\}$. The container is
the closed square $[0, L]^2$.

**Hypotheses.**

- **Condition 1.** The weighted atom set is invariant under the eight symmetries of
  $[0, L]^2$: for every atom, each of the eight images of its site under
  $(x, y) \mapsto (x, y), (L - x, y), (x, L - y), (L - x, L - y), (y, x), (L - y, x), (y, L - x), (L - y, L - x)$
  is a site of the same total weight.
  The proof uses only the reflection $(x, y) \mapsto (y, x)$; the certificate declares
  the full group, and checking it is a stronger hypothesis, hence safe.
- **Condition 2.** $\sum_i w_i < n$.
- **Condition 3.** $\theta_K \ge \pi/4$. Since $\tan(\pi/8) = \sqrt{2} - 1$ is the
  positive root of $t^2 + 2t - 1$ and that polynomial increases for $t \ge 0$, this is
  exactly $t_K^2 + 2 t_K - 1 \ge 0$, a rational inequality.
- **Condition 4.** $B(1 + D) < 1$, where
  $D = \max_k (t_{k+1} - t_k) / (1 + t_k t_{k+1})$. Since $\theta = 2 \arctan t$, half
  the gap between adjacent net angles is $\arctan t_{k+1} - \arctan t_k$, whose tangent
  is exactly that quotient, so $D$ is the tangent of the largest half-gap.
- **Condition 5.** For every $k$ and every closed square $Q$ of side $B$ whose edges
  make angle $\theta_k$ with the axes and which lies inside $[0, L]^2$:
  $\operatorname{mass}(Q) \ge 1$.

**Conclusion.** $n$ unit squares with pairwise disjoint interiors do not fit in
$[0, L]^2$. Hence $s(n) \ge L$.

## The Proof

Suppose closed unit squares $S_1, \dots, S_n \subset [0, L]^2$ have pairwise disjoint
interiors. We derive $n \le \sum_i w_i$, contradicting Condition 2.

1. **Orientation reduction.** A square is unchanged by a quarter turn, so its
   orientation $\varphi$, the angle its edges make with the axes, may be taken in
   $[0, \pi/2)$. If $\varphi > \pi/4$, apply the reflection $R(x, y) = (y, x)$. It maps
   $[0, L]^2$ onto itself and sends a direction at angle $\alpha$ to angle
   $\pi/2 - \alpha$, so $R(S_j)$ is a unit square in $[0, L]^2$ with orientation
   $\pi/2 - \varphi \in (0, \pi/4)$. Write $S'_j$ for $S_j$ or $R(S_j)$, whichever has
   orientation $\varphi' \in [0, \pi/4]$.
2. **A net angle nearby.** By Condition 3 and $t_0 = 0$, the net angles run from $0$ to
   at least $\pi/4$, so $\varphi'$ lies in some $[\theta_k, \theta_{k+1}]$, and the
   nearer endpoint $\theta$ satisfies
   $d := |\varphi' - \theta| \le (\theta_{k+1} - \theta_k)/2$. Since $\tan$ increases on
   $[0, \pi/2)$, $\tan d \le D$.
3. **A concentric shrunken square.** Let $Q$ be the closed square of side $B$, centered
   at the center of $S'_j$, with orientation $\theta$. Its support function in the
   direction of any edge normal of $S'_j$ is $(B/2)(\cos d + \sin d)$, while $S'_j$
   extends $1/2$ from its center in that direction, so $Q$ lies in the open interior of
   $S'_j$ as soon as $B(\cos d + \sin d) < 1$. Now
   $\cos d + \sin d = \cos d \,(1 + \tan d) \le 1 + \tan d \le 1 + D$, and Condition 4
   gives $B(1 + D) < 1$. Hence $Q \subset \operatorname{int}(S'_j) \subset [0, L]^2$,
   strictly inside.
4. **Condition 5 applies.** $Q$ is a closed $B$-square at the net angle $\theta$ lying
   inside $[0, L]^2$, so $\operatorname{mass}(Q) \ge 1$.
5. **Pull back.** Let $P_j = Q$ if $S'_j = S_j$, and $P_j = R(Q)$ otherwise.
   Then $P_j \subset \operatorname{int}(S_j)$, and
   $\operatorname{mass}(P_j) = \operatorname{mass}(Q) \ge 1$ because by Condition 1 the
   weighted atom set is invariant under $R$: the atoms inside $R(Q)$ are the images of
   the atoms inside $Q$, with the same weights.
6. **Count.** The interiors of the $S_j$ are pairwise disjoint, so the $P_j$ are
   pairwise disjoint and each atom lies in at most one of them.
   With $w_i \ge 0$, $n \le \sum_j \operatorname{mass}(P_j) \le \sum_i w_i < n$.
   Contradiction.

So no such packing exists in $[0, L]^2$. If $s(n) < L$, the definition of the infimum
gives a packing in some square of side $L' < L$, which sits inside $[0, L]^2$; therefore
$s(n) \ge L$.

Two remarks a careful reader will want settled.
First, $Q$ is closed and Condition 5 counts atoms on its boundary.
This never double-counts, because step 3 puts $Q$ strictly inside the interior of one
unit square. Second, Condition 5 quantifies over every $B$-square inside $[0, L]^2$ at a
net angle, a superset of the squares the proof meets.
A stronger hypothesis can only make the theorem harder to apply, never unsound.

## Why the Sweep Is Exact

Condition 5 quantifies over a continuum of centers, and the verifier decides it by a
finite enumeration. At the net direction with half-tangent $t_k$, put
$c_k = (1 - t_k^2)/(1 + t_k^2)$ and $s_k = 2 t_k/(1 + t_k^2)$, so that
$c_k^2 + s_k^2 = 1$ exactly, and $h_k = (B/2)(|c_k| + |s_k|)$. The closed $B$-square at
that direction with center $(X, Y)$ lies inside $[0, L]^2$ exactly when
$h_k \le X, Y \le L - h_k$, and it contains the atom at $(x_i, y_i)$ exactly when
$|c_k (x_i - X) + s_k (y_i - Y)| \le B/2$ and
$|-s_k (x_i - X) + c_k (y_i - Y)| \le B/2$. In the rotated coordinates
$U = c_k X + s_k Y$ and $V = -s_k X + c_k Y$, each atom therefore contributes its weight
on one closed axis-parallel rectangle of centers, and the edges of these rectangles,
with the four lines at the extreme $U$- and $V$-coordinates of the admissible square,
cut the plane into finitely many open cells.
The admissible square is oblique in these coordinates unless $\theta_k$ is a multiple of
$\pi/2$, and its own edges are not among the lines: a cell may straddle one of them, and
the clipping test in `least_mass` decides exactly which cells meet the square, from the
exact range of $V$ the square occupies over each strip between adjacent $U$-lines.
The covered mass is constant on each open cell.
On a cell’s boundary it can only be larger, because the rectangles are closed and the
weights are nonnegative.
And every admissible center lies in the closure of some open cell that meets the
admissible square: that square has interior when $2 h_k < L$, so it has interior points
within every distance of the center; finitely many lines cannot cover an open set, so
within every distance of the center some cell meeting the square has a point; and there
are finitely many cells, so one cell does at every distance, which is to say the center
lies in its closure.
So the least mass over all admissible centers is the least over the open cells that meet
the admissible square, and scoring each of them once decides Condition 5 at that
direction. Every quantity is rational, so every score is exact.

Two shapes of the admissible square need no cells.
When $2 h_k > L$, no $B$-square at that direction fits inside the container, so
Condition 5 quantifies over nothing there and holds vacuously; the verifier counts such
a direction as admitting no placement rather than as decided, and a certificate whose
every direction admits none is reported as having decided nothing.
When $2 h_k = L$, the one admissible center is $(L/2, L/2)$, and the verifier scores
that single closed square directly.
Neither arises here: $B < 1$ and $L > 2$, so $2 h_k \le B \sqrt{2} < L$ at every
direction.

## How to Check It

Save this file as `{{FILE_NAME}}` and the verifier block below as `{{VERIFIER_NAME}}`,
then run the verifier on this file with any CPython 3.12 or later.
It needs nothing outside the standard library, and it reads the certificate out of the
fenced `json` block at the end.

```
python {{VERIFIER_NAME}} {{FILE_NAME}}
```

It also accepts the certificate on its own, saved from that block as `{{CERT_NAME}}`.

It prints one line per condition, then a line comparing the file’s declared `claim`,
`total_mass` and `least_cell_mass` with what it computed, then a verdict.
For this certificate the verdict is `VERIFIED: s(11) >= {{L_FRAC}}`, with Condition 5
reporting the least covered mass ${{LEAST_FRAC}}$ at direction $0$ and center
${{WITNESS_CENTER}}$ over the {{N_DIRECTIONS}} directions.
It takes {{RUNTIME}} in pure Python on a laptop, most of it on the finite sweep of
Condition 5 that “Why the Sweep Is Exact” describes.
The sweep runs only once Conditions 1 to 4 hold; after a failure among them, the
Condition 5 line says it was not evaluated.
Before any condition, a file that is not a certificate of the theorem’s shape is refused
by name: among the refusals are a rational written as a JSON number, a negative weight,
a `variant` other than `unconditional`, an atom outside the container, and two atoms at
one site. The theorem would tolerate the last two, an outside atom only adding to the
total and a repeated site being one site of the summed weight, but a well-formed
certificate has neither, and the pinned checker `minimal_verify.py`, beside this file in
the repository, refuses them too.

The exit status is 0 only when all five conditions hold and the three declarations
match, and 1 on any refusal.
A third status, 2, means no verdict was reached: a usage error, or the sweep’s own
cross-check failing.
At every direction the verifier re-sums the atoms directly at the center it reports and
compares that with the swept minimum; a disagreement is a bug in the verifier, not in
the certificate, and it prints one line beginning `INTERNAL ERROR` in place of the
verdict. Four perturbations show the verifier deciding rather than agreeing, each with
its magnitude and the line that refuses it.
Condition 5 holds by the margin ${{LEAST_FRAC}} - 1 = {{MARGIN_FRAC}}$, and the
placement attaining it, centered at ${{WITNESS_CENTER}}$, covers the atom at
${{TIGHT_ATOM}}$, of weight ${{TIGHT_WEIGHT}}$ and one of {{TIGHT_ORBIT}} in its orbit,
the atoms at ${{TIGHT_ORBIT_SITES}}$.

- Lighten all {{TIGHT_ORBIT}} atoms of that orbit by ${{LIGHTEN_FRAC}}$, more than the
  margin. Conditions 1 to 4 still hold, and Condition 5 fails: that placement now covers
  at most ${{LIGHTENED_LEAST_FRAC}}$, and the least covered mass reported is no more
  than that.
- Lighten one of them alone by the same amount, or drop it.
  Condition 1 fails, and Condition 5 is not evaluated.
- Set `angle_limit` to $41/100$, short of $\tan(\pi/8) = 0.4142\ldots$. Condition 3
  fails, and Condition 5 is not evaluated.
- Lighten the central atom at ${{CENTER_ATOM}}$, a one-point orbit of weight
  ${{CENTER_WEIGHT}}$, by the margin ${{MARGIN_FRAC}}$ or by less.
  All five conditions still hold: Condition 1 is untouched, Condition 2 improves, and
  every placement loses at most the margin.
  What refuses the file is the declarations line, since its `total_mass` is now stale;
  write the values that line computed into the file, and the verdict is `VERIFIED`.

The first two also leave the file’s `total_mass` stale, and the first its
`least_cell_mass`; the declarations line, after the conditions, says so.
The condition lines are what to read.

## How This Repository Decided It

{{DECIDED_HERE}}

## The Verifier

`{{VERIFIER_NAME}}`, byte for byte as kept in the repository at
[`{{VERIFIER_NAME}}`]({{VERIFIER_URL}}).

````python
{{VERIFIER_SOURCE}}
````

## The Certificate

`{{CERT_NAME}}`, as kept in the repository.

````json
{{CERTIFICATE_JSON}}
````

## What Is and Is Not Claimed

This file decides the ${{L_FRAC}}$ bound, and its proof covers exactly what the five
conditions establish: that eleven unit squares do not fit in a square of side
${{L_DEC}}$. Nothing here depends on the correctness of any other code in the
repository, and nothing here claims that ${{L_FRAC}}$ is the true value of $s(11)$: the
best known packing puts $s(11) \le {{BEST_PACKING_TEX}}$, and the gap is open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
