                                                                          Replica Exchange Monte Carlo applied to Hard Spheres
                                                                                                          Gerardo Odriozola
                                                                                 Programa de Ingenierı́a Molecular, Instituto Mexicano del Petróleo,
                                                                                        Lázaro Cárdenas 152, 07730 México, D. F., México
                                                                                                       (Dated: June 12, 2018)
                                                                     In this work a replica exchange Monte Carlo scheme which considers an extended isobaric-
                                                                  isothermal ensemble with respect to pressure is applied to study hard spheres (HS). The idea behind
arXiv:1010.2923v1 [cond-mat.stat-mech] 14 Oct 2010




                                                                  the proposal is expanding volume instead of increasing temperature to let crowded systems char-
                                                                  acterized by dominant repulsive interactions to unblock, and so, to produce sampling from disjoint
                                                                  configurations. The method produces, in a single parallel run, the complete HS equation of state.
                                                                  Thus, the first order fluid-solid transition is captured. The obtained results well agree with previous
                                                                  calculations. This approach seems particularly useful to treat purely entropy-driven systems such
                                                                  as hard body and non-additive hard mixtures, where temperature plays a trivial role.


                                                                     I.   INTRODUCTION                                 sitions have problems at very high densities[5]. There-
                                                                                                                       fore, the freezing and melting points are at least difficult
                                                        The replica exchange Monte Carlo (REMC) method                 to determine [14]. Indeed, for the HS model, simula-
                                                     [1, 2], also called parallel tempering [3], was derived to        tions have recently produced an accurate determination
                                                     achieve good sampling of systems that present a free en-          of the freezing and melting point theoretically reported
                                                     ergy landscape with many local minima [4, 5]. It consists         in the sixties [14, 15]. That is despite the intense study
                                                     on simulating several replicas of the same system at dif-         of HS through the past decades, and the fact that the HS
                                                     ferent thermodynamic states, and allowing for replica ex-         model was one of the first systems ever studied by com-
                                                     changes (swap moves). Thus, it is possible to implement           puter simulations [16–18]. Additionally, the HS model
                                                     an ergodic walk through free energy barriers connecting           shows a high density metastable branch ending at the
                                                     disjoint configuration subspaces by defining a set of close       random close package density [19], which adds difficulty
                                                     enough thermodynamic states. Although it has been de-             for sampling from equilibrium.
                                                     veloped at the end of the last century [1, 2], its accep-            The aim of this study is to show that the REMC can be
                                                     tance is already high due to its clearness, simplicity, and       successfully applied to study hard body systems. Hence,
                                                     its wide applicability. Proof of that is its employment           the REMC is used by performing a NPT ensemble exten-
                                                     to find zeolite structures [6], to study different conforma-      sion on pressure and applied to HS. The paper is struc-
                                                     tions of proteins[7], and to access phase equilibrium of          tured as follows. Sec. I is this brief introduction. Sec. II
                                                     many single and multicomponent systems [8–10].                    describes the employed algorithm. Results are given in
                                                        Most frequently, the REMC technique is employed to             Sec. III. Finally, in Sec. IV conclusions are drawn.
                                                     sample an extended canonical ensemble in temperature.
                                                     Thus, those replicas having larger temperatures are ca-
                                                     pable of escaping from local free energy minima, where                          II.   NUMERICAL METHOD
                                                     the pair potential attraction of the constituting parti-
                                                     cles plays a key role. When the free energy minima are               As mentioned, in the parallel tempering scheme nr
                                                     mainly dictated by the entropic term, i. e., by the ex-           identical replicas are considered, each following a typi-
                                                     cluded volume repulsive interactions [11–13], enlarging           cal canonical simulation. However, a different temper-
                                                     the temperature has a small effect. In other words, the           ature is set for each one of them. Thus, an extended
                                                     benefits of the method become restricted. This is espe-           ensemble can be Qndefined   so that its partition function
                                                     cially true when dealing with hard body systems (purely           is Qextended = i=1  r
                                                                                                                                             QN V T i , being QN V T i the partition
                                                     entropy-driven systems) such as hard spheres (HS), rods,          function of ensemble i at temperature Ti , number of par-
                                                     plates, polymers, and non-additive hard mixtures, since           ticles N , and volume V . The existence of this extended
                                                     they constitute limiting cases where the pair interactions        ensemble justifies the introduction of swap trial moves
                                                     are repulsive only and the temperature plays a trivial            between any two ensembles (each ensemble is sampled by
                                                     (null) role. Thus, it is not very surprising that the REMC        only one replica at a time), whenever the detail balance
                                                     technique has not been applied yet to this kind of sys-           condition is satisfied. If all (i, Ti )(j, Tj ) → (j, Ti )(i, Tj )
                                                     tems. To do this, an alternative would be performing              swap trials have the same a priori probability of being
                                                     the ensemble extension in pressure instead of tempera-            performed, the swap acceptance probability becomes
                                                     ture, to provide the particles more freedom to rearrange
                                                     as the volume expands. This idea is tested in this work                      Pacc = min(1, exp[(βj − βi )(Ui − Uj )])           (1)
                                                     for HS.
                                                        It is well known that fluid-solid transitions represent a      where βi = 1/(kB Ti ) is the reciprocal temperature of
                                                     challenge for computational science [14, 15]. Most tech-          replica i, kB is the Boltzmann’s constant, and Ui is the
                                                     niques which properly work for accessing liquid-gas tran-         energy of replica i. Hence, by introducing these swap
                                                                                                                          2

