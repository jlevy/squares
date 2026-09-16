               BY SIMULATEDANNEALING:AN EXPERIMENTAL
    OPTIMIZATION
           EVALUATION;PART 1, GRAPH PARTITIONING
                                                            DAVIDS. JOHNSON
                                                A T&T Bell Laboratories, Murray Hill, New Jersey


                                                           CECILIAR. ARAGON
                                                   University of California, Berkeley, California

                                                            LYLEA. McGEOCH
                                                     Amherst College, Amherst, Massachusetts

                                                         CATHERINESCHEVON
                                                 Johns Hopkins University, Baltimore, Maryland
                             (ReceivedFebruary1988;revisionreceivedJanuary1989;acceptedFebruary1989)

        In this and two companionpapers,we reporton an extendedempiricalstudy of the simulatedannealingapproachto
        combinatorialoptimizationproposedby S. Kirkpatricket al. That study investigatedhow best to adapt simulated
        annealingto particularproblemsand comparedits performanceto that of more traditionalalgorithms.This paper(Part
        I) discusses annealingand our parameterizedgeneric implementationof it, describeshow we adaptedthis generic
        algorithmto the graphpartitioningproblem,and reportshow well it comparedto standardalgorithmslike the Kernighan-
        Lin algorithm.(For sparserandomgraphs,it tended to outperformKernighan-Linas the numberof verticesbecome
        large,even when its much greaterrunningtime was taken into account.It did not performnearlyso well, however,on
        graphsgeneratedwitha built-ingeometricstructure.)We alsodiscusshow we wentaboutoptimizingourimplementation,
        and describethe effectsof changingthe variousannealingparametersor varyingthe basicannealingalgorithmitself.




A ew approach to the approximate solution of                                     new problems (even in the absence of deep insight
      difficult combinatorial optimization problems                              into the problems themselves) and, because of its
recently has been proposed by Kirkpatrick,Gelatt and                             apparent ability to avoid poor local optima, it offers
Vecchi (1983), and independently by Cerny (1985).                                hope of obtaining significantlybetter results.
This simulatedannealingapproach is based on ideas                                  These observations, together with the intellectual
from statistical mechanics and motivated by an anal-                             appeal of the underlying physical analogy, have
ogy to the behavior of physical systems in the presence                          inspiredarticlesin the popular scientific press(Science
of a heat bath. The nonphysicist, however, can view                              82, 1982 and Physics Today 1982) as well as attempts
it simply as an enhanced version of the familiar tech-                           to apply the approach to a variety of problems, in
nique of local optimizationor iterativeimprovement,                              areas as diverse as VLSI design (Jepsen and
in which an initial solution is repeatedlyimproved by                            Gelatt 1983, Kirkpatrick, Gelatt and Vecchi 1983,
making small local alterationsuntil no such alteration                           Vecchi and Kirkpatrick 1983, Rowan and Hennessy
yields a better solution. Simulated annealing random-                            1985), pattern recognition (Geman and Geman 1984,
izes this procedurein a way that allows for occasional                           Hinton, Sejnowski and Ackley 1984) and code gen-
uphillmoves(changes that worsen the solution), in an                             eration (El Gamal et al. 1987), often with substantial
attempt to reduce the probability of becoming stuck                              success. (See van Laarhoven and Aarts 1987 and
in a poor but locally optimal solution. As with local                            Collins, Eglese and Golden 1988 for more up-to-date
search, simulated annealing can be adapted readily to                            and extensive bibliographiesof applications.)Many of
Subject classifications: Networks/graphs, heuristics: algorithms for graph partitioning. Simulation, applications: optimization by simulated annealing.

Operations Research                                                                                                  0030-364X/89/3706-0865 $01.25
Vol. 37, No. 6, November-December 1989                                     865                           ? 1989 Operations Research Society of America




                                This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                                 All use subject to JSTOR Terms and Conditions
866 /     JOHNSON ET AL.

  the practicalapplications of annealing, however, have           for sparse random graphs it tended to outperform
  been in complicated problem domains, where pre-                 Kernighan-Lin as the number of vertices became
  vious algorithms either did not exist or perfom-led             large. For a class of random graphs with built-in
  quite poorly. In this paper and its two companions,             geometric structure,however, Kernighan-Linwon the
  we investigatethe performanceof simulated annealing             comparisonsby a substantialmargin. Thus, simulated
  in more competitive arenas, in the hope of obtaining            annealing's success can best be describedas mixed.
  a better view of the ultimate value and limitations of             Section 4 describes the experiments by which we
 the approach.                                                    optimized the annealing parametersused to generate
    The arena for this paper is the problem of partition-         the resultsreportedin Section 3. Section 5 investigates
 ing the vertices of a graph into two equal size sets to          the effectiveness of various modifications and alter-
 minimize the number of edges with endpoints in                   natives to the basic annealing algorithm. Section 6
 both sets. This application was first proposed by                discusses some of the other algorithmsthat have been
 Kirkpatrick, Gelatt and Vecchi, but was not exten-               proposed for graph partitioning, and considers how
 sively studied there. (Subsequently, Kirkpatrick 1984            these might factor into our comparisons. We conclude
 went into the problem in more detail, but still did not          in Section 7 with a summary of our observationsabout
 deal adequately with the competition.)                           the value of simulated annealing for the graph parti-
    Our paper is organized as follows. In Section 1, we           tioning problem, and with a list of lessons learned that
 introduce the graph partitioning problem and use it              may well be applicable to implementations of simu-
 to illustrate the simulated annealing approach. We               lated annealing for other combinatorial optimization
 also sketch the physical analogy on which annealing              problems.
 is based, and discuss some of the reasons for optimism              In the two companion papers to follow, we will
 (and for skepticism) concerning it. Section 2 presents           report on our attempts to apply these lessons to three
 the details of our implementation of simulated anneal-           other well studied problems: Graph Coloring and
 ing, describing a parameterized, generic annealing               Number Partitioning (Johnson et al 1990a), and the
 algorithm that calls problem-specificsubroutines,and             Traveling Salesman Problem (Johnson et al. 1990b).
 hence, can be used in a variety of problem domains.
    Sections 3 through 6 present the results of our               1. SIMULATEDANNEALING:THE BASIC
experiments with simulated annealing on the graph                    CONCEPTS
partitioning problem. Comparisons between anneal-
ing and its rivals are made difficult by the fact that            1.1. Local Optimization
the performance of annealing depends on the partic-              To understand simulated annealing, one must first
ular annealing schedule chosen and on other, more                understand local optimization. A combinatorial opti-
problem-specific parameters. Methodological ques-                mization problem can be specified by identifying a set
tions also arise because annealing and its main com-             of solutions together with a cost function that assigns
petitors are randomized algorithms (and, hence, can              a numerical value to each solution. An optimal solu-
give a variety of answers for the same instance) and             tion is a solution with the minimum possible cost
because they have running times that differ by factors           (there may be more than one such solution). Given
as large as 1,000 on our test instances. Thus, if com-           an arbitrarysolution to such a problem, local opti-
parisons are to be convincing and fair, they must be             mization attempts to improve on that solution by a
based on large numbers of independent runs of the                series of incremental, local changes. To define a local
algorithms, and we cannot simply compare the aver-               optimization algorithm, one first specifies a method
age cutsizes found. (In the time it takes to perform             for perturbingsolutions to obtain different ones. The
one run of the slower algorithm, one could perform               set of solutions that can be obtained in one such step
many runs of the faster one and take the best solution           from a given solution A is called the neighborhoodof
found.)                                                          A. The algorithmthen performsthe simple loop shown
    Section 3 describes the problem-specific details of          in Figure 1, with the specific methods for choosing S
