                                                               Models and algorithms for the next generation of glass transition studies
                                                                                   Andrea Ninarello, Ludovic Berthier, and Daniele Coslovich
                                                                    Laboratoire Charles Coulomb, UMR 5221 CNRS-Université de Montpellier, Montpellier, France
                                                                                                     (Dated: May 1, 2017)
                                                                      Successful computer studies of glass-forming materials need to overcome both the natural tendency
                                                                   to structural ordering and the dramatic increase of relaxation times at low temperatures. We present
                                                                   a comprehensive analysis of eleven glass-forming models to demonstrate that both challenges can be
arXiv:1704.08864v1 [cond-mat.stat-mech] 28 Apr 2017




                                                                   efficiently tackled using carefully designed models of size polydisperse supercooled liquids together
                                                                   with an efficient Monte Carlo algorithm where translational particle displacements are complemented
                                                                   by swaps of particle pairs. We study a broad range of size polydispersities, using both discrete and
                                                                   continuous mixtures, and we systematically investigate the role of particle softness, attractivity and
                                                                   non-additivity of the interactions. Each system is characterized by its robustness against structural
                                                                   ordering and by the efficiency of the swap Monte Carlo algorithm. We show that the combined
                                                                   optimisation of the potential’s softness, polydispersity and non-additivity leads to novel computer
                                                                   models with excellent glass-forming ability. For such models, we achieve over ten orders of magnitude
                                                                   gain in the equilibration timescale using the swap Monte Carlo algorithm, thus paving the way to
                                                                   computational studies of static and thermodynamic properties under experimental conditions. In
                                                                   addition, we provide microscopic insights into the performance of the swap algorithm which should
                                                                   help optimizing models and algorithms even further.


                                                                       I.   INTRODUCTION                                computing arena suggests that progress could be made at
                                                                                                                        a faster pace if novel technologies become available. Ex-
                                                                                                                        ploiting them in the context of molecular simulations [13–
                                                         Computer simulations play an increasingly important
                                                                                                                        17] requires nonetheless a substantial investment in code
                                                      role in elucidating the nature of the glass transition be-
                                                                                                                        development and low-level optimization.
                                                      cause they allow particle-level resolution of any relevant
                                                      static or dynamic observable [1]. While a similar spa-               The above summary suggests that it is desirable to de-
                                                      tial resolution can now be achieved in experiments per-           velop alternative strategies, which do not simply rely on
                                                      formed with colloids [2], less direct microscopic informa-        the brute force increase of computing power. A possible
                                                      tion is available from experimental studies of molecular          path is to take advantage of the flexibility offered by sim-
                                                      liquids [3]. Regarding timescales, however, colloidal ex-         ulations and implement algorithms that simulate equi-
                                                      periments and computer simulations cover at best the              librium material properties more efficiently [18]. Several
                                                      first 4-5 decades of the dynamic slowing down of systems          such strategies have already been explored. A first line
                                                      approaching a glass transition [4], whereas 12-13 orders of       of research concerns the development of collective par-
                                                      magnitude of glassy slowdown can be analyzed in molec-            ticle displacements to improve sampling efficiency [19–
                                                      ular liquids [5]. Therefore, the exquisite level of detail        21]. This approach follows the method employed to study
                                                      gained from simulations in the description of the onset of        phase transitions in spin systems [22, 23]. For instance,
                                                      slow dynamics concerns a dynamical regime which is sep-           the event-chain Monte Carlo algorithm has proved use-
                                                      arated from experiments on molecular glasses by about             ful in the study of two-dimensional melting [21], but its
                                                      eight orders of magnitude. The dichotomy between ac-              gain in efficiency for the three-dimensional dense fluids
                                                      cessible length-scales and timescales is a major challenge        considered here is at most a factor of 40 [24], which re-
                                                      for glass transition studies [1, 6, 7].                           mains insufficient to close the gap with experiments. A
                                                         There are several promising experimental advances              crucial aspect for the efficiency of this approach is the
                                                      which could improve either the dynamic range of colloidal         choice of the correct type of collective move, which still
                                                      experiments [8] or the spatial resolution in molecular su-        requires some a priori knowledge of the relaxation path
                                                      percooled liquids [9]. In addition, new protocols to pre-         used by the system [25]. This, however, is precisely one of
                                                      pare molecular glasses corresponding to even larger relax-        the informations that remains to be understood in fragile
                                                      ation times are being developed [10]. On the simulation           glass-forming materials.
                                                      front, the situation appears challenging, as the increase in         A different simulation strategy is the replica-exchange
                                                      the time window accessible to computer simulations has            technique, where simulations of the same system are con-
                                                      been rather slow, amounting to a gain of about 3 orders           ducted in parallel over a range of state points, and in-
                                                      of magnitude over the last 30 years [4, 11, 12], and this         frequent exchanges between neighboring state points are
                                                      is mostly due to improvements in computer hardware. A             performed [27–30]. The idea is that navigating through
                                                      rough extrapolation of this trend would pessimistically           different state points would facilitate the crossing of large
                                                      suggest that it could take another 100 years for sim-             barriers in a complex free energy landscape, and in-
                                                      ulations to close the gap with experimentally relevant            deed the technique was first developed to study spin
                                                      thermodynamic conditions. The recent advent of graphic            glasses [27]. In dense fluids the reported speedup is
                                                      processing units and accelerators in the high-performance         again of about two orders of magnitude [29, 30], with
                                                                                                                               2



      P(σ)

                     Binary    Ternary                      Continuous polydisperse                               Hybrid
       n              12         12              8     12       18       24      12     12     12            12       12-6
       ε               0          0              0      0       0         0     0.1     0.2    0.3            0            0


               1.2



                 1
      T/TMCT




               0.8



               0.6



     log(τα/τ0)        3          6              4      6       10       >12    >12    >12      3             8            8


FIG. 1. Summary of the results obtained for the eleven models studied in this work. The top row sketches the particle size
distribution for each model, the next two lines specify the pair potential and its additivity. Below, we use a temperature axis
rescaled by the location of the mode-coupling crossover where blue points indicate equilibrium disordered fluid configurations,
red diamonds indicate instability towards crystalline or demixed states. The bottom line indicates the estimated range of
equilibrium relaxation times τα that can be studied in stable equilibrium conditions for each model, using τ0 as the relaxation
time at the onset temperature [26]. We have constructed several models which remain stable and can be equilibrated deep in
the temperature regime T /TM CT < 1 that conventional simulation studies are unable to penetrate, three of which allowing us
to reach temperature below the experimental glass transition, conventionally defined as τα /τ0 = 1012 .


the additional drawback that the replica-exchange tech-              and hard spheres [50]. In an effort to improve the sta-
nique scales very poorly with the number of particles and            bility of discrete mixtures, Gutierrez et al. recently in-
looses most of its efficiency for system sizes of thousands          troduced a ternary mixture of soft spheres to study the
of particles, which are typically used in studies of the bulk        increase of a static length-scale [51]. Very low tempera-
glass transition [30]. Therefore, replica exchange works             tures were studied and a claim of a 10-decade efficiency
best for studies of equilibrium phase transitions in small           gain was made. We demonstrate below that changing
systems, as confirmed in a series of recent studies [31–34].         from a binary to a ternary mixture indeed improves the
Different algorithms such as Wang-Landau sampling [35]               thermodynamic stability, but the claims made in [51] do
and population dynamics [36] have also been employed                 not resist our detailed analysis of the structure and ther-
in the context of glass studies.                                     malization dynamics of the model. We will demonstrate
   The swap Monte Carlo algorithm is another longstand-              that the efficiency gain for this model is much more mod-
ing simulation technique that has been used in computer              est and the accessible dynamical window is increased by
studies of the glass transition. The algorithm was first in-         about 2-3 orders of magnitude.
troduced to study the equation of state of a non-additive               The aim of our work is to bring the swap algorithm to
hard sphere system [37] and later rediscovered in the con-           a whole new level of performance. We present a system-
text of the glass transition of a binary mixture of soft             atic study of glass-forming ability and thermalization effi-
spheres [38]. The swap algorithm has since been mostly               ciency over a broad range of glass-forming models, vary-
used in the glass context, for both binary mixtures [39–             ing the particle size distribution and the nature of the
42] and for continuously polydisperse systems [43–45].               pair interactions, while optimizing the swap Monte Carlo
For the binary mixture of Ref. [46], the reported speedup            algorithm. Our main result, summarized in Fig. 1, is
in terms of equilibration times is a factor of 180, inde-            the discovery that particular combinations of parameters
pendent of temperature [47]. The glass-forming ability               yield both excellent glass-forming ability and a dramatic
of this model is, however, poor due to the appearance                decrease of the computer time needed to obtain thermal-
of ordered phases [38, 48, 49]. Little quantitative infor-           ized configurations at low temperatures. This insight has
mation is available concerning the efficiency of the swap            already led to some new results on related phenomena,
algorithm for continuously polydisperse soft [44, 45, 48]            such as jamming [52] and the Gardner transition [53].
                                                                                                                          3

   As shown in Fig. 1, we systematically change the size       lis acceptance rule, which ensures that detailed balance
distribution, using a variety of discrete and continuous       is obeyed at each temperature T . For each model, the
mixtures, we vary the softness of the pair repulsion,          typical jump length δl is fixed to a fraction of the aver-
its additivity, and we add attractive forces. For each         age particle diameter, which results in an acceptance rate
case, we determine both the temperature regime where           ranging typically from about 60% at high temperatures
the model is structurally unstable (shown with red sym-        to 30% at low temperatures. This approach to simulat-
bols) and the temperature regime where the disordered          ing glass-formers has been validated by direct comparison
fluid states is stable at equilibrium (shown with blue         with molecular dynamics results for the specific case of a
symbols). The vertical axis represents the temperature         binary mixture [56].
T , scaled by the location of the corresponding mode-             In addition to displacement moves, during a swap
coupling crossover, TMCT . Although somewhat arbi-             Monte Carlo simulation we also attempt to exchange the
trary, this rescaling demonstrates the efficiency of the       diameters of two randomly chosen particles. The diam-
thermalization because conventional computer simula-           eter exchange is again accepted based on the Metropo-
tions typically fail to reach equilibrium in the regime        lis criterion. At every Monte Carlo step, such a “swap
T /TMCT < 1. Despite the differences between systems,          move” is attempted with probability p. We emphasize
several of them can be thermalized in the supercooled          that swap moves preserve detailed balance and thus guar-
liquid state at significantly lower temperatures than or-      antee an equilibrium sampling of phase space [18]. In
dinary simulations. We demonstrate that this tempera-          other words, despite the “nonphysical” nature of the
ture regime corresponds, for some of these models, to a        swap moves (in an experiment, particles would not ex-
range of relaxation times of more than twelve decades,         change their diameters spontaneously) the swap Monte
which implies that we can access in equilibrium a tem-         Carlo dynamics enables a proper sampling of the equi-
perature regime that is even lower than the experimental       librium thermodynamic properties of the model. In pre-
glass transition temperature, Tg . We show that this cor-      vious implementations of the swap Monte Carlo, particle
responds to a speed-up of the thermalization of about ten      swaps were described as particles exchanging their posi-
orders of magnitude at Tg .                                    tions, instead of their diameters [38]. Both descriptions
   The two key factors enabling such progress are the          are of course fully equivalent, but our choice offers the
use of an appropriate size polydispersity to prevent both      advantage that single particle dynamics can be followed
crystallization (when polydispersity is too small) and         in time, because particles do not make arbitrarily large
phase separation (when it gets too large), and a parti-        jumps during the swap moves. Standard time correla-
cle size distribution that allows for a large acceptance       tion functions based on particle displacements can thus
rate for particle swaps, in turn leading to a fast thermal-    be measured in swap and ordinary Monte Carlo simula-
ization and equilibrium sampling of phase space.               tions in the exact same way. Dynamic measurements are
   The outline of the article is as follows. Sec. II is ded-   a crucial tool to assess the thermalization of our swap
icated to the simulation strategy and technicalities. Re-      simulations, just as they are for standard simulations
sults for two families of systems (mixtures and continuous     of supercooled liquids. One Monte Carlo sweep is then
polydisperse systems) are reported and discussed respec-       defined as N consecutive attempts to either displace or
tively in Secs. III and IV. We give a physical insight on      swap particles diameters, and one such sweep will repre-
swap dynamical relaxation and heterogeneities in Sec. V.       sent in the following our time unit.
Sec. VI deals with the introduction of a model designed           In this work we study three different classes of sys-
to maximize the algorithm efficiency. Finally, Sec. VII        tems, with particle size distributions as sketched in Fig. 1.
presents our conclusions and offers further perspectives       They are either discrete or continuous mixtures. Discrete
for future work.                                               mixtures are characterized by a particle size distribution
                                                               P (σ) of the form
                                                                                          m
                                                                                          X
      II.   DETAILS OF THE SIMULATIONS                                          P (σ) =         xα δ(σ − σα ),          (1)
                                                                                          α=1
 A.   Algorithm, interactions and size distributions
                                                               where m is the total number of components, xα indicates
                                                               the fractional composition of each species, and σα is the
   We simulate systems of N particles in a cubic box of        diameter of species α. Within the class of continuously
side L with periodic boundary conditions [54]. Through-        polydisperse systems, we focus on a specific kind of size
out the paper we will compare results obtained from two        dispersity, which scales as the inverse of the occupied
kinds of simulation methods: standard Monte Carlo sim-         volume:
ulations in the canonical ensemble [55] and swap Monte
                                                                                   A
Carlo simulations [37, 38]. Both simulation algorithms                     P (σ) = 3 ,     σ ∈ [σmin , σmax ],       (2)
involve the same displacement moves, in which we pick                              σ
up one particle at random and attempt to translate it          where A is a normalizing constant and σmin and σmax
by a displacement vector randomly drawn in a cube of           are the minimum and the maximum diameter values, re-
linear size δl. The move is accepted using the Metropo-        spectively. This functional form ensures that the volume
                                                                                                                        4