trials, a particular replica seals through many tempera-        are considered. These boxes are filled by randomly plac-
tures allowing it to overcome free-energy barriers. Ad-         ing N hard spheres of diameter σ. The initial density,
ditionally, sampling on particular ensembles is not dis-        ρ = N πσ 3 /(6L), is set to 0.30 for all replicas. A geomet-
turbed but enriched by the different contributions of the       rically increasing pressure, βP , is set from approximately
nr replicas.                                                    2 to 100 σ −3 , and arbitrarily assigned to the replicas.
   For studying systems where excluded volume interac-          Where the fluid-solid transition is expected, intermedi-
tions dominate, it may be convenient to allow the replicas      ate pressures are added (the total number of replicas
to expand for destroying any local order. Additionally,         equals the number of different pressures). An optimal
in the case of a HS system (or any other purely entropy-        allocation of replicas should lead to a constant swap ac-
driven model) an extended ensemble in temperature is            ceptance probability for all pair of adjacent ensembles
pointless, since this variable does not affect the system       [21]. Two experiments were done, one with N = 32 and
structure. For that purpose,
                           Qnr the extended ensemble is         the other with N = 108. The simulation starts by fol-
defined as Qextended = i=1      QN T P i , being QN T P i the   lowing the trial moves above described (see the appendix
partition function of the isobaric-isothermal ensemble of       for details).
system i, at pressure Pi , fixed temperature T , and num-          Sampling consists on measuring densities, radial distri-
ber of particles N (note that the extension is in pres-         bution functions, average number of neighbors, and the
sure; an isobaric-isotermal extension in temperature ap-        order parameter Q6 , as a function of the pressure. The
plied to a Lennard Jones system is given by Okabe et.           average number of neighbors, Nn , is computed account-
al. [20]). This extended ensemble can be sampled by             ing for all pairs having a center-center distance smaller
performing standard N T P simulations on each replica,          than 1.2σ (the vectors joining the centers of these pairs
which implies typical particle displacement trials and vol-     are named bonds). The order parameter Q6 is defined as
ume change trials. Notwithstanding, the sampling can            [19, 22]
be significantly improved by introducing swap trials be-                                                       !1/2
tween neighboring ensembles. Again, the only restriction                            m=6
                                                                                 4π X
is that the detail balance condition must prevail to guar-               Q6 =            | < Y6m (θ, φ) > |2            (3)
                                                                                 13 m=−6
anty the correct sampling. One way of achieving this is
by setting equal all a priori probabilities of choosing the
                                                                where < Y6m (θ, φ) > is the average over all bonds and
different adjacent pairs of replicas, and accounting for
                                                                configurations of the spherical harmonics of the orien-
the following acceptance probability
                                                                tation angles θ and φ (these are the polar angles of the
         Pacc = min(1, exp[β(Pi − Pj )(Vi − Vj )])       (2)    bonds measured with respect to any fixed coordinate sys-
                                                                tem, since Q6 is invariant). Q6 should go to zero for a
where Vi − Vj is the volume difference between replicas i       completely random
                                                                            p       system√of a large number of points,
