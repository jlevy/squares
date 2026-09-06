# BC-242 Full-Size Density Proof Contract

Status: **author draft complete, with a self-contained weak-duality derivation;
source-distinct theorem review, strong duality, attainment, a singular-mass extension, a
continuum primal certificate, and every numerical BC-243 result remain open.**

This packet supplies BC-242’s (`think-9xxh`) author draft at theorem-contract scope;
coordinator and source-distinct review disposition remain open.
It fixes which finite objects have valid lower- or upper-bound semantics before any
density value is interpreted.
It neither runs BC-243 nor proves a global eleven-square packing theorem.

## Frozen scope and inputs

- Official T+0: `2026-09-06T03:31:00Z`.
- Launch commit: `c55726e1e885227f63110131c0a914665175ff89`.
- Preregistration commit: `f1b6c641e8d3a2fea39cf5aa5292cb8fc1221772`.
- Agenda 026 SHA-256:
  `096470755cb056d6dcd9d103d4233819d03f8bff9035e1027d213ca51ab4cb49`.
- Frozen Trump witness SHA-256:
  `3b4eae938c37c13af6252ac5d83fa99aa95f6b1627b99920c5df8be94c56bea9`.
- Frozen BC-199 result SHA-256:
  `db124b9956d8051682388cbba3b16772e65406a0003debba1c92b915c0c489a8`.
- Frozen exp-013 result SHA-256:
  `60a4b7c48034b37063509a8a641974ed5eae86dccd056e9cbc6cf2fd7f2f0661`.

The exact Trump placement supplies a retained dual control of mass eleven.
It is an input to the pilot contract, not evidence that a mass-eleven primal density
exists or that all compatible eleven-tuples have been classified.

## Placement space and primal

Fix a side length \(L>0\). Let

\[
C_L=[0,L]^2,\qquad Q=[-1/2,1/2]^2,
\]

and let \(\mathbb T_4=\mathbb R/(\pi/2)\mathbb Z\) be the compact angle quotient for a
square. A placement \(p=(c,\theta)\) represents the closed unit square

\[
S_p=c+R_\theta Q.
\]

The admissible placement space is

\[
P_L=\{(c,\theta)\in C_L\times\mathbb T_4:S_p\subseteq C_L\}.
\]

The four corner-containment inequalities are continuous in \((c,\theta)\), so \(P_L\) is
a closed subset of the compact space \(C_L\times\mathbb T_4\). Thus \(P_L\) is compact.
No optimizer-attainment claim follows from that fact alone.

For \(\rho\in L^1_+(C_L)\), define

\[
F_\rho(p)=\int_{S_p}\rho(x)\,dx
\]

and the absolutely continuous covering value

\[
\tau_{\mathrm{ac}}(L)=
\inf\left\{
\int_{C_L}\rho(x)\,dx:
\rho\in L^1_+(C_L),\ F_\rho(p)\geq1\text{ for every }p\in P_L
\right\}.
\]

The normalization is one unit of density mass on every closed full-size placement.
Square boundaries are Lebesgue null, so changing a representative of \(\rho\) on a null
set changes neither feasibility nor objective value.
For \(L\geq1\), the constant density \(\rho\equiv1\) is feasible and has mass \(L^2\);
for \(L<1\), \(P_L\) is empty and the value is zero.
Thus the Trump-side application has a nonempty finite primal problem.

The coverage functional is continuous on \(P_L\). Indeed, if \(p_k\to p\), then the
Lebesgue area of \(S_{p_k}\mathbin\triangle S_p\) tends to zero.
Absolute continuity of the \(L^1\) integral gives

\[
|F_\rho(p_k)-F_\rho(p)|
\leq\int_{S_{p_k}\mathbin\triangle S_p}\rho(x)\,dx\longrightarrow0.
\]

This continuity supports a compact pose-cover proof, but it does not turn a finite
sample into a continuum certificate.

## Almost-everywhere dual and weak duality

