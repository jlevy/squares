                                             T HE F LOW-L IMIT OF R EFLECT-R EFLECT-R ELAX :
                                               E XISTENCE , S TABILITY, AND D ISCRETE -T IME
                                                                 B EHAVIOR
arXiv:2512.23843v1 [math.OC] 29 Dec 2025




                                                                               Manish Krishan Lal*

                                                                                  January 1, 2026



                                                                                           Abstract

                                                 We study the Reflect–Reflect–Relax (RRR) algorithm in its small–step (flow–limit)
                                                 regime. In the smooth transversal setting, we show that the transverse dynamics form
                                                 a hyperbolic sink, yielding exponential decay of a natural gap measure. Under uniform
                                                 geometric assumptions, we construct a tubular neighborhood of the feasible manifold
                                                 on which the squared gap defines a strict Lyapunov function, excluding recurrent dy-
                                                 namics and chaotic behavior within this basin.
                                                     In the discrete setting, the induced flow is piecewise constant on W-domains and
                                                 supports Filippov sliding along convergent boundaries, leading to finite-time capture
                                                 into a solution domain. We prove that small-step RRR is a forward–Euler discretiza-
                                                 tion of this flow, so that solution times measured in rescaled units converge to a fi-
                                                 nite limit while iteration counts diverge, explaining the emergence of iteration-optimal
                                                 relaxation parameters. Finally, we introduce a heuristic mesoscopic framework based on
                                                 percolation and renormalization group to organize performance deterioration near the
                                                 Douglas–Rachford limit.


                                           2020 Mathematics Subject Classification: Primary 37N40; Secondary 49J53, 90C30,
                                           65K10.

                                           Keywords: Reflect-Reflect-Relax, flow limit, nonconvex feasibility, dynamical systems,
                                           Filippov sliding, Lyapunov stability
                                              * Mathematics, Technical   University   of    Munich,   Garching,   85748,   Germany.     E-mail:
                                           manish.krishanlal@tum.de.


                                                                                              1
1    Introduction

Projection and reflection methods such as Douglas Rachford splitting and the Reflect-
Reflect-Relax (RRR) algorithm have proved effective for feasibility problems involving
nonconvex and even discrete constraints. These methods are used in a wide range of ap-
plications, including combinatorial design problems, constraint satisfaction, and learning
formulations cast as feasibility problems [3]. Despite their empirical success, the mech-
anisms governing their convergence and their dependence on algorithmic parameters
remain only partially understood.

   Motivated by extensive numerical experiments, Elser proposed a flow limit viewpoint
for RRR, in which progress is measured not in raw iteration counts but in rescaled time
units of the form t = kε, where ε > 0 denotes the step size and xk the kth iterate. From
this viewpoint, a robust empirical phenomenon emerges: as ε decreases, the solution time
measured in rescaled units often stabilizes to a finite value, while the number of iterations
required to reach a solution increases and exhibits a problem dependent optimal choice of
ε. This behavior is observed across a range of nonconvex feasibility problems, including
those studied in [4].

   The purpose of this paper is to provide a rigorous mathematical foundation for this
small step flow picture. We focus on two regimes that arise naturally in practice. The
first is a smooth regime, in which the constraint sets are smooth manifolds intersecting
transversally. The second is a discrete regime, in which the constraint sets are finite and
the induced dynamics exhibit sharp switching behavior. In both cases, we interpret RRR
as a discretization of an underlying continuous time system and analyze the structure of
the resulting flow. To this end, we define the RRR flow field

                      v( x ) := PB ( R A x ) − PA x,        R A := 2PA − Id,

and study the continuous dynamics ẋ = v( x ) together with its small step discretization

                                      x k +1 = x k + ε v ( x k ).

This formulation allows us to treat smooth and nonsmooth behavior within a single
framework and to make precise comparisons between continuous trajectories and dis-
crete iterates.


Contributions and scope. All of our rigorous results are established under local as-
sumptions. In the smooth setting, they are proved within a positively invariant tubular
neighborhood of the feasible manifold on which the metric projections are single valued.
In the discrete setting, they are proved along specified chains of convergent W-domain
boundaries. Within this framework, we establish the following results.

                                                  2
  (i) Transverse stability from the flow linearization. In the smooth transversal regime,
      we use the explicit linearization of the RRR flow in terms of tangent space projectors
      and prove that the transverse dynamics form a hyperbolic sink, with exponential
      decay rates determined by principal angles (Lemma 2.1, Theorem 3.1).
 (ii) Piecewise constant flow and sliding capture. For finite constraint sets, the induced
      flow is piecewise constant on W-domains. Along two cell boundaries satisfying a
      convergent normal condition, the associated Filippov sliding dynamics drive trajec-
      tories into a solution cell in finite time (Theorem 3.2).
(iii) Euler approximation of the flow. Small step RRR is an O(ε) accurate forward Eu-
      ler discretization of the continuous flow on finite time intervals, including across
      sliding segments, yielding O(ε) errors in trajectories (Theorem 3.3).
(iv) Flow limit behavior of solution times. In the feasible case, the continuous solution
      time to reach a fixed gap threshold is finite, and the discrete solution time converges
      to this limit as ε ↓ 0, while the corresponding iteration count diverges like 1/ε (The-
      orems 3.4 and 3.5).
 (v) Lyapunov structure and absence of recurrence. Under uniform geometric assump-
      tions, the squared gap defines a strict Lyapunov function on a tubular neighbor-
      hood of the feasible manifold, excluding nontrivial recurrence and chaotic dynamics
      within this basin (Theorem 4.2, Corollary 4.3).

  Beyond these local results, we introduce a formal but heuristic mesoscopic framework
based on percolation and renormalization group to organize the empirical deterioration
of RRR performance as the relaxation parameter approaches the Douglas Rachford limit.
We do not claim global convergence or a complete description of RRR dynamics for ar-
bitrary step sizes. Instead, our results provide a rigorous foundation for the small step
regime of the flow limit conjecture and for the absence of chaotic behavior near feasible
solutions.



2     Preliminaries

2.1   RRR and the flow field

Let A, B ⊂ Rm be closed sets with (possibly multivalued) metric projections PA , PB . The
RRR update with step ε > 0 is
                                                            
                         xk+1 = xk + ε PB ( R A xk ) − PA xk .                         (1)
where R A = 2PA − Id is the reflector. Formally, as ε → 0 and t = kε, the piecewise-linear
interpolation of { xk } approaches the solution of the ODE
                             ẋ = v( x ) = PB ( R A x ) − PA x.                           (2)

                                             3
We call v the RRR flow field. A point x is a (RRR) fixed point of the flow if v( x ) = 0. We
write the gap
                                    g( x ) := ∥v( x )∥ ,                                  (3)
as our basic measure of progress; in the smooth setting, g( x ) is equivalent to the trans-
verse distance from x to A ∩ B in a neighborhood of a transversal intersection.


2.2   Regularity classes