fraction occupied by particles within a given bin size is      Systems characterized by ǫ = 0 and ǫ 6= 0 will be re-
constant. Such a scaling property has been shown to en-        ferred to as additive and non-additive systems, respec-
hance glass-forming ability in discrete mixtures [57], but     tively. Non-additivity is another ingredient which has
we have not tested this hypothesis in great detail for the     been widely used to enhance glass-forming ability in sim-
present systems.                                               ple binary models [58] and is a consequence of the band
   Finally, we introduce a second type of continuous par-      structure of the electronic density of states in metallic
ticle size distributions, which combine the salient features   alloys [59]. Physically, the non-additive rule in Eq. (8)
of both discrete and continuous mixtures. For this reason      implies that particles with identical diameters interact
we call them “hybrid” distributions, see Fig. 1. Mathe-        as before, but that small and large particles can have a
matically, the distributions read                              larger overlap than for additive systems.
                       m
                       X
             P (σ) =         xα θ(bα − |σ − σα |),      (3)
                       α=1
                                                                              B.   Physical observables

where θ(x) is the Heaviside function and xα is defined
                                                                  In this section we introduce the basic observables used
as before. In this approach each component of the “mix-
                                                               to characterize the structure and dynamics of the studied
ture” is characterized by a flat particle size distribution
                                                               models. We will use them to monitor the equilibration
of width bα . The goal is to construct models that com-
                                                               and the stability of the fluids under supercooled condi-
bine advantages of both discrete mixtures, which are typ-
                                                               tions and to quantify and compare the degree of thermal-
ically good glass-formers, and continuous distributions,
                                                               ization achieved by both standard and swap simulations.
for which swap dynamics is very efficient.
                                                                  We systematically compute the structure factor [60],
   We quantify the degree of polydispersity of a system
by the normalized root mean square deviation                                                1
                                                                                   S(k) =     hρk ρ−k i,              (9)
                        p
                          hσ 2 i − hσi2                                                     N
                    δ=                  ,               (4)    where ρk is the Fourier transform of the microscopic den-
                              hσi
                                                               sity at wavevector k. The behavior of S(k) at small wave-
 where the brackets indicate an average of the particle        number provides information on possible long-range den-
Rsize distribution. In the following, we will use hσi =        sity fluctuations and will be checked to identify signals
   P (σ)σdσ as the unit length for each studied model.         of instability of the homogeneous fluid. Since we deal
    We model the interactions between two particles i and      with size-disperse systems, we compute partial structure
 j via a soft repulsive pair potential of the type             factors associated to each subpopulation. In the case of
                                 n
                                                               continuously polydisperse systems, we group particles of
                           
                             σij
                 v(rij ) =          + F (rij ),        (5)     comparable size into families labeled by an index α, for
                             rij
                                                               which we compute the partial structure factor Sαα (k). A
where n is an exponent controlling the softness of the         strong increase of Sαα (k) at small k values is associated
repulsive potential, and F (rij ) is a function that smooths   to phase separation or demixing, and we have monitored
the potential at the cutoff distance rcut , beyond which       this quantity systematically in our models.
the potential is set to zero. Unless otherwise specified,         Beside particle demixing, the main instability to be
we use [51]                                                    overcome is of course crystallization. To detect the pres-
                            
                              rij
                                  2       
                                             rij
                                                 4            ence of crystalline local order, we measure the 6-fold
         F (rij ) = c0 + c2           + c4          .    (6)   bond-orientational order parameter [61]
                              σij            σij
                                                                                 v
                                                                                                                      2+
The coefficients c0 , c2 , and c4 ensure the continuity of
                                                                                 u
                                                                                         6          Nb (i)
                                                                         *
                                                                           1     u 4π X         1 X
                                                                             X   u
the potential up to the second derivative at the cutoff           Q6 =           t                         Y6m (rij )    ,
distance rcut = 1.25σij . Additionally, we also studied                    N i      13 m=−6 Nb (i) j=1
a polydisperse model where particles interact with the                                                                (10)
Lennard-Jones potential                                        where Y6m (rij ) are spherical harmonics. The sum over
                          12        6                      1 < j < Nb (i) runs over the neighbors of particle i in
                       σij         σij
           v(rij ) =           −          + cLJ ,      (7)     a sphere of radius corresponding to the minimum of the
                       rij         rij
                                                               distribution function of rescaled inter-particle distances,
for which we simply cutoff and shift the pair potential at     g(rij /σij ). We inspect the time and temperature varia-
the cutoff distance rcut = 2.5σij .                            tion of Q6 , as well as that of the potential energy e, to
  Finally, to ensure a high structural stability in our        check whether the systems are stable against crystalliza-
models, we introduce a generalized non-additive inter-         tion.
action rule for the cross diameters σij in the pair inter-        We provide a systematic characterization of both self
action, which reads                                            and collective dynamics of the models. This enables us
                    σi + σj                                    to quantify the degree to which swap simulations en-
              σij =         (1 − ǫ|σi − σj |).         (8)     hance thermalization compared to standard Monte Carlo.
                        2
                                                                                                                           5

We note that while standard Monte Carlo dynamics [56]            divergence of the relaxation time at low temperature. A
can be used to mimic overdamped Brownian dynam-                  final form that we use is the Arrhenius law,
ics, as appropriate for a colloidal suspension [4], the                                          ′′ 
microscopic dynamics of swap simulations is not phys-                                     ′′      A
                                                                                   τα = τ∞ exp          ,           (15)
ical. We emphasize however that particles’ trajectories                                           T
remain well-defined, because the swap moves only ex-
                                                                        ′′
change the particle diameters, not their positions. Thus,        with τ∞    and A′′ two fitting parameters.
even though the microscopic dynamics is nonphysical,                Using these functional forms will be useful below to es-
time-dependent correlation functions still quantify the          timate the range of relaxation times that swap dynamics
timescale over which individual particles diffuse (for self-     allows us to access. Our analysis shows that the VFT
correlation functions) and over which the density fluctu-        law presumably overestimates the growth of the relax-
ations relax (for collective correlations). Time correla-        ation time whereas the Arrhenius law underestimates it,
tion functions will be used in the following to determine        the parabolic law falling somewhat in-between. Thus the
whether the system has been efficiently thermalized at a         combination of all three fitting functions provides an es-
given state point.                                               timate of the actual physical behavior and a sensible con-
   We characterize the single particle dynamics through          fidence interval in low temperature extrapolations.
the self-part of the intermediate scattering function               The relaxation of collective density fluctuations is mea-
                             *                        +          sured via the time-dependent overlap function
                               1 X ik·[rj (t)−rj (0)]
   Fs (k, t) = hfs (k, t)i =       e                    , (11)
                                                                                    *                                +
                               N j                                                    1 X
                                                                           Fo (t) =          θ(a − |ri (t) − rj (0)|) ,  (16)
                                                                                      N i,j
where the wavenumber k corresponds to the first peak
of the total structure factor S(k). Notice that since the        using a cutoff distance a = 0.3. This quantity provides
particle diameter changes during the course of the sim-          similar information as the coherent intermediate scatter-
ulations, the sum in Eq. (11) runs over all particles, the       ing function at wavevector k = 2π/a, but is computation-
distinction between large and small particles being im-          ally more advantageous because it presents much smaller
material. The structural relaxation time τα is then de-          statistical fluctuations. From this function, we define a
fined as the value at which Fs (k, τα ) = e−1 , following        relaxation time τo for the decorrelation of collective den-
common practice. We use the relaxation time τα mea-              sity fluctuations, such that Fo (τo ) = e−1 .
sured for standard Monte Carlo simulations to locate the            For selected models we computed a number of addi-
mode-coupling crossover at T = TMCT , which we take as           tional static and dynamical observables with the aim of
a relevant temperature scale for computer simulations.           understanding microscopic processes taking place during
In order to obtain TMCT we fit the standard dynamics             the swap Monte Carlo simulations. These more specific
(without swap) in the interval τ0 < τα < 103 τ0 with a           observables are described later in Sec. V.
power law divergence [62],

                   τα ∝ (T − TMCT )−γ .                  (12)                 C.   Efficiency of swap moves

When discussing the dynamics of our models, we will also            Because the swap Monte Carlo is conceptually very
use other functional forms to describe the temperature           simple, there are very few parameters that can be ad-
evolution of the relaxation time. A well-known functional        justed to optimize its efficiency. We discuss how to
form is the Vogel-Fulcher-Tamman (VFT) law [1],                  achieve maximal efficiency in the present section.
                                                                  The extent to which swap moves accelerate the sam-
                                  A                              pling of configuration space during a Monte Carlo sim-
                 τα = τ∞ exp             ,           (13)
                                T − T0                           ulation must depend on the frequency used to attempt
                                                                 such moves, which is given by the probability p. There
where τ∞ , A and T0 are fitting parameters. Because              are two obvious limiting cases. For p = 0 one recovers the
this functional form describes a dynamic singularity at a        dynamics of a standard Monte Carlo simulation without
finite temperature T = T0 , it produces a very steep tem-        swap moves. For p = 1, instead, only swap moves are
perature dependence. A less pronounced temperature               attempted and the particle positions are never updated,
dependence is obtained with the parabolic law [63],              so that by construction structural relaxation cannot take
                         "             2 #                     place. The optimal choice for p is thus the one that min-
                    ′        ′   1   1                           imizes the structural relaxation time τα of the system
             τα = τ∞ exp A         −         ,        (14)
                                T    T1                          with respect to p.
                                                                    We illustrate the optimisation procedure for a continu-
        ′
where τ∞  , A′ and T1 are again free parameters. Notice          ously polydisperse particles system interacting via a soft
that no dynamic singularity is predicted from Eq. (14),          repulsive potential as in Eq. (5) with n = 12, with a non-
since T1 captures the onset of slow dynamics and not the         additivity ǫ = 0.2. This model is further discussed in
                                                                                                                                                   6

              1                                                                        even when taking this additional effect into account. In
                                                 2
                                            10
                                                                                       terms of CPU time, one MC sweep with p = 0.2 takes
                                                 1
                                            10                                         only 20% longer on average than a standard sweep with
                                                 0
                                                                                       p = 0. This should be contrasted with the orders of mag-




                                    P(∆σ)
              -1                            10
         10
                                            10
                                                 -1                                    nitude of gain achieved in terms of structural relaxation
                                                                                       time.
τα/τ*α




                                             -2
                                            10
                                             -3
                                                                                          Another major advantage of the swap Monte Carlo al-
          -2                                10 0
         10                                                0.1        0.2    0.3       gorithm is that both its implementation and its efficiency
                                                                 ∆σ
                                                                                       are insensitive to the number of particles in the system,
                                                                                       N . This contrasts strongly with the replica exchange
              -3
                                                                                       method, which scales very poorly with N [27–30].
         10                                                                               In general, the acceptance ratio of Monte Carlo moves
          10
                   -6    -5
                        10
                               -4
                              10    10
                                       -3              -2
                                                      10          10
                                                                        -1
                                                                               10
                                                                                   0   decreases upon lowering temperature or increasing the
                                    p                                                  density. Similarly, the acceptance ratio of swap moves
                                                                                       decreases when the size difference ∆σ = |σ1 − σ2 | of the
FIG. 2. The relaxation time τα as function of the swap at-                             two selected particles increases, because a large parti-
tempt probability p, normalized by τα∗ , its value for standard                        cle will not easily fit into the hole occupied by a small
Monte Carlo simulations when p = 0. A broad minimum                                    one. As will be clear in the following, the efficiency of
indicates that p ≈ 0.20 optimizes the efficiency of the swap                           swap moves is highest in continuously polydisperse sys-
Monte Carlo algorithm. The inset shows the probability dis-                            tems, where the diameter difference between any two par-
tribution of swap acceptance as a function of the diameter
                                                                                       ticles can be arbitrarily small. In these systems, it is
difference ∆σ = |σ1 − σ2 | between the particles for which
the swap move is attempted. The system is a soft repulsive                             pertinent to avoid attempting exchanges when ∆σ is too
system of non-additive particles studied in Sec. IV C, with                            large because the swap move is then essentially always re-
ǫ = 0.2 and T = 0.101.                                                                 jected [48]. This point is illustrated in the inset of Fig. 2,
                                                                                       where we show P (∆σ), the probability distribution of
                                                                                       acceptance rates for swap moves between pairs of parti-
Sec. IV C. The general trend found for this model is rep-                              cles with a size difference ∆σ for the same parameters
resentative of the three classes of systems we investigated                            as in the main frame of the figure. We notice that the
and is shown in Fig. 2, where we report the structural                                 acceptance rate decays exponentially fast with ∆σ and
relaxation time of the system versus p at a constant tem-                              becomes vanishingly small when ∆σ >      ∼ 0.25. Following
perature, T = 0.101. We normalized the relaxation time                                 Ref. [48], we therefore disregard swaps between particles
by the corresponding value in the absence of swap moves                                with a diameter difference larger than a certain cutoff.
at p = 0. At this particular temperature, we observe that                              We choose here ∆σmax = 0.2, which we found to be a
the structural relaxation time becomes almost three or-                                reasonable trade-off. We implement this threshold value
ders of magnitude faster compared to standard dynamics                                 in a way that preserves detailed balance. In practice, we
already for very small values of p, i.e. p of the order of                             always choose two particles at random, but we directly
a few percents. We observe a relatively broad minimum                                  reject the swap without evaluating any energy difference
around p ≈ 0.2 before τα starts to grow again and di-                                  if ∆σ exceeds the chosen cutoff value.
verges for p = 1 as τα ∼ (1 − p)−1 , when particles stop
diffusing for the trivial reason mentioned above. From
such a graph, we deduce that p ≈ 0.2 is the optimal value                                       D.    Equilibration and metastability
for the probability to perform swap moves. We find that
this value is fairly robust when temperature is changed                                   Simulations of glass-forming liquids must be long
or across different models, which presumably stems from                                enough to ensure equilibrium sampling of the observables
the fact that the minimum reported in Fig. 2 is relatively                             of interest and yet short enough to avoid crystallization
flat. Another remarkable feature of this figure is the very                            or more complex forms of structural ordering. Simple
steep decrease of τα observed for even very small values                               models such as binary mixtures or weakly polydisperse
of p suggesting that even a fairly small amount of swap                                systems have been shown to crystallize over sufficiently
moves is in fact sufficient to facilitate enormously the                               long times [44, 45, 48, 64–66]. Computer simulations of
structural relaxation of the system.                                                   glass-forming materials thus always represent a narrow
   Efficiency considerations should also take into account                             compromise between those two limits that both need to
