                                                                   How to Simulate Billiards and Similar Systems
arXiv:cond-mat/0503627v2 [cond-mat.mtrl-sci] 28 Jul 2006




                                                                                                Boris D. Lubachevsky
                                                                                                  bdl@bell-labs.com
                                                                                                  Bell Laboratories
                                                                                                600 Mountain Avenue
                                                                                               Murray Hill, New Jersey




                                                                                                       Abstract
                                                                     An N -component continuous-time dynamic system is considered whose components
                                                                 evolve autonomously all the time except for in discrete asynchronous instances of pair-
                                                                 wise interactions. Examples include chaotically colliding billiard balls and combat
                                                                 models. A new efficient serial event-driven algorithm is described for simulating such
                                                                 systems. Rather than maintaining and updating the global state of the system, the al-
                                                                 gorithm tries to examine only essential events, i.e., component interactions. The events
                                                                 are processed in a non-decreasing order of time; new interactions are scheduled on the
                                                                 basis of the examined interactions using preintegrated equations of the evolutions of
                                                                 the components. If the components are distributed uniformly enough in the evolution
                                                                 space, so that this space can be subdivided into small sectors such that only O(1)
                                                                 sectors and O(1) components are in the neighborhood of a sector, then the algorithm
                                                                 spends time O(log N ) for processing an event which is the asymptotical minimum. The
                                                                 algorithm uses a simple strategy for handling data: only two states are maintained for
                                                                 each simulated component. Fast data access in this strategy assures the practical effi-
                                                                 ciency of the algorithm. It works noticeably faster than other algorithms proposed for
                                                                 this model.

                                                                 Key phrases:
                                                                 collision detection, dense packing, molecular dynamics, hard spheres, granular flow

                                                           1. Introduction

                                                                Many continuous time dynamic systems can be accurately approximated by models
                                                           whose components evolve autonomously all the time except for in discrete asynchronous
                                                           instances of pairwise interactions. A typical example is a set of chaotically colliding billiard
                                                           balls. Each ball moves along a straight line until it collides with another ball or an immobile

                                                                                                            1
obstacle. Only pairwise ball collisions are considered, since the probability is zero that more
than two balls are involved in the same collision.
    Such “billiards” or “hard sphere” models have been in use among computational physi-
cists since the pioneering work [1]. Recently these models have attracted the attention of
simulationists [5], [12]. The task of simulation of such a model is reconstruction of the his-
tory of each component. Many models, even as far from billiards as models of combat [11],
are conceptually similar to billiards. The similarity is in the techniques for handling spatial
combinatorics of multitude of asynchronous pairwise interactions. Processing an interaction
(two-ball collision) or an autonomous evolution of a component (moving a billiard ball along
a straight line) depends on the specific model in hand.
    Most of the recent attention has been drawn to the parallelization of such a simulation
[5], [8]. However, it remains not obvious how to write a practically efficient serial algorithm
for the billiard-type simulation. A “naive” serial algorithm advances the global state of the
billiards from collision to collision. The states of all N balls are examined and updated
at times t0 ≤ t1 ≤ t2 ≤ ..., where t0 is the initialization time and ti+1 is the nearest next
collision time seen at time ti . The naive scheme is inefficient for large N because of high
costs it incurs while performing the following actions:
    (a) the same collision is repeatedly scheduled an order of N times until it occurs,
    (b) at a typical cycle, most balls are not participating in collisions; still, they are examined
by the algorithm.
    Aside from costly actions (a) and (b), there exists problem (c) of finding an inexpensive
method of determining the nearest collision for a chosen ball. A straight-forward method is
to compare the chosen ball with N − 1 others. The standard improvement in this method
is the division of the pool table into an order of N sectors. Only balls in the neighboring
sectors have to be checked to determine the immediate collision which reduces the work from
O(N) to O(1) per one collision scheduled.
    A natural idea for improvement in (a) and (b) is to postpone examining and updating
the state of a ball until its collision. Implementing this idea does not appear as easy as it
might seem. As the simulation progresses, a scheduled collision of a given ball may require
rescheduling. The need for such rescheduling and the desire not to loose information about
already planned collisions lead in [1] to a complicated data structure and update scheme
called “time-table” in [3]. Observe that, with all its computing inefficiency, the naive scheme
has an attractively simple double-buffering data structure. The structure consists of only
two copies of the global state vector, the old and the new, so that the new vector is computed
on the basis of the old one and, in turn, becomes the old one during the next cycle.
    We propose a new serial algorithm for the simulations like billiards. The attraction of
this algorithm is that it utilizes a simple and easy to handle double-buffering data structure,
while avoiding costly actions (a) and (b). Problem (c) is handled in our algorithm using
the standard technique of sectoring. In most cases the algorithm examines and processes
only the events whose processing is unavoidable, e.g., ball collisions and boundary cross-
ings. Sometimes, like the naive algorithm, it also processes events whose examining is not
necessary. However, the fraction of such overhead events is less than 15% in most exper-
iments, and does not grow with N, while the speed-up due to simplicity of data handling
is substantial. The proposed algorithm achieves the same theoretical optimal performances

                                                 2
as other published algorithms, i.e., O(log N) instructions per one processed event with sec-
toring and O(N) without. But its practical algorithmic (i.e., computer independent) speed
for the billiard case is at least an order of magnitude higher than that of other algorithms.
We were able to handle thousands balls and millions of collisions on a non-supercomputer
VAX8550 using FORTRAN (using languages better adapted for the computer should result
in additional speed-ups). Figure 9.2 in Section 9 represents results of the experiments for
2000 balls. Using the same program on the same computer, the number could be easily
increased to 104 .
    When writing this algorithm we paid special attention to an often overlooked tradeoff
between the complexity of data organization and the amount of computations the algorithm
is willing to abandon risking to incur them again. For example, to determine the next collision
for a ball A we have to try to collide it with any other ball (within its neighborhood, in the
presence of sectoring) and then choose the collision closest in time, say it is a collision with
ball B. However this collision of A and B may not necessarily be the one which would
take place because the tentative partner B, in its turn, may choose an even better party C,
C 6= A. As a result, later in the computations, A might figure out that the party B1, which
was previously rated second to best, is to be considered the best.
    Rating potential candidates costs computations: the algorithm tries to simulate a poten-
tial collision of ball A with a candidate X in order to rate this X. Should the algorithm
retain the results of these preliminary simulations which correspond to the second, third
etc. to best parties B1, B2,... when the best candidate B is being chosen ? Or is it more
economical to abandon the information obtained during the rating and, if later needed, sim-
ulate these collisions again ? The answer determines the data organization strategy which
crucially affects algorithm efficiency. In the billiard case, a ”pack rat” strategy entailing a
search through dumped items to find the needed one incurs too high a cost. In a general
case, the best tradeoff depends on the relative cost of the basic operations, e.g., the amount
of computing needed for repeated scheduling versus that needed to retrieve the same data.
    Another scale of strategies and the associated tradeoff is that of the “aggressiveness”
of precomputation. In a more aggressive strategy, when the next collision for ball A is
being scheduled, not only the existing states of other balls are taken into account but also
their possible future states which might result from their as yet unprocessed collisions. The
degree of aggressiveness might be measured in how many future collisions the other balls are
being looked ahead. The two scales are not independent: a more aggressive precomputation
requires a more complicated data structure and encourages the choice of a more “pack rat”
data handling strategy.
    In the described two tradeoff scales, the strategy used in the proposed algorithm is close to
the “wasteful” and “lazy” ends of the scales, the opposite of the “pack rat” and “aggressive”
ones. Both the storage of not immediately needed data and precomputation lookahead are
reduced. The candidates for the next collision for a particular ball which are rated below the
winner are abandoned after the winner is chosen. The future collision of a ball is predicted
based only on the existing states of the other balls, not on their future states after possible
future collisions.
    For a reader who is not familiar with simulation terminology, it is worth adding that
