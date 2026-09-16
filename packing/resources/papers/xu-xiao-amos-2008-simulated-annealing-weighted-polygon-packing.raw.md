O tober 26, 2021                            23:46       Engineering Optimization         submission



                                            Engineering Optimization
                                            Vol. 00, No. 00, Month 200x, 113




                                                                       RESEARCH ARTICLE
                                                           Simulated Annealing for Weighted Polygon Pa king
                                                                       Yi-Chun Xua , Ren-Bin Xiaob and Martyn Amosc,†
                                                a
                                                 Institute of Intelligent Vision & Image Information, China Three Gorges University,
    arXiv:0809.5005v1 [cs.CG] 29 Sep 2008




                                                                                        China
                                             b
                                                Institute of System Engineering, Huazhong University of S ien e & Te hnology, China
                                               c
                                                 Department of Computing & Mathemati s, Man hester Metropolitan University, UK
                                                                     (Re eived 00 Month 200x; nal version re eived 00 Month 200x)

                                                      In this paper we present a new algorithm for a layout optimization problem: this on erns
                                                      the pla ement of weighted polygons inside a ir ular ontainer, the two obje tives being to
                                                      minimize imbalan e of mass and to minimize the radius of the ontainer. This problem arries
                                                      real pra ti al signi an e in industrial appli ations (su h as the design of satellites), as well as
                                                      being of signi ant theoreti al interest. Previous work has dealt with ir ular or re tangular
                                                      obje ts, but here we deal with the more realisti ase where obje ts may be represented as
                                                      polygons and the polygons are allowed to rotate. We present a solution based on simulated
                                                      annealing and rst test it on instan es with known optima. Our results show that the algorithm
                                                      obtains ontainer radii that are lose to optimal. We also ompare our method with existing
                                                      algorithms for the (spe ial) re tangular ase. Experimental results show that our approa h
                                                      out-performs these methods in terms of solution quality.



                                            1.       Introdu tion


                                            The      Layout Optimization Problem (LOP)                      on erns the physi al pla ement of in-
                                            struments or pie es of equipment in a spa e raft or satellite. Be ause these obje ts
                                            have mass, the system is subje t to additional                     onstraints (beyond simple Cartesian
                                            pa king) that ae t our solution. The two main                         onstraints that we handle in this
                                            paper are (1) the spa e o                 upied by a given          olle tion of obje ts (envelopment),
                                            and (2) the non-equilibrium (i.e. imbalan e) of the system. The rest of the paper is
                                            organized as follows: In Se tion 2 we rst present a detailed des ription of the prob-
                                            lem, and des ribe previous related resear h. In Se tion 3 we des ribe our algorithm,
                                            and in Se tion 4 we give the results of numeri al experiments.




                                            2.       The Layout Optimization Problem in Satellites


                                            The Layout Optimization Problem (LOP) was proposed by Feng                                   et al. (5) in 1999,
                                            and has signi ant impli ations for the                      ost and performan e of devi es su h as
                                            satellites and spa e raft. It               on erns the       two dimensional physi al pla ement of
                                            a       olle tion of   obje ts (instruments or other pie es of equipment) within a spa e-
                                              raft/satellite  abinet", or       ontainer. The LOP is demonstrably NP-hard (6). Early
                                            work on this problem (11, 13, 15, 17) almost always modeled obje ts as                               ir les in or-
                                            der to simplify the pa king pro ess. However, in real-world appli ations, obje ts are
                                            generally re tangular or polygonal in shape, and modeling them as                                 ir les leads to




                                             † Email: M.Amosmmu.a .uk

                                            ISSN: 0305-215X print/ISSN 1029-0273 online
                                               200x Taylor & Fran is
                                            DOI: 10.1080/0305215YYxxxxxxx
                                            http://www.informaworld. om
