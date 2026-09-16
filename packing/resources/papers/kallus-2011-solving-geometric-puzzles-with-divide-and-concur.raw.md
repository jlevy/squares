SOLVING GEOMETRIC PUZZLES WITH DIVIDE
            AND CONCUR




                          A Dissertation
         Presented to the Faculty of the Graduate School

                       of Cornell University
    in Partial Fulfillment of the Requirements for the Degree of
                       Doctor of Philosophy




                                by
                           Yoav Kallus
                           August 2011
  c 2011 Yoav Kallus

ALL RIGHTS RESERVED
        SOLVING GEOMETRIC PUZZLES WITH DIVIDE AND CONCUR
                                  Yoav Kallus, Ph.D.
                                Cornell University 2011



In this dissertation we discuss a variety of geometric constraint satisfaction problems.
The greatest part of the discussion is devoted to infinite packing problems, where the
packing arrangement of an infinite number of congruent copies of an object with the

greatest density is sought. We develop a general method, based on the Divide and Con-
cur scheme, for discovering dense periodic packings of any convex object. We use this
method to improve on the previous greatest known packing density of regular tetrahe-
dra. We then generalize the discussion of regular tetrahedra to a one-parameter family

of shapes interpolating between the regular tetrahedron and the sphere. We investigate
how the likely optimal packing changes as the shape is changed and what continuous
and abrupt transitions arise. We also use the method to reproduce the densest known lat-
tice sphere packings and the best known lattice kissing arrangements in up to 14 and 11

dimensions respectively – the first such numerical evidence for their optimality in some
of these dimensions. We then shift our discussion to the inverse problem of inferring the
structure of biomolecules from a set of structural restraints derived from nuclear mag-
netic resonance experiments. We describe a constraint-based approach which avoids

the minimization of a cost/energy function and use it to reconstruct the structure of a
beta-amyloid fibril formed by a 40-amino-acid peptide associated with Alzheimer’s dis-
ease based on restraints published in the literature. Finally, we study a simple model
of rippling in a two-dimensional atomic sheet due to bond length heterogeneity. We

describe a form of dislocations which is not present in a homogeneous crystal and use a
relationship between the dislocation density and the Gaussian curvature to characterize
the relaxed conformation of the sheet. We find a relationship between this conformation
and a surface in an abstract space associated with the combinatorial aspect of the bond
length heterogeneity.
                             BIOGRAPHICAL SKETCH


Yoav Kallus was born in Haifa, Israel in 1986. A classic faculty brat, thanks to his
professorial mother, he began sitting in on math courses at the Israeli Institute of Tech-
nology in Haifa (Technion) at age 15. The next year, moving with his family to Berkeley,

California for his mother’s sabbatical year, he stopped attending high school and began
taking classes at the University of California full time. He continued in Berkeley for
another year after his mother went back to teach in Haifa, but transferred to Rice Uni-
versity the following year, where in 2006 he earned a BSc in physics. Yoav then went on

to seek a PhD in physics from Cornell University, where he worked under the advising
of Veit Elser from 2007. He earned an MSc in 2010 and a PhD in 2011. Yoav expects to
be a post-doctoral fellow with the Princeton Center for Theoretical Sciences from 2011
to 2014.




                                           iii
To my parents.




      iv
                             ACKNOWLEDGEMENTS


   I first thank my adviser, Veit Elser, who has guided and supervised all the work
presented. He has been remarkably devoted and enthusiastic in filling his advisory role,
and virtuosic in his artfully minimalist application of motivational stimuli. While this

dissertation marks the end of our formal attachment as student and adviser, I will surely
keep seeking out his advice for years to come.
   I shared this incredible adviser with an equally incredible group of lab mates. Simon
Gravel, Duane Loh, Kartik Ayyer, Diarmuid Cahalane, and Zhen Wah Tan have all made

working in the Elser group an incredible academic experience. I have my lab mates to
thank for contributions to many of the ideas presented in this dissertation. Beside my
lab mates and my adviser, others have been useful sources of insight and background
to the material discussed in this dissertation, and I acknowledge useful conversations

with Henry Cohn, Bob Connelly, Michael Engel, Sharon Glotzer, Chris Henley, Erich
Mueller, Ricky Pollack, Sal Torquato, James Sethna, and Rob Thorne. The last two
deserve special mention for serving on my special committee with Veit Elser and facil-
itating my degree candidacy and dissertation defense examinations. I should not forget

to cite my brother Nathan Kallus in this context for the useful conversations I have
had with him. There are other colleagues at Cornell whom I must thank for constantly
sharing their ideas with me and critically hearing out my own: Srivatsan Chakram, Joe
Chen, Bryan Daniels, Phil Kidd, Johannes Lischner, Ben Machta, Stefan Natu, Tim

Novikoff, Stefanos Papanikolaou, Frank Petruzielo, Sumiran Pujari, Tristan Rocheleau,
Mark Transtrum, and Arend van der Zande. I also thank the administrative and techni-
cal staffs of the Department of Physics, the Cornell Center for Materials Research, the
Laboratory of Atomic and Solid State Physics, and the Graduate School.

   To my parents, my sister, and my brother, I owe thanks for providing a moving home
to escape to from Ithaca.


                                           v
   Finally, my time as a graduate student would not have been as enjoyable without the
great people of Ithaca and Cornell: my house mates over the years, my office mates, my
friends, and, of course, my wonderful girlfriend Alisa.




                                           vi
                               TABLE OF CONTENTS
   Biographical Sketch . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     iii
   Dedication . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     iv
   Acknowledgements . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          v
   Table of Contents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     vii
   List of Tables . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     ix
   List of Figures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     x

1 Introduction                                                                            1
  1.1 Geometric Puzzles . . . . . . . . . . . . . . . . . . . . . . . . . . . .           1
       1.1.1 Packing problems . . . . . . . . . . . . . . . . . . . . . . . . .           2
       1.1.2 Distance Geometry . . . . . . . . . . . . . . . . . . . . . . . .            4
  1.2 The difference map . . . . . . . . . . . . . . . . . . . . . . . . . . . .          6
  1.3 Random walk reconstruction . . . . . . . . . . . . . . . . . . . . . . .            7
       1.3.1 Background . . . . . . . . . . . . . . . . . . . . . . . . . . . .           7
       1.3.2 Divide and Concur . . . . . . . . . . . . . . . . . . . . . . . .            8
       1.3.3 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         10
  1.4 Conclusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         13

2 Dense periodic packings of tetrahedra with small repeating units                       14
  2.1 Abstract . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       14
  2.2 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       14
  2.3 One-parameter family of dimer-double-lattice packings . . . . . . . . .            15
  2.4 Simple double-lattice packing . . . . . . . . . . . . . . . . . . . . . .          21
  2.5 Discussion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       22

3 A method for dense packing discovery                                                   24
  3.1 Abstract . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       24
  3.2 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       25
  3.3 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       30
      3.3.1 The D − C scheme . . . . . . . . . . . . . . . . . . . . . . . .             30
      3.3.2 The difference map . . . . . . . . . . . . . . . . . . . . . . . .           35
  3.4 Constraints . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        37
      3.4.1 Periodic sphere packing and kissing . . . . . . . . . . . . . . .            37
      3.4.2 Convex polytope packing . . . . . . . . . . . . . . . . . . . . .            41
  3.5 Implementation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         44
      3.5.1 “Divide” projections . . . . . . . . . . . . . . . . . . . . . . .           44
      3.5.2 “Concur” projections . . . . . . . . . . . . . . . . . . . . . . .           49
      3.5.3 Formal configuration space maintenance . . . . . . . . . . . . .             53
  3.6 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      56
      3.6.1 Sphere packing . . . . . . . . . . . . . . . . . . . . . . . . . .           56
      3.6.2 Kissing number . . . . . . . . . . . . . . . . . . . . . . . . . .           57
      3.6.3 Polytope packing . . . . . . . . . . . . . . . . . . . . . . . . .           58
  3.7 Conclusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         61


                                           vii
4 Dense packing crystal structures of physical tetrahedra                             64
  4.1 Abstract . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    64
  4.2 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    64
  4.3 Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     66
  4.4 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   69
  4.5 Discussion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    72

5 Constraint-based method for structure determination                                 75
  5.1 Abstract . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    75
  5.2 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    75
  5.3 Constraint-based approach . . . . . . . . . . . . . . . . . . . . . . . .       78
      5.3.1 Data restraints . . . . . . . . . . . . . . . . . . . . . . . . . .       78
      5.3.2 Local physical restraints . . . . . . . . . . . . . . . . . . . . .       79
      5.3.3 Non-local physical restraints . . . . . . . . . . . . . . . . . . .       81
      5.3.4 Divide and Concur . . . . . . . . . . . . . . . . . . . . . . . .         82
  5.4 Implementation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      85
      5.4.1 The divide constraint . . . . . . . . . . . . . . . . . . . . . . .       85
      5.4.2 Distance bound restraints . . . . . . . . . . . . . . . . . . . . .       86
      5.4.3 Rigid unit restraints . . . . . . . . . . . . . . . . . . . . . . . .     86
      5.4.4 Torsion angle restraints . . . . . . . . . . . . . . . . . . . . . .      87
      5.4.5 The concur constraint . . . . . . . . . . . . . . . . . . . . . .         88
      5.4.6 Non-local energy bound . . . . . . . . . . . . . . . . . . . . .          88
  5.5 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   90
  5.6 Discussion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    93

6 Conformations of a graphene-like sheet with heterogeneity in bond lengths 97
  6.1 Abstract . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 97
  6.2 Bond length heterogeneity in an atomic sheet . . . . . . . . . . . . . . 97
  6.3 Fractional dislocations in a six-fold two-dimensional crystal . . . . . . 98
  6.4 Random tilings, projection, and the phason dimension . . . . . . . . . . 100
  6.5 A relationship between two apparently disparate surfaces . . . . . . . . 102

Bibliography                                                                          107




                                          viii
                               LIST OF TABLES

2.1   The construction of the dimer-double-lattice family of packings. . . . 16
2.2   The construction of the simple-double-lattice packing in a general tri-
      clinic coordinate basis. . . . . . . . . . . . . . . . . . . . . . . . . . . 21
2.3   Some studied transitive and non-transitive packings of regular tetrahedra 22

3.1   A summary of the D − C constraints for periodic sphere packing, the
      average kissing number problem, and polytope packing. . . . . . . . .            44
3.2   Results of PDC searches for dense lattice packing in dimensions d =
      2, . . . 14. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   57
3.3   Results of PDC searches for lattice packing with high kissing number
      in dimensions d = 2, . . . 11. . . . . . . . . . . . . . . . . . . . . . . .     58
3.4   Coordinates of the densest pentatope packing discovered by the PDC
      search. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      61

5.1   Root-mean-square errors in four models of the amyloid fibril produced
      by the constraint based method and four models produced by a tradi-
      tional method . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      92
5.2   Root-mean-square deviations between different models of the amyloid
      fibril. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    92




                                         ix
                              LIST OF FIGURES
1.1   Reconstructions of a random walk with N = 16000 steps based on
      M = 1600, M = 2400, M = 5200, and M = 8000 non-local distance
      constraints. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    11
1.2   The mean RMSD in an ensemble of solutions to the random walk re-
      construction problem in the underconstrained region, averaged over ten
      random realizations for each value of N and M . . . . . . . . . . . . .         12

2.1   Small portions of one layer and three stacked layers in the dimer-
      double-lattice packing. . . . . . . . . . . . . . . . . . . . . . . . . . .     18
2.2   The contacts on the surface of a dimer in the dimer-double lattice pack-
      ing shown on a net diagram. . . . . . . . . . . . . . . . . . . . . . . .       20
2.3   Small portions of one layer and three stacked layers in the simple-
      double-lattice packing. . . . . . . . . . . . . . . . . . . . . . . . . . .     20

3.1   An illustration of the D − C scheme in the case of packing three disks
      into a square box. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    32
3.2   An illustration of the “divide” and “concur” projections in the two-
      dimensional periodic sphere packing problem with p = 3. . . . . . . .           41
3.3   An illustration of the polytope exclusion and rigidity constraint projec-
      tions for the case of regular pentagons. . . . . . . . . . . . . . . . . .      45
3.4   The course of a sample run searching for dense periodic packings (p =
      4) of unit edge-length regular tetrahedra. . . . . . . . . . . . . . . . .      59
3.5   Lower dimensional cuts through dense packings of tetrahedra and pen-
      tatopes. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    60

4.1   Tetrahedral puffs of varying asphericity. . . . . . . . . . . . . . . . . .     66
4.2   A unit cell of each of the four structures described, (from left to right)
      the S0 -, D1 -, S1 -, and D0 -structures. . . . . . . . . . . . . . . . . . .   70
4.3   Highest densities φ achieved for packings of tetrahedral puffs of varying
      asphericity γ. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    71

5.1   An aspargine residue partitioned into maximal rigid units. . . . . . . .        81
5.2   The distribution of errors in the lowest error model of the amyloid fibril
      constructed in this work and a representative model constructed by a
      traditional method after a relaxation run. . . . . . . . . . . . . . . . .      93
5.3   Backbone traces of a model of the amyloid fibril constructed in this
      work and a representative model constructed by a traditional method
      after a relaxation run. . . . . . . . . . . . . . . . . . . . . . . . . . . .   94

6.1   The five patterns of single and double bonds in a 6-cycle of the honey-
      comb lattice that are allowed in a Kekulé structure. . . . . . . . . . . . 99
6.2   Correspondence of a Kekulé structure to a tiling by decorated rhombi. . 101
6.3   Correspondence of a Kekulé structure to the projection of a three di-
      mensional surface. . . . . . . . . . . . . . . . . . . . . . . . . . . . . 101


                                         x
6.4   The five possible arrangements of rhombi around a vertex of the tiling. 103
6.5   The Gaussian curvature in the manifold traced out by the bond net-
      work in equilibrium can be shown, by direct enumeration of local ar-
      rangements, to be proportional to the Gaussian curvature of the surface
      whose projection gives the rhombus tiling corresponding to the Kekulé
      structure. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 104
6.6   Two ordered Kekulé structures which demonstrate the relationship be-
      tween positive or negative Gaussian curvature in the surface whose pro-
      jection is the corresponding tiling and in the manifold traced out by the
      bond network in equilibrium. . . . . . . . . . . . . . . . . . . . . . . 105




                                       xi
                                       CHAPTER 1
                                   INTRODUCTION



1.1 Geometric Puzzles


The problems we address in this dissertation, covering work done in the Laboratory

of Atomic and Solid State Physics between 2007 and 2011, are problems of geometric
constraint satisfaction. Though in each of the following chapters we present a relatively
isolated discussion of a specific problem and the results we find in our investigation of it,
the central theme connecting all the chapters is that they deal with geometric problems

of constraint satisfaction. Additionally, in all but the last chapter we use the Divide and
Concur scheme as a numerical method of discovering solutions. In this introduction
we will discuss these two shared aspects, reviewing first some of the many contexts
in which geometric constraint satisfaction problems arise and then some of the many

considerations which arise when attempting to solve such problems using the Divide
and Concur scheme.


   Many geometric constraint satisfaction problems take the form of puzzles: the prob-
lem consists of individual pieces which need to be arranged in space according to some
rules. Putting all the pieces together in such a way that is consistent with all the rules
yields a solution. In a physical setting, such problems usually arise in one of two ways:

as a direct problem or as an inverse problem. If we have a model of how the microscopic
elements in a system interact, and wish to know what collective structure is consistent
with such interactions, we arrive at a direct type of constraint satisfaction problem where
the structure is the physical result of the constraints. If we wish to study a structure,

which cannot be observed directly, by utilizing a number of indirect observations, we
arrive at an inverse type of constraint satisfaction problem, where the constraints are the


                                             1
physical result of the structure.


   Formally, we can describe constraint satisfaction problems using a factor graph. The
factor graph is a bipartite graph, with one set of nodes A identified with the elements of
the puzzle, another set of nodes B associated with constraints, and edges E connecting
constraints to the elements they constrain. A configuration is a possible way of laying

out the elements, namely an assignment to each element a point in layout space: y : A →
Ω. A configuration satisfies constraint b ∈ B if its restriction to Ab , the set of elements
                                                      
it is connected to, satisfies some condition fb y|Ab = 0. The constraint satisfaction
problem is then to find an assignment which simultaneously satisfies all the constraints

B. Though each constraint individually might be simple to satisfy, they are hard to
satisfy simultaneously because multiple constraints involve the same variable (i.e. they
are dependent). Below are some examples of geometric constraint satisfaction problems.




1.1.1 Packing problems


Packing problems might be the simplest and most versatile family of geometric puzzles.

In a finite packing problem, we are given a number of solids and we must lay them out
in some box so that there are no overlaps between elements. For example, we might be
asked to pack N unit disks into a square box of side a. A common problem of interest is
to find the largest density possible for some particular type of packing. In the previous

example, that would mean finding for a given N the smallest side length a for which
a packing is possible [65]. We can also consider the problem of packing an infinite
number of unit spheres with the greatest density possible [34]. If we wish to avoid a
box with boundaries, but still to consider finite packings, we can consider packings on a

compact manifold. For example, the problem of packing spherical caps on an n-sphere



                                             2
is known as the problem of spherical codes [16].


   Spheres have only translational degrees of freedom, so the layout space becomes
more complicated when we consider non-spherical objects. For example, in Chapter 2,
we consider the problem of packing an infinite number of regular tetrahedra and discover
a packing with greater density than any packing previously known. In Chapter 4, we

generalize our discussion to a one-parameter family of shapes interpolating between
the regular tetrahedron and the sphere. We investigate how the likely optimal packing
changes as the shape is changed and what continuous and abrupt transitions arise.


   Soft objects may be used instead of hard objects. Soft objects are ones that are
allowed to either overlap with each other or deform at some energetic cost. In soft
packing problems, we might ask how a finite number of these soft objects may be packed

into a given box (or an infinite number at some given density) with the smallest energy
(resp. energy density) possible.


   Another interesting variation on the infinite packing problem is to limit the type of
arrangements allowed. For example, we can ask for the greatest density possible if we
restrict ourselves to lattice packings of some object, where the packing is generated

from a single object by the action of a group of translations (i.e. a Bravais lattice). In
many cases the answer is the same as for the unrestricted problem: for example, for all
convex, centrally-symmetric, two-dimensional objects, and for spheres in up to three
dimension and probably also other low dimensions [4, 34, 16]. One of the problems

considered in Chapter 3 is the problem of lattice sphere packings in up to 14 dimensions.
We successfully reproduce in that chapter the densest lattice packings known in each
dimension, a result which has not been achieved previously by an unbiased numerical
search.




                                            3
   It is worth noting that although packing is very well-suited to this constraint-based
formulation, some equally basic and versatile families of problems are not. Notably,
the covering problem and the quantizer problem [16] do not have natural formulations
in terms of constraint satisfaction problems. It is possible, if unnatural and cumber-

some, to formulate these problems as soft packing problems with a series of two-body
interactions, three-body interactions, four-body interactions, and so on [67].




1.1.2 Distance Geometry


Another wide family of geometric puzzles are distance geometry problems. In distance
geometry problems we attempt to determined a structure, represented by a number of

points, based on some knowledge about the distances between the points. For example,
we might be given a list of data of the form “the distance between point i and point
j is d”, and asked to determine a structure that is consistent with this data. Unless
we are given the absolute positions of some of the points, we can only determine the

structure up to rotations, reflections, and translations. Of course, depending on whether
the list of distances is consistent and underconstrained, consistent and overconstrained,
or inconsistent, the problem might have, respectively, many, one, or no solutions. In

Section 1.3, we study the ensemble of solutions in the underconstrained regime of the
problem of random walk reconstruction, where we attempt to reconstruct a random walk
based on a partial list of distances.


   In some problems, we are not given the distances exactly. This can happen due to
noise in the measurement of the distance (in an inverse problem), or because the distance
is flexible (in a direct problem). In either case, what we have is a soft distance geometry

problem, where we must minimize a cost function that is written in terms of the dis-



                                            4
tances. The inverse version of the soft distance geometry problem occurs for example
in network localization [5], where nodes in a network measure their spatial distances to
neighboring nodes (with some noise), and we try to reconstruct the spatial location of the
nodes based on the measurements. The direct version occurs when we have a network

of atoms connected by bonds of various types, and we wish to determine the equilib-
rium conformation of the network. In Chapter 6 we consider a theoretical version of
such a network, inspired by graphene. We consider a network of atoms connected with
bonds as in the honeycomb lattice, except that instead of all bonds being identical, our

network has two types of bonds (say, single and double bonds) with different relaxed
lengths. We discover an interesting relationship between the relaxed conformation such
a sheet takes when allowed to relax in three-dimensional space and an abstract surface
associated with the combinatorics of possible assignments of single and double bonds.


   Some geometrical puzzles combine many types of constraints. For example, the

biomolecular structure determination problem, considered in Chapter 5, combines as-
pects of soft distance geometry, hard distance geometry, and soft packing. More im-
portantly, it combines aspects of direct and inverse problems: some of the constraints
on the structure come from the underlying physical and chemical interactions, while

others are derived from nuclear magnetic resonance spectroscopy. In Chapter 5, we
develop a framework for biomolecular structure determination using the Divide and
Concur scheme and use it to reconstruct the structure of a beta-amyloid fibril formed
by a peptide associated with Alzheimer’s disease [58]. The rigid unit constraint, to be

introduced in Chapter 5, is simply a more efficient way of combining many distance
constraints.




                                            5
1.2 The difference map


Some constraint satisfaction problems possess a special structure where the set of con-
straints B can be partitioned into two sets B1 and B2 such that each set is easy to satisfy
on its own and in fact allows the projection to the set of satisfying configurations to be
computed efficiently. The projection map P1 (resp. P2 ) is a map in the space of con-

figurations, taking any configuration y to the nearest configuration (according to some
appropriate metric) that satisfies all the constraints in B1 (resp. B2 ). This map is a
projection, in the geometric sense, to the set {y|y satisfies B1 }, or briefly a projection to
B1 . In these cases, the difference map becomes a useful tool for discovering solutions.

Specifically, if B1 consists of independent constraints (involving distinct sets of vari-
ables), which are easy to satisfy (in the sense of allowing an efficient projection), then
B1 would also be easy to satisfy.


   Assuming the configuration space is an affine space, we can construct the difference
map as an iterated map in configuration space out of projections and affine combinations:

                     yn+1 = DM(yn ) = yn + β(P1 ( f2 (yn )) − P2 ( f1 (yn )))           (1.1)

                                fi (yn ) = (1 + γi )Pi (yn ) − γi yn ,                  (1.2)

where γ1 = −1/β and γ2 = 1/β. The benefits of using the difference map as a search
dynamic in configuration space are manifold, but are not the focus of the discussion
here. More details about the workings of the difference map can be found elsewhere
[29, 30, 23, 20]. It suffices to mention that the map is computationally simple, that all

its fixed points correspond to solutions, fixed points are attractive, and the dynamics of
the iteration are such that fixed points are usually rapidly discovered.


   In problems where the assumptions above do not hold, we can use the Divide and
Concur scheme to convert the problem into one on which the difference map can nev-


                                                  6
ertheless be used. It is possible to give a general recipe for how to apply the scheme,
which is universally well defined. However, such a recipe does not capture the flexibility
of the scheme and subtleties of how it is used in practice. Therefore, we prefer to give
an example of its application, noting where variations might occur.




1.3 Random walk reconstruction



1.3.1 Background


