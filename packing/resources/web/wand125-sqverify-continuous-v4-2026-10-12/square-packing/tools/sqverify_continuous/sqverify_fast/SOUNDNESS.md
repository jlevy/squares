# Soundness of sqverify-fast

This is the proof obligation of the clean-room measure verifier: every lemma the code
relies on, stated and proved, with the code that discharges it.
It was derived from the mathematics of the net-and-shrink argument, not from any
checker’s source; [INDEPENDENCE.md](INDEPENDENCE.md) records what was read.

A verdict of `verified` for all directions of a net, together with the exact admission
premises, proves $s(n) \ge L$. Every other verdict proves nothing.

“Spec §” below cites lane W1’s specification,
`docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md`, which is
not on this branch: it is on W1’s branch and in this branch’s history at the parent of
commit `abf0a592b`.

## The Claim

A certificate gives a side $L$, a shrunk side $B$, a net step $D$ and count $N_\theta$
(here $83/40000$ and $201$), and orbit representatives $R_j = [x_1, x_2] \times [y_1,
y_2]$ with weights $w_j \ge 0$, all exact rationals.
Its density is

$$
g = \sum_j \frac{w_j}{8 |R_j|} \sum_{S \in D_4} \mathbf 1_{S(R_j)},
$$

with $D_4$ the symmetry group of $K = [0, L]^2$. So $g \ge 0$, $g$ is $D_4$-invariant,
and $\int g = M = \sum_j w_j$.

**Theorem.** If $M < n$, $B(1 + D) < 1$, $t_{\max} = (N_\theta - 1) D$ satisfies
$t_{\max}^2 + 2 t_{\max} - 1 > 0$, and for every net index $r$ and every centre $c \in
[a_r, L - a_r]^2$ the closed square $Q_r(c)$ of side $B$, centre $c$ and angle $\theta_r
= 2 \arctan(rD)$ satisfies $\int_{Q_r(c)} g \ge 1$, where $a_r = B(\cos\theta_r +
\sin\theta_r)/2$, then $n$ unit squares do not pack in $K$; hence $s(n) \ge L$.

*Proof.*

1. *Net (N1).* With $t_r = rD$, consecutive half-angle tangents differ by $D$, so every
   $t \in [0, t_{\max}]$ lies within $D/2$ of some $t_r$. The endpoint condition says
   $\tan(\theta_{\max}/2) > \sqrt 2 - 1 = \tan(\pi/8)$, so $\theta_{\max} > \pi/4$.

2. *Orientation (N2).* A unit square’s angle is defined modulo $\pi/2$; take $\varphi
   \in [0, \pi/2)$. If $\varphi > \pi/4$, reflect the whole configuration in the
   diagonal $y = x$, which maps $K$ to itself, preserves $g$, preserves disjointness,
   and sends $\varphi$ to $\pi/2 - \varphi < \pi/4$. So assume $\varphi \in [0,
   \pi/4]$, which N1 places below $\theta_{\max}$, and let $\theta_r$ be a net angle
   with $|\tan(\varphi/2) - t_r| \le D/2$ (N1). With $\delta = |\varphi - \theta_r|$,
   $z = \tan(\delta/2) = |\tan(\varphi/2) - t_r|/(1 + t_r \tan(\varphi/2)) \le D/2$;
   $\delta$ itself may reach $2\arctan(D/2)$, which exceeds $\arctan D$, so the argument
   uses only the bound on $z$. The fold is at $\pi/4$, not at $\theta_{\max}$: lemma D’s
   per-bin domain (format M) depends on it, since the half-width $\rho$ falls again past
   $\tan(\pi/8)$ and a square folded only above $\theta_{\max}$ could sit at half-angle
   tangent up to $t_{200} + D/2$, where $\rho$ is below $\rho(a_{200})$. Tokoharu’s
   domain needs no such care, but the same fold serves it.

3. *Shrink (N3).* The concentric square of side $B$ at angle $\theta_r$, seen in the
   unit square’s frame, is rotated by $\delta$; with $z = \tan(\delta/2) \le D/2$ (N2),
   its extent along either of the unit square’s axes is
   $B(\cos\delta + \sin\delta) = B(1 + 2z - z^2)/(1 + z^2) \le B(1 + 2z) \le B(1 + D)
   < 1$, since $(1 + 2z)(1 + z^2) - (1 + 2z - z^2) = 2z^2 + 2z^3 \ge 0$ (spec N2, N3).
   So it lies in the open unit square, hence in $K$, and its centre lies in $[a_r, L -
   a_r]^2$, the set of centres whose $B$-square at angle $\theta_r$ lies in $K$. Both
   domains rest on this half-angle form: Tokoharu’s and the per-bin domain (format M),
   whose bins are the half-angle tangents within $D/2$ of $t_r$. Admission checks the
   stronger tangent form $B(1 + D/(1 - D^2/4)) < 1$ for format M as well, which a proof
   through $\cos\delta(1 + \tan\delta)$ would need: at $D = 83/40000$ the two limits on
   $B$ are about $0.99792929671$ and $0.99792929449$, and every retained certificate has
   $B =
   9977/10000$, below both (question of the 3 October testing review).

