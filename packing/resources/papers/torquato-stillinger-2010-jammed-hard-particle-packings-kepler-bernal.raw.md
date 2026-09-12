                                                     Jammed Hard-Particle Packings: From Kepler to Bernal
                                                     and Beyond
arXiv:1008.2982v1 [cond-mat.stat-mech] 17 Aug 2010




                                                         S. Torquato∗

                                                         Department of Chemistry, Department of Physics, Princeton Center for Theoretical
                                                         Science,Princeton Institute for the Science and Technology of Materials,
                                                         and Program in Applied and Computational Mathematics, Princeton University,
                                                         Princeton New Jersey, 08544 USA and
                                                         School of Natural Sciences, Institute of Advanced Study, Princeton New Jersey,
                                                         08540 USA

                                                         F. H. Stillinger†

                                                         Department of Chemistry, Princeton University, Princeton New Jersey,
                                                         08544 USA




                                                                                            1
                                         Abstract
Understanding the characteristics of jammed particle packings provides basic in-

sights into the structure and bulk properties of crystals, glasses, and granular media,

and into selected aspects of biological systems. This review describes the diversity

of jammed configurations attainable by frictionless convex nonoverlapping (hard)

particles in Euclidean spaces and for that purpose it stresses individual-packing

geometric analysis. A fundamental feature of that diversity is the necessity to

classify individual jammed configurations according to whether they are locally,

collectively, or strictly jammed. Each of these categories contains a multitude of

jammed configurations spanning a wide and (in the large system limit) continuous

range of intensive properties, including packing fraction φ, mean contact number

Z, and several scalar order metrics. Application of these analytical tools to spheres

in three dimensions (an analog to the venerable Ising model) covers a myriad of

jammed states, including maximally dense packings (as Kepler conjectured), low-

density strictly-jammed tunneled crystals, and a substantial family of amorphous

packings. With respect to the last of these, the current approach displaces the

historically prominent but ambiguous idea of “random close packing” (RCP) with

the precise concept of “maximally random jamming” (MRJ). Both laboratory pro-

cedures and numerical simulation protocols can, and frequently have been, used

for creation of ensembles of jammed states. But while the resulting distributions

of intensive properties may individually approach narrow distributions in the large

system limit, the distinguishing varieties of possible operational details in these

procedures and protocols lead to substantial variability among the resulting distri-

butions, some examples of which are presented here. This review also covers recent

advances in understanding jammed packings of polydisperse sphere mixtures, as

well as convex nonspherical particles, e.g., ellipsoids, “superballs”, and polyhedra.

Because of their relevance to error-correcting codes and information theory, sphere

packings in high-dimensional Euclidean spaces have been included as well. We also

make some remarks about packings in (curved) non-Euclidean spaces. In closing

this review, several basic open questions for future research to consider have been



                                             2
           identified.




∗
    Electronic address: torquato@princeton.edu
†
    Electronic address: fhs@princeton.edu

                                                 3
  Contents


   I. Introduction                                                           5


  II. Preliminaries and Definitions                                          10


 III. Lessons From Disordered Jammed Packings of Spheres                     15


 IV. Jamming Categories, Isostaticity, and Polytopes                         19

     A. Jamming Categories                                                   19

     B. Isostaticity                                                         22

     C. Polytope Picture of Configuration Space                              23


  V. Order Metrics                                                           29

     A. Specific Order Metrics                                               30

     B. Characteristics of a Good Order Metric                               32


 VI. Order Maps and Optimal Packings                                         33

     A. Strict Jamming                                                       35

     B. Collective and Local Jamming                                         38

     C. Broader Applications to Other Condensed States of Matter             38


VII. Protocol Bias, Loss of Ergodicity, and Nonuniqueness of Jammed States   38


VIII. Attributes of the Maximally Random Jammed State                        41


 IX. Packings of Spheres With a Size Distribution                            44


  X. Packings of Nonspherical Particles                                      50

     A. Ellipsoid Packings                                                   51

     B. Superball Packings                                                   55

     C. Polyhedron Packings                                                  61

     D. Additional Remarks                                                   69


 XI. Packing Spheres in High-Dimensional Euclidean Spaces                    70


XII. Remarks on Packing Problems in Non-Euclidean Spaces                     80


                                                  4
XIII. Challenges and Open Questions                                                          82


      Acknowledgments                                                                        84


      References                                                                             84



I. INTRODUCTION


   The importance of packing hard particles into various kinds of vessels and the questions it
raises have an ancient history. Bernal has remarked that “heaps (close-packed arrangements
of particles) were the first things that were ever measured in the form of basketfuls of grain
for the purpose of trading or the collection of taxes” (Bernal, 1965). Although packing
problems are easy to pose, they are notoriously difficult to solve rigorously. In 1611, Kepler
was asked: What is the densest way to stack equal-sized cannon balls? His solution, known
as “Kepler’s conjecture,” was the face-centered-cubic (fcc) arrangement (the way your green
grocer stacks oranges). Gauss, 1831 proved that this is the densest Bravais lattice packing
(defined below). But almost four centuries passed before Hales proved the general conjecture
that there is no other arrangement of spheres in three-dimensional Euclidean space whose
density can exceed that of the fcc packing (Hales, 2005); see Aste and Weaire, 2008 for a
popular account of the proof. Even the proof of the densest packing of congruent (identical)
circles in the plane, the two-dimensional analog of Kepler’s problem, appeared only 70 years
ago (Conway and Sloane, 1998; Rogers, 1964); see Fig. 1.
   Packing problems are ubiquitous and arise in a variety of applications. These exist in the
transportation, packaging, agricultural and communication industries. Furthermore, they
have been studied to help understand the symmetry, structure and macroscopic physical
properties of condensed matter phases, liquids, glasses and crystals (Ashcroft and Mermin,
1976; Bernal, 1960, 1965; Chaikin and Lubensky, 1995; Hansen and McDonald, 1986;
Mayer and Mayer, 1940; Speedy, 1994; Stillinger et al., 1964; Stillinger and Salsburg, 1969;
Weeks et al., 1971; Woodcock and Angell, 1981). Packing problems are also relevant for the
analysis of heterogeneous materials (Torquato, 2002), colloids (Chaikin and Lubensky, 1995;
Russel et al., 1989; Torquato, 2009), and granular media (Edwards, 1994). Understanding
the symmetries and other mathematical characteristics of the densest sphere packings in vari-
ous spaces and dimensions is a challenging area of long-standing interest in discrete geometry


                                             5
FIG. 1 A portion of the densest packing of identical circles in the plane, with centers lying at the sites of a
                                                                                       √
triangular lattice. The fraction of R2 covered by the interior of the circles is φ = π/ 12 = 0.906899 . . .. The

first claim of a proof was made by Thue in 1892. However, it is generally believed that the first complete

error-free proof was produced only in 1940 by Fejes Tóth; see Rogers, 1964 and Conway and Sloane, 1998

for the history of this problem.


and number theory (Cohn and Elkies, 2003; Conway and Sloane, 1998; Rogers, 1964) as well
as coding theory (Cohn and Kumar, 2007b; Conway and Sloane, 1998; Shannon, 1948).
   It is appropriate to mention that packing issues also arise in numerous biological contexts,
spanning a wide spectrum of length scales. This includes “crowding” of macromolecules
within living cells (Ellis, 2001), the packing of cells to form tissue (Gevertz and Torquato,
2008; Torquato, 2002), the fascinating spiral patterns seen in plant shoots and flowers (phyl-
lotaxis) (Nisoli et al., 2010; Prusinkiewicz and Lindenmayer, 1990) and the competitive set-
tlement of territories by animals, the patterns of which can be modeled as random sequen-
tial packings (Tanemura and Hasegawa, 1980; Torquato, 2002). Figure 2 pictorially depicts
macromolecular crowding and a familiar phyllotactic pattern.
   We will call a packing a large collection of nonoverlapping (i.e., hard) particles in either a
finite-sized container or in d-dimensional Euclidean space Rd . The packing fraction φ is the
fraction of space covered by (interior to) the hard particles. “Jammed” packings are those
particle configurations in which each particle is in contact with its nearest neighbors in such
a way that mechanical stability of a specific type is conferred to the packing (see Section IV).
Jammed packings and their properties have received considerable attention in the literature,

                                                     6
FIG. 2 Biological examples of packing geometries. Left panel: Schematic representation of the approximate
numbers, shapes and density of packing of macromolecules inside a cell of Escherichia coli. (Illustration by

David S. Goodsell, the Scripps Research Institute.) Molecular crowding occurs because of excluded volume

effects due to the mutual impenetrability of all of the macromolecules. This nonspecific steric repulsion is

always present, regardless of any other attractive or repulsive interactions that might occur between the

macromolecules. Thus, molecular crowding is essentially a packing problem (Ellis, 2001). Right panel:

Close-up of a daisy capitulum (flower head), as given by Prusinkiewicz and Lindenmayer, 1990. The most

prominent feature is two sets of spirals, one turning clockwise and the other counterclockwise. There are

several models that relate such phyllotactic patterns to packings problems (Prusinkiewicz and Lindenmayer,

1990).


both experimental and theoretical. Within the domains of analytical theory and computer
simulations, two conceptual approaches for their study have emerged. One is the “ensemble”
approach (Bernal, 1960, 1965; Edwards, 1994; Edwards and Grinev, 2001; Gao et al., 2006;
Liu and Nagel, 1998; Makse and Kurchan, 2002; O’Hern et al., 2003; Parisi and Zamponi,
2010; Silbert et al., 2002, 2005; Song et al., 2008; Wyart et al., 2005), which for a given
packing procedure aims to understand typical configurations and their frequency of oc-
currence. The other, more recently, is the “geometric-structure” approach (Donev et al.,
2004a, 2007a, 2004c; Kansal et al., 2002b; Torquato et al., 2003; Torquato and Stillinger,
2001, 2007; Torquato et al., 2000), which emphasizes quantitative characterization of single-
packing configurations, without regard to their occurrence frequency in the algorithmic
method used to produce them. Our primary objective is to review the latter approach,


                                                   7
while at the same time to show that these two approaches are complementary in that they
represent different aspects of the larger context of hard-particle jamming phenomena. In
particular, a wide range of jammed packing ensembles can be created by the choice of the
generating algorithm, and the geometric-structure approach analyzes and classifies individ-
ual members of those ensembles, whether they be crystalline or amorphous at any achievable
packing fraction φ.
   The process of cooling an initially hot liquid ultimately to absolute zero temperature
provides a close and useful analogy for the subject of hard-particle jamming. Figure 3 sum-
marizes this analogy in schematic form, showing typical paths for different isobaric cooling
rates in the temperature-volume plane. While these paths are essentially reproducible for a
given cooling schedule, i.e., giving a narrow distribution of results, that distribution depends
sensitively on the specific cooling schedule, or protocol, that has been used. A very rapid
quench that starts with a hot liquid well above its freezing temperature will avoid crystal
nucleation, producing finally a glassy solid at absolute zero temperature. A somewhat slower
quench from the same initial condition can also avoid nucleation, but will yield at its T = 0
endpoint a glassy solid with lower volume and potential energy. An infinitesimal cooling
rate in principle will follow a thermodynamically reversible path of equilibrium states, will
permit nucleation, and will display a volume discontinuity due to the first order freezing
transition on its way to attaining the structurally perfect crystal ground state. By analogy,
for hard-particle systems compression qualitatively plays the same role as decreasing the
temperature in an atomic or molecular system. Thus it is well known that compressing
a monodisperse hard-sphere fluid very slowly leads to a first-order freezing transition, and
the resulting crystal phase corresponds to the closest packing arrangement of those spheres
(Mau and Huse, 1999). The resulting hard sphere stacking variants are configurational im-
ages of mechanically stable structures exhibited for example by the venerable Lennard-Jones
model system. By contrast, rapid compression rates applied to a hard-sphere fluid will create
random amorphous jammed packings (Rintoul and Torquato, 1996b), the densities of which
can be controlled by the compression rate utilized (see Fig. 11 in Sec. IV below). In both
the cases of cooling liquid glass-formers, and of compressing monodisperse hard spheres, it
is valuable to be able to analyze the individual many-particle configurations that emerge
from the respective protocols.
   We begin this review, after introducing relevant terminology, by specifically considering

                                              8
FIG. 3 Three isobaric (constant pressure) cooling paths by which a typical liquid may solidify, represented
in a volume vs. temperature diagram. An infinitesimal cooling rate from the high-temperature liquid traces

out the thermodynamic equilibrium path (shown in green), including a discontinuity resulting from the

first-order freezing transition. This reversible path leads to the ground state defect-free crystalline structure

in the T → 0 limit. Very slow but finite cooling rate (not shown) can involve crystal nucleation but typically

creates defective crystals. More rapid cooling of the liquid (blue curves) can avoid crystal nucleation, passing

instead through a glass transition temperature range, and resulting in metastable glassy solids at absolute

zero. The volumes, energies, and other characteristics of those glasses vary with the specific cooling rate

employed in their production.


packings of frictionless, identical spheres in the absence of gravity, which represents an ide-
alization of the laboratory situation for investigations of jammed packings; see Section III.
This simplification follows that tradition in condensed matter science to exploit idealized
models, such as the Ising model, which is regarded as one of the pillars of statistical mechan-
ics (Domb, 1960; Gallavotti, 1999; Onsager, 1944). In that tradition, this idealization offers
the opportunity to obtain fundamental as well as practical insights, and to uncover unifying
concepts that describe a broad range of phenomena. The stripped-down hard-sphere “Ising
model” for jammed packings (i.e., jammed, frictionless, identical spheres in the absence of
gravity) embodies the primary attributes of real packings while simultaneously generating
fascinating mathematical challenges. The geometric-structure approach to analyzing indi-
vidual jammed states produced by this model covers not only the maximally dense packings


                                                      9
(e.g., Kepler’s conjecture) and amorphous “Bernal” packings, but an unbounded collection
of other jammed configurations. This approach naturally leads to the inevitable conclusion
that there is great diversity in the types of attainable jammed packings with varying degrees
of order, mechanical stability, and density.
   Important insights arise when jammed sphere packings are placed in a broader context
that includes jammed states of noncongruent spheres as well as nonspherical objects, as
discussed in Secs. IX and X. These extensions include polydisperse spheres, ellipsoids,
“superballs,” and polyhedra in three dimensions. In addition, this broader context also
involves sphere packings in Euclidean space with high dimensions (Sec. XI), which is relevant
to error correcting codes and information theory (Conway and Sloane, 1998; Shannon, 1948),
and packings in non-Euclidean spaces (Sec. XII). Finally, in Sec. XIII, we identify a number
of basic open questions for future research.


II. PRELIMINARIES AND DEFINITIONS


   Some basic definitions concerning packings are given here. A packing P is a collection of
nonoverlapping solid objects or particles in d-dimensional Euclidean space Rd . Packings can
be defined in other spaces (e.g., hyperbolic spaces and compact spaces, such as the surface
of a d-dimensional sphere), but our primary focus in this review is Rd . A saturated packing
is one in which there is no space available to add another particle of the same kind to the
packing.




FIG. 4     Symmetries associated with three particle shapes. Chords pass through each particle
centroid. Left panel: A “superdisk” is centrally symmetric and possesses two equivalent principal
axes. Middle panel: An ellipse is centrally symmetric but does not possess two equivalent principal
axes. Right panel: A triangle is not centrally symmetric.



                                               10
   We will see subsequently that whether a particle possesses central symmetry plays a fun-
damental role in determining its dense packing characteristics. A d-dimensional particle is
centrally symmetric if it has a center C that bisects every chord through C connecting any
two boundary points of the particle, i.e., the center is a point of inversion symmetry. Ex-
amples of centrally symmetric particles in Rd are spheres, ellipsoids and superballs (defined
in Section X). A triangle and tetrahedron are examples of non-centrally symmetric two-
and three-dimensional particles, respectively. Figure 4 depicts examples of centrally and
non-centrally symmetric two-dimensional particles. A d-dimensional centrally symmetric
particle for d ≥ 2 is said to possess d equivalent principal (orthogonal) axes (directions)
associated with the moment of inertia tensor if those directions are two-fold rotational sym-
metry axes such that the d chords along those directions and connecting the respective pair
of particle-boundary points are equal. (For d = 2, the two-fold (out-of-plane) rotation along
an orthogonal axis brings the shape to itself, implying the rotation axis is a “mirror im-
age” axis.) Whereas a d-dimensional superball has d equivalent directions, a d-dimensional
ellipsoid generally does not (see Fig. 4).
   A lattice Λ in Rd is a subgroup consisting of the integer linear combinations of vectors
that constitute a basis for Rd . In the physical sciences and engineering, this is referred to
as a Bravais lattice. Unless otherwise stated, the term “lattice” will refer here to a Bravais
lattice only. A lattice packing PL is one in which the centroids of the nonoverlapping identical
particles are located at the points of Λ, and all particles have a common orientation. The
set of lattice packings is a subset of all possible packings in Rd . In a lattice packing, the
space Rd can be geometrically divided into identical regions F called fundamental cells, each
of which contains the centroid of just one particle. Thus, the density of a lattice packing is
given by
                                                  v1
                                         φ=             ,                                   (1)
                                                Vol(F )
where v1 is the volume of a single d-dimensional particle and Vol(F ) is the d-dimensional
volume of the fundamental cell. For example, the volume v1 (R) of a d-dimensional spherical
particle of radius R is given explicitly by
                                                  π d/2 Rd
                                     v1 (R) =              ,                                (2)
                                                Γ(1 + d/2)
where Γ(x) is the Euler gamma function. Figure 5 depicts lattice packings of congruent
spheres and congruent nonspherical particles.

                                                11
FIG. 5   Examples of lattice packings (i.e., Bravais lattices) depicted in two dimensions. Left
panel: A portion of a lattice packing of congruent spheres. Each fundamental cell (depicted as a
rhombus here) has exactly one assigned sphere center. Right panel: A portion of a lattice packing
of congruent nonspherical particles. Each fundamental cell has exactly one particle centroid. Each
particle in the packing must have the same orientation.

   A more general notion than a lattice packing is a periodic packing. A periodic packing
of congruent particles is obtained by placing a fixed configuration of N particles (where
N ≥ 1) with arbitrary nonoverlapping orientations in one fundamental cell of a lattice Λ,
which is then periodically replicated without overlaps. Thus, the packing is still periodic
under translations by Λ, but the N particles can occur anywhere in the chosen fundamental
cell subject to the overall nonoverlap condition. The packing density of a periodic packing
is given by
                                       Nv1
                                      φ=       = ρv1 ,                                (3)
                                     Vol(F )
where ρ = N/Vol(F ) is the number density, i.e., the number of particles per unit volume.
Figure 6 depicts a periodic non-lattice packing of congruent spheres and congruent nonspher-
ical particles. Note that the particle orientations within a fundamental cell in the latter case
are generally not identical to one another.
   Consider any discrete set of points with position vectors X ≡ {r1 , r2 , . . .} in Rd . Associ-
ated with each point ri ∈ X is its Voronoi cell, Vor(ri ), which is defined to be the region of
space no farther from the point at ri than to any other point rj in the set, i.e.,

                       Vor(ri ) = {r : |r − ri | ≤ |r − rj |for all rj ∈ X}.                  (4)

The Voronoi cells are convex polyhedra whose interiors are disjoint, but share common faces,
and therefore the union of all of the polyhedra is the whole of Rd . This partition of space

                                              12
FIG. 6   Examples of periodic non-lattice packings depicted in two dimensions. Left panel: A
portion of a periodic non-lattice packing of congruent spheres. The fundamental cell contains
multiple spheres located anywhere within the cell subject to the nonoverlap constraint. Right panel:
A portion of a periodic non-lattice packing of congruent nonspherical particles. The fundamental
cell contains multiple nonspherical particles with arbitrary positions and orientations within the
cell subject to the nonoverlap constraint.


is called the Voronoi tessellation. While the Voronoi polyhedra of a lattice are congruent
(identical) to one another, the Voronoi polyhedra of a non-Bravais lattice are not identical to
one another. Attached to each vertex of a Voronoi polyhedron is a Delaunay cell, which can
be defined as the convex hull of the Voronoi-cell centroids nearest to it, and these Delaunay
cells also tile space. Very often, the Delaunay tessellation is a triangulation of space, i.e.,
it is a partitioning of Rd into d-dimensional simplices (Torquato, 2002). Geometrically the
Voronoi and Delaunay tessellations are dual to each other. The contact network is only
defined for a packing in which a subset of the particles form interparticle contacts. For
example, when the set of points X defines the centers of spheres in a sphere packing, the
network of interparticle contacts forms the contact network of the packing by associating
with every sphere a “node” for each contact point and edges that connect all of the nodes. As
we will see in Sec. IV, the contact network is crucial to determining the rigidity properties of
the packing and corresponds to a subclass of the class of fascinating objects called tensegrity
frameworks, namely strut frameworks; see Connelly and Whiteley, 1996 for details. Figure
7 illustrates the Voronoi, Delaunay and contact networks for a portion of a packing of
congruent circular disks.
   Some of the infinite packings that we will be considering in this review can only


                                               13
FIG. 7 Geometric characterization of packings via bond networks. Left panel: Illustrations of the Voronoi
and Delaunay tessellations for a portion of a packing of congruent circular disks. The blue and red lines

are edges of the Voronoi and Delaunay cells, respectively. Right panel: The corresponding contact network

shown as green lines.


be characterized spatially via statistical correlation functions. For simplicity, consider a
nonoverlapping configuration of N identical d-dimensional spheres centered at the positions
rN ≡ {r1 , r2 , · · · , rN } in a region of volume V in d-dimensional Euclidean space Rd . Ulti-
mately, we will pass to the thermodynamic limit, i.e., N → ∞, V → ∞ such that the number
density ρ = N/V is a fixed positive constant. For statistically homogeneous sphere packings
in Rd , the quantity ρn gn (rn ) is proportional to the probability density for simultaneously
finding n sphere centers at locations rn ≡ {r1 , r2 , . . . , rn } in Rd (Hansen and McDonald,
1986). With this convention, each n-particle correlation function gn approaches unity when
all particle positions become widely separated from one another. Statistical homogeneity
implies that gn is translationally invariant and therefore only depends on the relative dis-
placements of the positions with respect to some arbitrarily chosen origin of the system,
i.e.,
                                      gn = gn (r12 , r13 , . . . , r1n ),                            (5)

where rij = rj − ri .
   The pair correlation function g2 (r) is the one of primary interest in this review. If the
system is also rotationally invariant (statistically isotropic), then g2 depends on the radial
distance r ≡ |r| only, i.e., g2 (r) = g2 (r). It is important to introduce the total correlation
function h(r) ≡ g2 (r) − 1, which, for a disordered packing, decays to zero for large |r|
sufficiently rapidly (Torquato and Stillinger, 2006b). We define the structure factor S(k) for



                                                    14
a statistically homogeneous packing via the relation

                                      S(k) = 1 + ρh̃(k),                                    (6)

where h̃(k) is the Fourier transform of the total correlation function h(r) ≡ g2 (r) − 1
and k is the wave vector. Since the structure factor is the Fourier transform of an au-
tocovariance function (involving the “microscopic” density) (Hansen and McDonald, 1986;
Torquato and Stillinger, 2006b), then it follows it is a nonnegative quantity for all k, i.e.,

                                   S(k) ≥ 0        for all k.                               (7)

The nonnegativity condition follows physically from the fact that S(k) is proportional
to the intensity of the scattering of incident radiation on a many-particle system
(Hansen and McDonald, 1986). The structure factor S(k) provides a measure of the density
fluctuations in the packing at a particular wave vector k.


III. LESSONS FROM DISORDERED JAMMED PACKINGS OF SPHERES


   The classical statistical mechanics of hard-sphere systems has generated a huge col-
lection of scientific publications, stretching back at least to Boltzmann, 1898.          That
collection includes examinations of equilibrium, transport, and jammed packing phe-
nomena.     With respect to the last of these, the concept of a unique “random
close packing” (RCP) state, pioneered by Bernal, 1960, 1965 to model the struc-
ture of liquids, has been one of the more persistent themes with a venerable history
(Anonymous, 1972; Berryman, 1983; Gotoh and Finney, 1974; Jodrey and Tory, 1985;
Jullien et al., 1997; Kamien and Liu, 2007; Pouliquen et al., 1997; Scott and Kilgour, 1969;
Tobochnik and Chapin, 1988; Visscher and Bolsterli, 1972; Zinchenko, 1994). Until about a
decade ago, the prevailing notion of the RCP state was that it is the maximum density that a
large, random collection of congruent (identical) spheres can attain and that this density is a
well-defined quantity. This traditional view has been summarized as follows: “Ball bearings
and similar objects have been shaken, settled in oil, stuck with paint, kneaded inside rubber
balloons–and all with no better result than (a packing fraction of) . . . 0.636” (Anonymous,
1972). Torquato et al., 2000 have argued that this RCP-state concept is actually ill-defined
and thus should be abandoned in favor of a more precise alternative.

                                              15
   It is instructive to review briefly these developments because they will point to the need