the CPU time needed to perform a swap move as opposed                                  be addressed carefully.
to a standard displacement. An attempt to swap diam-                                      These issues become particularly severe when employ-
eters entails the computation of the local energy varia-                               ing enhanced sampling algorithms, such as swap Monte
tion between the new and the old configuration for two                                 Carlo moves which are precisely constructed to promote
particles, which is twice what is needed for an ordinary                               a more efficient exploration of phase space. For in-
displacement move involving only one particle. However,                                stance, crystallization of two-component mixtures of re-
we found that the optimum value for p barely changes                                   pulsive spheres has been reported in swap Monte Carlo
                                                                                                                         7

simulations [48, 49, 67]. The ground-state of polydis-         to obtain a rough estimate of the structural relaxation
perse repulsive particles was studied both with swap           time τα in the presence of swap moves. After this is
Monte Carlo [44] and in the semi-grand canonical en-           done, the system is simulated over a total of 200τα to
semble [64, 65]. These studies found that for sufficiently     measure static and dynamic properties over a sufficiently
high polydispersity the stable structure is a fractionated     wide time window. Notice that this thermalization pro-
crystal, where the system presents multiple crystals each      cedure is rather demanding and thermalization thus re-
involving a fraction of the system overall particle size       quires that we are able to perform simulations over a time
distribution. However, as noticed in [64], the free en-        window which is 2 orders of magnitude longer than the
ergy cost of forming an interface between distinct phases      structural relaxation time. We emphasize that such pro-
is generally high and crystallization may be difficult to      cedure is not specific to the presence of the swap moves.
observe in practice.                                           We think that simulation of supercooled liquid should fol-
   The general conclusion to be drawn from these earlier       low similar strict rules to claim that equilibration as well
works is that a model considered as a good glass-forming       as a proper sampling of phase space has been achieved.
system when studied using conventional simulations tech-          Almost every system we simulated eventually displays
niques may turn out to be a very poor model when using         some form of structural instability at sufficiently low tem-
an enhanced simulation technique that is able to probe a       perature, such as nucleation of an ordered phase or long
much wider range of temperatures. Indeed, we find that         wavelength density fluctuations and demixing. These in-
many previously studied types of glass-forming models          stabilities are detected via the observables introduced in
do not withstand basic stability criteria when the swap        the previous section. To decide whether a given state
technique is applied, forcing us to develop novel numer-       point remains in a metastable disordered fluid state, we
ical models in addition to the optimization of the swap        use the following criterion. We perform five independent
Monte Carlo method.                                            simulations along the lines described above. If at least
   To make a consistent comparison of the glass-forming        one among the five samples shows an instability over a
ability of the studied models in standard and swap sim-        time window of 200τα , then we classify this state point
ulations, we follow a rigorous and identical equilibration     as unstable and that the system is a poor glass-former
protocol for all our models. First, we obtain static and       at this temperature. The precise meaning of “instabil-
dynamical properties of the system by means of stan-           ity” is system-dependent and will be specified in each
dard Metropolis Monte Carlo simulations in the N V T           studied case in Secs. III and IV. This criterion is rather
ensemble [55]. From these simulations we extract the           strict, as there could still be room for achieving ther-
average potential energy value, the structure factors and      malization and performing equilibrium sampling while
the structural relaxation times. For each model we deter-      avoiding structural instability, but this is dangerous as
mine TMCT using Eq. (12), which will serve as a reference      fluctuations related to ordering could interfere with the
temperature scale to compare the degree of supercooling        physics of the metastable disordered state. In addition,
across different models. This is not an ideal choice, but it   we find that when a state point is deemed unstable using
offers the advantage that extrapolation of the relaxation      our criterion, then lower temperatures are also unstable
times to low temperatures is not needed.                       and the instability rapidly becomes so severe that further
   Swap Monte Carlo simulations start from a configura-        studies can not be safely performed. Thus, changing the
tion equilibrated at the onset temperature To [26], fol-       details of our criterion would simply shift the range of
lowed by an instantaneous quench to the target temper-         “metastable” temperatures by a very small amount and
ature T . The following criteria are used to determine         our conclusions would not be affected.
whether the system has reached equilibrium at T . First,          We directly compare the equilibration process between
we monitor the potential energy e per particle. We in-         standard and swap simulations in Fig. 3. Starting from a
spect both its instantaneous value as a function of time,      high temperature configuration we progressively quench
e(t, T ), to detect aging, as well as its time average as a    the system down to zero temperature using a constant
function of temperature hei(T ), to detect possible dis-       cooling rate γ = dT /dt with values changing logarith-
continuities or change of slope in the equation of state       mically over a broad interval (2.5 × 10−5 , 2.5 × 10−9 ).
of the liquid. Second, we ensure that    Pthe total mean-      We further average our results using ten independent
squared displacement ∆r2 (t) = h1/N i [ri (t) − ri (0)]2 i     initial configurations. For standard Monte Carlo simu-
has reached a value at least larger than 6. This spe-          lations, we retrieve the expected behaviour where depar-
cific value is relatively immaterial as this criterion only    ture from the equilibrium equation state arises at lower
conveniently guides us between state points where parti-       temperature for lower cooling rate, as signalled by a rate
cle displacements are large over the numerical time win-       dependence of the energy. Using swap simulations, we
dow, from those where particle dynamics is essentially ar-     obtain the very same equation of state at equilibrium,
rested. Finally, we look at the self-incoherent scattering     and a similar rate-dependent behaviour at low temper-
function. For this quantity, we check, within statistical      atures. The major difference between the two sets of
fluctuations, both the absence of aging and the complete       simulations is that swap simulations clearly fall out of
decorrelation to zero at long times. Once equilibration        equilibrium at considerably lower temperatures than or-
has been reached, we perform a first set of simulations        dinary Monte Carlo simulations. The agreement of the
                                                                                                                                                             8

     0.7                                                                      1
                               -5
                                                                                                                                  Standard
                   γ=2.5x10
     0.6                       -6
                                                                            0.8
                        2.5x10
                               -7
                        2.5x10




                                                                                                                                  Sw
                               -8
     0.5                2.5x10




                                                                                                                                     ap
                                                                            0.6




                                                                  Fs(k,t)
     0.4
 e




                       rd
               nda                                                          0.4
            Sta
     0.3
                                                                            0.2
                    ap                                                             (a)
     0.2          Sw

                                                                             0
     0.1                                                                       0         1        2      3           4    5         6        7       8
        0          0.5              1        1.5   2     2.5                 10     10       10        10       10       10       10       10       10
                                        T/TMCT                                                                   t
                                                                              1

FIG. 3. Potential energy per particle in simulations with dif-
ferent cooling rates γ using both standard and swap Monte                   0.8
Carlo. Both dynamics produce consistent results at high
temperatures, but the swap dynamics remains at equilibrium
                                                                            0.6
down to much lower temperatures than the standard one. The




                                                                  Fo(t)
system is the soft repulsive system of non-additive particles
studied in Sec. IV C, with ǫ = 0.2.                                         0.4


                                                                            0.2
                                                                                    (b)
two sets of curves when they both probe equilibrium is an
indication that swap dynamics has been correctly imple-                      0 0         1        2         3        4        5        6        7        8
                                                                             10     10       10        10       10       10       10       10       10
mented and and provides the correct sampling of phase                                                            t
space. The second information gained from this set of
data is the clear indication that the swap Monte Carlo           FIG. 4. Swap dynamics in a soft repulsive system of non-
algorithm extends the regime where equilibrium studies           additive particles studied in Sec. IV C with ǫ = 0.2. (a) Self-
are possible by a large amount and is able to produce            incoherent scattering Fs (k, t) computed respectively on the
highly stable glass configurations.                              first (full lines) and second (dashed lines) half of the simu-
                                                                 lation run. Results for standard dynamics without swap for
   To illustrate our equilibration protocol, we show in          the lowest temperature are shown with a dotted line. (b)
Fig. 4(a) the incoherent scattering function for the same        Collective overlap correlation function Fo (t). In both panels,
system as in Fig. 2 (see also Sec. IV C) evaluated over the      temperatures are T = 0.25, 0.175, 0.125, 0.092, 0.075, 0.065,
first and the second halves of the simulation at various         0.062, 0.058, 0.0555, from left to right. Swap Monte Carlo
temperatures. As we can see, the two sets of curves agree        simulations fully decorrelate both single particle and collec-
within statistical uncertainty over a wide range of tem-         tive density fluctuations in a regime where standard Monte
peratures, demonstrating the absence of aging. For the           Carlo simulations may be fully arrested.
lowest temperature at which thermalization with swap
moves is achieved, we show the corresponding relaxation
function obtained without swap, which quickly decays                 III.         RESULTS FOR DISCRETE MIXTURES
to a plateau that extends over the last 6 decades of the
simulation. This shows that without swap moves, the dy-                                      A.       Binary mixtures
namics is fully arrested at these low temperatures, and
no equilibrium simulations can presently be performed in
                                                                    Simple binary mixtures of repulsive spheres were the
this regime with conventional computational techniques.
                                                                 first computer models for supercooled liquids simulated
   In Fig. 4(b), we show the collective overlap func-            using the swap Monte Carlo method [37, 38]. Here, we
tion, Eq. (16), which decorrelates to a density-dependent        focus on the “historical” 50:50 binary mixture introduced
plateau at long times, as expected in ergodic equilib-           long ago by Bernu et al. [68], which has been frequently
rium simulations. The two plots of Fig. 4 underline the          used since its introduction. The pair interaction is given
fact that swap Monte Carlo simulations fully decorrelate         by Eqs. (5) and (8) with ǫ = 0 and F (rij ) = cαβ , where
both single particle and collective density fluctuations in      α, β = A, B are species indexes. The size ratio is σσBA
                                                                                                                         =
a regime where standard Monte Carlo simulations may              1.2, resulting in a polydispersity δ = 9.1%. √
                                                                                                              The potential
be fully arrested and therefore represent an efficient and       is cutoff and shifted at a distance rcut = 3, a specific
reliable method to sample the configuration space.               value which was often used in previous studies [38, 48,
                                                                                                                                              9

       6                                                                            of a temperature regime that is not already accessible
     10
                                                                                    with ordinary simulations.


              St a
                                                                                       In the inset of Fig. 5 we show the time series of the

                  nda
                                      2                                             potential energy of a sample at T = 0.2, where rapid




                                 e
       5

                     rd
     10                                                                             crystallization is observed when swap dynamics is em-
                                                                                    ployed. We note that crystallization in this model is well-
τα




                                                                                    documented and has been studied in detail in small sam-
                                     1.9
     10
       4      Sw
                ap
                                       0.0         1.0×10
                                                          6               6
                                                                     2.0×10         ples [48, 69]. Since complex strategies would be needed
                                                      t                             to detect and filter out crystallized configurations [67]
                                                                                    already near the mode-coupling crossover, we conclude
          3                                                                         that this “historical” model can indeed be efficiently sim-
     10
                                                                                    ulated using swap Monte Carlo but is too poor a glass-
      0.2                 0.25               0.3              0.35            0.4   former to fruitfully explore novel physical regimes.
                                             T                                         Within the realm of simple binary mixtures, it is diffi-
                                                                                    cult to make further progress using swap Monte Carlo be-
FIG. 5. Relaxation times τα of standard (black empty points)                        cause to increase the structural stability of the system one
and swap (red full squares) simulations for the binary mixture
                                                                                    would need to increase the size ratio (for instance using
of soft repulsive spheres studied in Sec. III A. The speedup of-
fered by the swap moves is obvious, but the system is unstable
                                                                                    the more stable σA /σB = 1.4 well-studied model), but
below T = 0.202 where it crystallizes, and temperatures be-                         this would imply that the already very low acceptance
low the mode-coupling temperature TM CT = 0.199 cannot                              rate for swap moves would become vanishingly small and
be studied. The inset shows a time series of the potential                          swap would thus not be a useful method. Therefore,
energy for standard (black) and swap (red) simulations at                           the trade-off between stability and swap efficiency leaves
T = 0.2, showing that crystallization is easily observed when                       very little room for a drastic improvement of simulation
swap moves are introduced.                                                          techniques when binary mixture models of glass-formers
                                                                                    are used. Another option is to introduce non-additivity
                                                                                    in the interactions, as for instance in the classic Kob-
67]. We simulate N = 1024 particles at the number                                   Andersen mixture [58]. Rather than for binary mixtures,
density ρ = 1.                                                                      we will explore this possibility for a different family of
   As already demonstrated before [67], swap moves help                             models based on continuously polydisperse particles (see
to accelerate sampling in this system, even though their                            Sec. IV).
acceptance rates is relatively low, of order a ∼ 10−2 . We
confirm this finding in Fig. 5 where we compare the struc-
tural relaxation time τα measured during standard and                                               B.    A ternary mixture
swap Monte Carlo simulations. Over the range of tem-
peratures at which the system can be equilibrated accord-                              Given the limits demonstrated above for binary mix-
ing to our criteria (see Sec. II D), swap moves result in                           tures, a natural strategy is to increase the number of
a speedup of about 2 orders of magnitude at the lowest                              components in the model. Adding more chemical com-
temperature. Notice that contrary to published analy-                               ponents is indeed a commonly used method to improve
sis [47], we find that the efficiency of the swap over the                          the glass-forming ability of metallic alloys. In addition,
standard Monte Carlo method is strongly temperature-                                by increasing the number of components, one can simul-
dependent, and efficiency increases rapidly as tempera-                             taneously increase the polydispersity, and thus the glass-
ture decreases.                                                                     forming ability of the model, while preserving the swap
   Unfortunately, however, the temperature range that                               efficiency by introducing particles with size ratios that