and j. It should be noted that the ensemble extension in        following 1/ N Nn /2 ± 1/ 13N Nn [19].
pressure leads to a simple acceptance rule where energy
terms vanish.
   For (Pi − Pj )(Vi − Vj ) ≥ 0, Pacc = 1 and so, the ac-                           III.   RESULTS
ceptance rule tends to order the replicas by volume size
(lower volumes at higher pressures). For (Pi − Pj )(Vi −          Figure 1 a) shows the probability density functions,
Vj ) < 0, Pacc depends on the absolute value of the pres-       PDFs, to find a replica at a given density for all pressures
sure differences of the adjacent ensembles, β|Pi − Pj |. A      and for N = 32. The 70 PDFs correspond to the different
decrease of β|Pi − Pj | leads to a larger acceptance prob-      assigned pressures. In general, the PDFs are bell-shaped
ability. Consequently, adjacent pressures should be close       and centered on a maximum which location depends on
enough to provide large exchange acceptance rates be-           the assigned pressure. The leftmost curve corresponds
tween neighboring ensembles. This is particularly impor-        to the lowest pressure (2.16 β −1 σ −3 ) and the rightmost
tant where a phase transition takes place (characterized        to the highest one (100 β −1 σ −3 ). As pressure increases,
by large |Vi − Vj |), which generally leads to a bottleneck     the curves narrow and shift to the right producing larger
of the swap acceptance rate. Additionally, the swap ac-         densities (the narrowing is very pronounced for high pres-
ceptance rate also depends on the system size. Larger           sures). The exception occurs for densities close to 0.5,
system sizes produce narrower distribution of densities         where the PDFs split yielding bimodal distributions. At
(volumes) for a given pressure, providing smaller over-         ρ ≃ 0.5, the replicas produce few configurations, and
lap regions between adjacent ensembles. Hence, a larger         the bimodals yield a local peak below 0.49 and another
system size leads to a decrease of the swap acceptance          above 0.51. Thus, a jump on density from ρf = 0.474 to
probability. Finally, in order to take a good advantage         ρs = 0.520 is produced for βP = (9.95 ± 0.10)σ −3, point-
of the method, the replica at the lowest pressure must          ing out the well known HS fluid-solid transition. The
assure large jumps in configuration space, so that the          inset of figure 1 a) zooms in the density region around
higher pressure ensembles can be sampled from disjoin           0.5, where the PDFs are much clearly seen. There it is
configurations.                                                 shown the pressures that correspond to the PDFs which
   In this work, nr = 70 cubic boxes of initial side L          are closer to the transition.
                                                                                                                                                3

   0.15      0.03                                                                                  12

                            βP=9.76 σ
                                         −3                                  a)                                               ref. [14]
             0.02                                                                                                             ref. [ 4]
                                  βP=10.01 σ
           PDFs                                −3
                                                                                                                              ref. [15]
   0.10
                                                                                                   11                         This work
  PDFs




             0.01




                                                                                         βP (σ )
                                                                                          -3
   0.05      0.00
                0.46       0.48       0.50      ρ 0.52          0.54
                                                                                                   10


   0.00
                                                                                                        0.00   0.01    0.02      0.03
              0.06
                     0.3           0.4          ρ 0.5                  0.6    0.7
                                                                                                                      1/N
     0.2
                                         βP=10.74 σ
                                                      −3                     b)
              0.04
                                          βP=10.98 σ
                                                           −3                       FIG. 2. βP as a function of the inverse of the system size,
           PDFs
  PDFs




                                                                                    1/N . Solid symbols correspond to this work results. The
                                         βP=11.23 σ
                                                       −3
              0.02                                                                  solid symbol at 1/N = 0 is an extrapolation of the data and
                                                                                    the solid lines are drawn to estimate the corresponding error.
     0.1
              0.00                                                                  Open symbols are values reported by different authors.
                 0.46      0.48        0.50 ρ       0.52        0.54


                                                                                    be seen, the obtained agreement is good, suggesting that
     0.0
                                                                                    the RECM method works properly for capturing the HS
                     0.3           0.4
                                                ρ 0.5                  0.6    0.7
                                                                                    fluid-solid transition.
                                                                                       The topmost plot of figure 3 is built by plotting the
