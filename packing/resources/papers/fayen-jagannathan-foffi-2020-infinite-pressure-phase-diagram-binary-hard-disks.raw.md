                                                 Infinite-pressure phase diagram of binary mixtures of (non)additive hard disks
                                                           Etienne Fayen,1 Anuradha Jagannathan,1 Giuseppe Foffi,1, a) and Frank Smallenburg1, b)
                                                           Université Paris-Saclay, CNRS, Laboratoire de Physique des Solides, 91405 Orsay,
                                                           France
                                                           (Dated: 29 May 2020)
                                                           One versatile route to the creation of two-dimensional crystal structures on the nanometer to micrometer
                                                           scale is the self-assembly of colloidal particles at an interface. Here, we explore the crystal phases that can
                                                           be expected from the self-assembly of mixtures of spherical particles of two different sizes, which we map
                                                           to (additive or non-additive) hard-disk mixtures. We map out the infinite-pressure phase diagram for these
                                                           mixtures, using Floppy Box Monte Carlo simulations to systematically sample candidate crystal structures
                                                           with up to 12 disks in the unit cell. As a function of the size ratio and number ratio of the two species of
arXiv:2003.08889v2 [cond-mat.soft] 28 May 2020




                                                           particles, we find a rich variety of periodic crystal structures. Additionally, we identify random tiling regions
                                                           to predict random tiling quasicrystal stability ranges. Increasing non-additivity both gives rise to additional
                                                           crystal phases and broadens the stability regime for crystal structures involving a large number of large-small
                                                           contacts, including random tilings. Our results provide useful guidelines for controlling the self-assembly of
                                                           colloidal particles at interfaces.


                                                 I.   INTRODUCTION                                               behavior of mixtures of hard disks provides useful in-
                                                                                                                 sights into a wide range of (quasi-)two-dimensional self-
                                                    The self-assembly of colloidal particles into organized      assembly processes. Finally, the existence and control of
                                                 crystals provides an elegant and versatile route for the        random tiling phases can help to rationalize the existence
                                                 creation of materials with well-controlled structure on         and behaviour of quasicrystalline self-assembly12 – a new
                                                 the nanometer to micrometer scale. By varying e.g.              emerging field in soft matter11,21,22 .
                                                 the shape, size distribution, and surface properties of            In this work, we explore the crystal structures formed
                                                 the building blocks, a stunning variety of crystal struc-       by mixtures of hard disks of two different sizes, in 2D,
                                                 tures can be obtained1–4 . Even in the seemingly sim-           considering both additive and non-additive mixtures. A
                                                 ple case of spherical particles self-assembling at a two-       phase diagram for additive i.e. non-overlapping hard
                                                 dimensional interface or substrate, mixing particles of dif-    disks, at infinite pressure has been proposed by Likos
                                                 ferent sizes has been demonstrated to lead to a variety of      and Henley19 , based on a large set of candidate struc-
                                                 crystalline5–10 and even quasicrystalline11,12 structures.      tures built explicitly using clever heuristics and defor-
                                                    When spherical particles self-assemble at an interface,      mation arguments. However, since there are an infinite
                                                 it can be useful to consider an effective problem where         number of possible crystal structures, it is impossible in
                                                 they essentially act as two-dimensional disks, forming          practice to make sure that no phase of even higher com-
                                                 a two-dimensional ordered structure8,13 . Which crystal         pacity has been missed. Here, we systematically detect
                                                 structure is selected for self-assembly depends on the (ef-     candidate crystal structures using so-called Floppy Box
                                                 fective) interactions between these disks. In the simplest      Monte Carlo simulations23,24 . While this method still
                                                 scenario – a single species of particles interacting via a      inevitably leaves room for missed crystal phases, we find
                                                 short-ranged interaction potential – the inevitable out-        both new stable crystals and several better-packed defor-
                                                 come is a hexagonal lattice. However, mixing two types          mations that were not considered in earlier work19 . This
                                                 of particles with differing interactions already leads to       leads to an updated phase diagram, which also includes
                                                 an impressive complexity. Binary systems with soft re-          two new regions where random tiling phases (and the
                                                 pulsive interactions, due to e.g. charge or dipolar forces,     associated quasicrystals) are expected. We then explore
                                                 stabilize a wide variety of binary crystal structures (see      how non-additivity, i.e. allowing the possibility that disks
                                                 e.g.14–18 ). Even simple hard disks, with no interactions       may overlap, affects the phase diagram. As explained in
                                                 beyond a hard-core exclusion, are predicted to have a           the next section, non additivity allows to mimic possi-
                                                 rich and varied phase diagram19,20 , containing periodic        ble 3D effects that may occur when different types of
                                                 crystals as well as lattice gases and random tilings. More-     colloidal particles with different sizes self-assemble at an
                                                 over, as these phases are all expected to be stable in the      interface and float at different levels (see Fig. 1). We find
                                                 limit of high packing fractions, they will be relevant for      three new crystal phases which are only stable for finite
                                                 any high-density system where the interactions include a        non-additivity, and we map out how the stability of the
                                                 hard repulsive core. As such, understanding the phase           other structures shifts as non-additivity increases. Our
                                                                                                                 results show that non-additivity has a drastic effect on
                                                                                                                 the phase diagram, strongly increasing the stability range
                                                                                                                 of crystals (and quasicrystals) that have a large number
                                                 a) Electronic mail: giuseppe.foffi@u-psud.fr                    of contacts between large and small disks.
                                                 b) Electronic mail: frank.smallenburg@u-psud.fr
                                                                                                                   In the remainder of this paper, we first present the
                                                                                                                                                                      22

                                                                                  by introducing
                                                                                 large   and small some   disks todegree
                                                                                                                      overlapof negative
                                                                                                                                   slightly. additivity
                                                                                                                                                 This is achievedas dis-
                                                                                 by   introducing
                                                                                  cussed    above. some   Fromdegree
                                                                                                                   simpleofgeometrical
                                                                                                                                 negative additivity            as dis-
                                                                                                                                                   considerations,
                                                             σLS                 cussed
                                                                                  one canabove.
                                                                                              show that   From    simple
                                                                                                              if the          geometrical
                                                                                                                        floating     levels of considerations,
                                                                                                                                                   the two species
Interface


                z                                                                one
                                                                                  are can
                                                                                       offsetshowby athat    if the
                                                                                                          distancep floating        levels of the two
                                                                                                                        z, the non-additivity                  species
                                                                                                                                                          parameter
                                                                                 are   offsetby
                                                                                  is given      by ∆ a distance
                                                                                                        = 1 − z,1 the           2 /(σ + can
                                                                                                                         − 4zsituation        σL )2be    mapped tof
                                                                                                                                                      . Particles
                                                                                                                                       S

                     σLS
                                                                                 athe
                                                                                    system
                                                                                        sameofspecies,
                                                                                                   non-additive
                                                                                                              since hardthey disks
                                                                                                                                lie atwith the asamenon additivity
                                                                                                                                                           level with
                                                                                 parameter
                                                                                  respect to the  given    by Eq 3.are not allowed to overlap: their
                                                                                                        interface,
FIG. 1.
      1. Hard
          Hard disks
                disks can
                       can be
                           be interpreted
                              interpreted as
                                                                                  minimal approach distances         s are unchanged.
FIG.                                      as hard
                                             hard spheres
                                                    spheres floating
                                                             floating                                                                         z2
at an
    an interface.
       interface. IfIf the
                       the two
                           two species
                                species do                                           We note that other sources of4 non-additivity                              can be
at                                      do not
                                            not float
                                                 float at
                                                       at the
                                                           the same
                                                                same                                    ∆=1− 1−                                 2                   (3)
level (left
level (left figure),
            figure), the
                      the corresponding
                          corresponding 2D2D ”top
                                              ”top view”
                                                     view” exhibits
                                                            exhibits              readily present in real-world(1self-assembling    + q) σL2                  systems.
overlap between
overlap  between large
                   large and
                          and small
                               smalldisks
                                     disks(right
                                           (rightfigure).
                                                   figure).The non-               Particles that interact via softer interactions (due to
additivity parameter ∆, and hence σLS are related to the                          charge,    dipolar
                                                                                     Particles     of theinteractions,
                                                                                                            same species,      ligand
                                                                                                                                  since coatings,
                                                                                                                                           they lie atetc.),       may,
                                                                                                                                                            the same
offset of the floating levels z by Eq. 3.                                         depending        on thetoverall        packing are  fraction,      favor to  configu-
                                                                                 level   with respect           the interface,             not allowed            over-
(non-)additive hard disks model (Section II). In Section                          rations
                                                                                 lap:       where
                                                                                        their          the favored
                                                                                                 minimal      approach   distance
                                                                                                                              distancesbetween       different pairs
                                                                                                                                              are unchanged.
III we outline the numerical simulations used to sample                           of We
                                                                                     particles
                                                                                           note that other sources of non-additivity interac-
                                                                                                   behaves      non-additively.          Non-additive          can be
(non-)additive hard disks model (Section II). In Section                          tions  have     been shown        to significant        impact the phase           be-
candidate structures and construct the phase diagrams.                           readily present           in real-world          self-assembling            systems.
III we outline the numerical simulations used to sample                           havior    of  mixtures       of  particles     25–29
                                                                                                                                        ,  and    hence     are   likely
Sections IV and V describe the main features of the phase                        Particles that interact via softer interactions (due to
candidate structures and construct the phase diagrams.                            to be andipolar
                                                                                               important        factor in ligand
                                                                                                                              predicting        the self-assembly
diagrams of binary mixtures of additive and non-additive                         charge,                  interactions,                  coatings,       etc.), may,
Sections IV and V describe the main features of the phase                         of hard-disk
hard disks respectively. Finally, we discuss our findings                        depending        onmixtures.
                                                                                                       the overall packing fraction, favor configu-