can be analyzed with this system does not change dra-                               are small enough for swap moves to be frequently ac-
matically when swap moves are introduced. In fact,                                  cepted.
even using standard MC, the system crystallizes at the                                 This strategy was recently followed in Ref. [51], where a
lowest studied temperature and becomes unstable when                                ternary mixture of soft spheres was introduced and stud-
T < 0.202, which is marginally larger than the location of                          ied using swap Monte Carlo dynamics. The potential
the mode-coupling crossover, TMCT ≈ 0.199. Notice that                              used in that work can be cast in the form of Eq. (5) with
earlier, incorrect determinations of the mode-coupling                              a softness parameter n = 12 and F (rij ) as in Eq. (6), with
crossover temperature of this system have misleadingly                              a cutoff distance rcut = 1.25σij . We simulated systems
suggested that temperatures well below TMCT could be                                with N = 1500 particles at the number density ρ = 1.1,
simulated with this system. In reality, TMCT represents                             as in the original version of the model [51]. The size
the lowest temperature that can be safely studied, swap                             ratio between two species is σσB A
                                                                                                                       = σσB
                                                                                                                           C
                                                                                                                              = 1.25, which is
moves merely providing a more efficient way of produc-                              slightly larger than for the binary mixture studied above
ing thermalized configuration in the temperature regime                             in Sec. III A, and compositions xA = 0.55, xB = 0.30,
T > TMCT . In other words, swap MC accelerates the dy-                              and xc = 0.15, which ensures that all species roughly
namics of the system but does not allow the exploration                             occupy the same fraction of the total volume. The cor-
                                                                                                                           10

       7
     10                                                           perature simulated by standard Monte Carlo, T = 0.29
                                                                  the relaxation time is reduced by a factor of about 102




                             Stan
                                                                  when swap moves are introduced. Following the evolu-
       6




                              dard
     10                                                           tion of τα using swap moves, we find however that τα be-
                                                                  comes too large to be accurately measured for T ≤ 0.24
                     Sw
                                                                  and particles in fact barely move over the entire simu-
                       ap
       5
                                                                  lation performed at T = 0.22. We conclude therefore
τα




     10
                                                                  that our swap Monte Carlo simulations fail to thermalize
                                                                  the model for T ≤ 0.24. In Ref. [51], thermalization
       4
     10                                                           was tested by reweighting the probability distribution
                                                                  functions of the potential energy. We could reproduce
                                                                  this thermalization test in our work, thus demonstrat-
          3
     10                                                           ing that this test fails to detect the lack of thermaliza-
      0.22    0.26          0.3      0.34   0.38   0.42   0.46    tion and proper sampling for the lowest studied temper-
                                        T
                                                                  atures. Measuring the structural relaxation time and the
FIG. 6. Relaxation times τα of standard (black empty              relaxation dynamics is thus a more accurate and more
points) and swap (red full squares) simulations for the ternary   discriminating thermalization test than techniques based
mixture of soft repulsive spheres studied in Sec. III B. The      on global static observables only.
speedup offered by the swap moves is obvious, but the sys-           In addition to the lack of thermalization at low temper-
tem is unstable below T = 0.26 ≈ 0.9TM CT where it demixes        atures, we also find signatures of structural instability of
and crystallizes. Disconnected squares are a rough estimate       the fluid at even higher temperatures, T ≤ 0.26. Below
of τα obtained using short simulations in the unstable re-        this temperature, our criteria for absence of crystalliza-
gion. Stable and equilibrated states can be accessed down to
                                                                  tion or demixing are no longer fulfilled, and the system
T ≈ 0.26 < TM CT = 0.288, extending the dynamic range by
about 2 orders of magnitude as compared to standard simu-
                                                                  is eventually unstable within the window of 200τα that
lations.                                                          we use to assess stability. Using shorter time windows
                                                                  before the system crystallizes, we obtain a rough esti-
                                                                  mate of the relaxation time τα in the unstable regime,
responding size polydispersity is δ ≈ 17%, and so we              and show these results as disconnected squares in Fig. 6.
can expect a smaller tendency for the system to crystal-          In Ref. [51], the glass-forming ability of the model was
lize. Simultaneously, we also expect the acceptance of            not discussed but there may be evidence of ordering in
the swap moves to be much smaller than for the binary             the reported peak of the specific heat. An alternative
mixture. In agreement with Ref. [51], we find that the            reason for the absence of ordering in the data of Ref. [51]
acceptance rate for swaps is of the order a ∼ 10−5 at low         is that the performed simulations covered a smaller time
temperatures. To speed up the simulations, we therefore           window of about 106 − 107 Monte Carlo sweeps, whereas
only attempt swap moves between species (A, B) and                we simulate up to 109 sweeps in our work. Of course, pre-
(B, C) separately, because the probability of accepting           venting ordering through shorter simulations implies that
swaps between pairs of (A, C) particles is negligible.            thermalization becomes more difficult to achieve, and an
   Despite the low acceptance rate, it was claimed in             accurate sampling of phase space is then problematic.
Ref. [51] that swap moves allow for a dramatic speedup               Comparing the stable results for the ternary mixture
of the thermalization in this model. In the reduced units         to the ones of the binary mixture in Fig. 5, it is clear
described above, we locate the mode-coupling crossover            that the efficiency of swap Monte Carlo is essentially pre-
temperature near TMCT ≈ 0.288, and Gutierrez et al.               served, and that thermalization and metastability of the
claim to have achieved thermalization down to T =                 fluid branch have indeed been extended to temperatures
0.22 ≈ 0.76TMCT . Based on dynamic scaling arguments,             below TMCT , although the gain is far less spectacular
they estimate that the relaxation time at T = 0.22 is             than the one claimed in Ref. [51], once thermalization
τα /τ0 ≈ 1015 , where τ0 is the value of the relaxation           and structural stability are more precisely characterized.
time near the onset temperature T0 . Thus, the claim is              We studied more carefully the structural properties
that swap Monte Carlo provides an increase in the ac-             of the ternary mixture using partial structure factors,
cessible window of relaxation times of about 10 orders of         and we show some representative results in Fig. 7 for
magnitude as compared to standard molecular dynamics              SCC (k) at various temperatures. At high temperatures,
simulations [51].                                                 T > 0.30, we find that the structure factor resem-
   We have repeated and extended these simulations us-            bles the one found for ordinary glass-forming models,
ing standard and swap Monte Carlo dynamics. In Fig. 6             with a strong first diffraction peak corresponding to the
we present the temperature evolution of the structural            inter-particle distance and a featureless plateau at lower
relaxation times for both these dynamics. We confirm              wavevectors. In the low-temperature regime, where swap
that despite the very low acceptance rate of the swap             Monte Carlo is mandatory to achieve thermalization,
moves, the speedup of the dynamics produced by these              0.26 < T ≤ 0.29 ≈ TMCT , we find that SCC (k) increases
rare swaps is important. For instance, at the lowest tem-         more strongly as k decreases towards 0, which suggests
                                                                                                                          11

            20                                                      Therefore, we confirm that the ternary mixture intro-
                       T=0.350                                    duced in Ref. [51] can be equilibrated at temperatures be-
                         0.267
                         0.267                                    low the mode-coupling crossover and we have estimated
            15           0.256                                    that this corresponds to an extension of the accessible dy-
                                                                  namic regime of about two decades compared to standard
   SCC(q)


                                                                  simulations. This achievement thus competes favorably
            10                                                    with the other computational approaches described in
                                                                  the introduction, but it still does not allow for an explo-
                                                                  ration of glass physics much closer to the experimental
             5                                                    glass transition, which we shall achieve below for contin-
                                                                  uous polydispersity.

             0
                   1                               10
                                   q                                           C.   Five-component mixtures


FIG. 7. Partial structure factor SCC (q) for small particles         Because ternary mixtures offered only limited success,
in the ternary mixture of Sec. III B. It is featureless at high   we tried to improve both swap move acceptance and the
enough temperatures, T = 0.350, displays strong composition       metastability of the liquid phase by performing an ex-
fluctuations at low k in the fluid at T = 0.267, that may even-   ploratory study using two different five-component mix-
tually lead to a demixed state at long times. For T ≤ 0.26,       tures. We again adjusted the concentration of the vari-
the system is demixed, as shown for T = 0.256. The inset          ous species so that each component roughly occupies the
shows a representative snapshot of a demixed and partially        same volume, and we chose the size ratio between the dif-
crystallized system at T = 0.256.
                                                                  ferent families to be small enough that swap moves are
                                                                  accepted with a reasonable acceptance rate.
                                                                     We studied two systems with diameters roughly lin-
that composition fluctuations are already quite strong            early spaced between σmin = 0.847 and σmax = 1.333
in this regime. Even for these state points, which we             for a polydispersity δ = 16%, and between σmin = 0.826
deemed “stable” based on our stability criterion, longer          and σmax = 1.771 for a polydispersity δ = 23%, Thanks
simulations show that these fluctuations can trigger a            to the reduced size ratio between individual components,
demixing in the system, as illustrated for T = 0.267 in           the swap acceptance rate increased considerably as com-
Fig. 7. We have obtained similarly demixed configura-             pared to the binary and ternary mixtures studied above,
tions for temperatures up to T = 0.27, showing that sta-          and ranges between a ≈ 10% and a ≈ 20% depending on
bility is a real issue in this model. Finally, for T ≤ 0.26,      temperature. However, both models displayed a strong
the system always demixes within our simulation time,             tendency to demix during swap Monte Carlo simulations
which produces a strong low-k peak in the structure fac-          and it proved impossible to equilibrate these systems well
tor, see Fig. 7. When the particles are segregated, they          below TMCT following the criteria described above.
then easily crystallize and we obtain configurations such            We have clearly not exhausted all possible discrete
as the ones shown in the inset of Fig. 7. We conclude             models of glass-formers, as the parameter space becomes
that maintaining this system in metastable fluid state at         very large when the number of components increases. It
low temperatures, T ≤ 0.26 ≈ 0.9TMCT , is actually very           is possible that some parameter combination provides
difficult because (i) thermalization becomes prohibitively        both a rapid thermalization and a good glass-forming
difficult and (ii) simulations longer than the thermaliza-        ability, and more work would be needed to explore this
tion time in this regime produce demixed and ordered              hypothesis in a more systematic manner, as done for in-
configurations.                                                   stance in the context of simplified models of bulk metallic
   Finally, to assess more quantitatively the gain in effi-       glasses [70].
ciency obtained for this ternary mixture, we have fitted
our dynamic relaxation data from standard Monte Carlo
simulations to various fitting formula commonly used                   IV.     CONTINUOUSLY POLYDISPERSE
                                                                                      SYSTEMS
in the glass literature. Using both a Vogel-Fulcher fit,
Eq. (13), which presumably overestimates the data at low
T , and a parabolic singularity-free formula, Eq. (14), we                A.    Why continuous polydispersity?
consistently obtain that the relaxation time at T = 0.26
is about τα ≈ 109 . This is two orders of magnitude slower          The difficulties highlighted in the previous sections
than the lowest temperature simulated without the swap            arise from the interplay of several competing effects.
moves, see Fig. 6. At this low temperature T = 0.26,              Reducing the diameter difference between species im-
the relaxation time using swap is τα ≈ 5 · 105 and so the         proves the acceptance of swap moves, and thus accel-
thermalization speedup due to swap moves is about three           erates thermalization, but the resulting reduced polydis-
orders of magnitude.                                              persity makes the system prone to crystallization. Addi-
                                                                                                                            12

                                                                      7
tionally, we found that simple multi-component mixtures             10
show an important tendency to demixing at low temper-                                                            n=8
ature.                                                                                                             12
                                                                      6                                            18
   To tackle these issues at once, we considered a class            10                                             24
of models characterized by a continuous particle size dis-
tribution P (σ). In such systems, swap moves are more                 5
                                                                    10
likely to be accepted, because there always exist pairs of




                                                               τα
particles whose diameters are sufficiently close to one an-
other. We found that the succession of a large number of            10
                                                                      4

successful swaps between pairs with similar diameters ac-
tually facilitates the thermalization of the system. Phys-
                                                                         3
ically, the end result is that the diameter of each particle        10
performs a kind of random walk in diameter space. An
efficient exploration of the diameter distribution seems             0.4         0.8         1.2         1.6            2
to be the key for efficient thermalization, as discussed                                      T/TMCT
further below in Sec. V.
   In addition, by choosing a sufficiently high degree of      FIG. 8. Relaxation times for continuously polydisperse sys-
polydispersity it may be possible to stabilize the liquid      tems of repulsive soft spheres with different softness exponents
against crystallization and fractionation. Therefore, well-    n = 8, 12, 18 and 24. Temperatures are scaled by TM CT to
                                                               allow direct comparison between models, with TM CT = 0.143,
chosen continuous particle size distributions seem able
                                                               0.267, 0.468, 0.662, respectively. Open symbols represent the
to solve all problems encountered in Sec. III above for        standard Monte Carlo dynamics, closed symbols the swap
discrete mixtures at once.                                     algorithm, for which unconnected symbols represent struc-
   In this section, we study models in which particles in-     turally unstable state points where only a rough estimate of