The problem we consider is an instance of the (hard) distance geometry problem. We
define a random realization of this problem by generating a three-dimensional random
walk y1 , y2 , . . . yN ∈ R3 , where ||yi − yi+1 || = 1. Then, we randomly sample M distances
from the set of non-fixed distances. The distances we will use to reconstruct the random

walk are the N − 1 step lengths and the M sampled distances. We use a random walk
instead of independently distributed points so that the graph of distances is guaranteed to
be connected. More importantly, this is a nice toy model for the biomolecular structure
determination problem discussed in Chapter 5, where the chemical bonding along the

chain gives local constraints and nuclear Overhauser effect spectroscopy gives non-local
constraints.


    A typical consideration in constraint satisfaction inverse problems is the transition,
as more constraints are introduced, between an underconstrained problem with multiple
solutions and an overconstrained problem with a unique solution (the designed solution).
Much work has been done to study this transition in discrete problems such as 3SAT,

where the transition between underconstraint and overconstraint in the thermodynamic
limit occurs at a certain ratio of constraints to variables [55, 56]. At a lower ratio still, in


                                               7
the underconstrained regime, typical solutions start to resemble to a greater and greater
degree the design solution. Namely, the space of solutions acquires an extensive back-
bone – a finite fraction of the variables in the thermodynamic limit take a fixed value in
all solutions [56, 76].


   In continuous problems, a simple Maxwellian constraint counting usually predicts

the transition between underconstraint to overconstraint [11, 42]. The growth of resem-
blance of a typical solution to the design solution in the underconstrained regime is our
interest here. A measure of how well a reconstructed walk matches the original walk
is the root-mean-square deviation (RMSD), which is the root-mean-square distance be-

tween the two point configurations after rotations and translations have been applied to
one to minimize this distance. Here we attempt to quantify the RMSD between recon-
structed solutions and the original walk as a function of N and M.




1.3.2 Divide and Concur


Since the set of M ′ = M+N −1 constraints in this problem cannot be partitioned into two

sets which are each easy to satisfy individually, we use the Divide and Concur scheme
to make the constraints independent from each other at the expense of introducing a
new set of constraints, which will also be independent from each other. We do this by
considering replica configurations instead of configurations. Recalling the factor graph,

where A is the set of configuration elements (here points), B is the set of constraints (here
prescribed distances), and E is the set of edges in the graph (here connecting a distance
constraint to the two points defining the distance), configurations are maps y : A → Ω,
where Ω = R3 is our layout space in this problem. A replica configuration shall be a map

x : E → Ω, where each edge is assigned a point in the layout space. Since many edges



                                             8
are incident on each element in A, in a replica configuration each element is represented
by multiple replicas that may all be laid out differently. A constraint b ∈ B is said to
be satisfied in a replica configuration if it is satisfied by the replicas on the edges E b
                       
incident on it: fb x|Eb = 0. Thus, the constraints of set B are rendered independent.


   We reinterpret the set A as another set of constraints. Namely, we interpret each node

in A as an equality constraint between all the layout assignments on the edges incident
on it. A replication map takes any configuration into a replica configuration by letting
R(y)(e) = y(a) if e ∈ E a , the set of edges incident on a. Thus, any replica configuration
satisfying the constraints A is in the range of R and can be mapped to a configuration

y = R−1 (x). If a replica configuration satisfies both A and B, it is the replication image
of a configuration satisfying B, and is thus a solution.


   In the present problem, since the layout space is affine, our replica configuration
space is automatically also an affine space and we can use the projections to A and B in
the difference map to find solutions. If the layout space is not affine, as when packing
disks in a square or when packing spherical caps on the surface of a sphere, we must

modify the constraints associated with set A. If the layout space is not already embedded
in an affine space, we must embed it as Ω ⊆ Rd and define replica configurations as maps
x : E → Rd . Then, in addition to requiring a unique assignment to all edges incident
on a ∈ A, we must also require that assignment to lie on Ω. This modification does not

usually make the projection much harder to compute.


   In some cases, the replication map used above to construct replica configurations
results in an unnecessarily high-dimensional configuration space. The important prop-
erties of R are that it renders all the constraints B independent, and that we can project
with ease to its range. The particular form of R given above is a simple one, that works

in general, but there is no particular reason to be restricted to it in any particular prob-



                                             9
lem. In general, it is often useful and more economical to construct our replication map
so that no extraneous replica variables are created. We wish to create enough replica
variables so that each constraint is independent, but no more. Therefore, it is usually de-
sirable that for each constraint, the replica configuration space includes as few variables

as possible, while keeping projections to the constraint and inversion of the replication
computationally simple. In Chapters 3 and 4, where we consider periodic packings, we
avoid creating extraneous replicas of the unit vectors defining the periodicity by adding
them directly into the relevant replicas.




1.3.3 Results


For each value of the parameters N and M we construct 10 random realizations of the
random walk reconstruction problem. We then use 100 runs of the difference map from
random initial conditions to obtain an ensemble of solutions. We consider configurations
where the root-mean-square deviation from the prescribed distances does not exceed

10−14 to be solutions. Figure 1.1 presents sample reconstructions of a random walk
based on different numbers of constraints.


   In Figure 1.2 we give the expected value (averaged over random realizations) of the
mean (averaged over the ensemble) RMSD. We observe that the data collapses nicely
when the axes are rescaled by appropriate powers of the length of the walk. That the

RMSD should scale as N 1/2 is an intuitive result, at least for M = 0. A less intuitive
result is that the relevant number of distance constraints also scales as M ∼ N β with
β ≈ 0.5.


   A simple way to interpret these results are in terms of the following scaling argument
for a lower bound on the RMSD when M ≪ N: imagine that the positions of all points


                                             10
Figure 1.1: Reconstructions of a random walk with N = 16000 steps based on
            M = 1600 (top left), M = 2400 (top right), M = 5200 (bottom left),
           and M = 8000 (bottom right) non-local distance constraints. The
           original walk is shown in black, and the reconstruction is shown in
           red.




                                     11
               RMSD
                    ô
                    ò

               15ì ô
                        ò
                        ì
                            ô
                    à       ò
                            ì
                        à       ò
                                ì
                                ô
               10           à       ì
                                    ò
                    æ
                        æ       à   ô ì
                                      ò
                            æ       à   ì
                                æ     à ò ì
                                    æ ô
                                      æ à ò
                                          à ì
                                        ô
                                        æ æ ò
                                            à ì
                                              à ì
                                          ô æ æ
                                              ò à à
                5                           ô   ò ì
                                                æ æ       à à
                                                          ì
                                                          æ ì
                                              ô   ò           à æ
                                                ô ô       ò æ æ
                                                              ì à æ
                                                                  à æ
                                                                ì ì à æ
                                                          ô ò
                                                            ô ò
                                                              ô ò
                                                                      à æ
                                                                    ì ì à à
                                                                ô ò
                                                                  ô ò ô ì
                                                                    ô ò ô ì
                                                                        ò ò
                                                                          ô
                                                                                        M N
                                    0.2        0.3        0.4         0.5         0.6

                     RMSD  N Β
                      0.25
                              æ
                                æ
                                 æ
                                 à
                      0.20         æ
                                   àì
                                    æ
                                     àæì
                                       æ
                                       àæ
                      0.15                ì
                                         òæ
                                         à æì
                                           à
                                             æ
                                             òæàì
                                             à
          æ         1000                        æôæ
                                                  àì
                      0.10                        òæ  ì
                                                    àæà
                                                      òôæàìà
                                                      æ
                                                          ææ
                                                           òìàôàò
           à        2000                                        ìàì
                                                                  òàìò
                                                                  à
                                                                  ô  àì
                                                                      à ò ò
                      0.05                                            ôàì ìô ì ì
                                                                               òô ìòì
          ì         4000                                                             ôòì

                      0.00                                                                   M N Α
          ò         8000 0                10            20             30               40

          ô 16000




Figure 1.2: The mean RMSD in an ensemble of solutions to the random walk
           reconstruction problem in the underconstrained region, averaged over
           ten random realizations for each value of N and M (top). We scale
           the axes so as to collapse the data on a single curve (bottom). We use
           α = 0.51 and β = 0.53, although a large range of exponents gives an
           equally visually pleasing collapse.




                                                     12
participating in a distance constraint were correctly identified – we can hope for no
more information than this from the constraints – then the M + 1 segments between
constrained points, each of approximately N/M steps, would be free chains fixed only
at their end points. If the solutions were sampled uniformly from all configurations

where the constrained points were at their original positions, then the RMSD would go
as (N/M)1/2 due to the typical extent of a random walk with fixed ends. This would
mean that RMSD/N 1/2 would vary with M, not M/N 1/2 as we find. The fact that we
find the latter suggests that the solutions are not sampled uniformly and that the free

segments more resemble extended chains than a random walk. If we assume extended
chains, with a typical extent linear with the number of steps – our lower bound gives that
the RMSD should go as N/M, and therefore RMSD/N 1/2 goes as function of M/N 1/2 as
observed. The non-uniform sampling of the solution space is a property of the particular

algorithm used. In fact, this behavior should be expected because the algorithm would
quit upon reaching the solution space, yielding a structure on its boundary and not in its
interior.




1.4 Conclusion


From the discussion above, we see that applying the Divide and Concur scheme is not
achieved simply by following a recipe. Apart from the considerations described above
– the embedding of the layout space in an affine space and the choice of an appropriate
replication map – there are others – such as optimization of the β parameter and dynamic

assignment of metric weights – which are discussed elsewhere [29, 30, 20]. In the
subsequent chapters we apply the Divide and Concur scheme to the study of a variety of
problems of physical and mathematical interest as discussed earlier in the introduction.




                                           13
                                       CHAPTER 2
      DENSE PERIODIC PACKINGS OF TETRAHEDRA WITH SMALL
                                 REPEATING UNITS



   The contents of this chapter have been published in Discrete and Computational
Geometry with coauthors Veit Elser and Simon Gravel [46].



2.1 Abstract


We present a one-parameter family of periodic packings of regular tetrahedra, with the
packing fraction 100/117 ≈ 0.8547, that are simple in the sense that they are transitive
and their repeating units involve only four tetrahedra. The construction of the packings
was inspired from results of a numerical search that yielded a similar packing. We

present an analytic construction of the packings and a description of their properties. We
also present a transitive packing with a repeating unit of two etrahedra and a packing
              √
fraction 139+40
            369
                10
                   ≈ 0.7194.




2.2 Introduction


The optimization problem of packing regular tetrahedra densely in space has seen invig-
orated interest over the last few years [17, 12, 69, 68, 33]. This interest has helped drive
up the packing fraction of the densest-known such packings from 0.7174 in 2006 [17] to
0.8503 [33] most recently (see Table 2.3). These improved packing fractions have been

obtained from more and more complex packings, with larger and larger repeating units.
This trend has led some to conjecture that the densest packing of tetrahedra might have
inherent disorder [68]. The more restrictive problem of packing tetrahedra transitively


                                            14
— that is, so that all tetrahedra in the packing are equivalent (a more rigorous definition
is given below) — has been less extensively studied and the densest previously-reported
transitive packing of regular tetrahedra fills only 2/3 of space [17]. Here we present
a one-parameter family of transitive but dense packings of tetrahedra with the packing

fraction 100/117 ≈ 0.8547.


   The discovery of this family of dense packings was inspired by the results of a nu-
merical search, which yielded a dense packing with similar structural properties to the
packing we present. The numerical method used was adapted from the divide and con-
cur approach to constraint satisfaction problems [30]. The divide and concur formalism

enables us to set up an efficient search through the parameter space consisting of the po-
sitions and orientations of tetrahedra inside the repeating unit and the translation vectors
governing its lattice repetition, subject to the constraint that no two tetrahedra over-
lap. The dynamics involved in the divide and concur search are highly non-physical,

which might explain why our method was able to discover this dense packing, while
earlier methods involving more physical dynamics were not [69, 68, 33]. In this note
we present only the analytically constructed packing without a full explication of the
numerical method, which will be forthcoming.




2.3 One-parameter family of dimer-double-lattice packings


The first set of packings we report on are naturally described as double lattices of bipyra-
midal dimers. A double lattice is the union of two Bravais lattices related to each other
by an inversion operation about some point. In [49], Kuperberg and Kuperberg used
the idea of a double lattice in the Euclidean plane to show that any planar convex body
                                                                              √
can be packed in an arrangement with a packing fraction no smaller than 3/2. We



                                            15
 fundamental                   T 0 = conv{ri | i = 1, 2, 3, 4}
 tetrahedron                   r1 = 27
                                     28
                                        a − 307
                                                b + 10
                                                     39
                                                        c
                               r2 = 14 a − 109 b
                                     1        1
                               r3 = 14  a + 10  b + 135 c
                                     3       1      5
                               r4 = 7 a + 10 b − 13    c
 other tetrahedra              T 1 = R2 (T 0 ) = conv{ 23 (r2 + r3 + r4 ) − r1 , r2 , r3 , r4 }
 in the unit cell              T 2 = I(T 0 ) = −T 0
                               T 3 = I(T 1 ) = −T 1
 space group                   translations by a, b, dx = 21 b + 12 c + xa
 generators                    I = inversion about 0
                               R2 = two-fold rotation about { 14 a + tb | t ∈ R}
 packing fraction              100/117
                                       √
 coordinate basis for which    a = (2 √7/5, 0, 0)
 tetrahedra are regular        b = (0, 3/2,    √ 0)
 with unit edge length         c = (0, 0, 13 3/14/5)
   Table 2.1: The construction of the dimer-double-lattice family of packings in
             terms of the parameter 29/56 ≤ x ≤ 9/14 in a general monoclinic
             coordinate basis (a · b = b · c = 0). The packing is generated starting
             from the fundamental tetrahedron by the action of the space group. A
             packing of regular tetrahedra is obtained when the general monoclinic
             coordinate basis reduces to the specified orthogonal coordinate basis.


naturally extend the idea of the double lattice to the three-dimensional Euclidean space.

The repeating unit of one constituent lattice is a bipyramidal dimer: two regular tetra-
hedra sharing a common face. Two of these dimers with mutually-inverted orientation
— a Kuper-pair — form the repeating unit of the double lattice, which thus has four
tetrahedra of distinct orientations. We state the existence of the packings as Theorem 1.

Theorem 1. There exists a one-parameter family of packings of regular tetrahedra,
each having packing fraction 110/117. These packings are periodic, with each unit
cell of the lattice containing two bipyramidal dimers. The group of isometries leaving
each packing invariant is a crystallographic space group of type C2/c (following the

classification and notation of [54]) and acts transitively on the individual tetrahedra of
the packing.




                                              16
Proof. We construct each packing by acting on a single regular tetrahedron with a group
of isometries. For a coordinate basis we use three pair-wise orthogonal vectors a, b, and
                     √            √                    √
c, of norms |a| = 2 7/5, |b| = 3/2, and |c| = 13 3/14/5. The initial tetrahedron
T 0 = conv{ri | i = 1, 2, 3, 4} is the convex hull of four vertices whose coordinates

are given in Table 2.1; it is a regular tetrahedron of unit edge length. The group of
isometries is the group of crystallographic type C2/c generated by the translations a, b,
and dx = 12 b + 21 c + xa (29/56 ≤ x ≤ 9/14), by the inversion about the point 0, and by
the rotation by 180 degrees about the axis { 41 a + tb | t ∈ R} [54]. This space group has a

point group of order 4 and its translations generate a centered monoclinic point lattice.
The construction is summarized in Table 2.1.


   By construction, each tetrahedron in the packing is the image of T 0 under an isometry
in the group. We have immediately then that all tetrahedra are congruent with T 0 , that the
packing is invariant under the action of the group, and that the group acts transitively on

individual tetrahedra. As the tetrahedra divide into four orbits of the lattice translations,
the packing fraction is given by
                                                     √
                                4 vol(T 0 )       4( 2/12) 100
                         φ=                     =             =
                            | det([a, b, dx ])|   |a||b||c|/2   117


   All that is left then to prove the theorem is to verify that the arrangement of tetrahedra
thus constructed is indeed a packing. As the packing is transitive (in the sense that its
symmetry group acts transitively on the constituent tetrahedra), it is enough to check

that one tetrahedron, T 0 , does not overlap any other tetrahedron. By means of a closest-
lattice-point algorithm such as the one in [1], we generate a list of all tetrahedra whose
                                                                  √
centroid is, for any 29/56 ≤ x ≤ 9/14, at a distance less than 3/2 from the centroid
of T 0 . There are 46 such tetrahedra. All other tetrahedra have circumspheres which do

not intersect the circumsphere of T 0 , and therefore they do not intersect T 0 . For each
tetrahedron in the list we can establish the existence of a separating plane separating it


                                             17
   Figure 2.1: Small portions of one layer and three stacked layers in the dimer-
               double-lattice packing given by x = 4/7.


from T 0 . Two tetrahedra have no overlap if and only if they are separated by a plane, and

moreover, such a plane always exists which passes through three of the eight vertices of
the two tetrahedra. By exhaustively verifying that one of the finitely many planes that
pass through three of the vertices separates the two tetrahedra, we establish that each
tetrahedron in the list can be separated from T 0 .                                       


   Note that the above construction, which uses a specific orthogonal coordinate basis
{a, b, c}, is a special case of a general family of packings of non-regular tetrahedra that
can be obtained using the same construction, but with a general monoclinic coordinate

basis (a · b = b · c = 0). Each of these more general packings is an image of a packing
in the original family under an affine map from a three-parameter family (not counting
pure dilation). As the lack of overlap between tetrahedra and the packing fraction are
both affine-invariant, these are also transitive packings of the same packing fraction.


   By the construction of the double lattice, there is an inversion center that sends

one lattice of dimers into the other. Note that a lattice translation composed with an
inversion about a point corresponds to an inversion about a point related to the original
inversion center by half the lattice vector. It follows then that in any primitive unit cell



                                             18
of the lattice, there are eight such inversion centers. These eight inversion centers form
the vertices of a parallelepiped one-eighth the volume of the primitive unit cell of the
lattice. This parallelepiped is the equivalent of the “extensive parallelogram” described
in [49] whose vertices are the inversion points that generate the double lattice. As in

[49], the parallelepiped is inscribed in the body being packed — the bipyramidal dimer
in our case.


   An interesting feature of the packing is the presence of the free parameter x. The
effect of a change in x is to slide fixed layers of the packing relative one another along
the a-direction. These layers are the layer generated by the translations a and b from the

four tetrahedra of the primitive unit cell and the layers parallel to it. The construction
yields a valid packing when the small protrusions in one layer are staggered to fit into
small gaps in the neighboring layer, which is the case for all 29/56 ≤ x ≤ 9/14 (mod 1).
Within this range, each layer can slide against the neighboring layer without changing

the spacing between the two or creating collisions. It is possible then to obtain equally
dense, non-transitive packings by staggering consecutive layers arbitrarily within the
allowed range.


   We describe next the contacts formed by each dimer in the packing, and they are il-
lustrated in Figures 2.1 and 2.2. Each of the eight vertices of the inscribed parallelepiped
corresponds to the center of a face-face contact between bipyramids of opposite orien-

tations, accounting for all contacts between oppositely-oriented bipyramids. Four of
these contacts are within one layer and four of them are with the layers above and be-
low. The contacts formed between like-oriented bipyramids vary with the parameter x:
for all values of x there are two edge-edge contacts, a vertex-edge contact and an edge-

vertex contact (all of these contacts occur on two-fold axes and are within one layer);
for x = 29/56 there are four additional edge-edge contacts with dimers in neighboring




                                            19
                                                                            

                                                                  


                                                              


                                                          

                                                                            

   Figure 2.2: The contacts on the surface of a dimer in the dimer-double lattice
               packing shown on a net diagram for x = 29/56 (left) and x = 9/14
               (right): the face-face contacts (gray), whose centers (black dots) lie on
               inversion centers, four of which are fixed and four of which move as
               a function of x; the four point contacts made regardless of the value
               of x (blue squares), all lying on two-fold axes; the four point contacts
               formed only for x = 29/56 (purple dots); and the four point contacts
               formed only for x = 9/14 (green dots).




   Figure 2.3: Small portions of one layer and three stacked layers in the simple-
               double-lattice packing.


layers (which turn into overlaps for x < 29/56); and for x = 9/14 there are instead
two vertex-face contacts and two face-vertex contacts with dimers in neighboring layers

(which again turn into overlaps for x > 9/14). Thus, each dimer makes respectively
twelve, sixteen, or sixteen contacts in the three cases, and correspondingly, each tetra-
hedron makes eight, ten, or eleven contacts.



                                            20
 fundamental                T 0 = conv{ri | i =
                                              √ 1, 2, 3, 4}         √
 tetrahedron                r1 = [(433 − 86√ 10)a + (611 − 133 10)b+
                                  (188 − 22 √10)c]/246           √
                            r2 = [(111 − 30√ 10)a + (93 − 75 10)b+
                                 (−66 − 42 √  10)c]/246           √
                            r3 = [(−85 −√28 10)a + (13 − 29 10)b+
                                  (4 + 10 10)c]/246
                                                √                    √
                            r4 = [(179 − 106 √   10)a  +  (427 − 101  10)b+
                                  (−20 − 50 10)c]/246
 other tetrahedron          T 1 = I(T 0 ) = −T 0
 in the unit cell
 space group                translations by a, b, c
 generators                 I = inversion about 0
                                       √
 packing fraction           (139 + 40 10)/369
                                             √
 coordinate basis for       a = (1, −(13√− 4 10)/3, √0)
 which tetrahedra are       b = (−(4 √− 10)/3, 3 √  − 10, −1)
 regular with unit edge     c = (3 − 10, 1, (4 − 10)/3)
   Table 2.2: The construction of the simple-double-lattice packing in a general tri-
              clinic coordinate basis.


2.4 Simple double-lattice packing


Our numerical search also yielded a packing with two tetrahedra per repeating unit,
which we could identify as a simple double lattice (that is a double lattice of tetrahedra,
                                             √
not of dimers) with packing fraction 139+40
                                        369
                                            10
                                               ≈ 0.7194. We present therefore a second
theorem.

Theorem 2. There exists a packing of regular tetrahedra having packing fraction
       √
139+40 10
   369
          .   This packing is periodic, with each unit cell of the lattice containing two
tetrahedra. The group of isometries leaving the packing invariant is a crystallographic
space group of type P1̄ and acts transitively on the individual tetrahedra of the packing.


    The proof of this theorem proceeds equivalently to the proof of Theorem 1. The

vertices of the initial tetrahedron T 0 are given in Table 2.2 in terms of a triclinic coordi-


                                             21
 Name                               φ                     N      Z̄      Transitive
 Optimal lattice[41]                18/49 ≈ 0.3673        1      14      Yes
 Warp and weft[17]                  2/3 ≈ 0.6666          2      10      Yes
 Welsh[17]                          17/24√≈ 0.7083        34     25.9    No
                                    139+40 10
 Simple double lattice                 369
                                              ≈ 0.7194    2      19      Yes
 Wagon wheels[12]                   0.7786                18     7.1     No
 Compressed wagon wheels[69]        0.7820                72     7.6     No
 Disordered wagon wheels[68]        0.8226                314    7.4     No
 Quasicrystal approximant[33]       0.8503                656            No
 Dimer double lattice               100/117 ≈ 0.8547      4      8 to 11 Yes
   Table 2.3: Some studied transitive and non-transitive packings of regular tetrahe-
              dra with packing fraction φ, number of tetrahedra in the repeating unit
              N, and average number of contacts per tetrahedron Z̄ where available.


nate basis which is also given in Table 2.2. The group of isometries we use to construct
the packing is generated by translation by the three vectors a, b, and c and by inversion
about the origin. This is a space group of crystallographic type P1̄, with a point group

