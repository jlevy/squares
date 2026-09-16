Accepted Manuscript


PACKING OF CONCAVE POLYHEDRA WITH CONTINUOUS
ROTATIONS USING NONLINEAR OPTIMISATION

T. Romanova , J. Bennell , Y. Stoyan , A. Pankratov

PII:                   S0377-2217(18)30046-8
DOI:                   10.1016/j.ejor.2018.01.025
Reference:             EOR 14926


To appear in:          European Journal of Operational Research

Received date:         14 December 2016
Revised date:          31 December 2017
Accepted date:         11 January 2018

Please cite this article as: T. Romanova , J. Bennell , Y. Stoyan , A. Pankratov , PACKING OF CON-
CAVE POLYHEDRA WITH CONTINUOUS ROTATIONS USING NONLINEAR OPTIMISATION, Euro-
pean Journal of Operational Research (2018), doi: 10.1016/j.ejor.2018.01.025




This is a PDF file of an unedited manuscript that has been accepted for publication. As a service
to our customers we are providing this early version of the manuscript. The manuscript will undergo
copyediting, typesetting, and review of the resulting proof before it is published in its final form. Please
note that during the production process errors may be discovered which could affect the content, and
all legal disclaimers that apply to the journal pertain.
                     ACCEPTED MANUSCRIPT

 Highlights

     Tools to describe non-overlapping and distance constraints for
        concave polyhedra.
     NLP-model of the packing problem of concave polyhedra with
        continuous rotations.
     A compaction algorithm to search for local extrema of the
        polyhedron packing problem.




                                               T
                                             IP
                                           CR
                                  US
                                AN
                          M
                ED
          PT
 CE
AC
                                    ACCEPTED MANUSCRIPT
                                                                                                        2


            PACKING OF CONCAVE POLYHEDRA WITH CONTINUOUS ROTATIONS
                                  USING NONLINEAR OPTIMISATION


                              T. Romanovaa*, J. Bennellb ,Y. Stoyana, A. Pankratova
a
    Department of Mathematical Modeling and Optimal Design, Institute for Mechanical Engineering
Problems of the National Academy of Sciences of Ukraine, Pozharsky Str., 2/10, Kharkov, 61046,
Ukraine
b




                                                                          T
    Southampton Business School, University of Southampton, Highfield, Southampton SO17 1BJ, UK




                                                                        IP
          Abstract. We study the problem of packing a given collection of arbitrary, in general




                                                                      CR
concave, polyhedra into a cuboid of minimal volume. Continuous rotations and translations of
polyhedra are allowed. In addition, minimal allowable distances between polyhedra are taken into
account. We derive an exact mathematical model using adjusted radical free quasi phi-functions for

                                                   US
concave polyhedra to describe non-overlapping and distance constraints. The model is a nonlinear
programming formulation. We develop an efficient solution algorithm, which employs a fast starting
                                                 AN
point algorithm and a new compaction procedure. The procedure reduces our problem to a sequence
of nonlinear programming subproblems of considerably smaller dimension and a smaller number of
nonlinear inequalities. The benefit of this approach is borne out by the computational results, which
                                          M


include a comparison with previously published instances and new instances.
          Keywords: packing; concave polyhedra; continuous rotations; mathematical modeling;
                             ED




nonlinear optimisation


1. Introduction
                    PT




          Cutting and packing problems have a long history of being tackled by the Operational
Research community. Where the objects have arbitrary shape, this research has a strong link with the
           CE




field of computational geometry (see, e.g., [24], [1], [9]). These problems have a wide spectrum of
applications, for example in modern biology, mineralogy, medicine, materials science,
AC




nanotechnology, robotics, pattern recognition systems, control systems, space apparatus control
systems, as well as in the chemical industry, power engineering, mechanical engineering,
shipbuilding, aircraft construction and civil engineering.
          At present, the interest in finding effective solutions for packing problems is growing rapidly.
This is due to a large number of applications and the development of new and sophisticated methods
that can exploit the ever increasing speed of computer processing.
          In this paper, we consider the practical problem of packing a collection of non-identical, and
in general, concave polyhedra into a cuboid of minimal sizes (in particular volume). We will refer to
the problem as the polyhedron packing problem.
                                  ACCEPTED MANUSCRIPT
                                                                                                      3
         An interesting example of applications of the polyhedron packing arises in engineering
design. Optimal packing of electronic components and payload has always been a pivotal concern in
vehicle engineering, in particular in applications where volume is at a premium, for example
embedding avionics in aircraft. The aim is to design an external envelope and determine the
configuration of the payload subject to a fixed volume constraint. Alternatively, the approach may be
to design an envelope around a fixed packing of the payload and the avionics in order to minimize
volume while satisfying a set of mechanical, technical and maneuverability constraints.
         Another application arises in the recent advent of additive manufacturing (AM), often referred
to as 3D printing. There are a variety of different AM technologies that build up objects by adding one




                                                                        T
very thin layer of material at a time, for example through material extrusion or sintering layers of




                                                                      IP
powder material. This procedure is very slow and not appropriate for repetitive manufacturing but
useful for individual items and prototyping. Combining objects into one compact print pattern can




                                                                    CR
reduce the print time, improving capacity utilization, and reduce the need for extra supporting
material that is often required as part of the printing process when objects are arranged in certain
configurations.

                                                 US
         The polyhedron problems are NP-hard [2] and, as a result, solution methodologies generally
employ heuristics, for example see [3], [8], [11], [12], [15], [20], [21]. Some researchers develop
                                               AN
approaches based on mathematical modeling and general optimisation procedures; for example see
[5], [6], [22].
                                        M


         Egeblad et al [5] present an efficient solution method for packing polyhedra within the
bounds of a container (a polyhedron). The central geometric operation of the method is an exact
horizontal or vertical translation of a given polyhedron to a position, which minimizes its volume of
                            ED




overlap with all other polyhedra. The translation algorithm is embedded into a local search heuristic.
Additional details are given for the three-dimensional case and appropriate results are reported for the
                   PT




problem of packing polyhedra into a rectangular parallelepiped. Utilization of container space is
improved by an average of more than 14 percentage points compared to previous methods proposed in
[18]. In the experiments the largest total volume of overlap allowed in a solution corresponds to
         CE




0.01% of the total volume of all polyhedra for the given problem.
         Liu et al [13] propose a new constructive algorithm, called HAPE3D, which is a heuristic
AC




algorithm based on the principle of minimum total “potential energy” for the 3D irregular packing
problem, involving packing a set of irregularly shaped polyhedrons into a box-shaped container with
fixed width and length but unconstrained height. The objective is to allocate all the polyhedrons in the
container, and thus minimize the waste or maximize profit. HAPE3D can deal with arbitrarily shaped
polyhedrons, which can be rotated around each coordinate axis at different angles. The most
outstanding merit is that HAPE3D does not need to calculate no-fit polyhedrons. HAPE3D can also
be hybridized with a meta-heuristic algorithm such as simulated annealing. Two groups of
computational experiments demonstrate the good performance of HAPE3D and prove that it can be
hybridized with a meta-heuristic algorithm that further improves the packing quality.
                                    ACCEPTED MANUSCRIPT
                                                                                                         4
           Our approach is based on the mathematical modeling of relations between geometric objects
and allowing the packing problem to be formulated as a nonlinear programming problem. To this end
we use the phi-function technique (see, [4]) to provide an analytic description of objects placed in a
container taking into account their continuous rotations and translations. At present phi-functions for
the simplest 3D-objects, such as parallelepipeds, convex polyhedra and spheres are considered in [16].
Phi-functions for 3D-objects, in particular polyhedra, can be highly complicated analytically, since
they involve many radicals and maximum operators, and are therefore difficult for NLP-solvers to
solve.
           In this paper we apply the quasi phi-functions concept introduced in [19], which is based on




                                                                          T
the idea proposed by [10] to use a separating plane to model non-overlapping constraints for circles




                                                                        IP
and convex polygons. The concept of quasi phi-functions extends the domain of phi-functions by
including auxiliary variables. The new functions can be described by analytical formulas that are




                                                                      CR
substantially simpler than those used for phi-functions, for some types of objects, in particular, for
convex polyhedra.
           The use of quasi phi-functions, instead of phi-functions, allows us to describe (or simplify)

                                                   US
the non-overlapping constraints. While this makes our models easier to solve, this comes at a price,
which is performing the optimisation over a larger set of parameters, including the extra (auxiliary)
                                                 AN
variables used by the quasi phi-functions. Our approach is capable of finding a good local optimal
solution in reasonable computational time.
           The phi- and quasi phi-functions have been widely and successfully used to model a variety
                                          M


of packing problems, as in ([4], [14], [17]-[19]). In the current manuscript, we consider packing
problem of concave polyhedra. The contributions of the work presented in this manuscript are as
                              ED




follows.
                  We construct radical free quasi phi-functions to describe analytically the non-
overlapping constraints for concave polyhedra and adjusted quasi phi-functions to describe
                     PT




analytically the minimal allowable distances between concave polyhedra.
                  We derive an exact mathematical model of the optimal packing problem of concave
           CE




polyhedra as a continuous nonlinear programming problem. Our feasible region is described by a
system of inequalities with infinitely differentiable functions.
AC




                  We develop an efficient solution algorithm, which employs a clear and simple
starting point algorithm and a new and original optimisation procedure (called COMPOLY) for the
compaction of concave polyhedra. The COMPOLY procedure reduces our problem to a sequence of
NLP subproblems of considerably smaller dimension and a smaller number of nonlinear inequalities.
The procedure allows us to search for local optimal solutions of the packing problem.
                  Our approach allows us to apply state of the art NLP solvers to the optimal packing
problem of concave polyhedra.
           The paper is organized as follows: in Section 2 we formulate the polyhedron packing
problem. In Section 3 we give definitions of a phi-function and a quasi phi-function, an adjusted phi-
                                     ACCEPTED MANUSCRIPT
                                                                                                                      5
function and an adjusted quasi phi-function and derive related functions for an analytical description
of non-overlapping, containment and distance constraints in the problem. In Section 4 we provide an
exact mathematical model in the form of a nonlinear programming problem by means of the phi-
function technique. In Section 5 we describe a solution algorithm, which involves a fast starting point
and efficient local optimisation procedures. In Section 6 we present our computational results for
some new instances and several instances studied before. Finally, Section 7 concludes this paper with
a brief summary and a discussion about our future research directions.


2. Problem formulation




                                                                                 T
         We consider here the packing problem in the following setting. Let  denote a cuboid,




                                                                               IP
  {( x, y, z)  R 3 : 0  x  l , 0  y  w, 0  z  h} . It should be noted that each of the three dimensions
( l or w or h ) can be variable. Let {1, 2, ..., N }  J N and a set of polyhedra           , q  J N be given.




                                                                             CR
         Each polyhedron         can be concave or convex. With each polyhedron                    we associate its
local coordinate system with origin denoted by v q .

         Assume that each concave polyhedron

                                        q
                                                       USis presented as a union of convex polyhedra K j ,
                                                                                                                  q
                                                     AN
j=1,…,nq. With each convex polyhedron K j we associate the local coordinate system of the

                                                 q                                                    q
polyhedron       . Each convex polyhedron K j is defined by its vertices p sqj , s  1, ...., m j , in the local
                                           M


coordinate system of       .
         We give here input data that form a concave polyhedron               by two lists:
                               ED




                                                                                                  q
                 List_1 contains the vertex coordinates of all the convex polyhedra K j , j=1,…,nq, and

                                                     q
                 List_2 contains the index sets J j , j=1,…,nq, of the numbers of vertices (with respect
                    PT




                                                                                q
                  to List_1) that define appropriate convex polyhedra K j , j=1,…,nq.

We note that List_1 involves all the original vertices of the concave polyhedron and, in general,
         CE




additional vertices that appear as a result of decomposing the concave polyhedron into convex
polyhedra. See Appendix A for details.
AC




                                                                    nq
         For the purposes of this paper, we assume that                    K qj is known.
                                                                    j 1

         Without loss of generality, we assume that the origin v q of a polyhedron                    coincides with

the center point of its circumscribed sphere S q of radius rq . In order to circumscribe a sphere around

