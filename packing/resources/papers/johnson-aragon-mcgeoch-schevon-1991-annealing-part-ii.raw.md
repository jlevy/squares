                                                            ARTICLES                                                                                   tends to dominate tm
                                                                                                                                                       graphs as the size and/o
                                                                                                                                                       but was roundly beaten I
                                                                                                                                                       structure. )
       OPTIMIZATION BY SIMULATED ANNEALING: AN EXPERIMENTAL                                                                                                 In this paper, we c
                                                                                                                                                       context of two addition
              EVALUATION; PART II, GRAPH COLORING AND                                                                                                  natorial optimization
                        NUMBER PARTITIONING                                                                                                             number partitioning, T
                                                                                                                                                        cause they have been stl
                                                            DAVID S. JOHNSON                                                                            traditionally been appn
                                               A T& T Bell Laboratories, Murray Hill, New Jersey                                                        the algorithmic template
                                                                                                                                                        is based,
                                                           CECILIA R. ARAGON                                                                                The graph coloring I
                                                  University of California, Berkeley, California                                                        tions in areas such as !
                                                                                                                                                         see Leighton (1979), 0
                                                            LYLE A. MCGEOCH                                                                             Werra (1985), We are
                                                    Amherst College, Amherst, Massachusetts                                                             asked to find the minim
                                                                                                                                                         can be partitioned into ,
                                                                                                                                                         of which contains botl
                                                           CATHERINE SCHEVON
                                              Johns Hopkins University, Baltimore, Maryland
                                                                                                                                                         Here, the apparent neE
                                                                                                                                                         past may not have been
                                (Received February 1989; revision received Juh~ 1990; accepted September 1990)
                                                                                                                                                         definition of the cost
                                                                                                                                                         extending the notion of
       This is the second in a series of three papers that empirically examine the competitiveness of simulated annealing in certain
                                                                                                                                                         up with a variety of p
       well-studied domains of combinatorial optimization. Simulated annealing is a randomized technique proposed by S. Kirkpatrick,
       C. D. Gelatt and M. P. Vecchi for improving local optimization algorithms. Here we report on experiments at adapting
                                                                                                                                                         mization that might yie
       simulated annealing to graph coloring and number partitioning, two problems for which local optimization had not previously                        of attempting to minim
       been thought suitable. For graph coloring, we report on three simulated annealing schemes, all of which can dominate                               annealing schemes bas
       traditional techniques for certain types of graphs, at least when large amounts of computing time are available. For number                        I) a penalty-function 2
       partitioning, simulated annealing is not competitive with the differencing algorithm of N. Karmarkar and R. M. Karp, except on                     current authors, 2) a
       relatively small instances. Moreover, if running time is taken into account, natural annealing schemes cannot even outperform                      interchanges and was
       multiple random runs of the local optimization algorithms on which they are based, in sharp contrast to the observed                               Shapiro (1986), and ~
       performance of annealing on other problems.                                                                                                        orthogonal approach dl
                                                                                                                                                          (1987). None of these
                                                                                                                                                          create good colorings
                                                                                                                                                          amounts of time availal
                                                                                                                                                          with (and often to dO!

S    imulated annealing is a new approach to the approxi-
     mate solution of difficult combinational optimization
problems. It was originally proposed by Kirkpatrick,
                                                                                 In Part I (Johnson et al. 1989), we describe the
                                                                              simulated annealing approach and its motivation, and
                                                                              report on extensive experiments with it in the context of
                                                                                                                                                          approaches. (Not one t
                                                                                                                                                          dominates the other tw
                                                                                                                                                              The second problerr
Gelatt and Vecchi (1983) and Cerny (1985), who re-                            the graph partitioning problem (given a graph G ==
                                                                                                                                                           was chosen less for it:
ported promising results based on sketchy experiments.                        (V, E), find a partition of the vertices into two equal-
                                                                                                                                                           challenges it presents
Since then there has been an immense outpouring of                            sized sets VI and V2 , which minimizes the number of
                                                                                                                                                           proach. In this problen
papers on the topic, as documented in the extensive                           edges with endpoints in both sets). We were concerned
                                                                                                                                                           numbers a"a 2 ,···,a
bibliographies of Collins, Eglese and Golden (1988) and                       with two main issues: 1) how the various choices made
                                                                                                                                                           to partition them into t
Van Laarhoven and Aarts (1987). The question of how                           in adapting simulated annealing to a particular problem
well annealing stacks up against its more traditional                         affect its performance, and 2) how well an optimized
competition has remained unclear, however, for a vari-                        annealing implementation for graph partitioning com-
ety of important applications. The series of papers,                          petes against the best of the more traditional algorithms
of which this is the second, attempts to rectify this                         for the problem. (For graph partitoning, the answer to                     is minimized, The ch2
situation.                                                                    the second question was mixed: simulated annealing                         natural "neighborhood
                                                                                                                                                         neighboring solutions (
Subject classifications: Mathematics, combinatorics: number partitioning heuristics. Networks/graphs, heuristics: graph coloring heuristics. Simula-
tion, applications: optimization by simulated annealing.                                                                                                 or two elements, have
                                                                                                                                                         rain, in which neighl
Operations Research                                                                                                0030-364X/91 /3903-0000 $01.25
Vol. 39, No.3, May-June 1991                                            37R                          © 1991 Operations Research Society of America
                                                                                                       Graph Coloring by Simulated Annealing           /   379
                                            to dominate traditional techniques on random           quality. Thus, traditional local optimization algorithms
                                             as the size and/or density of the graphs increases,   are not competitive with other techniques for this prob-
                                    but was roundly beaten on graphs with built-in geometric       lem, in particular the "differencing" algorithm of
                                    structure. )                                                   Karmarkar and Karp (1982). Consequently, it seems
 ERIMENTAL                             In this paper, we consider the same issues in the           unlikely that simulated annealing, which in essence is a
                                   context of two additional well-studied, NP-hard combi-          method for improving local optimization, can offer
 NO                                natorial optimization problems: graph coloring and              enough of an improvement to bridge the gap. Our exper-
                                    number partitioning. These problems were chosen be-            iments verify this intuition. Moreover, they show that
                                    cause they have been studied extensively, but neither had      for this problem even multiple random-start local
                                    traditionally been approached using local optimization,        optimization outperforms simulated annealing, a
                                   the algorithmic template upon which simulated annealing         phenomenon we have not observed in any of the
                                    is based.                                                      other annealing implementations we have studied
                                       The graph coloring problem has widespread applica-          (even the mediocre ones).
                                   tions in areas such as scheduling and timetabling, e.g.,           Although some familiarity with simulated annealing
                                    see Leighton (1979), Opsut and Roberts (1981), and de          will be helpful in reading this paper, our intention is that
                                   Werra (1985). We are given a graph G = (V, E), and              it be self-contained. In particular, although we shall
                                   asked to find the minimum k such that the vertices of G         frequently allude to Part I for background material, the
                                   can be partitioned into k color classes VI' ... , V k , none    reader should be able to understand the results we pre-
                                   of which contains both endpoints of any edge in E.              sent here without reference to that paper. The remainder
                                   Here, the apparent neglect of local optimization in the         of this paper is organized as follows. In Section 1, we
                                   past may not have been totally justified. By changing the       briefly outline the generic annealing algorithm that is the
                                   definition of the cost of a solution, and possibly by           basis for our implementations, as developed in Part I of
                                   extending the notion of what a solution is, one can come        this paper. Sections 2 and 3 are devoted to graph color-
ed annealing in certain
osed by S. Kirkpatrick,
                                   up with a variety of plausible proposals for local opti-        ing and number partitioning, respectively. Section 4
xperiments at adapting             mization that might yield good colorings as a side effect       concludes with a brief summary and a preview of the
tion had not previously            of attempting to minimize the new cost. We investigate          third and final paper in this series, which will cover our
,f which can dominate              annealing schemes based on three of these proposals:            experiments in applying simulated annealing to the infa-
 available. For number             1) a penalty-function approach that originated with the         mous traveling salesman problem.
 R. M. Karp, except on             current authors, 2) a variant that uses Kempe chain                All running times quoted in this paper are for an
:annot even outperform             interchanges and was devised by Morgenstern and                 individual processor of a Sequent Balance™ 21000 mul-
ntrast to the observed             Shapiro (1986), and 3) a more recent and somewhat               ticomputer, running under the Dynix™ operating system
                                   orthogonal approach due to Chams, Hertz and de Werra            (Balance and Dynix are trademarks of Sequent Computer
                                   (1987). None of these versions can be counted on to             Systems, Inc.). Comparable times would be obtained on
                                   create good colorings quickly, but if one has large             a VAX™ 750 without a floating point accelerator run-
                                   amounts of time available, they appear to be competitive        ning under Unix™ (VAX is a trademark of the Digital
                                   with (and often to dominate) alternative CPU-intensive          Equipment Corporation; Unix is a trademark of AT&T
   1989), we describe t
                                   approaches. (Not one of the three annealing approaches          Bell Laboratories). These are slow machines by modern
   and its motivation, a
                                   dominates the other two across the board.)                      standards; speedups by factors of 10 or greater are
  s with it in the context
                                       The second problem we study, number partitioning,           possible with currently available workstations. This
 m (given a graph G,
                                   was chosen less for its applications than for the severe        should be kept in mind when evaluating some of the
 : vertices into two equlf
                                   challenges it presents to the simulated annealing ap-           larger running times reported, and we shall have more to
 minimizes the number
                                   proach. In this problem, one is given a sequence of real        say about it in the Conclusion.
;ets). We were concerne
                                   numbers at, a2 , .. . , an in the interval [0,1], and asked
  the various choices ma .
                                   to partition them into two sets A I and A 2 such that
 g to a particular proble·                                                                         1. THE GENERIC ANNEALING ALGORITHM
) how well an optimiz
                                                                                                   Both local optimization and simulated annealing require
   graph partitioning com
                                                                                                   that the problem to which they are applied be describable
lore traditional algorithm
                                                                                                   as follows: For each instance I of the problem, there is a
Jartitoning, the answer t
                                   is minimized. The challenge of this problem is that the         set F of solutions, each solution S having a cost c(S).
'led: simulated annealin'
                                   natural "neighborhood structures" for it, those in which        The goal is to find a solution of minimum cost. (Note
                                   neighboring solutions differ as to the location of only one     that both problems mentioned in the Introduction have
raph coloring heuristics. Simul
                                   or two elements, have exceedingly "mountainous" ter-            this form.)
                                   rain, in which neighboring solutions differ widely in              In order to adapt either of the two approaches to such
J030-364X/91/3903-oo00$01.2.
ions Research Society of Americ,
380   /   JOHNSON ET AL.

                                                                                                                                space" may have been ei
a problem, one must additionally define an auxiliary                 All our annealing implementations start with the
                                                                                                                                just the feasible solutions
neighborhood graph on the space of solutions for a                parameterized generic annealing algorithm summarized
                                                                                                                                thus, our algorithm is can
given instance. This is a directed graph whose vertices           in Figure I. This generic procedure relies on several
                                                                                                                                solution found, rather thar
are the solutions, with the neighbors of a solution S             problem-specific subroutines. They are READ_
                                                                                                                                    The only substantive diJ
being those solutions S' for which (S, S') is an arc in the       INSTANCE(), INITIAL_SOLUTION(),
                                                                                                                                 summarized in Figure 1
neighborhood graph.                                               NEXT _CHANGE(), CHANGE_SOLN() and
                                                                                                                                 Part I is the inclusion her
   A local optimization algorithm uses this structure to          FINAL_SOLN( ). In addition, the procedure is para-
                                                                                                                                 spent at high temperatures
find a solution as follows: Starting with an initial solu-        meterized by the variables INITPROB, SIZEFAC-
                                                                                                                                 the moves are accepted).
tion S generated by other means, it repeatedly attempts           TOR, CUTOFF, TEMPFACTOR, FREEZE_LIM
                                                                                                                                 graph partitioning, and c
to find a better solution by moving to a neighbor with            and MINPERCENT. (See Part I for observations about
                                                                                                                                 ments for the problems st
lower cost, until it reaches a solution none of whose             the best values for these parameters and the interactions
                                                                                                                                 temperatures does not api
neighbors have a lower cost. Such a solution is called            between them.) Note that the generic algorithm never
                                                                                                                                 quality of the final solutiO!
locally optimal. Simulated annealing is motivated by the          deals with the solutions themselves, only their costs. The
                                                                                                                                 simply to start at lower
desire to avoid getting trapped in poor local optima, and         current solution, its proposed neighbor, the best solution
                                                                                                                                  can degrade, however, if
hence, occasionally allows "uphill moves" to solutions            found so far, and the cost of the latter are kept as static
                                                                                                                                  ture too low. Cutoffs all«
of higher cost, doing this under the guidance of a control        variables in the problem-specific part of the code. As in
                                                                                                                                  leaving a margin of safel
