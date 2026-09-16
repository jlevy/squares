                                                Packing unequal rectangles and squares in a fixed size circular
                                                          container using formulation space search
                                                                                  C.O. López∗1 and J.E. Beasley†2
arXiv:1802.07519v1 [math.OC] 21 Feb 2018




                                            1
                                                Faculty of Sciences, National Autonomous University of Mexico, Mexico City, Mexico
                                                    2
                                                      Mathematical Sciences, Brunel University, Uxbridge UB8 3PH, UK and JB
                                                                              Consultants, Morden, UK

                                                                               October 2017, Revised February 2018


                                                                                                 Abstract
                                                          In this paper we formulate the problem of packing unequal rectangles/squares into a fixed
                                                      size circular container as a mixed-integer nonlinear program. Here we pack rectangles so as
                                                      to maximise some objective (e.g. maximise the number of rectangles packed or maximise the
                                                      total area of the rectangles packed). We show how we can eliminate a nonlinear maximisation
                                                      term that arises in one of the constraints in our formulation. We indicate the amendments
                                                      that can be made to the formulation for the special case where we are maximising the number
                                                      of squares packed. A formulation space search heuristic is presented and computational
                                                      results given for publicly available test problems involving up to 30 rectangles/squares. Our
                                                      heuristic deals with the case where the rectangles are of fixed orientation (so cannot be
                                                      rotated) and with the case where the rectangles can be rotated through ninety degrees.

                                              Keywords: Formulation space search; Mixed-integer nonlinear program; Rectangle packing;
                                           Square packing


                                           1         Introduction
                                           In this paper we consider the problem of packing non-identical rectangles (i.e. rectangles of
                                           different sizes) into a fixed size circular container. Since the circular container may not be large
                                           enough to accommodate all of the rectangles available to be packed there exists an element of
                                           choice in the problem. In other words we have to decide which of the rectangles will be packed,
                                           and moreover for those that are packed their positions within the container. The packing should
                                           respect the obvious constraints, namely that the packed rectangles do not overlap with each
                                           other and that each packed rectangle is entirely within the container. This packing should be
                                           such so as to maximise an appropriate objective (e.g. maximise the number of rectangles packed
                                           or maximise the total area of the rectangles packed).
                                               To illustrate the problem suppose we have ten rectangles with sizes as shown in Table 1 to be
                                           packed into a fixed sized circular container. The rectangles shown in Table 1 have been ordered
                                           into ascending area order.
                                                ∗
                                                    claudia.lopez@ciencias.unam.mx
                                                †
                                                    john.beasley@brunel.ac.uk; john.beasley@jbconsultants.biz


                                                                                                      1
                              Rectangle    Length     Width
                                  1         1.10       1.61
                                  2         2.20       1.08
                                  3         1.68       1.46
                                  4         1.82       2.61
                                  5         2.70       2.57
                                  6         3.21       2.21
                                  7         2.99       3.51
                                  8         3.68       3.42
                                  9         4.62       3.36
                                 10         3.79       4.79

          Table 1: Rectangle packing example, circular container radius 4.18


Regarding the rectangles as being of fixed orientation, i.e. they cannot be rotated, then:

• If we are wish to maximise the number of rectangles packed Figure 1 shows the solution
  as derived by the approach presented in this paper. In that figure we can see that seven
  of the ten rectangles have been packed, three rectangles are left unpacked.

• If we are wish to maximise the total area of the rectangles packed Figure 2 shows the
  solution as derived by the approach presented in this paper. In that figure we can see that
  five of the ten rectangles have been packed.




                                                  4
                                     6                  1



                               3                        5
                                          7



                                          2


  Figure 1: Maximise the number of rectangles packed, no rotation, solution value 7

If the rectangles can be rotated through ninety degrees then:

• If we are wish to maximise the number of rectangles packed Figure 3 shows the solution
  as derived by the approach presented in this paper. In that figure we can see that seven
  of the ten rectangles have been packed, three rectangles are left unpacked.



                                              2
                                                       8
                                                                    3
                                   2

                                                                        4
                                                   9




Figure 2: Maximise the total area of the rectangles packed, no rotation, solution value 37.6878


   • If we are wish to maximise the total area of the rectangles packed Figure 4 shows the
     solution as derived by the approach presented in this paper. In that figure we can see that
     seven of the ten rectangles have been packed.

    In Figure 3 and Figure 4 the letter r after the rectangle number indicates that the rectangle
has been rotated through ninety degrees. Comparing Figure 1 and Figure 3 we can see that they
both involve the packing of seven rectangles. Whilst allowing rotation through ninety degrees
allows the possibility of a better solution as compared with the no rotation case this is by no
means assured. Comparing Figure 2 and Figure 4 we can see that in this particular case an
improvement in the total area of the rectangles packed has been made by making use of rotation.




                                               6               4r



                                                                    2r
                                       5
                                                           7
                                                                    1
                                           3



       Figure 3: Maximise the number of rectangles packed, rotation allowed, solution value 7

    The structure of this paper is as follows. In Section 2 we review the literature relating to
the packing of rectangles. We discuss application areas where rectangle packing problems arise.
We also review the literature relating to the particular metaheuristic, formulation space search,

                                                       3
                                                  2
                                                           3r


                                              8
                                                                  5r



                                              6              4r


                                                      1r

    Figure 4: Maximise the total area of the rectangles packed, rotation allowed, solution value 37.9687


used in this paper. In Section 3 we formulate the problem of packing unequal rectangles/squares
into a fixed size circular container as a mixed-integer nonlinear program. We show how we can
eliminate a nonlinear maximisation term that arises in one of the constraints in our formulation.
We also show how we can deal with the case where rectangles can be rotated through ninety
degrees. We indicate the amendments that can be made to the formulation for the special
case where we are maximising the number of squares packed. Section 4 gives details of the
formulation space search heuristic that we use to solve the problem. Computational results are
presented in Section 5 for problems involving up to 30 rectangles/squares. In that section we
give results both for maximising the number of rectangles/squares packed and for maximising
the total area of the rectangles/squares packed. Finally in Section 6 we present our conclusions.


2      Literature survey
In this section we first discuss the literature relating to the problem of packing rectangles and its
applications. We then discuss the literature relating to the particular metaheuristic, formulation
space search, we use to solve the rectangle packing problem considered in this paper.

2.1     Rectangle packing
The majority of the work in the literature related to rectangle packing deals with packing rect-
angles/squares within a larger container that is either a square, or a rectangle, or a rectangular
strip with one dimension fixed and the other dimension variable (e.g. fixed width, but variable
length).
    A common feature of such work is that it is assumed that all of the smaller rectangles
have to be packed into the larger container, which leads to an optimisation problem relating
to minimising the dimension of the container. For example for a square container a natural
optimisation problem is to minimise the side of the square container (which also minimises
its perimeter and area). For a rectangular container one can examine minimising either its
perimeter or its area. For a rectangular strip one can minimise the variable dimension. With


                                                      4
respect to the packing of rectangles within a circular container then the natural optimisation
problem is to minimise the radius of the container.
    In our literature survey below we focus principally on papers that take a packing approach.
The reader may be aware that a closely related problem to packing is cutting e.g. cutting
rectangles from a larger stock rectangle. There has been a substantial amount of work presented
in the literature dealing with cutting. However much of that work involves additional restrictions
with regard to the cuts that are made. One such restriction might be that the cuts are guillotine
cuts, a guillotine cut on a rectangle being a cut from one edge of the rectangle to the opposite
edge which is parallel to the two remaining edges. Another such restriction might be to limit the
cutting to a number of stages, where at each stage guillotine cuts are made, but in a direction
opposite to that adopted in the previous stage. So for example in the first stage guillotine cuts
are made parallel to the y-axis, then in the second stage guillotine cuts are made parallel to the
x-axis, etc. Since the primary focus of the work presented in this paper is packing rectangles
within a circular container we, for space reasons, exclude detailed consideration of work focused
on cutting rectangles from rectangular containers from the literature survey presented below.
    Unless otherwise stated all of the work considered below deals with orthogonal packing, so