a polyhedron we employ the algorithm described in [7], which computes the smallest enclosing sphere
of a collection of points. We use the library function found at (https://github.com/hbf/miniball), which
is sufficiently fast.
The location and orientation of each polyhedron            is defined by a vector u = (v, ) of its variable
                                        ACCEPTED MANUSCRIPT
                                                                                                               6

placement parameters. Here v = ( x, y, z ) is a translation vector, θ = ( 1,  2 , 3 ) is a vector of rotation

parameters, where 1,  2 ,  3 are Euler angles.

          A polyhedron rotated through angles 1,  2 ,  3 and translated by vector v is denoted as
  ( )      *                      ( )               +, where    =(     θ),       denotes the non-translated and

non-rotated polyhedron      , M ()  M (1,  2 , 3 ) is a rotation matrix of the form:

          cos 1 cos  3  sin 1 cos  2 sin  3  cos 1 sin  3  sin 1 cos  2 cos  3     sin 1 sin  2 
                                                                                                                
 M () =  sin 1 cos  3  cos 1 cos  2 sin  3  sin 1 sin  3  cos 1 cos  2 cos  3     cos 1 sin  2  .
                                                                                                                
                      sin  2 sin  3                          sin  2 cos  3                     cos  2      




                                                                                 T
                                                                                                                
It is possible to define minimal allowable distances between each pair of polyhedra               and




                                                                               IP
         , as well as, between a polyhedron       , q  I N , and the boundary of container  . It means that




                                                                             CR
each polyhedron        has to be located no closer                           than the given allowable distance
and each polyhedron         has to be located inside the container and no closer to the boundary of the
container than the given allowable distance.


K qj 
                                                      US
          We note that the minimal allowable distance between each pair of convex polyhedra
                                g
           q , j=1,…,nq, and K l       g , l=1,…,ng,               , is equal to the given allowable distance
                                                    AN
between the original polyhedra           and     . Moreover, the minimal allowable distance between each
                q
polyhedron K j , q  I N , and the boundary of the container  is equal to the given allowable distance
                                               M


between the original polyhedron          , q  I N , and the boundary of container  .
The polyhedron packing problem can be formulated in the form:
                              ED




          Pack the set of polyhedra           , q  J N , within a cuboid container  of minimal volume

F  l  w  h , taking into account the given minimal allowable distances.
                    PT




We note that it is possible that just one of the metrical characteristics of  can be variable.
In this definition, the term “pack” assumes polyhedra do not overlap and are fully enclosed in the
          CE




containing cuboid.


3 Mathematical modeling of placement constraints
AC




       In this section we describe our methodology for modeling the non-overlapping, containment and
minimal distance constraints. Here we introduce phi-functions and quasi phi-functions.


3.1 Placement constraints
Let us consider placement constraints that are met in the polyhedron packing problem:
         non-overlapping constraints – two polyhedra           q    and     g   do not have common interior

   points but may touch, i.e.
                            int    q    int    g   for each q, g  J N     with q  g ;
                                     ACCEPTED MANUSCRIPT
                                                                                                               7
        containment constraints – each polyhedron           has to be fully enclosed in the container, i.e.

                         q    int      q    *   for each q  J N ,  *  R 3 \ int  .
Distance constraints
         Let           denote the minimal allowable distance between two polyhedra                 and       and

        denote the minimal allowable distance between a polyhedron               and the object  * .
        distance constraints for "non-overlapping" – each polyhedron              has to be located no closer
                        than the given allowable distance          , i.e.
                        dist(      )         for each q, g  J N with q  g, where




                                                                                T
                                 dist(      )                    (    );
        distance constraints for "containment" – each polyhedron       has to be located inside the




                                                                              IP
   container no closer to the boundary of the container than the given allowable distance




                                                                            CR
                       dist(         )         for each q  J N ,  *  R 3 \ int  , where
                                     dist(       )                     (    ),
         d (a, b) represents the Euclidean distance between two points a, b  R 3 .

                                                     US
         In order to feasibly place two objects within a container, we need an analytical description of
the relationships between a pair of objects A and B considered in the placement constraints. We
                                                   AN
employ the phi-function technique for this [4], [19].


3.2 Phi-functions
                                              M


         Phi-functions allow us to distinguish the following three cases: A and B are intersecting so
that A and B have common interior points; A and B do not intersect, i. e. A and B do not have
                                ED




common points; A and B are in contact, i. e. A and B have only common frontier points.
Let A  R 3 and B  R 3 be two objects. Sizes of objects can change according to homothetic
coefficients (scaling parameters of objects)  A ,  B  0 . The position of object A is defined by a
                    PT




vector of placement parameters (v A ,  A ) , where: v A  ( x A , y A , z A ) is a translation vector and
         CE




 A  (1A ,  2A ,  3A ) is a vector of rotation angles. We denote the vector of variables for the object A
by u A  (v A ,  A ,  A ) and the vector of variables for the object B by u B  (v B ,  B ,  B ) . The object
AC




A, rotated by angles 1A ,  2A , 3A , translated by vector v A , and rescaled by homothetic coefficient
 A , will be denoted by A(u A ) .

Definition 1. A continuous and everywhere defined function  AB (u A , u B ) is called a phi-function
for objects A(u A ) and B(u B ) if

                                       AB  0, if A(u A )    B(u B )   ;

                  AB  0, if int A(u A ) int B (u B )   and frA(u A )        frB(u B )   ;

                                   AB  0, if int A(u A ) int B (u B )   ;
                                      ACCEPTED MANUSCRIPT
                                                                                                           8
provided that  A ,  B are fixed.
Here frA means the boundary (frontier) and intA means the interior of object A.
Figure 1 illustrates three situations that a phi-function distinguishes.


                                                                                      A
                 A            B                     A                                          B
                                                               B


                            (a)                           (b)                      (c)

Fig. 1 – Illustrations of definition 1: a)  AB  0 ; b)  AB  0 ; c)  AB  0.




                                                                               T
                                                                             IP
Thus, inequality  AB  0 represents the non-overlapping relationship int A(u A ) int B(u B )  ,

i.e.  AB  0  int A(u A ) int B(u B )  .




                                                                           CR
                                                                                                       *
We employ phi-functions for the description of the contaiment relation A  B as follows:  AB  0 ,

where B *  R 3 \ int B .
                                                      US
We emphasize that according to Definition 1, the phi-function  AB for a pair of objects A and B can
                                                    AN
be constructed by many different formulas [4], and we can choose the most convenient ones for our
optimisation algorithms.
                                             M


   We can take into account minimum allowable distance constraints by replacing the phi-functions
in the non-overlapping and containment constraints with adjusted phi-functions.
   Let   0 be a given minimal allowable distance between objects A(u A ) and B(u B ).
                                  ED




Definition 2. A continuous and everywhere defined function  AB (u A , u B ) is called an adjusted phi-
function for objects A(u A ) and B(u B ) , if
                     PT




                            AB  0, if dist( A, B)   ;  AB  0, if dist( A, B)   ;
         CE




                                           AB  0, if dist( A, B)   .

   We can describe the distance constraint for objects A(u A ) and B(u B ) in the form:  AB  0 
AC




dist(A,B)   . Figure 2 illustrates three situations that an adjusted phi-function distinguishes.
                                                                                               
                                                          
                                                                   B                     A
                A                                  A
                                                                                                   B
                                  B


                     (a)                                 (b)                                 (c)


Fig. 2 – Illustrations of Definition 2: a)  AB  0 ; b)  AB  0 ; c)  AB  0.
                                      ACCEPTED MANUSCRIPT
                                                                                                           9
           The literature only contains the construction of phi-functions for concave polyhedra without
rotation [17]. Constructing phi-functions for concave polyhedra with rotation is too complicated,
therefore in this research we apply the concept of quasi phi-functions.
3.3 Quasi phi-functions

 We introduce a function  AB (u A , u B , u ') that must be defined for all values of uA and uB. In
addition to the placement parameters of objects used with phi-functions, quasi phi-functions depend

on auxiliary variables u'. These extra variables u' take values in some domain U  R  . The number
and the nature of variables u' depend on the shapes of objects A(u A ) and B(u B ) , as well as on the
restrictions of a packing problem. We define  for a quasi phi-function of a pair of polyhedra later.




                                                                                T
                                                                              IP
Definition 3. A continuous and everywhere defined function  AB (u A , u B , u ') is called a quasi phi-

function for two objects A(u A ) and B(u B ) if max  AB (u A , u B , u ') is a phi-function for the




                                                                            CR
                                                          u 'U

objects.
 The main property of a quasi phi-function is:

                                                     US
            if  AB (u A , u B , u ')  0 for some u', then int A(u A ) int B(u B )   ,

 where  AB (u A , u B , u ') is a quasi phi-function for two objects A(u A ) and B(u B ) .
                                                    AN
   We note that the inverse proposition is not valid. It means that a quasi phi-function can take
negative values while objects do not overlap, in contrast to a phi-function.
                                             M


   Let   0 be a given minimal allowable distance between objects A(u A ) and B(u B ).

Definition 4. Function  ' AB (u A , u B , u ') is called an adjusted quasi phi-function for objects A(u A )
                               ED




and B(u B ) , if function max  ' AB (u A , u B , u ') is an adjusted phi-function for the objects.
                            u 'U
                     PT




   We can define the distance constraint for objects A(u A ) and B(u B ) in the form:   AB  0. The
inequality implies dist(A,B)   .
           CE




           In order to describe the non-overlapping constraints in our polyhedron packing problem, we
use quasi phi-functions, while for the containment constraints we use phi-functions. To formalise the
AC




distance constraints, we employ adjusted quasi phi-functions and adjusted phi-functions.


3.4 Construction of quasi phi-functions for non-overlapping and distance constraints

           To construct a quasi phi-function and an adjusted quasi phi-function of two concave
polyhedra we will use a quasi phi-function and an adjusted quasi phi-function for each pair of convex
polyhedra that together form the original concave polyhedra.
           First we consider a quasi phi-function for a pair of convex polyhedra.

           Let A(u A ) and B(u B ) be two convex polyhedra given by their vertices p sA , s  1, ...., m A ,
                                             ACCEPTED MANUSCRIPT
                                                                                                                                   10

and p sB , s  1, ...., m B .

A radical free quasi phi-function  AB (u A , u B , u  u P ) for convex polyhedra A(u A ) and B(u B ) can
be defined by the following formula:

                                                                                                  
                              AB (u A , u B , u   u P )  min{ AP (u A , u P ),  BP (u B , u P )} ,                         (1)
where P(u P )  {( x, y, z ) :  P    x    y    z   P  0} is a half-space,


  
                                      
                               0   cos  P
                                              1
                                                      sin 1P cos  2P        sin 1P sin  2P   0   sin 1P sin  2P 
                                                                                                                                
                                                                                                 
      M ( P ,  P , 0)   0  =  sin  P
              1      2                       1
                                                     cos 1P cos  2P          cos 1P sin  2P  .  0     cos 1P sin  2P  ,
                                                                                                                              




                                                                                              T
                           1 
                               0                     sin  2P                 cos  2P        1   cos  2P               
                                                                                                                               




                                                                                            IP
1P and  2P are appropriate (precession and nutation rotations) variable Euler angles (under intrinsic




                                                                                          CR
rotation  3P  0 ),

u P  (1P ,  2P ,  P )    is       a     vector      of     variable          parameters           that   define      a     plane

                                                               US
L AB  {( x, y, z ) :  P    x    y    z   P  0} in three-dimensional Euclidean space (we assume

 2   2   2  1 ),
                                                             AN

 AP (u A , u P ) is a phi-function of A(u A ) and half plane P(u P ) ,
                                                     M


      
 BP (u B , u P ) is a phi-function of B(u B ) and half plane P * (u P ) (the complement to P(u P ) ),
                                                                          *
                     AP (u A , u P )  min  P ( p sA ),  BP (u B , u P )  min ( P ( p sB )) .
                                      ED




                                           1sm A                                        1 s m B


We note that u p U  R ,   3.
                                  3
                         PT




It is known that if two fixed convex objects A and B do not have common points then there exists at

least one separating plane. Therefore there exists a vector u *P of parameters of a plane L AB such that
            CE




                                                                                                              
the distance d1   AP (u A , u *P ) from A to L AB equals to the distance d 2   BP (u B , u *P ) from B
AC




to L AB .        Thus           function         AB (u A , u B , u P )          reaches         its        maximum           when

(u A , u B , u *P )  (u A , u B , d * , d * ) , where d *  d1  d 2 .

Figure 3 illustrates two cases when   AB  0 :

a)  AB (u1, u 2 , u P0 )  min{d10 , d 20 }  d10 ;

b) max  AB (u1, u 2 , u P )   AB (u1, u 2 , u *P )  min{d1*, d 2*}  d1*  d 2*  d *.
     uP
                                        ACCEPTED MANUSCRIPT
                                                                                                              11




                                                                                     T
                                                                                   IP
                                  (a)                                                 (b)




                                                                                 CR
Fig.3 Separating planes for two fixed convex objects A and B : a)  AB  d * ; b)  AB  d10 .




                                                         US