for a geometric-structure approach generally to understand jammed packings, whether dis-
ordered or not. It has been observed (Torquato et al., 2000) that there has existed ample
evidence in the literature, in the form of actual and computer-simulation experiments, to
suggest strongly that the RCP state is indeed ill-defined and, in particular, dependent on
the protocol used to produce the packings and on other system characteristics. In a classic
experiment, Scott and Kilgour, 1969 obtained the “RCP” packing fraction value φ ≈ 0.637
by pouring ball bearings into a large container, vertically vibrating the system for sufficiently
long times to achieve a putative maximum densification, and extrapolating the measured
volume fractions to eliminate finite-size effects. Important dynamical parameters for this
kind of experiment include the pouring rate as well as the amplitude, frequency and direc-
tion of the vibrations. The shape, smoothness and rigidity of the container boundary are
other crucial characteristics. For example, containers with curved or flat boundaries could
frustrate or induce crystallization, respectively, in the packings, and hence the choice of
container shape can limit the portion of configuration space that can be sampled. The key
interactions are interparticle forces, including (ideally) repulsive hard-sphere interactions,
friction between the particles (which inhibits densification), and gravity. The final packing
fraction will inevitably be sensitive to these system characteristics. Indeed, one can achieve
denser (partially and imperfectly crystalline) packings when the particles are poured at low
rates into horizontally shaken containers with flat boundaries (Pouliquen et al., 1997).
   It is tempting to compare experimentally observed statistics of so-called RCP configu-
rations (packing fraction, correlation functions, Voronoi statistics) to those generated on a
computer. One must be careful in making such comparisons since it is difficult to simulate
the features of real systems, such as the method of preparation and system characteristics
(shaking, friction, gravity, etc.). Nonetheless, computer algorithms are valuable because
they can be used to generate and study idealized random packings, but the final states
are clearly protocol-dependent. For example, a popular rate-dependent densification algo-
rithm (Jodrey and Tory, 1985; Jullien et al., 1997) achieves φ between 0.642 and 0.649, a
Monte Carlo scheme (Tobochnik and Chapin, 1988) gives φ ≈ 0.68, a differential-equation
densification scheme produces φ ≈ 0.64 (Zinchenko, 1994), and a “drop and roll” pro-
cedure (Visscher and Bolsterli, 1972) yields φ ≈ 0.60; and each of these protocols yields
different sphere contact statistics.

                                              16
  As noted earlier, it has been argued that these variabilities of RCP arise because it is
an ambiguous concept, explaining why there is no rigorous prediction of the RCP density,
in spite of attempts to estimate it (Berryman, 1983; Gotoh and Finney, 1974; Song et al.,
2008). The phrase “close packed” implies that the spheres are in contact with one another
with the highest possible average contact number Z. This would be consistent with the
aforementioned traditional view that RCP presents the highest density that a random pack-
ing of close-packed spheres can possess. However, the terms “random” and “close packed”
are at odds with one another. Increasing the degree of coordination (nearest-neighbor con-
tacts), and thus the bulk system density, comes at the expense of disorder. The precise
proportion of each of these competing effects is arbitrary, and therein lies a fundamental
problem. Moreover, since “randomness” of selected jammed packings has never been quan-
tified, the proportion of these competing effects could not be specified. To remedy these
serious flaws, Torquato et al., 2000 replaced the notion of “close packing” with “jamming”
categories (defined precisely in Sec. IV), which requires that each particle of a particular
packing has a minimal number of properly arranged contacting particles. Furthermore, they
introduced the notion of an “order metric” to quantify the degree of order (or disorder) of
a single packing configuration.
  Using the Lubachevsky-Stillinger (LS) (1990) molecular dynamics growth algorithm to
generate jammed packings, it was shown (Torquato et al., 2000) that fastest particle growth
rates generated the most disordered sphere (MRJ) packings (with φ ≈ 0.64; see the left
panel of Fig. 8), but that by slowing the growth rates larger packing fractions could be
                                                √
continuously achieved up to the densest value π/ 18 ≈ 0.74048 . . . such that the degree
of order increased monotonically with φ. Those results demonstrated that the notion of
RCP as the highest possible density that a random sphere packing can attain is ill-defined,
since one can achieve packings with arbitrarily small increases in density at the expense
of correspondingly small increases in order. This led Torquato et al., 2000 to supplant the
concept of RCP with the maximally random jammed (MRJ) state, which is defined to be
that jammed state with a minimal value of an order metric (see Sec. V). This work pointed
the way toward a quantitative means of characterizing all packings, namely, the geometric-
structure approach.
  We note that the same LS packing protocol that leads to a uniformly disordered jammed
state in three dimensions typically yields a highly crystalline “collectively” jammed packing

                                            17
FIG. 8 Typical protocols used to generate disordered sphere packings in three dimensions produce highly
crystalline packings in two dimensions. Left panel: A three-dimensional MRJ-like configuration of 500

spheres with φ ≈ 0.64 produced using the Lubachevsky-Stillinger (LS) algorithm with a fast expansion rate

(Torquato et al., 2000). Right panel: A crystalline collectively jammed configuration (Sec. IV.A) of 1000

disks with φ ≈ 0.88 produced using the LS algorithm with a fast expansion rate (Donev et al., 2004c).


in two dimensions. Figure 8 illustrates the vivid visual difference between the textures
produced in three and in two dimensions (see Section VII for further remarks). The low-
concentration occurrence of crystal defects in the latter is evidence for the notion that there
are far fewer collectively jammed states for N hard disks in two dimensions compared to
N hard spheres in three dimensions. This distinction can be placed in a wider context by
recalling that there is only one type of jammed state for hard rods in one dimension, and it
is a defect-free perfect one-dimensional crystal. These cases for d = 1, 2, and 3, numerical
results for MRJ packing for d = 4, 5, and 6, and theoretical results (Torquato and Stillinger,
2006b), indicating that packings in large dimensions are highly degenerate, suggest that the
number of distinct collectively jammed packings (defined in Sec. IV.A) for a fixed large
number N of identical hard spheres rises monotonically with Euclidean dimension d. The
questions and issues raised by these differences in the degree of disorder across dimensions
emphasizes the need for a geometric-structure approach, to be elaborated in the following.




                                                  18
IV. JAMMING CATEGORIES, ISOSTATICITY, AND POLYTOPES


   A. Jamming Categories


   In much of the ensuing discussion, we will treat packings of frictionless, congruent spheres
of diameter D in Rd in the absence of gravity, i.e., the “Ising model” of jammed sphere
packings. Packing spheres is inherently a geometrical problem due to exclusion-volume
effects. Indeed, the singular nature of the hard-sphere pair potential (plus infinity or zero
for r < D or r ≥ D, respectively, where r is the pair separation) is crucial because it enables
one to be precise about the concept of jamming. Analyzing this model directly is clearly
preferable to methods that begin with particle systems having “soft” interactions, which
are then intended to mimic packings upon passing to the hard-sphere limit (Donev et al.,
2007c).
   Three broad and mathematically precise “jamming” categories of sphere packings can be
distinguished depending on the nature of their mechanical stability (Torquato and Stillinger,
2001, 2003). In order of increasing stringency (stability), for a finite sphere packing, these
are the following: (1) Local jamming: Each particle in the packing is locally trapped by its
neighbors (at least d+1 contacting particles, not all in the same hemisphere), i.e., it cannot be
translated while fixing the positions of all other particles; (2) Collective jamming: Any locally
jammed configuration is collectively jammed if no subset of particles can simultaneously be
displaced so that its members move out of contact with one another and with the remainder
set; and (3) Strict jamming: Any collectively jammed configuration that disallows all uniform
volume-nonincreasing strains of the system boundary is strictly jammed.
   We stress that these hierarchical jamming categories do not exhaust the universe of possi-
ble distinctions (Connelly et al., 1998; Donev et al., 2004c,d; Torquato and Stillinger, 2001),
but they span a reasonable spectrum of possibilities. Importantly, the jamming category
of a given sphere configuration depends on the boundary conditions employed. For exam-
ple, hard-wall boundary conditions (Torquato and Stillinger, 2001) generally yield different
jamming classifications from periodic boundary conditions (Donev et al., 2004c). These jam-
ming categories, which are closely related to the concepts of “rigid” and “stable” packings
found in the mathematics literature (Connelly et al., 1998), mean that there can be no “rat-
tlers” (i.e., movable but caged particles) in the packing. Nevertheless, it is the significant


                                              19
majority of spheres that compose the underlying jammed network that confers rigidity to the
packing, and in any case, the rattlers could be removed (in computer simulations) without
disrupting the jammed remainder. Figure 9 shows examples of ordered locally and collec-
tively jammed packings of disks in two dimensions within hard-wall containers. Observe the
square-lattice packing with square hard-wall boundary conditions can only be collectively
jammed (not strictly jammed) even in the infinite-volume limit. This is to be contrasted
with MRJ packings, where the distinction between collective and strict jamming vanishes
in the infinite-volume limit, as discussed in Sec. IV.B. Note that the configurations shown
in Fig. 8, generated under periodic boundary conditions, are at least collectively jammed.




FIG. 9 Illustrations of jamming categories. Leftmost panel: Honeycomb-lattice packing within a rectan-
gular hard-wall container is locally jammed, but is not collectively jammed (e.g., a collective rotation of a

hexagonal particle cluster, as shown, will unjam the packing). Middle panel: Square-lattice packing within

a square hard-wall container is collectively jammed. Rightmost panel: The square-lattice packing shown

in the middle panel can be sheared and hence is not strictly jammed. Thus, we see that the square-lattice

packing with square hard-wall boundary conditions can only be collectively jammed even in the infinite-

volume limit. Thus, the distinction between collective and strict jamming for such packings remains in the

thermodynamic limit.


   To emphasize the fact that the jamming category depends on the boundary conditions
of a packing, we tabulate whether common periodic structures are locally, collectively or
strictly jammed. Table I gives the jamming classification for such packings with hard-wall
boundary conditions. These results are compared to corresponding jamming categories for
periodic boundary conditions in Table II. The latter results will depend on the choice of the
number of particles N within the fundamental cell.




                                                   20
TABLE I Classification of some of the common jammed periodic (crystal) packings of identical spheres
in two and three dimensions, where Z denotes the contact number per particle and φ is the packing
fraction for the infinite packing (Torquato and Stillinger, 2001). Here hard boundaries are applicable: in
two dimensions we use commensurate rectangular boundaries and in three dimensions we use a cubical
boundary, with the exception of the hexagonal close-packed crystal in which the natural choice is a
hexagonal prism.

          Periodic (crystal) structures             Locally jammed Collectively jammed Strictly jammed

       Honeycomb (Z = 3, φ = 0.605 . . .)                yes                no                  no

        Kagomé (Z = 4, φ = 0.680 . . .)                  noa               noa                 noa

         Square (Z = 4, φ = 0.785 . . .)                 yes                yes                 no

       Triangular (Z = 6, φ = 0.907 . . .)               yes                yes                yes

        Diamond (Z = 4, φ = 0.340 . . .)                 yes                no                  no

      Simple cubic (Z = 6, φ = 0.524 . . .)              yes                yes                 no

  Body-centered cubic (Z = 8, φ = 0.680 . . .)           yes                yes                 no

  Face-centered cubic (Z = 12, φ = 0.740 . . .)          yes                yes                yes

Hexagonal close-packed (Z = 12, φ = 0.740 . . .)         yes                yes                yes

 a With appropriately placed regular triangular- or hexagonal-shaped boundaries, the Kagomé structure


   is locally, collectively and strictly jammed.




                                                   21
.
TABLE II Classification of the same periodic sphere packings described in Table I but for
periodic boundary conditions (Donev et al., 2004c). We chose the smallest fundamental
cells with N particles for which an unjamming motion exists, if there is one. The lattice
vectors for each packing are the standard ones (Donev et al., 2004c)

Periodic (crystal) structures N Locally jammed Collectively jammed Strictly jammed

         Honeycomb            4         yes                 no                 no

           Kagomé            3         yes                 no                 no

           Square             2         yes                 no                 no

          Triangular          1         yes                yes                yes

          Diamond             4         yes                 no                 no

         Simple cubic         2         yes                 no                 no

     Body-centered cubic      2         yes                 no                 no

     Face-centered cubic      1         yes                yes                yes

    Hexagonal close-packed    2         yes                yes                yes

    Rigorous and efficient linear-programming algorithms have been devised to assess whether
a particular sphere packing is locally, collectively, or strictly jammed (Donev et al., 2004c,d).
It is noteworthy that the jamming categories can now be ascertained in real-system exper-
iments using imaging techniques that enable one to determine configurational coordinates
of a packing [e.g., tomography (Aste et al., 2006), confocal microscopy (Brujic et al., 2003)
and magnetic resonance imaging (Man et al., 2005)]. Given these coordinates (with high
precision), one can rigorously test the “jamming” category of the experimentally generated
packing using the aforementioned linear programming techniques.


    B. Isostaticity


    A packing of N hard spheres of diameter D in a jammed framework in d-dimensional
Euclidean space is characterized by the (Nd)-dimensional configuration vector of centroid
positions R = rN ≡ {r1 , . . . , rN }. Assume that a configuration RJ represents a collectively
jammed framework of a packing (i.e., excluding rattlers) with packing fraction φJ , where
there are M interparticle contacts.

                                              22
   Isostatic packings are jammed packings that possess the minimal number of contacts for a
jamming category; namely, under periodic boundary conditions, for collective jamming, M =
2N −1 and 3N −2 for d = 2 and d = 3, respectively, and for strict jamming, M = 2N +1 and
3N +3 for d = 2 and d = 3, respectively (Donev et al., 2005d). Thus, we see that the relative
differences between isostatic collective and strict jammed packings diminish as N becomes
large, and since the number of degrees of freedom is essentially equal to Nd (depending on
the jamming category and boundary conditions (Donev et al., 2005d)), an isostatic packing
has a mean contact number per particle, Z, equal to 2d. Collectively/strictly jammed MRJ
packings in the infinite-volume limit are isostatic. Note that packings in which Z = 2d are
not necessarily collectively or strictly jammed; for example, we see from Table II that the
square and Kagomé lattices (with Z = 4) and the simple-cubic lattice (with Z = 6) are
neither collectively nor strictly jammed. Isostaticity has attained a special status in the
field, and has been closely linked to “generic” or “random” packings (Moukarzel, 1998). In
fact, as we will show, isostatic packings can be perfectly ordered; see also Mari et al., 2008.
Packings having more contacts than isostatic ones are hyperstatic and those having fewer
contacts than isostatic packings are hypostatic; for sphere packings, these latter packings
cannot be collectively or strictly jammed in the above sense (Donev et al., 2007a). The
terms overconstrained and underconstrained (or hypoconstrained), respectively, were used
by Donev et al., 2007a to describe such packings.


   C. Polytope Picture of Configuration Space


   Full understanding of the many-body properties of N particles in a d-dimensional con-
tainer of content (volume) V is facilitated by viewing the system in its dN-dimensional
configuration space. This is an especially useful approach for hard-particle models, and
helps to understand the full range of issues concerning the approach to a jammed state.
For the moment, we restrict attention specifically the cases of d-dimensional hard spheres.
When container content V is very large for fixed N, i.e., when packing fraction φ ≈ 0, the
hard spheres are free to move virtually independently. Consequently, the measure (content)
C of the available multidimensional configuration space is simply C ≈ V N . But decreasing
V enhances the chance for sphere collisions and correspondingly reduces C, the remaining
fraction of configuration space that is free of sphere overlaps. The amount of reduction is


                                             23
related exponentially to the excess entropy S (e) (N, V ) for the N-sphere system:

                             C(N, V ) ≈ V N exp[S (e) (N, V )/kB ],                        (8)

where kB is Boltzmann’s constant.
   In the low-density regime, the excess entropy admits of a power series expansion in
covering fraction φ:
                           S (e) (N, V )    X  βn   φ n
                                         =N                 .                              (9)
                               NkB          n≥1
                                                n+1   v1
Here v1 is the volume of a particle, as indicated earlier in Eq. (2). The βn are the irre-
ducible Mayer cluster integral sums for n + 1 particles that determine the virial coefficient
of order n + 1 (Mayer and Mayer, 1940). For hard spheres in dimensions 1 ≤ d ≤ 8, these
coefficients for low orders 1 ≤ n ≤ 3 are known exactly, and accurate numerical estimates
are available for n + 1 ≤ 10 (Clisby and McCoy, 2006). This power series represents a func-
tion of φ obtainable by analytic continuation along the positive real axis to represent the
thermodynamic behavior for the fluid phase from φ = 0 up to the freezing transition, which
occurs at φ ≈ 0.4911 for hard spheres in three dimensions (Noya et al., 2008). This value
is slightly below the minimum density φ ≈ 0.4937 at which collective jamming of d = 3
hard spheres is suspected first to occur (Torquato and Stillinger, 2007). Consequently, the
available configuration space measured by C(N, V ) remains connected in this density range,
i.e., any nonoverlap configuration of the N spheres can be connected to any other one by a
continuous displacement of the spheres that does not violate the nonoverlap condition.
   A general argument has been advanced that thermodynamic functions must experience a
subtle, but distinctive, essential singularity at first-order phase transition points (Andreev,
1964; Fisher and Felderhof, 1970). In particular, this applies to the hard-sphere freezing
transition, and implies that attempts to analytically continue fluid behavior into a metastable
over-compressed state are dubious. Aside from any other arguments that might be brought
to bear, this indicates that such extrapolations are fundamentally incapable of identifying
unique random jammed states of the hard-sphere system. Nevertheless, it is clear that
increasing φ beyond its value at the thermodynamic freezing point soon initiates partial
fragmentation of the previously connected nonoverlap configuration space in finite systems.
That is, locally disconnected portions are shed, each to become an individual jammed state
displaying its own geometric characteristics. (The jammed tunneled crystals mentioned in
Sec. VI are examples of such localized regions near the freezing point.) We shall elaborate

                                             24
on this point within this subsection after discussing the polytope picture of configuration
space near jamming points.
   Consider decreasing the packing fraction slightly in a sphere packing that is at least
collectively jammed by reducing the particle diameter by ∆D, δ = ∆D/D ≪ 1, so that
the packing fraction is lowered to φ = φJ (1 − δ)d . We call δ the jamming gap or distance
to jamming. It can be shown that there is a sufficiently small δ that does not destroy the
jamming confinement property, in the sense that the configuration point R = RJ + ∆R
remains trapped in a small neighborhood J∆R around RJ (Connelly, 1982). Indeed, there
exists a range of positive values of δ that depends on N and the particle arrangements that
maintains the jamming confinement property. Let us call δ∗ the threshold value at which
jamming is lost. How does δ∗ scale with N for a particular d? An elementary analysis based
on the idea that in order for a neighbor pair (or some larger local group) of particles to
change places, the surrounding N − 2 (or N − 3, . . .) particles must be radially displaced
and compressed outward so as to concentrate the requisite free volume around that local
interchangeable group concludes that δ∗ ∼ CN −1/d , where the constant C depends on the
dimension d and the original jammed particle configuration.
   It is noteworthy that for fixed N and sufficiently small δ, it can be shown that asymptot-
ically (through first order in δ) the set of displacements that are accessible to the packing
approaches a convex limiting polytope (a closed polyhedron in high dimension) P∆R ⊆ J∆R
(Salsburg and Wood, 1962; Stillinger and Salsburg, 1969). This polytope P∆R is determined
from the linearized impenetrability equations (Donev et al., 2004c,d) and, for a fixed system
center of mass, is necessarily bounded for a jammed configuration. This implies that the
number of interparticle contacts M is at least one larger than the dimensionality dCS of
the relevant configuration space. Examples of such low-dimensional polytopes for a single
locally jammed disk are shown in Fig. 10.
   Importantly, for an isostatic contact network, P∆R is a simplex (Donev et al., 2005d). A
d-dimensional simplex in Rd is a closed convex polytope whose d + 1 vertices (0-dimensional
points) do not all lie in a (d − 1)-dimensional flat sub-space or, alternatively, it is a finite
region of Rd enclosed by d+1 hyperplanes [(d−1)-dimensional “faces”] (e.g., a triangle for d =
2, a tetrahedron for d = 3 or a pentatope for d = 4). For overconstrained jammed packings
(e.g., ordered maximally dense states), the limiting high-dimensional polytopes have more
faces than simplices do and can be geometrically very complex (Salsburg and Wood, 1962;

                                             25
FIG. 10 The polytope of allowed displacements P∆R for a locally jammed disk (light shade) trapped among
three (left) or six (right, as in the triangular lattice) fixed disks (blue). The exclusion disks (dashed lines)

of diameter twice the disk diameter are drawn around each of the fixed disks, along with their tangents (red

lines) and the polytope P∆R they bound (black). The polytope for the isostatic (left) and overconstrained

(right) case is a triangle and hexagon, respectively.


Stillinger and Salsburg, 1969). The fact that P∆R is a simplex for an isostatic packing
enables one to derive rigorous results, as we will now describe.
   Consider adding thermal kinetic energy to a nearly jammed sphere packing in the absence
of rattlers. While the system will not be globally ergodic over the full system configuration
space and thus not in thermodynamic equilibrium, one can still define a macroscopic pres-
sure p for the trapped but locally ergodic system by considering time averages as the system
executes a tightly confined motion around the particular configuration RJ . The probability
distribution Pf (f ) of the time-averaged interparticle forces f has been rigorously linked to
the contact value r = D of the pair correlation function g2 (r) defined in Section II, and this
in turn can be related to the distribution of simplex face hyperareas for the limiting polytope
(Donev et al., 2005d). Moreover, since the available (free) configuration volume scales in a
predictable way with the jamming gap δ, one can show that the reduced pressure is asymptot-
ically given by the free-volume equation of state (Donev et al., 2005d; Salsburg and Wood,
1962; Stillinger and Salsburg, 1969),
                                          p    1       d
                                              ∼ =             ,                                            (10)
                                        ρkB T  δ  1 − (φ/φJ )
where T is the absolute temperature and ρ is the number density. So far as the limiting
polytope picture is concerned, the extremely narrow connecting filaments that in principle
connect the jamming neighborhoods have so little measure that they do not overturn the
free-volume leading behavior of the pressure, even as system size is allowed to go to infinity.

                                                     26
Although there is no rigorous proof yet for this claim, all numerical evidence strongly suggests
that it is correct. Relation (10) is remarkable, since it enables one to determine accurately
the true jamming density of a given packing, even if the actual jamming point has not quite
yet been reached, just by measuring the pressure and extrapolating to p = +∞.




FIG. 11 The isothermal phase behavior of three-dimensional hard-sphere model in the pressure-packing
fraction plane, adapted from Torquato, 2002. Increasing the density plays the same role as decreasing

temperature of a molecular liquid; see Fig. 3. Three different isothermal densification paths by which

a hard-sphere liquid may jam are shown. An infinitesimal compression rate of the liquid traces out the

thermodynamic equilibrium path (shown in green), including a discontinuity resulting from the first-order

freezing transition to a crystal branch. Rapid compressions of the liquid while suppressing some degree

of local order (blue curves) can avoid crystal nucleation (on short time scales) and produce a range of

amorphous metastable extensions of the liquid branch that jam only at the their density maxima.


   This free-volume form has been used to estimate the equation of state along “metastable”
extensions of the hard-sphere fluid up to the infinite-pressure endpoint, assumed to be ran-
dom jammed states (Torquato, 1995b, 2002). To understand this further, it is useful to recall
the hard-sphere phase behavior in three dimensions; see Fig. 11. For densities between zero
and the “freezing” point (φ ≈ 0.49), the thermodynamically stable phase is a liquid. Increas-
ing the density beyond the freezing point results in a first-order phase transition to a crystal
branch that begins at the melting point (φ ≈ 0.55) and whose ending point is the maximally
dense fcc packing (φ ≈ 0.74), which is a jammed packing in which each particle contacts 12


                                                 27
others (Mau and Huse, 1999). However, compressing a hard-sphere liquid rapidly, under the
constraint that significant crystal nucleation is suppressed, can produce a range of metastable
branches whose density end points are random “jammed” packings (Rintoul and Torquato,
1996b; Torquato, 2002), which can be regarded to be glasses. A rapid compression leads to
a lower random jammed density than that for a slow compression. The most rapid com-
pression presumably leads to the MRJ state with φ ≈ 0.64 (Torquato, 2002). Torquato,
1995a,b reasoned that the functional form of the pressure of the stable liquid branch (which
appears to be dominated by an unphysical pole at φ = 1) must be fundamentally different
from the free-volume form (10) that applies near jammed states, implying that the equation
of state is nonanalytic at the freezing point and proposed the following expression along any
constrained metastable branch:

                      p              1 − φF /φJ
                          = 1 + 4φgF                   for φF ≤ φ ≤ φJ ,                   (11)
                    ρkB T             1 − φ/φJ

