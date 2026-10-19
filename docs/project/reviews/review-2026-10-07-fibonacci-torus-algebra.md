# Fibonacci Torus: Independent Algebra Audit

The user-supplied abstract, *The Fibonacci Geometry of Eleven Squares* (Pingyou Ltd),
has several algebraic claims that can be proved without its missing manuscript.
The [retained checker](../../../packing/cases/fibonacci_torus/algebra.py) verifies the
finite calculations below using exact arithmetic.
Its reconstructed cover does not establish that the pictured packing has that cover.
The existing record already establishes
[optimality at eleven](../../../packing/frontier/n-011.md);
[seventeen remains open](../../../packing/frontier/n-017.md).

## Quotients and the Unique Regular Pair Action

Write $O=\mathbb Z[\varphi]$, with multiplication by $\varphi$ represented in the basis
$(1,\varphi)$ by $Q=\left(\begin{smallmatrix}0&1\\1&1\end{smallmatrix}\right)$. For the
Fibonacci and Lucas sequences $F_m,L_m$,

$$
Q^m-I=
\begin{pmatrix}F_{m-1}-1&F_m\\F_m&F_{m+1}-1\end{pmatrix},\qquad
N_m:=|R_m|=|\det(Q^m-I)|=L_m-1-(-1)^m.
$$

The quotient’s Smith factors are $d_m,N_m/d_m$, where
$d_m=\gcd(F_{m-1}-1,F_m,F_{m+1}-1)$. The first sizes, for $m=3,\ldots,8$, are
$4,5,11,16,29,45$. Multiplication by $\varphi$ has order exactly $m$: a smaller positive
exponent $k$ would make $\varphi^m-1$ divide $\varphi^k-1$, contradicting
$0<|\operatorname{Norm}(\varphi^k-1)|<N_m$. Conjugating translation by $1$ by
multiplication by $\varphi$ supplies translation by $\varphi$, so the generated affine
group is $R_m\rtimes C_m$, of order $mN_m$.

A free transitive action on unordered pairs therefore requires $N_m=2m+1$. The displayed
sizes exclude $m=3,4$ and give equality at $5$. For $m\geq5$,
$N_{m+1}-N_m=L_{m-1}+2(-1)^m\geq5$, so equality never returns.
At $m=5$, evaluation $\varphi\mapsto4$ identifies $R_5$ with $\mathbb F_{11}$;
$\langle4\rangle=\{1,3,4,5,9\}$ and its negative partition the nonzero residues.
Every pair consequently has trivial stabilizer and lies in one orbit.
The checker exhausts all 55 pairs and 55 affine maps, and its $m=3,\ldots,16$ sweep
checks the quotient arithmetic separately from this all-$m$ proof.

## A Consistent 121-Cell Algebraic Cover

The identities $\varphi^{10}-1=11\varphi^5$ and $X^2-X-1=(X-4)(X-8)$ modulo $11$ give
$R_{10}\cong O/(11)\cong\mathbb F_{11}\times\mathbb F_{11}$. This ring is not the field
$\mathbb F_{121}$. In evaluation coordinates $(\alpha,\beta)$, multiplication by
$\varphi$ is $(4\alpha,8\beta)$, and its fifth power is $(\alpha,-\beta)$. It fixes 11
elements and has 55 two-element orbits.

For $\beta\ne0$, the map $[\alpha,\beta]\mapsto\{\alpha\pm\beta^{-1}\}$ is a bijection
onto the 55 pairs. Its inverse is $\alpha=(x+y)/2$, $\beta=\pm2/(x-y)$. This midpoint
construction works over any odd field; the Fibonacci content here is the return map and
its equivariance: $8^{-1}=-4$ modulo $11$, so multiplication by $\varphi$ becomes
multiplication by $4$ on unordered pairs.
Base translation lifts as $(\alpha,\beta)\mapsto(\alpha+1,\beta)$, or addition of
$2+8\varphi$ in $O/(11)$. Addition of $1$ to the cover ring fails to preserve the return
orbits.

These computations prove the proposed finite model.
The missing geometric obligation is an explicit identification of its elements, return
map, and translation with the manuscript’s cells and marks.
A permutation of cell labels is not automatically an isometry, a preserved contact, or a
nonoverlap certificate.

## Bundle and Modular Geodesic Qualifications