Therefore always exists u P such that max  AB  0 for two non-overlapping convex polyhedra and


max  AB  0  int A(u A ) int B(u B )   .
                                              uP
                                                       AN
 uP


We identify here the important characteristic of a quasi phi-function: if  AB (u A , u B , u P )  0 for
some u P , then int A(u A ) int B(u B )   (see [19] for details).
                                              M


Let the minimal allowable distance  AB between two arbitrary convex polyhedra A(u A ) and B(u B )
                               ED




be given. To describe a distance constraint, dist( A , B )   AB , we use an adjusted radical free quasi
phi-function for convex polyhedra A(u A ) and B(u B ) derived by
                       PT




                                  AB (u A , u B , u P )   AB (u A , u B , u P )  0.5 AB .              (2)
         CE




Since   max  AB (u A , u B , u P )   AB (u A , u B )    and  AB (u A , u B )  0  dist( A, B)   AB , then
         uP

max  AB (u A , u B , u P )  0  dist( A, B)   AB . Based on the characteristic of a quasi phi-function,
AC




 uP

mentioned above, and formulas (1), (2), we can conclude that  AB (u A , u B , u P )  0 implies
dist( A, B)   AB .

        A quasi phi-function of two concave polyhedra is composed by quasi phi-functions for all
pairs of convex polyhedra that together form the original concave polyhedra. By analogy an adjusted
quasi phi-function of two concave polyhedra is constructed.
        Before we introduce a quasi phi-function and an adjusted quasi phi-function for a pair of
                                                   ACCEPTED MANUSCRIPT
                                                                                                                                             12

concave polyhedra we present a given collection of convex polyhedra, K qj , j=1,…,nq, q  J N , as a

                   N
set of n   n q convex polyhedra K i , i {1, 2, ..., n}  I n using the following rule: K j  K i ,
                                                                                                                                   q

                  q 1

      q 1
i   nl  j , j=1,…,nq, q  J N , provided that n 0  0.
      l 0

Now we introduce the “gluing” vector a  (a1, , , , a n ) , a i  J N , where a i  q , if K i takes part in

the composition of a polyhedron                         , q  J N . Let I n  I 1      I 2 ... I N be an ordered partition of
                        q
                             {i  I n , ai  q}, I q  nq , q  J N . For example, the “gluing” vector for polyhedra




                                                                                                  T
I n , where I




                                                                                                IP
             K1    K2,                 K3,                 K4    K5      K 6 has        the    form       a  (a1, a 2 , a 3 , a 4 , a 5 , a 6 )

                                                                            3
 (1,1, 2, 3, 3, 3) (Fig.4). In the example N=3 and n   n q  2  1  3  6 .




                                                                                              CR
                                                                           q 1




                                                                    US
                                                                  AN
                                                           M
                                          ED




Fig.4 – Generation of the “gluing” vector for polyhedra
                              PT




Let                         K i and                    K j be concave polyhedra and q  g .
              CE




                                                   g
                  iI   q                    jI


We introduce the following function:
AC




                                      Φqg (u q , u g , u qg )  min{ij (u q , u g , uij ), i  I q , j  I g } ,                         (3)

where ij (u q , u g , uij ) is the adjusted quasi phi-function and uij is a vector of auxiliary variables for

a pair of convex polyhedra                (        ) and     (   ), i  I q , j  I g , u qg  (u ij , i  I q , j  I g ) .

                                      
We note that u p U  R ,   3nqg , where nqg  nq  n g is the number of all pairs of appropriate

convex polyhedra that form                                   .

We show now that function (3) is an adjusted quasi phi-function Φqg for concave polyhedra                                               (     )
                                                    ACCEPTED MANUSCRIPT
                                                                                                                                     13
and       (    ). In fact, we need to prove that max Φqg (u q , u g , u qg ) is an adjusted phi-function for
                                                                      u qg

polyhedra            (   ) and           (     )

          Since each vector uij of auxiliary variables is met in appropriate function ij (u q , u g , uij )

only, then

                         max Φqg (u q , u g , u qg )  max min{ij (u q , u g , uij ), i  I q , j  I g } 
                         u qg                                  u qg


      min{max ij (u q , u g , uij ), i  I q , j  I g }  min{ ij (u q , u g ), i  I q , j  I g }  Φ qg (u q , u g ) ,
              uij




                                                                                                       T
where  ij (u q , u g ) is the adjusted phi-function for convex polyhedra                                            (   )       (   )




                                                                                                     IP
Φ qg (u q , u g ) is an adjusted phi-function for concave polyhedra                                 (       ) and   (    ) It should be




                                                                                                   CR
noted that function (3) is radical free.
From (3), a quasi phi-function for a pair of concave polyhedra,                                (    ) and       (   ) can be defined in
the form:

                                                                        US
                                 Φqg (u q , u g , u qg )  min{ij (u q , u g , u ij ), i  I q , j  I g } ,

where ij (u q , u g , uij ) is a quasi phi-function and uij is a vector of auxiliary variables for convex
                                                                      AN
polyhedra            (   ) and       (       ), i  I q , j  I g , u qg  (u ij , i  I q , j  I g ) .

Let us consider an example of a quasi phi-function for two polyhedra:                                   1 (u1 )  K1 (u1 ) and
                                                           M


  2 (u 2 )  K 2 (u 2 )         K 3 (u 2 ) (Fig. 5a).
                                         ED
                           PT
           CE
AC




                                                                         (b)
                                            ACCEPTED MANUSCRIPT
                                                                                                                               14
Fig.5 – a) polyhedra           1 and        2 ; b) separating planes          L12 and L13 for two pairs of appropriate

convex polyhedra K1 and K 2 ; K1 and K 3

A quasi phi-function for           1 (u1 ) and      2 (u 2 ) can be defined in the following form:


                          Φ12 (u1, u 2 , u12 )  min{12 (u1, u 2 , u12
                                                                        ), 13 (u1, u 2 , u13
                                                                                              )},

               , u13
where u12  (u12    ), 12 (u1, u 2 , u12
                                          ) is a quasi phi-function and u12
                                                                           is a vector of auxiliary

variables for a pair of convex polyhedra                 (    ) and       (    ), 13 (u1, u 2 , u13
                                                                                                    ) is a quasi phi-function

      is a vector of auxiliary variables for a pair of convex polyhedra
and u13                                                                                             (    ) and      (    )




                                                                                              T
 Figure 5b illustrates two separating planes L12 and L13 that provide 12 (u1, u 2 , u12
                                                                                        )  0 and




                                                                                            IP
13 (u1, u 2 , u13
                  )  0 that implies Φ12 (u1 , u 2 , u12 )  0 . Here Lij  {( x, y, z) :  ij  0} is a separating




                                                                                          CR
plane for K i (u q ) and K j (u g ) , where  ij   ij  x  ij  y   ij  z   ij ,  ij  sin 1ij sin  ij2 ,

 ij   cos 1ij sin  ij2 ,  ij  cos  ij2 and uij  (1ij ,  ij2 ,  ij ), i  1, j  2, 3, q  1, g  2.


                                                                US
3.5 Construction of phi-functions for containment - distance constraints
                                                              AN
An adjusted phi-function for a concave polyhedron                        (    ) and the object  * can be defined in the
form [4]

                                                      Φ q (u q )  min{ i (u q ), i  I q } ,                                (4)
                                                    M


where  i (u q ) is an adjusted phi-function for a convex polyhedron                                    (    ) and  * , i  I q .
                                   ED




Replacing each adjusted phi-function  i (u q ) in (4) by a phi-function  i (u q ) for i  I q , we can get

a phi-function Φ q (u q ) for a polyhedron                (    ) and the object  * .
                       PT




          To describe a containment constraint, K i (u q )    int K i (u q )  *   , we use a phi-

function for a convex polyhedron K i (u q ) and the object  * [4].
           CE




Let K i (u q ) be convex polyhedron, given in its local coordinate system by their vertices p ki ,
AC




k  1, ...., mi , where p ki  ( p ixk , p iyk , p izk ) . A radical free phi-function for a convex polyhedron

K i (u q ) and the object  * can be defined as

                                                       i (u q )  min{ min ik j (u q ), j  1, ..., 6},                     (5)
                                                                           1k mi

                          ik 1 (u q )  x q  p ixk ,  ik 2 (u q )  ( x q  p xk
                                                                                  i
                                                                                     )  l ,  ik 3 (u q )  y q  p iyk ,

               ik 4 (u q )  ( y q  p iyk )  w ,  ik 5 (u q )  z q  p izk ,  ik 6 (u q )  ( z q  p izk )  h .

Let minimal allowable distance                       between a convex polyhedron K i (u q ) and the object  * be
                                         ACCEPTED MANUSCRIPT
                                                                                                                              15
given. To describe distance constraint, dist( K i ,  * )   q , we use an adjusted phi-function for a

convex polyhedron K i (u q ) and the object  * defined by

                                                             i (u q )   i (u q )   q .                                   (6)


4. Mathematical model


The vector u  R  of all variables can be described as follows: u  (, )  R  , where
  (l , w, h, u1, u 2 , ..., u N ) , (l , w, h) denote the variable dimensions (length, width and height) of the




                                                                                            T
cuboid  and u a  (v a ,  a )  ( x a , y a , z a , 1a ,  a2 , 3a ) is the vector of placement parameters of




                                                                                          IP
                     i       i     i        i     i     i       i     i     i

K i , i  I n , an index a i {1, 2, ..., N } is a component of the ”gluing” vector a , defined in Section 3.




                                                                                        CR
Here   (u1 , ..., u m ) denotes the vector of all auxiliary variables, where u s  (1Ps ,  2Ps ,  s ) is a
              P          P                                                                          P                     P

vector of auxiliary variables for the s-th pair of convex polyhedra defined in (1), s  1,..., m,
m  card () ,
                                                              US
                                            {(i, j), ai  a j , i  j  1,..., n} .                                         (7)
                                                            AN
The number of the problem variables is derived as   3  6N  3m .
   Now a mathematical model of the polyhedron packing problem can be stated in the form
                                                 M


                                                                min       F (u) ,                                             (8)
                                                              uW  R 

                     W  {u  R  : ij (u ai , u a j , uai a j )  0, (i, j) ,  i (u ai )  0, i  1, 2,..., n} ,       (9)
                                 ED




where F (u)  l  w  h ,  ij' (u ai , u a j , uai a j ) is an adjusted quasi phi-function defined by (2),

ai , a j  I N , under (i, j )  , uai a j  u s , s  1,..., m,  is given by (7), for the pair of polyhedra K i
                         PT




                                                 P

and K j , taking into account minimal allowable distance  qg  0 ,  i (u ai ) is an adjusted phi-
         CE




function defined by (6) for a polyhedron K i and the object  * , taking into account minimal

allowable distance  q  0 . If  qg  0 and  q  0 then we replace the adjusted quasi phi-function
AC




ij (u ai , u a j , u ai a j ) by the quasi phi-function ij (u ai , u a j , uai a j ) , defined by (1), to enforce the

non-overlapping constraint and the adjusted phi-function  i (u ai ) by the phi-function  i (u ai ) ,

defined in (5), to enforce the containment constraint.
         It should be noted that in order to avoid redundant inequalities in containment constraints one

can use a collection of adjusted phi-functions Φ hq (u q )  0, q  1, ..., N , for the convex hull of concave

polyhedra         , q  1,..., N , instead of the collection of adjusted phi-functions  i (u ai )  0,

i  1,..., n, for convex polyhedra K i , i  1,..., n .
                                              ACCEPTED MANUSCRIPT
                                                                                                                             16
          Let us consider a mathematical model for a simple example of a packing problem for N=2
polyhedra:          1 (u1 )  K1 (u1 )        and     2 (u 2 )  K 2 (u 2 )       K 3 (u 2 )   (Fig.   5a)     in   a   cuboid

  {( x, y, z)  R 3 : 0  x  l , 0  y  w, 0  z  h} . Here n=3 is the number of convex polyhedra,
