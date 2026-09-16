                                                 How densely can spheres be packed with moderate effort in high dimensions?
                                                                                                    Veit Elser
                                                                                    Department of Physics, Cornell University
                                                                                               Ithaca, NY 14853

                                                          We generate non-lattice packings of spheres in up to 22 dimensions using the geometrical constraint
                                                        satisfaction algorithm RRR. Our aggregated data suggest that it is easy to double the density of
                                                        Ball’s lower bound, and more tentatively, that the exponential decay rate of the density can be
                                                        improved relative to Minkowski’s longstanding 1/2.
arXiv:2305.13492v2 [math.MG] 11 Jul 2023




                                                            I.   INTRODUCTION                               able to further improve c when n is divisible by four and
                                                                                                            Venkatesh [10] found that c could be replaced by log log n
                                              The packing of congruent spheres in Euclidean space           for very special n.
                                           has important practical implications and is a seemingly             These increasingly sophisticated bounds, all based on
                                           unbounded source of theoretical questions. A major               lattices, stand in stark contrast to a bound that makes
                                           recent success was the discovery by Viazovska [1] and            no reference to lattices at all and can be proved in five
                                           coworkers [2] of modular functions that make the Cohn-           sentences. A set of sphere centers Sn∗ is “saturated” for
                                           Elkies linear programming density upper bound [3, 4]             spheres of radius r if it is impossible to add another
                                           sharp for the E8 and Leech lattices, proving that these          sphere, also of radius r, without intersecting an exist-
                                           lattice-based schemes for packing spheres are the dens-          ing sphere. This property implies all points not covered
                                           est possible in eight and 24 dimensions. By contrast, the        by a sphere are within distance 2r of one of the sphere
                                           subject of lower bounds on achievable densities is much          centers. By doubling all the sphere radii, all of these
                                           murkier and progress seems to have stalled.                      points will be covered as well. But this could not happen
                                              Minkowski [5] was the first to find a lower bound for         if ∆(Sn∗ ) < 2−n , since doubling the radii increases each
                                           general dimension n that was superior to the density             sphere volume by 2n . We therefore know that
                                           achieved by any of the known packing schemes available
                                                                                                                                   ∆(Sn∗ ) ≥ 2−n .
                                           for arbitrary n. For example, a simple scheme is to cen-
                                           ter the spheres on the n-dimensional checkerboard lattice        Like the lattice-based bounds, this construction is not
                                           Dn , the subset of integer lattice points with even coor-        constructive in a practical sense. On the other hand,
                                           dinate sum. This gives the optimal density for n = 3 [6]         it reveals that matching the leading asymptotic part of
                                           and is also believed to be the best possible for n = 4 and       the sophisticated bounds is already achieved by a greedy
                                           5. On the other hand, the density ∆, or fraction of space        algorithm. Information on where spheres can be placed
                                           covered by spheres, decays as                                    is provided by the Voronoi diagram of the sphere centers
                                                                       1  eπ n/2                          already placed, something that can be locally updated in
                                                           ∆(Dn ) ∼ √                 ,                     a sequential construction of a periodic saturated packing.
                                                                       4πn n
                                                                                                               The crudeness of saturated packings suggests that easy
                                           which is much faster than Minkowski’s bound whose lead-          improvements on the lower bound should be possible just
                                           ing behavior is 2−n .                                            by dropping the lattice constraint. Theoretically this pro-
                                             Like Minkowski’s result, recent advances are also based        posal is still difficult because no one knows how to even
                                           on lattices and have asymptotic densities                        mildly enhance the density in a way that is also amenable
                                                                          n                                 to computations. Torquato and Stillinger (TS) [11, 12]
                                                                      c      ,                              have conjectured the existence of packings that have a
                                                                          2n
                                                                                                            particular limiting form of the sphere-center autocorre-
                                           with improvements in the value of the constant c. The            lation (pair distribution function) g2 in high dimensions.
                                           current best bound, for general n, is Ball’s bound [7]           If such packings exist, then the dominant 2−n behavior
                                                                                                            of the density would be improved to bn , with b ≈ 0.583.
                                                                           n−1
                                                            ∆ > ∆B =            ζ(n) ,                      The constrained optimization of g2 used by TS to ob-
                                                                           2n−1                             tain this b can be interpreted as an infinite-dimensional
                                           corresponding to c = 2. Ball’s result hinges on a lemma          linear program (LP) dual to the LP used by Cohn and
                                           in Bang’s proof of the “plank problem” [8] and cor-              Elkies [3, 4, 13] to establish upper bounds on the den-
                                           responds geometrically to the transformed problem of             sity. In this setting the TS-conjectured lower bound is
                                           custom-fitting a thin oblate ellipsoid in the integer lattice    a rigorous lower bound on the upper bounds that can
                                           that avoids all lattice points except the origin. Though         be achieved with the LP method. However, this “lower
                                           only the existence of the ellipsoid is established, and the      bound on the upper bounds” may well be above real-
                                           corresponding packing is not explicitly constructed, the         izable densities if it turns out that packings with the
                                           value c = 2 appears as a sharp estimate because the el-          conjectured g2 do not exist. To add perspective to the
                                           lipsoid is constrained all over its surface. Vance [9] was       Torquato-Stillinger constant 0.583, we note that by the
                                                                                                                        2

Kabatiansky-Levenshtein upper bound [14], the decay           physics that tries to eliminate the effects of boundaries,
constant of the density is less than 0.661.                   we look for asymptotic behavior only with respect to the
   This study was prompted by the dearth of evidence          dimension n. Even when confined to the smallest torus,