the proposed is an event-driven simulation algorithm in which the state of the simulated

                                               3
system is examined by the computer only at the times of the events, e.g., ball collisions. A
computational physicist may be more familiar with the time-driven simulation algorithms.
Such algorithms (see, e.g., [6]) are usually employed in the many-body problems in which
the components, say particles, rather than evolving almost always autonomously, are con-
tinuously interacting by exerting short and/or long range forces. The two computational
approaches are radically different and each has its own difficulties.
    A time-driven algorithm would maintain the snapshot of the states of all the simulated
components at a time t and would advance the time from t to t + ∆t by modifying all
these states. Given the same precision of simulation, ∆t should be rather small for billiards.
As a result, the time-driven algorithm would be tremendously slower than the proposed
event-driven algorithm. Event-driven algorithms are the best (and often the only practical)
choice for models where discrete instantaneous events occur asynchronously. In the proposed
algorithm, if at time t an event involving ball A is processed, only the state of A is examined
and explicitly modified. The states of most other balls need not be known at t and are not
examined by the algorithm. In fact, the global state is explicitly known at no time t, except
t = 0. However, if we wish to know the global state, say, if we wish to know the location of
each ball at a particular time t, then additional computations of “projecting” the motions
of all balls into time point t are required.
    The rest of the paper is organized as follows: In Sections 2 to 6, a definition of the basic
operations, the data organization, the formulation of the algorithm with examples of its
run, and some comments on the practical experience of its implementation are given. These
sections should be sufficient for a reader who wishes to understand and write a simulation
algorithm for a billiard-like system. Sections 7 and 8 introduce, explain, and analyze the
conditions under which this algorithm works correctly. Section 9 presents an application
example for the algorithm: a disk packing problem, Section 10 compares the performance
of this algorithm with other published proposals, and Section 11 discusses variants of the
billiard simulation and other simulation models like billiards including combat models.

2. Basic operations

    Assume that a basic function interaction time is available which, given state1 of com-
ponent 1 at time1 and state2 of component 2 at time2, computes the time of the next
potential interaction while ignoring the presence of other system components:

                    time ← interaction time(state1, time1, state2, time2)                         (1)

where time ≥ max(time1, time2). If interaction time can not find such finite time, e.g.,
when two billiard balls are moving away from each other, we assume that +∞ is returned.
    In the billiard simulation, the state of a ball is the pair of vectors state = (position, velocity).
If the velocities of the balls are constant between the collisions, and all balls are of the same
constant diameter D, then (1) is of the form

                                 time ← max(time1, time2) + t



                                                  4
where
                                    √
                             (−b −       b2 − ac)/a, if b ≤ 0 and b2 − ac ≥ 0
                    t=                                                                        (2)
                             +∞,                     if b > 0 or b2 − ac < 0

and

              a = |velocity2 − velocity1|2 ,


              b = hposition20 − position10, velocity2 − velocity1i,


              c = |position20 − position10|2 − D 2 ,


              position10 = position1 + velocity1(max(time1, time2) − time1),


              position20 = position2 + velocity2(max(time1, time2) − time2),

|v| denotes the length of vector v and hu, vi denotes the dot product of vectors u and v. The
expression for t in (2) is the least real solution t = t− of the equation at2 +2bt+c = 0 which is
derived from |p + vt|2 = D 2 where p = position20 −position10 and v = velocity2 −velocity1.
The meaning of the latter equation and of both its solutions t = t− and t = t+ is obvious from
Figure 2.1. Note that c may equal 0 in which case t = t− = 0 and time = max(time1, time2).
This means that interaction time is applied when one ball is already at the site of the
scheduled collision.
    Two components 1 and 2 with state1 and state2 are said to be interacting, if

                     interaction time(state1, time, state2, time) = time                      (3)

holds for any value of time. For example, billiard balls i and j of diameter D each with
velocities and positions vi , pi and vj , pj , respectively, are interacting (i.e., colliding), if

                               |pj − pi | = D, hvj − vi , pj − pi i ≤ 0                       (4)

    Assume that a basic function jump is available which, given state1 and state2 of in-
teracting components 1 and 2, computes new state1 and new state2 of these components
immediately after the interaction:

                      (new state1, new state2) ← jump(state1, state2)                         (5)

When two billiard balls collide, only their velocities experience jumps, not positions. As-
suming the energy and momentum are conserved, the tangential components of the initial
velocities are not changed, but the normal coordinates are switched as depicted in Figure 2.2.
    A ball bouncing off a boundary of the pool table, in principle, needs not be examined by
the algorithm. It may be considered as an ordinary point on the autonomous interval of the

                                                   5
                                                        y             t = t+




                                            t = t−
                                                             0                    x
          moving ball
                         v
                                                            immobile ball
                                 p
              t = 0




Figure 2.1: The geometrical meaning of the two solutions of equation |p + vt|2 = D 2




                                    v old                    p2      v norm
                                                                       1
                             v tang
                               1      1

                                             v norm
                                               2
            v new
              1
                                                                          v new
                                                                            2
                                      norm
                                 p 1 v1                          v tang
                                                                   2

               v norm                          v old
                                                 2
                 2




       Figure 2.2: Change of velocities of two billiard balls at their collision




                                              6
Figure 2.3: A ball is disappearing at a boundary and reappearing at the opposite side under
periodic boundary conditions

trajectory. For example, given positions (x0, y0) and the velocity vector v of a ball at time
t = 0, we can construct functions X(v, x0, y0, t) and Y (v, x0, y0, t) which would return the
position x = X and y = Y of the ball at time t without explicitly processing intermediate
boundary reflections. The complexity of computations by functions X() and Y () would not
depend on the number of bouncing.
    In most applications, however, such elaboration would be of little practical use, because
the ball would usually collide with another ball after at most one boundary reflection. Be-
sides, an explicit examination of the reflection event might be needed anyway for statistical
purposes and for convenience of data update. Thus we will treat a reflection from an immo-
bile obstacle as a separate event.
    A boundary crossing may be considered under a periodic boundary condition model,
wherein a ball, rather than bouncing off, disappears at a boundary and reappears at the
opposite side (see Figure 2.3). This may be treated as the same type of event as boundary
reflection. If the pool table is divided into sectors, a similar type of event constitutes a ball
moving from one sector to another. Such an event should be examined by the algorithm
in order to update the membership in the sectors. We will treat all such events as one-
component interactions.
    We will assume that basic functions with the same names interaction time and jump
represent one-component interactions
                      time ← interaction time(state1, time1, obstacle)                       (6)

                              new state ← jump(state, obstacle)                              (7)
where obstacle is the identification of a boundary or an immobile obstacle or a demarcation
line. To apply jump in (7), the component, whose state is represented in (7), must be
interacting with obstacle. The condition which defines such one-component interaction is:
                       interaction time(state1, time, obstacle) = time                       (8)

                                               7
holds for any time. This is similar to (3). Capital K will be reserved for the number of
obstacles so that obstacle in (6), (7), and (8) is an integer in the interval from 1 to K. The
one-component versions of functions interaction time and jump will be easily distinguished
by context from their two-component synonyms in (1) and (3).
    We also assume the availability of a basic function advance which, given state0 of a
component at time0 and a value time1 ≥ time0, returns state1 this component would have
at time1 ignoring possible interactions with other components or obstacles on the interval
(time0, time1):
                            state1 ← advance(state0, time0, time1)                           (9)
In a frictionless billiard, (9) is of the form
                      position1 ← position0 + (time1 − time0)velocity0
                                                                                            (10)
                      velocity1 ← velocity0
which simply says that the ball moves with velocity0 along a straight line starting from
position0 at time0.
    Note that in particular cases, specific calculations for interaction time, advance, and