teract via Eq. (5), with the cutoff function F (rij ) given    τα is obtained in short simulations. A larger n yields better
by Eq. (6) and a cut-off distance rcut = 1.25σij . We          efficiency and better structural stability.
simulate N = 1500 particles at ρ = 1. We also fix
the particle size distribution to be of the form given by
Eq. (2) and vary parameters such as the pair potential            In Fig. 8 we show the structural relaxation times as
and its additivity. This particle size distribution is con-    a function of the temperature for different softness ex-
trolled by a unique parameter, the size ratio σmax /σmin       ponents obtained from both standard and swap Monte
or, equivalently, the size polydispersity δ. Using insight     Carlo simulations. Temperatures are scaled by the cor-
from preliminary studies on hard sphere systems [52], we       responding mode-coupling temperature TMCT of each
fix σmax /σmin = 2.219 which implies δ ≈ 23%. This             model, so that different systems can be represented in
observation is in qualitative agreement with the earlier       the same graph. In all these systems swap moves speed
results of Fernandez et al. [44], who simulated repulsive      up thermalization significantly. As the exponent n in-
spheres with a flat size dispersion and found an optimal       creases, i.e. as repulsive forces get steeper, it becomes
stability for polydispersities in the interval 20%−30%. In     possible to equilibrate the system at increasingly lower
these models, the acceptance of swap moves is typically        temperatures relative to TMCT .
very high, a ∼ 20%-30%, and does not change dramati-              In addition, as for discrete mixtures, the models pre-
cally with temperature.                                        sented in this section also have a tendency to demix at
                                                               low temperatures. We have again carefully checked the
                                                               low-k behavior of the partial structure factors that in-
        B.    Influence of the particle softness               forms us about the presence of large composition fluc-
                                                               tuations. Despite the improved stability, we found that
   Our first analysis of models with continuous polydis-       the system may still demix at low enough temperatures
persity concerns the role of the particle softness. Pre-       during the swap Monte Carlo simulations. For these un-
vious studies have found that softness can have a non-         stable state points, we again use shorter simulations to
trivial impact on glass properties, such as fragility [71]     obtain a rough estimate of the relaxation time, and we
and glass-forming ability [57]. Here we simulated poly-        show these data using disconnected symbols in Fig. 8.
disperse soft particles varying the softness exponent n        Regarding the structural stability of the models, there is
using the values n = 8, 12, 18, 24. We focus on a con-         again a clear trend with the softness exponent n. We find
tinuously polydisperse model with additive interactions,       that softer systems are more prone to structural instabil-
ǫ = 0. In the limit where n → ∞, the model becomes es-         ity than harder ones. We emphasize that this result is
sentially equivalent to the hard sphere model studied in       most likely system-specific, since the opposite trend was
Ref. [52], which displays excellent stability and efficient    found in other models of glass-formers [57, 72].
thermalization. Therefore, the present family of mod-             Combining the effect of a more efficient thermaliza-
els appears as the natural extension of these hard sphere      tion and a better stability of the fluid state, we conclude
results to soft potentials.                                    that models with larger n values represent the best choice
                                                                                                                           13

      7
     10                                                          ous section, we scale the temperatures by the measured
                                                ε=0.0            TMCT for each model. For comparison, we also redraw
                                                  0.1
                                                  0.2            the results for the additive system (ǫ = 0) with n = 12.
      6                                           0.3
     10                                                          Regarding thermalization efficiency, we find that non-
                                                                 additivity improves the performance of the swap algo-
      5                                                          rithm, as lower temperatures relative to TMCT can be
     10
τα




                                                                 studied when ǫ > 0, but it is not easy to provide a de-
                                                                 tailed physical understanding of this result.
      4
     10                                                             Analysis of the low-k behavior of the partial structure
                                                                 factors Sαα (k) shows that phase separation is strongly
          3
                                                                 suppressed by the non-additivity for both ǫ = 0.1 and
     10                                                          0.2. At low temperature, however, the system can crys-
      0.4          0.8       1.2         1.6            2
                                                                 tallize, as detected from drops in the time series of the en-
                              T/TMCT                             ergy and from the appearance of well defined peaks in the
                                                                 structure factor, and we could frequently observe these
                                                                 crystallization events for ǫ = 0.2 and 0.3. For ǫ = 0.1, the
FIG. 9. Relaxation times for systems with continuous poly-
dispersity, n = 12 and different non-additivity parameter ǫ.     liquid remained stable down to the lowest temperature we
Temperatures are scaled by TM CT to allow direct compari-        could equilibrate with the swap Monte Carlo. This is in
son between models, with TM CT = 0.267, 0.176, 0.104, and        fact the only model among the eleven ones studied in this
0.0534, respectively. Open symbols represent the standard        paper that perfectly fulfilled our equilibration and stabil-
Monte Carlo dynamics, closed symbols the swap algorithm,         ity criteria throughout the entire accessible temperature
for which unconnected symbols represent structurally unsta-      range.
ble state points where only a rough estimate of τα is obtained      The existence of an optimal non-additivity parameter ǫ
in short simulations. A well-chosen amount of non-additivity,    for glass-forming ability presumably results from a com-
ǫ ≈ 0.1-0.2, considerably improves the efficiency of thermal-
                                                                 petition between demixing, which takes place when ǫ = 0,
ization and the structural stability.
                                                                 and crystallization, for large ǫ. We suggest that the ex-
                                                                 istence of these two distinct paths to ordering actually
                                                                 compete for ǫ = 0.1-0.2, which results in an enhanced
of parameter within the present family, the system with          frustration and thus a higher structural stability. Simi-
n = 24 being stable and efficiently thermalized down to          lar physical arguments have been proposed in Ref. [70] to
T ≈ 0.6TMCT , see Fig. 8. The trend that we find sug-            explain glass-forming ability of simple non-additive mix-
gests that a system of polydisperse hard spheres with            tures.
n = ∞, such as the one recently simulated in Ref. [52],             Whereas the additive model with n = 12 was not the
might actually prove the best glass-former in this class         best choice of softness in the previous section, we find
of systems with continuous polydispersity, repulsive in-         that including non-additivity significantly improves both
teractions, and additive interactions.                           the efficiency of the swap algorithm and the structural
                                                                 stability of this model. We suggest that models with
                                                                 larger n (including hard spheres) with non-additive di-
              C.   Non-additive interactions                     ameters would be even better choices.
                                                                    It is interesting to contrast the results for the n = 12
  To suppress the tendency to demixing while preserv-            soft repulsion using a continuous size distribution and a
ing a continuous form of polydispersity, we have intro-          non-additivity ǫ = 0.1 to the results obtained for the bi-
duced non-additivity in the potential by modifying the           nary mixture in Sec. III A for the same pair potential.
sum rule for particle diameters, as described in Eq. (8).        The conclusion is that the thermalization and stability
Non-additive interactions are known to stabilize the liq-        limits have been decreased from T ≈ TMCT for the bi-
uid in metallic alloys [57, 58]. Moreover, this effect           nary mixture down to T ≈ 0.5TMCT for the present sys-
has been demonstrated explicitly in non-additive hard-           tem. This represents a major methodological improve-
spheres [73, 74]. Physically, choosing ǫ > 0 frustrates          ment that we try to quantify in terms of timescales in
phase separation, because particles of different diameters       the next subsection.
can now stay closer to one another than in the additive
case with ǫ = 0. To study the effect of non-additivity,
we set the softness exponent to n = 12 and we vary ǫ                 D.   Experimental timescales are matched by
using ǫ = 0.0, 0.1, 0.2 and 0.3. Note that some results                              simulations
for the case ǫ = 0.2 have been already presented in Sec. II
above, when discussing the details of the swap algorithm           In the previous section, we showed that by optimizing
and the thermalization checks.                                   the additivity and the form of the pair potential, tem-
  Figure 9 shows the structural relaxation times obtained        peratures as low as T ≈ 0.5TMCT could be thermalized
by varying the degree of non-additivity. As in the previ-        using swap Monte Carlo in the metastable fluid state.
                                                                                                                                                                           14

                                                                         7
Because ordinary simulations stop near T ≈ TMCT , one               10
may wonder how large is the corresponding gain in terms                      (a)




                                                                                                 rd
of structural relaxation times. It is relatively easy to an-




                                                                                              nda
                                                                         6
                                                                    10
swer this question when the improvement is modest, but




                                                                                             Sta
this becomes a delicate task in our case, as thermalization
                                                                         5
is achieved in a temperature regime where the standard              10
dynamics is completely frozen in our observation window




                                                               τα
and where equilibrium timescales can only be obtained                                                            ap
                                                                    10
                                                                         4                                  Sw
by extrapolation. Extrapolating timescales down to the




                                                                                                                                                     Arrhenius
                                                                                                                                   Parabolic
lowest temperatures where the swap Monte Carlo can                       3
thermalize may depend sensitively of the fitting proce-             10




                                                                                                                      VFT
dure and it therefore requires some care.
                                                                         2
   We have devised a robust strategy which answers for              10 2           4   6     8         10             12                 14          16             18
each model the following question: Is the thermaliza-                                                   1/T
tion speedup due to the swap Monte Carlo algorithm                   7
                                                                    10       (b)
large enough to fill the eight-decade gap between ordi-
nary simulations and experiments? To answer this ques-               6
tion for a given model, we employ ordinary Monte Carlo              10
simulations to access a range of relaxation time up to
τα /τ0 ≈ 104 , where τ0 represents the value of τα at the            5
                                                                    10




                                                               τα
onset of glassy dynamics. In experiments [5], the glass
temperature Tg corresponds to the value τα /τ0 ≈ 1012 ,              4
                                                                    10
                                                                                                                                                                 n=8
                                                                                                                                                                   12
which we will take as our practical definition of Tg . Us-                                                                                                         18




                                                                                                                       Parabolic
ing the various functional forms described in Sec. II B, we                                                                                                        24




                                                                                                        Tg+∆Tg




                                                                                                                                           Tg-∆Tg
                                                                    10
                                                                         3                                                                                       ε=0.1
realized that estimating the location of Tg from numeri-                                                                                                           0.2
                                                                                                                                                                   0.3
cal measurements of τα is actually possible with modest
                                                                     2
uncertainty. More precisely, for a given model we use all           10       0.4       0.6            0.8                     1                     1.2                  1.4
three functional forms in Eqs. (13, 14, 15) to estimate the                                            Tg/T
location of Tg from the definition τα (Tg )/τ0 = 1012 . De-
spite the qualitative differences between these functional     FIG. 10. (a) Relaxation times for the non-additive model
forms, the range of Tg values is reasonably small, typi-       with n = 12 and ǫ = 0.2 for standard and swap Monte Carlo
cally ∆Tg /Tg = (TgVFT −TgArrhenius)/(2Tgparabolic) ≈ 12%,     dynamics. The standard dynamics is fitted with the VFT,
with minor variations from one model to the other. Be-         parabolic and Arrhenius laws, as shown with lines, which are
cause the VFT law tends to overestimate the increase τα        used to estimate the location of the experimental glass tem-
and the Arrhenius law underestimates it, these two forms       perature Tg , as shown with vertical dashed lines. For this
respectively provide an upper and a lower bound to the         system, the swap dynamics is able to provide stable and ther-
real location of Tg , while estimates from the parabolic       malized configurations at temperature below Tg . (b) Relax-
law usually fall between those two bounds. Elmatad et          ation times obtained from standard (open symbols) and swap
al. [63] have shown that the parabolic law accounts for        (filled symbols) dynamics for various size polydisperse mod-
                                                               els of various softness (n) and non-additivity (ǫ) are shown
the variation of relaxation times of glass-forming liquids
                                                               in an Arrhenius form with rescaled temperature Tg /T , where
over a broad range of temperatures, ranging from the on-       Tg is estimated as in (a). For all models the thermalization
set down to the laboratory glass transition. We therefore      speedup near Tg is of about 10 orders of magnitude, some
expect our parabolic extrapolation to provide a reason-        models being structurally stable down to temperatures below
able determination of Tg , and the other two temperatures      Tg .
to provide a solid estimate of the interval of confidence.
   We illustrate this procedure in Fig. 10(a) where we
show the temperature evolution of τα (T ) from standard        maintained metastable at temperatures even below the
Monte Carlo dynamics for the non-additive model stud-          experimental glass temperature Tg . This finding has sev-
ied in Sec. IV C, using an Arrhenius representation. We        eral important consequences.
fit these Monte Carlo dynamic data and estimate three             • The speedup of the thermalization at Tg is of about
different locations for Tg , which delimit the range of pos-        10 (±1) orders of magnitude, implying that com-
sible values for the location of Tg , highlighted with the          puter simulations can now comfortably study that
vertical dashed lines. We then show the evolution of the            temperature regime in thermal equilibrium.
relaxation time for metastable fluid states when swap
Monte Carlo moves are used in the same Arrhenius rep-             • The maximal speedup obtained with the swap
resentation. We find that the swap relaxation time re-              Monte Carlo is in fact much larger than these 10
mains modest in the vicinity of Tg , τα /τ0 ≈ 102 − 103             orders of magnitude, because temperatures lower
and that this particular system can be thermalized and              than Tg can be thermalized, but estimating that
                                                                                                                          15

      gain becomes very sensitive to the chosen extrapo-                1.5




                                                                σ(t)
      lation.
                                                                          1
   • For selected models we can now access a temper-
                                                                          3
     ature regime that even experiments cannot reach,




                                                                ∆r(t)
                                                                          2
     thus opening a novel observational window on the
                                                                          1
     physics of glasses in a regime that has never been
                                                                          0
     probed before, either experimentally or numeri-                    1.5
     cally.




                                                                σ(t)
                                                                          1
   To quantify the performance of the swap algorithm, we
estimate the range of Tg values for each model studied in                3




                                                                ∆r(t)