where φF ≈ 0.491 is the packing fraction at the freezing point, gF ≈ 5.72 is the corresponding
value of the pair correlation function at contact, and φJ is the jamming density, whose value
will depend on which metastable path is chosen. [Torquato, 1995a,b actually considered the
more general problem of nearest-neighbor statistics of hard-sphere systems, which required
an expression for the equation of state.] Unfortunately, there is no unique metastable branch
(see Fig. 11) because it depends on the particular constraints used to generate the metastable
states or, in other words, the protocol employed, which again emphasizes one of the themes
of this review. Moreover, in practice, metastable states of identical spheres in R3 have
an inevitable tendency to crystallize (Rintoul and Torquato, 1996b), but even in binary
mixtures of hard spheres chosen to avoid crystallization the dispersion of results and ultimate
nonuniqueness of the jammed states still apply. We note that Kamien and Liu, 2007 assumed
the same free-volume form to fit the pressure of “metastable” states for monodisperse hard
spheres as obtained from both numerical and experimental data to determine φJ . Their best
fit yielded φJ = 0.6465.
   We note that density of states (vibrational modes) in packings of soft spheres has been
the subject of recent interest (Silbert et al., 2005; Wyart et al., 2005). Collective jamming in
hard-sphere packings corresponds to having no “soft modes” in soft-sphere systems, i.e., no
unconstrained local or global particle translations are allowed, except those corresponding
to rattlers. Observe that it immediately follows that if a hard-sphere packing is collectively

                                             28
jammed to first order in δ, a corresponding configuration of purely soft repelling particles
will possess quadratic modes in the vibrational energy spectrum for such a system of soft
spheres.


V. ORDER METRICS


   The enumeration and classification of both ordered and disordered jammed sphere pack-
ings for the various jamming categories is an outstanding problem. Since the difficulty of the
complete enumeration of jammed packing configurations rises exponentially with the number
of particles, it is desirable to devise a small set of intensive parameters that can characterize
packings well. One obvious property of a sphere packing is the packing fraction φ. Another
important characteristic of a packing is some measure of its “randomness” or degree of dis-
order. We have stressed that one ambiguity of the old RCP concept was that “randomness”
was never quantified. To do so is a nontrivial challenge, but even the tentative solutions
that have been put forth during the last decade have been profitable not only to characterize
sphere packings (Kansal et al., 2002b; Torquato and Stillinger, 2003; Torquato et al., 2000;
Truskett et al., 2000) but also glasses, simple liquids, and water (Errington and Debenedetti,
2001; Errington et al., 2002, 2003; Truskett et al., 2000).
   One might argue that the maximum of an appropriate “entropic” metric would be a
potentially useful way to characterize the randomness of a packing and therefore the MRJ
state. However, as pointed out by Kansal et al., 2002b, a substantial hurdle to overcome in
implementing such an order metric is the necessity to generate all possible jammed states
or, at least, a representative sample of such states in an unbiased fashion using a “universal”
protocol in the large-system limit, which is an intractable problem. Even if such a universal
protocol could be developed, however, the issue of what weights to assign the resulting config-
urations remains. Moreover, there are other fundamental problems with entropic measures,
as we will discuss in Sec. VIII, including its significance for two-dimensional monodisperse
hard-disk packings as well as polydisperse hard-disk packings with a sufficiently narrow size
distribution. It is for this reason that we seek to devise order metrics that can be applied
to single jammed configurations, as prescribed by the geometric-structure point of view.
   A many-body system of N particles is completely characterized statistically by its N-body
probability density function P (R; t) that is associated with finding the N-particle system


                                              29
with configuration R at some time t. Such complete information is virtually never available
for large N and, in practice, one must settle for reduced information, such as a scalar order
metric ψ. Any order metric ψ conventionally possesses the following three properties: (1)
it is a well-defined scalar function of a configuration R; (2) it is subject typically to the
normalization 0 ≤ ψ ≤ 1; and, (3) for any two configurations RA and RB , ψ(RA ) > ψ(RB )
implies that configuration RA is to be considered as more ordered than configuration RB .
The set of order parameters that one selects is unavoidably subjective, given that there
appears to be no single universal scalar measure of order. However, one can construct order
metrics that lead to consistent results (e.g., common minima for jammed packings), as we
will discuss after considering specific examples.


   A. Specific Order Metrics


   Many relevant order metrics have been devised, but here we briefly describe only some
of them. The bond-orientational order Qℓ (Steinhardt et al., 1983) in three dimensions
is defined in terms of the spherical harmonics Yℓm (θi , ϕi ), where θi and ϕi are the polar
and azimuthal angles (relative to a fixed coordinate system) of the near-neighbor bond for
particle pair i. A near neighbor could be defined as any sphere within a specified local
radius (e.g., set by the first minimum of the pair correlation function beyond contact) or by
a sphere within a face-sharing Voronoi polyhedron (Torquato, 2002). The average of Qℓ over
all of the near-neighbor bonds Nb provides a global measure of symmetries in many-particle
systems. Of particular interest is the average when ℓ = 6, i.e.,
                                                              2
                                                                   1/2
                                      6        Nb
                                   4π X    1   X
                         Q6 ≡                    Y6m (θi , ϕi )         ,               (12)
                                   13 m=−6 Nb i=1

since it reaches its maximum value for the perfect fcc lattice and is zero for a Poisson
(uncorrelated) point distribution in the infinite-volume limit (Rintoul and Torquato, 1996a)
(see Fig. 12 for the two-dimensional analog). It is seen that Q ≡ Q6 /Qf6 cc lies in the closed
interval [0,1] and therefore qualifies as an order metric (Torquato et al., 2000).
   A more local measure of bond-orientational order, Q6,local , can be obtained by evaluating
the bond order at each sphere individually, and then averaging over all spheres (Kansal et al.,




                                              30
2002b), i.e.,
                                                                                     1/2
                                      N            6             nj               2
                                    1 X         4π X           1 X
                       Q6,local ≡                                    Y6m (θi , ϕi )        ,            (13)
                                    N j=1       13 m=−6 nj i=1

where nj is the number of nearest-neighbors of sphere j. This is analogous to the two-
dimensional definition of local bond-orientational order studied by Kansal et al., 2000. As
noted in that work, such a local measure of order is more sensitive to small crystalline
regions within a packing than is its global counterpart Q6 , and thus avoids the possibility
of “destructive” interference between differently oriented crystalline regions.




FIG. 12 Two types of order. (a) Bond-orientational order contains information about the orientation of
the vectors connecting neighboring particles in the packing of interest (left). If these orientations persist

throughout the packing, as they do in a triangular lattice (right), the packing is considered to be perfectly

bond-orientationally ordered. (b) Translational order contains information about the relative spacing of

particles in the packing of interest (left) relative to that of the densest packing at the same density (right).


   Using the fcc lattice radial coordination structure as a reference system, one can define
a translational order metric T based upon the mean occupation of sphere centers within
thin concentric shells around each sphere in the packing as compared to the mean occu-
pation of the same shells in the fcc lattice and the ideal gas at the same packing fraction
(Torquato et al., 2000; Truskett et al., 2000), i.e.,
                                                 NX
                                                  shells

                                                           ni − nideal
                                                                         
                                                                 i
                                                  i=1
                                       T ≡      NX
                                                                             .                            (14)
                                                 shells

                                                           nfcc  ideal
                                                                       
                                                            i − ni
                                                 i=1



                                                          31
Here ni is the average occupancy of the ith shell, with superscripts having the obvious
meaning, and Nshells is the total number of shells employed. Figure 12 illustrates the two-
dimensional analog of this order metric.
   All of the order metrics defined above were constructed to yield their maximum values of
unity (when appropriately normalized) for the densest and most symmetrical (close-packed
crystal) packing. Order metrics that are not based on any specific crystal structure have also
been devised. For example, two different translational order metrics have been constructed
that are based on functionals of the pair correlation function (Truskett et al., 2000). It has
been suggested that local density fluctuations within a “window” of a given size also can be
a useful order metric (Torquato and Stillinger, 2003). In particular, calculation of the local
number variance for a variety of crystal, quasicrystal and “hyperuniform” disordered point
patterns reveals that it provides a useful rank-order of these hyperuniform spatial patterns
at large length scales (Torquato and Stillinger, 2003; Zachary and Torquato, 2009). A hype-
runiform point pattern is one which the infinite-wavelength density fluctuations vanish or,
equivalently, possesses a structure factor S(k) (defined in Sec. II) that tends to zero in the
limit k → 0 (Torquato and Stillinger, 2003).


   B. Characteristics of a Good Order Metric


   The specific order metrics have both strengths and weaknesses. This raises the question
of what are the characteristics of a good order metric? There is clearly an enormous family
of scalar functions that possess the aforementioned three generic properties of an order
metric ψ, but they may not necessarily be useful ones. It has been suggested that a good
order metric should have the following additional properties (Kansal et al., 2002b): (1)
sensitivity to any type of ordering without bias toward any reference system; (2) ability to
reflect the hierarchy of ordering between prototypical systems given by common physical
intuition (e.g., perfect crystals with high symmetry should be highly ordered, followed by
quasicrystals, correlated disordered packings without long-range order, and finally spatially
uncorrelated or Poisson distributed particles); (3) capacity to detect order at any length
scale; and (4) incorporation of both the variety of local coordination patterns as well as
the spatial distribution of such patterns should be included. Moreover, any useful set of
order metrics should consistently produce results that are positively correlated with one


                                            32
another (Torquato, 2002; Torquato et al., 2000). The development of improved order metrics
deserves continued research attention.


VI. ORDER MAPS AND OPTIMAL PACKINGS


  The geometric-structure classification naturally emphasizes that there is a great diver-
sity in the types of attainable jammed packings with varying magnitudes of overall order,
density, and other intensive parameters. The notions of “order maps” in combination with
the mathematically precise “jamming categories” enable one to view and characterize well-
known packing states, such as the densest sphere packing (Kepler’s conjecture) and max-
imally random jammed (MRJ) packings as extremal states in the order map for a given
jamming category. Indeed, this picture encompasses not only these special jammed states,
but an uncountably infinite number of other packings, some of which have only recently been
identified as physically significant, e.g., the jamming-threshold states (least dense jammed
packings) as well as states between these and MRJ.
  The so-called order map (Torquato et al., 2000) provides a useful means to classify pack-
ings, jammed or not. It represents any attainable hard-sphere configuration as a point in
the φ-ψ plane. This two-parameter description is but a very small subset of the relevant pa-
rameters that are necessary to fully characterize a configuration, but it nonetheless enables
one to draw important conclusions. For collective jamming, a highly schematic order map
has previously been proposed (Torquato et al., 2000).
  Here we present a set of refined order maps for each of three jamming categories in R3 (see
Fig. 13) based both upon early work (Kansal et al., 2002b; Torquato et al., 2000) and the
most recent investigations (Donev et al., 2004c; Torquato and Stillinger, 2007). Crucially,
the order maps shown in Fig. 13 are generally different across jamming categories and
independent of the protocols used to generate hard-sphere configurations, and for present
purposes include rattlers. In practice, one needs to use a variety of protocols to produce
jammed configurations in order to populate the interior and to delineate the boundary of
the jammed regions shown in the Fig. (Kansal et al., 2002b). Moreover, the frequency of
occurrence of a particular configuration is irrelevant insofar as the order map is concerned.
In other words, the order map emphasizes a geometric-structure approach to packing by
characterizing single configurations, regardless of how they were generated or their occur-


                                            33
FIG. 13 Schematic order maps in the density-order (φ-ψ) plane for the three different jamming categories
in R3 under periodic boundary conditions. White and blue regions contain the attainable packings, blue

regions represent the jammed subspaces, and dark shaded regions contain no packings. The locus of points

A-A′ correspond to the lowest-density jammed packings. The locus of points B-B ′ correspond to the densest

jammed packings. Points MRJ represent the maximally random jammed states, i.e., the most disordered

states subject to the jamming constraint. It should be noted that the packings represented are not subject

to rattler exclusion.




FIG. 14 Three different optimal strictly jammed packings identified in the right most graph of Fig.
13. Left panel: A: Z = 7. Middle panel: MRJ: Z = 6 (isostatic). Right panel: B: Z = 12.


rence probability. In Fig. 13, the white and blue regions represent geometrically possible
configurations, while the dark shaded regions are devoid of packings (e.g., maximally dense
packings with very low order-metric values do not exist). Clearly, an appreciably reduced
region of attainable packings will be occupied by jammed packings and, for any finite pack-
ing, its size must decrease as the stringency of the jamming category increases. In the
infinite-size limit (not depicted in Fig. 13), the regions occupied by collectively and strictly
jammed sets become identical. The following extremal points or loci in each jammed region
are particularly interesting (Fig. 14):


                                                  34
   1. The locus of points A-A′ corresponds to the lowest-density jammed packings.
      We denote by φmin the corresponding jamming-threshold packing fraction. These
      packings are expected to be characterized by a relatively high degree of order
      (Torquato and Stillinger, 2007).
   2. The locus of points B-B ′ correspond to the densest jammed packings with packing
      fraction φmax .
   3. The MRJ point represents the maximally random jammed state. Exclusion of rattlers
      from the MRJ state compromises its maximal irregularity; the corresponding displaced
      position in the order map involves a small reduction in packing fraction from φ ≈ 0.64
      and a slight increase in order measure.
   4. More generally, any point along the boundary of the blue region is an extremal point,
      residing at the limit of attainability for the jamming category under consideration.

   A. Strict Jamming

   We will first discuss the strict-jamming order map.         The densest sphere packings
in three dimensions, which lie along the locus B-B ′ are strictly jammed (Donev et al.,
2004c; Torquato and Stillinger, 2001), implying that their shear moduli are infinitely large
(Torquato et al., 2003). We take point B to correspond to the fcc packing, i.e., it is the most
ordered and symmetric densest packing. The other points along the line B-B ′ represent the
stacking variants of the fcc packing. All can be conveniently viewed as stacks of planar tri-
angular arrays of spheres, within which each sphere contacts six neighbors. These triangular
layers can be stacked on one another, fitting spheres of one layer into “pockets” formed by
nearest-neighbor triangles in the layer below. At each such layer addition there are two
choices of which set of pockets in the layer below are to be filled. Thus, all of the stacking
variants can individually be encoded by an infinite binary sequence and therefore constitute
an uncountably infinite number of maximally dense packings called the Barlow packings
(Barlow, 1883). The most disordered subset of these is denoted by point B ′ . A rigorous
                    √
proof that φmax = π/ 18 = 0.74048 . . . has only recently appeared (Hales, 2005). In two
dimensions, the strictly jammed triangular lattice is the unique densest packing (Fejes Tóth,
1964) and so for d = 2 the line B-B ′ collapses to a single point B.
   The MRJ state is a well-defined minimum in an order map in that for a particular choice
of jamming category and order metric it can be identified unambiguously. The MRJ concept
is automatically compromised by passing either to the maximal packing density (fcc and its

                                             35
stacking variants) or the minimal possible density for strict jamming (tunneled crystals),
thereby causing any reasonable order metric to rise on either side. This eliminates the
possibility of a flat horizontal portion of the lower boundary of the jammed accessible region
in the φ − ψ plane in Fig. 13 (multiple MRJ states with different densities) and therefore
indicates the uniqueness of the MRJ state in density for a particular order metric. Indeed, at
least for collective and strict jamming in three dimensions, a variety of sensible order metrics
produce an MRJ state with a packing fraction approximately equal to 0.64 (Kansal et al.,
2002b) (see Fig. 8), close to the traditionally advocated density of the RCP state, and with
an isostatic mean contact number Z = 6. This consistency among the different order metrics
speaks to the utility of the order-metric concept, even if a perfect order metric has not yet
been identified. However, the packing fraction of the MRJ state should not be confused with
the MRJ state itself. It is possible to have a rather ordered strictly jammed packing at this
very same density (Kansal et al., 2002b), as indicated in Fig. 13; for example, a jammed
but vacancy-diluted fcc lattice packing. This is one reason why the two-parameter order
map description of packings is not only useful, but necessary. In other words, density alone
is far from sufficient in characterizing a jammed packing.
   The packings corresponding to the locus of points A-A′ have received little attention
until recently. Although it has not yet been rigorously established as such, a candidate
for the lower limiting packing fraction φmin for strictly jammed packings is the subset of
“tunneled crystals” that contain linear arrays of vacancies (Torquato and Stillinger, 2007).
These relatively sparse structures are generated by stacking planar “honeycomb” layers one
upon another, and they all amount to removal of one-third of the spheres from the maximally
dense structures with packing fraction φmax . Consequently, φmin = 2φmax /3 = 0.49365 . . ..
Every sphere in a tunneled crystal contacts 7 immediate neighbors in one of two possible
coordination geometries, and all of the stacking variants exhibit some form of long-range
order. It is appropriate to view the two families of maximum-density and of minimum-density
strictly jammed packings as structural siblings of one another. Note that jammed packings
can trivially be created whose densities span the entire range between these extremal cases
simply by filling an arbitrary fraction of the vacant sites in any one of the tunneled structures.
The dashed lines joining the points A to B and points A′ to B ′ shown in Fig. 13 are the
result of sequentially filling the most ordered and disordered tunneled crystals with spheres
until the filling process ends with the most ordered and disordered densest Barlow packings,

                                              36
respectively. Interestingly, the tunneled crystals exist at the edge of mechanical stability,
since removal of any one sphere from the interior would cause the entire packing to collapse.
It is noteworthy that Burnell and Sondhi, 2008 have shown that an infinite subclass of
the tunneled crystals has an underlying topology that greatly simplifies the determination
of their magnetic phase structure for nearest-neighbor antiferromagnetic interactions and
O(N) spins.
  It should come as no surprise that ensemble methods that produce “most probable”
configurations typically miss interesting extremal points in the order map, such as the locus
of points A-A′ and the rest of the jamming-region boundary, including remarkably enough
the line B-B ′ . However, numerical protocols can be devised to yield unusual extremal
jammed states, as discussed in Sec. VII, for example.
  Observe that irregular jammed packings can be created in the entire non-trivial range
of packing fraction 0.64 < φ < 0.74048 . . . (Kansal et al., 2002b; Torquato et al., 2000)
using the LS algorithm. Thus, in the rightmost plot in Fig. 13, the MRJ-B ′ portion of the
boundary of the jammed set, possessing the lowest order metric, is demonstrably achievable.
Until recently, no algorithms have produced disordered strictly jammed packings to the
left of the MRJ point. A new algorithm described elsewhere (Torquato and Jiao, 2010c)
has indeed yielded such packings with φ ≈ 0.60, which are overconstrained with Z ≈ 6.4,
implying that they are more ordered than the MRJ state (see Sec. VII for additional details).
The existence of disordered strictly jammed packings with such anomalously low densities
expands conventional thinking about the nature and diversity of disordered packings and
places in a broader context those protocols that produce “typical” configurations.
  Indeed, there is no fundamental reason why the entire lower boundary of the jammed set
between the low-density jamming threshold and MRJ point cannot also be realized. Note
that such low-density disordered packings are not so-called “random loose” packings, which
are even less well-defined than RCP states. For example, it is not clear that the former are
even collectively jammed. A necessary first step would be to classify the jamming category
of a random loose packing (RLP), which has yet to be done. Therefore, in our view, the
current tendency in the literature to put so-called RCP and RLP on the same footing as far
as jamming is concerned (Song et al., 2008) is premature at best.
  In R2 , the so-called “reinforced” Kagomé packing with precisely 4 contacts per particle
(in the infinite-packing limit) is evidently the lowest density strictly jammed subpacking of

                                            37
                                                                     √
the triangular lattice packing (Donev et al., 2004c) with φmin =         3π/8 = .68017 . . .. Note
that this packing has the isostatic contact number Z = 4 and yet is an ordered packing,
which runs counter to the prevalent notion that isostaticity is a consequence of “genericity”
or randomness (Moukarzel, 1998).


   B. Collective and Local Jamming


   Observe that the locus of points B-B ′ is invariant under change of the jamming category,
as shown in Fig. 13. This is not true of the MRJ state, which will generally have a differ-
ent location in the local-jamming and collective-jamming order maps. Another important
distinction is that it is possible to pack spheres subject only to the weak locally-jammed
criterion, so that the resulting packing fraction is arbitrarily close to zero (Böröczky, 1964;
Stillinger et al., 2003). But demanding either collective jamming or strict jamming evidently
forces φ to equal or exceed a lower limit φmin that is well above zero.


   C. Broader Applications to Other Condensed States of Matter


   Although methods for characterizing structural order in regular crystalline solids are well
established (Ashcroft and Mermin, 1976; Chaikin and Lubensky, 1995), similar techniques
for noncrystalline condensed states of matter are not nearly as advanced. The notions of
order metrics and order maps have been fruitfully extended to characterize the degree of
structural order in condensed phases of matter in which the constituent molecules (jammed
or not) possess both attractive and repulsive interactions. This includes the determination
of the order maps of models of simple liquids, glasses and crystals with isotropic interactions
(Errington et al., 2003; Truskett et al., 2000), models of water (Errington and Debenedetti,
2001; Errington et al., 2002), and models of amorphous polymers (Stachurski, 2003).


VII. PROTOCOL BIAS, LOSS OF ERGODICITY, AND NONUNIQUENESS OF
JAMMED STATES


   A dilute system of N disks or spheres is free to reconfigure largely independently of
particle-pair nonoverlap constraints. However, as φ increases either as a result of compression


                                              38
or of particle size growth, those constraints consume larger and larger portions of the dN-
dimensional configuration space, making reconfiguring more and more difficult. Indeed,
the available subspace begins to fracture, producing isolated “islands” that each eventually
collapse with increasing φ into jammed states (Salsburg and Wood, 1962). This fracturing,
or disconnection, implies dynamical non-ergodicity. Owing to permutation possibilities for
N identical objects, each disconnected region belongs to a large family of essentially N!
equivalent regions. But the configuration space fracturing has even greater complexity in
that the number of inequivalent such families and their jamming limits rises exponentially
with N in the large-system asymptotic limit. The jamming-limit φ values for the families
vary over the ranges indicated in Fig. 13 for collective and strict jamming.




FIG. 15 A schematic of the disjoint set of nearly jammed packings that develop in multidimensional
configuration space as covering fraction φ increases. The two axes represent the collection of configurational

coordinates. Note that each individual region approaches a polytope in the jamming limit, as discussed in

Sec. IV.C.


   Figure 15 offers a simple schematic cartoon to illustrate this dN-dimensional discon-
nection feature. Several allowed regions with different sizes and shapes are shown. Their
boundaries consist of sets of slightly curved hypersurfaces, each of which corresponds to a
particle pair contact, or contact with a hard wall if present. Particle growth or system com-
pression causes hypersurfaces (numbering at least dN + 1 for hard walls) to move inward,
reducing region content toward zero. The larger the region shown, the larger should be
understood its jamming φ value. The basic issue involved in either laboratory or computer
experiments is how and why the various jamming protocols used populate the disconnected


                                                    39
regions. Presumably any given algorithm has associated with it a characteristic set of occu-
pation weights, leading in turn to well-defined averages for any property of interest, including
packing fraction φ and any chosen order metric ψ. The fact that these averages indeed vary
with algorithm is a major point of the present review.
   Ensemble methods have been invoked to attach special significance to so-called “typical”
or “unique” packings because of their frequency of occurrence in the specific method em-
ployed. In particular, significance has been attached to the so-called unique J (jammed)
point, which is suggested to correspond to the onset of collective jamming in soft sphere
systems (O’Hern et al., 2003). The order maps described in Sec. V as well as the ensuing
discussion demonstrate that claims of such uniqueness overlook the wide variability of pack-
ing algorithms and the distribution of configurations that they generate. Individual packing
protocols (numerical or experimental) produce jammed packings that are strongly concen-
trated in isolated pockets of configuration space that are individually selected by those
protocols. Therefore, conclusions drawn from any particular protocol are highly specific
rather than general in our view.
   Indeed, one can create protocols that can lead to jammed packings at any preselected