4. *Counting (N4).* The $n$ unit squares have disjoint interiors, so their $B$-squares
   are pairwise disjoint closed sets in $K$. With $g \ge 0$, $n \le \sum_i \int_{Q_i} g
   \le \int_K g \le M < n$, a contradiction.

The code checks every premise but the coverage in exact rationals at admission
(`certificate::admit`): $0 < M < n$; $0 < B < 1$; $B(1 + D) < 1$; the endpoint
polynomial; $t_{\max} \le 1/2$ (so every net angle is below $\pi/2$, its sine is
positive and its cosine at least $3/5$); $L^2 \ge 2B^2$ (so $a_r \le L/2$ and the
domains are nonempty); and $0 \le x_1 < x_2 \le L$, $0 \le y_1 < y_2 \le L$ for every
positive-weight rectangle (containment is not needed for N4 but is the format’s
promise). Lemma F3’s caps are checked there too: $L \le 1000$, at most $2^{16}$ net
directions, at most $10^6$ listed rows, and every expanded rectangle’s density at most
$2^{96}$. Negative weights, duplicate JSON keys, a count or side that disagrees with the
request, and decimal tokens that do not parse exactly are refusals, and so is a gzip
input with a second member or any byte after its first, which another reader would see
differently (finding TI-2 of the 3 October testing review).
Decimal JSON numbers are their literal values, never the nearest binary64. The expansion
multiplies nothing out of order: each image’s exact density is summed when images
coincide, and the expanded total must integrate back to $M$ exactly.