We will use two basic regimes:

   • (S1) Smooth transverse case. A and B are C2 embedded submanifolds of Rm that
     intersect transversally at x ∗ ∈ A ∩ B. In a sufficiently small neighborhood U of x ∗
     the metric projections PA and PB are single-valued and C1 , and their derivatives at x ∗
     are the orthogonal projectors p A , p B onto the tangent spaces T x∗ A, T x∗ B respectively.
     The intersection M := A ∩ B is then a C2 submanifold, and PA , PB restrict to the
     identity on M near x ∗ .
   • (S2) Discrete W-domain case. A and B are finite subsets of Rm . Then PA and PB are
     single-valued everywhere (nearest neighbors are unique except on a set of measure
     zero), and the induced velocity field v is piecewise constant on a finite partition
     of W-domains. For more general stratified sets, one typically obtains a piecewise
     C1 velocity field; here we focus on the finite case where the geometry is purely
     combinatorial.


2.3   Principal angles and the Jacobian at a regular point

In the smooth transverse case (S1), the linearization of the RRR flow at a feasible point
admits an explicit expression in terms of the orthogonal projectors onto the tangent spaces
of the constraint manifolds. Let p A and p B denote the orthogonal projectors onto the
tangent spaces T x∗ A and T x∗ B at a transversal intersection x ∗ ∈ A ∩ B. The direct sum
T x∗ A + T x∗ B admits an orthogonal decomposition into principal-angle planes and the
common tangent subspace T x∗ A ∩ T x∗ B. On each principal-angle plane the angle between
T x∗ A and T x∗ B is some θ ∈ (0, π2 ].
Lemma 2.1 (Linearization of the flow at a feasible point). Assume (S1) and let x ∗ ∈ A ∩ B
be a transversal intersection. Then x ∗ is an equilibrium of the flow (2), and its Jacobian is
            Dv( x ∗ ) = DPB ( x ∗ ) DR A ( x ∗ ) − DPA ( x ∗ ) = 2p B p A − p B − p A .
                                                                                     
                                                                                           (4)
Moreover:

                                               4
  (i) On the intersection T x∗ A ∩ T x∗ B we have Dv( x ∗ ) = 0.
 (ii) On each principal-angle 2-plane with angle θ ∈ (0, π2 ], there exists an orthonormal
      basis in which
                                                  "                          #
                                                      cos2 θ
                                    
                                 1 0                             cos θ sin θ
                        pA =           ,     pB =                              ,
                                 0 0                cos θ sin θ    sin2 θ

      and in this basis the restriction of Dv( x ∗ ) is
                                         "                         #
                                            − sin2 θ − sin θ cos θ
                                r (θ ) =                             .
                                           sin θ cos θ  − sin2 θ

      The eigenvalues of r (θ ) are − sin2 θ ± i sin θ cos θ, and its symmetric part equals
      − sin2 θ I2 .

Proof. Since PA ( x ∗ ) = PB ( x ∗ ) = x ∗ , we have R A ( x ∗ ) = x ∗ and hence v( x ∗ ) = 0. On U the
chain rule gives DR A ( x ∗ ) = 2DPA ( x ∗ ) − I = 2p A − I, DPB ( x ∗ ) = p B , and DPA ( x ∗ ) = p A ,
which yields (4). (i) follows from p A z = p B z = z for z ∈ T x∗ A ∩ T x∗ B. The block decom-
position in (ii) is standard principal-angle geometry: in the stated basis one computes
r (θ ) by direct multiplication of 2p B p A − p B − p A , and the eigenvalues and symmetric
part follow from a short calculation.                                                                ■
  Thus M = A ∩ B is a manifold of equilibria, and on the transverse complement of T x∗ M
the linearization has eigenvalues with strictly negative real part, forming a stable spiral
when 0 < θ < π2 and a stable node when θ = π2 .


2.4    W-domains and piecewise-constant fields

In the discrete case (S2) we assume A and B are finite sets. For each pair ( a, b) ∈ A × B
define the corresponding W-domain

                     W ( a, b) := x ∈ Rm PA ( x ) = a, PB ( R A x ) = b .
                                 
                                                                                        (5)

Away from a set of measure zero where projections are nonunique, the family
{W ( a, b)}(a,b)∈ A× B forms a partition of Rm into finitely many cells. On such a cell we
have
                      v( x ) = PB ( R A x ) − PA x ≡ b − a,  x ∈ W ( a, b),
so the velocity field is piecewise constant. The interfaces between W-domains are smooth
codimension-one manifolds almost everywhere, given by Voronoi bisectors and their re-
flections, with lower-dimensional junction sets where three or more domains intersect.

                                                   5
2.5   Filippov solutions and sliding

The piecewise-constant field v is discontinuous on W-domain boundaries. We use the
notion of Filippov solutions [5]. For a measurable, locally bounded vector field v : Rm →
Rm , its Filippov regularization at x is the closed convex hull F ( x ) of all essential values of
v near x. A Filippov solution of
                                          ẋ (t) ∈ F ( x (t))
is an absolutely continuous curve x (·) satisfying the inclusion almost everywhere. Con-
sider a smooth portion of a boundary Σ separating two W-domains with constant veloci-
ties v1 and v2 . Let Σ = ∂W ( a1 , b1 ) ∩ ∂W ( a2 , b2 ) be a C1 two-cell interface, and let n denote
the unit normal to Σ oriented from W ( a1 , b1 ) into W ( a2 , b2 ). The Filippov set on Σ is

                              F ( x ) = co{v1 , v2 },         v i : = bi − a i .

If the convergent normal condition

                                         ( n · v1 ) ( n · v2 ) < 0                               (6)

holds, there exists a unique vslide ∈ F ( x ) satisfying n · vslide = 0. Writing
                                                                    n · v2
                   vslide = αv1 + (1 − α)v2 ,            α=                    ∈ (0, 1),
                                                               n · ( v2 − v1 )
this is equivalently expressed as
                                             ( n · v2 ) v1 − ( n · v1 ) v2
                                 vslide :=                                 .                     (7)
                                                    n · ( v2 − v1 )
Under (6), Σ is locally attracting for Filippov solutions, which evolve along Σ with veloc-
ity vslide [1]. For a C1 interface Σ and x ∈ Σ, let ΠΣ ( x ) denote the orthogonal projector
onto the tangent space Tx Σ. We say that the sliding velocity satisfies a uniform tangential
speed bound on Σ if
                            ∥ΠΣ ( x ) vslide ∥ ≥ s0 > 0,    ∀ x ∈ Σ.                     (8)


2.6   Solution time in continuous and discrete time

Fix a tolerance δ > 0. For a (Carathéodory or Filippov) flow solution x (·) of (2) we define
the continuous hitting time

                           Tδ∗ ( x0 ) := inf t ≥ 0 g x (t) ≤ δ ,
                                                         
                                                                                          (9)

with the convention that Tδ∗ ( x0 ) = +∞ if the set is empty, and with initial condition
x (0) = x0 . We refer to g( x ) as the gap function (3), which vanishes precisely at RRR fixed

                                                     6
points. For the discrete RRR iteration (1) with step ε > 0, we define the corresponding
discrete hitting time
                                     t∗δ (ε; x0 ) := kε,                            (10)
where k is the smallest index such that g( xk ) ≤ δ, if such an index exists, and t∗δ (ε; x0 ) =
+∞ otherwise. One of our main goals is to understand the dependence of t∗δ (ε; x0 ) on ε
and its relation to the flow-limit Tδ∗ ( x0 ) as ε ↓ 0.



3     Main Results

We now state and prove our main results in the smooth transverse regime (S1) and the
discrete W-domain regime (S2).