FIG. 1. Probability density functions, PDFs, to find a replica                      pressure as a function of the most frequent density for
at a given density, ρ. The 70 different curves correspond to the                    N = 108. It is also shown as a red line a Padé approxi-
different assigned pressures. Fig. a) corresponds to N =32                          mation to data obtained from the HS fluid state [23], and
and Fig. b) to N =108. Both insets zoom in the correspond-                          as a blue line a fit to the HS face cubic centered (FCC)
ing data.                                                                           solid state [24], both data series obtained by means of
                                                                                    simulations. As an inset, it is shown a zoom in of the
                                                                                    same data for the coexistence, where there were added
   The PDFs obtained for N = 108 are shown in figure 1                              the data obtained for N = 32. Both curves here reported,
b). As expected, similar trends are seen. That is, PDFs                             for the fluid and solid states, well agree with the equa-
are bell-shaped, they narrow and shift toward larger den-                           tion of state given by Speedy. This confirms the good
sities for increasing pressure, and they turn bimodal for                           behavior of the REMC ensemble extension on pressure.
densities close to 0.5. Nevertheless, PDFs are higher (ap-                          Nevertheless, there is a slight deviation from the FCC
proximately two times higher) and (consequently) nar-                               curve of Speedy close to the transition. This may signal
rower than for N = 32. Also the bimodal distributions                               the presence of hexagonal close-packed (HCP) arrange-
become sharper producing interpeak regions rarely vis-                              ments and even hybrid FCC-HCP structures.
ited by the replicas. In fact, for ρ ≃ 0.508 the PDFs                                  The middle and bottommost plots of figure 3 show the
are practically zero. In other words, the HS fluid-solid                            order parameter, Q6 , and the number of first neighbors,
transition turns more evident by increasing the system                              Nn , as a function of ρ, respectively. The middle plot also
size. As in figure 1 a), the inset of figure 1 b) zooms in                          shows as bullets the value of Q6 for completely space-
the corresponding PDFs. From there it can be estimated                              uncorrelated particles. As expected, Q6 is small for the
the transition occurring at βP = (10.99 ± 0.10)σ −3 with                            fluid region, pointing out the practical absence of angular
ρf = 0.487 and ρs = 0.538. Thus, the transition occurs                              order. However, it is always somewhat larger than the
at a higher pressure and shifts to larger densities for in-                         value of Q6 for a random system. The difference between
creasing the system size. The gap between the fluid and                             these two values diminishes for decreasing ρ. On the
solid densities also enlarges.                                                      other hand, Q6 reaches 0.5732 for βP = 100σ −3 , which
   The data obtained for small N values can be ex-                                  is slightly lower than the Q6 value of the FCC arrange-
trapolated to estimate the HS bulk coexistence pres-                                ment, 0.5745, and well above the corresponding value of
sure, fluid density, and solid density. These are βPtr =                            the HCP structure, Q6 = 0.4848. This signals that only
(11.43 ± 0.17)σ −3 , ρf =0.492 ± 0.004, and ρs =0.545 ±                             replicas approaching the FCC lattice are allowed for the
0.004, respectively. These values are in good agreement                             highest applied pressures. This is not surprising since
with previous calculations [5, 14, 15]. Figure 2 shows the                          108 identical spherical particles can be perfectly packed
extrapolation for the coexistence pressure, and a com-                              on a cubic box on a FCC lattice, but cannot on a HCP
parison with data reported by different authors. As can                             lattice. Thus, the system is being forced to promote FCC
                                                                                                                                                                     4

      100            15                                                    e)                        a)           b)                   c)             d)             e)

       80
                                                                                        10
 βP (σ )



       60            10
 -3




                                                                      d)
               βP (σ )
               -3




                                                                                      RDFs
       40
                         5                                                                   5
       20                      0.4     ρ   0.5

                                                                 c)
        0
                         a)                b)
      0.6
                                                                                             0
                                                                                                 1   2    3 1     2    3 1         2        3 1   2        3 1   2        3
      0.4
                                                                                                                             r/σ
  Q6




      0.2
                                                                                      FIG. 4. Radial distribution functions (black lines) and their
      0.0                                                                             integrals (red lines) for cases a), b), c), d), and e), as shown in
       12                                                                             figure 3, from left to right. The insets are the corresponding
                                                                                      snapshots. Integrals (red lines) are scaled by a factor 1/10.
           9
   Nn




           6
                                                                                      case a)), and a well defined second shell of neighbors.
           3                                                                          This case corresponds to a liquid close to the coexistence.
                                                                                      Slightly above the coexistence, the RDF looks like case
                         0.3         0.4         0.5
                                                       ρ   0.6                  0.7
                                                                                      c). Here a small peak appears at r/σ ≃ 1.5, whereas the
                                                                                      valley in-between this peak and the contact one deepens.