Let \(w\) be a finite nonnegative Borel measure on \(P_L\). Its closed-square overlap
depth is

\[
d_w(x)=\int_{P_L}\mathbf 1_{S_p}(x)\,dw(p).
\]

The incidence relation \(\{(x,p):x\in S_p\}\) is closed, hence the integrand is Borel
measurable. Call \(w\) dual-feasible when

\[
d_w(x)\leq1\quad\text{for Lebesgue-almost-every }x\in C_L.
\]

Define

\[
\nu_{\mathrm{ae}}(L)=
\sup\{w(P_L):w\text{ is dual-feasible}\}.
\]

### Weak-duality theorem

For every primal-feasible \(\rho\) and dual-feasible \(w\),

\[
w(P_L)\leq\int_{C_L}\rho(x)\,dx.
\]

Consequently \(\nu_{\mathrm{ae}}(L)\leq\tau_{\mathrm{ac}}(L)\).

**Proof.** Primal feasibility, nonnegativity, and Tonelli’s theorem give

\[
\begin{aligned}
w(P_L)
&\leq\int_{P_L}F_\rho(p)\,dw(p)\\
&=\int_{C_L}\rho(x)
   \left(\int_{P_L}\mathbf 1_{S_p}(x)\,dw(p)\right)dx\\
&=\int_{C_L}\rho(x)d_w(x)\,dx\\
&\leq\int_{C_L}\rho(x)\,dx.
\end{aligned}
\]

All integrands are nonnegative, so no unproved integrability interchange is hidden in
the argument. \(\square\)

An interior-disjoint packing \(p_1,\ldots,p_m\) yields the atomic measure
\(w=\sum_i\delta_{p_i}\). Outside the finite union of square boundaries, at most one
closed square contains any point.
That union is Lebesgue null, so \(w\) is dual-feasible and has mass \(m\). In
particular, the exact Trump placement supplies the retained lower bound

\[
11\leq\nu_{\mathrm{ae}}(L_{\mathrm{Trump}})
\leq\tau_{\mathrm{ac}}(L_{\mathrm{Trump}}).
\]

This is why `packing/src/sqpack/fractional/ceiling.py`’s pointwise closed-set depth
checker is not a verifier for this dual: it intentionally rejects touching squares,
whereas the theorem ignores only the proved null union of their edges and corners.
It must not be weakened or relabelled; BC-243 needs a separate a.e.-depth instrument.

## Conditional equality consequences

No strong-duality or optimizer-attainment theorem is asserted.
If, in a later result, a primal optimizer \(\rho\) and a dual optimizer \(w\) exist and
have equal objective value, use the exact gap decomposition

\[
\begin{aligned}
\int_{C_L}\rho\,dx-w(P_L)
&=\int_{C_L}\rho(1-d_w)\,dx\\
&\quad+\int_{P_L}(F_\rho-1)\,dw.
\end{aligned}
\]

Both terms on the right are nonnegative, so they vanish separately and give

\[
F_\rho(p)=1\quad w\text{-almost everywhere},
\qquad
\rho(x)(1-d_w(x))=0\quad\text{almost everywhere}.
\]

For the unit-atomic Trump dual these conditions say that each of the eleven retained
placements has coverage exactly one and that \(\rho\) vanishes almost everywhere off the
saturated union.
They do not determine \(\rho\), exclude another compatible eleven-tuple,
or prove the equality classification required by BC-244.

Conversely, any packing of eleven interior-disjoint unit squares forces every
primal-feasible density to have mass at least eleven: sum the eleven coverage
inequalities and use the fact that their overlaps are boundary-null.
Therefore a certified primal mass below eleven would contradict the retained exact
packing and would expose an error in the certificate or frozen inputs.

## Singular measures and boundary charges

The weak-duality argument above is deliberately restricted to \(\rho(x)\,dx\). Suppose a
later variant admits a finite nonnegative Borel measure \(\mu\) on \(C_L\), with primal
constraints \(\mu(S_p)\geq1\). Tonelli then uses the closed depth against \(\mu\):