density with a high probability of occurrence anywhere over a wide density range. Unless it
were chosen to be highly restrictive, a typical disk or sphere jamming algorithm applied to a
large number N of particles would be capable of producing a large number of geometrically
distinguishable results. In particular, these distinguishable jammed configurations from
a given algorithm would show some dispersion in their φ and ψ values. However, upon
comparing the distributions of obtained results for a substantial range of particle numbers
N (with fixed boundary conditions), one must expect a narrowing of those distributions with
increasing N owing to operation of a central limit theorem. Indeed, this narrowing would
converge individually onto values that are algorithm-specific, i.e., different from one another.
Figure 16 provides a clear illustration of such narrowing with respect to φ distributions, with
evident variation over algorithms, as obtained by Jiao et al., 2010b The examples shown
contrast results for two distinctly different sphere system sizes (∼ 250 and ∼ 2500 particles),
and for two different algorithms that have results for disordered jammed packings converging,
respectively, onto packing fractions of about 0.60, 0.64, 0.68 and 0.72 The histogram for the
lowest density was produced using the new algorithm (Torquato and Jiao, 2010c) noted
in Section VI, while the other two histograms were generated using the LS algorithm. We

                                             40
FIG. 16 Packing protocols can be devised that lead to strictly jammed states at any specific density with
a high probability of occurrence anywhere over a wide density range. Shown are histograms of jammed

packings that are centered around four different packing fractions: φ ≈ 0.60, 0.64, 0.68 and 0.72, as obtained

by Jiao et al., 2010b. The distributions become narrower as the system size increases.


stress once again that any temptation to select a specific φ value as uniquely significant (e.g.,
0.64) is primarily based on inadequate sampling of the full range of algorithmic richness and
diversity that is available at least in the underlying mathematical theory of sphere jamming.


VIII. ATTRIBUTES OF THE MAXIMALLY RANDOM JAMMED STATE


   The MRJ state under the strict-jamming constraint is a prototypical glass
(Torquato and Stillinger, 2007) in that it is maximally disordered without any long-
range order and perfectly rigid (the elastic moduli are indeed unbounded (Torquato et al.,
2003)). This endows such packings, which are isostatic (Z = 2d), with special attributes
(Donev et al., 2005a,d). For example, the pair correlation function g2 (r) (which provides the


                                                    41
              3                                                   5
                                                                                                0.04


             2.5                                                           Linear fit
                                                                  4
                                                                                                0.02
              2
                                                                  3




                                                           S(k)
     g2(r)




             1.5                                                                                 0
                                                                       0   0.2          0.4   0.6
                                                                  2
              1

                                                                  1        Data
             0.5

              0                                                   0
               0   0.25   0.5           0.75   1   1.25            0             0.5             1         1.5     2
                                r/D-1                                                         kD/2π



FIG. 17 Pair statistics for packings in the immediate neighborhood of the three-dimensional MRJ state
(Kansal et al., 2002b) with φ ≈ 0.64. Left panel: Computational data on the pair correlation function

g2 (r) versus r/D − 1 averaged over 5 packings of 10, 000 spheres (Donev et al., 2005d) of diameter D. It is

normalized so that at large distances it tends to unity, indicating no long-range order. The split second peak,

the discontinuity at twice the sphere diameter, and the divergence near contact are clearly visible. Right

panel: The corresponding structure factor S(k) as a function of the dimensionless wavenumber kD/(2π) for

a million particle packing (Donev et al., 2005a). The inset shows the linear ( |k|) nonanalytic behavior at

k = 0.


distribution of pair distances) of three-dimensional MRJ packings possesses a split second
peak (Zallen, 1983), with a prominent discontinuity at twice the sphere diameter, as shown
in the left panel of Fig. 17, which is a well-known characteristic of disordered jammed pack-
                         √
ings. The values r = 3D and r = 2D are highlighted in the figure, and match the two
observed singularities. Interestingly, an integrable power-law divergence (1/(r/D − 1)α with
                                                                                       √
α ≈ 0.4) exists for near contacts (Donev et al., 2005d). No peaks are observed at r = 2D
       √
or r = 5D, which are typical of crystal packings, indicating that there is no detectable
undistorted crystal ordering in the packing. We note that in a computational study of stiff
“soft” spheres (Silbert et al., 2002), a nearly square-root divergence for near contacts was
found.
   The MRJ state possesses unusual spatial density fluctuations.                                       It was conjectured
(Torquato and Stillinger, 2003) that all strictly jammed saturated packings of congruent
spheres (disordered or not) are hyperuniform, i.e., infinite-wavelength density fluctuations
vanish or, equivalently, the structure factor S(k) vanishes in the limit k → 0. (Recall that a
saturated packing is one in which no space exists to insert additional particles.) Disordered


                                                     42
hyperuniform point distributions are uncommon. Not only was this conjecture verified nu-
merically for an MRJ-like state using a million-particle packing of monodisperse spheres, but
it was shown that the structure factor has an unusual nonanalytic linear dependence near
the origin (Donev et al., 2005a), namely, S(k) ∼ |k| for k → 0, or equivalently, a quasi-long-
ranged tail of the total pair correlation function h(r) ∼ −r −4 . This same linear nonanalytic
behavior of S(k) near the origin is also found in such diverse three-dimensional systems
as the early Universe (Peebles, 1993), ground state of liquid helium (Feynman and Cohen,
1956; Reatto and Chester, 1967) and nonintercting spin-polaried fermionic ground states
(Scardicchio et al., 2009; Torquato et al., 2008). The generalization of the aforementioned
conjecture that describes when strictly jammed saturated packings of noncongruent sphere
packings as well as other particle shapes has been given by Zachary et al., 2010. Specif-
ically, the void spaces of general MRJ packings are highly constrained by the underlying
contact network, which induce hyperuniformity and quasi-long-range behavior of the two-
point probability function for the void phase.
   The quasi-long-range behavior of g2 (r) as well as the aforementioned pair-correlation
features distinguish the MRJ state strongly from that of the equilibrium hard-sphere fluid
(Hansen and McDonald, 1986), which is characterized by a structure factor that is analytic
at k = 0 and thus has a pair correlation function that decays exponentially fast to unity for
large r. Consequently, early attempts (Bernal, 1960) to use disordered jammed packings to
model liquid structure were imprecise.
   It should be recognized that MRJ-like sphere packings created in practice via computer
algorithms (Donev et al., 2005a; O’Hern et al., 2002; Torquato et al., 2000) or actual exper-
iments may contain a small concentration of rattlers, the average concentration of which is
protocol-dependent. The packings leading to the data depicted in Fig. 17 contain between
2-3 percent rattlers. Thus, the hyperuniformity property of the MRJ state requires that the
rattlers be retained in the packing.
   It is well known that lack of “frustration” (Jullien et al., 1997; Torquato, 2002) in two-
dimensional analogs of three-dimensional computational and experimental protocols that
lead to putative RCP states result in packings of identical disks that are highly crystalline,
forming rather large triangular coordination domains (grains). Such a 1000-particle packing
with φ ≈ 0.88 is depicted in the right panel of Fig. 8, and is only collectively jammed at
this high density. Because such highly ordered packings are the most probable outcomes

                                            43
for these typical protocols, “entropic measures” of disorder would identify these as the
most disordered, a misleading conclusion. An appropriate order metric, on the other hand,
is capable of identifying a particular configuration (not an ensemble of configurations) of
considerably lower density (e.g., a jammed vacancy-diluted triangular lattice or its multi-
domain variant) that is consistent with our intuitive notions of maximal disorder. However,
typical packing protocols would almost never generate such disordered disk configurations
because of their inherent implicit bias toward undiluted crystallization. Note that the same
problems persist even for polydisperse disk packings provided that the size distribution is
sufficiently narrow.
   Importantly, previously reported low packing fractions of 0.82 – 0.84 for so-called
RCP disk arrangements (Berryman, 1983) were found not even to be collectively jammed
(Donev et al., 2004c). This conclusion clearly demonstrates that the distinctions between
the different jamming categories are crucial. Moreover, the geometric-structure approach to
jamming reveals the basic importance of collective motions potentially involving an arbitrar-
ily large number of particles. Therefore, methods that assume collective jamming based only
on packing fraction and local criteria, such as nearest-neighbor coordination and Voronoi
statistics (Song et al., 2008), are incomplete.


IX. PACKINGS OF SPHERES WITH A SIZE DISTRIBUTION


   Polydispersity in the size of the particles constitutes a fundamental feature of the mi-
crostructure of a wide class of dispersions of technological importance, including those
involved in composite solid propellant combustion (Kerstein, 1987), sintering of powders
(Rahaman, 1995), colloids (Russel et al., 1989), transport and mechanical properties of par-
ticulate composite materials (Christensen, 1979), and flow in packed beds (Scheidegger,
1974).
   The spheres generally possess a distribution in radius R characterized by a probability
density f (R) that normalizes to unity, i.e.,
                                      Z ∞
                                           f (R)dR = 1.                                 (15)
                                        0

The average of any function w(R) is defined by
                                         Z ∞
                              hw(R)i =       w(R)f (R)dR.                               (16)
                                             0


                                             44
                       1.5                                                               4.0
                                   m=12                                                                             β=0.1

                                                                                         3.0
                       1.0   m=0




                                                                              f(R) <R>
            f(R) <R>                                                                     2.0

                             m=3
                       0.5
                                                                                         1.0                          β=0.2
                                                                                                  β=1.0


                       0.0                                                               0.0
                          0.0             1.0            2.0          3.0                   0.0               1.0             2.0   3.0
                                                R/<R>                                                                R/<R>


FIG. 18 Frequently used hard-sphere size distributions. Left panel: Schulz size distribution for
several values of m. Right panel: Log-normal size distribution for several values of β.


The overall packing fraction φ of the system is defined as

                                                                   φ = ρhv1 (R)i,                                                         (17)

where ρ is the total number density, v1 (R) is given by (2) and hv1 (R)i is the average sphere
volume defined by
                                                                          π d/2
                                                        hv1 (R)i =                hRd i.                                                  (18)
                                                                       Γ(1 + d/2)
   There is a variety of choices for the size distribution f (R) that deserve consideration.
Two continuous probability densities that have been widely used to characterize physical
phenomena are the Schulz (Schulz, 1939) and log-normal (Cramer, 1954) distributions. The
Schulz distribution is defined as
                                                                           m+1                          
                                                                                                          
                                           1                       m+1                         m−(m + 1)R
                                f (R) =                                                   R exp             .                             (19)
                                        Γ(m + 1)                   hRi                             hRi
where Γ(x) is the gamma function. When the parameter m is restricted to nonnegative
integer values, Γ(m + 1) = m!, and the nth moment of this distribution is given by
                                                               (m + n)! 1
                                                  hRn i =                    hRin .                                                       (20)
                                                                 m! (m + 1)n
By increasing m, the variance decreases, i.e., the distribution becomes sharper. In the
monodisperse limit m → ∞, f (R) → δ(R − hRi). The case m = 0 gives an exponential
distribution in which many particles have extremely small radii. By contrast, the log-normal
distribution is defined as
                                                                [ln(R/hRi)]2
                                                                            
                                                    1
                                           f (R) = p      exp −                ,                                                          (21)
                                                  R 2πβ 2            2β 2

                                                                       45
where β 2 = h(ln R)2 i − hln Ri2 . The quantity ln R has a normal or Gaussian distribution.
The nth moment is given by

                                 hRn i = exp(n2 β 2 /2) hRin .                           (22)

As β 2 → 0, f (R) → δ(R − hRi). Figure 18 shows examples of the Schulz and log-normal
size distributions.
   One can obtain corresponding results for spheres with M discrete different sizes from the
continuous case by letting
                                            M
                                            X ρi
                                  f (R) =             δ(R − Ri ),                        (23)
                                            i=1
                                                  ρ
where ρi and Ri are number density and radius of type-i particles, respectively, and ρ is the
total number density. Therefore, the overall volume fraction using (17) is given by
                                                  M
                                                  X
                                         φ=             φ(i)                             (24)
                                                  i=1

where
                                       φ(i) = ρi v1 (Ri )                                (25)

is the packing fraction of the ith component.
   Sphere packings with a size distribution exhibit intriguing structural features, some of
which are only beginning to be understood. It is known, for example, that a relatively small
degree of polydispersity can suppress the disorder-order phase transition seen in monodis-
perse hard-sphere systems (Henderson et al., 1996). Interestingly, equilibrium mixtures of
small and large hard spheres can “phase separate” (i.e., the small and large spheres demix) at
sufficiently high densities but the precise nature of such phase transitions has not yet been
established and is a subject of intense interest; see (Dijkstra et al., 1999) and references
therein.
   Our main interest here is in dense polydisperse packings of spheres, especially jammed
ones. Very little is rigorously known about the characteristics of such systems. For example,
the maximal overall packing fraction of even a binary mixture of hard spheres in Rd , which
               (2)
we denote by φmax , for arbitrary values of the mole fractions and radii R1 and R2 is unknown,
not to mention the determination of the corresponding structures. However, one can bound
 (2)                                                                   (1)
φmax from above and below in terms of the maximal packing fraction φmax for a monodisperse
sphere packing in the infinite-volume limit using the following analysis of (Torquato, 2002).

                                              46
                       (2)                                                               (1)
It is clear that φmax is bounded from below by the maximum packing fraction φmax . The
                 (2)         (1)
lower bound φmax ≥ φmax is independent of the radii and corresponds to the case when
the two components are completely phase separated (demixed), each at the packing fraction
 (1)                                   (2)                                                     (1)
φmax . Moreover, one can bound φmax from above in terms of the monodisperse value φmax
for arbitrary values of R1 and R2 . Specifically, consider a wide separation of sizes (R1 ≪ R2 )
and imagine a sequential process in which the larger spheres are first packed at the maximum
         (1)
density φmax for a monodisperse packing. The remaining interstitial space between the larger
                                                                                  (1)
spheres can now be packed with the smaller spheres at the packing fraction φmax provided
                                                                                   (1)
that R1 /R2 → 0. The overall packing fraction in this limit is given by 1 − (1 − φmax )2 , which
                                                  (2)                 √
is an upper bound for any binary packing. Thus, φmax ≤ 1 − (1 − π/ 12)2 ≈ 0.991 for d = 2
      (2)               √                                    (1)
and φmax ≤ 1 − (1 − π/ 18)2 ≈ 0.933 for d = 3, where φmax corresponds to the maximal
packing fraction in two or three dimensions, respectively.
   The same arguments extend to systems of M different hard spheres with radii
R1 , R2 , . . . , RM in Rd (Torquato, 2002). Specifically, the overall maximal packing fraction
 (M )
φmax of such a general mixture in Rd [where φ is defined by (17) with (23)] is bounded from
above and below by
                                   φ(1)    (M )            (1) M
                                    max ≤ φmax ≤ 1 − (1 − φmax ) .                             (26)

The lower bound corresponds to the case when the M components completely demix, each at
               (1)
the density φmax . The upper bound corresponds to the generalization of the aforementioned
ideal sequential packing process for arbitrary M in which we take the limits R1 /R2 → 0,
R2 /R3 → 0, · · · , RM −1 /RM → 0. Specific nonsequential protocols (algorithmic or other-
wise) that can generate structures that approach the upper bound (26) for arbitrary values
of M are currently unknown and thus the development of such protocols is an open area
of research. We see that in the limit M → ∞, the upper bound approaches unity, cor-
responding to space-filling polydisperse spheres with an infinitely wide separation in sizes
(Herrmann et al., 1990). Furthermore, one can also imagine constructing space-filling poly-
disperse spheres with a continuous size distribution with sizes ranging to the infinitesimally
small (Torquato, 2002).
   Jammed binary packings have received some attention but their characterization is far
from complete. Here we briefly note work concerned with maximally dense binary packings
as well as disordered jammed binary packings in two and three dimensions. Among these


                                                47
FIG. 19 One large disk and two small disks in mutual contact provide the densest local arrange-
ment of binary disks (Florian, 1960). The intersection of the shaded 
                                                                      triangle with the three disks
                                         2           2            α
                                       πα + 2(1 − α )arc sin
                                                                 1+α
yields the local packing fraction φU =                     1/2          , where α = RS /RL .
                                               2α(1 + 2α)


cases, we know most about the determination of the maximally dense binary packings in
R2 . Let RS and RL denote the radii of the small and large disks (RS ≤ RL ), the radii ratio
α = RS /RL and xS be the number fraction of small disks in the entire packing. Ideally, it is
desired to obtain φmax as a function of α and xS . In practice, we have a sketchy understanding
of the surface defined by φmax (α, xS ). Fejes Tóth, 1964 has reported a number of candidate
maximally dense packing arrangements for certain values of the radii ratio in the range
α ≥ 0.154701 . . .. Maximally dense binary disk packings have been also investigated to
determine the stable crystal phase diagram of such alloys (Likos and Henley, 1993). The
determination of φmax for sufficiently small α amounts to finding the optimal arrangement of
the small disks within a tricusp: the nonconvex cavity between three close-packed large disks.
A particle-growth Monte Carlo algorithm was used to generate the densest arrangements
of small identical disks (ranging in number from one through 19) within such a tricusp
(Uche et al., 2004). All of these results can be compared to a relatively sharp upper bound




                                               48
on φmax given by                                                      
                                          2         2             α
                                     πα + 2(1 − α )arc sin
                                                                 1+α
                       φmax ≤ φU =                                 .                   (27)
                                             2α(1 + 2α)1/2
The fraction φU corresponds to the densest local packing arrangement for three binary disks
shown in Fig. 19 and hence bounds φmax from above (Florian, 1960). Inequality (27) also
applies to general multicomponent packings, where α is taken to be the ratio of the smallest
disk radius to the largest disk radius.
   The most comprehensive study of the densest possible packings of binary spheres in
R3 as well as more general size-discrete mixtures has been reported in a recent paper by
Hudson and Harrowell, 2008. These authors generated candidate maximally dense polydis-
perse packings based on filling the interstices in uniform three-dimensional tilings of space
with spheres of different sizes. They were able to find for certain size ratios and compositions
a number of new packings. The reader is referred to Hudson and Harrowell, 2008 for details
and some history on the three-dimensional problem.
   One of the early numerical investigations of disordered jammed packings of binary disks in
R2 and binary spheres in R3 employed a “drop and roll” procedure (Visscher and Bolsterli,
1972). Such numerical protocols and others (Okubo and Odagaki, 2004), in which there
is a preferred direction in the system, tend to produce statistically anisotropic packings,
which exhibit lower densities than than those generated by packing protocols that yield sta-
tistically isotropic packings (Donev et al., 2004c). It is not clear that the former packings
are collectively jammed. In two dimensions, one must be especially careful in choosing a
sufficiently small size ratio in order to avoid the tendency of such packings to form highly
crystalline arrangements. The LS algorithm has been used successfully to generate disor-
dered strictly jammed packings of binary disks with φ ≈ 0.84 and α−1 = 1.4 (Donev et al.,
2006). By explicitly constructing an exponential number of jammed packings of binary disks
with densities spanning the spectrum from the accepted amorphous glassy state to the phase-
separated crystal, it has been argued (Donev et al., 2006, 2007b) that there is no “ideal glass
transition” (Parisi and Zamponi, 2005). The existence of an ideal glass transition remains
a hotly debated topic of research.
   In three dimensions, it was shown by Schaertl and Sillescu, 1994 that increasing poly-
dispersity increases the packing fraction over the monodisperse value that an amorphous
hard-sphere system can possess. The LS algorithm has been extended to generate jammed

                                              49
sphere packings with a polydispersity in size (Kansal et al., 2002a). It was applied to show
that disordered packings with a wide range of packing fractions that exceed 0.64 and varying
degrees of disorder can be achieved; see also Chaudhuri et al., 2010. Not surprisingly, the
determination of the maximally random jammed (MRJ) state for an arbitrary polydisperse
sphere packing is a wide open question. Clusel et al., 2009 have carried out a beautiful series
of experiments to understand polydisperse random packings of spheres. Specifically, they
produced three-dimensional random packings of frictionless emulsion droplets with a high
degree of size polydispersity, and visualize and characterize them using confocal microscopy.
   The aforementioned investigations and the many conundrums that remain serve to il-
lustrate the richness of polydisperse jammed packings but further discussion is beyond the
scope of this review.


X. PACKINGS OF NONSPHERICAL PARTICLES


   Jammed packing characteristics become considerably more complex by allowing for
nonspherical particle shapes (Betke and Henk, 2000; Chaikin et al., 2007; Chen, 2008;
Chen et al., 2010; Conway and Torquato, 2006; Donev et al., 2004a, 2007a, 2004b, 2005b,c;
Haji-Akbari et al., 2009; Jiao et al., 2010a; Kallus et al., 2010; Man et al., 2005; Roux, 2000;
Torquato and Jiao, 2009a,b, 2010b; Williams and Philipse, 2003). We focus here on the
latest developments in this category, specifically for particle shapes that are continuous
deformations of a sphere (ellipsoids and superballs) as well as polyhedra. Nonsphericity
introduces rotational degrees of freedom not present in sphere packings, and can dramati-
cally alter the jamming characteristics from those of sphere packings. [We note in passing
that there has been deep and productive examination of the equilibrium phase behavior and
transport properties of hard nonspherical particles (Allen, 1993; Frenkel and Maguire, 1983;
Frenkel et al., 1984; Yatsenko and Schweizer, 2008).]
   Very recent developments have provided organizing principles to characterize and classify
jammed packings of nonspherical particles in terms of shape symmetry of the particles
(Torquato and Jiao, 2009a). We will elaborate on these principles in Sec.X.C where we
discuss packings of polyhedra. We will begin the discussion by considering developments
within the last several years on ellipsoid packings, which has spurred much of the resurgent
interest in dense packings of nonspherical particles.


                                             50
   A. Ellipsoid Packings


   One simple generalization of the sphere is an ellipsoid, the family of which is a contin-
uous deformation of a sphere. A three-dimensional ellipsoid is a centrally symmetric body
occupying the region
                                 x 2        x 2          x 2
                                   1           2              3
                                         +              +            ≤ 1,                  (28)
                                  a            b              c
where xi (i = 1, 2, 3) are Cartesian coordinates and a, b and c are the semi-axes of the
ellipsoid. Thus, we see that an ellipsoid is an affine (linear) transformation of the sphere. A
spheroid is an ellipsoid in which two of the semi-axes are equal, say a = c, and is a prolate
(elongated) spheroid if b ≥ a and an oblate (flattened) spheroid if b ≤ a.
   Figure 20 shows how prolate and oblate spheroids are obtained from a sphere by a linear
stretch and shrinkage of the space along the axis of symmetry, respectively. This figure
also illustrates two other basic points by inscribing the particles within the smallest circular
cylinders. The fraction of space occupied by each of the particles within the cylinders is an
invariant equal (due to the affine transformations) to 2/3. This might lead one to believe that
the densest packing of ellipsoids is given by an affine transformation of one of the densest
sphere packings, but such transformations necessarily lead to ellipsoids that all have exactly
the same orientations. Exploiting the rotational degrees of freedom so that the ellipsoids are
not all required to have the same orientations turns out to lead to larger packing fractions
than that for maximally dense sphere packings. Furthermore, because the fraction of space
remains the same in each example shown in Figure 20, the sometimes popular notion that
going to the extreme “needle-like” limit (b/a → ∞) or extreme “disk-like’ limit (b/a → 0)
can lead to packing fractions φ approaching unity is misguided.
   Experiments on M&M candies (spheroidal particles) (Donev et al., 2004a; Man et al.,
2005) as well as numerical results produced by a modified LS algorithm (Donev et al.,
2005b,c) found MRJ-like packings with packing fractions and mean contact numbers that
were higher than for spheres. This led to a numerical study of the packing fraction φ and
mean contact number Z as a function of the semi-axes (aspect) ratios.
   The results were quite dramatic in several respects. First, it was shown that φ and Z, as
a function of aspect ratio, each have a cusp (i.e., non-differentiable) minimum at the sphere
point, and φ versus aspect ratio possesses a density maximum; see Fig. 21, which shows the
more refined calculations presented in (Donev et al., 2007a). The existence of a cusp at the

                                                   51
FIG. 20 A sphere inscribed within the smallest circular cylinder (i) undergoes a linear stretch and
shrinkage of the space along the vertical direction leading to a prolate spheroid (ii) and an oblate
spheroid (iii), respectively. This linear transformation leaves the fraction of space occupied by the
spheroids within the cylinders unchanged from that of the fraction of the cylinder volume occupied
by the sphere, equal to 2/3.




                   0.74



                   0.72




                    0.7

                                      1         2              3
                               12
                   0.68
                               10
                                                                          (oblate)
                              Z
                   0.66           8

                                                                          (prolate)
                                  6
                   0.64
                          1               1.5            2          2.5               3
                                                Aspect ratio
FIG. 21 Density φ versus aspect ratio α for MRJ packings of 10,000 ellipsoids as obtained in
(Donev et al., 2007a). The semi-axes here are 1, αβ , α. The inset shows the mean contact number
Z as a function of α. Neither the spheroid (oblate or prolate) or general ellipsoids cases attain
their isostatic values of Z = 10 or Z = 12, respectively.



                                                    52