rectangles/squares are packed without rotation.
    Li and Cheng [31] show that the problem of determining whether a set of squares can be
packed into a larger rectangle is strongly NP-complete. In addition they show that the problem
of determining whether a set of rectangles can be packed into a square is NP-complete. Leung
et al. [30] show that the problem of determining whether a set of squares can be packed into a
square is strongly NP-complete.
    Picouleau [47] considered the worst-case analysis of three fast heuristics for packing squares
into a square container so as to minimise the size of the square. Murata et al. [44] present a
simulated annealing algorithm for the problem for packing rectangles into a rectangular container
so as to minimise the size (area) of the container. Liu and Teng [33] present a genetic algorithm
for the problem of packing a set of rectangles into a strip of fixed width using minimum height.
    Wu et al. [53] present a heuristic attempting to pack every member of a set of rectangles
inside a fixed size rectangular container. Caprara et al. [14] discuss absolute worst-case perfor-
mance ratios for lower bounds on packing rectangles/squares into a square container so as to
minimise the size of the square container. They consider the case where the rectangles have fixed
orientation and the case where they can be rotated through ninety degrees. Huang et al. [27]
present a heuristic approach to packing rectangles within a fixed size rectangular container so as
to maximise the total area of the rectangles packed where the rectangles can be rotated through
ninety degrees.
    Birgin et al. [7] consider packing the maximal number of identically sized rectangles inside
a rectangular container. Their approach is based upon recursive partitioning and allows the
rectangles to be rotated through ninety degrees. Korf et al. [29] consider the problem of packing
a set of rectangles (with and without ninety degree rotation allowed) in a rectangular container
of minimal area. They adopt a constraint satisfaction approach to the problem. Maag et al. [39]
consider the problem of packing a set of rectangles in a rectangular container of minimal area.
Their approach is based on relaxing the constraint on rectangle overlap.
    Huang and Korf [26] consider the same problem as [29] but adopt an approach based on first
deciding x-coordinate values for each rectangle. Bortfeldt [10] presents a number of heuristic
approaches (based on solution methods for two-dimension knapsack and two-dimension strip
packing) for packing rectangles into a rectangular container so as to minimise the size (area) of


                                                5
the container.
    Martello and Monaci [41] consider the problem of packing rectangles/squares into a square
container so as to minimise the size of the container. They present a linear integer programming
formulation and an exact approach based on a two-dimensional packing algorithm as well as a
metaheuristic. They deal with the case where the rectangles have fixed orientation and also the
case where they can be rotated through ninety degrees. Delorme et al. [17] present a Benders’
decomposition approach to the problem of packing a set of rectangles (with ninety degree rotation
allowed) into a strip of fixed width using minimum height. Their approach (as they discuss)
can be easily applied to the problem of packing rectangles/squares into a square container of
minimal size.
    It is important to note here that a number of the approaches given in the literature for
the problem of packing rectangles within a rectangular container utilise the fact that rectangle
position coordinates can be taken from a finite discrete set (e.g. by packing rectangles so that
they are positioned at their lowest bottom-left position). For example see [17, 41]. However in
this paper we consider a circular container, and the lack of rectangular sides to the container
render such discretisation approaches invalid for the problem we consider.
    As far as we are aware the problem considered in this paper of packing unequal rectan-
gles/squares into a circular container has only been considered by just a few papers in the
literature previously. Li et al. [32] consider the problem of packing orthogonal unequal rectan-
gles in a circular container with an additional constraint related to mass balance. Their objective
function is to minimise the radius of the container. A heuristic algorithm is presented.
    Hinostroza et al. [25] consider the problem of cutting rectangular boards from a log, regarded
as a circular container. They present a nonlinear formulation of the problem (based on [9]), and
two heuristics, one based on ordering the rectangles and the other on simulated annealing. Note
here that, in our judgement, their formulation is flawed.
    Work has been presented in the literature relating to packing rectangles/squares into arbi-
trary convex regions, and such work can be applied to a circular container. We discuss this work
below.
    Birgin at al [8] introduce the concept of sentinels sets, which are finite subsets of the items
to be packed such that, when two items are superposed, at least one sentinel of one item is
in the interior of the other item. Using these sentinel sets they consider packing identical
rectangles within both convex regions and a rectangular container, with and without rectangle
rotation (both ninety degree rotation and arbitrary rotation). Birgin et al. [9] consider packing
rectangles (with and without ninety degree rotation). Their objective is to feasibly pack all
rectangles. Iteratively increasing the number of rectangles enables one to maximise the number
of (identical) rectangles placed. Their approach is based on nonlinear optimisation.
    Birgin and Lobato [6] consider packing identical rectangles within an arbitrary convex region
where a common rotation of θ degrees (not restricted to θ = 90) of all the rectangles is allowed.
In addition a rectangle can be rotated through ninety degrees before a rotation of θ is applied.
Their solution method is a combination of branch and bound and active-set strategies for bound-
constrained minimization of smooth functions. Cassioli and Locatelli [15] present a heuristic
approach based on iterated local search for the problem of packing the maximum number of
rectangles of the same size within a convex region (where rectangle rotation through ninety
degrees is allowed).
    Andrade and Birgin [3] present symmetry breaking constraints for two problems relating to
packing identical rectangles (with or without ninety degree rotation) in a polyhedron. They


                                                6
consider packing as many identical rectangles as possible within a given polyhedron as well
as finding the smallest polyhedron of a specified type that accommodates a fixed number of
identical rectangles.
    More generally Birgin [5] considers the application of nonlinear programming in packing
problems. They note that nonlinear programming formulations and methods have been suc-
cessfully applied to a wide range of packing problems. In particular we in this paper, as in the
formulation presented below, use a nonlinear model.

2.2   Applications
The problem of packing rectangular objects into a larger container (equivalently cutting rect-
angular objects from a larger container) appears in a number of practical situations. As noted
in Dowsland and Dowsland [18] the earliest applications were in glass and metal industries
where smaller rectangular objects had to be cut from larger (typically rectangular) stock pieces.
A further application they discuss occurs in pallet loading where rectangular boxes have to be
packed onto a wooden pallet for transport. Sweeney and Paternoster [49] present an application-
orientated research bibliography that lists some of the early work related to packing.
    Lodi et al. [34] present a literature survey relating to two-dimensional packing and solu-
tion approaches. They mention a number of practical applications relating to rectangle cut-
ting/packing. These include the arrangement of articles and advertisements on newspaper pages
and in the wood and glass industry cutting rectangular items from larger sheets of material.
They also mention the placement of goods on shelves in warehouses. Wascher et al. [52] also
mention some practical applications (such as pallet loading) in their work presenting a typology
of cutting and packing problems.
    In relation to the specific problem considered in this paper of packing unequal rectan-
gles/squares into a fixed size circular container we are aware of a number of practical appli-
cations.
    For example in the forestry/lumber industry consider the cutting of rectangular wooden
boards from timber logs made from trees that have been felled. Here, by approximating the
shape of the timber log by a circle of known radius, we have the problem considered in this
paper, namely which of the rectangles (of known sizes) that we desire to cut should be cut from
the circular log [25].
    A further practical example relates to the problem considered in [32] which was concerned
with packing orthogonal unequal rectangles in a circular container with an additional constraint
related to mass balance. Here the container was a satellite and the rectangular objects related
to items comprising the satellite payload. The mass balance constraint considered in [32] was a
single nonlinear constraint that involved the (mass weighted) centres of each rectangle. Since,
as will become apparent below, our formulation space search approach for packing rectangles
into a fixed size circular container is based on a mixed-integer nonlinear program it is trivial
to introduce into our approach a single additional nonlinear constraint (such as a mass balance
constraint).