3.1   Smooth transverse case

The local affine form of the flow suggests contracting behavior transverse to the feasible
manifold, as illustrated through low-dimensional examples [4, Figures 5.3-5.4]. The fol-
lowing theorem makes this precise by establishing exponential decay of the flow in the
transverse directions near a transversal feasible point.
Theorem 3.1 (Hyperbolic sink and exponential decay of the gap). Assume (S1) and let
x ∗ ∈ A ∩ B be a transversal intersection. Then x ∗ is an equilibrium of (2), and there exist
constants µ > 0, C ≥ 1 and a neighborhood U of x ∗ such that for any solution x (·) of (2)
with x (0) ∈ U,
                       ∥v( x (t))∥ ≤ C e−µt ∥v( x (0))∥      ∀t ≥ 0.                     (11)
In particular, for any δ > 0 and x (0) ∈ U with g( x (0)) > δ,
                                                         C ∥v( x (0))∥ 
                        Tδ∗ ( x (0))   ≤ µ   −1
                                                  log                       < ∞.           (12)
                                                               δ

Proof. By (S1), the projections PA , PB are single-valued and C1 on a neighborhood of x ∗ ,
hence v = PB ◦ R A − PA is C1 there. By Lemma 2.1, v( x ∗ ) = 0, so x ∗ is an equilibrium of
(2). Let J := Dv( x ∗ ).

   Step 1 (coercivity of the symmetric part on the transverse sum). Set T := Tx∗ A + Tx∗ B and
let PT be the orthogonal projector onto T . By Lemma 2.1(i)-(ii), on T the symmetric part
S∗ := 12 ( J + J ⊤ ) satisfies

                   S∗ ⪯ −σ PT ,          σ := min{sin2 θ j : θ j ∈ (0, π2 ]} > 0,          (13)

                                                        7
and S∗ = 0 on T ⊥ .

  Step 2 (transverse dominance of v near x ∗ ). Since v is C1 and v( x ∗ ) = 0, we have

                                                                ∥r ( x )∥
                      v ( x ) = J ( x − x ∗ ) + r ( x ),                  → 0 ( x → x ∗ ).                     (14)
                                                               ∥ x − x∗ ∥
Moreover, ran( J ) ⊆ T by Lemma 2.1 (since J acts as a direct sum of blocks supported on
T ), hence PT J = J. Fix η ∈ (0, 1) and shrink r > 0 so that ∥r ( x )∥ ≤ η ∥ J ( x − x ∗ )∥ for all
∥ x − x ∗ ∥ ≤ r. Then for all such x,
∥ PT v( x )∥ = ∥ J ( x − x ∗ ) + PT r ( x )∥ ≥ (1 − η )∥ J ( x − x ∗ )∥,      ∥v( x )∥ ≤ (1 + η )∥ J ( x − x ∗ )∥,
and therefore
                                                           1−η
              ∥ PT v( x )∥ ≥ κ ∥v( x )∥,            κ :=       ∈ (0, 1),         ∀ x ∈ B ( x ∗ , r ).          (15)
                                                           1+η

  Step 3 (Lyapunov inequality for E = 12 ∥v∥2 ). Define E( x ) := 12 ∥v( x )∥2 on B( x ∗ , r ). Along
any solution x (·) of (2) with x (t) ∈ B( x ∗ , r ) we compute
              d
                 E( x (t)) = ⟨v( x (t)), Dv( x (t))v( x (t))⟩ = ⟨v( x (t)), S( x (t))v( x (t))⟩,               (16)
              dt
where S( x ) := 21 ( Dv( x ) + Dv( x )⊤ ). By continuity of Dv at x ∗ , after shrinking r we may
assume
                                                 σκ 2
                              ∥ S ( x ) − S∗ ∥ ≤       ∀ x ∈ B ( x ∗ , r ).
                                                  4
                   ∗
Then for x ∈ B( x , r ),

                                                                               σκ 2            σκ 2
     ⟨v, S( x )v⟩ ≤ ⟨v, S∗ v⟩ + ∥S( x ) − S∗ ∥ ∥v∥2 ≤ −σ∥ PT v∥2 +                  ∥ v ∥2 ≤ −      ∥ v ∥2 ,
                                                                                4               2
where the second inequality uses (13) and the last uses (15). Hence, along solutions stay-
ing in B( x ∗ , r ),
                                                          σκ 2
                        Ė( x (t)) ≤ −2µ E( x (t)), µ :=       > 0.
                                                           2
Gronwall yields E( x (t)) ≤ E( x (0))e−2µt , i.e.

                                        ∥v( x (t))∥ ≤ e−µt ∥v( x (0))∥,
which proves (11) with C = 1 (and thus also with any C ≥ 1 after shrinking U).

  Finally, if ∥v( x (0))∥ > δ, then the first hitting time Tδ∗ ( x (0)) := inf{t ≥ 0 : ∥v( x (t))∥ ≤
                  ∗
δ} satisfies e−µTδ ∥v( x (0))∥ ≤ δ/C, which is equivalent to (12).                                 ■

                                                           8
3.2   Discrete W-domains and sliding capture

In the discrete regime (S2), where the constraint sets are finite, the RRR flow is piecewise
constant on a finite partition of the state space into W-domains, with trajectories exhibit-
ing attraction to domain boundaries [4, Section 5.5.4, Figure 5.6]. The following result
provides a precise formulation of this behavior using Filippov solutions and establishes
finite-time capture along convergent boundaries.