of order 2 and a triclinic lattice [54]. Figure 2.3 shows a portion of the packing.


   The simple-double-lattice packing again has eight inversion centers per primitive
cell at the vertices of a parallelepiped. However, in this case only five of the vertices
are on the surface of the tetrahedron. Each tetrahedron in the packing is in contact with
nineteen others.




2.5 Discussion


In Table 2.3, we compare the packings presented here to other studied packings of regu-
lar tetrahedra. Both packings are denser than the densest previously-reported transitive
packing, a double lattice presented by Conway and Torquato (which we call the ”warp-
and-weft” packing due to the interweaving arrangement of its tetrahedra) [17], and the

dimer double lattice is denser than any previously-reported packing.


                                            22
   The results presented go against the recent trend of ever-growing repeating units in
densest-known packings and demonstrate that a large repeating unit is not a necessary
property of a dense packing of regular tetrahedra. It is curious that previous simulations,
utilizing a more physical search dynamic [69, 68, 33], yielded dense packings that were

either disordered, had quasicrytalline order, or had crystalline order characterized by a
very large repeating unit, and were not able to find the denser class of structures pre-
sented here, (reminiscent perhaps of Kurt Vonnegut’s ice-nine, a fictional phase of water
that is more stable, but kinetically unreachable).


   Our results yield the surprising situation wherein the densest-known packing of

icosahedra is now sparser than the corresponding packing of tetrahedra, a solid which
just four years ago was a prime candidate for a counterexample of a conjecture by Ulam
that the sphere is the sparsest-packing convex solid [17]. As the packing can be gener-
ally extended to any tetrahedron in a three-parameter family generated by deformations

of the monoclinic coordinate basis, if any tetrahedron provides a counterexample of
Ulam’s conjecture, it is not a tetrahedron of that family.


   The regular tetrahedron is no longer outcast, as it long was, from the respectable
family of convex polyhedra whose largest-achieved packing density is realized by a
transitive arrangement. While there are some convex solids whose maximum packing
density clearly cannot be achieved by a transitive arrangement (the convex Schmitt-

Conway-Danzer polyhedron can tile space, but only in aperiodic and non-transitive ways
[18]), the majority of regular and semi-regular polyhedra have been to-date packed most
densely in transitive packings [69]. Whether this situation is accidental, the result of bias
favoring the discovery of transitive packings, or a more fundamental property governing

the packing of a certain class of solids is still an open question.




                                             23
                                      CHAPTER 3
                A METHOD FOR DENSE PACKING DISCOVERY



   The contents of this chapter have been published in Physical Review E with coau-
thors Veit Elser and Simon Gravel [47].


3.1 Abstract


The problem of packing a system of particles as densely as possible is foundational in

the field of discrete geometry and is a powerful model in the material and biological sci-
ences. As packing problems retreat from the reach of solution by analytic constructions,
the importance of an efficient numerical method for conducting de novo (from-scratch)
searches for dense packings becomes crucial. In this paper, we use the divide and con-

cur framework to develop a general search method for the solution of periodic constraint
problems, and we apply it to the discovery of dense periodic packings. An important
feature of the method is the integration of the unit cell parameters with the other packing
variables in the definition of the configuration space. The method we present led to pre-

viously reported improvements in the densest-known tetrahedron packing. Here, we use
the method to reproduce the densest known lattice sphere packings and the best known
lattice kissing arrangements in up to 14 and 11 dimensions respectively (the first such
numerical evidence for their optimality in some of these dimensions). For non-spherical

particles, we report a new dense packing of regular four-dimensional simplices with
density φ = 128/219 ≈ 0.5845 and with a similar structure to the densest known tetra-
hedron packing.




                                            24
3.2 Introduction


The dense packing behavior of a general solid body (particle) in a Euclidean space is
a problem of interest in mathematics, physics, and many other fields. A packing is a
collection of particles in the Euclidean space Rd , wherein no two particles overlap (i.e.,
the intersection of any two particles has an empty interior) and the packing fraction or

density φ is then the volume fraction of space covered by the particles. Of particular
interest are packings of a given particle (wherein all particles are congruent), and the
problem of interest is to determine the maximum possible density φmax among all pack-
ings of a given particle. A packing that realizes this maximum can be thought of as the

equilibrium state of the system of classical hard particles in the limit of infinite pressure
or zero temperature.


   The general problem of packing congruent particles was posed as a part of the eigh-
teenth of David Hilbert’s famous Mathematische Probleme:


      How can one arrange most densely in space an infinite number of equal
      solids of a given form, e.g., spheres with given radii or regular tetrahedra
      with given edges (or in prescribed position), that is, how can one so fit them

      together that the ratio of the filled to the unfilled space may be as large as
      possible? [38]


This part of the problem has been taken over the years as the resolution of the Ke-
pler conjecture about the densest packing of spheres in three dimensions [60], and has
therefore been considered resolved since the latter was proved by Hales [34]. However,
Hilbert’s statement of the problem does not single out the sphere, and actually men-

tions the regular tetrahedron as another particle of interest. Recent work diverging from
the focus on spherical particles has spotlighted ellipsoids [19], regular and semi-regular


                                             25
polyhedra [69, 68] (and the regular tetrahedron in particular [12, 33, 46, 70, 13]), and
superballs [44]. Few bounds are known for the maximum packing fraction of general
convex particles. Kuperberg and Kuperberg have shown that for any convex particle in
                       √
two dimensions, φmax ≥ 3/2 ≈ 0.86602 [49]. Torquato et al. used the known maximal

packing density of spheres to derive an upper bound on the packing density of any solid,
but this bound is trivial (i.e., φmax ≤ φU , where φU > 1) for many solids [69]. Ulam has
conjectured that in three dimensions, the sphere achieves the lowest maximum packing
                    √
fraction, φmax = π/ 18 ≈ 0.74048, among all convex particles [27].


   In the quest for dense packings of various particles, analytic and numerical investi-

gations have both played important roles. The former have been very successful in the
study of the dense packing of spheres, where analytic constructions based on groups,
codes, and laminated lattices have produced the densest-known sphere packings and lat-
tice sphere packings in many dimensions [16]. However, the analytic approach to the

construction of dense packings relies on the imagination of the constructor, and for a
variety of other problems the densest packings have evaded the creativity of analytic
investigators and were only uncovered in computational investigations. While complete
(i.e., exhaustive) algorithms exist for some problems (such as the algorithm in Ref. [62],

which gave new best known results for the lattice covering and covering-packing prob-
lems in some dimensions), they do not exist or have runtimes that are too long for other
problems. In those cases, incomplete search algorithms become necessary.


   One example of a dense packing that has only been uncovered by a de novo numeri-
cal search is the currently densest-known packing of tetrahedra, whose structure was first
hinted at by a numerical search using the method described in this paper [46]. The struc-

ture was later optimized by Torquato and Jiao [70] and by Chen et al. [13]. Results of
subsequent Monte Carlo simulations have reproduced this structure and suggest it is the




                                           26
densest packing of regular tetrahedra at least with a small number (≤ 16) of tetrahedra
in the unit cell [70, 13]. Another de novo search with Monte Carlo dynamics has un-
covered a packing based on a quasicrystal approximant reminiscent of the Frank-Kasper
σ-phase with a slightly lower density [33]. As these two structures were overlooked by

previous analytical investigations [12, 17], it is quite likely that without the results of de
novo searches, they would have remained unimagined and undiscovered.


   In the best case, such searches would produce the optimal packing possible subject
to the built-in restrictions (such as number of particles in the unit cell or unit cell shape).
However, in problems exhibiting a large degree of frustration, the presence of many local

optima that are separated from each other by high barriers complicates the task of finding
the optimal packing. The tendency of simulations to get stuck in the local optima of such
a rugged optimization landscape, especially when these local optima proliferate as more
particles are simulated, has been held responsible for suboptimal results in searches

[69, 68]. One technique which has been observed to relieve dynamical stagnation in
Monte Carlo simulations at high pressures has been to allow slightly unphysical moves,
such as allowing particles to temporarily overlap [33].


   We propose a novel search method as an alternative to Monte Carlo simulations, with
a number of features that directly address these observations. The method is based on the
dynamics of the difference map, a constraint-satisfaction iterative search algorithm, and

on the divide and concur constraint framework (we abbreviate this combination D − C,
where the minus sign stands for the difference map) [23, 30, 29]. It adapts the D − C
approach to the case of periodic problems and we shall call it periodic divide and con-
cur (PDC). The difference map is designed to avoid being trapped in local optima and

has been demonstrated in multiple applications to find solutions of highly non-convex
problems, including finite packing problems with large numbers of particles, from ran-




                                              27
dom starting configurations [23, 30, 29]. The search proceeds through a non-physical
configuration space, cutting through the conventional physical optimization landscape.
Still, it is to be expected that the exponential growth in the number of local optima in
the configuration space, which the search will still have to traverse, will nevertheless

lead to suboptimal results when many independent particles are included in the search.
Therefore, as discussed below, it is crucial for the unit cell variables to be aggressively
optimized so that the number of particles to be simulated can be reduced. The incorpo-
ration of the unit cell variables directly into the basic dynamics of the search achieves

this goal.


   Numerical searches are restricted to finite-dimensional configuration spaces, and
therefore have been largely limited to investigating periodic packings, packings which
are preserved under translations by a lattice Λ. In a general periodic packing, the parti-
cles are partitioned into p orbits of the lattice Λ, and when p = 1 the packing is called

a lattice packing. In physics, any periodic arrangement is usually referred to as a lattice
and the special case of p = 1 is known as a Bravais lattice. In general, the maximum
density need not be realizable by a periodic packing, but arbitrarily close densities are
realizable with periodic packings of arbitrarily large p. Similarly, arbitrarily accurate

approximations of any packing can be obtained using a sufficiently large cubic or or-
thorhombic unit cell. However, due to the rapid increase in computational complexity
and the proliferation of local optima as the number of independent particles rises, it is
often preferable to include fewer particles but allow for a variable unit cell shape. We

focus then on searching for packings with a small number of particles in the unit cell.

   To our knowledge, variable unit cells have only been introduced recently to searches

for dense packings, for instance with the adaptive shrinking cell scheme in Refs. [19, 68]
and with the use of Parrinello-Rahman dynamics in the space of lattices in Ref. [14].




                                            28
The increased particle population associated with restricting unit cell variability can
sometimes be tolerated in two and three dimensions, but in high dimensions the number
of particles that must be simulated grows exponentially due to the curse of dimension-
ality and this approach becomes impractical. The constraint-satisfaction formulation of

the periodic packing problem used in PDC features a variable unit cell and naturally
treats the positions of particles in the unit cell and the unit cell parameters on the same
footing. This new approach allows us to successfully look for dense sphere packings
in dimensions as high as 14, further than probed by any previously reported unbiased

numerical exploration of periodic packings.


   Besides the density of a packing, another attribute of interest is the coordination
number, that is, the number of nearest neighbors of particles in the packing. In the case
of spherical particles, this amounts to the number of spheres in contact with a given
sphere, known as the kissing number [16]. Searching for high-coordination number

arrangements around a single sphere has been accomplished previously with the D − C
method [30]. Here we apply PDC to search for space-filling periodic arrangements of
high coordination number, and particularly lattice arrangements.


   An efficient de novo numerical search method can provide critical utility in the field
of packing. In addition to the ability of a de novo search to provide confidence in a
putative, but not proven, optimal result, a de novo search has often been responsible

for surprising new results: two recent examples in which unexpected (as it turns out,
quasiperiodic) packings were found as the results of de novo searches are in the problem
of tetrahedron packing [33] and in the ten-dimensional kissing number problem [21]. It
is with these motivations that we introduce the PDC method in this paper. In Section 3.3

we introduce the D−C scheme by presenting a simple example which serves to motivate
the constructions in the subsequent sections. In Section 3.4 we formulate the problems




                                            29
tackled in this paper — sphere packing, the lattice kissing number, and polytope packing
— in terms of constraint satisfaction. In Section 3.5 we describe in detail aspects of our
implementation of the PDC search, including efficient computation of projections to
the constraints of Section 3.4. In Section 3.6 we present some results of PDC for the

problems discussed, including a newly discovered packing of regular four-dimensional
simplices. In Section 3.7 we present concluding remarks.




3.3 Motivation



3.3.1 The D − C scheme


The key step in applying the D−C approach to packing problems is to recast the problem
as a problem of constraint satisfaction. Particularly, we must express it as the problem

of finding a configuration in a Euclidean configuration space (Ω), which satisfies two
constraints. We identify a constraint C with the subset C ⊆ Ω of configurations satisfy-
ing the constraint. A projection of a configuration x to a constraint C is the operation of
finding a configuration x′ ∈ C that minimizes the distance ||x − x′ ||. Each of the two con-

straints (C, D ⊆ Ω), must be simple enough that the operation of projecting an arbitrary
configuration to it can be computed efficiently. The iterative map used in exploring the
configuration space takes advantage of the formulation of the problem in terms of two
simple constraints, as outlined in section 3.3.2. In this section we present the application

of the D − C scheme to finite sphere packing problems, which has been developed and
implemented in Ref. [30], as an introduction to the main ideas of the scheme.


   The defining constraint of packing problems is the constraint that no particles in the
packing overlap, which we call the exclusion constraint. As a simple illustration of this


                                            30
constraint, consider the exclusion of a pair of unit-radius disks in R2 . In this case, the
configuration space Ψ is parameterized by the positions of the centers of the two disks:


                                    Ψ = {(x1 , x2) : x1 , x2 ∈ R2 }.                 (3.1)


The exclusion constraint is then


                           Kexcl = {(x1 , x2 ) ∈ Ψ : ||x1 − x2 || ≥ 2} ⊆ Ψ.          (3.2)

This constraint adheres to the simplicity criterion of having an efficient method to com-

pute a projection to it. Specifically, the projection is given by
                                              
                                              
                                                 ′    ′
                                              
                                              (x1 , x2 ) if ||x1 − x2 || < 2
                                              
                                              
                                              
                                              
                        πKexcl [(x1 , x2 )] = 
                                                                                    (3.3)
                                              
                                              
                                              (x1 , x2 ) otherwise,
                                              
                                              

where,

                                          2 − ||x1 − x2 ||
                                x′1 =x1 +                  (x1 − x2 )                (3.4)
                                           2||x1 − x2 ||
                                          2 − ||x1 − x2 ||
                                x′2 =x2 −                  (x1 − x2 )                (3.5)
                                           2||x1 − x2 ||

as illustrated in Figure 3.1.

    A more complicated case arises when three or more disks are considered. In this

case, the exclusion constraint,


                            Kexcl = {(x1 , . . . xn ) ∈ Ψ :

                                 ||xi − x j || ≥ 2 for all 1 ≤ i < j ≤ n},


is not a simple constraint according to the criterion above. Alternatively, we could
replace Kexcl by many pairwise exclusion constraints

                             i, j
                            Kexcl = {(x1 , . . . xn ) ∈ Ψ : ||xi − x j || ≥ 2}.      (3.6)



                                                   31
Figure 3.1: An illustration of the D − C scheme in the case of packing three disks
            into a square box. In the case of two overlapping disks (a), the exclu-
            sion constraint is simple in the sense that a projection to the constraint
            can be performed efficiently. The projection is given by (3.3) and
            yields the configuration (b). In the case of three disks (c), there is no
            similarly efficient projection method to the constraint that no overlaps
            occur. In the D − C scheme, each disk is represented by two repli-
            cas (d), which together make three independent replica pairs (e). The
            exclusion constraint, now also called the “divide” constraint, is mod-
            ified so that only replica pairs are prohibited from overlapping, and
            any other overlaps are allowed. Thus, the projection to the exclusion
            constraint can be performed independently on each replica pair as in
            the case of two disks (f). A second constraint, the “concur” constraint,
            requires all replicas representing a single disk to coincide and requires
            the disk to lie within the confinement box. The result of projecting the
            configuration (d) to this constraint is the configuration (g). In order
            to search for a configuration satisfying both constraints, we do not al-
            ternately project from one constraint to the other, but instead use the
            difference map (3.12) to evolve the configuration. The result of a suc-
            cessful search is a configuration (h) satisfying both constraints, which
            by construction corresponds to a solution of the problem.




                                         32
The pairwise constraints are all individually simple. However, as noted above, we are
limited to problems described by only two simple constraints.


    Divide and concur provides a general procedure for reducing the number of simple
constraints to two, at the expense of enlarging the configuration space. This reduction
is achieved by parameterizing the configuration space with more variables than are nec-

essary to fully specify a configuration. In the example at hand, the new configuration
space is
                       Ω = {(x1,2, . . . xn,n−1 ) : xi, j ∈ R2 for all i , j},            (3.7)

where we call all the variables xi, j for a particular index i the replicas of the original
variable xi . Every configuration (x1 , . . . xn ) ∈ Ψ can be identified with a configura-
tion (x1,2 , . . . xn,n−1 ) ∈ Ω, wherein xi, j = xi for all i, j, through a simple linear map A.
Enough redundant variables have been introduced to the configuration space so that each

pairwise exclusion constraint can now be written in terms of a private set of variables,
disjoint from the private variables of other constraints:

                       Di, j = {(x1,2 , . . . xn,n−1 ) ∈ Ω : ||xi, j − x j,i || ≥ 2}.     (3.8)

The intersection, D ⊆ Ω, of all of the pairwise exclusion constraints, which we will
call the “divide” constraint, is now also simple, since the projection can be performed

independently on each set of private variables (Figure 3.1).

    The map A : Ψ → Ω from the original configuration space (the physical configura-

tion space) to the new one (the formal configuration space) is not surjective, and so a
general point in the formal configuration space does not correspond to a valid physical
configuration. The “concur” constraint C = A(Ψ) is given by the range of A, the subset
of Ω that does correspond to valid configurations. That is, the constraint requires redun-

dant specifications of an original variable to concur in regard to its value. Since A is
linear, C is also a simple constraint.


                                                    33
   Another constraint that must usually be addressed in packing problems with a finite
number of particles is the confinement constraint. In most cases the particles, or their
centers, are confined to lie in some subset M of space, where M can be either some
region of finite volume, or a compact manifold (as in the case of spherical codes). As a

subset of the original configuration space, the confinement constraint is written as

                      Kconf = {(x1 , . . . xn ) ∈ Ψ : xi ∈ M for all i} ⊆ Ψ.            (3.9)

We can incorporate this constraint into the “concur” constraint, C, by modifying it to be
the image A(Kconf ) instead of the entire range of A. In our example, this would give the
constraint

                   C = {(x1,2 , . . . xn,n−1 ) ∈ Ω : xi, j = xi ∈ M for all i, j}.     (3.10)

Since A is linear, the projection to C = A(Kconf ) can be decomposed into a projection
to A(Ψ) followed by a projection to A(Kconf ). The first step is performed by taking

the average position of all the replicas of each disk. The second step is performed
by projecting this average position to M (see Figure 3.1). In general, this two-step
projection method is valid for handling the constraints in the physical configuration
space that are simple at the outset and do not require the introduction of new variables.


   The result of the above construction is that a configuration in Ω satisfies the “divide”

and “concur” constraints simultaneously if and only if it corresponds to a configuration
in Ψ which satisfies all the exclusion constraints and the confinement constraint; that is,
it corresponds to a solution of the packing problem under consideration.


   In the following sections we modify the above simple construction so as to gener-
alize the method in two major ways. The first generalization is to packings of infinite
regions, instead of only finite ones. Specifically, we allow for periodic packings with an

arbitrary unit cell. This is achieved by generalizing the idea of replicas of particles to in-
clude also their periodic images. When the unit cell vectors are included in the original


                                                34
set of parameters, the map from the original parameter space to the space of replica con-
figurations is still linear, though a little more elaborate. Additionally, the confinement
constraint of finite packings is replaced in the case of periodic packings by a constraint
on the unit cell volume, ensuring a specified density.


   The second generalization is to packings of non-spherical particles, specifically con-

vex polytopes. This is achieved by representing each particle not only by the position
of its centroid, but by the positions of all its vertices. A new constraint, the rigidity
constraint, is added to ensure that the particle is not deformed in the solution. Despite
the mathematical complications that arise from these two generalizations, the concep-

tual framework is identical to the above example, and the constructions in the following
sections will draw attention to the analogy with the construction presented above.




3.3.2 The difference map


Given a problem formulated as the task of finding a configuration x ∈ C ∩ D, simulta-
neously satisfying the constraints C, D ⊆ Ω, we wish to use the availability of efficient

methods for computing the projections πC and πD to the constraints in order to set up an
iterated map to search through the configuration space for a solution. Naive schemes,
such as the alternating projections map x 7→ πD (πC (x)), suffer from the problem of stag-
nation at near solutions (local minima of the distance between the two constraints). The

difference map, a slightly more sophisticated scheme, is designed to provide efficient
search dynamics while avoiding the traps of local minima [23].


   The difference map (DM) can be written in terms of the projections πC and πD and
one parameter β:
                                     DM : Ω → Ω                                    (3.11)


                                           35
                                                                 
                            x 7→ x + β πD ( fC (x)) − πC ( fD (x)) ,                 (3.12)

where
                                              !
                                            1        1
                                fD (x) = 1 − πD (x) + x,
                                            β        β
                                              !
                                            1        1
                                fC (x) = 1 + πC (x) − x.
                                            β        β
In this paper we use only β = 1. A difference map search proceeds by starting from a ran-
dom initial configuration x0 and iteratively applying the difference map: xi = DM(xi−1 )
[23]. When the map reaches a fixed point x f p , a solution is obtained by

                                                                
                            x sol = πC fD (x f p ) = πD fC (x f p ) .                (3.13)


Notice that the ability to obtain a solution from any fixed point of the map, due to the
cancelation of the two bracketed terms in (3.12), relies on the definition of the problem
in terms of only two simple constraints. For a given iterate xi , the terms πC ( fD (xi ))

and πD ( fC (xi )) provide two estimates of the solution, each satisfying one of the two
constraints. We call these respectively the C- and D-estimates of the solution at the ith
iteration. The distance between the two estimates is the error ǫ and the search terminates
when the error converges to zero.


   To summarize, a simple difference map solver for continuous constraints would con-

sist of the following simple steps:


   1. Initialize the iterate x to a random configuration.

   2. Compute the two estimates of the solution xC ← πC ( fD (x)) and xD ← πD ( fC (x)).

   3. Compute the error ǫ ← ||xC − xD ||. If it is below a predefined convergence thresh-
        old, the search terminates, and the solution is given by xC ≈ xD .

   4. Advance the iterate x ← x + β(xD − xC ). Start the next iteration at Step 2.



                                               36
3.4 Constraints



3.4.1 Periodic sphere packing and kissing


A periodic packing of equal-sized spheres (radius r) in d dimensions can be generated

by the action of a lattice Λ on a set of p primitive spheres. Let P be the set of centers
of the primitive spheres. We define a generating matrix of the packing as a (d + p) ×
d matrix M whose first d rows are a set of generators of Λ and whose remaining p
rows are the vectors in the set P. Combining these quite different sets of configuration

variables into a single matrix serves to remind us that at the highest level of our search
algorithm both sets are treated in a uniform manner by the projection operators. The
detailed constraints, of course, distinguish among the two parts of M, which we denote
M0 (lattice generators) and M1 (primitive sphere centers). The set of all the centers of

spheres in the packing is then the Minkowski sum

                          Λ + P = {b0 M0 + y : b0 ∈ Zd , y ∈ P}                       (3.14)

                                  = {bM : b ∈ Zd ⊕ E p },