O tober 26, 2021   23:46     Engineering Optimization      submission

                   2

                   expensive wastage of spa e. We have re ently reported work on solving the re tan-
                   gular     ase (14), and here we report a new algorithm (based on a dierent approa h)
                   to solve the polygonal        ase.
                        We now briey introdu e related work on the pa king of irregular items. Dowsland
                   et al. use a so- alled "Bottom-Left" strategy to pla e polygonal items in a bin
                   (3), with items having xed orientations. Poshyanonda et al. (12) ombine geneti
                   algorithms with arti ial neural networks to obtain reasonable pa king densities.
                   In other related work, Bergin            et al. study the pa king of identi al re tangles in
                   an irregular     ontainer (1, 7). Burke and Kendall have applied simulated annealing
                   to translational polygon pa king (i.e., without rotations) (2). Other authors have
                   applied simulated annealing to solve the problem of rotational polygon pa king on
                   a    ontinuous spa e (8, 9).
                        Given the additional      onstraint that imbalan e of mass must be minimised, it is
                   di ult to see how these existing methods may be dire tly applied to the                           urrent
                   problem. In what follows we des ribe a new nonlinear optimization model for the
                   LOP, and then show how it may be solved using simulated annealing.




                   2.1.     Notation and Denitions
                   Here we des ribe the formal optimization model, by rst explaining our notation
                   for the representation of polygons. We then show how to quantify relations between
                   polygons (su h as distan e and degree of overlap), whi h are                       entral to the problem
                   of assessing the overall quality of a layout.


                   2.1.1.     Stru ture of a polygon
                        Suppose there are k polygons (1, 2, . . . , k) to be pa ked. The              stru ture of a polygon
                   in ludes both its     shape and its mass. We use str(i) to denote the initial stru ture
                   of a polygon, i:




                                          str(i) = (ni , mi , (r1 , r2 , ..., rni ), (θ1 , θ2 , ..., θni ))              (1)



                        where mi is the mass of polygon i, and ni is the number of verti es in the graph
                   representation of polygon i. The positions of the ni verti es are dened by two lists
                   of   polar oordinates. List (r1 , r2 , ..., rni ) denes the Eu lidean distan e from ea h of
                   the ni verti es to the polygon's            entre of mass, and list (θ1 , θ2 , ..., θni ) denes the
                   orientation of ea h of the ni verti es relative to the entre of mass. Figure 1 shows
                   how to dene the initial stru ture of a square with edge length 1; in Figure                        1 (a),
                   the shape's      entre of mass is lo ated at the shape                entre, whereas in Figure      1(b),
                   the     entre of mass is lo ated at one vertex. We dene the point of referen e of ea h
                   polygon as its      enter of mass, in order to simplify the notation.


                   2.1.2.     Radius of a polygon
                        The radius of polygon i is dened as the maximum of (r1 , r2 , ..., rni ):




                                                        r(i) = max{r1 , r2 , ..., rni }                                  (2)



                        With the polygon's       entre of mass at its own             entre, the       ir le with radius r(i)
                   denes the minimum-sized             ir le that      an   ompletely       over the polygon.
O tober 26, 2021   23:46    Engineering Optimization     submission

                                                                                                               3




                                        Figure 1. Illustration of the stru ture denition of polygons




                                               Figure 2. Illustration of the state of a polygon


                   2.1.3.    State of a polygon
                      We use Cartesian      oordinates to re ord the positions of the polygons, and set the
                     enter of the    ontainer (that is, the       ir le) as the original point. We use sta(i) to
                   denote the state of a polygon i:




                                                          sta(i) = (xi , yi , αi )                           (3)


                      where xi , yi is the position of the       entre of mass, and α denes a rotation angle.
                   Then with str(i) and sta(i), we           an draw a polygon, i, as in Figure         2.

                   2.1.4.    Distan e between two polygons
                      The distan e between two polygons is dened as the Eu lidean distan e between
                   their    entres of mass:



                                                             q
                                               dis(i, j) =       (xi − xj )2 + (yi − yj )2 )                 (4)



                   2.1.5.    Overlap between two polygons
                      If two polygons do not overlap, this measure is zero. If two polygons i and j
                   overlap at all, we measure this as:
O tober 26, 2021   23:46       Engineering Optimization     submission

                   4




                                                 Figure 3. The overlap fun tion is not ontinuous




                                               ove(i, j) = max{0, r(i) + r(j) − dis(i, j)}                                (5)



                   This measurement of overlap has                ertain    hara teristi s:


                   • In Equation (5), r(i) and r(j) are two onstants, therefore dis(i, j)                     an be dire tly
                        obtained by the positions of the two polygons.
                   • It is      lear that ove(i, j) ≥ 0. To satisfy the        non-overlapping onstraint, we should
                     minimize ove(i, j) to zero.
                   • ove(i, j) is not a ontinuous fun tion of the positions. As shown in Figure                            3,
                        when two squares with edge length 2 are adja ent on one side, their overlap is
                        zero, but when the left square is moved a little to the right, the overlap jumps"
                             √
                        to 2     2 − 2.

                        As ertaining overlap between two polygons is not a di ult problem in                          ompu-
                   tational geometry or          omputer graphi s. In this paper, we look at ea h edge of one
                   polygon in turn; if it is interse ted by any edge of another polygon, then an overlap
                   exists; otherwise, if one polygon is           ontained     within another, then learly an overlap
                   exists. So the as ertaining of overlap has                 omplexity O(mn), where m, n are the
                   number of edges of the two polygons.


                   2.1.6.      State of a layout
                        A layout X is dened as the           ombination of the states of k polygons:




                                                X = (x1 , y1 , α1 , x2 , y2 , α2 , ..., xk , yk , αk )                    (6)



                   2.1.7.      Radius of a layout
                        If (Xx , Xy ) denotes the position of the           entre of mass of a layout X , then



                                                           Pk                       Pk
                                                                 m i xi                     mi y i
                                                  Xx =      Pi=1
                                                              k
                                                                        , Xy =       Pi=1
                                                                                       k
                                                                                                     .                    (7)
                                                              i=1 mi                     i=1 mi


                        We dene the radius r(X) of a layout X as the longest Eu lidean distan e from
                   its     entre of mass to any of the verti es of the polygons. Be ause of the                     imbalan e
                       onstraint, we pla e the        entre of mass of the layout at the                 ontainer   enter, so
                   r(X) denes the minimum-sized                 ontainer.


                   2.1.8.      Overlap of a layout
                        The overlap of a layout is the sum of all overlaps between its polygons:
O tober 26, 2021   23:46     Engineering Optimization   submission

                                                                                                                 5



                                                               k
                                                               X k
                                                                 X
                                                    ove(X) =                  ove(i, j)                        (8)
                                                               i=1 j=1,j6=i


                   2.1.9.    Problem denition
                        From the denitions above, we obtain an un onstrained optimization problem:




                                               minimize f (X) = λ1 ove(X) + λ2 r(X)                            (9)


                        where λ1 , λ2 are two    onstants. Be ause the overlap fun tion ove(X) is not          on-
                   tinuous, f (X) is not      ontinuous. In general, the overlaps are extremely deleterious,
                   so λ1 should be set large enough to prevent their introdu tion. However, we note
                   that the     omputation does not introdu e overlaps when attempting to de rease the
                   radius of the layout at the nal stage of optimization, be ause of the dis ontinuous
                   of the ove fun tion.




                   3.      Simulated annealing algorithm


                   Simulated annealing (SA) is a probabilisti meta-heuristi that is well-suited to
                   global optimization problems (10). Annealing refers to the pro ess of heating then
                   slowly     ooling a material until it rea hes a stable state. The heating enables the
                   material to a hieve      higher internal energy states, while the slow ooling allows the
                   material more opportunity to nd an internal energy state           lower than the initial
                   state. SA models this pro ess for the purposes of optimization. A point in the
                   sear h spa e is regarded as a system state, and the obje tive fun tion is regarded
                   as the internal energy. Starting from an initial state, the system is perturbed at
                   random, moving to a new state in the neighbourhood, and a                   hange of energy ∆E
                   takes pla e. If ∆E <0, the new state is a                 downhill move), otherwise the
                                                                      epted (a
                                                                              (an uphill move), where T is
                                                                      −∆E
                   new state is a       epted with a probability exp(      )
                                                                      Kb T
                   the temperature at that time and Kb is Boltzmann's                     onstant. When the system
                   rea hes equilibrium, T is de reased. When the temperature approa hes zero, the
                   probability of an uphill" move be omes very small, and SA terminates.
                        Let t0 denote the initial temperature, imax denote the maximum number of itera-
                   tions, E(x) denote the energy fun tion, and emax denote the "stopping" energy.The
                   general pseudo- ode for simulated annealing may be written as follows:

                               Algorithm 1: Standard SA

                               set the initial state x and initial temperature t = t0 , let i = 0
                               while i < imax and E(x) > emax
                                       perturb x in its neighbourhood and get x
                                                                                           ′

                                       if E(x′ ) < E(x) then x = x′
                                       else x = x′ with probability exp( E(x)−E(x )        ′

                                                                             t      )
                                       de rease the temperature
                                       i =i+1
                               return x

                        The performan e of SA may be ae ted by several parameters: the initial temper-
O tober 26, 2021   23:46    Engineering Optimization     submission

                   6

                   ature t0 , the maximum number of iterations, imax, the stopping" energy, emax,
                   the stru ture of the neighbourhood, and the s hedule of           ooling. For a given prob-
                   lem, the values of these parameters should be          arefully sele ted.




                   3.1.     SA for polygon pa king
                   3.1.1.    Neighbourhood stru ture
                       In ea h iteration of SA, we perturb one polygon, thus obtaining a new layout, and
                   then de ide whether to a           ept or reje t the new layout by means of an evaluation.
                   In the ith iteration, the (i mod k)th polygon will be perturbed. Given an initial
                   radius R0 , whi h is large enough to          ontain the polygons, the neighbourhood for
                   polygon j is dened as:




                                                       imax
                                    xj , y j ∈ (                + 1.05) × R0 × random(−1, 1)             (10)
                                                   i − 2 × imax



                                                    imax
                                       αj ∈ (                + 1.05) × π × random(−1, 1)                 (11)
                                                i − 2 × imax

                       Equations (10) and (11) show that, at the beginning of the algorithm's exe ution,
                   the position of a polygon may vary by (−0.55R0 , 0.55R0 ), and its orientation may be
                   perturbed by (−0.55π, 0.55π ). This neighbourhood is large, and and the polygon         an
                   thus explore" more spa e. As the algorithm pro eeds, the neighbourhood be omes
                   in reasingly smaller. At the end of the algorithm's exe ution, the neighbourhood
                   shrinks to 0.05 times its original size, then SA          hooses the best solution in the
                   neighbourhood.


                   3.1.2.    Temperature de reasing
                       We use a simple rule to de rease the temperature: every cmax iterations, we let
                   t = d × t, where d < 1.

                   3.1.3.    Des ription of the algorithm
                       The detailed SA algorithm for polygon pa king is therefore des ribed as follows:


                              Algorithm 2: SA for the pa king problem

                              randomly generate an initial layout X . Let t = t0 , i = 0
                              while i < imax and f (X) > emax
                                      let j = (i mod k)
                                      randomly sele t xj , yj , αj by (10) and (11) and get new X
                                                                                                     ′

                                      if f (X ′ ) < f (X) then X = X ′
                                      else X = X ′ with probability exp( f (X)−f (X )  ′

                                                                               t      )
                                      if i mod cmax = cmax − 1 then t = d × t
                                      i =i+1
                              return x
O tober 26, 2021   23:46       Engineering Optimization      submission

                                                                                                                                7

                   Table 1. Four instan es with known optima
                   Instan e         k     R0     Stru ture
                                                                      √      √    √      √
                           1        5     2.3    str(i) = (4, 30, ( 210 , 210 , 210 , 210 ),
                                                 (atan( 31 ), π − atan(        1
                                                                                 ), π + atan( 31 ), 2π − atan( 13 )), i = 1, 2
                                                                          √ 3√ √ √
                                                 str(i) = (4, 10, ( 22 , √        2   2     2
                                                                                 2 , 2 , 2 ),
                                                                                                 π 3
                                                                                                   , 4 π, 54 π, 74 π), i = 3, 4, 5
                                                                                              √( 4 √
                           2        5     2.8    str(i) = (5, 100, (2, 2 2 − 2, 2, 2, 2),
                                                 (0, 41 π, 12 π, 54 π, 74 π)),
                                                                           √ i√   = 1,√2, 3,√4,
                                                 str(i) = (4, 100, ( 2, 2, 2, 2), (0, 41 π, 12 π, 32 π)), i = 5
                           3        6     3.4    str(i) = (3, 100, (2, 2, 2), (0, 32 π, 43 π), i = 1, 2, 3, 4, 5, 6
                                                                                           3
                           4       12     5.0    str(i) = (3, 10, (1, 1, 1),   √ (0, √π, 2 π)), i5= 1,     2, 3, 4,
                                                                                                         7
                                                 str(i) = (4, 20, (2, 2, √ 2, √2), (0, π, 4 π, 4 π)), i = 5, 6, 7, 8,
                                                                                                   5     7
                                                 str(i) = (4, 20, (2,√2, 2,√ 2),        √(0, π, √ 4 π, 14 π),3i =59, 10,     11, 12
                                                                                                                         7
                           5        3     8.0    str(i) = (4, 40, (2√ 2, , 2√ 2, √2, 2 √2), (√           4 π, 4√π, 4 π, 4 π)), i = 1,
                                                 str(i) = (8, 60, (2 2, 2 5, 2 5, 2 5, 2 5, 2 2, 2, 2), ( 41 π, atan(2),
                                                 π − atan(2), π +√atan(2),     √ √−atan(2),
                                                                                          √          − 41 π, − 12 π, 21 π)), i = 2, 3
                                                                                                  1     3     5     7
                           6        5     5.0    str(i) = (4, 60, ( 2,      √ 2,√ 2, √2),√      ( 4 π, √        √ 4 π)), i = 1, 2, 3, 4
                                                                                                        4 π, 4 π,
                                                 str(i)√= (12,
                                                 √              √ 500, √( √    10, √  10, 2, 10, 10, 2,
                                                   10, 10, 2, 10, 10, 2), (−atan( 31 ), atan( 31 ),
                                                 1     1                 1 1                1 3                      1               1
                                                 4 π, 2 π − atan( 3 ), 2 π + atan( 3 ), 4 π, π − atan( 3 ), π + atan( 3 ),
                                                 5     3                 1 3                1 7
                                                 4 π, 2 π − atan( 3 ), 2 π + atan( 3 ), 4 π)), i = 5



                   4.      Numeri al Results



                   We are not aware of any standard library of ben hmark instan es for this                             parti -
                   ular problem, although su h libraries do exist for other related problems (4). We
                   therefore take a two-stage approa h to testing our algorithm; we rst design six in-
                   stan es with         known optima, against whi h we may initially validate our method. We
                   note that these instan es in lude both                   onvex and non onvex polygons. After es-
                   tablishing the ee tiveness of our SA algorithm, we then test our algorithm against
                   other re ently-des ribed methods for              re tangle pa king (re tangles, of ourse, being
                   members of the polygon               lass), using both existing instan es from the literature
                   and new, larger instan es.




                   4.1.        Known Optima
                   The instan es with known optima are des ribed in Table 1, with graphi al repre-
                   sentations given in Figure 4.
                        For ea h instan e, we use SA to try to nd the optimal layout. The value of imax
                   is set to 20000 × k , the value of cmax is set to 100 × k , and the initial temperature
                   is set to 100. The           onstants λ1 and λ2 are set to 100 (to indu e a large f (x) and
                   adjust the probability of uphill movement). In ea h                    ase, the algorithm is exe uted
                   40 times.
                        Values for the best radius found, rbest , mean radius, r̄ , and varian e v are pre-
                   sented in Table 2. Representations of the best results obtained are given in Figure
                   5. From Table 2 and Figure 5, we observe that the SA algorithm                                an nd layouts
                   that are very         lose to the the optimal          onguration for instan es 1, 2, and 3, where
                   the number of polygons is relatively small and the overall stru tures are simple.
                                                                                                         3
                                                                                                             √
                   The optimal radius for instan e 1 was originally                     al ulated as
                                                                                                         2       2 = 2.121, but
                   the our results yielded a smaller value. This prompted a re-estimation, giving a
                                            q
                                                   9
                   new optimum of               4 64 ). In the rst three instan es, the errors to the optimum are
O tober 26, 2021   23:46       Engineering Optimization    submission

                   8




                                                     Figure 4. Instan es with known optima.

                               rbest −roptimum
                   about
                                  roptimum     = 2%. The algorithm performs less well on instan e 4, with 12
                   polygons in a relatively         omplex        onguration. In this     ase, our algorithm    annot
                   nd the best        onguration, and the error to the optimum is 15%. Instan es 5 and 6
                   feature non ovex polygons. Be ause of the                 omplexity of the shapes, the algorithm
                   is unable to solve these instan es to optimality. The errors to the optimal radius
                   are 11% and 4% for instan es 5 and 6 respe tively.

                   Table 2. Numeri al results for SA on four instan es with known optima
                       Instan e      Est. roptimum        rbest       r         v
                                     q
                           1           4 9 = 2.034        2.080     2.167     0.027
                                      √64
                           2         2√2 = 2.828          2.861     3.209     0.010
                           3         2√3 = 3.464          3.522     4.065     0.157
                           4         3√2 = 4.242          4.887     5.149     0.024
                           5         4√2 = 5.656          6.295     9.266     59.25
                           6         3 2 = 4.242          4.423     7.034    119.44




                   4.2.        Re tangular Instan es
                   We now test our algorithm on four instan es of the LOP                     ontaining only re tangu-
                   lar shapes. The rst three instan es were rst des ribed in (16), and the fourth in
                   (14), where all four instan es were used to ben hmark three dierent approa hes:
                   a geneti       algorithm (GA), parti le swarm optimisation (PSO) and a hybrid                   om-
                   pa tion algorithm followed by parti le swarm lo al sear h (CA-PSLS). Depi tions
                   of ea h instan e are depi ted in Figure                6, and full des riptions are given in Table
                   3. Sin e both parti le-based algorithms out-performed the GA, we do not                      onsider
                   this last method here.
                       We run ea h algorithm 50 times on ea h instan e, re ording the best radius
                   found, rbest , average radius, r , standard deviation of radii, rσ and average run time
                   in se onds, t. Ea h algorithm is               oded in C,    ompiled with g++ 4.1.0 , and run
O tober 26, 2021   23:46     Engineering Optimization    submission

                                                                                                                    9




                                       Figure 5. Best results obtained for instan es with known optima




                                             Figure 6. Four instan es of the LOP using re tangles

                   under SUSE Linux 10.1 (kernel version 2.6.16.54-0.2.5-smp) on a                       omputer with
                   dual Intel Harpertown E5462 2.80GHz pro essors, 4GB of RAM and an 80GB hard
                   drive.
                      The three algorithms (SA, CA-PSLS and PSO) ea h run over a number of it-
                   erations, whi h is di tated by the value of the                onstant CYCLE. In this set of
                   experiments, we set CYCLE=3000 for ea h algorithm. The SA parameter values
                   for cmax, initial temperature, λ1 , and λ2 are set as before, and the imax values set
                   as to 100000, 120000, 108000 and 100000 for instan es 1-4 respe tively. The results
                   obtained are depi ted in Table          4.
                      On the rst three (small) instan es, both parti le-based algorithms slightly out-
                   perform the SA method in terms of solution              quality; on average, by 10%. However,
                   this     omes at a signi ant        ost disadvantage in terms of run time; over the rst
                   three instan es, the parti le-based methods require four times the exe ution time
O tober 26, 2021   23:46      Engineering Optimization            submission

                   10

                   Table 3. Four instan es from the literature
                   Instan e     k   R0    Stru ture
                       1        5   20
                                                            √     √   √    √
                                          str(1) = (4, 12, ( 25, 25, 25, 25), (atan( 3 4
                                                                                         )), π − atan( 4 3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                                           4                  4
                                                            √     √   √    √
                                          str(2) = (4, 16, ( 32, 32, 32, 32), (atan( 4 4
                                                                                         )), π − atan( 4 4 ), π + atan( 4 ), 2π − atan( 4 )))
                                                                                                                           4                  4
                                                            √     √   √    √           3                 3                 3                  3 )))
                                          str(3) = (4, 15, ( 34, 34, 34, 34), (atan( 5 )), π − atan( 5 ), π + atan( 5 ), 2π − atan( 5
                                                            √     √   √    √           2                 2                 2                  2 )))
                                          str(4) = (4, 12, ( 40, 40, 40, 40), (atan( 6 )), π − atan( 6 ), π + atan( 6 ), 2π − atan( 6
                                                           √     √   √    √
                                          str(5) = (4, 9, ( 18, 18, 18, 18), (atan( 33
                                                                                       )), π − atan( 3 3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                                         3                  3
                        2       6   40
                                                            √     √   √    √
                                          str(1) = (4, 12, ( 25, 25, 25, 25), (atan( 3 4
                                                                                         )), π − atan( 4 3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                                           4                  4
                                                            √     √   √    √
                                          str(2) = (4, 16, ( 32, 32, 32, 32), (atan( 4 4
                                                                                         )), π − atan( 4 4 ), π + atan( 4 ), 2π − atan( 4 )))
                                                                                                                           4                  4
                                                            √     √   √    √           3                 3                 3                  3 )))
                                          str(3) = (4, 15, ( 34, 34, 34, 34), (atan( 5 )), π − atan( 5 ), π + atan( 5 ), 2π − atan( 5
                                                            √     √   √    √           4                 4                 4                  4 )))
                                          str(4) = (4, 20, ( 41, 41, 41, 41), (atan( 5 )), π − atan( 5 ), π + atan( 5 ), 2π − atan( 5
                                                            √     √   √    √
                                          str(5) = (4, 25, ( 50, 50, 50, 50), (atan( 5 5
                                                                                         )), π  − atan(  5 ), π + atan( 5 ), 2π − atan( 5 )))
                                                                                                         5                 5                  5
                                                            √     √   √    √
                                          str(6) = (4, 18, ( 45, 45, 45, 45), (atan( 3 6
                                                                                         )), π − atan( 6 3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                                           6                  6
                        3       9   40
                                                            √     √   √    √
                                          str(1) = (4, 12, ( 25, 25, 25, 25), (atan( 3 4
                                                                                         )), π  − atan(  3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                         4                 4                  4
                                                            √     √   √    √
                                          str(2) = (4, 16, ( 32, 32, 32, 32), (atan( 4 4
                                                                                         )), π  − atan(  4 ), π + atan( 4 ), 2π − atan( 4 )))
                                                                                                         4                 4                  4
                                                            √     √   √    √
                                          str(3) = (4, 15, ( 34, 34, 34, 34), (atan( 3 5
                                                                                         )), π  − atan(  3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                         5                 5                  5
                                                            √     √   √    √
                                          str(4) = (4, 20, ( 41, 41, 41, 41), (atan( 4 5
                                                                                         )), π  − atan(  4 ), π + atan( 4 ), 2π − atan( 4 )))
                                                                                                         5                 5                  5
                                                            √     √   √    √
                                          str(5) = (4, 25, ( 50, 50, 50, 50), (atan( 5 5
                                                                                         )), π  − atan(  5 ), π + atan( 5 ), 2π − atan( 5 )))
                                                                                                         5                 5                  5
                                                            √     √   √    √
                                          str(6) = (4, 12, ( 40, 40, 40, 40), (atan( 2 6
                                                                                         )), π  − atan(  2 ), π + atan( 2 ), 2π − atan( 2 )))
                                                                                                         6                 6                  6
                                                            √     √   √    √
                                          str(7) = (4, 18, ( 45, 45, 45, 45), (atan( 3 6
                                                                                         )), π  − atan(  3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                         6                 6                  6
                                                            √     √   √    √
                                          str(8) = (4, 24, ( 52, 52, 52, 52), (atan( 4 6
                                                                                         )), π  − atan(  4 ), π + atan( 4 ), 2π − atan( 4 )))
                                                                                                         6                 6                  6
                                                            √     √   √    √
                                          str(9) = (4, 30, ( 61, 61, 61, 61), (atan( 5   )), π  − atan(  5 ), π + atan( 5 ), 2π − atan( 5 )))
                                                                                  √ 6                    6                 6                  6
                        4      20   100
                                                            √       √       √
                                          str(1) = (4, 10, ( 22.25, 22.25, 22.25, 22.25), (atan( 2.5  4
                                                                                                          )),  π −  atan(  2.5 ), π + atan( 2.5 ),
                                                                                                                            4                   4
                                                      2.5
                                          2π − atan( 4 )))
                                                           √     √   √    √          4                 4                 4                  4
                                          str(2) = (4, 8, ( 20, 20, 20, 20), (atan( 2 )), π − atan( 2 ), π + atan( 2 ), 2π − atan( 2 )))
                                                            √     √   √    √
                                          str(3) = (4, 15, ( 34, 34, 34, 34), (atan( 3   )), π − atan( 5 3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                            √       √       √     √ 5                                      5
                                                                                                      4 )), π − atan( 4 ), π + atan( 4 ),
                                                                                                                                              5
                                          str(4) = (4, 14, ( 28.25, 28.25, 28.25, 28.25), (atan( 3.5                       3.5                3.5
                                                       4
                                          2π − atan( 3.5 )))
                                                              √      √       √     √
                                          str(5) = (4, 7.50, ( 27.25, 27.25, 27.25, 27.25), (atan( 5 )), π − atan( 5 ), π + atan( 1.5
                                                                                                       1.5                    1.5
                                                                                                                                                   5
                                                                                                                                                       ),
                                          2π − atan( 1.5
                                                       5
                                                          )))
                                                            √     √   √    √           3                 3                 3                  3
                                          str(6) = (4, 18, ( 45, 45, 45, 45), (atan( 6 )), π − atan( 6 ), π + atan( 6 ), 2π − atan( 6 )))
                                                            √     √   √    √
                                          str(7) = (4, 12, ( 40, 40, 40, 40), (atan( 2 6
                                                                                         )), π − atan( 6 2 ), π + atan( 2 ), 2π − atan( 2 )))
                                                                                                                           6                  6
                                                            √     √   √    √
                                          str(8) = (4, 18, ( 45, 45, 45, 45), (atan( 3 6
                                                                                         )), π − atan( 6 3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                                           6                  6
                                                            √     √   √    √           5                 5                 5                  5 )))
                                          str(9) = (4, 20, ( 41, 41, 41, 41), (atan( 4 )), π − atan( 4 ), π + atan( 4 ), 2π − atan( 4
                                                                √      √       √     √                   1.5                   1.5                 1.5 ),
                                          str(10) = (4, 5.25, ( 14.50, 14.50, 14.50, 14.50), (atan( 3.5 )), π − atan( 3.5 ), π + atan( 3.5
                                                      1.5 )))
                                          2π − atan( 3.5
                                                              √    √   √    √
                                          str(11) = (4, 12, ( 25, 25, 25, 25), (atan( 3  4
                                                                                           )), π − atan( 4 3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                                             4                  4
                                                            √       √       √     √
                                          str(12) = (4, 6, ( 18.25, 18.25, 18.25, 18.25), (atan( 1.5  4
                                                                                                          )),  π − atan( 1.54
                                                                                                                                ), π + atan( 1.54
                                                                                                                                                    ),
                                          2π − atan( 1.5
                                                       4
                                                          )))
                                                              √    √   √    √            3                 3                 3                  3
                                          str(13) = (4, 15, ( 34, 34, 34, 34), (atan( 5 )), π − atan( 5 ), π + atan( 5 ), 2π − atan( 5 )))
                                                              √    √   √    √
                                          str(14) = (4, 20, ( 41, 41, 41, 41), (atan( 4    )), π − atan( 5 4 ), π + atan( 4 ), 2π − atan( 4 )))
                                                                 √      √       √     √5                                     5                  5
                                          str(15) = (4, 17.50, ( 37.25, 37.25, 37.25, 37.25), (atan( 3.5     5
                                                                                                                )), π − atan( 3.5  5
                                                                                                                                     ), π + atan( 3.5  5
                                                                                                                                                          ),
                                          2π − atan( 3.5
                                                       5
                                                          )))
                                                              √      √       √     √
                                          str(16) = (4, 15, ( 42.25, 42.25, 42.25, 42.25), (atan( 2.5   6
                                                                                                           )), π − atan( 2.5  6
                                                                                                                                 ), π + atan( 2.5 6
                                                                                                                                                     ),
                                          2π − atan( 2.5
                                                       6
                                                          )))
                                                              √    √   √    √
                                          str(17) = (4, 12, ( 40, 40, 40, 40), (atan( 2  6
                                                                                           )), π − atan( 6 2 ), π + atan( 2 ), 2π − atan( 2 )))
                                                                                                                             6                  6
                                                              √    √   √    √
                                          str(18) = (4, 20, ( 41, 41, 41, 41), (atan( 4  5
                                                                                           )), π − atan( 5 4 ), π + atan( 4 ), 2π − atan( 4 )))
                                                                                                                             5                  5
                                                              √    √   √    √
                                          str(19) = (4, 30, ( 61, 61, 61, 61), (atan( 5  6
                                                                                           )), π − atan(   5 ), π + atan( 5 ), 2π − atan( 5 )))
                                                                                                           6                 6                  6
                                                            √     √   √    √
                                          str(20) = (4, 9, ( 18, 18, 18, 18), (atan( 3 3
                                                                                         )), π  − atan(  3 ), π + atan( 3 ), 2π − atan( 3 )))
                                                                                                         3                 3                  3




                   of the SA algorithm to terminate. When the problem size is in reased to 20, the
                   benets of the SA algorithm begin to be ome apparent, as it out-performs the other
                   two algorithms in terms of both solution quality                            and run time. In order to establish
                   the signi an e of this, we now test all three methods on mu h larger instan es.




                   4.3.       Large Re tangular Instan es
                   We designed instan es with 40, 60, 80 and 100 re tangles. Spa e pre ludes a detailed
                   des ription of these, but the full problem set is available from the                                            orresponding
                   author. As before, ea h method was run 50 times on ea h instan e. Be ause of
                   the      omputational       ost in urred, we redu ed CYCLE to 1000 for ea h algorithm.
                   The results are depi ted in Table                   5, with an example solution for the 40 re tangle
                   instan e depi ted in Figure               7.
                        The SA method signi antly out-performs the other two methods in terms of
                   solution quality, but with an asso iated                           ost in terms of run time. However, as
                   shown by the gures for standard deviation, SA oers a                                        onsistently high-quality
                   solution method (at a pri e), whereas the other two algorithms oer solutions of
                   more variable quality, but more qui kly.