our implementation of annealing for graph partition-             and S' left as implementation details.
ing. It then introducestwo generaltypes of test graphs,             Although S need not be an optimal solution when
and summarizes the results of our comparisons                    the loop is finally exited, it will be locally optimal in
between annealing, local optimization, and an algo-              that none of its neighbors has a lower cost. The hope
rithm due to Kernighan-Lin(1970) that has been the               is that locally optimal will be good enough.
long-reigning champion for this problem. Annealing                  To illustratethese concepts, let us consider the graph
almost always outperformed local optimization, and               partitioningproblem that is to be the topic of Section




                        This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                         All use subject to JSTOR Terms and Conditions
                                                                      GraphPartitioningby SimulatedAnnealing / 867

 1.   Get an initialsolution S.
                                                                       Simulated annealing is an approach that attempts
 2.   While there is an untested neighbor of S do the                to avoid entrapment in poor local optima by allowing
      following.                                                     an occasional uphill move. This is done under the
      2.1 Let S' be an untested neighbor of S.                       influence of a random number generatorand a control
      2.2 If cost (S') < cost (S), set S = S'.                       parametercalled the temperature.As typically imple-
 3.   Return S.
                                                                     mented, the simulated annealing approach involves a
                                                                     pair of nested loops and two additional parameters,a
              Figure 1. Local optimization.
                                                                     cooling ratio r, 0 < r < 1, and an integer temperature
                                                                     length L (see Figure 3). In Step 3 of the algorithm,the
3. In this problem, we are given a graph G = (V, E),                 term frozen refers to a state in which no further
where V is a set of vertices(with I V I even) and E is a             improvement in cost(S) seems likely.
set of pairs of vertices or edges. The solutions are                   The heart of this procedure is the loop at Step 3.1.
partitions of V into equal sized sets. The cost of a                 Note that e-A/T will be a number in the interval (0, 1)
partition is its cutsize, that is, the number of edges in            when A and T are positive, and rightfully can be
E that have endpoints in both halves of the partition.               interpretedas a probabilitythat depends on A and T.
We will have more to say about this problem in                       The probabilitythat an uphill move of size A\will be
Section 3, but for now it is easy to specify a natural               accepted diminishes as the temperaturedeclines, and,
local optimization algorithm for it. Simply take the                 for a fixed temperature T, small uphill moves have
neighbors of a partition II =I V1U V2I to be all those               higherprobabilitiesof acceptancethan largeones. This
partitions obtainable from II by exchanging one ele-                 particular method of operation is motivated by a
ment of V, with one element of V2.                                   physicalanalogy, best describedin terms of the physics
   For two reasons, graph partitioning is typical of the             of crystal growth. We shall discuss this analogy in the
problems to which one might wish to apply local                      next section.
optimization. First, it is easy to find solutions, perturb
them into other solutions, and evaluate the costs of                 1.3. A Physical Analogy With Reservations
such solutions. Thus, the individual steps of the iter-              To grow a crystal, one starts by heating the raw
ative improvement loop are inexpensive. Second, like                 materials to a molten state. The temperature of this
most interesting combinatorial optimization prob-                    crystal melt is then reduced until the crystal structure
lems, graph partitioning is NP-complete (Garey,                      is frozen in. If the cooling is done very quickly (say,
Johnson and Stockmeyer 1976, Garey and Johnson                       by dropping the external temperatureimmediately to
 1979). Thus, finding an optimal solution is presum-                 absolute zero), bad things happen. In particular,wide-
ably much more difficult than finding some solution,                 spread irregularitiesare locked into the crystal struc-
and one may be willing to settle for a solution that is              ture and the trapped energy level is much higher than
merely good enough.                                                  in a perfectly structuredcrystal. This rapid quenching
   Unfortunately, there is a third way in which graph                process can be viewed as analogous to local optimi-
partitioning is typical: the solutions found by ldcal                zation. The states of the physical system correspond
optimization normally are not good enough. One can                   to the solutions of a combinatorial optimization prob-
be locally optimal with respect to the given neighbor-               lem; the energy of a state correspondsto the cost of a
hood structureand still be unacceptably distant from
the globally optimal solution value. For example, Fig-
ure 2 shows a locally optimal partition with cutsize 4
for a graph that has an optimal cutsize of 0. It is clear
that this small example can be generalizedto arbitrar-
ily bad ones.
1.2. Simulated Annealing
It is within this context that the simulated annealing
approach was developed by Kirkpatrick, Gelatt and
Vecchi. The difficulty with local optimization is that
it has no way to back out of unattractivelocal optima.               Figure 2. Bad but locally optimal partition with
We never move to a new solution unless the direction                           respect to pairwise interchange. (The dark
is downhill, that is, to a better value of the cost                            and light vertices form the two halves of the
function.                                                                      partition.)




                           This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                            All use subject to JSTOR Terms and Conditions
868 /    JOHNSON ET AL.

 1. Get an initialsolution S.
                                                                       The simulated annealing approach was first devel-
 2. Get an initialtemperature T > 0.                                oped by physicists, who used it with success on the
 3. While not yet frozen do the following.                          Ising spin glass problem (Kirkpatrick, Gelatt and
    3.1 Perform the following loop L times.                         Vecchi), a combinatorial optimization problem where
         3.1.1 Pick a random neighbor S' of S.                      the solutions actually are states (in an idealized model
         3.1.2 Let A = cost (S')- cost (S).
         3.1.3 If A ? 0 (downhill move),
                                                                    of a physical system), and the cost function is the
                    Set S = S'.                                     amount of (magnetic) energy in a state. In such an
         3.1.4 If A > 0 (uphillmove),                               application, it was natural to associate such physical
                    Set S = S' with probabilitye-1T.                notions as specific heat and phase transitionswith the
    3.2 Set T = rT (reduce temperature).                            simulated annealing process, thus, furtherelaborating
 4. Return S.
                                                                    the analogy with physical annealing. In proposing that
                                                                    the approach be applied to more traditional combi-
            Figure 3. Simulated annealing.
                                                                    natorial optimization problems, Kirkpatrick, Gelatt
                                                                    and Vecchi and other authors (e.g., Bonomi and
solution, and the minimum energy or ground state
                                                                    Lutton 1984, 1986, White 1984) have continued
corresponds to an optimal solution (see Figure 4).
                                                                    to speak of the operation of the algorithm in these
When the external temperature is absolute zero, no
                                                                    physical terms.
state transition can go to a state of higher energy.
                                                                      Many researchers,however, including the authors
Thus, as in local optimization, uphill moves are pro-
                                                                    of the current paper, are skeptical about the relevance
hibited and the consequences may be unfortunate.
                                                                    of the details of the analogy to the actual performance
   When crystals are grown in practice, the danger of
                                                                    of simulated annealing algorithms in practice. As a
bad local optima is avoided because the temperature
                                                                    consequence of our doubts, we have chosen to view
is lowered in a much more gradual way, by a process
                                                                    the parameterized algorithm described in Figure 3
that Kirkpatrick, Gelatt and Vecchi call "careful
                                                                    simply as a procedureto be optimized and tested, free
annealing." In this process, the temperaturedescends
                                                                    from any underlying assumptions about what the
slowly througha series of levels, each held long enough
                                                                    parametersmean. (We have not, however, gone so far
for the crystal melt to reach equilibrium at that tem-
                                                                    as to abandon such standard terms as temperature.)
perature.As long as the temperatureis nonzero, uphill
                                                                    Suggestions for optimizing the performance of simu-
moves remain possible. By keeping the temperature
                                                                    lated annealing that are based on the analogy have
from getting too far ahead of the current equilibrium
                                                                    been tested, but only on an equal footing with other
energy level, we can hope to avoid local optima until
                                                                    promising ideas.
we are relatively close to the ground state.
   Simulated annealing is the algorithmic counterpart
                                                                    1.4. Mathematical Results, With Reservations
to this physical annealing process, using the well
known Metropolis algorithm as its inner loop. The                  In addition to the supportthat the simulated annealing
Metropolis algorithm (Metropolis et al. 1953) was                  approachgains from the physical analogy upon which
developed in the late 1940's for use in Monte Carlo                it is based, there are more rigorous mathematical
simulations of such situations as the behavior of gases            justifications for the approach, as seen, for instance,
in the presence of an external heat bath at a fixed                in Geman and Geman (1984), Anily and Federgruen
temperature (here the energies of the individual gas               (1985), Gelfand and Mitter (1985), Gidas (1985),
molecules are presumed to jump randomly from level                 Lundy and Mees (1986) and Mitra, Romeo and
to level in line with the computed probabilities).The              Sangiovanni-Vincentelli (1986). These formalize the
name simulated annealing thus refers to the use of                 physical notion of equilibriummathematically as the
this simulation technique in conjunction with an                   equilibrium distributionof a Markov chain, and show
annealing schedule of declining temperatures.                      that there are cooling schedules that yield limiting
                                                                   equilibrium distributions, over the space of all solu-
                                                                   tions, in which, essentially, all the probability is con-
   PHYSICAL SYSTEM           OPTIMIZATIONPROBLEM
                                                                   centrated on the optimal solutions.
     State                       Feasible Solution                    Unfortunately, these mathematical results provide
     Energy                      Cost
     Ground State                Optimal Solution
                                                                   little hope that the limiting distributions can be
     Rapid Quenching             Local Search                      reached quickly. The one paper that has explicitly
     Careful Annealing           Simulated Annealing               estimated such convergence times (Sasaki and Hajek
                                                                    1988) concludes that they are exponential even for a
                 Figure 4. The analogy.                            very simple problem. Thus, these results do not seem




                          This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                           All use subject to JSTOR Terms and Conditions
                                                                  GraphPartitioningby SimulatedAnnealing /           869
to provide much direct practicalguidance for the real-           paper and its companions has been to subject simu-
world situation in which one must stop far short of              lated annealing to rigorous competitive testing in
the limiting distribution, settling for what are hoped           domains where sophisticated alternatives already
to be near-optimal,ratherthan optimal solutions. The             exist, to obtain a more complete view of its robustness
mathematical results do, however, provide intuitive              and strength.
support to the suggestion that slower cooling rates
(and, hence, longer running times) may lead to better
solutions, a suggestion that we shall examine in some            2. FILLINGIN THE DETAILS
detail.
                                                                 The first problem faced by someone preparingto use
                                                                 or test simulated annealing is that the procedure is
1.5. Claims and Questions
                                                                 more an approach than a specific algorithm. Even if
Although simulated annealing has already proved its              we abide by the basic outline sketched in Figure 3, we
economic value in practical domains, such as those               still must make a variety of choices for the values of
mentioned in the Introduction, one may still ask if it           the parameters and the meanings of the undefined
is truly as good a general approach as suggestedby its           terms. The choices fall into two classes:those that are
first proponents. Like local optimization, it is widely          problem-specific and those that are generic to the
applicable,even to problems one does not understand              annealing process (see Figure 5).
very well. Moreover, annealing apparentlyyields bet-                We include the definitions of solution and cost in
ter solutions than local optimization, so more of these          the list of choices even though they are presumably
applications should prove fruitful. However, there are           specified in the optimization problem we are trying to
certain areas of potential difficulties for the approach.        solve. Improved performance often can be obtained
   First is the question of running time. Many                   by modifying these definitions: the graph partitioning
researchershave observed that simulated annealing                problem covered in this paper offers one example, as
needs large amounts of running time to perform well,             does the graph coloring problem that will be covered
and this may push it out of the range of feasible                in Part II. Typically, the solution space is enlarged
approachesfor some applications. Second is the ques-             and penalty terms are added to the cost to make the
tion of adaptability. There are many problems for                nonfeasible solutions less attractive. (In these cases,
which local optimization is an especially poor heuris-           we use the term feasible solution to characterize
tic, and even if one is preparedto devote largeamounts           those solutions that are legal solutions to the original
of running time to simulated annealing, it is not clear          problem.)
that the improvement will be enough to yield good                   Given all these choices, we face a dilemma in eval-
results. Underlying both these potential drawbacksis             uating simulated annealing. Although experimentsare
the fundamental question of competition.                         capable of demonstrating that the approach performs
   Local search is not the only way to approach com-             well, it is impossible for them to prove that it performs
binatorial optimization problems. Indeed, for some               poorly. Defenders of simulated annealing can always
problems it is hopelessly outclassed by a more con-              say that we made the wrong implementation choices.
structivetechnique one might call successive augmen-             In such a case, the best we can hope is that our
tation. In this approach, an initially empty structure           experiments are sufficiently extensive to make the
is successively augmented until it becomes a solution.           existence of good parameterchoices seem unlikely, at
This, in particular, is the way that many of the effi-
ciently solvable optimization problems, such as the
Minimum Spanning Tree Problem and the Assign-
                                                                   PROBLEM-SPECIFIC
ment Problem, are solved. Successive augmentation                   1. Whatis a solution?
is also the design principle for many common heuris-                2. Whatare the neighborsof a solution?
tics that find near-optimal solutions.                              3. Whatis the cost of a solution?
   Furthermore, even when local optimization is the                 4. Howdo we determinean initialsolution?
method of choice, there are often other ways to                    GENERIC
                                                                    1. Howdo we determinean initialtemperature?
improve on it besides simulated annealing, either by                2. Howdo we determinethe coolingratior?
sophisticated backtracking techniques, or simply by                 3. Howdo we determinethe temperaturelengthL?
 running the local optimization algorithm many times                4. Howdo we knowwhen we are frozen?
 from different starting points and taking the best
 solution found.                                                  Figure 5. Choices to be made in implementing sim-
   The intent of the experiments to be reportedin this                      ulated annealing.




                        This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                         All use subject to JSTOR Terms and Conditions
870 /     JOHNSON ET AL.

least in the absence of firm experimentalevidence that               ITERNUM
such choices exist.                                                    The number of annealing runs to be performed with this
   To provide a uniform framework for our experi-                      set of parameters.
ments, we divide our implementations into two parts.                 INITPROB
                                                                       Used in determining an initialtemperature for the current
The first part is a generic simulated annealing pro-
                                                                       set of runs. Based on an abbreviated trialannealing run, a
gram, common to all our implementations. The sec-                      temperature is found at which the fraction of accepted
ond part consists of subroutines called by the generic                 moves is approximately INITPROB,and this is used as the
program which are implemented separately for each                      starting temperature (if the parameter STARTTEMPis set,
problem domain. These subroutines,and the standard                     this is taken as the starting temperature, and the trial run
                                                                       is omitted).
names we have established for them, are summarized
                                                                     TEMPFACTOR
in Figure 6. The subroutines share common data                         This is a descriptive name for the cooling ratio r of
structuresand variablesthat are unseen by the generic                  Figure 3.
part of the implementation. It is easy to adapt our                  SIZEFACTOR
annealing code to new problems, given that only the                    We set the temperature length L to be N*SIZEFACTOR,
                                                                       where N is the expected neighborhood size. We hope to
problem-specificsubroutines need be changed.
                                                                       be able to handle a range of instance sizes with a fixed
   The generic part of our algorithm is heavily para-                  value for SIZEFACTOR;temperature length will remain
meterized, to allow for experiments with a variety of                  proportional to the number of neighbors no matter what
factorsthat relateto the annealing process itself. These               the instance size.
parametersare describedin Figure 7. Because of space                 MINPERCENT
                                                                       This is used in testing whether the annealing run is frozen
limitations, we have not included the complete generic
                                                                       (and hence, should be terminated). A counter is maintained
code, but its functioning is fully determined by the                   that is incremented by one each time a temperature is
information in Figures 3, 6, and 7, with the exception                 completed for which the percentage of accepted moves is
of our method for obtaining a starting temperature,                    MINPERCENT     or less, and is reset to O each time a solution
given a value for INITPROB, which we shall discuss                     is found that is better than the previous champion. If the
                                                                       counter ever reaches 5, we declare the process to be
in Section 3.4.2.
                                                                       frozen.
   Although the generic algorithm served as the basis
for most of our experiments, we also performed lim-
                                                                         Figure 7. Generic parametersand their uses.
ited tests on variantsof the basic scheme. For example,
we investigated the effects of changing the way tem-
peraturesare reduced, of allowing the number of trials              per temperatureto vary from one temperatureto the
                                                                    next, and even of replacingthe e-/T of the basic loop
                                                                    by a different function. The results of these experi-
 READ-INSTANCE()                                                    ments will be reported in Section 6.
   Reads instanceand sets up appropriatedata structures;
   returnsthe expected neighborhoodsize N for a solution
   (to be used in determiningthe initialtemperatureand the          3. GRAPH PARTITIONING
   numberL of trialsper temperature).
 INITIAL-SOLUTION()                                                The graph partitioning problem described in Section
   Constructs an initialsolution S0 and returnscost (SO),          2 has been the subjectof much researchover the years,
   setting the locally-storedvariableS equal to So and the
   locally-storedvariablec* to some trivialupper bound on          because of its applications to circuit design and
   the optimalfeasiblesolutioncost.                                because, in its simplicity, it appeals to researchersas
 PROPOSE-CHANGE()                                                  a test bed for algorithmic ideas. It was proved NP-
   Chooses a randomneighborS' of the currentsolutionS              complete by Garey, Johnson and Stockmeyer (1976),
   and returnsthe differencecost (S') - cost (S), saving S'        but even before that researchers had become con-
   for possible use by the next subroutine.
 CHANGE-SOLUTION()                                                 vinced of its intractability, and hence, concentrated
   Replaces S by S' in local memory,updatingdata struc-            on heuristics, that is, algorithms for finding good but
   tures as appropriate.IfS' is a feasible solutionand cost        not necessarilyoptimal solutions.
   (S') is better than c*, then sets c* = cost (S') and sets         For the last decade and a half, the recognizedbench-
   the locallystored championsolutionS* to S'.
                                                                   mark among heuristics has been the algorithm of
 FINALSOLUTION()
   Modifiesthe currentsolutionS to obtaina feasiblesolution        Kernighan and Lin (1970), commonly called the
   S". (S" = S if S is alreadyfeasible). If cost (S") S c*,        Kernighan-Lin algorithm. This algorithm is a very
   outputsS"; otherwiseoutputsS*.                                  sophisticated improvement on the basic local
                                                                   search procedure described in Section 2.1, involving
       Figure 6. Problem-specific subroutines.                     an iterated backtracking procedure that typically




                          This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                           All use subject to JSTOR Terms and Conditions
                                                                    GraphPartitioningby SimulatedAnnealing /            871
finds significantly better partitions. (For more                   solutions, it penalizes them accordingto the squareof
details, see Section 7.) Moreover, if implemented                  the imbalance. Consequently, at low temperaturesthe
using ideas from Fiduccia and Mattheyses (1982), the               solutions tend to be almost perfectly balanced. This
Kernighan-Lin algorithm runs very quickly in prac-                 penalty function approach is common to implemen-
tice (Dunlop and Kernighan 1985). Thus, it repre-                  tations of simulated annealing, and is often effective,
sents a potent competitor for simulated annealing,                 perhaps because the extra solutions that are allowed
and one that was ignored by Kirkpatrick, Gelatt                    provide new escape routes out of local optima. In the
and Vecchi when they first proposed using simulated                case of graph partitioning, there is an extra benefit.
annealing for graph partitioning. (This omission was               Although this scheme allows more solutions than the
partially rectified in Kirkpatrick (1984), where                   original one, it has smaller neighborhoods (n neigh-
limited experiments with an inefficient implementa-                bors versus n2/4). Our experiments on this and other
tion of Kernighan-Linare reported.)                                problems indicate that, under normal cooling rates
   This section is organized as follows. In 3.1, we                such as r = 0.95, temperaturelengths that are signifi-
discuss the problem-specificdetails of our implemen-               cantly smallerthan the neighborhoodsize tend to give
tation of simulated annealing for graph partitioning               poor results. Thus, a smaller neighborhood size may
and in 3.2 we describe the types of instances on which             well allow a shorterrunning time, a definite advantage
our experiments were performed. In 3.3, we present                 if all other factors are equal.
the results of our comparisons of local optimization,                 Two final problem-specific details are our method
the Kernighan-Lin algorithm, and simulated anneal-                 for choosing an initial solution and our method for
ing. Our annealing implementation generally outper-                turning a nonfeasible final solution into a feasible one.
forms the local optimization scheme on which it is                 Initial solutions are obtained by generatinga random
based, even if relative running times are taken into               partition (for each vertex we flip an unbiased coin to
account. The comparison with Kernighan-Linis more                  determine whether it should go in V1 or V2). If the
problematic, and depends on the type of graph tested.              final solution remains unbalanced, we use a greedy
                                                                   heuristic to put it into balance. The heuristic repeats
3.1. Problem-Specific Details                                      the following operation until the two sets of the par-
Although the neighborhood structurefor graph parti-                tition are the same size: Find a vertex in the largerset
tioning described in Section 2.1 has the advantage of              that can be moved to the opposite set with the least
simplicity, it turns out that better performancecan be             increase in the cutsize, and move it. We output the
obtained through indirection. We shall follow                      best feasible solution found, be it this possibly modi-
Kirkpatrick,Gelatt and Vecchi in adopting the follow-              fied final solution or some earlier feasible solution
ing new definitions of solution, neighbor,and cost.                encountered along the way. This completes the
   Recall that in the graph partitioning problem we                description of our simulated annealing algorithm,
are given a graph G = (V, E) and are asked to find                 modulo the specification of the individual parameters,
that partition V = V1 U V2 of V into equal sized sets              which we shall provide shortly.
that minimizes the number of edges that have end-
points in different sets. For our annealing scheme, a              3.2. The Test Beds
solution will be any partition V = VI U V2 of the                  Our explorations of the algorithm, its parameters,and
vertex set (not just a partition into equal sized sets).           its competitors will take place within two general
Two partitionswill be neighborsif one can be obtained              classes of randomly generated graphs. The first type
from the other by moving a single vertex from one of               of graph is the standard random graph, defined in
its sets to the other (rather than by exchanging two               terms of two parameters, n and p. The parameter n
vertices, as in Section 2.1). To be specific, if (V1, V2)          specifies the number of vertices in the graph; the
is a partition and v E V1, then (VI - uv},V2 U {v})                parameterp, 0 < p < 1, specifies the probability that
and (Vl, V2) are neighbors. The cost of a partition                any given pair of vertices constitutes an edge. (We
(VI, V2)is defined to be                                           make the decision independently for each pair.) Note
                                                                   that the expected averagevertex degree in the random
c(VI, V2)=I    flU, v} E E: u E VI & v E V2} I                     graph Gn, is p(n - 1). We shall usually choose p so
              +a(   VI I -     2 1)2                               that this expectation is small, say less than 20, as most
                                                                   interesting applications involve graphs with a low