where E p is the set of all cyclic permutations of the p-element vector (1, 0, 0, . . . , 0).
The space R(d+p)×d of generating matrices takes the role of the physical configuration
space Ψ.


   A matrix M generates a valid packing if the centers of any two sphere of the packing,
b1 M and b2 M, are separated at least by a distance of 2r when b1 , b2 . Each choice of

b1 and b2 generates a constraint on the matrix M

                                    ||b1 M − b2 M|| ≥ 2r,                             (3.15)

which we call an exclusion constraint. Note that there are infinitely many indepen-
dent exclusion constraints (constraints with b1 − b2 = b′1 − b′2 are not independent).


                                             37
However, for any non-degenerate matrix M only finitely many independent exclusion
constraints are violated or are even remotely close to being violated. In practice, only
those constraints need be tested in our computations. We call those constraints the rele-
vant exclusion constraints (let there be n of them), and we define a 2n × (d + p) matrix

A whose rows a2i−1 and a2i are the vectors b1 and b2 related to the ith relevant exclusion
constraint. We discuss below how the relevant constraints are identified.


   The linear map A : M 7→ X = AM is a map from the physical configuration space
Ψ to a larger-dimensional space, Ω = R2n×d , which we use as the formal configuration
space. As before, since the map A is not surjective, only a subset (a linear subspace,

in fact) of formal configurations have a corresponding generating matrix in the physical
configuration space. The choice of constraints below will guarantee that solutions be-
long to this subset. The size of the configuration space grows as the number of relevant
independent exclusion constraints, which is the number of independent near neighbor

pairs for which overlap needs to be actively avoided. Notice that each relevant exclu-
sion constraint can now be written in terms of a private set of variables. Specifically,
each row of the matrix X corresponds to the position of one particle, and the ith relevant
exclusion constraint is given by


                             Di = {X ∈ Ω : ||x2i−1 − x2i || ≥ 2r}.                  (3.16)


The intersection of all the relevant exclusion constraints forms our “divide” constraint,


                     D = {X ∈ Ω : ||x2i−1 − x2i || ≥ 2r for i = 1, . . . n}.        (3.17)


Each set of private variables associated with one exclusion constraint is composed of the
coordinates of replicas of two particles, and we call these two replicas a replica pair.


   As mentioned in Section 3.3.1, the confinement constraint of finite packing prob-
lems is replaced in the case of periodic packings with a constraint on the density of the


                                               38
packing. The density of a packing generated by a matrix M is given by the density of
the unit cell, whose volume is | det M0 | and which contains p particles of volume V1 :

                                                   pV1
                                           φ=              .                             (3.18)
                                                | det M0 |

Therefore, if we wish to find a packing of density φ ≥ φtarget , the density constraint on
the generating matrix will be

                             Kdensity = {M ∈ Ψ : | det M0 | ≤ Vtarget },                 (3.19)

where Vtarget = pV1 /φtarget .


    As in the example of Section 3.3.1, since the map A is not surjective, a general el-

ement X ∈ Ω of the formal configuration space does not correspond to a well-defined
physical configuration. We therefore impose a constraint that requires X to lie in the
range of A. In the context of the PDC construction we call this the lattice constraint
because it requires different periodic images of a primitive particle to lie on the points

of a lattice, and requires that lattice to be the same for all primitive particles (up to trans-
lation). Again, as in Section 3.3.1, we combine the lattice constraint with the density
constraint to form the “concur” constraint:

                            C =A(Kdensity )                                              (3.20)

                                 ={X = AM ∈ Ω : | det M0 | ≤ Vtarget }.


    With these definitions of the constraint sets, X = AM ∈ C ∩ D if and only if M
generates a periodic packing of density φ ≥ φtarget . The action of the projections πD and

πC to the two constraints is illustrated in Figure 3.2 and Sections 3.5.1 and 3.5.2 discuss
how the projections are computed efficiently.


    The basic operations of the search — projections — depend directly on the metric
defined on the formal configuration space. Therefore, the choice of metric affects both


                                                 39
the complexity of implementing the projection and the search dynamics. The simplest
choice for the metric is the distance induced from the Frobenius (Euclidean) norm

                                                                  
                       ||X1 − X2 ||2F = trace (X1 − X2 )(X1 − X2 )T .                  (3.21)


This choice of metric amounts to giving all replicas of a particle equal weight in influ-
encing its consensus position in the “concur” projection. We can use a slightly different
Euclidean metric, given by

                                                                  
                      ||X1 − X2 ||2W = trace W(X1 − X2 )(X1 − X2 )T ,                  (3.22)


where W is a diagonal matrix whose diagonal elements wi are the metric weights of
different replicas. Performance is greatly enhanced by adjusting the metric weights
throughout the search to afford greater weight to replica pairs that continually violate

their constraints and smaller weight to replica pairs that are in low risk of violating their
constraints [30]. Note that removing a constraint from the list of relevant constraints
(i.e., removing the corresponding pair of rows from A and X) is equivalent to setting the
metric weight of its replicas to zero. Therefore, in the course of the search we not only

adjust the weights wi of replica pairs, but also add and remove replica pairs. The details
of how these changes are applied systematically are given in Section 3.5.3.


   This constraint formulation of the periodic sphere packing problem (finding a peri-
odic packing with density φtarget ) can be straightforwardly modified to describe instead
the periodic kissing number problem (finding a periodic packing with average coordi-

nation number τtarget ). First, the “divide” constraint is modified so that each replica pair
must still be separated by a distance of at least 2r, but at least pτtarget replica pairs must
be separated by a distance of exactly 2r. Second, the condition on the volume of the unit
cell is dropped from the “concur” constraint. Projections to these modified constraints

are also given in Section 3.5.



                                             40
                                                                                 HcL       C                 B       HdL
  HaL                                             HbL                                                                          B
                C
                                      B                     C       B

                                                                                                       AA
                                                                                       B           A
                                                                                                   A
                                                                                                        AA
                                                                                                                 C

        B
                            A
                            AA
                             A
                                  A
                                                        B
                                                                A
                        A                 C                             C


                                                                                               C
                                                                                                             B             A
                    C
                                                            C       B
                                      B




  HcL       C                         B            HdL
                                    B “divide” and “concur” projections in the two-
   Figure 3.2: An illustration of the
        B A
              dimensional periodic sphere packing problem with p = 3. (a) A hypo-
                            AA
                             AA
                                              C
              thetical configuration of six replica pairs involving the primitive disk
                        A




              A. Disks with the same letter marking their centers are replicas of the
                    C
                             A        B

              same primitive disk (as for disk A) or of its lattice translates (as for
              disks B and C). One replica pair, violating its exclusion constraint,
              is emphasized. (b) The output of the “concur” projection: the clos-
              est configuration to (a) such that all replicas of a particular primitive
              disk lie on top of each other, or a lattice translation apart (arrows),
              and such that those lattice translations define a lattice with a suffi-
              ciently small unit cell volume. This projection is a modification of
              the “concur” projection depicted in Figure 3.1d,g. (c) The output of
              the “divide” projection: the closest configuration to (a) such that no
              replica pair violates its exclusion constraint. This is identical to the
              “divide” projection depicted in 3.1d-f. Detail: (d) the emphasized
              replica pair before the “divide” projection (thin-outline disks) and af-
              ter (thick-outline disks) isolated for clarity.


3.4.2 Convex polytope packing


The symmetry of the spherical particle allows its configuration to be described solely
by the position of its center. In the case of a general convex particle, the variables of
the configuration space need to include information also about the orientation of the

particle. One possible description of the particle assigns variables separately to the
position of its centroid and to the description of the rotation about the centroid (e.g.,
a rotation matrix or a quaternion). In this paper, however, we find it more convenient
to describe convex polytopes by reference to the positions of their vertices. Therefore,



                                                                            41
a polytope with v vertices is represented by a v × d vertex matrix and is given by the
convex hull of these vertices. Although the configuration of a single particle is no longer
represented by a single vector but by a matrix composed of v vectors, it is convenient
to treat these matrices as vectors, which we typeset as bold-face upper-case Latin letters

(e.g., X for the vertex matrix of the polytope K = conv X = conv{xi : i = 1, . . . v}), and to
construct matrices whose rows are such vectors. A translation by t of a polytope conv X
is given by conv(X + cT t), where cT is a column vector of unit elements and cT t is the
translation matrix corresponding to the translation vector t. Similarly, a rotation is given

by conv(XR), where R is a d × d orthogonal matrix.


   A periodic packing is again generated by the action of a lattice Λ on a set of p
primitive polytopes whose vertex matrices form the set P. The set of all vertex matrices
of polytopes in the packing is the Minkowski sum

                         cT Λ + P = {b0 M0 + Y : b0 ∈ Zd , Y ∈ P}                      (3.23)

                                   = {bM : b ∈ Zd ⊕ E p },

where M is a generating matrix of the packing, whose first d rows (comprising M0 ) are
translation matrices generating Λ, and whose remaining p rows (comprising M1 ) are the
vertex matrices of the set P. The space of generating matrices Ψ = R(d+p)×(v×d) is the

physical configuration space.

   Each exclusion constraint between two particles of the packing requires the convex

hulls conv(b1 M) and conv(b2 M) not to overlap for any b1 , b2 . To construct the formal
configuration space we again form one replica pair for the particles involved in each
relevant exclusion constraint, which gives Ω = R2n×(v×d) . The map A from physical
configurations to formal configurations is given by the matrix A whose rows a2i−1 and

a2i are the vectors b1 and b2 related to the ith relevant exclusion constraint. The “divide”
constraint is given by the intersection of all the relevant exclusion constraints, each


                                             42
expressed in terms of its private replica pair:


                      D = {X ∈ Ω : int(conv X2i−1 ∩ conv X2i ) = ∅                 (3.24)

                                                    for i = 1, 2, . . . n}.


   In addition to the lattice constraint and the density constraints, which combine in
Section 3.4.1 to form the “concur” constraint, in the case at hand we must include a third

constraint, the rigidity constraint. The primitive particles of a packing generated by a
general matrix M are only constrained in their number of vertices, not in the arrangement
of those vertices. However, we are interested only in packing where all the particles are
congruent with a given shape, and so we impose the constraint on M that the vertices

of its primitive particles are obtained from the vertices of the given particle by a rigid
motion:


                          Krigidity = {M ∈ Ψ : Y = Y(0) Ri + cT ti                 (3.25)

                                         for all p rows Y of M1 },


where Y(0) is the vertex matrix of the given particle. The “concur” constraint C =
A(Kdensity ∩ Krigidity ) is given by combining the density and rigidity constraints on the
generating matrix with the lattice constraint. The result of constructing the “divide”

and “concur” constraints is that a formal configuration satisfies both of them if and
only if it corresponds to a generating matrix in the physical configuration space which
yields a packing of the given particle with the desired density. Table 3.1 summarizes the
D − C constraints for the three problems discussed and Section 3.5 describes in detail

the projections to these constraints.




                                             43
                        “divide” constraint          “concur” constraint
               sphere   ||x2i−1 − x2i || ≥ 2r for    X = AM
               packing all n replica pairs           M ∈ Kdensity
               kissing  ||x2i−1 − x2i || ≥ 2r for    X = AM
               number all n replica pairs and
                        = 2r for pτtarget pairs
               polytope convex hulls of X2i−1        X = AM
               packing and X2i+1 non-overlap-        M ∈ Kdensity
                        ping for all n replica       and M ∈ Krigidity
                        pairs
   Table 3.1: A summary of the D − C constraints for periodic sphere packing, the
              average kissing number problem, and polytope packing. The “divide”
              constraint encompasses the relevant exclusion constraints, while the
              “concur” constraint encompasses, where applicable, the density, rigid-
              ity, and lattice constraints.


3.5 Implementation



3.5.1 “Divide” projections


Sphere packing and kissing


In order to implement an iterated difference map search, whose iterations are given by
(3.12), we must implement efficient projections to the “divide” and “concur” constraints.
These implementations are the subject of Sections 3.5.1 and 3.5.2. In the course of the
search, considerations of efficiency require certain changes to the formal configuration

space – specifically adding and removing replica pairs, changing metric weights, and
lattice reduction. In section 3.5.3 we discuss when and how these changes are applied.


   In the case of sphere packing, the “divide” constraint simply requires that the cen-
ters of the two spheres comprising each replica pair be a certain distance apart. This is
obtained by applying equation (3.3) to each replica pair. Note that the “divide” projec-



                                           44
HaL                     HbL                        HcL                 HdL




  HcL                  HdL                         HeL                 HfL
  HeL                   HfL                                 HgL



  HeL                   HfL                                 HgL
             HgL

   Figure 3.3: An illustration of the polytope exclusion and rigidity constraint pro-
               jections for the case of regular pentagons. (a) The pentagons are non-
            HgLoverlapping, as demonstrated by the existence of a separating axis
               (dashed red line) that passes through one vertex of each pentagon (red
               dots). (b) A hypothetical situation of overlapping pentagons. No axis,
               and particularly no axis passing through one vertex of each pentagon,
               separates the two sets of vertices. (c) For the input pentagons in (b),
               the subset S = T (red dots) that minimizes δ(S )2 , the sum of squared-
               distances to the least-squares axis (dashed red line) while satisfying
               that the latter separates the remaining vertices. (d) Another choice
               of S that yields a valid separating axis, but a larger sum of squared-
               distances. (e) A choice of S that yields an axis that fails to separate
               the remaining vertices. (f) Using T found in (c), the output of the pro-
               jection to the exclusion constraint is determined by moving the points
               of T onto their least-squares axis. (g) The output (solid line) of the
               rigidity projection for the input pentagons (dashed) in (b).


tion acts independently on each replica pair, and since the metric weight of all variables

specifying one replica pair are equal, the metric weights have no influence on this pro-
jection. The action of this projection is illustrated in Figure 3.2. For the kissing number
problem, the first case of (3.3) is also used if the replica pair is one of the pτtarget closest
replica pairs.




                                              45
Convex polytope packing


Although identifying and resolving overlaps between two spheres is straightforward, the
same task is more challenging in the case of other convex objects, where more degrees
of freedom come into play. The literature on the topic of detecting overlaps (colli-

sions) between polyhedral solids is extensive (driven in part by applications in computer
graphics), and many efficient techniques exist for checking whether two convex polyhe-
dra, conv X1 and conv X2 , overlap (see e.g., [72, 10]). In our case, as we are interested
in computing the projection to the exclusion constraint, we also need to determine the

distance-minimizing resolution of the overlap. That is, we must find the smallest dis-
placement of the vertices such that the new polyhedra do not overlap. As far as we have
been able to determine, there is not an established, efficient computational method de-
veloped for this specific problem. The method we provide here is efficient enough for

the purpose of packing polyhedra with a small number of vertices, but the computation
time required grows exponentially with the number of vertices. A more efficient reso-
lution method for particles with more vertices and for smooth particles is currently in
development.


   The method relies on the separating plane theorem: the convex hulls of two sets of
vertices in Rd do not overlap if and only if there is a (d − 1)-dimensional plane that

separates the two sets, so that each is contained in a different half-space. The theorem
can be made even stronger by specifying that the separating plane can always be chosen
to contain d vertices from the given sets, including at least one from each. Therefore,
one can check whether two polytopes overlap by checking whether they are separated by

any of the planes defined by any such subset of vertices (Figure 3.3a–b). If the polytopes
are non-overlapping, the resolution leaves the vertices unchanged.


   If the polytopes overlap, we must find the smallest displacement of their vertices


                                           46
that resolves the overlap. In the resolved configuration there is a separating plane, V sp =
{r ∈ Rd : n̂sp · r = h sp }, that separates the two sets of vertices. As a consequence of
distance minimization, the only vertices moved in the course of the resolution are the
vertices which lie on V sp in the resolved configuration. Let T and T ′ be the pre- and

post-resolution positions, respectively, of those vertices that are displaced during the
resolution. Therefore, T ′ is the set of points in V sp closest to the points of T :

                         T ′ = {r + (h sp − r · n̂sp )n̂sp : r ∈ T } ⊆ V sp .          (3.26)

The squared norm of the resolution displacement is
                                       X
                                             (h sp − r · n̂sp )2 .                     (3.27)
                                       r∈T



    For any set of points S there is at least one plane V = {r ∈ Rd : n̂ · r = h} that
minimizes the sum of squared distances
                                         X
                                          (n̂ · r − h)2 .                              (3.28)
                                          r∈S

We call such a plane a least-squares plane of S . The separating plane of the resolved
configuration is always a least-squares plane of T . If this were not the case, a small
tilting of the separating plane towards such a least-squares plane (with a corresponding

movement of the points in T ′ ) would result in a resolution by a smaller displacement. In
order to resolve an overlap between polytopes conv X1 and conv X2 , we therefore have
to solve a discrete problem: among all subsets S of X1 ∪ X2 with a least-squares plane
separating the remaining vertices X1 \ S from X2 \ S , find the one with the minimal sum

of squared distances (3.28). This is the set T (Figure 3.3c–f).

    The least-squares plane Vls of a set S is determined by minimizing the sum of

squared distances (3.28). Note that for a fixed normal direction n̂, the value of h that
                                          P
minimizes the sum is h = n̂ · r, where r = r∈S r/|S | is the centroid of S . Therefore, we


                                                   47
wish to minimize
                                                                         
                       X                             X                   
                             [n̂ · (r − r)]2 = n̂  (r − r)T (r − r) n̂T ,
                                                     
                                                                                            (3.29)
                       r∈S                              r∈S

the minimum of which is equal to the smallest eigenvalue of the symmetric matrix
P            T
  r∈S (r − r) (r − r). The minimum is realized when n̂ is the corresponding eigenvector.

Degenerate cases with equal lowest eigenvalues occur, but they do not pose a problem:
whenever an optimal separating plane occurs as a degenerate least-squares plane of some
set S , its degeneracy implies that there is a least-squares plane of S which also includes

an extra vertex; this plane will be equally optimal and will occur as a less degenerate
least-squares plane of a superset S ′ ⊇ S . Therefore, the optimal least-squares plane
always occurs as a non-degenerate least-squares plane of a set S .


   To summarize, the overlap detection and resolution algorithm consists of three steps
(illustrated in Figure 3.3a–f):


   1. Consider all subsets S ⊆ X1 ∪ X2 of size |S | = d with at least one point from each
      polytope. Let V = {r ∈ Rd : n̂ · r = h} be a plane that includes S . For each S let
                                    X                    X
                         ∆2+ (S ) =      (n̂ · x − h)2 +   (n̂ · x − h)2 ,           (3.30)
                                           x∈X1                       x∈X2
                                          n̂·x>h                     n̂·x≤h
                                          X                          X
                             ∆2− (S ) =            (n̂ · x − h)2 +        (n̂ · x − h)2 ,   (3.31)
                                           x∈X1                       x∈X2
                                          n̂·x≤h                     n̂·x>h

                                     ∆2 (S ) = min(∆2+ (S ), ∆2− (S )),                     (3.32)

      and let

                                                   ∆2 = min∆2 (S ).                         (3.33)
                                                            S

      ∆2 provides a measure for the interpenetration of the two polytopes. If ∆2 = 0,
      then a separating plane exists, the input polytopes do not overlap, and the algo-

      rithm ends here by returning the original vertex positions X1 and X2 . If ∆2 > 0,
      the polytopes overlap and the algorithm continues to Step 2.


                                                       48
   2. Consider all subsets S ⊆ X1 ∪ X2 of size |S | > d with at least one point from
      each polytope. Let V = {r ∈ Rd : n̂ · r = h} be a least-squares plane of S . If the
      plane separates the vertex sets with the points of S removed — X1 \ S and X2 \ S
      — let δ2 (S ) be the sum of squared-distances from S to the plane. Otherwise, let

      δ2 (S ) = ∞. Among the subsets S considered, let T be the subset that minimizes
      δ2 (S ) and VT = {r ∈ Rd : n̂T · r = hT } be its associated least-squares plane. As
      δ2 (S ) < ∞ if S contains all vertices, the minimum is always finite. Continue to
      Step 3.

   3. The sets of vertices returned are given by X1′ and X2′ , wherein x′ ∈ X1′ ∪ X2′ is given
      by                         
                                 
                                 
                                 x                         if x < T
                                 
                                 
                                 
                               ′
                                 
                              x =
                                                                                      (3.34)
                                 
                                 x + (hT − x · n̂T )n̂T    if x ∈ T ,
                                 
                                 
                                 

      where x ∈ X1 ∪ X2 is the corresponding original vertex position.


    The projection πD (X) to the “divide” constraint (3.24), of an input matrix X com-
prised of pairs of vertex matrices X2i−1 and X2i , is then achieved by applying the above
algorithm independently to all i = 1, . . . n pairs.




3.5.2 “Concur” projections


Lattice constraint


All the “concur” constraint sets described in this paper are of the form


                            C = A(K) = {X = AM ∈ Ω : M ∈ K}                            (3.35)




                                              49
where A is constant, and M is variable, but must satisfy a constraint M ∈ K. The
projection then is given by
                                    πC : X 7→ X′ = AM,                            (3.36)

where M realizes the minimum over K of the distance
                                                            
                     ||X − X ′ ||2 = trace W(X − AM)(X − AM)T .                   (3.37)


   Absent any constraints on M (as for example in the “concur” constraint for the kiss-

ing number problem, where K = Ψ), the solution would be given by

                               M = (AT WA)−1 AT WX.                               (3.38)

This can easily be seen by writing M = M + δM, which gives
                                                              
                      ||X − X ′ ||2 = trace W(X − AM)(X − AM)T

                                   = c + trace(WA δM δMT AT )

                                   = c + trace(W′ δM δMT ),                       (3.39)

where W′ = AT WA and the constant term c does not depend on δM. The second term
is non-negative, and when M is unconstrained, (3.39) is minimized by letting M = M.
Additionally, we have just reduced the constrained case to the problem of finding M ∈ K
that minimizes the cost function
                                                        
                         f (M) = trace W′ (M − M)(M − M)T .                       (3.40)


   This projection strategy parallels the two-step strategy used in Section 3.3.1. First,
the formal configuration X is projected to the range A(Ψ) of the physical configuration
space, giving AM. Then, the projection of M to the additional constraint K is performed
in the physical configuration space using the metric induced on its image in the formal

configuration space. Below, we solve the second step of this projection problem for
various constraints K.


                                            50
Density constraint


In the “concur” constraint for the sphere packing problem, the only constraint on the
generating matrix is the density constraint. The set of generating matrices M satisfying
the density constraint is


                             Kdensity = {M : | det M0 | ≤ Vtarget },                   (3.41)


where M0 is the generating matrix of the lattice and is given by the first d rows of M. If
| det M0 | ≤ Vtarget , then the projection to the constraint (the choice of M that minimizes

the cost function (3.40)) is trivially M = M. Otherwise, since M1 is unconstrained,
we can minimize (3.40) with respect to M1 for a given M0 . This yields M1 = M1 −
W′ −1  ′                     ′                             ′
   11 W10 (M0 − M0 ), where WIJ are the block-elements of W acting on M I to the left

and on M J to the right. Thus, the cost function for M0 is simply

                                                               
                       f (M0 ) = trace W′′ (M0 − M0 )(M0 − M0 )T ,                     (3.42)


where W′′ = W′00 − W′01 W′ −1  ′
                           11 W10 .



   The projection becomes easier to analyze in terms of the matrix L = (W′′ )1/2 M0 .
The cost function then takes the form of the simple Frobenius distance

                                                          
                              f (L) = trace (L − L)(L − L)T ,                          (3.43)