2.3   Formulation space search
When solving nonlinear non-convex problems with the aid of a solver, Mladenović et al. [42]
observed that different formulations of the same problem may have different characteristics.


                                               7
Hence a natural way to proceed is by swapping between formulations. Under this framework
Mladenović et al. [42] use formulation space search (henceforth FSS) for the circle packing
problem considering two formulations of the problem: one in a Cartesian coordinate system, the
other in a Polar coordinate system. Their algorithm solves the problem with one formulation at
a time and when the solution is the same for all formulations the algorithm terminates. They
consider packing identical circles into the unit circle and the unit square.
    In Mladenović et al. [43] they improve on [42] by considering a mixed formulation of the
problem. They set a subset of the circles in the Cartesian system whilst the rest of the circles
were in the Polar system. López and Beasley [35] use FSS for the problem of packing equally
sized circles inside a variety of containers. They present computational results which show that
their approach improves upon previous results based on FSS presented in the literature. For
some of the containers considered they improve on the best result previously known. López and
Beasley [36] use FSS to solve the packing problem with non-identical circles in different shaped
containers. They present computational results which were compared with benchmark problems
and also proposed some new instances. López and Beasley [38] use FSS to solve the problem of
packing non-identical circles in a fixed size container.
    Essentially FSS exploits the fact that:
    • because of the nature of the solution process in nonlinear optimisation we often fail to
      obtain a globally optimum solution from a single formulation; and so
    • perturbing/changing the formulation and then resolving the nonlinear program may lead
      to an improved solution.
Given the above it is a simple matter to construct iterative schemes that move between formu-
lations in a systematic manner.
    FSS has been applied to a few problems additional to circle packing (e.g. timetabling [28]).
In [37] FSS was used to solve some benchmark mixed-integer nonlinear programming problems.
In a more general sense an adaptation to FSS was presented in [11] for solving continuous
location problems. More discussion as to FSS can be found in Hansen et al. [21]. A related
approach is variable space search, which has been applied to graph colouring (Hertz et al. [23,
24]). Other related approaches are variable formulation search which has been applied to the
cutwidth minimisation problem [19, 45] and variable objective search which has been applied to
the maximum independent set problem [13].
    As noted in Pardo et al. [45] variable space search, variable formulation search and variable
objective search contain similar ideas as originally expounded using FSS. At a slightly more
general level FSS can be regarded as a variant of variable neighbourhood search, for example
see [2, 22].


3    Formulation
In this section we first present our basic formulation for the problem of packing unequal rectan-
gles in a fixed size circular container as a mixed-integer nonlinear program (MINLP). We then
show how we can eliminate a nonlinear maximisation term that arises in one of the constraints
in our formulation. We indicate how we can deal with the case where rectangles can be rotated
through ninety degrees. For the special case where we are maximising the number of squares
packed we present the amendments that can be made to the formulation.




                                               8
3.1   Basic formulation
The problem we consider is to find the maximal weighted packing of n unequal rectangles in a
fixed size circular container. Here we have the option, for each unequal rectangle, of choosing
to pack it or not. We can formulate this problem as follows.
    Let the fixed size circular container be of radius R and, without loss of generality, let it be
centred at the origin of the Euclidean plane. We have n rectangles from which to construct a
packing, where rectangle i has a horizontal side of length Li and a vertical side of width Wi ,
and value (if packed) Vi . In our basic formulation we do not allow any rotation when packing
rectangles so that rectangles are packed with their horizontal (length) edges parallel to the x-
axis, their vertical (width) edges parallel to the y-axis. Clearly if we are dealing with packing
squares then Li = Wi . Here we label the rectangles so that they are ordered in increasing size
(area) order (i.e. Li Wi ≤ Li+1 Wi+1 i = 1, . . . , n − 1).
    Using a value Vi here for each rectangle i enables us to consider a number of different
problems within the same formulation. For example if we take Vi = 1 i = 1, . . . , n then we have
the problem of maximising the number of rectangles packed. If we take Vi = Li Wi i = 1, . . . , n
then we have the problem of maximising the total area of the rectangles packed. Alternatively
the Vi i = 1, . . . , n can be assigned arbitrary values.
    Then the variables are:
    • αi = 1 if rectangle i is packed, 0 otherwise; i = 1, . . . , n
    • (xi , yi ) the position of the centre of rectangle i; i = 1, . . . , n
With regard to the positioning (so (xi , yi )) of any unpacked rectangle i (for which αi = 0) our
formulation forces all unpacked rectangles to be positioned at the origin. Let Q be the set of all
rectangle pairs [(i, j) | i = 1, ..., n; j = 1, ..., n; j > i]. The formulation is:
                 n
                 X
        max            αi Vi                                                                           (1)
                 i=1
  subject to
                     q                                  q
               − αi ( (R2 − Wi2 /4) − Li /2) ≤ xi ≤ αi ( (R2 − Wi2 /4) − Li /2) i = 1, . . . , n (2)
                     q                                  q
               − αi ( (R2 − L2i /4) − Wi /2) ≤ yi ≤ αi ( (R2 − L2i /4) − Wi /2) i = 1, . . . , n (3)
               (xi + Li /2)2 + (yi + Wi /2)2 ≤ αi R2 + (1 − αi )(L2i /4 + Wi2 /4)      i = 1, . . . , n (4)
               (xi + Li /2) + (yi − Wi /2) ≤ αi R + (1 − αi )(L2i /4 + Wi2 /4)
                               2           2        2
                                                                                       i = 1, . . . , n (5)
               (xi − Li /2)2 + (yi + Wi /2)2 ≤ αi R2 + (1 − αi )(L2i /4 + Wi2 /4)      i = 1, . . . , n (6)
               (xi − Li /2)2 + (yi − Wi /2)2 ≤ αi R2 + (1 − αi )(L2i /4 + Wi2 /4)      i = 1, . . . , n (7)
               αi αj [max{|xi − xj | − (Li + Lj )/2, |yi − yj | − (Wi + Wj )/2}] ≥ 0   ∀(i, j) ∈ Q     (8)
               αi ∈ {0, 1}                                                             i = 1, . . . , n (9)

   The objective function, Equation (1), maximises the value of the rectangles q
                                                                               packed. Equa-
tion (2) ensures that if a rectangle is packed (i.e. αi = 1) its x-coordinate lies in [−( (R2 − Wi2 /4)−
          q
Li /2), +( (R2 − Wi2 /4) − Li /2)]. These limits can be easily deduced from geometric consid-
erations, e.g. consider the centre x-coordinate value associated with a rectangle placed with its
centre on the x-axis and with two of its corners just touching the circular container. The key


                                                    9
feature of Equation (2) is that if the rectangle is not packed (i.e. αi = 0) then the x-coordinate is
forced to be zero. Equation (3) is the equivalent constraint to Equation (2) for the y-coordinate.
    Equations (4)-(7) ensure that if a rectangle is packed (so for rectangle i with αi = 1) its
centre is appropriately positioned such that the entire rectangle lies inside the circular container.
To achieve this we need to ensure that all four corners of the rectangle lie inside the circular
container. These four corners are (xi ± Li /2, yi ± Wi /2) and Equations (4)-(7) ensure that
the (squared) distance from the origin to each these corners is no more than the (squared)
radius of the container. Note that if the rectangle is packed (so αi = 1) the left-hand side of
Equations (4)-(7) is R2 .
    If the rectangle is not packed (so αi = 0) then from Equations (2),(3) the rectangle is