FIG. 3. Topmost; HS equation of state (pressure as a func-                            Other peaks also form at larger distances. For density
tion of the corresponding most frequent density) for N =108                           values close to 0.68, case d), the RDF develops the full
( symbols). The red line corresponds to the HS fluid equa-                            character of a crystal. That is, peaks are very high and
tion of state of Speedy [23] and the blue one to the HS face                          narrow, and valleys turn practically zero. The integral
cubic centered equation of state of the same author [24]. In-                         (red line) of this case highlights this fact, since it shows
set; zoom in of the same plot, where  symbols were added
                                                                                      a step-like behavior. The first step reaches 12, point-
corresponding to N =32. Middle plot; Order parameter, Q6 ,
as a function of ρ ( symbols), and the corresponding   value
                                                                                      ing out the first shell coordination number (integral   √ of
                                            p
for a completely random system of points 1/ N Nn /2 (small                            the peak at r/σ = 1),√the second yields 18 (r/σ = 2),
bullets). Bottommost; Number of first neighbors, Nn , as a                            the third 42 (r/σ = 3), and the fourth 54 (r/σ = 2),
function of ρ.                                                                        what corresponds to the FCC structure. Nonetheless,
                                                                                      a small p shoulder appears at the left of the fourth peak
                                                                                      (r/σ = 11/3 ≃ 1.91), suggesting the existence of few
over HCP at high pressures. For lower but still over the                              configurations having a HCP structure. For larger den-
coexistence pressures, Q6 is close to 0.5, suggesting that                            sities, case e), this shoulder disappears and a practically
both lattices and their hybrids contribute to the average.                            pure FCC RDF is observed.
It should be noted that Q6 sharply increases at the fluid-
solid transition. Thus, it can be employed to detect any
trace of local angular order. This was shown to be much                                                     IV.       CONCLUSIONS
more reliable than the radial distribution function peak
that develops close to 1.5σ [19]. Finally, Nn monotoni-                                  This work shows that a replica exchange Monte Carlo
cally increases with ρ. It also shows a sharp increase at                             scheme can be successfully applied to study hard spheres
the coexistence, although less pronounced than for Q6 .                               at high densities. For that purpose, an extension of
At large densities Nn reaches 12, which is the largest                                the isobaric-isothermal ensemble with respect to pres-
possible HS coordination number, as it is well known.                                 sure is used. The algorithm employs standard particle
   The radial distribution functions (RDFs) and their cor-                            trial displacements and volume changes together with
responding integrals for cases a), b), c), d), and e) pointed                         replica exchanges (swap moves). These easy to imple-
out in figure 3 are plotted in figure 4. Cases a) and b)                              ment trials are shown to be enough for capturing the
correspond to the fluid phase, and the other three cor-                               fluid-solid transition of hard spheres and the solid equi-
respond to the solid phase. Case a) shows the typical                                 librium branch for small systems. The obtained results
low density liquid structure, where a relatively small con-                           well agree with previous calculations. The principal idea
tact value is developed and the second shell of neighbors                             behind this scheme is to increase the particles mobili-
is poorly seen. As the density increases, case b), the                                ties by decreasing the pressure (expanding the volume),
RDF shows a larger contact value (two times larger than                               so that systems characterized by large excluded volume
                                                                                                                                                                       5

contributions are able to visit disjoint configurations of
                                                                                                                        100             equilibrium
configurational space. This approach seems particularly                                                                                            10
                                                                                                                                        trials ~ 10
useful to deal with purely entropy-driven systems such as                                                       N=32
                                                                                                                N=108                   trials ~ 10
                                                                                                                                                   11




                                                                Swap acceptance rate
hard body and non-additive hard mixtures, where tem-                                   0.8
                                                                                                                                        trials ~ 10
                                                                                                                                                   12


perature plays a trivial role.

                                                                                             a)                              50    b)
                                                                                       0.6




                                                                                                                        βP(σ )
    V.    APPENDIX- SIMULATION DETAILS                                                                                                                          ρfcc




                                                                                                                        -3
   Once the nr = 70 boxes are filled with the N spheres                                                                                                 ρrcp