jump may be not as simple as in the billiard case. The assumption that they are basic saves
us from the burden to detail them in the general discussion.

3. Data organization

The basic data unit of the algorithm is called event and has the following format
                                 event = (time, state, partner)                             (11)
where:
    time is the time to which state of a component corresponds. Note that state is the new
state of the component immediately after the event, e.g., if a ball has experienced a collision
at time, the velocity-coordinate of the state is the new velocity vector after the collision;
    partner identifies the other component, if any, involved in the event. If there is no partner
in the event, the program assigns a special “no-value” symbol Λ to the partner coordinate.
    If time = +∞, then the other three coordinates in the event have no value, i.e., state =
type = partner = Λ.
    At any stage of simulation, the algorithm maintains two events for each component: an
old, already processed in the past event and a new, next scheduled event. This information
is stored in array event[1 : N, 1 : 2], where N is the number of components of the simulated
system. Let us agree to understand a reference like time[3, 1] as the time coordinate of
element event[3, 1] of this array.
    Two arrays new[1 : N] and old[1 : N] with elements equal 1 or 2 are maintained. The
value new[i] is the pointer to the new event for component i and the value old[i] is the
pointer to the old event for component i, so that new event for component i is stored at
event[i, new[i]] and old event for component i is stored at event[i, old[i]]. When new[i] is
updated, old[i] is updated immediately after, so that relation new[i] + old[i] = 3 remains
invariant.

                                                 8
4. The algorithm

     In the algorithm pseudocode in Figure 4.1, /” and ”/ mark the beginning and the end
of a comment, the minimum over an empty set of values is assumed +∞, and the following
short-hand notations are used:

         def
     Pij = interaction time(state[i, old[i]], time[i, old[i]], state[j, old[j]], time[j, old[j]]).


where 1 ≤ i, j ≤ N and

                        def
                    Qik = interaction time(state[i, old[i]], time[i, old[i]], k)


where 1 ≤ i ≤ N and 1 ≤ k ≤ K.
    The main cycle in Figure 4.1 essentially consists of two steps:
1) selecting the next component i∗ to process its event (line 2),
2) processing the event (the rest of the cycle).
    Processing of the event comprises scheduling of the next events for the chosen component
and for the other components involved, if any. P and Q are the nearest next interaction
times. There are two main cases in such scheduling depending on the type of the future
event:
    a) when Q < P, scheduling an interaction which involves only the chosen component i∗
(lines 8, 10, and 11);
    b) when Q ≥ P, scheduling an interaction which involves also a second party j∗ (lines 8
and 13 - 17) and may involve a third party m∗ , the previous partner, if any, of j∗ (lines 19
and 20).
    Section 5 further explains this simple algorithmic structure in concrete examples of its
execution. Now we discuss the aspects of the algorithm which are not represented in the
aggregated pseudocode in Figure 4.1, namely, the ways the three minimizations in lines 2,
4, and 5 are implemented. Since these techniques are well-known, their discussion will be
brief.
    Note that for a small number of balls, say N = 10, the best way to minimize is to use the
straight-forward element-by-element testing. Such straight-forward method to find the mini-
mum of time[i, new[i]] for i ranging from 1 to N in line 2 requires O(N) operations per event.
Instead, the algorithm organizes values time[i, new[i]] into an implicit heap structure with
two pointer arrays pht[1 : N] and pth[1 : N] so that time[pht[m], new[pht[m]]] is the value
which is implicitly located at the m-th position of the imaginary heap array and pth is the
inverse map for pht, i.e., pth[pht[m]] = m for all m. In particular, time[pht[1], new[pht[1]]]
corresponds to the heap tree root, i.e., the minimum value. Thus line 2 could be simply
rewritten as


                        i∗ ← pht[1],     current time ← time[i∗ , new[i∗ ]]

                                                  9
The payment for this computationally cheap method of finding the minimum is the need
to update the heap structure, i.e., arrays pht and pth, each time a value of time[i, new[i]]
is changed in other sections of the algorithm. The total cost of finding the minimum next
event time thus runs to as much as O(log N) operations per one event. For a large N, the
cost O(log N) is still much better than the original cost of O(N).
     The main difficulty in the straight-forward method for minimizations in lines 4 and 5 is
the need for computing the N − 1 values Pi∗ j in line 4 and the K values Qi∗ k in line 5. The
opportunity to decrease the O(N + K) complexity burden of these computations depend
on the topology of the evolution space and the uniformity of the component and obstacle
distribution in this space. In the billiard case the space is just the Euclidean plane and
there is an upper bound on the number of balls which can be located in a bounded vicinity
of a given ball. To take a computational advantage of this, the simulation space is divided
into sectors and only the components or obstacles incident to the neighboring sectors are
examined. The sector boundaries naturally become additional “obstacles” in this method
and their processing constitute the method’s overhead. However the practical gain in the
method is high as examples in Section 5 and 9 show. Theoretically, the cost reduces to O(1)
when using this method.
     Among the available grids used for planar sectorization, the grid of equal squares is
the most convenient. (The ratio of the area to the perimeter of a sector is larger for the
hexagonal grid, though.) Specifically in the case of equal balls, we usually choose square
sides larger than the ball diameter, and for each square we maintain the membership linked-
list of balls whose centers project to this square. Processing of a square boundary crossing is
accompanied by the update of the two lists. Only those Pi∗ j are computed and are subject
to minimization in line 4, for which the center of ball j belongs to one of the nine sectors
neighboring the one whose member is i∗ .


5. Simple example

     Two examples of the execution of the algorithm in Figure 4.1 are reproduced in Fig-
ures 5.2 and 5.3. Four-ball billiards are simulated in both examples. The pool table is a
square. Unlike real billiards with hard wall boundaries, periodic boundary conditions are
assumed (these conditions are explained in Section 2, see Figure 2.3). In the example shown
in Figure 5.2, the table is subdivided into 3 × 3 equal square sectors. Figure 5.2 consists
of three frames, a, b, and c. Each frame shows a snapshot of the simulation state at a
particular current time with the identification, position, and velocity vector of each ball at
this time. Since the execution state usually does not contain positions of all the balls at the
same current time, a picture-producing routine (not presented in this discussion) accepts
t = current time as an input and interpolates between the old and the new positions of
the ball as shown in Figure 5.1. Note that while Figure 5.1 shows a “general” case, with
time[i, old[i]] < t < time[i, new[i]], the snapshots in Figure 5.2 and 5.3 have many “degen-
erated” cases, e.g., time[i, old[i]] = t. Also note that for simplicity of the pictures, the times
are rounded off to their integer parts (the computer manipulates them with the machine

                                               10
initially current time ← 0 and for i = 1, 2, ...N : new[i] ← 1, old[i] ← 2, time[i, 1] ← 0,
partner[i, 1] ← Λ, state[i, 1] ← initial state of component i, event[i, 2] ← event[i, 1]
———————————————————————————————————————

   1. while current time < end time do {

   2.     current time ← min1≤i≤N time[i, new[i]] ;
            i∗ ← an index which supplies this minimum (i.e., current time) ;

   3.     new[i∗ ] ← old[i∗ ]; old[i∗ ] ← 3 − new[i∗ ] ;

   4.     P ← minj∈A(i∗ ) Pi∗ j , where A(i∗ ) = {1 ≤ j ≤ N, j 6= i∗ , time[j, new[j]] ≥ Pi∗ j } ;
            if P < +∞ then j∗ ← an index which supplies this minimum (i.e., P) ;

   5.     Q ← mink∈B Qi∗ k , where B = {1 ≤ k ≤ K} ;
           if Q < +∞ then k∗ ← an index which supplies this minimum (i.e., Q) ;

   6.     R ← min{P, Q}; time[i∗ , new[i∗ ]] ← R;

   7.     if R < +∞ then {

   8.       state1 ← advance(state[i∗ , old[i∗ ]], time[i∗ , old[i∗ ]], R ) ;

   9.       if Q < P then {

  10.          state[i∗ , new[i∗ ]] ← jump(state1, k∗ ) ;

  11.         partner[i∗ , new[i∗ ]] ← Λ ;
            } /” end Q < P clause ”/

  12.       else { /” case Q ≥ P ”/

  13.          time[j∗ , new[j∗ ]] ← R ;

  14.          state2 ← advance(state[j∗ , old[j∗ ]], time[j∗ , old[j∗ ]],R) ;

  15.          (state[i∗ , new[i∗ ]], state[j∗ , new[j∗ ]]) ← jump(state1, state2) ;

  16.          m∗ ← partner[j∗ , new[j∗ ]] ;

  17.          partner[i∗ , new[i∗ ]] ← j∗ ; partner[j∗ , new[j∗ ]] ← i∗ ;

  18.          if m∗ 6= Λ and m∗ 6= i∗ then { /” update third party m∗ ”/

  19.            state[m∗ , new[m∗ ]] ←
                     advance(state[m∗ , old[m∗ ]], time[m∗ , old[m∗ ]], time[m∗ , new[m∗ ]]) ;

  20.             partner[m∗ , new[m∗ ]] ← Λ ;
               } /” end update third party ”/
             } /” end Q ≥ P clause ”/
          } /” end R < +∞ clause ”/
        } /” end while loop ”/

                         Figure 4.1: The simulation algorithm
                                                11
precision for representing real numbers).
    Figure 5.2a shows the positions and velocities of the four balls at current time = 0.