positioned at the origin (so has xi = yi = 0). In that case the left-hand side of Equations (4)-(7)
becomes L2i /4 + Wi2 /4, as does the right-hand side, and so the constraints are automatically
satisfied.
    Equation (8) guarantees that any two rectangles i and j which are both packed (so αi =
αj = 1) do not overlap each other. This constraint is derived from that given previous in [16]. It
states that two rectangles of size [Li , Wi ] and [Lj , Wj ] do not overlap provided that the difference
between their centre x-coordinates is at least (Li + Lj )/2 or that the difference between their
centre y-coordinates is at least (Wi + Wj )/2 (or both). If one or other of the rectangles is not
packed the left-hand side of Equation (8) becomes zero due to the product term (αi αj ) which
means that the constraint is automatically satisfied. Equation (9) is the integrality constraint.
    As discussed above our formulation positions any unpacked rectangle at the origin. For un-
packed rectangle i the inclusion of an appropriate αi term on the left-hand side of Equation (8)
ensures that this unpacked rectangle, although positioned at the origin, does not actively par-
ticipate in the overlap constraint which must apply between all packed rectangles.
    Our formulation (Equations (1)-(9)) is a mixed-integer nonlinear program (MINLP). Com-
putationally MINLPs are recognised to be very demanding, involving as they do both an element
of combinatorial choice and solution of an underlying continuous nonlinear program. For the
problem considered in this paper the combinatorial choice relates to the choice of the set of
rectangles to be packed, and the underlying continuous nonlinear program relates to deciding
where to feasibly position within the circular container the rectangles that are packed.

3.2    Elimination of the maximisation term
The overlap constraint (Equation (8)) contains the expression max{|xi − xj | − (Li + Lj )/2, |yi −
yj | − (Wi + Wj )/2}. For the particular problem considered in this paper this maximisation term
can be eliminated, albeit by enlarging the size of the MINLP to be solved.
     Introduce additional continuous variables βij , ∀(i, j) ∈ Q, defined by:

                          0 ≤ βij ≤ 1                            ∀(i, j) ∈ Q                        (10)

   Then we can replace Equation (8) by:
                                                                              
  αi αj βij [|xi − xj | − (Li + Lj )/2] + (1 − βij )[|yi − yj | − (Wi + Wj )/2] ≥ 0   ∀(i, j) ∈ Q   (11)

    The logic here is that the αi αj term ensures that the Equation (11) is always satisfied when
either αi = 0 or αj = 0 (as indeed it does in Equation (8)). It only remains to check therefore
the validity of replacing Equation (8) with Equation (11) in the case αi = αj = 1.


                                                  10
    When αi = αj = 1 Equation (11) becomes βij [|xi − xj | − (Li + Lj )/2] + (1 − βij )[|yi − yj | −
(Wi +Wj )/2] ≥ 0. Now the weighted sum on the left-hand side of this constraint can only be non-
negative provided that at least one of the two terms in it is itself non-negative. In other words
Equation (11) will ensure that one (or both) of [|xi −xj |−(Li +Lj )/2] and [|yi −yj |−(Wi +Wj )/2]
will be non-negative. Since one or both of these terms are non-negative it is therefore true that
the maximisation term in Equation (8), max{|xi − xj | − (Li + Lj )/2, |yi − yj | − (Wi + Wj )/2},
must also be non-negative. This in turn implies that Equation (8) is satisfied. Therefore it is
valid to replace Equation (8) by Equation (11).
    Note here that it is also valid to replace Equation (8) by Equation (11) if we define βij as
binary (zero-one) variables. However we might well expect there to be computational benefit in
defining these variables as continuous, rather than binary, variables.

3.3   Rotation
As is common in the literature (e.g. [7, 14, 25, 26, 29, 34, 39, 41]) in the basic formulation pre-
sented above we did not allow any rotation when packing, so that the items to be packed (rect-
angles/squares) were packed with their horizontal (length) edges parallel to the x-axis, their
vertical (width) edges parallel to the y-axis. If rotation of any item is allowed (which might be
dependent on the practical problem being modelled) then the situation becomes more complex,
although obviously rotation might enable a better solution to be found.
    In the literature rotation through ninety degrees is the most common situation modelled
(e.g. [7,14,17,26,27,29,32,41,44,53]). Clearly rotation through ninety degrees is irrelevant when
we are packing squares (as they are the same under ninety degree rotation) and only relevant
when we are dealing with unequally sized rectangles. Our formulation can be extended to deal
with rotation through ninety degrees as discussed below. Rotation through an arbitrary angle
cannot be dealt with by our approach.
    If the rectangles can be rotated through ninety degrees then this is easily incorporated
into our formulation. Suppose that rectangle i can be rotated through ninety degrees. Then
create a new rectangle (j say) that represents rectangle i if it is rotated, so that we have
Lj = Wi , Wj = Li , Vj = Vi . Add to the formulation:

                                           αi + αj ≤ 1                                         (12)

Equation (12) ensures that we cannot use both the original rectangle i and its rotated equivalent
j. Dealing with rectangle rotation therefore requires creating a new rectangle for each original
rectangle that can be rotated and adding a single constraint to the formulation.
    In terms of the effect on the formulation then if all n rectangles can be rotated this only
directly adds n constraints (Equation (12)) to the formulation. However the creation of an
additional n rotated rectangles doubles the number of rectangles to be considered for packing.
This means that the number of linear constraints associated with Equations (2),(3) doubles, as
does the number of nonlinear constraints associated with Equations (4)-(7). The more significant
effect is that the number of nonlinear constraints associated with Equation (8) increases from
n(n − 1)/2 to 2n(2n − 1)/2 (so approximately increases by a factor of 4). This increase in the
number of nonlinear constraints associated with Equation (8) also carries through to increase
the number of βij variables (Equation (10)) that need to be considered by an (approximate)
factor of 4. For this reason we would expect that, computationally, dealing with a problem with


                                                11
n rectangles with fixed orientation becomes much more challenging if all n rectangles can be
rotated.

3.4   Maximising the number of squares packed
From our previous work [38] we know that when we are considering a packing problem where
all the items to be packed can be ordered such that item i fits inside item j for all j > i then,
in the case where we are maximising the number of items packed, the optimal solution consists
of the first K items, for some K.
     Clearly items can be ordered to fit inside each other if we are considering packing squares,
i.e. order the squares in increasing size (length) order, but such an ordering is unlikely to be
possible if we are packing rectangles. Hence we shall just consider square packing here.
     In the case of square packing therefore, when we are maximising the number of squares
packed, we can impose the additional constraints:

               αi−1 ≥ αi                      i = 2, . . . , n                                 (13)
                                             k
                                             X
               αk = 0                   if         L2i > πR2            k = 1, . . . , n       (14)
                                             i=1

Equation (13) ensures that if αi is one (so square i is packed) then αi−1 must also be one (so
square i − 1 is packed). If square i is not packed (αi = 0) then the right-hand side of this
constraint is zero, so the constraint is always satisfied whatever the value for αi−1 . Collectively
the (n − 1) inequalities represented in Equation (13) ensure that the optimal solution consists
of the first K squares, for some K.
    In Equation (14) we have that if we were to pack square k then we would have to pack all
squares up to and including square k. If this packing exceeds the area of the container then
clearly square k cannot be packed.
    Aside from these additional constraints we can amend the overlap constraint, Equation (11).
Note that Equation (11) includes a αi αj term and applies for (i, j) ∈ Q, where Q is defined to
have j > i. Now if αj = 1 we automatically know that αi = 1 (since j > i) and hence that
αi αj = 1. If αj = 0 then it is irrelevant what value αi takes since we must have αi αj = 0. In
other words the αi αj term in Equation (11) can be replaced by αj so that the overlap constraint,
Equation (11), becomes:
                                                                             
    αj βij [|xi − xj | − (Li + Lj )/2] + (1 − βij )[|yi − yj | − (Wi + Wj )/2] ≥ 0 ∀(i, j) ∈ Q (15)