where IX I is the number of elements in set X and a                averagedegree, and because such graphsare better for
is a parametercalled the imbalancefactor. Note that                distinguishingthe performance of different heuristics
although this scheme allows infeasible partitions to be            than more dense ones. (For some theoretical results




                         This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                          All use subject to JSTOR Terms and Conditions
872 /    JOHNSON ET AL.

about the expected minimum cutsizes for random                       compared this particular implementation (hereafter
graphs, see Bui 1983.)                                               referred to as Annealing with a capital A) to the
   Our second class of instances is based on a non-                  Kernighan-Linalgorithm (hereafterreferredto as the
standardtype of random graph,one that may be closer                  K-L algorithm), and a local optimization algorithm
to real applications than the standardone, in that the               (referredto as Local Opt) based on the same neigh-
graphsof this new type will have by definition inherent             borhood structure as our annealing algorithm, with
structure and clustering. An additional advantage is                the same rebalancing heuristic used for patching up
that they lend themselves to two-dimensional depic-                 locally optimal solutions that were out-of-balance.
tion, although they tend to be highly nonplanar. They               (Experiments showed that this local optimization
again have two parameters, this time denoted by n                   approach yielded distinctly better average cutsizes
and d. The random geometricgraph U,,d has n vertices                than the one based on the pairwiseinterchangeneigh-
and is generatedas follows. First, pick 2n independent              borhood discussed in Section 2.1, without a substan-
numbers uniformly from the interval (0, 1), and view                tial increase in running time.) All computations were
these as the coordinates of n points in the unit square.            performed on VAX 11-750 computers with floating
These points represent the vertices; we place an edge               point accelerators and 3 or 4 megabytes of main
between two vertices if and only if their (Euclidean)               memory (enough memory so that our programscould
distance is d or less. (See Figure 8 for an example.)               run without delays due to paging), running under the
Note that for points not too close to the boundary the              UNIX operatingsystem (Version 8). (VAX is a trade-
expected averagedegree will be approximately nwrd2.                 mark of the Digital Equipment Corporation; UNIX
   Although neither of these classes is likely to arise in          is a trademarkof AT&T Bell Laboratories.)The pro-
a typical application, they provide the basis for repeat-           grams were written in the C programminglanguage.
able experiments, and, it is hoped, constitute a broad                 The evaluation of our experiments is complicated
enough spectrum to yield insights into the general                  by the fact that we are dealing with randomizedalgo-
performanceof the algorithms.                                       rithms, that is, algorithmsthat do not always yield the
                                                                    same answer on the same input. (Although only the
3.3. Experimental Results                                           simulated annealing algorithm calls its random num-
As a result of the extensive testing reportedin Section             ber generator duringits operation, all the algorithms
5, we settled on the following values for the five                  are implemented to start from an initial random par-
parameters in our annealing implementation: a =                     tition.) Moreover, results can differ substantiallyfrom
0.05, INITPROB = 0.4, TEMPFACTOR = 0.95,                            run to run, making comparisons between algorithms
SIZEFACTOR = 16, and MINPERCENT=                 2. We              less straightforward.
                                                                       Consider Figure 9, in which histograms of the cuts
                                                                    found in 1,000 runs each of Annealing, Local Opt,
                                                                    and K-L are presented. The instance in question was
                                                                    a random graph with n = 500 and p = 0.01. This
                                                                    particulargraph was used as a benchmark in many of
                                                                    our experiments, and we shall referto it as G500in the
                                                                    future. (It has 1,196 edges for an average degree of
                                                                    4.784, slightly less than the expected figure of 4.99.)
                                                                    The histogramsfor Annealing and Local Opt both can
                                                                    be displayed on the same axis because the worst cut
                                                                    found in 1,000 runs of Annealing was substantially
                                                                    better (by a standarddeviation or so) than the bestcut
                                                                    found during 1,000 runs of Local Opt. This disparity
                                                                    more than balances the differences in running time:
                                                                    Even though the average running time for Local Opt
                                                                    was only a second compared to roughly 6 minutesfor
                                                                    Annealing, one could not expect to improve on
                                                                    Annealing simply by spending an equivalent time
                                                                    doing multiple runs of Local Opt, as some critics
                                                                    suggested might be the case. Indeed, the best cut
  Figure 8. A geometric graph with n = 500 and                      found in 3.6 million runs of Local Opt (which took
            n7rd2    10.                                            roughly the same 600 hours as did our 1,000 runs of




                           This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                            All use subject to JSTOR Terms and Conditions
                                                                           GraphPartitioningby SimulatedAnnealing / 873
                                                                          m >> k runs, and then compute the expected best
                                                                          of a random sample of k of these particularm runs,
                                                                          chosen without replacement. (This can be done by
                                                                          arrangingthe m results in order from best to worst
                                                                          and then looping through them, noting that, for
                                                                           1 < j < m - k + 1, the probability that the jth best
  no -
 50-           l\           -      S                    K
                                                                          value in the overall sample is the best in a subsample
  100         22       24              26         28        3      0
                                                                          of size k is k/(m - j + 1) times the probability that
                                                                          none of the earliervalues was the best.) The reliability
      200     220      240             260        280       300   320
                                                                          of such an estimate on the best of k runs, of course,
      SIMULATEDANNEALING                    LOCALOPTIMIZATION             decreases rapidly as k approaches m, and we will
                                                                          usually cite the relevant values of m and k so that
150-                                                                      readerswho wish to assess the confidence intervalsfor
                                                                          our results can do so. We have not done so here as we
                                                                          are not interested in the precise values obtained from
100                                                                       any particular experiment, but rather in trends that
                                                                          show up across groups of related experiments.
                                                                             Table I shows our estimates for the expected best of
 50-
                                                                          k runs of Annealing, k runs of K-L, and 100k runs of
                                                                          K-L for various values of k, based on the 1,000 runs
                                                                          of Annealing charted in Figure 9 plus a sample of
       200    220      240             260        280       300   320      10,000 runs of K-L. Annealing clearly dominates
                KERNIGHAN-LIN                                             K-L if running time is not taken into account, and
                                                                          still wins when running time is taken into account,
Figure 9. Histograms of solution values found for
                                                                          although the margin of victory is much less impressive
          graph G500 during 1,000 runs each of
                                                                          (but note that the margin increases as k increases).
          Annealing, Local Opt.and Kernighan-Lin.
                                                                          The best cut ever found for this graph was one of size
          (The X-axis corresponds to cutsize and the
                                                                          206, seen once in the 1,000 Annealing runs.
          Y-axis to the number of times each cutsize
                                                                             To put these results in perspective, we performed
          was encountered in the sample.)
                                                                          similar, though less extensive, experiments with ran-
                                                                          dom graphsthat were generatedusingdifferentchoices
Annealing) was 232, compared to 225 for the worst                         for n and p. We considered all possible combinations
 of the annealing runs. One can, thus, conclude that                      of a value of n from 124, 250, 500, 1,0001 with a