sphere point runs counter to the prevailing expectation in the literature that for “generic”
(disordered) jammed frictionless particles the total number of (independent) constraints
equals the total number of degrees of freedom df , implying a mean contact number Z = 2df
(df = 2 for disks, df = 3 for ellipses, df = 3 for spheres, df = 5 for spheroids, and df = 6 for
general ellipsoids). This has been referred to as the isostatic conjecture (Alexander, 1998)
or isocounting conjecture (Donev et al., 2007a). Since df increases discontinuously with the
introduction of rotational degrees of freedom as one makes the particles nonspherical, the
isostatic conjecture predicts that Z should have a jump increase at aspect ratio α = 1
to a value of Z = 12 for a general ellipsoid. Such a discontinuity was not observed by
Donev et al., 2004a, rather, it was observed that jammed ellipsoid packings are hypostatic,
Z < 2df , near the sphere point, and only become nearly isostatic for large aspect ratios.
In fact, the isostatic conjecture is only rigorously true for amorphous sphere packings after
removal of rattlers; generic nonspherical-particle packings should generally be hypostatic (or
sub-isostatic) (Donev et al., 2007a; Roux, 2000).
   Until recently, it was accepted that a sub-isostatic or hypostatic packing of nonspherical
particles cannot be rigid (jammed) due to the existence of “floppy” modes (Alexander, 1998),
which are unjamming motions (mechanisms) derived within a linear theory of rigidity, i.e.,
a first-order analysis in the jamming gap δ (see Sec. IV.C). The observation that terms
of order higher than first generally need to be considered was emphasized by Roux, 2000,
but this analysis was only developed for spheres. It has recently been rigorously shown that
if the curvature of nonspherical particles at their contact points are included in a second-
order and higher-order analysis, then hypostatic packings of such particles can indeed be
jammed (Donev et al., 2007a). For example, ellipsoid packings are generally not jammed to
first order in δ but are jammed to second order in δ (Donev et al., 2007a) due to curvature
deviations from the sphere.
   To illustrate how nonspherical jammed packings can be hypostatic, Fig. 22 depicts two
simple two-dimensional examples consisting of a few fixed ellipses and a central particle
that is translationally and rotationally trapped by the fixed particles. Generically, four con-
tacting particles are required to trap the central one. However, there are special correlated
configurations that only require three contacting particles to trap the central one. In such
instances, the normal vectors at the points of contact intersect at a common point, as is
necessary to achieve torque balance. At first glance, such configurations might be dismissed

                                             53
as probability-zero events. However, it was shown that such nongeneric configurations are
degenerate (frequently encountered). This “focusing capacity” toward hypostatic values of
Z applies to large jammed packings of nonspherical particles and in the case of ellipsoids
must be present for sufficiently small aspect ratios for a variety of realistic packing protocols
(Donev et al., 2007a). It has been suggested that the degree of nongenericity of the pack-
ings be quantified by determining the fraction of local coordination configurations in which
the central particles have fewer contacting neighbors than the average value Z (Jiao et al.,
2010a).




FIG. 22 Simple examples of hypoconstrained packings in which all particles are fixed, except the
central one. Left panel: Generically, four contacting particles are required to trap the central
one. Right panel: Special correlated configurations only require three contacting particles to trap
the central one. The normal vectors at the points of contact intersect at a common point, as is
necessary to achieve torque balance.


   Having established that curvature deviations from the spherical reference shape exert a
fundamental influence on constraint counting (Donev et al., 2007a), it is clear that similar
effects will emerge when the hard-particle interactions are replaced by nonspherical particles
interacting with soft short-range repulsive potentials. It immediately follows that jamming
to first and second order in δ for hard nonspherical particles, for example, leads to quadratic
and quartic modes in the vibrational energy spectrum for packings of such particles that
interact with purely soft repulsive interactions. The reader is referred to Mailman et al., 2009
and Zeravcic et al., 2009 for studies of the latter type for ellipses and ellipsoids, respectively.


                                               54
   It is noteworthy that in striking contrast with MRJ-like sphere packings, the rattler
concentrations of the MRJ-like ellipsoid packings appear practically to vanish outside of some
small neighborhood of the sphere point (Donev et al., 2007a). It was shown that MRJ-like
packings of nearly-spherical ellipsoids can be obtained with φ ≈ 0.74, i.e., packing fractions
approaching those of the densest three-dimensional sphere packings (Donev et al., 2004a).
This suggested that there exist ordered ellipsoid packings with appreciably higher densities.
Indeed, the densest known ellipsoid packings were subsequently discovered (Donev et al.,
2004b); see Fig. 23. These represent a new family of non-Bravais lattice packings of ellipsoids
with a packing fraction that always exceeds the density of the densest Bravais lattice packing
(φ = 0.74048 . . .) with a maximal packing fraction of φ = 0.7707 . . ., for a wide range of
                       √          √
aspect ratios (α ≤ 1/ 3 and α ≥ 3). In these densest known packings, each ellipsoid has
14 contacting neighbors and there are two particles per fundamental cell.
   For identical ellipse packings in R2 , the maximally dense arrangement is obtained by
an affine stretching of the optimal triangular-lattice packing of circular disks with φmax =
  √
π/ 12, which leaves φmax unchanged (Donev et al., 2004b; Fejes Tóth, 1964); see Fig. 24.
This maximally dense ellipse packing is not rotationally jammed for any noncircular shape,
since it can be sheared continuously without introducing overlap or changing the density
(Donev et al., 2007a). The packing is, however, strictly translationally jammed.


   B. Superball Packings


   Virtually all systematic investigations of the densest particle packings have been carried
out for convex objects. A d-dimensional superball is a centrally symmetric body in d-
dimensional Euclidean space occupying the region

                              |x1 |2p + |x2 |2p + · · · + |xd |2p ≤ 1,                     (29)

where xi (i = 1, . . . , d) are Cartesian coordinates and p ≥ 0 is the deformation parameter
(not pressure as denoted in Sec. IV.C), which controls the extent to which the particle shape
has deformed from that of a d-dimensional sphere (p = 1). Thus, superballs constitute a
large family of both convex (p ≥ 0.5) and concave (0 ≤ p < 0.5) particles (see Fig. 26).
   In general, a “superdisk,” the designation in the two-dimensional case, possesses square
symmetry. As p moves away from unity, two families of superdisks with square symmetry

                                               55
FIG. 23 The packing fraction of the “laminated” non-Bravais lattice packing of ellipsoids (with a
two-particle basis) as a function of the aspect ratio α. The point α = 1 corresponding to the face-
centered cubic lattice sphere packing is shown, along with the two sharp maxima in the packing
                                          √                                  √
fraction for prolate ellipsoids with α = 3 and oblate ellipsoids with α = 1/ 3, as illustrated
                                 √           √
in the insets. For both α < 1/ 3 and α > 3, the packing fractions of the laminated packings
drop off precipitously holding the particle orientations fixed (blue lines). The presently maximal
achievable packing fraction φ = 0.7707 . . . is highlighted with a thicker red line, and is constant for
       √            √
α ≤ 1/ 3 and α ≥ 3 because there is an affine stretch by an arbitrary factor along a direction
in a mirror plane of the particle directions; see Donev et al., 2004b.


can be obtained depending on whether p < 1 or p > 1 such that there is a 45-degree
rotation with respect to the “protuberances.” When p < 0.5, the superdisk is concave (see
Fig. 25). The candidate maximally dense packings were recently proposed for all convex
and concave shapes (Jiao et al., 2008). These are achieved by two different families of
Bravais lattice packings such that φmax is nonanalytic at the “circular-disk” point (p = 1)
and increases significantly as p moves away from unity. The broken rotational symmetry
of superdisks influences the packing characteristics in a non-trivial way that is distinctly
different from ellipse packings. Recall that for ellipse packings, no improvement over the
maximal circle packing density is possible. For superdisks, one can take advantage of the
four-fold rotationally symmetric shape of the particle to obtain a substantial improvement


                                                 56
FIG. 24 A portion of the densest packing of congruent ellipses, which is simply an affine transfor-
mation of the densest circle packing, i.e., the densest triangular lattice of circles. This maximally
dense ellipse packing is not rotationally jammed for any noncircular shape, but is strictly transla-
tionally jammed.




FIG. 25 (color online) Superdisks with different values of the deformation parameter p.


on the maximal circle packing density. By contrast, one needs to use higher-dimensional
counterparts of ellipses (d ≥ 3) in order to improve on φmax for spheres. Even for three-
dimensional ellipsoids, φmax increases smoothly as the aspect ratios of the semi-axes vary
from unity (Donev et al., 2004b), and hence has no cusp at the sphere point. In fact,
congruent three-dimensional ellipsoid packings have a cusp-like behavior at the sphere point
only when they are randomly jammed (Donev et al., 2004a).
   Increasing the dimensionality of the particle imbues the optimal “superball” packings with
structural characteristics that are richer than their two-dimensional counterparts (Jiao et al.,
2009). For example, in three dimensions, a superball is a perfect sphere at p = 1, but can
possess two types of shape anisotropy: cube-like shapes (three-dimensional analog of the
square symmetry of the superdisk) and octahedron-like shapes, depending on the value of


                                               57
FIG. 26 (color online). Superballs with different values of the deformation parameter p.




            (a)                       (b)                       (c)                        (d)


FIG. 27 (color online). Candidate optimal packings of superballs: (a) The C0 -lattice packing of
superballs with p = 1.8. (b) The C1 -lattice packing of superballs with p = 2.0. (c) The O0 -lattice
packing of superballs with p = 0.8. (d) The O1 -lattice packing of superballs with p = 0.55.


the deformation parameter p (see Fig. 26). As p continuously increases from 1 to ∞, we have
a family of convex superballs with cube-like shapes; at the limit p = ∞, the superball is a
perfect cube. As p decreases from 1 to 0.5, a family of convex superballs with octahedron-
like shapes are obtained; at p = 0.5, the superball becomes a regular octahedron. When
p < 0.5, the superball still possesses an octahedron-like shape but is now concave, becoming
a three-dimensional “cross” in the limit p → 0. Note that the cube and regular octahedron
(two of the five Platonic polyhedra) have the same group symmetry (i.e., they have the same
48 space group elements) because they are dual to each other. Two polyhedra are dual to
each other if the vertices of one correspond to the faces of the other.
   Jiao et al., 2009 have obtained analytical constructions for the densest known super-
ball packings for all convex and concave cases. The candidate maximally dense packings
are certain families of Bravais lattice packings (in which each particle has 12 contacting
neighbors) possessing the global symmetries that are consistent with the symmetries of a


                                               58
superball. Evidence is provided that these packings are indeed optimal, and Torquato and
Jiao (Torquato and Jiao, 2009b) have conjectured that the densest packings of all convex
superballs are their densest lattice packings; see Fig. 27. For superballs in the cubic regime
(p > 1), the candidate optimal packings are achieved by two families of Bravais lattice
packings (C0 and C1 lattices) possessing two-fold and three-fold rotational symmetry, re-
spectively, which can both be considered to be continuous deformations of the fcc lattice.
For superballs in the octahedral regime (0.5 < p < 1), there are also two families of Bra-
vais lattices (O0 and O1 lattices) obtainable from continuous deformations of the fcc lattice
keeping its four-fold rotational symmetry, and from the densest lattice packing for regular
octahedra (Betke and Henk, 2000; Minkowski, 1905), keeping the translational symmetry of
the projected lattice on the coordinate planes, which are apparently optimal in the vicinity
of the sphere point and the octahedron point, respectively (see Fig. 27).
   The proposed maximal packing density φmax as a function of deformation parameter p is
plotted in Fig. 28. As p increases from unity, the initial increase of φmax is linear in (p − 1)
and subsequently φmax increases monotonically with p until it reaches unity as the particle
shape becomes more like a cube, which is more efficient at filling space than a sphere. These
characteristics stand in contrast to those of the densest known ellipsoid packings, achieved by
certain crystal arrangements of congruent spheroids with a two-particle basis, whose packing
density as a function of aspect ratios has zero initial slope and is bounded from above by a
value of 0.7707 . . . (Donev et al., 2004b). As p decreases from unity, the initial increase of
φmax is linear in (1−p). Thus, φmax is a nonanalytic function of p at p = 1, which is consistent
with conclusions made about superdisk packings (Jiao et al., 2008). However, the behavior
of φmax as the superball shape moves off the sphere point is distinctly different from that
of optimal spheroid packings, for which φmax increases smoothly as the aspect ratios of the
semi-axes vary from unity and hence has no cusp at the sphere point (Donev et al., 2004b).
The density of congruent ellipsoid packings (not φmax ) has a cusp-like behavior at the sphere
point only when the packings are randomly jammed (Donev et al., 2004a). The distinction
between the two systems results from different broken rotational symmetries. For spheroids,
the continuous rotational symmetry is only partially broken, i.e., spheroids still possess one
rotationally symmetric axis; and the three coordinate directions are not equivalent, which
facilitates dense non-Bravais packings. For superballs, the continuous rotational symmetry
of a sphere is completely broken and the three coordinate directions are equivalently four-fold

                                             59
                            1
                                  0.76

                         0.95
                                0.7595
                          0.9                1.15         1.1525


                       φ 0.85                                                     O1-Lattice Packing
                                                                                  O0-Lattice Packing
                                                                                  C0 Lattice-Packing
                          0.8
                                                                                  C1-Lattice Packing

                         0.75


                            0.5          1          1.5      2      2.5       3      3.5    4    4.5   5
                                                                          p

FIG. 28 (color online). Density versus deformation parameter p for the packings of convex super-
balls (Jiao et al., 2009). Insert: Around p∗c = 1.1509 . . ., the two curves are almost locally parallel
to each other.

rotationally symmetric directions of the particle. Thus, a superball is less symmetric but
more isotropic than an ellipsoid, a shape characteristic which apparently favors dense Bravais
lattice packings. The broken symmetry of superballs makes their shapes more efficient in
tiling space and thus results in a larger and faster increase in the packing density as the
shape moves away from the sphere point.
   As p decreases from 0.5, the superballs become concave particles, but they still possess
octahedron-like shapes [see Fig. 26(a)]. The lack of simulation techniques to generate concave
superball packings makes it very difficult to find the optimal packings for the entire range
of concave shapes (0 < p < 0.5). However, based on their conclusions for convex superball
packings, Jiao et al., 2009 conjectured that near the octahedron point, the optimal packings
possess similar translational symmetry to that of the O1 -lattice packing, and based on
theoretical considerations proposed candidate optimal packings for all concave cases with a
density versus p as shown in Fig.29.
   Jiao et al., 2010a have determined the packing fractions of maximally random jammed
(MRJ) packings of binary superdisks in R2 and monodispersed superballs in R3 . They found
that the MRJ densities of such packings increase dramatically and nonanalytically as one
moves away from the circular-disk and sphere point (p = 1). Moreover, these disordered
packings were demonstrated to be hypostatic, i.e., the average number of contacting neigh-
bors is less than twice the total number of degrees of freedom per particle, and the packings

                                                                   60
FIG. 29 (color online). Density versus deformation parameter p for the lattice packings of concave
superballs (Jiao et al., 2009). Insert: a concave superball with p = 0.1, which will becomes a
three-dimensional cross at the limit p → 0.


are mechanically stable. As a result, the local arrangements of the particles are necessarily
nontrivially correlated to achieve jamming and hence “nongeneric.” The degree of “non-
genericity” of the packings was quantitatively characterized by determining the fraction of
local coordination structures in which the central particles have fewer contacting neighbors
than the average value Z. Figure 30 depicts local packing structures with more contacts
than average and those with less contacts than average in MRJ binary superdisk packings
for different p values. It was also explicitly shown that such seemingly “special” packing
configurations are counterintuitively not rare. As the anisotropy of the particles increases,
it was shown that the fraction of rattlers decreases while the minimal orientational order
(as measured by the cubatic order metric) increases. These novel characteristics result from
the unique rotational symmetry breaking manner of superdisk and superball particles.


   C. Polyhedron Packings


   Until some recent developments, very little was known about the densest packings of
polyhedral particles. The difficulty in obtaining dense packings of polyhedra is related to
their complex rotational degrees of freedom and to the non-smooth nature of their shapes.
   The Platonic solids (mentioned in Plato’s Timaeus) are convex polyhedra with faces
composed of congruent convex regular polygons. There are exactly five such solids: the

                                              61
FIG. 30 (color online). Local packing structures with more contacts than average (shown in blue)
and those with less contacts than average (shown in pink) in two-dimensional MRJ superdisk
packings for different values of the deformation parameter p, as obtained from Jiao et al., 2010a.
Note that the degree of nongenericity decreases as p moves away from its sphere-point value. Here
the size ratio (diameter of large superdisks divided by the diameter of the small superdisks) is 1.4
and the molar ratio (number of large superdisks divided by the number of small superdisks) is 1/3.




FIG. 31 (color online). The five Platonic solids: tetrahedron (P1), icosahedron (P2), dodecahedron
(P3), octahedron (P4), and cube (P5).


tetrahedron (P1), icosahedron (P2), dodecahedron (P3), octahedron (P4), and cube (P5)
(see Fig. 31) [We note in passing that viral capsids often have icosahedral symmetry; see,
for example, Zandi et al., 2004.] Here we focus on the problem of the determination of the


                                               62
densest packings of each of the Platonic solids in three-dimensional Euclidean space R3 ,
except for the cube, which is the only Platonic solid that tiles space.
   It is useful to highlight some basic geometrical properties of the Platonic solids that we
will employ in subsequent sections of this review. The dihedral angle θ is the interior angle
between any two face planes and is given by

                                            θ   cos(π/q)
                                      sin     =          ,                                 (30)
                                            2   sin(π/p)

where p is the number of sides of each face and q is the number of faces meeting at
                                                   √               √               √
each vertex (Coxeter, 1973). Thus, θ is 2 sin−1 (1/ 3), 2 sin−1 (Φ/ 3), 2 sin−1 (Φ/ Φ2 + 1),
         p
2 sin−1 ( 2/3), and π/2, for the tetrahedron, icosahedron, dodecahedron, octahedron, and
                                    √
cube, respectively, where Φ = (1 + 5)/2 is the golden ratio. Since the dihedral angle for
the cube is the only one that is a submultiple of 2π, the cube is the only Platonic solid that
tiles space. It is noteworthy that in addition to the regular tessellation of R3 by cubes in the
simple cubic lattice arrangement, there is an infinite number of other irregular tessellations
of space by cubes. This tiling-degeneracy example vividly illustrates a fundamental point
made by Kansal et al., 2002b, namely, packing arrangements of nonoverlapping objects at
some fixed density can exhibit a large variation in their degree of structural order. We note
in passing that there are two regular dodecahedra that independently tile three-dimensional
(negatively curved) hyperbolic space H3 , as well as one cube and one regular icosahedron
(Coxeter, 1973); see Sec. XII for additional remarks about packings in curved spaces.
   Every polyhedron has a dual polyhedron with faces and vertices interchanged. The dual
of each Platonic solid is another Platonic solid, and therefore they can be arranged into dual
pairs: the tetrahedron is self-dual (i.e., its dual is another tetrahedron), the icosahedron and
dodecahedron form a dual pair, and the octahedron and cube form a dual pair.
   An Archimedean solid is a highly symmetric, semi-regular convex polyhedron composed
of two or more types of regular polygons meeting in identical vertices. There are thirteen
Archimedean solids: truncated tetrahedron (A1), truncated icosahedron (A2), snub cube
(A3), snub dodecahedron (A4), rhombicosidodecahdron (A5), truncated icosidodecahdron
(A6), truncated cuboctahedron (A7), icosidodecahedron (A8), rhombicuboctahedron (A9),
truncated dodecahedron (A10), cuboctahedron (A11), truncated cube (A12) and truncated
octahedron (A13) (see Fig. 32). Note that the truncated octahedron is the only Archimedean
solid that tiles R3 . The duals of the Archimedean solids are an interesting set of new

                                              63
FIG. 32 (color online) The 13 Archimedean solids: truncated tetrahedron (A1), truncated icosa-
hedron (A2), snub cube (A3), snub dodecahedron (A4), rhombicosidodecahdron (A5), truncated
icosidodecahedron (A6), truncated cuboctahedron (A7), icosidodecahedron (A8), rhombicubocta-
hedron (A9), truncated dodecahedron (A10), cuboctahedron (A11), truncated cube (A12), and
truncated octahedron (A13). This typical enumeration of the Archimedean solids does not count
the chiral forms (not shown) of the snub cube (A3) and snub dodecahedron (A4), which implies
that the left-handed and right-handed forms of each of these pairs lack central symmetry. The re-
maining 11 Archimedean solids are non-chiral (i.e., each solid is superposable on its mirror image)
and the only non-centrally symmetric one among these is the truncated tetrahedron.


polyhedra that are called the Archimedean duals or the Catalan polyhedra, the faces of
which are not regular polygons.
   Another important observation is that the tetrahedron (P1) and the truncated tetrahe-
dron (A1) are the only Platonic and non-chiral Archimedean solids, respectively, that are
not centrally symmetric. The chiral snub cube and chiral snub dodecahedron are the only
other non-centrally symmetric Archimedean solids. A particle is centrally symmetric if it


                                               64
has a center C that bisects every chord through C connecting any two boundary points of
the particle, i.e., the center is a point of inversion symmetry. We will see that the central
symmetry of the majority of the Platonic and Archimedean solids (P2 – P5, A2 – A13) dis-
tinguish their dense packing arrangements from those of the non-centrally symmetric ones
(P1 and A1) in a fundamental way.
   Tetrahedral    tilings   of   space   underlie   many     different   molecular    systems
(Conway and Torquato, 2006).      Since regular tetrahedra cannot tile space, it is of in-
terest to determine the highest density that such packings of particles can achieve (one
of Hilbert’s 18th problem set). It is of interest to note that the densest Bravais-lattice
packing of tetrahedra (which requires all of the tetrahedra to have the same orienta-
tions) has φ = 18/49 = 0.367 . . . and each tetrahedron touches 14 others.           Recently,
Conway and Torquato, 2006 showed that the maximally dense tetrahedron packing cannot
be a Bravais lattice (because dense tetrahedron packings favor face to face contacts) and
found non-Bravais lattice (periodic) packings of regular tetrahedra with φ ≈ 0.72. One such
packing is based upon the filling of “imaginary” icosahedra with the densest arrangement of
20 tetrahedra and then arranging the imaginary icosahedra in their densest lattice packing
configuration.   Using “tetrahedral” dice, Chaikin et al., 2007 experimentally generated
jammed disordered packings of such dice with φ ≈ 0.75; see also Jaoshvili et al., 2010 for a
refined version of this work. However, because these dice are not perfect tetrahedra (vertices
and edges are slightly rounded), a definitive conclusion could not be reached. Using physical
models and computer algebra system, Chen, 2008 discovered a dense periodic arrangement
of tetrahedra with φ = 0.7786 . . ., which exceeds the density of the densest sphere packing
by an appreciable amount.
   In an attempt to find even denser packings of tetrahedra, Torquato and Jiao, 2009a,b
have formulated the problem of generating dense packings of polyhedra within an adaptive
fundamental cell subject to periodic boundary conditions as an optimization problem, which
they call the Adaptive Shrinking Cell (ASC) scheme. Starting from a variety of initial
unjammed configurations, this optimization procedure uses both a sequential search of the
configurational space of the particles and the space of lattices via an adaptive fundamental
cell that shrinks on average to obtain dense packings. This was used to obtain a tetrahedron
packing consisting of 72 particles per fundamental cell with packing fraction φ = 0.782 . . .
(Torquato and Jiao, 2009a). Using 314 particles per fundamental cell and starting from an

                                            65
“equilibrated” low-density liquid configuration, the same authors were able to improve the
packing fraction to φ = 0.823 . . . (Torquato and Jiao, 2009b). This packing arrangement
interestingly lacks any long-range order. Haji-Akbari et al., 2009 numerically constructed
a periodic packing of tetrahedra made of parallel stacks of “rings” around “pentagonal”
dipyramids consisting of 82 particles per fundamental cell and a density φ = 0.8503 . . ..
   Kallus et al., 2010 found a remarkably simple “uniform” packing of tetrahedra with high
symmetry consisting of only four particles per fundamental cell (two “dimers”) with packing
             100
fraction φ = 117 = 0.854700 . . .. A uniform packing has a symmetry (in this case a point
inversion symmetry) that takes one tetrahedron to another. A dimer is composed of a
pair of regular tetrahedra that exactly share a common face. Torquato and Jiao, 2010a
subsequently presented an analytical formulation to construct a three-parameter family of
dense uniform dimer packings of tetrahedra again with four particles per fundamental cell.
(A uniform dimer packing of tetrahedra has a point of inversion symmetry operation that
takes any dimer into another.) Making an assumption about one of these parameters resulted
                                                                                  12250