Note here that we have used Wi and Wj in Equation (15) for clarity of comparison with Equa-
tion (11). Obviously since we are just considering square packing here we have Wi = Li i =
1, . . . , n.


4     FSS algorithm
In this section we present our FSS algorithm for the problem. For simplicity we present our
approach using the basic formulation of the problem, Equations (1)-(9), before the amendments
as discussed above (i.e. elimination of the maximisation term and adaptions for packing squares).
We discuss at the end of this section how we incorporate a number of other constraints, presented
in this section, into our approach.

                                                    12
4.1    Algorithm
Consider the formulation, Equations (1)-(9), given above. Letting δ be a small positive constant
replace the integrality requirement, Equation (9), by:
                        n
                        X
                              αi (1 − αi ) ≤ δ                                                       (16)
                        i=1
                        0 ≤ αi ≤ 1                                  i = 1, . . . , n                 (17)
    If δ was zero these equations would force [αi , i = 1, . . . , n] to assume zero-one values.
However given the capabilities of nonlinear optimisation software simply replacing an explicit
integrality condition by Equations (16),(17) would not be computationally successful, since we
would be hoping to generate a (globally optimal) solution to a continuous nonlinear optimisation
problem with a very tight inequality constraint. Note that if δ is zero then Equation (16) is
effectively an equality constraint as the left-hand side is non-negative.
    Accordingly we adopt a heuristic approach and have δ > 0. Hence our original MINLP,
Equations (1)-(9), has now become a continuous nonlinear optimisation problem, since we have
relaxed the integrality requirement using Equations (16),(17). This nonlinear optimisation prob-
lem is optimise Equation (1) subject to Equations (2)-(8),(16),(17). We refer to this problem as
the continuous FSS relaxation of the problem.
    If we solve this nonlinear problem the [αi , i = 1, . . . , n] can deviate (albeit only slightly, if δ
is small) from their ideal zero-one values, but we can round them to their nearest integer value
to recover an integer set of values. Given an integer set of values for [αi , i = 1, . . . , n] then the
original formulation (Equations (1)-(9)) becomes a nonlinear feasibility problem. This nonlinear
feasibility problem is to find positions (xi , yi ) for each rectangle i that we have chosen to pack
(so with αi = 1 in the rounded solution). Note here that this is a feasibility problem as the
objective function, Equation (1), is purely a function of the zero-one variables (and these have
been fixed by rounding).
    With just a single value for δ we have just a single nonlinear problem: optimise Equation (1)
subject to Equations (2)-(8),(16),(17). However changing δ is a systematic fashion creates a
series of different problems that can be given to an appropriate nonlinear solver in an attempt
to generate new and improved solutions to our original MINLP. The idea here is that altering
δ perturbs the nonlinear formulation and hence, given the nature of any nonlinear solution
software, might lead to a different solution.
    The pseudocode for our FSS algorithm for the rectangle packing problem considered in this
paper is presented in Algorithm 1. In this pseudocode let P denote the original MINLP (here
optimise Equation (1) subject to Equations (2)-(9)) and P ∗ denote the continuous FSS relaxation
(here optimise Equation (1) subject to Equations (2)-(8),(16),(17)).
    We first initialise values, here Zbest is the best feasible solution found and t is an iteration
counter. We then solve the original MINLP P .
    In this pseudocode all attempts to solve a nonlinear problem (e.g. P or P ∗ ) must be subject
to a time limit, since otherwise the computation time consumed could become extremely high.
For this reason we always terminate the solution process after a predefined time limit, returning
the best feasible solution found (if one has been found). In the computational results reported
later below this time limit was set to 10n seconds.
    SCIP is capable of solving our MINLP formulation P to proven global optimality because
SCIP restricts the type of nonlinear expression allowed [12, 50, 51]. However with regard to our

                                                   13
computational results for all the problem instances considered below this never occurred within
the time limit imposed.
    Note here that even if solving P or P ∗ returns a feasible solution we have no guarantee that
this is an optimal solution, since a better solution might have been found had we increased the
time limit.
    The iterative process in the pseudocode is to update the iteration counter and solve the
continuous FSS relaxation P ∗ . If a feasible solution for P ∗ has been found then we round
that solution and solve the resulting feasibility problem (again subject to the predefined time
limit). The best feasible solution found (if any) is updated and provided we have not reached
the termination condition we reduce δ by a factor γ and repeat.
    We terminate when δ is small (≤ 10−5 ) or we have performed a number of consecutive
iterations (three iterations) without improving the value of the best solution found. We reduce
δ by a factor γ = 0.5 at each iteration and replicate (repeat) our heuristic a number of times
(five replications were performed in the computational results reported below). The values for
these factors were set based on our previous computational experience with FSS.

Algorithm 1 Formulation space search pseudocode

  Initialisation: δ ← 0.05 Zbest ← −∞ t ← 0
  Solve P and update Zbest if a feasible solution for P has been found
  Iterative process:
  while not termination condition do
     Update the iteration counter t ← t + 1
     Solve P ∗
     if a feasible solution for P ∗ has been found then
        Round the [αi , i = 1, . . . , n] values in the P ∗ solution and solve the resulting feasibility
        problem
        Update Zbest using the solution to the feasibility problem if a feasible solution for that
        problem has been found
     end if
     If δ ≤ 10−5 or Zbest has not improved in the last three iterations stop
     Update δ ← γδ
  end while


4.2   Constraints
There are a number of general constraints that apply whatever the objective adopted. Recall
that Zbest is the value of the best feasible solution encountered during our FSS heuristic. Let
the set of rectangles that are packed in this best feasible solution be denoted by F . Then the




                                                  14
general constraints that apply are:

          αi + αj ≤ 1                         ∀(i, j) ∈ Q min(Li + Lj , Wi + Wj ) > 2R        (18)
          Xn
              αi Li Wi ≤ πR2                                                                  (19)
           i=1
           Xn
                  αi Vi ≥ Zbest                                                               (20)
           i=1
           X             X
                  αi +    (1 − αi ) ≥ 1                                                       (21)
           i6∈F          i∈F

    Equation (18) says that if the minimum of the sum of the sides of any two rectangles is greater
than the container diameter then we cannot pack both rectangles. Equation (19) ensures that
the total area of the rectangles packed cannot exceed the area of the container. Equation (20)
ensures that the value of any solution found is at least that of the best feasible solution known.
Equation (21) is a feasible solution exclusion constraint and ensures that whatever solution is
found must differ from the best known solution (of value Zbest with packed rectangles F ) by
at least one rectangle. The effect of Equations (20) and (21) is to seek an improved feasible
solution.
    Note here that although these constraints may be redundant in the original MINLP they
may not be redundant in any relaxation of the problem, in particular here the continuous FSS
relaxation when we drop the requirement that the [αi , i = 1, . . . , n] are zero-one.

4.3    Summary
We have presented a considerable number of constraints above and so here (for clarity) we specify
the constraints that are involved with P (the original MINLP) and P ∗ (the continuous FSS
relaxation) that are used in the statement of our FSS heuristic given above (see Algorithm 1).

    • P is optimise Equation (1) subject to Equations (2)-(7),(9)-(11),(18)-(21)

    • P ∗ is optimise Equation (1) subject to Equations (2)-(7),(10),(11),(16)-(21)

    When considering just the packing of squares, so as to maximise the number of squares
packed, we add Equations (13),(14) to P and P ∗ and replace Equation (11) by Equation (15).
When rectangles can be rotated through ninety degrees we amend the problem in the manner
discussed above when we considered Equation (12).