parameter called the temperature.                                 Part I, we allow for the possibility that the "solution
                                                                                                                                  With the addition of CI
                                                                                                                                  closely mirrors the am
                                                                                                                                  Kirkpatrick's original cod
                                                                                                                                     In each implementatio
                1. Call READ_INSTANCE() to read input, compute an upper bound c* on the                                           describe the relevant sub!
                        optimal solution value, and return the average neighborhood size N.                                        chosen for the parameter
                2. Call INITIAL_SOLUTIONO to generate an initial solution S and return c = cost (S).                               Step 3 is implemented, be
                3. Choose an initial temperature T > 0 so that in what follows the changes/ trials ratio                           used for graph partitioni
                        starts out approximately equal to INITPROB.                                                                methods.
                4. Setjreezecount = O.
                5. While jreezecount < FREEZE_LIM (Le., while not yet "frozen") do the following:                                ~2. GRAPH COLORING

                        5.1 Set changes =trials =O.                                                                             f~The graph coloring prabl,
                            While trials < SIZEFACTOR'N and changes < CUTOFF'N, do the following:                               ~'a prime candidate for heu
                                                                                                                                'lilian, and indeed none a
                            5.1.1     Set trials = trials + 1.
                                                                                                                                    ave been of this type. R
                            5.1.2     Call NEXT_CHANGEO to generate a random neighbor S' of S
                                                                                                                                '> roblem we are given a g
                                      and return c' = cost (S').
                                                                                                                                  .Ind a partition of V int'
                            5.1.3     Let ~ = c' - c.
                                                                                                                                    lasses C 1 , C z "'" C k ,
                            5.1.4     If ~ $ 0 (downhill move),
                                                                                                                                   Can be in the same color (
                                           Set changes = changes + 1 and c = c'.                                                   . em, i.e., if E contains
                                           Call CHANGE_SOLNO to set S =S' and. if S' is feasible                                    , ssible number of calc
                                                and cost (S') < c*, to set s* = S' and c* = cost (S').                              ,hromatic number of C
                            5.1.5     If ~ > 0 (uphill move),                                                                       oloring has widespread:
                                           Choose a random number r in [0,1].                                                         ith scheduling (in situ2
                                           If r $ e-MT (Le., with probability e-IJ.lT),                                             ;odel the events being sc
                                                Set changes = changes + 1 and c = c'.                                                o/ents represented by ed
                                                Call CHANGE_SOLNO.                                                                   '79, Opsut and Roberts
                                                                                                                                       Because graph colorinJ
                        5.2 Set T = TEMPFACTOR . T (reduce temperature).
                                                                                                                                      . lcient optimization alg
                            If c* was changed during 5.1, set jreezecount = O.
                                                                                                                                           s guaranteed to fi
                            If changes/ trials < MINPERCENT, set jreezecount = jreezecount + 1.                                         arey and Johnson 1979
                6. Call FINAL_SOLNO to output S*.                                                                                      . t of developing heuri
                                                                                                                                        bmal colorings qui,
                                                                                                                                      ,mplexity-theoretic ob
                                    Figure 1. The generic simulated annealing algorithm.
                                                                                                  Graph Coloring by Simulated Annealing            /   381

entations start wi                " may have been expanded to include more than              (1976) show that for any r < 2, it is NP-hard to con-
19 algorithm summ·                  e feasible solutions to the original problem, and        struct colorings using no more than rX( G) colors. Fortu-
                                ~',our algorithm is careful to output the best feasible      nately, NP-hardness is a worst case measure, and does
lcedure relies on s
;. They are R.                  :'on found, rather than simply the best solution.            not rule out the possibility of heuristics that work well in
\. L _ SOL U T Wi                 e only substantive difference between the algorithm        practice. There have thus been many attempts to devise
<\NGE_SOLN( )                      arized in Figure I and the generic algorithm of           such heuristics, e.g., see Welsh and Powell (1967),
 , the procedure is'                 is the inclusion here of cutoffs to limit the time      Matula, Marble and Isaacson (1972), Johnson (1974),
NITPROB, SIZE                      at high temperatures (where, say, 50% or more of          Grimmet and McDiarmid (1975), Brelaz (1979),
CTOR, FREEZE!.                     aves are accepted). As we observe in Part I for           Leighton (1979), and Johri and Matula (1982). Until
1 I for observations'
                                     partitioning, and confirm in preliminary experi-        recently, the literature has concentrated almost exclu-
ieters and the interac               for the problems studied here, time spent at high       sively on heuristics that use a technique we might call
  generic algorithm                ratures does not appear to contribute much to the         successive augmentation, as opposed to local optimiza-
 ves, only their costs.::       'ty of the final solution. One way to limit this time is     tion. In this approach, a partial coloring is extended,
eighbor, the best solu           Iy to start at lower temperatures. Solution quality         vertex by vertex, until all vertices have been colored, at
Ie latter are kept as s           egrade, however, if we make the starting tempera-          which point the coloring is output without any attempt to
IC part of the code.
                                 too low. Cutoffs allow us to save time while still          improve it by perturbation. In the next section, we
ibility that the '               ng a margin of safety in the starting temperature.          describe several such algorithms because they illustrate
                                    the addition of cutoffs, our generic algorithm           annealing's competition, and they provide the basic in-
                                 ly mirrors the annealing structure implicit in              sights that can lead us to simulated annealing implemen-
                               kpatrick's original code.                                     tations.
                                   each implementation that we discuss, we shall
                                ribe the relevant subroutines and specify the values         2.1. Successive Augmentation Heuristics
                                en for the parameters. We shall also discuss how             Perhaps the simplest example of a successive augmenta-
)Sf (5).
                                 3 is implemented, be it by the "trial run" approach         tion heuristic is the "sequential" coloring algorithm
 ratio                            for graph partitioning in Part I, or more ad hoc           (denoted in what follows by SEQ). Assume that the
                                 ods.                                                        vertices are labeled VI' . . . , V no We color the vertices in
                                                                                             order. Vertex v I is assigned to color class C 1 , and
wing:                                                                                        thereafter, vertex Vi is assigned to the lowest indexed
                                                                                             color class that contains no vertices adjacent to Vi (i.e.,
                                  graph coloring problem does not seem at first to be        no vertices u such that {u, Vi} EE). This algorithm
Jllowing:                         me candidate for heuristics based on local optimiza-       performs rather poorly in the worst case; 3-colorable
                                 , and indeed none of the standard heuristics for it         graphs may end up with Q(n) colors (Johnson). For
'5                                 been of this type. Recall that in the graph coloring      random graphs with edge probability p = 0.5, however,
                                 lem we are given a graph G = (V, E), and asked to           it is expected (asymptotically as n = I V I gets large) to
                                  a partition of V into a minimum number of color            use no more than 2· x(G), i.e., twice the optimal num-
                                  es C 1, C 2 , •. . , C k , where no two vertices u and v   ber of colors (Grimmet and McDiarmid). No polynomial
                                 be in the same color class if there is an edge between      time heuristic has been proved to have better average
                                  , i. e., if E contains the edge {u, v}. The minimum        case behavior. (The best worst case bound proved for a
                                 ible number of color classes for G is called the            polynomial time heuristic is only a slight improvement
                                omatic number of G and denoted by x(G). Graph                over the worst case bound for SEQ: Berger and Rompel
                                 ring has widespread applications, many having to do         (1990) improve on constructions of Johnson (1974) and
                            with scheduling (in situations where the vertices of G           Wigderson (1983) to construct an algorithm that will
                            mOdel the events being scheduled, with conflicts between         never use more than O(n(log log n Ilog n)3) times the
                            evrnts represented by edges) (de Werra 1985, Leighton            optimal number of colors.)
                            W79, Opsut and Roberts 1981).                                       Experimentally, however, SEQ is outperformed on
                               Because graph coloring is NP-hard, it is unlikely that        average by a variety of other successive augmentation
                            efficient optimization algorithms for it exist (i.e., algo-      algorithms, among the best of which are the DSATUR
                            rithms guaranteed to find optimal colorings quickly)             algorithm of Brelaz and the Recursive Largest First
I.
                            (Garey and Johnson 1979). The practical question is thus         (RLF) algorithm of Leighton. The former dynamically
                            that of developing heuristic algorithms that find near-          chooses the vertex to color next, picking one that is
                            optimal colorings quickly. Even here, there are                  adjacent to the largest number of distinctly colored ver-
                            Complexity-theoretic obstacles. Garey and Johnson                tices. The latter colors the vertices one color class at a
382    /   JOHNSON ET AL.
time, in the following "greedy" fashion. Let C be the                  60                                                                    Problem-Specific Det
next color class to be constructed, V' be the set of                                                                                         neighborhood structure,
                                                                  N    50                               1000-VERTEX RANDOM GRAPH
as-yet-uncolored vertices, and U be an initially empty            U                                                                          tioning implementation
                                                                  M
set of uncolored vertices that cannot legally be placed           B
                                                                   E   40
                                                                                                                                             solutions and penalty fun
                                                                   R
in C.                                                              0
                                                                                                                                             partition of V int
                                                                   F
                                                                       30                                                                    Cl,CZ, ... ,Ck , I~k~
1. Choose a vertex VOE V' that has the maximum num-               C
                                                                  0                                                                          color classes or not. Tw
                                                                  L
   ber of edges to other vertices in V'. Place Vo in C            0
                                                                  R    20
                                                                                                                                             one can be transformed
                                                                   1
   and move all u E V' that are adjacent to Vo from V'            N
                                                                   G                                                                         from one color class to
                                                                   S   10
   to U.
2. While V' remains nonempty, do the following:
     Choose a vertex v E V' that has a maximum num-
                                                                       o I
                                                                            100
                                                                                   J
                                                                                   I
                                                                                  105
                                                                                             'I
                                                                                              I
                                                                                            110
                                                                                                    J    I
                                                                                                        115
                                                                                                              n I
                                                                                                               120
                                                                                                                      r
                                                                                                                           I
                                                                                                                          125
                                                                                                                                n
                                                                                                                                130
                                                                                                                                   I    I
                                                                                                                                       135
                                                                                                                                             neighbor, we will rand
                                                                                                                                             class COLD' a vertex v
                                                                                                                                             1 ~ i ~ k + I, where k
      ber of edges to vertices in U. Add v to C and                               RLF (10.7 Min)   DSATUR(2.1 Min)    SEQ(l.l Min)
                                                                                                                                             classes. The neighbor is
      move all UE V' that are adjacent to v from V'                                                                                          class C i . If i = k + 1 tl
      to U.                                                       Figure 2. Histogram of the colorings found by running
                                                                            each of RLF, DSATUR and SEQ for 100                              new, previously empty (
   Let G R be the residual graph induced by the vertices                    different starting permutations of the vertices                  we try again. Note that
left uncolored after C is formed (i.e., the vertices in U                   of a typical G 1,000.0.s random graph. (The                      of v toward vertices in ;
when V' has finally been emptied). The goal of this                         average times per run on a Sequent processor                     presumably desirable bl
procedure is to make C large while assuring that G R has                    are given in parentheses.)                                       such classes.
as many edges eliminated from it as possible, with the                                                                                          The key to making a
additional constraint that since Vo has to be in some                                                                                        borhood structure is th<
color class it might as well be in this one.                      substantial cost in running time. Its average of 107.9                     here is where we adapt
   To get a feel for the relative effectiveness and effi-         colors is also better than the results reported in Johri and               which constructs its coil
ciency of these three algorithms, let us first see how they       Matula for other successive augmentation algorithms,                       tine for generating lar
do on what has become a standard test case for graph              such as DSATUR With Interchange (111.4) and Smallest                       function has two compO!
coloring heuristics, the 1,000-vertex random graph. In            Last With Interchange (115.0).                                             classes, the second fav
the notation of Part I, this is G 1.000 . OS ' the 1,000-vertex      None of these algorithms, however, uses close to the                    (C l , ... , C k ) be a soluti
graph obtained by letting a pair {u, v} of vertices be an         optimal number of colors for G, ,000, o.s' which is esti-                  of edges from E both 01
edge with probability p = 0.5, independently for each             mated to be about 85 by Johri and Matula. (This is only                    the set of bad edges in
pair. Although unlikely to have much relevance to prac-           a heuristic estimate. All that can currently be said with                                    k
tical applications of graph coloring, such a test bed has         rigor is that x(G"ooo,os) ~ 80 with very high probabil-                    cost (11) = -    L ICil'
the pedagogical advantage that results for it seem to be          ity, as shown by Bollobas and Thomason.) It appears                                         i=1

stable (behavior on one graph of this type is a good              likely that, if we want to approach 85 colors, we will                        An important observ.
predictor for behavior on any other) and that different           need much larger running times than used by the typical                    that all its local minim:
heuristics yield decidedly different results for it. Papers       successive augmentation algorithms. Moreover, given                        To see this, suppose thai
that have used this graph as a prime example include              the narrow variance in results of such algorithms, as                      endpoint of one of the 1
Johri and Matula (1982), Bollobas and Thomason (1985),            typified by the histograms in Figure 2, the approach of                    that moving v from C
Morgenstern and Shapiro (1986), Chams, Hertz and de               performing multiple runs of anyone seems unlikely to                       Ck +'   reduces the cost
Werra (1987). (We shall subsequently consider a selec-            yield significantly better colorings even if a large amount                second component of tI
tion of other types of graphs, but the well-studied               of time is available. Thus, the way is open for computa-                   increasing the first by a
G 1.000 . 0 .S graph provides a convenient setting in which to    tion-intensive approaches such as simulated annealing.
introduce our ideas.)
   Figure 2 presents a histogrammatic comparison of the           2.2. Three Simulated Annealing Implementations
three algorithms on a typical G1.000,0.s random graph.            Despite the lack of traditional neighborhood search algo-                  Observe that this cost f
Although none of the three algorithms is, as defined, a           rithms for graph coloring, the problem has proved a                        the number of k of c
randomized algorithm, each depends, for tie-breaking if           surprisingly fertile area for simulated annealing imple-                   minimize this as a sid
nothing else, on the initial permutation of the vertices.         mentations. We will describe and compare three serious                     function. The use of s
By varying that permutation, one can get different re-            candidates.                                                                counted for more than I
sults, and the figure plots histograms obtained for the                                                                                      annealing, from the g
results of each for 100 different initial permutations.           2.2.1. The Penalty Function Approach                                       tioned before to pre
Note that each algorithm produces colorings within a              We begin with the historically first of the three, the one                 compaction (e.g., see
tight range, that the ranges do not overlap, and that RLF         with which we began our studies in 1983. This approach                     1983, Vecchi and Kirkr
is significantly better than the other two, albeit at a           was motivated in part by the success of RLF.                               Golden 1988). Note als(
                                                                                                          Graph Coloring by Simulated Annealing           /   383

                                   Problem-Specific Details. Consider the following                   classes the cost function is biased toward colorings that
                                   neighborhood structure, one that, as in the graph parti-           are unbalanced, rather than ones where all classes are
:TEX RANDOM GRAPH
                                   tioning implementation of Part I, involves infeasible              approximately the same size. Consequently, an optimal
                                   solutions and penalty functions. A solution will be any            solution with respect to this cost function need not use
                                   partition of V into nonempty disjoint sets                         the minimum possible number of colors, although in
                                   C" C2 ,··· , Ck , 1 ~ k ~ 1V I, whether the C; are legal           practice, this does not seem to be a major drawback.
                                   color classes or not. Two solutions will be neighbors if           Moreover, the bias may be profitable in certain applica-
                                   one can be transformed to the other by moving a vertex             tions. For instance, colorings for which ~ I C; 1 2 is
                                   from one color class to another. To generate a random              maximized are precisely what is needed in a scheme for
                                   neighbor, we will randomly pick a (nonempty) color                 generating error-correcting codes due to Brouwer et al.
                                   class COLD' a vertex VECOLD ' and then an integer i,               (1990), and our annealing software has been useful in
          125      I~O    I
                          135'
                              "!
                                   I ~ i ~ k + 1, where k is the current number of color              this application, as reported in that paper. (Aarts and
vlin)   SEQ (1.1 Min)
                                   classes. The neighbor is obtained by moving v to color             Korst (1989) describe an alternative cost function with
)rings found by running';          class C;. If i = k + 1 this means that v is moved to a             respect to which solutions of minimum cost do have the
LUR and SEQ for 100                new, previously empty class. If v is already in class C;           minimum possible number of colors, but their function
nutations of the vertices'.        we try again. Note that this procedure biases our choice           has other drawbacks.)
 ,5 random graph. (Thd,
                                   of v toward vertices in smaller color classes, but this is            To complete the specification of the problem-specific
l on a Sequent processor\'
                                   presumably desirable because it is our goal to empty               details in our penalty function implementation, we must
ses.)                              such classes.                                                      say how we generate initial solutions. One possibility
                                      The key to making annealing work using this neigh-              would be to start with all the vertices in a single class
                                   borhood structure is the cost function we choose, and              C I; the other extreme would be to start each vertex in its
~. Its average of 107.9'           here is where we adapt the general philosophy of RLF,              own unique one-element class. On the basis of limited
Its reported in Johri and          which constructs its colorings with the aid of a subrou-           experiments, an intermediate approach seems reason-
Igmentation algorithms,~           tine for generating large independent sets. Our cost               able, in which one assigns the vertices randomly to
Ige (111.4) and Smallest           function has two components, the first favors large color          CHROM_EST classes, where CHROM_EST is a
                                   classes, the second favors independent sets. Let II =              rough estimate of the chromatic number. The neighbor-
Never, uses close to the'          (C I , . . . , C k ) be a solution, and E;, 1 ~ i ~ k be the set   hood size returned is then CHROM_EST' I V I, a
:1 1,000,0.5' which is esti-:i     of edges from E both of whose endpoints are in C;, i.e.,           good estimate of the number of neighbors a solution will
ld Matula, (This is only           the set of bad edges in C;. We then have                           have toward the end of the annealing schedule. We did
1 currently be said with.                                                                             not follow this approach precisely, however. For our
                                                    k                     k
                                                                                                      G\,000,0.5 graph, we set CHROM_EST= 90, a reason-
",ith very high probabil c         cost(II) = -    L     I   C; 1
                                                                    2
                                                                        + L 2 C;
                                                                               1   I .   I   E; I·
  Thomason.) It appears                            ;=\                   ;=\                          able estimate, but then for simplicity we left it at tl1is
mch 85 colors, we will                                                                                value in our experiments with other graphs, even though
                                      An important observation about this cost function is
than used by the typical.                                                                             in some cases 90 was a substantial over or underesti-
                                   that all its local minima correspond to legal colorings.
hms, Moreover, given·;                                                                                mate. Given tl1at we were varying SIZEFACTOR any-
                                   To see this, suppose that E; is nonempty, and let v be an
 of such algorithms, as;                                                                              way, errors in neighborhood size were not deemed to be
                                   endpoint of one of the bad edges contained in E;. Note
gure 2, the approach of                                                                               significant, and fixing CHROM_EST left us with one
                                   that moving v from C; to the previously empty class
lone seems unlikely to'-                                                                              less parameter to worry about.
                                   Ck + I reduces the cost function because we reduce the
s even if a large amount';                                                                               Nevertheless, the effective neighborhood size (the
                                   second component of the cost by at least 2 I C; I while
ay is open for computa-"                                                                              number of neighbors that a near-optimal solution can
                                   increasing the first by at most
s simulated annealing.                                                                                have) can be substantially bigger than that for graph
                                   I C; I 2 - (( I C; I - 1) 2 + 12 ) = 2 I C; I - 2.                 partitioning in Part I (where it was simply the number of
ing Implementations                                                                                   vertices). Here, the higher the chromatic number, the
ighborhood search algo- '          Observe that this cost function does not explicitly count          bigger the effective neighborhood size gets. Assuming,
 problem has proved a              the number of k of color classes in II; we hope to                 as our experiments with graph partitioning suggest, that
ulated annealing imple-            minimize this as a side-effect of minimizing the cost              the number of trials we should perform at each tempera-
d compare three serious            function. The use of such indirect techniques has ac-              ture must be a sizeable multiple of this neighborhood
                                   counted for more than one practical success claimed for            size, we can see that we are in for much larger running
                                   annealing, from the graph partitioning problem men-                times than we encountered with graph partitioning: for
~pproach                           tioned before to problems of circuit layout and                    G I ,000, 0.5 the running times might blow up by a factor of
rst of the three, the one          compaction (e.g., see Kirkpatrick, Gelatt and Vecchi               90 or more!
 in 1983. This approach            1983, Vecchi and Kirkpatrick 1983, Collins, Eglese and                As with graph partitioning, however, the time for
cess of RLF,                       Golden 1988). Note also that for a given number of color           proposing and accepting moves is manageable. If we
 384   /   JOHNSON ET AL.

store the graph in adjacency matrix form and the color        Part I. (Limited experiments with higher starting tem-                          CHROM_EST= 100 (slJ
classes as doubly-linked lists, the time to propose a move    peratures yielded longer running times but no better                            ard value, although this h
is proportional to the sizes of the two color classes         solutions.) To further reduce running time, we used                             picture), TEMPTFACT,
involved, and the time to accept a proposed move is           cutoff with CUTOFF = 0.10.                                                      TOR = 2. So that more'
constant. (Our data structures are optimized for dense           For our termination condition, we set MINPER-                                can be seen, we used an il
graphs with relatively small color classes, as these are      CENT = 2 %, allowing for the likelihood that a certain                          than the value of 10 used
common in applications and are the main ones we study         small number of zero-cost moves will always be possible                         temperature 10 was rea
in this paper. For sparser graphs with larger color           and hence accepted, and set FREEZE_LIM = 5.                                     Trials) / 10,000 reached 91
classes, it may be more appropriate to represent the          Finally, rather than perform explicit exponentiation each                       picture, cutoffs were turm
graph in adjacency list form and maintain an array that       time we need the value e- t1 / T , we use the table-lookup                      manually once it was clea
specifies the color of each vertex. The average time for      method described in Part I for quickly obtaining a close                              The top display shows I
proposing a move would then be proportional to the            approximation. (This method is also used in our other                           sets in the current partiti
average vertex degree.)                                       two annealing implementations.) Running times were                               (the first data point), th(
                                                              then varied by changing the values of TEMPFACTOR                                 jumped from the initial I
 Penalty Function Local Optimization. Before we turn          and SIZEFACTOR.                                                                  and from then on it increa
 to the implementation details in the generic part of the                                                                                      peak of 233 before decli
algorithm, let us briefly examine how well this neighbor-     The Dynamics of Penalty Function Annealing. Fig-                                 Interestingly, this behavi(
hood scheme performs in the context of pure local             ure 3 presents "time exposures" of an annealing run                              movement of the "curren!
optimization. In our implementa~ion of local optimiza-        under this scheme on our G 1.000, 0.5 graph with                                 display, which is consiste
tion based on this scheme, we' limit ourselves to a                                                                                            this lack of correlation lie
maximum of 200 color classes, thus giving us at most                240 r - - - - - - - - - - - - : ; - - - - - - - - - - r - - - - - - - ,     "random neighbor." Re
200 I V I possible moves from any given partition. We          ~ 220
                                                               M
                                                                                                                                                nonempty color class and
start with a random assignment of the vertices to 200          ~    200                                                                         class to move. This intro
                                                               R
color classes, and a random permutation of the 200 I V I       o 180                                                                            bers of small classes. Sin
possible moves. We then examine each move in turn,             F 160
                                                               C
                                                                                                                                                size of the chosen class t
performing the move only if it results in a net decrease       2 140                                                                            temperatures, small classe
                                                               o
in cost. Once all 200 I V I moves have been considered,        ~ 120                                                                            they are filled. Indeed,
we re-permute them and try again, repeating this proce-             100                                                                          temperature at which 99 ~
dure until for some permutation of the moves, none is              25K                                                                           (here we start at roughl)
accepted. Then we know we have reached a locally                   20K                                                                           would have been fluctual
optimal solution and stop.                                     5R 15K                                                                            As the temperature drop~
                                                               ~ 10K
   For our standard GI,OOO.0.5 random graph, we per-                                                                                             that penalizes "bad edges
                                                               ~ 5K
formed 100 runs of this local optimization algorithm.          C      0
                                                                                                                                                ~up the number of colors
The results, although better than what was obtainable in       o                                                                               \edges for the cOmponenl
                                                               f -5K
practice by pure sequential coloring, were unimpressive:           -10K
                                                                                Penalty Function Annealing
                                                                                                                                              ~wards big color classes t
the average time per run was 37.3 minutes (slower than             -15K                                                                       l~Colors back down.
                                                                                                                                              "y

RLF) , but the median solution used 117 colors (worse                80                                                                       ~. The appearance of the
                                                               P
than both RLF and the much faster DSATUR algorithm).          R
                                                               E                                                                              'by a vertical line throu
                                                              C     60
No solutions were found using fewer than 115 colors.          E                                                                               "Current cost (middle (
                                                              N                                                                               "fc
Fortunately, this neighborhood structure is better for        T                                                                                '!n0notonically, there is
                                                              A     40
simulated annealing than for local optimization.              C
                                                              C
                                                                                                                                                illccurring slightly to the I
                                                              E
                                                              t 20                                                                                did not see in the time
Generic Details of Penalty Function Annealing. Al-            E
                                                              D                                                                                   'artitioning. Bumps of tl
though all our annealing implementations follow the
                                                                                        500            1000             1500           2000
                                                                                                                                                   ,f penalty function anne:
generic outline of Figure 1, certain parameters and rou-                                      (NUMBER OF TRIALS)/IO,OOO                                slope for the curve,
tines therein must be specified before the description of                                                                                            ange in acceptance rat,
any given implementation is complete. For penalty func-       Figure 3. Three views of the evolution of an annealing                                  ttom display.) Anneal
tion annealing, we obtained our starting temperature by                 run for a G 1.000. 0.5 graph under the penalty                              ,ight suggest that such
trial and error, discovering that a single initial tempera-             function annealing scheme. (The time at                                       n" (Kirkpatrick, Gela
ture usually sufficed for a given class of graphs. In the               which the first legal coloring was encoun-                                   ere is no good explanati
case of 0n.0.5 graphs, an initial temperature of 10 tended              tered is marked by a vertical line in all three                              ey can be exploited.
to yield an initial acceptance ratio between 0.3 and 0.4,               displays. Temperature was reduced by a fac-                                   The total running tin
which seemed adequate based on the experiments of                       tor of 0.95 every 20 data points.)                                        'bout 11 hours. This w(
                                                                                                      Graph Coloring by Simulated Annealing                /   385
 \lith higher starting                     OM_EST = 100 (slightly higher than our stand-         cantly had we used cutoffs and the lower standard initial
 ing times but no                  e      alue, although this has no significant effect on the   temperature of 10, but it is already less than the 17.9
  running time, we;                      re), TEMPTFACTOR = 0.95 and SIZEFAC-                    hours it took to perform 100 runs of RLF. (Recall that
                                           == 2. So that more of the total annealing process     RLF never used fewer than 105 colors, 3 more than we
 :on, we set MIN',                        e seen, we used an initial temperature of 96, rather   needed here). By further increasing the running time (via
   likelihood that a c'                   the value of 10 used in the later experiments. The     increased values for TEMPFACTOR and SIZEFAC-
 ~s will always be p                       rature 10 was reached when the Number of              TOR), still better colorings are obtainable by this
 ~t FREEZE_LIM'                          s)/lO,OOO reached 918. Also, for the sake of a full     approach. As we shall see in Section 2.4, it is possible
 Jlicit exponentiation'                  re, cutoffs were turned off and the run was stopped     with this approach to get colorings using as few as 91
   we use the table-Ioo                   ally once it was clear that convergence had set in.    colors, if one is willing to spend 182 hours.
 quickly obtaining a c:                  e top display shows the evolution of the number of
 , also used in our o'                   in the current partition. Note that by trial 10,000     2.2.2. The Kempe Chain Approach
 ;.) Running times w                     first data point), the number of sets has already       Preliminary reports of the penalty function implementa-
 ues of TEMPFA CTj.                      ed from the initial 100 to something close to 140,      tion and the results for it inspired Morgenstern and
                                        from then on it increases more or less smoothly to a     Shapiro to proposed the following alternative, which
                                           of 233 before declining to a final value of 102.      retains the cost function but makes a major change in the
 nction Annealing. E                    estingly, this behavior does not correlate with the      neighborhood structure.
 :s" of an annealing ,                  ement of the "current cost" presented in the middle
   G l,{lOO, 0.5 graph                 lay, which is consistently declining. The reason for      Problem-Specific Details. Solutions are now restricted
                                    's lack of correlation lies in our method for choosing a     to be partitions C 1 , . . . , C k that are legal colorings, i.e.,
                                   ,,~ndom neighbor." Recall that we pick a random,              are such that no edge has both endpoints in the same
                                 'bonempty color class and then a random member of that          class. (Note that this means that all the sets E; of bad
                                  class to move. This introduces a bias toward the mem-          edges are empty, and so the cost function simplifies to
                                  ~rs of small classes. Since a move always reduces the          just - I: ~= 1 I C; I 2.) In order to ensure that moves pre-
                                  size of the chosen class by one, this means that at high       serve the legality of the coloring, Morgenstern and
                                 lemperatures, small classes will tend to empty faster than      Shapiro go to a much more complex sort of move, one
                                  ~ey are filled. Indeed, had we started our run at a            involving Kempe chains.
                                  t~~perature at which 99 % of the moves were accepted              Suppose that C and D are disjoint independent sets in
                                 (liyre we start at roughly 75 %), the number of colors          a graph G. A Kempe chain for C and D is any
                                 '~~uld have been fluctuating between 30 and 40 or so.           connected component in the subgraph of G induced by
                                 ~§ the temperature drops, the part of the cost function         CUD. Let X Ll Y denote the symmetric difference
                                'that penalizes "bad edges" begins to take effect, driving       (X - Y) U ( Y - X) between two sets X and Y. The
                                 qp the number of colors until there are few enough bad          key observation is that if H is a Kempe chain for
                                 lldges for the component of the cost function that re-          disjoint independent sets C and D, then C Ll Hand
                               'wards big color classes to begin driving the number of           D Ll H are themselves disjoint independent sets whose
                                colors back down.                                                union is CUD. This suggests the following move gen-
                                   .The appearance of the first legal coloring is marked         eration procedure: Randomly choose a nonempty color
                              ,by a vertical line through the display. Although the              class C and a vertex v E C, as in the penalty function
                                current cost (middle display) declines more-or-less              approach. Then randomly choose a nonempty color class
                                monotonically, there is a definite bump in the curve             D other than C, and let H be the Kempe chain for C
                                occurring slightly to the left of that line, a bump that we      and D that contains v. Repeat the above procedure until
                                did not see in the time exposures of Part I for graph            one obtains C, v, D and H such that H* CUD (i.e.,
                               partitioning. Bumps of this sort regularly occur in runs          such that H is not "full"), in which case the next
               1500
                                of penalty function annealing. Unlike the other changes          partition is obtained by replacing C by C Ll Hand D by
IALS)/JO.OOO                   in slope for the curve, they do not reflect a similar             DLlH in the current one. (Using a full Kempe chain in
                               change in acceptance rate. (The latter is depicted in the         this operation simply changes the names of the two
volution of an annealing       bottom display.) Annealers with physics backgrounds               colors, a meaningless change, which is why we ignore
graph under the penalty        might suggest that such bumps indicate "phase transi-             such moves.)
scheme. (The time at           tion" (Kirkpatrick, Gelatt and Vecchi). Unfortunately,               This procedure appears to be substantially more ex-
I coloring was encoun-         there is no good explanation of why they arise or whether         pensive than the move generation procedure in the penalty
 vertical line in all three    they can be exploited.                                            function approach, and it is. It also makes substantially
e was reduced by a fac-             The total running time for the time exposure was             bigger changes in the solutions, however, and so may be
data points.)                 about 11 hours. This would have been reduced signifi-              worth the extra effort. Moreover, it is not exorbitantly
386   /   JOHNSON ET AL.

                                                                  350
expensive, at least for dense graphs. For such graphs the                                                                       4 results from the fact th:
                                                             N
color classes tend to be small, and so the following         I!t 300                                                            ently with acceptance per
                                                             B
technique can find the Kempe chain H relatively quickly.     Ii: 250                                                            Whereas the initial teml
Whenever a new vertex u is added to H (including the         ~ 200                                                              acceptance rate under the
first vertex LJ), we scan the members of the other color                                                                        a 99% rate. Thus, much (
                                                             6 150
class that are not yet in H and add to H each one that is    L
                                                             o                                                                  at too high a temperature
                                                             R 100
adjacent to u. Furthermore, we use two auxiliary tables      S                                                                  temperature T = 4, whid
                                                                   50
to help us whenever possible avoid the wasted time of                                                                           acceptance ratio of 70 %
constructing full Kempe chains that must be abandoned.           -2K    ~------------------
                                                                                                                                function approach, we <
One stores for each pair C, D the time at which they         C -4K                                                              number of colors as we
                                                             U
were last discovered to have a full Kempe chain; the         R                                                                  Note also that the curve
                                                             ~ -6K
other stores for each C the time at which it was last        N                                                                  "current cost" are simil:
                                                             T
modified. When C and D are first chosen, we check to         C -8K                                                              tion approach the corres
                                                             0
see whether we have seen a full Kempe chain for them         S
                                                             T -10K                                                             tially. There the number I
                                                                          Kempe Chain Armealing
since the last time they were modified, and if so, aban-                                                                        the cost declines, here t
                                                                 -12K
don their further consideration immediately.                                                                                    values and then undergo <
   To complete the specification of the problem-specific     p
                                                                  100                                                           chain implementation, Ii1
                                                             E
details of the Kempe chain approach, we must say how         R     80                                                           tion approach, is biase<
                                                             C
instance "size" is determined and how initial solutions      E
                                                             N                                                                  small color classes for
                                                             T     60
are generated. We perform random sequential colorings        A
                                                                                                                                move is roughly as like
                                                             C
for both purposes. When an instance is read, we perform      C    40                                                            chosen class as to decrea
                                                             E
a random sequential coloring, and return the size K I V I,   P
                                                             T                                                                  to empty at high tempera
                                                             E    20
where K is the number of colors used in the coloring. A      D                                                                  ber is high rather than 10
second random sequential coloring is performed each                               500            1000             1500   2000       A third observation a
                                                                                        (NUMBER OF TRIALS)!I ,000
time a new initial solution is requested.                                                                                       Figure 4 is that the soh
                                                             Figure 4. Three views of the evolution of an annealing             percentage of accepted I
Kempe Chain Local Optimization. As with the penalty                                                                             penalty function run of
                                                                       run for a G UJOO ,O.5 graph under the Kempe
function approach, the Kempe chain approach can serve                                                                            annealing implementatior
                                                                       chain annealing scheme. (The temperature
as the basis for a local optimization algorithm. Here,                                                                          solution value is not sel
                                                                       was reduced by a factor of 0.95 every 20 data
because we are restricted to legal colorings, we limit the                                                                       quite low, In the run 01
                                                                       points.)
total allowable number of colors to 150, yielding                                                                                coloring does not appear
150 I V I possible moves. Initial solutions are generated                                                                       to about 0.5%, For the 1
by random sequential colorings as just specified. Other-                                                                         acceptance rate still hm
wise, the details are the same as for penalty function       function approach). For comparison purposes, we also                number of colors is fin
local optimization, as outlined previously. The results      set the neighborhood size to the same 100,000 value                attributable to the topog
were also similar (and similarly mediocre). The average      used in the previous run, and used the same starting               particular the structure 0
running time over 100 runs was 33.3 minutes (slightly        temperature T = 96. A first observation is that the curves          colorings. Such a colori
better than for the penalty function approach but still      are significantly more irregular than those for penalty            Kempe changes that impr
much slower than RLF), and the median number of              function annealing, For the most part, this may be                 it the same) than it will
colors was again 117.                                        attributable to the reduced value of SIZEFACTOR, since              ally change color withou
                                                             this means that each data point represents 1,000 rather            moves under the penalty
The Dynamics of Kempe Chain Annealing. Before                than 10,000 trials, and so successive data points may be               Moreover, in explanal
describing the generic parameters governing the start and    correlated more closely. There may, however, be a                   cursion in the acceptanc(
finish of a run, let us compare the operation of Kempe       different reason for the extreme excursion in the accept-           likely to have far more
chain annealing to the penalty function approach. Figure     ance rate curve. Such excursions occur in the tails of              This inhomogeneity of tl
4 presents "time exposures" for Kempe chain anneal-          other Kempe chain runs, but at random places (unlike                ac(;ep,tarlce rate at conver
ing, analogous to those in Figure 3 for the penalty          the regularly occurring smooth bump in the middle of                   run, going as high as
function approach. All parameters except SIZEFACTOR          the "current cost" curve for penalty function annealing             the next, This makes it (
were given the same values as in the penalty function        in Figure 3), Here the excursion seems attributable to the          gence parameters of our
run; because of the greater expense of the moves here,       topography of the Kempe chain solution space, as we                 vative in the experim<
we reduced SIZEFACTOR from 200 to 20 (and the run            shall hypothesize in more detail below.                              MINPERCENT = 15 %
still took 18 hours, as opposed to the 11 for the penalty       A second difference between the runs in Figures 3 and            up to 10 before termina
                                                                                                   Graph Coloring by Simulated Annealing            /   387
                                 results from the fact that temperature correlates differ-     temperatures by manual trial and error, observing as
                                ~$t1y with acceptance percentage under the two regimes,        with penalty function annealing that the same initial
                                , ereas the initial temperature T = 96 yields a 75 %           temperature seems to work well across entire classes of
                               ;~~~eptance rate under the earlier approach, here it yields     graphs. For random graphs with p = 0.5, we use an
                               ~99% rate. Thus, much of the time in Figure 4 is wasted         initial temperature of T = 5, which generally yields an
                                  kt too high a temperature. If we instead choose a starting   initial acceptance rate between 50 % and 80 %. As with
                                  femperature T = 4, which yields approximately the same       penalty function annealing, we use CUTOFF = 0.10 in
                                  ~cceptance ratio of 70 % as did T = 96 for the penalty       our main experiments.)
                                 function approach, we converge to roughly the same               A final observation about the run in Figure 4 (and
                                  Il~mber of colors as we do here, but in only six hours.      presumably the most important) is that the numh"f of
                                  Note also that the curves for "number of colors" and         colors to which the run converges is 94, as oppC·" to
                                ·"current cost" are similar, whereas in the penalty func-      101 for the penalty function approach. The running time
                               · lion approach the corresponding curves differ substan-        is somewhat longer, 17.9 hours versus 11, but in 17.9
                               rBallY. There the number of colors initially increase while     hours the fewest number of colors we have been able to
                               'the cost declines, here they both jump quickly to high         obtain with the penalty function approach, even using
                                ·values and then undergo correlated declines. (Our Kempe       cutoffs, is only 98. In the 182 hours it takes penalty
                                 chain implementation, like the one for the penalty func-      function annealing to find a 9l-coloring, Kempe chain
                                 tion approach, is biased toward choosing vertices in          annealing can find one using only 89 colors, and, as we
                                 small color classes for recoloring. Here, however, a          shall see in Section 2.4, it can do even better with just a
                                 move is roughly as likely to increase the size of the         bit more time. Thus, it appears that the extra complexity
                                  chosen class as to decrease it. Thus, classes do not tend    of the neighborhood structure for Kempe chain annealing
                                 to empty at high temperatures, and the equilibrium num-       can more than pay for itself, and we shall confirm this in
                                 ber is high rather than low.)                                 the more extensive experiments that follow.
J                                    A third observation about the Kempe chain run of
RIALS)/! ,000
                                 Figure 4 is that the solution cost converges while the        2.2.3. The Fixed-K Approach
;:volution of an annealiIi       percentage of accepted moves is still rather high. The        Our final annealing implementation is derived from a
  graph under the Kern'          penalty function run of Figure 3 is typical of most           paper by Chams, Hertz and de Werra, and solves a
heme. (The temperatur            annealing implementations we have seen in that the best       slightly different problem. Instead of attempting to mini-
~tor of 0.95 every 20 da         solution value is not seen until the acceptance rate is       mize the number of colors used in a legal coloring, this
                                 quite low. In the run of Figure 3, the first legal 102-       approach attempts to minimize the number of monochro-
                                 coloring does not appear until the acceptance rate drops      matic edges in a not-necessarily-legal coloring with a
                                 to about 0.5%. For the Kempe chain run, however, the          fixed number of color classes.
                                 acceptance rate still hovers around 7% when its best
 lfison purposes, we als:        \lumber of colors is first encountered. This is largely       Problem-Specific Details. Given a graph G = ( V, E)
 the same 100,000 valu           attributable to the topography of the solution space, in      and a number of colors K, the solutions are all partitions
I used the same startin         particular the structure of the neighborhoods of "good"        of V into K sets (empty sets are allowed), and the cost
 ervation is that the curve      colorings. Such a coloring is likely to have far more         of a solution is simply the total number of edges that do
lr than those for penalt        Kempe changes that improve its "cost" (or at least leave       not have endpoints in different classes (the "bad edges").
most part, this may b,           it the same) than it will have vertices that can individu-    A partition IT 2 is a neighbor of a partition IT I if the two
: of SIZEFACTOR, sine,          ally change color without negative effect (the analogous       partitions differ only as to the location of a single vertex
t represents 1,000 rathe        moves under the penalty function approach).                    v, and v is an endpoint of a bad edge in IT I .
~ssive data points may b'           Moreover, in explanation of the abovementioned ex-            Note that here the neighbor relation is not symmetric;
re may; however, be             cursion in the acceptance rate, some good colorings are        in particular, a legal coloring has no neighbors because it
~ excursion in the accept       likely to have far more "good" neighbors than others.          has no bad edges. This is of course no problem, for if
Jns occur in the tails 0        This inhomogeneity of the solution space means that the        ever the annealing process finds a legal coloring, there is
at random places (unlik         acceptance rate at convergence can vary wildly from run        no point in proceeding any further. Limited experimenta-
1 bump in the middle 0          to run, going as high as 15 % one time and as low as 5 %       tion indicates that this neighborhood structure is much
enalty function annealing       the next. This makes it difficult to fine-tune the conver-     more effective than the less-restrictive one in which
1 seems attributable to the:    gence parameters of our implementation. To be conser-          v need not be an endpoint of a bad edge. (The less-
in solution space, as we,       vative in the experiments to be reported, we set               restrictive neighborhood was essential in our penalty
I below.                        MINPERCENT = 15 % and allow jreezecount to go                  function adaptation, since the goal was to reduce the
 the runs in Figures 3 and      up to 10 before terminating. (We again set our initial         number of color classes, which might entail emptying
388   /   JOHNSON ET AL.

out a class even though it contained no bad edges.) To         ing) is found, the "converged" tail of the curve is
choose a random neighbor, we first choose a random             truncated, as explained before. The one fact of note is                        Progn
"bad vertex" v (v is bad if it is the endpoint of a bad        that, with SIZEFACTOR = 4, TEMPFACTOR = 0.95                                      1.(
edge), and then choose a random new color class for v          and cutoffs turned off, runs with K fixed at 96, 97 and
                                                                                                                                              Functi
from among the K - I that do not contain v.                    98 all succeeded (in roughly 11.8 hours), whereas a run
   The remaining problem-specific details are as follows:      with K = 95 took 13.9 hours and failed to find a legal                             Vi:
The size parameter is set to K I V I, reflecting a worst       coloring. Thus, this approach too seems to dominate                                C i:
case situation in which all vertices are bad. The initial      penalty function annealing, which took 11.1 hours to                               B i:
solution is a random partition into K sets.                    find a 101-coloring. This domination is not complete,                              K·
                                                               however, as we shall see in Section 2.4 when we com-                               (Tl
Fixed-K Local Optimization. A local optimization al-           pare the two approaches with cutoffs enabled and with
                                                                                                                                                  an
gorithm based on the fixed-K neighborhood structure            their standard fixed starting temperatures in place.
and cost function can be implemented in much the same             Moreover, the domination assumes that one knows in                              1.
way as we implemented local optimization versions of           advance which values of K go with a given (SIZEFA C-
the two previous approaches. There are just K I V I            TOR, TEMPFACTOR) pair. The extra experimenta-
possible moves, which we cycle through as before. Each         tion to match up these parameters provides fixed-K
run starts with a random partition into K color classes.       annealing with an additional overhead not present for the
   The evaluation of an algorithm of this type is, how-        previous two approaches. We shall have more to say
                                                                                                                                                  2.
ever, a different matter. For this local optimization          about this overhead after we present our more detailed
approach to be useful, it must reach a solution of cost 0      experimental results.
(i.e., a legal coloring). Thus, the relevant question to ask
                                                               2.3. Exhaustive Search Alternatives                                                 3.
is what is the minimum K for which such a success
                                                               As indicated, the domain of applicability for our simu-
                                                                                                                                                   4.
occurs regularly. Unfortunately, the answer is quite dis-
couraging. We performed 100 runs each for various              lated annealing implementations consists of those situa-
values of K (this was not too burdensome, as the               tions where the computing time available is far larger                              5.
running times were much smaller than those for the two         than that required by traditional successive augmentation                           6.
previous approaches, less than 90 seconds per run). The        heuristics like RLF, DSATUR and SEQ. Annealing is
first value of K for which any of the 100 trials pro-          not the only way to apply large amounts of time to the
duced a successful coloring was K = 141, well above the        problem, however, and in this section we describe           Figure 5. Branch-and-t
number of colors in the worst coloring we ever found           two major competitors in the arena of multihour                       data structun
using sequential coloring. The success rate did not reach      computation.                                                          adjacencies. )
50% until K = 150. Thus, simulated annealing has far              The first is exhaustive search. On seeing reports of
more to redeem for this approach than for the previous         100 + hour running times, the reader might be excused       based on ideas first Sl
two.                                                           for asking why, with all that time available, one does      augmented here by a fin
                                                               not simply use exhaustive search and find an optimal        invoked when the set of
Generic Details and the Dynamics of Fixed-K                    coloring? As we shall see, however, even when using          is sufficiently small. TI
Annealing. In performing fixed-K annealing, we again           branch-and-bound techniques to prune the search space        in Figure 7. To underst,
set the initial temperature manually (T= 2.0 yields a          dynamically, this approach becomes infeasible well be-       RLF one can view the
50-60% initial acceptance rate for the random graphs           fore 100 vertices. In particular, we implement the           color class as a heurist
we tested), and cutoffs are used with CUTOFF = 0.10.           branch-and-bound algorithm outlined in Figure 5, which        solution to the follow in
For termination we use MINPERCENT= 30% (large                  includes most of the obvious shortcuts (e.g., see Brelaz)     independent set C cor
numbers of O-cost moves are likely to exist), and quit         and seems competitive with the best previous implemen-        uncolored vertices sue
when either a solution with no bad edges is achieved           tations. Figure 6 reports the results of running this         VE V' - c} I is maxirr
or the freezecount reaches 10. Running time is                 algorithm on random Gn • O.5 graphs. Three samples each     . edges in the residual g
adjusted, as before, by varying SIZEFACTOR and                 were generated for n = 40,45, ... ,85,90. As can be         jndicate that this is a
TEMPFACTOR.                                                    seen, the growth rate in running time is clearly exponen-      finding an independent
   Time exposures for this approach, analogous to those        tial, and only two of the three 85-vertex samples (and        that it tends to approxi
in Figures 3 and 4, will be omitted, as they do not            none of the 90-vertex samples) finished within 1,000           denote the algorithm i
display any of the anomalies we observed for penalty           hours.                                                       :mization subproblem i
function and Kempe chain annealing. That is, they look            Our second alternative is more competitive: a parame-     .one can view XRLF (-
remarkably like the standard curves seen in Kirkpatrick,       terized generalization of RLF that can make productive         set to 0) as providing
Gelatt and Vecchi and in Part I of this paper, except that,    use of long running times when the time is available.           RLF*. Depending on
in those cases where a O-cost solution (i.e., legal color-     This algorithm, which we shall denote by XRLF, is            SETLIM, TRIALNU,
                                                                                                           Graph Coloring by Simulated Annealing        /   389

 ~d"   tail of the curve
 . The one fact of not                           Program CHROM_NUM(G) (Given a graph G == (V,E), outputs X(G).)
, TEMPFACTOR ==                                     1. Output COLOR(V,<j>, IV lO).
ith K fixed at 96, 97
1.8 hours), whereas a.                           Function COLOR(U,C,B,K)
 and failed to find a r                             U is the set of as yet uncolored vertices.
I too seems to domi                                 C is a set of pairs (u,i), where u e V - U and i, 1 :;;; i:;;; Ivl is a color.
 hich took 11.1 hour'                               B is the number of colors in the best legal coloring seen so far.
nination is not compl"                              K < B is the number of colors used in C.
~ction 2.4 when we cd
                                                    (This function returns the minimum of B and the fewest number of colors in
 cutoffs enabled and wi
                                                    an extension of C to a full legal coloring.)
nperatures in place.
ssumes that one knows t                             1. If IU I == 1, let u be the single member of U, and do the following:
 with a given (SIZEFA                                    1.1. If there is any color j, 1 :;;; j :;;; K, such that no vertex adjacent to u
  The extra experimen                                          has color j, return K.
meters provides fixed';                                  1.2. If K + 1 < B, return K + 1.
erhead not present for t                                 1.3. Return B.
  shall have more to s
lresent our more detail                             2. Otherwise, choose a u e U that is adjacent to already colored vertices with the
                                                         maximum number of different colors, breaking ties in favor of vertices that
                                                         are adjacent to the most as yet uncolored vertices.
,rnatives                                           3. If u is adjacent to B-1 colors, return B.
Jplicability for our simu'                          4. For each color j, 1 :;;; j :;;; K, to which u is not adjacent, do the following:
 s consists of those situa;                              4.1. SetB = COLOR(U - {u},C U {(u,j)},B,K).
le available is far large'
                                                    5. If K < B-1, setB = COLOR(U - {u},C U {(u,K + l)},B,K + 1).
I successive augmentatio'
                                                    6. ReturnB.
. and SEQ. Annealing i;
e amounts of time to th
:lis section we describ       Figure 5. Branch-and-bound algorithm for finding X(G). (In the implementation, U and C are maintained in a global
he arena of multihou                    data structure to which pointers are passed. Data structures are also maintained for vertex degrees and color
                                        adjacencies.)
 :h. On seeing reports a
  reader might be excused!                                                                             1000    ~------------------;r---,
                              based on ideas first suggested by Johri and Matula,
 time available, one doe'     augmented here by a final "exact coloring" phase that is                   100         Branch and Bound
 rch and find an optimal'     invoked when the set of vertices remaining to be colored
 wever, even when using       is sufficiently small. The details of XRLF are sketched              T 10
                                                                                                   M
 ) prune the search space;    in Figure 7. To understand what is going on, note that in            E
                                                                                                   I
 :omes infeasible well be~    RLF one can view the process of constructing the next                N

 dar, we implement            color class as a heuristic attempt to find a near-optimal            ~      .1
                                                                                                   U
 Hined in Figure 5, which     solution to the following NP-hard subproblem: Find an                R
                                                                                                   S     .01
 ortcuts (e.g., see Brelaz)   independent set C contained in the current set V' of
  best previous implemen-     uncolored vertices such that 1{{u,v}eE: ueC and                           .001

  results of running this     ve V' - C} I is maximized, and hence the number of                       .0001
lphs. Three samples each      edges in the residual graph is minimized. (Experiments                           40    50           60        70     80       90
                                                                                                                              NUMBER OF VERTICES
 , ... , 85, 90. As can be    indicate that this is a slightly better goal than simply
: time is clearly exponen-    finding an independent set C of maximum size, a goal                Figure 6. Running times for brand-and-bound on Gn • D.5
   85-vertex samples (and     that it tends to approximate anyway.) If one lets RLF*                        random graphs.
;) finished within 1,000      denote the algorithm in which the residual edge mini-
                              mization subproblem is solved optimally at each step,               from ones that are even weaker than RLF all the way up
'e competitive: a parame-     one can view XRLF (with the parameter EXACTLIM                      to RLF* itself.
hat can make productive       set to 0) as providing a full range of approximations to               Algorithm XRLF constructs a new color class C by
;n the time is available.     RLF*. Depending on the values of the parameters                     repeating the following experiment for TRIALNUM
111 denote by XRLF, is        SETLIM, TRIALNUM and CANDNUM, these range                           iterations and then taking the best result: Initially all
390    /   JOHNSON ET AL.

uncolored vertices are candidates and set C is empty. If      tions for graph coloring and their competitors. Our
the number of remaining candidates is less than               experiments cover a variety of types and sizes of graphs,                Program
SETLIM, use exhaustive search to find the best exten-         and we discover that the approach of choice can depend                    1. Set R =
sion to C. If there are more than SETLIM candidates           strongly on the type of instance in question, and how                             (if
and C is empty, choose a random candidate, add it to C,       much computing time is available. The first set of exper-                 2. While
and declare all its neighbors to be noncandidates. If C is    iments covers the G 1,000,0.5 graph that has been our
                                                                                                                                                2.
not empty, randomly sample CANDNUM candidates,                standard example so far, As hinted, these experiments
let v be one that is adjacent to the most uncolored           paint a rather bleak picture of annealing (although, as we                3. Output
noncandidates, add v to C, and declare all neighbors of       shall see subsequently, not necessarily a typical one),
v to be noncandidates. (When TRIALNUM = 1, the                                                                                          Function
first vertex chosen is actually one of maximum degree,        2.4.1. Random p = 0.5, 1,000-Vertex Graphs
                                                                                                                                        1. Set bei
as in RLF, although when more trials are performed,            For the G 1,000, 0.5 graph that has been our standard                            v(
random choices seem to do better. The algorithm of            example, Figure 8 illustrates the tradeoff between run-                   2. IfTRI_
Figure 7 also contains an optimization to handle the case     ning time and the number of colors for the four main                               aI
when TRIALNUM is so large that exhaustive search              approaches we have been considering (penalty function                     3. Ifmin
would be faster than repeated trials.) Within this basic      annealing, Kempe chain annealing, fixed-K annealing,
                                                                                                                                        4. ForTJ,
algorithmic structure, RLF is obtained, at least approxi-      and algorithm XRLF). Note that for all approaches,
mately, by setting (EXACTLIM, SETLIM, TRIAL-                   reducing the number of colors used requires substantial                           4
NUM, CANDNUM) = (0, 0, 1, N), where N is suffi-                increases in running time (effected by altering the appro-
ciently large that all vertices are likely to be considered   priate algorithmic parameters). From this picture, we
as candidates in Step 4.3.2. RLF* is obtained by setting      can see that XRLF clearly dominates all three ap-
EXACTLIM = a and SETLIM = N. (For random                      proaches based on annealing, and Kempe chain anneal-                               4
0n.O.5 graphs, this is feasible for N as large as 250, if      ing clearly dominates penalty function annealing. The
                                                                                                                                                   4
one uses a tightly coded implementation of Step 4.3.1         comparison between penalty function and fixed-K an-
that avoids considering any subset more than once.)            nealing is less clearcut, with an apparent crossover oc-
   We point out, however, that even though the limiting        curring at 92 colors. (Conclusions based on running time
algorithm RLF* solves an NP-hard problem as a subrou-         differences of less than a factor of two are somewhat
tine, it is not guaranteed to find optimal colorings.         suspect, however, given that our annealing implementa-
Constructions in Johnson can be modified to show that,         tions were not thoroughly optimized.)
as with the simpler heuristics mentioned earlier, RLF*            A more detailed presentation of the data is presented
can in the worst case use numbers of colors that are           in Table I, which gives for each of the approaches the
arbitrary multiples of the optimal number. Nevertheless,      computing time needed to find legal colorings with spec-
as we shall see, even approximations to RLF* can do            ified numbers of colors, (For co~mparison, we also in-
well in practice, and our use of exhaustive search to          clude the median and best number of colors for 100 runs
finish up the coloring can make up for some of RLF*'s          of RLF, together with the time required for 1 and 100
drawbacks. In particular, for the G 1•000 . 0.5 random         runs, respectively, and the percent of times the best
graph we have been considering, XRLF with                      value occurred in the 100 runs. Since only 100 runs were
(EXACTLIM, SETLIM, TRIALNUM, CANDNUM)                          performed, the value quoted for" best" may not be very
(70, 63, 640, 50) finds 86-colorings in roughly 68             robust unless the percentage of occurrence is high
hours, substantially outperforming all our annealing          enough. It is clear, however, that the 17.9 hours needed
implementations.                                               for 100 runs of RLF can be more productively put to use
   In the next section, we examine more carefully the          by any of the other four algorithms.) All annealing                        5. Outpl
tradeoffs between running time and the quality of solu-       parameters except TEMPFACTOR and SIZEFAC-
tion for the graph coloring heuristics we have discussed,      TOR (TF and SF in Table I) were fixed as described in        Figure 7. The Algoritl
and how they depend on the type and size of graph in          Section 2.2. The values of the latter two parameters are                XRLF, as d
question. We report on experiments both with random           given in parentheses, with TEMPFACTOR represented                       found.)
0n,0.5 graphs and with graphs of distinctly different          by a shorthand that emphasizes the fact that halving the
character. As we shall see, the dominance of XRLF for         cooling rate should approximately double the running
   °
the 1,000,0.5 graph is not necessarily typical.               time, as should doubling SIZEFACTOR (an effect
                                                              studied in more detail in Part I). To be specific, if the
                                                                                                                            values taken for i =
                                                                                                                            0.9025, 0.95, 0.9747, (
2.4. Experiments in Graph Coloring                            code is i, TEMPFACTOR is approximately 0.95(1/i),             For XRLF, paramete
                                                                                                                            Were fixed at 63 and
In this section, we report more extensively on our exper-     representing an i-fold decrease in the cooling rate over
                                                                                                                            XRLF[ i, j] indicatin
imental comparison of the three annealing implementa-         the base of TEMPFACTOR = 0.95, (The precise
                                                                                                        Graph Coloring by Simulated Annealing    /   391

their competitors. Ou>
pes and sizes of graphs;                      Program XRLF(G) (Given graph G = (V.E), outputs an upper bound on X(G).)
 h of choice can depen)                       1. Set R = V, K = 0
: in question, and ho.                               (in what follows, GR is the subgraph of G induced by R).
:. The first set of expe                      2. While I R I > EXACTLIM. do the following.
lph that has been 0\1;
lted, these experiment                                2.1. Set R = R - IND_SET(GR) and K = K + 1.
lealing (although, as Wi                      3. OutputK + CHROM_NUM(GR ).
sarily a typical one).
                                              Function IND_SET(H) (Given graph H = (U,F). returns an independent set c* ~ U.)
·Vertex Graphs
                                              1. Set best = -1, C* = Co = <\>. and let D min and D max be the minimum and maximum
  las been our standard \                             vertex degrees in H.
  : tradeoff between run-'.
                                              2. If TRIALNUM = 1 and I U I >SETUM, let V max be a vertex of degree D max in H,
  llors for the four mainl,
                                                      and let Co = {v max}'
  lering (penalty function?
                                              3. Ifmin{TRIALNUM,SETUM+D min }? I U I ,setSETUM= I U I andTRIALNUM=1.
  ng, fixed-K annealing,.
                                              4. For TRIALNUM iterations, grow a trial independent set C as follows:
  tat for all approaches,'
  sed requires substantial'                           4.1. If Co ;c<\>. set C =C o, X= {u E U: {vmax'u} E F}.
  d by altering the appro- \.                              Else if I U I > SETUM, choose a random vertex v E U and
  From this picture, we:                                       set C={v},X={u E U: {v,u} E F}.
  )minates all three ap- (                                 Else set C =X =<\>.
  d Kempe chain anneal-
                                                      4.2     Let W = U - (C u X) (the set of vertices still eligible for C).
  mction annealing. The
  Iction and fixed-K an-                              4.3. While W is not empty, do the following:
   apparent crossover oc-                                        4.3.1. If I wi -::;'SETUM, do the following:
  , based on running time                                                     Use exhaustive search to find a set W' ~ W that maximizes
    of two are somewhat
                                                                                        I ({u,v}EF:uEWandvEU-(CuW')} I
   annealing implementa-
                                                                              SetC=CuW.
 led.)
                                                                              If I {{u, v} E F: U E C and v E U -C} I > best,
 )f the data is presented
                                                                                       set C* =C and
 I of the approaches the
                                                                                       set best = I {{U, v} E F : U E C and v E U - C} I
 sal colorings with spec-
 )mparison, we also in-                                                       Exit loop beginning with statement 4.3.
 r of colors for 100 runs                                        4.3.2. Set bestdegree=-I, cand = <\>.
 required for 1 and 100                                                 For CANDNUM iterations, do the following:
 ~ent of times the best
                                                                              Choose a random vertex U E W.
  nce only 100 runs were
                                                                              Lets(u)= I {{u,v}EF:vEX} I.
  'best" may not be very
                                                                              If s (u) > bestdegree, set bestdegrcc = s (u) and cand = u.
 )f occurrence is high
 • the 17.9 hours needed                                         4.3.3. Set C = C u {candY, X =X u {v E W: {cando v} E F} •
   productively put to use                                                   and W=W-X-{cand}.
 rithms.) All annealing                       5. Output C*.
TOR and SIZEFAC-
 re fixed as described in       Figure 7. The Algorithm XRLF with parameters EXACTLIM, SETLIM, TRIALNUM and CANDNUM. (Although
tter two parameters are                   XRLF, as described, outputs only the number of colors used, it is easily modified to produce the coloring
 )FACTOR represented                      found.)
he fact that halving the
 Iy double the running
'iFACTOR (an effect             values taken for i=0.25,O.5,I,2,4,8 are 0.8145,                     EXA CTLIM = j. Typically, we chose EXA CTLIM to
   To be specific, if the       0.9025,0.95,0.9747,0.9873 and 0.99358, respectively.)               be either 0 or the maximum value for which
 pproximately 0.95(1/i),        For XRLF, parameters SETLIM and CANDNUM                             CHROM_NUM( ) could be expected to terminate in
11 the cooling rate over        were fixed at 63 and 50, respectively, with an entry                reasonable amounts of time (in this case, EXACTLIM =
= 0.95. (The precise            XRLF[ i, j] indicating that TRIALNUM = i and                        70), and for both options we adjust running times by
392        /     JOHNSON ET AL.

     300                                                                               chain annealing, and XRLF are for the most part based            threshold is reached, no
                                                                                       on one or two runs for each parameter setting. We report         the threshold, an occas
     250                                                        Kempe     ain
                                                                                       the average running time, and give for the number of             Once past it, legal colc
                                                                                       colors the smallest integer k such that k or fewer colors        runs. (This at least he],
     200
                                                                                       were used on more than half the runs. Here the one               The table entries com
 H
 o                                                                                     exception is marked by an asterisk: for penalty function         settings for the best SuCi
 W 150
 S                                                                                     annealing, the [2,64] parameter setting yielded one 91-          50% or greater are deet
     100                                                                               coloring and one 92-coloring. Since fixed-K annealing,                Another observation
                                                                                       unlike the other algorithms, does not produce legal col-          when raw machine sp'
      50                                                                                                                                                 running times appear to
                   Penalty Function
                                                                  XRLF
                                                                                       ors when it fails, it is more important to know how likely
                                                                                       it is to succeed for a given choice of parameters. Thus,          reported by Chams, Hel
           100      98         96        94       92       90      88           86     we typically performed more runs for it. Table I indi-            more difficult values of
                                      NUMBER OF COLORS
                                                                                       cates the fraction of successful runs for each listed             1.8 hours for a 98-col,
Figure 8. Tradeoffs between time and colors for a                                      parameter setting; the entry (a, b) specifies that b trials       processor used by Cham
                                                                                       were performed, of which a resulted in legal colorings.           which should be four
          G,,000,0.5 random graph.
                                                                                          If the last entry in a column has a parenthesized              Sequent Balance 21000
                                                                                       running time, this indicates that the given coloring was          explanation is that the '
letting TRIALNUM increase by factors of 2. (Note that                                  never successfully constructed for any parameter choice,          al. seem to have been 0
increasing EXACTLIM from 0 to 70 does not always                                       with the reported run being the longest attempted. In             values of K.)
have a significant effect on running time because the                                  general, the entries in the table are for the parameter               Before passing on to
residual graph on which CHROM_NUM( ) is called                                         settings that generated the given colorings in the least          G ',000, 0.5 random graph
need not have the full 70 vertices.)                                                   amount of time. (We typically tested nearby values for            modifies it to take adv<
   Since all these approaches involve randomization, they                              TEMPFACTOR and SIZEFACTOR, although we did                        of such graphs. Bollob
need not generate the same number of colors on every                                   not study the parameter space exhaustively.) Note that             alternative approximatic
run, even when the parameter values are fixed. Since we                                with fixed-K annealing and a given fixed K, the results           tail probabilities to pw
were interested only in general trends, the results sum-                               often passed through three phases as the parameters were           from being entered ex
marized in Table I for penalty function annealing, Kempe                               changed to allow increased running time: until a certain           conditions. With this ai,
                                                                                                                                                          colorings that average,
                                                                                                                                                          G 1,OOO,O.5 graphs, using
                                                                        Table I                                                                           IBM 3081. This com
                                              Running Times Required to Obtain Given Colorings for the                                                    processor and hence is
                                                        G 1000, 0.5 Random Graph of Figure 8 a                                                            87-coloring for our gra
                  Penalty Function Annealing Kempe Chain Annealing                             Fixed-K Annealing              Successive Augmentation     and Thomason might h
     Colors         Hours             [TF,SF]          Hours       [TF,SF]           Hours        [TF,SF]          (Trials)   Hours       Algorithm       as much running time
                                                                                                                                                          best results on G 1,000
      108                                                                                                                      0.5     RLF[median]
      105                                                                                                                     17.9     RLF[best: I %]     EXA CTLIM = 70 and
      102                5.0           [1,2]                                                                                                              settings, the average n
      100                                                1.4      [0.25,0.1]            1.8         [I, I]         (10/10)                                averaged 85.5 colors (
       99             10.2             [1,4]                                            2.0         [I, I]          (8/10)                                graphs. The graph in 1
       98             18.0             [1,8]             2.0       [0.5,0.1]            3.7         [1,2]           (7/7)                                  which an 85-colo~ing v.
       97                                                3.1         [1,0.1]            4.3         [1,2]          (10/16)     0.2     XRLF[I,O]
       96            30.0              [1,16]                                           7.7         [1,4]           (8/10)                                 it also had a slight
       95            41.3              [2,16]            7.6            [1,0.25]        9.0         [1,4]           (4/10)                                 (0.5000152), whereas t
       94                                                                              17.3         [1,8]           (5/10)                                 Were found both had
       93                                               21.2            (1,0.5]        31.3         [1,16]          (4/7)      0.5     XRLF[4,0]           expected 0.50.
       92            70.9              [2,32]           35.7            (I, I]         62.1         [2,16]          (3/7)      0.6     XRLF[4,70]
       91           182.3*             [2,64]                                         122.8         [2,32]          (2/6)                               ; 2.4.2. Random p = 0
       90          (343.1)             [4,64]           64.1            [2,2]        (236.6)        [4,32]          (0/1)      4.7     XRLF[40,0]
       89                                                                                                                                                        Vertices
                                                       170.8            [4,4]                                                  8.0     XRLF[20, 70]
       88                                                                                                                      9.6     XRLF[40, 70]     \The same sort of expel
       87                                              285.3            [8,4]                                                 18.3     XRLF[160, 70]     G,.OOO,O.5 random gral
       86                                                                                                                     68.3     XRLF[640, 70]     also performed on G n ,
   aFor algorithms that always yield legal colorings, the listed number of colors was attained more than half the time for the given parameter           250 and 500. As was tt
settings unless the time for the entry is marked by a *, in which case more.details can be found in the text. For penalty function annealing, the        trated on just one sarr
(Trials) column gives the fraction of runs that resulted in legal colorings. A parenthesized running time indicates that the desired coloring was        Was to spot trends r
never found using the given parameter settings. See text for elaborations of these points and explanations of other shorthands used.
                                                                                                   Graph Coloring by Simulated Annealing            /   393

  for the most part bas,:       'thrlesh,OlO is reached, no legal colorings are found. Near    expected results for any particular choice of nand p.
 meter setting. We rep                 threshold, an occasional legal coloring was found.      For the validity of the trends we observe, we rely on
 give for the number'             Once past it, legal colorings were found on almost all       limited "confirmation" tests on other sample instances,
 h that k or fewer col~           runs. (This at least held true for the easier colorings.)    and on past observations that experimental results for
the runs. Here the               The table entries correspond to the fastest parameter         graphs of this type do not vary substantially from in-
isk: for penalty funct           settings for the best success rate attained, where rates of   stance to instance.
  setting yielded one            50% or greater are deemed equally good.                           Results are summarized in Table II, whose entries
 ince fixed-K anneali'              Another observation on our fixed-K results is that         obey the same conventions as those for Table 1. (For
 s not produce legal c           when raw machine speed is taken into account, our             XRLF, if the value for trialnum is listed as "ex," this
rtant to know how lik            running times appear to be significantly faster than those    indicates that XRLF was run in the "exhaustive mode,"
ce of parameters. Th             reported by Chams, Hertz and de Werra, at least for the       i.e., with SETLIM set to the number of vertices and
illS for it. Table lind          more difficult values of K. Although Chams et al. report       TRIALNUM = CANDNUM = 1.) For comparison
II runs for each liste            1.8 hours for a 98-coloring compared to our 3.7, the          purposes, we once again include the results for RLF (the
b) specifies that b tria         processor used by Chams et al. is a CDC Cyber 170-855,        best of the traditional heuristics on these graphs), giving
 ulted in legal coloring         which should be four or more times faster than the            both the median and best coloring found over 100 runs,
m has a parenthesize             Sequent Balance 21000 processor we used. (One possible        and the times for 1 and 100 runs, respectively. To put
  the given coloring w           explanation is that the cooling parameters by Chams et        the results in perspective, we also give for each graph
>r any parameter choice,         al. seem to have been optimized for high rather than low      both its computed density and the current best lower
e longest attempted. I           values of K.)                                                 bound on the expected chromatic number for graphs of
~ are for the paramete              Before passing on to other graphs, we remark that for      its type (e.g., D = 0.5020, LB = 46 for the case of
11 colorings in the leas         0 1,000,0.5 random graphs, XRLF can be improved if one        n = 500). The lower bound, like that of Bollobas and
.ested nearby values for'        modifies it to take advantage of the expected properties      Thomason for G I ,000, 0.5' is determined by computing the
TOR, although we did            of such graphs. Bollobas and Thomason developed an             smallest K for which the expected number of K-
:xhaustively.) Note that         alternative approximation to RLF* that uses estimates on      colorings exceeds 0.5. Typically, if L is this lower
len fixed K, the results         tail probabilities to prevent their analogue of Step 4.3.1    bound, the expected number of L-colorings is in fact
; as the parameters were         from being entered except under the most promising            something like 105, whereas the expected number of
ing time: until a certain        conditions. With this algorithm, they were able to obtain     (L - I)-colorings is 10- 10 . (The expected number of
                                colorings that averaged 86.9 colors over ten sample            K-colorings for G n , p can be computed using standard
                                0 1,000,0.5 graphs, using less than one hour per run on an     counting arguments; we used a cleverly-optimized
                                IBM 3081. This corresponds to 8-10 hours on our                program for doing this provided by Thomason 1987.)
                                processor and hence is half the time it took us to get an          Note that for these smaller graphs, simulated anneal-
                                87-coloring for our graph. It is not clear what Bollobas       ing is a much stronger competitor. For the 125-vertex
Successive Augmentation         and Thomason might have achieved if they had allowed           graph, both Kempe chain and fixed-K annealing succeed
'lours        Algorithm         as much running time as we did. For the record, our            in finding a 17-coloring, whereas the best that XRLF can
                                best results on G I ,000, 0.5 graphs were obtained with        do, even with its parameters turned as high as they could
  0.5      RLF[median]
 17.9      RLF[best: 1%]        EXACTLIM = 70 and TRIALNUM = 1,260. For these                  feasibly go, is 18 colors. Moreover, 18-colorings could
                                settings, the average run length was 136 hours, but we         be found more quickly with the two annealing ap-
                                averaged 85.5 colors over a sample of four G 1,ooo,O.5         proaches than with XRLF. For the 250-vertex, XRLF
                                graphs. The graph in Table I was not one of those for          was capable of finding the best coloring we saw, but

 0.2       XRLF[I,OI
                                which an 85-coloring was found. Perhaps coincidentally,        only on 2 out of 5 runs, and the running times required
                                it also had a slightly higher-than-expected density            by Kempe chain and fixed-K annealing for the best
                                (0.5000152), whereas the graphs for which 85-colorings         colorings are at least in the same ballpark. (It is interest-
                                were found both had densities slightly less than the           ing to note t.hat we could actually perform the limiting
 0.5       XRLF[4,0]            expected 0.50.                                                 algorithm RLF*, i.e., XRLF[ex,O], for both the 250-
 0.6       XRLF[4,70]
                                                                                               and 125-vertex graphs, and in each case it required two
                                2.4.2. Random p = 0.5 Graphs With 500 and Fewer                colors more than the minimum found by other methods.)
 4.7       XRLF[40,0]
 8.0       XRLF[20,70]
                                       Vertices                                                    For n = 500, the situation begins to look more like
 9.6       XRLF[40, 70]         The same sort of experiments that we performed on the          that in Table I for n = 1,000, in that for 50 or more
18.3       XRLF[160,70]
                                G1.000, 0.5 random graph of the previous section were          colors, XRLF is substantially faster than any of the other
68.3       XRLF[640,70]
                                also performed on G n ,0.5 random graphs with n = 125,         approaches. Even here, however, despite our best efforts
ime for the given parameter     250 and 500. As was the case for n = 1,000, we concen-         at increasing its running time, we were never able to get
1alty function annealing, the   trated on just one sample of each graph. Our purpose           it to obtain a 49-coloring, which Kempe chain annealing
hat the desired coloring was
r shorthands used.
                                was to spot trends rather than estimate the precise            found in 161. 3 hours (on one out of two tries with the
394        1 JOHNSON ET AL.
                                                                  Table II
                                      Running Times Used to Obtain Given Colorings for
                                              0n,Os Random Graphs, n ~ 500 a
              Penalty Function Annealing Kempe Chain Annealing                Fixed-K Annealing               Successive Augmentation                   Graph
  Colors        Hours      [TF,SF]        Hours       [TF,SF]         Hours      [TF,SF]          (Trials)   Hours         Algorithm             I VI           x(G)
                                       125 Vertex, p = 0.5 Random Graph (D = 0.5021, LB = 16)                                                     125           -17
      21                                                                                                       0.0       RLF[median]                               9
      20                                                                                                       0.2       RLF[best:37%]            250           - 29
      19          0.2       [I, I]         0.0       [0.5,0.5]         0.0         [1,1]          (8/10)       0.0       XRLF[ex,O]                               15
      18          1.7       [1,16]         0.2         [1,2]           0.1         [1,4]          (7/10)       0.5       XRLF[80,65]              500           -49
      17        (24.1)      [2,128]       21.6        [16,64]          1.8         [1,64]         (2/8)       (6.4)      XRLF[ex,75]                              25
                                                                                                                                                 1000           - 85
                                       250-Vertex, p = 0.5 Random Graph (D = 0.5034, LB = 27)
                                                                                                                                                                  45
      35                                                                                                      0.0        RLF[median]
      33                                                                                                      1.2        RLF[best:2 %]
      31          1.5       [1,4]           0.1      [0.5,0.25]        0.2         [1,2]          (7/10)      0.1        XRLF[ex,O]
      30          2.5       [1,8]           0.8        [I, I]          0.9         [1,8]          (6/10)      1.3        XRLF[160,0]          the hidden colorings b~
      29         14.4       [2,32]          6.2        [4,2]           6.4         [2,32]         (5/10)      2.2*       XRLF[160,65]         constructed clique (whi
                                                                                                                                              than-normal degrees),
                                       500-Vertex, p = 0.5 Random Graph (D = 0.5020, LB = 46)
                                                                                                                                              succeeds (even with 10
      60                                                                                                       0.1       RLF[median]
      59                                                                                                       7.5       RLF[best:7%]
                                                                                                                                              graphs. Indeed, for the I
      55          3.7       [1,4]                                                                              0.1       XRLF[I,O]            number of colors on 1
      54                                    1.5      [0.5,0.5]         1.1         [1,2]          (5/10)       0.1       XRLF[2,0]            slightly better than thai
      53          8.4       [1,8]          2.2         [1,0.5]         2.1         [1,4]          (5/10)       0.2       XRLF[4,0]            sponding standard grapl
      52         -2                       10.6         [1,2]           8.4         [1,16]         (5/10)       0.3       XRLF[8,0]            the true chromatic numl
      51         42.2       [2,32]        16.9         [2,2]          28.0         [4,16]         (3/14)       4.5       XRLF[160,0]
                            [2,128]       45.2         [4,8]        (212.4)        [4,128]                     9.8       XRLF[320,65]
                                                                                                                                                 The optimal number (
      50        136.8                                                                             (0/1)
      49                                 161.3*        [4,16]                                                (73.8)      XRLF[2560,70]        by each of the four apr
                                                                                                                                              ing, given enough tim
   QThe notational shorthands of Table I continue to apply here. An ex under XRLF means that the set-finding in the algorithms as performed
in exhaustive search mode (see text), D stands for the actual edge density, and LB for the lower bound on expected chromatic number
                                                                                                                                              mately how much time
described in the text.                                                                                                                        each approach, the time
                                                                                                                                              to find an optimal color
                                                                                                                                              and half that time did r
given parameters). Indeed, without the final exact color-               and a number of vertices n, we generated our graphs as                ing, the given settings)
ing phase, we never got XRLF to use fewer than 52                       follows:                                                              of the time for all fo
colors, even when run in the mode where each color                       I. Randomly assign vertices with equal probability to K              annealing approaches ar
class was constructed by exhaustive search, subject to                      color classes.                                                     125-vertex graph, and f
the constraint that it contain the current maximum degree               2. For each pair {u, v} of vertices not in the same color             far of the three. This
vertex.                                                                     class, place an edge between u and v with probability              with several grains of s:
   Finally, observe that for all three graphs, fixed-K                      K 1(2(K - 1», i.e., the probability required to make               quoted are for runs \\
annealing is a much stronger rival to Kempe chain                           the average degree roughly n 12.                                  optimal value, i.e., witl
annealing than it was for n = 1,000, although on the                    3. Pick one vertex as a representative of each class and               secret we are trying to
500-vertex graph it weakens considerably once one drops                     add any necessary edges to ensure that these K                     these graphs were the
below 52 colors, and is surpassed even by the penalty                       vertices form a clique (assuming that K is not too
function approach at 50 colors, mirroring its decline on                    large, no class will be empty, so such representatives
the larger graph.                                                           will exist).
                                                                           Using this procedure, we generated "cooked" graphs
                                                                        to match the graphs of the previous two sections, and
2.4.3. Graphs With Unexpectedly Good Colorings
                                                                        with chromatic numbers as indicated in Table III. The                           Graph          Pel
In this section, we consider the ability of the various                 table also presents, for each of these graphs, the running
                                                                                                                                                                x(G)
graph coloring heuristics to find unexpectedly good col-                times (per 100 runs) and the number)
                                                                                                                of colors obtained               I VI
orings. We generated graphs that superficially looked                   by each of the standard heuristics of Section 2.1, and                     125            9
like Gn,o.s random graphs, but in fact had colorings that                                                                                          250           15
                                                                        compares these results to those obtained for the more-
                                                                                                                                                   500           25
used only about half the number of colors found in the                  truly-random counterparts of these graphs that were                      1,000           45
experiments of the previous section.                                    studied in Sections 2.4.1 and 2.4.2. Note that although a
   In particular, having chosen a chromatic number K                                                                                            QHere the parameter setti
                                                                        clever special purpose algorithm might be able to find
                                                                                                                                              SETLIM = 63 and CAND
                                                                                                                 Graph Coloring by Simulated Annealing                   /      395

                                                                                                  Table III
                                                                               Performance of Traditional Heuristics on
                                                                                     Standard and Cooked Graphs
 )uccessive Augmentation                   Graph                         lOO*SEQ                             lOO*DSATUR                                  100*RLF
 ours        Algorithm
                                    I VI           X(G)       Median        Best        Time       Median         Best         Time          Median           Best      Time
                                     125            - 17         25          23          1.8 m        22           20          4.2 m            21             20      11.4 m
 ),0      RLF[median]                                  9         23          19          1.8 m        17           10          4.1 m            12             10      11.2 m
 ).2      RLF[best:37%]              250            - 29         42          40          6.9 m        38           36         14.7 m            35             33      62.2 m
 ).0      XRLF[ex,O]                                  15         41          38          6.9 m        36           32         14.6 m            26             23      62.1 m
 J.5      XRLF[80,65]               500             - 49         73          70         27.0 m        66           63         55.0 m            60             59       7.5 h
 5.4)     XRLF[ex,75]                                 25         72          69         27.1 m        65           61         54.9 m            56             47       7.1 h
                                    1000            - 85        127         124          1.8 h       117          114          3.6 h           108            106      52.2 h
 ).0      RLF[median]                                 45        126         123          1.8h        116          113          3.5 h           106            102      51.2 h
 1.2      RLF[best:2%]
 ).1      XRLF[ex,O]
 1.3      XRLF[160,0]            the hidden colorings by identifying the vertices of the                   would never have thought to run the fixed-K approach
 2.2*     XRLF[160,65]           constructed clique (which should have slightly higher-                    with such small value of K, although we might well
                                 than-normal degrees), none of the standard heuristics                     have chosen the parameter settings needed for the other
                                 succeeds (even with 100 tries) on anyone of the four                      three approaches to find the hidden coloring.
 0.1      RLF[median]
 7.5      RLF[best:7%]           graphs. Indeed, for the larger graphs, the heuristics use a                  Also, that penalty function annealing seems to be
 0.1      XRLF[I,O]              number of colors on the cooked graphs that is only                        competitive with Kempe chain annealing for these graphs,
 0.1      XRLF[2,0]              slightly better than that which they use for the corre-                   whereas it lagged far behind for the uncooked examples.
 0.2      XRLF[4,0]              sponding standard graphs, despite the large difference in                 This is most likely because the ultimate color class size
 0.3      XRLF[8,0]
                                 the true chromatic numbers.                                               for the cooked graphs is roughly twice what it was for
 4.5      XRLF[160,0]
 9.8      XRLF[320,65]              The optimal number of colors can, however, be found                    the originals. (Recall that our implementation of Kempe
 3.8)     XRLF[2560,70]         by each of the four approaches we have been consider-                      chain annealing. can take time proportional to the square
                                 ing, given enough time. Table IV indicates approxi-                       of the largest color class to generate a move, whereas
 the algorithms as performed,
 expected chromatic number'     mately how much time that is for each approach. For                        our penalty function implementation takes time only
                                each approach, the time given in the table was sufficient                  linear in that size.)
                                to find an optimal coloring for the corresponding graph,
                                and half that time did not suffice. (For fixed-K anneal-                   2.4.4. Random p = 0.1 and p = 0.9 Graphs
 generated our graphs as        ing, the given settings yield legal colorings at least 90%                 In iliis section, we consider random Gn • p graphs with
                                of the time for all four graphs.) Note that all three                      values of p different from the p = 0.5 or previous