Theorem 3.2 (Piecewise-constant flow and sliding capture). Assume (S2) and A ∩ B ̸= ∅.
Then:

  (i) There exists a finite family {W ( a, b)}(a,b)∈ A× B such that

               Rm =
                       [
                               W ( a, b) up to a null set,          v( x ) = b − a ∀ x ∈ W ( a, b).
                      ( a,b)

       For any x0 ∈
                      S
                         / (a,b) ∂W ( a, b), the Carathéodory solution of (2) with x (0) = x0 is
       unique until the first boundary hit.
  (ii) Let Σ = ∂W ( a1 , b1 ) ∩ ∂W ( a2 , b2 ) be a C1 interface with unit normal n and velocities
       vi = bi − ai . If (6) holds, then there exists a unique vslide ∈ co{v1 , v2 } satisfying
       n · vslide = 0, and Σ is locally attracting for Filippov solutions.
 (iii) Let Σ1 , . . . , Σ N be C1 interfaces with

                   Σ j ⊂ ∂W ( a j , b j ) ∩ ∂W ( a j+1 , b j+1 ),      Σ N ∩ W ( a∗ , a∗ ) ̸= ∅,

      and assume (6) and (8) hold on each Σ j . If length(Σ j ) = ℓ j < ∞, then any Filippov
      solution entering Σ1 reaches W ( a∗ , a∗ ) in time
                                                             N  ℓj
                                                  Tcap ≤ ∑         .
                                                                s
                                                            j =1 0


Proof. (i) By Definition (5) and §2.4, the sets {W ( a, b)}(a,b)∈ A× B form a finite partition of
Rm up to a null set. On each W ( a, b) we have v( x ) ≡ b − a. Since v is constant on each
cell, Carathéodory solutions are unique until the first boundary hit.

  (ii) On a two-cell interface Σ, the Filippov set is F ( x ) = co{v1 , v2 }. Under (6), Filippov
theory [5, Ch. 2] yields a unique vslide ∈ F ( x ) with n · vslide = 0, and local attraction to Σ.

  (iii) Along each Σ j , solutions slide with tangential speed bounded below by s0 by (8).
Traversing a segment of length ℓ j therefore takes at most ℓ j /s0 time. Summation over j
gives the bound and finite-time capture into W ( a∗ , a∗ ), where v ≡ 0.                ■


                                                       9
3.3    Euler-flow approximation and hitting times

The small-step interpretation of RRR as a time-rescaled continuous flow, observed empir-
ically in [4, Section 5.5.8], is justified here by explicit error bounds for the Euler discretiza-
tion and their consequences for hitting times.

For ε > 0 and x0 ∈ Rm , define the RRR iterates xk+1 = xk + εv( xk ), x0 ∈ Rm , and let x ε (·)
be the piecewise-linear interpolation with x ε (kε) = xk .
Theorem 3.3 (Euler-flow approximation). Let K ⊂ Rm be compact and T > 0. Assume
either

  (a) (S1) holds on an open neighborhood of K, or
  (b) (S2) holds and the Filippov solution x (·) intersects only finitely many two-cell inter-
      faces on [0, T ] and satisfies dist( x (t), J ) ≥ δ0 > 0 for all t ∈ [0, T ], where J denotes
      the set of multiway junctions.

Then there exist ε 0 > 0 and C = C (K, T ) > 0 such that for all x0 ∈ K and 0 < ε ≤ ε 0 ,
                                         sup ∥ x ε (t) − x (t)∥ ≤ C ε,                         (17)
                                        t∈[0,T ]

where x (·) is the Carathéodory (resp. Filippov) solution of (2) with x (0) = x0 .

Proof. Let eε (t) := x ε (t) − x (t).

  Step 1: Lipschitz regions. On any open set Ω ⊂ Rm where v is L-Lipschitz, eε satisfies
                   ėε (t) = v( x ε (t)) − v( x (t)),          ∥ėε (t)∥ ≤ L∥eε (t)∥ + O(ε),
for a.e. t away from grid points. By Grönwall,
                                              sup ∥eε (t)∥ ≤ C1 ε.                             (18)
                                             t∈[0,T ]

Under (S1) this holds on a neighborhood of K; under (S2) it holds on each W-domain
away from interfaces.

  Step 2: two-cell interfaces. Let Σ be a C1 interface satisfying (6). By Theorem 3.2(ii), the
Filippov solution satisfies ẋ (t) = vslide on Σ. Let xk be such that the Euler step crosses Σ
at some τ ∈ (0, ε). A two-step Taylor expansion of the Euler scheme yields
                                     xk+2 − xk = 2ε vslide + O(ε2 ),                           (19)
and the normal component of x ε relative to Σ is O(ε2 ) (cf. [1, Sec. 3]). Hence
                                              sup         ∥eε (t)∥ ≤ C2 ε.                     (20)
                                         t∈[kε,(k +2)ε]


                                                          10
  Step 3: summation. By assumption, only finitely many interfaces are crossed on [0, T ]
and junctions are avoided. Combining (18) and (20) over the resulting partition of [0, T ]
yields (17).                                                                           ■
Theorem 3.4 (Hitting-time convergence). Assume (S1) and let x0 ∈ U, where U is as in
Theorem 3.1. For δ > 0, define

       Tδ∗ ( x0 ) := inf{t ≥ 0 : ∥v( x (t))∥ ≤ δ},            t∗δ (ε; x0 ) := inf{kε : ∥v( xk )∥ ≤ δ}.

Then there exist ε 0 > 0 and Cδ > 0 such that for all 0 < ε ≤ ε 0 ,

                                       t∗δ (ε; x0 ) − Tδ∗ ( x0 ) ≤ Cδ ε.                                 (21)

Proof. By Theorem 3.1,
                                                            d
               ∥v( x (t))∥ ≤ C0 e−µt ∥v( x0 )∥,                ∥v( x (t))∥ ≤ −µ∥v( x (t))∥
                                                            dt
for a.e. t with v( x (t)) ̸= 0. Hence

                                  ∥v( x˙(t))∥ t=T ∗ (x ) ≤ −µδ < 0,
                                                    δ   0


so the crossing of {∥v∥ = δ} is transversal. Fix T > Tδ∗ ( x0 ). By Theorem 3.3,

                                        sup ∥ x ε (t) − x (t)∥ ≤ Cε.
                                       t∈[0,T ]

Continuity of v on U implies the existence of Lδ > 0 such that

                             sup ∥v( x ε (t))∥ − ∥v( x (t))∥ ≤ Lδ Cε.
                            t∈[0,T ]

Therefore, for ε sufficiently small, x ε (·) crosses the band {δ/2 ≤ ∥v∥ ≤ 2δ} exactly once,
and the implicit function theorem yields the estimate (21).                               ■


3.4   Quantitative flow limit

We summarize the asymptotic behavior of the solution time in the flow and its discrete
approximation.
Theorem 3.5 (Quantitative flow time and discrete correction). Assume the hypotheses of
Theorem 3.1. Then there exist c1 , c2 > 0, δ0 > 0, and a neighborhood U of x ∗ such that for
all x0 ∈ U and δ ∈ (0, δ0 ],
                                                           1
                                   Tδ∗ ( x0 ) ≤ c1 + c2 log .                           (22)
                                                           δ

                                                     11
Moreover, for the discrete RRR iteration (1),
                           t∗δ (ε; x0 ) = Tδ∗ ( x0 ) + O(ε),                  ε ↓ 0,     (23)
where the O(ε) term is uniform for x0 in compact subsets of U.

Proof. By Theorem 3.1, there exist C, µ > 0 and a neighborhood U of x ∗ such that
                     ∥v( x (t))∥ ≤ Ce−µt ∥v( x0 )∥,                 ∀ x0 ∈ U, t ≥ 0.
Fix a compact K ⊂ U and set
                                  M := sup ∥v( x0 )∥ < ∞.
                                             x0 ∈ K

Evaluating the above bound at t = Tδ∗ ( x0 ) gives
                                                                          ∗
                           δ ≤ ∥v( x ( Tδ∗ ( x0 )))∥ ≤ Ce−µTδ ( x0 ) M,
which implies (22) with c2 = µ−1 and c1 = µ−1 log(CM ). The discrete correction (23)
follows directly from the hitting-time estimate of Theorem 3.4, which yields
                                 |t∗δ (ε; x0 ) − Tδ∗ ( x0 )| ≤ Cδ ε
uniformly for x0 ∈ K and ε sufficiently small.                                             ■
Remark 3.6 (Flow-limit behavior of the solution time). For any fixed x0 ∈ U and δ ∈
(0, δ0 ],
                            lim t∗δ (ε; x0 ) = Tδ∗ ( x0 ) < ∞.
                                 ε ↓0
Consequently, the flow-time stabilizes as ε ↓ 0, while the iteration count
                                                           t∗δ (ε; x0 )
                                        k∗δ (ε; x0 ) :=
                                                                 ε
diverges at rate O(ε−1 ). This separation explains the empirical observation that small
step sizes regularize solution time while inducing a problem-dependent iteration-optimal
choice of ε.


3.5   Discrete Lyapunov inequality for small-step RRR

Let x ∗ ∈ A ∩ B be a transversal intersection in the smooth regime (S1). Set

                          T M := Tx∗ A ∩ Tx∗ B,                T ⊥ := (T M )⊥ ,
and let PT denote the orthogonal projector onto T ⊥ . Let J := Dv( x ∗ ) be the Jacobian from
Lemma 2.1.

                                                      12
Theorem 3.7 (Local discrete Lyapunov inequality). Assume (S1) and let x ∗ ∈ A ∩ B be
transversal. Define JT := PT JPT . Then there exist HT ∈ Rm×m , c > 0, ε 0 > 0, and r > 0
such that:

   (i) HT ⪰ 0, ker HT = T M , and HT |T ⊥ ≻ 0;
  (ii) for all 0 < ε ≤ ε 0 and ∥ x0 − x ∗ ∥ ≤ r, the RRR iterates xk+1 = xk + εv( xk ) satisfy
       ∥ xk − x ∗ ∥ ≤ r for all k ≥ 0;
 (iii) the quadratic form
                                      V ( x ) := ( x − x ∗ )⊤ HT ( x − x ∗ )              (24)
      satisfies
                                   V ( xk+1 ) ≤ (1 − cε) V ( xk )       ∀k ≥ 0;                          (25)
 (iv) in particular,
                                      V ( xk ) ≤ e−ckε V ( x0 )     ∀k ≥ 0,                              (26)
      and ∥ PT ( xk   − x ∗ )∥ → 0 exponentially in discrete time t         k = kε.


Proof. By Lemma 2.1 and Theorem 3.1, the spectrum of JT satisfies ℜλ( JT ) < 0 on T ⊥ ,
and JT = 0 on T M . By the continuous-time Lyapunov theorem, there exists HT satisfying
((i)) and
                                HT JT + JT⊤ HT ⪯ −2γHT                              (27)
on T ⊥ for some γ > 0.

  Consider the linearized map yk+1 = ( I + εJ )yk . Then
                                                h                                  i
                 V ( y k +1 ) − V ( y k ) = y ⊤
                                              k   ε ( J ⊤
                                                          HT + HT J ) + ε 2 ⊤
                                                                           J  HT J   yk .                (28)

On T ⊥ , (27) and finite dimensionality imply J ⊤ HT J ⪯ C1 HT for some C1 > 0. Choosing
0 < ε 0 ≤ γ/C1 , we obtain
                              ( I + εJ )⊤ HT ( I + εJ ) − HT ⪯ −γεHT ,
hence V (yk+1 ) ≤ (1 − γε)V (yk ) for the linearized system. For the nonlinear RRR itera-
tion, write
            xk+1 − x ∗ = ( I + εJ )( xk − x ∗ ) + εr ( xk ),      r ( x ) : = v ( x ) − J ( x − x ∗ ).
Since v ∈ C1 near x ∗ , there exists C2 > 0 such that ∥r ( x )∥ ≤ C2 ∥ x − x ∗ ∥2 locally. Expand-
ing V ( xk+1 ) and using (28) yields

                  V ( xk+1 ) ≤ (1 − γε)V ( xk ) + C3 ε∥ xk − x ∗ ∥3 + C4 ε2 ∥ xk − x ∗ ∥4 .
Since HT |T ⊥ ≻ 0, there exist m, M > 0 such that

                         m∥ PT ( xk − x ∗ )∥2 ≤ V ( xk ) ≤ M ∥ PT ( xk − x ∗ )∥2 .

                                                     13
Choosing r > 0 sufficiently small ensures

                          C3 ε∥ xk − x ∗ ∥3 + C4 ε2 ∥ xk − x ∗ ∥4 ≤ γ2 εV ( xk )

whenever ∥ xk − x ∗ ∥ ≤ r. Thus

                                    V ( xk+1 ) ≤ (1 − γ2 ε)V ( xk ),

which gives (25) with c = γ/2. Invariance of B( x ∗ , r ) follows by induction, and (26) is
obtained by iteration.                                                                   ■



4     Global basins, generic chains, and junctions

4.1    Smooth tubular basin

We strengthen Theorem 3.1 under uniform geometric control of the feasible manifold
M := A ∩ B.
Assumption 4.1 (Smooth tube). Assume (S1) and that M := A ∩ B is compact. Suppose:

  (i) ∠(T x A, T x B) ∈ [θ0 , π/2] for all x ∈ M and some θ0 > 0;
 (ii) A and B have reach ≥ ρ > 0 and second fundamental forms bounded by κ < ∞.

Define, for 0 < r ≤ ρ,

                      Sr := { x ∈ Rm : dist( x, A) ≤ r, dist( R A x, B) ≤ r }.          (29)

Theorem 4.2 (Strict Lyapunov function on a tube). Under Assumption 4.1 there exist
r ∈ (0, ρ] and σ > 0 such that for every solution x (·) of (2) with x (t) ∈ Sr ,
                               d 1                 2
                                                      
                                    ∥ v ( x ( t ))∥     ≤ −σ ∥v( x (t))∥2 .             (30)
                               dt 2
Consequently, ∥v( x (t))∥ → 0 exponentially and dist( x (t), M ) → 0 as t → ∞.

Proof. For x̄ ∈ M, Lemma 2.1 and Assumption 4.1(i) yield
                                               ⊤
                       1
                                                   ⪯ − sin2 θ0 PTx̄ A+Tx̄ B .
                                                 
                       2 Dv ( x̄ ) + Dv ( x̄ )

Assumption 4.1(ii) implies PA , PB ∈ C1 (Sr ) for r small, and there exists C < ∞ such that

                       ∥ Dv( x ) − Dv( x̄ )∥ ≤ Cr,        x ∈ Sr , x̄ := PM ( x ).

                                                   14
Choosing r > 0 so that Cr ≤ 12 sin2 θ0 , the symmetric part S( x ) := 12 ( Dv( x ) + Dv( x )⊤ )
satisfies
                       S( x ) ⪯ − 21 sin2 θ0 PTx̄ A+Tx̄ B , ∀ x ∈ Sr .
Let E( x ) := 12 ∥v( x )∥2 . Along solutions in Sr ,

Ė( x (t)) = ⟨v( x (t)), Dv( x (t))v( x (t))⟩ = ⟨v( x (t)), S( x (t))v( x (t))⟩ ≤ − 12 sin2 θ0 ∥v( x (t))∥2 ,

which is (30) with σ := 12 sin2 θ0 .                                                                      ■
Corollary 4.3 (No recurrence in the tube). Consider Assumption 4.1. Let x (·) be a solution
of ẋ = v( x ) with x (0) ∈ Sr . Then

                                         ω ( x ) ⊆ M := A ∩ B.

In particular, Sr contains no nontrivial periodic orbits and no chaotic invariant sets of the
flow.

Proof. By Theorem 4.2,

                     Ė( x (t)) ≤ −σ ∥v( x (t))∥2 < 0      whenever v( x (t)) ̸= 0.

Hence E( x (t)) is strictly decreasing along any nonconstant trajectory in Sr . Therefore no
point x ∈ Sr \ M can belong to ω ( x ), and ω ( x ) ⊆ { x : v( x ) = 0} = M.               ■
Remark 4.4 (Regularity in the feasible case). In the feasible case A ∩ B ̸= ∅, Assump-
tion 4.1 and Theorem 4.2 yield a strict Lyapunov function E( x ) = 12 ∥v( x )∥2 on Sr . Con-
sequently, the flow restricted to Sr is gradient-like: all trajectories converge to M, and no
recurrent dynamics occur in Sr .

  This is consistent with the observations in [4, Chapter 5], where chaotic behavior for
RRR is reported only for infeasible instances (A ∩ B = ∅) or outside basins of attraction.
The present results are local: they exclude recurrence near M but do not address global
dynamics.


4.2    Generic descent chains in the discrete case

Assumption 4.5 (Discrete genericity). Assume (S2) and:

  (i) {∥b − a∥2 : ( a, b) ∈ A × B} are pairwise distinct;
 (ii) for each b ∈ B (resp. a ∈ A), the Voronoi adjacency graph on A (resp. B) is con-
      nected;

                                                    15
 (iii) W-domain boundaries are in general position; in particular, all multiway junctions
       have codimension ≥ 2.

  For ( a, b) ∈ A × B, define the pair distance
                                              d( a, b) := ∥b − a∥2 .
Lemma 4.6 (Descent across an A-switch). Let b ∈ B and let Σ ⊂ ∂W ( a1 , b) ∩ ∂W ( a2 , b) be
an A-switch boundary. Let n be the unit normal to Σ oriented from W ( a1 , b) to W ( a2 , b),
and set vi := b − ai . Define
                                α : = ⟨ a2 − a1 , b − a1 ⟩.
Then:

  (i) (n · v1 )(n · v2 ) < 0 ⇔ α ∈ (0, ∥ a2 − a1 ∥2 );
 (ii) along the sliding velocity vslide on Σ,
                            d
                               d( a(t), b) < 0 whenever α > 21 ∥ a2 − a1 ∥2 ,
                           dt
      where a(t) ∈ { a1 , a2 } denotes the active A-index along the sliding path.

Proof. Since Σ is a Voronoi bisector between a1 and a2 with b fixed, its normal satisfies
n = ±( a2 − a1 )/∥ a2 − a1 ∥. Direct evaluation of n · vi yields (i). Statement (ii) follows since
d( a, b) depends only on the active index a, and the inequality α > 12 ∥ a2 − a1 ∥2 selects the
direction corresponding to the strictly smaller distance.                                       ■
Theorem 4.7 (Finite descent chain to a solution cell). Assume Assumption 4.5 and A ∩
B ̸= ∅. Then for any nonsolution cell W ( a, b) there exists a finite sequence
             W ( a, b) = W ( a0 , b0 ) → W ( a1 , b1 ) → · · · → W ( a N , b N ) = W ( a∗ , a∗ )
such that:

  (i) W ( a j , b j ) and W ( a j+1 , b j+1 ) share a boundary satisfying (6);
 (ii) d( a j+1 , b j+1 ) < d( a j , b j ) for all j, and
                  d( a, b) − d( a∗ , a∗ )
             N≤                           ,      ∆ :=             min                   |d( a′ , b′ ) − d( a′′ , b′′ )| > 0.
                            ∆                                ( a′ ,b′ )̸=( a′′ ,b′′ )
                                                        ( a′ ,b′ ),( a′′ ,b′′ )∈ A× B

Consequently, any Filippov solution following these convergent boundaries reaches
W ( a∗ , a∗ ) after finitely many boundary transitions.

            / arg mina′ ∈ A d( a′ , b), Assumption 4.5(ii) provides a Voronoi path in A to some
Proof. If a ∈
a with d( a′ , b) < d( a, b); by Lemma 4.6, one can choose A-switches along which d strictly
 ′

decreases. If b ∈ / arg minb′ ∈ B d( a, b′ ), the symmetric argument applies. Since all values of
d are distinct and bounded below by d( a∗ , a∗ ), the number of strict decreases is finite and
bounded by (d( a, b) − d( a∗ , a∗ ))/∆.                                                        ■

                                                        16
4.3     Nonunique projections and junctions

Let M A , M B ⊂ Rm denote the medial axes where PA , PB are multivalued, and let J
denote the set of points where three or more W-domains intersect.
Theorem 4.8 (Negligibility of medial and junction sets). Assume either (S1) with compact
M = A ∩ B or (S2) with Assumption 4.5. Then:

  (i)
                                      Lm (M A ) = Lm ( R− 1
                                                        A (M B )) = 0;
 (ii) in case (S2),
                               Lm (J ) = 0,        L1 ({t ≥ 0 : x (t) ∈ J }) = 0
        for every Filippov solution x (·).

Proof. (i) For closed C2 submanifolds (and for finite sets), medial axes have Hausdorff
codimension at least 1, hence zero Lebesgue measure. Since R A is a C1 diffeomorphism
on Sr in case (S1) and an affine map in case (S2) (Definition (5)), the preimage R− 1
                                                                                  A (M B )
also has measure zero.

  (ii) Under Assumption 4.5(iii), J is a finite union of intersections of at least two
smooth codimension-1 hypersurfaces and therefore has codimension at least 2, imply-
ing Lm (J ) = 0. Since Filippov solutions are absolutely continuous, their preimages of J
have one-dimensional Lebesgue measure zero.                                             ■


4.4     A percolation and renormalization group model for the β ↑ 1 catas-
        trophe

This subsection is heuristic. Its role is to formalize a mesoscopic object that can carry the
β ↑ 1 divergence picture discussed in [4, Ch. 5] and measured in §5.1.


Cell dynamics induced by Tβ . Assume (S2) and use the W-domain partition from (5).
Index the (a.e.) cells by a finite set V,
                Rm =
                       G
                              Wi   (up to a null set),      v( x ) = vi for a.e. x ∈ Wi ,
                       i ∈V

so that the RRR map is
                                     Tβ ( x ) = x + βvi ,    x ∈ Wi .
Fix a probability measure µ on Rm with continuous strictly positive density. The quantity
below measures how much of cell i is transported into cell j by one step of Tβ .

                                                     17
Definition 4.9 (Cell transition kernel, support digraph, and absorbing set). For β > 0,
define                                                                     
                                                   µ W i ∩ ( Wj − βv i )
                Pβ (i, j) := µ Wi ∩ Tβ−1 (Wj ) Wi =                          .
                                                            µ(Wi )
Define the support digraph Gβ = (V, Eβ ) by
                                (i → j) ∈ Eβ ⇔ Pβ (i, j) > 0.
Let
                                   S : = { i ∈ V : vi = 0 }
denote the set of solution cells (absorbing fixed points of Tβ ).

  The deterministic orbit xk+1 = Tβ ( xk ) induces a cell itinerary ik ∈ V via xk ∈ Wik .
The kernel Pβ is a coarse model of cell-to-cell transport under a reference distribution;
Gβ records which transitions are possible at all. Large strongly connected regions of Gβ
represent a mechanism for long wandering before hitting S, consistent with the “search
phase” dominating in §5.1.


Order parameter. Consider a problem family indexed by n with cell sets Vn and solution
sets Sn ⊆ Vn . Write Gβ,n for the corresponding support digraph.
Definition 4.10 (Wandering order parameter and graph phase transition). Let SCCmax ( G )
be a largest strongly connected component of G. Define
                                    1
                        Φn ( β) :=
                                                                 
                                         SCCmax Gβ,n ↾ (Vn \ Sn ) .
                                   |Vn |
We say the family exhibits a (directed) phase transition at β c ∈ (0, 1) if
                lim Φn ( β) = 0 ( β < β c ),        lim inf Φn ( β) > 0 ( β > β c ).
                n→∞                                  n→∞


To connect β 7→ Gβ,n with standard threshold heuristics, we randomize edges according
to Pβ as an inhomogeneous directed percolation model [2, 7].
Definition 4.11 (Edge percolation on the support digraph). Let {Uij }(i,j)∈V ×V be i.i.d.
Unif[0, 1]. Define Gβω by declaring i → j open iff Uij ≤ Pβ (i, j). Equivalently, conditional
on Pβ , edges are independent with P(i → j open) = Pβ (i, j).
Lemma 4.12 (Monotone coupling in β). If Pβ (i, j) is nondecreasing in β for all (i, j), then
there exists a coupling such that
                             β 1 ≤ β 2 ⇒ E( Gβω1 ) ⊆ E( Gβω2 )    a.s.

Proof. Use common uniforms Uij and the inclusion {Uij ≤ Pβ1 (i, j)} ⊆ {Uij ≤ Pβ2 (i, j)}.
■

                                               18
Renormalization group coarse-graining. We coarse-grain G by collapsing its recurrent
blocks (SCCs), in the spirit of RG block transformations (cf. [6]).
Definition 4.13 (SCC condensation RG map). Let C( G ) be the condensation digraph of G
(vertices are SCCs; edges record inter-SCC reachability). Define

                     R( G ) := C( G ),        G (0) = G, G (ℓ+1) = R( G (ℓ) ).
Lemma 4.14 (Condensation preserves reachability). For any digraph G and vertices u, v,
                         u ⇝ v in G ⇔ SCC(u) ⇝ SCC(v) in C( G ).

Proof. Map a path to SCC labels and delete repeats; conversely concatenate inter-SCC
edges with intra-SCC connectivity.                                                 ■
Conjecture 4.15 (β-catastrophe as emergence of a giant wandering SCC). For certain hard
discrete families, there exists β c ∈ (0, 1) such that the order parameter Φn ( β) from Def-
inition 4.10 undergoes a phase transition at β c . For β > β c , typical trajectories exhibit
long transients supported by the giant SCC of Gβ,n ↾ (Vn \ Sn ) before reaching Sn , causing
rapid growth (or divergence) of solution times as β ↑ 1.

  The heatmap diagnostics done in §5.1 can be viewed as empirical proxies for (i) acces-
sibility of Sn (entry probability) and (ii) recurrence within Vn \ Sn (mesoscopic recurrence
index), both of which are predicted to change sharply across β c under Conjecture 4.15.



5    Numerical Evidences

We consider the foundational framework in [3], where the learning problem was framed
as feasibility formulation. The training subproblem for a single sample is the feasibility
problem                                        \
                                      find z ∈   Cv .
                                                       v ∈V

For a mini-batch {( x (i) , y(i) )}iB=1 , the framework constructs a single enlarged computation
graph by replicating all data-dependent nodes per sample while sharing parameter nodes
across samples. Thus, parameter nodes have outgoing edges into every sample replica,
      par
and C p enforces cross-sample consensus automatically. The resulting feasibility prob-
lem can be written as
                                                                      
                                           B
                                           \     \  (i )      \     par
                          find z ∈                Cv  ∩         Cp  .
                                       
                                    i =1 v ∈V (i )            p∈Vpar
                                               data


                                                      19
There is a single edge-state z on a single (batch-expanded) graph; the only batch coupling
is through the shared parameter-node constraints. We provide an equivalence interpre-
tation that is useful to the set-valued and variational analysis, operator splitting, and
machine learning communities.
Theorem 5.1 (Two-level wire feasibility and canonical finite-sum inclusion). Fix N ∈ N.
Let Vdata be a finite index set of local relation types, Wact a finite index set of activation-
wire types, and Θ a finite index set of shared parameter wires. For w ∈ Wact let Hw ≃ Rdw ,
and for θ ∈ Θ let Hθ ≃ Rdθ .

 (i) (Local-copy wire lift). For each replica i ∈ [ N ] and each relation v ∈ Vdata , let
     W (v) ⊆ Wact ∪ Θ and define
                                 Hi,v :=        ∏       Hω ,       Mi,v ⊆ Hi,v .
                                             ω ∈W (v)

     Set
                                        N
                               H := ∏           ∏ Hi,v ,          x = ( xi,v ) ∈ H.
                                    i =1 v∈Vdata
 (ii) (Set-feasibility formulation). Define the product of local relations
                                                  N
                                        M := ∏             ∏ Mi,v ⊆ H.
                                                 i =1 v∈Vdata

     For each (i, w) ∈ [ N ] × Wact , let ∆i,w be the diagonal subspace enforcing equality of
     all copies of wire (i, w) across { xi,v }v . For each θ ∈ Θ, let ∆θ enforce equality of all
     copies of θ across all replicas. Define
                                         N                         
                             Dwire :=       ∏ ∏            ∆i,w × ∏ ∆θ ⊆ H.
                                            i =1 w∈Wact               θ ∈Θ

     The two-level wire feasibility problem is
                                             find x ∈ M ∩ Dwire .
(iii) (Finite-sum operator inclusion). Assume all Mi,v are nonempty and closed, and let
      NM denote the normal cone of M. Then the feasibility problem in (ii) is equivalent
      to the inclusion
              N                             N
           0∈∑      ∑ NMi,v (x) + ∑ ∑                      N∆i,w ( x ) +   ∑ N∆θ (x),   x ∈ H,   (31)
              i =1 v∈Vdata                  i =1 w∈Wact                    θ ∈Θ

     where each normal cone acts on its own coordinate block in H (and as zero else-
     where). In particular, JNM = PMi,v and JN∆ = P∆ , where P∆i,w is within-replica
                                i,v
     averaging and P∆θ is cross-replica averaging.

                                                      20
(a) Search and convergence times Tsearch ( β)        (b) Euler scaling of E[ Tconv ( β) | solved] for β ≤
and Tconv ( β).                                      0.3.

                 Figure 1: Local versus mesoscopic time scales in LEDM.


Corollary 5.2 (One-layer special case). In the one-layer case, the index set of local relations
can be taken as a Cartesian grid Vdata = [n] and replicas as [ N ] = [m], so that the local
constraints are naturally indexed by pairs (i, v) ∈ [m] × [n]. Then Theorem 5.1, yields a
feasibility model consisting of mn local relation blocks together with diagonal (consensus)
constraints enforcing equality of replicated variables [8].


5.1   Numerical evidence on one-layer LEDM instance

LEDM (Low-rank Euclidean Distance Matrix) is a one-layer nonnegative matrix fac-
torization feasibility problem in which a symmetric matrix Y ∈ Rm×m with entries
                         2
Yij = (i − j)/(m − 1) is factorized as Y ≈ WZ ⊤ with W, Z ≥ 0 and fixed rank. This
fits the one-layer special case of Corollary 5.2, and hence the two-level wire feasibility
formulation of Theorem 5.1. We run the RRR iteration with hyperparameters fixed as in
[3]: batch size B = m, rank r+ = m − 1, normalization Ω ∈ [0.6, 0.9] depending on m, and
iteration budgets up to kmax = 2 × 104 to 1.2 × 105 . The observable is the reconstruction
residual err( xk ). All quantities are averaged over multiple random initializations. The
experiments are intended to characterize dynamical regimes rather than to benchmark
performance.


Two-phase decomposition. Fix tolerances 0 < δsolve < δenter with δenter = 10−2 and
δsolve = 3 × 10−2 . Define the discrete hitting indices
                                                                   
 kenter ( β) := inf k ≥ 0 err( xk ) ≤ δenter ,    ksolve ( β) := inf k ≥ 0 err( xk ) ≤ δsolve ,



                                                21
and the corresponding flow-time quantities
                                                                                       
            Tsearch ( β) := β kenter ( β),    Tconv ( β) := β ksolve ( β) − kenter ( β) + .

Figure 1 (left) reports empirical means of Tsearch ( β) and Tconv ( β). The data show that
Tsearch dominates the total runtime across all β, while Tconv remains comparatively small
whenever entry occurs. This directly reflects the locality of the flow analysis in §4: Theo-
rems 3.1-3.3 govern only the post-entry regime.


Euler scaling in the regular regime. Conditioning on successful entry/solve, we restrict
to a small-β window β ≤ 0.3 and fit the conditional mean convergence time

                                 E[ Tconv ( β) | solved] ≈ a + b β.

Figure 1 (right) displays the fit, with coefficient of determination R2 ≈ 1. This linear scal-
ing is consistent with the first-order Euler discretization of the limiting flow (Theorem 3.3)
and the local contraction properties established in Theorem 3.1 and Theorem 3.7.


Non-local diagnostics over problem size.           To characterize dynamics prior to entry, for
each (m, β) define the entry probability

                               penter (m, β) := P(kenter ( β) < kmax ) ,

estimated empirically under a fixed iteration budget kmax .                Figure 2 (left) displays
penter (m, β).

   To quantify non-local wandering before entry, log the error trace {err( xk )}kT=1 and de-
fine a coarse state
                                                                               
                sk := π (err( xk )) ∈ {0, . . . , B − 1}, π (r ) := bin log10 r ,

using quantile binning. The mesoscopic recurrence index is
                               "                                          #
                                         T
                                   1
                                 T − w k=∑
                  R(m, β) := E                1{sk ∈ {s1 , . . . , sk−1 }} ,
                                         w +1

with fixed burn-in w. Figure 2 (right) displays R(m, β). Larger values indicate increased
recurrent or mixing behavior prior to entry, complementing the local flow description.

  Thus, figures 1 and 2 jointly suggests that: local flow-limit theory accurately predicts
Tconv once entry occurs, while global performance and the β → 1 deterioration are gov-
erned by non-local, instance-dependent entry dynamics, as anticipated in §4.4.

                                                  22
       (a) Entry probability penter (m, β).              (b) Mesoscopic recurrence index R(m, β).

            Figure 2: Non-local diagnostics across problem size and step size.

6    Conclusion and outlook

This paper develops a rigorous dynamical-systems description of the Reflect-Reflect-
Relax (RRR) algorithm in the small-step regime, centered on the limiting flow ẋ = v( x )
governing the behavior of RRR as β ↓ 0.

  In the smooth transversal setting (S1), each feasible intersection x ∗ ∈ A ∩ B is shown
to be a hyperbolic sink of the flow, with strictly negative real spectrum of Dv( x ∗ ) on the
transverse subspace and exponential decay of the gap g( x ) = ∥v( x )∥ (Theorem 3.1). Un-
der uniform geometric assumptions, this local structure extends to a positively invariant
tubular neighborhood Tr of the feasible manifold, where E( x ) = 21 ∥v( x )∥2 is a strict Lya-
punov function and no recurrent or chaotic dynamics occur (Theorem 4.2, Corollary 4.3).

   In the discrete regime (S2), the limiting vector field is piecewise constant on W-domains.
We showed that convergent two-cell boundaries support Filippov sliding with explicit
sliding velocity, and that, under genericity assumptions, finite descent chains of W-
domains lead to finite-time capture into a solution cell (Theorem 3.2).

   The continuous and discrete descriptions are connected by proving that small-step RRR
is a forward-Euler discretization of the flow with O( β) trajectory error on finite time in-
tervals, including across sliding segments (Theorem 3.3). As a consequence, hitting times
of any fixed gap threshold δ > 0 satisfy
                                 t∗δ ( β; x0 ) → Tδ∗ ( x0 )   as β ↓ 0,
while the iteration count diverges like 1/β (Theorems 3.4 and 3.5). A discrete Lyapunov
inequality further yields exponential convergence rates for the iterates consistent with the
flow analysis (Theorem 3.7).

  Numerical experiments on a one-layer LEDM instance support this picture (§5.1),
showing that local convergence follows the predicted Euler scaling once a regular regime

                                                   23
is reached, while overall runtime is dominated by a distinct mesoscopic entry phase
whose dependence on β is non-local and instance-dependent. This separation clarifies
both the scope of the flow-limit theory and the origin of the deterioration observed near
the Douglas-Rachford limit β ↑ 1.


Outlook. Extending the analysis to global phase portraits of the RRR flow and map,
particularly in the infeasible case A ∩ B = ∅ where numerical evidence suggests com-
plex invariant sets, chaotic attractors, and long transients, remains open. In the discrete
setting, while generic finite descent chains were established, a quantitative theory relat-
ing geometric properties of the W-domain adjacency graph (connectivity, diameter, ex-
pansion, recurrent classes) to entry times, mixing times, coupling times, or hitting-time
distributions is largely undeveloped. Moreover, numerical evidence indicates that the
regime β ↑ 1 is governed by non-local, instance-dependent wandering and metastability
not captured by local flow analysis; developing rigorous criteria for such β-driven tran-
sitions and relating them to coarse-grained or renormalized descriptions of the induced
cell dynamics is an important direction for future work.



References
[1] Bernard Brogliato. Nonsmooth Mechanics: Models, Dynamics, and Control. Communica-
    tions and Control Engineering. Springer, Cham, 3 edition, 2016.
[2] Rick Durrett. Random Graph Dynamics. Cambridge University Press, 2006.
[3] Veit Elser. Learning without loss. Fixed Point Theory and Algorithms for Sciences and
    Engineering, 2021(1):12, 2021.
[4] Veit Elser. Solving Problems with Projections: From Phase Retrieval to Packing. Cambridge
    University Press, 2025.
[5] A. F. Filippov. Differential Equations with Discontinuous Righthand Sides, volume 18
    of Mathematics and Its Applications. Kluwer Academic Publishers, Dordrecht, 1988.
    Translated from the Russian original (1985).
[6] Nigel Goldenfeld. Lectures on Phase Transitions and the Renormalization Group. Frontiers
    in Physics. Addison–Wesley, 1992.
[7] Geoffrey Grimmett. Percolation. Springer, 2 edition, 1999.
[8] Manish Krishan Lal. Nonconvex Projections Arising in Bilinear Mathematical Models. PhD
    thesis, The University of British Columbia, 2023.


                                             24
