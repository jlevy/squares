# Proof outline

## Theorem

Let \(s(17)\) be the infimum side length of a square containing seventeen pairwise interior-disjoint unit squares of arbitrary orientations. The bundled certificate proves, conditional only on verifier correctness,

\[
s(17)\ge \frac{9141}{2000}=4.5705.
\]

## Weighted obstruction lemma

Let \(C=[0,S]^2\), and let \(\mu\) be a finite nonnegative atomic measure on \(C\). Assume

\[
\mu(C)<17
\]

and every closed unit square \(Q\subseteq C\) satisfies

\[
\mu(Q)\ge1.
\]

If seventeen unit squares fit in a square of side \(s<S\), embed that smaller container strictly inside \(C\). Apply an arbitrarily small common translation so that no certificate atom lies on any packed-square boundary. The captured atom sets are then disjoint, giving

\[
17\le \sum_{i=1}^{17}\mu(Q_i)\le\mu(C)<17,
\]

a contradiction.

Thus it is enough to verify the two certificate properties at \(S=9141/2000\).

## Exact certificate

The measure has 71 representatives under the dihedral symmetry group of the container and 560 expanded atoms. Coordinates are multiples of \(1/4000\). All weights have denominator \(10^{12}\).

The exact total mass is

\[
\mu(C)=\frac{16994734834452}{10^{12}}
      =\frac{4248683708613}{250000000000}
      =16.994734834452<17.
\]

The exact slack is

\[
17-\mu(C)=\frac{1316291387}{250000000000}
          =0.005265165548.
\]

## Center-space reduction

By square and container symmetry it suffices to consider

\[
0\le\theta\le\frac\pi4.
\]

For an atom \(p=(p_x,p_y)\), rotate coordinates by \(-\theta\):

\[
u_p=p_x\cos\theta+p_y\sin\theta,
\qquad
v_p=-p_x\sin\theta+p_y\cos\theta.
\]

A unit square with rotated center \((u,v)\) captures \(p\) precisely when

\[
|u-u_p|\le\frac12,
\qquad
|v-v_p|\le\frac12.
\]

Thus each atom contributes its weight on an axis-aligned unit rectangle in center space. Coverage is constant on every open cell of the resulting rectangular arrangement. The feasible centers form the rotated image of

\[
\left[\rho(\theta),S-\rho(\theta)\right]^2,
\qquad
\rho(\theta)=\frac{\cos\theta+\sin\theta}{2}.
\]

## Finite orientation partition

The arrangement can change only when an atom boundary swaps order with another atom boundary or meets a boundary feature of the feasible-center square. After scaling coordinates by 4000, every event equation has the form

\[
A_0+A_c\cos\theta+A_s\sin\theta
 +A_2\cos2\theta+B_2\sin2\theta=0
\]

with integer coefficients.

Under

\[
t=\tan(\theta/2),
\]

multiplication by \((1+t^2)^2\) yields an integer polynomial of degree at most four.

The generator produces exactly 1,344,862 primitive event polynomials. An exact Bernstein-sign test on

\[
0\le t\le83/200
\]

proves that 1,194,331 have no relevant interior root. Exact Sturm sequences for the remaining 150,531 polynomials produce 148,936 distinct interior algebraic event roots. Exact polynomial gcds prove that all polynomial roots assigned to one gap are the same algebraic number.

There are therefore 148,937 open orientation cells.

## Exact coverage audit

One exact rational \(t=p/q\) is chosen in every open orientation cell. Then

\[
\cos\theta=\frac{q^2-p^2}{q^2+p^2},
\qquad
\sin\theta=\frac{2pq}{q^2+p^2},
\]

so all transformed atom boundaries, feasible-center boundaries, and separating-axis calculations become integers after a common scaling.

For each sample, the verifier:

1. constructs all center-space rectangle boundaries exactly;
2. accumulates coverage by exact integer range additions;
3. merges all vertically adjacent cells with coverage below \(10^{12}\);
4. proves each such rectangle is strictly outside the feasible-center diamond by one of four exact separating-axis inequalities.

The audit checks all 148,937 cells and 278,950,150 maximal subthreshold runs. No subthreshold run intersects the feasible region.

## Endpoints and event orientations

The orientations \(\theta=0\) and \(\theta=\pi/4\) are checked separately with exact integer and quadratic-integer arithmetic. The minimum axis-aligned open-cell coverage is

\[
1.000300000011.
\]

At \(\theta=\pi/4\), all 700 subthreshold runs lie outside the feasible-center diamond.

At an event angle, a closed unit square can gain atoms lying on its capture boundary but cannot lose atoms relative to the appropriate neighboring open-cell limit. Feasible event configurations are also limits of feasible configurations in adjacent orientation cells. Thus the open-cell audit plus endpoint checks covers the full closed orientation interval.

## Conclusion

The exact measure has mass below 17 and every contained unit square has mass at least 1. By the weighted obstruction lemma,

\[
\boxed{s(17)\ge4.5705}.
\]