The coverage threshold $T$ defaults to the one the certificate declares (format T’s
`coverage_lower_bound_exact`, $10001/10000$ in every file here; $1$ for formats M and
L), and is never below $1$, which is what N4 needs.
A larger $T$ only makes acceptance harder.
Formats M and L change the measure and, for M, the centre domain; the section
[Formats M and L](#formats-m-and-l-points-segments-and-domains) states what changes.

## Reduction of Centres

**Lemma C1 (quarter turn).** Let $\rho$ be the rotation by $\pi/2$ about $(L/2, L/2)$.
Then $\rho(Q_r(c)) = Q_r(\rho c)$, since a square is invariant under a quarter turn
about its centre, and $g \circ \rho = g$. So $F_r(c) = \int_{Q_r(c)} g$ satisfies
$F_r(\rho c) = F_r(c)$, and every point of $[a_r, L - a_r]^2$ has an image under a power
of $\rho$ in the closed quadrant $[L/2, L - a_r]^2$. It suffices to check that quadrant.
A reflection would reverse the angle and is not used here.

The search box for $r \ge 1$ is $[\ell, u]^2$ with $\ell \le L/2$ and $u \ge L - a_r$
the outward binary64 roundings, a superset of the quadrant.

## Direction $r = 0$

**Lemma A1 (vertices suffice).** For $\theta = 0$, $F(x, y) = \sum_k \rho_k\,
o^x_k(x)\, o^y_k(y)$ over the expanded rectangles, where $o^x_k(x) = |[x - h, x + h]
\cap [x_1, x_2]|$ with $h = B/2$. Each $o^x_k$ is continuous and affine between
consecutive points of $\{x_1 \pm h, x_2 \pm h\}$. Let $E$ be the set of all such points
in $[L/2, L - h]$ together with both ends.
On each cell of $E \times E$ every term is a product of an affine function of $x$ and
one of $y$, so $F$ is bilinear there, hence a convex combination of its four corner
values: its minimum over the closed quadrant is a minimum over grid vertices.
The event sets are computed and sorted in exact rationals (`axis::verify_axis`).

**Lemma A2 (the column sweep).** With $o^y_k(y) = r(y + h - y_1) - r(y + h - y_2) - r(y
- h - y_1) + r(y - h - y_2)$ and $r(z) = \max(z, 0)$, the column function $G(y) = \sum_k
  a_k o^y_k(y)$ for fixed weights $a_k = \rho_k o^x_k(x)$ is affine between
consecutive events, with slope changes $+a_k, -a_k, -a_k, +a_k$ at $y_1 - h, y_2 - h,
  y_1 + h, y_2 +
  h$. Every in-range breakpoint is itself an event (located by exact binary
search), a breakpoint below the domain belongs to the initial slope, and one above it
never acts. So $G(y_{j+1}) = G(y_j) + \sigma_j (y_{j+1} - y_j)$ with $\sigma_j$ the sum
of steps at or below $y_j$, which the code evaluates in interval arithmetic (lemma I1),
starting from a directly evaluated $G(y_0)$. The verdict compares the least lower
endpoint with the upper end of $T$’s enclosure.

## Directions $r \ge 1$

Write $c = \cos\theta_r$, $s = \sin\theta_r$ (exact rationals, both positive), $h =
B/2$, $u = (c, s)$, $v = (-s, c)$, so $Q(p) = \{q : |u \cdot (q - p)| \le h, |v \cdot (q
- p)| \le h\}$. A box of centres is $C = [x_0 \pm d_x] \times [y_0 \pm d_y]$; the code
takes $x_0$ the rounded midpoint and $d_x$ an upward-rounded half-width, so the real box
  it reasons about contains the box it was given.
  Splitting a box at its rounded midpoint yields two closed boxes whose union is the
  box, so the leaves cover the search box.

**Lemma R1 (classification).** Let $R$ have centre $m$ and half-sizes $(w_x, w_y)$. Put
$\Delta = m - (x_0, y_0)$, $d_u = |u \cdot \Delta|$, $d_v = |v \cdot \Delta|$, $e_u
= c w_x + s w_y$, $e_v = s w_x + c w_y$, $b_u = c d_x + s d_y$, $b_v = s d_x + c d_y$.

- If $d_u + e_u + b_u \le h$ and $d_v + e_v + b_v \le h$, then $R \subseteq Q(p)$ for
  every $p \in C$. For $q \in R$, $p \in C$: $|u \cdot (q - p)| \le d_u + |u \cdot (q -
  m)| + |u \cdot (p - p_0)| \le d_u + e_u + b_u$, and likewise for $v$.
- If $d_u \ge e_u + h + b_u + \tau'$ for some $\tau' > 0$ (or the same along $v$, or the
  axis-aligned extents are separated by $\tau'$), then $R \cap Q(p) = \emptyset$ for
  every $p \in C$, by the same triangle inequality.

Inside rectangles contribute their exact mass $\rho |R|$ at every $p \in C$ and nothing
to the derivative; outside ones contribute nothing.
Both tests are made in plain binary64 with the slack `TAU` $= 10^{-9}$ added against the
decision (lemma F2), and anything not certified either way is a boundary rectangle.
A child box is a subset of its parent, so a parent’s inside and outside verdicts hold
for the child and only the parent’s boundary list is reclassified.

**Lemma R2 (area at the centre).** Fix $p_0$ and $R$ with an inner representable
rectangle $R^- \subseteq R$ (the code takes $[x_1^{\uparrow}, x_2^{\downarrow}] \times
[y_1^{\uparrow}, y_2^{\downarrow}]$ from the tight enclosures).
For $\xi$ in $R^-$’s abscissa range (as offsets from $x_0$), the vertical section of
$R^- \cap Q(p_0)$ has length $\max(0, \eta(\xi))$ where

$$
\eta(\xi) = \min(e, f_1(\xi), f_2(\xi)) - \max(b, g_1(\xi), g_2(\xi)),
$$

$e, b$ are the section’s top and bottom offsets, $f_1 = (h - c\xi)/s$, $f_2 = (h +
s\xi)/c$, $g_1 = (-h - c\xi)/s$, $g_2 = (s\xi - h)/c$. (On the vertical line, $|c\xi +
s\eta| \le h$ and $|-s\xi + c\eta| \le h$ are exactly $g_1 \le \eta \le f_1$ and $g_2
\le \eta \le f_2$.) So $\eta$ is a minimum of nine affine functions and is concave on
all of $\mathbb R$. For any nodes $\xi_0 < \dots < \xi_k$ in the abscissa range and
lower bounds $\lambda_i \le \eta(\xi_i)$,

$$
|R \cap Q(p_0)| \ge \int_{\xi_0}^{\xi_k} \max(0, \eta) \ge \sum_{i \in P} \frac{(\xi_{i+1}
- \xi_i)(\lambda_i + \lambda_{i+1})}{2}
$$

for any set $P$ of pieces with positive summands: on each piece $\max(0, \eta) \ge
\eta$, and the trapezoid underestimates the integral of a concave function.
The bound needs no breakpoint to be located exactly; the code places nodes at the
approximate breakpoints (where two affine pieces cross, and at the zeros of $\eta$) so
the bound is nearly exact, takes $P$ to be the pieces whose summand is positive, and
rounds every step downward (lemma I1). `rotated::area_dn`.

**Lemma R3 (mean value).** $F$ is Lipschitz (translating a square by $\delta$ changes it
by a set of area at most $4B|\delta|$, and $g$ is bounded), so it is absolutely
continuous on every segment.
If $|\partial_x F| \le G_x$ and $|\partial_y F| \le G_y$ almost everywhere on $C$, then
for $p \in C$, along the path $p_0 \to (p_x, y_0) \to
p$ inside $C$,

$$
F(p) \ge F(p_0) - G_x d_x - G_y d_y.
$$

**Lemma R4 (the derivative).** For a rectangle $R = [x_1, x_2] \times [y_1, y_2]$ and a
measurable $S$, $t \mapsto |(R - t e_1) \cap S| = \int_{y_1}^{y_2} |[x_1 - t, x_2 - t]
\cap S_y|\, dy$ is Lipschitz with derivative, for almost every $t$, $\ell(\{x_1 - t\}
\times [y_1, y_2] \cap S) - \ell(\{x_2 - t\} \times [y_1, y_2] \cap S)$, by
differentiating each one-dimensional section and Fubini.
Translating the square by $+t$ is translating $R$ by $-t$ relative to it, so

$$
\partial_x |R \cap Q(p)| = \ell(\text{left edge} \cap Q(p)) - \ell(\text{right edge}
\cap Q(p)),
$$

and $\partial_y$ is bottom minus top.
$\partial F$ is the $\rho$-weighted sum over the boundary rectangles (inside and outside
ones have zero derivative on $C$).

**Lemma R5 (edge lengths over a box).** For the vertical edge $\{a\} \times [b, e]$ and
$p \in C$, with $\omega = a - p_x$, $e' = e - p_y$, $b' = b - p_y$, the length inside
$Q(p)$ is $\max(0, \min_i T_i)$ over

$$
e - b,\ e' + \tfrac hs + \tfrac cs \omega,\ e' + \tfrac hc - \tfrac sc \omega,\
\tfrac hs - \tfrac cs \omega - b',\ \tfrac hc + \tfrac sc \omega - b',\ \tfrac{2h}s,\
\tfrac{2h}c,\ \tfrac hs + \tfrac hc - \tfrac{\omega}{sc},\ \tfrac hs + \tfrac hc +
\tfrac{\omega}{sc},
$$

the nine differences $X - Y$, $X \in \{e', f_1(\omega), f_2(\omega)\}$, $Y \in \{b',
g_1(\omega), g_2(\omega)\}$. Each $T_i$ depends on $p$ only through $\omega$ or $p_y$,
separately, so its interval enclosure over $C$ (with $a, b, e$ enclosed too) is valid,
and $\max(0, \min_i T_i)$ is enclosed by $[\max(0, \min_i T_i^{\mathrm{lo}}), \max(0,
\min_i T_i^{\mathrm{hi}})]$. Horizontal edges are the same with $c$ and $s$ exchanged.
An edge certified inside every square of the box (R1 with $w_x = 0$) has length exactly
$e - b$; one certified outside has length zero.
`rotated::segment_length`, `rotated::edge_length`.

**Acceptance.** A box is accepted when the downward-rounded $F^-(p_0) - G_x d_x - G_y
d_y$, with $F^-$ the sum of inside masses and R2 bounds and $G$ the magnitude of the
interval sum of R4–R5 enclosures, is at least the upper end of $T$’s enclosure.
The receipt’s minimum certified bound is the least accepted value, a lower bound on
$\min F$ over the quadrant.
With points or segments, the box’s atom bound (lemmas B1 to B3) is added after the
derivative penalty, which it does not enter.
Every accept is the comparison `bound >= threshold`, which is false for `NaN`; a box
whose centre bound, atom bound or derivative enclosure is not finite stops the direction
as `non-finite`, a refusal, and lemma F3 proves that this cannot happen for an admitted
certificate. A box whose centre bound falls below $T - 10^{-9}$, and whose centre still
falls below it when the atoms are estimated from above (points within `TAU` of the
square counted, segment parameters widened by `TAU`), stops the direction as a
counterexample candidate, which is a refusal; `--confirm` evaluates the candidate centre
in exact rationals (`oracle::coverage`). The estimate decides only which refusal is
reported. A box at the depth limit is set aside and the search goes on, so that a
counterexample elsewhere is still found; the first 32 such boxes have their centre’s
capture evaluated exactly, and one below $T$ is reported as a counterexample candidate,
since the estimate’s error can hide a band of centres just below the threshold.
Otherwise the direction is `unresolved`, as it is when the node budget runs out or 4,096
boxes reach the depth limit.
Every one of these outcomes is a refusal.

## Formats M and L: Points, Segments and Domains

Formats M and L (spec §1.4) keep the theorem above with three changes: the measure has
point masses and segments of mass spread uniformly by length beside the rectangles, the
threshold is $\Gamma = 1$, and format M declares the per-bin centre domain.
Admission refuses a negative mass, a point or segment endpoint outside $[0, L]^2$, a
segment of length zero, a nonempty format M `points` list, a format L `net` other than
step $83/40000$ and last index $200$, certificate metadata that changes the net of
either format (finding TI-3), format M’s premise $B(1 + D/(1 - D^2/4)) < 1$ failing
(N3), and a `total_mass` other than the exact sum.
A format M candidate may declare its own uniform net as `proof_net: {step, last}`, with
$D$ = `step` and $N_\theta$ = `last` + 1; without it the net is $83/40000$ and $201$.
The declaration is part of the candidate, not metadata, so TI-3 is unchanged, and a
candidate that carries both is refused.
Lemmas N1 to N3, D and F3 are stated for a general $D$, and admission checks each of
their premises for the declared net exactly as for the default one: $B(1 + D) < 1$, the
tangent form above, $(1 + (N_\theta - 1) D)^2 > 2$ and $(N_\theta - 1) D \le 1/2$.
Every row is an orbit representative whose eight $D_4$ images carry an eighth of its
mass each; coincident images are merged by exact key (a segment and its reverse are one
key), and the merged total must equal $M$.

**Lemma D (domains).** At index $r$ the claim is checked on $[L/2, U_r]^2$ with $U_r = L
- B(c_r + s_r)/2$ (Tokoharu’s domain, formats T and L) or $U_r = L - \rho(a_r)$, $a_r =
  \max(0, t_r - D/2)$, $\rho(a) = (1 + 2a - a^2)/(2(1 + a^2))$ (the per-bin domain,
format M), as spec §1.5 derives; `certificate::domain_upper` computes $U_r$ exactly and
refuses $U_r \le L/2$. The axis sweep at $r = 0$ takes $U_0$ as its upper end, so a
format M sweep stops at $L - 1/2$. Lemma C1 applies unchanged.

**Lemma B1 (classification of atoms).** A point is R1’s rectangle with $w_x = w_y = 0$;
a segment is classified by its bounding box, which contains it.
Inside means inside every closed square of the box, so the atom’s whole mass counts
there and in every sub-box; outside is R1’s strict separation by more than `TAU`, so the
atom meets no square of the box.
A point or segment on a square’s boundary is never certified outside, which keeps the
closed-square convention of spec §1.2: such an atom contributes zero, a lower bound.

**Lemma B2 (points).** A straddling point contributes zero to the box bound.
Points certified inside contribute their enclosure’s lower end.

**Lemma B3 (segments).** For a straddling segment $P(\lambda) = P_0 + \lambda(P_1 -
P_0)$, the code picks binary64 parameters $0 \le \lambda_0 < \lambda_1 \le 1$ by any
means (`rotated::lambda_range`, which solves for the parameters within $h - b_u -
2\tau$ and $h - b_v - 2\tau$ of the box centre along the square’s axes), then proves
$P(\lambda_0)$ and $P(\lambda_1)$ inside every square of the box by R1 with zero extent.
Each square is convex, so the whole piece between them is inside, and mass uniform by
length is uniform in $\lambda$: the segment contributes at least $w(\lambda_1
- \lambda_0)$, rounded down. If either proof fails after a nudge inward, the segment
contributes zero. The points tested are computed in binary64 as $x_0 + \lambda(x_1 -
  x_0)$ from endpoints within a unit in the last place, so they lie within $2 \times
  10^{-12}$ of the exact $P(\lambda)$; with F2’s $3 \times 10^{-11}$ the decision error
  stays below `TAU`. `rotated::segment_dn`. The atom bound of a box is the inherited
  inside mass plus these straddling parts (B0 of spec §1.6: lower bounds of the parts of
  a measure add), and it bounds the atoms’ capture at every centre of the box, so it is
  added to R3’s bound for the rectangles.

**Lemma B5 (which method at $r = 0$).** The vertex sweep (A1, A2) assumes a measure of
rectangles alone. With points or segments present the capture is not bilinear and a
point’s capture is only upper semicontinuous, so direction zero runs the branch and
bound with the axis-aligned square (Z1, Z2) and B1–B3. `lib::run_direction_inner`.

**Lemma Z1 (area at $r = 0$).** For the axis-aligned square, $|R \cap Q(p)| =
o_x(p_x)\, o_y(p_y)$ with $o_x(x) = |[x - h, x + h] \cap [x_1, x_2]|$. With the inner
representable rectangle and $h^- \le h$, the downward-rounded
$\max(0, \min(x + h^-, x_2^\downarrow) - \max(x - h^-, x_1^\uparrow))$ is at most
$o_x(x)$, and so for $o_y$; their downward-rounded product bounds the area.
`rotated::area_dn_axis`.

**Lemma Z2 (derivative at $r = 0$).** Almost everywhere, $\partial_x |R \cap Q(p)| =
o_y(p_y)(\mathbf 1[p_x + h \in (x_1, x_2)] - \mathbf 1[p_x - h \in (x_1, x_2)])$: the
square’s right side gains and its left side loses one unit of $o_x$ per unit moved,
while that side lies within $R$’s abscissa range, and where $o_x = 0$ both indicators
vanish. Over the box each indicator is enclosed by $\{1\}$ when $[p_x \pm h]$ provably
lies in $[x_1, x_2]$ for every $p$ and every $h \in [h^-, h^+]$, by $\{0\}$ when it
provably misses it, and by $[0, 1]$ otherwise; $o_y$ is unimodal in $p_y$, so over the
box it lies between its smaller value at the outward-rounded ends and $\min(2h^+, y_2 -
y_1)$. The interval product, scaled by $\rho$, encloses the derivative; $\partial_y$ is
the same with the axes exchanged.
R3 and R6 then apply unchanged.
`rotated::gradient_axis`.

## Floating Point

**Lemma I1 (directed steps).** Let $z$ be real, $x = \mathrm{fl}(z)$ its
round-to-nearest value (finite), $x^+$ and $x^-$ the adjacent binary64 values above and
below $x$, and

$$
\mathrm{up}(x) = \mathrm{fl}\big(x + \mathrm{fl}(\mathrm{fl}(|x| 2^{-52}) +
2^{-1074})\big),\qquad \mathrm{dn}(x) = \mathrm{fl}\big(x -
\mathrm{fl}(\mathrm{fl}(|x| 2^{-52}) + 2^{-1074})\big).
$$

Then $\mathrm{dn}(x) \le z \le \mathrm{up}(x)$. *Proof.* $z \le x^+$: if $z > x^+$, then
$x^+$ would be nearer to $z$ than $x$. Let $g = x^+ - x$, a power of two.
For normal $x$, $g \le 2^{-52}|x|$ (also for $x =
-2^e$, where $g = 2^{e-53}$); rounding is monotone and $g$ is representable, so
$\delta = \mathrm{fl}(|x| 2^{-52}) \ge g$. For zero or subnormal $x$, $g = 2^{-1074}$.
Either way $\mathrm{fl}(\delta + 2^{-1074}) \ge g$, hence $x + \mathrm{fl}(\delta +
2^{-1074}) \ge x^+$, and by monotonicity $\mathrm{up}(x) \ge \mathrm{fl}(x^+) = x^+ \ge
z$. The lower step is symmetric.
The step is branch-free and may land two values out, which costs a few units in the last
place and nothing in soundness.
`interval::tests::steps_reach_the_adjacent_values` checks $\mathrm{up}(x) \ge x^+$ on
special values and 100,000 random bit patterns.
(The first build used `next_up` and `next_down`; experiment exp-005 replaced them.)
Rust neither fuses multiply-adds nor uses x87, so each `+ - * /` is one correctly
rounded IEEE operation.
Every interval operation in `interval.rs` applies I1 to each endpoint.

**Lemma I2 (enclosing rationals).** `exact::enclose` returns the largest binary64 value
at most $q$ and the smallest at least $q$, decided by exact comparisons of $q$ with $\pm
m 2^e$ (`exact::compare`), so the starting approximation’s accuracy does not matter.

**Lemma F2 (classification slack).** The R1 tests and the edge tests are evaluated in
plain binary64 from approximations within two units in the last place of the exact
centre, half-sizes, $c$, $s$ and $h$. Every operand has magnitude below $4L + 4 \le
4004$ (sides are admitted up to `MAX_SIDE` $= 1000$), and each tested quantity is at
most ten operations deep, so by the standard model $|\mathrm{fl}(a \circ b) - a \circ b|
\le 2^{-53} |a \circ b|$ its absolute error is below $30 \cdot 4004 \cdot 2^{-52} <
3 \times 10^{-11}$, far below `TAU`. Decisions near the slack become boundary items,
which R2–R5 handle soundly.

**Lemma F3 (every intermediate is finite).** Lemma I1 needs every rounded result to be
finite: $\mathrm{dn}(+\infty)$ and $\mathrm{up}(-\infty)$ are `NaN`, and `NaN` fails
every comparison. Admission caps the inputs so that no intermediate on the certification
path exceeds $2^{200}$ in magnitude, far below the binary64 limit $2^{1024}$:

- Coordinates, offsets and half-widths are at most $4L \le 2^{12}$ (`MAX_SIDE`).
- $t_{\max} \le 1/2$ gives $c_r \ge 3/5$; at least two directions and at most $2^{16}$
  with the endpoint polynomial give $D \ge \tan(\pi/8)/2^{16} > 2^{-18}$, so $s_r \ge
  s_1 = 2D/(1 + D^2) > 2^{-18}$ for $r \ge 1$. Every line coefficient ($h/s$, $c/s$,
  $1/(sc)$, …) is then below $2^{19}$, and every term of R5 below $2^{32}$.
- Each expanded density is at most $2^{96}$ and there are at most
  $8 \cdot 10^6 < 2^{23}$ expanded items.
  A rectangle’s R2 area bound is below $2^{49}$ (thirteen trapezoids of width at most
  $2^{12}$ and height at most $2^{33}$), its weighted area below $2^{145}$, its
  derivative enclosure below $2^{130}$; the sums over every item stay below $2^{170}$,
  and the penalty, a derivative bound times a half-width, below $2^{182}$. Masses are
  below $n < 2^{64}$.
- In the axis sweep a column weight $\rho\, o_x$ is below $2^{108}$, a slope below
  $2^{133}$, an increment below $2^{145}$, and a vertex value below $2^{181}$ after at
  most $2^{26}$ events.
- Each directed step multiplies a magnitude by at most $1 + 2^{-51}$ and adds
  $2^{-1074}$, so outward rounding over fewer than $2^{40}$ operations per quantity
  stays within a factor of $2$.

The divisions on the path are by enclosed constants bounded away from zero ($c$, $s$,
and in `lambda_range` a slope at least the smallest normal, whose possibly infinite
quotient is clamped to $[0, 1]$ and only chooses parameters that B3 then proves).
So no infinity arises, and without one no `NaN` can (no $0/0$, no $\infty - \infty$, no
$0
\cdot \infty$). The code also makes `NaN` fatal wherever it could pass unseen: `fmin`
and `fmax` replace `f64::min` and `f64::max` in every interval primitive and in R2, Z1
and Z2, so a `NaN` endpoint propagates rather than being dropped (each selects with one
comparison, which keeps a `NaN` second operand, and adds $0 \cdot a$, which is `NaN`
when the first is `NaN` or infinite); the search checks the centre bound, the atom bound
and the derivative enclosure of every box and stops with `non-finite`; and the axis
sweep refuses a non-finite vertex rather than leaving it out of the minimum (finding S1
of the 3 October soundness review, whose reproducers are in `tests/adversarial.rs`).

## Tests That Hold the Lemmas

- `rotated_tests::area_lower_bound_is_below_and_close_to_exact`: R2 against exact
  rational clipping on random rectangles and directions, below and within $10^{-9}$.
- `rotated_tests::edge_length_enclosures_contain_exact_lengths_over_the_box`: R5 against
  exact rational edge lengths at the corners and interior points of 2,000 random boxes
  over five directions; a seeded wrong endpoint makes it fail.
- `interval::tests::steps_reach_the_adjacent_values`: I1 on special values and 100,000
  random bit patterns.
- `rotated_tests::area_lower_bound_is_below_and_close_to_exact` also runs Z1 at $r =
  0$.
- `rotated_tests::gradient_enclosures_contain_difference_quotients`: R4, R5 and Z2
  against exact difference quotients of the clipped area, which average the derivative
  over an interval inside the box, at $r \in \{0, 1, 77, 200\}$; reversing Z2’s sign
  makes it fail.
- `rotated_tests::atom_bounds_hold_at_every_sampled_centre`: B1–B3 against the exact
  capture of random points and segments (a third horizontal, a third vertical) at the
  corners and an interior point of random boxes, and the counterexample estimate above
  the exact capture at the centre; letting B3 skip its endpoint proofs makes it fail.
- `tests/adversarial.rs`, from the 3 October soundness review: admission against each
  broken premise and exact decimal masses, boundary configurations at side 1000 against
  the oracle, the per-bin fold, and lemma F3: the overflow certificate is refused at
  admission, and with its densities forced past the cap the axis sweep refuses it as
  `non-finite`, whether the overflow is in a column’s initial slope or inside the
  domain; a fault-injected run is never verified.
- `tests/adversarial.rs`, from the 3 October testing review’s findings: a gzip input
  with a second member or trailing bytes is refused; format L and M nets cannot be
  changed by metadata; format M’s tangent-form premise refuses a $B$ between the two
  limits, which format T admits.
- `tests/adversarial.rs`, for the declared net: a format M `proof_net` with step
  $1/1001$ and 416 directions is admitted with the per-bin domain it implies; a declared
  net failing $B(1 + D) < 1$, the endpoint or F3 is refused, as is a malformed
  declaration, one beside net metadata, and one on another format.
- `interval::tests::nan_is_never_dropped`: every interval primitive keeps a `NaN`
  endpoint, and an overflowing directed step is `NaN`.
- `rotated_tests::oracle_counts_closed_intersections`: the oracle counts a point on the
  square’s edge and a segment along it in full, and a segment touching a corner not at
  all.
- The release audit (A3) re-derives sampled boxes’ centre bounds and classifications
  from scratch; `--audit-every 1` re-derives every box’s.
- `devtools/check_sqverify_fast.py` compares, on retained certificates, the probe’s
  centre and box bounds with `sqpack.rectangle_density`’s exact coverage at sampled
  centres and box points, and runs the mutation controls; for formats M and L it
  compares with an exact evaluator of points, segments and rectangles written in the
  tool, apart from the crate’s oracle, and runs the retained mixed and linear controls.
  Its `--quick` subset runs in the gate step `measure verifier Rust (sqverify-fast)`.
- `devtools/sqverify_fast_census.py` verifies every replayed certificate at all 201
  directions and evaluates, in exact rationals, the capture at the centre of each
  certificate’s least-bound leaf; `--family mixed` does the same for formats M and L.

## The First Leg on Its Own Segment

**Lemma R7.** In R3’s path $p_0 \to (p_x, y_0) \to p$, the first leg lies on the segment
$S_x = [x_0 \pm d_x] \times \{y_0\}$, so it needs only $G^S_x \ge \sup_{S_x}
|\partial_x F|$; the second leg needs $G_y$ over the whole box.
Hence $F(p) \ge F(p_0) -
G^S_x d_x - G_y d_y$, and with the other order, $F(p) \ge F(p_0) - G_x d_x - G^S_y d_y$;
the larger of the two lower bounds holds.
$G^S_x$ is R5’s enclosure with the centre’s ordinate fixed at $y_0$ (the segment ends’
offsets enclosed with half-width zero), its abscissa still ranging over the box.
Any bound valid on the box is valid on the segment, so each segment bound is also capped
by the box’s. The current build does not use R7: experiments exp-009, exp-010 and
exp-016 found that it removes about a third of the boxes but costs as much again in
enclosures, eagerly, lazily, or fused with the box’s own enclosures.

## Inheritance of Derivative Bounds

**Lemma R6.** A bound $G_x \ge \sup_C |\partial_x F|$ proved on a box $C$ holds on every
sub-box $C' \subseteq C$. So a child may apply R3 with its parent’s bounds, and with the
smaller of its parent’s and its own, per axis.
Skipping a box’s own enclosure is only a choice of where to spend work: it never accepts
a box (experiment exp-003).

## The Release Audit

**Lemma A3 (what the audit establishes).** At an audited box two things are recomputed
from scratch, with nothing inherited.
First, the centre bound by R2 over every rectangle, with no classification: inside
rectangles enter the incremental sum as their exact mass and the full sum through R2,
which is within rounding of it.
Second, the classification of every rectangle, point and segment against the box (R1,
B1): the mass certified inside and the number of straddling items of each kind.
On a correct run the sums agree to within `AUDIT_TOLERANCE` (relative $10^{-9}$) plus
the representation slack, and the counts exactly.
The slack is, over every rectangle that can meet the centre’s square, its density times
the area between its outer and inner representable rectangles: the incremental sum
counts an inside rectangle by its exact mass, while R2 counts its inner representable
rectangle, and for a sliver of extreme density that difference is large (finding TI-1 of
the 3 October testing review, whose reproducer the audit refused falsely before).
The classification comparison is unaffected, and it is what catches a wrong inside
decision.
The slack also weakens the centre-bound comparison where densities are extreme:
near the $2^{96}$ cap a rectangle’s slack can exceed the bound itself, and there that
comparison cannot see a bookkeeping error (note R2 of the soundness re-review).
No acceptance rests on the audit: it only ever refuses, as defense in depth beside the
lemmas, which carry the proof.
The counts agree exactly because a sub-box’s fresh classification repeats its ancestors’
decisions (a rounding coincidence within $10^{-13}$ of a decision’s slack could break
the tie, which would be a false refusal, never an acceptance); a disagreement proves the
incremental bookkeeping wrong at that box or at an ancestor whose decisions it inherits.
The search then stops with `audit-failed`, a refusal.
The second comparison is what catches a straddling item wrongly certified inside whose
whole mass happens to lie in the centre’s own square, which leaves the centre bound
unchanged and removes only the item’s derivative or its straddling treatment.
The audit covers R1’s and B1’s decisions and their inheritance, not the derivative
enclosures or B3’s parameters, which `rotated_tests` and the differential tests check.
It is sampled (the root and every $K$-th box, $K = 1024$ by default), so a wrong
decision is caught at any audited box where it is still wrong; `--audit-every 1` audits
every box, which catches it at the box where it is made.
`--inject-fault-at-node N` certifies inside the first straddling rectangle at box $N$,
or the first straddling point or segment when no rectangle straddles, the control of
spec §4.2; the controls in `devtools/check_sqverify_fast.py` require the refusal.
A run with the flag is never evidence: every receipt and the summary record
`fault_injected_at_box`, and a direction the injected fault did not stop is reported
`fault-injected`, not `verified`, so the run exits non-zero whatever the audit caught.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