that could inform the pursuit of an improved lower            the fraction of a sphere’s surface available for contacts
bound. The blindest saturated packing construction,           with other spheres approaches 100% in high dimensions.
called random sequential addition (RSA), is an obvious        We use this property to help assess whether the asymp-
source of data [15]. In RSA, sphere placement is not in-      totic regime (in dimension) has been accessed.
formed by the Voronoi diagram (e.g. filling the smallest
available hole), but is sampled uniformly on the available
set. Accurate estimates of the saturation densities have                     II.   RRR ALGORITHM
been obtained in up to eight dimensions [16]. These data
are consistent with b = 1/2, and that may not be surpris-        The RRR algorithm [20] searches for a point x ∈ A∩B,
ing because this dominant behavior was proved for the         where A and B are sets in some Euclidean space. The
related ghost-RSA construction [17].                          elementary operations of the algorithm are the projectors
   Physics inspired constructions, also called simulations,   PA and PB . The point PA (x) is the element of A nearest
have generated data in up to 12 dimensions [18]. The          to x, and similarly for B. When a set is not convex
most widely used is the Lubachevsky–Stillinger algo-          there can be multiple nearest points, but only for x in a
rithm [19], where spheres execute Newtonian dynamics          set of measure zero. Since our computations have finite
with a simple billiard-type collision rule. Initially the     precision, the implementations of the projections always
spheres are small and easily packed into a simulation cell    output unique points.
with periodic boundary conditions. As the spheres redis-         After selecting an initial point x, RRR iterates the map
tribute themselves through collisions, they are also made
to slowly grow in size. Eventually the redistribution of               x 7→ x′ = x + β (PB (RA (x)) − PA (x)) .       (1)
the spheres, into more loosely packed configurations that
allow continued size-growth, slows so dramatically that       Here RA (x) = 2PA (x) − x reflects in constraint set A
the simulation cannot be continued any further. The           and β is a parameter analogous to a time step. When
highest densities achieved by this method, in 12 dimen-       A and B are locally affine, as they are in the sphere
sions, are about 88% higher than Ball’s bound [18].           packing problem, RRR locally converges to fixed-point
   We present two kinds of data of relevance to the lower     sets X ∗ associated with solutions x∗ ∈ A ∩ B. Though
bound problem. Both are generated by the general pur-         fixed-point convergence is assured by the convexity of the
pose relaxed-reflect-reflect (RRR) algorithm [20]. RRR        affine local approximations of A and B, RRR performs
is a generalization, to general constraint sets, of the       something analogous to an actual search when A and B
constraint satisfaction algorithm used in phase retrieval.    are not convex. One of the sets in the sphere packing
Provided the problem at hand can be formulated as the         problem is nonconvex. RRR derives its name from the
search for a point in the intersection of sets A and B        form it takes when (1) is entirely expressed in terms of
in some Euclidean space, and projections to these sets        reflectors. For additional background on this approach
can be computed efficiently, the application of RRR is        to solving problems see [23, 24].
straightforward.
   Though RRR can find some of the densest-known pack-
ings, such as Best’s packing in ten dimensions [21, 22],           III.   A AND B FOR SPHERE PACKING
our focus has been on what density improvements are
possible with only moderate effort. In our first applica-        We used divide-and-concur [25] to define A and B,
tion of RRR we find packings that exactly double the          where variables are given multiple copies to make con-
density of Ball’s bound while taking careful account of       straint projections easy. In the sphere packing problem
the effort involved. Our results extend to 22 dimensions      we use (N2 ) pairs of n-tuple (sphere center) variables. For
and look like they can be continued indefinitely. In the      example, xij is the copy of sphere center i “that cares
second, more ambitious application, we do not set a den-      about” sphere j, and vice versa for xji . For all pairs
sity goal and instead specify a moderate level of computa-    (i, j), the projector PA moves the centers xij and xji by
tional effort. These results extend to 19 dimensions and      the minimum distance to make their spheres tangent if
the resulting densities support the existence of a bound      they intersect and does nothing if these sphere-copies are
with b > 1/2, though less convincingly than the conclu-       already disjoint. The other projector, PB , implements
sion of the first study.                                      “concur” by restoring equality to the copies in a distance
   A key part of both studies is to demonstrate that the      minimizing way. The total number of (replicated) vari-
experiments have crossed into the asymptotic regime, so       ables, N (N − 1)n, is the dimension of the space in which
that the data are relevant for the lower bound question.      RRR executes the search.
Our handle on this is to pack spheres into the small-            Finding distance-minimizing displacements that make
est possible n-torus, whose period equals the sphere di-      two spheres tangent when they intersect (set A), and the
ameter. Instead of the usual “thermodynamic limit” of         concurring point nearest to N −1 copies (set B), are both
                                                                                                                               3

                                                                        1.0
easy computations. Details, including complications that
arise because of the torus geometry, are provided in the
appendix. Our implementation also allows the metric
that defines the projections to adiabatically adjust to cir-            0.8
cumstances. Though all the spheres are identical, their
equivalence under constraint projections is broken al-
ready in the initial, randomly generated configuration.
                                                                        0.6
This has many sphere intersections, some spheres worse
off than others. Details for the general metric-update
heuristic we used that addresses such inequities can also          fn
be found in the appendix.                                               0.4




           IV.    PACKING THE n-TORUS
                                                                        0.2

  Our RRR sphere packing implementation packs N
unit-diameter spheres in the n-torus of width w:
                                                                        0.0
                    Tn (w) = Rn /(wZ)n .                                      10           20              30       40    50

                                                                                                       n