O tober 26, 2021   23:46       Engineering Optimization   submission

                                                                                                                         11

                   Table 4. Results for SA, CA-PSLS and PSO on four re tangular instan es from the literature (CYCLE=3000)
                     Instan e        Size    Algorithm      rbest        r        rσ          t (s)
                           1          5          SA       12.776       13.693     0.62         0.82
                                             CA-PSLS      10.942       11.704     0.49         4.31
                                                PSO       11.046       11.716     0.49         4.89
                           2          6          SA       16.004       17.377     0.69         1.66
                                             CA-PSLS      14.686       15.590     0.67         7.76
                                                PSO       14.320       15.349     0.56         8.28
                           3          9          SA       20.849       22.328     0.87         6.84
                                             CA-PSLS      18.157       19.797     1.03        21.07
                                                PSO       18.579       19.205     0.49        22.84
                           4          20         SA       29.969       31.680     0.98        92.01
                                             CA-PSLS      27.927       33.129     5.48        125.52
                                                PSO       32.596       34.426     2.23        138.00




                   Table 5. Results for SA, CA-PSLS and PSO on large instan es (CYCLE=1000)
                     Instan e        Size    Algorithm      rbest            r           rσ           t (s)
                           1          40         SA       164.061       174.586        4.81       263.24
                                             CA-PSLS      179.508       253.627     60.42         219.84
                                                PSO       242.471       276.939     24.44         197.03
                           2          60         SA       170.284       187.312        6.32       905.75
                                             CA-PSLS      184.984       288.642     124.26        579.31
                                                PSO       272.282       317.739     26.17         451.72
                           3          80         SA       265.654       281.087        8.54       2178.31
                                             CA-PSLS      298.524       544.421     162.81        1016.70
                                                PSO       432.347       490.862     35.75         813.59
                           4         100         SA       406.991       423.087        7.87       4260.54
                                             CA-PSLS      658.352       880.537     108.65        1611.52
                                                PSO       598.265       688.785     48.06         1277.43




                   5.      Con lusions


                   In this paper we des ribe a novel algorithm based on simulated annealing for the
                   problem of pa king weighted polygons inside a                 ir ular      ontainer. As well as being
                   of signi ant theoreti al interest, this problem has real signi an e in domains su h
                   as satellite design in the aerospa e industry. Our algorithm                       onsistently generates
                   high-quality solutions that oer a signi ant improvement over those generated by
                   other methods. However, this superiority              omes with an asso iated              omputational
                   overhead, so the         hoi e of method should largely be driven by the anti ipated appli-
                     ation. Future work will involve improving the method's performan e on problems
                     ontaining non onvex polygons, as well as its extension into three dimensions.




                   A knowledgements


                   This work was partially supported by the Dalton Resear h Institute, Man hester
                   Metropolitan University.