h equal probability to K
                                annealing approaches are faster than XRLF on all but the                   sections, to determine the effect of increased and de-
                                125-vertex graph, and fixed-K annealing is the fastest by                  creased edge density on our comparisons. Table V sum-
;es not in the same color
                                far of the three. This latter observation must be taken                    marizes the results of experiments with Gn • 0 . 1 graphs for
 u and v with probability.
                                with several grains of salt, however, given that the times                 our standard values of n. For these graphs, certain
ability required to make
                                quoted are for runs where K is already fixed at its                        changes had to be made in the standard parameter choices
1/2.                      .
                                optimal value, i.e., with advance knowledge of the very                    for some of the algorithms. First, the sparseness of the
ltative of each class and.
                                secret we are trying to discover. If one had thought that                  graphs meant that color classes would be much larger,
o ensure that these K
                                these graphs were the Gn • O.5 graphs they mimic, we                       and so we could no longer afford to run XRLF with as
ming that K is not too
, so such representatives
                                                                                                  Table IV
~rated "cooked" graphs                                         Times Required by the Three Annealing Approaches and XRLF to
 vious two sections, and                                             Find Optimal Colorings of the Four Cooked Graphs G
[cated in Table III. The                   Graph           Penalty Function Annealing    Kempe Chain Annealing           Fixed-K Annealing                      XRLF
 hese graphs, the running
 mber of colors obtained ..        I VI            x(G)      Time        [TF,SF]          Time       [TF,SF]         Time          [TF, SF]            Time          [TN, XLI
ics of Section 2.1, and             125              9      34.1 s       [0.5,0.1]       47.8 s      [0.5.0.1]       16.3 s        [0.5,0.51           34.2 s          [4,0]*
  obtained for the more-            250             15       4.6 m       [0.5,0.51        4.3 m      [0.5,0.1]        1.4 m        [0.5,0.5]           12.5 m          [5,0]
                                    500             25      35.1 m         [I, I]        18.0m         [1,0.1]        8.9 m          [1,0.5]          107.8 m         [20,0]
 hese graphs that were            1,000             45                     [2,8]                       [I, I]                        [2, I]
                                                            15.2 h                       14.3 h                       3.7 h                            64.1 h        [640,0]
U. Note that although a
[l might be able to find
                                 aHere the parameter settings for XRLF on the 125-vertex graph are marked by a ,*, to indicate that we did not use the standard values of
                                SETLIM = 63 and CANDNUM = 50 on this graph, but instead set these parameters to 32 and 10, respectively.
396        /   JOHNSON ET AL.

                                                              Table V
                                          Running Times Required to Obtain Given Colorings
                                                     of Gn,a.l Random Graphs
                                                                                                                                                      Kempe Chai
                Penalty Functional Annealing Kempe Chain Annealing            Fixed-K Annealing                Successive Augmentation
                                                                                                                                                     Hours
  Colors         Hours     [TF, SF]            Hours     [TF,SF]      Hours      [TF,SF]          ([rials)    Hours       Algorithm
                                           l25-Vertex, p = 0.1 Random Graph (D = 0.0950, LB = 5)
       6           0.1       [0.5,0.25]          0.0        [1,0.5]    0.0      [0.5,0.25]     (7/10)           0.0    RLF[med, best)    50
       5           2.9         [2,8]             4.8        [4,16]     0.2        [1,16]       (4/10)           0.0    XRLF[I,125]       48
                                                                                                                                         45            0.1
                                           250-Vertex, p = 0.1 Random Graph (D = 0.1034, LB = 7)                                         44            6.6
      10                                                                                                        0.0    RLF[median)
                                                                                                                                         43          (46.9)
       9           0.2          [1,0.5]          0.5       [1,1]        0.0       [1,0.5)          (9/10)       1.8    RLF[best:45 %)
       8         (36.9)         [4,16]         (25.6)      [4,16]       2.6       [4,16]           (5/10)     (40.3)   XRLF[1280,125)
                                           500-Vertex, p = 0.1 Random Graph (D = 0.0999, LB = 11)                                            84
      15                                                                                                        0.1    RLF[median)           82
      14           2.0          [I, 1]           1.6     [0.5,0.5]      0.1       [1,0.5)     (10/10)          11.8    RLF[best:18%)         76
      13          24.2          [2,16]          68.6       [2,16]       1.0       [2,2]        (8/10)          16.5    XRLF[320,IOO)         75         0.3
                                          I,ODD-Vertex, p = 0.1 Random Graph (D = 0.0994, LB = 19)                                           74
      24           3.2          [1,0.5]          7.0      [0.5,0.5]     0.3     [0.5,0.5]     (10/10)           0.8    RLF[med, best)        73         0.8
      23          13.0          [1,2)           21.0        [1,1)       0.6       [1,0.5)      (6/6)            1.2    XRLF[5,IOO)           72        20.0
      22          37.0          [2,4)          124.6        [1,8)       4.1       [2,2)        (4/4)           35.1    XRLF[160,IOO)          71      (70.8)
      21        (101.0)         [2,16)        (281.9)       [1,16)     36.1       [2,16]       (2/2)         (137.0)   XRLF[640, 100)
                                                                                                                                             155
                                                                                                                                             152
large a value as 63 for SETLIM, settling instead for                     again dominates the latter). In contrast to the Gn ,O.5             134         1.1
                                                                                                                                             133
SETLIM = 20. We also discovered that we had to in-                       graphs, however, Kempe chain annealing substantially
                                                                                                                                             132
crease the starting temperature for penalty function an-                 outperforms both XRLF and fixed-K annealing on all the              131         3.6
nealing from 10 to 30, and for Kempe chain annealing                     graphs with n? 250. Fixed-K annealing outperforms                    130        6.5
from 5 to 10, in order for the initial acceptance ratio to               XRLF on all graphs with n:( 500, but XRLF seems to                   129       15.2
reach the 30% level. (The starting temperature of 2                      have caught it by n = 1,000.                                         128       29.1
remained sufficient for fixed-K annealing.)
   Note that here, with even bigger color classes, Kempe                 2.4.5. Geometrically Defined Graphs                                 283
chain annealing falls behind penalty function annealing.                 In this, our final section of results, we consider how the          276
                                                                                                                                             238         10.0
Moreover, as with the graphs of the previous section,                    various heuristics behave on graphs in which there is               237
both are dominated by fixed-K annealing, as is XRLF.                     built-in structure (but not built-in colorings). In particu-        236
   Table VI summarizes the results of experiments with                   lar, we consider the "geometrical" graphs of Part I, and            235
Gn •a.9 graphs for our standard values of n. We only                     their complements. A random geometrical graph Un,d is               234
                                                                                                                                             233         36.3
consider two of the three annealing approaches in detail                 generated as follows. First, pick 2 n independent num-
                                                                                                                                              232
here. Given the trends in running times indicated by our                 bers uniformly from the interval (0, 1), and view these as           231
results for p = 0.1 and p = 0.5, it seemed highly un-                    the coordinates of n points in the unit square. These                230        44.7
likely that penalty function annealing would be competi-                 points represent vertices, and we place an edge between              229
tive with Kempe chain annealing when p = 0.9. (As a                      two vertices if and only if their (Euclidean) distance is d          228       122.4
                                                                                                                                              227
test case, we ran both on the Gsoo ,a.9 graph. The pen-                  or less. Table VII summarizes our results for three
                                                                                                                                               226       350 +
alty function approach required 27 hours to find a 132-                  examples of such graphs, all with n = 500: a Usoo,a.l
coloring, whereas Kempe chain annealing found a 131-                     graph, a Usoo,a.s graph, and the complement of a Usoo, 0.1        aThe 232- and 235-color
                                                                                                                                          'RIALNUM as specified. 1
coloring in just 3.6 hours.) As in the p = 0.5 case, we                  graph (denoted i!soo,a.l)' The densities of these graphs        i the run had survived until
used starting temperatures of 5.0 and 2.0 for Kempe                      were 0.0285,0.4718 and 0.9721, respectively. (Experi-           , tter coloring.)
chain and fixed-K annealing, respectively.                               ments with second examples of each type of graph,
   For these graphs it is possible to run XRLF in the                    having slightly different densities, yield qualitatively
                                                                                                                                            more surpnsmg, be
exhaustive mode even for n = 1,000, although this                        similar results.)
                                                                                                                                         j SATUR, a successive
may not always be the best choice. (In particular, a 232-                   Again, we drop penalty function annealing from the
                                                                                                                                           hed well behind RLF
coloring of the 1,000-vertex graph was obtained more                     comparison, and use starting temperatures of 5,0 and 2.0
quickly with SETLIM < 1,000, as indicated in the table.)                 for Kempe chain and fixed-K annealing, respectively.              erforming 100 runs of
                                                                         The story is once again mixed. Although fixed-K anneal-          .nd the best coloring fc
Once again, both annealing and XRLF can find substan-
tially better colorings than traditional successive augmen-              ing is the winner for the d = 0.1 graph, it is outper-            auld find in 50 or m<
tation heuristics like RLF and DSATUR (and the former                    formed by Kempe chain annealing for d = 0.5, and what           [technique or XRLF. Ind
                                                                                                           Graph Coloring by Simulated Annealing                /     397
                                                                                             Table VI
                                                                   Running Times Needed to Obtain Given Colorings for
                                                                                                                 a
                                                                                     0n,a.9 Random Graphs
                                                   Kempe Chain Annealing                     Fixed-K Annealing                         Successive Augmentation
 ,urs                                             Hours         [TF,SF]           Hours          [TF,SF]             (Trials)       Hours              Algorithm
                                                                       125-Vertex, p = 0.9 Random Graph (D = 0.8982, LB = 40)
),0     RLF[med, best]!             50                                                                                                 0.0          RLF[median]
l.O     XRLF[I,125]                 48                                                                                                 0.1          RLF[best:48%]
                                    45              0.1        [0.25,0.1]            0.0          [I, I]             (8/10)            0.0          XRLF[ex,O]
),0     RLF[median]                44               6.6           [2,8]              0.3          [1,8]              (7/10)            1.7          XRLF[ex, 80]
 .8     RLF[best:45%],             43             (46.9)          [8,16]            (9.3)         [8,64]             (0/3)
),3)    XRLF[l280, 125]                                                250-Vertex, p = 0.9 Random Graph (D = 0.8963, LB = 70)
                                    84                                                                                                 0.0          RLF[median]
).1     RLF[median]                 82                                                                                                 0.5          RLF[best: II %]
 .8     RLF[best:18%]               76                                                                                                 0.0          XRLF[ex, 60]
;.5     XRLF[320, 100]              75              0.3        [0.25,0.1]           0.6           [2,2]              (8/10)         (184.7)         XRLF[ex,80]
                                    74                                               1.3          [2,4]              (5/10)
1.8                                 73              0.8         [0.5,0.25]          5.0           [2,16]             (3/4)
 .2                                 72             20.0           [2,4]           (48.5)          [8,64]             (0/1)
;.1                                 71            (70.8)          [2,16]
'.0)
                                                                      500-Vertex, p = 0.9 Random Graph (D = 0.9013, LB = 122)
                                  ISS                                                                                                  0.0          RLF[median]
                                  152                                                                                                  3.2          RLF[best:6%]
 contrast to the Gn,a..           134               1.1        [0.25,0.1]           2.7           [2,2]              (7/10)            0.3          XRLF[ex,O]
 annealing substantiall           133                                               4.8           [2,4]              (8/8)             0.3          XRLF[ex, 60]
                                  132                                               9.6           [4,4]              (2/3)             1.5          XRLF[ex, 70]
j-K annealing on all th
                                  131               3.6         [0.5,0.25]          9.6           [4,4]              (3/3)           (77.8)         XRLF[ex,80]
 annealing outperform'            130               6.5           [1,0.25]         21.6           [2,16]             (2/6)
)0, but XRLF seems t i            129              15.2            1,0.5]         (80.2)          [8,16]             (0/1)
                                  128              29.1           [I, I]
                                                                     I,DOD-Vertex, p = 0.9 Random Graph (D = 0.8998, LB = 217)