a  (a1, a 2 , a 3 )  (1, 2, 2)   is the gluing vector,   {(i, j ), ai  a j , i  j  1, 2, 3}  {(1, 2), (1, 3)},

u ai  (v ai ,  ai )  ( x ai , y ai , z ai , 1ai ,  a2i , 3a ) is the vector of placement parameters of K i , i  1, 2, 3 .
                                                       i

according to the gluing vector, m=2 is the number of pairs of convex polyhedra with respect to  ,

                        , u13
  (u 1P , u 2P )  (u12    )          is     the        vector       of         auxiliary      variables,          3m  6 ,




                                                                                              T
                           , u13
u  (l , w, h, u1, u 2 , u12    ) is the vector of the problem variables. The number of the problem




                                                                                            IP
variables is   3  6N  3m  21 .
Now mathematical model (8)-(9) for the packing problem takes the form




                                                                                          CR
                                                             min        F (u) ,
                                                           uW  R 21

W  {u  R 21 : 12 (u1, u 2 , u12
                                  )  0, 13 (u1, u 2 , u13
                                                            )  0, 1(u1)  0,  2 (u 2 )  0,  3 (u 2 )  0},
where
12 (u1, u 2 , u12
                                                              US
                  ) is a quasi phi-function for K 1 (u1 ) and K 2 (u 2 ),
                                                            AN
13 (u1, u 2 , u13
                  ) is a quasi phi-function for K 1 (u1 ) and K 3 (u 2 ) ,

 1 (u1 ) is a phi-function for K 1 (u1 ) and the object  * ,
                                                    M


 2 (u 2 ) is a phi-function for K 2 (u 2 ) and the object  * ,

 3 (u 2 ) is a phi-function for K 3 (u 2 ) and the object  * .
                                   ED




We note, that in the model we can use two phi-functions: phi-function 1 (u1 ) and a phi-function for

the convex hull of concave polyhedra                   and the object  * instead of phi-functions  i (u ai )  0,
                       PT




i  1, 2, 3, for convex polyhedra K i , i  1, 2, 3 and the object  * .
          CE




          Each quasi phi-function inequality in (9) is presented by a system of inequalities with
infinitely differentiable functions. Our model (8)-(9) is a non-convex and continuous nonlinear
programming problem and an exact formulation for the polyhedron packing problem. It contains all
AC




globally optimal solutions. It is possible, at least in theory, to use a global solver for the nonlinear
programming problem and to obtain a solution, which is an optimal packing.

          However in practice, the model contains a large number of variables and a huge number of
inequalities. Specifically, the model (8)-(9) involves O(n2) nonlinear inequalities and O(n2) variables
due to the auxiliary variables in quasi phi-functions, where n is the number of convex polyhedra. As a
result, finding a locally optimal solution becomes an unrealistic task for the available state of the art
NLP-solvers employed directly to model (8)-(9): for N >15 starting from a random point and for N
>30 starting from a feasible point.
                                      ACCEPTED MANUSCRIPT
                                                                                                                 17
          In order to search for a “good” locally optimal polyhedron packing within a reasonable
computational time we propose here an efficient solution algorithm, which employs a fast starting
point algorithm (FAPA) and a new compaction procedure. In most cases the procedure reduces our
problem to a sequence of nonlinear programming subproblems of considerably smaller dimension
(O(n)) and a smaller number of nonlinear inequalities (O(n)). We use NLP-solver (IPOPT) to solve
each of the NLP subproblems starting from the feasible points found by the special procedures
described in Section 5.


5. Solution algorithm




                                                                                T
          Our multi-start solution strategy involves the following steps:




                                                                              IP
1) Generate a set { 0 } of vectors  0  (l 0 , w0 , h 0 , u10 , u 20 ,..., u N
                                                                                0
                                                                                  ) of feasible placement parameters




                                                                            CR
    (u10 , u 20 ,..., u N
                        0
                          ) of polyhedra placed into the container  0 of sizes (l 0 , w0 , h 0 ) in the problem
   (8)-(9). Various algorithms exist for obtaining a feasible solution (for example [17]). We employ
   here the clear and fast algorithm, which is described in Subsection 5.1.

                                                      US
2) Search for a local minimum of the objective function F(u) in problem (8)-(9), starting from each

   point from the set { 0 } obtained at Step 1. To get a local minimum of problem (8)-(9) we
                                                    AN
   develop a compaction algorithm for rotated polyhedra described in Subsection 5.2.
3) Choose the best local minimum from those found at Step 2 as the final solution of the problem (8)-
   (9).
                                               M


The actual search for a local minimum in all optimization procedures (to realize steps 1-2) is
performed by IPOPT [23], which is available at an open access noncommercial software depository
                               ED




