         Packing Equal Spheres by Means of the Block
                 Coordinate Descent Method

                G. Yaskov[0000-0002-1476-1818], A. Chugay[0000-0002-4079-5632]

    A. Pidgorny Institute of Mechanical Engineering Problems of the National Academy of
              Sciences of Ukraine, 2/10 Pozharsky St., 61046 Kharkiv, Ukraine
              yaskov2004@gmail.com, chugay.andrey80@gmail.com




       Abstract. The paper deals with the problem of packing a large number of equal
       spheres into a container of spherocylindrical shape with a cylindrical prohibi-
       tion area which arises in chemical industry. The problem is presented as a
       mathematical programming problem on the ground of the Stoyan’s phi-
       functions method. Solving the problem is reduced to solving a sequence of non-
       linear programming problems making use of the block coordinate descent
       method and analysis of Lagrange multipliers to realize sequential addition of
       spheres. Numerical examples for up to two millions of spheres are given.

       Keywords: packing, sphere, spherocylinder, catalyst, optimization




1      Introduction

Packing spheres consists to arrange equal or non-equal non-overlapping spheres with-
in a containing space or into a larger three-dimensional domain (container). A typical
objective is to fill as much of the space (container) as possible. The optimization
sphere packing problem is studied in discrete and computational geometry.
   C.F. Gauss proved in 1831 [1] that the hexagonal lattice sphere-packing configura-
tion has the highest density amongst all possible lattice packings with the asymptotic
value  /(3 2 ) . Given a bounded container, the maximum packing density decreases
depending on the ratio of the sphere diameter to the container sizes.
   The sphere packing problems are of interest in studying structure of crystals [2],
liquids [3], glassy materials [4], catalysts and fuel elements [5-8], etc. The packing
density of equal spheres is a significant factor in the study of processes in thermal
heat exchangers, chemical and nuclear reactors [9]. Well-known are applications of
packing spheres in medicine and engineering.
   The aim of the paper is to develop a method of dense random packing a large num-
ber of equal spheres into a composed container being a geometric model of a chemi-
cal reactor.

  Copyright © 2020 for this paper by its authors. Use permitted under Creative
Commons License Attribution 4.0 International (CC BY 4.0).
2       Problem Statement

Let there be spheres Si , i  I N  {12,… N } with radius r and a container C which
is a specific composition of cylinders C1 , C2 and a spherical segment S0 (Fig. 1):

                                      C   C1  S0  \ int C2

where cC2  is the compliment of C2 , int   is the interior of the set,

                                                                          
                        C1  x, y, z   R 3 | x 2  y 2  R 2 , 0  z  H ,


                          
                   C2   x, y, z   R 3 | x 2  y 2  rc2 ,  R  z   R  h , 
                    
              S0  x, y, z   R 3 | x 2  y 2  z 2  R 2 ,  R  z  min{0, H } ,  
R  0 is radius of S0 and of base of C1 , H is height of C1 , h  0 is height of C2
and rc  0 is radius of its base,  R  h  H .
   The bottom of C is of spherocylindrical shape and the top of C is bounded above
by the plane z  H . In general, H can be negative. In this case C1   .




                                          R                C1
                                                                      H      Si

                                                                       2r
                                                                 S0
                                      R
                                                 rc
                                                        C2        h


                        Fig. 1. Container and a sphere (catalyst) to be packed

   The problem is formulated as follows: pack the maximal number n * of spheres
from the set Si , i  I N into the container C without overlappings and calculate their
center coordinates vi*   xi* , yi* , zi*  , i  12,… n* .
3        Literature review

A review of numerical simulation methods to solve sphere packing problems is pre-
sented in [8]. A major part of investigations make use of the Monte-Carlo method
[9,10], Discrete Element Models [11] and sequential addition techniques [6,12,13].
The papers consider as a rule cylindrical or rectangular containers.
   Mueller [13] applies a sequential addition technique to pack equal spheres into a
right circular cylinder and develops the packing algorithm based on a dimensionless
packing parameter. The algorithm yields a layerwise structure of the desired number
of spheres. The spheres are packed in stable positions under gravity with the maxi-
mum dimensionless packing parameter.
   Catalytic reactors (packed bed reactors) are used in chemical industry [14]. Reac-