and the density constraint is still in the form

                                                   ′
                                       | det L| ≤ Vtarget ,                            (3.44)

       ′
where Vtarget = Vtarget /| det W ′′ |1/2 . Since the absolute value of the determinant of L is
given by the product of its singular values, the solution to this minimization problem is
given by a matrix L = UΣV with the same (right and left) singular vectors as the matrix



                                               51
L = UΣV, but different singular values. The cost function expressed in terms of the
singular values σi and σi of, respectively, L and L takes the form
                                            d
                                            X
                                  f (Σ) =         (σi − σi )2 .                   (3.45)
                                            i=1

We numerically minimize this quadratic function subject to the density constraint (3.44).
Through back substitution we then have the matrix M that minimizes (3.37) and πC (X) =
X′ = AM.



Rigidity constraint


In the “concur” constraint for the polytope packing problem, an additional constraint on
the generating matrix M is that the primitive polytopes that make up M1 are congruent
with a given polytope. The generating matrix is then constrained to the set

                                  K = Kdensity ∩ Krigidity                        (3.46)

where

                          Kdensity = {M : | det M0 | ≤ Vtarget },

                          Krigidity = {M : Y = Y(0) Ri + cT ti

                                       for all p rows Y of M1 }.

To calculate the projection πC (X), the cost function (3.40) must be minimized over K.
However, since the off-diagonal block W′01 couples the lattice parameters M0 to the
primitive particle parameters M1 , this minimization is complicated. Instead of exact

minimization, we employ a two-step heuristic method, which results in an approximate
projection.


   In the first step, we calculate the matrix M′ ∈ Kdensity that minimizes the cost func-
tion, as in Section 3.5.2. Then, in the second step, we calculate the matrix M ∈ K by


                                             52
applying to each row Y of M′1 the smallest change so that it becomes a vertex matrix of a
polytope congruent with the reference polytope. The second step is achieved by finding
the rigid motion applied to the reference polytope which brings its vertices as close as
possible to the vertices of Y as measured by the sum of squared distances (Figure 3.3g).

The problem of finding the rigid motion that brings one given list of points closest to
another given list, sometimes known as the problem of absolute orientation, occurs fre-
quently in a variety of fields (e.g., in calculating RMSD between two conformations of
a biomolecule) and several efficient methods for its solution have been developed (see

[39, 40]).


   The output of the approximate projection is then given by X′ = π̃C (X) = AM ≈
πC (X). As X′ ∈ C, the approximate projection gives a configuration in the constraint
set, but might not give the closest one to the input configuration. We justify the use of the
approximate projection by noting that it is an exact projection if the off-diagonal block

W′01 is zero. A non-zero off-diagonal block is the result of correlations in the relevant
exclusion constraint vectors b between the coefficients of lattice translations and the
coefficients of primitive particle vertex positions. We expect these coefficients to give
uncorrelated contributions and to add up to small off-diagonal elements due to random

cancellations. Indeed, we find that the off-diagonal block is small in comparison with
the diagonal blocks, and we expect our heuristic to yield a good approximate projection.




3.5.3 Formal configuration space maintenance


In our discussion of the choice of metric in Section 3.4, we discussed the ideas of dy-
namically readjusting the metric (through the weights wi of the various replicas) and of

removing and adding replicas (removing replicas is formally equivalent to setting their



                                             53
weight to zero). The latter is necessary for implementation reasons: there are infinitely
many independent exclusion constraints (and therefore replicas), but we can only repre-
sent a finite number of replicas in our implementation. As the set of relevant constraints
changes over the course of the search, we must remove and add replicas. Our criterion

for which replicas to represent is based on the difference map’s current “concur” esti-
mate: we include a replica pair for each pair of particles whose centroids in the “concur”
estimate are closer than some cut-off distance. Using the generating matrix obtained in
the “concur” projection we can easily find all such pairs using the method of Agrell et

al. [1]. The cut-off distance is chosen so that at least all replicas that might be in risk of
overlap are represented.


    The problem of implementation is not the only reason we wish to limit the number
of replicas we represent. A proliferation of unnecessary replicas has the adverse effect
of attenuating the information obtained from the “concur” projection by diluting the

influence of more critical replicas. We observe that such replica proliferation could
result not only in a slower search, but also in an increased tendency to become trapped
in local optima. Limiting the number of replicas is one way to avoid this effect, but
we find it useful to further amplify the information from critical constraints by giving

them greater weights [30]. We perform the weight adjustments adiabatically, that is,
slowly over the course of many iterations, by updating the weights of each replica pair
according to the rule
                                           τwi + w′i (Xc )
                                    wi →                   ,                           (3.47)
                                               τ+1
where w′i (Xc ) is a function that assigns replicas weights based on their configuration
in the “concur” estimate, and τ is a relaxation time for the replica weights in units of
iterations.


    In the sphere packing problem (in d dimensions, with unit spheres), we choose the



                                              54
weight function to be
                                    
                                                 2
                                      eα(4−||xi || )
                                    
                                                            if ||xi || ≤ 2
                                    
                                    
                                    
                        w′i (Xc ) = 
                                    
                                                                                     (3.48)
                                    
                                    
                                    
                                    (||xi ||2 − 3)−2−d/2   if ||xi || > 2,
                                    
                                    
                                    

with α ≈ 20. The dimensional dependence is chosen so that under the assumption of uni-

form density, the total weight from replicas over a certain distance follows a dimension-
independent power law. In the polytope packing problem, we similarly use
                          
                          
                            α∆2i
                          
                          e                    if the polytopes overlap
                          
                          
                          
                 ′
                          
               wi (Xc ) = 
                                                                                    (3.49)
                          
                          (1 + ri2 − 4rin2 )−2 if not,
                          
                          
                          

with α ≈ 10, where rin is the inradius of the polytope, ri is the centroid-centroid distance
of the polytopes, and ∆2i is the measure of the overlap between the polytopes defined in
(3.33).


   In addition to the maintenance of replicas, which is performed after every iteration
of the difference map, we also periodically perform a lattice reduction using the LLL
algorithm [50]. The lattice generated by M0 is re-represented using the LLL-reduced

generating matrix M′0 = G0 M0 , where G0 is a unimodular integer matrix. Additionally,
                                                                               P
all primitive particles whose centroids are outside of the unit cell given by { i λi ai : −
1/2 ≤ λi < 1/2} are re-represented by their lattice-translate in that cell. In summary, the
new packing generating matrix M′ is given by
                                                       
                                               G 0 
                                                 0
                                M′ = GM = 
                                                        
                                                           M,                       (3.50)
                                                 G 1 
                                                   1


where G1 gives the lattice translations to be applied to the primitive particles. Since
the actual positions of the particles, as represented in the matrix X = AM, should be
unchanged, the lattice reduction must also be applied to the nominally constant matrix
A (A → A′ = AG−1 ).


                                               55
3.6 Results



3.6.1 Sphere packing


Using the PDC scheme described in the previous sections we perform a de novo search

for the densest lattice (p = 1) sphere packings in dimensions 2—14. The PDC search,
starting from random initial configurations, was able to reproduce the densest packing
lattices known for all cases, and the results of the search are summarized in Table 3.2.
For dimensions 2—8 the lattices are known to be optimal, and for dimensions 9—14

these results are, to our knowledge, the first numerical evidence from a de novo search
that the known lattices are optimal.


   Note that the number of replicas is determined by the number of near neighbors of
each sphere, which rises rapidly with the number of dimensions. This rise causes an
increased computational storage cost per physical degree of freedom in a PDC search,

compared to a constant storage cost per physical degree of freedom in a method in-
volving a local search in the physical configuration space. However, this rise need not
affect the scaling of CPU costs, since both search methods need necessarily check a
comparable number of particle pairs for possible overlaps.


   In dimensions d = 10, 11, 13 there are known non-lattice packings with p =
40, 72, 144 respectively that are denser than the densest known lattices [16]. In up to

11 dimensions, we searched for non-lattice packings with as many as p = 12 primitive
spheres, but the searches did not produce packings denser than the lattice packings. For
a density target matching the lattice density, the searches reproduced the lattice packing,
suggesting that the lattice packing in these dimensions is the optimal packing with a

small number of spheres in the unit cell.



                                            56
          d    Λdensest   φ(L)
                           densest    hNiter i    hni       titer    success rate
          2    A2         0.90690     42          11        0.1ms    100/100
          3    D3         0.74047     230         38        0.2ms    100/100
          4    D4         0.61685     191         127       0.4ms    100/100
          5    D5         0.46526     308         323       1ms      100/100
          6    E6         0.37295     173         977       2ms      100/100
          7    E7         0.29530     217         2740      5ms      96/100
          8    E8         0.25367     99          8528      20ms     96/100
          9    Λ9         0.14577     161         16314     30ms     85/100
          10   Λ10        0.092021    394         31433     70ms     47/100
          11   K11        0.060432    421         68722     0.3s     54/100
          12   K12        0.049454    397         204321    0.9s     55/100
          13   K13        0.029208    577         430796    2s       25/100
          14   Λ14        0.021624    1652        1007250   6s       4/10
  Table 3.2: Results of PDC searches for dense lattice packing in dimensions d =
             2, . . . 14. For each dimension, 100 runs from random initial conditions
             were performed with the density target φtarget = φ(L) densest , the density of
             the densest known lattice Λdensest [16]. The runs were limited to 5000
             iterations, and the number of converged runs is quoted in the right-most
             column. For dimensions 10 and above, each run was first allowed to
             converge at a density target of 0.8φdensest and then continued with the fi-
             nal target. The mean number of difference map iterations in converged
             runs was hNiter i, and the mean number of relevant exclusion constraint
             used was hni. Each iteration took an average runtime of titer on a sin-
             gle 3 GHz CPU. In d = 14 only 10 runs were performed with three
             intermediate targets.


3.6.2 Kissing number


For the kissing number problem, PDC searches were able to reproduce the best known

lattice kissing arrangements in dimensions 2—11. In dimensions 2—9, the result is
known to be optimal, and for dimensions 10 and 11, we are not aware of previous
numerical evidence for their optimality. Table 3.3 summarizes the performance of our
method.




                                             57
                  d    Λhighest   τ(L)
                                   highest   hNiter i   hni     success rate
                  2    A2         6          27         12      100/100
                  3    D3         12         54         40      100/100
                  4    D4         24         132        118     98/100
                  5    D5         40         163        331     94/100
                  6    E6         72         225        928     64/100
                  7    E7         126        597        2729    66/100
                  8    E8         240        511        6988    55/100
                  9    Λ9         272        350        15604   63/100
                  10   Λ10        336        438        32203   28/100
                  11   Λ11        438        549        73766   10/100
   Table 3.3: Results of PDC searches for lattice packing with high kissing num-
              ber in dimensions d = 2, . . . 11. For each dimension, 100 runs from
              random initial conditions were performed with a target coordination
              τtarget = τ(L)
                         highest , the highest coordination number known for a lattice
              of that dimension, Λhighest [16]. The runs were limited to 5000 iter-
              ations, and the number of converged runs is quoted in the right-most
              column. The mean number of difference map iteration in converged
              runs was hNiter i, and the mean number of relevant exclusion constraints
              used was hni.


3.6.3 Polytope packing


By inspection of a packing of regular tetrahedra yielded by our numerical search during

early phases of its development, we were able to construct a new transitive, periodic (p =
4) packing of tetrahedra with a higher density (φ ≈ 0.8547) than previously reported
[46]. This packing takes the form of a double lattice of bipyramidal dimers (the union of

two face-sharing tetrahedra). The packing has since been slightly improved to a closely
related, but less symmetric packing with density φ ≈ 0.8563 [70, 13]. In its current form,
our search method is able to reproduce this densest known packing reliably (fifteen out
of a hundred runs converged within the iteration limit), and Figure 3.4 shows the results

of a sample run converging to this packing.

   For the problem of packing regular four-dimensional simplices (pentatopes) in four-



                                               58
              2

                                                          iteration
              0
                           10 000       20 000                30 000   40 000

             -2


             -4


             -6                                          1+log10 Ε2


             -8
                                                 log10 SDi2

            -10



   Figure 3.4: The course of a sample run searching for dense periodic packings
              (p = 4) of unit edge-length regular tetrahedra. The plot shows ∆2i ,
                                                                                  P
              a measure of the total interpenetration between tetrahedra in the “con-
              cur” estimate (lower blue line, defined in (3.33)), and ǫ 2 , the squared
              distance between the “divide” and “concur” estimates (upper purple
              line, shifted up for clarity), both on a logarithmic scale. The density
              target for the search is started at φtarget = 0.75 and adjusted when the
              search is converged on a solution (vertical red lines) to φtarget = 0.82
              (at iteration 15751) and then to φtarget = 0.8563 (at iteration 15898).
              Each iteration took 14 millisecond on average on a single 3 GHz CPU.


dimensional Euclidean space, we report a new packing discovered by our search method
(Figure 3.5). This packing, with density φ = 128/219 ≈ 0.5845, is, to our knowledge,
denser than any previously reported packing of regular pentatopes. Like the densest
known tetrahedron packing, this packing also takes the form of a double lattice of dimers

(a dimer here is the union of two cell-sharing pentatopes). This structure, composed of a
repeating unit of two oppositely oriented dimers, repeatedly came up as the densest in de
novo PDC searches with p = 4 and p = 8 pentatopes in the unit cell, whereas searches
with intermediate values of p yielded sparser packings. We subsequently refined the

packing with a restricted search where the dimer was taken as the basic particle.


   Note that the density reported is slightly lower than that of the densest known pack-


                                           59
   Figure 3.5: Lower dimensional cuts through dense packings of tetrahedra and
              pentatopes. The top figure shows a two-dimensional cut through the
              densest known packing of tetrahedra. The plane of the cut is parallel to
              the bases of the bipyramidal dimers. Triangular sections from dimers
              of one orientation (red triangles pointing right) and from dimers of
              inverted orientation (blue triangles pointing left) are visible. The bot-
              tom figure shows a three-dimensional cut through the densest known
              packing of pentatopes. The cut is taken parallel to the bases of the
              pentatope dimers, and tetrahedral sections from the two dimer ori-
              entations (tetrahedra with fore-facing edges oriented in perpendicular
              diagonal directions) are visible.


ing of four-dimensional spheres (φ = π2 /16 ≈ 0.6169). It remains to be determined
whether this is the case because the optimal packing density of pentatopes is smaller
than that of spheres or because the dimer double lattice is suboptimal. The vertex coor-

dinates of the four primitive pentatopes and the generating matrix of the lattice are given
in Table 3.4.




                                            60
                primitive pentatopes    K1 = conv{r1 , r2 , r3 , r4 , r5 }
                                        K2 = conv{r2 , r3 , r4 , r5 r6 }
                                        K3 = t − K1
                                        K4 = √  t − K2
                                where   r1 = 5(1, 1, 1, 1)
                                        r2 = (3, −1, −1, −1)
                                        r3 = (−1, 3, −1, −1)
                                        r4 = (−1, −1, 3, −1)
                                        r5 = (−1, √ −1, −1, 3)
                                        r6 = − 5(1, 1, 1, 1)√
                                        t = 41 (−7, 1, 3, 3) − 45 (1, 1, 1, 1)
                lattice                 Λ = Z4 M 0
                                                                             
                                                         −6 10 −6 2 
                                                           −8 −4 4 8 
                                where   M0 = 14                          
                                                             −7 5 9 −7 
                                                                 1 −7 9 −3
                                                                      
                                                   2 2 2 2 
                                              √     2 2 2 2 
                                                5
                                          + 4                      
                                                      1 1 1 1 
                                                               3 3 3 3
   Table 3.4: Coordinates of the densest pentatope packing discovered by the PDC
              search (φ = 4 vol(K1 )/ det(M0 ) = 128/219 ≈ 0.5845).


3.7 Conclusion


In this article we report on the development of PDC, a novel, constraint-based method
for discovering dense periodic packings through de novo numerical searches. We lay
out the principles of the method and demonstrate its application for selected problems.

In addition to the dense packing of regular tetrahedra reported in Ref. [46], we also
discover a new dense packing of regular pentatopes using the PDC method. We also
use the method to numerically recover the lattice sphere packings of highest known

density and highest known kissing number in a range of dimensions, providing empirical
evidence of their optimality.


   In developing the PDC scheme, we adapt the D − C framework to periodic systems.


                                            61
PDC retains the mindset of the traditional D − C approach of Ref. [30], but generalizes
its formalism in a few ways. We introduce an expanded configuration space parameter-
ized by linear combinations of the original parameters, such that these new parameters
over-determine the configuration. Therefore, by contrast with the traditional construc-

tion, where new parameters are, specifically, redundant copies of original parameters
and concurrence is described by the equality of all copies of a given original parameter,
here we allow concurrence to be described by a general linear relation. With this gen-
eralization, we can treat the periodic images of a particle as “replicas” of the particle,

even as they are related by a lattice vector instead of being identical. Thus, the vari-
ables describing the periodic repetition of the configuration, namely the lattice vectors,
are not imposed as constants or adjusted in dedicated steps. Instead, due to the projec-
tion formulation of the dynamics, the unit cell variables that minimize the change to the

configuration are determined at each iteration. These variables are treated on the same
footing as particle positions and orientations and are optimized as aggressively.


   Additionally, we develop a displacement-minimizing overlap resolution algorithm
for the convex hulls of two sets of points in Rd . We use this algorithm to implement the
projection to the exclusion constraint in the case of polytopal particles.


   Unlike Monte Carlo simulations, which explore the physical optimization land-
scape using stochastic moves, a PDC search uses a deterministic map in an expanded,

non-physical configuration space. As such, it is useful when interest lies more in
discovering optimal configurations and less in discovering the physical pathways to
such configurations. This is also the viewpoint espoused by the so-called ”geometric-
structure” approach, which emphasizes characterizing structures, without inordinate re-

gard to physically-inspired methods for obtaining them [71]. Moreover, introducing
non-physical dynamics has been observed to be important in overcoming dynamical




                                            62
stagnation [33]. The projection-based dynamics make PDC particularly well-suited in
problems with hard constraints, such as hard particle packing, or with step potentials,
which prohibit the use of gradient information.


       While no direct comparison has been made between the performance of PDC and
Monte Carlo searches in the case of periodic packing problems, difference map and

D − C methods in the case of other problems have been shown to perform better than or
on a par with specialized and general-purpose methods [23, 30, 29, 22]. The generality
of the PDC scheme and its demonstrated ability to discover dense packings in a variety
of settings indicate its utility as a general method for conducting de novo numerical

searches and as a possibly attractive alternative to conventional methods 1 .

       Y. K. acknowledges N. Duane Loh for valuable discussions. This work was sup-

ported by grant NSF-DMR-0426568.




   1
       An implementation of our algorithm is available upon request from the corresponding author.


                                                    63
                                      CHAPTER 4
DENSE PACKING CRYSTAL STRUCTURES OF PHYSICAL TETRAHEDRA



   The contents of this chapter have been published in Physical Review E with coauthor
Veit Elser [45].


4.1 Abstract


We present a method for discovering dense packings of general convex hard particles

and apply it to study the dense packing behavior of a one-parameter family of particles
with tetrahedral symmetry representing a deformation of the ideal mathematical tetrahe-
dron into a less ideal, physical, tetrahedron and all the way to the sphere. Thus, we also
connect the two well studied problems of sphere packing and tetrahedron packing on a

single axis. Our numerical results uncover a rich optimal-packing behavior, compared to
that of other continuous families of particles previously studied. We present four struc-
tures as candidates for the optimal packing at different values of asphericity, providing
an atlas of crystal structures which might be observed in systems of nano-particles with

tetrahedral symmetry.




4.2 Introduction


Impenetrable (hard) mathematical bodies (e.g. spheres, spheroids, superballs, and poly-
hedra) have received much attention as models for the equilibrium behavior of systems

of nano-particles and for the wealth of equilibrium and non-equilibrium structures they
exhibit [19, 44, 4, 28, 69, 68]. For the tetrahedron alone, quasicrystal structures, novel
crystal structures, and glassy structures have been reported in numerical simulations


                                           64
[69, 68, 46, 33, 13]. However, in all cases, the tetrahedral particles studied were mathe-
matically ideal (polyhedral) tetrahedra. By contrast, in an experiment which found that
regular tetrahedra have random packings that are denser than observed for any other
body, the tetrahedral macro-particles (dice) used had rounded edges and vertices [43, 2].

Tetrahedral nano-particles used as colloids are not only imperfectly-shaped tetrahedra,
but are also sometimes soft, in the sense that the interactions beyond hard-core repul-
sion are significant [31, 66, 59, 3]. In this paper, we attempt to characterize the packing
behavior of physical, rather than mathematical, tetrahedra by studying a one-parameter

family of particles with tetrahedral symmetry that interpolates between the mathemati-
cal tetrahedron on one end of the parameter’s range and the sphere on the other end. We
explore the effect of this parameter by constructing, using a de novo numerical search,
candidate structures for the optimal packing of the different particles in the family.


   A particle interpolating between the sphere and the regular tetrahedron can be

achieved by a variety of constructions. The simplest construction, probably, is to place
the centers of four unit spheres at the vertices of a regular tetrahedron with edges of
length a and consider the volume at the intersection of all four spheres. We call the re-
sulting figure a tetrahedral puff (Figure 4.1). For a special value of a, the tetrahedral puff

is the Reuleaux tetrahedron (a three-dimensional version of the Reuleaux triangle, but
not a solid of constant width) [53]. A more convenient parameter than this edge length
is the asphericity γ, which is the ratio between the radii of the particle’s circumscribing
and inscribed spheres. The value γ = 1 obtained when the four spheres coincide cor-

responds to a sphere. The value γ = 3, which is the largest asphericity possible for a
convex particle with tetrahedral symmetry and corresponds to a regular tetrahedron, is
obtained in the limit that the four spheres intersect at a point. The Reuleaux tetrahedron
                                       √
is the puff with asphericity γ = (3 + 24)/5 ≈ 1.58.




                                             65
   Figure 4.1: Tetrahedral puffs of varying asphericity. From left to right, the as-
              phericities of the puffs shown are γ = 4/3, 2, 8/3.


4.3 Methods


To efficiently search for candidate optimal packing structures we run a numerical search
for packings at increasing densities. To prevent overlaps between different particles
in the structure we employ an overlap resolution step. In a packing of congruent par-
ticles, every particle can be obtained from a single primitive particle K by a rotation

and a translation: K1 = R1 K + r1 = {R1 x + r1 |x ∈ K}, where R1 , a rotation matrix,
and r1 , a translation vector, parameterize the configuration of the particle K1 . We call
an exclusion projection the operation of, for any two particles K1 and K2 that over-
lap, identifying the new set of configuration parameters (R′1 , R′2 , r′1 , r′2 ) that resolves the

overlap while minimizing the distance in configuration-space from the original config-
uration, (R1 , R2 , r1 , r2 ). This is the projection in configuration-space to the set of non-
overlapping configurations. Below we give the method of implementing this projection.


    At high densities, however, we may have to resolve overlaps of a particle with mul-
tiple other particles, and the projection that applies to pairs cannot be used directly.

Therefore, we introduce multiple independent copies (replicas) of the configuration pa-
rameters of each particle, so that after an exclusion projection, any pair of particles will
have at least one overlap-free pair of replicas. Another projection ensures that in the
final structure obtained from the search all replicas of a single particle agree on its con-

figuration. The two projections are not applied alternately, but instead composed with


                                                66