These quantities are the initial values. Observe that no two balls overlap. (A method to
define such initial positions is discussed in Section 9. Correct simulation should preserve this
property.) As the initialization statement in Figure 4.1 reads, the balls are initialized at the
same zero time with identical old and new events. Succeeding the test in line 1, Figure 4.1
(assuming end time is sufficiently large), the algorithm is searching for a ball index i∗ which
yields the minimum to time[i, new[i]]. As Figure 5.2a indicates, the algorithm has chosen
ball 1. Observe that in the beginning of simulation, all four new events have the same time
so the other three choices would be also correct. After switching the senses of old and new
event storages for ball 1 in line 3 (here a redundant manipulation), in line 4 the algorithm
tries to select the ball with which ball 1 will collide first. Since time[i, new[i]] = 0 for all
i and all Pij > 0, no j satisfies time[j, new[j]] ≥ Pi∗ j . This means that the set subject to
minimization in line 4 is empty. Hence P= +∞, and no j∗ is selected. In line 5 the algorithm
selects the boundary k∗ which will be reached by ball 1 first. This boundary happens to be
the lower side of the sector to which position[1, old[1]] belongs and the ball reaches it (in the
absence of other balls) at time Q = 58. In line 6, R and time[1, new[1]] are becoming equal
to this time. Tests in line 7 and 9 are succeeding and the rest of cycle 1 is spent on assigning
to the new coordinates their scheduled values in lines 8, 10, and 11. These new values
will be in effect immediately after crossing the specified boundary. Note that if obstacle
is a demarcation boundary between sectors, then jump is defined as an identical function:
                        def
jump(state, obstacle) = state. Then the algorithm takes the snapshot of the situation (and
this snapshot is shown in Figure 5.2a), after which cycle 2 is started. On the snapshot, ball
1 has a scheduled event at time 58, while the other three balls still have scheduled events at
time 0 as indicated.
    Cycles 2, 3, and 4 are spent on scheduling the future events with positive times for
the remaining three balls. Figure 5.2b shows the progress made in this scheduling. While
current time is still at 0 because no event with positive time has been processed yet, balls 2
and 3 have scheduled boundary crossings (case Q < P) and ball 4 has scheduled a collision
at time 25 with ball 1 (case Q ≥ P). When a scheduled collision is indicated on a picture,
not only its time is given but also (in parentheses) the partner index. Thus, (4)25 at the
new position of ball 1 means that (the center of) ball 1 reaches this position at time 25 and
when it does so, it collides with ball 4. (The dashed line which is supposed to indicate the
future motion of ball 4 is overstricken by the arrow indicating the velocity.)
    The algorithm schedules this collision at cycle 3 when balls 1 and 2 have already scheduled
their next events, boundary crossings at times 58 and 124 respectively, but ball 3 has not
been touched by the algorithm yet. This scheduling proceeds as follows. First (line 4), ball
i∗ = 4 finds out that the only P4j which is not larger than time[j, new[j]] is P41 = 25 and
P becomes 25. Then (line 5), it is determined that the nearest boundary crossing occurs at
time Q. The smallest of the two, P and Q, becomes R and also time[4, new[4]] in line 6.
Since R is finite and Q is larger than P, test in line 7 succeeds but test in line 9 fails. As
a result, the sequence of statements in lines 8 and 13 - 17 is executed whereby balls 4 and
1 have scheduled a collision at time 25 and the index m∗ of the third party is remembered.


                                               12
Since there was no partner in the previously scheduled by ball 1 new event, m∗ becomes Λ
and lines 19 and 20 are skipped.
     Time 25 becomes the smallest one in the event-list and the next two cycles, 5 and 6,
are spent on processing two events, event[1, new[1]] and event[4, new[4]], both representing
the collision of balls 1 and 4 at time 25 but from the “viewpoints” of two different balls.
Processing the collision event by ball 1 generates new boundary crossing scheduled for time
94 and processing the collision by ball 4 generates another collision scheduled for time 87 with
ball 2. The latter collision preempts the previously scheduled by ball 2 boundary crossing for
time 124. The result of all these processings is shown in Figure 5.2c. Two velocity vectors
are indicated for each colliding ball in Figure 5.2c: before and after the collision. As seen,
ball 1 has collided not with ball 4 but with its periodic image.
     The sequence of snapshots shown in Figure 5.3 corresponds to the same initial condition
of the balls as in Figure 5.2 but without sectoring. During cycles 1 to 4 two collisions are
scheduled: one of balls 1 and 4 for time 25 and another of balls 2 and 3 for a distant time 388.
However after cycle 5 the more distant collision of balls 2 and 3 is preempted by a collision
of balls 1 and 2 for earlier time 226. As a result, ball 3 is left without a collision; its tentative
collision is turned into a no-partner event which will be convenient to call advancement.
However, at cycle 6 the preemptor, collision of balls 1 and 2 for time 226, is itself preempted
by a collision of balls 2 and 4 scheduled for even earlier time 87. As a result, ball 1 has now
scheduled an advancement event, the one previously believed to be a collision scheduled for
time 226.
     It seems that events develop faster in the experiments without sectoring shown in Fig-
ure 5.3 than in those with sectoring in Figure 5.2. Without sectoring the balls attempt to
schedule their new events with larger horizons, they are more “aggressive.” However, each
cycle here takes more computing time. We have continued both experiments for 105 col-
lisions, each pairwise collision counted twice. Without sectoring, it takes more than three
times longer of the CPU time, than with sectoring.
     This is so because to schedule a collision with sectoring, a ball should check nine neigh-
boring sectors including its own, where it finds at most three other balls. Without sectoring
a ball should check the same three balls, and also their 3 × 8 periodic boundary images.
Functions interaction time are formally different in the two cases. In the case without sec-
tors, time of a next collision with a ball A is in fact given not as (2) but as the minimum
of nine times, one of which represents a collision with A and is given by (2) and the other
eight represent collisions with eight periodic images of A.

6. Comments on the practical execution of the algorithm

     Overlaps. A practically working algorithm for billiard simulation should be resistant