and are assigned the corresponding different pressures,                                0.4                                    0
the algorithm starts performing the trials. As mentioned,
they are: particle displacements, volume changes, and
                                                                                                  10       -3
                                                                                                       βP(σ )
                                                                                                                  100             0.5          0.6
                                                                                                                                                     ρ         0.7

swap moves. The probability for selecting a particle dis-
placement trial (in any of the nr boxes), Pd , is fixed        FIG. 5. a) Swap acceptance rate as a function of the ensem-
to Pd = nr N/(nr (N + 1) + w(nr − 1)). The probabil-           ble pressure. b) Evolution of the densities with the number
ities for selecting a volume change trial, Pv , and a swap     of trials during the initializing procedure (N = 108). As a
trial, Ps , are Pv = nr /(nr (N + 1) + w(nr − 1)) and          reference, the data obtained from equilibrium are added as
Ps = w(nr − 1)/(nr (N + 1) + w(nr − 1)). Here, w is            a solid line. The dotted lines show the random close pack-
a weight factor fixed to 1/50. Additionally, the proba-        ing density as obtained from the square symbols and the face
bility of performing a particle displacement trial and a       cubic centered density.
volume change trial in a replica enlarges as it is closer
to the fluid-solid transition pressure. These probabilities
are 10 times larger for the central replica than for those     (initializing procedure). During this process, the max-
having the highest and the lowest pressures. All parti-        imum displacements of particles and maximum volume
cles of a given replica have the same a priori probability     changes for each pressure are tuned to yield acceptance
of being selected to perform a displacement trial. The         rates close to 0.4. Thus, particle maximum displacements
same is true for selecting a pair of adjacent replicas to      and maximum volume changes of ensembles having high
attempt a swap move (there are nr − 1 pairs). Thus,            pressures turn smaller than those associated to ensembles
a random number homogeneously distributed in [0,1] is          having low pressures. Once this is done, all maximum
generated in order to determine the type of trial to be        displacements (one for each pressure) and maximum vol-
performed. In case of selecting a particle displacement,       ume changes (also one for each pressure) become fixed.
the algorithm provides the replica and the particle for        1.0×1013 trials are then employed to yield the data shown
applying the trial. In case of a volume change trial, it       in the body of the article (equilibrium sampling).
identifies the replica; and in case of a swap trial, the al-      The acceptance rates obtained for the swap trials are
gorithm gives the adjacent replicas to apply it. Next,         shown in Fig. 5 a) as a function of the pressure, βP .
another random number is generated to produce a sec-           As expected, the acceptance rates for the smaller system
ond trial. If these two trials are independent the one         (N = 32) are, in general, larger than the ones obtained
another (for instance, they are particle trials on different   for the larger system (N = 108). This is a consequence of
replicas) the algorithm generates a third trial (note that     the larger overlaps of the distributions. In both cases the
these trials are not being applied yet). This procedure        values are above the recommended acceptance rate of 0.2
is repeated until the last trial cannot be performed inde-     [21]. For βP > βPtr , the acceptance rate is practically
pendently of the others (for instance, a particle displace-    constant. On the contrary, for βP < βPtr , the accep-
ment trial on a replica in which a volume change trial         tance rate increases with decreasing βP . This means that
must be previously performed). This way, the algorithm         for the fluid region, βP should be reduced more than geo-
have randomly selected a given number of independent           metrically for optimization purposes. For 10 . βP . 12,
trials to be applied on the replicas. Immediately after,       the acceptance rate increases. This is due to the fact
the algorithm parallelizes (in two threads, since a dual       that smaller pressure differences are set between the ad-
core desktop is used), and the trials are done. The last       jacent ensembles to compensate the natural decrease of
generated trial (which was not yet performed) becomes          the acceptance rate at the fluid-solid transition. Note
now the first trial to be applied on the following series of   that more than the necessary replicas are added in or-
trials. This procedure is followed to strictly preserve the    der to decrease the error of the coexistence pressure (the
detail balance condition (to build a symmetric transition      natural decrease of the acceptance rate is overcompen-
matrix) while performing a parallelization. Verlet lists       sated). In addition, this study is focussed on yielding a
are employed for saving CPU time (note that the saving         detailed sampling of a large βP range. To acquire equilib-
can be quite large since replicas at high pressures rarely     rium data from a high pressure system only, many fewer
update their lists).                                           replicas would be required (the optimal swap acceptance
   Sampling is not performed for the first 3.0 × 1012 trials   rate is close to 20% when temperature is employed as the
                                                                                                                         6

thermodynamic variable of ensemble extension [21]).           βP/ρ2 ∝ (ρrcp − ρ)−1 [19]. This is larger than the re-
   Figure 5 b) shows the evolution of the pressure versus     ported value of ρrcp = 0.644 ± 0.005 [19], suggesting that