linear combinations to give the difference map iteration [23]. This scheme, called divide
and concur (D − C), has previously allowed us to study dense packings of a variety
of polyhedral and high-dimensional spherical particles, and is here generalized to any
convex particle. Apart from the exclusion projection, described here, the rest of the

application of the scheme to dense periodic packing discovery is described in Ref. [47].


    Given a pair of particles (or replicas) in a configuration (R1 , R2 , r1 , r2 ) which over-
laps, the exclusion projection resolves the overlap by identifying a new set of configu-
ration parameters (R′1 , R′2 , r′1 , r′2 ) while minimizing the distance to the original configu-
ration as defined by
                                      X
                               d2 =           ||ri − r′i ||2 + ||Ri − R′i ||2 ,            (4.1)
                                      i=1,2

where the matrix norm is the Frobenius norm. The projection algorithm for a general
convex particle is most easily expressed in terms of the particle’s support function h(u) =

maxx∈K u · x. If the support function h(u) of K is known, then the support function of Ki
is hi (u) = maxx∈K u · Ri x + u · ri = h(RTi u) + u · ri [61].


    By the separating plane theorem, K1 and K2 do not overlap if and only if a vector u
exists such that ∆h(u) = h1 (u) + h2 (−u) ≤ 0 [61]. We can determine if such a vector
exists by numerically minimizing ∆h(u)/||u||, which is bounded and attains a minimum
over u. If the minimum value of ∆h(u)/||u|| is positive, we must make the minimal

change possible to the configuration parameters so that


                               h′1 (u) + h′2 (−u) = 0 for some u.                          (4.2)


    If we relax the condition that R′i is a rotation matrix, then we can reduce this con-
strained optimization problem to a simple unconstrained optimization problem in three

vector variables. Namely, these vectors are u, v1 = R′T             ′T
                                                     1 u, and v2 = R2 u. Given these




                                                      67
three vectors, the new configuration parameters which minimize (4.1) and satisfy (4.2)
are given by

                                               u
                                 r′1 = r1 −          ∆h                             (4.3a)
                                            2||u||2
                                               u
                                 r′2 = r2 +          ∆h                             (4.3b)
                                            2||u||2
                                              u
                                 R′i = Ri +       2
                                                    (vTi − uT Ri ),                 (4.3c)
                                            ||u||

where ∆h = h(v1 ) + h(−v2 ) + (r1 − r2 ) · u and the configuration distance is given by

                               ∆h2 /2 + ||uR1 − v1 ||2 + ||uR2 − v2 ||2
                        d2 =                                            .            (4.4)
                                               ||u||2

And so, we have reduced the problem, as promised, to an unconstrained minimization
of (4.4) over three vector variables. Note that (4.4) is invariant under uniform positive

rescaling of u, v1 , and v2 , and the resulting vanishing gradient direction must be taken
into account when performing the minimization.


   The restriction on Ri to be a rotation matrix, i.e. the requirement on the rigidity
of the particle, as in Ref. [47], is restored in the concurrence constraint of the D − C
scheme. The projection of a general matrix into the subset of orthogonal matrices is as

simple as taking its singular value decomposition and setting all the singular values to
unity [37].


   As a method for exploring dense configurations of general hard particles, we believe
our projection-based method to be more direct and efficient when compared to event-
driven MD simulations and stochastic MC methods [44]. Partly, the D−C scheme draws
its power from temporarily allowing non-physical configurations, with overlaps, non-

concurring replicas, and non-rigid particles, but then systematically acting to minimize
these non-physicalities. In MC simulations, such temporary allowance has also been
observed to be critical in efficiently exploring structures at high density [33].


                                                68
4.4 Results


For a selection of puffs of different asphericities, we use the D − C scheme to perform
repeated de novo searches for periodic packings with p = 1, 2, 3, 4, 6, and 8 puffs per unit
cell. The densest packing found for each value of γ is reported here as a candidate for
the optimal packing structure. Every packing density that is reported here as putatively

optimal for a puff of some asphericity has been reproduced by the numerical search at
least 3 times from random initial conditions and if the structure has two puffs in the
primitive unit cell, it has been reproduced in searches with both p = 2 and p = 4.


   As suggested by the results of our numerical searches, four different packing struc-
tures are optimal at different asphericities, separated by one continuous structural tran-

sition and two abrupt ones. Of most interest are the structures of the optimal packing for
puffs of small asphericity and large asphericity in the parameter ranges near the sphere
and the tetrahedron respectively. The optimal packing structure for small asphericity,
which we call the S0 -structure (for simple double lattice), is a tetragonal double lattice

– that is, the union of two lattices (with one particle per unit cell) that are related to each
other by an inversion about a point (Figure 4.2) [49]. In the S0 -structure, the puffs are
arranged into square layers so that from each layer, the puffs stick out on one side in
parallel ridges running in one direction and on the other side in parallel ridges running

in a perpendicular direction. By stacking each consecutive layer with a 90◦ rotation,
the ridges of one layer align with the ridges of the layer above it. In the limit γ → 1,
each layer approaches a square packing of spheres, and the S0 -structure approaches the
face-centered cubic sphere packing structure.


   For large asphericities, the optimal packing structure, which we call the D0 -
structure, is a dimer double lattice (i.e. each of the two inversion-related lattices is a



                                              69
   Figure 4.2: A unit cell of each of the four structures described, (from left to right)
               the S0 -, D1 -, S1 -, and D0 -structures. For the S0 - and S1 -structure, a
               unit cell consisting of two primitive unit cells is shown. In all cases,
               the purple (top-left) and pink (bottom-left) puffs are related by inver-
               sion to the green (bottom-right) and teal (top-right) puffs respectively.
               The S0 -structure is a body-centered tetragonal crystal where the body-
               centered puff is inverted in orientation from the corner puffs. The D1 -
               structure occurs when next-nearest square layers of the S0 -structure
               come into contact, and its symmetry is broken by a re-orientation of
               different puffs of the same layer in different directions. By contrast,
               the S1 -structure arises by an abrupt transition at both ends of the pa-
               rameter interval on which it is optimal. In the D0 -structure the mirror
               planes of the green and teal puffs, which form a dimer, are not aligned,
               so that both can be in contact with the purple puff. In the limit γ → 3,
               the green and teal puffs become aligned and form a bipyramidal dimer.
               The structure becomes the dimer double lattice structure reported in
               Refs. [46, 13] as the densest known packing of regular tetrahedra.


lattice of dimers). The unit cell contains four puffs, two of which, which are in contact
and form a shape similar to a triangular bipyramid, are related by inversion to the other

two (Figure 4.2). We call each of the two inversion related pairs a dimer, in analogy
with the dimer double lattice of Refs. [46, 13], which is the limit of the D0 -structure as
γ → 3, and is the densest known packing of regular tetrahedra. In this limit, each dimer

exactly forms a triangular bipyramid. Note that away from γ = 3, the mirror planes of
the two puffs constituting the dimer are not aligned with each other, making the dimer
look twisted. This allows both puffs to form a contact with a nearby puff (see Figure


                                             70
                    Φ
                 0.86
                                                                                                       ò

                 0.84                                                                        ò
                                                                 ì                   ò
                 0.82                                           ìì           ò
                                              æ             ì        ì ò
                                          æ       à                   ìò
                                                  çà    ì              í
                 0.80                 æ
                                                    à ì                  í       æ           S0
                                  æ                ç àíá                         à          D1
                 0.78            æ                  í
                                æ                                                ì          S1
                            æ                                                    ò          D0
                 0.76
                        æ                                                                S0 analytic
                    æ                                                                                        Γ
                                          1.5               2.0                  2.5                   3.0




   Figure 4.3: Highest densities φ (filled markers) achieved for packings of tetrahe-
               dral puffs of varying asphericity γ. Densities are obtained and re-
               produced to an accuracy of 0.0005, much smaller than the marker
               size. The empty markers represent the density attained by a struc-
               ture at an asphericity where it is suboptimal, as determined either by
               runs where the search got trapped away from the optimal structure or
               by runs where the number of particles per unit cell was incompatible
               with the optimal structure. The two abrupt structural transitions can
               be easily seen here where the density line for the S1 -structure crosses
               the lines for the other structures at critical asphericities at which the
               S1 -structure coexists with them. On the other hand, the continuous
               structural transition between the S0 - and D1 -structures is associated
               with a broken symmetry instead: the line corresponds to an analytic
               construction of the S0 -structure, imposing its tetragonal symmetry.
               At γ ≈ 1.63, next-nearest layers come into contact with each other,
               leading to a sharp decline in density (dashed line). If we allow the
               tetragonal symmetry to be broken, but still allow only two particle ori-
               entations, the D − C search produces slightly higher packing densities
               (empty disks). The D1 -structure obtains higher densities by continu-
               ously breaking that symmetry as well.


4.2), which in the limit of the bipyramidal dimer is facilitated simply by a contact along
a common edge or vertex.


   The S0 -structure appears to be the optimal packing structure from γ = 1 to γ ≈ 1.63.
On the other end of the asphericity scale, the D0 -structure appears to be optimal from
γ ≈ 2.19 to γ = 3. However, in the intermediate range it appears that both of these


                                                            71
structures are suboptimal and different structures take over. For γ . 1.63, the density
of the S0 -structure increases monotonically with asphericity. However, for the puff with
γ ≈ 1.63, contacts between next-nearest layers of the S0 -structure appear, and start to
constrain the layer spacing. Assuming no change to the orientations of the puffs and

to the construction of the layers, this constraint leads to a sharp drop in the density of
the S0 -structure. However, the structure found by the numerical searches shows a re-
orientation of the puffs so that each layer is now composed of puffs of two different
orientations (Figure 4.2). This structure, dubbed the D1 -structure, still leads to a decline

in the packing density, but a less dramatic one. Therefore, we have a local maximum in
the packing density at the transition from the S0 -structure to the D1 -structure. This tran-
sition seems to arise by a continuous deformation of the S0 -structure and is not abrupt.
The re-orientation of the puffs suggests the beginning of a tendency towards the dimer-

ization seen in the D0 -structure. However, an intermediate structure is encountered
between the D1 -structure and the D0 -structure, producing another local maximum in
the optimal density. This structure, to be called the S1 -structure, is a simple (non-dimer)
double lattice without the tetragonal symmetries of the S0 -structure (Figure 4.2), and is

reminiscent of the simple double lattice structure reported in Ref. [46]. This structure
appears to be separated from the others by an abrupt transition. Figure 4.3 plots out the
densities of the different structures as obtained by the numerical search.




4.5 Discussion


The proper context for the results obtained here for tetrahedral puffs is in comparison
to two other one-parameter families of particles that include the sphere as a special
case and whose dense packing structures have been investigated vigorously, namely
spheroids [19] and superballs [44]. The putative optimal packing of spheroids and su-


                                             72
perballs becomes monotonically denser the less sphere-like they become. By contrast,
the optimal packing density of puffs does not exhibit such monotonicity, although it is
always higher than that of the sphere (consistently with a conjecture by Ulam that the
sphere is the worst-packing three-dimensional convex solid [27]). Unlike superballs,

but like spheroids, the optimal packing of puffs is in all cases (besides the sphere) not a
lattice packing, and the crystal unit cell includes at least two particles of different orien-
tations. However, like superballs, and unlike spheroids, the optimal packing structure of
puffs goes through an abrupt transition, where two dissimilar structures obtain an equal,

optimal density.


   A major difference of tetrahedral puffs in comparison to spheroids and superballs is
the lack of inversion symmetry. However, not only do the putative optimal packings of
puffs in all cases have such a symmetry (Figure 4.2), it is in some cases the only sym-
metry of the packing besides its lattice translations. Presumably, inversion symmetry

plays an important role in forming close-packed structures of particles with tetrahedral
symmetry and maybe even of other particles, a result already observed in the plane by
Kuperberg and Kuperberg [49].


   The tetrahedral puffs exhibit a much richer optimal packing behavior than either
spheroids or superballs, and this richness is likely to be mirrored in the behavior of tetra-
hedral nano-particles. The variety of qualitatively different dense packing structures ob-

served for mathematical tetrahedra is compounded when a physical shape parameter is
added. A possible way to experimentally access the parameter investigated here, which
describes a swollen tetrahedron, is by using colloidal particles that swell as a function
of their temperature [75]. Thus, a variety of structures and structural transitions could

be explored. We have attempted here to provide an atlas of the possible crystal struc-
tures which might be observed in systems of particles with tetrahedral symmetry. Our




                                             73
candidates for optimal tetrahedral puff packings provide a starting point for the study
of the phase behavior of systems of particles with tetrahedral symmetry, both hard and
soft, away from the limit of the mathematical tetrahedron. The method presented here,
applicable to any hard convex particle, could also be useful in characterizing possible

structures of many other particulate systems.


   We thank Simon Gravel for noting the relation of the tetrahedral puff to the Reuleaux
tetrahedron and for other helpful suggestions. This work was supported by NSF grant
DMR-0426568.




                                          74
                                      CHAPTER 5
  CONSTRAINT-BASED METHOD FOR STRUCTURE DETERMINATION



   The contents of this chapter are co-authored with Veit Elser. We acknowledge Robert
Tycko for assistance in acquiring and using his published data and results. We acknowl-
edge support from the National Science Foundation under grant number DMR-0426568.



5.1 Abstract


The inverse problem of inferring the structure of biomolecules from a set of structural
restraints is the important last step in the process of nuclear magnetic resonance struc-
ture determination. Traditional methods minimize a cost/energy function, consisting of
physical potentials and restraint potentials, to obtain structural models. By contrast, we

present a constraint-based approach where structural models are obtained by treating
experimental and physical restraints as hard constraints and using the iterated difference
map to obtain configurations that satisfy all the constraints. We apply our approach to
determination of the structure of a beta-amyloid fibril formed by a 40-amino-acid pep-

tide associated with Alzheimer’s disease based on restraints published in the literature.




5.2 Introduction


Since the first publication of a biomolecular structure solved by nuclear magnetic res-
onance (NMR) spectroscopy in 1985 [74], the use of NMR techniques for determining

the structure of biomolecules has become a leading complementary method to crystal-
lography. Solution and solid state NMR techniques can provide many restraints on the
structure of a molecule, including estimates of interatomic distances – based on nuclear


                                           75
Overhauser effect (NOE) measurements, spin label measurements, or various solid state
NMR techniques – estimates of torsional angles – based on chemical shift or J-coupling
measurements – location of hydrogen bonds – based on rates of proton exchange – and
bond orientation – based on residual dipolar coupling [32, 73, 58].


   After acquiring the data and analyzing it to derive restraints on the underlying struc-

ture comes the task of using the restraints to construct a three-dimensional model of
the structure. Such a molecular model is customarily constructed by minimizing a
cost/energy function, which usually combines the potential energy function of a molec-
ular dynamics (MD) force field with additional cost terms corresponding to the various

experimental restraints.

   Though this general approach has served for many years as a workhorse for structure

determinations, there are many things about it that are unsatisfactory. The approach of
minimizing a cost function is familiar to us from the problem of fitting a theoretical
curve to experimental data. There, the cost function arises as a means of maximizing
a statistical likelihood: we know that the theoretical curve cannot fit all data points

without error, and the cost function is a way of correctly balancing out the different
errors. In structure determination, however, our mindset should be different. To have
confidence in a reconstructed model we wish to use a large number of conservative
restraints so that all the restraints can be satisfied with good accuracy by a correct model,

and the simultaneous satisfaction of all the restraints can lend credibility to the model.
In contrast with the curve fitting case, we do expect all errors to be small.


   To the cost function associated with the errors in satisfying the experimentally de-
rived restraints, an energy function, associated with a physical force field, is usually
added. What we understand from this mystifying mix of the two different types of

forces is that the physical realizability of the structure is itself a restraint on it and must



                                              76
be balanced out against the experimental restraints. Again, this need for balancing out
errors belongs to the wrong mindset. That the structure is physically realizable, should
always be the case, not merely in a likelihood maximizing way. Moreover, the fact that
two structures have different energies, within this reasonable range, should not automat-

ically make one be considered a better solution, since the MD force field energy is an
approximation of the real free energy of the structure. This is especially true when the
solvent is treated implicitly. Below a certain energy resolution, such force-field energy is
unreliable as a discriminator, and over-reliance on it may bias the determined structure.


   We present in this work an alternative approach to the problem of structure determi-

nation from NMR restraints, which is based directly on the nature of the data as restraints
and does not attempt to convert it into an energy minimization problem. Our approach
is based on the Difference Map (DM), an iterated dynamical system in the space of con-
figurations. The DM has been used successfully before on a variety of problems that

suggests its usefulness in the present case. For example, the protein folding problem
has been compared to finding the ground state of spin glasses [9], a task at which a
DM approach has been shown to do reasonably well [23]. More relevantly, Elser and
Rankenburg have applied the DM to a toy model of the problem of finding ground state

conformations of heteropolymers given their monomer sequence [24]. Their difference
map implementation was able to discover lower energy conformations than other ap-
proaches could. In the toy model they study, the monomers are modeled as soft spheres.
In real proteins, of course, amino acids come in a variety of shapes with internal degrees

of freedom, and these shapes have to be packed into the core of the folded structure.
It is promising then that the DM has also been successfully used for discovering dense
packings of a variety of shapes [47, 45]. Finally, the DM has generally been found use-
ful in inverse problems where a hidden configuration is used to generate data, which is

then utilized to try to reconstruct the hidden configuration. Such problems include SAT,



                                            77
where an unknown truth value assignment to a set of variables is reconstructed based
on a list of clauses which the assignment satisfies, and phase retrieval, where a two
dimensional image is reconstructed based on the magnitudes of its Fourier transform
[30, 20].




5.3 Constraint-based approach


The difference map deals, on the lowest level, with constraints. Therefore we seek a
formulation of the problem of structure determination from NMR restraints in terms of
constraints. Particularly, we wish our formulation to be in terms of two simple con-

straints, that are each easily satisfied, but are in competition with each other, so that
finding a configuration satisfying both (i.e. a solution) is hard. We achieve this with the
Divide and Concur approach [30].




5.3.1 Data restraints


As discussed above, there are two sets of restraints which must be utilized to determine

the structure. The first is the set of restraints which we extract from NMR data (data
restraints), and the second is the set of restraints coming from physical realizability
(physical restraints). Within the set of physical restraints, there are again two, funda-
mentally different, sets of restraints: local and non-local. We refer here to locality along

the protein backbone, not to locality in space.


   The data restraints are at the center of our structure determination problem. Whereas
traditional methods formulate the information extracted from the NMR experiments as
soft restraints – that is, potentials to be added on to the cost/energy function to be mini-


                                            78
mized – we treat them as hard restraints – each to be satisfied individually in a solution.
For example, an estimate on the distance between two atoms from a NOE measurement
will be treated as a bound (single- or double-sided) on the distance, instead of as a force
between the atoms.




5.3.2 Local physical restraints


The local physical restraints deal with the primary structure of the molecule, namely
the geometry of covalent bonds. Covalent bonding generates a network of bonds, bond
angles, and torsion angles. Bond lengths and bond angles are not given much freedom
by quantum chemistry and stay, to a few per cent, at a fixed value, determined by the type

of bonds and functional groups involved [25]. Therefore, the conformational freedom of
the molecule comes principally from the possibility of torsional rotations about bonds,
although the torsional angle about some bonds (like the peptide bond) is also fixed.


   Most MD packages enforce this fixed covalent geometry by means of a potential
energy where each bond length, bond angle, and dihedral angle is subject to a separate

potential of the form V(x) = kx (x − x0 )2 , where x0 represents the equilibrium value of the
variable [52]. Of course, the quantum chemistry leading to these equilibrium values is
not as simple as the form of these potentials might suggest. For example, different bonds
and angles should not vary independently, and should have some degree of correlation.

While these potentials are therefore inadequate for appropriately capturing deviations
from equilibrium values, they are quite adequate if all we want is to constrain the bond
lengths and angles to the appropriate covalent geometry. In fact, for this purpose it is
enough to have only a single potential for each maximal rigid unit.


   A set of atoms is called a rigid unit if the distance between any pair of atoms in it


                                             79
is fixed. The entire molecule can be partitioned into rigid units that are maximal, that
is, not proper subsets of rigid units. In such a partitioning, two rigid units may overlap,
but may have up to only two (assuming non-collinearity) atoms in common. The form
of the potential associated with each rigid unit can be written as the root-mean-square

deviation (RMSD) when its atoms are superimposed with the equilibrium configuration
of the rigid unit:
                                                       N
                                                       X
                           V (r1 , r2 , . . .) = min         ||ri − T (yi )||2 ,          (5.1)
                                                T
                                                       i=1

where r1 , r2 , . . . are the coordinates of the atoms comprising the rigid unit, T is any rigid
transformation (i.e. a composition of rotations and translations), and y1 , y2 , . . . are the
atomic coordinates of a reference rigid unit in equilibrium. We immediately see the
advantage of this formulation when inspecting a simple amino acid such as aspargine.

While three rigid unit restraints are enough to properly enforce the covalent geometry
within the amino acid (see Figure 5.1), it would be necessary to use 11 bond length
restraints and 18 angle restraints.


    More important however than the form we choose for the restraints that enforce
covalent geometry, is the way we choose to treat them within our constraint-based ap-

proach. Namely, because the deviations from rigidity are quite small compared to other
variables in the problem (such as the softness of non-local potentials and uncertainty
in distance bounds), we treat the local physical restraints as hard restraints, instead of
soft ones. Practically, this means that instead of adding the local potentials to the com-

bined cost/energy function to be minimized, we require that each potential individually
vanishes. Thus, we treat the local physical restraints in the same way we treat the data
restraints.




                                                80
   Figure 5.1: An aspargine residue partitioned into maximal rigid units (right). A
               view from the same angle and with traditional chemical element colors
               is given (left) for reference. The red, blue, and green rigid units are
               centered around the Cα , Cβ and Cγ atoms respectively. We do not
               include the HN and O′ atoms, as they do not belong to a maximal
               rigid unit which is contained inside the residue. Each of these atoms
               belongs to a planar rigid unit which spans the peptide bond.


5.3.3 Non-local physical restraints


After we remove the local interaction potentials and the data restraint potentials, having

turned them into hard restraints, the only components left in the cost/energy function are
the non-local interactions. There are many non-local interaction which contribute to sta-
bilizing protein folds and make the structure physically realizable. A balance between
attractive interactions such as hydrophobic clustering, salt bridge formation, and hydro-

gen bonding, and repulsive interactions, such as exclusion of van der Waals spheres,
stabilize the structure. However, when reconstructing structures based on NMR data,
it is possible and customary to rely only on the experimental restraints and the repul-
sive interactions, ignoring the attractive ones [58]. As a model for the energy due to

non-local interaction, we may use a standard MD force-field with all local energy terms



                                           81
turned off.


    While this energy function is no longer a mystifying mix of real and imaginary
forces, we would still like to avoid a direct minimization of it. Instead we would formu-
late the requirement of physical realizability as an upper bound on this energy. We are
inclined to do so because we do not want to bias the reconstructed structure based on a

wrong, oversimplified model of the underlying forces. While imposing an upper bound
on the energy of the structure is necessary for getting reasonable structures, we do not
want to pretend to know more about the forces acting to stabilize it than we actually do.
This is especially important because the model for the non-local interaction is very of-

ten chosen for computational efficiency as much as for accurately reproducing physical
forces.




5.3.4 Divide and Concur


To summarize, in our formulation of the structure determination problem all we require
of a solution is to satisfy three sets of restraints:


   1. the experimentally derived restraints (data restraints),

   2. the rigid unit restraints (local physical restraints), and

   3. a bound on non-local interaction energy (non-local physical restraints).