When extended periodically this realizes a packing of Eu-
clidean space with density                                       FIG. 1: Fraction of the sphere of radius 1 available for tan-
                                                                 gencies when spheres are packed in the unit n-torus.
                                 vn (1/2)
                      ∆=N                 ,
                                   wn
where vn (r) is the volume of the n-ball of radius r. To         where
keep N small in high dimensions we used the smallest                               am = vol(Sm (1)) = mvm (1)
possible width, or the unit torus of width w = 1. Though
our packings are in many respects random, in the unit            is the volume of the unrestricted m-sphere,
torus each sphere will at least be tangent to 2n others
(when the packing is extended periodically). Packing                                            3
                                                                                                X            
                                                                                                           ℓℓ  n
more than one sphere in the unit torus first becomes pos-                          b(n, k) =          (−1)
                                                                                                            k  ℓ
sible in four dimensions, and the optimal packing, of two                                       ℓ=k
spheres, is unique.
                                                                 is a combinatorial factor, and
   Unit diameter spheres with centers x1 and x2 that
are tangent in Euclidean n-space can be packed in Tn (1)                            Z
                                                                                                           n−2−k
only if x1 and x2 have no coordinate differences greater                  c(n, k) =             1 − kzk22     2
                                                                                                                  ,
                                                                                        z∈Ck (1/2)
than 1/2 in absolute value. When this is not the case,
then one sphere has a coset representative with a smaller        is an integral over the k-cube with c(n, 0) = 1. When
coordinate-difference magnitude, giving it a smaller dis-        interpreting our packing experiments we will refer to the
tance to the other sphere, in violation of the packing           plot of the fraction of the tangency volumes, fn = ãn /an ,
constraint.                                                      shown in Figure 1.
   The set of torus-restricted-tangencies just described,
that is, the allowed set of center differences z = x1 − x2 ,
is the set                                                               V.   EXPERIMENTS WITH TORUSPACK

                 Sen (1) = Sn (1) ∩ Cn (1/2) ,             (2)
                                                                   The main inputs for our RRR implementation, called
where Sn (1) is the unit radius n-sphere and                     toruspack [26], are the dimension n, the number of spheres
                                                                 to be packed N , and the torus width w. In this study
            Cn (1/2) = {z ∈ Rn : kzk∞ ≤ 1/2}                     we always set w = 1 except when we want to specify
                                                                 a precise value for the density. In that case we let the
is the centered n-cube of unit width. In the appendix we         density determine a fractional N with w = 1, round this
provide details for the formula (n > 3)                          upward to the nearest integer, and then compensate by
                                                                 appropriately increasing w. Because N grows rapidly
         vol(Sen ) = ãn                                         with n, the value of w even in these experiments is only
                      3
                      X                                          very slightly greater than 1.
                  =         (−1)k an−k b(n, k) c(n, k) ,   (3)     The other inputs relate to the behavior of RRR and are
                      k=0                                        not special to the sphere packing problem. Though local
                                                                                                                                          4

                     0.8                                                       is always in set B, where each sphere has perfectly con-
                                                                               curring copies, but is otherwise uniformly sampled in the
                                                                               n-torus.
  normalized error

                     0.6                                                          The small run-to-run variation in I for the lower bound
                                                                               instances is related to the near monotonicity of the error
                                                                               time series in these relatively easy packing problems. In
                     0.4
                                                                               order to have control over the degree of difficulty, torus-
                                                                               pack has a parameter m called the “monotonicity.” A so-
                                                                               lution is m-monotone if for every iteration i, the error sat-
                     0.2
                                                                               isfies ǫi+m < ǫi . The easiest instances, where the error is
                                                  n = 10    N = 40             strictly decreasing, have 1-monotone solutions. Runs are
                                                                               terminated by toruspack as soon as the m-monotonicity
                     0.0
                           0   20 000   40 000   60 000    80 000    100 000   criterion is violated and the trial is declared unsuccess-
                                          iterations                           ful. A packing instance, or (n, N ) pair, has m-monotone
                                                                               difficulty if a successful run with monotonicity param-
FIG. 2: Error time series in four runs of packing 40 spheres in                eter m has probability one-half (when sampling initial
ten dimensions, three of which found Best’s packing in under                   points). In our second experiment we find the densi-
105 iterations.                                                                ties of packings that have 100-monotone difficulty. Using
                                                                               toruspack this means fixing n and m, then performing
fixed-point convergence is fastest when β = 1 is used for                      trials with increasing N to identify the largest N (n, m)
the RRR time step, smaller values are more productive                          before the success probability drops below one-half. Fig-
when the search is faced with nonconvex constraints. We                        ure 3 shows successful error time series for packings in
used β = 0.5 in all the experiments. The parameter that                        14 dimensions and difficulty ranging from 1-monotone to
controls the update-rate of the metric was set at the same                     1000-monotone. The time scales have been stretched to
small value, γ = 10−3 , in all the experiments except the                      have the same extent to highlight the qualitative differ-
one instance of a hard search (Best’s packing), where we                       ences. The actual number of iterations and related infor-
used γ = 10−2 .                                                                mation is given in Table I. In all except the m = 1 runs
   The algorithm’s progress is monitored via the normal-                       there is a very short initial rise in the error. We interpret
ized error                                                                     this as transient behavior associated with the initial point
                                  √                                            exactly satisfying constraint B. The m-monotonicity cri-
                    ǫ = kx′ − xk/ N ,                                          terion is imposed only after this maximum error has been
                                                                               passed.
which may be interpreted both as the current root-mean-
                                                                                  The fixed point convergence shown in Figures 2 and