(https://projects.coin-or.org/Ipopt) .
                    PT




5.1 Feasible Placement Parameters Algorithm (FPPA)
In order to find a vector of starting feasible placement parameters of polyhedra we apply an algorithm,
which is based on the homothetic (scaling) transformation of objects. The algorithm consists of the
          CE




following steps.

Firstly we choose a sufficiently large starting length l 0 , width w 0 and height h 0 for a container  0
AC




to allow for a placement of all spheres S q , q  1, 2,..., N , within the container  0 , where

                                                                                                       
S q  S q  S  is the Minkovski sum of a sphere S q of radius rq (Fig. 6) and a sphere S                 of radius

  0.5 max{ max  qg , max  q } , provided that S q and S  have the same center point. For
               q, gJ N      qJ N

                                           n
example, we can set l 0  w 0  h 0  2  rq  (n  1)  .
                                          q 1

Secondly we generate within the container  0 a set of N randomly chosen center points
                                                    ACCEPTED MANUSCRIPT
                                                                                                                                   18
( x q0 , y q0 , z q0 ) of S q , q  1, 2,..., N .




                                                                                                   T
                                                                                                 IP
           Fig. 6 – Concave polyhedra                      and appropriate spheres S q .




                                                                                               CR
Thirdly we grow the spheres S q of radius (rq  ) , q  1, 2, ..., N , starting from   0 to the full


                                                                        US
size (   1) and the decision variables are: the centres of S q and a homothetic coefficient (a scaling

parameter)  , where 0    1 (Fig 7.). In order to realise this step we fix l  l 0 , w  w 0 , h  h 0 ,
                                                                      AN
and, starting from the point v 0  ( x10 , y10 , z10 ,..., x N
                                                             0    0
                                                               , yN    0
                                                                    , zN ,  0  0) , solve the following NLP-
subproblem:
                                                           M


                                                                            max  ,                                               (10)
                                                                            vW

                                                                      S *
                 W  {v  R 3N 1 :  q g (v)  0,  q
                                                S S
                                                                             (v)  0, q  g  1, 2, ..., N ,1    0,   0} ,
                                        ED




                                                                                                                                  (11)
     where v  ( x1, y1, z1, ..., x N , y N , z N , ) ,
                                 S S
                               q g (v)  ( xq  x g ) 2  ( y q  y g ) 2  ( z q  z g ) 2   2 (rq  2  rg ) 2 ,
                           PT




                                                                                                                                  (12)

     is an adjusted phi-function for a sphere S q of radius  rq and a sphere S g of radius  rg ;
            CE




                                                      S *
                                                     q         (v)  min{ kq (v), k  1, ..., 6} ,                              (13)

     is an adjusted phi-function for a sphere S q of radius  rq and the object  * , where
AC




                                  1q (v)   x q  l 0  (rq   q ) ,  2q (v)  xq  (rq  2) ,

                                  3q (v)   y q  w 0  (rq   q ) ,  4q (v)  y q  (rq  2) ,

                                   5q (v)   z q  h 0  (rq   q ) ,  4q (v)  z q  (rq  2) .

We        denote          a      point         of       the        global       maximum         of      problem       (10)-(11)    by

v *  ( x1* , y1* , z1* ,..., x *N , y *N , z *N ,  *  1) .

Finally we form a vector of feasible parameters  0  (l 0 , w 0 , h 0 , u10 , ..., u q0 , ..., u N
                                                                                                  0
                                                                                                    ) , assuming that
                                             ACCEPTED MANUSCRIPT
                                                                                                                                      19
u q0  ( x q0 , y q0 , z q0 ,  0q ) , ( x q0 , y q0 , z q0 )  ( x q* , y q* , z q* ) and  0q is a vector of randomly generated rotation

parameters of polyhedra               , q  1,..., N .
We note that the global solution of problem (10)-(11) always can be found (since the chosen starting

sizes l 0 , w 0 and h 0 at the first step are sufficiently large). The solution automatically respects all
the non-overlapping, containment and distance constraints for the concave polyhedra.




                                                                                               T
         0                                           0                                         0




                                                                                             IP
               0                                           0.3                                      0.75




                                                                                           CR
                                       0
                                                                US                    0
                                                              AN
                                                0.97                                         1
     Fig. 7 – Illustration of the optimisation procedure FPPA to search for feasible placement
     parameters of polyhedra, using homothetic transformations
                                                     M


Our FPPA algorithm returns the vector  0 to generate a starting point u 0  ( 0 ,  0 ) for a subsequent
                                    ED




search for a local minimum of the problem (8)-(9). To search for vector  0 we apply special
optimisation procedure, called Feasible Auxiliary Parameters Algorithm (FAPA), described below.
                        PT




5.2 Compaction Algorithm (COMPOLY)
           CE




           Since our problem (8)-(9) can not be solved for N >30 by direct use of state of the art NLP-
solvers (starting from a feasible point), we propose an iterative compaction algorithm to search for
AC




local minima of the problem.
          Our algorithm reduces the problem (8)-(9) that has a large number of inequalities and
dimension O(n2) of the feasible set W, described by (9), to a sequence of nonlinear programming
subproblems that have a smaller number of nonlinear inequalities (O(n)) and dimension O(n). The key
idea of the algorithm is as follows: For each vector of feasible placement parameters of our
polyhedral, we construct fixed individual cubic containers of spheres that circumscribe the appropriate
convex polyhedra. Then we move each sphere within the appropriate individual container. The motion
of each sphere we describe by a system of six linear  -inequalities. Then we form a subregion of
feasible region W in the following way: we add O(n)  -inequalities (for all spheres) to the inequality
                                       ACCEPTED MANUSCRIPT
                                                                                                                     20
                                                        2
system (9), that allows us to delete O(n ) phi-inequalities for such pairs of polyhedra whose
individual containers do not overlap each other and delete some redundant containment constraints.
Then we search for a local minimum on the subregion of dimension O(n). The subregion is described
by O(n) nonlinear inequalities. Then we use this local minimum as a starting point for the next
iteration. On the last iteration of our algorithm we find a local minimum of problem (8)-(9).
          Let us consider the algorithm in details.

We assume here that spheres S q0  S q (0) of radius rq and the center point vq  ( xq , y q , z q ),

circumscribed around each non-translated and non-rotated concave polyhedron                         , q  1, ..., N , as

well as, spheres S i0  S i (0) of radius ri and the center point v ci  ( xci , y ci , z ci ) circumscribed




                                                                                         T
                                                                                       IP
around each non-translated and non-rotated convex polyhedron K i0 , i  1,..., n , are constructed.
          The COMPOLY algorithm is an iterative procedure and involves the following steps.




                                                                                     CR
Step 1. Let k  1 . Take the vector  k 1  (l k 1, w k 1, h k 1, u1k 1,..., u N
                                                                                    k 1
                                                                                         ) of feasible placement

parameters of polyhedra         , q  1,..., N , within the container  k 1 .

Step 2. Derive the appropriate vector (v c(1k 1) , .., v cn  US
                                                          ( k 1)
                                                                  ) of center points of spheres S i (u a(k 1) ),

i  1, 2,..., n . With respect to the gluing vector a, the center point v ci of S i  K i after translation and
                                                                                                                 i
                                                            AN
rotation of initial convex polygon K i0 takes the form
                                 (k 1)
                                vci      vci (u a(k 1) )  v a(k 1)  M ( (ak 1) )  vci .
                                               M


                                                    i            i               i

For the sake of simplicity, we provide some illustrations to the algorithm for the 2D case.
                               ED




Figure 8 illustrates the concave polygon                ( )          ( )       ( ) with translation vector (0, 0) and
rotation angle   0 . Circles S1 (0) and S 2 (0) , circumscribed around K1 (0) and K 2 (0) have center

                                    ( ), translated by vector v 0 and rotated by angle  0 , is denoted by
                      PT




points v c1 and v c 2 . Polygon

  (   )       (   )      (    ), where u 0  (v 0 ,  0 ) . Center points of circles S1 (u 0 ) and S 2 (u 0 ) are
          CE




denoted by vc01 and v c02 .
AC
                                                                ACCEPTED MANUSCRIPT
                                                                                                                                                   21

             Fig. 8 – Translation and rotation parameters of S1 (u 0 ) and S 2 (u 0 ) of concave polygon

  ( )             ( )                ( ), translated by vector v 0 and rotated by angle  0 .


Step 3. For each sphere S i (u a(k 1) ) we construct a fixed individual container  ik  S i  K i with
                                                        i

                                                                                      ( k 1)
equal half-sides of length ri   , i  1,..., n , and the center of symmetry point v ci      , assuming
     n
   ri / n . Figure 9 illustrates individual containers 1 (u a0 ) and  2 (u a0 ) for circles S1 (u a0 ) and
                                                                                                       1                       2               1
    i 1




                                                                                                                         T
S 2 (u a0 ) considered in the above example. Note, that here a1  a 2 .
         2




                                                                                                                       IP
                                                                                  1       
             S1




                                                                                                                     CR
                        v c01                                                         v c01
                                                                                                                           
                                 0         v c02                                               v0
                            v

                                                   S2
                                                                                        US                 
                                                                                                               v c02

                                                                                                                           2
                                                                                      AN
             Fig. 9 – Individual containers 1 (u a0 ) and  2 (u a0 ) for circles S1 (u a0 ) and S 2 (u a0 ).
                                                                              1                    2                               1       2
                                                                      M


Step 4. Move each sphere S i , associated with the convex polyhedron K i , within the appropriate

fixed individual container  ik (found at Step 3). Hence, for each sphere S i we construct a phi-
                                              ED




                        
function  S i  i for sphere S i and *i  R 3 \ int  i in the form:
              
     S i  i (v ai , v a( k 1) )  min{ x ci (u a( k 1) )  x ai  ,  y ci (u a( k 1) )  y ai  ,  z ci (u a( k 1) )  z ai  ,
                                PT




                             i                                    i                                    i                               i

                  xci (u a(k 1) )  x ai  , y ci (u a(k 1) )  y ai  , z ci (u a(k 1) )  z ai  }.
                             i                                        i                                i
             CE




                                       
The inequality  S i  i (v ai , v a( k 1) )  0 provides S i   ik and can be described by the following
                                                    i

inequality system of six linear "  -constraints":
AC




                   xci (u a(k 1) )  xai    0,  y ci (u a(k 1) )  y ai    0,  z ci (u a(k 1) )  z ai    0,
                                 i                                                i                                        i

                    xci (u a(k 1) )  xai    0, y ci (u a(k 1) )  y ai    0, z ci (u a(k 1) )  z ai    0.
                                 i                                                i                                    i


 Now we introduce an auxiliary (artificial) subset  k of additional "  -constraints" on the translation

vectors vai  ( x ai , y ai , z ai ) , i  1,..., n, of convex polyhedra K i , i  1,..., n :

                             k  {u  R  :  xci (u a(k 1) )  x ai    0,  y ci (u a(k 1) )  y ai    0,
                                                                          i                                      i

                                             z ci (u a(k 1) )  z ai    0, xci (u a(k 1) )  xai    0,
                                                            i                                  i
                                                                    ACCEPTED MANUSCRIPT
                                                                                                                                                                                    22

                                         y ci (u a(k 1) )  y ai    0, z ci (u a(k 1) )  z ai    0, i  1, ..., n} .
                                                         i                                      i


Then we add the inequality system of 6n additional linear "  -constraints" that describe the subset  k

to the inequality system that defines the feasible region W and obtain k-th subregion Wk  W                                                                                   k .

It should be noted that the inequality system that describes the feasible subregion W k in most cases
involves O(n2) redundant phi-inequalities.


Step 5. To avoid the redundant phi-inequalities that describe W k we form special index sets 1k and




                                                                                                                                     T
 k2 that involve indexes of all pairs of objects that are associated with non-redundant non-overlapping




                                                                                                                                   IP
and containment constraints respectively.
To form index set 1k we exclude from  (7) indexes of all pairs of convex polyhedra where




                                                                                                                                 CR
individual containers do not intersect each other (see Appendix B):



1k  {(i, j ) 1kS : 
                                              ik  kj
                                                                                          US
                                                         (v a( k 1) , v a( k 1) )  0} , where 1kS  {(i, j )  : 
                                                             i

                                                       ik  kj
                                                                          j
                                                                                                                                         S ai S a j
                                                                                                                                                      (v a(k 1) , v a(k 1) )  0}
                                                                                                                                                          i           j
                                                                                        AN
                                                                 (v a( k 1) , v a( k 1) )  max{ ijs (v a( k 1) , v a( k 1) ), s  1, ..., 6} ,
                                                                      i           j                              i               j


             1ij (v a( k 1) , v a(k 1) )  ( xi(k 1)  x (jk 1) )  Rij ,  ij2 (v a(k 1) , v a(k 1) )  ( y i( k 1)  y (jk 1) )  Rij ,
                            i            j                                                               i               j
                                                                              M


              3ij (v a( k 1) , v a(k 1) )  ( z i(k 1)  z (jk 1) )  Rij ,  ij4 (v a(k 1) , v a(k 1) )  ( xi(k 1)  x (jk 1) )  Rij ,
                            i            j                                                              i            j
                                                         ED




             5ij (v a(k 1) , v a(k 1) )  ( y i(k 1)  y (jk 1) )  Rij ,  ij6 (v a(k 1) , v a(k 1) )  ( z i( k 1)  z (jk 1) )  Rij ,
                        i            j                                                                       i               j

                                                                              Rij  (ri  r j )  ij  2 ,
                                   PT




    S ai S a j
                (v a( k 1) , v a( k 1) ) is an adjusted phi-function (12) for a pair of spheres S q and S g (
                       i             j
                 CE




                                                                                                                 (       )               (     )                          (     )
                 ), circumscribed around concave polyhedra                                                   (               )       (              ) and         (                 )
        (        )
    (                ). We provide some illustrations to form index set 1k in Appendix B.
AC




              We note that if (i, j ) 1k , then we do not need to check the distance (or non-overlapping)
                                                                                                                                             ( k 1)
constraint for the corresponding pair of polyhedra K i (u a(k 1) ) and K j (u a                                                                       ) . If  ij  0 then
                                                                                                                 i                              j

                      ik  kj
function                        (v a( k 1) , v a( k 1) ) becomes a phi-function for two oriented parallelepipeds  i and  j .
                                     i                   j


To form index set  k2 we exclude from (8) all phi-inequalities for containment constraints of convex

polyhedra where individual containers do not intersect the set  k*  R 3 \ int  k , such that

                                  k  {( x, y, z) :   x  l (k 1)  ,   y  w (k 1)  ,   z  h (k 1)  }.
                                                                   ACCEPTED MANUSCRIPT
                                                                                                                                                                           23
                                               ik                                             k 
Thus,  k2  {i  kS
                   2 :                                   (v a( k 1) )  0} , where   i   (v a( k 1) ) is an adjusted phi-function for a
                                                               i                                          i

                                                                                                                  S  k                           S ai  k *
polyhedron K i (u a(k 1) ) and the object  k* ,  kS
                                                     2  {i  I n : 
                                                                      ai
                                                                                                                             (v a(k 1) )  0},                   is an
                                      i                                                                                          i

                                                                                                                                                               (       )
adjusted phi-function (13) for a sphere S q , associated with concave polyhedron                                                                       (                   )

       (       )
  (                ), and the object * , a i  q ,
                                                           k       k
                                                     i   (v a( k 1) )  min{ is (v a( k 1) ), s  1, ..., 6} ,
                                                                         i                          i

                        1i (v a(k 1) )  xi(k 1)  Ri ,  i2 (va(k 1) )  yi(k 1)  Ri ,  3i (v a(k 1) )  z i(k 1)  Ri ,




                                                                                                                        T
                                  i                                               i                                     i

                             i4 (v a(k 1) )   xi(k 1)  l (k 1)  Ri ,  5i (va(k 1) )   yi(k 1)  w(k 1)  Ri ,




                                                                                                                      IP
                                          i                                                         i

                                               i6 (va(k 1) )   z i(k 1)  h (k 1)  Ri , Ri  ri   q  2 .




                                                                                                                    CR
                                                           i

We note that if i  k2 , then we do not need to check the distance (or containment) constraint for the

polyhedron K i (u a(k 1) ) and the object  k .
                                  i

Step 6. Generate the k-th subproblem on solution subset Wk  W
                                                                                        US                             k with deleted redundant phi-
                                                                                      AN
function inequalities and reduced dimension (O(n)):
                                                                                      min         F (u wk ) ,                                                          (14)
                                                                             u wk Wk  R  k
                                                                         M


                   Wk  {u wk  (,  wk )  R  k :  ij' (u ai , u a j )  0, (i, j ) 1k ,  i (u ai )  0, i  2k ,
                             k
                    S i  i (u ai )  0, i  1, ..., n, l  l ( k 1)  , w  w ( k 1)  , h  h ( k 1)  },
                                                   ED




where 1k and  k2 are defined on Step 5,  k  3(m  card (1k )) is the number of all deleted auxiliary
variables                meeting                   in              the        appropriate           redundant                phi-function             inequalities,
                                  PT




   k  3  6 N  card ( 1k ), card (1 ) is (O(n)).
                                                                         k


Step 7. Generate a feasible starting point u (k 1)  ( (k 1) ,  (wk 1) ) for problem (14). Since a vector
               CE




                                                                                                              k


 ( k1) has already defined, we need to find values of the vector of auxiliary variables
AC




 (wk 1)  (u (k 1)1,..., u (k 1) s ,..., u (k 1)m ) for such s {1,..., m} that (i, j ) 1 .
                                                                                                                                     k
   k                P                     P                        P

       To derive a vector u (k 1) s we employ the FAPA algorithm.
                                               P

               The key idea of the FAPA algorithm lies in the following (see Appendix C): we derive a

vector u (k 1) s as a vector of feasible parameters of a separating plane for two spheres S i (u a(k 1) ) and
               P                                                                                                                                           i


S j (u a( k 1) ) if  i j  0 , using simple geometrical calculations, otherwise we find a vector u (k 1) s ,
                              SS
           j                                                                                                                                                       P

solving the following auxilary subproblem
                                       ACCEPTED MANUSCRIPT
                                                                                                                         24
                                               max  s.t. (u s , ) W' ,                                             (15)
                                                                 P

where

                          W'  {(u s , )  R 4 :  ij' (u a( k 1) , u a( k 1) , u s )    0} ,
                                       P                         i         j           P


  R1 , u s  (1Ps ,  2Ps ,  s ), under fixed parameters (u a( k 1) , u a( k 1) ) involving in the appropriate
            P                 P                                            i               j

                                    ( k 1) ( k 1)
adjusted quasi phi-function ij (u a , u a , u s ) , (i, j )  . It should be noted that any
                                      i        j    P


nonnegative value of  in (15) provides feasible values of u s .
                                                                               P




                                                                                               T
Thus, all adjusted quasi phi-functions and phi-functions in (14) at the point u ( k 1) take nonnegative




                                                                                             IP
values.

     Step 8. Solve subproblem (14), starting from the feasible point u ( k 1)




                                                                                           CR
                                                                min                F (u wk ) ,                         (16)
                                                         u wk Wk  R  k


and get a local minimum point u *w  ( *k , *wk ) .
                                  k                     k
                                                          US
If the point u *wk of local minimum of subproblem (16) belongs to the frontier of an auxiliary subset
                                                        AN
 k , i.e. u *wk  fr  k , then we take  *k as a starting vector  k for the next iteration of the procedure

(set k =k+1 and go to Step 2), otherwise we stop the optimisation procedure.
                                               M


We claim that the point u *  u *k  ( *k , *k )  R  is a point of local minimum of problem (8)-(9),

where  *k involves *wk and auxiliary variables that are deleted at the k-th iteration. Note that the  k
                              ED




                          k

previously deleted auxiliary variables can be redefined by FAPA algorithm. However we do not need
to redefine the deleted auxiliary variables at the last step of the algorithm, since the values of auxiliary
                    PT