Whereas the conventional approach to finding a configuration that satisfies a list of re-
straints is to combine them into a single cost/energy function and attempt global mini-
mization, we use the DM as part of the approach known as Divide and Concur. In this

approach, we expand the configuration space by introducing multiple replicas of each
atom – one replica for each restraint it is involved in. Thus, by relaxing the requirement


                                               82
(known as the concur constraint) that all replicas of a single atom coincide spatially, we
can very easily satisfy all the restraints, since they are all independent. In fact, not only
can we easily find a configuration (in the expanded space) that satisfies all restraints, but
we can also find the closest such configuration to a given arbitrary configuration. We call

such a configuration the projection of the given configuration onto the constraint set (the
subset of configuration space containing all configurations satisfying all the restraints).
Of course, to obtain a valid solution, we must find a configuration that satisfies not only
this constraint (the divide constraint) but also the concur constraint. We achieve this

using an iterated map that can be written as a composition of the projections to the two
constraints and affine combinations. The dynamical system thus constructed, the DM,
is designed to efficiently explore the important regions of the configuration space, and
its fixed points correspond to solutions.


    Formally, we can construct the configuration space, the constraints, and the map as

follows. Let I be the set of atoms in the molecule and let A be the set of restraints. We
consider a bipartite graph with edges E connecting restraints to the atoms they involve.
Each restraint involves only a small fraction of the atoms in the molecule. Since the
energy bound restraint (3) involves all the atom in the molecule, and it is the only one

that does so, it turns out to be much more efficient to include it as part of the concur
constraint than as part of the divide constraint. Therefore, A includes only the data
restraints and the rigid unit restraints.


    Our configuration space is the space of maps from the set of edges E to three di-
mensional Euclidean space R3 . That is, a configuration x = (re ), where e = hi, αi ∈ E,
assigns a position in space to each atom i ∈ I for each restraint α ∈ A it is involved

in. The configuration space is therefore an M × 3-dimensional Euclidean space, where
           P           P
M = |E| = α∈A |E α | = i∈I |E i |, E α is the set of edges incident on restraint α, and E i is




                                             83
the set of edges incident on atom i. We call rhi,αi a replica of atom i involved in restraint
α.


     The divide constraint is the subset of our configuration space where a restraint is
satisfied by the atomic positions assigned to its incident edges:

                                              
                        D = x such that Vα x|Eα = 0 for all α ∈ A ,                                (5.2)

where x|Eα is the restriction of the assignment x to the edges E α incident on restraint

α. The concur constraint is the subset where a unique atomic position is assigned to
all edges incident on the same atom, and where this assignment of positions to atoms
satisfies the energy bound restraint:

 C = {x = (re ) such that re = ri for all i, e ∈ E i and Vnon-local (r1 , r2 , . . .) ≤ E bound } . (5.3)


     In the next section we discuss how to construct projections pC and pD to these two
constraints. Provided these projections, we set up a dynamical system based on an

iterated map. Given a configuration x j at the jth stage of the iteration, the configuration
at the next iteration is given by

                        x′j = λx j + (1 − λ)pD (x j )                                              (5.4)
                                                                
                     x j+1 = DM(x′j ) = x′j + pD 2pC (x′j ) − x′j − pC (x′j ).                     (5.5)

For λ = 1 (i.e x′j = x j ), these are purely iterations of the difference map DM. Note
                                                         
that every fixed point xfp of DM has pD 2pC (xfp ) − xfp = pC (xfp ) = xsol which lies in
the intersection of D and C and is therefore a solution. However, it is sometimes the
case that the two constraints are inconsistent, due to slight inaccuracies, and that only an
approximate solution is possible. The modified iteration with 0 < λ < 1 makes sure that

these approximate solutions are also stable despite not being fixed points of DM [51].
We use the value λ = 0.9 in all our runs.


                                                  84
5.4 Implementation


In the previous section we have defined the projections pC and pD to the concur and
divide constraints and used them to set up our difference map iteration scheme. In this
section we focus on how to efficiently calculate these projections in a computational
implementation. The calculations involved in projecting to the divide constraint will

depend on the form of the underlying data restraints. We will discuss the case of two
common types of restraints, distance bounds and torsion angle bounds, but many more
cases are feasible in this type of approach, including restraints on bond orientation and
distance bounds with uncertain assignment.




5.4.1 The divide constraint


Given an arbitrary configuration x, in order to compute pD (x) we wish to find a con-
figuration x′ ∈ D (where D is given in (5.2)) that minimizes ||x − x′ ||. It is easy to
see that this optimization problem decomposes into independent optimization problems
– one for each restraint. Namely, for each restraint (α), we must find a configuration

x′ |Eα , restricted to edges incident on α, which minimizes ||x|Eα − x′ |Eα ||, while satisfying
Vα (x′ |Eα ) = 0. Each of these optimizations also take the form of a projection, and so we
refer to them as subprojections or projections to the restraints. The calculation involved
in each of these subprojections will depend on the form of the restraint Vα .




                                              85
5.4.2 Distance bound restraints


The simplest restraint is the restraint bounding an interatomic distance dmin < ||rhi,αi −
rhi′ ,αi || < dmax . This kind of restraint is commonly derived from cross-peaks in NOE
spectroscopy [73], but can also arise from many other experimental measurements, or

as a way of enforcing hydrogen bonding geometry for a known hydrogen bond [58].

   The projection to this restraint is given simply by

                                                  ∆d
                              r′hi,αi = rhi,αi +     (rhi,αi − rhi′ ,αi )                (5.6)
                                                  2d
                                                  ∆d
                             r′hi′ ,αi = rhi,αi −    (rhi,αi − rhi′ ,αi ),               (5.7)
                                                  2d

where d = ||rhi,αi − rhi′ ,αi || and ∆d = −(dmin − d) if d < dmin , ∆d = d − dmax if d > dmax ,
and ∆d = 0 otherwise.




5.4.3 Rigid unit restraints


We impose the covalent geometry by use of rigid unit restraints of the form
                                       |Eα |
                                       X
                                 min           ||rek − T (yk )||2 = 0,                   (5.8)
                                  T
                                       k=1

where T may vary over all rigid transformations (compositions of rotations and trans-
lations), ek ∈ E α are the edges between the restraint α and the atoms included in the

rigid unit, and y1 , y2 , . . . is the equilibrium configuration of the rigid unit. The pro-
jection of a configuration x|Eα to this restraint is then given by r′ek = T (yk ), where T
minimizes δ(T ) = |E
                   P α|
                     k=1 ||rek − T (yk )||. This minimization problem, known sometimes as

absolute orientation, is well studied, and various closed-form solutions exist [39, 40]. It

is identical to the problem of superposing two molecular structures so as to minimize
root-mean-square distance (RMSD) between then.


                                                   86
    We construct the reference structures y1 , y2 , . . . based on the all-atom CHARMM22
force field [52]. We identify the 38 rigid units that can occur in polypeptides that include
the 20 standard amino acids. For each such rigid unit we build a small molecule that
includes it and extract the reference structure for the rigid unit from the equilibrium

structure of the molecule subject to the CHARMM22 force field. A more reliable set of
reference structures might be derived from a database of high resolution X-ray structures
of small compounds, as in Ref. [25].




5.4.4 Torsion angle restraints


The backbone torsion angles φ and ψ can often be estimated based on the chemical shifts

of surrounding nuclei by comparison to a database of structures with known chemical
shifts [64].


    Suppose the angle φ is known to be in the range φmin ≤ φ ≤ φmax . We can put this
restraint in a similar form to the previous restraint:
                                            |Eα |
                                            X
                               min                  ||rek − T (yk (φ))||2 = 0,         (5.9)
                           T,φmin ≤φ≤φmax
                                            k=1

where the restraint involves all atoms which form a maximal rigid unit if φ is held
constant, and (y1 (φ), y2 (φ), . . .) is the equilibrium configuration of that rigid unit. As
calculating δ(φ) = minT δ(T, φ) is straight forward, as described above, we must simply

numerically minimize δ(φ) over φmin ≤ φ ≤ φmax . Note that even though the set of atoms
involved in this restraint is not a rigid unit, but includes two rigid units, this restraint
implicitly includes the two rigid unit restraints and replaces them.




                                                      87
5.4.5 The concur constraint


Like the projection to the divide constraint, the projection to the concur constraint will be
computed using a subprojection – a projection operation in a lower-dimensional space.
Given an arbitrary configuration x, in order to compute pC (x) we wish to find atomic

positions r′1 , r′2 , . . ., concurring across all restraints, which minimize the distance func-
tion
                                                     X
                               δ r′1 , r′2 , . . . =   ||rhi,αi − r′i ||2 ,
                                                  
                                                                                             (5.10)
                                                         hi,αi∈E

while satisfying a bound on the non-local energy

                                  Vnon-local (r′1 , r′2 , . . .) ≤ Ubound .                  (5.11)

The projection would then be given by r′hi,αi = r′i . It is easy to show that δ(r′1 , r′2 , . . .)

depends only on the distances between r′i and ri = (1/|E i |) e∈Ei re , the averaged position
                                                             P

of atom i across all its replicas. In fact, the distance function can be rewritten, up to a
constant which does not depend on its arguments, as
                                                         X
                                δ(r′1 , r′2 , . . .) =         |E i |||ri − r′i ||2 .        (5.12)
                                                           i

Therefore, the subprojection calculation involves projecting the replica-averaged con-
figuration r1 , r2 , . . . to the energy bound restraint subject to the weighted metric (5.12).




5.4.6 Non-local energy bound


If the replica-averaged configuration already satisfies the energy bound, the subprojec-
tion leaves it unchanged, and the projection is given simply by the averaging opera-

tion. Otherwise, the subprojection must yield a configuration where the energy bound is
marginally satisfied, Vnon-local (r′1 , r′2 , . . .) = Ubound . To find this configuration we use the


                                                         88
Lagrange multiplier method for constrained minimization. Consider a combined energy
function Vk′ (r′1 , r′2 , . . .) = Vnon-local (r′1 , r′2 , . . .) + kδ(r′1 , r′2 , . . .). For each value of the La-
grange multiplier k, a global minimization of Vk′ yields a configuration r′1 (k), r′2 (k), . . .
                                                       
with an energy U(k) = Vnon-local r′1 (k), r′2 (k), . . . . The configuration we seek is the one

for which U(k) = Ubound . A numerical root-finding algorithm can find the solution to
this equation with a modest number of evaluations of U(k). Each evaluation of U(k)
involves minimizing Vk′ , the sum of the non-local potential and a harmonic potential,
restraining each atom independently to its replica-averaged position in the input config-

uration. Such a potential is easy to implement in force-field software packages such as
XPLOR-NIH, which we use to perform this minimization [63]. Although, formally, the
Lagrange multiplier method above only holds if the global minimum is found in calcu-
lating U(k), we are forced by considerations of efficiency to apply local minimization.

However, due to the harmonic restraint, the global minimum cannot be very far from
our initial point which is the replica-averaged input configuration.


    The projection holds for enforcing a bound on any potential energy function. In this
work we use a simple form of the van der Waals exclusion potential:
                                                              X
                                  Vexcl (r1 , r2 , . . .) =             Vi j (||ri − r′i ||),              (5.13)
                                                              hi,i′ i

where                                    
                                         
                                                   ′     2
                                                                            r < ηRi + ηR′i
                                         
                                         (ηRi + ηRi − r)
                                         
                                         
                                         
                                         
                              Vi j (r) = 
                                                                                                          (5.14)
                                         
                                         
                                         0
                                         
                                                                           otherwise,

Ri is the van der Waals radius of the ith atom as given by the CHARMM22 force field
[52], η = 0.81 determines to what degree we allow van der Waals spheres to overlap
without penalty, and the sum skips pairs that are connected by a path of three covalent
bonds or fewer.




                                                         89
5.5 Results


As a demonstration of our new approach to NMR structure determination, we study
a structure that has already been reconstructed with a traditional approach, so that we
have a point of reference for our results. The structure is a three-fold symmetric amy-
loid fibril formed by a 40-residue peptide associated with Alzheimer’s disease [58]. The

experimental restraints we use are the same restraint as used in Ref. [58] (see supporting
information there), which include distance bounds – both intramolecular in intermolec-
ular – and backbone torsion angle bounds. As in Ref. [58], we ignore the eight residues
of the peptide which form a disordered region.


   We perform the reconstruction, based on the difference map iteration described

above, in two steps. In the first step, we reconstruct the structure of one cross-beta unit,
modeled by six polypeptide chains. We include only the restraints that apply within a
single cross-beta unit. As an initial condition, we use six well-separated, parallel, ex-
tended chains with randomized backbone torsion angles, and with all replicas of each

atom initially in agreement. In most runs, the difference map iterations quickly yield
a structure that reasonably satisfies both constraints. In those runs, we then take three,
well-separated copies of the model, arranged in a three-fold symmetric way about an
axis, and perform more iterations of the difference map with all restraints being in-

cluded. We evaluate the final models by how well the structure that satisfies the concur
constraint, given by xC = pC (xfinal ) does at satisfying the various restraints included in
the divide restraint. We can do this easily, by looking at the distances between the po-
sitions of the atomic replicas in xD = pD (xC ) to the ones in xC . These distances, which

we will call errors, indicate by what degree the restraint which involves the replica is
unsatisfied.




                                            90
   Of fifty runs, taking approximately a total of 800 CPU hours, we pick the four which
yielded models with the smallest root-mean-square error, and we compare them to the
four models presented in Ref. [58]. We perform short relaxation runs on the four models
of Ref. [58] using our difference map iterations. This relaxation run is necessary for a

comparison on an equal footing because of our formulation of the restraints, which is
presumably slightly different than the formulation used to derive these models. Indeed,
the relaxed models have a lower root-mean-square error than the unrelaxed model. A
quantitative comparison between the two sets of models is presented in Tables 5.1 and

5.2, Figure 5.2 compares the distribution of the errors in two models from the two sets,
and Figure 5.3 compares the two models visually.


   Though the models produced in this work have virtually the same distribution of er-
ror magnitudes as the relaxed version of the models in Ref. [58], they are quite different
from each other. Though each run starts from a different random initial condition, our

four lowest-error models, like in the other set of models, fall only ∼ 2 angstroms from
one another in terms of RMSD, but the two sets are ∼ 7 angstroms apart. Visually, we
observe that the models produced in this work have a greater twist along the fibril axis.
As both models reasonably satisfy all the restraints, there is not enough information in

the restraints alone to exclude either possibility. There is no obvious reason why our
method, over many runs, would repeatedly converge to one cluster of models, but never
to the cluster of models represented by the models in Ref. [58], which satisfy the con-
straints equally well. It is possible that without the bias introduced by the energy/cost

minimization, the latter cluster is destabilized entropically with respect to the former
cluster. However, it is also possible that this result simply speaks to the unavoidable
inherent bias in any search dynamics used for structure determination.




                                           91
                             root-mean-square error (10−2 Å)
                 model set 1 2.33 2.40 2.41 2.42
                 model set 2 9.37 9.44 9.56 9.66
                 model set 3 2.32 2.50 2.29 2.29


Table 5.1: Root-mean-square errors in four models of the amyloid fibril produced
           by the constraint based method (set 1) and four models produced by a
           traditional method (set 2) [58]. For proper comparison, we perform
           short relaxation runs on the four models of set 2 using our difference
           map iterations (set 3). The root-mean-square error is an average over
           the atomic replicas of the distance each needs to move from the position
           agreed upon by all replicas of the same atom to the position where it
           must be for the restraint it is involved in to be satisfied.




                                             model set 1
                     RMSD1 (Å)      2.84     1.59 1.70     1.89
                     RMSD2 (Å)      9.54     7.37 7.43     6.96
                     RMSD3 (Å)      9.27     7.05 7.12     6.67
                                             model set 2
                     RMSD1 (Å)      7.48     8.30 7.97     7.75
                     RMSD2 (Å)      2.08     2.49 1.60     1.93
                     RMSD3 (Å)      2.35     2.71 1.99     2.17
                                             model set 3
                     RMSD1 (Å)      7.16     7.97 7.63     7.43
                     RMSD2 (Å)      2.25     2.57 1.72     2.11
                     RMSD3 (Å)      1.93     2.33 1.43     1.79


Table 5.2: Root-mean-square deviations between different models of the amyloid
           fibril. In calculating the RMSD, we consider only the alpha-carbons.
           We compute an average structure for each of the three sets of models
           (see Table 5.1) by aligning all models against a single model and taking
           the centroid position for each atom. The table gives the RMSD between
           each model and the average structure of each of the three sets (RMSD1
           is the distance of a model to the average of set 1 and so on).




                                        92
        frequ en cy

          800



          600



          400



          200



                                                                            error H ÞL
                   0.015 0.020    0.030     0.050   0.070   0.100   0.150



   Figure 5.2: The distribution of errors in the lowest error model of the amyloid
              fibril constructed in this work (blue) and a representative model con-
              structed by a traditional method [58] after a relaxation run (purple).
              The errors corresponding to each restraint are the distances by which
              the atoms involved in the restraint need to moved for the restraint to
              be satisfied. The left-most point represents all errors smaller than 0.01
              angstroms.


5.6 Discussion


In this work we developed a constraint-based formulation of the problem of structure

determination from NMR restraints, and proceeded to implement a numerical method
based on the difference map and the Divide and Concur approach for solving this con-
straint satisfaction problem. We divided the information used for reconstruction into
data restraints, local physical restraints, and non-local physical restraints. The data re-

straints and local physical restraints were formulated as hard restraints, which should be
individually satisfied in a solution. These restraints became part of the divide constraint,
which required all of them to be simultaneously satisfied, but allowed different replicas
of a single atom to be in different positions. The concur constraint required all repli-

cas of a single atom to agree on its position. Also, it included the non-local physical


                                            93
Figure 5.3: Backbone traces of a model of an amyloid fibril constructed in this
           work (top) and a representative model constructed by a traditional
           method [58] after a relaxation run (bottom). The colors serve to vi-
           sually distinguish different chains and the two models.




                                      94
restraints, which were formulated as an energy bound.


   With the restraints thus divided, we can observe the essentially geometric nature of
the structure determination problem. The restraints included in the divide constraint –
distance bounds, and rigid units (with or without internal degrees of freedom) – all refer
to how the different atoms of the molecules are held together, either locally along the

chain by covalent bonds, or across the chain by prescribed distances, as measured in
experiment. The atoms then form a network of hinges, joints, and pistons with either
free or constrained ranges of motion. The exclusion restraint on the other hand, or
by its more geometric name, the packing constraint, prevents atoms in contact from

overlapping when they are pushed against each other, as if their centers were held apart
by a bar. This formulation brings to mind Buckminster Fuller’s tensegrity structures,
whose structure is stabilized by a balance of tensile elements (cables) holding points of
the structure together and compressive elements (bars) holding points apart, and which

form an interesting topic in the geometrical study of rigidity [15].

   In constructing the difference map scheme, there are many choices to make as to how

to divide the many restraints into two sets, forming the divide and concur constraints.
The difference map appears to find solutions most efficiently when the two projections
it employs are in direct competition with each other [24]. This is the case here, where
the competition is between the tensile restraints, holding the atoms together, and the

compressive restraints, holding them apart.


   The purpose of this work is not to compare the efficiency of the difference map
method presented here to that of traditional methods, but to demonstrate its feasibility
and discuss its possible advantages or disadvantages. We leave off the former task to
future work. The results presented in the previous section clearly demonstrate that the

method we developed here is capable of constructing a model satisfying the restraints



                                            95
with as much accuracy as models produced by traditional methods. Also, the model is
not much different, so that we may surmise that our method does not disrupt any of the
important physics needed for structure determination by abandoning traditional physical
dynamics in favor of the artificial difference map dynamics or by introducing unphysical

replicas. To the extent that the differences in the resulting models are due to the lack of
particular interactions, they can be easily added. In this work, the only non-local physi-
cal interaction included was the van der Waals exclusion potential, but the approach we
present can accommodate any desired force field. To include electrostatic interactions,

for example, all that is necessary is to change a flag in the force-field package used in
Section 5.4.6.


   While the approach developed here for constructing models based on structural re-
straints appears to be as powerful as traditional methods, it cannot now replace them.
For one, further work will be needed to develop an interface for the computational en-

vironment that is more intuitive to spectroscopists. More work could be done to study
and optimize the performance of the method and the quality of models produced, as
measured by standard metrics. Though we address only two types of data restraints in
this work, many more can be easily implemented.


   The main advantage of employing an approach such as the one developed here is
that it deals with restraints as restraints and not as potentials. Instead of combining

disparate pieces of information into a single cost/energy function, our constraint-based
approach handles each restraint individually as a hard restraint, and attempts to find a
configuration that satisfies all of them. Since any model satisfying all of the restraints
should a priori be considered an equivalently valid structure prediction, we avoid in this

way biasing the predicted structure because of an incomplete or simplistic model of the
physical forces.




                                            96
                                      CHAPTER 6
          CONFORMATIONS OF A GRAPHENE-LIKE SHEET WITH
                     HETEROGENEITY IN BOND LENGTHS



6.1 Abstract


We study a simple model of rippling in a two-dimensional netwrok of bonds due to

bond length heterogeneity. We describe a form of dislocations which is not present in
a homogeneous crystal and use a relationship between the dislocation density and the
Gaussian curvature to characterize the relaxed conformation of the sheet. We find a
relationship between this conformation and a surface in an abstract space associated

with the combinatorial aspect of the bond length heterogeneity.




6.2 Bond length heterogeneity in an atomic sheet


One possibility that has been suggested as an explanation of intrinsic rippling of

graphene sheets is the diversity of types of chemical bonds that two carbon atoms
may form [26]. This suggestion raises the geometrical question of how might a two-
dimensional network of bonds conform in three-dimensional space if its bonds vary in
some non-regular way, and particularly, how might a flat sheet be perturbed away from

flatness at the introduction of such heterogeneity. We attempt to answer this question for
a simple, albeit historically important, model of bond heterogeneity: Kekulé structures
[36]. Kekulé structures are ones in which each bond of the honeycomb lattice is desig-
nated either a single bond or a double bond, and each carbon atom participates in exactly

two single bonds and one double bond. While this model is very unlikely as an explana-
tion of mechanical instabilities in graphene, the problem from which it is inspired, the


                                           97
geometrical problem it poses is of scientific interest. Particularly, it is potentially inter-
esting as a mechanism for pattern formation in self-assembled and designer materials.


   The model we wish to study is one wherein the conformation of the network mini-
mizes a simple classical potential
                          X                                  X
                    U=            kb (di j − lσ(i, j) )2 −            ka cos(θi jk − 2π/3),   (6.1)
                          hi ji                              hi jki

where σ(i, j) ∈ {s, d} represents the type of bond between atoms i and j, di j is its length,
and l s and ld are the relaxed lengths for single and double bonds respectively. In the

limit where l s = ld , the equilibrium conformation of the network is the familiar two-
dimensional honeycomb lattice. This is the reference structure to which we will relate
the equilibrium structure when ld < l s as a perturbation. Similarly, if ld < l s , but the
double bonds are identified with one of the three sublattices of like-oriented bonds, then

the equilibrium conformation is again the familiar structure, except it is compressed
along the direction of double bonding. We would like to know what happens if ld < l s
for an arbitrary Kekulé structure. We restrict ourselves to the case where l s − ld ≪ l s




6.3 Fractional dislocations in a six-fold two-dimensional crystal


On a coarse-grained scale, we can think of the atomic network as tracing out a two-
dimensional manifold in space. Much work has been done by Bowick and co-workers