tors with a single adiabatic bed are traditionally used in either exothermic or endo-
thermic reactions. Catalyst pellets have the shape of sphere or cylinder. Packed beds
of catalysts should avoid unstable and inefficient arrangements. The packing density
of catalysts influences on chemical reactions.
   The concept of phi-functions and quasi phi-functions is known to be an efficient
tool for mathematical modeling of 3D packing problems for geometrical objects [15-
17]. Powerful tools to solve problems of packing geometric objects of various spatial
shapes are proposed in [18-24].
   Paper [19] proposes a method of solving the sphere packing problem based on
homothetic transformations of spheres. The radii of the spheres are assumed to be
variable and the auxiliary problems are solved, the sum of the sphere volumes being
maximized. The optimization process continues until the sphere radii reach their
original values. The method allows to jump from one local extremum to another.
   In this paper we consider a method to obtain a dense random packing of a large
number of equal spheres into a composed container being a geometric model of the
catalytic reactor with a single adiabatic bed. The Stoyan’s phi-function method
[15,16] is applied to describe packing constraints. Solving the problem is reduced to
solving a sequence of nonlinear programming problems making use of the block co-
ordinate descent method [25] and analysis of Lagrange multipliers [26]. We realize
sequential addition of spheres. Groups of variables are formed by center coordinates
of spheres to be packed. A local minimum point is calculated for each group of vari-
ables.


4        Mathematical model

A mathematical model of the problem is presented as follows:
                                                N
                                   n*  max  i vi  s.t. v  G                 (1)
                                               i 1



where v  v1 , v2 ,..., v N   R 3 N , vi  xi , yi , zi   R 3 , i  I N ;
                                                           1 if Φ i vi   0,
                                         i vi   
                                                           0 otherwise;


                                                                   
                        G  {v  R 3 N :  ij vi , v j  0, i, j  I N , i  j} ;


                    ij  vi , v j    xi  x j    yi  y j    zi  z j   4r 2 ;
                                                       2                        2                   2




 i  vi  is a phi-function of Si and cint C  , c  and int() are the compliment and
the interior of the set () respectively;  ij  vi , v j  is a phi-function of Si and S j ,
i, j  I N , i  j .
   The inequality  i  vi   0 provides the sphere Si , i  I N , being within the con-
tainer and the inequality  ij  vi , v j   0 specifies non-overlapping the spheres Si and
S j , i, j  I N , i  j .
   The phi-function  i  vi  can be constructed according to [15]:

                                  Φi  0, vi   min Φ1i  vi  , Φ 2i  vi  ,

   where

          Φ1i  vi   max 1i  vi  ,  2i  vi  , Φ 2i  vi   max 1i  vi  , 2i  vi  ,


                               1i  vi   max 1i  vi  ,  2i  vi  , i  vi  ,


                1i  vi   H  zi ,  2i  vi   zi , i  vi   R  r  xi2  yi2 ,



                                             x  y  r    z  R  h  r ,
                                                                        2
                       1i  vi              2           2                                    2
                                               i           i        c               i




                                              x  y  r    z  R  r .
                                                                            2
                             2i  vi            2            2                           2
                                                   i           i        c               i



   The objective function  i  vi  is piecewise constant. The problem (1) is multiex-
tremum, all local maxima being non-strict due to the axial symmetry. The number of
non-linear inequalities is nn  1/2 .
5       Solution Method
The number of spheres that can be packed into the container C is not defined in ad-
vance. It is can be only evaluated making use of the maximum packing ratio
 /(3 2 )  0.74 [1] as an upper bound. If the number of spheres is up to 100, one can
adopt the method for packing spheres into a cylinder proposed in [19]. However, if
the dimension of the problem is large, then the sequential addition scheme is most
suitable to obtain a dense sphere packing.
    According to the scheme solving the problem (1) is reduced to solving a sequence
of problems. On the first step the sphere S1 from the set Si , i  I N is packed into C
being located at a position with the minimum value of z-coordinate. Then, the sphere
 S2 , i  I N is packed into C , the sphere S1 being immovable, and so on. The number
of the last sphere Sn* from the set Si , i  I N which can be packed into C gives an
evaluation of the maximum n * of the problem (1). The sequential addition scheme
can be realized by applying the block coordinate descent method [25].
   Let the spheres S1 , S2 ,..., Sk 1 be packed at the previous k  1 steps, the center co-