variables have no effect on the value of the objective function, i.e. F (u *wk )  F (u *k ) .
          CE




          Figure 10 shows the diagram of the COMPOLY procedure to solve problem (8)-(9). We
illustrate the procedure of solving a sequence of subproblems, given by (16), for k=2,3,4. Note, that

feasible starting point u (0) is found by algorithm FPPA. Each auxiliary (artificial) set  k , described
AC




at Step 4 of the COMPOLY procedure, is shown as a square with the centre point u (k 1) , k=1,2,3,4.

          We take the feasible point u (0) , form set 1 with the center point u (0) , solve subproblem

(16) on subregion W1  1        W and get a local minimum point u *w1 . The point u *w1 belongs to the

frontier of set 1 , therefore we form the next set  2 with the center point u (1)  u *w1 and search for

a local minimum point u *w2 of subproblem (16) on subregion W2   2                            W . The point u *w2 belongs

to the frontier of set  2 , therefore we form the next set  3 with the center point u (2)  u *w2 and
                                    ACCEPTED MANUSCRIPT
                                                                                                            25

search for a local minimum point u *w3 of subproblem (16) on subregion W3   3              W . The point

u *w3 belongs to the interior of set  3 , i.e. u *w3  int  3 , therefore we stop our procedure. The point

u *w3 = u* is a point of local minimum of problem (8)-(9).




                                                                            T
                                                                          IP
                                                                        CR
                                                   US
                                                 AN

        Fig. 10 – Diagram of the COMPOLY procedure.
                                          M


Figure 11 illustrates the iterative procedure of packing concave polyhedra that is related to the
                             ED




Diagram shown in Figure 10.
                   PT
        CE
AC




                                                       u(0)




                  u(1)                                        u(2)                              u* = u(3)
    Fig. 11 – Arrangements of concave polyhedra, corresponding to the sequence of feasible points
                                          ACCEPTED MANUSCRIPT
                                                                                                                26
      (0)     (1)   (2)   *   (3)
    u , u ,u ,u =u                  with respect to the Diagram.


We note that dist( u *wk , u *w k 1 )   , if u *wk 1  fr  k , and we take the value of  that is considerably

greater than the accuracy of IPOPT ( 10  8 ). Thus, we can conclude that the stopping condition of the
COMPOLY procedure is always reached in a finite number of iterations.
            If the IPOPT program fails to find a local minimum of subproblem (14), we halve the value of
 and start up the COMPOLY procedure. If a local minimum is found under the half value of  then
we recover the initial value of epsilon and continue the COMPOLY procedure for a new feasible




                                                                                T
starting point, otherwise we terminate the procedure.
            Our algorithm, in most cases, takes consideration of significantly fewer pairs of polyhedra




                                                                              IP
than m (here m is the number of all pairs of convex polyhedra considered in problem (8)-(9)),




                                                                            CR
because for each polyhedron only its “  -neighbors” have to be monitored. It should be noted that the
algorithm is not efficient for special cases when all objects are “  -neighbors”.
            The parameter  provides a balance between the number of inequalities in each nonlinear

                                                         US
programming subproblem (14) and the number of the subproblems (12), which we need to generate
and solve in order to get a local optimal solution of problem (8)-(9).
                                                       AN
Thus the COMPOLY algorithm allows us to reduce the problem (8)-(9) with a large number of
inequalities and dimension O(n2) of the feasible set W, described by (9), to a sequence of subproblems
(14) with a smaller number of nonlinear inequalities and dimension O(n) of solution subset Wk .
                                                M


6. Computational experiments
                                    ED




            We present a number of examples to demonstrate the efficiency of our methodology. We have
run all experiments on an AMD Athlon 64 X2 5200+ computer, Programming Language C++,
Windows 7. For the local optimisation we use the IPOPT code (https://projects.coin-or.org/Ipopt) by
                          PT




means of program interface using the default options.
            The following examples set   5 for the COMPOLY procedure.
            CE




Example 1. We generate a collection of n = 98 convex polyhedra, consisting of the 7 types of
polyhedra from example 1 given in [18] and in Appendix A. We include 14 of each type of polyhedra.
AC




Figure 12 shows the local optimal placement of the collection of convex polyhedra. The container has

dimensions and volume: a) (l * , w* , h * ) =(30.9324, 28.1897, 26.5064) and F (u * )  23113.06 with

  0 (Fig. 12a). One starting point is used. Computational time is 147967.3 sec.; b) (l * , w* , h * )

=(41.3510, 33.0721, 31.7988) and F (u * )  43487.0040 with   1.5 (Fig. 12b). One starting point is
used. Computational time is 48152.79 sec.
                                      ACCEPTED MANUSCRIPT
                                                                                                        27




                                                                            T
                               (a)                              (b)




                                                                          IP
         Fig. 12 – Local optimal placement of polyhedra in Example 1: a)   0 ; b)   1.5.




                                                                        CR
Example 2. We generate a collection of N=20 concave polyhedra, consisting of the 2 types of
polyhedra given in [17] and in Appendix A. We include 10 of each type of polyhedra. Figure 13

                                                  US
shows the local optimal placement of the collection of concave polyhedra. The container has

dimensions and volume: a) (l * , w* , h * ) =(26.3522, 23.7514, 24.4055) and F (u * )  15275.4815 with
                                                AN
  0 (Fig. 13a). Two starting points are used. Computational time is 8729.45 sec.; b) (l * , w* , h * )

=(26.5890, 26.5239, 36.1706) and F (u * )  25509.2576 with   1.5 . Ten starting points are used.
                                         M


Computational time is 24696.46 sec. (Fig. 13b).
                            ED
                   PT
        CE




                                (a)                                   (b)
         Fig. 13 – Local optimal placement of polyhedra in Example 2: a)   0 ; b)   1.5.
AC




Example 3. We consider a collection of N=20 equal concave polyhedra given in [17] and in Appendix
A. Figure 14 shows the local optimal placement of the collection of concave polyhedra. The container

has dimensions and volume: a) (l * , w* , h * ) =(23.7706, 26.6212, 20.2363) and F (u * )  12805.6718
with   0 . Ten starting points are used. Computational time is 59497.9 sec. (Fig. 14a); b)

(l * , w* , h * ) =(27.9795, 26.5408, 30.6725) and F (u * )  22777.4233 with   1.5 . Ten starting points
are used. Computational time is 28700.16 sec. (Fig. 14b).
                                    ACCEPTED MANUSCRIPT
                                                                                                             28




                                                                           T
                                  (a)                                           (b)
            Fig.14 – Local optimal placement of polyhedra in Example 3: a)   0 ; b)   1.5 .




                                                                         IP
                                                                       CR
Example 4. We pack 45 concave polyhedra of 10 types given in Appendix A. We include 5 polyhedra
of each type of the upper polyhedra row and 4 polyhedra of each type of the lower polyhedra row
(Fig. A3). Figure 15 shows the local optimal placement of the collection of concave polyhedra. The

                                                   US
container has dimensions (l * , w* , h * ) = (39.7324, 34.8629, 44.6587) and volume F (u * )  61860.807.
Three starting points are used. Computational time is 159884.0 sec.
                                                 AN
                                          M
                             ED
                    PT




                 Fig.15 – Local optimal placement of concave polyhedra in Example 4.
         CE




Futher we compare our results to those given in [17] and [18]. We search for locally optimal solutions
employing the compaction algorithm: a) starting from a feasible point generated by FPPA algorithm
AC




described in Section 5.1 and b) starting from a feasible point found by the algorithm developed in [17]
and [18].
Example 5. We consider a collection of n=80 convex polyhedra, of example 1 given in [18] and in
Appendix A. Figure 16 shows the local optimal placement of the collection of convex polyhedra. The

container has dimensions and volume: a) (l * , w* , h * ) =(43.4338, 41.8435, 45.0059) and F (u * ) 
81795.2169, starting from the feasible point found by FPPA. Computational time is 46035.78 sec.; b)

(l * , w* , h * ) =(36.3569, 40.8764, 56.2557) and F (u * )  83604.0544, starting from the feasible point
                                  ACCEPTED MANUSCRIPT
                                                                                                  29
found by the algorithm given in [18]. Computational time is 42950.4 sec.. Improvement of the value
of objective function in comparison to the result given in [18]: a) 27.88%; b) 26.29%
.




                                                                        T
                                                                      IP
                       (a)                                    (b)




                                                                    CR
        Fig.16 – Local optimal placement of polyhedra in Example 5: a) starting from the feasible
point found by FPPA; b) starting from the feasible point found by the algorithm given in [18].



                                                US
Example 6. We consider a collection of N=20 concave polyhedra, of example 2 given in [17] and in
Appendix A. Figure 17 shows the local optimal placement of the collection of concave polyhedra. The
                                              AN
container has dimensions and volume: a) (l * , w* , h * ) =(29.7159, 30.6070, 30.1616) and F (u * ) 

27432.6412, starting from the feasible point found by FPPA; b) (l * , w* , h * ) =(31.4820, 27.8994,
                                       M


32.0000) and F (u * )  28106.6387, starting from the feasible point found by the algorithm given in
[17]. We generate 11 starting points, time limit is 10 hours. Improvement of the value of objective
                              ED




function in comparison to the result given in [17]: a) 18.36%; b) 16.35%
                  PT
        CE
AC




                        (a)                                         (b)
        Fig.17 – Local optimal placement of polyhedra in Example 6: a) starting from the feasible
point found by FPPA; b) starting from the feasible point found by the algorithm given in [17].


Example 7. We consider a collection of N=30 concave polyhedra, of example 3 given in [17] and in
Appendix A. Figure 18 shows the local optimal placement of the collection of concave polyhedra. The

container has dimensions and volume: a) (l * , w* , h * ) =(36.9929, 36.3796, 30.9454) and F (u * ) 
                                  ACCEPTED MANUSCRIPT
                                                                                                   30

41646.1709, starting from the feasible point found by FPPA; b) (l * , w* , h * ) =(31.4376, 26.1920,

48.9148) and F (u * )  40277.1892, starting from the feasible point found by the algorithm given in
[17]. We generate 11 starting points, time limit is 10 hours. Improvement of the value of objective
function in comparison to the result given in [17]: a) 19.06 %; b) 21.72%




                                                                         T
                                                                       IP
                                                                     CR
                       (a)                                            (b)

                                                US
        Fig.18 – Local optimal placement of polyhedra in Example 7: a) starting from the feasible
point found by FPPA; b) starting from the feasible point found by the algorithm given in [17].
                                              AN
Example 8. We consider a collection of N=40 concave polyhedra, of example 4 given in [17] and in
Appendix A. Figure 19 shows the local optimal placement of the collection of concave polyhedra. The
                                       M


container has dimensions and volume: a) (l * , w* , h * ) =(34.9974, 36.9655, 43.2777) and F (u * ) 

55988.4619, starting from the feasible point found by FPPA; b) (l * , w* , h * ) =(31.1419, 30.8086,
                             ED




55.4061) and F (u * )  53158.8838, starting from the feasible point found by the algorithm given in
[17]. We use 3 starting points, time limit is 10 hours. Improvement of the value of objective function
                  PT




in comparison to the result given in [17]: a) 15.64%; b) 19.91%
        CE
AC




                       (a)                                     (b)
        Fig.19 – Local optimal placement of polyhedra in Example 8: a) starting from the feasible
point found by FPPA; b) starting from the feasible point found by the algorithm given in [17].
Example 9. We consider a collection of n=50 concave polyhedra, of example 9 given in [17] and in
                                    ACCEPTED MANUSCRIPT
                                                                                                           31
Appendix A. Figure 20 shows the local optimal placement of the collection of concave polyhedra. The

container has dimensions and volume: a) (l * , w* , h * ) =(46.9742, 34.8305, 41.6923) and F (u * ) 

68214.5610, starting from the feasible point found by FPPA; b) (l * , w* , h * ) =(32.0000, 25.5894,

75.2637) and F (u * )  61630.6754, starting from the feasible point found by the algorithm given in
[17]. One starting point is used, time limit is 10 hours. Improvement of the value of objective
function in comparison to the result given in [17]: a) 17.45%; b) 25.42%




                                                                            T
                                                                          IP
                                                                        CR
                                                   US
                                                 AN
                    (a)                                                 (b)
        Fig.20 – Local optimal placement of polyhedra in Example 9: a) starting from the feasible