to describe how the structure of a six-fold two-dimensional crystals is disrupted when
forced to lie on a curved manifold [7, 8, 6]. We can use the same results to investigate
instead how a disruption to the structure of the crystal can affect the curvature of the
manifold it traces out. The bond orientation of the crystal at each point on the manifold

gives a local coordinate frame. By enforcing the topological requirement that as we
follow a closed loop, the accumulated change to the coordinate frame vanishes (up to


                                                      98
   Figure 6.1: The five patterns of single and double bonds in a 6-cycle of the
              honeycomb lattice that are allowed in a Kekulé structure. The Burg-
              ers vector of each hexagon can be determined by travelling counter-
              clockwise around the cycle, taking shorter steps when travelling on
              double bonds. The vector connecting the termini of the path is the
              Burgers vector (in blue, not to scale). Three of the cycles above have
              vanishing Burgers vectors.


π/3-rotations), we can associate the Gaussian curvature (density of total curvature) of
the manifold with the sum of two contributing densities: the circulation density (curl) of
Burgers vectors associated with dislocations and the density of disclination charges [8].


   Our model 6.1 assumes a perfect honeycomb lattice with no dislocations or discli-
nations. However, we may view the heterogeneity in bond lengths as introducing a type
of fractional dislocation that does not exist in homogeneous crystals. Namely, imagine

following a cycle in the network and tracing out a related path using a fixed coordinated
frame: each bond traversed in the cycle corresponds to a step in the path along one of the
six bond directions given by the reference frame, and the length of the step is given by
l s or ld depending on the type of bond traversed. Because of the heterogeneity in bond

lengths, this path will not be a closed path, and we may think of the vector connecting
its termini as a Burgers vector. We can thus associate a Burgers vector with any of the
five possible 6-cycles in a Kekulé structure (see Figure 6.1).


   Since the dislocations in our model are ubiquitous and the magnitude of each is
small, we are in limit where we may consider a continuous density of Burgers vectors



                                            99
b(x) forming a vector field over our manifold. Bowick and co-workers show that the
Gaussian curvature is given by the differential 2-form K(x) = db(x) [8]. Note that
mean curvature, since it lacks the topological nature of the Gaussian curvature, is not
determined by the pattern of dislocations, and will probably depend on the particular

parameters of the model 6.1.




6.4 Random tilings, projection, and the phason dimension


It is useful now to leave the geometrical problem for a while, and focus on the com-
binatorial problem of enumerating and characterizing Kekulé structures. In the field of

combinatorics and statistical physics this problem has a long history and is known as the
problem of dimer covers or perfect matching, as applied to the honeycomb lattice [48].
Associating each double bond with a rhombic tile decorated with two carbon atoms, a
double bond, and four halves of single bonds (see Figure 6.2), we can now ask to enu-

merate the ways of tiling the plane with such tiles. Thus, a uniform (that is, drawn from
a uniform distribution) Kekulé structure is equivalent to a uniform random tiling with
π/3-rhombi.


   In the field of random tiling, it is often useful to view a planar or spatial tiling, as
the projection of a higher dimensional surface onto two or three dimensions [35]. The
extra dimensions, which are projected out, are called the phason dimensions. In the case

of π/3-rhombi, this projection construction is very easy to visualize, as illustrated in
Figure 6.3. The three-dimensional surface whose projection is the tiling is formed by
square plaquettes oriented normal to the x, y, or z directions, and the phason dimension
is along the (111) direction. Note that if instead of fully applying the projection, we

simply contract the phason dimension by a large factor, we are left with rhombi that are



                                           100
   Figure 6.2: Correspondence of a Kekulé structure to a tiling by decorated rhombi:
               a portion of a uniform Kekulé structure composed of single and dou-
               ble bonds on a honeycomb lattice (left); and the corresponding tiling
               by rhombic tiles each decorated by a centered double bond and four
               halves of single bonds.




   Figure 6.3: Correspondence of a Kekulé structure to the projection of a three
              dimensional surface: the tiling of Figure 6.2 can be obtained as a pro-
              jection of a surface composed of square plaquettes, viewed here from
              slightly off the projection axis for ease of visualization.


related to the decorated π/3-rhombi by a small contraction along the double bonding di-
rection. This observation raises the possibility that this surface, obtained by incomplete

projection, is the same (at least viewed on a large scale) as the manifold traced out by
the bond network in equilibrium.


   Such a relationship, between the strain of a structure in physical space and strain



                                           101
in phason space has been identified before in quasicrystalline random tilings. In Ref.
[57], Nori, Ronchetti, and Elser conduct the following numerical experiment: As their
reference structure, they start with some tiling, where each tile is decorated with atoms
and bonds so that all bonds lengths are at their relaxed value. In Ref. [57] this results

in two relaxed bond lengths, identified with bonds of two different types. Then, they
perturb the structure by changing the relaxed length of one type of bond by a small
amount, and they let the network relax to its equilibrium. The authors find that when
the reference structure is given by the projection of a hypersurface whose phason co-

ordinates remain in a bounded region, then the deviation of the relaxed structure from
the reference structure also remains bounded everywhere and no strain accumulates. On
the other hand, when the deviation of the phason coordinate accumulates linearly as a
distance from some reference point, so does the physical strain accumulate linearly. The

numerical experiment of Ref. [57] demonstrates an indirect relationship between pha-
son strain and physical strain, in the sense that the pattern of deviation in physical space
is not shown to be related to the pattern of deviation in phason space. Here, we seek a
direct and analytical version of this relationship, by relating the Gaussian curvatures of

the surface which is projected to give the tiling related to the Kekulé structure and the
manifold traced out by the bond network in its equilibrium conformation.




6.5 A relationship between two apparently disparate surfaces


The Gaussian curvature of the surface which is composed of square plaquettes is, of

course, vanishing everywhere, except at its vertices, where it diverges. At these vertices
the contribution to the total curvature is proportional to the number of plaquettes meeting
at the vertex, being equal to π/2 if three plaquettes meet and decreasing by π/2 for each
additional plaquette (see Figure 6.4). Recall that the density of total curvature (i.e.


                                            102
   Figure 6.4: The five possible arrangements of rhombi around a vertex of the tiling.
               Equivalently, these are the five possible types of vertices present in
               the surface corresponding to the tiling. The Gaussian curvature of
               the lifted surface vanishes on its faces and edges, but it is singular at
               its vertices, contributing a total curvature of π/2, 0, 0,−π/2, and −π
               respectively from left to right at the five vertices shown.


Gaussian curvature) in the manifold traced out by the bond network is given by the
density of circulation (i.e. curl) of the Burgers vector density. In fact, it is easy to show

by complete enumeration of possible local Kekulé structures, that the total curvature
associated with the circulation of Burgers vectors in the three 6-cycles around an atom
is proportional to the average of the total curvatures associated with the three tiling
vertices surrounding it (see Figure 6.5).


   Note that both surfaces can only appear continuous and smooth when viewed at a

coarse-grained scale: one because it is traced out by point-like atoms, the other because
it is composed of discrete plaquettes. However, we have shown that on scales larger than
the lattice spacing, the total curvature in corresponding subregions of the two surfaces
is proportional. The constant of proportionality can be gotten rid of by appropriately

scaling the phason dimension so that the curvatures of the two surfaces are equal, as
suggested by the incomplete projection construction above.


   For a disordered, uniform Kekulé structures, this relation between the two surfaces is
particularly hard to corroborate in a simulation. This is because the height variations in



                                            103
                     Π
                                                     Π              Π           Π
         0       -                                                          -
                     2                   0       -
                                                                    2           2
                                                     2
                                             Π                          Π
             0
                                                                        2
                                             2




Figure 6.5: The Gaussian curvature in the manifold traced out by the bond net-
           work in equilibrium can be shown, by direct enumeration of local ar-
           rangements, to be proportional to the Gaussian curvature of the sur-
           face whose projection gives the rhombus tiling corresponding to the
           Kekulé structure. Three sample cases of the complete enumeration
           are presented. In each case, we traverse the loop (red) in a counter-
           clockwise direction, adding up the components of the Burgers vectors
           encountered (blue) tangent to the loop. The results are −ξ, 0, and +ξ,
           where ξ is a positive total curvature value that depends on the relative
           lengths of double and single bonds. We compare this value to the av-
           erage total curvature at the three surrounding vertices of the projected
           surface. The common ratio is 6ξ/π.




                                       104
   Figure 6.6: Two ordered Kekulé structures (left) which demonstrate the relation-
               ship between positive (top) or negative (bottom) Gaussian curvature in
               the surface whose projection is the corresponding tiling (center) and
               in the manifold traced out by the bond network in equilibrium (right).


surfaces associated with random tilings of π/3-rhombi grow only logarithmically with
the size of the system [48]. Therefore, as the relationship holds only on scales larger
than the lattice spacing, we require a huge system before the systematic height variations
associated with the phason strain become noticeable over the fluctuations on the scale of

the lattice spacing. However, for ordered Kekulé structures, where the height variations
may grow linearly with the size of the system, we can corroborate the relationship by
inspection, without even the need for simulation.


   We considered above the Kekulé structure where the double bonds are identified
with one of the three sublattices of bonds, for which the equilibrium conformation is
a flat sheet, compressed along the direction of double bonding. Consider then the two

Kekulé structures in Figure 6.6, where the sheet is divided into three or six sectors with



                                           105
uniform direction of double bonding in each sector. The manifold that will be traced
out by the network can be constructed by cutting a flat sheet into sectors, stretching or
compressing the sectors along the bisector line, and stitching them back together. These
manifolds, with vanishing Gaussian curvature except for a point of positive or negative

total curvature at the origin, are clearly the same as the surfaces we get by performing
the incomplete projection on the plaquette surfaces.


   The slow growth of height fluctuations in the case of uniform Kekulé structure is a
consequence of the slowly decaying correlations caused by the strong Kekulé constraint.
If we depart from the simple Kekulé-constrained binary model of bond heterogeneity

we chose at the beginning of the chapter, we might imagine that the situation would
change. For example, if we allowed a certain density of defects in the Kekulé structure,
such as atoms with no double bonds or with multiple ones, or made some allowance for
conjugated bonds, then these defects will presumably screen the correlations, permitting

the height fluctuations to grow faster. The analysis of the simple Kekulé case might be
a good starting point for analyzing those more complicated cases. In any case, the
interpretation of a bond heterogeneity as introducing fractional dislocations should hold
no matter the distribution of these bonds.


   Based on the similar previous results of Ref. [57] in a quasicrystalline tiling model,
it stands to reason that the ultimate result of this paper, directly relating accumulation

of strain in the phason space to accumulation of strain in the physical space, can be
generalized to the vast family of dimer covering and random tiling models.




                                             106
                                  BIBLIOGRAPHY

 [1] E. Agrell et al. Closest point search in lattices. IEEE Trans. Inform. Theory,
     48:2201, 2002.

 [2] J. Baker and A. Kudrollli. Maximum and minimum stable random packings of
     platonic solids. Phys. Rev. E, 82:061304, 2010.

 [3] J. W. Berenschot et al. Chemically anisotropic single-crystalline silicon nanotetra-
     hedra. Nanotechnology, 20:475302, 2009.

 [4] A. Bezdek and W. Kuperberg. Dense packing of space with various convex solids.
     2010. arXiv:1008.2398.

 [5] P. Biswas et al. Semidefinite programming approaches for sensor network localiza-
     tion with noisy distance measurements. IEEE Transactions on Automation Science
     and Engineering, 3:360, 2006.

 [6] M. J. Bowick et al. Crystalline order on a sphere and the generalized thomson
     problem. Physical Review Letters, 89:185502, 2002.

 [7] M. J. Bowick, D. R. Nelson, and A. Travesset. Interacting topological defects on
     frozen topographies. Phys Rev B, 62:8738, 2000.

 [8] M. J. Bowick and A. Travesset. The geometrical structure of 2d bond-orientational
     order. J Phys A, 34:1535, 2001.

 [9] J. D. Bryngelson and P. G. Wolynes. Spin glasses and the statistical mechanics of
     protein folding. Proc. Natl. Acad. Sci. USA, 84:7524, 1987.

[10] S. Cameron. Enhancing gjk: computing minimum and penetration distance be-
     tween convex polyhedra. In Proceedings of International Conference on Robotics
     and Automation, page 3112, 1997.

[11] T. M. Charlton. Maxwell, jenkin and cotterill and the theory of statically-
     indeterminate structures. Notes and Records of the Royal Society, 21:233, 1971.

[12] E. R. Chen. A dense packing of regular tetrahedra. Discrete Comput. Geom.,
     5:214, 2008.

[13] E. R. Chen, M. Engel, and S. C. Glotzer. Dense crystalline dimer packings of
     regular tetrahedra. Discrete Compu. Geom., 44:253, 2010.


                                          107
[14] H. Cohn, A. Kumar, and A. Schürmann. Ground states and formal duality relations
     in the gaussian core model. Phys. Rev. E, 80:061116, 2009.

[15] R. Connelly. Tensegrity structures: Why are they stable? In M. F. Thorpe and
     P. M. Duxbury, editors, Rigidity Theory and Applications, Fundamental Materials
     Research, pages 47–54. Springer US, 2002.

[16] J. H. Conway and N. J. A. Sloane. Sphere Packings, Lattices and Groups. Springer-
     Verlag, New York, 3 edition, 1998.

[17] J. H. Conway and S. Torquato. Packing, tiling and covering with tetrahedra. Proc.
     Natl. Acad. Sci. USA, 103:10612, 2006.

[18] L. A. Danzer. A family of 3d-spacefillers not permitting any periodic or quasiperi-
     odic tiling. In G. Chapuis and W. Paciorek, editors, Aperiodic ’94, page 11. World
     Scientific, Singapore, 1994.

[19] A. Donev et al. Unusually dense crystal packing of ellipsoids. Phys. Rev. Lett.,
     92:255506, 2004.

[20] V. Elser. Phase retrieval by iterated projections. J. Optical Soc. Amer. A, 20:40,
     2003.

[21] V. Elser and S. Gravel. Laminating lattices with symmetrical glue. Discrete Com-
     put. Geom., 43:363, 2010.

[22] V. Elser and I. Rankenburg. Deconstructing the energy landscape: constraint-based
     algorithms for folding heteropolymers. Phys. Rev. E, 73:026702, 2006.

[23] V. Elser, I. Rankenburg, and P. Thibault. Searching with iterated maps. Proc. Natl.
     Acad. Sci. USA, 104:418, 2007.

[24] Veit Elser and Ivan Rankenburg. Deconstructing the energy landscape: Constraint-
     based algorithms for folding heteropolymers. Phys. Rev. E, 73(2):026702, Feb
     2006.

[25] R. A. Engh and R. Huber. Accurate bond and angle parameters for x-ray protein
     structure refinement. Acta Cryst., A47:392, 1991.

[26] A. Fasolino, J. H. Los, and M. I. Katsnelson. Intrinsic ripples in graphene. Nature
     Materials, 6:858, 2007.



                                          108
[27] M. Gardner. The Colossal Book of Mathematics. Norton, New York, 2001.

[28] S. C. Glotzer and M. J. Solomon. Anisotropy of building blocks and their assembly
     into complex structures. Nat. Mater., 6:557, 2007.

[29] S. Gravel. Using Symmetries to Solve Asymmetric Problems. PhD thesis, Cornell
     University, Ithaca, New York, January 2009.

[30] S. Gravel and V. Elser. Divide and concur: a general approach to constraint satis-
     faction. Phys. Rev. E, 78:036706, 2008.

[31] E. C. Greyson, J. E. Barton, and T. W. Odom. Tetrahedral zinc blende tin sulfide
     nano- and microcrystals. Small, 2:368, 2006.

[32] M. R. Gryk, J. Vyas, and M. W. Maciejewski. Biomolecular nmr data analysis.
     Prog Nucl Magn Reson Spectrosc.

[33] A. Haji-Akbari, M. Engel, et al. Disordered, quasicrystalline and crystalline phases
     of densely packed tetrahedra. Nature, 462:773, 2009.

[34] T. C. Hales. A proof of the kepler conjecture. Ann. Math., 162:1065, 2005.

[35] C. L. Henley. Random tiling models. In Quasicrystal: the state of the art. World
     Scientific, Singapore, 1991.

[36] W. C. Herndon. Resonance theory and the enumeration of kekule structures. J.
     Chem. Educ., 51:10, 1974.

[37] N. J. Higham. Matrix nearness problems and applications. In M. J. C. Gover and
     S. Barnett, editors, Applications of Matrix Theory. Oxford University Press, 1989.

[38] D.C. Hilbert. Matematical problems. Bull. Am. Math. Soc., 8:437, 1902.

[39] B. K. P. Horn. Closed-form solution of absolute orientation using unit quaternions.
     J. Opt. Soc. Am. A, 4:629, 1987.

[40] B. K. P. Horn, H. M. Hilden, and S. Negahdaripour. Closed-form solution of
     absolute orientation using orthonormal matrices. J. Opt. Soc. Am. A, 5:1127, 1988.

[41] D. J. Hoylman. The densest lattice packing of tetrahedra. Bull. Amer. Math. Soc.,
     76:135, 1970.


                                          109
[42] D. J. Jacobs and M. F. Thorpe. Generic rigidity percolation: The pebble game.
     Phys. Rev. Lett., 75:4051, 1995.

[43] A. Jaoshvili et al. Experiments on the random packing of tetrahedral dice. Phys.
     Rev. Lett., 104:185501, 2010.

[44] Y. Jiao, F. H. Stillinger, and S. Torquato. Optimal packing of superballs. Phys.
     Rev. E, 79:041309, 2009.

[45] Y. Kallus and V. Elser. Dense-packing crystal structures of physical tetrahedra.
     Phys. Rev. E, 83:036703, 2011.

[46] Y. Kallus, V. Elser, and S. Gravel. Dense periodic packings of tetrahedra with
     small repeating units. Discrete Compu. Geom., 44:245, 2010.

[47] Y. Kallus, V. Elser, and S. Gravel. A method for dense packing discovery. Phys.
     Rev. E, 82:056707, 2010.

[48] R. Kenyon. Height fluctuations in the honeycomb dimer model. Communications
     in Mathematical Physics, 281:675, 2008.

[49] G. Kuperberg and W. Kuperberg. Double-lattice packings of convex bodies in the
     plane. Discrete Compu. Geom., 5:389, 1990.

[50] A. K. Lenstra, H. W. Lenstra, and L. Lovász. Factoring polynomials with rational
     coefficients. Math. Ann., 261:515, 1982.

[51] Ne-Te Duane Loh, Stefan Eisebitt, Samuel Flewett, and Veit Elser. Recover-
     ing magnetization distributions from their noisy diffraction data. Phys. Rev. E,
     82(6):061128, Dec 2010.

[52] A. D. MacKerell, D. Bashford, Bellott, R. L. Dunbrack, J. D. Evanseck, M. J. Field,
     S. Fischer, J. Gao, H. Guo, S. Ha, D. Joseph-McCarthy, L. Kuchnir, K. Kucz-
     era, F. T. K. Lau, C. Mattos, S. Michnick, T. Ngo, D. T. Nguyen, B. Prodhom,
     W. E. Reiher, B. Roux, M. Schlenkrich, J. C. Smith, R. Stote, J. Straub, M. Watan-
     abe, J. Wirkiewicz-Kuczera, D. Yin, and M. Karplus. All-atom empirical poten-
     tial for molecular modeling and dynamics studies of proteins. J. Phys. Chem. B,
     102:3586–3616, 1998.

[53] E. Meiner and F. Schilling. Drei gipsmodelle von flchen konstanter breite. Z. Math.
     Phys., 60:92, 1912.



                                          110
[54] N. D. Mermin. The space groups of icosahedral quasicrystals and cubic, or-
     thorhombic, monoclinic, and triclinic crystals. Rev. Modern Phys., 64:3, 1992.

[55] David Mitchell, Bart Selman, and Hector Levesque. Hard and easy distributions
     of sat problems. In Proceedings of the Tenth National Conference on Artificial
     Intelligence, page 459, 1992.

[56] Rmi Monasson, Riccardo Zecchina, Scott Kirkpatrick, Bart Selman, and Lidror
     Troyansky. Determining computational complexity from characteristic ’phase
     transitions’. Nature.

[57] F. Nori, M. Ronchetti, and V. Elser. Strain accumulation in quasicrystalline solids.
     Phys Rev Lett, 61:2774, 1988.

[58] Anant K. Paravastu, Richard D. Leapman, Wai-Ming Yau, and Robert Tycko.
     Molecular structural basis for polymorphism in alzheimer’s -amyloid fibrils. Proc.
     Natl. Acad. Sci. USA, 105:18349, 2008.

[59] Z. Quan and J. Fang. Superlattices with non-spherical building blocks. Nano
     Today, 5:390, 2010.

[60] D. Rowe and J. Jeremy. The Hilbert Challenge. Oxford University Press, 2001.

[61] R. Schneider. Convex Bodies: The Brunn-Minkowski Theory. Cambridge Univer-
     sity Press, 1993.

[62] A. Schürmann and F. Vallentin. Computational approaches to lattice packing and
     covering problems. Discrete Comput. Geom., 35:73, 2006.

[63] C.D. Schwieters, J.J. Kuszewski, N. Tjandra, and G.M. Clore. The xplor-nih nmr
     molecular structure determination package. J. Magn. Res., 160:66, 2003.

[64] Yang Shen, Frank Delaglio, Gabriel Cornilescu, and Ad Bax. Talos+: a hybrid
     method for predicting protein backbone torsion angles from nmr chemical shifts.
     Journal of Biomolecular NMR, 44:213, 2009.

[65] P. G. Szabo et al. New approaches to circle packing in a square. Springer-Verlag,
     New York, 2007.

[66] Z. Tang et al. Self-assembly of cdte nanocrystals into free-floating sheets. Science,
     314:274, 2006.



                                           111
[67] S. Torquato. Reformulation of the covering and quantizer problems as ground
     states of interacting particles. Physical Review E, 82:056109, 2010.

[68] S. Torquato and Y. Jiao. Dense packings of polyhedra: Platonic and archimedean
     solids. Phys. Rev. E, 80:041104, 2009.

[69] S. Torquato and Y. Jiao. Dense packings of the platonic and archimedean solids.
     Nature, 460:876, 2009.

[70] S. Torquato and Y. Jiao. Analytical construction of a family of dense tetrahedron
     packings and the role of symmetry. Phys. Rev. E, 81:041310, 2010.

[71] S. Torquato and F. H. Stillinger. Jammed hard-particle packings: From kepler to
     bernal and beyond. Rev. Mod. Phys., 82:2633, 2010.

[72] G. van den Bergen. Proximity queries and penetration depth computation on 3d
     game objects, 2001. Game Developers Conference.

[73] M. K. Williamson. Applications of the noe in molecular biology. Annu. Rep. NMR
     Spect., 65:77, 2009.

[74] M. P. Williamson, T. F. Havel, and K. Wüthrich. Solution conformation of pro-
     teinase inhibitor iia from bull seminal plasma by 1 H nuclear magnetic resonance
     and distance geometry. J. Mol. Bio., 182:195, 1985.

[75] P. Yunker, Z. Zhang, K. B. Aptowicz, and A. G. Yodh. Irreversible rearrange-
     ments, correlated domains, and local structure in aging glasses. Phys. Rev. Lett.,
     103:115701, 2009.

[76] Weixiong Zhang. Phase transitions and backbones of 3-sat and maximum 3-sat. In
     Toby Walsh, editor, Principles and Practice of Constraint Programming. Springer-
     Verlag, 2001.




                                         112