this simulated annealing implementation is intrinsi-                      value of np (approximately the expected average
cally more powerful than the local optimization heu-                      degree) from {2.5, 5, 10, 20[. We only experimented
ristic on which it is based, even when running time is                    with one graph of each type, and, as noted above, the
taken into account.                                                       overallpatternof resultsis much more significantthan
   Somewhat less conclusive is the relative perform-                      any individual entry. Individual variability among
ance of Annealing and the sophisticated K-L algo-                         graphs generated with the same parameters can be
rithm. Here the histogramswould overlap if they were                      substantial:the graph with n = 500 and p = 0.01 used
placed on the same axis, although the median and                          in these experiments was significantly denser than
other order statistics for Annealing all improve on the
correspondingstatistics for K-L. However, once again,                                                Table I
Annealing is by far the slower of the two algorithms,                      Comparisonof Annealingand Kernighan-Linon
this time by a factor of roughly 100 (K-L had an                                                       G50
average running time of 3.7 seconds on G500).Thus,                                       Anneal           K-L             K-L
ideally we should compare the best of 100 runs of K-                            k      (Best of k)     (Best of k)   (Best of 100k)
L versus one run of Annealing, or the best of 100k                               1       213.32         232.29          214.33
runs versus the best of k.                                                       2       211.66         227.92          213.19
   Fortunately, there is a more efficient way to obtain                          5       210.27         223.30          212.03
                                                                                10       209.53         220.49          211.38
an estimate of the expected best of k runs than simply                          25       208.76         217.51          210.81
to repeatedly perform sets of k runs and compute                                50       208.20         215.75          210.50
the average of the bests. We perform some number                               100       207.59         214.33          210.00




                                This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                                 All use subject to JSTOR Terms and Conditions
874 /    JOHNSON ET AL.

G500,which was generatedusing the same parameters.                                 Table III
It had an average degree of 4.892 versus 4.784 for                  AverageAlgorithmicResults for 16 Random
G500,and the best cut found for it was of size 219                  Graphs(PercentAbove Best Cut EverFound)
versus 206. Thus, one cannot- expect to be able to                                Expected Average Degree
replicate our experiments exactly by independently                              2.5      5.0     10.0   20.0
                                                                       lvi                                     Algorithm
generating graphs using the same parameters. The                        124     87.8    24.1      9.5   5.6    Local Opt
cutsizes found, the extent of the lead of one algorithm                         18.7     6.5      3.1   1.9    K-L
over another, and even their rank order, may vary                                4.2     1.9      0.6   0.2    Annealing
from graph to graph. We expect, however, the same                      250     101.4    26.5     11.0   5.5    Local Opt
general trends to be observable. (For the record, the                           21.9     8.6      4.3   1.9    K-L
                                                                                10.2     1.8      0.8   0.4    Annealing
actual average degrees for the 16 new graphs are:
                                                                       500     102.3     32.9    12.5   5.8    Local Opt
2.403, 5.129, 10.000,20.500 for the 124-vertexgraphs;                           23.4     11.5     4.4   2.4    K-L
2.648, 4.896, 10.264, 19.368 for the 250-vertexgraphs;                          10.0      2.2     0.9   0.5    Annealing
2.500, 4.892, 9.420, 20.480 for the 500-vertex graphs;                1,000    106.8     31.2    12.5   6.3    Local Opt
and 2.544, 4.992, 10.128, 20.214 for the 1,000-vertex                           22.5     10.8     4.8   2.7    K-L
                                                                                 7.4      2.0     0.7   0.4    Annealing
graphs.)
   The results of our experiments are summarized in
Tables II-V. We performed 20 runs of Annealing for
each graph, as well as 2,000 runs each of Local Opt                  A comment about the running times in Table IV is
and K-L. Table II gives the best cuts ever found for              in order. As might be expected, the running times for
each of the 16 graphs,which may or not be the optimal             Kernighan-Linand Local Opt increase if the number
cuts. Table III reports the estimated means for all the           of vertices increases or the density (number of edges)
algorithms, expressed as a percentage above the best              increases. The behavior of Annealing is somewhat
cut found. Note that Annealing is a clear winner in               anomalous, however. For a fixed number of vertices,
these comparisons, which do not take running time                 the running time does not increase monotonically
into account.                                                     with density, but instead goes through an initial de-
   Once again, however, Annealing dominates the                   cline as the average degree increases from 2.5 to 5.
other algorithmsin amount of time required,as shown               This can be explained by a more detailed look at the
in Table IV. The times listed do not include the time             way Annealing spends its time. The amount of time
needed to read in the graph and create the initial data           per temperatureincreases monotonically with density.
structures,as these are the same for all the algorithms,          The number of temperaturereductions needed, how-
independently of the number of runs performed, and                ever, declines as density increases, that is, freezing
were, in any case, much smaller than the time for a               sets in earlier for the denser graphs. The interaction
single run. The times for Annealing also do not                   between these two phenomena accounts for the
include the time used in performing a trial run to                nonmonotonicity in total running time.
determine an initial temperature.This is substantially               Table V gives results better equalized for running
less than that required for a full run; moreover, we              time. Instead of using a single run of Annealing as our
expect that in practice an appropriatestartingtemper-             standard for comparison, we use the procedure that
ature would be known in advance-from experience                   runs Annealing 5 times and takes the best result. As
with similar instances-or could be determined ana-                can be seen, this yields significantlybetter results, and
lyticallyas a simple function of the numbersof vertices           is the recommended way to use annealing in practice,
and edges in the graph, a line of researchwe leave to             assuming enough running time is available. For each
the interested reader.                                            of the other algorithms, the number of runs corre-
                                                                  sponding to 5 Anneals was obtained separately for
                                                                  each graph, based on the running times reported in
                    Table II                                      Table IV. Observethat once again Annealing's advan-
     Best Cuts Found for 16 Random Graphs                         tage is substantiallyreduced when running times are
                      Expected Average Degree                     taken into account. Indeed, it is actually beaten by
       lvi      2.5      5.0        10.0        20.0              Kernighan-Lin on most of the 124- and 250-vertex
        124      13       63         178          449             graphs,on the sparsest500-vertex graph,and by Local
        250      29      114         357          828             Opt on the densest 124-vertexgraph. Annealing does,
        500      52      219         628        1,744             however, appear to be pulling away as the number of
      1,000     102      451       1,367        3,389
                                                                  vertices increases. It is the overall winner for the




                        This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                         All use subject to JSTOR Terms and Conditions
                                                                         GraphPartitioning by Simulated Annealing /              875

                           Table IV                                     with 500 vertices and four with 1,000. For these we
Average Algorithmic Running Times in Seconds                            chose values of d so that the expected degrees nird2E
           for 16 Random Graphs                                         {5, 10, 20, 401. (The actual averagedegreeswere 5.128,
               Expected Average Degree                                  9.420, 18.196, and 35.172 for the 500-vertex graphs
                                                                        and 4.788, 9.392, 18.678, and 36.030 for the 1,000-
   lvi       2.5        5.0       10.0     20.0     Algorithm
                                                                        vertex graphs.) We performed 20 runs of Annealing
    124       0.1        0.2        0.3      0.8    Local Opt
              0.8        1.0        1.4      2.6    K-L                 and 2,000 runs each of Local Opt and K-L on each of
             85.4       82.8       78.1    104.8    Annealing           the 8 graphs.The best cuts ever found for these graphs
    250       0.3        0.4        0.8      1.3    Local Opt           were 4, 26, 178, and 412 for the 500-vertex graphs,
              1.5        2.0        2.9      4.6    K-L                 and 3, 39, 222, and 737 for the 1,000-vertex graphs.
            190.6      163.7      186.8    223.3    Annealing
                                                                        None of these were found by Annealing; all but the 4,
    500       0.6        0.9        1.5      3.2    Local Opt           3, and 39 were found by K-L. The latter three were
              2.8        3.8        5.7     11.4    K-L
            379.8      308.9      341.5    432.9    Annealing           found by a special hybrid algorithm that takes into
   1,000      2.4        3.8       6.9      14.1    Local Opt           account the geometry of these graphs, and will be
              7.0        8.5      14.9      27.5    K-L                 discussed in more detail in Section 6. Table VI sum-
            729.9      661.2     734.5     853.7    Annealing           marizes the average running times of the algorithms.
                                                                        Table VII estimates the expected best cut encountered
densest 250-vertex graph, the three densest 500-vertex                  in 5 runs of Annealing or a time-equivalent number
graphs, all four 1,000-vertex graphs, and for each                      of runs of K-L or Local Opt. Note that for geometric
density its lead increases with graph size. Note, how-
ever, that by choosing to use the best of 5 runs, for                                       Table VI
Annealing as our standardof comparison, ratherthan                        Average Algorithmic Running Times in Seconds
a single run, we have shifted the balance slightly to                                for 8 Geometric Graphs
Annealing's advantage (assuming the results reported                                                 n7rd2
in Table I are typical). Indeed, had we compared the
                                                                              Vi       5        10       20      40      Algorithm
expected cut for a single Annealing run to an equiva-
lent number of K-L runs on the 1,000-vertex,average                           500      1.0      1.6       3.2     7.2    Local Opt
                                                                                       3.4      4.8       7.4    11.1    K-L
degree 2.5 graph, K-L would outperform Annealing                                     293.3    306.3     287.2   209.9    Annealing
rather than lose to it by a small amount as it does                         1,000      2.2      3.7       7.2     18.0   Local Opt
here.                                                                                  7.6     11.9      18.9     28.7   K-L
  Our next series of experiments concerned geometric                                 539.3    563.7     548.7   1038.2   Annealing
graphs. We considered just 8 graphs this time, four

                                                                         graphs.On the sparsestgraphs, none of the algorithms
                     Table V
                                                                         is particularly good, but K-L substantially outper-
   Estimated Performance of Algorithms When
                                                                         forms Annealing.
   Equalized for Running Times (Percent Above
                                                                           Annealing's poorer relative performance here may
              Best Cut Ever Found)a
                                                                         well be traceableto the fact that the topographyof the
                   Expected Average Degree                               solution spaces for geometric graphs differs sharply
     vi       2.5        5.0       10.0    20.0     Algorithm            from that of random graphs. Here local optima may
     124      7.7        1.6       0.1     0.0     Locals                be far away from each other in terms of the length of
              0.0        0.0       0.0     0.0     K-L's                 the shortest chain of neighborsthat must be traversed
              0.0        0.4       0.1     0.2     5 Annealsa
                                                                         in transformingone to the other. Thus, Annealing is
     250     31.0        5.3       2.1     1.4     Locals
                                                                         much more likely to be trapped in bad local optima.
              0.0        0.3       0.2     0.1     K-L's
              1.8        0.6       0.3     0.0     5 Anneals             As evidence for the different nature of the solution
     500     59.6       13.2       4.5     2.5     Locals                spaces for geometricgraphs,consider Figure 10, which
              1.7        2.6       0.8     0.6     K-L's                 shows a histogram of cutsizes found by K-L for a
              5.7        0.8       0.2     0.2     5 Anneals             geometric graph with n = 500, n7rd2= 20. Compared
    1,000    72.4       19.9       7.6     3.7     Locals                to Figure 9, which is typical of the histograms one
              3.7        3.6       1.5     0.9     K-L's
              3.2        0.8       0.2     0.1     5 Anneals             generates for standard random graphs, the histogram
  a The best of 5 runs of Annealing is compared with the best
                                                                         of Figure 10 is distinctly more spiky and less bell
obtainable in the same overall running time by performing                shaped, and has a much larger ratio of best to worst
multiple runs of Local Opt and Kernighan-Lin.                            cut encountered. The corresponding histogram for




                               This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                                All use subject to JSTOR Terms and Conditions
876         /   JOHNSONETAL.

                                  Table VII                                     even be precisely applicable to graph partitioning if
      Estimated Performance of Algorithms When                                  the graphsare substantiallylargeror differentin char-
      Equalized for Running Times (Percent Above                                acter from those we studied. (The main experiments
                  Best Cut Ever Found)                                          were performed on our standard graph G500, with
                                   nird2                                        secondaryruns performedon a small selection of other
                                                                                types of graphs to provide a form of validation.) As
        VI             5         10        20       40       Algorithm
                                                                                there were too many parametersfor us to investigate
        500       647.5         169.6      11.3     0.0      Locals
                  184.5           3.3       0.0     0.0      K-L's              all possible combinations of values, we studied just
                  271.6          70.6      11.3    15.5      5 Anneals          one or two factors at a time, in hope of isolating their
      1,000      3217.2        442.7       82.5     6.4      Locals             effects.
                  908.9         44.4        1.3     0.0      K-L's                 Despite the limited nature of our experiments, they
                 1095.0        137.2       15.7     7.2      5 Anneals
                                                                                may be useful in suggesting what questions to inves-
                                                                                tigate in optimizing other annealing implementations,
Local Opt is slightly more bell shaped, but continues                           and we have used them as a guide in adapting
to be spiky with a large ratio of best to worst cut                             annealing to the three problems covered in Parts II
found. (For lower values of d, the histograms look                              and III.
much more like those for random graphs, but retain
some of their spikiness. For higher values of d, the                            4.1. The Imbalance Factor
solution values begin to be separatedby large gaps.)                            First, let us examine the effect of varying our one
  In Sections 4 and 5, we consider the tradeoffs                                problem-specific parameter, the imbalance factor a.
involved in our annealing implementation, and                                   Figure 11 shows, for each of a set of possible values
examine whether altering the implementation might                               for a, the cutsizes found by 20 runs of our annealing
enable us to obtain better results for annealing than                           algorithm on G500.In these runs, the other annealing
those summarized in Tables V and VII.                                           parameterswere set to the standard values specified
                                                                                in the previous section. The results are representedby
4. OPTIMIZINGTHE PARAMETERSETTINGS                                              box plots (McGill, Tukey and Desarbo 1978), con-
                                                                                structed by the AT&T Bell Laboratories statistical
In this section, we will describe the experiments that                          graphics package S, as were the histograms in the
led us to the standard parameter settings used in the                           preceding section. Each box delimits the middle two
above experiments. In attempting to optimize our                                quartilesof the results (the middle line is the median).
annealing implementation, we faced the same sorts of                            The whiskers above and below the box go to the
questions that any potential annealer must address.                             farthestvalues that are within distance (1.5) * (quartile
We do not claim that our conclusions will be appli-                             length) of the box boundaries. Values beyond the
cable to all annealing implementations; they may not                            whiskersare individually plotted.
                                                                                   Observe that there is a broad safe range of equiva-
120                                                                             lently good values, and our chosen value of a = 0.05
                                                                                falls within that range. Similar results were obtained
100
                                                                                for a denser 500-vertex random graph and a sparser
80-                                                                              1,000-vertex random graph, as well as for several
                                                                                geometric graphs.For all graphs,large values of a lead
60-
                                                                                to comparatively poor results. This provides support
40-                                                                             for our earlier claim that annealing benefits from the
                                                                                availability of out-of-balance partitions as solutions.
20-
                                                                                The main effect of large values of a is to discourage
                                                                                such partitions.As this figure hints, the algorithmalso
      150        200          250      300        350         400        450
                           KERNIGHAN-LIN
                                       on a GeometricGraph
                                                                                performspoorly for small values of a. For such a, the
                                                                                algorithm is likely to stop (i.e., freeze) with a partition
Figure 10. Histogram of solution values found for a                             that is far out-of-balance, and our greedy rebalancing
           geometric graph with n = 500, nxrd2= 20                              heuristic is not at its best in such situations.
           during 2,000 runs of K-L. (The X-axis                                   Unexpectedly, the choice of a also has an effect on
           corresponds to cutsize and the Y-axis to                             the running time of the algorithm. See Figure 12,
           the number of times each cutsize was                                 where running time is plotted as a function of a for
           encountered in the sample.)                                          our runs on graph G500.Note that the averagerunning




                                      This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                                       All use subject to JSTOR Terms and Conditions
                                                                                       GraphPartitioning by Simulated Annealing /              877
       300
                                                                                      time among such candidates. No candidate yielded a
                                                                                      simultaneous minimum for all the graphs, but our
       280
                                                                                      value of a = 0.05 was a reasonablecompromise.
U      260
T
S
                                                                                      4.2. Parameters for Initializationand Termination
 Z
 E
       240                                                                            As we have seen, the choice of a has an indirect effect
                   T
                                                                                      on the annealing schedule. It is mainly, however, the
       220                                        T           T    T
                                                                                      generic parametersof our annealing implementation
                                                                                      that affect the ranges of temperaturesconsidered, the
       200       .0016   .0031   .0063   .0125   .025   .05   .1   .2   .4   .8
                                                                                      rate at which the temperatureis lowered, and the time
                                           IMBALANCE FACTOR
                                                                                      spent at each temperature.Let us first concentrate on
Figure 11. Effect of imbalance factor a on cutsize                                    the range of temperatures,and do so by taking a more
           found for G5oo.                                                            detailed look at the operation of the algorithm for an
                                                                                      expanded temperaturerange.
                                                                                        Figure 13 presents a time exposure of an annealing
time first increases, then decreasesas a increases. The                               run on our standardrandom graph G500.The standard
same behavior occurs for the other graphs we tested,
although the point at which the running time attains
its maximum varies. This appears to be a complex                                             700

phenomenon, and severalfactors seem to be involved.
First, lower values of a should make escaping from
local optima easier, and hence, quicker. On the other                                    U   500
                                                                                         T
hand, an interaction between a and our freezing
                                                                                         Z
criterion may prolong the cooling process. As a                                          E
                                                                                             400

decreases,so does the cost of the cheapest uphill move,
                                                                                             300
that is, a move that increases the imbalance from 0 to
2 but does not change the number of edges in the cut.                                        200   tI                                    I

Since moves of this type are presumably always avail-                                              0            500            1000     1500
                                                                                                                 (NUMBER OF TRIALS)/N
able, lowering their cost may lower the temperature
needed for the solution to become frozen, given that                                  Figure 13. The evolution of the solution value during
we don't consider ourselves frozen until fewer than                                                     annealing on G500. (Time increases, and
2% of the moves are accepted. This effect is, in turn,                                                  hence, temperature decreases along the
partially balanced by the fact that the initial temper-                                                 X-axis. The Y-axis measures the current
ature-chosen to be such that 40% of the moves are                                                       solution value, that is, the number of edges
accepted-also declines with a.                                                                          in the cut plus the imbalance penalty.)
   In choosing a standard value for a, we restricted
attention to those values that lay in the safe ranges for
all the graphstested with respectto cutsizes found and                                parameters were used with the exception of INIT-
attempted to find a value that minimized running                                      PROB, which was increased to 0.90, and MINPER-
                                                                                      CENT, which was dropped to 1%. During the run,
                                                                                      the solution value was sampled each N = 500 trials
      900
                                                                                      (i.e., 16 times per temperature),and these values are
      800
                                                                                      plotted as a function of the time at which they were
C 700                                                                                 encountered(i.e., the number of trials so far, expressed
NT
N
      600    -                                                                        as a multiple of 500). This means that temperature
N
G                                                                                     decreasesfrom left to right. It is clear from this picture
     T500-                                                                            that little progressis made at the end of the schedule
M 400-
E                                                                                     (there is no change at all in the last 100 samples).
      300    -                                                                        Moreover,the value of the time spent at the beginning
      200
                                                                                      of the schedule is also questionable. For the first 200
                 .0016   .0031   .0063   .0125   .025   .05   .1   .2   .4   .8

                                           IMBALANCE FACTOR
                                                                                      or so samples the cutsizes can barely be distinguished
                                                                                      from those of totally random partitions (1,000 ran-
Figure 12. Effect of imbalance factor a on running                                    domly generatedpartitions for this graph had a mean
           time in seconds for G500.                                                  cutsize of about 599 and ranged from 549 to 665).




                                            This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                                             All use subject to JSTOR Terms and Conditions
878 /          JOHNSON ET AL.

   Furthermore,although the curve in Figure 13 begins                               500


to slope downward at about the 200th sample, a view
                                                                                U 400 |
behind the scenes suggests that serious progress does                           T

not begin until much later. Figure 14 depicts a second                          ZE 300           v

annealing run, where instead of reporting the cutsize
for each sample, we report the cutsize obtained when                                200   tItI

                                                                                          0          500           1000     1500
Local Opt is applied to that sample (a much lower                                                    (NUMBER OF TRIALS)/N

figure). Comparing Figure 14 with the histogram for
Local Opt in Figure 9, we note that the values do not                        Figure 15. Comparison of the tail of an annealing run
fall significantly below what might be expected from                                    where INITPROB = 0.4 and MINPER-
random startLocal Opt until about the 700th sample,                                     CENT = 2% with an entire annealing run
and are only beginning to edge their way down when                                      where INITPROB = 0.9 and MINPER-
the acceptance rate drops to 40% (the dotted line at                                    CENT = 1%.
sample 750).
   There still remains the question of whether the time                      differentvalues of INITPROB, from 0.1 to 0.9. Given
spent at high temperaturesmight somehow be laying                            the inherent variability of the algorithm, all values of
necessary, but hidden, groundwork for what follows.                          INITPROB from 0.2 (or 0.3) to 0.9 seem to be roughly
Figure 15 addresses this issue, comparing a much                             equivalent in the quality of cutsize they deliver. Run-
shorter annealing run, using our standard values of                          ning time, however, clearlyincreaseswith INITPROB.
INITPROB = 0.4 and MINPERCENT = 2%, with                                     Similar results were obtained for the other graphs
the tail of the run depicted in Figure 13. (All samples                      mentioned in Section 4.1, and our choice of INIT-
from Figure 13 that represent temperatures higher                            PROB = 0.4 was again based on an attempt to reduce
than the initial temperaturefor the INITPROB = 0.4                           running time as much as possible without sacrificing
run were deleted.) Note the marked similaritybetween                         solution quality. Analogous experiments led to our
the two plots, even to the size of the cuts found (214                       choice of MINPERCENT = 2%.
and 215, respectively, well within the range of varia-
bility for the algorithm).                                                   4.3. TEMPFACTOR and SIZEFACTOR
  All this suggests that the abbreviated schedule im-                        The remaining generic parameters are TEMPFAC-
posed by our standardparameterscan yield results as                          TOR and SIZEFACTOR,which together control how
good as those for the extended schedule, while using                         much time is taken in cooling from a given starting
less than half the running time. More extensive exper-                       temperatureto a given final one. Tables VIII and IX
iments support this view: Figures 16 and 17 present                         illustrate an investigation of these factors for our
box plots of cutsize and running time for a series of                        standardrandom graph G500.(Similarresultsalso were
runs on G500.We performed 20 runs for each of nine                           obtained for geometric graphs.) We fix all parameters
                                                                            except the two in question at their standard settings,
     320                                                                    in addition we fix the starting temperature at 1.3, a
                                       40% Acceptance Rate                  typical value for this graph when INITPROB = 0.4.
                                                                            We then let TEMPFACTORand SIZEFACTORtake
                                                                            on various combinations of values from {0.440 1,
L    280
                                                                            0.6634, 0.8145, 0.9025, 0.9500, 0.9747, 0.9873} and
p
E:   260       **    ***           *     *     a
                                                                             t0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1,024},
D                                                                           respectively. Note that increasing either value to the
C
T    240
                                                                            next largershould be expected to approximatelydou-
                                                                            ble the running time, all other factors being equal.
z
E    220                                                                    (The increases in TEMPFACTOR amount to replac-
                                                                            ing the current value by its square root, and hence,
     200                    X                                    l          yield schedules in which twice as many temperatures
           0               500                      1000       1500
                                 (NUMBER OF TRIALS)/N
                                                                            are encountered in a given range.) The averages pre-
                                                                            sented in Tables VIII and IX are based on 20 anneal-
Figure 14. The evolution of Local-Opt(S) during                             ing runs for each combination of values.
           annealing on G500,where S is the current                            Table VIII shows the effects of the parameters on
           solution and Local-Opt(S) is the cutsize                         running time. Our running time prediction was only
           obtained by applying Local Opt to S.                             approximately correct. Whereas doubling the time




                                   This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                                    All use subject to JSTOR Terms and Conditions
                                                                                                             GraphPartitioning by Simulated Annealing /                                        879
     230                                                  -
                                                                                                             solutions, although beyond a certain point further
                                                                                                             increases do not seem cost effective. A second obser-
         225     -
                                                                                                             vation is that increasingTEMPFACTORto its square
C
U        220 '
                                                                                                             root appears to have the same effect on quality of
T
                                                                                                             solution as doubling SIZEFACTOR even though it
    1-
         215     -                                                                                           does not add as much to the running time. (The values
                                                                                                             along the diagonals in Table IX remain fairly con-
         210     -
                                                                                                             stant.) Thus, increasing TEMPFACTOR seems to be
         205         0.1   0.2
                                                                                                             the preferred method for improving the annealing
                                  0.3       0.4     0.5             0.6   0.7        0.8   0.9
                                                                                                             results by adding running time to the schedule.
                                                  INITPROB
                                                                                                               To test this hypothesis in more detail, we performed
Figure 16. Effect of INITPROB on cutsize found for                                                           300 runs of Annealing on G500with SIZEFACTOR=
           G500.                                                                                             1 and TEMPFACTOR = 0.99678 (approximately
                                                                                                             0.95 1/16). The average running time was 10% better