5     Results
The computational results presented below (Windows 2.50GHz pc, Intel i5-2400S processor, 6Gb
memory) are for our formulation space search heuristic as coded in FORTRAN. We used SCIP
(Solving Constraint Integer Programs, version 4.0.1) [1, 40, 48] as the mixed-integer nonlinear
solver. For a technical explanation as to how SCIP solves MINLPs see Vigerske and Gleixner [51].
To input our formulation into SCIP we made use of the modelling language ZIMPL (Zuse
Institute Mathematical Programming Language), and to solve continuous nonlinear problems


                                                15
we used Ipopt (Interior Point OPTimizer, version 3.12.8), both of which are included within
SCIP.
    We generated a number of test problems involving n = 10, 20, 30 rectangles/squares, with
rectangle/square dimensions being randomly generated (to two decimal places) from [1, 5]. For
each test problem we considered three different container radii, where the container radii R
                                                  2                     1 1    2
      Pnso that the area of the container (πR ) was approximately 3 , 2 and 3 of the total
were set
area ( i=1 Li Wi ) of the n rectangles/squares. All of the randomly generated test problems
considered in this paper are publicly available from OR-Library [4], see
http://people.brunel.ac.uk/∼mastjjb/jeb/orlib/rspackinfo.html.

5.1   Rectangle packing, no rotation
Table 2 shows the results obtained for the rectangle packing test problems considered (where
the rectangles have fixed orientation, so no rotation is allowed). In that table we show the value
of n and the value of the container area fraction. For the two objectives considered (maximise
the number of rectangles packed, maximise the total area of the rectangles packed) we give the
value of the best solution achieved. We also show the replication at which we first encountered
the best solution shown, as well as the total time (in seconds) over all five replications.
    In Table 2 for a fixed n (and so a fixed set of rectangles to be packed) we can see that, as we
would expect, as the container area fraction increases (so the container is of larger radius and
we can hence pack more of the rectangles) the solution value also increases.
    As an illustration of the results obtained Figure 5 and Figure 6 show the solutions in Table 2
for the two problems in that table with n = 30 and the largest container area fraction.
    In Figure 5 we can see that the solution consists of rectangles 1-18, together with rectangle
23. Recalling that rectangles are ordered in increasing size (area) order this packing is as we
would expect, in that many of the smaller rectangles are used in a solution that aims to maximise
the number of rectangles packed.
    In Figure 6 we can see that the solution consists of a mix of rectangles. The first six smallest
rectangles, rectangles 1-6, together with rectangles 8,11-13,17,19,22-24,28. This figure contains
16 rectangles in total, compared with the 19 rectangles used in Figure 5.

5.2   Square packing
Table 3 shows the results obtained for the square packing test problems considered. This table
has the same format as Table 2. As an illustration of the results obtained Figure 7 and Figure 8
show the solutions in Table 3 for the two problems in that table with n = 30 and the largest
container area fraction.
    For Figure 7, since we are maximising the number of squares packed, the solution must
consist of the first K squares, for some K (the squares being ordered in increasing size order).
In Figure 7 we can see that all squares up to and including square K = 23 are packed. Visually
whether square 24, which must be at least as large as square 23 (and possibly larger), can also
be packed into the circular container through judicious rearrangement of all of the currently
positioned squares is unclear.
    In Figure 8 we can see that the packing consists of a mix of squares. Squares 1-19, which
are the 19 smallest squares, are all packed along with the two of the larger squares, squares 22
and 28. This figure contains 21 squares in total, compared with the 23 squares used in Figure 7.


                                                16
      Number      Container               Maximise number                         Maximise area
        of          area        Best        Replication      Total      Best       Replication     Total
 rectangles (n)    fraction    solution                     time (s)   solution                   time (s)
                      1
        10            3
                                  5              2           3058      18.4441          1          3292
                      1
                      2
                                  6              1           2862      28.9390          1          2992
                      2
                      3
                                  7              1           2966      37.6878          2          4754
                      1
        20            3
                                  7              1           6278      43.3885          1          7227
                      1
                      2
                                 10              5           4530      63.1643          1          9791
                      2
                      3
                                 11              1           7311      84.4446          2          10601
                      1
        30            3
                                 13              5           11514     60.3570          4          14011
                      1
                      2
                                 16              5           10029     85.2113          5          19786
                      2
                      3
                                 19              5           6966      103.4802         5          19470

                  Table 2: Computational results: rectangle packing, no rotation

      Number      Container               Maximise number                         Maximise area
        of          area        Best        Replication      Total      Best       Replication     Total
 rectangles (n)    fraction    solution                     time (s)   solution                   time (s)
                      1
        10            3
                                  4              1           1123      22.9485          1          2762
                      1
                      2
                                  5              1           2761      36.7126          1          3402
                      2
                      3
                                  6              1           2275      51.7583          3          4593
                      1
        20            3
                                 11              5           5450      54.1054          5          9412
                      1
                      2
                                 12              1           6465      85.2107          4          11304
                      2
                      3
                                 14              1           6995      109.8363         5          7636
                      1
        30            3
                                 16              2           13552     54.4941          5          16629
                      1
                      2
                                 20              2           13457     77.5814          4          14808
                      2
                      3
                                 23              5           10427     103.0963         5          15145

                           Table 3: Computational results: square packing


5.3     Rectangle packing, rotation allowed
Table 4 shows the results obtained for the rectangle packing test problems considered in Table 2,
but where rotation through ninety degrees is allowed. That table has the same format as Table 2.
    As an illustration of the results obtained Figure 9 and Figure 10 show the solutions in Table 2
for the two problems in that table with 30 rectangles and the largest container area fraction.
In those figures the letter r after the rectangle number indicates that the rectangle has been
rotated through ninety degrees.
    Comparing Table 4 with Table 2 we can see that the solution value where rotation is allowed
is greater than (or equal to) the solution value with no rotation for all but two of the 18 test
problems considered.


                                                     17
    In the discussion above as to how to extend our formulation to deal with rotation through
ninety degrees we noted the increase in the consequent size of the formulation, both with respect
to the number of linear and nonlinear constraints and with respect to the number of variables.
Comparing the computation times in Table 4 with those in Table 2 does indeed indicate that
dealing with a problem where rectangles can be rotated is much more challenging computation-
ally than dealing with a problem where the rectangles have fixed orientation.

  Number      Container              Maximise number                         Maximise area
      of        area       Best        Replication        Total    Best       Replication     Total
 rectangles   fraction    solution                     time (s)   solution                   time (s)
                  1
      10          3
                             5             1              9836    19.6702          1          8771
                  1
                  2
                             6             1              10332   29.5041          1          16093
                  2
                  3
                             7             1              12409   37.9687          2          15526
                  1
      20          3
                             8             3              22759   43.6850          2          50558
                  1
                  2
                            10             1              30682   63.5279          1          50013
                  2
                  3
                            12             4              30823   84.7008          3          63350
                  1
      30          3
                            14             1              49724   57.9328          5          69565
                  1
                  2
                            17             1              45857   84.3715          1          82101
                  2
                  3
                            20             1              57427   110.3253         3          39564

              Table 4: Computational results: rectangle packing, rotation allowed


5.4    Comment
As with many heuristic algorithms presented in the literature it is difficult to draw firm conclu-
sions as to the quality of the results obtained without knowing either the optimal solutions of
the test problems solved, or the results obtained by other heuristic algorithms by other authors
on the same set of test problems.
    For the problem considered in this paper we are not aware of any appropriate publicly
available test problems which could be used to provide direct insight into the quality of our
heuristic. We would stress here however that all of the test problems used in this paper are
publicly available for use by future workers to see if they can develop approaches that perform
better than the formulation space heuristic presented in this paper.
    Despite this lack of appropriate test problems it is possible to gain some insight into the