square 2-norm of the distances moved by the copies of
                                                                               3 are qualitatively different and are misleading, as pre-
each sphere, as well as the current proximity to a solution
                                                                               sented. Not only is the overall error-behavior of the easy
— since ǫ = 0 corresponds to a fixed point. Figure 2
                                                                               instances quasi-monotone, the rate of convergence ac-
shows the time series of ǫ in four runs with n = 10,
                                                                               celerates. We believe this is simply related to the fact
N = 40 and w = 1. This is a hard instance, with ǫ
                                                                               that these packings are inherently disordered, where all
behaving chaotically. The occasional dips to small values
                                                                               spheres are able to rattle around, though typically in a
indicate the discovery of near solutions, where only a
                                                                               very small free volume. The concur projection PB at least
few concurring spheres are intersecting, or only a few
                                                                               provides a mechanism that can keep spheres from being
spheres are unable to settle on concurred positions, or a
                                                                               tangent in a solution. But whereas the constraint prob-
combination of these. Eventually, when a true solution
                                                                               lem for the easy instances becomes increasingly trivial
is found, ǫ goes all the way to zero. In this instance it
                                                                               with time, this is not the case in hard instances, where
is Best’s packing [21, 22], the best known for n = 10, in
                                                                               spheres have many tangencies in a solution. The late
which the sphere centers form a binary code of Hamming
                                                                               stage convergence of Best’s packing (not shown in Figure
distance four.
                                                                               2) is in fact much slower than in a disordered packing,
   In all the experiments we terminate runs and declare
                                                                               and runs were terminated already at ǫ < 10−2 . Best’s
them successful when ǫ falls below 10−4 . The number
                                                                               packing, of course, was easy to confirm by rounding co-
of iterations I needed to find solutions is interesting be-
                                                                               ordinates.
cause it measures the computational work, but depends
unpredictably on the random initial point. Though the
run-to-run variation in I is much smaller for our “lower-
                                                                                                    VI.   RESULTS
bound instances” than it is for Best’s packing, the de-
termination of accurate values for the average number of
iterations, I, is important for some of our results. To                                      A.   Doubling Ball’s density
facilitate this, another toruspack input allows the user to
specify the number of “trials,” or separate runs differ-                        Figure 4 shows the growth in the average number of
ing only in the initial random point x0 . The point x0                         RRR iterations, I n , to pack spheres at twice the density
                                                                                                                                                              5

                             m=1    m = 10       m = 102          m = 103
                                                                                                           Δ = 2ΔB
                        1



                                                                                                1000

                     0.100
  normalized error




                                                                              iterations
                                                                                                 500



                     0.010




                     0.001                                                                       100



                                                                                                  50

                      10-4

                                                                                                                10                 15               20

                                                                                                                          n
                                             iterations
                                                                             FIG. 4: Average number of iterations I n used by RRR to
FIG. 3: Representative time series of the normalized error                   pack spheres in n dimensions at twice the density of Ball’s
when packing spheres in 14 dimensions as the monotonicity                    bound.
m is increased from 1 to 103 . The horizontal scales were
stretched to aid comparison. Table I gives the actual number
of iterations and the number of spheres packed for each m.                                      1.8

                                                                                                                                             Δ = 2ΔB
                     m                 1        10          102        103
                                                                                                1.7
                     N (14, m)        17        42          115        164
                     ∆/∆B          0.392     0.968        2.651      3.780
                                                                                                1.6
                     I                59       163         1190       3980
                                                                              iteration ratio




                     δI/I          0.092     0.047        0.070      0.184
                                                                                                1.5

TABLE I: Growth in the number of spheres N (14, m) that
can be packed in 14 dimensions as the monotonicity m is in-                                     1.4
creased. Also tabulated is the density relative to Ball’s bound,
the average number of iterations, and the normalized standard
deviation in the number of iterations.                                                          1.3



                                                                                                1.2


of Ball’s bound. The results are consistent with simple
                                                                                                1.1
exponential growth beyond 16 dimensions, as shown in
the plot of the ratios I n+1 /I n in Figure 5. Our reach                                               6    8   10   12       14        16     18        20
into high dimensions was limited not so much by the ex-                                                                   n
ponential growth in the number of iterations, but the
super-exponential growth in the number of spheres be-                        FIG. 5: Successive ratios I n+1 /I n of the iteration counts
ing packed. For n = 22 RRR was packing N = 11397                             plotted in Figure 4.
spheres, and the divide-and-concur scheme works with
O(N 2 ) variables. By using neighbor lists this number
can be reduced, but not by all that much since most
pairs of spheres in the unit torus are neighbors for mod-                    Ball’s lower bound on the packing density can at least be
erate n. However, the particulars of the growth in time                      doubled.
and memory are mostly irrelevant for what we are aim-                          The transient behavior in I n for n < 16 is likely a torus
ing to demonstrate, which is showing that we can count                       artifact. The fraction fn of the unit-distance sphere avail-
on the algorithm being able to complete its task for arbi-                   able for tangencies in the n-torus, plotted in Figure 1, has
trary n. A negative result would be signs that the num-                      an inflection point at this dimension. It appears that the
ber of iterations might diverge at some n. The absence                       torus restriction makes the task of packing spheres easier,
of such signs in our experiments raises confidence that                      at least for density 2∆B .
                                                                                                                                 6

                 n      N (n, 100)       I                                           R         2ΔB            b k
                 6               4      71                           
                 7               5     237
                 8               8     293
                 9              12     454
                10              18     471                           
                11              29     588
                12              46     736
                13              72     869
                                                                Δ 0 
                14        115 ± 2     1190
                15        156 ± 1     1080
                16        274 ± 2     1410
                17        507 ± 1     1960
                18        967 ± 2     2830
                                                                   5 × 10   -4




                19       1884 ± 3     4240