spent per temperature seems to double the running                                                            than for our standard parameters, and the average
time, it appears that halving the cooling rate only                                                          cutsize was 213.8, only slightly worse than the 213.3
multiplies it by a factor of roughly 1.85. Thus, the                                                         average for the standard parameters. It is not clear
(TEMPFACTOR,SIZEFACTOR)pair (0.6634, 128),                                                                   whether this slight degradation is of great statistical
which spends 8 times longer per temperature than                                                             significance, but there is a plausible reason why the
(0.95, 16) but makes only one temperature drop for                                                           cutsize might be worse:Once the acceptancerate drops
every 8 made by the latter, ends up taking almost                                                            below MINPERCENT, our stopping criterion will
twice as long to freeze. Two factorsseem to be working
here. Compare Figure 18, which provides a time
                                                                                                                  800
exposure of an annealing run with the pair (0.6634,
128), with the left half of Figure 14, which does the                                                             700 -
                                                                                                             R
same thing for (0.95, 16). First, we observe that our                                                        NU 600     -
                                                                                                             N
stopping criterion, which requires 5 consecutive tem-
                                                                                                             N 500      -_
peratureswithout an improvement, causes the frozen                                                           G
                                                                                                             T 400      -
tail of the time exposure to be much longer in the                                                            I                                                  1       :   -

(0.6634, 128) case. Second, although this appears to                                                         E 300      -                                a

be a more minor effect, the onset of freezing seems to                                                            200
have been delayed somewhat, perhapsbecause so little
                                                                                                                  100                                                                              __
                                                                                                                             0.1       0.2   0.3       0.4      0.5  0.6         0.7   0.8   0.9
progressis made while the temperatureis fixed.                                                                                                               INITPROB
  Table IX shows the average cut found for each
combination of the parameters. Unsurprisingly, in-                                                           Figure 17. Effect of INITPROB on running time in
creasing the running time tends to yield better                                                                         seconds for G500.


                                                        Table VIII
                           Dependenceof Running Time on SIZEFACTORand TEMPFACTORfor G500
                                                   (Numberof Trials/N)
                                                              -                                          TEMPFACTOR
                                   SIZE
                                 FACTOR               0.4401                0.6634           0.8145          0.9025           0.9500          0.9747             0.9873
                                        0.25                                     _                                                               _                  37
                                        0.5                                      -                       -                         -              78                45
                                        I                                                          --                             49               86              164
                                     2                        -                  -                              53                97             178               323
                                     4                        ---                                   65         109               190             332               662
                                     8                                             88              130         209               361             682             1,317
                                    16                  130                       174              261         411               734           1,336             2,602
                                    32                  208                       336              490         820             1,459           2,854
                                    64                  416                       691              992       1,600             2,874                                 -
                                   128                1,024                     1,331            1,971       3,264
                                   256                2,048                     2,688            3,994                                             -
                                   512                4,096                     5,427
                                 1,024                8,192                      -




                                            This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                                             All use subject to JSTOR Terms and Conditions
880 /       JOHNSON ET AL.
  450
                                                                             tation time between the number of runs and time per
                                                                             run? In simplest terms, suppose that we are currently
                                                                             taking the best of k runs. Could we get better results
                                                                            by performing2k runs with the parametersset so that
                                                                            each run takes half as long, or should we perhaps
                                                                            perform k/2 runs, each taking twice as long?
                                                                                There does not appear to be a simple answer. The
        _
  250
                                                                             choice may vary, depending on the total time avail-
                                                                             able. For small time limits, it appearsthat it is best to
  200
        0    200    400    600    800     1000   1200     1400    1600       spend all the time on a single run. Consider our
                          (NUMBER OF TRIALS)/N
                                                                             standard random graph G500.Experiments indicate
Figure 18. Evolution of cutsize when TEMPFAC-                                that if we allow annealing 3 seconds (say setting
           TOR = 0.6634 and SIZEFACTOR= 128.                                 SIZEFACTOR = 1 and TEMPFACTOR = 0.05),
                                                                            the best we can hope for is that Annealing approxi-
                                                                             mate Local Opt in the quality of solution found. Thus,
terminate a run if there are roughly 5 VI SIZE-                              if we only have 6 minutes available, the histogramsof
FACTOR consecutive trials without an improvement,                           Figure 9 indicate that it is better to spend that time
and the smallerSIZEFACTORis, the higherthe prob-                            on a single 6-minute annealing run rather than on
ability that this might occur prematurely. For this                          120 runs of 3 seconds each. Suppose, however, that
paper, we have chosen to stick with our standard                            we have 12 minutes or 24 hours. Does a point of
parameter values, rather than risk solution degrada-                        diminishing returns ever set in, or is it always better
tion for only a small improvement in running time.                          to spend all the time in one run?
In practice, however, one might prefer to gamble on                             For a partial answer, see Table X, which summa-
the speedup. In Section 6 we shall discuss how such                         rizes an experiment performedon the geometric graph
speedups (in conjunction with others) might effect the                      of Figure 8. Fixing SIZEFACTORat 1 and the starting
basic comparisons of Section 4.                                             temperature at a typical value corresponding to
                                                                            INITPROB = 0.4, we ran a sequence of annealing
4.4. A Final TimelQuality Tradeoff                                          runs for various values of TEMPFACTOR (1,024
The final generic parameter to be investigated is                           for TEMPFACTOR = 0.95, 512 for 0.9747, 256
ITERNUM, the number of iterationsto be performed.                           for 0.9873, 128 for 0.99358, 64 for 0.99678, 32 for
In previous sections, we saw that we could improve                          0.99839, and 16 for 0.99920, where each value of
on the results of a single run of annealing by perform-                     TEMPFACTOR is approximately the square root of
ing multiple runs and taking the best solution found.                       its predecessor). Normalizing the running times so
The results just reported indicate that we can also                         that the TEMPFACTOR = 0.99920 runs averaged
obtain improved cuts by allowing an individual run                           100 units, we compared the quality of solutions ex-
to take more time. The question naturallyarises:what                        pected for each value of TEMPFACTOR under var-
is the best way to allocate a given amount of compu-                        ious time bounds, assuming that as many runs as

                                                   Table IX
                   Dependence of Average Cutsize Found on SIZEFACTOR and TEMPFACTOR
                                                                          TEMPFACTOR
                       SIZE
                     FACTOR          0.4401      0.6634          0.8145     0.9025     0.9500    0.9747     0.9873
                          0.25                                                                              234.8
                          0.5                                                 -                   222.1     230.9
                          1                                                            235.0      225.2     221.4
                          2                                                  230.1     224.9      220.1     217.2
                          4                                      232.4       225.1     220.3      216.0     214.1
                          8                       229.9          223.8       218.7     215.2      214.2     212.4
                         16          228.1        223.3          219.6       215.0     213.6      210.8     209.7
                         32          229.5        220.8          215.3       214.7     211.9      211.0
                         64          219.6        217.0          212.9       211.0     211.4
                        128          216.1        213.4          212.3       211.9                 -
                        256          216.2        212.0          211.3
                        512          215.2        212.6
                      1,024          210.6                        -




                            This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                             All use subject to JSTOR Terms and Conditions
                                                                    GraphPartitioning by Simulated Annealing /                                                         881
                     Table X                                       some of the options available to us if we are prepared
 Results of Experiment Comparing the Effect of                     to modify the generic structure,and examine whether
Allowing More Time Per Run Versus Performing                       they offer the possibility of improved performance.
More Runs for the Geometric Graph of Figure 8
    (Cutsize as a Function of Time Available)                      5. 1. Cutoffs
            NORMALIZED             TIME AVAILABLE                  One commonly used speedup option is the cutoff,
  TEMP-      RUNNING                                               included in Kirkpatrick's original implementations.
 FACTOR        TIME           25    50    100   200    400
                                                                   Cutoffs are designed to remove unneeded trials from
  0.99920        100.0                   51.1   42.7   35.5        the beginning of the schedule. On the assumption that
  0.99893         53.0        -   55.8   45.8   37.8   32.1
  0.99678         28.5       64.6 53.2   43.5   36.6   30.8        it is the number of moves accepted (rather than the
  0.99358         15.4       61.5 55.6   46.2   37.0   30.7        number of trials) that is important, the processing at
  0.98730          8.6       64.6 55.3   47.1   40.0   33.7        a given temperature is terminated early if a certain
  0.97470          4.9       70.2 62.1   54.6   47.0   40.1
  0.95000          2.9       71.6 63.8   56.3   49.6   43.5        threshold of accepted moves is passed. To be specific,
                                                                   we proceed at a given temperature until either
                                                                   SIZEFACTOR * N moves have been tried or
possible within the bound were made and the best                   CUTOFF * SIZEFACTOR * N moves have been
result taken. (The actual number of runs used was                  accepted. This approach was orginally proposed in
the integer nearest to (TIME LIMIT)/(RUNNING                       the context of annealing runs that started at high
TIME).) Note that a point of diminishing returnssets               temperatures (INITPROB - 0.9 rather than the
in at around TEMPFACTOR = 0.99678. It is better                    INITPROB = 0.4 of our standard implementation).
to run once at this TEMPFACTOR than a propor-                      It is, thus, natural to compare the effect of using high
tionately increased number of shorter runs at lower                starting temperaturesand cutoffs versus the effect of
TEMPFACTORs, but it is also better to run 2 or 4                   simply startingat a lower temperature.
times at this value than a proportionately decreased                  Figure 19 plots the (running time, cutsize) pairs for
number of longer runs at higher TEMPFACTORs.                       annealing runs made using both approaches. The
   It is interesting to note that, by analogy with                 points marked by *s were obtained from 10 runs
the results displayed in Tables VIII and IX, the                   each with CUTOFF = 1.0 (i.e., no cutoff), and with
(SIZEFACTOR,TEMPFACTOR) pair (1, 0.99678)                          INITPROB E l0.1, 0.2, ..., 0.9} (the same data
should correspond roughly to the (16, 0.95) pair we                used to generate Figures 16 and 17). The points
used in our experiments in the quality of solutions                marked by Os came from 20 runs each with INIT-
found. Similar experiments with SIZEFACTOR= 16                     PROB = 0.95 and CUTOFF E {0.5, 0.25, 0.125,
and TEMPFACTOR = 0.95, 0.9747, and 0.9873 sup-                     0.0625, 0.03 125, 0.015625}.
ported the conclusion that multiple runs for the (16,                 There appearsto be little in the figure to distinguish
0.95) pair were to be preferredover fewer longer runs.             the two approaches.If there is any correlationpresent,
Analogous experiments with our standard random                     it seems to be between running time and cutsize, no
graph G500were less conclusive, however, showing no                matter which method for reducing running time is
statistically significant difference between the three             used. More extensive experimentation might reveal
TEMPFACTORs when running time was taken into                       some subtle distinctions, but tentatively we conclude
account. Thus, the tradeoff between ITERNUM and                    that the two approaches are about equally effective.
TEMPFACTOR appears to be another variable that
can differ from application to application, and possi-                      235   -

bly, from instance to instance.                                         230
                                                                                                                                                0   Varying CUTOFF
                                                                                                                                                    Varying INITPROB
                                                                                          0         a                n                                 0
                                                                            225   -       00         0*
                                                                        c                           00
5. MODIFYINGTHE GENERICALGORITHM                                                                                                          a                0
                                                                    S       220                40         90p0

In choosing the standard values for our parameters,
                                                                        215       -   O            0??                                0aD*                     0