ordinates being vk*   xk* , yk* , zk*  , i  1, 2,..., k  1 respectively. Coordinates of the
sphere Sk form a group of variables at the step k :

                vk*  arg min  k  vk  , s.t. v k  G k  R 3 , k  1, 2 ,...,N ,         (2)

where  k  vk   zk ;

                                                            
               Gk  {vk  R 3 : Φ k vk   0, Φ jk v*j , vk  0, j  1,2,..., k  1} .     (3)

    We search for a local minimum point of the problem (2)–(3). If a feasible point of
the problem (2)–(3) for k  n * 1 cannot be found, then the solution of the previous
problem ( k  n * ) solved is a solution N  n0 of the problem (1).
    We indicate some peculiarities of the problem (2)–(3): the objective function
  k  vk   zk is linear and minima are reached at extreme points of the feasible region
Gk .
    The frontier of the feasible region Gk ( fr  Gk ) consists of points satisfying the
equations Φ jk  v*j , vk   0 , j  1, 2,..., k  1 , or Φ k  vk   0 :

                                                                 
                fr Gk   v   x, y, z   R 3 : v  T  Gk  , k  1, 2 ,...,N ,

where

                                   T  T0  T1  T2  ...  Tk 1 ,
                                              
                  T j  v  R 3 : Ф jk v *j , v  0 , j  1, 2,..., k  1 ,


                       T0  T01  T02  T03  T04  T05  T06 (Fig. 2).




                                                         T01

                                    T02                              T02

                                       T05         T06         T05


                                       T04                      T04
                                                                               T03


                                       Fig. 2. Illustration of T0


T02 and T04 lie on planes:

                                                                    
                 v  R 3 : z  H  r , x 2  y 2  R  r 2 if H  0,
          T01  
                                                                              
                  v  R 3 : z  H  r , x 2  y 2  R  r 2  H 2 otherwise,


                    if H   R  h  r ,
             T06  
                                                                          
                     v  R 3 : z   R  h  r , x 2  y 2  rc 2 otherwise.

T02 and T04 lie on cylindrical surfaces:

                       
                   v  R 3 : x 2  y 2  R  r 2 , 0  z  H - r if H  0,
            T02  
                                                                               
                    otherwise,


                   
            T03  v  R 3 : x 2  y 2  rc  r 2 ,

                           R  r 2  rc  r 2  z  min( R  h), H  r .
                                                                                     


T03 lies on spherical surface
                          
                   T03  v  R 3 : x 2  y 2  z 2  R  r 2 ,

                              R  r 2  rc  r 2  z  min0, H  r .
                                                                                

