                                                              Generating ultradense jammed ellipse packings using biased SWAP

                                                                                                        Robert S. Hoy
                                                                       Department of Physics, University of South Florida, Tampa, FL 33620 USA∗
                                                                                               (Dated: October 1, 2024)
                                                                 Using a Lubachevsky-Stillinger-like growth algorithm combined with biased SWAP Monte Carlo
                                                              and transient degrees of freedom, we generate ultradense disordered jammed ellipse packings. For
                                                              all aspect ratios α, these packings exhibit significantly smaller intermediate-wavelength density
                                                              fluctuations and greater local nematic order than their less-dense counterparts. The densest pack-
                                                              ings are disordered despite having packing fractions√ φJ (α) that are within less than 0.5% of that
arXiv:2409.19196v1 [cond-mat.soft] 28 Sep 2024




                                                              of the monodisperse-ellipse crystal [φxtal = π/(2 3) ≃ .9069] over the range 1.25 . α . 1.4
                                                              and coordination numbers ZJ (α) that are within less than 0.5% of isostaticity [Ziso = 6] over the
                                                              range 1.3 . α . 2.0. Lower-α packings are strongly fractionated and consist of polycrystals of
                                                              intermediate-size particles, with the largest and smallest particles isolated at the grain boundaries.
                                                              Higher-α packings are also fractionated, but in a qualitatively-different fashion; they are composed
                                                              of increasingly-large locally-nematic domains reminiscent of liquid glasses.


                                                                    INTRODUCTION                                   packings’ multiscale structure differs qualitatively from
                                                                                                                   that of their less-dense counterparts, in a nontrivial and
                                                    Much attention has been paid over the past 20 years            strongly-α-dependent fashion.
                                                 to jammed packings of anistropic particles and how they
                                                 differ from those formed by disks and spheres [1–18]. In                                  METHODS
                                                 parallel, over the past decade, the SWAP Monte Carlo
                                                 algorithm [19, 20] has enabled preparation of lower-T
                                                                                                                      We recently performed a detailed characterization of
                                                 equilibrated supercooled liquids, more-stable glasses, and
                                                                                                                   jammed ellipse packings’ structure [5] over a much wider
                                                 denser disordered jammed packings than was previously
                                                 feasible [21–27]. Recent work has shown that allowing             range of aspect ratios (1 ≤ α ≤ 10) than had been con-
                                                                                                                   sidered in previous studies [2–4, 6–8]. To understand the
                                                 particles’ diameters to vary independently during sam-
                                                 ple preparation provides additional transient degrees of          effects of particle dispersity, we employed three different
                                                                                                                   probability distributions for the ellipses’ inital minor-axis
                                                 freedom (TDOF) which can be exploited to obtain even-
                                                                                                                   lengths σ:
                                                 stabler glasses and even-denser packings [28–30].
                                                    Surprisingly, however, the latter two developments                              Pmono (σ) = δ(σ − .07),
                                                 have not yet been exploited to shed light on the first
                                                 topic. More generally, very few simulation studies have                                 δ(σ − .05a) δ(σ − .07)
                                                                                                                             Pbi (σ) =              +           ,
                                                 attempted to determine how jammed anistropic-particle                                        2          2
                                                 packings’ structure depends on their preparation pro-                                                                        (1)
                                                 tocol, despite the great insights obtained from com-                                     ( 7
                                                                                                                                                ,       .05 ≤ σ ≤ .07
                                                 parable studies of disk and sphere packings [23, 31–                 and Pcontin   (σ) =  4σ 2                           ,
                                                 33] and the many open science questions raised by re-
                                                                                                                                              0    , σ < .05 or σ > .07
                                                 cent experimental studies of anistropic-particle (colloidal
                                                 and small-molecule) glasses with strongly-preparation-            where δ is the Dirac delta function and σ is expressed
                                                 protocol-dependent multiscale structure [34–41].                  in arbitrary units of length. For all but the smallest
                                                    This combination of factors presents an opportunity            aspect ratios (where systems with P = Pmono formed
                                                 to make progress on multiple fronts by applying SWAP              jammed states with a high degree of crystallinity, as ex-
                                                 and TDOF moves during the preparation of jammed                   pected [42]), all three of these P (σ) produced the same
                                                 anistropic-particle packings. Two-dimensional ellipses            qualitative structural trends. For example, the densest
                                                 are perhaps the best shapes with which to begin such              jammed packings always had the best-ordered first coor-
                                                 an effort, since they are a straightforward generalization        dination shells, exhibiting positional-orientation correla-
                                                 of disks and their jamming phenomemology for prepara-             tions which were substantially greater than those of their
                                                 tion protocols which mimic fast compression has already           less-dense counterparts, even though the details of these
                                                 been extensively studied [2–8]. In this paper, we show            correlations were strongly P (σ)-dependent.
                                                 that adding a suitably biased SWAP algorithm and a                   Choosing P = Pcontin produces systems in which equal
                                                 minimalistic implementation of TDOF to a Lubachevsky-             areas are occupied by particles of different sizes, and ap-
                                                 Stillinger (LS)-like particle-growth algorithm [42] yields        parently optimizes glass-formability for a wide variety of
                                                 jammed ellipse packings which are significantly denser            interparticle force laws [20]. Moreover, in contrast to
                                                 than any previously reported for all 1 < α ≤ 5. These             Pbi , which has been employed as the standard model for
                                                                                                                           2

granular materials over the past 20 years [43] and was          brackets is a lower bound for the amount by which parti-
the only P (σ) employed in all other previous studies of        cles i and j can grow without overlapping: specfically, it
ellipse jamming [2–4, 6–8], it allows for efficient particle-   is the factor by which particles i and j can grow without
diameter swapping [20].                                         overlapping if they are aligned end-to-end. The minimum
   We made no attempt in Ref. [5], however, to employ           in Eq. 2 is taken over all nearest neighbors (j) of parti-
SWAP or indeed to investigate preparation-protocol de-          cle i, while the subsequent minimum defining G̃ is taken
pendence in any way. Instead, all packings were gener-          over all i. These choices make the algorithm more effi-
ated using the same protocol: a LS-like particle-growth         cient by allowing particles to grow slower when gaps are
algorithm [42] that mimicked rapid compression. Each            small and faster when they are large. We emphasize that
growth cycle consisted of two steps:                            imposing a uniform growth rate G̃ preserves the shape of
                                                                the particle-size distribution P (σ) defined in Eq. 1. In
   1. Attempting to translate each particle i by a ran-
                                                                other words, the ratio σmax /σmin = 1.4 of the largest
      dom displacement along each Cartesian direction
                                                                and smallest ellipses’ minor-axis lengths, and indeed the
      and rotate it by a random angle; and
                                                                ratios Rof all other moments of P (σ), remain constant as
                                                                         σmax
   2. Increasing all particles’ minor-axis lengths σ by the     hσi = σmin     σP (σ)dσ increases.
      same factor G̃, where G̃ is the value that brings one        Step (3) begins by recalculating all the gij and then
      pair of ellipses into tangential contact.                 re-indexing particles in order of increasing g̃i = min(gij ),
Here we obtain substantially higher jamming densities by        where the minimum is again taken over particle i’s near-
adding two more steps to this cycle:                            est neighbors. Then, for each i < N , a particle index
                                                                k > i is randomly selected; the corresponding particles
   3. SWAP moves which exchange the diameters of                necessarily have g̃k > g̃i . If they also have σk < σi ,
      larger particles with smaller “gaps” (defined below)      the SWAP move is accepted, the g̃ values for particles i,
      with those of smaller particles with larger gaps; and     k and their nearest neighbors are recalculated to reflect
                                                                the new configuration, and the re-indexing is repeated.
   4. TDOF moves which grow particles by different fac-
                                                                If, on the other hand, the selected particle has σk > σi ,
      tors Gi and thus allow the shape of P (σ) to vary.
                                                                the move attempt is canceled and a different k-value (i.e.,
   As in Ref. [5], we begin by placing N = 1000 nonover-        a different potential SWAP partner) is selected. When
lapping ellipses of aspect ratio α, with random posi-           either a swap has been completed or N/10 k-values have
tions and orientations, and minor-axis-length distribu-         been sampled without finding a particle with σk > σi ,
tions given
       √     by P = Pcontin , in square L × L domains with      the algorithm proceeds to the next particle (the next i
L = N α. Periodic boundary conditions are applied               value). This procedure yields high SWAP-move success
along both directions, so these initial states have packing     rates, particularly when φ is still low.[45]
fractions φ < 0.01. Then we begin the particle-growth              Step (4) also begins by recalculating all the g̃i and
procedure, which executes steps 1-3 for each growth cycle       then re-indexing particles in order of increasing g̃i .
throughout the run, and step 4 in the latter stages of the      Then it proceeds by growing each particle by a factor
run. Overlaps between ellipse pairs (i, j) are prevented        min(Gi , 10−3 ); this cap on the growth rate prevents par-
throughout the entire process using Zheng and Palffy-           ticles with unusually large g̃i from growing too quickly.
Muhoray’s exact expression [44] for their orientation-          In contrast to step (2), step (4) allows P (σ) to vary, and
dependent distance of closest approach dcap (i, j).             effectively adds one transient DOF per particle [28–30].
   In step (1), the attempted translations and rotations        Note that this step is executed only if f < 10−2 . We
have maximum magnitudes 0.05f and (16f /α)◦ , respec-           found that this choice both maximizes the final φJ (α)
tively. The move-size factor f is set to 1 at the begin-        and keeps increases in systems’ polydispersity over the
ning of all runs, and multiplied by 3/4 whenever 100            course of the packing-generation runs very modest.
consecutive growth cycles have passed with G̃ < 10−10 .            Critically, in contrast to standard hard-particle SWAP
Runs are terminated and the configurations are consid-          [19] which accepts any move that does not introduce in-
ered jammed when f drops below 2 × 10−8. These cutoff           terparticle overlap, our procedure is biased towards both
values for f and G̃ are the smallest values allowed by our      increasing the minimum value of g̃i . By effectively intro-
double-precision numerical implementation.                      ducing an “energy” cost for nonuniform {g̃i }, both the
   In step (2), the fractional particle-growth rate per cycle   SWAP moves and the TDOF moves act in a similar spirit
is set to the maximum value which does not introduce any        to the TDOF moves employed in Refs. [28–30]. Specif-
interparticle overlaps, i.e. by G̃ = min(Gi ), where            ically, they both decrease the width of the probability
                           
                                 σi
                                                               distributions P (g̃) by systematically transferring mass
                 Gi = min                 gij .           (2)   from regions with smaller gaps to regions with larger
                             2α(σi + σj )
                                                                gaps. The SWAP moves accomplish this while leaving
The gap distances gij are defined using the relation            the packing fraction unchanged, while the TDOF moves
gij = rij − dcap (i, j), so the quantity within the square      produce a spatially-nonuniform densification rate.
                                                                                                                                                   3

                                     RESULTS                                             TDOF moves decreases monotonically from ∼5% to ∼1%
                                                                                         as α increases from 1 to 1.6. This rapid decrease makes
   In this section, we will both qualitatively and quanti-                               the shape of the φJ (α) curve obtained using SWAP and
tatively compare the structure of jammed ellipse pack-                                   TDOF moves differ in two key ways from those ob-
ings generated using different sample-preparation proto-                                 tained without these moves, including results from pre-
cols. Novel results obtained using all four steps of the                                 vious studies [2–5]. First, the initial slope (∂φJ /∂α)α=1 ,
growth algorithm described above were averaged over 25                                   whose positive value demonstrates that anisotropic parti-
independently prepared samples. Results obtained using                                   cles’ ability to rotate away from one another allows them
only steps (1-2) of this algorithm are taken from Ref.                                   to pack more densely than disks [1–3], is much smaller
[5]. Ref. [2]’s were generated using a LS-like algorithm                                 when SWAP and TDOF moves are employed, suggest-
similar in spirit to (if different in its details from) that                             ing that the density-enhancing effect of allowing particle
detailed in steps (1-2). Ref. [3]’s were obtained using                                  rotations weakens as systems get denser.
the standard LS algorithm [42, 46]. Ref. [4]’s and Refs.                                    Second, the aspect ratio αmax at which φJ (α) is max-
[6–8]’s were obtained by successive cycles of compression                                imized gets shifted to lower values. Specifically, while
followed by conjugate gradient (CG) energy minimiza-                                     Refs. [2], [3] and [5] respectively found αmax = 1.43,
tion; their φJ (α) were identified as the packing fractions                              αmax = 1.40 and αmax = 1.45, here we find αmax = 1.30.
above which potential energy no longer dropped to zero.                                  Ref. [4] also found αmax = 1.30; the fact that this re-
In some figures, we will show data from refs. [2–4] to il-                               sult was similar to ours, rather than those from Refs.
lustrate the variety of results obtained in previous studies                             [2, 3, 5], probably owes to the authors’ choice of sample-
of ellipse jamming. Results from Refs. [6–8] followed the                                preparation protocol. CG minimization of dense systems
same general trends, and will be omitted for clarity.                                    generates forces which can transmit stress over substan-
                                                                                         tial distances, and hence (much like biased-SWAP and
        0.91           With SWAP and TDOF            No SWAP or TDOF (Ref. [5])          TDOF moves) tend to suppress long-wavelength density
                                                                          Ref. [2]       fluctuations.
                                                                          Ref. [3]
        0.89                                                              Ref. [4]
                                                                                            Refs. [2–5] respectively found φJ (αmax ) = .895, .8974,
                                                                                         .891 and .8917. Here we find φJ (αmax ) = .9034, which
                                                                                         is less than 0.4% below φxtal . Although this packing
      0.87
    J




                             6
                             5
                                                                                         fraction is only ∼ 1% larger than the largest value re-
                % increase




                             4
                             3
                                                                                         ported in previous studies of ellipse jamming, it reduces
        0.85                 2                                                           the minimum values of the void area fractions φv (α) =
                             1
                             0
                                                                                         φxtal − φJ (α) by 71%, 64%, 79%, and 78% from those
                                 1   2   3       4   5
        0.83                                                                             reported in Refs. [2–5], respectively. In other words,
            1                                2                3          4           5
                                                                                         the densest packings we obtain using SWAP and TDOF
                                                                                        moves have far less “free volume” than those obtained
FIG. 1. Jamming densities of systems prepared with and                                   in previous studies. Comparably large reductions in free
without SWAP and TDOF moves. The dashed line indicates                                   volume persist over a wide range of α. For example, we
φxtal ≃ .9069, and the inset shows the percentage increases                              find that φJ (α) > .995φxtal [and hence φv (α) < .005φxtal ]
over the φJ (α) obtained in Ref. [5] obtained by adding steps                            for all 1.25 . α . 1.40. Here we have implicitly assumed
(3-4) to the particle-growth procedure.                                                  that φxtal is the maximum possible packing fraction. This
                                                                                         hypothesis has been proven correct for monodisperse el-
   Figure 1 shows the preparation-protocol dependence                                    lipses [48], and no denser polydisperse ellipse packings
of φJ (α). Adding SWAP and TDOF moves always gen-                                        have been reported to the best of our knowledge. On
erates substantially denser packings, but the degree to                                  the other hand, Ref. [30] found φJ (1) > φxtal in sys-
which this is so, and the structural differences asso-                                   tems with a substantially larger polydispersity index than
ciated with the density improvement, are strongly α-                                     those considered here, and a more advanced algorithm
dependent. The packing fraction obtained for disks,                                      might be able to achieve the same result for α > 1.
φJ (1) ≃ .883, is consistent with previous studies of col-                                  For α > 1.6, the packing-efficiency gain increases
lectively jammed monodisperse disk packings [32], which                                  monotonically, reaching ∼6% by α = 5. This rapid in-
are typically highly crystalline. Polydisperse disk pack-                                crease causes the shape of the φJ (α) curve to differ in
ings with such high densities were not reported until very                               a third key way from those reported in previous stud-
recently. Refs. [30, 47] used sophisticated SWAP and/or                                  ies. Specifically, the rapid decrease of φJ (α) for α > 2
TDOF-based algorithms to obtain even denser packings,                                    [2, 4, 5], which is widely believed to be a general feature
which had .89 . φJ . .91 despite remaining amorphous,                                    of anisotropic-particle jamming [9, 11] provided systems
but the methods employed in these studies are not readily                                remain isotropic as they are compressed, is sufficiently
generalizable to anistropic particles.                                                   strongly suppressed that ∂ 2 [ln(φJ )]/∂[ln(α)]2 is positive
   The packing-efficiency gain from adding SWAP and                                      rather than negative. In other words, the slow crossover
                                                                                                                                   4

to φJ ∼ 1/α scaling expected from Onsager-like argu-                    more dramatic decrease in the degree of hypostaticity
ments [49] and evident in the φJ (α) curves presented in                H(α) = Ziso − ZJ (α). The very small H(α) over the
Refs. [2, 5] is absent when SWAP and TDOF moves are                     range 1.3 . α . 2.0 suggest that these systems have
employed, at least for the range of α considered here.                  very few ways available to pack more densely, and there-
Below, we will argue that this qualitative difference is                fore, in contrast to those discussed in Refs. [1–8], are
made possible by the moves’ tendency to increase pack-                  nearly maximally stable; note that the maximally-dense
ings’ orientational order.                                              monodisperse-ellipse crystal also has Z = Ziso . As α in-
   Previous work on ellipse jamming has devoted much                    creases past ∼3, however, the ZJ (α) rapidly drop below
attention to ZJ (α) because it illlustrates several key fea-            those reported in Refs. [2, 5], apparently because employ-
tures of how anisotropic particles pack. Since smooth                   ing SWAP and TDOF moves increases the tendency of
2D convex anisotropic particles have three degrees of                   ellipses to pack into stable Z = 4 configurations where
freedom (two translational, one rotational), one would                  they are trapped by one parallel-aligned neighbor on ei-
naively expect them to jam at isostaticity (ZJ = Ziso =                 ther side and one unaligned neighbor on either end. This
6). This behavior, however, has not been observed in                    result is rather surprising because it indicates that max-
previous studies of ellipses [2–8], spherocylinders [4, 12],            imizing φJ and maximizing ZJ need not always coincide.
or superdisks [13]. Instead, all previous studies of el-                   To begin connecting the above results to differences in
lipses have found a square-root
                           √       singularity at small as-             the packings’ multiscale structure, we visually inspected
pect ratios [ZJ − 4 ∝ α − 1 for α − 1 ≪ 1] and a                        them. Typical results for four aspect ratios that illus-
substantially-hypostatic plateau at intermediate aspect                 trate the key trends we observed are shown in Figure
ratios [5.5 . ZJ . 5.8 for 1.5 . α . 3]. These trends                   3. Results in the top row are similar to those found in
have been interpreted in terms of particles being mechan-               previous studies [2–8]. Those in the bottom row, how-
ically stabilized by their curvature at the point of contact            ever, are dramatically different. For small aspect ratios,
[3] and/or by quartic vibrational modes [6–8], but in light             adding SWAP and TDOF moves yields strongly fraction-
of the protocol-dependence of φJ (α) discussed above, it is             ated packings consisting of polycrystals of intermediate-
worth revisiting the protocol-dependence of ZJ (α) here.                size particles, with the largest and smallest particles iso-
                                                                        lated at the grain boundaries. The crystalline domains
        6.0
               With SWAP and TDOF   No SWAP or TDOF (Ref. [5])          exhibit particle-size gradients whose formation is pre-
                                                         Ref. [2]       sumably a collective effect of particle-diameter swapping
                                                         Ref. [3]
                                                         Ref. [4]
                                                                        [23]. The grain boundaries contain “dislocation cores”
        5.5
                                                                        which have long been recognized as a distinctive feature
                                                                        of dense polycrystalline disk packings [32], but have not
   ZJ




        5.0                                                             (to the best of our knowledge) been previously observed
                                                                        in anisotropic-particle packings.
        4.5                                                                The abovementioned fractionation weakens slowly with
                                                                        increasing α, but short-ranged orientational order weak-
        4.0                                                             ens sufficiently rapidly that the densest packings we ob-
           1                    2            3          4           5
                                                                        tained (α = αmax = 1.3) are apparently amorphous de-
                                    α
                                                                        spite having a density less than 0.4% below that of the
FIG. 2. Coordination numbers of systems prepared with and
                                                                        crystal. For α = 2, while the packing generated using
without SWAP and TDOF moves. The dotted line indicates                  SWAP and TDOF appears to have greater short-ranged
Ziso = 6.                                                               orientational order (to be quantified below), it clearly
                                                                        does not include any large locally-nematic domains. Vi-
   Figure 2 shows that adding SWAP and TDOF moves                       sual inspection suggests that for these aspect ratios, the
increases ZJ by ∼ 1 for small aspect ratios, e.g. from                  packing-efficiency gains achieved by adding steps (3-4)
4.02 to 5.04 for α = 1. After going through a minimum                   to the particle-growth procedure appear to be associ-
in ∂ZJ /∂α at α = 1.1 which will be discussed further                   ated primarily with their ability to eliminate most of
below, the coordination numbers again increase rapidly                  the sizable voids present in the top-row packings. We
until reaching a plateau. Systems have ZJ > .995Ziso                    believe that the biased-SWAP moves favor formation of
over a very wide range of aspect ratios (1.3 . α . 2.0),                unjammed packings with high φ and few such voids, and
and over a narrower range of α & αmax (specifically,                    the TDOF moves performed at the end of the packing-
1.35 . α . 1.55), they have ZJ > .998Ziso. These val-                   generation runs allow formation of extra contacts that
ues were calculated without attempting to remove “rat-                  bring ZJ very close to (i.e. within less than 0.5% of) Ziso .
tlers.” Much as the results shown in Fig. 1 indicated a                    For larger aspect ratios, we find that the increas-
dramatic decrease in the free volume φv (α) despite the                 ing packing-efficiency gains highlighted in Fig. 1 are di-
relatively modest absolute increases in φJ (α), those re-               rectly associated with increasingly-long-ranged orienta-
ported in Fig. 2 (at least for α . 3) indicate an even                  tional order. Locally-nematic domains are present in the
                                                                                                                           5




FIG. 3. Snapshots of typical jammed states with α = 1.05, 1.3, 2, and 4 from left to right. The top (bottom) rows show states
prepared without (with) SWAP and TDOF moves. Particle colors vary from purple to red, in order of increasing σi .


jammed states for α & 3; their appearance coincides with        positional or orientational order illustrated in Fig. 3, none
the beginning of the drops in ZJ (α) illustrated in Fig.        of the packings discussed above are close to any of these
2. In packings generated using SWAP or TDOF moves,              three limiting behaviors. On the other hand, Figure 4
these domains look very similar to those found in ex-           also shows that SWAP and TDOF moves strongly affect
perimental “liquid glasses” formed by ellipsoidal colloids      all three of these structural metrics, and that – as was
with comparable aspect ratios [34–37]. In packings gen-         the case for φJ (α) and ZJ (α) – they do so in a strongly-
erated without these moves, the growth of such domains          α-dependent fashion.
with increasing α is far more gradual. Moreover, an ad-            Panel (a) shows that these moves can increase Ψ6
ditional distinguishing structural feature is already evi-      by up to ∼ 50%. This increase is consistent with the
dent by α = 4. In the top-row (but not the bottom-row)          formation of fractionated polycrystals discussed above,
packing, numerous large gaps between differently-ordered        but it only persists over a narrow range of aspect ratios
domains are visible. Thus the locally-nematic domains           (1 ≤ α . 1.15). We believe that the sharp drop in Ψ6
in packings generated using SWAP or TDOF moves, in              over the upper third of this range is responsible for the
addition to being larger, fit together better, as is evident    abovemenentioned minimum in ZJ (α) [Fig. 2].
from the huge reduction in space-wasting tip-to-side con-          Panel (b) shows that SWAP and TDOF moves in-
tacts visible in this snapshot.                                 crease S over the same range of α for which they increase
   Figure 4 quantitatively compares the packings’ multi-        Ψ6 , but only very slightly. S remains below .03 for all
scale structure using three additional metrics: the hex-        α . 1.4, supporting our above claim that the densest
atic order parameter Ψ6 [50], the nematic order pa-             packings with φJ (α) > .995φxtal remain amorphous. On
rameter S = h[3 cos2 (∆θij ) − 1]/2i (where ∆θij is the         the other hand, adding these moves makes ∂S/∂α sub-
orientation-angle difference between
                                   p ellipses i and j), and     stantially larger for all α & 1.3. As long as packings re-
the density fluctuations δφ =        hφ2 i − hφi2 . Here Ψ6     main effectively isostatic, i.e. for 1.3 . α . 2, the result-
captures orientational ordering on the nearest-neighbor         ing differences in S are not associated with the formation
scale, while S snd δφ respectively capture intermediate-        of sizable locally-nematic domains. Instead they appear
range orientational and positional order over regions           to be associated with the moves’ promotion of side-to-
of a size corresponding to a typical particle’s first           side contacts, which are more space-efficient than tip-to
three coordination shells.[51] Since the optimally-dense        side contacts. Only for α & 3, when S exceeds ∼ 0.3
monodisperse-ellipse crystal with φ = φxtal is simply the       do such liquid-glass-like domains become apparent (Fig.
triangular lattice affinely stretched by a factor α along       3). Their appearance coincides with the beginning of the
one direction [48], it has Ψ6 (α) = 1−O(α2 ) for α−1 ≪ 1,       rapid increase in packing-efficiency gain and decrease in
S = 1 for all α > 1, and α-independent δφ. As might             ZJ (α) shown in Figs. 1-2.
have been expected from the apparent lack of long-range            Panel (c) shows that (i) adding SWAP and TDOF
                                                                                                                            6

                                                  0.5
         0.15                           (a)                                                0.04
                                                  0.4
          0.1                                     0.3




                                                                                      δϕ
    Ψ6




                                              S
                                                  0.2                                      0.03
         0.05                                     0.1
                                                   0                            (b)                                   (c)
           0                                                                               0.02
            1          2       3    4     5         1         2        3    4     5            1     2       3    4     5
                           α                                      α                                      α


FIG. 4. Hexatic order Ψ6 [50], local nematic order S, and local density fluctuations δφ of systems prepared with and without
SWAP and TDOF moves. All quantities were calculated as described in Ref. [5]. Colors are the same as in Figs. 1-2.


moves substantially reduces δφ for all α, and (ii) the            oriented domains [5]. Because the nature of these traps
fractional reductions in δφ closely track the packing-            is strongly α-dependent, so is the packing-efficiency gain.
efficiency gains shown in Fig. 1. δφ(α) initially decreases          Analogous effects have been extensively studied for
with increasing α, as the fractionated-polycrystal-plus-          disk and sphere packings [21–30], but had not previ-
dislocation-core structure evident for α . 1.15 gradually         ously been explored for anistropic particles. Ref. [18]
gives way to the homogeneous disordered structure evi-            showed that decreasing the particle growth rate G̃ in an
dent for α ≃ αmax . Its broad minimum, i.e. δφ(α) < .022          adaptive-shrinking-cell (ASC)-based algorithm [52] pro-
over the range 1.25 . α . 2.1, closely corresponds to             duces denser, better-ordered packings for a wide variety
the range of aspect ratios over which packings are ef-            of particle shapes: rhombi, obtuse scalene and curved tri-
fectively isostatic (Fig. 2). For larger aspect ratios, it        angles, lenses, “ice cream cones” and “bowties.” It also
increases again, but at a slower rate than in packings gen-       explained these effects in terms of kinetics, but since it
erated without these moves, consistent with the moves’            considered only monodisperse systems, did not explore
tendency to make the nematic domains fit together better          their connection to SWAP or TDOF. Since employing
(Fig. 3).                                                         standard SWAP moves speeds up dynamics by many
   Finally we briefly discuss the relative contributions of       orders of magnitude in disordered hard-sphere systems
SWAP and TDOF moves to producing the abovemen-                    above their glass transition densities [22], we expect that
tioned differences. We performed separate runs that               employing the biased SWAP moves discussed above can
omitted growth cycle step (4), and found that the result-         be a far more effective method for bypassing anisotropic-
ing φJ (α) were only ∼ 0.1% lower, the ZJ (α) were sub-           particle glasses’ kinetic traps than simply decreasing G̃.
stantially lower, the Ψ6 (α) and S(α) did not change sig-            Our results show that all previous studies of polydis-
nificantly, and the δφ(α) were slightly larger. All trends        perse ellipse jamming [2–8] have failed to access these
suggest that the main effect of TDOF moves as employed            systems’ most-stable disordered jammed states. The ul-
in this study is adding up to 1 contact per particle at the       tradense packings obtained here presumably have vibra-
end of the packing-generation runs.                               tional properties which are substantially different from
                                                                  their less-dense counterparts; for example, their far-
                                                                  higher ZJ (α) suggests that they will have far fewer quar-
          DISCUSSION AND CONCLUSIONS                              tic modes [6–8]. Moreover, the effectively-isostatic pack-
                                                                  ings for α ≃ αmax may have ideal-glass like vibrational
   All of the abovementioned structural differences be-           and thermal properties which are the elliptical analogues
tween the ultradense ellipse packings discussed above and         of those explored in Refs. [29, 30]. Followup studies that
those reported in previous studies [2–8] may have a sin-          employ soft rather than hard ellipses could explore these
gle, common explanation. We hypothesize that they all             issues.
arise because including biased-SWAP and TDOF moves                   Here we have employed a “maximalist” biased-SWAP
in the packing-generation procedure allows systems to es-         + TDOF approach aimed at generating packings which
cape kinetic traps [18]. In other words, including these          are as dense as possible while remaining amorphous on
moves allows systems to bypass the slow dynamics which            large length scales. However, we emphasize that our
otherwise lead to jamming at much lower densities. For            method can be generalized to produce packings with any
low α, escaping the traps allow systems to form frac-             density between those reported in Ref. [5] and those re-
tionated polycrystals. For intermediate α, it allows sys-         ported here, simply by varying the frequency with which
tems to access the slow processes by which small voids            the SWAP and TDOF moves are applied. For exam-
are eliminated, and form very-stable isostatic packings,          ple, varying the fraction of particles for which SWAP
For large α, it allows systems to form much greater lo-           moves are attempted during step (3), or only performing
cal nematic order and shrink the large voids which are            step (3) periodically, should allow one to systematically
otherwise present at the boundaries between differently-          study how jammed ellipse packings are affected by sample
                                                                                                                                7

preparation protocol. Such studies could improve our un-           [14] Y. Jiao and S. Torquato, “Maximally random jammed
derstanding of multiple real-world systems composed of                  packings of platonic solids; hyperuniform long-range cor-
anistropic particles whose shapes are sufficiently ellipse-             relations and isostaticity,” Phys. Rev. E 84, 041309
                                                                        (2011).
like, including liquid glasses formed by ellipsoidal colloids
                                                                   [15] P. F. Damasceno, M. Engel, and S. C. Glotzer, “Predic-
[34–37], active cell populations [53], and potentially even             tive self-assembly of polyhedra into complex structures,”
the trisnapthylbenzenes which have attracted great inter-               Science 337, 453 (2012).
est in recent years because some of them form anisotropic          [16] H. M. Jaeger, “Celebrating soft matter’s 10th anniver-
quasi-ordered glasses when vapor-deposited [38–41].                     sary: Toward jamming by design,” Soft Matt. 11, 12
                                                                        (2015).
   We dedicate this paper to Mark Ediger for his numer-            [17] R. S. Hoy, “Jamming of semiflexible polymers,” Phys.
ous contributions to our understanding of supercooled                   Rev. Lett. 118, 068002 (2017).
liquids and glasses, and thank Madelaine Y. Payne for              [18] C. E. Maher, F. H. Stillinger, and S. Torquato, “Kinetic
                                                                        frustration effects on dense two-dimensional packings of
helpful discussions. This material is based upon work
                                                                        convex particles and their structural characteristics,” J.
supported by the National Science Foundation under                      Phys. Chem. B 125, 2450 (2021).
Grant Nos. DMR-2026271 and DMR-2419261.                            [19] T. S. Grigera and G. Parisi, “Fast monte carlo algorithm
                                                                        for supercooled soft spheres,” Phys. Rev. E 63, 045102
                                                                        (2001).
                                                                   [20] A. Ninarello, L. Berthier, and D. Coslovich, “Models
                                                                        and algorithms for the next generation of glass transition
  ∗
     rshoy@usf.edu                                                      studies,” Phys. Rev. X 7, 021039 (2017).
 [1] A. Donev, I. Cisse, D. Sachs, E. A. Variano, F. H. Still-     [21] L. Berthier, P. Charbonneau, Y. Jin, G. Parisi,
     inger, R. Connelly, S. Torquato, and P. M. Chaikin,                B. Seoane,       and F. Zamponi, “Growing timescales
     “Improving the density of jammed disordered packings               and lengthscales characterizing vibrations of amorphous
     using ellipsoids,” Science 303, 990 (2004).                        solids,” Proc. Nat. Acad. Sci. 113, 8397 (2016).
 [2] G. Delaney, D. Weaire, S. Hutzler, and S. Murphy, “Ran-       [22] L. Berthier, D. Coslovich, A. Ninarello, and M. Ozawa,
     dom packing of elliptical disks,” Phil. Mag. Lett. 85, 89          “Equilibrium sampling of hard spheres up to the jam-
     (2005).                                                            ming density and beyond,” Phys, Rev. Lett. 116, 238002
 [3] A. Donev, R. Connelly, F. H. Stillinger, and S. Torquato,          (2016).
     “Underconstrained jammed packings of nonspherical             [23] M. Ozawa, L. Berthier, and D. Coslovich, “Exploring
     hard particles: Ellipses and ellipsoids,” Phys. Rev. E 75,         the jamming transition over a wide range of critical den-
     051304 (2007).                                                     sities,” SciPost Phys. 3, 027 (2017).
 [4] K. VanderWerf, W. Jin, M. D. Shattuck, and C. S.              [24] M. Ozawa, L. Berthier, G. Biroli, A. Rosso, and G. Tar-
     O’Hern, “Hypostatic jammed packings of frictionless                jus, “Random critical point separates brittle and ductile
     nonspherical particles,” Phys. Rev. E 97, 012909 (2018).           yielding transitions in amorphous materials,” Proc. Nat.
 [5] S. L. Rocks and R. S. Hoy, “Structure of jammed ellipse            Acad. Sci. 115, 6656 (2018).
     packings over a wide range of aspect ratios,” Soft Matt.      [25] L.-J. Wang, A. Ninarello, P.-F. Guan, L. Berthier,
     19, 5701 (2023).                                                   G. Szamel, and E. Flenner, “Low-frequency vibrational
 [6] M. Mailman, C. F. Schreck, C. S. O’Hern,               and         modes of stable glasses,” Nature Comm. 10, 26 (2019).
     B. Chakraborty, “Jamming in systems composed of fric-         [26] C. Scalliet, L. Berthier, and F. Zamponi, “Nature of exci-
     tionless ellipse-shaped particles,” Phys. Rev. Lett. 102,          tations and defects in structural glasses,” Nature Comm.
     255501 (2009).                                                     10, 5102 (2019).
 [7] C. F. Schreck, N. Xu, and C. S. O’Hern, “A comparison         [27] C. Scalliet, B. Guiselin, and L. Berthier, “Thirty mil-
     of jamming behavior in systems composed of dimer- and              liseconds in the life of a supercooled liquid,” Phys. Rev.
     ellipse-shaped particles,” Soft Matt. 6, 2960 (2010).              X 12, 041028 (2022).
 [8] C. F. Schreck, M. Mailman, B. Chakraborty, and C. S.          [28] G. Kapteijns, W. Ji, C. Brito, M. Wyart, and E. Lerner,
     O’Hern, “Constraints and vibrations in static packings of          “Fast generation of ultrastable computer glasses by min-
     ellipsoidal particles,” Phys. Rev. E 85, 061305 (2012).            imization of an augmented potential energy,” Phys. Rev.
 [9] A. P. Philipse, “The random contact equation and its               E 99, 012106 (2019).
     implications for (colloidal) rods in packings, suspensions,   [29] V. F. Hagh, S. R. Nagel, A. J. Liu, M. L. Manning, and
     and anisotropic powders,” Langmuir 12, 1127 (1996).                E. I. Corwin, “Transient learning degrees of freedom for
[10] S. R. Williams and A. P. Philipse, “Random packings                introducing function in materials,” Proc. Natl. Acad. Sci.
     of spheres and spherocylinders simulated by mechanical             119, e2117622119 (2022).
     contraction,” Phys. Rev. E 67, 051301 (2003).                 [30] P. Morse V. M. Bolton-Lum,                 R. C. Den-
[11] K. Desmond and S. V. Franklin, “Jamming of three-                  nis,     “The Ideal Glass E. Corwin,                  and
     dimensional prolate granular materials,” Phys. Rev. E              https://arxiv.org/pdf/2404.07492       the    Ideal   Disk
     73, 031306 (2006).                                                 Packing in Two Dimensions”,.
[12] T. Marschall and S. Teitel, “Compression-driven jam-          [31] S. Torquato, T. M. Truskett, and P. G. Debenedetti,
     ming of athermal frictionless spherocylinders in two di-           “Is random close packing of spheres well defined?” Phys.
     mensions,” Phys. Rev. E 97, 012905 (2018).                         Rev. Lett. 84, 2064 (2000).
[13] Y. Jiao, F. H. Stillinger, and S. Torquato, “Distinctive      [32] A. Donev, S. Torquato, F. H. Stillinger, and R. Connelly,
     features arising in maximally random jammed packings               “Jamming in hard sphere and disk packings,” J. App.
     of superballs,” Phys. Rev. E 81, 041304 (2010).                    Phys. 95, 989 (2004).
                                                                                                                                8

[33] P. Chaudhuri, L. Berthier, and S. Sastry, “Jamming                packings,” J. Stat. Phys. 64, 501 (1991).
     transitions in amorphous packings of frictionless spheres    [43] C. S. O’Hern, L. E. Silbert, A. J. Liu, and S. R. Nagel,
     occur over a continuous range of volume fractions,” Phys.         “Jamming at zero temperature and zero applied stress:
     Rev. Lett. 104, 165701 (2010).                                    The epitome of disorder,” Phys. Rev. E 68, 011306
[34] Z. Zheng, F. Wang, and Y. Han, “Glass transitions                 (2003).
     in quasi-two-dimensional suspensions of colloidal ellip-     [44] X. Zheng and P. Palffy-Muhoray, “Distance of closest ap-
     soids,” Phys. Rev. Lett. 107, 065702 (2011).                      proach of two arbitrary hard ellipses in two dimensions,”
[35] C. K. Mishra, A. Rangarajan, and R. Ganapathy, “Two-              Phys. Rev. E 75, 061709 (2007).
     step glass transition induced by attractive interactions     [45] Success rates only become small when either the ordering
     in quasi-two-dimensional suspensions of ellipsoidal parti-        of the g̃i amongst the N particles parallels the ordering
     cles,” Phys. Rev. Lett. 110, 188301 (2013).                       of their σi , or when most of the g̃i drop to zero.
[36] J. Roller, J. D. Geiger, M. Voggenreiter, J.-M. Meijer,      [46] A. Donev, S. Torquato, and F. H. Stillinger, “Neigh-
     and A. Zumbusch, “Formation of nematic order in 3d                bor list collision-driven molecular dynamics simulation
     systems of hard colloidal ellipsoids,” Soft Matt. 16, 1021        for nonspherical hard particles. I. Algorithmic details,”
     (2020).                                                           J. Comp. Phys. 202, 737 (2005).
[37] J. Roller, A. Laganapan, J.-M. Meijer, M. Fuchs, and         [47] S. Kim and S. Hilgenfeldt, “Exceptionally dense and re-
     A. Zumbusch, “Observation of liquid glass in suspen-              silient critically jammed polydisperse disk packings,” Soft
     sions of ellipsoidal colloids,” Proc. Nat. Acad. Sci. 118,        Matter 20, 5598 (2024).
     2018072118 (2021).                                           [48] F. Toth, “Some packing and covering theorems,” Acta
[38] T. Liu, K. Cheng, E. Salami-Ranjbaran, F. Gao, C. Li,             Sci. Math. Szeged. 12/A, 62 (1950).
     X. Tong, Y.-C. Lin, Y. Zhang, W. Zhang, L. Klinge, P. J.     [49] L. Onsager, “The effects of shape on the interaction of
     Walsh, and Z. Fakhraai, “The effect of chemical struc-            colloidal particles,” Ann. New York Acad. Sci. 51, 627
     ture on the stability of physical vapor deposited glasses         (1949).
     of 1,3,5-triarylbenzene,” J. Chem. Phys. 143, 084506         [50] E. P. Bernard and W. Krauth, “Two-step melting in two
     (2015).                                                           dimensions: First-order liquid-hexatic transition,” Phys.
[39] T. Liu, A. L. Exarhos, E. C. Alguire, F. Gao, E. Salami-          Rev. Lett. 107, 155704 (2011).
     Ranjbaran, K. Cheng, T. Z. Jia, J. E. Subotnik, P. Walsh,    [51] More specifically, as described in Ref. [5], S was calcu-
     J. M. Kikkawa, and Z. Fakhraai, “Birefringent sta-                lated using each particles’ 18 nearest neighbors, while δφ
     ble glass with predominantly isotropic molecular orien-           was calculated using N randomly positioned circular win-
     tation,” Phys. Rev. Lett. 119, 095502 (2017).                     dows of a radius R chosen to make the average window
[40] A. Gujral, J. Goomez, S. G. Ruan, M. F. Toney, H. Bock,           contain 19 particles.
     L. Yu, and M. D. Ediger, “Vapor-deposited glasses with       [52] S. Atkinson, Y. Jiao, and S. Torquato, “Maximally dense
     long-range columnar crystalline order,” Chem. Mat. 29,            packings of two-dimensional convex and concave noncir-
     9110 (2017).                                                      cular particles,” Phys. Rev. E 86, 031302 (2011).
[41] R. Teerakapibal, C. Huang, A. Gujral, M. D. Ediger, and      [53] V. Leech, F. N. Kenny, S. Marcotti, T. J. Shaw, B. M.
     L. Yu, “Organic glasses with tunable crystalline order,”          Stramer, and A. Manhart, “Derivation and simula-
     Phys. Rev. Lett. 120, 055502 (2018).                              tion of a computational model of active cell populations:
[42] B. D. Lubachevsky, F. H. Stillinger, and E. N. Pin-               How overlap avoidance, deformability, cell-cell junctions
     son, “Disks vs spheres: contrasting properties of random          and cytoskeletal forces affect alignment,” PLOS Comput.
                                                                       Biol. 20, e1011879 (2024).