we attempted to select values that yielded the quickest                                                   (080           aaaaa                       oA         Wa
                                                                        210                        00                    a                    0O*              aaa
running time without sacrificing the quality of the                               -


                                                                                          0
                                                                                                                 W               DarW?.
                                                                                                                     aW
solutions found. We were, however, limited in our                       205                    ?
                                                                                                                     *0
                                                                                                                        I
alternativesby the fact that we were operating within                             0                 200
                                                                                                             RUNNING
                                                                                                                       400
                                                                                                                     TIME  IN SECONDS
                                                                                                                                                      600              800

the framework of our generic algorithm, which was
designed for constructing prototype implementations                Figure 19. Comparison of the effects of cutoffs versus
ratherthan a final product. In this section, we consider                      lowering INITPROB.




                         This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                          All use subject to JSTOR Terms and Conditions
882 /    JOHNSON ET AL.

In particular,using INITPROB = 0.95 and CUTOFF                    we temporarily modified our generic algorithm to
= 0.125 is roughly equivalent in running time and                 apportion its time amongst temperaturesadaptively.
quality of solution to our standard choice of INIT-               At each temperaturewe repeat the following loop.
PROB = 0.4 and CUTOFF = 1.0. Reducing CUTOFF
                                                                  1. Run for SIZEFACTOR * N trials, observing the
below 0.125 has the same effect as reducing INIT-
                                                                     best solution seen and the average solution value.
PROB below 0.4: running time is saved but the aver-
                                                                  2. If either of these is better than the corresponding
age solution quality deteriorates.Limited experimen-
                                                                        values for the previous SIZEFACTOR* N trials,
tation also indicated that little was to be gained by
                                                                        repeat.
using cutoffs in conjunction with INITPROB-= 0.4.
                                                                        Otherwise,lower the temperaturein the standard
5.2. Rejection-Free Annealing                                           way.

In the previous section, we investigated the effect of              This adaptive technique approximately tripled the
shortcuts at the beginning of the annealing schedule.            running time for a given set of parameters.Its effect
Alternatively, one might attempt to remove unneces-              on solutions could not, however, be distinguished
sary computations from the end of the schedule. At               from that of tripling the running time by changing
low temperatures almost all our time is spent in                 SIZEFACTORor TEMPFACTOR. See Figure 20 for
considering moves that we end up rejecting. Viewing              a display of solutions found using the adaptivemethod
this as wasted time, Green and Supowit (1986) pro-               (indicated by Os)and the standard method (indicated
pose that we reorganize the computation as follows.              by *s) as a function of running time. SIZEFACTOR
Compute for each possible move the probability pi                was fixed at 16 and each method was run for the range
that it would be accepted if chosen. Let the sum of all          of values of TEMPFACTOR used in Tables VIII and
these probabilities be P. We construct a probability             IX, with the smallest value omitted in the nonadaptive
distribution over the set of all moves where the prob-           case and the largestvalue omitted in the adaptive case.
ability of move i is pi/P, select a move randomly                All other parameterswere set to their standardvalues,
according to this distribution, and accept it automat-           with the starting temperature fixed at 1.3. Ten trials
ically. Green and Supowit show that this is equivalent           were performed for each value.
to doing annealing in the ordinaryway. Moreover, for                Note how solution quality correlates much more
the generalizationof graph partitioningthat they con-            strongly with running time than with method (adap-
sider,the probabilitiescan be updatedefficiently. Con-           tive or nonadaptive). On the basis of these observa-
sequently, the procedure runs more quickly than the              tions and similar ones for geometric graphs, we saw
ordinary method as soon as the percentage of accept-             no need to add the extra complication of adaptive
ances drops below some cutoff (1 1-13% in Green and              annealing schedules to our algorithm. Furtherstudies
Supowit's experiments). Although we did not investi-             of adaptive cooling may, however, be warranted,both
gate this approach ourselves, it appears that for low            for this and other problems. The approach we took,
values of INITPROB, a time savings of up to 30%                  although easy to implement, is rathersimple-minded.
might be obtainable. Note, however, that this ap-                More sophisticated adaptive cooling schedules have
proach may not be generallyapplicable,as the efficient           been proposed recently in which the cooling rate
updatingof the pi's depends in largepart on the nature           is adjusted based on the standard deviation of the
of the cost function used.

5.3. Adaptive Cooling Schedules                                        235


Although much of the time spent by Annealing at                        230230 -
                                                                                                                                            0   ADAPTIVE
very high and very low temperaturesseems unproduc-                    ur225
                                                                                            0
                                                                                                         * o                . .             *
                                                                                                                                                NON-ADAPTIVE
tive, we saw in Section 4.3 that the amount of time                                             0*
                                                                  T
spent at temperaturesbetweenthese limits had a large              S
                                                                  I
                                                                       220      -               0
                                                                                                     00
                                                                                                           0
                                                                  Z                                         00
effect on the quality of solution obtained. The follow-                215      -
                                                                                                T          00          *
                                                                                                             0                    0
ing alternative method for increasing this time was                       210           ~             *~080
                                                                                                                       0
                                                                                                                                  0    00
suggested by Kirkpatrick, Gelatt and Vecchi. Based                        210       -                             o    -          ~~0
                                                                                                                                   0.
                                                                                                                                      0 *             0A
                                                                                                                                                     ob
                                                                                                                                                            0O
                                                                                                                       0
on their reasoning about the physical analogy, they                    205              .            _

proposed spending more time at those temperatures                               0                                500             1000
                                                                                                                       RUNNING TIME IN SECONDS
                                                                                                                                                     1500        2000

where the current average solution value is dropping
rapidly, arguing that more time was needed at such                Figure 20. Results for adaptive and nonadaptive
temperaturesto reach equilibrium.To investigatethis,                         schedules as a function of running time.




                        This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                         All use subject to JSTOR Terms and Conditions
                                                                    GraphPartitioning by Simulated Annealing /                     883

solution values seen at the current temperature.                   A
                                                                   C
                                                                         1.0

Promising initial results for such approaches have                 C
                                                                   E
                                                                   P     -0.8
been reported by Aarts and Van Laarhoven (1984),                   T
                                                                   A
                                                                   N
Lam and Delosme (1986), and Huang, Romeo, and                      C     0.6    -.
                                                                   E                              *
Sangiovanni-Vincentelli(1986).                                      P
                                                                    R*
                                                                   o     0.4    -
5.4. Alternative Cooling Schedules                                 A
                                                                    B*

                                                                   B
                                                                   1     0.2
Returning briefly to Figure 13, we note that some                  L

authors have suggested that the shape of this cooling               Y 0.0
curve,in particularthe points at which its slope under-                         0    20     40           60           80     100    120
                                                                                          Number of Temperature Reductions
goes a major change, may in some way reflect a
process analogous to the phase transitions that H20                Figure 22. Probability that a given uphill move will
undergoes when it is cooled from a gaseous to a solid                         be accepted as a function of the number
state. For these experiments, however, there seems to                         of times the temperaturehas been lowered
be a much better explanation for the shape of the                             under geometric cooling.
curve. First note, as displayed in Figure 21, that there
is a direct correlation between cutsize and the per-
centage of moves currently accepted when the cutsize               A be the size of an uphill move accepted with proba-
is encountered, with cutsize improving essentially lin-            bility INITPROB at temperature To. The ith temper-
early as the probabilityof acceptancegoes down. Since              ature Ti is then chosen so that the probabilitypi that
the percentage of acceptance presumably is deter-                  an uphill move of size A will be accepted equals
mined by the temperature,it is naturalto ask how our               ((C - i)C) * INITPROB. (This is guaranteed by set-
cooling schedule affects the probability of acceptance.            ting Ti = -A/(ln((C - i)C) * INITPROB), or more
Figure 22 displays the probability P(t) that an uphill             precisely the minimum of this figure and 0, since the
move of size 1 will be accepted when the temperature               solution may still be improving at temperature Tloo,
is TO(0.95)t,where To is chosen so that P(1) = 0.99.               in which case, we will need additional temperatures
Note how similar this curve is to that in Figure 13.               to ensure freezing according to our standardcriterion
   A natural question to ask is how important is the               of five temperatureswithout improvement.)
nature of this curve?What about other possible meth-                 This cooling method is intriguing in that it yields
ods of temperature reduction, and the curves they                  time exposures that approximate straight lines (see
inspire? To investigate this question, we considered               Figure 23), furtherconfirming our hypothesis that the
three proposed alternatives.                                       shapes of such time exposure curves are determined
   The first is what we shall call linear probability              by the cooling schedule. Based on limited experi-
cooling. We first fix INITPROB and the number C of                 ments, it appears that this cooling technique is far
temperaturereductions that we wish to consider. Next               more sensitive to its startingtemperaturethan is geo-
we choose a startingtemperature Toat which approx-                 metric cooling. For To = 1.3 (correspondingto INIT-
imately INITPROB of the moves are accepted, letting                PROB = 0.4 for the graph G500),we were unable to
                                                                   distinguish the results for this cooling method from
                                                                   those for the geometric method when the parameters
  700
                                                                   were adjustedto equalize running time. In particular,
  600                                                              for C = 100 and SIZEFACTOR = 8, the running time
                                                                   for linear probabilitycooling was roughly the same as
U 500
T
                                                                   that for geometric cooling under our standardparam-
S                                                                  eters (346 seconds versus 330), while averaging a
Z 400   -
E                                                                  cutsize of 213.5 over 50 runs, compared to 213.3 for
                                                                   the standardparameters.However, if we set To= 1.3
                                                                   (correspondingto INITPROB = 0.9), the average cut
                                                                   increased significantly (to 220.4), even if we doubled
        0      20          40               60       80   100
                      Percentage of Accepted Moves
                                                                   C to take account of the fact that we were starting at
                                                                   a higher temperature. Recall that under geometric
Figure 21. Correlation between cutsize and percent-                cooling, increasing INITPROB above 0.4, although it
           age of acceptance for the annealing run                 led to increasedrunning time, had no significanteffect
           depicted in Figure 13.                                  on cutsizes found.




                         This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                          All use subject to JSTOR Terms and Conditions
884 /         JOHNSON ET AL.

                          LINEAR PROBABILITY COOLING
                                                                           at step i be C/( 1 + log(i)) for come constant C, and if
    700
                                                                           one is willing to wait long enough, then the process
                                                                           will almost surely converge to an optimalsolution.
                                                                           The catch is that waiting long enough may well mean
U   500                                                                    waiting longer than it takes to find an optimal solution
                                                                           by exhaustive search. It is, thus, unlikely that such
Z
E
    400
                                                                           results have anything to tell us about annealing as it
                                                                           can be implemented in practice.
    300
                                                                              Nevertheless, for completeness, we performed lim-
    200   ,                 ,,       1000              1500
                                                                           ited experiments with such logarithmicoolingsched-
          O         500
                             (NUMBER OF TRIALS)/N
                                                                  2000
                                                                           ules, executing logarithmic cooling runs of 1,000,000
                                                                           steps for G500and various values of C. This seems to
Figure 23. Time exposure for linear probability                            give logarithmic cooling the benefit of the doubt,
           cooling.                                                        because a typical geometric cooling run on G500using
                                                                           the standard paramreterstook about 400,000 steps.
   The second cooling method we shall call linear                          Note, however, that under logarithmic cooling the
temperaturecooling, and it has apparently been used                        temperature only drops by about 5% during the last
by some experimenters (e.g., Golden and Skiscim                            half of the schedule; indeed, after the first 0.1% of the
 1986). In this method we choose C and derive a                            schedule it drops only by a factor of 2. Thus, the
starting temperature To from INITPROB as before.                           choice of C seems to be crucial. Too high a value of
The ith temperature Ti is then simply ((C - i)/C) *                        C will cause the annealing run to finish at too high a
 To. Time exposures for this cooling method (see Fig-                      temperaturefor the solution to be frozen in the normal
ure 24) again reflect the curve of acceptance proba-                       sense. Too low a value will result in almost all the
bility values. This technique proved to be equally                         time spent at near-zero temperatures, thus yielding
sensitive to the choice of To. For our standard in-                        results that are little better than Local Opt. For G500,
stance G500,setting C = 100, SIZEFACTOR= 8, and                            the best value of C we could find was one that yielded
 To= 1.3 again yielded an averagecutsize over 50 runs                      a schedule for which the last 80% of the time was
of 213.5 (again using approximatelythe same time as                        spent with an acceptance ratio between 2 and 3%, and
geometric cooling), whereas increasing Toto 11.3 and                       for which the averagecutsize found (over 20 runs) was
C to 200 yielded an average cutsize of 219.9. Because                      219.7, significantlyabove the 213.3 that our standard
of this lack of robustness, it appearsthat neither linear                  method averagedwhile using less than half the time.
probability cooling nor linear temperature cooling is
to be preferredto geometric cooling.                                       5.5. Choosing Moves According to Random
  The final alternative we considered was suggested                             Permutations
by the mathematical proofs of convergence for simu-                       In our description of the basic annealing process in
lated annealing that were discussed in Section 1.4. In                    Figure 3, the neighboring solution S' to be tested is
the papers cited there, it is shown that if one changes                   simply chosen randomly from the set of all neighbors
the temperatureat every step, letting the temperature                     of the currentsolution. In terms of graphpartitioning,
                                                                          we randomly choose a vertex as a candidate for mov-
                      LINEARTEMPERATURE
                                     COOLING                              ing from one side of the partition to the other, inde-
    700
                                                                          pendently of all previous choices. Although this has
                                                                          the appeal of simplicity, there are reasons to think it
                                                                          might be inefficient. Suppose, for instance, that just
                                                                          one of the N vertices in the graphwill yield an accept-
T
S                                                                         able new solution if moved. Then there is a nonnegli-
Z 400
                                                                          gible probability that we may have to perform sub-
                                                                          stantiallymore than N trials before we encounter that
    300
                                                                          special vertex. Thus, it has been suggestedthat, instead
    200 ,                           ,,                        _
                                                                          of picking our moves independently at each iteration,
        0           500            1000                1500       2000
                            (NUMBEROFTRIALS)/N
                                                                          we should introduce enough dependence so that each
                                                                          vertex is chosen once in each successive block of N
Figure 24. Time exposure for linear temperature                           moves. This can be done while still maintaining a
           cooling.                                                       high degree of randomness, simply by choosing a




                                 This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                                  All use subject to JSTOR Terms and Conditions
                                                                   GraphPartitioningby SimulatedAnnealing / 885
random permutation of the vertices at the beginning               graph G500,and so no significant speedup could be
of each block, and using that permutation to generate             expected. Furthermore, for G500 the average cutsize
the next N moves.                                                 found over 100 runs was exactly the same as the
  Using this modification, but otherwise making no                average for random starts. There also seems to be no
changes from the standard parameters and starting                 significantbenefit to using K-L startson the 16 stand-
time, we performed 100 annealing runs on our stand-               ard random graphs covered by Tables II-V, although
ard geometric graph Gsoo.The average running time                 this conclusion is based only on 20 runs with and
was essentially unchanged, but the average cutsize                without the K-L starts for each graph. (We also did
found was 212.5, as compared to 213.3 for 1,000 runs              not attempt to determine optimal values of INIT-
of the standard algorithm. This seems significant                 PROB for each graph separately, but stuck with the
because none of the 10 groups of 100 runs that made               value of 0.4 indicated by our experiments with G500.)
up that 1,000 yielded an averagebetter than 212.9. In                The situation for geometric graphs was somewhat
view of the results summarized in Table IX, the re-               better. Although, once again, the optimal value of
duction in cutsize obtained by using permutations to              INITPROB was around 0.4 and so no speedup could
generate moves seems to be almost as much as one                  be obtained, the use of starting solutions generated
would obtain by doubling the running time and stay-               by K-L yields better solutions on average, as seen in
ing with the standard method. This conclusion was                 Table XI. As shown in the table, however, for these
further supported by experiments with the geometric               geometric graphs there proved to be an even better
graph of Figure 8. Here the average cutsize found                 startingsolution generator,a simple heuristic we shall
during 100 trials dropped from 22.6 for the standard              call the Line Algorithm. This heuristic is tailored
method to 20.4 using permutationgeneration,without                especially to the geometric nature of these instances.
a significant change in running time. If we used per-             Recall that a geometric graph is based on a model in
mutation generation but reduced the value of SIZE-                which vertices correspondto points in the unit square,
FACTOR from 16 to 8, the average cutsize went                     and there is an edge between two vertices if and only
back up to 22.8 but we only used half the time of                 if the vertices are sufficiently close to each other. In
the standard implementation. Based on these limited               terms of this underlying model, one might expect a
experiments, it seems that move generation by                     good partition to divide the unit square into two
permutation is a promising approach.                              regions, and the size of the cut to be roughly propor-
                                                                  tional to the length of the boundary between the two
5.6. Using Better-Than-Random Starting Solutions
Many authors have suggested the possibility of using
better-than-random
                 starting solutions, and lower than                                 Table XI
normal startingtemperatures,to obtain better results,                AverageCutsizesFound for Line, K-L, and
or at least better running times. We studied this                   Annealing(the LatterTwo With and Without
possibility, and our results indicate that the source of           Good StartingSolutionsComparedto Best Cuts
the better-than-random solutions may be of crucial                                 Ever Founda
significance.                                                                               n-xd2
   We first studied the effect on annealing of using                  lvi     5       10        20       40        Algorithm
partitionsgeneratedby K-L, which are far better than                  500     4      26       178       412      (Best Found)
random, as our starting solutions. We revised our
                                                                             38.1    89.4     328.4     627.8    Line
Initial-Solution routine to return the result of K-L                         36.1    89.7     221.0     436.3    K-L
running on a random partition, ratherthan a random                           12.5    45.0     200.8     442.8    Line + K-L
partition itself. (Since K-L works only on bal-                              21.1    65.8     247.0     680.3    Anneal
anced partitions, we actually started from a random                          22.2    52.4     192.4     507.4    K-L + Anneal
                                                                             12.9    48.6     217.0     501.1    Line + Anneal
balanced partition, as we normally did for K-L, rather
than a general random partition, as we normally did                  1000     3      39       222       737      (Best Found)
for annealing.) We then ran experiments analogous to                         47.2   123.7     381.8     1128.7   Line
those in Figures 16 and 17 to find an appropriate,                           70.7   157.5     316.7      857.8   K-L
                                                                             15.7    64.6     272.0      825.5   Line + K-L
presumably lower than normal, value of INITPROB.
                                                                            41.2    120.4     355.3     963.8    Anneal
Surprisingly,it turned out that the boxplots for these                      38.1     99.9     295.0     833.8    K-L + Anneal
good starts looked just like the boxplots for random                        15.8     54.7     262.5     839.6    Line + Anneal
starts in Figures 16 and 17. The best values of INIT-               a These figures do not take running time into account, and
PROB were still 0.3 or 0.4 for our standard random                thus, overestimate the relative efficacy of annealing.




                        This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                         All use subject to JSTOR Terms and Conditions
886 /    JOHNSON ET AL.

regions. Since the shortest such boundary is a straight           where it does not already beat it without accounting
line, this suggests looking at those partitions that are          for running time. (The especially good value for K-L
formed by straightlines.                                          + Annealing on the 500-vertex, nird2 = 20 graph
   The Line Algorithm is given as input the coordi-               appears to be a statistical anomaly, arising from the
nates of the points pi, 1 < i < n, in the model for a             fact that the starting solutions generated by K-L for
geometric graph and proceeds as follows.                          these 20 runs had a much better than normal per-
                                                                  centage of very good cutsizes.)
1. Pick a random angle 0, 0 < 0 S ir.
                                                                     We conclude from these experiments that there is
2. For each point pi, compute the y-intercept yi of the
                                                                  value to be gained by using good starting solutions,
   straightline throughpi with a slope equal to tan(0).
                                                                  but that the nature of the startingsolutions can make
3. Sort the points according to their values of yi, and
                                                                  a crucial difference. It is especially helpful if the start-
   form a partition between the vertices correspond-
                                                                  ing solutions are in some sense orthogonalto the kinds
   ing to the first n/2 points and those corresponding
                                                                  of solutions generatedby annealing, as is the case with
   to the last n/2.
                                                                  the Line solutions for geometric graphs, which make
 Compared to our more sophisticated algorithms, the               use of geometric insights into the nature of the in-
running time for the 0(n log n) Line Algorithm was                stances that are not directly available to a general
negligible, e.g., 1.5 seconds for the 1,000-vertex, ex-           algorithm like annealing that must work for all in-
pected degree 5 graph. (Note that by using a linear-              stances. (One might hypothesize that the reason that
time, median-finding algorithm instead of the sorting             K-L startingsolutions were also helpful for geometric
in Step 3, we could reduce the overall time to 0(n),              graphsis that the detailed operation of K-L is adapted
although for the size of problems we consider here,               to take advantage of the local structure of geometric
the time saving is not worth the programmingeffort.)              graphsin ways that annealing is less likely to find. See
   Table XI shows the averagecuts found for our eight             Section 7 for a brief description of how K-L works.)
standard geometric graphs by 20 runs of Annealing                 Moreover, good starts may be equally or more useful
starting from random partitions, K-L partitions, and              when used with approachesother than annealing.
Line partitions. For comparison purposes, it also                   The above results mirror practical experience we
shows the best cuts ever found by any method and                  had with certain real-life instances. The real-life in-
the averages of 1,000 runs of Line, 2,000 runs of                stances came from a related problem, that of hyper-
K-L, and 1,000 runs of K-L from a Line start. Note               graph partitioning. In a hypergraphthe edges are sets
that Line by itself is as good or better than K-L for            of vertices,not just pairs,and the cutsize for a partition
the sparser graphs, but that the true value of Line               V = V, U V2 is the number of edges that contain
appears to be as an initial partition generator. Even            vertices from both V, and V2.A scheme for designing
more intriguingthan the averagesreportedin the table             "standard-cell VLSI circuits," developed at AT&T
are the cutsizes of the best partitions found by the             Bell Laboratories and described by Dunlop and
various algorithms for the 1,000-vertex graph with               Kernighan, performscell layout by repeatedcalls to a
n-rd2 = 5: The best partition ever found by random               hypergraphpartitioning algorithm. Traditionally the
start K-L has cutsize 26 (compared to 30 for random              K-L algorithmhas been used for this (it was originally
start Annealing), the best Line partition found had              defined in general hypergraphterms). On real circuits,
cutsize 19, and both Line + K-L and Line + Annealing             it gives its best results when started from a partition
found cuts of size 3. Moreover, with Line starts,it was          providedby the circuit designersor a slightly random-
possible to begin Annealing at a very low temperature            ized variant thereof. Such starting partitions were
(INITPROB = 0.025) without losing on solution qual-              significantlybetter than the partitions typically found
ity, and so substantial speedups (as big as a factor of          by K-L when it was started from a purely random
5) were possible. (The combination of Line with K-L              partition. They made use of instance-specific inside
was also slightly faster than K-L by itself, no doubt            information, just as the Line starting partitions
because fewer K-L iterations were needed, given the              did for our geometric instances of ordinary graph
good start.)                                                     partitioning.
   Note that the results in Table XI do not take run-               The same behavior was observed with an imple-
ning time into account. If one equalizes for running             mentation of annealing for hypergraphpartitioning.
time, Line beats Annealing (usually substantially)on             In a victory for our generic approach, this implemen-
all but the 500-vertex graphwith nwrd2 = 20, and beats           tation was obtained from our graph partitioning im-
K-L on all the graphswith nird2 , 10. Moreover, Line             plementation in a few hours by just making some
+ K-L passes Line + Annealing on the two graphs                  minor changes to the problem-specific routines. If




                        This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                         All use subject to JSTOR Terms and Conditions
                                                                   GraphPartitioningby SimulatedAnnealing /                 887
started from a random partition, annealing was not                This better approximation uses the following table
competitive with the designers; starting from their               lookup scheme. First note that the ratio between the
partition, with a low initial temperature, it made                smallest uphill move that has a nonnegligible chance
substantialimprovements. On certain graphs the im-                of rejection and the largest uphill move that has a
provements were more substantial than those made                  nonnegligible chance of acceptance is no more than
by K-L, on others they were less. Overall, the compe-              1,000 or so (an uphill move of size T/200 has an
tition between the two algorithms for this application            acceptance probability0.9950 whereas one of size 5 T
was inconclusive, so long as one did not take running             has an acceptance probability0.0067). Thus, to obtain
time into account.                                                the value of e-I/T to within a half percent or so, all we
   As a final comment on our experiments with good                need do is round 200A/T down to the nearest integer,
starting solutions, we note that they also indicate a             and use that as an index into a table of precomputed
furtherdimension to the superiorityof Annealing over              exponentials (if the index exceeds 1,000, we automat-
K-L when running time is ignored. For the graphG500,              ically reject). Implementing this latter scheme saved
the solutions found by Annealing averaged9% better                 1/3 the running time, and had no apparent effect on
than the initial K-L solutions when INITPROB = 0.4.               quality of solution. We have used it in all our subse-
They were still averaging 1% better than the initial              quent experimentswith Annealing on other problems,
K-L solutions when INITPROB was set to 0.025,                     choosing it over the linear approximation so that we
which reduced the running time of Annealing by a                  could still claim to be analyzing what is essentiallythe
factor of 4. In contrast, when we performed limited               standardannealing approach.
experiments in which K-L was started from the final                   Had we used this approximation in our graph par-
solution found by Annealing, K-L never yielded an                 titioning experiments, it would skew the results
improvement.                                                      slightly more in Annealing's favor, but not enough to
                                                                  upset our main conclusions, even if we combine it
5.7. Approximate Exponentiation                                   with the two other major potential speedups uncov-
In looking for other savings, a natural candidate for             ered in this study. Table XII shows the reduction in
 streamlining is the exponentiation e-/T that takes               running time obtained by: 1) using table lookup ex-
place once each time through the inner loop of the                ponentiation, 2) doing more generation by random
code. On a VAX 11-750, even with a floating point                 permutation while halving the temperature length,
accelerator,this is an expensive operation. Under our             as suggested in Section 6.5, and 3) combining a
standardparameters,Annealing will perform approx-                 further reduction in the temperature length (SIZE-
imately 400,000 such exponentiations in handling                  FACTOR = 1) with a correspondingdecrease in the
G500,and these will take almost one third of the                  cooling rate (TEMPFACTOR = 0.99358 = (0.95)'/8)
running time. It thus seems appealing to use some                 for smoothercooling, as suggestedin Section 5.3. Five
other function than e-A/T to determine the probability            runs of this modified Annealing algorithm were per-
of acceptance. Although there are mathematical mo-                formed for each of the 16 random graphs in our
tivations for using the exponential, they only apply in           ensemble, and Table XII reports the ratios of the
certain asymptotic senses (e.g., see Anily and                    resultingaveragerunning times to the averagesfor our
Federgruen, and Mitra, Romeo and Sangiovanni-                     original implementation, as reportedin Table IV.
Vincentelli). There is no a priori reason why some                    Note that the running time was reduced by a factor
other, simpler to compute function might not serve                of at least two in all cases, with significantly more
just as well or better in the context of the algorithm            improvement as the graphs became sparser and/or
as actually used. One appealing possibility is the func-
tion 1 - A/T, which involves just one division and at
least approximates the exponential. It takes less than                                     Table XII
 V/25as much time to compute on our system, thus                        AverageSpeedupsUsing Approximate
presumably offering about a 33% speedup. On the                      Exponentiation,PermutationGeneration,and
basis of 300 runs with this function and our standard                 SmootherCooling (RunningTime Ratios)
parameters,we can confirm the speedup, and notice                                          Expected Average Degree
no significant difference in the quality of the solution
                                                                          lvi        2.5        5.0      10.0        20.0
(an averagecutsize of 213.2 versus 213.3 for e-'/T).                      124       0.29       0.28      0.38        0.40
   We did not investigate this approximation further                      250       0.31       0.36      0.35        0.41
however, as an equivalent speedup can be obtained                         500       0.34       0.39      0.41        0.47
                                                                         1000       0.34       0.37      0.39        0.49
by an alternative and better approximation to e-/T.




                        This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                         All use subject to JSTOR Terms and Conditions
888 /       JOHNSONETAL.

                          Table XIII                                 partitioning problems, researchershaving concluded
  Comparison of K-L and C-K-L With Sped-up                           that the true message in this relative success is not that
 Annealing (Percent Above Best Cut Ever Found)                       annealing is good, but that K-L is a much poorer
                ExpectedAverageDegree                                algorithm than-previouslythought.
              2.5   5.0      10.0      20.0
                                                                       We have done limited tests of two of the most
     IVI                                       Algorithm
                                                                     promising approaches. The first is based on the
      124     0.0   0.0       0.0      0.0     K-L's
              0.0   0.1       0.0      0.0     C-K-L's               Fiduccia-Mattheysesalgorithm, a variant of K-L. The
              0.0   0.4       0.1      0.2     5 Anneals             K-L algorithm operates only on balanced partitions,
      250     0.1   0.9       0.5      0.2     K-L's                 and is based on a repeated operation of finding the
              0.0   0.4       0.6      0.2     C-K-L's               best pair of as-yet-unmoved vertices (one from V1and
              1.8   0.6       0.3      0.0     5 Anneals
                                                                     one from V2) to interchange (best in the sense that
      500     4.0   3.3       1.1      0.7     K-L's
                                                                     they maximize the decrease in the cut, or if this is
              1.9   2.2       1.2      0.8     C-K-L's
              5.7   0.8       0.2      0.2     5 Anneals             impossible, minimize the increase). If this is done for
    1,000     5.2   4.5      1.8       1.0     K-L's                 a total of I V /2 interchanges, one ends up with the
              2.0   3.5      1.6       1.1     C-K-L's               original partition, except that V1and V2are reversed.
              3.2   0.8      0.2       0.1     5 Anneals             One then can take the best of the I VI/2 partitions
                                                                     seen along the way as the starting point for another
                                                                     pass, continuing until a pass yields no improvement.
 smaller. The running time reductions for our eight                  For a fuller description, see Kernighan and Lin.
geometric graphs were similar, with ratios ranging                     Fiduccia and Matheyses (F-M) proposed to speed
from 0.33 to 0.45 in all but one case (the ratio for the             up the process by picking just the best single vertex to
 500-vertexgeometric graphwith nwrd   2= 40 was 0.76).               move at each step. This reduces the number of possi-
These running time savings were obtained with no                    bilities from I V 2 to I V I and, with the proper data
appreciable loss in solution quality: the average cut-              structures (adjacency lists, buckets, etc.) can reduce
sizes were roughly the same for both implementations.               the total worst case running time (per pass) to
These speedups for both types of graphsalterthe time-                0(I Vj + IEI) from what looks like Q(I VI3) for
equalized comparison of Annealing and K-L reported                  K-L. In practice, this speedup is illusory, as K-L
in Tables V and VII, as fewer runs of K-L could be                  runs in time 0(I V I + IE I) per pass in practicewhen
performed in the time it takes to do 5 anneals. The                 implemented with the same proper data structures,
typical change, however, involves only a minor in-                  and the two algorithmshad comparablerunning times
crease in K-L's expected excess over the best cutsize               in our limited tests. Nor were we able to get F-M to
found, and K-L still has a significant lead over An-                outperform K-L in the quality of solutions found.
nealing for all the geometric graphs and for the ran-               F-M was actually slightly worse under the standard
dom 250- and 500-vertex graphswith expected degree                  implementation in which vertices are chosen alter-
2.5. (To see the effect on random graphs, compare                   nately from V1and from V2,to ensure that every other
Table XIII with Table V.) Moreover, if we are willing               partition encountered is in balance. If instead we
to go to such efforts to optimize our annealing imple-              choose to move the best vertex in either V1or V2,and
mentation, we should also consider attempts to                      use the imbalance squared penalty function of our
improve on K-L by more traditional means. We do                     Annealing algorithm, F-M improved to parity with
this in the next section.                                           K-L, but no better. (As remarked in Section 4.3, lo-
                                                                    cal optimization based on this penalty function is
6. MORE ON THE COMPETITORS                                          substantiallybetter than local optimization based on
                                                                    pairwise interchanges: The average of 1,000 runs of
Simulated annealing is not the only challenger to the               the former on G50 was 276 versus 290 for the latter.)
Kernighan-Lingraph partitioningthrone. Alternative                     The second approach has been embodied in algo-
algorithms for graph and hypergraphpartitioning re-                 rithms due to Goldberg and Burstein and to Bui,
cently have been proposed by a variety of researchers,              Leighton, and Heigham, and involves coalescing ver-
including Fiduccia and Mattheyses (1982), Goldberg                  tices to form a smaller graph, and applying K-L to
and Burstein (1983), Bui et al. (1984), Goldberg                    this. Based on our implementation of both algorithms,
and Gardner (1984), Krishnamurthy (1984), Bui,                      the Bui, Leighton, and Heigham algorithm seems to
Leighton-andHeigham (1986), and Frankle and Karp                    be superior and can offer a significant improvement
(1986). Some of this work in fact has been stimulated               over basic K-L. In this algorithm, one first finds a
by the reported success of annealing on certain graph               maximal matching on the vertices of the graph, and




                           This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                            All use subject to JSTOR Terms and Conditions
                                                                  GraphPartitioning by Simulated Annealing /       889

forms a new graphby coalescing the endpoints of each             unless the graph is very sparse;normally there should
edge in the matching (or all but one of them, if the             still be one monster component that contains most of
number of edges in the matching is not divisible by              the vertices, and this was indeed the case for all the
4). The result is a graph with an even number of                 test graphsstudied. We were, however, able to generate
vertices, upon which K-L is performed. The resulting             a 500-vertex geometric graph with this property by
partition is expanded by uncoalescing the matched                taking d = 0.05 (expected average degree slightly less
vertices, and, if necessary, modified by random shifts           than 4). This graph had an optimum cutsize of 0 that
so that it becomes a balanced partition of the original          was found by using a connected components algo-
graph. This is then used as the starting solution for a          rithm with an 0(n2) dynamic programmingalgorithm
run of K-L on the entire graph, the result of which is           for solving the resulting subset sum problem. Neither
the output of the algorithm. We shall refer to this              K-L nor Annealing, however, ever found such a cut,
algorithm as coalesced Kernighan-Linand abbreviate               despite thousands of runs of the former and hundreds
it as C-K-L.                                                     of the latter.
   Despite the two calls to K-L, the running time of
C-K-L is less than twice that of K-L, rangingbetween
                                                                  7. CONCLUSIONS
 1.1 and 1.9 times that for K-L by itself on our test
graphs(the first call to K-L is on a smaller graph, and          In light of the above, simulated annealing seems to be
the second is from a good starting partition). The               a competitive approachto the graphpartitioningprob-
excess over K-L's running time tends to go up as the             lem. For certain types of random graphs,it appearsto
density of the graph increases. Taking this increased            beat such traditional heuristics as Kemighan-Lin, as
running time into account, however, C-K-L outper-                well as more recent improvements thereon, even when
forms basic K-L on all our geometric test graphs and             running time is taken into account. It was substan-
on the sparserof our random ones. It did not outper-             tially outclassed on other types of graphs, however.
form Line + K-L on the geometric graphs, however.                Generalizingfrom the resultswe observed for random
Table XIII is the analog of Table V for our test bed of          and geometric graphs, it appears that if the graph is
random graphs. Both K-L and C-K-L are compared                   particularlysparse or has some local structure,it may
to our original estimate for the best of 5 anneals, with         well be better to spend an equivalent amount of time
the time equalization taking into account the speedups           performing multiple runs of K-L or C-K-L, or using
for Annealing reported in Table XII. The K-L data                heuristics specially tuned to the instances at hand.
are derived from our original suite of 2,000 runs per               In addition to evaluating annealing's performance
graph; data for C-K-L are based on 1,000 runs                    on the graph partitioning problem, our experiments
per graph.                                                       may also provide some preliminary insight into
   Note that C-K-L dominates our sped-up Annealing               how best to adapt our generic annealing algorithm to
implementation on all the graphs with expected av-               other problems. In particular,we offer the following
erage degree 2.5 (except the smallest, where all three           observations.
algorithms are tied). In comparison, K-L loses out on
the 1,000-vertex graph of this type, even when com-              Observation 1. To get the best results, long annealing
pared to the slower Annealing implementation, as in              runs must be allowed.
Table V. Annealing still seems to be pulling away,
however, as the graphsbecome largerand denser.                   Observation 2. Of the various ways to increase the
   Finally, all three algorithms (K-L, C-K-L, and An-            length of an annealing run, adding time to the begin-
nealing) can be beaten badly on special classes of               ning or end of the schedule does not seem to be as
graphs. We have seen the efficacy of the Line Algo-              effective as adding it uniformly throughout the sched-
rithm for geometric graphs. Bui et al. report on an              ule. The latter can be accomplished by increasing
approach based on network flow that almost surely                TEMPFACTOR, increasing SIZEFACTOR,or using
finds the optimal cut in certain regular graphs with             adaptive temperaturereduction. It is not clear which
unique optimal cuts. Neither Annealing nor K-L                   of these methods is to be preferred,although a TEMP-
matches its performance on such graphs. For espe-                FACTOR increase seems to yield a slight running
cially sparsegraphs, another possibility suggestsitself.         time advantagein our implementation.
Such graphs may not be connected, and it is thus
possible that some collection of connected compo-                Observation3. It may not be necessaryto spend much
nents might contain a total of exactly I V 1/2 vertices,         time at very high temperatures(ones where almost all
yielding a perfect cut. Theoretically this is unlikely           moves are accepted). One can reduce the time spent




                        This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                         All use subject to JSTOR Terms and Conditions
890 /    JOHNSON ET AL.

at such temperatures by using cutoffs, or simply by              Observation 10. The best values of the annealing
starting at a lower temperature. It is not clear if it           parameters may depend not only on the problem
makes a difference which technique is used, so long              being solved, but also on the type and size of instance
as the value of the cutoff/starting temperature is               at hand. One must beware of interactionsbetween the
properly chosen. For this, experimentation may be                generic parameters,and between these and any prob-
required.                                                        lem specific parametersthat may exist in the imple-
                                                                 mentation. Given this warning, however, the generic
Observation 4. Simple minded adaptive scheduling                 parametervalues we derived for our graphpartitioning
appears to yield no improvement beyond that to be                implementation seem like a good starting point,
expected due to the increase in overall running time             assuming they result in feasible running times.
it provides. We do not rule out the possibility that
more sophisticated adaptive schedules or schedules               Observation11. In adapting annealing to a particular
hand-tuned to particulartypes of instances might be              problem, it may pay to expand the definition of solu-
more effective, especially if instances exhibit evidence         tion. One can allow violations of some of the basic
of the "phase transitions" alluded to by Kirkpatrick,            constraints of the problem definition, so long as a
Gelatt and Vecchi. No such transitions were evident              penalty for the violation is included in the cost func-
in our graph partitioning instances, however. For                tion. This allows for a smoother solution space in
these, the shape of a time exposure of current solution          which local optima are easier to escape. The smaller
values seems to be determined mostly by the curve of             the penalty, the smoother the space, and surprisingly
declining move probabilities, with no unexplained                small penalties may still be enough to ensure that final
irregularitiesthat an adaptive schedulermight attempt            solutions are legal, or close to it.
to exploit.
                                                                   Although based on the study of a single application
Observation 5. There seems no reason to replace the              of annealing, these observations have been supported
standard geometric cooling method by any of the                  by our subsequent work on other applications. In
nonadaptivealternativeswe have examined (logarith-               particular,they will be used and elaborated on in the
mic cooling, linear temperaturecooling, etc.).                   two companion papers (Johnson et al. 1990a, b),
                                                                 which report on our experiments adapting simulated
Observation6. It appearsthat better solutions can be             annealing to graph coloring, number partitioningand
found subject to a given bound on running time, if               the traveling salesman problem.
one does not simply generate candidate moves one at                As a service to readers who would like to replicate
a time, independently, but instead uses random per-              or improve upon our graph partitioning experiments
mutations to generate sequences of N successive                  and desire a common basis for comparison, we are
moves without repetition.                                        prepared,for a limited time, to make electronic copies
                                                                 available of the graphs used as instances in this study.
Observation7. Even with long runs, there can still be            Interestedreadersshould contact the firstauthor (elec-
a large variation in the quality of solutions found by           tronic mail address:dsj@research.att.com).
differentruns. However, up to a certainpoint, it seems
to be better to perform one long run than to take the
                                                                 ACKNOWLEDGMENT
best of a time-equivalent collection of shorterruns.
                                                                 The authors thank Phil Anderson for providing the
Observation8. There can be an advantageto starting               initial stimulation for this study, Scott Kirkpatrickfor
at a good solution rather than a randomly generated              his help in getting us started,Jon Bentley, Mike Garey,
one (an advantagein quality of solution, runningtime,            MarkGoldberg,Martin Grotschel, Tom Leighton and
or both), but this depends strongly on the nature of             John Tukey for insightful discussions along the way,
the good solution. Starting solutions that take advan-           and the Referees for suggestions that helped improve
tage of some special structurein the instance at hand            the final presentation.
seem to be preferable to those obtained by general
heuristics.
                                                                 REFERENCES
Observation9. Replacing the computation of the ex-               AARTS, E. H. L., AND P. J. M. VAN LAARHOVEN. 1985.
ponential e-/T with a table lookup approximation                      A New Polynomial-TimeCoolingSchedule.In Proc.
seems to be a simple way to speed up the algorithm                    IEEE Int. Conf: on CAD (ICCAD 85), pp. 206-208,
without degradingits performance.                                     SantaClara,Calif.




                        This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                         All use subject to JSTOR Terms and Conditions
                                                                  GraphPartitioningby SimulatedAnnealing /              891
ANILY,S., AND A. FEDERGRUEN.       1985. Simulated An-           GOLDBERG, M. K., AND M. BURSTEIN. 1983. Heuristic
     nealing Methods With General Acceptance Prob-                    Improvement Technique for Bisection of VLSI Net-
     abilities. Preprint. Graduate School of Business,                works. In Proc. IEEE International Conf on Com-
     Columbia University, New York.                                   puter Design, 122-125, Port Chester, N.Y.
BONOMI,E., ANDJ.-L. LUTTON.1984. The N-City Trav-                GOLDBERG, M. K., AND R. D. GARDNER. 1984. Com-
    elling Salesman Problem: Statistical Mechanics and              putational Experiments: Graph Bisecting. Unpub-
    the Metropolis Algorithm. SIAM Review 26,                       lished Manuscript.
     551-568.                                                    GOLDEN, B. L., AND C. C. SKISCIM. 1986. Using Simu-
Bui, T. 1983. On Bisecting Random Graphs. Report                    lated Annealing to Solve Routing and Location
     No. MIT/LCS/TR-287, Laboratory for Computer                    Problems. Naval. Res. Logist. Quart. 33, 261-279.
     Science, Massachusetts Institute of Technology,             GREEN, J. M., AND K. J. SUPOWIT. 1986. Simulated
     Cambridge, Mass.                                               Annealing Without Rejecting Moves. IEEE Trans.
Bui, T., S. CHAUDHURI,T. LEIGHTON       AND M. SIPSER.              Computer-Aided Design CAD-5, 221-228.
     1984. Graph Bisection Algorithms With Good Av-              HINTON, G. E., T. J. SEJNOWSKIAND D. H. ACKLEY.
    erage Case Behavior. In Proceedings 25th Ann.                     1984. Boltzmann Machines: Constraint Satisfaction
    Symp. on Foundationsof ComputerScience, 181-                      Networks That Learn. Report No. CMU-CS-84- 119,
     192. Los Angeles, Calif.                                         Department of Computer Science, Carnegie-Mellon
Bui, T., T. LEIGHTON     AND C. HEIGHAM.1986. Private                 University, Pittsburgh, Pa.
    Communication.                                               HUANG, M. D., F. ROMEO AND A. SANGIOVANNI-
CERNY,V. 1985. A Thermodynamical Approach to the                    VINCENTELLI. 1986. An Efficient General Cooling
    Travelling Salesman Problem: An Efficient Simula-                 Schedule for Simulated Annealing. In Proc. IEEE
    tion Algorithm. J. Optim. TheoryAppL.45, 41-51.                   Int. Conf on CAD (ICCAD 86), 381-384, Santa
COLLINS,  N. E., R. W. EGLESE   ANDB. L. GOLDEN.1988.                 Clara, Calif.
    Simulated Annealing: An Annotated Bibliography.              JEPSEN, D. W., AND C. D. GELATT, JR. 1983. Macro
    Report No. 88-019, College of Business and Man-                 Placement by Monte Carlo Annealing. In Proc. In-
    agement, University of Maryland, College Park, Md.              ternational ConfJ on Computer Design, 495-498,
DUNLOP,A. E., ANDB. W. KERNIGHAN.         1985. A Proce-            Port Chester, N.Y.
    dure for Placement of Standard-Cell VLSI Circuits.           JOHNSON,D. S., C. R. ARAGON, L. A. McGEOCH AND C.
    IEEE Trans. Computer-Aided Design 4, 92-98.                     SCHEVON. 1990a. Optimization by Simulated An-
EL GAMAL,A. A., L. A. HEMACHANDRA,         I. SHPERLING             nealing: An Experimental Evaluation, Part II (Graph
    AND V. K. WEI. 1987. Using Simulated Annealing                  Coloring and Number Partitioning). Opns. Res. (to
    to Design Good Codes. IEEE Trans. Inform. Theory                appear).
    33, 116-123.                                                 JOHNSON, D. S., C. R. ARAGON, L. A. McGEOCH
FIDUCCIA,C. M., AND R. M. MATTHEYSES.           1982. A             AND C. SCHEVON. 1990b. Optimization by Sim-
    Linear-Time Heuristic for Improving Network Par-                ulated Annealing: An Experimental Evaluation,
    titions. In Proc. 19th Design Automation Conference,            Part III (The Traveling Salesman Problem). (In
    pp. 175-18 1, Las Vegas, N.M.                                   Preparation.)
FRANKLE,   J., ANDR. M. KARP. 1986. Circuit Placements           KERNIGHAN, B. W., AND S. LIN. 1970. An Efficient
    and Cost Bounds by Eigenvector Decomposition. In                Heuristic Procedure for Partitioning Graphs. Bell
    Proc. IEEE Int. ConfJ on CAD (ICCAD 86), pp.                    Syst. Tech. J. 49, 291-307.
    414-417, Santa Clara, Calif.                                 KIRKPATRICK,S. 1984. Optimizationby SimulatedAn-
GAREY,M. R., AND D. S. JOHNSON.1979. Computers                        nealing: Quantitative Studies. J. Statis. Phys. 34,
    and Intractability: A Guide to the Theory of NP-                  975-986.
    Completeness. W. H. Freeman, San Francisco.                  KIRKPATRICK,S., C. D. GELATT, JR. AND M. P. VECCHI.
GAREY, M. R., D. S. JOHNSON AND L. STOCKMEYER.                        13 May 1983. Optimization by Simulated Anneal-
    1976. Some Simplified NP-Complete Graph Prob-                     ing. Science 220, 671-680.
    lems. Theor.Comput.Sci. 1, 237-267.                          KRISHNAMURTHY,B. 1984. An ImprovedMin-Cut Al-
GELFAND, S. B., AND S. K. MITTER. 1985. Analysis of                gorithm for Partitioning VLSI Networks. IEEE
    Simulated Annealing for Optimization. In Proc. 24th            Trans. Computers C-33, 438-446.
    Conf on Decision and Control, 779-786, Ft.                  LAM, J., AND J. M. DELOSME.1986. Logic Minimization
   Lauderdale, Fla.                                                Using Simulated Annealing. In Proc. IEEE Int.
GEMAN,S., ANDD. GEMAN.1984. Stochastic Relaxation,                 Conf: on CAD (ICCAD 86), 348-351, Santa Clara,
   Gibbs Distribution, and the Bayesian Restoration of             Calif.
    Images.IEEE Proc. PatternAnalysis and Machine                LUNDY, M., AND A. MEES. 1986. Convergence         of the
    IntelligencePAMI-6, 721-741.                                   Annealing Algorithm. Math. Prog. 34, 111-124.
GIDAS, B. 1985. Non-Stationary Markov Chains and                Math of a Salesman. 1982.Science 3:9, 7-8 (November).
   Convergence of the Annealing Algorithm. J. Statis.            McGILL, R., J. W. TUKEY AND W. A. DESARBO. 1978.
   Phys. 39, 73-131.                                                  Variations on Box Plots. Am. Stat. 32:1, 12-16.




                       This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                        All use subject to JSTOR Terms and Conditions
892 /    JOHNSON ET AL.

METROPOLIS,  W., A. ROSENBLUTH, M. ROSENBLUTH, A.                 SASAKI, G. H., AND B. HAJEK. 1988. The Time Com-
    TELLER AND    E. TELLER. 1953. Equation of State                   plexity of Maximum Matchingby Simulated An-
    Calculations by Fast Computing Machines. J. Chem.                   nealing. J. Assoc. Comput. Mach. 35, 387-403.
    Phys. 21, 1087-1092.                                          Statistical Mechanics Algorithm for Monte Carlo
MITRA,   D.,   F.   ROMEO AND A. SANGIOVANNI-                          Optimization. 1982. Physics Today 35:5, 17-19
    VINCENTELLI.  1986. Convergence and Finite-Time                     (May).
    Behavior of Simulated Annealing. J. Advan. Appl.              VAN LAARHOVEN, P. J. M.,      AND E. H. L. AARTS.
    Prob. 18, 747-771.                                                  1987. Simulated Annealing: Theory and Practice,
NAHAR, S., S. SAHNI AND E. SHRAGOWITZ.  1985. Exper-                 Kluwer Academic Publishers, Dordrecht, The
    iments with Simulated Annealing. In Proceedings                  Netherlands.
    22nd Design Automation Conference, 748-752, Las               VECCHI, M. P., AND S. KIRKPATRICK.1983. Global Wir-
    Vegas, N.M.                                                      ing by Simulated Annealing. IEEE Trans. Com-
ROWEN, C., AND J. L. HENNESSY. 1985. SWAMI: A                          puter-Aided Design CAD-2, 215-222.
   Flexible Logic Implementation System. In Proceed-              WHITE, S. R.      1984. Concepts of Scale in Simulated
    ings 22nd DesignAutomationConference,169-175,                      Annealing. In Proc. International ConfJon Computer
    Las Vegas, N.M.                                                    Design, 646-651, Port Chester,N.Y.




                         This content downloaded from 128.208.219.145 on Thu, 04 Jun 2015 21:20:57 UTC
                                          All use subject to JSTOR Terms and Conditions