For $B=-Q^3=\left(\begin{smallmatrix}-1&-2\\-2&-3\end{smallmatrix}\right)$, $\det B=-1$,
so its mapping torus is nonorientable.
The integral involution $C=\left(\begin{smallmatrix}1&1\\0&-1\end{smallmatrix}\right)$
satisfies $CBC=Q^{-3}$. The degree-$k$ cyclic cover along the base circle has
$H_1\cong\mathbb Z\oplus\operatorname{coker}(B^k-I)
\cong\mathbb Z\oplus R_{3k}$ as abelian groups.
The cokernel formula follows either by abelianizing $\mathbb Z^2\rtimes_{B^k}\mathbb Z$
or by the mapping-torus exact sequence; compare
[Boyer, Luft and Zhang, Lemma 4.1](https://www.nsm.buffalo.edu/~xinzhang/BLZ.pdf).

Reading “recover” as an equality with $R_k$ would be false.
Reading it as recovery by quotients is possible: $R_{3m}$ surjects onto $R_m$. The
bundle group itself surjects onto the order-55 affine group by sending a fiber vector
$(a,b)$ to translation by $a+8b$ modulo $11$, and the base generator to slope $5$; the
relation holds because $(1,8)B\equiv5(1,8)$.

The length $4\log\varphi$ is correct for the usual curvature-$-1$ modular metric: $Q^2$
has determinant $1$, trace $3$, and translation length
$2\operatorname{arccosh}(3/2)=4\log\varphi$. An integral hyperbolic matrix cannot have
smaller absolute trace.
[Delecroix’s golden-torus notes](https://www.labri.fr/perso/vdelecro/golden_orbits.html)
also identify this shortest geodesic.
If the torus lattice really has column matrix $I+wQ$, its complex shape is

$$
x=\frac{2w+w^2}{1+w^2},\qquad
y=\frac{1+w-w^2}{1+w^2},\qquad
(x-\tfrac12)^2+y^2=\tfrac54.
$$

For the physical range $0\leq w\leq1/2$, $y>0$ and this is the required geodesic arc.
The abstract’s contact-matrix statement alone does not identify the actual lattice.

## The Side Field Has Galois Group $S_8$

For the [recorded side polynomial](../../../packing/frontier/n-011.md), the checker
verifies squarefree factorizations into irreducible factors of degrees $(8)$ modulo
$29$, $(1,7)$ modulo $7$, and $(1,2,5)$ modulo $73$. The first proves irreducibility
over $\mathbb Q$.
[Dedekind’s cycle-type theorem](https://kconrad.math.uconn.edu/blurbs/gradnumthy/galois-Q-factor-mod-p.pdf)
then supplies a 7-cycle and an element whose fifth power is a transposition.
A transitive degree-eight group containing a 7-cycle is 2-transitive: the stabilizer of
the fixed point is already transitive on the other seven.
Conjugating the transposition therefore gives all transpositions, proving $S_8$. The
exact factor coefficients are retained in the checker.
This confirms the abstract’s field claim for the known side, independently of its torus
construction.

## Consequences for Seventeen

The discriminant $5$ is a quadratic nonresidue modulo $17$. Thus $O$ has no quotient
$\mathbb F_{17}$ and $Q$ has no invariant sublattice of index $17$. There is also a
stronger obstruction to transferring the regular pair action: its group would have order
$\binom{17}{2}=136$, hence an involution, and any nonidentity involution of 17 labels
swaps two labels and fixes their unordered pair.
No such regular action exists, even outside the affine construction.
The square-slope affine group over $\mathbb F_{17}$ instead has two 68-pair orbits, each
pair with stabilizer of order two.

A different hyperbolic monodromy can have a 17-element cokernel:
$A=\left(\begin{smallmatrix}-2&5\\5&-13\end{smallmatrix}\right)$ has determinant $1$,
trace $-15$, and $\operatorname{coker}(A-I)\cong\mathbb Z/17$. Here $\det(A-I)=17$; a
matrix with determinant $17$ itself would not define a torus automorphism.
This example supplies no packing interpretation.
An actionable transfer test must derive an integral return matrix from the actual
three-angle contact family, retain its boundary marks, and check which pair constraints
its action preserves.
The arithmetic rules out the direct Fibonacci version before any search is warranted.

Replay from `packing/` with `uv run --frozen --all-extras --group dev python -m
cases.fibonacci_torus.algebra`. Controls reject a changed side polynomial, addition of
slope $-1$ to a claimed free action, omission of the reciprocal in the equivariance
claim, cover translation by $1$, and use of $\beta=0$ in the reciprocal map.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