this section, and use these fitted values to construct an                2
Angell plot, representing the logarithm of the relaxation                1
times as a function of the scaled inverse temperature,                   0
                                                                          0    0.5        1          1.5       2        2.5
Tg /T , see Fig. 10(b). In practice, we use the value given                                   t/τα
by the parabolic which falls in the middle of the fitted
range and show the corresponding uncertainty, estimated        FIG. 11. Time-series of individual displacement ∆r(t) and di-
from VFT and Arrhenius fits, with the vertical dashed          ameter value σ(t) for two tagged particles in the non-additive
lines in Fig. 10(b). Standard Monte Carlo simulations          model of Sec. IV C with ǫ = 0.2 at T = 0.0555. Intermittent
typically stop near T /Tg ≈ 1.3-1.5, in the vicinity of the    diffusion in real and diameter space is observed, with strong
mode-coupling crossover. For most models, the swap al-         correlations between ∆r(t) and σ(t) highlighted with dashed
gorithm performs so well that the thermalization time at       lines, but we also observe many events in one observable that
Tg remains modest, τα /τ0 ≈ 102 . This corresponds to a        have no counterpart in the other indicating that the correla-
                                                               tion between the two observables is non-local.
thermalization speedup at Tg of 10 orders of magnitude.
As mentioned before, models with soft potentials and ad-
ditive interactions are prone to structural instability, and
                                                               a position where another particle was caged too. There-
some of them are not stable down to T = Tg . However
                                                               fore, it is not clear that the cage is affected at all after a
for several models, we find that thermalization and fluid
                                                               swap move, and this simple explanation cannot explain
metastability can be maintained below Tg .
                                                               the speedup of the dynamics.
   The discovery of such glass-forming models associated
                                                                  This conclusion is more easily grasped when one con-
to an efficient algorithm to thermalize them represents
                                                               siders, as we do, that particles simply exchange their di-
the main achievement of our work.
                                                               ameters during a swap move, without changing position.
                                                               In that case, the diameter of each caged particle slowly
                                                               fluctuates in time. For continuous polydisperse systems,
    V.   MICROSCOPIC INSIGHTS INTO THE                         these time fluctuations take the form of a random walk in
              SWAP DYNAMICS
                                                               diameter space. Therefore, we conclude that it is rather
                                                               the slow wandering of the diameter of each particle that
         A.   Dynamics of particle diameters                   allows the system to relax more efficiently towards equi-
                                                               librium. A naive physical explanation would be that a
   The previous sections demonstrated that swap Monte          caged particle with a large diameter could start diffusing
Carlo moves can enhance thermalization by several or-          by shrinking its radius, thus being able to squeeze and
ders of magnitude, the effect being most spectacular in        escape through a small channel. We shall now demon-
continuously polydisperse systems, for which swap moves        strate that the physics is actually more complicated and
have a very high acceptance rate. In this section we shed      more collective than this naive image.
some light on the microscopic mechanisms that are re-             To see this, let us start with some qualitative observa-
sponsible for this acceleration. We carry out this anal-       tions on the time evolution of the diameter of a tagged
ysis for a non-additive polydisperse model with ǫ = 0.2        particle. We show two typical time series of σi (t) for
introduced in Sec. IV C.                                       two different particles in Fig. 11. We rescale the time
   It has been previously suggested that the swap moves        axis by τα to better appreciate how much the particle di-
increase the particle mobility because they allow the par-     ameter changes over a relaxation time of the system. On
ticles to escape the cage formed by their neighbors [38, 51]   short time scales the diameter fluctuates around its initial
after a non-local swap move. This view seems correct           value, while at longer times it changes and eventually vis-
when one considers that particles exchange their posi-         its all values allowed by the particle size distribution. At
tions, because a caged particle indeed appears to jump in-     low temperature these relaxation events occur suddenly
stantaneously to a novel position. However, the swapped        and appear as jumps. Overall, this behavior strongly re-
particle is actually replaced by another particle which is     sembles the typical features of glassy dynamics known
then occupying the caged position itself, and it jumps to      from real space analysis of single particle displacements,
                                                                                                                                                               16

                             1                                                                  sition dynamics, we define a time correlation associated
                                                                                                to the time evolution of the diameters. We define the
                     0.8                                                                        following auto-correlation function for diameter fluctua-
                                                                                                tions:
                     0.6
 Cσ(τ)




                                                                                                                               P                     
                                                                                                                                     δσi (t)δσi (0)
                                                                                                                                    iP
                     0.4                                                                                 Cσ (t) = hcσ (t)i =               2              ,   (17)
                                                                                                                                       i δσi (0)

                     0.2
                                    (a)
                                                                                                where δσi (t) = σi (t) − hσi. This function is normalized
                             0 0          1      2    3        4    5     6         7      8
                                                                                                so that it evolves from unity when t = 0, to zero at large
                             10      10        10    10   10       10   10       10      10     times when diameters become completely uncorrelated
                                                            t
                     7                                                                          from their initial values. The temperature variation of
                    10
                                                                                                this function is shown in Fig.12(a). By lowering the tem-
                                                                             τα
                                                                                                perature Cσ (t) develops a plateau after an initial short
                     6
                    10                                                       τσ/τα(To)          time decay and eventually decorrelates at longer times.
 Relaxation times




                                                                             τo/τα(To)          This confirms the previous qualitative observations that
                                                                                                the diameters remain “caged” around some initial value
                     5
                    10                                                                          before complete decorrelation.

                     4
                                                                                                   Let us define the diameter decorrelation times τσ as
                    10                                                                          the value of time such that Cσ (τσ ) = e−1 . In Fig. 12(b),
                                                                                                we compare the temperature evolution of three different
                         3
                                   (b)                                                          relaxation times for single-particle motion, τα , for single-
                    10
                                                                                                particle diameter, τσ , and for collective density fluctua-
                     0.04                     0.08        0.12          0.16              0.2   tions, τo . We absorb the observable dependence of these
                                                           T                                    three timescales by rescaling them at a single tempera-
                                                                                                ture where the relaxation is fast, namely T = 0.175. The
FIG. 12. Non-additive model of Sec. IV C with ǫ = 0.2. (a)                                      striking result of these measurements is that single parti-
Time auto-correlation of particle diameters Cσ (t) measured                                     cle displacements, density fluctuations and diameter fluc-
during the swap dynamics for temperatures as in Fig. 4. (b)                                     tuations all relax on the same timescale. Because diffu-
Relaxation times τα , τσ and τo as a function of temperature,                                   sion is fully arrested when the diameters do not fluctuate
with τσ and τo rescaled to coincide with τα at T = 0.175                                        we conclude that it is the efficient dynamics in diameter
(shown with horizontal bar). The three timescales obviously
                                                                                                space which drives the structural relaxation in position
have the same temperature dependence.
                                                                                                space, and therefore, the efficient thermalization of the
                                                                                                system.
mimicking very much the cage effect and hopping mo-                                                A further intriguing observation about the role of di-
tion. To reinforce this analogy, we show the time series                                        ameter fluctuations stems from the data shown in Fig. 4,
of the particle displacements for the same two tagged                                           where time correlation functions for standard and swap
particles in Fig. 11. As expected, they display periods of                                      dynamics are compared at the same very low temper-
immobility separated by rapid jumps.                                                            ature, where even the swap dynamics is very slow. In
   The comparison of the two panels reveals that some                                           that case one observes that the plateau height related
of the sudden jumps in diameter space occur at similar                                          to short-time vibrational motion is different in the two
times as the sudden jumps of the particle in real space                                         dynamics, the amplitude of these vibrations being much
which indicates that diameter dynamics can trigger dif-                                         larger when the swap dynamics is used. This observa-
fusion. However, we can also detect jumps occurring in                                          tion implies that at short times the small fluctuations
real space without clear counterparts in diameter space,                                        in particle diameters act as an additional degree of free-
and vice versa. These observations suggest that changing                                        dom that allows each particle to perform back and forth
the diameter of a single particle is not necessarily enough                                     caged motion over a typical distance that is larger than
to trigger a rearrangement, and also that changes in the                                        in the standard dynamics. These larger in-cage fluctua-
neighborhood of one particle may be enough to trigger a                                         tions suggest a possible “softening” of local cages, which
displacement. Overall, the physical picture is that relax-                                      seems to correlate well with an acceleration of the dy-
ation in these supercooled states is a collective process                                       namics. Such a correlation between short-time motion
and the efficient thermalization with swap cannot be ex-                                        and structural relaxation is often discussed in the con-
plained on the basis of a simple single-particle argument.                                      text of glass-forming models [75–78], and it would be
   To quantify the correlation between diameter and po-                                         interesting to study it further in the present context.
                                                                                                                                     17

                                                                                                                ∗
                                                                               τα Standard                   χ 4(t) Standard    12
                                                                      7
                                                                   10          τα Swap                          ∗
                                                                                                             χ 4(t) Swap
                                                                                                                σ∗
                                                                                                             χ    4
                                                                                                                    (t)         10
                                                                      6
                                                                   10
                                                                                                                                8

                                                                      5
                                                                   10                                                           6

                                                                      4                                                         4
                                                                   10
                                                                                                                                2
FIG. 13. Snapshots of the 10% of particles with (a) the largest         3
displacements (b) the largest diameter change, computed be-        10
                                                                                                                                 0
tween times t = 0 and t = τα /2 for T = 0.0555. There is a           0.05                0.1             0.15                  0.2
clear correlation between the spatial regions where dynamics                                      T
in real and diameter spaces are fast, but the correlation is
weak at the single-particle level.                                FIG. 14. Temperature evolution of dynamic susceptibili-
                                                                  ties (right axis) and relaxation times (left axis), the vertical
                                                                  dashed line is TM CT = 0.104. Whereas χd4 (t) grows together
        B.    Spatially heterogeneous dynamics                    with τα in standard simulations, χd4 (t) and χσ4 (t) behave simi-
                                                                  larly and have a very different temperature dependence which
                                                                  mirrors instead the evolution of the swap relaxation time.
   The correspondence between the timescales for diam-
eter and position dynamics, accompanied by a lack of
strong correlation at the single particle level, suggests
that the physics of diffusion in real and diameter space          particle displacements and of diameter changes, and they
is cooperative in nature. For instance, diffusive events          typically display a peak around the timescales τα and τσ ,
could be happening more easily in a spatial region where          respectively. In Fig. 14 we report the height of these two
the diameter dynamics has been particularly efficient.            peaks, χd∗        σ∗
                                                                            4 and χ4 , as a function of the temperature. In
This hypothesis suggests to investigate the existence of          addition we also measure and report the behavior of χd∗  4
spatial correlations of the dynamical relaxations.                for the standard Monte Carlo dynamics.
   To illustrate this point qualitatively, we show in Fig. 13        This figure provides two main pieces of information.
two typical configurations at a temperature T = 0.0555.           First, we notice that the temperature dependence of
We measure the dynamics between an arbitrary initial              χd∗
                                                                    4 in standard and swap simulations are very differ-
time t = 0 and a later time t = τα (T )/2. In Fig. 13(a) we       ent. The behavior for standard Monte Carlo is as re-
show the particles having the 10% largest displacements           ported before [80], where χd∗ 4 increases rapidly from a
in real space over this time lag, whereas in Fig. 13(b) we        value χd∗
                                                                          4  ≈  1 when  the temperature   is decreased below
show the particles having the 10% largest displacements           the onset To ≈ 0.18 to a value χd∗4  ≈ 12  when approach-
in diameter space. Particles are drawn using rescaled             ing TMCT , in way that mirrors the evolution of the re-
final diameter values. We observe a close similarity be-          laxation time τα , as demonstrated in Fig. 14. The tradi-
tween regions of faster diffusing particles and regions of        tional interpretation is that dynamics becomes spatially
particles with large diameter changes, but we also rec-           correlated over larger length-scales as the temperature is
ognize that the correlation does not hold at the parti-           lowered. A striking observation is that the swap dynam-
cle level. Thus, we conclude that diameter changes and            ics near TMCT displays essentially no spatial dynamic
structural relaxation may affect each other in a non-local        correlations. By construction, swap moves can affect the
fashion.                                                          dynamics of the system but not its equilibrium static
   The spatial correlations of diameter fluctuations can be       properties. Therefore, we conclude that the growth of
characterized using the multi-point functions introduced          the spatial correlations detected by χd∗ 4 for T > TMCT
to study cooperative motion in supercooled liquids [79].          in standard dynamics is mostly of dynamic, rather than
The generic expression of the dynamical susceptibility            structural, origin. This finding, which agrees qualita-
related to a time-dependent observable O(t) is                    tively with previous conclusions [81, 82], may also explain
                           2                2                    why the swap algorithm can be very efficient, because if
              χO
                                               
                4 (t) = N hO (t)i − hO(t)i       .       (18)
                                                                  spatial correlations had a strong structural component,
It quantifies the extent of spatial correlations associated       then a strong numerical acceleration would likely neces-
to the local observable O over a time scale t [79]. Here          sitate the introduction of a more collective algorithm.
we measure dynamic susceptibilities associated both to               The second key information from Fig. 14 is that both
the self-part of density fluctuations, χd4 (t) with O(t) =        quantities χd∗         σ∗
                                                                               4 and χ4 with swap dynamics are quan-
fs (k, t) [see Eq. (11)], and to diameter fluctuations, χσ4 (t)   titatively very close, which confirms that fluctuations
with O(t) = cσ (t) [see Eq. (17)]. These functions provide        in real and in diameter spaces are strongly correlated.
information on the spatially heterogeneous dynamics of            Even though the correlation is not strong at the local
                                                                                                                          18

                                                                    7
scale, diameters fluctuations display the same tempera-            10
ture evolution as dynamic heterogeneities. In addition,                                                       Repulsive
both quantities follow the growth of the swap relaxation            6
                                                                                                              LJ
time, the swap algorithm becoming slow at low enough               10
temperatures, at which important spatial correlations of
the diameter dynamics become needed to relax to system              5
                                                                   10