Graphs                            283                                                                                                  0.2          RLF[median]
 s, we consider how th            276                                                                                                 21.5          RLF[best: I %]
                                  238              10.0         [0.5,0.1]          38.7           [2,8]              (3/3)
aphs in which there i
                                  237
I colorings). In particu.
                                  236                                              78.7           [2,16]             (4/4)
[" graphs of Part I, and          235                                              88.9           [2,16]             (1/7)             0.2          XRLF[5,0]*
Jmetrical graph Un, d (           234                                              84.6           [2,16]             (1/4)             3.0          XRLF[ex,O]
. 2 n independent num,            233              36.3         [0.5,0.2]        (172.5)          [4,16]             (0/2)             4.9          XRLF[ex, 60]
 0, 1), and view these a'•.       232                                                                                                 11.0          XRLF[20, 70]*
                                  231                                                                                               (277.5)         XRLF[ex,80]
the unit square. These!           230                             [1,0.25]
                                                   44.7
 place an edge between'           229
:<:uclidean) distance is d.       228             122.4           [I, I]
  our results for three'          227
                                  226             350+           [2,2]
ith n = 500: a Usoo ,a. Ii
omplement of a USOO ,O.I.        "The 232- and 235-colorings of the 1,OOO-vertex graph using XRLF were obtained with SETLIM = 250, CANDNUM = 50, and
:nsities of these graphs'     TRIALNUM as specified. The Kempe chain run that found the 226-coloring was terminated by a computer crash rather than by convergence.
, respectively. (Experi-.     If the run had survived until convergence, it might have taken much more time than the 350 hour actually used. (It might also have found a
                              better coloring.)
f each type of graph,
ies, yield qualitatively
                              is more surprising, both are beaten substantially by                    uses fewer colors than any of the other techniques. (The
ion annealing from the        DSATUR, a successive augmentation heuristic that fin-                   percentages we quote here for DSATUR are based on a
>eratures of 5.0 and 2.0      ished well behind RLF on all our nongeometric graphs.                   set of 1,000 runs, rather than the standard 100, and so
lnnealing, respectively.      Performing 100 runs of this heuristic took only 1.3 hours               should be fairly robust for this graph.)
 though fixed-K anneal-       and the best coloring found was 3 colors better than we                    Our final graph, the complement of a d = 0.1 graph,
.1 graph, it is outper-       could find in 50 or more hours using either annealing                   also shows some anomalies. Here DSATUR again out-
~ for d = 0.5, and what       technique or XRLF. Indeed, one in five runs of DSATUR                   performs XRLF, but is itself beaten by ordinary RLF.
398     /   JOHNSON ET AL.

                                                                 Table VII
                                                                                                                                                                         A
                                   Running Times Needed to Obtain Given Colorings for
                                              Various Geometric Graphs a
              Kempe Chain Annealing                   Fixed-K Annealing                        XRLF             Successive Augmentation
  Colors       Hours      [TF, SFl          Hours         [TF,SF]         (Trials)   Hours       [TN, ELI      Hours        Algorithm

                                              500-Vertex, d = O. I Random Geometric Graph
      13                                                                          0.0              [1,0]*       0.0     DSAT[med.]
      12         0.8     [0.25,0.25]          0.0      [0.5,0.5]     (10/10)     (7.1)            [50,0]*       1.2     DSAT[best:29 %]

                                              500-Vertex, d = 0.5 Random Geometric Graph
      132                                     1.4       [1,2]        (5/10)                                     0.8     RLF[med.]
      131                                     4.2        [2,4]       (6/10)                                     7.5     RLF[best: I %]
      130        3.8         [1,0.5]          8.1        [2,8]       (5/10)      0.0                  [1,0]*                                                           tiOJ
      129        7.4         [I, I]          17.8        [2,16]      (1/6)                                      0.0     DSAT[med.]
      128       20.7*        [2,2]           32.4        [4,16]      (2/10)
      127       72.5*        [2,8]         (113.3)       [4,64]      (0/2)       2.3               [1,0]*                                  dixed-K annealing by a (~
      126     (126.5)        [2,16]                                           (59.8)              [20,0]*
                                                                                                                                            to account for the extra 0
      125
      124                                                                                                       1.3     DSAT[best: I %]     ing K. If the contest is cc
                                                                                                                                              xclamation point. Note
                                       Complement of a SOD-Vertex, d = 0.1 Random Geometric Graph
                                                                                                                                             rom fixed-K annealing t(
      95                                                                                0.1       [ex, 180]
                                                                                                                                                aphs get denser (althou
      94                                                                                0.3       [ex, 210]
      93                                                                                8.7       [ex, 270]     0.0      DSAT[med.]             ses where XRLF and I
      92                                                                                0.5       [ex, 280]                                     At present, we have
      91                                                                               18.8       [ex, 290]                                    hy a given approach dOl
      90          4.0     [0.5,0.5]                                                     1.9       [ex, 300]     0.0      RLF[med.]               t another. One factor
      89          5.0       [1,0.5]                                                  (100 +)      [ex, 315]     1.3      DSAT[best:4 %]
                                                                                                                                               hether the data structu
      88         12.3       [1,1]                                                                               1.5      RLF[best:4 %]
      87       (239.8)      [2,16]             0.0        [0.5,0.5]       (10/10)
                                                                                                                                                 timized for sparse or
      86                                       0.0          [I, I]        (10/10)                                                              empe chain implementa
      85                                       0.0          [2,2]         (10/10)                                                             olor classes are small,
      84                                     (75.3)         [4,64]         (0/1)                                                                 nse graphs.)
   aThe first five entries in the XRLF column are marked by "*"s because the parameters SETLIM and CANDNUM had to be varied to
                                                                                                                                                 Another important fact
obtain the best results, although our format only allows us to specify TRIALNUM and EXHA USTLIM. These entries were derived using              ood colorings for the gr
the following (SETLIM, TRIALNUM, CANDNUM) combinations: (20, 1,50), (30,40,50), (63, I, I), (250, I, I), and (250,20,50). The                 'on and Kempe chain ani
final XRLF run for the third graph had not yet terminated after 100 hours, at which point it was killed.                                          t rewards colorings in
                                                                                                                                                 ewed: better a large ar
                                                                                                                                               zed ones. (XRLF has t]
The annealing implementations reassert themselves,                           variance in the running times of our exhaustive coloring           ay in which it operate
however, with the fixed-K approach again coming out                          routine, as seen in Figure 6.)                                    ther hand, is neutral as
on top. Once the correct values for SIZEFACTOR and                                                                                            {constructs, and so migt
TEMPFACTOR were chosen, it took only 30 seconds                              2.5. Commentary                                                  ralanced colorings. Thu
per run for 85-colorings. (Much more time was spent                          The experiments we report in Section 2.4 do not allow            ,lorings of the latter 1
finding the correct parameter values, however. When we                       us to identify a best graph coloring heuristic. Indeed,           • proach may well outpe]
tried to 85-color the graph with SIZEFACTOR set to I                         they reinforce the notion that there is no best heuristic.        .~rticular, this appears t
instead of 2, no legal coloring was found and a typical                      Table VIII displays the winners for each of the graphs             . al graph we studied,
run took an hour or more.) Another running time anomaly                      we studied (except the cooked graphs, for which all three          , dom geometric graph
is evident from the results for XRLF. Here, because of                       annealing algorithms were in the same ballpark, and                 ¢ best costs under the
the density of the graph, we could exhaustively search                       pulled away from XRLF as soon as n reached 250). For                 finitely not the best col.
for the best independent set at each step, and switch over                   each graph, we name the heuristic with the best perfor-             !It cost less than 88-(
to exhaustive coloring when the number of uncolored                          mance, along with a runner-up if the competition is                   ugh this was a very d
vertices was stilI quite large. Our running times, how-                      close. In judging performance for a given graph, we                    e expected Kempe ch
ever, do not monotonically increase with EXACTLIM,                           rank the algorithms first according to the best coloring               ealing could in sec(
the parameter controling the switchover, but instead                         they found. If this is a tie, we then consider the time the          bstantially better than
gyrate wildly. (Most likely, this is due to the wide                         algorithms took to find this best coloring, penalizing             hain algorithm in hundr
                                                                                                        Oraph Coloring by Simulated Annealing           /   399
                                                                                         Table VIII
                                                        Algorithms Providing the Best Performance for Each of the Random
                                                         Graphs On. p and Geometric Graphs Un, d Covered in Our Study a
                                                                                              Number of Vertices
;uccessive Augmentation                                  Graph
                                                         Type             125                 250                  500          1,000
Jurs        Algorithm
                                                         °n.O.1       XRLF              Fixed!              Fixed!             Fixed!
                                                         °n.0.5       Fixed, Kempe      XRLF, Kempe         Kempe, XRLF        XRLF!
),0     DSAT[med.]                                                    Fixed             Kempe!              Kempe!             Kempe!
                                                         °n.0.9
..2     DSAT[best:29%]                                                                                      Fixed, DSAT
                                                         Un . O. 1
                                                         Un . 0 . 5                                         DSAT!
l.8      RLF[med.]                                       Un . o. 1                                          Fixed'
7.5      RLF[best: 1%]                                   °Close runners up are also listed. Runaway winners are annotated with an exclama-
                                                      tion point.
         DSAT[med.]

                                 fixed-K annealing by a (somewhat arbitrary) factor of 3               In considering which of the new algorithms is best in
                                to account for the extra overhead it must incur in choos-           which situation, we should not lose sight of the more
  1.3        DSAT[best: 1%I     ing K, If the contest is considered a runaway, we add an            fundamental implication of our results: as a class, these
                                exclamation point. Note that the balance tends to shift             new randomized search algorithms (including XRLF)
                                from fixed-K annealing to Kempe chain annealing as the              offer the potential for substantial improvement over tra-
                                graphs get denser (although this effect is masked in the            ditional successive augmentation heuristics. When suffi-
  0.0        DSAT[med.]         cases where XRLF and DSAT win),                                     cient running time is available, they are usually to be
                                    At present, we have only tentative explanations of              preferred over the option of performing multiple itera-
                                why a given approach dominates one class of graphs and              tions of a traditional heuristic, with the advantage in-
  0.0        RLF[med.]          not another, One factor no doubt is the question of                 creasing as more running time becomes available, More-
  1.3        DSAT[best:4%]
                                whether the data structures of our implementation are               over, the running times of 100 hours and more that
  1.5        RLF[best:4 %]
                                optimized for sparse or dense graphs. (Recall that our              characterize the extremes of our experiments are not
                                Kempe chain implementation is most efficient when the               normally necessary if all one wants to do is outperform
                                color classes are small, which is likely to happen with             the traditional heuristics. On our instance of 0 1,000,0.5'
                                dense graphs.)                                                      XRLF took only 10 minutes on a slow computer to
  NDNUM had to be varied t          Another important factor may be the "nature" of the             improve by 8 colors over the best solution we ever found
 ese entries were derived usin  good   colorings for the graphs in question. Penalty func-          using traditional heuristics.
 l, 1, 1), and (250,20,50). Th. tion and Kempe chain annealing both use a cost function                The approaches we study here of course do not ex-
                                that rewards colorings in which the color class sizes are           haust the possibilities for computationally intensive ran-
                                skewed: better a large and a small class than two equal             domized search. For instance, there is the "tabu" search
                                sized ones. (XRLF has the same bias, given the greedy               technique of Glover (1989), which has been applied to
 .f our exhaustive coloring     way in which it operates.) Fixed-K annealing, on the                graph coloring by Hertz and de Werra (1987). As with
                                other hand, is neutral as to the sizes of the color classes         simulated annealing, this is a randomized modification of
                                it constructs, and so might be expected to construct more           local optimization that allows uphill moves, Here, how-
                                balanced colorings. Thus, for graphs in which good                  ever, the basic principle is closer to that used in the
  Section 2.4 do not allow colorings of the latter type predominate, the fixed-K                    Kernighan and Lin (1970) graph partitioning heuristic
)loring heuristic. Indeed, approach may well outperform the other two methods. In                   and the Lin and Kernighan (1973) traveling salesman
there is no best heuristic.     particular, this appears to have been the case with the             heuristic, studied in Parts I and III of this paper, respec-
rs for each of the graphs' final graph we studied, the complement of a Un,o.\                       tively. Given a solution, one randomly samples r neigh-
~raphs, for which all three     random geometric graph. Here, the colorings that had                bors, and moves to the best one, even if that means
   the same ballpark, and the best costs under the Kempe chain formulation were                     going uphill, unless that move is on the current "tabu"
mas n reached 250). Fo( definitely not the best colorings (94-colorings were found                  list. In the implementation of Hertz and de Werra, which
istic with the best perfor-, that cost less than 88-colorings). Consequently, even                  is based on the fixed-K neighborhood structure, a move
up if the competition is' though this was a very dense graph on which we might                      that changes the color of vertex v from i to j is
~ for a given graph, we: have expected Kempe chain annealing to excel, fixed-K                      considered tabu if v was colored j at any time during
rding to the best coloring~ annealing could in seconds find colorings that were                     the last 7 moves. No tabu move can be made except in
then consider the time the;: SUbstantially better than anything seen by the Kempe                   the following situation: The current cost is c, the new
 best coloring, penalizingi chain algorithm in hundreds of hours.                                   cost would be c' < c, and at no time in the past has a
400    /   JOHNSON ET AL.

 move been made that improved a solution of cost c to          shall have more to say about these generic issues in Karmarkar et al. (1986) h
 one of cost as good as c'.                                    Section 4.                                                    value of the optimal s
    According to Hertz and de Werra, this technique                                                                          D( If! /2 n), i.e., exponen
 (augmented with special purpose routines that may be of                                                                     expected value of the sm2
                                                               3. NUMBER PARTITIONING
 some use in jumping to a legal coloring at the end of the                                                                   neighboring solutions unde
 process) outperforms the original fixed-K annealing           In this section, we consider the application of simulated link, only polynomially
 implementation of Chams, Hertz and de Werra. In our           annealing to the number partitioning problem described solution will be a local 0
 own limited experiments with tabu search, we have seen        in the Introduction. For an instance A = (aI' a 2 , .•. , an) structure and will be buri<
 some speed-up on small instances and for easy colorings,     of this problem, a feasible solution is a partition of A, solution space, i.e., all it
 but no general dominance. (This may be because we             i.e., a pair of disjoint sets A I and A 2 whose union is all that are worse by very higl
 failed to tune the tabu parameters properly, or it may be     of A. In contrast to the situation with graph partitioning over, the most frequent ~
 because, as indicated in Section 2.4.1, our fixed-K           in Part I, there is no requirement that the cardinality of selves be worse than the bl
 annealing implementation seems to be significantly faster    the sets be equal; all partitions are feasible solutions. factors. Thus, a local opti
 than that of Chams, Hertz and de Werra.) There is            The cost of such a partition is I LoeA,a - LoeA,al, tf~om a random partition,
 clearly much room for further investigation, both with       and the goal is to find a partition of minimum cost.           ~ielatively bad solution.
 these algorithms and alternatives, such as the hybrids           We make no claims about the practical significance of 5i Can simulated annealing
 suggested in Chams, Hertz and de Werra (1987) and            this NP-hard problem, although perfect solutions (ones            at annealing allows occ"
 Hertz and de Werra (1987), or entirely new annealing         with cost 0) might have code-breaking implications                    a long time, we would
 implementations. (One such new implementation has            (Shamir 1979). We have chosen it mainly for the ex-                  visit many distinct 10,
 been proposed in Morgenstern (1989), with promis-            tremely wide range of locally optimal solution values              lution it sees should m
                        °
 ing results: For some 1 ,000,0.5 random graphs it finds
 84-colorings. )
                                                              that its instances can have (as measured in terms of the
                                                              ratio between the bset and the worst: see below),
                                                                                                                                 erage solution found by
                                                                                                                                 be the case (as it was f(
    A final issue to be discussed here is the appropriate     and because of the challenges it presents to simulated                   is better than what
 methodology for organizing the multiple runs that seem       annealing.                                                            nding the same amoun
 necessary if one is to get the best results possible for a       The major challenge is that of devising a suitable and            s of local optimizatic
given new graph from a given algorithm in a given             effective neighborhood structure. We shall argue that the          . ountainous" nature (
 amount of time. For penalty function annealing, Kempe        natural analogs and generalizations of the structures for           ubts.
chain annealing, and XRLF, one would presumably start         graph partitioning and graph coloring have serious limi-            Moreover, it will not 1
with a short run and then adjust the parameters on each       tations, and then show experimentally that the simulated            ghtly on local optimiz
 successive run so as to double the running time until no     annealing procedure does not have enough power to                   ists an efficient algorithr
 further improvement occurs or the available time is used     overcome these drawbacks. This does not imply that                   n or neighborhood stn
up. Assuming that the last run provides the best results,     there is no way of successfully adapting simulated an-                 t asymptotically, outp
only about half the overall time will have been wasted on     nealing to this problem, but at present we can think of no         gorithm     based on a neigJ
preliminary work. This was essentially the procedure          better alternatives than the ones we consider.                     "   This  is the "differenc
used here, although we have not fully investigated the                                                                             d Karp.
question of which parameters to adjust when there are         3.1. Neighborhood Structures
choices, and it sometimes seemed to make a difference.                                                                          '12. The Competition
                                                              The "natural" neighborhood structures referred to above
(As we mentioned, this is especially the case with XRLF.)     form a series, SW1 , SW2 , ••• • In the neighborhood                . e differencing algorithl
For fixed-K annealing, a similar approach can be taken,       graph SWk , there is an edge between solutions (A I' A z)          Jlrks by creating a tree
only now one must also decide when and how far to             and (B I' B 2 ) if and only if A I can be obtained from A 2           as vertices, and then fo
decrease or increase K (which is why we imposed a             by "swapping" k or fewer elements, i.e., I Al - B I 1+              ¢ tree and letting A i be
factor-of-3 run-time penalty on fixed-K annealing when         I B I - AI I ~ k. We shall refer to SWk as the k-swap              ;for i E { I , 2}. (Such a
ranking the algorithms for Table VIII). One possibility is    neighborhood. (Our annealing implementation for graph                . ctible in linear time.
to start with a high value of K and a short running time.     partitioning in Part I extends the definition of solution to           ows.
Thereafter, if the run is successful, try again with the      include all partitions and then uses the I -swap neighbor-                e begin with a verte;
same run-time parameters and reduce K by I; if not, try       hood graph.)                                                            value of that element;
again with K fixed and the running time doubled. Under           The limitations of these neighborhoods are illustrated              n repeatedly perform
this methodology, significantly more than half the time       (and emphasized) when we consider instances consisting                 re is but a single live
may be spent on preliminary runs, but the time spent on       of random numbers drawn independently from a uniform                    ices u and v with
such runs should still be manageable.                         distribution over [0, I]. Let In be the random variable               ,ken arbitrarily), and 2
   Our experiments also raise questions about the             representing an n-element instance of this type and                   ;d an edge between u a
methodologies used for starting and terminating runs; we      OPT( In) represents the optimum solution value for In'               od set label(u) = label(
                                                                                               Graph Coloring by Simulated Annealing          /   401
 these generic issues         I(armarkar et al. (1986) have shown that the expected         essentially makes the decision to put u and u on
                              value of the optimal solution value OPT(1n) is                opposite sides of the partition, postponing for IDe time
                              O( iii /2 n), i.e., exponentially small. In contrast, the     being the decision as to which sides those are to be.)
                              expected value of the smallest cost difference between          It is easy to prove inductively that at any point in the
                              neighboring solutions under neighborhood S Wk is about       construction we will have constructed a forest in which
application of simulat        1/ nk , only polynomially small. Thus, any reasonable        each tree contains exactly one live vertex, and the label
Ining problem describ         solution will be a local optimum of the neighborhood         of that vertex is precisely the value of the partition
;eA=(al,aZ,··.,a)             structure and will be buried in a deep" valley" of the       induced by that tree (the difference between the sums of
ion is a partition of A       solution space, i.e., all its neighbors will have values     the two sets that we obtain by 2-coloring that tree).
d A z whose union is          that are worse by very high multiplicative factors. More-    Thus, the value of the eventual partition formed is
l with graph partitionin'     over, the most frequent such local optima will them-         simply the label of the final live vertex.
It that the cardinality 0     selves be worse than the best by very high multiplicative       For random instances of the type we have been dis-
; are feasible solutions:'   factors. Thus, a local optimization algorithm, if started     cussing, the expected value of this final label is thought
  I LaEA,a - LaEA,al,        from a random partition, is almost certain to stop at a       to be O(I/n'ogn), which is asymptotically smaller than
I of minimum cost.           relatively bad solution.                                      the expected smallest move size for any of the neighbor-
practical significance 0        Can simulated annealing do any better? Given the fact      hoods S Wk' (The 0(1/ n 10g n) has not actually been
  perfect solutions (one     that annealing allows occasional uphill moves and runs        proved for the differencing algorithm, but rather for a
~-breaking implication'      for a long time, we would expect a typical annealing run      variant specially designed to simplify the probabilistic
[} it mainly for the ex;     to visit many distinct local optima, and so the best          analysis (Karmarkar and Karp). There is no apparent
optimal solution value'      solution it sees should most likely be better than the        reason, however, why this variant should be better than,
leasured in terms of th      average solution found by local optimization. But would       or even as good as, the original.) Although O(I/n 1ogn )
Ie worst: see below),        it be the case (as it was for graph partitioning) that this   is still far larger than the expected optimum, it offers
 t presents to simulated     best is better than what could be obtained by simply          formidable competition to other approaches, and simu-
                             spending the same amount of time performing multiple          lated annealing would have to improve substantially on
  devising a suitable and    runs of local optimization from random starts? The            local optimization to be in the running. Can it do so?
  We shall argue that the    "mountainous" nature of the solution space raises
'ns of the structures for    doubts.                                                       3.3. Implementation Details
Jring have serious limi-        Moreover, it will not be enough merely to improve          To investigate this question, we construct implementa-
Itally that the simulated    slightly on local optimization. This is because there         tions based on both the I-swap and 2-swap neighborhood
lave enough power to,        exists an efficient algorithm, not based on local optimiza-   structures. Note that, if all the annealing parameters of
is does not imply that       tion or neighborhood structures at all, that should, at       our generic algorithm in Figure 1 are fixed, the latter
 adapting simulated an-      least asymptotically, outperform any local optimization       implementation will take much more time per tempera-
~sent we can think of no     algorithm based on a neighborhood SWk for some fixed          ture, as its neighborhood size is n + n(n - 1)/2 =
Ne consider.                 k. This is the "differencing" algorithm of Karmarkar          (n z + n)/2 versus simply n for the SW1 neighborhood.
                             and Karp.                                                     The neighborhood size for SWk , k> 2 would analo-
                                                                                           gously have been Q(n k ) and we abandon all those
 ctures referred to above,   3.2. The Competition                                          neighborhood structures as computationally infeasible.
. In the neighborhood'       The differencing algorithm runs in O(n log n) time. It           Among the problem-specific subroutines used in our
'een solutions (A I' A 2)     works by creating a tree structure with the elements of      implementation only the INITIAL_SOLN() and
m be obtained from A 2.      A as vertices, and then forming a partition by 2-coloring     NEXT_CHANGE( ) routines merit detailed discussion.
 nts, i.e., I A, - B, 1+     the tree and letting A i be the set of elements with color    (The others are determined by our choice of neighbor-
to SWk as the k-swap         i for i E { 1, 2}. (Such a coloring is unique and con-        hood structure and the details of the problem itself.) For
lplementation for graph      structible in linear time.) The tree is constructed as        our initial solution, we pick a random partition by inde-
definition of solution to    follows.                                                      pendently "flipping a fair coin" for each a i to decide
:s the I-swap neighbor-         We begin with a vertex for each element, labeled by        the set to which it is assigned. To pick a random
                             the value of that element and declared to be "live." We       neighbor under SW" we simply choose a random ele-
lorhoods are illustrated     then repeatedly perform the following operations until        ment of A and move it from its current set (A 1 or A z)
jer instances consisting     there is but a single live vertex: 1) Find the two live       to the other set. Rather than choose a new random
ndently from a uniform       vertices u and u with the largest labels (ties are            element each time NEXT _CHANGE( ) is called, how-
le the random variable       broken arbitrarily), and assume label(u) ~ label(u). 2)       ever, we initially choose a random permutation of A,
mce of this type and         Add an edge between u and u, declare u to be "dead,"          and then at each call simply choose the next element in
I solution value for In'     and set label(u) = label(u) -label(u). (This operation        the permutation, until the permutation is used up. Every
402   /   JOHNSON ET AL.
                                                                                                                                                                                              appears may be a random
I A I moves we rescramble the permutation and start               Figure 9 presents a "time exposure" of an individual
                                                                                                                                                                                               related to the convergen
over. This approach was mentioned in Part I and was            annealing run on a random 100-element instance, using
                                                                                                                                                                                               Since for this study we we
observed to yield a more efficient use of time. It also        the SW2 neighborhood structure and SIZEFACTOR '"
                                                                                                                                                                                               value as well as the chaml
helps ensure that the annealing process will end up with       16. (The generic termination conditions were turned off
                                                                                                                                                                                               lion conditions in the eJ
a solution that is truly locally optimal (if there is an       and the time exposure was run until visual evidence
                                                                                                                                                                                               followS: To halt, we requ
 improving move, it must be encountered sometime in the        indicated that "freezing" had set in.) The x-axis of the
                                                                                                                                                                                               less than MINPERCEN
next 2 n trials). An analogous process is used for the         plot measures time, or more precisely, the number of
                                                                                                                                                                                               value remain unchanged
SW2 case, only now we work from a permutation of all           calls to NEXT _CHANGE( ) divided by the neighbor-
                                                                                                                                                                                               temperatures (or more pre
 1- and 2-element subsets X of A.                              hood size N = 5,050. The y-axis gives the value of the
                                                                                                                                                                                               at the end of each of those
    Since we were mainly interested in deriving rough          objective function on a logarithmic scale. The points in
                                                                                                                                                                                                   With this change, we r
order-of-magnitude estimates of tradeoffs between run-         the plot represent the current solution value, as sampled
                                                                                                                                                                                               200-element random instal
ning time and the quality of the annealing solutions           once every 5,050 steps. Also depicted is a horizontal line
                                                                                                                                                                                             ;instance, summarized in F
found, we did not do extensive experiments to optimize         with the y-coordinate equal to the value of the solution
                                                                                                                                                                                             ];iment concerned the 2oo-e
the parameters of the generic algorithm, but merely            found by the Karmarkar-Karp algorithm.
                                                                                                                                                                                             "'neighborhood. We perfor
adopt reasonable values based on the lessons learned              Note that although the best solution encountered was
                                                                                                                                                                                             l"FACTOR taking on val
from our experiments with graph partitioning in Part I.        better than the Karmarkar-Karp solution, the value to
                                                                                                                                                                                             ~running from 2 to 2,048.
(We did find it necessary to modify the generic termina-       which the process converged was substantially worse,
                                                                                                                                                                                             J'best solutions found for e
tion condition, however, due to the anomalous way that         and indeed was little better than the average value seen
                                                                                                                                                                                               t'+ "s, respectively, and
annealing behaves for this problem; see the next section.)     during the last quarter of the cooling schedule. This is in
                                                                                                                                                                                                jme. For comparison pur
In particular, we set INITPROB = 0.5 and TEMP-                 contrast to standard annealing time exposures like those
                                                                                                                                                                                                 ound by the Karmarkar-
FACTOR = 0.9, and adjust the length of time spent in           for graph coloring in the previous section, where the
                                                                                                                                                                                                ;epresented by a horizont
the annealing process by varying SIZEFA CTOR. (For             process converges essentially to the best value seen.
                                                                                                                                                                                                   In contrast to the bel
these experiments we kept CUTOFF = SIZEFACTOR;                 Since our implementation outputs the best solution seen
                                                                                                                                                                                                 ;artitioning and graph co
i.e., cutoffs were not used.)                                  rather than the last, this is not a fatal defect, although it
                                                                                                                                                                                                 olution values do not al
    The remaining detail to be filled in is the method for     does indicate that the neighborhood structure is having a
                                                                                                                                                                                               Jme increases, but remail
selecting the starting temperature. As no one temperature      rather striking effect on the annealing process.
                                                                                                                                                                                                'mallest move for this
seemed to work equally well for all n, we chose to use            These anomalies will also confuse our generic termi-
                                                                                                                                                                                                  .005, far above the Ka
an adaptive method. To explain this, we should say a           nation test, which was predicated on the assumption that
                                                                                                                                                                                                   ore precise, the averagl
little bit about how our experiments were performed.           "freezing" began when one stopped seeing improve-
                                                                                                                                                                                                        solutions found (n
For each instance and value of SIZEFACTOR consid-              ment in the current "champion" solution. As suggested
                                                                                                                                                                                                   2.27, whereas log JO(l
ered, we performed 10 annealing runs, all with the same        by Figure 9, the time at which the final champion
                                                                                                                                                                                                     smallest possible mov
starting temperature. This common starting temperature
                                                                                                                                                                                                               large, slight!
was based on the average uphill move encountered when
calling NEXT _CHANGE( ) N times (where N was the                      10,.----------------------,

neighborhood size) for each of 10 randomly chosen                                                                                                                                                                        200- ELEMENT IN'
                                                                                                                                                                                                  10- 1
initial solutions produced by INIT _SOLN( ). The initial
temperature was chosen so that the probability of accept-
ing this average uphill move was INITPROB = 0.5.               ?F
                                                                    to-I


                                                                    10-2
                                                                                                                                                                                                  10-2

                                                                                                                                                                                                  10-3
                                                                                                                                                                                                           o ~o   0
                                                                                                                                                                                                                  '0
                                                                                                                                                                                                                  III
                                                                                                                                                                                                                       80
                                                                                                                                                                                                                             t
                                                                                                                                                                                                                             0
                                                                                                                                                                                                                              0
                                                                                                                                                                                                                                    ~
                                                                                                                                                                                                                                      (J)




                                                               F
Such a technique is simpler but somewhat less accurate                                                                                                                                                         +                    6'
                                                               ~    10- 3
                                                                                                                                                                                                  10--4        ++*           +
                                                                                                                                                                                                                             +
                                                                                                                                                                                                             + + +                  ++
than the "trial run" technique used for selecting starting     E
                                                               ~    10--4
                                                                                                                            ** ***    *>11< ... "'....
                                                                                                                                                 ~* t.>Ilc>t:t* **
                                                                                                                                                                       •
                                                                                                                                                                     __ -
                                                                                                                                                                                                                             t+     +
                                                                                                                                 .. ",*.
                                                                                                                                                                                                  10- 5           -II-       ./l-   $-...
temperatures in Part 1. It tends to result in higher initial   E
                                                                                                                                           ",*      '" '" .. *'i'
                                                                                                                                                                                                            +
                                                                                                                                                                                                            +
                                                                                                                                                                                                                             +      ++
                                                                    10-5
temperatures, and hence, somewhat longer running times.                                                                                                                                            10-<;

Fortunately, our results did not depend on the fine                                                                                                                                                10-7
details of the running times, as we shall see.
                                                                    10-7 " - - - - - - - ' - - - - - - - - ' - - - - ' - - - - - - ' - - - - - - - - ' - - - - ' - - - - ' - - - - - - - '
                                                                                       200           400           600          800              1000           1200       1400
3.4. Experimental Results                                                                                       (NUMBER OF TRIALS)!N
                                                                                                                                                                                                                  100                500
All our experiments concern random instances of the            Figure 9. The evolution of the solution value for a                                                                                                                          Rl
type discussed in Section 2.1. In order that rounding                    random loo-element instance under simulated
                                                                                                                                                                                                                      Final and be
effects not obscure the quality of the solutions generated               annealing with the 2-swap neighborhood
                                                                                                                                                                                                                      spectively) f(
by the Karmarkar-Karp algorithm, each input number                       structure, compared to the solution found us'
                                                                                                                                                                                                                      random 200-,
was generated in multiprecision form, with 36 decimal                    ing the Karmarkar-Karp algorithm (dotted
                                                                                                                                                                                                                      stance, as a
digits to the right of the decimal point, and multi-                     line). (Note that one isolated annealing data
                                                                                                                                                                                                                      SIZEFACTC
precision arithmetic was used throughout.                                point falls below the dotted line.)
                                                                                                                                                          Graph Coloring by Simulated Annealing                                                 /      403

                             appears may be a random phenomenon, only tangentially                                                                   log 10(0.03) = - 1.52, and I-swap local optimization only
Jsure" of an individual
                             related to the convergence of the annealing process.                                                                    has - 1. 80 as its average value for log JO( difference).
~lement instance, using
                             Since for this study we were interested in the final frozen                                                             Thus, although time spent on annealing in excess of 50
and SIZEFACTOR ==
                             value as well as the champion, we modified the termina-                                                                 seconds seems wasted if one is interested only in final
ditions were turned off"
                             tion conditions in the experiments reported below as                                                                    solutions, that first 50 seconds seems to have been worth
I until visual evidence'
                             follows: To halt, we require that the acceptance ratio be                                                               something.
: in.) The x-axis of the!
                             less than MINPERCENT = I % and that the solution                                                                           The best solutions tell a different story: these im-
ecisely, the number o(
                             value remain unchanged during each of the last 10                                                                       proved steadily with increased running times, approach-
vided by the neighbor- 1:
                             temperatures (or more precisely, that the values reported                                                               ing the solution value obtained by the Karmarkar-Karp
) gives the value of the:
                             at the end of each of those temperatures all be the same).                                                              algorithm. Note, however, that in this range we are
lic scale. The points in
                                With this change, we ran a suite of experiments on a                                                                 spending well over 10,000 times the 1.1 seconds re-
Jtion value, as sampled
                             ZOO-element random instance, and a 500-element random                                                                   quired by Karmarkar and Karp, which is enough time for
lcted is a horizontal line
                             instance, summarized in Figures 10-13. Our first exper-                                                                 over 100,000 runs of I-swap local optimization (ignoring
Ie value of the solution
                             iment concerned the 200-element instance and the I-swap                                                                 input time, which can be amortized, 10 such runs can be
~orithm.
                             neighborhood. We performed 10 trials each with SIZE-                                                                    performed in a second). Figure II compares our anneal-
lution encountered was
                             FACTOR taking on values equal to the powers of 2                                                                        ing results with those obtained by spending an equivalent
  solution, the value to
                             running from 2 to 2,048. Figure 10 depicts the final and                                                                amount of time performing local optimization from ran-
as substantially worse,
                             best solutions found for each run, marked by "o"s and                                                                   dom starts. For each value J = 500, 1,000, ... ,
 the average value seen:
                             " + "s, respectively, and plotted as a function of running                                                             512,000, we perform 10 independent sets of J runs of
ing schedule. This is
                             time. For comparison purposes, the value of the solution                                                               local optimization, and plot the best solution in that
ne exposures like those
                             found by the Karmarkar-Karp algorithm is once again                                                                    subset versus the overall running time for the group (as
)us section, where the
                             represented by a horizontal dotted line.                                                                               estimated from our figure for the average time per run),
) the best value seen.
                                In contrast to the behavior of annealing on graph                                                                   These points, marked by 'o's, were then combined with
) the best solution seen
                           , partitioning and graph coloring, here the final annealed                                                               the data points for annealing bests from Figure 10.
fatal defect, although it
                             solution values do not appreciably improve as running                                                                      Note that across the board local optimization does just
Jd structure is having
                             time increases, but remain in the vicinity of the expected                                                              as well as annealing, if not better. Moreover, even if we
lling process.
                             smallest move for this neighborhood, i.e., 1/200 =                                                                     could speed up our annealing implementation by a factor
fuse our generic
                             0.005, far above the Karmarkar-Karp solution. To be                                                                    of 4, the resulting comparison (obtained by shifting the
  on the assumption
                             more precise, the average of log JO( difference) over all                                                               local optimization data points two steps to the right)
)pped seeing
                             final solutions found (regardless of running time) is                                                                   would still be about equal. When we turn to the 2-swap
  solution. As su~~ge:sted
                              - 2.27, whereas log JO(l /200) = - 2.30. Interestingly,                                                                neighborhood, or larger instances under the I-swap
~h the final
                             the smallest possible move for this instance is uncharac-
                             teristically large, slightly bigger than 0.03, yielding
                                                                                                                                                                             S[MULATED ANNEALING VERSUS LOCAL OPTIMIZATION
                                                                                                                                                          10- 3

                                                                                                                                                                              +

                                     10- 1
                                                               2ao-ELEMENT INSTANCE. I-SWAP NE[GHBORHOODS
                                                                                                                                                            ~~ + ++"
                                                                                                                                                          10-4
                                                                                                                                                                      +
                                                                                                                                                                 g + 0+                 ~+         +

                                     10-2
                                              ° 0° ° 8°
                                             If'        'I>
                                                        III
                                                                   t        #J
                                                                               (f)


                                                                                        f
                                                                                            0    6'0
                                                                                                    d'
                                                                                                           d'
                                                                                                           ~
                                                                                                                         I0     I°   <\\
                                                                                                                                     B
                                                                                                                                               •
                                                                                                                                               ~
                                                                                                                                                      D 10-
                                                                                                                                                      I
                                                                                                                                                            1ft 0
                                                                                                                                                                5... ~
                                                                                                                                                               + 0
                                                                                                                                                                     tJt+


                                                                                                                                                                                   0+
                                                                                                                                                                                        .
                                                                                                                                                                                        ll";1-
                                                                                                                                                                                                   +
                                                                                                                                                                                                   +
                                                                                                                                                                                                  0+
                                                                                                                                                                                                  0++
                                                                                                                                                                                                          ++
                                                                                                                                                                                                          ++
                                                                                                                                                                                                         g+
                                              0                   0                             i                               0                                                                              IJ'
                                     10- 3                         0                                       8
                                                                                                           00
                                                                                                                                     0                F                  +              r+        l+     r;                 t
                                                                                                                                                                                                               ~+
                                                                                                                                     B                F
                                              °                                                                                                       E                                                                 St+
                                            .....
                                             +
                                 I 10-4 ~ + + +
                                 D                +
                                                   +
                                                                            d'
                                                                                                                                                      ~
                                                                                                                                                          [0""                                    0+
                                                                                                                                                                                                   +     0+
                                                                                                                                                                                                                 +      tlt
                                                                                                                                                                                                                           +
                                                                                                                                                                                                                                   0+
                                                                                                                                                                                                                                    +
                                                                                                                                                                                                                                   e"+
                                                                                                                                                                                                                                            +
                                                                                                                                                                                                                                            "
                                                                                                                                                                                                                                                     +
                                                                                                                                                                                                                                                     ....
                                 F                                t+        ++          t                                                             N                                                  8      +                          0+
                                              +                             +                                                                                                                                           8....      B++              0#
                                 F
                                 E   10- 5 ft+          -II-       ~        :\1-. .
                                                                                        +
                                                                                        +       1++
                                                                                                                                                      C
                                                                                                                                                      E   10-7                                                  +
                                                                                                                                                                                                                +
                                                                                                                                                                                                                        0          0+
                                                                                                                                                                                                                                       +   80.... 8"
                                 R
                                 E
                                 N
                                             +
                                                                   +         ++         ++
                                                                                        -t
                                                                                                 +
                                                                                                 +
                                                                                                           +             +
                                                                                                                          t
                                                                                                                                                                                                                                   0
                                                                                                                                                                                                                                            +
                                                                                                                                                                                                                                           0+
                                                                                                                                                                                                                                                    6+
                                                                                                           ~
                                     10""
                                                                                                "                        +++         +
                                 ~
                                                                                                                         " \t+ ...." t"
                                                                                         +                                                     +
                                                                                         +                 ++                        +
                                                                                                           +             -II-
                                     10-7                                                                                       +
                                                                                                           +                                    +               9
                                                                                                                                +    +                    10-       "'--'-------'----'-                               '-------'-                --'-_......l
                                     10-8                                                                                            +
                                                  ,~.<l!1:Dpr\o;fl_~-K_arp .so.1.uti.oq (l., 1.S,c~qn4~)                                                            50       100         500       WOO               5000                       50000
    1000   1200   1400   1600
                                                                                                                                                                                                 Running Time in Seconds
UALS)!N                              10-9
                                             50       [00                    500        [000                   5(](]()                     5lX1OO   Figure 11. Comparison of best solutions found on an-
~  solution value for a                                                               Running Time in Seconds                                                  nealing runs ( + 's) with best solutions found
nstance under simulated
                                Figure 10. Final and best solutions (o's and + 's, re-                                                                         by performing multiple starts of local opti-
  2-swap neighborhood
                                           spectively) found by I-swap annealing for a                                                                         mization for an equivalent amount of time
) the solution found us-
                                           random 200-element number partitioning in-                                                                          (o's). (Results are for the 200-element in-
:arp algorithm (dotted
                                           stance, as a function of running time as                                                                            stance of Figure 10, with both algorithms
 isolated annealing data
                                           SIZEFACTOR increases from 2 to 2,048.                                                                               using the I-swap neighborhood.)
lotted line.)
404           /   JOHNSON ET AL.


neighborhood, the comparison is no longer close, and                                                              SOO-ELEMENT INSTANCE. I-SWAP NEIGHBORHOODS                              amounts of running time, (
multiple start local optimization substantially outper-                                             JO--4
                                                                                                                   "j!-
                                                                                                                                                                                          by the time n = 500.
                                                                                                                                ....
forms annealing, as can be seen in Figures 12 and 13.
   Figure 12 shows the results for the 2-swap neighbor-
                                                                                                   10-5
                                                                                                                  :t-
                                                                                                                      J          +
                                                                                                               g}- + jI-;,. :t:+ +$+
                                                                                                                                       ++
                                                                                                                                         +

                                                                                                                                                                                           but
                                                                                                                                                                                              We did not perform exp,
                                                                                                                                                                                                  the trends are alread)

                                                                                                                                                                            ,
                                                                                                                        0+                                         ++
                                                                                                               8+            II                    +       -H-++         +
                                                                                                   10"                + 8    0                                        #-                   expectations:        Annealing I
hood and the 200-element instance of Figures IO and 11.
                                                                                                                                   8t
                                                                                                                                                    +
                                                                                                                                                           ot 4: +'t.- +++
The best solutions found by annealing during 10 runs
                                                                                                D
                                                                                                I
                                                                                                F lO-7
                                                                                                                             S+
                                                                                                                                      0
                                                                                                                                                Q
                                                                                                                                                B+      *          +
                                                                                                                                                                             ;,.    ...    slightly lesser extent) wi
each for SIZEFACTOR = 0.25, 0.5, 1,2,4 and 8 are
                                                                                                F
                                                                                                E
                                                                                                R
                                                                                                E 10- 8
                                                                                                                                      0
                                                                                                                                      0         i
                                                                                                                                                @
                                                                                                                                                8          0
                                                                                                                                                                           cJ+
                                                                                                                                                                           0+
                                                                                                                                                                                           outclassed
                                                                                                                                                                                     * crease. Note that ty
                                                                                                                                                                                                             by Karmarkar
plotted, along with the best solutions found during 10
trials each of 150, 300, 600, 1,200, 2,400 and 4,800
                                                                                                N
                                                                                                c
                                                                                                E
                                                                                                   10- 9
                                                                                                                                                                    t I            @
                                                                                                                                                                                            (Karmarkar-Karp) are]
                                                                                                                                                                                   0
local optimization runs. (For the 2-swap neighborhood,                                                                                                                                      (in 6.5 seconds), - 16 fOI
                                                                                                  10- 10
local optimization takes about 6.5 seconds per run, so                                                                                                                                      and - 24 for n = 1O,OC
                                                                                                             .... ~~.~~~~~~~~.~~.~~.I~.t.i~~. q.".l..~~~~.~~.~~
150 runs take roughly 1,000 seconds.) Many data points                                                11
                                                                                                  10. t....----'-            ----'-_---L                       -'--_'--            '---.J   number partitioning, at
                                                                                                         SO   100              SOO 1000                       Sooo               soooo      dom instances we have b
fall below the line representing the Karmarkar-Karp
                                                                                                                                     Running Time in Seconds
solution, although most of them come from local opti-                                                                                                                                     !limitations of simulated ar
mization. The annealing bests appear to be only slightly                                       Figure 13. Comparison for the I-swap neighborhood                                          ~,When          the solution spa
better on average than those obtained in equivalent time                                                           and a 500-element random instance of besl                              ~bus,       annealing's   advantag
using the I-swap neighborhood, as shown in Figure 10.                                                              solutions found on annealing runs ( + 's) with                         ~:start      local optimization   c
(Although not depicted here, the final values found by                                                             best solutions found by performing multiple                            ,       er    approaches,   not tie
annealing were again relatively independent of running                                                             starts of local optimization for an equivalent                               ound a solution space,
time, and slightly better than those obtained by local                                                             amount of time (o's).                                                        bstantially.
optimization. Here the average of 10gJO(difference) for                                                                                                                                          There remains the qu
all annealing runs was -4.76, compared to -4.60 for                                                                                                                                              ighborhood structure D
                                                                                              from 1-512. (The final values found were again rela-
local optimization. Both these values are substantially                                                                                                                                        'fferent notions of soluti
                                                                                              tively independent of running time, with the average of
better than those we obtain using the I-swap neighbor-                                                                                                                                            enable to annealing. 1
                                                                                              log JO( difference) for all annealing runs being - 3.57,
hood structure, and presumably reflect the fact that much                                                                                                                                      'lity, although at prese
                                                                                              compared to - 3.04 for local optimization and - 2.7 for
smaller moves are possible with the S W 2 , on the order                                                                                                                                        rnatives. The natural i<
                                                                                              log JO(l /500). For this instance, the smallest possible
of 1/200 2 instead of 1/200; note that log JO(l /200 2 ) =                                                                                                                                        plementation by repla
                                                                                              move was substantially smaller than expected.)
 -4.53.)                                                                                          Once again, local optimization substantially outper-                                          ve     function by loge difJ
   Figure 13 shows the results for a 500-element instance                                                                                                                                         Ip, based on limited ex
                                                                                              forms annealing on a time-equalized basis. Also, as
and the I-swap neighborhood. Here annealing was run                                                                                                                                              ation of additional poss
                                                                                              expected, both annealing and local optimization are much
with values of SIZEFACTOR going up by factors of 2                                            further away from the Karmarkar-Karp solution value
                      ZOO-ELEMENT INSTANCE, Z-SWAP NEIGHBORHOODS
                                                                                              than they were in the 200-e1ement case, This is true even                                         . CONCLUSION
      10"     c-------------------                                                            if we allow for a linear increase in running time with
                                                                                                                                                                                                    this paper, we consid,
                                          +
                                                                                              instance size, as happens with annealing when we com-
                             + :lie   +                                                                                                                                                           nealing for two proble:
      10"                   ++
                              +
                                                    ++
                                                                                              pare results for a fixed value of SIZEFACTOR. For
                                           ++      + +          ++                                                                                                                                ought accessible to loc
 D
                              +0
                                          +
                                                   ++
                                                      +         + +
                                                                    +    +....
                                                                                              example, when SIZEFACTOR = 512, the median an-
                                                                                                                                                                                               _ aph coloring and numl
 I                                                  +           ++                            nealing best is only 40 times larger than the Karmarkar-
      10-7                    +§                                         -H--<t
 F                                    + +8                                              +~
 F                                       0             +~           +0                                                                                                                          ring results, as summar
 E
 R                                       8                                        ~      +    Karp solution when n = 200, whereas it is roughly
 E                                                      9                         0      +0                                                                                                     Jy positive for simulat,
 N    10.8                                              9                         0            10,000 times larger when n = 500. For local optimiza-
 C                 .. 0'"
                                                                                  5       0                                                                                                     llierate the large compt
 E
                                                                                          8   tion and equivalent running times, the corresponding
                                                                                  0       0                                                                                                     .ults for number partitic
      10"                                                           +B
                                                                                  0     ++S   ratios are roughly 40 and ISO-still growing, but not
                                                                                  0       0                                                                                                         ly negative, with anne
                                                                                              quite so rapidly.
                                                                                                                                                                                                      the much faster Karrr
     10- 10                                                                                       We performed limited experiments using the 2-swap
                                                                                                                                                                                                    aten (on a time-equali.
                    1000                        SOOO        10000                     soooo   neighborhood on the 500-element instance, but, within
                                          Running Time in Seconds                                                                                                                                 , timization.
                                                                                              the 100,000 second time bound (approximately 30 hours)
                                                                                                                                                                                                     This all fits in with th,
Figure 12. Comparison for the 2-swap neighborhood of                                          neither 2-swap annealing nor 2-swap local optimization
                                                                                                                                                                                                     per (Johnson et aI. l'
           best solutions found on annealing runs (+ 's)                                      did as well as our I-swap results. (The quadratic growth
           with best solutions found by performing                                                                                                                                                :, ly valuable tool but
                                                                                              rate of the 2-swap neighborhood seems to have begun to
           multiple starts of local optimization for an                                                                                                                                            ohnson et aI. 1990) VI
                                                                                              take its toll; one run of 2-swap local optimization takes
           equivalent amount of time (o's). (Results are                                                                                                                                             ploration of how well
                                                                                              40 seconds on average, versus 0.25 seconds for I-swap
           again for the 200·element random instance                                                                                                                                                e more traditional co
                                                                                              local optimization.) Thus, although we could approach
           of Figure 10, and the dotted line represents                                                                                                                                          ,amous combinatorial 01
                                                                                              and even surpass the performance of the Karmarkar-Karp
           the Karmarkar-Karp solution.)                                                                                                                                                          nd the one for which il
                                                                                              algorithm when n = 200, given large but feasible
                                                                                                                   Graph Coloring by Simulated Annealing           /   405
I-SWAP NEIGHBORHOODS                            amounts of running time, our luck seems to have run out         (1985) and Kirkpatrick, Gelatt and Veechi (1983): the
                                               by the time n = 500.                                            traveling salesman problem.
                                                   We did not perform experiments for values of n > 500,          In performing our final experiments for that paper
                                               but the trends are already obvious and conform to our           shall take into account several lessons learned from ilie

                                   ,
              .+
                    ....-• .+
   •.f+
   o\.        .J
              ..;                              expectations: Annealing (and local optimization, to a           experiments reported here. First, due to difficulties we
              +     ~     +
                                                slightly lesser extent) will be even more substantially        encountered, it has become clear iliat both our starting
                           ij.
          0                         ....
          §                                    outclassed by Karmarkar Karp as n continues to in-              and terminating procedures need revision.
                         t *
                         et+
          8
          0                                    crease. Note that typically values for log 10                      Our current termination tests ask whether FREEZE_
                                               (Karmarkar-Karp) are less than: -13 for n = 1,000               LIM consecutive temperatures have occurred in which:
                                               (in 6.5 seconds), - 16 for n = 2,000 (in 13.6 seconds),         a) the acceptance ratio was below MINPERCENT, and
                                               and -24 for n = 10,000 (in 75.8 seconds). Thus,                 b) no improvement in the best solution seen has taken
                                               number partitioning, at least for the types of ran-             place. For several types of instances encountered, we
      5000                       50000         dom instances we have been considering, illustrates the         had to make major changes in ilie termination parameters
e in Seconds
                                               limitations of simulated annealing as a general technique.      simply because an abundance of O-cost moves kept ilie
le I-swap neighborho                           When the solution space is sufficiently mountain-               acceptance frequency high, even though no further im-
 random instance of be                         ous, annealing's advantage over straightforward multiple        provement in cost was occurring. Thus, the termination
annealing runs ( + ' s) wi'                    start local optimization can be lost entirely. Moreover,        condition should probably be altered so iliat only ilie rate
d by performing multip                         other approaches, not tied to the concept of navigating         at which uphill moves are accepted is relevant (a very
nization for an equivalerl                     around a solution space, may be able to outperform it           simple modification).
s).                                            substantially.                                                     We also found ourselves regularly having to choose
                                                   There remains the question of wheilier some oilier          starting temperatures in an ad hoc manner because the
• found were again relat                       neighborhood structure for the problem, perhaps using           generic methods we had devised for this (using either
 ime, with the average 0"                      different notions of solution and cost, might prove more        trial runs or multiple calls to NEXT _CHANGE) were
lling runs being - 3.57,                       amenable to annealing. We do not rule out this possi-           not sufficiently robust. We suspect that, for most prob-
Jtimization and - 2.7 fot:                     bility, although at present we see not reasonable al-           lems, starting temperatures can be determined using
 e, the smallest possibl~,                     ternatives. The natural idea of modifying the annealing         simple problem-specific formulas (analytically or empiri-
 than expected.)           .                   implementation by replacing difference as the objec-            cally derived) that depend only on the desired initial
ion substantially outper~'                     tive function by loge difference) appears to be of little       acceptance ratio and a few easily computable parameters
lualized basis. Also, a                        help, based on limited experiments. We leave ilie invest-       of the instance. For instance, I V I and I E I might well
;al optimization are muc~                      igation of additional possibilities to future researchers.      suffice in the case of graph coloring. Thus, there is
rkar-Karp solution valu.                                                                                       likely to be a problem-specific INITIAL_TEMP routine
 nt case. This is true eve                                                                                     in our future implementations.
                                               4. CONCLUSION
lse in running time with                                                                                          A final observation is that the running-time/quality-
annealing when we com{                          In this paper, we consider implementations of simulated        of-solution tradeoff inherent in most annealing imple-
 of SIZEFACTOR. For                             annealing for two problems that had previously not been        mentations may well extend far beyond the standard
~ = 512, the median an~                        thought accessible to local optimization and its variants:      limits of acceptable running time. In our graph coloring
rger than the KarmarkW;                         graph coloring and number partitioning. Our graph col-         experiments, we saw positive results come out of runs
   whereas it is roughly!                       oring results, as summarized in Section 2.5, were gener-       that took a week or more of continuous computing. That
500. For local optimiza-i                      ally positive for simulated annealing, assuming one can         this may be of more than academic interest follows from
imes, the corresponding;,                      tolerate the large computation times involved. The re-          the rapid rate at which the price of computer cycles is
-still growing, but not!li                     sults for number partitioning were, as expected, decid-         declining. That compute-week could be almost free if it
                                               edly negative, with annealing substantially outperformed        were spent on one of the idle personal computers iliat
                                           i   by the much faster Karmarkar-Karp algorithm, and even           now decorate many offices, or it could be an overnight
 iments using the 2-swap'
~nt instance, but, within                      beaten (on a time-equalized basis) by multiple start local      background run on one of the much faster machines
(approximately 30 hours)                       optimization.                                                   becoming more widely available. For problems in which
 -swap local optimization                         This all fits in with the view expressed in Part I of this   the economic value of finding improved solutions is
s. (The quadratic growth                       paper (Johnson et aI. 1989), iliat annealing is a poten-        substantial, this is a thought to keep in mind.
I seems to have begun to                       tially valuable tool but in no ways a panacea. Part III
  local optimization takes                     (Johnson et aI. 1990) will conclude this series with an
                                               exploration of how well simulated annealing does against        REFERENCES
0.25 seconds for I-swap
>ugh we could approach                         the more traditional competition on perhaps the most            AARTS, E. H. L., AND J. H. M. KORST. 1989. Simulated
:e of the Karmarkar-Karp                       famous combinatorial optimization problem of them all,              Annealing and Boltzmann Machines. John Wiley &
ven large but feasible                         and the one for which it was originally touted by Cerny             Sons, Chichester, U.K.
406    /   JOHNSON ET AL.                                                                                                                         OJ
BERGER, B., AND J. ROMPEL. 1990. A Better Perform-         KARMARKAR, N., R. M. KARP, G. S. LUEKER AND A. M,                               PARA
    ance Guarantee for Approximate Graph Coloring.             ODLYZKO. 1986. Probabilistic Analysis of Optimum
      Algorithmica 5, 459-466.                                 Partitioning. J. Appl. Prob. 23, 626-645.
BOLLOBAS, B., AND A. THOMASON. 1985. Random Graphs         KERNIGHAN, B. W., AND S. LIN. 1970. An Efficient Heuris-
    of Small Order. Ann. Discrete Math. 28,47-97.              tic Procedure for Partitioning Graphs. Bell Syst. Tech.
BRELAZ, D. 1979. New Methods to Color Vertices of a            J. 49, 291-307.
    Graph. Comm. ACM 22, 251-256.                          KIRKPATRICK, S., C. D. GELATT AND M. P. VECCHI. 13
BROUWER, A. E., 1. B. SHEARER, N. J. A. SLOANE AND W.          MAY 1983. Optimization by Simulated Annealing.
    D. SMITH. 1990. A New Table of Constant Weight             Science 220, 671-680.                                                              (Reo
    Codes. IEEE Trans. In! Theory 36, 1334-1380.           LEIGHTON, F. T. 1979. A Graph Coloring Algorithm for
CERNY, V., 1985. A Thermodynamical Approach to the             Large Scheduling Problems. J. Res. Natl. Bur.                   This paper deals with
    Traveling Salesman Problem: An Efficient Simulation        Standards 84, 489-506.                                          maximize the system'
    Algorithm. J. Optimiz. Theory Appl. 45,41-51.          LIN, S., AND B. W. KERNIGHAN. 1973. An Effective Heuris-            reliability of compone
CHAMS, M., A. HERTZ AND D. DE WERRA. 1987. Some                 tic Algorithm for the Traveling-Salesman Problem.              developed to obtain aI
    Experiments With Simulated Annealing for Coloring          Opns. Res. 21, 498-516.                                         with only two positior
    Graphs. Eur. J. Opns. Res. 32, 260-266.                MATULA, D. W., G. MARBLE AND J. D. ISAACSON. 1972.
COLUNS, N. E., R. W. EGLESE AND B. L. GOLDEN. 1988.            Graph Coloring Algorithms. In Graph Theory and
    Simulated Annealing: An Annotated Bibliography.            Computing, R. C. Read (ed.). Academic Press, New
      Am. J. Math. Mgmt. Sci. 8, 205-307.                      York.
DE WERRA, D. 1985. An Introduction to Timetabling. Eur.


                                                                                                                         .c
                                                           MORGENSTERN, C. 1989. Algorithms for General Graph
    J. Opns. Res. 19, 151-162.
                                                               Coloring. Doctoral Dissertation, Department of
GAREY, M. R., AND D. S. JOHNSON. 1976. The Complexity                                                                           onsider a reliabilit
                                                               Computer Science, University of New Mexico,
    of Near-Optimal Graph Coloring. J. Assoc. Comput.                                                                           slots. Suppose that
                                                               Albuquerque.
      Mach. 23, 43-49.
                                                           MORGENSTERN, C., AND H. SHAPIRO. 1986. Chromatic              which can be assigned t
GAREY, M. R., AND D. S. JOHNSON. 1979. Computers and
                                                               Number Approximation Using Simulated Annealing.           reliability of component
    Intractability: A Guide to the Theory of NP-
                                                               Unpublished manuscript.                                   position i, that is, the
    Completeness. W. H. Freeman, San Francisco.
                                                           OPSUT, R. J., AND F. S. ROBERTS. 1981. On the Fleet             epends on the position i
GLOVER, F. 1989. Tabu Search, Part I. ORSA J. Comput.
    1, 190-206.
                                                               Maintenance, Mobile Radio Frequency, Task Assign-           everal practical situati<
                                                               ment, and Traffic Phasing Problems. In The Theory            or example, some pc
GRIMMET, G. R., AND C. J. H. McDIARMID. 1975. On
    Colouring Random Graphs. Math. Proc. Cambridge
                                                               and Applications of Graphs, G. Chartrand, Y. Alavi,         xposed to the frequent
                                                               D. L. Goldsmith, L. Lesniak-Foster and D. R. Lick
      Phi/os. Soc. 77, 313-324.                                                                                          rest are well protected
                                                               (eds.). John Wiley & Sons, New York, 479-492.
HERTZ, A., AND D. DE WERRA. 1987. Using Tabu Search                                                                      Sometimes, the intensity
    Techniques for Graph Coloring. Computing 39,           SHAMIR, A. 1979. On the Cryptocomplexity of Knapsack
                                                                                                                          ion to position. In this
      345-351.                                                 Systems. In Proceedings lith Annual ACM Sympo-
                                                               sium on Theory of Computing. Association for Com-            f assigning component:
JOHNSON, D. S. 1974. Worst-Case Behavior of Graph Col-
                                                               puting Machinery, New York, 118-129.                      the system's reliabilit:
    oring Algorithms. In Proceedings 5th Southeastern
                                                           THOMASON, A. 1987. Private communication.                     Sethuraman (1986) con
      Conference on Combinatorics, Graph Theory, and
      Computing. Utilitas Mathematica Publishing,          VAN LAARHOVEN, P. J. M. AND E. H. L. AARTS. 1987.                 ries (PS) and series-pa
    Winnipeg, 513-527.                                         Simulated Annealing: Theory and Practice. Kluwer             hey elegantly obtain a
JOHNSON, D. S., C. R. ARAGON, L. A. MCGEOCH AND C.             Academic Publishers, Dordrecht, The Netherlands.             ents for PS systems u:
    SCHEVON. 1989. Optimization by Simulated Annealing:    VECCHI, M. P., AND S. KIRKPATRICK. 1983. Global Wiring           nd the nature of Scht
    An Experimental Evaluation, Part I, Graph Partition-       by Simulated Annealing. IEEE Trans. Computer-                erive some interestinf
    ing. Opns. Res. 37, 865-892.                               Aided Design of Integrated Circuits and Systems              ptimal allocations in Sl
JOHRI, A., AND D. W. MATULA. 1982. Probabilistic Bounds        CAD-2, 215-222.                                           ,onfine ourselves to the
    and Heuristic Algorithms for Coloring Large Random     WELSH, D. J. A., AND M. B. POWELL. 1967. An Upper                  The problem of maxi I
    Graphs. Technical Report, Southern Methodist Univer-      Bound on the Chromatic Number of a Graph and Its            . rough the optimal ass
    sity, Dallas, Texas.                                      Application to Timetabling Problems. Comput. J. 10,
                                                                                                                            ombinatorial in nature.
KARMARKAR, N., AND R. M. KARP. 1982. The Differencing          85-86.
                                                                                                                             e maximization of a nl
    Method of Set Partitioning. Report No. UCB/CSD         WIGDERSON, A. 1983. Improving the Performance Guar-
                                                                                                                            ~bject to linear constr;
    82/113, Computer Science Division, University of           antee of Approximate Graph Coloring. J. AssoC.
    California, Berkeley.                                      Comput. Mach. 30, 729-735.                                    e concept of majorizat
                                                                                                                           ,s well as PS systems

                                                                                                                          Ubject classification: Relial