point found by FPPA; b) starting from the feasible point found by the algorithm given in [17].
                                              M


        Table 1 lists some examples presented in [13]. For each example the minimal volume of the
container found by our method is smaller than the best solution reported in [13].
                                ED




        Table 1. Comparison of our results to those in [13]
                    PT




    Problem          the best    the best       found by         found by         found by        found by
                    volume      time (sec.)     FPPA* +          FPPA* +          [17]** +        [17]** +
                   from [13]    from [13]      COMPOLY          COMPOLY         COMPOLY          COMPOLY
         CE




                                                 volume          time (sec.)       volume        time (sec.)
  20 from [17]       32550      26202.1         27432.64         34313.34         28106.64         5360.67
AC




  30 from [17]       48300      53741.5         41646.17         35289.34         40277.19        33008.89
  40 from [17]       61950      99952.0         53158.88         201501.5         55988.46       195051.51
  50 from [17]       77280      125210.6        68214.56         215144.55        61630.68       270654.84
  36 from [13]       12480      9637.5          10461.67         23023.12             –               –
        Note. In table 1: * – a starting feasible point found by FPPA; ** – a starting feasible point found by
algorithm found in [17].


Example 10. We consider the collection of polyhedra of example 1 given in [13] and in Appendix A.
Figure 21 shows the local optimal placement of n=36 concave polyhedra, starting from the feasible
                                  ACCEPTED MANUSCRIPT
                                                                                                  32

point found by FPPA. The container has dimensions (l * , w* , h * ) =(21.5851, 19.8685, 24.3938) and

volume F (u * )  10461.67. We generate 5 starting points, time limit is 10 hours. Improvement of the
value of objective function is 16.18%.




                                                                      T
                                                                    IP
        Fig.21 – Local optimal placement of polyhedra in Example 10.




                                                                  CR
To show the effectiveness of the COMPOLY procedure, some tests were performed. In the example


                                                US
for N = 10 concave polyhedra from Appendix A, the average computational time per one local
extremum is: a) 1380 sec. without the use of the COMPOLY procedure; b) 283 sec. using the
COMPOLY procedure. The number of variables and inequalities is: a) 1791 and 7934 without the use
                                              AN
of the COMPOLY procedure; 626 and 3086 using the COMPOLY procedure at the last iteration.
In Example 6 for N=20 concave polyhedra, the average computational time per one local extremum is:
                                         M


a) 75026.31 sec. without the use of the COMPOLY procedure; b) 4980.74 sec. using the COMPOLY
procedure. The number of variables and inequalities is: a) 7471 and 30916 without the use of the
COMPOLY procedure; 1334 and 8028 using the COMPOLY procedure at the last iteration.
                           ED




In Example 7 for N=30 concave polyhedra a local minimum has not been found within the time limit
                  PT




of 72 hours without using of the COMPOLY procedure. The average computational time per one local
extremum is 35289.34 sec. using the COMPOLY procedure.
        CE




7. Conclusions and future work
We derive radical free adjusted quasi phi-functions to describe non-overlapping constraints for
AC




concave polyhedra and use adjusted phi-functions to describe containment constraints. These tools
take into account continuous rotations of polyhedra and minimal allowable distances between objects.
We introduce an exact mathematical model for the optimal polyhedron packing problem as a
nonlinear programming problem with smooth functions. Our approach involves a fast starting point
algorithm. We also propose the COMPOLY procedure to search for “good” local optimal solutions. It
can be used as a compaction algorithm, starting from a feasible point found by any algorithm
published before. The COMPOLY procedure allows us to reduce computational costs (time and
memory) considerably. This reduction is of a paramount importance, since we deal with nonlinear
optimisation problems. Our results on new instances and instances from the literature show our
                                   ACCEPTED MANUSCRIPT
                                                                                                    33
approach has superior performance. In the near future, we intend to apply our methodology to pack
arbitrary polyhedra into different shaped containers (a sphere, a cylinder, a polytope, a spheroid, an
ellipsoid) with different objectives (e.g., maximum of the space usage) and additional constraints
(e.g., behavior constraints).

References
    1. Bennell, J., Oliveira, J. (2008). The geometry of packing problems:A tutorial.European
        Journal of Operational Research184:397–415.
    2. Chazelle, B., Edelsbrunner, H., Guibas, L. J. (1989). The complexity of cutting complexes.
        Discr. & Comput. Geom., 4(2), 139–181. DOI: 10.1007/BF02187720.




                                                                         T
    3. Chen, E. R., Klotsa, D., Engel, M., Damasceno, P. F., Glotzer, S. C. (2014). Complexity in




                                                                       IP
        surfaces    of   densest   packings   for   families   of   polyhedra.   Phys   Rev   X   4(1),
        DOI:10.1103/PhysRevX.4.011024.




                                                                     CR
    4. Chernov, N., Stoyan, Y., Romanova, T. (2010). Mathematical model and efficient algorithms
        for object packing problem. Comput. Geom.: Theory and Appl., 43(9), 535–553.
        DOI:10.1016/j.comgeo.2009.12.003.
                                                 US
    5. Egeblad, J., Nielsen, B. K., Brazil, M. (2009). Translational packing of arbitrary polyhedra.
        Comp. Geom., 42(4), 269–288. DOI:10.1016/j.comgeo.2008.06.003.
                                               AN
    6. Fasano, G. A. (2013). Global Optimisation point of view for non-standard packing problems.
        J. Glob. Optim., 55(2), 279–299. DOI: 10.1007/s10898-012-9865-8.
                                        M


    7. Fischer, K., Gärtner, B. and Kutz, M. (2003). Fast Smallest-Enclosing-Ball Computation in
        High Dimensions. Algorithms - ESA 2003, 2832, 630–641. DOI:10.1007/978-3-540-39658-
        1_57.
                                ED




    8. Galrão, R. A., Oliveira J. F., Gonçalves J. F., Lopes M. P. (2016) A container loading
        algorithm with static mechanical equilibrium stability constraints. Transportation Research,
                   PT




        (Part B), 91, 565-581. DOI: 10.1016/j.trb.2016.06.003.
    9. Gomes, A. Miguel Irregular Packing Problems: Industrial Applications and New Directions
         CE




        Using Computational Geometry. (2014) Paper in special issue on “Cutting and Packing". Vol
        11 | Part 1, 378-383. DOI: 10.3182/20130522-3-BR-4036.00113.
    10. Kallrath, J. (2009). Cutting Circles and Polygons from Area-Minimizing Rectangles. Journal
AC




        of Global Optimization, 43(2), 299–328. DOI: 10.1007/s10898-007-9274-6.
    11. Korte, A. C. J., Brouwers H. J. H. (2013). Random packing of digitized particles. Powder
        Techn., 233, 319–324. DOI: 10.1016/j.powtec.2012.09.015.
    12. Li, S. X., Zhao, J., Lu, P., Xie, Y. (2010). Maximum packing densities of basic 3D objects.
        Chin. Scien. Bull., 55(2), 114–119. DOI: 10.1007/s11434-009-0650-0.
    13. Liu, X., Liu, J., Cao, A., Yao, Z. (2015). HAPE3D – a new constructive algorithm for the 3D
        irregular packing problem. Frontiers of Information Technology & Electronic Engineering,
        16(5), 380–390. DOI: 10.1631/FITEE.1400421.
    14. Pankratov, A., Romanova, T., Chugay, A. (2015). Optimal packing of convex polytopes using
                               ACCEPTED MANUSCRIPT
                                                                                                 34
    quasi phi-functions. Journal of Mechanical Engineering, 18 (2), 55-64.
15. Smeets, B., Odenthal, T., Vanmaercke, S., Ramon, H. (2015). Polygon-based contact
    description for modeling arbitrary polyhedra in the Discrete Element Method. Computer
    Methods      in      Applied   Mechanics      and    Engineering,       290,    277-289.    DOI:
    10.1016/j.cma.2015.03.004.
16. Stoyan, Y., Chugay, А. (2012). Mathematical modeling of the interaction of non-oriented
    convex polyhedra. Cyber. and Sys. Anal.,48 (6), 837–845. DOI: 10.1007/s10559-012-9463-2.
17. Stoyan, Y. G., Gil, N. I., Pankratov, A. V., et al., (2004). Packing Non-convex Polyhedra into
    a Parallelepiped. Technische Universitat Dresden.




                                                                    T
18. Stoyan, Y., Gil, N., Scheithauer, G., Pankratov, A., Magdalina, I. (2005). Packing of convex




                                                                  IP
    polyhedra     into    a   parallelepiped.   Optimisation,   54   (2),     215    –   235.   DOI:
    10.1080/02331930500050681.




                                                                CR
19. Stoyan, Y., Pankratov, A., Romanova, T. (2016). Quasi phi-functions and optimal packing of
    ellipses. J. of Glob. Optim., 65 (2), 283–307. DOI: 10.1007/s10898-015-0331-2.
20. Stroeven, P. and He, H. (2013). Packing of non-spherical aggregate particles by DEM.

                                              US
    Advances in Cement and Concrete Technology in Africa, Uzoegbo, H.C. and Schmidt, W.
    (Eds.) BAM Fed. Inst. Mat. Test., Berlin: 809-816.
                                            AN
21. Tasios, N., Gantapara, A. P., Dijkstra M. (2014). Glassy dynamics of convex polyhedra. The
    Journal of Chemical Physics. 141: 224502. PMID 25494755 DOI: 10.1063/1.49029922.
22. Torquato, S., Jiao, Y. (2009). Dense polyhedral packings: Platonic and Archimedean solids.
                                     M


    Phys. Rev., 80, 041104. DOI: 10.1103/PhysRevE.80.041104.
23. Wachter, A., Biegler, L. T. (2006). On the implementation of an interior-point filter line-
                          ED




    search algorithm for large-scale nonlinear programming. Math. Program., 106 (1), 25–57.
    DOI: 10.1007/s10107-004-0559-y.
24. Wаscher, G., Hauner, H., Schumann, H. (2007). An improved typology of cutting and
                PT




    packing problems. Eur. J. Oper. Res., 183(3), 1109–1130. DOI: 10.1016/j.ejor.2005.12.047.
    CE




                      APPENDIX A: DATA FOR EXAMPLES IN SECTION 6

    1. DATA FOR CONVEX POLYHEDRA