in a two-parameter family, including those with a packing fraction as high as φ = 14319 =
0.855506 . . . (see left panel of Fig. 33). Chen et al., 2010 recognized that such an assumption
was made in the formulation of Torquato and Jiao, 2010a and employed a similar formalism
to obtain a three-parameter family of tetrahedron packings, including the densest known
dimer packings of tetrahedra with the very slightly higher packing fraction φ = 4000
                                                                                4671
                                                                                     =
0.856347 . . . (see right panel of Fig. 33). The most general analytical formulation to date
to construct dense periodic packings of tetrahedra with four particles per fundamental cell
was carried out by Torquato and Jiao, 2010b. This study involved a six-parameter family of
dense tetrahedron packings that includes as special cases all of the aforementioned “dimer”
packings of tetrahedra, including the densest known packings with packing fraction φ =
4000
4671
       = 0.856347 . . .. This most recent investigation strongly suggests that the latter set
of packings are the densest among all packings with a four-particle basis. Whether these
packings are the densest packings of tetrahedra among all packings is an open question for
reasons given by Torquato and Jiao, 2010b.
   Using the ASC scheme and a variety of initial conditions with multiple particles in the
fundamental cell, (Torquato and Jiao, 2009a,b) were also able to find the densest known
packings of the octahedra, dodecahedra and icosahedra (three non-tiling Platonic solids)
with densities 0.947 . . ., 0.904 . . ., and 0.836 . . ., respectively. Unlike the densest tetrahedron

                                                66
FIG. 33 (color online) Closely related dense tetrahedron packings. Left panel: A portion of one member of
the densest two-parameter family of tetrahedron packings with 4 particles per fundamental cell and packing
             12250
fraction φ = 14319 = 0.855506 . . . (Torquato and Jiao, 2010a). The blue particles (lighter shade) represent

two dimers (i.e., 4 tetrahedra) but from this perspective each dimer appears to be a single tetrahedron.

Right panel: A portion of one member of the densest three-parameter family of tetrahedron packings

with 4 particles per fundamental cell and packing fraction φ = 4000
                                                               4671 = 0.856347 . . . (Chen et al., 2010;

Torquato and Jiao, 2010b). The green particles (lighter shade) represent two dimers. It is clear that these

two packings are configurationally almost identical to one another.


packing, which must be a non-Bravais lattice packing, the densest packings of the other non-
tiling Platonic solids found by the algorithm are their previously known optimal (Bravais)
lattice packings (Betke and Henk, 2000; Minkowski, 1905); see Fig. 34. These simulation
results as well as other theoretical considerations, which we briefly describe immediately
below, led them to general organizing principles concerning the densest packings of a class
of nonspherical particles.
   Rigorous upper bounds on the maximal packing fraction φmax of packings of nonspherical
particles of general shape can be used to assess the packing efficiency of a particular dense
packing of such particles. However, it has been highly challenging to formulate upper bounds
for non-tiling particle packings that are nontrivially less than unity. It has recently been
shown that φmax of a packing of congruent nonspherical particles of volume vP in R3 is




                                                   67
FIG. 34 (color online) Portions of the densest lattice packings of three of the centrally symmetric
Platonic solids found by the ASC scheme (Torquato and Jiao, 2009a,b). Left panel: Icosahedron
packing with packing fraction φ = 0.8363 . . .. Middle panel: Dodecahedron packing with packing
fraction φ = 0.9045 . . .. Right panel: Octahedron packing with packing fraction φ = 0.9473 . . ..


bounded from above according to
                                                               
                                                         vP π
                               φmax ≤ φUmax = min           √ ,1 ,                              (31)
                                                         vS 18
where vS is the volume of the largest sphere that can be inscribed in the nonspherical
               √
particle and π/ 18 is the maximal sphere-packing density (Torquato and Jiao, 2009a,b).
The upper bound (31) will be relatively tight for packings of nonspherical particles provided
that the asphericity γ (equal to the ratio of the circumradius to the inradius) of the particle
is not large. Since bound (31) cannot generally be sharp (i.e., exact) for a non-tiling,
nonspherical particle, any packing whose density is close to the upper bound (31) is nearly
optimal, if not optimal. It is noteworthy that a majority of the centrally symmetric Platonic
and Archimedean solids have relatively small asphericities and explain the corresponding
small differences between φUmax and the packing fraction of the densest lattice packing φLmax
(Betke and Henk, 2000; Minkowski, 1905).
   Torquato and Jiao, 2009a,b have demonstrated that substantial face-to-face contacts be-
tween any of the centrally symmetric Platonic and Archimedean solids allow for a higher
packing fraction. They also showed that central symmetry enables maximal face-to-face
contacts when particles are aligned, which is consistent with the densest packing being the
optimal lattice packing.
   The aforementioned simulation results, upper bound, and theoretical considerations led
to the following three conjectures concerning the densest packings of polyhedra and other
nonspherical particles in R3 (Torquato and Jiao, 2009a,b, 2010b):
Conjecture 1: The densest packings of the centrally symmetric Platonic and Archimedean

                                                68
solids are given by their corresponding optimal lattice packings.
Conjecture 2: The densest packing of any convex, congruent polyhedron without central
symmetry generally is not a (Bravais) lattice packing, i.e., set of such polyhedra whose
optimal packing is not a lattice is overwhelmingly larger than the set whose optimal packing
is a lattice.
Conjecture 3: The densest packings of congruent, centrally symmetric particles that do
not possesses three equivalent principle axes (e.g., ellipsoids) generally cannot be Bravais
lattices.
   Conjecture 1 is the analog of Kepler’s sphere conjecture for the centrally symmetric
Platonic and Archimedean solids. Note that the densest known packing of the non-centrally
symmetric truncated tetrahedron is a non-lattice packing with density at least as high as
23/24 = 0.958333 . . . (Conway and Torquato, 2006). The arguments leading to Conjecture 1
also strongly suggest that the densest packings of superballs are given by their corresponding
optimal lattice packings (Torquato and Jiao, 2009b), which were proposed by Jiao et al.,
2009.


   D. Additional Remarks


   It is noteworthy that the densest known packings of all of the Platonic and Archimedean
solids as well as the densest known packings of superballs (Jiao et al., 2009) and ellipsoids
(Donev et al., 2004b) in R3 have packing fractions that exceed the optimal sphere packing
                 √
value φSmax = π/ 18 = 0.7408 . . .. These results are consistent with a conjecture of Ulam
who proposed without any justification [in a private communication to Martin Gardner
(Gardner, 2001)] that the optimal packing fraction for congruent sphere packings is smaller
than that for any other convex body. The sphere is perfectly isotropic with an asphericity γ
of unity, and therefore its rotational degrees of freedom are irrelevant in affecting its packing
characteristics. On the other hand, each of the aforementioned convex nonspherical particles
break the continuous rotational symmetry of the sphere and thus its broken symmetry can be
exploited to yield the densest possible packings, which might be expected to exceed φSmax =
  √
π/ 18 = 0.7408 . . . (Torquato and Jiao, 2009a). However, broken rotational symmetry in
and of itself may not be sufficient to satisfy Ulam’s conjecture if the convex particle has a
little or no symmetry (Torquato and Jiao, 2009a).

                                              69
   Apparently, the two-dimensional analog of Ulam’s conjecture (optimal density of congru-
                              √
ent circle packings (φmax = π/ 12 = 0.906899 . . .) is smaller than that for any other convex
two-dimensional body) is false. The “smoothed” octagon constructed by (Reinhardt, 1934)
                                                                     √          √
is conjectured to have smallest optimal packing fraction (φmax = (8−4 2−ln 2)/(2 2−1) =
0.902414 . . .) among all congruent centrally-symmetric planar particles.
   It will also be interesting to determine whether Conjecture 1 can be extended to other
polyhedral packings. The infinite families of prisms and antiprisms provide such a class
of packings. A prism is a polyhedron having bases that are parallel, congruent polygons
and sides that are parallelograms. An antiprism is a polyhedron having bases that are
parallel, congruent polygons and sides that are alternating bands of triangles. They are
generally much less symmetric than either the Platonic or Archimedean solids. Moreover,
even the centrally symmetric prisms and antiprisms generally do not possess three equivalent
directions. Thus, it is less obvious whether Bravais lattices would still provide the optimal
packings for these solids, except for prisms that tile space, e.g., hexagonal prism or rhombical
prisms (Torquato and Jiao, 2009b). Torquato and Jiao, 2009b have also commented on the
validity of Conjecture 1 to polytopes in four and higher dimensions.


XI. PACKING SPHERES IN HIGH-DIMENSIONAL EUCLIDEAN SPACES


   There has been resurgent interest in sphere packings for d > 3 in both the physical
and mathematical sciences (Adda-Bedia et al., 2008; Cohn, 2002; Cohn and Elkies, 2003;
Cohn and Kumar, 2009; Conway and Sloane, 1995; Elkies, 2000; Frisch and Percus, 1999;
Lue et al., 2010; van Meel et al., 2009; Parisi and Slanina, 2000; Parisi and Zamponi, 2006,
2010; Rohrmann and Santos, 2007; Scardicchio et al., 2008; Skoge et al., 2006; Torquato,
2006; Torquato and Stillinger, 2006a,b; van Meel et al., 2009). Remarkably, the optimal
way of sending digital signals over noisy channels corresponds to the densest sphere pack-
ing in a high-dimensional space (Conway and Sloane, 1998; Shannon, 1948). These “error-
correcting” codes underlie a variety of systems in digital communications and storage, in-
cluding compact disks, cell phones and the Internet; see Fig. 35. Physicists have studied
sphere packings in high dimensions to gain insight into liquid and glassy states of matter as
well as phase behavior in lower dimensions (Adda-Bedia et al., 2008; Frisch and Percus,
1999; van Meel et al., 2009; Parisi and Slanina, 2000; Parisi and Zamponi, 2006, 2010;


                                             70
Rohrmann and Santos, 2007; Skoge et al., 2006; van Meel et al., 2009). Finding the densest
packings in arbitrary dimension is a problem of long-standing interest in discrete geometry
(Conway and Sloane, 1998). A comprehensive review of this huge subject is beyond the
scope of this article. We instead briefly summarize the relevant literature leading to a recent
development that supports the counterintuitive possibility that the densest sphere packings
for sufficiently large d may be disordered (Scardicchio et al., 2008; Torquato and Stillinger,
2006b), or at least possess fundamental cells whose size and structural complexity increase
with d.
   The sphere packing problem seeks to answer the following question: Among all packings
of congruent spheres in Rd , what is the maximal packing density φmax and what are the cor-
responding arrangements of the spheres (Conway and Sloane, 1998)? The optimal solutions
are known only for the first three space dimensions (Hales, 2005). For 4 ≤ d ≤ 9, the densest
known packings are Bravais lattice packings (Conway and Sloane, 1998). For example, the
“checkerboard” lattice Dd , which is a d-dimensional generalization of the fcc lattice (densest
packing in R3 ), is believed to be optimal in R4 and R5 . The remarkably symmetric E8
and Leech lattices in R8 and R24 , respectively, are most likely the densest packings in these
dimensions (Cohn and Kumar, 2009). Table III lists the densest known sphere packings in
Rd for selected d. Interestingly, the non-lattice (periodic) packing P10c (with 40 spheres
per fundamental cell) is the densest known packing in R10 , which is the lowest dimension
in which the best known packing is not a (Bravais) lattice. It is noteworthy that for suffi-
ciently large d, lattice packings are most likely not the densest (see Fig. 36), but it becomes
increasingly difficult to find explicit dense packing constructions as d increases. Indeed, the
problem if finding the shortest lattice vector in a particular lattice packing (densest lattice
packing) grows super-exponentially with d and is in the class of NP-hard (non-deterministic
polynomial-time hard)problems (Ajtai, 1998).
   For large d, the best that one can do theoretically is to devise upper and lower bounds
on φmax (Conway and Sloane, 1998). The nonconstructive lower bound of Minkowski, 1905
established the existence of reasonably dense lattice packings. He found that the maximal
packing fraction φLmax among all lattice packings for d ≥ 2 satisfies

                                                      ζ(d)
                                            φLmax ≥        ,                               (32)
                                                      2d−1
               P∞        −d
where ζ(d) =     k=1 k        is the Riemann zeta function. Note that for large values of d, the

                                                71
FIG. 35 (color online) A fundamental problem in communications theory is to find the best way to
send signals or “code words” (amplitudes at d different frequencies) over a noisy channel. Each code
word s corresponds to a coordinate in Rd . The sender and receiver desire to design a “code book”
that contains a large number of code words that can be transmitted with maximum reliability
given the noise inherent in any communications channel. Due to the noise in the channel, the code
word s will be received as r 6= s such that |s − r| < a, where the distance a is the maximum error
associated with the channel. Shannon, 1948 showed that the best way to send code words over
a noisy channel is to design a code book that corresponds to the densest arrangement of spheres
of radius 2a in Rd . To understand this remarkable result, this figure depicts two choices for the
code book in two dimensions. Left panel: Three code words (depicted as green points) that are
circumscribed by circles of radius a are shown in which the distance between any two words is
chosen to be less than 2a. The received signal (red point) falls in the region common to all circles
and therefore the receiver cannot determine which of the three code words shown was sent. Right
panel: By choosing a code book in which the code words are at least a distance 2a apart (which
corresponds to a sphere packing), any ambiguity about the transmitted code word is eliminated.
Since one desires to send many code words per unit volume, the best code book corresponds to the
densest sphere packing in Rd in the limit that the number of code words tends to infinity.



asymptotic behavior of the Minkowski lower bound is controlled by 2−d .
   Since 1905, many extensions and generalizations of (32) have been obtained (Ball, 1992;
Conway and Sloane, 1998; Davenport and Rogers, 1947; Vance, 2009), but none of these
investigations have been able to improve upon the dominant exponential term 2−d . It is
useful to note that the packing fraction of a saturated packing of congruent spheres in Rd

                                               72
FIG. 36 (color online) Lattice packings in sufficiently high dimensions are almost surely unsaturated
because the “holes” or space exterior to the spheres dominates Rd (Conway and Sloane, 1998). To
get an intuitive feeling for this phenomenon, it is instructive to examine the hypercubic lattice
Zd (square lattice for R2 and the simple cubic lattice for R3 ). Left panel: A fundamental cell
of Zd represented in two dimensions. Note that the distance between the point of intersection of
the longest diagonal in the hypercube with the hypersphere boundary and the vertex of the cube
                                √
along this diagonal is given by d − 1 for a sphere of unit radius. This means that Zd already
becomes unsaturated at d = 4. Placing an additional sphere in Z4 doubles the density of Z4 and,
in particular, yields the four-dimensional checkerboard lattice packing D4 , which is believed to
be the optimal packing in R4 . Right panel: A schematic “effective” distorted representation of
the hypersphere within the hypercubic fundamental cell for large d, illustrating that the volume
content of the hypersphere relative to the hypercube rapidly diminishes asymptotically. Indeed,
the packing fraction of Zd is given by φ = π d/2 /(Γ(1 + d/2)2d ). It is the presence of the gamma
function, which grows like (d/2)!, in the denominator that makes Zd far from optimal (except for
d = 1). In fact, the checkerboard lattice Dd with packing fraction φ = π d/2 /(Γ(1 + d/2)2(d+2)/2 )
becomes suboptimal in relatively low dimensions because it too becomes dominated by larger and
larger holes as d increases.



for all d satisfies
                                                    1
                                              φ≥       .                                        (33)
                                                    2d
The proof is trivial. A saturated packing of congruent spheres of unit diameter and packing
fraction φ in Rd has the property that each point in space lies within a unit distance from


                                               73
TABLE III The densest known sphere packings in Rd for selected d. Except for the non-lattice
packing P10c in R10 , all of the other densest known packings listed in this table are lattice packings:
Z is the integer lattice, A2 is the triangular lattice, Dd is the checkerboard lattice (a generalization
of the fcc lattice), Ed is one the root lattices, and Λd is the laminated lattice. The reader is referred
to Conway and Sloane, 1998 for further details.


                Dimension, d Packing Structure         Packing Fraction, φ
                     1              Z                            1
                                                           √
                     2              A2                 π/ 12 = 0.9068 . . .
                                                           √
                     3             D3                  π/ 18 = 0.7404 . . .
                     4             D4                  π 2 /16 = 0.6168 . . .
                                                              √
                     5             D5             2π 2 /(30 2) = 0.4652 . . .
                                                              √
                     6              E6            3π 2 /(144 3) = 0.3729 . . .
                     7              E7                 π 3 /105 = 0.2952 . . .
                     8              E8                 π 4 /384 = 0.2536 . . .
                                                              √
                     9              Λ9            2π 4 /(945 2) = 0.1457 . . .
                    10             P10c              π 5 /3072 = 0.09961 . . .
                    16             Λ16             π 8 /645120 = 0.01470 . . .
                    24             Λ24         π 12 /479001600 = 0.001929 . . .

the center of some sphere. Thus, a covering of the space is achieved if each sphere center is
encompassed by a sphere of unit radius and the packing fraction of this covering is 2d φ ≥ 1.
Thus, the bound (33), which is sometimes called the “greedy” lower bound, has the same
dominant exponential term as (32).
   We know that there exists a disordered but unsaturated packing construction, known as
the “ghost” random sequential addition (RSA) packing (Torquato and Stillinger, 2006a),
that achieves the packing 2−d for any d. This packing, depicted in Fig. 37 and described in
its caption, is a generalization of the standard RSA packing, also described in the caption of
Fig 37. It was shown that all of the n-particle correlation functions of this nonequilibrium
model, in a certain limit, can be obtained analytically for all allowable densities and in
any dimension. This represents the first exactly solvable disordered sphere-packing model
in arbitrary dimension. (Note that Matérn, 1986 gave an expression for the pair correla-
tion function for this model.) The existence of this unjammed disordered packing strongly
suggests that Bravais-lattice packings (which are almost surely unsaturated for sufficiently


                                                 74
large d) are far from optimal for large d. Further support for this conclusion is the fact
that the maximal “saturation” packing fraction of the standard disordered RSA packing
apparently scales as d · 2−d or possibly d · ln(d) · 2−d for large d (Torquato et al., 2006).
Spheres in both the ghost and standard RSA packings cannot form interparticle contacts,
which appears to be a crucial attribute to obtain exponential improvement on Minkowski’s
bound (Torquato and Stillinger, 2006b), as we discuss below.




FIG. 37 (Color online) The ghost RSA packing model in Rd is a subset of the Poisson point process
and a generalization of the standard RSA process. The latter is produced by randomly, irreversibly, and

sequentially placing nonoverlapping objects into a large volume in Rd that at some initial time is empty

of spheres (Cooper, 1988; Feder, 1980; Viot et al., 1993; Widom, 1966). If an attempt to add a sphere at

some time results in an overlap with an existing sphere in the packing, the attempt is rejected and further

attempts are made until it can be added without overlapping existing spheres. As the process continues in

time, it becomes more difficult to find available regions into which the spheres can be added, and eventually

in the saturation or infinite-time limit , no further additions are possible. In the ghost RSA process, a

sphere that is rejected is called a “ghost” sphere. No additional spheres can be added whether they overlap

an existing sphere or a ghost sphere. The packing fraction at time t for spheres of unit diameter is given

by φ(t) = [1 − exp(−v1 (1)t)]/2d , where v1 (R) is the volume of sphere of radius R [cf. (2)]. Thus, we see

that as t → +∞, φ → 2−d . This figure shows a configuration of 468 particles of a ghost RSA packing

in a fundamental cell in R2 at a packing fraction very near its maximal value of 0.25, as adapted from

Scardicchio et al., 2008. Note that the packing is clearly unsaturated and there are no contacting particles.



                                                   75
     The best currently known lower bound on φLmax for dimensions not divisible by four was
obtained by Ball, 1992. He found that
                                                  2(d − 1)ζ(d)
                                        φLmax ≥                .                          (34)
                                                       2d
For dimensions divisible by four, Vance, 2009 has recently found the tightest lower bound
on the maximal packing fraction among lattice packings:
                                                         6d
                                        φLmax ≥                    .                      (35)
                                                  2d e(1 − e−d )
Table IV gives the dominant asymptotic behavior of several lower bounds on φLmax for large
d. Note that the best lower bounds on φLmax improve on Minkowski’s bound by a linear
factor in d rather than providing exponential improvement. This suggests that the packing
fraction of the densest lattice packing in high d is controlled by the exponential factor 2−d .

TABLE IV Dominant asymptotic behavior of lower bounds on φL
                                                          max for sphere packings for large

d. The bound due to Vance, 2009 is applicable for dimensions divisible by four. The best lower
bounds do not provide exponential improvement on Minkowski’s lower bound; they instead only
improve on the latter by a factor linear in d.



                                (2)2−d        Minkowski (1905)
                                √
                            [ln( 2)d]2−d Davenport and Rogers (1947)

                              (2d)2−d                  Ball (1992)

                             (6d/e)2−d                 Vance (2009)



TABLE V Dominant asymptotic behavior of upper bounds on φmax for sphere packings for large
d.


                         (d/2)2−0.5d              Blichfeldt (1929)

                         (d/e)2−0.5d               Rogers (1958)

                          2−0.5990d Kabatiansky and Levenshtein (1979)


     Nontrivial upper bounds on the maximal packing fraction φmax for any sphere packing in
Rd have been derived. Blichfeldt, 1929 showed that the maximal packing fraction for all d

                                                  76
satisfies φmax ≤ (d/2 + 1)2−d/2 . This upper bound was improved by Rogers, 1958, 1964 by
an analysis of the Voronoi cells. For large d, Rogers’ upper bound asymptotically becomes
d · 2−d/2 /e. Kabatiansky and Levenshtein, 1978 found an even stronger bound, which in the
limit d → ∞ yields φmax ≤ 2−0.5990d . All of these upper bounds prove that the maximal
packing fraction tends to zero in the limit d → ∞. This rather counterintuitive high-
dimensional property of sphere packings can be understood by recognizing that almost all of
the volume of a d-dimensional sphere for large d is concentrated near the sphere surface. For
example, the volume contained with such a sphere up to 99% of it radius is (99/100)d, which
tends to zero exponentially fast. Thus, in high-dimensional sphere packings (densest or not),
almost all of the volume is occupied by the void space (space exterior to the spheres), which
is to be contrasted with the densest sphere packings in low dimensions in which the volume
contained within the spheres dominates over the void volume.
   Cohn and Elkies, 2003 obtained and computed linear programming upper bounds, which
provided improvement over Rogers’ upper bounds for dimensions 4 through 36, but it is
not yet known whether they improve upon the Kabatiaksky-Levenshtein upper bounds for
large d. Cohn and Kumar, 2009 used these techniques to prove that the Leech lattice is the
unique densest lattice in R24 . They also proved that no sphere packing in R24 can exceed
the density of the Leech lattice by a factor of more than 1 + 1.65 × 10−30 , and gave a new
proof that E8 is the unique densest lattice in R8 . Table V provides the dominant asymptotic
behavior of several upper bounds on φmax for large d. Note that the best upper and lower
bounds on φmax differ by an exponential factor as d → ∞.
   Since 1905, many extensions and generalizations of Minkowski’s bound have been derived
(Conway and Sloane, 1998), but none of them have improved upon the dominant exponen-
tial term 2−d . Torquato and Stillinger, 2006b used a conjecture concerning the existence
of disordered sphere packings and a g2 -invariant optimization procedure that maximizes φ
associated with a radial “test” pair correlation function g2 (r) to provide the putative expo-
nential improvement on Minkowski’s 100-year-old bound on φmax . Specifically, a g2 -invariant
process (Torquato and Stillinger, 2002) is one in which the functional form of a “test” pair
correlation g2 (r) function remains invariant as density varies, for all r, over the range of
packing fractions
                                        0 ≤ φ ≤ φ∗ .                                     (36)

The terminal packing fraction φ∗ is the maximum achievable density for the g2 -invariant

                                            77
process subject to satisfaction of certain nonnegativity conditions on pair correlations. For
any test g2 (r) that is a function of radial distance r ≡ |r| associated with a packing, i.e.,
g2 (r) = 0 for r < D, they maximized the corresponding packing fraction,

                                          φ∗ ≡ lim φ,                                       (37)
                                                 max


subject to satisfying the following two necessary conditions:

                                    g2 (r) ≥ 0     for all r,                               (38)

and
                                      S(k) ≥ 0 for all k.                                   (39)

Condition (39) is a necessary condition for the existence of any point process [cf. (7)]. When
there exist sphere packings with a g2 satisfying these conditions in the interval [0, φ∗ ], then
one has the lower bound on the maximal packing fraction given by

                                           φmax ≥ φ∗                                        (40)

   Torquato and Stillinger, 2006b conjectured that a test function g2 (r) is a pair correlation