diagrams of binary mixtures of additive and non-additive                             In this     work,
and                                                                              rations    where     the we     focusdistance
                                                                                                            favored         on findingbetween the different
                                                                                                                                                     stable crystal
                                                                                                                                                                  pairs
hardconclude   the paper in
      disks respectively.   SectionweVI.
                          Finally,    discuss our findings                        structures
                                                                                 of  particles in      the limit
                                                                                                   behaves            of high pressures.
                                                                                                               non-additively.          Non-additive  In this     limit,
                                                                                                                                                              interac-
and conclude the paper in Section VI.                                             the most
                                                                                 tions   havestable
                                                                                                 been shownphase to forsignificant
                                                                                                                          any givenimpact combinationthe phase of com-
                                                                                                                                                                    be-
II.         (NON)ADDITIVE HARD-DISK MODEL                                         position
                                                                                 havior    ofxmixtures
                                                                                                 S , size ratio    q, and non-additivity
                                                                                                              of particles      25–29
                                                                                                                                       , and hence     parameter
                                                                                                                                                           are likely  ∆
                                                                                  is the  best-packing        phase:       the  one   with
                                                                                 to be an important factor in predicting the self-assembly     the   lowest     volume
II.         (NON)ADDITIVE HARD-DISK MODEL
                                                                                  perhard-disk
                                                                                 of     particle v.  mixtures.
    We consider, in two dimensions, mixtures of large and
                                                                                     In this work, we focus on finding the stable crystal
small
    We hard     disksin(HD)
         consider,               with diameters
                           two dimensions,          σL andofσlarge
                                                mixtures         S respec-
                                                                        and      structures in the limit of high pressures. In this limit,
tively.   Suchdisks
 small hard       mixtures
                        (HD) are withcharacterised
                                        diameters σLbyand   theσSsize  ratio
                                                                    respec-       III. most
                                                                                 the     METHODS
                                                                                               stable phase for any given combination of com-
of  the large
 tively.   Such and     small are
                   mixtures      disks   q = σS /σL by
                                     characterised     andthe thesize
                                                                   number
                                                                       ratio     position xS , size ratio q, and non-additivity parameter ∆
fraction    of small    disks
 of the large and small disks   x S =   N   /(N   +N
                                         qS= σSL/σL andS ),  with  NL and
                                                              the number         is the
                                                                                     To best-packing
                                                                                          construct a phase   phase:diagram,
                                                                                                                          the one with        the lowest
                                                                                                                                      one first     needs to   volume
                                                                                                                                                                  know