AC




    Data for Example 1

    We consider 7 types of covex polyhedra K1, K2, K3, K4, K5 , K6, K7 (Fig. A1).




                Fig. A1 – Types of convex polyhedra      , i=1,…,7 in Example 1.
                                      ACCEPTED MANUSCRIPT
                                                                                                              35
         Vertex coordinates of polyhedron K1:
{(xj,yj,zj), j=1,2,…,9}={(3,6,0), (3,6,8), (3,0,8), (3,0,0), (0,6,0), (0,6,8), (0,0,8), (0,0,0), (5,3,4)}
         Vertex coordinates of polyhedron K2:
{(xj,yj,zj), j=1,2,…,4}={(8,0,-4), (-3,4,-4), (6,2,10), (0,0,-4)}
         Vertex coordinates of polyhedron K3:
{(xj,yj,zj), j=1,2,…,7}={(3,0,-4), (3,4,-4), (3,0,8), (0 4,-4), (0,4,8), (0,0,8), (0,0,-4)}
         Vertex coordinates of polyhedron K4:
{(xj,yj,zj), j=1,2,…,10}={(2,0,0), (1,2,-4), (2,4,0), (-1,4,0), (-1,0,0), (2,0,7), (2,4,7), (1,2,12), (-1,4,8),
(-1,0,8)}




                                                                                T
         Vertex coordinates of polyhedron K5:




                                                                              IP
{(xj,yj,zj), j=1,2,…,11}={(2,-4,0), (2,4,0), (1,2,6), (1,-2,6), (0,4,0), (-2,0,0), (-1,2,6), (0,-4,0), (2,0,-4),
(0,0,-4), (2,4,-4)}




                                                                            CR
         Vertex coordinates of polyhedron K6:
{(xj,yj,zj), j=1,2,…,6}={(4,7,0), (4,7,7), (6,0,7), (6,0,0), (0,0,0), (0,0,7)}
         Vertex coordinates of polyhedron K7:

                                                      US
{(xj,yj,zj), j=1,2,…,10}={(4,-4,2), (4,-4,-1), (2,0,-4), (1,5,-4), (1,5,5), (3,0,5), (0,0,5), (0,0,-4), (-2,-5,-
1), (-2,-5,2)}
                                                    AN
         Data for Example 5

         We consider 5 types of covex polyhedra K1, K2, K3, K4, K5 (Fig. A2).
                                             M
                               ED
                      PT




                      Fig. A2 – Types of convex polyhedra         , i=1,2,…,5 in Example 5.
         CE




         Vertex coordinates of polyhedron K1:
{(xj,yj,zj), j=1,2,…,14}={(4,2,0), (2,7,0), (0,3,3), (-11,8,-18), (1,5,-8), (3,0,-8), (-1,1,-5), (-14,10,-10),
(-4,3,3), (-2,7,0), (-10,6,-10), (0,-1,3), (-10,10,-10), (4,-2,0)}
AC




         Vertex coordinates of polyhedron K2:
{(xj,yj,zj), j=1,2,…,16}={(3,-4,8), (3,-4,0), (3,6,0), (3,6,8), (-1,6,0), (-1,6,8), (-1,-4,8), (-5,-1,-1), (-5,-1,
7), (-5,5,7),(-5,5,-1), (-1,-4,0), (2,-2,-8), (-2,-2,-8), (-2,4,-8), (2,4,-8)}
         Vertex coordinates of polyhedron K3:
{(xj,yj,zj), j=1,2,…,10}={(8,0,10), (8,0,3), (6,5,0), (4,10,0), (4,10,13), (6,5,13), (2,5,13), (2,5,0),
(0,0,3), (0,0,10)}
         Vertex coordinates of polyhedron K4:
{(xj,yj,zj), j=1,2,…,15}={(7,0,8), (7,8,8), (7,4,12), (7,0,12), (0,8,8), (0,8,12), (4,8,12), (0,4,8), (0,4,12),
(4,0,12), (6,2,0), (3,2,0), (3,6,0), (6,6,0), (4,0,8)}
                                      ACCEPTED MANUSCRIPT
                                                                                                           36
         Vertex coordinates of polyhedron K5:
         {(xj,yj,zj), j=1,2,…,11}={(2,-4,0), (2,4,0), (1,2,4), (1,-2,4), (-1,-2,-8), (1,2,-8), (1,-2,-8), (0,-

4,0), (-4,0,0), (-3,2,4), (-2,4,0)}

         2. DATA FOR CONCAVE POLYHEDRA

         Data for Examples 2- 4 and Examples 6 - 9

         We consider 10 types of concave polyhedra (Fig.A3)




                                                                            T
                                                                          IP
                                                                        CR
                                                    US
                                                  AN
                         Fig. A3 – Types of concave polyhedra         , q=1,2,…,10.

         Each type of concave polyhedron is presented as a union of convex polyhedra given by the
                                          M


related collection of vertices in the local coordinate system of the appropriate concave polyhedron.
Figure A4 shows decomposition of concave polyhedron             with convex polyhedrons Ki, i=1,2,3,4.
                              ED




                                                                          K4
                                                                          K1
                    PT




                                                                   K2
                                                                                K3
                                8
         CE




 Fig. A4 – Concave polyhedron           and convex polyhedrons Ki, i=1,2,3,4 that form the polyhedron.
AC




         We give here input data of vertices of convex polyhedrons that form concave polyhedra by
two lists: list1 of vertex coordinates and list 2 of numbers of vertices (with respect to the list1) that
define a collection of vertices of convex polyhedra that form appropriate concave polyhedron.


         Remark. List 1 involves vertices of a concave polyhedron and, in general, additional vertices
that appear as outcomes in construction of decomposition of the concave polyhedron with convex
polyhedra.
         List 1 of vertex coordinates (xj,yj,zj), j=1,2,…,mq for description of concave polyhedra:
                                       ACCEPTED MANUSCRIPT
                                                                                                               37
            : {(xj,yj,zj), j =1,2,…,28}={(0,0,0), (8,0,0), (8,0,20), (0,0,20), (0,1,0), (0,1,20), (8,1,20),

(8,1,0), (8,18,0), (8,18,20), (7,18,0), (7,18, 20), (7,0,20), (8,17,0), (0,17,0), (0,17,20), (8,17,20),

(1,18,20), (0,18,20), (1,0,20), (1,0,0), (1,18,0), (0,18,0), (0,18,1), (0,0,1), (8,0,1), (8,18,1), (7,0,0)};

            :{(xj,yj,zj), j=1,2,…,12}={(0,0,0), (4,0,0), (4,8,0), (0,8,0), (4,0,8), (4,8,8), (0,8,8), (0,0,8),

(2,-8,4), (2,4,-10), (2,18,4), (2,4,19);

            :{(xj,yj,zj), j=1,2,…,21}={(0,0,0), (4,0,0), (4,15,0), (0,15,0), (4,0,5), (4,15,5), (0,15,5),

(0,0,5), (3,4,0), (1,4,0), (1,10,0), (3,10,0), (2,7,-6), (4,4,5), (0,4,5), (2,2,16), (4,6,5), (0,6,5), (0,12,5),




                                                                              T
(4,12,5), (2,9,12)};




                                                                            IP
            :{(xj,yj,zj), j=1,2,…,10}={(2,-3,0), (-2,-3,0), (-2,3,0), (2,3,0), (0,0,9), (0,0,4), (2,-5,14),




                                                                          CR
(2,5,14), (-2,5,14), (-2,-5,14)};

            :{(xj,yj,zj), j=1,2,…,12}={(0,0,0), (3,0,0), (3,-4,0), (3,-4,5), (0,0,5), (3,0,5), (3,0,3), (0,4,3),

(0,4,9), (3,0,9), (0,0,9), (0,0,3)};
                                                     US
            : {(xj,yj,zj), j=1,2,…,24}={(0,0,0), (4,0,0), (4,0,16), (0,0,16), (0,1,0), (4,1,0), (4,1,16),
                                                   AN
(0,1,16), (0,18,16), (4,18,16), (4,18,0), (0, 18,0), (0,17,16), (4,17,16), (4,17,0), (0,17,0), (4,0,2),

(4,18,2), (0,18,2), (0,0,2), (4,0,14), (4,18,14), (0,18,14), (0,0,14)};
                                           M


            : {(xj,yj,zj), j=1,2,…,22}={(3,0,0), (3,4,0), (0,4,0), (3,0,10), (3,4,10), (0,4,10), (5,0,8),
                              ED




(5,4,8), (5,4,4), (5,0,4), (3,0,8), (3,4,8), (3,4,4), (3,0,4), (2,4,6), (2,4,10), (1,9,8), (0,4,6), (2,4,4),

(0,4,4), (2,4,0), (1,8,2)};
                    PT




            : {(xj,yj,zj), j =1,2,…,7}={(0,0,0), (12,0,8), (-8,8,8), (-8,-8,8), (0,-4,12), (0,4,12), (-4,0,12)};

            : {(xj,yj,zj), j =1,2,…,7}={(0,0,0), (12,0,-8), (-8,8,-8), (-8,-8,-8), (0,-4,-12), (0,4,-12), (-4,0,-
         CE




12)};

             : {(xj,yj,zj q), j =1,2,…,5}={(0,0,0), (0,-4,4), (0,4,4), (16,0,16), (-16,0,16)}.
AC




         List 2 of vertex numbers of the corresponding convex polyhedron Ki for each concave

polytope     , q=1,2,…,10:

            = K1 U K2 U K3 U K4 U K5

         K1:{3,10,9,2,13,12,11,28},        K2:{2,9,10,19,23,14,15,16,17},        K3:{18,20,21,22,1,23,19,4},

K4:{1,2,3,4,5,6,7,8}, K5:{1,2,9,23, 24,25,26,27};

            = K1 U K2 U K3 U K4 U K5
                                             ACCEPTED MANUSCRIPT
                                                                                                                38
                   : K1:{1,2,5,8,9}, K2:{5,6,7,8,12}, K3:{3,4,6,7,11}, K4:{4,3,2,1,10}, K5:{1,2,3,4,5,6,7,8};

                   = K1 U K2 U K3 U K4

                   : K1:{1,2,3,4,5,6,7,8}, K2:{5,8,15,14,16}, K3:{17,18,19,20,21}, K4:{9,10,11,12,13};

                   = K1 U K2

                   : K1:{1,2,3,4,5}, K2:{6,7,8,9,10};

                   = K1 U K2

                   : K1:{1,2,3,4,5,6}, K2:{7,8,9,10, 11,12};




                                                                                    T
                   = K1 U K2 U K3 U K4




                                                                                  IP
                   :       K1:{1,2,3,4,5,6,7,8},       K2:{9,10,11,12,13,14,15,16},   K3:{17,18,19,20,1,2,11,12},




                                                                                CR
        K4:{21,22,23,24,3,4,9,10};

                   = K1 U K2 U K3 U K4


                                                              US
                   : K1:{1,2,3,4,5,6}, K2:{7,8,9,10,11,12,13,14}, K3:{15,16,17,18,6}, K4 :{19,20,21,22,3};

                   = K1 U K2 U K3 U K4
                                                            AN
                   : K1:{1,5,6,7}, K2:{1,4,5,7}, K3:{1,2,5,6}, K4:{1,3, 6,7};

                   = K1 U K2 U K3 U K4
                                                   M


                   : K1:{1,5,6,7}, K2:{1,4,5,7}, K3:{1,2,5,6}, K4:{1,3,6,7};
                                      ED




                       = K1 U K2

                       : K1:{1,2,3,4}, K2:{1,2,3,5}.
                             PT




                APPENDIX B. FORMING INDEX SET 1k IN COMPOLY ALGORITHM

Let three polyhedra are placed inside the container  k at k-th iteration of COMPOLY algorithm (Fig. B1)
                CE
       AC




         Fig. B1 – Illustration to construction of the index set 1k at k-th iteration of COMPOLY algorithm.
                                               ACCEPTED MANUSCRIPT
                                                                                                                                               39
For the example the index set  defined by (7) has the form:
  {(1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2,5), (2, 6), (3, 5), (3, 6), (4, 5), (4, 6)}.

Firstly we define the index set 1kS (Fig B1a):
                         S ai S a j
1kS  {(i, j )  :                 (v1(k 1) , v 2(k 1) )  0}  {(1, 3), (1, 4), (2, 3), (2, 4)}.

It means that only spheres S1 and S 2                        for concave polyhedra                          and          have nonempty

intersection, i.e.  S1S 2 (v1( k 1) , v 2( k 1) )  0 , and therefore it is sufficient to consider only possible

intersection of convex polyhedra: K1 and K 3 , K1 and K 4 , K 2 and K 3 , K 2 and K 4 .




                                                                                                  T
                                                                                           ik  kj
Then we form the index set 1k (Fig B1b): 1k  {(i, j ) 1kS :                                     (v a( k 1) , v a( k 1) )  0}  {(1, 4)}.




                                                                                                IP
                                                                                                          i          j


It means that only individual containers 1k and  k4 for convex polyhedra K1 and K 4 have




                                                                                              CR
                                              k     k
nonempty intersection, i.e. 1  4 (v1(k 1) , v2(k 1) )  0 and therefore we need to include in our

subproblem only quasi phi-function for polyhedra K1 and K 4 .
                                                                 US
         APPENDIX C. SEARCHING FOR FEASIBLE AUXALIRY VARIABLES IN THE
                                                               AN
FAPA ALGORITHM

On the seventh step of the COMPOLY algorithm we find values of the vector of auxiliary variables
                                                        M


u P , employing the FAPA algorithm. Figure C1 illustrates two cases to derive a vector of feasible

parameters u P of a separating plane: a) for two spheres S i and S j if int S i                                      int S j   ; for two
                                      ED




convex polyhedra K i and K j if int S i                   int S j  .
                      PT
          CE
AC




                                      (a)                                           (b)

        Fig. C1 – Illustration to 7th step at the k-th iteration of COMPOLY algorithm:

                                  a) S i          S j   ; b) int S i    int S j  .
                                 ACCEPTED MANUSCRIPT
                                                                                                  40

For case a) we use trivial geometrical calculations to find u P ; for case b) we solve NLP subproblem

(15) to find a nonnegative value of  that corresponds to the problem of searching for a nonnegative
value of a quasi phi-function of two convex polyhedra K i and K j




                                                                        T
                                                                      IP
                                                                    CR
                                                US
                                              AN
                                       M
                           ED
                  PT
        CE
AC