\[
\int_{P_L}\mu(S_p)\,dw(p)=\int_{C_L}d_w(x)\,d\mu(x).
\]

Thus the same uncorrected weak-duality inequality is valid only after certifying
\(d_w\leq1\) \(\mu\)-almost everywhere.
A Lebesgue-a.e. depth certificate does not provide that fact.

If an instrument certifies only the open-interior depth

\[
d_w^\circ(x)=\int_{P_L}\mathbf 1_{\operatorname{int}S_p}(x)\,dw(p)\leq1
\quad\mu\text{-almost everywhere},
\]

then the exact identity is

\[
\int_{P_L}\mu(S_p)\,dw(p)
=\int_{C_L}d_w^\circ(x)\,d\mu(x)+B(\mu,w),
\]

where

\[
B(\mu,w)=\int_{P_L}\mu(\partial S_p)\,dw(p)\geq0.
\]

It yields only \(w(P_L)\leq\mu(C_L)+B(\mu,w)\). Recovering the desired bound requires an
exact proof that the boundary term is zero, such as \(\mu(\partial S_p)=0\) for every
admissible placement, or a separately stated and verified replacement inequality.
Wall-supported or other singular mass can charge square boundaries, so it is refused by
this contract absent that theorem.

## Wall strata and stationarity

Write the placement-space containment constraints locally as \(h_k(p)\geq0\). If
\(\rho\) is primal-feasible and \(F_\rho(p)=1\), then \(p\) is a global, hence local,
minimum of \(F_\rho\) on \(P_L\). If additional regularity makes \(F_\rho\)
differentiable on a selected feature branch, its first-order condition has the form

\[
\nabla F_\rho(p)-\sum_{k\in A(p)}\lambda_k\nabla h_k(p)=0,
\qquad \lambda_k\geq0,
\]

subject to the applicable constraint qualification; without that qualification the
corresponding Fritz–John form is required.
Hence the derivative belongs to the cone generated by active wall rows.
At a wall placement it need not be zero in the ambient centre-angle coordinates.

On a fixed trigonometric sign branch, put \(r(\theta)=(|\cos\theta|+|\sin\theta|)/2\)
and use

\[
h_\ell=c_x-r,\quad h_r=L-c_x-r,\quad
h_b=c_y-r,\quad h_t=L-c_y-r.
\]

The centre and angle equations are then

\[
\partial_{c_x}F_\rho=\lambda_\ell-\lambda_r,
\qquad
\partial_{c_y}F_\rho=\lambda_b-\lambda_t,
\qquad
\partial_\theta F_\rho=-r'(\theta)
(\lambda_\ell+\lambda_r+\lambda_b+\lambda_t),
\]

with inactive-wall multipliers zero.
At trigonometric or density-feature ties these smooth equations are replaced by the
retained branch or nonsmooth condition below.

For a piecewise density, wall, density-cell, vertex, and edge ties can make \(F_\rho\)
nonsmooth. A valid certificate must retain every tied feature branch or use a proved
nonsmooth Fritz–John or Clarke condition.
The \(L^1\) formulation alone supplies continuity, not differentiability or
stationarity.

## Certified finite objects

### Exact dual lower object

A finite dual record consists of exact placements \(p_i\in P_L\) and exact weights
\(a_i\geq0\). Its value is \(D=\sum_i a_i\). It is a certified lower bound only when an
exact arrangement certificate proves

\[
\sum_i a_i\mathbf 1_{S_{p_i}}(x)\leq1
\]

on every full-dimensional cell of the square-edge arrangement.
The ignored set must be identified as the finite union of arrangement edges and vertices
and proved Lebesgue null.
Exact containment of each placement is also part of the certificate.
Under those conditions, \(D\leq\nu_{\mathrm{ae}}(L)\leq\tau_{\mathrm{ac}}(L)\).

A nested sequence of such finite families gives monotone nondecreasing lower values only
when the old feasible record embeds unchanged in the new family.
Floating overlap tests, point samples, and a pointwise closed-depth refusal have no
substitute semantics.