TABLE II: Number of spheres N (n, 100) that RRR can pack
in the unit n-torus with 100-monotone difficulty, along with                     6     8   10     12      14       1        18
the average number of iterations. These are the data that                                             n
were used for the density shown in Figure 6.
                                                               FIG. 6: Density of 100-monotone packings found by RRR
                                                               compared with twice Ball’s bound and the best known pack-
       B.    Density of 100-monotone packings                  ings.


   One approach for gaining information about the pos-
sibility of b > 1/2 in the decay of the lower bound would      largest N (n, 100) for which p − σ > 1/2, while the largest
be to try various b’s and, as in the previous section, look    candidate is the largest N (n, 100) for which p + σ > 1/2.
for signs that the number of RRR iterations will diverge       The uncertainties given in Table II correspond to half the
beyond some value of b. But this is unlikely to produce        difference of these extreme estimates of N (n, 100). We
convincing results because one would also have to spec-        performed 100 trials for each N (n, 100).
ify the equally unknown subdominant behavior of the               The densities associated with the data in Table II are
bound, whose effect may be as large as an increase in b,       plotted in Figure 6 and compared with 2∆B and the dens-
which is surely small if nonzero.                              est known packings. In this plot the uncertainties are
   We have taken an alternative approach, where the de-        smaller than the plotting symbol. The former become no-
gree of ‘moderate effort’ is specified through the mono-       ticeable in the plot of the density ratios in Figure 7. Both
tonicity m of the solution process. As shown in Figure 3,      plots are consistent with the interpretation given earlier,
the time series of the normalized error is suggestive of a     that the tight unit-torus constraint makes packing eas-
reliable route to packings for m as large as 103 . We chose    ier, but that this effect wears off above 16 dimensions.
m = 100 because this lowers the average number of iter-        Like the 2∆B experiments, here it appears we have also
ations and also the number of spheres to be packed. The        just barely been able to access the asymptotic regime.
small run-to-run variation in the number of iterations,        Though the ratios are plotted against 1/n, the data do
δI/I = 0.07 for n = 14 (Table I), also lends support to        not extend to large enough n and the uncertainties are
the assertion that RRR can be counted on to complete           too large to attempt an estimate of b by extrapolating to
its task at this degree of effort.                             n = ∞. Still, it appears that a lower bound with b > 1/2
                                                               is not easily ruled out by these results.
   The number of spheres N (n, 100) that can be packed
by the m = 100 criterion are given in Table II. For small
n these numbers are known with high accuracy. That is
because enough trials can be performed to establish that              C.         Binary-code coordinate modulation
N (n, 100) spheres have 100-monotone solutions in over
50% of trials, while this drops below 50% for N (n, 100) +       Additional evidence that torus artifacts are absent
1 spheres. For larger n the uncertainties in N (n, 100)        above n = 16 can be seen in the distribution of coor-
are estimated as follows. T trials are performed for a         dinate values of the packed spheres, shown in Figure 8.
range of equally spaced candidate values of N (n, 100)         In a disordered packing, without periodicity imposed by
and the number of successful 100-monotone solutions S          an n-torus, the coordinates should have a uniform distri-
is tabulated for each of them. The success probability is      bution. While this is what we see above 16 dimensions,
estimated as p = S/T , with standard uncertainty σ =
p                                                              there are strong departures in lower dimensions. As epit-
   p(1 − p)/T . The smallest candidate is identified as the    omized by Best’s packing, the unit-torus is the perfect
                                                                                                                                                                  7

                                                                     ΔB
                       0.70                                                                                10
                                                                                                                                       n = @A   N = BCDE


                       89:;
                                                                                                            5



                                                                                                  g2 (r)
                       2347
                                                                                                            1

 rn ,-./
                                                                                                           0.5
                                                                                                                 1.00        1.05      1.10     1.15       1.20

                       ()*+                                                                                                            r

                                                                                                FIG. 9: Sphere-center autocorrelation function g2 (r) for the
                       $%&'                                                                     100-monotone packings in 19 dimensions.


                                                                                                After alignment, the distributions for all n dimensions,
                       0.40
                          0.00                               0.10               !"#         and all the successful 100-monotone packings, were com-
                                                          1/n                                   bined into a single distribution.

FIG. 7: Successive ratios rn = ∆n+1 /∆n of the 100-monotone
densities of Figure 6 plotted against 1/n.                                                                       D.     Sphere center autocorrelation

                                    n = 14              n = <=           n = >?                     Because of the compact nature of our torus constraint,
                         5                                                                      the sphere center autocorrelations g2 of our packings
                                                                                                are probably not good tests of the Torquato-Stillinger
                                                                                                conjectures [11]. The g2 (r) function for our highest-
                                                                                                dimension (n = 19) and densest (N = 1890) packing
 probability density




                                                                                                is plotted in Figure 9. To avoid the normalization com-
                         2
                                                                                                plications arising from the torus, these were created by
                                                                                                filling center-center distance bins (r), first for the spheres
                                                                                                of the packing, and also for an equal number of uniformly
                         1                                                                      distributed random points. The plot shows the ratio of
                                                                                                the two kinds of bin counts.

                       0.5
                                                                                                                           VII.     OUTLOOK
                              0.0   0.2           0.4            0.6          0.8         1.0

                                                           x                                       The endurance of Minkowski’s 2−n leading-order be-
                                                                                                havior of the sphere packing density lower bound can be