density plot with the number of performed trials during       some degree of crystallization is already taking place on
the initializing procedure (N = 108). For ∼ 1010 tri-         the replicas at high pressure. This is in fact confirmed by
als, the sampling yields a curve at βP > βPtr which           the Q6 analysis (not shown). As the initializing process
may correspond to the random close packing (RCP)              advances, the degree of crystallization augments and the
metastable branch. There are also 5 replicas which            high pressure curve shifts approaching the equilibrium
reached the equilibrium state (since they crystalized,        branch (Q6 also enlarges). For ∼ 1012 trials, the curve
they were pushed towards the highest pressure region).        practically yields the equilibrium branch. From here on,
Another one, producing the point laying on the dotted         only those replicas having a large degree of crystallinity
line, may correspond to a partially crystalized struc-        are able to access the high pressure region. At this point,
ture. Assuming this well defined curve corresponds to         the initializing procedure ends and the sampling from
the RCP branch, ρrcp = 0.680 ± 0.005 is obtained from         equilibrium process starts.




 [1] A. P. Lyubartsev, A. A. Martsinovski, S. V. Shevkunov,   [13] F. Jiménez-Ángeles, Y. Duda, G. Odriozola, and
     and P. N. Vorontsov-Velyaminov, J. Chem. Phys. 96,            M. Lozada-Cassou, J. Chem. Phys. 129, 111101 (2008).
     1776 (1991).                                             [14] N. B. Wilding and A. D. Bruce, Phys. Rev. Lett. 79,
 [2] E. Marinari and G. Parisi, Europhys. Lett. 19, 451            3002 (1997).
     (1992).                                                  [15] E. G. Noya, C. Vega, and E. de Miguel, J. Chem. Phys.
 [3] Q. L. Yan and J. J. de Pablo, J. Chem. Phys. 111, 9509        128, 154507 (2008).
     (1992).                                                  [16] M. N. Rosenbluth and A. W. Rosenbluth, J. Chem. Phys.
 [4] E. Bittner, A. Nußbaumer, and W. Janke, Phys. Rev.            22, 881 (1954).
     Lett. 101, 130603 (2008).                                [17] W. W. Wood and J. D. Jacobson, J. Chem. Phys. 27,
 [5] D. Frenkel and B. Smit, Understanding molecular simu-         1207 (1957).
     lation (Academic, New York, 1996).                       [18] B. J. Alder and T. E. Wainwright, J. Chem. Phys. 27,
 [6] M. Falcioni and M. W. Deem, J. Chem. Phys. 110, 1754          1208 (1957).
     (1999).                                                  [19] M. D. Rintoul and S. Torquato, J. Chem. Phys. 105, 9258
 [7] J. Hernández-Rojas and J. M. G. Llorente, Phys. Rev.         (1996).
     Lett. 100, 258104 (2008).                                [20] T. Okabe, M. Kawata, Y. Okamoto, and M. Masuhiro,
 [8] C. E. Fiore, Phys. Rev. E. 78, 041109 (2008).                 Colloid Polym. Sci. 335, 435 (2001).
 [9] A. Imperio and L. Reatto, J. Chem. Phys. 124, 164712     [21] N. Rathore, M. Chopra, and J. J. de Pablo, J. Chem.
     (2006).                                                       Phys. 122, 024111 (2005).
[10] A. Arnold and C. Holm, Eur. Phys. J. E 27, 21 (2008).    [22] P. J. Seinhardt, D. R. Nelson, and M. Ronchetti, Phys.
[11] A. Fortini and M. Dijkstra, J. Phys.: Condens. Matter         Rev. B. 28, 784 (1996).
     18, L371 (2006).                                         [23] R. J. Speedy, J. Phys.: Condens. Matter 9, 8591 (1997).
[12] G. Odriozola, F. Jiménez-Ángeles, and M. Lozada-       [24] R. J. Speedy, J. Phys.: Condens. Matter 10, 4387 (1998).
     Cassou, J. Chem. Phys. 129, 111101 (2008).
