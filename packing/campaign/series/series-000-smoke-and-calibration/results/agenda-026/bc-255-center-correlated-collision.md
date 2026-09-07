# BC255 — A Center-Correlated Collision Region

At $q=1939/500$, the three vertices of the reviewed outer triangle of
distinguished-square centers move by less than $\varepsilon=1/500$ in each world
coordinate throughout the full near45 band.
The same bound holds on the larger closed tangent-half-angle interval used by the
existing instruments.
It gives the fixed center region $C^*$ below: a near-axis square centered there
intersects every admissible distinguished square.

This is a source-free analytical proof prepared under `think-8x6o` on September 7, 2026,
for independent review.
No scientific source, polygon vertices for $C^*$, cover packet, or target invocation was
constructed. Whether adding $C^*$ completes the remaining near-axis cover is untested.

The premises are the
[H124 center-triangle and whole-band kernel reductions](../../../../hypotheses/H-124-full-distinguished-square-compatibility.md#a-stronger-continuous-common-obstacle).
[Exp125](../../experiments/exp-125-h124-complete-residual-cover.md) independently
certified the diagonal-band sufficient cover; its axis producer returned `no_chain`
without a reader invocation.
Neither that receipt nor this proof resolves the remaining cover.

## World-Frame Triangle Vertices

Write

$$
m=q/2,\qquad W=m-1=939/1000,\qquad
r=\sqrt2/2,\qquad k=1+W/2,
$$

and, for the distinguished square’s orientation $\theta$, put

$$
C=\cos\theta,\qquad S=\sin\theta,\qquad
h=(C+S)/2,\qquad \Delta=1-2h+WCS.
$$

Here $S$ denotes the sine.
Denote the second square by $\mathcal S$ below.

The accepted H124 reduction places every admissible distinguished-square center in

$$
K_\theta=\{(x,y):U\le u_*,\ V\le v_*,\ SU+CV\ge h\},
$$

where

$$
U=Cx+Sy,\qquad V=-Sx+Cy,\qquad
u_*=Cm+S-1/2,\qquad v_*=C-S-1/2.
$$

Avoidance of the two closed P10 marks $(1,1)$ and $(m,1)$ gives strict upper
inequalities for $U,V$; the closed triangle is a safe enlargement.
Bottom-wall containment supplies $y=SU+CV\ge h$. The other P10 conditions are not
asserted for every point of this enlarged triangle.

For $C,S>0$, the largest possible value of $SU+CV$ under the two upper bounds is
$Su_*+Cv_*=h+\Delta$. Thus $K_\theta$ is empty when $\Delta<0$, is a singleton when
$\Delta=0$, and otherwise has frame-coordinate vertices

$$
(u_*,v_*),\qquad
(u_*-\Delta/S,v_*),\qquad
(u_*,v_*-\Delta/C).
$$

Applying $(U,V)\mapsto(CU-SV,SU+CV)$ gives the world-frame vertices

$$
\begin{aligned}
v_E(\theta)
 &=\left(1+WC^2+\frac{S-C}{2},\ 1+WCS-h\right),\\
v_L(\theta)
 &=\left(v_{Ex}(\theta)-\cot\theta\,\Delta,\ h\right),\\
v_R(\theta)
 &=\left(v_{Ex}(\theta)+\tan\theta\,\Delta,\ h\right).
\end{aligned}
$$

The second coordinate of $v_E$ is $h+\Delta$, so both other vertices lie on $y=h$. At
$\theta_0=\pi/4$, $C=S=r$ and $\Delta_0=k-2r$. Consequently the nominal vertices are
exactly

$$
v_E^0=(k,k-r),\qquad
v_L^0=(2r,r),\qquad
v_R^0=(m+1-2r,r).
$$

The symbol $v_E$ labels a triangle vertex; the common obstacle $E$ used later is the
separate set $\operatorname{conv}(D\cup K_1)$.

## Uniform Coordinate Displacement

Use the already reviewed endpoint

$$
T=\frac{110880}{50803079},\qquad
\Theta=\{\pi/4+2\arctan t:-T\le t\le T\}.
$$

The [angle-instrument derivation](bc-255-angle-instrument-design.md) proves
$\tan(\pi/1440)<T$, so $\Theta$ contains the whole actual closed near45 band.
Also $360\cdot110880<50803079$, hence $T<1/360$. Throughout $\Theta$, therefore,

$$
d=|\theta-\theta_0|\le2\arctan T<2T<1/180.
$$

All bounds below hold on this entire interval, including both signs and both endpoints.
No midpoint inference or sampled angle is used.

### Trigonometric and denominator bounds

The rational inequalities

$$
\frac{707}{1000}<r<\frac{708}{1000},\qquad
\cos d\ge1-d^2/2,\qquad |\sin(\theta-\theta_0)|\le d
$$

give

$$
\begin{aligned}
C,S
 &>\frac{707}{1000}\left(1-\frac1{64800}-\frac1{180}\right)
 >\frac{703}{1000},\\
C,S
 &<\frac{708}{1000}\left(1+\frac1{180}\right)
 <\frac{89}{125},\\
\frac{353}{500}
 &<\frac{707}{1000}\left(1-\frac1{64800}\right)
 <h\le r<\frac57.
\end{aligned}
$$

In particular, $C$ and $S$ are positive, so every division in the vertex and derivative
formulas is valid. Since $|C-S|=\sqrt2|\sin(\theta-\theta_0)|$ and $\sqrt2<36/25$,

$$
|C-S|<1/125,\qquad |h'|<1/250.
$$

The ratio and reciprocal bounds needed for differentiation are

$$
0<\tan\theta,\cot\theta
 <\frac{712}{703}<\frac{41}{40},\qquad
\sec^2\theta,\csc^2\theta
 <\left(\frac{1000}{703}\right)^2<\frac{81}{40}.
$$

Using $W>9/10$, $C,S>7/10$, $h<708/1000$, and $CS\le1/2$ gives

$$
\frac1{40}
=1-\frac{177}{125}+\frac{441}{1000}
<\Delta
<1-\frac{353}{250}+\frac{939}{2000}
=\frac{23}{400}.
$$

Thus the triangle is nonempty throughout the present enlarged interval.
For reuse outside this domain, an empty $K_\theta$ means there is no admissible
distinguished-square center at that angle; it must be handled as a vacuous branch, not
as the convex hull of three formal vertex expressions.
The singleton case uses one repeated vertex and needs no division by $\Delta$.

### Derivative bounds

Differentiating the exact expressions yields

$$
\begin{aligned}
v_{Ex}'&=h-2WCS,\\
v_{Ey}'&=(C-S)\left(W(C+S)-\frac12\right),\\
\Delta'&=(C-S)\left(W(C+S)-1\right),\\
v_{Lx}'&=v_{Ex}'+\csc^2\theta\,\Delta-\cot\theta\,\Delta',\\
v_{Rx}'&=v_{Ex}'+\sec^2\theta\,\Delta+\tan\theta\,\Delta',\\
v_{Ly}'&=v_{Ry}'=h'.
\end{aligned}
$$

First, $2WCS>441/500>5/7>h$, so $v_{Ex}'<0$ and

$$
|v_{Ex}'|=2WCS-h<W-\frac{353}{500}=\frac{233}{1000}.
$$

Next, $7/5<C+S<10/7$ gives

$$
0<W(C+S)-1<\frac{239}{700}<\frac7{20},\qquad
0<W(C+S)-\frac12<\frac{589}{700}<\frac78.
$$

It follows that

$$
|\Delta'|<\frac7{2500},\qquad
|v_{Ey}'|<\frac7{1000}.
$$

For either bottom vertex, the triangle inequality now gives the exact rational bound

$$
\begin{aligned}
|v_{Lx}'|,|v_{Rx}'|
&<\frac{233}{1000}
  +\frac{81}{40}\frac{23}{400}
  +\frac{41}{40}\frac7{2500}\\
&=\frac{140923}{400000}<\frac9{25}.
\end{aligned}
$$

Every other coordinate derivative is also smaller than $9/25$ in absolute value.
The mean value theorem along the interval between $\theta_0$ and $\theta$ therefore
proves

$$
\boxed{\quad
\|v_i(\theta)-v_i^0\|_\infty
<\frac9{25}\frac1{180}
=\frac1{500}=\varepsilon,
\qquad i\in\{E,L,R\},\quad\theta\in\Theta.
\quad}
$$

At $\theta=\theta_0$ the displacement is zero.
The same fixed epsilon covers both signs; it was not selected by a radius sweep.

## A Fixed Region of Guaranteed Collision Centers

Let $R_\eta$ denote rotation through $\eta$ and let $U_\eta=R_\eta[-1/2,1/2]^2$ be the
centered closed unit-square kernel.
For a near-axis orientation $\psi\in\{2\arctan t:-T\le t\le T\}$, a square
$\mathcal S=z+U_\psi$ intersects the square $v+U_\theta$ exactly when

$$
z\in v+U_\theta+U_\psi,
$$

because $U_\psi$ is centrally symmetric.
For nonempty $K_\theta$, convexity gives

$$
\mathcal C_{\theta,\psi}
:=\bigcap_{v\in K_\theta}(v+U_\theta+U_\psi)
=\bigcap_{i\in\{E,L,R\}}(v_i(\theta)+U_\theta+U_\psi).
$$

Indeed, if $z-v_i$ lies in the convex set $U_\theta+U_\psi$ for each vertex, then
$z-\sum_i\lambda_i v_i=\sum_i\lambda_i(z-v_i)$ lies there for every convex combination.
The reverse inclusion follows because the vertices belong to $K_\theta$. For empty
$K_\theta$, the universal collision condition is vacuous and the intersection over no
centers is the whole plane.

Use the existing whole-band inner kernels

$$
\alpha=\frac{1+T^2}{2(1+2T-T^2)},\qquad
B_0=[-\alpha,\alpha]^2,\qquad
B_{\pi/4}=R_{\pi/4}[-\alpha,\alpha]^2,
$$

and put $M^*=B_{\pi/4}+B_0$. Its definition has positive denominators: $0<T<1/3$ implies
$1+2T-T^2>0$.

For an angular offset with $|t|\le T$, the required projection factor is

$$
f(|t|)=\frac{1+2|t|-t^2}{1+t^2},\qquad
f'(s)=\frac{2(1-2s-s^2)}{(1+s^2)^2}>0\quad(0\le s\le T<1/3).
$$

Hence $\alpha f(|t|)\le\alpha f(T)=1/2$. This proves $B_{\pi/4}\subseteq U_\theta$ and
$B_0\subseteq U_\psi$ for both enlarged closed angle bands, and consequently

$$
M^*\subseteq U_\theta+U_\psi.
$$

For $n=(n_x,n_y)$, write $h_A(n)=\sup_{a\in A}n\cdot a$ for a support function.
The complete set of outward facet directions of $M^*$ is

$$
\mathcal N=\{\pm(1,0),\ \pm(0,1),\ \pm(1,1),\ \pm(1,-1)\}.
$$

These normals are not normalized.
The support function is

$$
h_{M^*}(n)
=\alpha(|n_x|+|n_y|)
+\alpha r\bigl(|n_x+n_y|+|n_y-n_x|\bigr).
$$

It equals $\alpha(1+\sqrt2)$ on the four axis normals and $\alpha(2+\sqrt2)$ on the four
diagonal normals. A Minkowski sum of two convex polygons has only facet directions from
the summands: between consecutive such directions, each summand’s maximizing vertex is
constant. Thus these eight support inequalities describe all of $M^*$, including its
boundary.

Define the fixed closed set

$$
\boxed{\quad
C^*=\bigcap_{n\in\mathcal N}
\left\{z:n\cdot z\le
h_{M^*}(n)+\min_{i\in\{E,L,R\}}n\cdot v_i^0
-\varepsilon\|n\|_1\right\}.
\quad}
$$

The minimum retains every nominal vertex, including ties.
Equivalently, retain all 24 inequalities, one for each pair $(i,n)$. The subtraction is
$\varepsilon$ for an axis normal and $2\varepsilon$ for a diagonal normal.

For every $i,n,\theta$, the displacement theorem gives

$$
n\cdot v_i(\theta)
\ge n\cdot v_i^0-\varepsilon\|n\|_1
\ge\min_j n\cdot v_j^0-\varepsilon\|n\|_1.
$$

If $z\in C^*$, subtracting this inequality from the corresponding bound on $n\cdot z$
proves $n\cdot(z-v_i(\theta))\le h_{M^*}(n)$. The complete support description implies
$z-v_i(\theta)\in M^*$. Therefore

$$
C^*\subseteq
\bigcap_i(v_i(\theta)+M^*)
\subseteq\mathcal C_{\theta,\psi}
$$

for every pair of orientations in the enlarged bands.
In particular, every contained near-axis square centered in $C^*$ intersects every
admissible H124 distinguished square.
Tangency counts as intersection; this argument supplies no positive overlap or uniform
clearance claim.

## The Remaining Cover Obligation

$C^*$ is a region of second-square centers.
It is not asserted to lie inside Q and must be appended directly to the center cover,
without adding $B_0$ to it again.

Preserve the original 13 regions and their exact source definitions from H124: $E+B_0$,
the nine unchanged $p+B_0$ regions, and the three closed marked-corner patches.
With $Z_0=[1/2,q-1/2]^2$, the changed sufficient obligation is

$$
Z_0\subseteq
(E+B_0)\ \cup\ \bigcup_{p\in P_9}(p+B_0)
\ \cup R_B\cup R_D\cup R_F\ \cup C^*.
$$

There is no unmarked bottom-left patch.
The triangle forgets anchor information used to prove $D\subseteq Q$, so this argument
does not assert that $C^*$ contains the original $E+B_0$ region.
Appending preserves both valid collision mechanisms.

For any contained near-axis $\mathcal S$ avoiding all nine marks, the marked regions and
corner patches are unavailable.
A complete cover would therefore place its center either in $E+B_0$ or in $C^*$, each of
which forces intersection with Q. Together with exp125’s accepted diagonal-band lemma,
this would prove H124; H106, H123, and the reviewed closed-core counting reduction would
then prove restricted H036. It would not improve the unrestricted packing bound.

No vertices or positive-area assertion for $C^*$ have been computed here.
Source construction must retain the full eight-direction intersection and exact field
embedding, handle an empty or lower-dimensional result explicitly, and preserve all
original regions. The existing generic positive-area polygon reader cannot silently
accept or discard a degenerate added region.
A future implementation needs source-free controls, independent source reconstruction,
and a committed prospective protocol before any changed axis cover.
The completed exp125 calls remain terminal.
Failure of this sufficient cover would leave H124 unresolved, not refute it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