quality of our heuristic by taking test problems associated with a slightly different (but similar)
problem. This problem is the problem of packing n unit squares within a circle of small (ideally
minimal) radius. Here, unlike the problem we consider, all squares must be packed (whereas
our heuristic is particularised for the case where one or more squares need not be packed).
    We used our heuristic to maximise the number of unit squares packed into a circular container
of known radius utilising the test problems given by Friedman [20]. For these problems [20] gives
the best solution known for the minimum radius circle within which it is possible to pack all n
unit squares. Some of these best known solutions involve arbitrary rotation (which our heuristic
cannot deal with) and so we only considered problems which did not involve rotation. Note


                                                     18
also here that, as far as we aware, the results given in [20] were found by varying authors using
varying approaches (including, we believe, results based on human intervention). This contrasts
with our results produced by a single algorithmic heuristic approach that does not involve any
human intervention.
    The results are shown in Table 5. In that table we show the number of unit squares (n) and
the value of best solution (maximum number of unit squares packed) as found by our heuristic.
We also show the replication at which we first encountered the best solution shown, as well as
the total time (in seconds) over all five replications. Considering Table 5 we can see that for
13 of the 16 problems considered our heuristic succeeds in finding the best known solution by
packing all n unit squares into the given circular container.

         Number of                Best solution              Replication   Total time (s)
       unit squares (n)   (number of unit squares packed)
               1                         1                        1               0.0
               2                         2                        1               0.2
               3                         3                        1               0.3
               4                         4                        1               0.7
               5                         5                        1               3.6
               7                         7                        1             140.2
               9                         9                        1              49.2
              10                        10                        1             158.5
              11                        10                        1             2619.5
              12                        12                        1             120.2
              14                        14                        1             460.6
              16                        16                        5             4800.7
              18                        18                        2             3153.6
              21                        21                        5             4961.4
              26                        23                        1             8756.0
              30                        27                        1            18984.5

                     Table 5: Computational results: unit square packing



6    Conclusions and future work
In this paper we have formulated the problem of packing unequal rectangles/squares into a
fixed size circular container as a mixed-integer nonlinear program. We showed how we can
eliminate a nonlinear maximisation term that arises in one of the constraints in our formulation
and indicated the amendments that can be made to the formulation when considering packing
squares so as to maximise the number of squares packed.
    We discussed how to amend our formulation to deal with the case where unequal rectangles
can be rotated through ninety degrees. A formulation space search heuristic was presented and
computational results given for test problems involving up to 30 rectangles/squares, with these
test problems being made publicly available for future workers.
    In terms of future work we plan to investigate changes to our formulation, for example by
making use of McCormick cuts to replace products of variables.


                                               19
                                                                       23
                                     8                  18

                                     16                                 10

                                     14                      13                      5

                                                                                     9
                            1
                                     17                      11    2        3            15
                                                   7
                                                                                 6
                                                   12              4



 Figure 5: Maximising number of rectangles packed, no rotation, n = 30, container area fraction 32




                                                   8                    4

                                                                                 12
                                         24
                                                                  11
                                                                        1
                                                                                          28
                                22            5         17

                                              6                    2
                                                                                     13


                                                  23          3             19




Figure 6: Maximising total area of rectangles packed, no rotation, n = 30, container area fraction 32




                                                             20
                                                               15     1

                                            23                                 10
                                                                22
                          12                                                        16
                                       13         2
                                                                4
                     11         3                                         20
                                                 21             5                        17
                               9

                                                                          19
                               14            8             18

                                                                      6
                                                       7

 Figure 7: Maximising number of squares packed, n = 30, container area fraction 23




                                   1                       3
                                            11
                                                                     17
                               8                           7                    10
                                             4
                       5                               2
                                                                          19
                      12        16                6
                                                                                          9

                       14           13                18
                                                                      28


                                             22
                                                                15


Figure 8: Maximising total area of squares packed, n = 30, container area fraction 23




                                                           21
                                                                    8
                                                  9
                                         10                     3          13

                                         2r                                12

                             18                     17                          14
                                          11                   20
                                                                               19

                                7r
                                                  16                6
                                                                               15

                                                  4r                1r
                                                          5r


 Figure 9: Maximising number of rectangles packed, rotation allowed, container area fraction 23




                                                           5
                                              7                     1      4
                                                          2                9
                                     8
                                                   18                     10

                                         6r                         14
                           15
                                                                    17r              19r
                                               12
                             3r               13
                                                                    25r
                                              16

                                                         11r

Figure 10: Maximising total area of rectangles packed, rotation allowed, container area fraction 23




                                                          22
Acknowledgments
The first author has a grant support from the programme UNAM-DGAPA-PAPIIT-IA106916


References
 [1] Achterberg T. SCIP: Solving constraint integer programs. Mathematical Programming
     Computation 2009;1(1):1–41.
 [2] Amirgaliyeva Z, Mladenović N, Todosijević R, Urosević D. Solving the maximum min-
     sum dispersion by alternating formulations of two different problems. European Journal of
     Operational Research 2017;260(2):444–459.
 [3] Andrade R, Birgin EG. Symmetry-breaking constraints for packing identical rectangles
     within polyhedra. Optimization Letters 2013;7(2):375–405.
 [4] Beasley JE. OR-Library: distributing test problems by electronic mail. Journal of the Op-
     erational Research Society 1990;41(11):1069–1072.
 [5] Birgin EG. Applications of nonlinear programming to packing problems. In Anderssen RS,
     Broadbridge P, Fukumoto Y, Kajiwara K, Takagi T, Verbitskiy E, Wakayama M (eds).
     Applications + Practical Conceptualization + Mathematics = fruitful Innovation. Mathe-
     matics for Industry, vol 11. Springer, Tokyo, pp 31–39 (2016).
 [6] Birgin EG, Lobato RD. Orthogonal packing of identical rectangles within isotropic convex
     regions. Computers & Industrial Engineering 2010;59(4):595–602.
 [7] Birgin EG, Lobato RD, Morabito R. An effective recursive partitioning approach for the
     packing of identical rectangles in a rectangle. Journal of the Operational Research Society
     2010;61(2):306–320.
 [8] Birgin EG, Martı́nez JM, Mascarenhas WF, Ronconi DP. Method of sentinels for pack-
     ing items within arbitrary convex regions. Journal of the Operational Research Society
     2006;57(6):735–756.
 [9] Birgin EG, Martı́nez JM, Nishihara FH, Ronconi DP. Orthogonal packing of rectangular
     items within arbitrary convex regions by nonlinear optimization. Computers & Operations
     Research 2006;33(12):3535–3548.
[10] Bortfeldt A. A reduction approach for solving the rectangle packing area minimization
     problem. European Journal of Operational Research 2013;224(3):486–496.
[11] Brimberg J, Drezner Z, Mladenović N, Salhi S. A new local search for continuous location
     problems. European Journal of Operational Research 2014;232(2):256–265.
[12] Bussieck MR, Vigerske S. MINLP solver software. In J.J. Cochran, L.A. Cox Jr., P. Ke-
     skinocak, J.P. Kharoufeh and J.C. Smith (editors), Wiley Encyclopaedia of Operations
     Research and Management Science, Wiley, New York, 2011. Updated version available
     from http://www2.mathematik.hu-berlin.de/∼stefan/minlpsoft.pdf Last accessed February
     15 2018.
[13] Butenko S, Yezerska O, Balasundaram B. Variable objective search. Journal of Heuristics
     2013;19(4):697–709.
[14] Caprara A, Lodi A, Martello S, Monaci M. Packing into the smallest square: worst-case
     analysis of lower bounds. Discrete Optimization 2006;3(4):317–326.
[15] Cassioli A, Locatelli M. A heuristic approach for packing identical rectangles in convex
     regions. Computers & Operations Research 2011;38(9):1342–1350.