towards equilibrium.




                                                              τα
                                                                    4
                                                                   10
  VI.     IDEAS FOR THE FUTURE DESIGN OF
             GLASS-FORMING MODELS
                                                                        3
                                                                   10
   In this section, we build on the detailed level of un-
derstanding of the swap mechanism reached in the previ-                       0.8          1.2          1.6           2
                                                                                            T/TMCT
ous sections to propose novel directions and ideas to de-
sign new glass-forming models for which the swap Monte
Carlo approach could be very efficient.                       FIG. 15. Relaxation times for repulsive and Lennard-Jones
                                                              potentials with a hybrid particle size distribution. Tempera-
                                                              tures are scaled by TM CT to allow direct comparison between
                                                              models, with TM CT = 0.680 and 0.543 for repulsive and LJ
     A.    “Hybrid” models for binary mixtures                potentials, respectively. Open symbols represent the standard
                                                              Monte Carlo dynamics, closed symbols the swap algorithm,
   A large number of models studied in the past were          for which unconnected symbols represent structurally unsta-
based on discrete mixtures [58, 68, 83], as studied in        ble state points where only a rough estimate of τα is obtained
Sec. III. We concluded there that swap was not well-          in short simulations.
suited for binary mixtures because a large acceptance
rate for the swap seems incompatible with a good struc-
tural stability. We now show that it is possible to con-      scribed by Eq. (3) with the chosen parameters xA = 0.33,
struct models which have the characteristics of binary        xB = 0.34, xC = 0.33, σA = 0.76, σB = 1.23, σC = 1.00,
mixtures, reasonable stability, and can be efficiently sim-   bA = 0.04, bB = 0.04, bC = 0.26. The two-body poten-
ulated using the swap algorithm.                              tial is given by Eqs. (5, 6) with n = 12 and a cut-off
   Our idea is to introduce what we call a “hybrid” par-      distance of rcut = 1.25σij . We perform simulations with
ticle size distribution, as sketched in Fig. 1. These dis-    N = 1000 at ρ = 1.3. With these parameters, the poly-
tributions are composed of two main peaks which are a         dispersity is δ = 20%.
good representation of an A − B binary mixture. In or-           Results for the relaxation times are presented in
der to have a good glass-forming ability, we choose an        Fig. 15. As usual, we use disconnected points to represent
equal concentration of particles in these two peaks, and,     unstable state points for which short simulations are used
more importantly, we choose a size ratio which is large       to estimate τα . For this system again, we observe that
enough to avoid the crystallization observed otherwise.       equilibration is easily attainable for temperatures below
Because such a large size ratio implies that (A, B) swap      TMCT , and resistance to ordering is ensured down to rel-
moves are always rejected, we introduce a third specie in     atively low temperatures, T ≈ 0.75TMCT . However, at
the model, associated to a flat continuous distribution of    lower temperatures the system again present instabilities
particle sizes that connects smoothly the two main peaks      due to the tendency to phase separation that we observe
of the binary mixture. The main idea is that a parti-         through low-k values of the structure factor. Preliminary
cle belonging to one of the two main components can           results indicate that using non-additive interactions will
be swapped with particles belonging to the intermediate       most certainly stabilize the system down to even lower
third specie, and it can then slowly tunnel through to        temperatures, but the main goal of this section has nev-
reach the other specie. In other words, whereas a direct      ertheless been reached. We have indeed designed a model
particle exchange between A and B is unlikely, the addi-      which is structurally similar to an equimolar binary mix-
tion of the interpolating specie facilitates such exchanges   ture with size ratio 1.6, but that can be efficiently stud-
which can then happen via a large number of intermedi-        ied using the swap algorithm down to T = 0.75TMCT via
ate swaps which all have a large acceptance rate.             the introduction of a third, intermediate specie. Using
   In practice, we introduce two species (A, B) with flat     the same fitting procedure as above, we estimate that
continuous polydispersity around two average diameter         these low temperatures allow us to access a total dy-
values (σA , σB ) such that σB /σA = 1.6. We add a            namic range of about τα /τ0 ≈ 108 , so that the swap
third specie, C, with an average diameter value σC =          Monte Carlo method already allows the exploration of a
(σA + σB )/2, which continuously interpolates between         novel temperature regime corresponding to an increase in
small and large diameters. Each specie contains roughly       relaxation times of about 3-4 orders of magnitude as com-
1
3 of the particles.     The final size distribution is de-    pared to standard Monte Carlo simulations. It would be
                                                                                                                         19

interesting to study hybrid variants of discrete mixtures,       low temperatures. For some models, we have been able
in which the concentration of specie C is small enough           to thermalize the metastable fluid down to temperatures
to be considered as a small perturbation of the original         that are lower than the laboratory glass transition, which
model. Work in this direction is in progress.                    represents the current experimental limit for molecular
                                                                 liquids. Therefore, our paper not only fills the eight or-
                                                                 ders of magnitude gap between ordinary simulations and
            B.   Lennard-Jones interactions                      experimental work, but it actually goes beyond state-of-
                                                                 the-art experiments and demonstrates that both static
   Up to now, we have studied pair potentials describing         and short-time dynamical properties can now be studied
repulsive soft spheres with inverse power law repulsion          in computer simulations in a novel temperature regime.
of various softness. However, more realistic pair interac-       In addition to static quantities, by using thermalised con-
tions including attractive forces are often used in studies      figurations obtained with the swap method as initial con-
of supercooled liquids. Perhaps the most studied pair in-        ditions for trajectories generated without swap, we be-
teraction is the Lennard-Jones potential [58], which con-        lieve it is possible to substantially extend the dynamic
tains a soft power law repulsion with exponent n = 12,           window for structural relaxation, which may shed new
combined with a soft power law attraction with exponent          light on the glassy dynamics as well.
n = 6, see Eq. (7).                                                 Our achievements are summarized in Fig. 1, but
   In this final study, we test whether Lennard-Jones in-        throughout the article we have suggested several ways
teractions can also be efficiently studied using the swap        in which our approach could be extended to devise dif-
Monte Carlo algorithm. To this end, we start from the            ferent or more realistic models of glass-forming materials.
previous “hybrid” model studied in Sec. VI A and in-             We have also suggested ways in which the algorithm it-
clude a power law attraction. Because the potential is           self could be improved and described several paths that
now longer-ranged, we use a larger cutoff rcut = 2.5σij ,        remain to be explored in future work. We expect these
and shift the potential by the constant cLJ to ensure the        results to trigger a large research activity towards these
continuity of the potential at the cut-off. All other pa-        goals.
rameters are equal to the ones employed in the hybrid               Obtaining thermalized states in simple models of su-
repulsive model above in Sec. VI A.                              percooled liquids at temperatures comparable to the ex-
   We again perform a comparison of the standard and             perimental glass transition paves the way to a number
swap dynamics for this Lennard-Jones system, and                 of novel studies, because essentially all simulation work
present the results along the ones of the corresponding          published over the past 30 years could be performed
repulsive case in Fig. 15. We find that including attrac-        again over a previously inaccessible temperature regime.
tive forces modifies very little both dynamics, apart from       Some works along these lines have been already pub-
a rescaling of the temperature scale: the mode-coupling          lished [52, 53], and others are currently in progress re-
crossover temperature shifts from 0.680 to 0.543 when in-        garding the thermodynamic properties of deeply super-
cluding attractive forces [84]. As a result, the above con-      cooled liquids, their local structure, vibrational and me-
clusions regarding stability and thermalization efficiency       chanical properties, and the existence of a Gardner tran-
directly carry out to this Lennard-Jones system. Our             sition in soft glasses.
main conclusion is therefore that our “feasibility study”
is successful and that glass-forming models with Lennard-
Jones interactions and a binary-like size distribution can
be devised and studied down to very low temperatures us-                        ACKNOWLEDGMENTS
ing the swap algorithm. Such models will most certainly
prove useful in future studies of the glass transition.             We thank G. Biroli, R. Jack, M. Ozawa, I. Procac-
                                                                 cia, G. Tarjus, and M. Wyart for useful exchanges about
                                                                 this work. We thank R. Gutierrez for providing addi-
                 VII.   PERSPECTIVES                             tional information regarding simulations performed in
                                                                 Ref. [51]. The research leading to these results has
   In this article, we established that a number of glass-       received funding from the European Research Council
