# BC-255: Uniform Vertex Displacement Review

The coordinate displacement bound $\varepsilon=1/500$ is proved for all three formal
triangle vertices throughout the actual closed near-45 angle band.
The derivative estimates below give the stronger bound $1/720$. They also justify the
fixed collision region $C^*$ defined below.
This review does not construct that region, evaluate a scientific source, or prove its
remaining nine-mark cover.

This is the independent mathematical review under `think-rit7`. The companion author’s
new note was not read.
The retained inputs are
[H124’s triangle geometry](../../../../hypotheses/H-124-full-distinguished-square-compatibility.md#a-stronger-continuous-common-obstacle)
and its
[whole-band inner kernels](../../../../hypotheses/H-124-full-distinguished-square-compatibility.md#a-continuous-cover-contract-not-two-angle-samples).
The declared allocation begins at 10:49:11 UTC on September 7, 2026, and ends at
11:14:11 UTC. The first sampled clock was 10:52:44 UTC; reasoning had already begun.
Proof and formatting checks completed at 11:00:29 UTC, 678 seconds after dispatch.
This conservative interval includes the reasoning before the first clock sample.

## Coordinates and Denominator Bounds

Put

$$
W=939/1000,\quad m=1+W,\quad k=1+W/2,\quad r=\sqrt2/2,
$$

and write $C=\cos\theta$, $S=\sin\theta$, $h=(C+S)/2$ and $\Delta=1-2h+WCS$. The frame
bounds are $u_*=Cm+S-1/2$ and $v_*=C-S-1/2$. The angle satisfies

$$
\theta=\pi/4+\delta,\qquad |\delta|\le\pi/720<1/180.
$$

All vertex coordinates below are in the original container frame.
The frame coordinates in H124 are $(U,V)=R_{-\theta}(x,y)$; they must be rotated back
before being compared with these nominal points or added to fixed world-frame kernels.
The three formal world-frame vertices are

$$
\begin{aligned}
v_E&=\left(1+WC^2+\frac{S-C}{2},\ 1+WCS-h\right),\\
v_L&=\left(v_{E,x}-\frac CS\Delta,\ h\right),\\
v_R&=\left(v_{E,x}+\frac SC\Delta,\ h\right).
\end{aligned}
$$

These follow by applying $R_\theta$ to $(u_*,v_*)$, $(u_*-\Delta/S,v_*)$ and
$(u_*,v_*-\Delta/C)$. At $\theta=\pi/4$ they are exactly

$$
v_E^0=(k,k-r),\qquad v_L^0=(2r,r),\qquad
v_R^0=(m+1-2r,r).
$$

The rational inequalities $707/1000<r<708/1000$ follow by squaring positive numbers.
Since sine and cosine have derivatives of absolute value at most one,

$$
\frac7{10}
<\frac{707}{1000}-\frac1{180}
<C,S
<\frac{708}{1000}+\frac1{180}
<\frac{18}{25}.
$$

In particular, $C$ and $S$ stay positive and bounded away from zero, and $7/10<h<18/25$.
All differentiations and divisions below are valid on the entire angle interval.
Also $9/10<W<19/20$, $CS\le1/2$, and

$$
h'=\frac{C-S}{2}=-r\sin\delta,\qquad |h'|<1/180.
$$

## Uniform Coordinate Derivatives

For the upper vertex,

$$
v_{E,x}'=h-2WCS.
$$

Its sign is negative: $2WCS>2(9/10)(7/10)^2=441/500>18/25>h$. Consequently,

$$
|v_{E,x}'|=2WCS-h\le W-h<\frac{19}{20}-\frac7{10}=\frac14.
$$

The vertical derivative is

$$
v_{E,y}'=W\cos(2\theta)-h'.
$$

Since $\cos(2\theta)=-\sin(2\delta)$, $W<1$ and $r<1$,

$$
|v_{E,y}'|\le 2W|\delta|+r|\delta|<3/180=1/60.
$$

For the left vertex, use its defining equations $y=h$ and $-Sx+Ch=C-S-1/2$ to remove the
apparent dependence on $W$:

$$
v_{L,x}=1+\frac CS(h-1)+\frac1{2S}.
$$

Differentiating gives

$$
v_{L,x}'=\frac{1-C-S/2}{S^2}+\frac CS h'.
$$

The numerator in the first term lies between $-2/25$ and $-1/20$. Thus

$$
|v_{L,x}'|
<\frac{2/25}{49/100}+\frac{36}{35}\frac1{180}
=\frac8{49}+\frac1{175}
=\frac{207}{1225}<\frac15.
$$

The identity

$$
v_{R,x}(\theta)=m+1-v_{L,x}(\pi/2-\theta)
$$

follows because reflection exchanges $C$ and $S$, leaves $\Delta$ unchanged, and
$v_{E,x}(\theta)+v_{E,x}(\pi/2-\theta)=m+1$. The reflected angle remains in the same
band, so $|v_{R,x}'|<1/5$. Both lower vertices have vertical coordinate $h$, whose
derivative was bounded above.

Every coordinate derivative therefore has absolute value less than $1/4$. The mean value
theorem, on the interval between $\theta$ and $\pi/4$, proves

$$
\boxed{\ \|v_i(\theta)-v_i^0\|_\infty
<\frac14\frac1{180}=\frac1{720}<\frac1{500}=\varepsilon,
\qquad i\in\{E,L,R\}.\ }
$$

This includes both angle signs and the actual band endpoints.
The bound concerns motion of three formal vertices with orientation.
It is not a uniform clearance between hypothetical packed squares or their closed unit
cores.

## Empty Triangles and Closed Boundaries

H124’s outer center set has constraints $U\le u_*$, $V\le v_*$ and $SU+CV\ge h$, with
$Su_*+Cv_*-h=\Delta$. Positive $C,S$ imply that it is empty when $\Delta<0$, a singleton
when $\Delta=0$, and the closed triangle with the three stated vertices when $\Delta>0$.

The displacement estimates remain valid for the formal formulas in all these cases.
A canonical P10 avoider must satisfy the stricter inequalities $U<u_*$ and $V<v_*$, so
no such avoider exists when $\Delta\le0$. The H124 implication is then vacuous.
No positivity test at a sampled angle is needed for this case distinction.

When the triangle is nonempty, checking its vertices is sufficient for the collision
argument below because its other centers are convex combinations of them.
All collision and support inequalities are closed; an edge or point contact counts as
intersection. Failure of an outer-triangle condition does not supply an actual
P10-avoiding square.

## Fixed Support Bounds and the Collision Implication

Let $U_\gamma=R_\gamma[-1/2,1/2]^2$ be a centered closed unit-square kernel.
Use the retained constants

$$
T=\frac{110880}{50803079},\qquad
\alpha=\frac{1+T^2}{2(1+2T-T^2)},\qquad
B_0=[-\alpha,\alpha]^2,\qquad B_{45}=R_{\pi/4}B_0.
$$

The retained angle enclosure gives $\tan(\pi/1440)<T$, and $0<T<1/3$. Consequently
$1+2T-T^2>0$ and $\alpha>0$. For the absolute offset $d$ from either central frame, put
$t=\tan(d/2)$. Then $0\le t\le T$, and

$$
\cos d+\sin d=\frac{1+2t-t^2}{1+t^2},\qquad
\frac{d}{dt}\frac{1+2t-t^2}{1+t^2}
=\frac{2(1-2t-t^2)}{(1+t^2)^2}>0.
$$

The last sign holds even on $[0,1/3]$. The maximum projection of the corresponding inner
square is therefore $\alpha(\cos d+\sin d)\le1/2$. Hence $B_{45}\subseteq U_\theta$ for
every near-45 angle $\theta$, and $B_0\subseteq U_\psi$ for every near-axis angle
$\psi$.

Set $M_*=B_{45}+B_0$. It is the convex Minkowski sum of two centrally symmetric squares.
Its eight facet normals can be taken without normalization as

$$
N=\{\pm(1,0),\ \pm(0,1),\ \pm(1,1),\ \pm(1,-1)\}.
$$

For $n=(n_x,n_y)$, its support function, the maximum of $n\cdot x$ over $x\in M_*$, is

$$
H_*(n)=\alpha\|n\|_1+\alpha\sqrt2\|n\|_\infty.
$$

This follows by adding the support functions of $B_0$ and $B_{45}$. The normals listed
above are complete because every edge of a polygon Minkowski sum is parallel to an edge
of one of its summands.
Thus $M_*=\{x:n\cdot x\le H_*(n)\text{ for every }n\in N\}$.

The coordinate displacement bound gives, for every listed normal and vertex,

$$
n\cdot v_i(\theta)\ge n\cdot v_i^0-\varepsilon\|n\|_1.
$$

Define the fixed closed region

$$
C^*=\left\{z:
n\cdot z\le H_*(n)+\min_{i\in\{E,L,R\}}n\cdot v_i^0
-\varepsilon\|n\|_1\quad\text{for every }n\in N\right\}.
$$

The axis support values are $\alpha(1+\sqrt2)$, with penalty $\varepsilon$. The
unnormalized diagonal support values are $\alpha(2+\sqrt2)$, with penalty
$2\varepsilon$. Rescaling a normal requires rescaling both its support and its penalty.
In particular, using only $\varepsilon$ on an unnormalized diagonal is not justified by
the coordinate bound.

For $z\in C^*$ and every $i,n$,

$$
n\cdot(z-v_i(\theta))
\le H_*(n)+\min_j n\cdot v_j^0-n\cdot v_i^0
\le H_*(n).
$$

Therefore $z-v_i(\theta)\in M_*$ for all three vertices.
If an actual Q center is $a=\sum_i\lambda_i v_i(\theta)$, convexity gives
$z-a=\sum_i\lambda_i(z-v_i(\theta))\in M_*$. Write this difference as $b_{45}+b_0$ with
$b_{45}\in B_{45}$ and $b_0\in B_0$. Then

$$
a+b_{45}=z-b_0\in(a+U_\theta)\cap(z+U_\psi),
$$

where central symmetry supplies $-b_0\in B_0$. Thus a near-axis square centered in $C^*$
intersects every admissible distinguished Q. Its point of intersection may depend on Q.

This proves the fixed collision region’s sufficient meaning, including its boundary.
It does not prove that $C^*$ is nonempty, maximal, or large enough to complete the
remaining cover. Appending a correctly reconstructed $C^*$ to the existing thirteen
regions preserves those regions’ separate proofs and does not require a claim that $C^*$
contains the old obstacle dilation.
Any cover invocation and its independent source-bound replay still require a separately
committed prospective allocation.

No scientific constructor, coordinate evaluation, sign sweep, target check or test was
run during this review.
No companion author file was inspected.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