O tober 26, 2021   23:46    Engineering Optimization    submission

                   12                                        REFERENCES




                                     Figure 7. Best 40 re tangle solution generated by SA (r = 134.07)


                   Referen es


                        [1℄ E. G. Birgin, J. M. Martínez, F.H. Nishihara, and D. P. Ron oni. Orthogonal
                           pa king of re tangular items within arbitrary              onvex regions by nonlinear
                           optimization.   Computers and operations resear h, 33(12):35353548, 2006.
                        [2℄ E. Burke and G. Kendall. Applying simulated annealing and the no t polygon
                           to the nesting problem. In      Pro eedings of the World Manufa turing Confer-
                           en e, pages 2730, 1997.
                        [3℄ K.A. Dowsland, Vaid S., and W.B. Dowsland.                 An algorithm for polygon
                           pla ement using a bottom-left strategy.            European Journal of Operational
                           Resear h, 141:371381, 2002.
                        [4℄ S.P. Fekete and J.C. van der Veen. Pa kLib2: An integrated library of multi-
                           dimensional pa king problems.          European Journal of Operational Resear h,
                           183(3):11311135, 2007.
                        [5℄ E. Feng, X.L. Wang, X.M. Wang, and H. Teng.                    An algorithm of global
                           optimization for solving layout problems.           European Journal of Operational
                           Resear h, 114:430436, 1999.
                        [6℄ R.J. Fowler, M.S. Paterson, and S.L. Tanimoto. Optimal pa king and               overing
                           in the plane are NP- omplete.       Information Pro essing Letters, 12(3):133137,
                           1981.
                        [7℄ Birgin E. G., J. M. Martínez, W. F. Mas arenhas, and D. P. Ron oni. Method
                           of sentinels for pa king items within arbitrary            onvex regions.     The Journal
                           of the Operational Resear h So iety, 6(57):735746, 2006.
                        [8℄ R. He kmann and T. Lengauer. A simulated annealing approa h to the nest-
                           ing problem in the textile manufa turing industry.                Annals of Operations
                           Resear h, 57(1):103133, 1995.
                        [9℄ P. Jain, P. Feynes, and R. Ri hter. Optimal blank nesting using simulated
                           annealing.   Transa tions of the Ameri an So iety of Me hani al Engineers,
                           114:160165, 1992.
                     [10℄ S. Kirkpatri k, C. D. Gelatt, and M. P. Ve              hi. Optimization by simulated
                           annealing.   S ien e, 220(4598):671680, 1983.
                     [11℄ N. Li, F. Liu, and D. Sun.           A study on the parti le swarm optimization
                           with mutation operator       onstrained layout optimization.          Chinese Journal of
                           Computers, 27(7):897903, 2004.
                     [12℄ Poshyanonda P. and C.H. Dagli. Geneti              neuro-nester.    Journal of Intelligent
                           Manufa turing, 15(2):201218, 2004.
O tober 26, 2021   23:46    Engineering Optimization   submission

                                                            REFERENCES                                      13

                     [13℄ F. Tang and H. Teng. A modied geneti               algorithm and its appli ation to
                           layout optimization.    Journal of Software, 10:10961102, 1999.
                     [14℄ Yi-Chun Xu, Ren-Bin Xiao, and Martyn Amos.                Parti le swarm algorithm
                           for weighted re tangle pla ement. In Pro eedings of the 3rd International
                           Conferen e on Natural Computation (ICNC'07), pages 728732. IEEE Press,
                           August 24-27, 2007.
                     [15℄ Y. Yu, J. Cha, and X. Tang. Learning based GA and appli ation in pa king.
                           Chinese Journal of Computers, 24(12):12421249, 2001.
                     [16℄ J. Zhai, E. Feng, Z. Li, and H. Yin.        Non-overlapped geneti     algorithm for
                           layout problem with behavioral       onstraints.   Journal of Dalian University of
                           Te hnology, 39(3):352357, 1999.
                     [17℄ C. Zhou, L. Gao, and H. Gao. Parti le swarm optimization based algorithm
                           for   onstrained layout optimization.    Control and De ision, 20(1):3640, 2005.