N  S the number
 fraction   of small of    large
                        disks   xSand
                                    = Nsmall
                                          S /(NLdisks
                                                  +NSrespectively.
                                                         ), with NL and          per   particlethat
                                                                                  the phases        v. compete for stability, i.e. candidate pack-
 NSThetheinteraction
            number ofpotentials
                            large and between      tworespectively.
                                         small disks    disks uij (i, j =
L orThe S interaction
           for large and       small disks
                          potentials          respectively)
                                        between    two disks auijdistance
                                                                     (i, j =      ings of disks with a given size ratio and composition.
rL apart,
    or S foris given    by small disks respectively) a distance
                large and                                                            In order to systematically generate candidate crystal
                                                                                 III. METHODS
 r apart, is given by                                                             structures, we use the so-called Floppy-box Monte Carlo
                                  (
                                                                                  (FBMC) simulation method23 . In this method, we sim-
                                   (∞ if r < σij                                     To construct         a phase of  diagram,       one    first
                     uij (r) = ∞ if r < σ                                 (1)     ulate   a small number                  particles     (up     to needs
                                                                                                                                                     12) intoaknow peri-
                     uij (r) = 0            otherwise.
                                                    ij                           the   phases     that    compete      for  stability,     i.e.  candidate       pack-it
                                                                          (1)     odic box at slowly increasing pressures and compress
                                    0       otherwise.                           ings
                                                                                  untilofa disks
                                                                                             densewith       a given
                                                                                                        packing           size ratio and
                                                                                                                     is reached.                composition. all
                                                                                                                                          To accommodate
Where σSS = σS and σLL = σL . The interspecies diam-                                 In order
                                                                                  unit-cell        to systematically
                                                                                               shapes,      Monte Carlogenerate  moves are    candidate
                                                                                                                                                   includedcrystalwhich
 Where
eter       σSS = σasS and σLL = σL . The interspecies diam-
       is defined                                                                structures,
                                                                                  deform the we         use the so-called
                                                                                                   simulation       box. At        Floppy-box
                                                                                                                                  the   end    of  theMonte      Carlo
                                                                                                                                                         simulation,
 eter is defined as                                                              (FBMC)                                      23
                                                 σS + σL                          a quench simulation
                                                                                                 to infinite method
                                                                                                                 pressure .is In       this method,
                                                                                                                                    performed                 we sim-
                                                                                                                                                       to freeze     the
                   σLS = σSL = (1 − ∆) σS + σL                            (2)    ulate
                                                                                  configuration, which is then taken as a candidatea struc-
                                                                                          a  small     number       of   particles     (up     to   12)   in      peri-
                   σLS = σSL = (1 − ∆)              2                     (2)    odic
                                                    2                             ture.box at slowly increasing pressures and compress it
where ∆ is the so-called non-additivity parameter. When                          until   a dense
                                                                                     In our            packing we
                                                                                                simulations,        is reached.
                                                                                                                          consideredToallaccommodate
                                                                                                                                                 possible compo-     all
∆where
    = 0,∆the is model
                the so-called
                          is callednon-additivity
                                      additive andparameter.         When
                                                       the disks behave          unit-cell    shapes,       Monte     Carlo      moves
                                                                                  sitions with up to 12 disks in the simulation box and at  are   included       which
 ∆ =standard
like    0, the modelhardis disks
                              called that
                                      additive   and overlap.
                                             cannot   the disks behave
                                                                    In this      deform
                                                                                  least one thelarge
                                                                                                   simulation
                                                                                                         and onebox.  small Atdisk.
                                                                                                                                 the endFor of    the simulation,
                                                                                                                                               larger    numbers of
 like standard
paper     we will hard
                     studydisks      that ofcannot
                               the case              overlap.
                                               negative             In this
                                                          additivity,     i.e.   aparticles,
                                                                                     quench to   theinfinite
                                                                                                       methodpressure
                                                                                                                    becomesis less  performed
                                                                                                                                          reliable,toasfreeze
                                                                                                                                                            the num-the
∆ > 0 that will be implied for the rest of the paper. i.e.
 paper    we   will  study     the  case   of  negative   additivity,            configuration,         which    is  then     taken    as
                                                                                  ber of possible arrangements increases very rapidly with   a  candidate        struc-
 ∆ However,
    > 0 that will  2D be (orimplied    for the
                                quasi-2D)       rest of the paper.
                                              superlattices      are often       ture.
                                                                                  the number of particles. Nonetheless, this has proven
    However,       2D    (or    quasi-2D)     superlattices
formed out of 3D spherical particles, self-assembling           are often  at     toInbeour    simulations,
                                                                                          an effective       methodwe considered           all possible
                                                                                                                           for systematically                 compo-
                                                                                                                                                        finding     unit
 formed
an          out 5–10
     interface    of 3D
                      . In spherical
                             principle, particles,
                                          large  andself-assembling
                                                       small   nanoparti-  at    sitions    with    up    to 12   disks     in  the   simulation
                                                                                  cells of complex crystal structures in a large variety                box     and at of
                 5–10
 an interface
cles                  . In principle,
      may have different          surfacelarge   and small
                                            properties,        nanoparti-
                                                          leading    to dif-     least
                                                                                  systemsone24,30–36
                                                                                               large and , as one
                                                                                                               longsmall
                                                                                                                       as the disk.
                                                                                                                                  unitFor celllarger
                                                                                                                                                 is not numbers
                                                                                                                                                            too large.of
 cles  may   have   different     surface   properties,
ferent wetting angles with the solvent. As a result,      leading    to dif-
                                                                          the    particles,
                                                                                  Since the the numbermethod       becomesinless
                                                                                                             of particles           thereliable,
                                                                                                                                          box is small,as thesimula-
                                                                                                                                                                  num-
 ferent
two       wetting
       species   may angles
                         float with   the solvent.
                                 at different   levels As
                                                        with a result,
                                                                respectthe to    ber   of  possible      arrangements          increases
                                                                                  tions are fast, allowing us to produce at least 50 candidatevery     rapidly     with
 two interface.
the    species may       float cases,
                    In such      at different   levels with
                                        small particles     canrespect
                                                                  partiallyto    the    number       of   particles.       Nonetheless,
                                                                                  structures for each composition and size ratio we inves-       this   has     proven
 the interface. In such cases, small particles can partially                     to be an effective method for systematically finding unit
slide   below (or above) the large ones, as illustrated in                        tigated. Note that typically, the most efficiently packed
 slide below (or above) the large ones, as illustrated in                        cells of complex crystal structures in a large variety of
Fig. 125   . This 3D effect can be accounted for by allowing                      crystal structures are found multiple times in these 50
 Fig. 125 . This 3D effect can be accounted for by allowing                      systems24,30–36 , as long as the unit cell is not too large.
large and small disks to overlap slightly. This is achieved                       independent runs.
                                                                                                                                                   3

                                      0.05                                                              Common tangent
                                                                                                        Simulation points
                                      0.04
                                                                                                        Stable phases
                (v − vHex (xS ))/σL
                                  2
                                      0.03


                                      0.02


                                      0.01


                                      0.00


                                             0.0      0.2              0.4                0.6                0.8                 1.0
                                                                                xS




                                                                                                                        HexS


                                               HexL
                                                             T1                                       S2

FIG. 2. Common tangent construction at size ratio q = 0.23. On the vertical axis, we subtracted the volume per particle
FIG. 2. Common tangent construction at size ratio q = 0.23. On the vertical axis, we subtracted the volume per particle
vHex (xS ) of the coexistence of hexagonal phases of large and small disks. Blue dots represent candidate crystal structures found
vHex (x ) of the coexistence of hexagonal phases of large and small disks. Blue dots represent candidate crystal structures found
by 50 SFBMC simulations for each of the 66 compositions LiSj with i, j ≥ 1 and i + j ≤ 12. Red dots correspond to stable
by 50 FBMC simulations for each of the 66 compositions LiSj with i, j ≥ 1 and i + j ≤ 12. Red dots correspond to stable
pure crystals and arrows point to snapshots of the FMBC output (unit cells are repeated 9 times). The red line indicates, for
pure crystals and arrows point to snapshots of the FMBC output (unit cells are repeated 9 times). The red line indicates, for
all intermediate fraction of small disks, the volume per particle of the stable coexistence.
all intermediate fraction of small disks, the volume per particle of the stable coexistence.


    Equipped with a set of candidate structures, we used                       straight line that joins T1 and HexL points gives the
Since the number of particles in the box is small, simula-                    a common tangent construction as depicted                   in Fig. 2
 an approach that is analogous to a common tangent con-                        volume per particle of their coexistence for all composi-
tions are fast, allowing us to produce at least 50 candidate                  for q = 0.23. For monodisperse disks, the best pack-
 struction to determine the relative stability of the cor-                     tions xS ∈ (0, 2/3). This coexistence is stable because
structures for each composition and size ratio we inves-                      ing is proven      to be the hexagonal close packing37 , so
 responding phases. In particular, for a given size ratio                      no point is found below the line. As xS is increased, S2
tigated. Note that typically, the most efficiently packed                     at xS = 0 and xS = 1 the stable phase is a hexago-
 q, we plot each obtained candidate structure as a point                       is found stable for x = 4/5. S2 coexists with T1 for
crystal structures are found multiple times in these 50                       nal packing of large Sand small disks respectively. For
 in the (xS − v)-plane, where v is the volume per parti-                       x ∈ (2/3, 4/5), and with HexS for xS ∈ (4/5, 1). For
independent      runs.                                                        xSS = 2/3, the T1 phase achieves             the best packing. The
 cle. At any xS , the stable state is the crystal phase, or                    clarity, the volume per particle of the coexisting hexago-
                                                                              straight line that joins T1 and HexL points gives the
 coexistence
    Equipped of     twoa crystal
                 with              phases, which
                          set of candidate              has the
                                                 structures,    welowest
                                                                    used       nal phases vHex (xS ) = xS vHexS + (1 − xS )vHexL has been
                                                                              volume per particle        of their coexistence for all composi-
 volume
an         per particle.
     approach                For a coexistence
                 that is analogous     to a common   of two    phases
                                                          tangent    con-α     subtracted on the vertical axis of Fig. 2.
                                                                              tions xS ∈ (0, 2/3). This coexistence is stable because
 and β, involving
struction               a fraction
             to determine                        nβ = 1 −
                                     nα and stability
                               the relative                 of nthe
                                                                 α ofcor-
                                                                       all
                                                                              no Phase
                                                                                   point diagrams
                                                                                          is found below      the line.
                                                                                                      are mapped       outAsby xrepeating
                                                                                                                                 S is increased,   S2
                                                                                                                                            this con-
 particles respectively,
responding      phases. In the    overall fraction
                               particular,    for a givenof small   disks
                                                              size ratio
                                                                              is  found   stable   for  x S =    4/5.   S2   coexists   with
                                                                               struction for the various size ratios q scanned with simu-     T1  for
 is we
q,   xS plot
          = neach
              α xS,αobtained
                       + nβ xS,βcandidate
                                  . The volume          per as
                                                structure    particle
                                                                 a pointv
                                                                                S ∈ (2/3,
                                                                              xlations.  Once4/5),   andphases
                                                                                                stable     with Hex    S for xS ∈
                                                                                                                  are identified       (4/5,
                                                                                                                                    from     1). For
                                                                                                                                          simulation
 of the
in   the (x
          coexistence
            S − v)-plane,is also  linear
                              where    v isinthethevolume
                                                     number  perfraction
                                                                   parti-
                                                                              clarity,  the  volume    per  particle   of  the  coexisting
                                                                               snapshots, we identify contacts between pairs of particles,   hexago-
 of particles
cle.   At any xinvolved      each of
                  S , the stable       theisphases.
                                   state       the crystalTherefore,
                                                              phase, or in
                                                                              nal  phases
                                                                               which        vHexus
                                                                                       provide    (xSwith
                                                                                                       ) = xaS vset S +
                                                                                                                 Hexof    (1 − xS )vHex
                                                                                                                        constraints         hasparti-
                                                                                                                                       onL the  been
 the (xS − v)-plane,
coexistence                 pointsphases,
                of two crystal      corresponding
                                              which has  to the
                                                             purelowest
                                                                    crys-
                                                                              subtracted     on the   vertical   axis  of  Fig.  2.
                                                                               cle positions, and hence define the corresponding ideal
 tal phases
volume     percan   be joined
                particle.   For by   straight lines
                                 a coexistence       of which   give the
                                                         two phases     α
 volume
and        per particle
       β, involving        of their ncoexistences.
                       a fraction      α and β = Hence,  1 − nαtoffind all     structure.    The volume
                                                                                 Phase diagrams              per particle
                                                                                                     are mapped             of the ideal
                                                                                                                    out by repeating     thisstruc-
                                                                                                                                               con-
 the set ofrespectively,
particles     stable phases  thefor   a given
                                 overall         size ratio,
                                            fraction    of smallwe disks
                                                                    draw       tures are for
                                                                              struction   thenthe
                                                                                                computed     analytically
                                                                                                   various size             as a function
                                                                                                                  ratios q scanned    with of   the
                                                                                                                                             simu-
isa x
    common
      S  =  n   tangent
                x
              α S,α   +  n construction
                             x
                           β S,β .    The   as   depicted
                                            volume      per  in   Fig.
                                                             particle    v2    size ratio
                                                                              lations.  Once    determine
                                                                                           q tostable  phases their exact stability
                                                                                                                are identified         range. For
                                                                                                                                from simulation
 forthe
of    q =   0.23. Forismonodisperse
          coexistence       also linear in disks,      the best
                                               the number           pack-
                                                                fraction       this, we take
                                                                              snapshots,       intoideal
                                                                                            their    account   the optimized
                                                                                                          volume    per particle structure   of the
                                                                                                                                    is computed
 ingparticles
of     is proven    to be each
                involved    the hexagonal
                                  of the phases.         packing37 in
                                                 close Therefore,       so     FBMC simulations,
                                                                              analytically              and of
                                                                                             as a function    find
                                                                                                                 theansize
                                                                                                                        analytical
                                                                                                                           ratio q tosolution
                                                                                                                                       determine for
 at x(x
the    S S=− 0v)-plane,
                 and xS points
                           = 1 the      stable phasetois pure
                                    corresponding            a hexago-
                                                                    crys-      the  particle  coordinates,    based   on  the pairs   of
                                                                              their exact stability range. For this, we take into accountparticles
 nalphases
tal    packingcanofbelarge
                       joinedandbysmall    disks
                                    straight        respectively.
                                                lines  which give the For      in the
                                                                              the     simulated
                                                                                   optimized        unit cellofwhich
                                                                                                 structure             are in direct
                                                                                                                the FBMC              contactand
                                                                                                                               simulations,      af-
 xS = 2/3,
volume     per the  T1 phase
                particle        achieves
                          of their           the bestHence,
                                    coexistences.        packing.     The
                                                                  to find      ter quenching.     More  details  about   this procedure
                                                                              find an analytical solution for the particle coordinates,    can    be
the set of stable phases for a given size ratio, we draw                       found  in  the  Supplementary      Information.     Visualisations
                                                                              based on the pairs of particles in the simulated unit cell
                                                                                                                           4

are done using Ovito38 .                                       Fig. 4), except that it will consist of shields and triangles.
                                                                   There are two other special regions in the phase dia-
                                                               gram. The first, shown as dotted regions, are random
IV.   BINARY ADDITIVE HARD-DISK MIXTURES                       lattice gases, and the second, hashed, regions are random
                                                               tilings. At small size ratios, large disks form a hexago-
   We performed the analysis outlined above for additive       nal compact packing ( HexL ) whose interstices can host
hard disks with size ratios between 0.05 and 1, with a step    small disks. The T1, T2, and T3 phases all consist of
size of 0.01. An overview of all stable crystal structures     this same hexagonal packing, in which all interstices are
obtained – i.e. those that correspond to the best packing      filled with 1,3, and 4 particles, respectively. In principle,
for some combination of xS and q – is shown in Fig. 3.         more of these types of structures exist with more small
Each structure is named according to the same scheme as        particles in each hole20 , but we have not investigated
the one used in Ref. 19, extended when necessary. Note         such extremely asymmetric size ratios and compositions.
that here we show each structure at a so-called “magic”        Where these phases coexist, it is often possible to ran-
size ratio, where a large number of neighbor pairs exactly     domly fill the interstices with a fluctuating number of
touch. However, each binary crystal structure exists over      particles, such that the overall composition requirement
a range of different size ratios q. Depending on the exact     is satisfied. As this random distribution is entropically
size ratio, certain“bonds” – or contacts between particles     favored, such a homogeneous random lattice gas state
can be broken, and the unit cell deformed accordingly. As      is expected to be stable over a purely phase separated
an example, in the S2 phase in Fig. 2, the square unit         regime19 . We indicate this as dotted regions in the phase
cell is slightly deformed with respect to the “ideal” one in   diagram. Note that when the size ratio becomes too large
Fig. 3, such that some of the large particles are no longer    to accommodate the small particles without deforming
touching. In the Supplemental Information (SI), we show        the hexagonal lattice, this lattice gas phase is no longer
for each structure how it gets deformed and which bonds        optimal in terms of packing. This can be seen, on the
are broken as the size ratio moves away from the magic         right edge of the lattice gas regions connecting T1 and
values.                                                        T2, or T2 and T3.
   To summarize the best packed structures at each size            The random tilings occur when the unit cells of two
ratio and composition, we show in Fig. 4 the infinite-         coexisting phases are commensurate, such that they can
pressure phase diagram for this system. Horizontal lines       randomly mix. Usually, creating a boundary between two
correspond to the stability ranges of pure crystal phases,     coexisting phases carries a volume cost. This normally
which only exist at one fixed composition each. Points         limits mixing of phases in the infinite pressure limit, re-
outside of those line correspond to coexistence regions        sulting in a true phase separation. However, some struc-
of the two phases that lie directly above and below the        tures have matching unit-cell edges. If, moreover, the
point (q, xS ).                                                structures shapes can tile the plane without gaps or over-
   As expected39 , no stable phase other than the coex-        laps, the two phases in coexistence can dissolve into one
istence of two hexagonal compact packing is found for          another and form a random tiling phase. For example, as
size ratios above 0.74. For smaller size ratios, a wealth      illustrated in Fig. 5, there is no volume-per-particle cost
of crystal structures are obtained. The main features of       for creating a boundary between S1 squares and HexL
Likos and Henley’s phase diagram19 are reproduced, but         triangles (half a HexL unit cell), and one can tile the
new stable phases (S3, S4, Sh1) are found among the            plane with squares and triangles. Random tiling and fully
candidates generated by FBMC simulations. S3 and S4            phase separated mixtures at the same composition p pack
are both rhombic phases, with 5 and 7 small particles in       equally well (they have the same volume per particle),
the unit cell, respectively.                                   however the former has a finite configurational entropy
   The repeating unit of the Sh1 lattice can be decom-         per disk41 . Therefore, wherever possible, random tiling
posed into a shield tile (hence the Sh label), contain-        regions, depicted as hashed rectangles in the phase dia-
ing the 3 small disks, and 2 HexL triangular tiles. As         gram, should be preferred, on thermodynamic grounds,
long as the size ratio is smaller than a magic ratio for       compared with phase separated coexistences.
which the deformed shield looses contacts between large            A square-triangle random tiling is an ensemble of
disks, shields can be combined with HexL triangle with-        tilings of the infinite plane with squares and triangles.
out volume-per-particle cost. Periodic structures can be       As the proportion of small disks xS varies, the ratio of
constructed, that have the same volume per particle as         the number of squares
                                                                                   √     Nsq and triangles Ntr changes.
the Sh1-HexL coexistence40 . Examples of such struc-           When Nsq /Ntr = 3/4, the random tiling ensemble has
tures are shown in the SI. In principle, these phases are      maximum entropy (the number of possible configurations
all equally stable as the coexistence between Sh1 and          is the highest) and forms a random-tiling quasicrystal of
HexL at infinite pressure. At finite pressure, it is likely    12-fold symmetry41–44 . The corresponding compositions
that vibrational entropy breaks this stalemate in favor of     have been marked in red in Fig. 4 for each random tiling
one specific crystal structure. However, at this point, we     region. It has been argued that an average over this en-
make no strong claims about the exact phase to be ex-          semble exhibits quasi-long-range order with algebraically
pected in this region (the very small area shaded gray in      decaying diffraction peaks at the positions of the 12-fold
                                                                                                                                                                    55
                                                                                                                                                                    5



                                                            T1                                                   H1                H3
                                                             T1                                 S3               H1                H3
                                                                               S1               S3
                                                                                S1


                                        HexS
                                         Hex                T2
                                            S                T2
                                                                               S2                                    H2
                                                                                                                     H2
                                                                                S2                                              Sh1
                                                                                                                                Sh1
                                                                                                 S4
                                                                                                 S4

                                                            T3
                                                             T3
                                        HexL
                                         HexL



FIG.
FIG.
 FIG.3.  Stable
     3.3.Stable  structures        appearininthe
                             thatappear
                  structuresthat
          Stablestructures                        additivephase
                                              theadditive                                                 their respective
                                                                                                       at their
                                                                                                shown at
                                                                                 structures aaa shown
                                                                            The structures
                                                                   diagram. The
                                                           phasediagram.        structures      shown  at their respective ”magic
                                                                                                                respective         ratios”.
                                                                                                                            ”magicratios”.
                                                                                                                            ”magic  ratios”.
Dashed
Dashed   grey
        grey  lines
              lines outline the  repeating   unit of each lattice.  Complete deformation
                                                                             deformation   paths
                                                                                           paths   are
                                                                                                    are depicted
                                                                                                        depicted
 Dashed grey lines outline the repeating unit of each lattice. Complete deformation paths are depicted in the SI. in
                                                                                                                   in the
                                                                                                                      the SI.
                                                                                                                          SI.


                                          1.0
                                           1.0
                                                                                                     Hex
                                                                                                     HexSS
                                                           T3
                                                            T3 S4
                                                         T2
                                                          T2    S4 T2
                                                                    T2          T2
                                                                                T2
                                                                 S3
                                                                  S3 S2              S2
                                           0.8                         S2             S2 H3
                    Fraction of small discs xSS




                                            0.8                                          H3
                    Fraction of small discs x




                                                                  T1
                                                                   T1     T1
                                                                          T1                         T1
                                                                                                     T1H1
                                                                                                        H1
                                           0.6
                                            0.6
                                                                                      S1
                                                                                       S1 H2
                                                                                          H2          Sh1
                                                                                                      Sh1        H2
                                                                                                                 H2

                                           0.4
                                            0.4


                                           0.2
                                            0.2

                                                                                                    Hex
                                                                                                    HexLL
                                           0.0
                                            0.0
                                                  0.0
                                                   0.0             0.2
                                                                    0.2               0.4
                                                                                       0.4                     0.6
                                                                                                               0.6        0.8
                                                                                                                          0.8               1.0
                                                                                             Size
                                                                                              Size ratio
                                                                                                    ratio qq

FIG.
FIG.   4.4.Infinite
  FIG.4.     Infinite pressure
              Infinitepressure    phase
                       pressurephase       diagram
                                            diagramof
                                    phasediagram      ofofbinary
                                                          binary
                                                           binary additive
                                                                       additive hard-disk
                                                                      additive                   mixtures. Horizontal
                                                                                   hard-disk mixtures.
                                                                                   hard-disk    mixtures.       Horizontal lines
                                                                                                                Horizontal    lines   represent stability
                                                                                                                               lines represent               ranges of
                                                                                                                                                  stability ranges   of
pure
pure     crystalphases.
  purecrystal
       crystal     phases. For
                  phases.    Forstate
                            For     statepoints
                                  state   points   outside of
                                           pointsoutside
                                                  outside     ofof those                           phase is
                                                                                           stable phase
                                                                                     the stable
                                                                            lines, the
                                                                    those lines,
                                                                   those   lines,   the   stable  phase           coexistence of
                                                                                                           is aaa coexistence
                                                                                                           is     coexistence      of the
                                                                                                                                      the two
                                                                                                                                           two pure   crystal phases
                                                                                                                                               pure crystal     phases
  thatlie
that
that  lielieimmediately
              immediatelyabove
            immediately      aboveand
                            above     and    belowthe
                                       andbelow
                                            below    the point.
                                                    the    point. The
                                                          point.       The grey
                                                                      The                          under Sh1
                                                                                      rectangle under
                                                                               grey rectangle
                                                                              grey   rectangle    under            corresponds to
                                                                                                            Sh1 corresponds
                                                                                                           Sh1     corresponds      to aa region   where an
                                                                                                                                          region where     an infinite
                                                                                                                                                               infinite
  familyof
family
family    ofofperiodic
                periodicstructures
              periodic    structuresare
                        structures      arefound,
                                       are   found,with
                                            found,    withthe
                                                     with     the same
                                                            the      same volume
                                                                    same     volume per
                                                                            volume     per   particle  as the
                                                                                              particle as
                                                                                        per particle   as   the Sh1-Hex
                                                                                                           the    Sh1-HexLL
                                                                                                                  Sh1-Hex        coexistence. Dotted
                                                                                                                                 coexistence.
                                                                                                                             L coexistence.     Dotted andand hashed
                                                                                                                                                               hashed
rectangles
rectangles       depictrandom
  rectanglesdepict
               depict    randomlattice
                       random        latticegas
                                   lattice   gasand
                                            gas  and     random tiling
                                                  andrandom
                                                       random         tiling
                                                                         √ regions
                                                                     tiling    regions
                                                                              regions     respectively. √
                                                                                       √respectively.
                                                                                         respectively.    In         latter,
                                                                                                                the latter,
                                                                                                           In the
                                                                                                          In    the      √ the
                                                                                                                     latter,   the
                                                                                                                               the horizontal
                                                                                                                                     horizontal  red lines  highlight
                                                                        √
                                                                        √             √√                  √
                                                                                                          √              √
                                                                                                                         √                  √ red lines
                                                                                                                                            √           √ highlight
                                                                                                                                                        √
  random-tiling
random-tiling
random-tiling        quasicrystals.
                   quasicrystals.
               √√ quasicrystals.
                            √√         Their
                                       Their   compositionsare
                                        Theircompositions
                                              compositions        are      3/(2+
                                                                    are 3/(2
                                                                          3/(2    ++222 3)3) ≈
                                                                                         3)  ≈≈ 0.317,       3/(2 +
                                                                                                0.317, 222 3/(2
                                                                                                0.317,       3/(2      3 3)
                                                                                                                    + 33
                                                                                                                    +      3)
                                                                                                                            3) ≈≈  0.481, 44 3/(2
                                                                                                                                ≈ 0.481,      3/(2 ++ 55 3)3) ≈
                                                                                                                                                              ≈ 0.650
                                                                                                                                                                 0.650
               √            √
  and(4
and
and  (4(4+        3)/(6+
          ++77 7 3)/(6
                 3)/(6 ++888 3)   ≈≈0.812
                              3)3)≈    0.812for
                                      0.812   forS1-Hex
                                             for  S1-HexL
                                                 S1-Hex    LL,, ,T1-Hex
                                                                 T1-HexL
                                                                 T1-Hex        , S2-Hex
                                                                                 S2-HexL
                                                                           LL,, S2-Hex   LL and           random tiling
                                                                                                  S4-T1 random
                                                                                             and S4-T1
                                                                                             and  S4-T1   random       tiling  quasicrystal
                                                                                                                       tiling quasicrystal
                                                                                                                               quasicrystal respectively.
                                                                                                                                              respectively.




  FIG.5.5.S1
FIG.         S1ororS2
                    S2squares
                       squaresand
                               andHex
                                   HexLLtriangles
                                         trianglescan
                                                    canbe bejoined
                                                              joined without
                                                                       without volume-per-particle
                                                                                 volume-per-particle cost.
                                                                                                     cost. Moreover,
                                                                                                             Moreover, squares
                                                                                                                          squares and
                                                                                                                                   and triangles
                                                                                                                                        triangles
FIG.    5. S1 or  S2 squares  and Hex L triangles can be joined without volume-per-particle cost. Moreover, squares and triangles
  tilethe
        theplane,
            plane,sosoS1-Hex
                       S1-HexLLand
                                andS2-Hex
                                    S2-Hex     coexistences result
                                                               result in
                                                                       in aa square-triangle
                                                                              square-triangle random
                                                                                              random tiling
                                                                                                      tiling (left).
                                                                                                              (left). Random
                                                                                                                       Random tilings
                                                                                                                                tilings can  also
tile the plane, so S1-HexL and S2-HexL coexistences result in a square-triangle random tiling (left). Random tilings can
tile                                        L coexistences
                                           L                                                                                             can also
                                                                                                                                              also
  be   obtained
be obtained
    obtained by   by  mixing rhombi with triangles
                                   with triangles
                            rhombi with
                    mixing rhombi
                by mixing                           (see  for
                                                   (see for
                                        triangles (see         example     T1-Hex    and  S4-T1  random   tilings  (right)).
                                                         for example
                                                              example T1-Hex
                                                                         T1-HexLL andand S4-T1
                                                                                          S4-T1 random
                                                                                                 random tilings
                                                                                                          tilings (right)).
                                                                                   L
be                                                                                                                 (right)).
                                                                                                                                                                      66

                                              1.0
                                                          T3                                         HexS
                                                               S4    T2
                                                                       S2            S2     H3                 S2
                                              0.8


                 Fraction of small discs xS
                                                                      T1                              T1     H1                           H1     H4
                                              0.6




                                                                                                                                                           ∆ = 0.03
                                                                                            S1 H2            Sh1           H2                    H2

                                              0.4


                                              0.2


                                                                                                      HexL
                                              0.0
                                                    0.0             0.2                   0.4                     0.6            0.8                 1.0
                                              1.0
                                                                                                     HexS
                                                          T3
                                                                    T2                      S3
                                              0.8                         S2         S2     H3               S2
                 Fraction of small discs xS




                                                                           T1                                  H1                    H1         H4
                                              0.6




                                                                                                                                                           ∆ = 0.05
                                                                                                S1      H2 Sh1             H2                   H2

                                              0.4


                                              0.2


                                                                                                            HexL
                                              0.0
                                                    0.0             0.2                   0.4                     0.6            0.8                 1.0
                                              1.0
                                                          T3                                      HexS
                                                                          T2    S5
                                                                                      S3
                                                                                T4                S2
                                              0.8
                 Fraction of small discs xS




                                                                                                   H3
                                                                           T1                                              H1              H4
                                              0.6
                                                                                                        S1                      H2                         ∆ = 0.1

                                              0.4


                                              0.2

                                                                                                                    HexL
                                              0.0
                                                    0.0             0.2                   0.4                     0.6            0.8                 1.0
                                                                                                Size ratio q

  FIG.6.6.Infinite
FIG.        Infinitepressure
                     pressurephase
                              phasediagrams
                                    diagramsofofbinary
                                                 binarynon-additive
                                                        non-additive hard
                                                                       hard disk
                                                                            disk mixtures
                                                                                 mixtures for ∆ = 0.03 (top), ∆ = 0.05 (middle)
                                                                                                                        (middle) and
                                                                                                                                  and
∆∆==0.1 0.1(bottom).
             (bottom). TheTheoverlap
                              overlapbetween
                                      between large
                                               large and
                                                      and small
                                                           small discs
                                                                 discs allowed
                                                                       allowed by
                                                                                by the
                                                                                   the non-additivity
                                                                                       non-additivity is represented in each
                                                                                                                        each case
                                                                                                                             case for
                                                                                                                                   for
q q==0.2,
      0.2,0.5
           0.5and
                and0.8.
                     0.8.


 semble exhibits                              19 algebraically
symmetric    Braggquasi-long-range    order with
                    peaks of a quasicrystal     .                                                     trianglerandom
                                                                                                      sulting  tilings when
                                                                                                                        tilingthe
                                                                                                                                is size  ratio q exactly
                                                                                                                                     a continuous        corresponds
                                                                                                                                                    deformation     of a
 decaying   diffraction peaks  at the  positions
   Note that the random tilings in Fig. 4 are      of the 12-fold                                     to  the magic   ratio   for   either  S2  or S1.
                                                                                                      square-triangle tiling, but no longer possesses itsIn   all12-fold
                                                                                                                                                                  other
                                               19 only square-
 symmetric    Bragg   peaks of a quasicrystal     .
triangle tilings when the size ratio q exactly corresponds                                            cases, the squares
                                                                                                      symmetry.    Note, forare    deformed
                                                                                                                               example,       into
                                                                                                                                           that     rhombi.
                                                                                                                                                 random        The
                                                                                                                                                          tiling     re-
                                                                                                                                                                  pieces
to the magic ratio for either S2 or S1. In all other                                                  sulting random
                                                                                                      displayed  in Fig. tiling
                                                                                                                          5 are isisomorphic.
                                                                                                                                     a continuous deformation of a
    Note that the random tilings in Fig. 4 are only square-
cases, the squares are deformed into rhombi. The re-                                                       The coexistence of S4 and T1 yields a new rhombus-
                                                                                                                                                                  77

triangle      random tiling,
  square-triangle          tiling,butwith     an associated
                                        no longer         possesses quasicrys-
                                                                        its 12-fold                                                           H4
tal.     The FBMC
  symmetry.         Note, forsimulations
                                 example, that   also random
                                                          revealedtilingmorepieces
                                                                                 op-
timally      packed     deformation        paths for T2, T3 and S2                                        T4
  displayed      in Fig.    5 are isomorphic.                                                                        S5
phases,
      The that       modifyofthe
             coexistence          S4 extent
                                      and T1ofyields   the stability       regions
                                                               a new rhombus-
intriangle
     their vicinity.
                random In       particular,
                            tiling,   with antheassociated coexistence      of the
                                                                        quasicrys-
new    S2   deformation
  tal. The FBMC simulations   with   Hex   L   is more       stable
                                                  also revealed more  than   T1op- at
xStimally
      = 2/3,packed
                 revealing     a narrow paths
                          deformation         rhombus-triangle
                                                         for T2, T3 random         S2
tiling
  phases,regionthatand    hencethe
                      modify       a quasicrystal.
                                       extent of theInstability   total, we     find
                                                                            regions
4 indifferent     types of In
       their vicinity.         random      tilingthe
                                  particular,          quasicrystal
                                                            coexistenceregions,
                                                                             of the
                                                                                        FIG. 7.
                                                                                        FIG.  7. Repeating
                                                                                                 Repeating units of the T4, S5 and
                                                                                                                                and H4
                                                                                                                                     H4 lattices
                                                                                                                                         lattices at
                                                                                                                                                  at (q
                                                                                                                                                      (q =
                                                                                                                                                         =
obtained       from S1-Hexwith
  new S2 deformation             L , T1-Hex
                                       HexL√isL more, S2-Hex  stable
                                                                 √L   and
                                                                       than  S4-T1
                                                                              T1 at
                                                                                        0.344,∆
                                                                                        0.344, ∆= = 0.1),
                                                                                                     0.1), (q
                                                                                                           (q == 0.337,
                                                                                                                 0.337, ∆
                                                                                                                        ∆== 0.1)
                                                                                                                             0.1) and
                                                                                                                                  and (q
                                                                                                                                       (q == 0.905,
                                                                                                                                              0.905,∆∆=  =
coexistences,
  x
  √ S   =  2/3,   √  at   compositions
                   revealing    a  narrow
                                        √         3/(2      +
                                                            √  2
                                                rhombus-triangle   3)    ≈   0.317,
                                                                           random
                                                                                        0.05) respectively.
                                                                                               respectively. These
                                                                                                              These structures
                                                                                        0.05)                       structures are
                                                                                                                               are only
                                                                                                                                   only stable
                                                                                                                                         stable for
                                                                                                                                                 for non-
                                                                                                                                                      non-
2 tiling
     3/(2  region and hence
         √ + 3 3) ≈
                                     a quasicrystal. In total, we find
                          √ 0.481, 4 3/(2 + 5 3) ≈ 0.650 and                            additive hard
                                                                                        additive  hard disks.
                                                                                                       disks.
(44+different
        7 3)/(6types + 8 of 3) random
                                ≈ 0.812 tiling           quasicrystal
                                             respectively.                 regions,
                                                                   Deformation
  obtained       from    S1-Hex     ,  T1-Hex
paths of all the stable phases can√be found√in the SI.
                                  L                L  ,  S2-Hex    L   and   S4-T1
  coexistences,
    We
    √ would √          at  compositions
                    like to point out              3/(2      +  2
                                          √ that we √have only inves-3)  ≈    0.317,     phases, T4 and S5, are found stable at smaller size ratios.
                                                                                        case.
  2    3/(2   +   3   3)   ≈   0.481,   4     3/(2
tigated √size ratios√q ≥ 0.05, and compositions below  +   5   3)  ≈    0.650    and     These   lattices
                                                                                           In Fig.   7, two areglobal
                                                                                                                 depicted   in Fig.
                                                                                                                        trends    are 7.observed
                                                                                                                                          T4 and as   H4∆cannot
                                                                                                                                                              is in-
xS(4 ≤+ 711/123)/(6       8 3) ≈
                    ≃ +0.917.        0.812
                                  This         respectively.
                                          likely     leads to some  Deformation
                                                                           missed       creased. First, most phases can be seen as smallturns
                                                                                         exist  without    non-additivity,     while  S5   can,    but   disksouten-
  paths of all
structures       in the
                     the stable
                           top leftphases
                                       corner canofbethe   found
                                                               phasein the   SI.
                                                                         diagram.        to not into
                                                                                        closed   packshells
                                                                                                        efficiently  enough
                                                                                                               of large  ones to   be Fig.
                                                                                                                                (see  stable        the additive
                                                                                                                                              3).inThese    phases
      We would
In this     regime,like we toexpect
                                point that
                                         out thatthe phasewe have      only inves-
                                                                  diagram      gets      case. become unstable as q increases beyond the point
                                                                                        quickly
  tigated
more     and size
                moreratios     q ≥ 0.05,
                        complicated              and compositions
                                          for more        extreme size ratios below         In Fig.
                                                                                        where         7, two global
                                                                                                 the (cluster           trends
                                                                                                                 of) small        are observed
                                                                                                                             spheres    fit into the as holes
                                                                                                                                                         ∆ is left
                                                                                                                                                                 in-
        ≤ 11/12
  xS large
and                   ≃ 0.917.
                fractions           This disks
                              of small      likely20leads       to someexplor-
                                                        . Moreover,         missed       creased.
                                                                                        by          First,
                                                                                             the large      mostNon-additivity
                                                                                                         ones.     phases can be mitigates
                                                                                                                                     seen as small  thedisks    en-
                                                                                                                                                          inflation
  structures       in the    top  left  corner       of
ing this is computationally expensive (due to large unit  the   phase     diagram.       closed
                                                                                        of        smallshells
                                                                                            the into              large ones
                                                                                                          diskofclusters   as (see    Fig. 3).
                                                                                                                                q grows,      whichThese    phases
                                                                                                                                                        causes    an
  In this
cells),   andregime,      we expect
                 not necessarily         thattothe
                                      likely              phaseinteresting
                                                    include        diagram gets   re-    quickly   become     unstable   as  q increases    beyond
                                                                                        overall shift of the phase diagram towards larger size          the  pointra-
  moreAs
sults.     andsuch,
                  morewecomplicated
                            have avoided   for this
                                                  moreregimeextremeof   size phase
                                                                        the   ratios     whereSecond,
                                                                                        tios.    the (cluster    of) small spheres
                                                                                                            non-additivity     favors fit   into the
                                                                                                                                         phases     withholes   left
                                                                                                                                                            a large
  and large fractions of small disks20 . Moreover, explor-
diagram.                                                                                 by  the  large  ones.   Non-additivity      mitigates
                                                                                        number of contacts between large and small disks, such      the  inflation
  ing this is computationally expensive (due to large unit                               of T1,
                                                                                        as   the S1,
                                                                                                  smallS2,disk
                                                                                                            H1 clusters
                                                                                                                 and H2. as     q grows,
                                                                                                                            Those     phases which     causestake
                                                                                                                                                  gradually      an
  cells), and not necessarily likely to include interesting re-                          overall  shift  of  the phase   diagram     towards
                                                                                        over larger and larger portions of the phase diagram.     larger   size  ra-
V.sults.   As such,
       BINARY            we have avoided
                    NON-ADDITIVE             HARD this DISK
                                                          regimeMIXTURES
                                                                     of the phase        tios.  Second,
                                                                                           Another          non-additivity
                                                                                                       interesting    effect offavors   phases with
                                                                                                                                  non-additivity           a large
                                                                                                                                                       is the   ten-
  diagram.                                                                               number of contacts between large and small disks, such
                                                                                        dency to promote random lattice gas and random tiling
                                                                                         as T1, S1, S2, H1 and H2. Those phases gradually take
   We now turn our attention to non-additive binary                                     regions. In Fig. 8, we plot the evolution of√the phase               √ dia-
                                                                                         over larger and larger portions of the phase diagram.
hard-disk       mixtures,       focusing on       non-additivity      param-            gram with ∆ at a fixed composition xS = 3/(2+2 3) ≈
  V. BINARY            NON-ADDITIVE           HARD      DISK MIXTURES                       Another interesting effect of non-additivity is the ten-
eters ∆ = 0.03, 0.05 and 0.1. The corresponding phase                                   0.317 equal to the composition where quasicrystal for-
                                                                                         dency to promote random           lattice gas and random tiling
diagrams are presented in Fig. 6.                                                       mation is expected19 . In this way, we can, for example,
                                                                                         regions. In Fig. 8, we plot the evolution of√the phase                dia-
      We now turn our attention to non-additive binary
   One of the most immediate effects of non-additive oc-                                follow the growth of the S1-HexL quasicrystalline √                 region.
  hard-disk mixtures, focusing on non-additivity param-                                  gram with ∆ at a fixed composition xS = 3/(2+2 3) ≈
curs on the right-hand side of the phase diagram. While                                 As ∆ increases, S1 is one of the few remaining stable
  eters ∆ = 0.03, 0.05 and 0.1. The corresponding phase                                  0.317 equal to the composition where quasicrystal for-
for additive disks, this region is dominated by a phase                                 phases, along with 19     T1 and H2. This results in a signif-
  diagrams are presented in Fig. 6.                                                      mation is expected . In this way, we can, for example,
separation between large disks and small disks hexag-                                   icant   growth     of the
                                                                                         follow the growth of the  range   of q over
                                                                                                                        S1-Hex           which the S1-HexL
      One of the most immediate effects of non-additive oc-                                                                       L quasicrystalline region.
onal crystals, non-additivity allows denser packings for                                quasicrystal
                                                                                         As ∆ increases, S1 is one of the fewseen
                                                                                                         is stable.   In  contrast,   as           in Fig. stable
                                                                                                                                             remaining       6, the
  curs on the right-hand side of the phase diagram. While                               random     tiling   regions   involving    S4   and    T1,   and    S2  and
high size ratios. One of these phases, H4, was not ob-                                   phases, along with T1 and H2. This results in a signif-
  for additive disks, this region is dominated by a phase                               Hex     vanish    for these  values    of  ∆.
served     at all between
  separation        in the additive        case.and
                                 large disks       Thesmall
                                                         repeating
                                                               disks unit
                                                                       hexag-of               L
                                                                                         icant growth of the range of q over which the S1-Hex                     L
this   lattice    is  presented      in  Fig.   7-right.
  onal crystals, non-additivity allows denser packings for The  others     can          quasicrystal is stable. In contrast, as seen in Fig. 6, the
behigh
     seensize
            as variations
                 ratios. One    of the   H1 and
                                    of these        H2 phases,
                                                phases,    H4, wasdeformed
                                                                      not ob-           random tiling regions involving S4 and T1, and S2 and
such                                                                                    VI.
                                                                                        HexLCONCLUSIONS
                                                                                              vanish for theseAND   DISCUSSION
  served at all in the additive case. The repeating crystal
        that   the   lattice   is approximately       a  hexagonal     unit of                                  values of ∆.
ofthis
    small    disksiswith
         lattice              part ofinthe
                        presented            particles
                                          Fig.   7-right.replaced   by large
                                                            The others      can
disks.
  be seen At asthevariations
                     exact sizeofratiothe H1where
                                               and the    contact deformed
                                                     H2 phases,     distance                We have systematically explored the infinite-pressure
between
  such that   a large     and ais small
                 the lattice                disk ((1 −
                                    approximately         ∆)(σS + σcrystal
                                                        a hexagonal     L )/2)          phase   diagram of additive
                                                                                         VI. CONCLUSIONS          ANDand    negatively non-additive bi-
                                                                                                                         DISCUSSION
isofequal    to
      small disksσ   , the   large   spheres    can  be   placed
                   S with part of the particles replaced by large randomly              nary hard disk mixtures in two dimensions. These phase
inside
  disks.the Athexagonal
                 the exact size crystal   of where
                                      ratio   small spheres    withdistance
                                                      the contact      no ad-           diagrams
                                                                                            We have can  serve as useful
                                                                                                      systematically        guidelines
                                                                                                                         explored        for targeted 2D
                                                                                                                                    the infinite-pressure
ditional
  between a large and a small disk ((1 − ∆)(σS + lattice
             volume       cost,   leading    to  another    zone   of  σL )/2)          self-assembly    experiments,     since   many    building blocks
                                                                                         phase diagram of additive and negatively non-additive           bi-
gas.     However,
  is equal     to σS , for
                         the values      of q slightly
                               large spheres               away from
                                                 can be placed            this
                                                                   randomly             comprising
                                                                                         nary hard disk mixtures in two dimensions.particles
                                                                                                     a hard   core  will behave   as hard             when
                                                                                                                                              These phase
magic
  insideratio,      deformations
            the hexagonal               of the
                                  crystal        hexagonal
                                            of small   sphereslattice
                                                                with no makead-         compressed
                                                                                         diagrams can to serve
                                                                                                          sufficiently   high
                                                                                                                 as useful     densities.forIntargeted
                                                                                                                            guidelines          the case2Dof
this   random
  ditional          placement
               volume               unfavorable
                            cost, leading            and the
                                              to another       best-packed
                                                             zone   of lattice          additive   hard disks,
                                                                                         self-assembly           our phase
                                                                                                         experiments,         diagram
                                                                                                                          since   many expands
                                                                                                                                         building on    ear-
                                                                                                                                                    blocks
crystal    remains periodic.
  gas. However,            for values of q slightly away from this                      lier  work19 aby
                                                                                         comprising       incorporating
                                                                                                        hard                several
                                                                                                              core will behave        newparticles
                                                                                                                                  as hard   stable phases
                                                                                                                                                     when
  magic ratio, to
   In   addition          the changesofathe
                      deformations             high  values oflattice
                                                  hexagonal     q, twomakenew           (see  S3, S4, to
                                                                                         compressed    Sh1sufficiently
                                                                                                             in Fig. 3),high
                                                                                                                          as well   as better-packed
                                                                                                                              densities.   In the case de-of
phases,     T4   and    S5,   are  found   stable   at
  this random placement unfavorable and the best-packed smaller size   ratios.          formations   of the
                                                                                         additive hard        previously
                                                                                                         disks,  our phase identified
                                                                                                                              diagramstructures.
                                                                                                                                        expands onTheseear-
These
  crystal lattices
              remains  areperiodic.
                             depicted in Fig. 7. T4 and H4 cannot                       modifications
                                                                                         lier work19 byreveal     two new several
                                                                                                           incorporating     randomnew tiling  regions
                                                                                                                                            stable       (S2
                                                                                                                                                    phases
existInwithout
          additionnon-additivity,
                        to the changeswhile at highS5values
                                                        can, but
                                                              of q,turns   out
                                                                     two new            in  coexistence
                                                                                         (see            with
                                                                                               S3, S4, Sh1   in Hex   andasS4well
                                                                                                                Fig.L3),        in coexistence   with T1),
                                                                                                                                    as better-packed    de-
to not pack efficiently enough to be stable in the additive                             with their associated quasicrystals. Hence, simple binary
                                                                                                                                                                  88

                                        0.10



           Non-additivity parameter ∆   0.08


                                                                                                                          H2
                                        0.06
                                                           T1
                                                                                                  H1
                                                                                       S1
                                        0.04                                 H3

                                                                                                      Sh1                                         H1

                                        0.02                                                                 H1
                                                                            S2               T1
                                                            S2                                                                        HexS
                                        0.00                           T2               HexS           HexS
                                               0.1   0.2         0.3             0.4        0.5          0.6            0.7            0.8             0.9
                                                                                       Size ratio q

FIG. 8.          √ of the phase diagram as a function of the
       √ Evolution                                           the non-additivity
                                                                  non-additivity parameter
                                                                                  parameter ∆ ∆∈ ∈ [0,
                                                                                                    [0,0.1]
                                                                                                        0.1] at
                                                                                                             at fixed
                                                                                                                 fixed composition
                                                                                                                       composition
xSS = 3/(2 + 2 3) ≈ 0.317 where the S1+HexLL quasicrystal
                                                    quasicrystal is
                                                                 is expected.
                                                                     expected. At
                                                                                At this
                                                                                   this composition,
                                                                                        composition, no no pure
                                                                                                            pure periodic
                                                                                                                  periodic phase
                                                                                                                            phase isis
stable, and the phase diagram consists of coexistences between Hex
                                                                HexLL and
                                                                        and other
                                                                            other phases.
                                                                                  phases. For
                                                                                          For clarity,
                                                                                               clarity, we
                                                                                                        we only
                                                                                                            only display
                                                                                                                  display the
                                                                                                                           the name
                                                                                                                               name
of the pure phase in coexistence with HexL L in the labels. As in
                                                               in previous
                                                                    previous diagrams,
                                                                             diagrams, the
                                                                                        the dotted
                                                                                            dotted region
                                                                                                    region highlight
                                                                                                             highlight the
                                                                                                                        the random
                                                                                                                             random
lattice gas and random tiling regions are hashed.


 formations
hard          of the previously
        disk mixtures     exhibit aidentified    structures.
                                      surprisingly            These
                                                     rich phase  di-                        afound
                                                                                               systematic
                                                                                                     by oursampling
                                                                                                                methods.of candidate        structures.
                                                                                                                                We also stress     that the phase
 modifications
agram,     with areveal   two newcomparable
                     complexity      random tilingto regions
                                                      that of (S2 in
                                                               three                         diagram here is drawn at infinite pressure, where the vi-
 coexistence   with    Hex      45 S4 in coexistence with T1),
                              and
dimensional hard spheres   L      .                                                          brational entropy of particles can be neglected. At finite
 with their associated quasicrystals. These results bol-                                     pressures,
    For the non-additive systems, we observe an overall                                         We notewe  thatexpect
                                                                                                                   despitethe our
                                                                                                                                phase  diagram to
                                                                                                                                    systematic        simplify
                                                                                                                                                  search         con-
                                                                                                                                                           for can-
 ster the observation that 2D hard disks exhibit a much                                      siderably,  as  some     structures    will  rapidly  lose stability  to
shift of the stability regions towards larger size ratios, as                               didate crystal structures, it is impossible to exclude the
 richer phase diagram than 3D hard spheres in the limit                                      other  phases    favored     by   entropic   considerations.    Explo-
well as improved stability        for phases with a large num-                              possibility that additional, better packing crystal struc-
 of large pressures44,45 . As discussed in Ref.19 , this is                                  rationare
                                                                                                     of possible
                                                                                                         the finite-pressure       phase behavior       will be the
ber of contacts between large and small disks. Two                                          tures                    in these systems.       This is particularly
 caused by the fact that many more constraints must be                                       subject  of  a future     study.
new phases, H4 and T4 (see Fig. 3), only possible in                                        relevant for the top left corner of the phase diagrams
 satisfied in three dimensions to have a dense structure at                                     Finally,   we emphasize
non-additive systems, are also found to be stable. The                                      (low   size ratios     and high that        in the
                                                                                                                                 fractions       infiniteparticles),
                                                                                                                                             of small       pressure
 a ”magic ratio”, due to the larger number of neighbours.
S5 phase, which can be constructed with additive disks                                      where the best-packed structures will primarily aconsist
                                                                                             limit,  the   phase     diagrams      proposed     here   set     lower
 Indeed, many reasonable candidate structures, such as                                       bound   on the that
                                                                                                               packing     fraction   of binary
but was not stable in this case, appears as a stable                                        of  structures            pack    more and      morehard
                                                                                                                                                   smalldisks  pack-
                                                                                                                                                           particles
 cubic lattice of large spheres with icosahedral clusters of                                 ings.the
                                                                                                    Apart   from 9 magic        ratios
phase in the non-additive mixtures. With increasing                                         into       interstices      between    the for  which
                                                                                                                                         large      compact
                                                                                                                                                disks          pack-
                                                                                                                                                       in hexag-
 small spheres in the interstices packs worst than a co-                                     ings have   been
                                                                                                           20 demonstrated to achieve maximum pack-
non-additivity, random tiling regions extend over larger                                    onal lattice 47,48
                                                                                                             . As we limit ourselves here to unit cells
 existence of face center cubic phases of large and small                                    ing fractionat most , it is12still an opensuchmathematical
composition      ranges, potentially making them easier to                                  containing                      particles,         structures problem
                                                                                                                                                            are not
 particles46,47 .
observe in self-assembly experiments, where fine control                                    found by our methods. We also stress for
                                                                                             to prove   which    is  the   densest   structure    thata given   com-
                                                                                                                                                         the phase
over                                                                                         position  and   size   ratio.
                                                                                            diagram here is drawn at infinite pressure, where the vi-
    Forthe
         thesize   ratio is hard
              non-additive           to achieve.
                               systems,   we observe Negative   non-
                                                         an overall
additivity   tends   to favor  contacts  between    large and  small                        brational entropy of particles can be neglected. At finite
 shift of the stability regions towards larger size ratios, as
disks.                                                                                      pressures, we expect the phase diagram to simplify con-
 well asThis   could stability
          improved      also be achieved
                                  for phasesbywith
                                            46
                                                 considering
                                                      a large selec-
                                                               num-                          ACKNOWLEDGEMENTS
tive  attraction    between   the  particles   .  Future  studies in                        siderably,   as some structures will rapidly lose stability to
 ber of contacts between large and small disks.                 Two
this  direction    could  benefit   from  FBMC      simulations  for                        other phases favored by entropic considerations. Explo-
 new phases, H4 and T4 (see Fig. 3), only possible in
anon-additive
   systematic sampling       of candidate   structures.                                     ration   of theThomas
                                                                                                We thank      finite-pressure
                                                                                                                          Fernique,phase    behavior
                                                                                                                                       Marianne         will be the
                                                                                                                                                    Impéror-Clerc,
                  systems, are    also found   to be stable. The
                                                                                            subject   of a future
                                                                                             Jean-François     Sadoc, study.
                                                                                                                           and Laura Filion for many useful
S5We    notewhich
    phase,      that despite     our systematic
                       can be constructed      withsearch     for disks
                                                       additive    can-
didate
but was  crystal    structures,
             not stable           it iscase,
                            in this      impossible
                                              appears  to as
                                                          exclude   the
                                                              a stable                       discussions. This work is funded by the ANR grant ANR-
possibility
phase in the   thatnon-additive
                      additional, better     packing
                                     mixtures.      Withcrystal  struc-
                                                            increasing                       18-CE09-0025.
tures  are possible
non-additivity,          in these
                     random         systems.
                               tiling   regionsThis
                                                 extendis particularly
                                                           over larger                         Finally, we emphasize that in the infinite pressure
relevant
composition for the    top potentially
                 ranges,    left corner making
                                           of the phase
                                                      them diagrams
                                                             easier to                      limit, the phase diagrams proposed here set a lower
(low
observesizeinratios    and high
               self-assembly        fractions ofwhere
                                experiments,        smallfine
                                                            particles),
                                                               control                      SUPPLEMENTARY
                                                                                            bound   on the packing   MATERIAL
                                                                                                                        fraction of binary hard disks pack-
where
over the thesize
               best-packed     structures
                    ratio is hard            will primarily
                                      to achieve.      Negativeconsist
                                                                  non-                      ings. Apart from 9 magic ratios for which compact pack-
of structures
additivity    tendsthat   pack contacts
                      to favor  more and      more large
                                           between    smallandparticles
                                                                 small                         Inhave
                                                                                            ings  the supplementary
                                                                                                       been demonstrated    material, we provide
                                                                                                                                 to achieve        representa-
                                                                                                                                             maximum    pack-
into
disks.theThis
            interstices
                could also between    the large
                              be achieved          disks in a hexag-
                                              by considering     selec-                     tions
                                                                                            ing    of the49,50
                                                                                                fraction   deformation        paths
                                                                                                               , it is still an openconsidered   for the
                                                                                                                                      mathematical        vari-
                                                                                                                                                     problem
                                              48
      lattice20 . between
tive attraction
onal                           the particles
                     As we limit      ourselves  . here
                                                    Future
                                                         to studies  in
                                                             unit cells                     to
                                                                                            ousprove  whichphases
                                                                                                 candidate     is the densest    structure
                                                                                                                        along with          for avalues
                                                                                                                                     numerical    given of
                                                                                                                                                         com-
                                                                                                                                                           the
this direction
containing         could 12
               at most     benefit   from such
                              particles,    FBMC      simulations
                                                  structures        for
                                                               are not                      position  and for
                                                                                            magic ratios   sizethree
                                                                                                                  ratio.values of the non-additivity param-
                                                                                                                                            9

eter. We also discuss the existence of a family of stable               21 T. Dotera, T. Oshiro,   and P. Ziherl, Nature 506, 208 (2014).
                                                                        22 P.-Y. Wang and T. G. Mason, Nature 561, 94 (2018).
periodic structures with more than 12 particles in the                  23 L. Filion, M. Marechal, B. van Oorschot, D. Pelt, F. Smallenburg,
unit cell involving the Sh1 tile.
                                                                          and M. Dijkstra, Phys. Rev. Lett. 103, 188302 (2009).
                                                                        24 J. de Graaf, L. Filion, M. Marechal, R. van Roij, and M. Dijkstra,

                                                                           J. Chem. Phys. 137, 214101 (2012).
DATA AVAILABILITY                                                       25 D.  Salgado-Blanco and C. I. Mendoza, Soft Matter 11, 889
                                                                           (2015).
                                                                        26 M. Dijkstra, Phys. Rev. E 58, 7523 (1998).
  The data that support the findings of this study are                  27 A. A. Louis, R. Finken, and J. Hansen, Phys. Rev. E 61, R1028
available from the corresponding author upon reasonable                    (2000).
request.                                                                28 F. Saija and P. Giaquinta, J. Chem. Phys. 117, 5780 (2002).
                                                                        29 A. Widmer-Cooper and P. Harrowell, J. Chem. Phys. 135,
1 S. C. Glotzer and M. J. Solomon, Nat. Mater. 6, 557 (2007).
                                                                           224515 (2011).
2 D. Vanmaekelbergh, Nano Today 6, 419 (2011).                          30 S. Torquato and Y. Jiao, Phys. Rev. E 80, 041104 (2009).
3 S. Sacanna, D. J. Pine,   and G.-R. Yi, Soft Matter 9, 8096 (2013).   31 M. Marechal, U. Zimmermann, and H. Löwen, J. Chem. Phys.
4 M. A. Boles, M. Engel,      and D. V. Talapin, Chem. Rev. 116,           136, 144506 (2012).
  11220 (2016).                                                         32 E. Bianchi, G. Doppelbauer, L. Filion, M. Dijkstra, and G. Kahl,
5 M. H. Kim, S. H. Im,     and O. O. Park, Adv. Funct. Mater. 15,          J. Chem. Phys. 136, 214102 (2012).
   1329 (2005).                                                         33 T. Vissers, Z. Preisler, F. Smallenburg, M. Dijkstra,        and
 6 J. Yu, Q. Yan, and D. Shen, ACS Appl. Mater. Interfaces 2,
                                                                           F. Sciortino, J. Chem. Phys. 138, 164505 (2013).
   1922 (2010).                                                         34 I. Staneva and D. Frenkel, J. Chem. Phys. 143, 194511 (2015).
 7 J. Zhang, Y. Li, X. Zhang, and B. Yang, Adv. Mater. 22, 4249
                                                                        35 A. Gabriëlse, H. Löwen, and F. Smallenburg, Materials 10, 1280
   (2010).                                                                 (2017).
 8 A. Dong, X. Ye, J. Chen, and C. B. Murray, Nano Lett. 11,
                                                                        36 W. Shen, J. Antonaglia, J. A. Anderson, M. Engel, G. van An-
   1804 (2011).                                                            ders, and S. C. Glotzer, Soft Matter 15, 2571 (2019).
 9 J.-T. Zhang, L. Wang, D. N. Lamont, S. S. Velankar, and S. A.
                                                                        37 L. F. Toth, Math. Z 48, 676 (1943).
   Asher, Angew. Chem. Int. Ed. 51, 6117 (2012).                        38 A. Stukowski, Model. Simul. Mater. Sci. Eng. 18 (2010),
10 V. Lotito and T. Zambelli, Adv. Colloid Interface Sci. 246, 217
                                                                           10.1088/0965-0393/18/1/015012.
   (2017).                                                              39 G. Blind, J. Reine Angew. Math. 236, 145 (1969).
11 D. V. Talapin, E. V. Shevchenko, M. I. Bodnarchuk, X. Ye,
                                                                        40 T. Fernique, A. Hashemi, and O. Sizova, in Discrete Geom-
   J. Chen, and C. B. Murray, Nature 461, 964 (2009).                      etry for Computer Imagery, Vol. 11414, edited by M. Couprie,
12 X. Ye, J. Chen, M. E. Irrgang, M. Engel, A. Dong, S. C. Glotzer,
                                                                           J. Cousty, Y. Kenmochi, and N. Mustafa (Springer International
   and C. B. Murray, Nat. Mater. 16, 214 (2017).                           Publishing, Cham, 2019) pp. 420–431.
13 X. Ye, C. Zhu, P. Ercius, S. N. Raja, B. He, M. R. Jones, M. R.
                                                                        41 M. Widom, Phys. Rev. Lett. 70, 2094 (1993).
   Hauwiller, Y. Liu, T. Xu, and A. P. Alivisatos, Nat. Commun.         42 H. Kawamura, Prog. Theor. Phys. 70, 352 (1983).
   6 (2015), 10.1038/ncomms10052.                                       43 P. A. Kalugin, Journal of Physics A: Mathematical and General
14 L. Assoud, R. Messina, and H. Löwen, Europhys. Lett. 80, 48001
                                                                           27, 3599 (1994).
   (2007).                                                              44 B. Nienhuis, Phys. Rep. 301, 271 (1998).
15 L. Assoud, R. Messina, and H. Löwen, J. Chem. Phys. 129,
                                                                        45 A. B. Hopkins, F. H. Stillinger, and S. Torquato, Phys. Rev. E
   164511 (2008).                                                          85, 021130 (2012).
16 J. Fornleitner, F. Lo Verso, G. Kahl, and C. N. Likos, Soft
                                                                        46 A. V. Tkachenko, Proc. Natl. Acad. Sci. U.S.A. 113, 10269
   Matter 4, 480 (2008).                                                   (2016).
17 J. Fornleitner, F. Lo Verso, G. Kahl, and C. N. Likos, Langmuir
                                                                        47 T. Kennedy, Discrete Comput. Geom. 35, 255 (2006).
   25, 7836 (2009).                                                     48 T. Fernique and N. Bédaride, arXiv preprint arXiv:2002.07168
18 A. D. Law, D. M. A. Buzza, and T. S. Horozov, Phys. Rev. Lett.
                                                                           (2020).
   106 (2011), 10.1103/physrevlett.106.128302.
19 C. N. Likos and C. L. Henley, Phil. Mag. B 68, 85 (1993).
20 O. Uche, F. Stillinger, and S. Torquato, Physica A 342, 428

   (2004).