FIG. 8: Disappearance of the binary-code coordinate modu-                                       interpreted in two ways. Either it represents something
lation above 14 dimensions.                                                                     fundamental that has resisted proof, mostly for lack of
                                                                                                imagination on how that can be done. The other pos-
                                                                                                sibility is that packings with a slower decay exist, but
scaffolding for packings with a Hamming-distance-4 bi-                                          that constructions analogous but better than saturated
nary code structure. Though the 100-monotone packings                                           packings have likewise eluded the imagination. Though
are disordered and far from a binary code, the distribu-                                        experiment will never replace proof (and imagination),
tion of coordinates shows a strong binary modulation in                                         it can provide guidance on which of these alternatives is
low dimensions. Figure 8 shows how the amplitude of                                             the more promising one to pursue.
this modulation rapidly decays above 14 dimensions. To                                             In this study we showed that the RRR algo-
create these distributions we applied independent shifts                                        rithm is a good source of data for the lower bound
s to the coordinates in each of the n dimensions that                                           question. Like random sequential addition and the
maximize the sums                                                                               Lubachevsky–Stillinger algorithm [19], RRR is a sim-
                                          N
                                          X                                                     ple dynamical system, appropriate for constructing
                                                cos 4π(xi + s) .                                the disordered packings that prevail at the lower
                                          i=1                                                   bound.       Unlike random sequential addition, but
                                                                                                                             8

like Lubachevsky–Stillinger, RRR acts synchronously               advantage of Dn over Zn is that the spheres will have
on the spheres in the packing.            However, unlike         a much rounder environment. For example, the analo-
Lubachevsky–Stillinger, RRR is not prone to jamming               gous inflection point in the fractional volume available
and glassy behavior.                                              for tangencies (Figure 1) occurs already at n = 12. This
   Our two sets of results fall short of the level one has        lowering of the asymptotic regime will have a greater ben-
come to expect, say in statistical mechanics, for support-        efit than extending the range in n through neighbor lists.
ing hypotheses in intractable problems. Though the ex-            Also, with this scale for Dn the cosets of (Z/2)n /Dn sup-
periments have nearly doubled the reach into high dimen-          port dense packings in much the same way as (Z/2)n /Zn
sions, even higher dimensions are needed to convincingly          (Hamming-distance-4 codes). The disappearance of a co-
eliminate “torus artifacts.”                                      ordinate modulation with n (Figure 8) could again be
   Using neighbor lists and allocating divide-and-concur          used to assess the homogeneity of the packings. Hard
copies only for neighbors will certainly cut down on mem-         sphere liquid simulations have also used Dn boundary
ory as well as the time per iteration. But only a few extra       conditions [27].
dimensions can be gained in this way. A more significant
improvement is possible in principle by modifying the
periodicity of the packings. Instead of using the tightest
possible “cubic” cell for unit diameter spheres, Zn , we
                                                                                     Acknowledgements
propose using the checkerboard lattice Dn to define the
periodicity. This is not the tightest
                                  √ possible cell with that
symmetry — that would be Dn / 2 — but the one having                I thank Keith Ball for providing unpublished material
the same volume, up to a factor of two, as Zn . The main          on his lower bound.




 [1] M. S. Viazovska, Annals of Mathematics , 991 (2017).         [21] M. Best, IEEE Transactions on Information Theory 26,
 [2] H. Cohn, A. Kumar, S. Miller, D. Radchenko, and M. Vi-            738 (1980).
     azovska, Annals of Mathematics 185, 1017 (2017).             [22] J. H. Conway and N. J. A. Sloane, Designs, Codes and
 [3] H. Cohn and N. Elkies, Annals of Mathematics , 689                Cryptography 4, 31 (1994).
     (2003).                                                      [23] V. Elser, I. Rankenburg, and P. Thibault, Proceedings of
 [4] H. Cohn, Geometry & Topology 6, 329 (2002).                       the National Academy of Sciences 104, 418 (2007).
 [5] H. Minkowski, Journal für die reine und angewandte          [24] S. B. Lindstrom and B. Sims, Journal of the Australian
     Mathematik 130, 220 (1905).                                       Mathematical Society 110, 333 (2021).
 [6] T. C. Hales, Annals of Mathematics , 1065 (2005).            [25] S. Gravel and V. Elser, Physical Review E 78, 036706
 [7] K. Ball, International Mathematics Research Notices               (2008).
     1992, 217 (1992).                                            [26] https://github.com/veitelser/toruspack.
 [8] T. Bang, Proceedings of the American Mathematical So-        [27] P. Charbonneau, Y. Hu, J. Kundu, and P. K. Morse, The
     ciety 2, 990 (1951).                                              Journal of Chemical Physics 156 (2022).
 [9] S. Vance, Advances in Mathematics 227, 2144 (2011).
[10] A. Venkatesh, International Mathematics Research No-
     tices 2013, 1628 (2013).                                                      Appendix A: Software
[11] S. Torquato and F. H. Stillinger, Experimental Mathe-
     matics 15, 307 (2006).
[12] A. Scardicchio, F. Stillinger, and S. Torquato, Journal of     The RRR C-language implementation toruspack, a
     Mathematical Physics 49, 043301 (2008).                      short user’s guide, and sample outputs can be found at
[13] H. Cohn and N. Triantafillou, Mathematics of Computa-        [26]. The program is a single file and compiles with just
     tion 91, 491 (2022).                                         the standard libraries.
[14] G. A. Kabatiansky and V. I. Levenshtein, Problemy
     Peredachi Informatsii 14, 3 (1978).