with respect to small overlap of the balls. Figure 5.3 shows “a preemption of a preemptor”
phenomenon when ball 1 has preempted a collision of balls 2 and 3 by scheduling an earlier
collision with ball 2 (Figure 5.3b) only to be later preempted by ball 4 which schedules an
even earlier collision with ball 2 (Figure 5.3c). In the simulations with thousands of balls,
more involved phenomena of this kind occur. Combined with the roundoff, occasionally, they
cause small overlaps of the balls as shown in the following example. Suppose, a scheduled

                                                 13
                                      velocity( 3 ,old( 3 ) )


                                                                position( 3 ,new( 3 ) )
                                                 3
                                                                     217 = time( 3 ,new( 3 ) )
          position( 3 ,old( 3 ) )


       position at time t (the circle center)


       Figure 5.1: Ball 3 at time current time = t (a legend for Figure 5.2 and 5.3)

collision of balls A and B for time tAB is later preempted by scheduling collision of B and C
for time tBC < tAB . As a result, the collision event for A becomes an advancement for time
tAB . Suppose, that later, collision of C and D scheduled for time tCD < tBC preempts the
collision of B and C. As a result, the collision event for B becomes an advancement for time
tBC . Now the originally scheduled collision of A and B for time tAB needs to be scheduled
again. However, it will be done starting with different initial positions. If formula (2) is
used in this scheduling, then c = 0 and t = 0 because max(time1, time2) = tAB . Because
of roundoff errors and different computational paths, c may be “slightly” negative as if balls
A and B would slightly overlap at time tAB and so negative could be t. In the existing
program this problem is handled as follows: whenever interaction time computes a negative
but small by absolute value t in (2), this is not reported as an error, but the value of t is
replaced by zero.
    Advancement events. A preempted two-component interaction is turned into an ad-
vancement for the third party, e.g., the preempted collision for time 388 of balls 2 and 3 in
Figure 5.3a is turned for ball 3 into an advancement in Figure 5.3b. A more aggressive strat-
egy would perform a full-fledged new event scheduling for ball 3. Such strategy is less efficient
partly because advancements are usually far fetched in the future and have a great chance
to be rescheduled so it is not worthwhile to waste precomputations on them. By the time
of event processing only a small fraction of events remain advancements, in most simulated
cases less than 15%. More importantly, the fraction of the processed advancements does not
grow with N. (No theoretical analysis of this statement is available.) Another possibility is
“rolling back” the preempted ball to the old event. This would break the time-orderly event
processing.
    Delayed update. There exists a subtle inefficiency in the algorithm in Figure 4.1.
When scheduling an interaction, the algorithm applies advance and jump operations. If
the event is later preempted, these computations are wasted. For example, when scheduling
a collision of balls 2 and 3 for time 388 (Figure 5.3a), new velocities are computed, using
jump. Later, however, this collision is preempted (Figure 5.3b). To correct this inefficiency,

                                                14
                                                 a) result of cycle 1; current_time = 0; ball 1
                                 2
                             0                      has scheduled a boundary crossing for time 58
          1
                                        4
        58                               0




                         3
                     0




                                                   b) result of cycles 2, 3, and 4; current_time = 0;
                                 2
                                                         ball 2 has scheduled a boundary crossings for
          1                  124
                                        4                time 124; ball 3 has scheduled a boundary crossing
      (4) 25
                                        (1) 25
                                                         for time 150; ball 4 has scheduled a collision
                                                         with ball 1 for time 25



               150
                         3




                             2                      c)    result of cycles 5 and 6; current_time = 25;

          1              (4) 87                            balls 1 and 4 have processed a collision for
4                                         4
               94
                                     (2) 87               time 25; ball 1 has scheduled a boundary
                                                          crossing for time 94; balls 2 and 4 have
                                                           scheduled a collision for time 87


               150
                     3




    Figure 5.2: An example of the algorithm execution. Space is sectorized



                                              15
                                                              a)     result of cycles 1 to 4; current_time = 0;
                              2
                                                                     balls 1 and 4 have scheduled a collision for
      (4) 25 1
                                             4                       time 25; balls 2 and 3 have scheduled
                                             (1) 25
                                        (3) 388                      a collision for time 388
    (2) 388




                          3




                                                             b)     result of cycle 5; current_time = 25;
                              2                                     ball 1 has processed its collision
              1
                                                 4                 with ball 4 for time 25; balls 1 and 2
                                  (1) 226
                                               (1) 25
                   (2) 226                                          have scheduled a collision for

      388                                                          time 226; ball 2 canceled an earlier
                                                                   scheduled collision with ball 3 for
                                                                    later time 388 and this collision is
                      3                                            turned into an advancement for ball 3




                              2                              c)     result of cycle 6; current_time = 25;

              1           (4) 87                                   ball 4 has processed its collision with
                                                  4
                                            (2) 87                 ball 1 at time 25; balls 2 and 4 have
                     226
                                                                    scheduled a collision for time 87 ;
      388
                                                                     ball 2 has canceled an earlier
                                                                   scheduled collision with ball 1 for

                      3                                             later time 226 and this collision is
                                                                   turned into an advancement for ball 1



Figure 5.3: An example of the algorithm execution. Space is not sectorized. The initial
conditions for the balls are the same as in Figure 5.2
                                                        16
the application of advance and jump should be delayed until the latest possible moment
when the scheduled event is being processed. Such optimized pseudocode (which looks less
transparent than the original one) is given in Figure 6.1.

    The encoding of partner is different in the algorithm in Figure 6.1 comparing with that
in Figure 4.1. In the new version,
                       
                        Λ                               for an advancement
  partner[i, new[i]] =   the index of the partner        for a two-component interaction
                         N + the index of the obstacle for a one-component interaction
                       
                                                                                       (12)
assuming the interaction has not been processed yet. After the interaction has been processed
by one participant i∗ but not by the other j# , partner[j# , new[j# ]] becomes negative to
indicate that no state update by the second participant j# is required. This is so done
because processing for ball i∗ has updated both states.
    This code saves not a great deal in the billiard case because here advance and jump are
much lighter computationally than interaction time. The update pattern of array time[1 :
N, 1 : 2] in the algorithm in Figure 6.1 is the same as in the one in Figure 4.1.
    When the third party is the first party ? In both versions of the algorithm, the
third party update is conditioned to m∗ 6= i∗ (lines 18, 19 and 20 in Figure 4.1 and line 23
in Figure 6.1), which requires the third party to be distinct from the first party, the initiator
of the update. The existing program for billiard balls is supposed to report an occurrence of
m∗ = i∗ . In all the runs, this condition has never been reported. Is identity m∗ = i∗ at all
possible ?
    We can imagine a scenario when equality m∗ = i∗ is caused by two components interacting
twice, second interaction immediately after the first one without intermediate involvement
of other components or obstacles. In the billiard case with periodic boundary conditions two
subsequent collisions of the same pair of balls is highly improbable for large N. For small
N, e.g., N = 2, if balls are relatively large, this can occur with a high probability. In other
systems such occurrences may be probable even for large N. That is why in the general
algorithms, the execution is safeguarded with the test m∗ 6= i∗ .

7. Consistency of basic operations

    In the billiards application, the three basic functions of Section 2 are defined in terms
of a consistent model: by integrating differential equations of motion of a system, using
conservation laws, etc. However, the formulation of the algorithm in Section 4 employs no
additional model. Clearly, arbitrarily “bad” basic functions can cause arbitrarily bizarre
behavior even of a “good” algorithm. Thus, if we wish to provide certain assurance that the
algorithm is “correct,” we should request certain “correctness” or consistency properties of
the basic functions. Thus, we introduce the following conditions:

(I) Function interaction time is commutative with respect to the components, i.e., it de-
pends on the unordered pair of components, although in (1) the two participants in the

                                               17