forming models with various pair interactions, particle          under the European Unions Seventh Framework Pro-
size distributions and degree of non-additivity, can be          gramme (FP7/2007-2013)/ERC Grant Agreement No.
efficiently simulated using a simple swap Monte Carlo al-        306845. This work was supported by a grant from the
gorithm and remain excellent glass-formers down to very          Simons Foundation (# 454933, Ludovic Berthier).




 [1] Ludovic Berthier and Giulio Biroli, “Theoretical perspec-       Rev. Mod. Phys. 83, 587645 (2011).
     tive on the glass transition and amorphous materials,”
                                                                                                                               20

 [2] Gary L. Hunter and Eric R. Weeks, “The                            Phys. Rev. E 88, 053309 (2013).
     physics     of    the    colloidal    glass    transition,”  [18] M. E. J. Newman and G. T. Barkema, Monte Carlo meth-
     Rep. Prog. Phys. 75, 066501 (2012).                               ods in statistical physics (Clarendon Press Oxford Uni-
 [3] M.        D.       Ediger,      “Spatially        heteroge-       versity Press, Oxford New York, 1999).
     neous      dynamics       in     supercooled       liquids,” [19] C.     Dress    and    W.     Krauth,     “Cluster    algo-
     Ann. Rev. Phys. Chem. 51, 99 (2000).                              rithm for hard spheres and related systems,”
 [4] G. Brambilla, D. El Masri, M. Pierno, L. Berthier,                J. Phys. A: Math. Gen. 28, L597 (1995).
     L. Cipelletti, G. Petekidis,       and A. B. Schofield,      [20] Ludger Santen and Werner Krauth, “Absence of ther-
     “Probing the equilibrium dynamics of colloidal hard               modynamic phase transition in a model glass former,”
     spheres above the mode-coupling glass transition,”                Nature 405, 550 (2000).
     Phys. Rev. Lett. 102, 085703 (2009).                         [21] Etienne P. Bernard and Werner Krauth, “Two-step melt-
 [5] Thomas Blochowicz,         Alexander Brodin,            and       ing in two dimensions: First-order liquid-hexatic transi-
     Ernst A. Rössler, “Evolution of the dynamic sus-                 tion,” Phys. Rev. Lett. 107, 155704 (2011).
     ceptibility in supercooled liquids and glasses,” in          [22] Robert H. Swendsen and Jian-Sheng Wang, “Nonuni-
     Fractals, Diffusion, and Relaxation in Disordered Complex Systems versal critical dynamics in Monte Carlo simulations,”
     (Wiley-Blackwell, 2005) pp. 127–256.                              Phys. Rev. Lett. 58, 86 (1987).
 [6] R. Richert and C. A. Angell, “Dynamics of                    [23] Kurt Binder, The Monte-Carlo Methods in Condensed
     glass-forming liquids. V. On the link between                     Matter Physics (Springer, Heidelberg, 1992).
     molecular dynamics and configurational entropy,”             [24] Masaharu Isobe and Werner Krauth, “Hard-sphere melt-
     J. Chem. Phys. 108, 9016 (1998).                                  ing and crystallization with event-chain Monte Carlo,”
 [7] Pablo G. Debenedetti and Frank H. Stillinger,                     J. Chem. Phys. 143, 084509 (2015).
     “Supercooled liquids and the glass transition,”              [25] Richard L. C. Vink, “A finite-temperature monte
     Nature 410, 259 (2001).                                           carlo algorithm for network forming materials,”
 [8] Stefan W. Hell, “Far-field optical nanoscopy,”                    J. Chem. Phys. 140, 104509 (2014).
     Science 316, 1153 (2007).                                    [26] Srikanth Sastry, Pablo G. Debenedetti, and Frank H.
 [9] Sumit Ashtekar, Gregory Scott, Joseph Lyding, and                 Stillinger, “Signatures of distinct dynamical regimes
     Martin Gruebele, “Direct Visualization of Two-State               in the energy landscape of a glass-forming liquid,”
     Dynamics on Metallic Glass Surfaces Well Below Tg,”               Nature 393, 554557 (1998).
     J. Phys. Chem. Lett. 1, 1941 (2010).                         [27] Koji Hukushima and Koji Nemoto, “Exchange Monte
[10] Stephen F. Swallen, Kenneth L. Kearns, Marie K. Mapes,            Carlo Method and Application to Spin Glass Simula-
     Yong Seol Kim, Robert J. McMahon, M. D. Ediger,                   tions,” J. Phys. Soc. Jap. 65, 1604 (1996).
     Tian Wu, Lian Yu, and Sushil Satija, “Organic glasses        [28] Koji Hukushima, Hajime Takayama,              and Hajime
     with exceptional thermodynamic and kinetic stability,”            Yoshino, “Exchange Monte Carlo Dynamics in the SK
     Science 315, 353 (2007).                                          Model,” J. Phys. Soc. Jap. 67, 12 (1998).
[11] J.-L. Barrat, J.-N. Roux, and J.-P. Hansen, “Dif-            [29] Ryoichi Yamamoto and Walter Kob, “Replica-exchange
     fusion, viscosity and structural slowing down in                  molecular dynamics simulation for supercooled liquids,”
     soft sphere alloys near the kinetic glass transition,”            Phys. Rev. E 61, 5473 (2000).
     Chem. Phys. 149, 197 (1990).                                 [30] Gerardo Odriozola and Ludovic Berthier, “Equilibrium
[12] Walter Kob and Hans C. Andersen, “Test-                           equation of state of a hard sphere binary mixture at very
     ing mode-coupling theory for a supercooled bi-                    large densities using replica exchange Monte Carlo sim-
     nary     Lennard-Jones      mixture.    II.   Intermediate        ulations,” J. Chem. Phys. 134, 054504 (2011).
     scattering function and dynamic susceptibility,”             [31] Walter Kob and Ludovic Berthier, “Probing a Liquid to
     Phys. Rev. E 52, 4134–4153 (1995).                                Glass Transition in Equilibrium,” Phys. Rev. Lett. 110,
[13] Joshua A. Anderson, Chris D. Lorenz, and A. Trav-                 245702 (2013).
     esset, “General purpose molecular dynamics simula-           [32] Misaki Ozawa, Walter Kob, Atsushi Ikeda,               and
     tions fully implemented on graphics processing units,”            Kunimasa       Miyazaki,     “Equilibrium      phase    di-
     J. Comp. Phys. 227, 5342 (2008).                                  agram      of   a    randomly      pinned    glass-former,”
[14] Peter H. Colberg and Felix Höfling, “Highly ac-                  Proc. Nat. Acad. Sci. 112, 6914 (2015).
     celerated simulations of glassy dynamics using               [33] Ludovic Berthier, “Overlap fluctuations in glass-forming
     GPUs: Caveats on limited floating-point precision,”               liquids,” Phys. Rev. E 88, 022313 (2013).
     Comp. Phys. Commun. 182, 1120 (2011).                        [34] Ludovic Berthier and Robert L Jack, “Evidence for a
[15] Nicholas P. Bailey, Trond S. Ingebrigtsen, Jesper Schmidt         disordered critical point in a glass-forming liquid,” Phys.
     Hansen, Arno A. Veldhorst, Lasse Bhling, Claire A.                Rev. Lett. 114, 205701 (2015).
     Lemarchand, Andreas E. Olsen, Andreas K. Bacher,             [35] Roland Faller and Juan J. de Pablo, “Den-
     Heine Larsen, Jeppe C. Dyre, and et al., “RUMD: A                 sity of states of a binary Lennard-Jones glass,”
     general purpose molecular dynamics package optimized              J. Chem. Phys. 119, 4405 (2003).
     to utilize GPU hardware down to a few thousand parti-        [36] Jared Callaham and Jonathan Machta, “Population an-
     cles,” arXiv:1506.05094 (2015).                                   nealing simulations of a binary hard sphere mixture,”
[16] Joshua A. Anderson, Eric Jankowski, Thomas L. Grubb,              arXiv:1701.00263 (2017).
     Michael Engel, and Sharon C. Glotzer, “Massively paral-      [37] D. Gazzillo and G. Pastore, “Equation of state for
     lel Monte Carlo for many-particle simulations on GPUs,”           symmetric non-additive hard-sphere fluids: An approxi-
     J. Comp. Phys. 254, 27 (2013).                                    mate analytic expression and new Monte Carlo results,”
[17] R. Meyer, “Efficient parallelization of short-range molec-        Chem. Phys. Lett. 159, 388 (1989).
     ular dynamics simulations on many-core systems,”
                                                                                                                                21

[38] Tomas S. Grigera and Giorgio Parisi, “Fast Monte             [55] D. Frenkel and B. Smit, Understanding Molecular Simu-
     Carlo algorithm for supercooled soft spheres,”                    lation (Academic, New York, 2nd Ed., 2001).
     Phys. Rev. E 63, 045102 (2001).                              [56] L. Berthier and W. Kob, “The Monte Carlo dynam-
[39] G. Biroli, J.-P. Bouchaud, A. Cavagna, T. S. Grig-                ics of a binary Lennard-Jones glass-forming mixture,”
     era, and P. Verrocchio, “Thermodynamic signature                  J. Phys.: Condens. Matter 19, 205130 (2007).
     of growing amorphous order in glass-forming liquids,”        [57] Kai Zhang, Meng Fan, Yanhui Liu, Jan Schroers,
     Nat. Phys. 4, 771 (2008).                                         Mark D. Shattuck, and Corey S. O’Hern, “Beyond pack-
[40] Chiara Cammarota, Andrea Cavagna, Giacomo                         ing of hard spheres: The effects of core softness, non-
     Gradenigo, Tomas S. Grigera,            and Paolo Ver-            additivity, intermediate-range repulsion, and many-body
     rocchio, “Numerical determination of the expo-                    interactions on the glass-forming ability of bulk metallic
     nents controlling the relationship between time,                  glasses,” J. Chem. Phys. 143, 184502 (2015).
     length, and temperature in glass-forming liquids,”           [58] Walter Kob and Hans C. Andersen, “Scaling behavior in
     J. Chem. Phys. 131, 194901 (2009).                                the beta-relaxation regime of a supercooled lennard-jones
[41] C.    Cammarota,       A.    Cavagna,      I.    Giardina,        mixture,” Phys. Rev. Lett. 73, 1376 (1994).
     G. Gradenigo, T. S. Grigera, G. Parisi,               and    [59] Ch. Hausleitner and J. Hafner, “Hybridized nearly-
     P. Verrocchio, “Phase-Separation Perspective on                   free-electron tight-binding-bond approach to interatomic
     Dynamic Heterogeneities in Glass-Forming Liquids,”                forces in disordered transition-metal alloys. i. theory,”
     Phys. Rev. Lett. 105, 055703 (2010).                              Phys. Rev. B 45, 115 (1992).
[42] Andrea Cavagna, Tomas S. Grigera,              and Paolo     [60] J. P. Hansen and I. R. McDonald, Theory of simple liq-
     Verrocchio, “Dynamic relaxation of a liquid                       uids : with applications to soft matter (Academic Press,
     cavity under amorphous boundary conditions,”                      Amsterdam Boston, 2013).
     J. Chem. Phys. 136, 204502 (2012).                           [61] Hajime       Tanaka,     “Bond     orientational       order
[43] Sander Pronk and Daan Frenkel, “Melting of polydis-               in    liquids:      Towards     a    unified    description
     perse hard disks,” Phys. Rev. E 69, 066123 (2004).                of    water-like    anomalies,     liquid-liquid     transi-
[44] L. A. Fernández, V. Martı́n-Mayor,          and P. Ver-          tion,     glass    transition,    and      crystallization,”
     rocchio,    “Phase    Diagram      of    a    Polydisperse        Eur. Phys. J. E 35 (2012), 10.1140/epje/i2012-12113-y.
     Soft-Spheres Model for Liquids and Colloids,”                [62] Wolfgang Götze, Complex dynamics of glass-forming liq-
     Phys. Rev. Lett. 98, 085702 (2007).                               uids : a mode-coupling theory (Oxford University Press,
[45] L. A. Fernández, V. Martı́n-Mayor, B. Seoane, and                Oxford New York, 2009).
     P. Verrocchio, “Separation and fractionation of or-          [63] Yael S. Elmatad, David Chandler, and Juan P. Garra-
     der and disorder in highly polydisperse systems,”                 han, “Corresponding states of structural glass formers,”
     Phys. Rev. E 82, 021501 (2010).                                   J. Phys. Chem. B 113, 5563–5567 (2009).
[46] B. Bernu, J. P. Hansen, Y. Hiwatari, and G. Pa-              [64] P. Sollich and N. B. Wilding, “Phase behaviour of poly-
     store, “Soft-sphere model for the glass transition                disperse spheres: simulation strategies and an application
     in binary alloys: Pair structure and self-diffusion,”             to the freezing transition,” J. Chem. Phys. 133, 224102
     Phys. Rev. A 36, 4891 (1987).                                     (2010).
[47] L. A. Fernández, V. Martı́n-Mayor, and P. Verrocchio,       [65] Peter Sollich and Nigel B. Wilding, “Crys-
     “Critical behavior of the specific heat in glass formers,”        talline     Phases      of     Polydisperse       Spheres,”
     Phys. Rev. E 73, 020501 (2006).                                   Phys. Rev. Lett. 104, 118302 (2010).
[48] Yisroel Brumer and David R. Reichman, “Numerical In-         [66] Trond S. Ingebrigtsen and Hajime Tanaka, “Effect of size
     vestigation of the Entropy Crisis in Model Glass Form-            polydispersity on the nature of lennard-jones liquids,”
     ers,” J. Phys. Chem. B 108, 6832 (2004).                          J. Phys. Chem. B 119, 1105211062 (2015).
[49] L. A. Fernández, V. Martı́n-Mayor, and P. Verroc-           [67] Daniel A. Mártin, Andrea Cavagna, and Tomás S.
     chio, “Optimized Monte Carlo method for glasses,”                 Grigera, “Specific Heat Anomaly in a Supercooled
     Phil. Mag. 87, 581 (2007).                                        Liquid with Amorphous Boundary Conditions,”
[50] Ludger Santen and Werner Krauth, “Liquid, Glass and               Phys. Rev. Lett. 114, 225901 (2015).
     Crystal in Two-dimensional Hard disks,” arxiv:0107459        [68] B. Bernu, J. P. Hansen, Y. Hiwatari, and G. Pa-
     (2001).                                                           store, “Soft-sphere model for the glass transition
[51] Ricardo Gutiérrez, Smarajit Karmakar, Yoav G Pollack,            in binary alloys: Pair structure and self-diffusion,”
     and Itamar Procaccia, “The static lengthscale character-          Phys. Rev. A 36, 4891–4903 (1987).
     izing the glass transition at lower temperatures,” EPL       [69] Ludovic Berthier, Giulio Biroli, Daniele Coslovich,
     (Europhysics Letters) 111, 56009 (2015).                          Walter Kob,        and Cristina Toninelli, “Finite-size
[52] Ludovic Berthier, Daniele Coslovich, Andrea Ninarello,            effects in the dynamics of glass-forming liquids,”
     and Misaki Ozawa, “Equilibrium sampling of hard                   Phys. Rev. E 86 (2012).
     spheres up to the jamming density and beyond,”               [70] Kai Zhang, Bradley Dice, Yanhui Liu, Jan Schroers,
     Phys. Rev. Lett. 116, 238002 (2016).                              Mark D. Shattuck,          and Corey S. O’Hern, “On
[53] Ludovic Berthier, Patrick Charbonneau, Yuliang                    the origin of multi-component bulk metallic
     Jin, Giorgio Parisi, Beatriz Seoane, and Francesco                glasses:    Atomic size mismatches and de-mixing,”
     Zamponi, “Growing timescales and lengthscales                     J. Chem. Phys. 143, 054501 (2015).
     characterizing vibrations of amorphous solids,”              [71] Cristiano De Michele, Francesco Sciortino, and An-
     Proc. Nat. Acad. Sci. 113, 8397 (2016).                           tonio Coniglio, “Scaling in soft spheres: fragility
[54] M. P. Allen and D. J. Tildesley, Computer simulation of           invariance on the repulsive potential softness,”
     liquids (Clarendon Press Oxford University Press, Oxford          J. Phys.: Condens. Matter 16, L489 (2004).
     England New York, 1989).
                                                                                                                         22

[72] Ian Douglass, Toby Hudson,          and Peter Harrow-           lus in two van der waals bonded glass-forming liquids,”
     ell, “Density and glass forming ability in amorphous            Phys. Rev. B 95, 104202 (2017).
     atomic alloys: the role of the particle softness,”         [79] Cristina Toninelli, Matthieu Wyart, Ludovic Berthier,
     J. Chem. Phys. 144, 144502 (2016).                              Giulio Biroli,     and Jean-Philippe Bouchaud, “Dy-
[73] D. Gazzillo, G. Pastore, and S. Enzo, “Chemical short-          namical susceptibility of glass formers:           Con-
     range order in amorphous Ni-Ti alloys: an integral equa-        trasting the predictions of theoretical scenarios,”
     tion approach with a non-additive hard-sphere model,”           Phys. Rev. E 71, 041505 (2005).
     J. Phys.: Condens. Matter 1, 3469 (1989).                  [80] L. Berthier, G. Biroli, J.-P. Bouchaud, W. Kob,
[74] D Gazzillo, G Pastore, and R Frattini, “The role of             K. Miyazaki, and D. R. Reichman, “Spontaneous and
     excluded volume effects on the structure and chem-              induced dynamic fluctuations in glass formers. I. Gen-
     ical short-range order of Ni33Y67 metallic glass,”              eral results and dependence on ensemble and dynamics,”
     J. Phys.: Condens. Matter 2, 8463 (1990).                       J. Chem. Phys. 126, 184503 (2007).
[75] U. Buchenau and R. Zorn, “A relation between fast          [81] Ludovic Berthier and Robert L. Jack, “Structure and dy-
     and slow motions in glassy and liquid selenium,”                namics of glass formers: Predictability at large length
     EPL (Europhysics Letters) 18, 523 (1992).                       scales,” Phys. Rev. E 76, 041509 (2007).
[76] T. Scopigno, G. Ruocco, Francesco Sette, and Giulio        [82] Robert L. Jack, Andrew J. Dunleavy, and C. Patrick
     Monaco, “Is the fragility of a liquid embedded in the           Royall, “Information-theoretic measurements of cou-
     properties of its glass?” Science 302, 849–852 (2003).          pling between structure and dynamics in glass formers,”
[77] Jeppe C. Dyre, “Colloquium:           The glass transi-         Phys. Rev. Lett. 113, 095703 (2014).
     tion and elastic models of glass-forming liquids,”         [83] Göran Wahnström, “Molecular-dynamics study of a
     Rev. Mod. Phys. 78, 953972 (2006).                              supercooled two-component Lennard-Jones system,”
[78] Henriette W. Hansen, Bernhard Frick, Tina Hecksher,             Phys. Rev. A 44, 3752 (1991).
     Jeppe C. Dyre, and Kristine Niss, “Connection between      [84] Ludovic      Berthier   and    Gilles   Tarjus,   “The
     fragility, mean-squared displacement, and shear modu-           role of attractive forces in viscous liquids,”
                                                                     J. Chem. Phys. 134, 214503 (2011).