function of a translationally invariant disordered sphere packing in Rd for 0 ≤ φ ≤ φ∗ for suffi-
ciently large d if and only if the conditions (38) and (39) are satisfied. There is mounting evi-
dence to support this conjecture. First, they identified a decorrelation principle, which states
that unconstrained correlations in disordered sphere packings vanish asymptotically in high
dimensions and that the gn for any n ≥ 3 can be inferred entirely (up to small errors) from a
knowledge of ρ and g2 . This decorrelation principle, among other results, provides justifica-
tion for the conjecture of Torquato and Stillinger, 2006b, and is vividly exhibited by the ex-
actly solvable ghost RSA packing process (Torquato and Stillinger, 2006a) as well as by com-
puter simulations in high dimensions of the maximally random jammed state (Skoge et al.,
2006) and the standard RSA packing (Torquato, 2006). Second, other necessary conditions
on g2 (Costin and Lebowitz, 2004; Hopkins et al., 2009; Torquato and Stillinger, 2006b) ap-
pear to only have relevance in very low dimensions. Third, one can recover the form of
known rigorous bounds [cf. (32) and (34)] for specific test g2 ’s when the conjecture is in-
voked. Finally, in these two instances, configurations of disordered sphere packings on the
torus have been numerically constructed with such g2 in low dimensions for densities up to
the terminal packing fraction (Crawford et al., 2003; Uche et al., 2006).

                                              78
   Using a particular test pair correlation corresponding to a disordered sphere packing,
Torquato and Stillinger, 2006b found a conjectural lower bound on φmax that is controlled
by 2−(0.77865...)d and the associated lower bound on the average contact (kissing) number
Z is controlled by 2(0.22134...)d (a highly overconstrained situation). These results counter-
intuitively suggest that the densest packings as d increases without bound may exhibit
increasingly complex fundamental cells, or even become disordered at some sufficiently large
d rather than periodic. The latter possibility would imply the existence of disordered clas-
sical ground states for some continuous potentials. Scardicchio et al., 2008 demonstrated
that there is a wide class of test functions (corresponding to disordered packings) that lead
to precisely the same putative exponential improvement on Minkowski’s lower bound and
therefore the asymptotic form 2−(0.77865...)d is much more general and robust than previously
surmised.
   Interestingly, the optimization problem defined above is the dual of the infinite-
dimensional linear program (LP) devised by Cohn, 2002 to obtain upper bounds on the
maximal packing fraction; see Cohn and Elkies, 2003 for a proof. In particular, let f (r) be
a radial function in Rd such that

                                    f (r) ≤ 0 for r ≥ D,
                                    f˜(k) ≥ 0 for all k,                                 (41)

where f˜(k) is the Fourier transform of f (r). Then the number density ρ is bounded from
above by
                                            f (0)
                                          min       .                               (42)
                                           2d f˜(0)
The radial function f (r) can be physically interpreted to be a pair potential. The fact
that its Fourier transform must be nonnegative for all k is a well-known stability con-
dition for many-particle systems with pairwise interactions (Ruelle, 1999). We see that
whereas the LP problem specified by (38) and (39) utilizes information about pair correla-
tions, its dual program (41) and (42) uses information about pair interactions. As noted by
Torquato and Stillinger, 2006b, even if there does not exist a sphere packing with g2 satis-
fying conditions (38), (39) and the hard-core constraint on g2 , the terminal packing fraction
φ∗ can never exceed the Cohn-Elkies upper bound. Every LP has a dual program and when
an optimal solution exists, there is no duality gap between the upper bound and lower bound
formulations. Recently, Cohn and Kumar, 2007a proved that there is no duality gap.

                                             79
XII. REMARKS ON PACKING PROBLEMS IN NON-EUCLIDEAN SPACES


   Particle packing problems in non-Euclidean (curved) spaces have been the focus of re-
search in a variety of fields, including physics (Bowick et al., 2006; Modes and Kamien,
2007), biology (Goldberg, 1967; Prusinkiewicz and Lindenmayer, 1990; Tammes, 1930;
Torquato et al., 2002; Zandi et al., 2004), communications theory (Conway and Sloane,
1998), and geometry (Cohn and Kumar, 2007b; Conway and Sloane, 1998; Hardin and Saff,
2004). Although a comprehensive overview of this topic is beyond the scope of this review,
we highlight here some of the developments for the interested reader in spaces with constant
positive and negative curvatures. We will limit the discussion to packing spheres on the
positively curved unit sphere S d−1 ⊂ Rd and in negatively curved hyperbolic space Hd .
   The kissing (or contact) number τ is the number of spheres of unit radius that can
simultaneously touch a unit sphere S d−1 (Conway and Sloane, 1998). The kissing number
problem asks for the maximal kissing number τmax in Rd . The determination of the maximal
kissing number in R3 spurred a famous debate between Issac Newton and David Gregory
in 1694. The former correctly thought the answer was 12, but the latter wrongly believed
that 13 unit spheres could simultaneously contact another unit sphere. The optimal kissing
number τmax in dimensions greater than three is only known for R4 (Musin, 2008), R8 and
R24 (Levenshtein, 1979; Odlyzko and Sloane, 1979). Table VI lists the largest known kissing
numbers in selected dimensions.
   In geometry and coding theory, a spherical code with parameters (d, N, t) is a set of
N points on the unit sphere S d−1 such that no two distinct points in that set have inner
product greater than or equal to t, i.e., the angles between them are all at least cos−1 t. The
fundamental problem is to maximize N for a given value of t, or equivalently to minimize t
given N [sometimes called the Tammes problem, which was motivated by an application in
botany (Tammes, 1930)]. One of the first rigorous studies of spherical codes was presented
by Schuette and van der Waerden, 1951. Delsarte et al., 1977 introduced much of the most
important mathematical machinery to understand spherical codes and designs. One natural
generalization of the best way to distribute points on S d−1 (or Rd ) is the energy minimization
problem: given some potential function depending on the pairwise distances between points,
how should the points be arranged so as to minimize the total energy (or what are the
ground-state configurations)? The original Thomson problem of “spherical crystallography”


                                             80
TABLE VI The largest known kissing numbers for identical spheres in Rd for selected d. Except
for R9 and R10 , the largest known kissing numbers listed in this table are those found in the densest
lattice packings listed in Table III. P9a is a non-lattice packing with an average kissing number of
235 3/5 but with a maximum kissing number of 306. P10b is a non-lattice packing with an average
kissing number of 340 1/3 but with a maximum kissing number of 500. The reader is referred to
Conway and Sloane, 1998 for further details.


                     Dimension, d Packing Structure Kissing Number, τ
                          1              Z                  2
                          2              A2                 6
                          3             D3                  12
                          4             D4                  24
                          5             D5                  40
                          6              E6                 72
                          7              E7                126
                          8              E8                240
                          9             P9a                306
                         10             P10b               500
                         16             Λ16               4,320
                         24             Λ24              196,560

seeks the ground states of electron shells interacting via the Coulomb potential; but it
is also profitable to study ground states of particles interacting with other potentials on
S d−1 (Bowick et al., 2006). Cohn and Kumar, 2007b have introduced the beautiful idea of a
universally optimal configuration, a unique configuration that minimizes a class of potentials.
In particular, they proved that for any fixed number of points N on S d−1 there is a universally
optimal configuration that minimizes all completely monotonic potential functions (e.g., all
inverse power laws).
   The optimal spherical code problem is related to the densest local packing (DLP) problem
in Rd (Hopkins et al., 2010a), which involves the placement of N nonoverlapping spheres of
unit diameter near an additional fixed unit-diameter sphere such that the greatest radius
R from the center of the fixed sphere to the centers of any of the N surrounding spheres is
minimized. Let us recast the optimal spherical code problem as the placement of the centers
of N nonoverlapping spheres of unit diameter onto the surface of a sphere of radius R such


                                                81
that R is minimized. It is has been proved that for any d, all solutions for R between unity
                             √
and the golden ratio τ = (1 + 5)/2 to the optimal spherical code problem for N spheres are
also solutions to the corresponding DLP problem (Hopkins et al., 2010b). It follows that for
any packing of nonoverlapping spheres of unit diameter, a spherical region of radius R less
than or equal to τ centered on an arbitrary sphere center cannot enclose a number of sphere
centers greater than one more than the number that than can be placed on the spherical
region’s surface.
   We saw in Sec.VIII that monodisperse circle (circular disk) packings in R2 have a great
tendency to crystallize at high densities due to a lack of geometrical frustration. The hyper-
bolic plane H2 (for a particular constant negative curvature, which measures the deviation
from the flat Euclidean plane) provides a two-dimensional space in which global crystalline
order in dense circle packings is frustrated, and thus affords a means to use circle pack-
ings to understand fundamental features of simple liquids, disordered jammed states and
glasses. Modes and Kamien, 2007 formulated an expression for the equation of state for
disordered hard disks in H2 and compared it to corresponding results obtained from molec-
ular dynamics simulations. Modes and Kamien, 2007 derived a generalization of the virial
equation in H2 relating the pressure to the pair correlation function and developed the ap-
propriate setting for extending integral-equation approaches of liquid-state theory. For a
discussion of the mathematical subtleties associated with finding the densest packings of
identical d-dimensional spheres in Hd , the reader is referred to Bowen and Radin, 2003.


XIII. CHALLENGES AND OPEN QUESTIONS


   The geometric-structure approach advanced and explored in this review provides a com-
prehensive methodology to analyze and compare jammed disk and sphere packings across
their infinitely rich variety. This approach also highlights aspects of present ignorance, thus
generating many challenges and open questions for future investigation. Even for identical
spheres, detailed characterization of jammed structures across the simple two-dimensional
(φ-ψ) order maps outlined in Sec. V is still very incomplete. A partial list of open and
challenging questions in the case of sphere packings includes the following:

   1. Are the strictly jammed “tunneled” crystals (Torquato and Stillinger, 2007) the family
      of lowest density collectively jammed packings under periodic boundary conditions?

                                             82
  2. How can the extremal jammed packings that inhabit the upper and lower boundaries
      of occupied regions of each of those order maps be unambiguously identified?

  3. What would be the shapes of analogous occupied regions if the two-parameter versions
      illustrated in Fig. 13 were to be generalized to three or more parameters?

  4. To what extent can the rattler concentration in collectively or strictly sphere packings
      be treated as an independent variable? What is the upper limit to attainable rattler
      concentrations under periodic boundary conditions?

  5. What relations can be established between order metrics and geometry of the corre-
      sponding configurational-space polytopes?

  6. Can upper and lower bounds be established for the number of collectively and/or
      strictly jammed states for N spheres?

  7. Upon extending the geometric-structure approach to Euclidean dimensions greater
      than three, do crystalline arrangements with arbitrarily large unit cells or even disor-
      dered jammed packings ever provide the highest attainable densities?

   Jamming characteristics of nonspherical and even non-convex hard particles is an area of
research that is still largely undeveloped and therefore deserves intense research attention.
Many of the same open questions identified above for sphere packings are equally relevant
to packings of nonspherical particles. An incomplete list of open and challenging questions
for such particle packings includes the following:

  1. What are the appropriate generalizations of the jamming categories for packings of
      nonspherical particles?

  2. Can one devise incisive order metrics for packings of nonspherical particles as well as
      a wide class of many-particle systems (e.g., molecular, biological, cosmological, and
      ecological structures)?

  3. Can sufficient progress be made to answer the first two questions that would lead to
      useful order maps? If so, how do the basic features of order maps depend on the shape
      of the particle? What are the lowest density jammed states?


                                            83
   4. Why does the deformation of spheres into ellipsoids have the effect of strongly inhibit-
      ing (if not completely preventing) the appearance of rattlers in disordered ellipsoid
      packings for a wide range of aspect ratios? Does this same inhibitory phenomenon
      extend to disordered jammed packings of other nonspherical shapes?

   5. For non-tiling nonspherical particles, can an upper bound on the maximal packing
      fraction be derived that is always strictly less than unity? (Note that upper bound
      (31) is strictly less than unity provided that the asphericity is sufficiently small.)

   Jamming characteristics of particle packings in non-Euclidean spaces is an area of research
that is still largely undeveloped and therefore deserves research attention. This is true even
for simple particle shapes, such as spheres. For example, we know very little about the
jamming categories of spheres in curved spaces. Does curvature facilitate jamming or not?
Does it induce ordering or disordering? These are just a few of the many challenging issues
that merit further investigation.
   In view of the wide interest in packing problems that the research community displays
there is reason to be optimistic that substantial conceptual advances are forthcoming. It
will be fascinating to see how future review articles covering this subject document those
advances.


   Acknowledgments


   The authors are grateful to Yang Jiao for producing many of the figures and generating
the data for Fig. 16. We thank Yang Jiao, Henry Cohn and Aleksandar Donev for useful
discussions. This work was supported by the Division of Mathematical Sciences at the
National Science Foundation under Award No. DMS-0804431 and by the MRSEC Program
of the National Science Foundation under Award No. DMR-0820341.


   References


Adda-Bedia, M., E. Katzav, and D. Vella, 2008, “Solution of the Percus-Yevick equation for hard
  hyperspheres in even dimensions,” J.Chem. Phys. 129, 144506.




                                             84
Ajtai, M., 1998, in STOC ‘98: Proceedings of the thirtieth annual ACM symposium on Theory of
  computing, 10–19.
Alexander, S., 1998, “Amorphous solids: their structure, lattice dynamics and elasticity,” Phys.
  Rep. 296, 65–236.
Allen, M. P., 1993, “Simulations Using Hard Particles,” Phil. Trans. R. Soc. Lond. A 344, 323–337.
Andreev, A. F., 1964, “Singularity of Thermodynamic Quantities at a First Order Phase Transition
  Point,” Soviet Phys. J.E.T.P. 18, 1415–1416.
Anonymous, 1972, “What is Random Packing?,” Nature 239, 488–489.
Ashcroft, N. W., and D. N. Mermin, 1976, Solid State Physics (Thomson Learning, Toronto).
Aste, T., M. Saadatfar, and T. Senden, 2006, “Local and Global Relations Between the Number
  of Contacts and Density in Monodisperse Sphere Packs,” J. Stat. Mech. P07010.
Aste, T., and D. Weaire, 2008, The Pursuit of Perfect Packing (Taylor and Francis, New York), 2
  edition.
Ball, K., 1992, “A Lower Bound for the Optimal Density of Lattice Packings,” Int. Math. Res.
  Notices 68, 217–221.
Barlow, W., 1883, “Probable Nature of the Internal Symmetry of Crystals,” Nature 29, 186–188,.
Bernal, J. D., 1960, “Geometry and the Structure of Monatomic Liquids,” Nature 185, 68–70.
Bernal, J. D., 1965, in Liquids: structure, properties,solid interactions, edited by T. J. Hughel
  (Elsevier, New York), 25–50.
Berryman, J. G., 1983, “Random Close Packing of Hard Spheres and Disks,” Phys. Rev. A 27,
  1053–1061.
Betke, U., and M. Henk, 2000, “Densest lattice packings of 3-polytopes,” Comput. Geom. 16,
  157–186.
A. Bezdek, K. Bezdek, and Connelly, R., 1998, “Finite and Uniform Stability of Sphere Packings,”
  Discrete and Computational Geometry 20, 111–130.
Blichfeldt, H., 1929, “The Minimum Value of Quadratic Forms and the Closest Packing of Spheres,”
  Math. Ann. 101, 605–608.
Boltzmann, L., 1898, Lectures on Gas Theory (University of California Press, Berkeley, California),
  1964 translation by S. G. Brush of the original 1898 publication.
Böröczky, K., 1964, “Uber Stabile Kreis- und Kugelsysteme,” Ann. Univ. Sci. Budapest Estvss.
  Sect. Math. 7(79).


                                               85
Bowen, L., and C. Radin, 2003, “Densest Packing of Equal Spheres in Hyperbolic Space,” Discrete
  Comput. Geom. 29, 23–29.
Bowick, M. J., A. C., D. R. Nelson, and A. Travesset, 2006, “Crystalline particle packings on a
  sphere with long-range power-law potentials,” Phys. Rev. B 73, 024115.
Brujic, J., S. F. Edwards, I. Hopkinson, and H. A. Makse, 2003, “Measuring Distribution of
  Interdroplet Forces in a Compressed Emulsion System,” Physica A 327, 201–212.
Burnell, F. J., and S. L. Sondhi, 2008, “Classical antiferromagnetism on Torquato-Stillinger pack-
  ings,” Phys. Rev. B 78, 024407.
Chaikin, P. M., and T. C. Lubensky, 1995, Principles of Condensed Matter Physics (Cambridge
  University Press, New York).
Chaikin, P. M., S. Wang, and A. Jaoshvili, 2007, in Am. Phys. Soc. March Meeting.
Chaudhuri, P., L. Berthier, and S. Sastry, 2010, “Jamming Transitions in Amorphous Packings
  of Frictionless Spheres Occur over a Continuous Range of Volume Fractions,” Phys. Rev. Lett.
  104, 165701.
Chen, E. R., 2008, “A Dense Packing of Regular Tetrahedra,” Discrete Comput. Geom. 40, 214–
  240.
Chen, E. R., M. Engel, and S. C. Glotzer, 2010, “Dense crystalline dimer packings of regular
  tetrahedra,”, Discrete Comput. Geom. 44, 253–280.
Christensen, R. M., 1979, Mechanics of Composite Materials (Wiley, New York).
Clisby, N., and B. M. McCoy, 2006, “Ninth and Tenth Order Virial Coefficients for Hard Spheres
  in D Dimensions,” J. Stat. Phys. 122, 15–57.
Clusel, M., E. I. Corwin, A. O. N. Siemens, and J. Brujić, 2009, “A ‘Granocentric’ Model for
  Random Packing of Jammed Emulsions,” Nature 460, 611–615.
Cohn, H., 2002, “New upper bounds on sphere packings II,” Geom. Topol. 6, 329–353.
Cohn, H., and N. Elkies, 2003, “New upper bounds on sphere packings I,” Annals Math. 157,
  689–714.
Cohn, H., and A. Kumar, 2007a, private communication.
Cohn, H., and A. Kumar, 2007b, “Universally Optimal Distribution of Points on Spheres,” J. Am.
  Math. Soc. 157, 99–148.
Cohn, H., and A. Kumar, 2009, “Optimality and uniqueness of the Leech lattice among lattices,”
  Ann. Math. 170, 1003–1050.


                                              86
Connelly, R., 1982, “Rigidity and Energy,” Invent. Math. 66, 11–33.
Connelly, R., and W. Whiteley, 1996, “Second-Order Rigidity and Prestress Stability for Tensegrity
  Frameworks,” SIAM Journal of Discrete Mathematics 9, 453–491.
Conway, J. H., and N. J. A. Sloane, 1995, “What are All the Best Sphere Packings n Low Dimen-
  sions?,” Discrete Comput. Geom. 13, 383–403.
Conway, J. H., and N. J. A. Sloane, 1998, Sphere Packings, Lattices and Groups (Springer-Verlag,
  New York).
Conway, J. H., and S. Torquato, 2006, “Packing, Tiling and Covering with Tetrahedra,” Proc. Nat.
  Acad. Soc. 103, 10612–10617.
Cooper, D. W., 1988, “Random-sequential-packing simulations in three dimensions for spheres,”
  Phys. Rev. A 38, 522–524.
Costin, O., and J. Lebowitz, 2004, “On the Construction of Particle Distributions with Specified
  Single and Pair Densities,” J. Phys. Chem. B. 108, 19614–19618.
Coxeter, H. S. M., 1973, Regular Polytopes (Dover, New York).
Cramer, H., 1954, Mathematical Methods of Statistics (Princeton University Press, Princeton).
Crawford, J. R., S. Torquato, and F. H. Stillinger, 2003, “Aspects of Correlation Function Realiz-
  ability,” J. Chem. Phys. 119, 7065–7074.
Davenport, H., and C. Rogers, 1947, “Hlawka’s Theorem in the Geometry of Numbers,” Duke J.
  math. 14, 367–375.
Delsarte, P., J.-M. Goethals, and J. Seidel, 1977, “Spherical codes and designs,” Geom. Dedicata
  6, 363–388.
Dijkstra, M., R. van Roij, and R. Evans, 1999, “Direct simulation of the phase behavior of binary
  hard-sphere mixtures: Test of the depletion potential description,” Phys. Rev. Lett. 82, 117–120.
Domb, C., 1960, “On the Theory of Cooperative Phenomena in Crystals,” Adv. Phys. 9, 149–361.
Donev, A., I. Cisse, D. Sachs, E. A. Variano, F. H. Stillinger, R. Connelly, S. Torquato, and
  P. M. Chaikin, 2004a, “Improving the Density of Jammed Disordered Packings using Ellipsoids,”
  Science 303, 990–993.
Donev, A., R. Connelly, F. H. Stillinger, and S. Torquato, 2007a, “Underconstrained Jammed
  Packings of Nonspherical Hard Particles: Ellipses and Ellipsoids,” Phys. Rev. E 75, 051304.
Donev, A., F. H. Stillinger, P. M. Chaikin, and S. Torquato, 2004b, “Unusually Dense Crystal
  Ellipsoid Packings,” Phys. Rev. Lett. 92, 255506.


                                              87
Donev, A., F. H. Stillinger, and S. Torquato, 2005a, “Unexpected Density Fluctuations in Disor-
  dered Jammed Hard-Sphere Packings,” Phys. Rev. Lett. 95, 090604.
Donev, A., F. H. Stillinger, and S. Torquato, 2006, “Do Binary Hard Disks Exhibit an Ideal Glass
  Transition?,” Phys. Rev. Lett. 96, 225502.
Donev, A., F. H. Stillinger, and S. Torquato, 2007b, “Configurational Entropy of Binary Hard-Disk
  Glasses: Nonexistence of an Ideal Glass Transition,” J. Chem. Phys. 127, 124509.
Donev, A., S. Torquato, and F. H. Stillinger, 2005b, “Neighbor List Collision-Driven Molecular
  Dynamics for Nonspherical Hard Particles: I. Algorithmic Details,” J. Comput. Phys. 202, 737–
  764.
Donev, A., S. Torquato, and F. H. Stillinger, 2005c, “Neighbor List Collision-Driven Molecular Dy-
  namics for Nonspherical Hard Particles: II. Applications to Ellipses and Ellipsoids,,” J. Comput.
  Phys. 202, 765–793.
Donev, A., S. Torquato, and F. H. Stillinger, 2005d, “Pair Correlation Function Characteristics
  of Nearly Jammed Disordered and Ordered Hard-Sphere Packings,” Phys. Rev. E 71, 011105:
  1–14.
Donev, A., S. Torquato, F. H. Stillinger, and R. Connelly, 2004c, “Jamming in Hard Sphere and
  Disk Packings,” J. Appl. Phys. 95, 989–999.
Donev, A., S. Torquato, F. H. Stillinger, and R. Connelly, 2004d, “A Linear Programming Algo-
  rithm to Test for Jamming in Hard-Sphere Packings,” J. Comput. Phys. 197, 139–166.
Donev, A., S. Torquato, F. H. Stillinger, and R. Connelly, 2007c, “Comment on ‘Jamming at zero
  temperature and zero applied stress: The epitome of disorder’,” Phys. Rev. E 70, 043301.
Edwards, S. F., 1994, “Granular Matter,” (Springer-Verlag, New York).
Edwards, S. F., and D. V. Grinev, 2001, “The Tensorial Formulation of Volume Function for
  Packings of Particles,” Chem. Eng. Sci. 56, 5451–5455.
Elkies, N. D., 2000, “Lattices, Linear Codes, and Invariants, Part I,” Notices of the AMS 47,
  1238–1245.
Ellis, R., 2001, “Macromolecular Crowding: Obvious But Underappreciated,” Trends Biochem.
  Sci. 26, 597–604.
Errington, J. R., and P. G. Debenedetti, 2001, “Relationship Between Structural Order and the
  Anomalies of Liquid Water,” Nature 409, 318–321.
Errington, J. R., P. G. Debenedetti, and S. Torquato, 2002, “Cooperative Origin of Low-Density


                                                88
  Domains in Liquid Water,” Phys. Rev. Lett. 89, 215503.
Errington, J. R., P. G. Debenedetti, and S. Torquato, 2003, “Quantification of Order in the
  Lennard-Jones System,” J. Chem. Phys. 118, 2256.
Feder, J., 1980, “Random Sequential Adsorption,” J. Theor. Biol. 87, 237–254.
Fejes Tóth, L., 1964, Regular Figures (Macmillan, New York).
Feynman, R. P., and M. Cohen, 1956, “Energy Spectrum of the Excitations in Liquid Helium,”
  Phys. Rev. 102, 1189–1204.