### Globally covered primal upper object

A finite primal record specifies a nonnegative integrable density, its exact or
outward-rounded mass \(U\), and a finite exhaustive cover of \(P_L\). Every interior
pose box and every lower-dimensional wall stratum must carry a rigorous lower enclosure
for \(F_\rho\) whose endpoint is at least one.
The enclosure record must state its interval or Lipschitz direction and the hypotheses
used to cross density-cell feature changes.
If one box or stratum is open, \(U\) is not an upper bound.

A density satisfying only sampled placement constraints is a proposer.
The exact infimum obtained by dropping continuum constraints while leaving the density
class unchanged is at most \(\tau_{\mathrm{ac}}(L)\). A practical finite model usually
also restricts the density class, so its sampled optimum has no direction relative to
\(\tau_{\mathrm{ac}}(L)\) without another argument.
In either case, the returned sampled density is not primal-feasible and its mass is
never a certified upper endpoint.
A nested family of globally certified density classes can give monotone nonincreasing
upper values; changing bases, meshes, or unverified coverage guards carries no
monotonicity claim.

## BC-243 pilot contract

BC-243 remains blocked in this commissioning block because the tree has neither a new
exact a.e.-depth arrangement verifier nor a continuum primal-coverage guard.
The smallest later pilot must use the exact Trump side and perform these independent
checks:

1. Seed the dual with the exact eleven-atom Trump packing and recover \(D=11\). Accept
   edge and corner touching as the refusal control against pointwise closed-depth
   semantics. Perturb a wall-touching placement atom across containment and require
   rejection; perturb an interior placement atom to create positive-area overlap and
   require rejection; reject an overweight full-dimensional arrangement cell; and verify
   every exact containment row.
2. Fit or propose a finite density without assigning upper-bound semantics.
   Include a negative control that passes the sampled constraints but fails a known
   unsampled placement.
   Reject both wall-supported and interior atomic primal mass as outside the absolutely
   continuous measure class unless a separate boundary theorem has first opened the
   singular variant.
3. Attempt a continuum cover over all interior pose boxes and wall strata.
   Report a certified \(U\) only if every pose box or stratum has a certified coverage
   lower endpoint of at least one; otherwise report the one-sided bound \([D,\infty)\)
   when \(D\) itself is valid.
4. Report \([D,U]\) only when both certificates are independently valid.
   Preserve exact values and outward-rounded displays separately.

The exact decision rules are:

- any sound \(D>11\) kills the mass-eleven equality route immediately;
- a weak-duality failure, boundary-semantics failure, or control that fails to reject
  its mutation gives disposition `unsound`;
- a sound one-sided result, or a sound upper endpoint with \(U-11>1/4\) at the
  predeclared priced resolution, gives `sound but quantitatively weak`;
- only a sound interval with the Trump lower control \(D=11\), a genuine continuum upper
  endpoint \(U\leq45/4\), and all controls passing is `close enough to request
  BC-244`.

The final label opens nothing by itself; BC-243 needs a coordinator gate after this
contract is reviewed and committed.

## Draft-satisfied and open obligations

Supplied in this author draft:

- compactness of the placement space;
- continuity of coverage for absolutely continuous \(L^1\) densities;
- the Lebesgue-a.e. dual convention and weak-duality proof;
- the validity of an interior-disjoint exact packing as an atomic dual;
- conditional equality consequences without a classification claim;
- the boundary correction required by a singular-measure variant;
- the directions of exact finite dual and continuum-certified primal approximations;
- the wall normal-cone requirement and BC-243 accept or kill semantics.

Open:

- strong duality and primal or dual attainment;
- any admissible singular or wall-supported primal theorem;
- construction of the a.e.-depth verifier and continuum coverage guard;
- every numerical BC-243 pilot value;
- existence of a mass-eleven density and the BC-244 equality classification;
- any global conclusion about eleven squares in the Trump container.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