T05 lies on torus surface

                   if H   R  h,
                  
                  v  R 3 :  x 2  y 2  r   z  R  h) 2  r 2 ,
                                                2
                                          c
            T05                           
                  
                   x  y  rc ,- R  h  z  min R  h  r , H  r 
                       2     2    2
                                                                                       
                                                               otherwise.
                  

   The set of extreme points can be presented as
                                      k 1
                Ek  T02  T03    Ti  Tj  Tl   frGk , k  1,2 ,..., N .
                                   i , j ,l  0
                                   i  j l




  The set of local minima Lk , k  1, 2 ,...,N , consists of points of ( fr (G k ) whose
coordinate values are solutions either of the system:

                                   x 2  y 2  z 2  R  r 2 ,
                                    2
                                    x  y 2  rc  r 2

or the systems:

                   f i  0,
                  
                   f l  0, i, l , m  0,1,..., k  1, i  l  m, (i, l , m)  I .
                   f  0,
                   m

where f i , f l , f m are either Φ k  vk  or Φ jk  v*j , vk  , j  1, 2,..., k  1 ; the set I consists
of triples of indices for which the condition of minimum [26] is fulfilled.
   A sufficient condition of local minimum of the problem (2)–(3) is
 1  0,  2  0, 3  0 [26] where the Lagrange multipliers 1 ,  2 , 3 can be calcu-
lated by solving the following system of linear equations:
                                f i   fl             f m 
                                                            
                                xk    xk             xk 
                                                                1   0 
                                f i   fl             f m     
                                                             2  0 .
                                yk    yk             yk     
                                f                              3  1 
                                        fl             f m 
                                i                          
                                 zk   zk             zk 

    Thus, set
                                                 k 1
                        Lk   T03  T04          T  T  T   frG .
                                                              i   l   m       k
                                             i ,l , m  0
                                             i l  m
                                              i ,l , m I


  The number of local minima not belonging to the set is less than
2n(n  1)(n  2) / 6 .

    The solution strategy of the problems (2)–(3) consists of the following stages.

1. Random choice of an initial point of the feasible region Gk .
2. Movement to the frontier of Gk decreasing the objective.
3. Movement on the frontier of Gk to an extreme point of Gk decreasing the objec-
   tive.
4. Searching for an extreme point of Gk being a local minimum point of the problem
   (2)–(3).



6       Searching for a local minimum of subproblem

We consider a procedure to calculate a local minimum point of the problem (2)–(3).

1. A point vk0   xk0 , yk0 , zk0  such that (xk0 )2  ( yk0 )2  R 2 and zk0  H  rk is con-
   structed.
2. If vk0  Gk , then n*  k  1 is an approximate solution of the problem (1).
3. Otherwise ( vk0  Gk ), a point v1k   x1k , y1k , z1k    xk0 , yk0 , zk0  zq   frGk at which
    Sk touches frC or S p , p  1, 2,..., k  1 . The value zq , q  1, 2,..., is defined
    by bisection within the segment  0, R  H  .
4. If point v1k is a local minimum point, then set vk*  v1k and go to the next k .
5. Otherwise, let point v1k  Ti , i  0,1,..., k  1 . A point vk2   xk2 , yk2 , z k2   Ti  T j 
    is calculated where i  j  0,1,..., k  1 and zk2  z1k such that Sk touches frC
    and S j , j  1, 2,..., k  1 or Si and S j . To this end we solve the following sys-
    tems:


                                    f i  x, y, z   0,
                                   
                                    z  zk  zq , q  1, 2,...
                                             1

                                   
                                    ax  by  c,


   where the equation f i  x, y, z   0 describes the frontier of Ti and ax  by  c is an
    equation of a plane passing through the point v k 1  Ti . The value z q is defined by
    bisection within the segment 0, R  H  z1k  . If v k 2 is a local minimum point,
    then set vk*  vk2 and go to the next k .
 6. An      extreme      point      vk3   xk3 , yk3 , zk3   Ti  T j  Tl    is   calculated   where
    i  j  l  0,1,..., k  1 and z  z such that Sk touches frC and two spheres or
                                            3
                                            k
                                                  2
                                                  k

    three spheres. To this end we solve the following systems:


                                    fi  x, y, z   0,
                                   
                                     f j  x, y, z   0,
                                    
                                     z  zk  zq , q  1, 2,...,
                                             2




   where the equations f i  x, y, z   0 and f j  x, y, z   0 describe the frontiers of Ti
    and T j respectively. The value z q is defined by bisection within the segment
    0, R  H  zk2  . If vk3 is a local minimum point, then set vk*  vk3 and go to the step
    k 1.
 7. Otherwise ( 1  0 or  2  0 or  3  0 ) define i0  1, 2,3 such that
     i0  1 ,  i0   2 ,  i0   3 .
 8. If i  i0 , take i  j , j  l and vk2  vk3 and go to the item 6.
 9. If j  i0 , take j  l and vk2  vk3 and go to the item 6.
10. If l  i0 , take vk2  vk3 and go to the item 6.

    A special strategy of verifying the feasibility during optimization process is pro-
 posed. The strategy forms a list of inactive constraints analyzing distances from the
 sphere to be packed to the spheres already packed. This allows to essentially decrease
 the computational complexity of the algorithm.
    To improve the value of the objective of the problem (2)–(3) we realize the
 multistart method on each step and choose the best local minimum.
7      Experimental results and discussion

In order to numerically test the packing method proposed a software is developed.
Several examples with up to 2 million spheres are calculated. The Open Graphics
Library for visualization of the optimization process.
   Example 1. The metric characteristics of the container and the spheres to be packed
are R  250 , rc  80 , H  0 , h  250 and r  15 . We use 30 starting points for
each sphere. The number of spheres packed is n*  1017 (Fig. 3). The runtime is 1
sec.




                            Fig. 3. Illustration of Example 1


  Example 2. The metric characteristics are R  250 , rc  80 , H  120 , h  80
and r  5 . 30 starting points are chosen for each sphere. The number of spheres
packed is n*  9696 (Fig. 4). The runtime is 20 sec.




                            Fig. 4. Illustration of Example 2
  Example 3. The metric characteristics are R  250 , rc  50 , H  0 , h  270 and
r  2 . 30 starting points are chosen for each sphere. The number of spheres packed is
n*  539778 (Fig. 5). The runtime is 1 h 20 min.




                            Fig. 5. Illustration of Example 3

   Example 4. The metric characteristics are R  250 , rc  80 , H  10 , h  80
and r  1.25 . One local minimum is calculated for each sphere. The number of
spheres packed is n*  2 063 007 . The runtime is about 2 h.
   The large-dimension problem reduces to solving a sequence of subproblems by
means of the block coordinate descent method. The multistart method allows to
choose a better local position for each sphere, thus increasing the total packing den-
sity.
   As experimental results show (see Fig.4 and Fig.5) the spheres form regular struc-
tures along the packing domain frontier (the container wall).
   It is obvious that the packings obtained in the examples do not, in general, corre-
spond to local minimum points of the problem minimizing the height of the filled part
of the container when all the spheres are moveable.


8      Conclusion

The problem of packing equal sphere into a bounded container is considered in the
paper.
   The method suggested allow to solve the problem of large dimension due to apply-
ing the block coordinate descent method which allow to reduce solving the problem to
a sequence of non-linear programming problems.
   The optimization method realizes search of a frontier point of the feasible region,
an extreme point and movement to a local minimum point. Choice of descent direc-
tion is defined by analyzing Lagrange multipliers of active constraints.
   Numerical examples show effectiveness of the method for up to two millions equal
spheres.
   The Stoyan’s phi-function method allows to adopt the developed method to pack
spheres into containers of arbitrary spatial shapes.
   The method can be also extended to pack unequal spheres.


References
 1. Gauss, C. F.: Untersuchungen über die Eigenschaften der positiven ternären quadratischen
    Formen von Ludwig August Seber, Gôttingische gelehrte Anzeigen (1831)
 2. Frenkel, D.: Computer simulation of hard-core models for liquid crystals. Computer Phys-
    ics Communications, vol. 44(3), pp. 243–253 (1987) doi: 10.1016/0010-4655(87)90079-8
 3. Bernal, J.A.: Geometrical Approach to the Structure Of Liquids. Nature 183, pp. 141–147
    (1959) doi: 10.1038/183141a0
 4. German, R.M.: Particle packing characteristics. Metal Powder Industries Federation, NJ
    (1989)
 5. Gan, Yi., Kamlah, M., Reimann, J.: Computer Simulation of Packing Structure in Pebble
    Beds. Fusion Eng. Des. 85(10-12), pp. 1782–1787 (2010) doi: 10.1016/j.fusengdes.2010.
    05.042
 6. Mueller, G.E.: Radial porosity in packed beds of spheres. Powder Technol. 203, pp. 626–
    633 (2010) doi: 10.1016/j.powtec.2010.07.007
 7. Chigada, P.I.: Characterisation of flow and heat transfer patterns in low aspectratio packed
    beds by a 3D network-of-voids model. Chemical Engineering Research and Design 89, pp.
    230–238 (2011) doi: 10.1016/j.cherd.2010.05.002
 8. Burtseva, L., Valdez Salas, B., Werner, F., Petranovskii, V.: Packing of monosized spheres
    in a cylindrical container: models and approaches. Rev. Mex. Fís., vol. 61(1) pp. 20–27
    (2015)
 9. Abreu, C. R. A., Macias-Salinas, R., Tavares, F. W., Castier, M.: A Monte Carlo simula-
    tion of the packing and segregation of spheres in cylinders. Brazilian Journal of Chemical
    Engineering, vol. 16(4), pp. 395–405 (1999) doi: 10.1590/S0104-66321999000400008
10. Roozbahani, M.M., Huat, B.B.K., Asadi, A.: Effect of rectangular container's sides on po-
    rosity for equal-sized sphere packing. Powder technology 224, pp. 46-50 (2012) doi:
    10.1016/j.powtec.2012.02.018
11. Wensrich, C.M.: Boundary structure in dense random packing of monosize spherical parti-
    cles. Powder Technology, vol. 219, pp. 118–127 (2012) doi: 10.1016/j.powtec.2011.12.
    026
12. Magnico, P.: Hydrodynamic and transport properties of packed beds in small tube-to-
    sphere diameter ratio: pore scale simulation using an Eulerian and a Lagrangian approach.
    Chemical Engineering Science, vol. 58(22), pp. 5005–5024 (2003) doi: 10.1016/S0009-
    2509(03)00282-3
13. Mueller, G.E.: Numerically packing spheres in cylinders. Powder Technology 159,
    pp. 105–110 (2005) doi: 10.1016/j.powtec.2005.06.002
14. Major, A.: Modeling of a Catalytic Packed Bed Reactor and Gas Chromatograph Using
    COMSOL Multiphysics. Corpus ID: 18618192 (2009) https://www.semanticscholar.org/
    author/A.-Major/50519443
15. Stoyan, Y., Scheithauer, G., Romanova, T.: Mathematical modeling of interactions of pri-
    mary 3D geometric objects. Cybern Syst Anal 41, pp. 332-342 (2005) doi:
    10.1007/s10559-005-0067-y
16. Stoyan, Y., Scheithauer, G., Gil, M., Romanova, T.: Φ -function for complex 2D objects.
    4OR 2, pp.69-84 (2004) doi: 10.1007/s10288-003-0027-1
17. Stoyan, Y.G., Semkin, V.V., Chugay, A.M.: Modeling Close Packing of 3D Objects. Cy-
    bern Syst Anal 52, pp. 296-304 (2016) doi: 10.1007/s10559-016-9826-1
18. Stoyan, Y.G., Chugay, A.M.: Packing different cuboids with rotations and spheres into a
    cuboid. Advances in Decision Sciences, vol. 2014 (2014) doi: 10.1155/2014/571743
19. Stoyan, Y.G., Scheithauer, G., Yaskov, G.N.: Packing Unequal Spheres into Various Con-
    tainers. Cybern Syst Anal 52, pp. 419–426 (2016) doi: 10.1007/s10559-016-9842-1
20. Yaskov G., Romanova T., Litvinchev I., Shekhovtsov S.: Optimal Packing Problems:
    From Knapsack Problem to Open Dimension Problem. In: Vasant P., Zelinka I., Weber
    GW. (eds) Intelligent Computing and Optimization. ICO 2019. Advances in Intelligent
    Systems and Computing, vol 1072. Springer, Cham, pp. 671–678 (2020) doi: 10.1007/978-
    3-030-33585-4_65
21. Yakovlev, S.V.: The Method of Artificial Space Dilation in Problems of Optimal Packing
    of Geometric Objects. Cybern Syst Anal 53, pp. 725–731 (2017) doi: 10.1007/s10559-017-
    9974-y
22. Yakovlev, S., Kartashov, O., Korobchynskyi, K., Skripka, B.: Numerical Results of Vari-
    able Radii Method in the Unequal Circles Packing Problem. 2019 IEEE 15th International
    Conference on the Experience of Designing and Application of CAD Systems (CADSM),
    Polyana, Ukraine, pp. 1–4 (2019) doi: 10.1109/CADSM.2019.8779288
23. Yakovlev, S.: Configuration Spaces of Geometric Objects with Their Applications in
    Packing, Layout and Covering Problems. In: Lytvynenko V., Babichev S., Wójcik W.,
    Vynokurova O., Vyshemyrskaya S., Radetskaya S. (eds) Lecture Notes in Computational
    Intelligence and Decision Making. ISDMCI 2019. Advances in Intelligent Systems and
    Computing, vol 1020, Springer, Cham, pp. 122-132 (2020) doi: 10.1007/978-3-030-26474-
    1_9
24. Yaskov, G.: Methodology to solve multi-dimensional sphere packing problems. Journal of
    Mechanical engineering, vol. 22 (1), pp. 67-75 (2019) doi: 10.15407/pmach2019.01.067
25. Bertsekas, D.P.: Nonlinear Programming, 2nd ed., Athena Scientific, Belmont, MA (1999)
26. Gill, P.E., Murray, W., Wright, M.H.: Practical Optimization, Academic Press (1981)