[15] S. Torquato, O. Uche, and F. Stillinger, Physical Review
                                                                              Appendix B: RRR on the torus
     E 74, 061308 (2006).
[16] G. Zhang and S. Torquato, Physical Review E 88, 053312
     (2013).                                                         Though RRR is strictly defined for constraint sets in
[17] S. Torquato and F. Stillinger, Physical Review E 73,         Euclidean space, only two small modifications are re-
     031106 (2006).                                               quired to preserve the fixed-point behavior on the torus.
[18] P. Charbonneau, A. Ikeda, G. Parisi, and F. Zamponi,            In our divide-and-concur formulation of the sphere
     Physical Review Letters 107, 185702 (2011).
                                                                  packing problem, the variables live in the product space
[19] B. D. Lubachevsky, F. H. Stillinger, and E. N. Pinson,
     Journal of Statistical Physics 64, 501 (1991).
                                                                  of N (N − 1) tori Tn (w), and it is enough to address the
[20] V. Elser, Fixed Point Theory and Algorithms for Sciences     modifications in just one such factor. After replicating
     and Engineering 2021, 1 (2021).                              the sets A and B in all of Rn with the periodicity of
                                                                  Tn (w), the corresponding torus-distance between points
                                                                                                                             9

x, x′ ∈ Rn is defined by                                        where k corresponds to all the components of ũ whose
                                                                absolute values exceed w/2. In this decomposition the
               dist(x, x′ ) = k [x − x′ ]w k2 ,         (B1)    distance minimizing difference vector has the form
where k k2 is the standard norm in Euclidean space and
                                                                                 u′ = (w/2) sgn(uk ) + u′⊥ ,
[y]w = y ′ is the translate of y by an element of (wZ)n
where all components of y ′ have absolute value bounded         where the sign function sgn( ) is defined to be zero on
by w/2. We use the notation ky ′ k∞ ≤ w/2 to express this       the ⊥ components. The optimization problem for u′ has
property. Points with some components exactly equal to          been reduced to a similar optimization problem, now for
±w/2, for which [ ]w is ambiguous, do not arise in floating     the vector u′⊥ . This vector has fewer components, must
point computations.                                             also satisfy ku′⊥ k∞ ≤ w/2, and has a reduced magnitude
   The computations of PA and PB on the torus need not          bound:
be modified as long as (B1) is being minimized and the
projection outputs are interpreted as coset elements. The                  ku′⊥ k22 ≥ (2r)2 − (w/2)2 ksgn(uk )k22 .      (C1)
first modification of RRR is the definition of the reflector,
here for set A:                                                 This recursive definition of u′ terminates when all com-
                                                                ponents of the rescaled vector ũ⊥ have absolute value
              RA (x) = x + 2[PA (x) − x]w .                     below w/2. The level of recursion never exceeds four,
                                                                even in the smallest torus (w = 2r), since in that case
In words, this corresponds to “reflect in the nearest coset     the bound in (C1) collapses to zero when uk has four
element of A.”                                                  nonzero components.
   The second modification is the rule for incrementing
the current x by the difference of projections:
         x 7→ x′ = x + β[PB (RA (x)) − PA (x)]w .                           Appendix D: Concur projection

With this modification, the local analysis of RRR in Rn ,         In the concur projection, the sphere-center copies
in the presence of a set intersection or near-intersection,     xi1 , xi2 , . . . , xiN are all replaced by the same point in a
also applies in the torus. In particular, convergence to        distance minimizing way. Without the complication of
solutions is still characterized by the vanishing of the        the torus geometry, the distance minimizing point is just
Euclidean error, kx − x′ k2 .                                   the centroid. To simplify the presentation, when tak-
                                                                ing account of the torus, we may treat the n dimensions
                                                                independently. Given coordinates y1 , . . . , yN ∈ T1 (w) =
       Appendix C: Disjoint-sphere projection                   R/(wZ) (in one of the dimensions), the problem is to find
                                                                the ȳ ∈ T1 (w) that minimizes
  Let x1 = xij and x2 = xji be the sphere-center copies
that implement the disjointedness constraint between                                   N
                                                                                       X
spheres i and j, both of radius r. For packings in the                                       [ȳ − yj ]2w .              (D1)
torus Tn (w) we reduce the difference vector u = x1 − x2                               j=1
so that kuk∞ ≤ w/2. If this reduced vector satisfies
                                                                   For any ȳ, the numbers [ȳ − yj ]w are ordered in the in-
kuk2 ≥ 2r, the disjointedness constraint is satisfied and
                                                                terval Bw = [−w/2, w/2], which extends to an ordering
the projection leaves x1 and x2 unchanged.
                                                                on the circle if we identify −w/2 with w/2. Different ȳ
  Now suppose kuk2 < 2r. To satisfy the disjointed-
                                                                correspond to different ways of cutting the circle. There
ness constraint we seek a difference vector u′ satisfying
                                                                are exactly N places to cut the circle, each case corre-
ku′ k∞ ≤ w/2, ku′ k2 ≥ 2r and which minimizes ku′ −uk2 .
                                                                sponding to a different choice of j such that [ȳ − yj ]w
The last two conditions imply the new centers
                                                                is the smallest element in Bw . The ordering on the cir-
                   x′1 = x1 + (u′ − u)/2                        cle determines the ordering of all the others, now in Bw ,
                   x′2 = x2 − (u′ − u)/2                        and the distance minimizing ȳ is simply the centroid of
                                                                the correspondingly ordered yj . The N centroids ȳ de-