Fisher, M. E., and B. U. Felderhof, 1970, “Phase transitions in One-Dimensional Cluster-Interaction
  Fluids,” Ann. Phys. 58, 176–216.
Florian, A., 1960, “Ausfüllung der Ebene durch Kreise,” Rend. Circ. Mat. Palermo 1, 1–13.
Frenkel, D., and J. F. Maguire, 1983, “Molecular dynamics study of the dynamical properties of
  an assembly of infinitely thin hard rods,” Mol. Phys. 49, 503–541.
Frenkel, D., B. M. Mulder, and J. P. McTague, 1984, “Phase Diagram of a System of Hard Ellip-
  soids,” Phys. Rev. Lett. 52, 287–290.
Frisch, H. L., and J. K. Percus, 1999, “High Dimensionality as an Organizing Device for Classical
  Fluids,” Phys. Rev. E 60, 2942–2948.
Gallavotti, G., 1999, Statistical Mechanics (Springer-Verlag, New York).
Gao, G.-J., J. Blawzdziewicz, and C. S. O’Hern, 2006, “Understanding the Frequency Distribution
  of Mechanically Stable Disk Packings,” Phys. Rev. E 74, 061304.
Gardner, M., 2001, The Colossal Book of Mathematics: Classic Puzzles, Paradoxes, and Problems
  (Norton, New York).
Gauss, C. F., 1831, “Besprechung des Buchs von L. A. Seeber: Untersuchungen über die Eigen-
  schaften der positiven ternären quadratischen Formen,” Göttingsche Gelehrte Anzeigen See also
  J. reine angew. Math., vol. 20, 1840, 312-320.
Gevertz, J. L., and S. Torquato, 2008, “A Novel Three-Phase Model of Brain Tissue Microstruc-
  ture,” Plos. Comput. Bio. 4, e100052.
Goldberg, M., 1967, “Viruses and a mathematical problem,” J. Mol. Bio. 24, 337–338.
Gotoh, K., and J. L. Finney, 1974, “Statistical geometrical approach to random packing density of
  equal spheres,” Nature 252, 202–205.
Haji-Akbari, A., M. Engel, A. S. Keys, X. Zheng, R. G. Petschek, P. Palffy-Muhoray, and S. C.
  Glotzer, 2009, “Disordered, quasicrystalline and crystalline phases of densely packed tetrahedra,”


                                               89
  Nature 462, 773–777.
Hales, T. C., 2005, “A Proof of the Kepler Conjecture,” Ann. Math. 162, 1065–1185.
Hansen, J. P., and I. R. McDonald, 1986, Theory of Simple Liquids (Academic Press, New York).
Hardin, D. P., and E. B. Saff, 2004, “Discretizing manifolds via minimum energy points,” Notices
  Amer. Math. Soc. 51, 1186–1194.
Henderson, S. I., T. C. Mortensen, S. M. Underwood, and W. van Megen, 1996, “Effect of particle
  size distribution on crystallisation and the glass transition of hard sphere colloids,” Physica A
  233, 102–116.
Herrmann, H. J., G. Mantica, and D. Bessis, 1990, “Space-filling bearings,” Phys. Rev. Lett. 65,
  3223–3226.
Hopkins, A. B., F. H. Stillinger, and S. Torquato, 2009, “Dense Sphere Packings from Optimized
  Correlation Functions,” Phys. Rev. E 79, 031123.
Hopkins, A. B., F. H. Stillinger, and S. Torquato, 2010a, “Densest Local Sphere-Packing Diversity:
  General concepts and application to two dimensions,” Phys. Rev. E 81, 041305.
Hopkins, A. B., F. H. Stillinger, and S. Torquato, 2010b, “Spherical codes, maximal local packing
  density, and the golden ratio,” J. Math. Phys. 51, 043302.
Hudson, T. S., and P. Harrowell, 2008, “Dense packings of hard spheres of different sizes based on
  filling interstices in uniform three-dimensional tilings,” J. Phys. Chem. B 112, 8139–8143.
Jaoshvili, A., A. Esakia, M. Porrati, and P. M. Chaikin, 2010, “Experiments on the Random
  Packing of Tetrahedral Dice,” Phys. Rev. Lett. 104, 185501.
Jiao, Y., F. H. Stillinger, and S. Torquato, 2008, “Optimal Packings of Superdisks and the Role of
  Symmetry,” Phys. Rev. Lett. 100, 245505.
Jiao, Y., F. H. Stillinger, and S. Torquato, 2009, “Optimal Packings of Superballs,” Phys. Rev. E
  79, 041309.
Jiao, Y., F. H. Stillinger, and S. Torquato, 2010a, “Distinctive Features Arising in Maximally
  Random Jammed Packings of Superballs,” PRE 81, 041304.
Jiao, Y., F. H. Stillinger, and S. Torquato, 2010b, “Non-Universality of Density and Disorder in
  Jammed Sphere Packings,”, in preparation.
Jodrey, W. S., and E. M. Tory, 1985, “Computer simulation of close random packing of equal
  spheres,” Phys. Rev. A 32, 2347–2351.
Jullien, R., J.-F. Sadoc, and R. Mosseri, 1997, “Packing at random in curved space and frustration:


                                               90
  A numerical study,” J. Physique I 7, 1677–1692.
Kabatiansky, G. A., and V. I. Levenshtein, 1978, “Bounds for packings on a sphere and in space,”
  Problems of Information Transmission 14, 1–17.
Kallus, Y., V. Elser, and S. Gravel, 2010, “A dense periodic packing of tetrahedra with a small
  repeating unit,”, Discrete Comput. Geom. 44, 245–252.
Kamien, R. D., and A. J. Liu, 2007, “Why is Random Close Packing Reproducible?,” Phys. Rev.
  Lett. 99, 155501.
Kansal, A. R., S. Torquato, and F. H. Stillinger, 2002a, “Computer Generation of Dense Polydis-
  perse Sphere Packing,” JCP 117, 8212–8218.
Kansal, A. R., S. Torquato, and F. H. Stillinger, 2002b, “Diversity of Order and Densities in
  Jammed Hard-Particle Packings,” Phys. Rev. E 66, 041109.
Kansal, A. R., T. M. Truskett, and S. Torquato, 2000, “Nonequilibrium Hard-Disk Packings with
  Controlled Orientational Order,” J. Chem. Phys. 113, 4844–4851.
Kerstein, A. R., 1987, “Percolation Model of Polydisperse Composite Solid Propellant Combus-
  tion,” Combust. Flame 69, 95–112.
Levenshtein, V. I., 1979, “On bounds for packings in n-dimensional Euclidean space,” Soviet Math.
  Doklady 20, 417–421.
Likos, C. N., and C. L. Henley, 1993, “Complex alloy phases for binary hard-disk mixtures,” Philos.
  Mag. B 68, 85–113.
Liu, A. J., and S. R. Nagel, 1998, “Jamming is not just cool anymore,” Nature 396, 21–22.
Lubachevsky, B. D., and F. H. Stillinger, 1990, “Geometric Properties of Random Disk Packings,”
  J. Stat. Phys. 60, 561–583.
Lue, L., M. Bishop, and P. A. Whitlock, 2010, “The fluid to solid phase transition of hard hyper-
  spheres in four and five dimensions,” JCP 132, 104509.
Mailman, M., C. F. Schreck, C. S. O’Hern, and B. Chakraborty, 2009, “Jamming in Systems
  Composed of Frictionless Ellipse-Shaped Particles,” Physical Review Letters 102, 255501.
Makse, H. A., and J. Kurchan, 2002, “Testing the thermodynamic approach to granular matter
  with a numerical model of a decisive experiment,” Nature 415, 614–617.
Man, W., A. Donev, F. H. Stillinger, M. Sullivan, W. B. Russel, D. Heeger, S. Inati, S. Torquato,
  and P. M. Chaikin, 2005, “Experiments on Random Packing of Ellipsoids,” Phys. Rev. Lett. 94,
  198001.


                                               91
Mari, R., F. Krzakala, and J. Kurchan, 2008, “Jamming versus Glass Transitions,” Phys. Rev.
  Lett. 103, 025701.
Matérn, B., 1986, “Spatial Variation,” in Lecture Notes in Statistics (Springer-Verlag, New York),
  volume 36, second edition.
Mau, S. C., and D. A. Huse, 1999, “Stacking Entropy of Hard-Sphere Crystals,” Phys. Rev. E 59,
  4396–4401.
Mayer, J. E., and M. G. Mayer, 1940, Statistical Mechanics (John Wiley and Sons, New York).
van Meel, J. A., D. Frenkel, and P. Charbonneau, 2009, “Geometrical frustration: A study of
  four-dimensional hard spheres,” Phys. Rev. E 79, 030201.
Minkowski, H., 1905, “Diskontinuitätsbereich für arithmetische Äquivalenz,” J. reine angew. Math.
  129, 220–274.
Modes, C. D., and R. D. Kamien, 2007, “Hard Discs on the Hyperbolic Plane,” Phys. Rev. Lett.
  99, 235701.
Moukarzel, C. F., 1998, “Isostatic Phase Transition and Instability in Stiff Granular Materials,”
  Phys. Rev. Lett. 81, 1634–1637.
Musin, O. R., 2008, “The kissing number in four dimensions,” Ann. Math. 168, 1–32.
Nisoli, C., N. M. Gabor, P. E. Lammert, J. D. Maynard, and V. H. Crespi, 2010, “Annealing a
  magnetic cactus into phyllotaxis,” Phys. Rev. E 81, 046107.
Noya, E. G., C. Vega, and E. de Miguel, 2008, “Determination of the melting point of hard spheres
  from direct coexistence simulation methods,” J. Chem. Phys. 128, 154507.
Odlyzko, A. M., and N. J. A. Sloane, 1979, “New bounds on the number of unit spheres that can
  touch a unit sphere in n dimensions,” J. Combin. Theory Ser. A 26, 210–214.
O’Hern, C. S., S. A. Langer, A. J. Liu, and S. R. Nagel, 2002, “Random Packings of Frictionless
  Particles,” Phys. Rev. Lett. 88, 075507.
O’Hern, C. S., L. E. Silbert, A. J. Liu, and S. R. Nagel, 2003, “Jamming at zero temperature and
  zero applied stress: The epitome of disorder,” Phys. Rev. E 68, 011306.
Okubo, T., and T. Odagaki, 2004, “Random packing of binary hard discs,” J. Phys.: Cond. Matter
  16, 6651–6659.
Onsager, L., 1944, “Crystal statistics. I. A two-dimensional model with an order-disorder transi-
  tion,” Phys. Rev. 65, 117–149.
Parisi, G., and F. Slanina, 2000, “Toy model for the mean-field theory of hard-sphere liquids,”


                                               92
  Phys. Rev. E 62, 6544–6559.
Parisi, G., and F. Zamponi, 2005, “The ideal glass transition of hard spheres,” J. Chem. Phys.
  123, 144501.
Parisi, G., and F. Zamponi, 2006, “Amorphous packings of hard spheres for large space dimension,”
  J. Stat. Mech. P03017.
Parisi, G., and F. Zamponi, 2010, “Mean field theory of hard sphere glasses and jamming,” Rev.
  Mod. Phys. 82, 789—845.
Peebles, P. J. E., 1993, Principles of Physical Cosmology (Princeton University Press, Princeton).
Pouliquen, O., M. Nicolas, and P. D. Weidman, 1997, “Crystallization of non-Brownian spheres
  under horizontal shaking,” Phys. Rev. Lett. 79, 3640–3643.
Prusinkiewicz, P., and A. Lindenmayer, 1990, The Algorithmic Beauty of Plants (Springer-Verlag,
  New York).
Rahaman, M. N., 1995, Ceramic Processing and Sintering (Marcel Dekker, Inc., New York).
Reatto, L., and G. V. Chester, 1967, “Phonons and the Properties of a Bose System,” Phys. Rev.
  155, 88–100.
Reinhardt, K., 1934, “Über die dichteste gitterfrmige Lagerung kongruente Bereiche in der Ebene
  und eine besondere Art konvexer Kurven,” (Hansischer Universität, Abh. Math. Sem.), 216–230.
Rintoul, M. D., and S. Torquato, 1996a, “Computer Simulations of Dense Hard-Sphere Systems,”
  J. Chem. Phys. 105, 9258–9265 Erratum 107, 2698 (1997).
Rintoul, M. D., and S. Torquato, 1996b, “Metastability and Crystallization in Hard-Sphere Sys-
  tems,” Phys. Rev. Lett. 77, 4198–4201.
Rogers, C. A., 1958, “The Packing of Equal Spheres,” Proc. Lond. Math. Soc. 8, 609–620.
Rogers, C. A., 1964, Packing and Covering (Cambridge University Press, Cambridge).
Rohrmann, R. D., and A. Santos, 2007, “Structure of hard-hypersphere fluids in odd dimensions,”
  Phys. Rev. E 76, 051202.
Roux, J. N., 2000, “Geometric Origin of Mechanical Properties of Granular Materials,” Phys. Rev.
  E 61, 6802–6836.
Ruelle, D., 1999, Statistical Mechanics: Rigorous Results (World Scientific, Riveredge, New Jersey).
Russel, W. B., D. A. Saville, and W. R. Schowalter, 1989, Colloidal Dispersions (Cambridge
  University Press, Cambridge, England).
Salsburg, Z. W., and W. W. Wood, 1962, “Equation of state of classical hard spheres at high


                                               93
  density,” J. Chem. Phys. 37, 798–1025.
Scardicchio, A., F. H. Stillinger, and S. Torquato, 2008, “Estimates of the Optimal Density of
  Sphere Packings in High Dimensions,,” J. Math. Phys. 49, 043301.
Scardicchio, A., C. E. Zachary, and S. Torquato, 2009, “Statistical Properties of Determinantal
  Point Processes in High-Dimensional Euclidean Spaces,” Phys. Rev. E 79, 041108,.
Schaertl, W., and H. Sillescu, 1994, “Brownian dynamics of colloidal hard spheres: Equilibrium
  structures and random close packings,” J. Stat. Phys. 77, 1007–1025.
Scheidegger, A. E., 1974, The Physics of Flow Through Porous Media (University of Toronto Press,
  Toronto, Canada).
Schuette, K., and B. L. van der Waerden, 1951, “Auf welcher Kugel haben 5, 6, 7, 8 oder 9 Punkte
  mit Mindestabstand Eins Platz?,” Math. Ann. 123, 96–124.
Schulz, G. V., 1939, “Über die Kinetik der Kettenpolymerisationen,” Z. Physik Chem. B43, 25–46.
Scott, G. D., and D. M. Kilgour, 1969, “The density of random close packing of spheres,” Brit. J.
  Appl. Phys. 2, 863–866.
Shannon, C. E., 1948, “A Mathematical Theory of Communication,” Bell System Tech. J. 27,
  379–423: 623–656.
Silbert, L. E., D. Ertas, G. S. Grest, T. C. Halsey, and D. Levine, 2002, “Geometry of Frictionless
  and Frictional Sphere Packings,” Phys. Rev. E 65, 031304.
Silbert, L. E., A. J. Liu, and S. R. Nagel, 2005, “Vibrations and Diverging Length Scales Near the
  Unjamming Transition,” Phys. Rev. Lett. 95, 098301.
Skoge, M., A. Donev, F. H. Stillinger, and S. Torquato, 2006, “Packing Hyperspheres in High-
  Dimensional Euclidean Spaces,” Phys. Rev. E 74, 041127.
Song, C., P. Wang, and H. A. Makse, 2008, “A phase diagram for jammed matter,” Nature 453,
  629–632.
Speedy, R. J., 1994, “On the reproducibility of glasses,” J. Chem. Phys. 100, 6684–691.
Stachurski, Z. H., 2003, “Definition and Properties of Ideal Amorphous Solids,” Phys. Rev. Lett.
  90, 155502.
Steinhardt, P. J., D. R. Nelson, and M. Ronchetti, 1983, “Bond-orientational order in liquids and
  glasses,” Phys. Rev. B 28, 784–805.
Stillinger, F. H., E. A. DiMarzio, and R. L. Kornegay, 1964, “Systematic Approach to Explanation
  of the Rigid-Disk Phase Transition,” J. Chem. Phys. 40, 1564–576.


                                               94
Stillinger, F. H., and Z. W. Salsburg, 1969, “Limiting Polytope Geometry for Rigid Rods, Disks,
  and Spheres,” J. Stat. Phys. 1, 179–225.
Stillinger, F. H., S. Torquato, and H. Sakai, 2003, “Lattice-Based Random Jammed Configurations
  for Hard Particles,” Phys. Rev. E 67, 031107.
Tammes, P. M. L., 1930, “On the origin of number and arrangement of the places of exit on the
  surface of pollen-grains,” Recueil des Tavaux Botaniques Nérlandais 27, 1–84.
Tanemura, M., and M. Hasegawa, 1980, “Geometrical models for territory. I. Models for Syn-
  chronous and Asynchronous Settlement of Territories,” J. Theor. Biol. 82, 477–496.
Tobochnik, J., and P. M. Chapin, 1988, “Monte Carlo simulation of hard spheres near random
  closest packing using spherical boundary conditions,” J. Chem. Phys. 88, 5824–5830.
Torquato, S., 1995a, “Mean Nearest-Neighbor Distance in Random Packings of Hard D-
  Dimensional Spheres,” Phys. Rev. Lett. 74, 2156–2159.
Torquato, S., 1995b, “Nearest-Neighbor Statistics for Packings of Hard Spheres and Disks,” Phys.
  Rev. E 51, 3170–3182.
Torquato, S., 2002, Random Heterogeneous Materials: Microstructure and Macroscopic Properties
  (Springer-Verlag, New York).
Torquato, S., 2006, “Necessary Conditions on Realizable Two-Point Correlation Functions of Ran-
  dom Media,” Ind. Eng. Chem. Res. 45, 6293–6298.
Torquato, S., 2009, “Inverse Optimization Techniques for Targeted Self-Assembly,” Soft Matter 5,
  1157–1173.
Torquato, S., A. Donev, and F. H. Stillinger, 2003, “Breakdown of Elasticity Theory for Jammed
  Hard-Particle Packings: Conical Nonlinear Constitutive Theory,” Int. J. Solids Structures 40,
  7143–7153.
Torquato, S., S. Hyun, and A. Donev, 2002, “Multifunctional Composites: Optimizing Microstruc-
  tures for Simultaneous Transport of Heat and Electricity,” Phys. Rev. Lett. 89, 266601.
Torquato, S., and Y. Jiao, 2009a, “Dense Packings of the Platonic and Archimedean Solids,” Nature
  460, 876–881.
Torquato, S., and Y. Jiao, 2009b, “Dense Polyhedral Packings: Platonic and Archimedean Solids,”
  Phys. Rev. E 80, 041104.
Torquato, S., and Y. Jiao, 2010a, “Analytical Constructions of a Family of Dense Tetrahedron
  Packings and the Role of Symmetry,”, arXiv:0912.4210.


                                              95
Torquato, S., and Y. Jiao, 2010b, “Exact Constructions of a Family of Dense Periodic Packings of
  Tetrahedra,” Phys. Rev. E 81, 041310.
Torquato, S., and Y. Jiao, 2010c, “,’Robust Algorithm to Generate a Diverse Class of Dense
  Disordered and Ordered Sphere Packings via Linear Programming’, e-print arXiv:1008.2747.
Torquato, S., A. Scardicchio, and C. E. Zachary, 2008, “Point Processes in Arbitrary Dimension
  from Fermionic Gases, Random Matrix Theory, and Number Theory,” J. Stat. Mech.: Theory
  Exp. P11019.
Torquato, S., and F. H. Stillinger, 2001, “Multiplicity of Generation, Selection, and Classification
  Procedures for Jammed Hard-Particle Packings,” J. Phys. Chem. B 105, 11849–11853.
Torquato, S., and F. H. Stillinger, 2002, “Controlling the Short-Range Order and Packing Densities
  of Many-Particle Systems,” J. Phys. Chem. B 106, 8354–8359 Erratum 106, 11406 (2002).
Torquato, S., and F. H. Stillinger, 2003, “Local Density Fluctuations, Hyperuniform Systems, and
  Order Metrics,” Phys. Rev. E 68, 041113.
Torquato, S., and F. H. Stillinger, 2006a, “Exactly Solvable Disordered Sphere-Packing Model in
  Arbitrary-Dimensional Euclidean Spaces,” Phys. Rev. E 73, 031106.
Torquato, S., and F. H. Stillinger, 2006b, “New Conjectural Lower Bounds on the Optimal Density
  of Sphere Packings,” Experimental Math. 15, 307–331.
Torquato, S., and F. H. Stillinger, 2007, “Toward the Jamming Threshold of Sphere Packings:
  Tunneled Crystals,” J. Appl. Phys. 102, 093511 Erratum, 103, 129902 (2008).
Torquato, S., T. M. Truskett, and P. G. Debenedetti, 2000, “Is Random Close Packing of Spheres
  Well Defined?,” Phys. Rev. Lett. 84, 2064–2067.
Torquato, S., O. U. Uche, and F. H. Stillinger, 2006, “Random Sequential Addition of Hard Spheres
  in High Euclidean Dimensions,” Phys. Rev. E 74, 061308.
Truskett, T. M., S. Torquato, and P. G. Debenedetti, 2000, “Towards a quantification of disorder in
  materials: Distinguishing equilibrium and glassy sphere packings,” Phys. Rev. E 62, 993–1001.
Uche, O. U., F. H. Stillinger, and S. Torquato, 2004, “Concerning Maximal Packing Arrangements
  of Binary Disk Mixtures,” Physica A 342, 428–446.
Uche, O. U., F. H. Stillinger, and S. Torquato, 2006, “On the Realizability of Pair Correlation
  Functions,” Physica A 360, 21–36.
van Meel, J. A., B. Charbonneau, A. Fortini, and P. Charbonneau, 2009, “Hard sphere crystalliza-
  tion gets rarer with increasing dimension,” Phys. Rev. E 80, 061110.


                                               96
Vance, S. I., 2009, Lattices and Sphere Packings in Euclidean Space, Ph.D. thesis, University of
  Washington.
Viot, P., G. Tarjus, and J. Talbot, 1993, “Exact Solution of a Generalizd Ballistic-Deposition
  Model,” Phys. Rev. E 48, 480–488.
Visscher, and M. Bolsterli, 1972, “Random Packing of Equal and Unequal Spheres in Two and
  Three Dimensions,” Nature 239, 504–507.
Weeks, J. D., D. Chandler, and H. C. Andersen, 1971, “Role of Repulsive Forces in Determining
  the Equilibrium Structure of Simple Liquids,” J. Chem. Phys. 54, 5237–5247.
Widom, B., 1966, “Random Sequential Addition of Hard Spheres to a Volume,” J. Chem. Phys.
  44, 3888–3894.
Williams, S. R., and A. P. Philipse, 2003, “Random packings of spheres and spherocylinders sim-
  ulated by mechanical contraction,” Phys. Rev. E 67, 051301.
Woodcock, L. V., and C. A. Angell, 1981, “Diffusivity of the Hard-Sphere Model in the Region of
  Fluid Metastability,” Phys. Rev. Lett. 47, 1129–1132.
Wyart, M., L. E. Silbert, S. R. Nagel, and T. A. Witten, 2005, “Effects of compression on the
  vibrational modes of marginally jammed solids,” Phys. Rev. E 72, 051306.
Yatsenko, G., and K. S. Schweizer, 2008, “Glassy dynamics and kinetic vitrification of isotropic
  suspensions of hard rods.,” Langmuir 24, 7474–7484.
Zachary, C. E., Y. Jiao, and S. Torquato, 2010, “ Hyperuniform Long-Range Correlations are a
  Signature of Disordered Jammed Hard-Particle Packings.,”, e-print arXiv:1008.2548.
Zachary, C. E., and S. Torquato, 2009, “Hyperuniformity in point patterns and two-phase hetero-
  geneous media,” J. Stat. Mech.: Theory & Exp. P12015.
Zallen, R., 1983, The Physics of Amorphous Solids (Wiley, New York).
Zandi, R., D. Reguera, R. F. Bruinsma, W. M. Gelbart, and J. Rudnick, 2004, “Origin of icosahe-
  dral symmetry in viruses,” Proc. Nat. Acad. Sci. 101, 15556–15560.
Zeravcic, Z., N. Xu, A. J. Liu, S. R. Nagel, and W. van Saarloos, 2009, “Excitations of Ellipsoid
  Packings near Jamming,” Euro. Phys. Lett. 87, 26001.
Zinchenko, A. Z., 1994, “Algorithm for Random Close Packing of Spheres with Periodic Boundary
  Conditions,” J. Comput. Phys. 114, 298–307.




                                              97