initially current time ← 0 and for i = 1, 2, ...N : new[i] ← 1, old[i] ← 2, time[i, 1] ← 0,
partner[i, 1] ← Λ, state[i, 1] ← initial state of component i, event[i, 2] ← event[i, 1]
——————————————————————————————————————————–
   1. while current time < end time do {
   2.    current time ← min1≤i≤N time[i, new[i]] ;
           i∗ ← an index which supplies this minimum (i.e., current time) ;
   3.    state1 ← advance(state[i∗ , old[i∗ ]], time[i∗ , old[i∗ ]], time[i∗ , new[i∗ ]]) ;
   4.    j# ← partner[i∗ , new[i∗ ]] ;
   5.    if j# = Λ then state[i∗ , new[i∗ ]] ← state1
   6.    else /” case j# 6= Λ ”/
   7.      if j# > 0 then /” state update required ”/
   8.         if j# > N then /” one-component interaction ”/
                 state[i∗ , new[i∗ ]] ← jump(state1, j# − N )
   9.         else { /” 1 ≤ j# ≤ N , two-component interaction ”/
  10.            state2 ← advance(state[j# , old[j# ]], time[j# , old[j# ]], time[j# , new[j# ]]) ;
  11.            (state[i∗ , new[i∗ ]], state[j# , new[j# ]]) ← jump(state1, state2) ;
  12.            partner[j# , new[j# ]] ← −i∗ ; /” negative partner flags no state update for j# ”/
               } ; /” end two-component interaction clause,
               end state update required clause, end j# 6= Λ clause ”/
  13.      new[i∗ ] ← old[i∗ ]; old[i∗ ] ← 3 − new[i∗ ] ;
  14.      P ← minj∈A(i∗ ) Pi∗ j , where A(i∗ ) = {1 ≤ j ≤ N, j 6= i∗ , time[j, new[j]] ≥ Pi∗ j } ;
             if P < +∞ then j∗ ← an index which supplies this minimum (i.e., P) ;
  15.      Q ← mink∈B Qi∗ k , where B = {1 ≤ k ≤ K} ;
            if Q < +∞ then k∗ ← an index which supplies this minimum (i.e., Q) ;
  16.      R ← min{P, Q}; time[i∗ , new[i∗ ]] ← R;
  17.      if R < +∞ then
  18.        if Q < P then partner[i∗ , new[i∗ ]] ← N + k∗
  19.        else { /” case Q ≥ P ”/
  20.           time[j∗ , new[j∗ ]] ← R ;
  21.           m∗ ← partner[j∗ , new[j∗ ]] ;
  22.           partner[i∗ , new[i∗ ]] ← j∗ ; partner[j∗ , new[j∗ ]] ← i∗ ;
  23.          if m∗ 6= Λ and m∗ 6= i∗ then partner[m∗ , new[m∗ ]] ← Λ ;
              } /” end Q ≥ P clause ”/
        } /” end while loop ”/

  Figure 6.1: A version of the simulation algorithm with delayed state update




                                                    18
interaction are represented in a particular order.

(II) Similarly, function jump depends only on the unordered pair of arguments. This
means that assignment (new state2, new state1) ← jump(state2, state1) produces the same
new state1, and new state2 as assignment (5).

(III) Function advance(state0, time1, time2) satisfies a two-parametrical semigroup prop-
erty with respect to its second and third argument, i.e., for any t1 ≤ t2 ≤ t3 we have
advance(advance(s, t1 , t2 ), t2 , t3 ) = advance(s, t1 , t3 ) for any state s.

(IV) Moreover, there is a proper associativity between advance and interaction time, namely,
if t = interaction time(s1 , t1 , .), and t1 ≤ t2 ≤ t, then t = interaction time(advance(s1 , t1 , t2 ), t2 , .),
where dot (.) replaces an appropriate pair (state, time) if we have a two-component interac-
tion or it replaces an obstacle if we have a one-component interaction. For a two-component
interaction time, this property, coupled with (I), implies a similar associativity with respect
to the second set of arguments or with respect to both sets.

(V) The components are never stuck at each other. Namely, if two components 1 and 2
with state1 and state2 are interacting, i.e. (3) holds, jump is applied and new state1 and
new state2 are computed according to (5), then interaction time(new state1, time, new state2, time) >
time. Similarly, if a component with state is interacting with obstacle, i.e. (8) holds, jump is
applied and new state is computed according to (7), then interaction time(new state, time, obstacle) >
time.

    Computationally conditions (I) - (IV) might be “slightly” violated because of the round-
off. This can cause dependence of the simulated history on the processing order. In double-
precision billiard simulations, a few dozen collisions experienced by each ball is usually
sufficient for two differently ordered computations to completely diverge, even when started
with identical initial conditions. After the divergence the ball trajectories and the collisions
that occur in one such run are completely different from the trajectories and collisions that
occur in the other. Computational physicists are aware of such divergence [3] and consider
it a variant of physical irreproducibility. It is worth stating however that the second run
of exactly the same serial program starting with the same input data produces exactly the
same results.
    Now we are going to introduce a condition of a different kind. Consider the set of
components and obstacles I(t) interacting at a particular time t. If I(t) is non-empty, we
may introduce a binary relation among the elements in I(t), assuming element i is in the
relation with element j if i is interacting with j at t. Let ∼ be a reflexive, symmetric, and
transitive closure of this relation, so that ∼ is an equivalence.
    With this definition, the condition is:

(VI) No equivalence class for the relation ∼ contains more than two elements.

   In the billiard case, (VI) prohibits, for example, participation of more than two balls in

                                                   19
                                                        M
                           v 1( 1 )
                                            p1                         p3
                                                                             v 3( 2 )

                                                        v2
                                          v1                           v3
                                                   p2
                                                                       v 2( 1 )


                                                            v 2( 2 )


                                      Figure 7.1: A triple collision

the same collision (but several disjoint pairwise collisions may take place at the same time).
Figure 7.1 shows such prohibited triple collision where (4) holds for the pair (i = 1, j = 2)
and, separately, for the pair (i = 2, j = 3), but not for the pair (i = 1, j = 3), because
|p1 − p3 | > D.
    In Figure 7.1, the initial condition before collision, including positions of the balls and
their velocities v1 , v2 and v3 , is mirror symmetrical with respect to the middle vertical line
M. There are two possible orders of processing this collision by the algorithm. In one order,
balls 1 and 2 collide first and obtain new velocities v1 (1) and v2 (1) , and then balls 2 and 3
collide and obtain new velocities v2 (2) and v3 (2) . The initial velocity of ball 2 for the second
pairwise collision is v2 (1) as if the second collision occurred later than the first one. The
net result of the triple collision is the three balls moving away from the collision site with
velocities v1 (1) , v2 (2) , and v3 (2) , which are not mirror symmetrical with respect to M. Hence,
the outcome of the triple collision depends on the order of processing and so the history of
the entire simulation.
    With infinite precision computations, in the case of chaotically colliding billiard balls, the
probability of violating (VI) is zero. However, in our finite precision experiments multiple
collisions could practically occur and hence (VI) could be violated. The proof in Section 8
of correctness of the simulated trajectory should be understood as an assurance that if the
machine precision is infinite, the correctness holds for as long as (VI) holds.
    In order to show that the algorithm in Figure 4.1 reconstructs the trajectory of each
component “correctly” we must know what a “correct” trajectory is. With assumptions (I)
- (VI), starting with a global state at time 0, we can uniquely define the system state at
any positive time using the naive algorithm discussed in Introduction. We call the obtained


                                                   20
trajectory the correct one.
    The algorithm in Figure 4.1 ignores many events on this trajectory. The task of proof is
showing that despite of this the trajectory does not change.

8. Invariants and correctness proof

     The actions of either simulation algorithms in Figure 4.1 or in Figure 6.1 can be sum-
marized as follows: a repeated update of arrays new[1 : N], old[1 : N], and event[1 : N, 1 : 2]
in such a way that the following conditions remain invariant:

                              max time[i, old[i]] ≤ min time[i, new[i]]                     (13)
                          1≤i≤N                     1≤i≤N

for i = 1, 2, ...N we have:

                 time[i, new[i]] ≤ min{                min                Pij , min Qik }   (14)
                                          1≤j≤N,j6=i,time[j,new[j]]≥Pij       1≤k≤K


and
       either partner[i, new[i]] = Λ,
       or j = partner[i, new[i]] is an integer in the interval N + 1 < j ≤ N + K,           (15)
       or j is an integer in the interval 1 ≤ j ≤ N and partner[j, new[j]] = i

    Conditions (13), (14), and (15) are trivially satisfied in the beginning of the simulation.
Invariance of condition (13) is obvious. As to (14) and (15), their invariance can be violated
temporarily after a cycle during which one component participating in a two-component
interaction has been processed but the other has not been yet. After both components have
been processed, and no other two-component interaction processing has been started, (14)
and (15) hold. For (14), it follows from lines 4, 5, and 6 in Figure 4.1 and for (15), it follows
from symmetricity of matrix Pij . The symmetry is an obvious implication of (I) and (II).
Observe, that invariance of (13) and (14) requires no consistency conditions (I) - (VI).
    Invariant (14) is the key to understanding the “wasteful” strategy of the data update in
this algorithm. Consider an example. Let N = 3, K = 0. Figure 8.1 shows trajectories of
three billiard balls A, B, and C. We assume that at time t = 0 the balls are positioned on
the same horizontal line and we suppose that these are their old positions, i.e., those stored
in array event[., old[.]].
    On the basis of the old events only, C can see two immediate collisions, one with B when
the balls occupy positions B2 and C2; we call it collision B2,C2, and the other with A,
namely collision A2,C1. C also notes that both A and B have a scheduled event at time
earlier than times of either A2, C1 and B2, C2. Thus, the set of balls X over which the
minimum of PCX is to be taken according to (14) is empty and this minimum together with
the time of the immediate next interaction for C is +∞.
    With the given old events, the following assignment of new times would satisfy (14):
both time[A, new[A]] and time[B, new[B]] are equal to the time of collision A1, B1, end
time[C, new[C]] = +∞. With such an assignment, three inequalities (14) turn into equalities.


                                                  21
    The assignment time[i, [new[i]] = +∞ simply means that C sees no future interaction at
this stage of simulation. A more aggressive strategy of precomputation, in which C would
look one more step ahead and would examine possible collisions with A and B based on
their velocities after an as yet unprocessed collision A1, B1, is possible but is prohibited in
the proposed algorithm. Such an aggressive strategy perhaps would work well for a small
number of balls but if there are many of them, it would require a complicated data structure
to support an arbitrary-many-step lookahead. Following our “lazy” or “wasteful” strategy,
C does not do this and does not schedule for more than one step ahead. This allows us to
keep data structure very simple.
    Invariants (13) and (14) imply the following useful invariant
                  min{ min Pij ,       min       Qik } ≥ min time[i, new[i]]              (16)
                       1≤i,j≤N     1≤i≤N,1≤k≤K             1≤i≤N

   Now we prove correctness of the algorithm. The proof proceeds by showing that if

(*) the simulated trajectory is identical to the “correct” one defined in Section 7, for all
t in the interval 0 ≤ t ≤ max1≤i≤N time[i, old[i]],

then

(**) after all events with times equal to min1≤i≤N time[i, new[i]] will be processed, the thus
extended simulated trajectory will be identical to the “correct” trajectory for all t in the
interval 0 ≤ t ≤ min1≤i≤N time[i, new[i]].

    This would constitute the inductive step, while the base for the induction is obviously
satisfied since (*) is correct for the program state initialized for t = 0 as described in
Figure 4.1.
    The “correct” trajectory has no interaction on the open interval
                        max time[i, old[i]] < t < min time[i, new[i]],
                       1≤i≤N                       1≤i≤N

because if it did, (16) would be violated. Hence the simulated trajectory is identical to the
“correct” one for all t in the interval 0 ≤ t < min≤i≤N time[i, new[i]]. By (I) - (VI), this
property extends to the point t = min1≤i≤N time[i, new[i]] and this completes the proof.

9. An application example: disk packing problem

    The following model is simulated in [7]: N points are placed randomly within an L × L
square. Periodic boundary conditions apply in both directions. The N points are assigned
random initial velocities and in the absence of subsequent collisions would move with these
velocities along straight lines threading through an infinite sequence of periodic images of
the basic square. However, the points also begin to grow at a common rate into elastic rigid
disks, with diameters that are given by linear function of time D(t) = at, t > 0. As a result,
particle collisions become possible, and increase in frequency as D(t) increases. We permit
D(t) to grow until the system “jams up” thus obtaining the final packing.

                                              22
                             B2           C2

                                     A2        C1



                    A1          B1




A                               B                                 C


    Figure 8.1: Asynchronous collisions of three billiard balls




                                23
    This is a variant of the billiard simulations. Two differences are:
1) instead of equation |p + vt|2 = D 2 as in Figure 2.1, equation |p + vt|2 = (at)2 has to be
solved; the latter is still a quadratic equation with respect to t
2) the normal components of v1 new and v2 new , the velocities of disks after a collision (see
Figure 2.2), have to be increased to guarantee that disks do not overlap or stick at each
other. Any additive velocity larger than a/2 would be appropriate.
    Energy or momentum conservation are lost with such an additive; as the simulation
progresses the system “heats up” and as the disk speeds reach large values computational
precision may be lost. The existing program once in a while interrupts the simulation
projecting all the disk positions into a particular time value, then scales down and balances
them.
P       (The velocities vi , i = 1, ...N, of N disks of equal masses are said to be balanced if
   1≤i≤N vi = 0.)
    Figure 9.1 and 9.2 show some results of these experiments, in particular show “rattler”
disks which remains unjammed within the walls of jammed neighbors [7]. In the experiment
presented in Figure 9.2, the large square is subdivided into 40 × 40 small square sectors.
Rather than checking a possible next collision with 8 × 1999 candidates, only about 10 disk
candidates for the next collision are checked.

10. Comparing practical performance of the algorithm with the other published
    algorithms

     Physicists often study hard-sphere and hard-disk models using computing experiments.
However, with the exception of [3] and [1], nobody discusses the details of the algorithms
used and with the exception of [1], nobody gives performance data.
    We read in [1]: “The IBM704 calculator handles about 2000 collisions per hour for 100
molecules and about 500 collisions per hour for 500 molecules”
    Assuming that IBM704 was not slower than 0.02 MFLOP [2] this scales up to no more
than 30 collisions per second for a 1 MFLOP machine. The speed of our calculations is in
the range 150 - 450 pairwise collisions per second (independently of the number of disks) on
VAX8550 which has speed 1 MFLOP. Thus, even the most pessimistic comparison with [1]
gives about an order of magnitude speed-up of our algorithm.
    Simulation of 50000 to 55000 committed events in a random configuration of 160 disks is
reported in [5]. Let us count one pairwise collision as two committed events, and one sector
boundary crossing or cushion reflection as one committed event.
    The model [5] is different from the one we simulated in that instead of periodic boundary
conditions, rigid elastic “cushions” are employed to guard the cell boundaries. To compensate
for the difference, let us equate an external boundary crossing in program [7] with one cushion
reflection in [5]. Note that when scheduling a collision close to the cell boundary, program [7]
considers not only internal disks as the candidates for collision, as program [5] does, but also
their periodic images. This additional complexity in program [7] more than compensates
for a possible loss of complexity due to substituting a cushion reflection with a boundary
crossing.
    To make a fair comparison, ratio of the diameter to L must be set as in [5]. Since the
value of this ratio is not indicated in [5], different pictures of 160 randomly placed disks for

                                              24
                   .........................................
                   .                   27                                                          .
                   .                                                                               .
                   .
                   .                                  23                                           .
                                                                                                   .
                   .
                   .                                                 11                    16      .
                                                                                                   .
                   .
                   .        2                                                                      .
                                                                                                   .
                   .
                   .                      22                                                       .
                                                                                                   .
                   .
                   .                                     12                      4                 .
                                                                                                   .
                   .
                   .                                                                           21  .
                                                                                                   .
                   .
                   .           10                                                                  .
                                                                                                   .
                   .
                   .
                                                                    26                             .
                                                                                                   .
                   .
                   .                               24                                3             .
                                                                                                   .
                   18
                   .
                   .
                                                                                                   .
                                                                                                   .
                   .
                   .
                                    5                                                              .
                                                                                                   .
                   .
                   .
                                                                        14                         .
                                                                                                   .
                   .                                                                   15          .
                   . 6
                   .                          25                                                   .
                                                                                                   .
                   .
                   .                                          9                                    .
                                                                                                   .
                   .
                   .                                                        19                     .
                   .
                   .              17                                                         7 ...
                   .
                   .
                                                  20                                               .
                                                                                                   .
                   .
                   .
                                                                   1                               .
                                                                                                   .
                   . . .13
                         . . . . . . . . . . . . . . . . . . . . . . . . . . . . .8. . . . . . . . .




Figure 9.1: 27 disks after 100000 collisions; disk 24 is a rattler




                                                      25
Figure 9.2: 2000 disks after 42 × 106 collisions. Dots mark significant rattlers




                                      26
several different diameters were produced and the one which resembled the most Figure 9 in
[5] was selected. In the selected picture, the ratio is 0.015. Then we made a measuring run,
in which sector boundary crossings were counted only for 16 sectors as specified in series I
in [5]. The run was continued until the number reached 52000 as in [5]. It took 90 seconds
CPU to complete this run.
    A similar run in [5] (Series I) on one PE took 440 seconds and took 62 seconds on 32
nodes of a hypercube MARK III. (For 32 and 64 sectors, it took, respectively, 44 and 42
seconds in [5].) It is known [4] that one node of MARK III is about 60% faster than a VAX
8550, the host computer in [7]. Besides, algorithm [7] is a Fortran code while program [5] is
written in the C-language, both compiled under UNIX T M . This yields an additional 10%
in favor of algorithm [7], since Fortran is slower than C under a UNIX T M compilation.
    Thus, one concludes that the serial algorithm [7] runs about as fast as the parallel Time
Warp [5] on a 32-node hypercube. 1

11. Other billiard-like simulations

     A collision of two billiard balls of radius D/2 each can be considered as an interaction
of two zero-size particle with potential V (r) = 0 for distances r > D and V (r) = +∞
for r ≤ D. More general piece-wise constant potentials can be dealt with using the same
algorithm, e.g., the square-well potential [1]:

                                         V = +∞, ifr < σ1
                                         V = V0 , ifσ1 < r < σ2                                            (17)
                                         V = 0,   ifσ2 < r

where V0 , σ1 , and σ2 are finite constants. We can imagine two concentric balls: the “hard
core” ball of diameter σ1 and a larger external ball of diameter σ2 and correspondingly two
types of “collisions”: internal, of the hard-cores and of the external balls. Each type has its
own jump function.
    By the Monte-Carlo simulation [9] shows that larger particles move against the gravita-
tional force if placed in a vibrating container together with smaller particles. The balls of
different diameters can be easily handled in our scheme, if the ball diameter becomes a part
of its state. The model [9] can be easily simulated using direct representations of particle
dynamics, rather than by Monte-Carlo.
    The inhomogeneity of components, in general, can be treated in the same way, i.e., by
making the type or the class identification of a component an unchangeable part of its
state. Combat simulations [11] present such inhomogeneity to a large extend, since here a
   1
      After the measuring run was completed, A.P. Wieland kindly informed the author that one sector
boundary crossing is actually counted as two events in [5] rather than as one, as is assumed in this paper.
Also, one pairwise disk collision is counted not as two events as assumed, but as 4 + m events, where variable
m is the number of disks located in the involved sectors at the time of the collision. Suppose only one sector
is involved in each collision, and there are totally 16 sectors (as in Series I in [5]). Then m is about 10. This
makes the total count of events generated in [5] during a comparable simulation time interval several times
higher than was assumed in the experiments. This, in turn, makes program [7] faster than program [5].



                                                       27
component represents a military unit of one of the two opposing armies and there are many
types of such units.
    Collisions may be generalized to any state changes, not necessarily immediately leading
to the trajectory change. A typical simulation rule in [11] looks like follows: “if within
radius σ, a unit detects m units of the same army and n units of the opposing army, then it
takes course of action c(n, m) from the time of detecting this situation until the time when
another rule becomes applicable.” We can represent the set of these rules by surrounding a
zero-sized unit by several circles, each representing one such a rule, A counter “inside” the
unit state gets an instantaneous increment, when a particular circle “collides” with another
unit. The counter change may or may not trigger the change of the course of the actions.
Such mechanisms can be represented within the discussed framework and simulated using
the algorithm in Figure 4.1.
    According to [10], a variant of the dense packing algorithm can be used in finding optimal
spherical codes. Here the task is to find N points pi , i = 1, ...N, on the sphere in the k-
dimensional Euclidean space in such a way that mini6=j distance(pi , pj ) → max. We would
start with a random configuration of N points and then grow “caps” of equal size each
cap having one point as the center. Caps are prevented from the overlap by the mean of
collisions.

References

[1]        B.J. Alder and T.E. Wainwright, Studies in molecular dynamics. I. General
           method, Journ. Chem. Phys., 31, 2 (1959), 459–466.
[2]        C.J. Bashe et al., IBM’s early computers, MIT Press, 1986.
[3]        Erpenbeck, J.J, and Wood, W.W., Molecular dynamics techniques for hard-core
           systems, in Statistical mechanics. Part B: Time-dependent processes, Berne, J.B.,
           ed., Plenum, New York, 1977, p.1–40.
[4]        Fox, G.C., The hypercube and the Caltech concurrent computation program: a
           microcosm of parallel computing, in Special purpose computers, Alder, B.J., ed.,
           Acad.Press, New York, 1988, p.1–40.
[5]        P. Hontales, B. Beckman, et al., Performance of the colliding pucks simulation of
           the Time Warp operating systems, Proc. 1989 SCS Multiconference, Simulation
           Series, SCS, 21, 2, p.3–7.
[6]        J. Katzenelson, Computational structure of the N-body problem, Siam J. Sci.
           Stat. Comput., 10, 4 (1989), p.787–815.
[7]        B.D. Lubachevsky and F.H. Stillinger, Geometric properties of random disk pack-
           ings, J. Statistical Physics, 60, 5/6, (Sept. 1990) p.561–583.
[8]        Lubachevsky, B.D., Simulating colliding rigid disks in parallel using bounded lag
           without Time Warp, Proc. 1990 SCS Multiconference, Distributed Simulation,
           Simulation Series, SCS, 22, 1/2, p.194–202.

                                             28
[9]    Rosato, A., et al., Why the Brazil nuts are on top: size segregation of particulate
       matter by shaking, Physical Review Letters, 58, 10 (1087), p.1038–1040.

[10]   W. Smith, Private communication.

[11]   F. Wieland, and D. Jefferson, Case studies in serial and parallel simulation, Proc.
       1989 Int. Conf. Parallel Processing, Vol.III, Ris, F. and Kogge, M., eds., p.255–
       258.

[12]   www.pack-any-shape.com




                                         29