[16] Christofides N. Optimal cutting of two-dimensional rectangular plates. In CAD 74, Pro-
     ceedings of the International Conference on Computers in Engineering and Building Design,
     25-27 September 1974, Imperial College, London, UK 1974;1–10.
[17] Delorme M, Iori M, Martello S. Logic based Benders’ decomposition for orthogonal stock
     cutting problems. Computers & Operations Research 2017;78:290–298.
[18] Dowsland KA, Dowsland WB. Packing problems. European Journal of Operational Re-
     search 1992;56(1):2–14.
[19] Duarte A, Pantrigo JJ, Pardo EG, Sánchez-Oro J. Parallel variable neighbourhood search
     strategies for the cutwidth minimization problem. IMA Journal of Management Mathemat-
     ics 2016;27(1):55–73.
[20] Friedman E. Squares in circles. http://www2.stetson.edu/∼efriedma/squincir/ Last ac-
     cessed February 15 2018.
[21] Hansen P, Mladenović N, Brimberg J, Perez JAM. Variable neighborhood search, in Gen-
     dreau M. and Potvin J.-Y. (eds), Handbook of Metaheuristics, Springer. International Series
     in Operations Research & Management Science 2010;146:61–86.
[22] Hansen P, Mladenović N, Todosijević T, Hanafi S. Variable neighborhood search: basics
     and variants. EURO Journal on Computational Optimization 2017;5(3):423–454.
[23] Hertz A, Plumettaz M, Zufferey N. Variable space search for graph coloring. Discrete Ap-
     plied Mathematics 2008;156(13):2551–2560.
[24] Hertz A, Plumettaz M, Zufferey N. Corrigendum to “Variable space search for graph
     coloring” [Discrete Appl. Math. 156 (2008) 2551-2560]. Discrete Applied Mathematics
     2009;157(7):1335–1336.
[25] Hinostroza I, Pradenas L, Parada V. Board cutting from logs: optimal and heuristic ap-
     proaches for the problem of packing rectangles in a circle. International Journal of Produc-
     tion Economics 2013;145(2):541–546.
[26] Huang E, Korf KE. Optimal rectangle packing: an absolute placement approach. Journal
     of Artificial Intelligence Research 2012;46:47–87.
[27] Huang WQ, Chen DB, Xu RC. A new heuristic algorithm for rectangle packing. Computers
     & Operations Research 2007;34(11):3270–3280.
[28] Kochetov Y, Kononova P, Paschenko M. Formulation space search approach for the
     teacher/class timetabling problem. Yugoslav Journal of Operations Research 2008;18(1):1–
     11.
[29] Korf KE, Moffitt MD, Pollack ME. Optimal rectangle packing. Annals of Operations Re-
     search 2010;179:261–295.
[30] Leung JYT, Tam TW, Wong CS, Young GH, Chin FYL. Packing squares into a square.
     Journal of Parallel and Distributed Computing 1990;10(3):271–275.
[31] Li K, Cheng KH. Complexity of resource allocation and job scheduling problems in par-
     titionable mesh connected systems. Proceedings of the First Annual IEEE Symposium of
     Parallel and Distributed Processing. IEEE Computer Society, Silver Spring, MD, 1989, pp.
     358—365.
[32] Li ZQ, Wang XF, Tan JY, Wang YS. A quasiphysical and dynamic adjustment approach
     for packing the orthogonal unequal rectangles in a circle with a mass balance: satellite
     payload packing. Mathematical Problems in Engineering Volume 2014 (2014), Article ID
     657170.
[33] Liu DQ, Teng HF. An improved BL-algorithm for genetic algorithm of the orthogonal
     packing of rectangles. European Journal of Operational Research 1999;112(2):413–420.
[34] Lodi A, Martello S, Monaci M. Two-dimensional packing problems: A survey. European
     Journal of Operational Research 2002;141(2):241–252.
[35] López CO, Beasley JE. A heuristic for the circle packing problem with a variety of contain-
     ers. European Journal of Operational Research 2011;214(3):512–525.
[36] López CO, Beasley JE. Packing unequal circles using formulation space search. Computers
     & Operations Research 2013;40(5):1276–1288.
[37] López CO, Beasley JE. A note on solving MINLP’s using formulation space search. Opti-
     mization Letters 2014;8(3):1167–1182.
[38] López CO, Beasley JE. A formulation space search heuristic for packing unequal circles in a
     fixed size circular container. European Journal of Operational Research 2016;251(1):65–73.
[39] Maag V, Berger M, Winterfeld A, Kufer KH. A novel non-linear approach to minimal area
     rectangular packing. Annals of Operations Research 2010;179(1):243–260.
[40] Maher SJ, Fischer T, Gally T, Gamrath G, Gleixner A, Gottwald RL, Hendel G, Koch T,
     Lübbecke ME, Miltenberger M, Müller B, Pfetsch ME, Puchert C, Rehfeldt D, Schenker S,
     Schwarz R, Serrano F, Shinano Y, Weninger D, Witt JT, Witzig J. The SCIP Optimization
     Suite 4.0. ZIB Report 17-12 (March 2017, Revised September 2017). Available from
     https://opus4.kobv.de/opus4-zib/files/6217/scipoptsuite-401.pdf Last accessed February
     15 2018.
[41] Martello S, Monaci M. Models and algorithms for packing rectangles into the smallest
     square. Computers & Operations Research 2015;63:161–171.
[42] Mladenović N, Plastria F, Urošević D. Reformulation descent applied to circle packing
     problems. Computers & Operations Research 2005;32(9):2419–2434.
[43] Mladenović N, Plastria F, Urošević D. Formulation space search for circle packing problems.
     In “Engineering Stochastic Local Search Algorithms. Designing, Implementing and Analyz-
     ing Effective Heuristics”, Proceedings of the International Workshop, SLS 2007, Brussels,
     Belgium, September 6-8, 2007. Lecture Notes in Computer Science volume 4638, 2007,
     pages 212–216.
[44] Murata H, Fujiyoshi K, Nakatake S, Kajitani Y. VLSI module placement based on rectangle-
     packing by the sequence-pair. IEEE Transactions on Computer-Aided Design of Integrated
     Circuits and Systems 1996;15(12):1518–1524.
[45] Pardo EG, Mladenović N, Pantrigo JJ, Duarte A. Variable formulation search for the
     cutwidth minimization problem. Applied Soft Computing 2013;13(5):2242–2252.
[46] Pedroso JP, Cunha S, Tavares JN. Recursive circle packing problems. International Trans-
     actions in Operational Research 2016;23(1-2):355–368.
[47] Picouleau C. Worst-case analysis of fast heuristics for packing squares into a square. The-
     oretical Computer Science 1996;164(1-2):59–72.
[48] SCIP: Solving constraint integer programs. Available from http://scip.zib.de/ Last accessed
     February 15 2018.
[49] Sweeney PE, Paternoster ER. Cutting and packing problems:                      a categorized,
     application-orientated research bibliography. Journal of the Operational Research Society
     1992;43(7):691–706.
[50] Vigerske S. Private communication, April 2017.
[51] Vigerske S, Gleixner A. SCIP: Global optimization of mixed-integer nonlinear programs in
     a branch-and-cut framework. ZIB Report 16-24 (May 2016). Available from
     https://opus4.kobv.de/opus4-zib/frontdoor/index/index/docId/5937 Last accessed Febru-
     ary 15 2018.
[52] Wascher G, Haußner H, Schumann H. An improved typology of cutting and packing prob-
     lems. European Journal of Operational Research 2002;183(3):1109–1130.
[53] Wu YL, Huang WQ, Lau SC, Wong CK, Young GH. An effective quasi-human based heuris-
     tic for solving the rectangle packing problem. European Journal of Operational Research
     2007;141(2):341–358.