satisfy the disjointedness constraint in a distance min-        termined by the N places to cut the circle will have N
imizing way. If we did not have the first constraint,           squared-distances (D1), and the projection selects among
ku′ k∞ ≤ w/2, then u′ would just be a rescaling of u:           these the smallest.
                                                                   Instead of computing N centroids and their associated
                                2r                              squared-distances, the projection can be computed more
                        ũ =        u
                               kuk2                             efficiently by calculating the changes in the squared dis-
To describe what we must do when at least one compo-            tance between successive cuts of the circle. The work in
nent of ũ exceeds w/2 in absolute value, first express u       keeping track of the smallest squared-distance after all
as the orthogonal decomposition                                 N changes have been computed scales as O(N ), no dif-
                                                                ferent from the centroid computation without the torus
                       u = uk + u⊥ ,                            complication.
                                                                                                                                               10

            Appendix E: Metric auto-tuning                                 Appendix F: Torus-restricted sphere volume


   A diagonal modification of the isotropic Euclidean                    The volume ãn of the set Sen (1) defined in (2) can be
metric preserves the local convergence of the RRR al-                  expressed as
gorithm. In the sphere packing problem, first without                                n Z ∞                    
                                                                                     Y                                      
the torus complication, a natural diagonal modification                     ãn =                    dxi θ(xi ) 2δ kxk22 − 1 ,            (F1)
is                                                                                   i=1       −∞

                     X                                            
  dist2 (x, x′ ) =           gij kxij − x′ij k22 + kxji − x′ji k22 ,   where δ( ) is the Dirac delta distribution and
                     (i,j)                                                                     
                                                                                                 1, |x| ≤ 1/2
                                                                                        θ(x) =
                                                                                                 0, otherwise.
where the sum is over all pairs of sphere centers and the
gij are positive parameters. Because a rescaling of the                Rewriting (F1) in terms of θ̄ = 1 − θ, we notice that
variables (and their constraints) restores the Euclidean               terms involving products of four or more θ̄ are zero be-
metric, local convergence (of the rescaled variables) still            cause kxk22 > 1 when four of the xi have absolute value
holds. We will keep the variables (and constraints) un-                greater than 1/2. The surviving terms can be indexed by
rescaled and adjust the metric parameters gij by a heuris-             ℓ, 0 ≤ ℓ ≤ 3, and have the same value that only depends
tic based on constraint discrepancies. The adjustment is               on ℓ (in addition to n) :
performed automatically, and adiabatically, so as not to
upset the local convergence.                                                                       3
                                                                                                   X             
                                                                                                                ℓn
   The local constraint discrepancy is defined as                                          ãn =           (−1)     d(n, ℓ) .
                                                                                                                 ℓ
                                                                                                     ℓ=0

            ǫ2ij = kxA     B 2       A     B 2
                     ij − xij k2 + kxji − xji k2 ,                     The integral in

where superscripts A and B denote the A and B pro-                                   ℓ Z ∞
                                                                                     Y                                
jections in the current RRR update. The sphere-center                    d(n, ℓ) =                    dyj (1 − θ(yj ))
                                                                                                −∞
copies xij and xji for which ǫ2ij is above average are the                           j=0
                                                                                     Z ∞
most troublesome, and deserve an above-average metric                                                                                 
weight. We implement this heuristic with the following                          ×          (an−ℓ rn−ℓ−1 dr) 2δ kyk22 + r2 − 1             (F2)
                                                                                      0
metric-weight update rule, in each RRR iteration,
                                                                       over the n − ℓ variables that only appear via their norm
                 ′
                                                                      r in the integrand has been rewritten in terms of the
                gij = gij + γ         ǫ2ij /hǫ2 i − gij
                                                                       volume an−ℓ of the sphere in that many dimensions. The
                                                                       final step of the derivation of formula (3) is to express
where h i denotes the average of ǫ2ij over (i, j) and γ > 0            (F2) as a sum over the number of factors of θ, indexed
is a small parameter. The metric parameters are initial-               by k, all of which are equal:
ized at gij = 1 and over time the most troublesome con-
straints have their weights increased. As the packing is                                              3
                                                                                                      X           
                                                                                                                  ℓ k
refined, the metric parameters approach an equilibrium                                d(n, ℓ) =             (−1)     e(n, k) .
                                                                                                                  k
distribution gij ≈ ǫ2ij /hǫ2 i over a characteristic time of                                          k=0
1/γ iterations.
                                                                       Expressing the integral in e(n, k) as earlier for d(n, ℓ),
   The metric parameters have no effect on the projec-
tion to the A constraint, since the pairs of sphere centers                          k Z ∞                     
                                                                                     Y
involved share the same weight. However, the weights ap-                 e(n, k) =                    dyj θ(yj )
pear in an intuitive way in the B constraint. The expres-                            j=0        −∞
sion (D1) being minimized for concurrence of the copies                                   Z ∞
                                                                                                                                  
is replaced by                                                                       ×          (an−k rn−k−1 dr) 2δ kyk22 + r2 − 1 ,
                                                                                           0
                         N
                         X                                             we obtain
                                gij [ȳ − yj ]2w ,
                         j=1                                                                   k Z ∞
                                                                                               Y                          
                                                                                                                                       n−k−2
                                                                         e(n, k) = an−k                         dyj θ(yj ) (1 − kyk22 ) 2
                                                                                               j=0         −∞
which has the effect of weighting copy yj = xij of sphere
center i with weight gij in the centroid computations.                           = an−k c(n, k) .
The copy in the most troublesome constraint thereby gets
a stronger voice in deciding the sphere’s position.
