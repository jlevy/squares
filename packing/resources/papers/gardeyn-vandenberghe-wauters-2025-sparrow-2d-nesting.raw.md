                                                             An open-source heuristic
                                                          to reboot 2D nesting research
                                                            Jeroen Gardeyna,∗, Greet Vanden Berghea , Tony Wautersa
                                                                a
                                                                    KU Leuven, Department of Computer Science, NUMA, Belgium




                                        Abstract
arXiv:2509.13329v1 [cs.CG] 5 Sep 2025




                                        2D nesting problems rank among the most challenging cutting and packing problems. Yet, de-
                                        spite their practical relevance, research over the past decade has seen remarkably little progress.
                                        One reasonable explanation could be that nesting problems are already solved to near optimality,
                                        leaving little room for improvement. However, as our paper demonstrates, we are not at the limit
                                        after all. This paper presents sparrow, an open-source heuristic approach to solving 2D irregular
                                        strip packing problems, along with ten new real-world instances for benchmarking. Our approach
                                        decomposes the optimization problem into a sequence of feasibility problems, where collisions be-
                                        tween items are gradually resolved. sparrow consistently outperforms the state of the art — in
                                        some cases by an unexpectedly wide margin. We are therefore convinced that the aforementioned
                                        stagnation is better explained by both a high barrier to entry and a widespread lack of reproducibil-
                                        ity. By releasing sparrow’s source code, we directly address both issues. At the same time, we are
                                        confident there remains significant room for further algorithmic improvement. The ultimate aim
                                        of this paper is not only to take a single step forward, but to reboot the research culture in the
                                        domain and enable continued, reproducible progress.
                                        Keywords: cutting and packing, irregular, strip packing, open source, nesting


                                        1. Introduction

                                            2D irregular cutting and packing (C&P) – or nesting – problems involve fitting a set of smaller
                                        items into larger containers, where the shape of the items and/or containers can be irregular (non-
                                        rectangular). Such optimization problems arise in a wide range of industries such as garment
                                        manufacturing, furniture production, shipbuilding, printing, laser-cutting, metalworking, wood-
                                        working, foam-cutting, leather crafting, and microchip design. Designing effective algorithms to
                                        solve these NP-hard problems (Fowler et al., 1981) has been an active area of research since the
                                        1960s (Art Jr, 1966).
                                            Given the real-world relevance of 2D irregular C&P problems and the ongoing shift in ethos
                                        toward open-source practices (UNESCO, 2021), one would expect to find a vibrant ecosystem

                                           ∗
                                            Corresponding author
                                            Email addresses: jeroen.gardeyn@kuleuven.be (Jeroen Gardeyn), greet.vanden.berghe@kuleuven.be
                                        (Greet Vanden Berghe), tony.wauters@kuleuven.be (Tony Wauters)


                                        Preprint                                                                               September 18, 2025
                        Figure 1: The 2D irregular strip packing problem.


of publicly available implementations that respond to advances in the academic state of the art
(SotA). However, despite more than a decade of stagnation – where there has been little to no
improvement in achievable solution quality – the open-source landscape remains disconnected from
academic progress and trails significantly behind in performance. We hypothesize that there are
two interconnected factors primarily responsible for this situation.
   The first is a high barrier to entry. Beyond the fundamental optimization challenge of
finding good solutions within a vast search space, irregular C&P problems also pose a significant
geometric challenge of verifying the feasibility of such solutions in the first place. Accurately and
efficiently determining whether a given placement of items does not involve any collisions is far
from trivial. These compounding challenges are currently holding back academic advances, as all
implementations must start from scratch.
   The second factor, we believe, which is leading to this stagnation is a lack of reproducibility.
At the time of writing, not a single academically competitive algorithm for 2D irregular C&P
problems has publicly available source code. Moreover, many methods fail to provide enough
explanation to facilitate complete reproducibility.
   This paper has two interrelated goals: (i) bridge the gap between academic and open-source
algorithms and (ii) lower the barrier to entry for future researchers. When addressing these goals,
we will rely on the recently introduced Collision Detection Engine (CDE) for 2D irregular C&P
problems (Gardeyn et al., 2025), which can handle the geometric challenge. Our entire focus
can therefore target the optimization challenge. On top of the CDE, we will design an open-
source heuristic for the 2D irregular strip packing problem, arguably the most canonical 2D nesting
problem. While we focus on strip packing, our broader ambition is to develop an algorithm that
can generalize to other variants of 2D irregular C&P problems without much effort.


2. Problem definition

   The 2D irregular strip packing problem (2DISPP) involves placing a set of irregular items into
a rectangular strip of fixed width w and variable length l. The objective is to minimize the length
of the strip, while ensuring all items are placed entirely within it and none of them collide with
each other. Figure 1 illustrates the problem through an example solution.
   Let us begin by introducing some notation:


                                                  2
         i∈I              : an item i from the set of items to be packed I
         S                : the interior of a shape, represented by a set of points (x, y) ∈ R2
         Si               : item i’s shape
         t                : a rigid transformation: a translation ∈ R2 +
                           rotation ∈ [0, 2π[ + reflection ∈ {0, 1}
         t(S)             : the result of transforming shape S by t
         Sa ∩ Sb ̸= ∅     : a collision between two shapes

   We can now formulate the 2DISPP more formally:

                   min    l
                   s.t.   ti (Si ) ⊆ [0, w] × [0, l]                            ∀i ∈ I            (1)
                          ta (Sa ) ∩ tb (Sb ) = ∅                     ∀a, b ∈ I, a ̸= b           (2)
                          ti ∈ R2 × [0, 2π[ × {0, 1}                            ∀i ∈ I            (3)
                          l>0                                                                     (4)

   The objective of the 2DISPP is to determine a set of rigid transformations {ti : i ∈ I} such
that, when each item i’s shape is transformed by its corresponding transformation ti , all items are
positioned entirely within the strip (Equation 1) and none collide with each other (Equation 2) for
the smallest possible strip length l.
   In practice, the 2DISPP is more restricted than our definition. Item shapes are usually repre-
sented by the interior of simple polygons, with transformations restricted to continuous translations
plus a set of discrete rotations (such as multiples of 90 or 180 degrees). Continuous rotation and
reflection (flipping) are seldom considered in academic publications, despite them being relevant
for some real-world applications. In the interest of generality, we aim for our algorithm to be
compatible with any rigid transformation.


3. State of 2D irregular strip packing

   Solution methods for the 2DISPP fall into three main algorithmic categories. We will briefly
discuss each category, its notable contributions and some key takeaways.

Exact algorithms
   Exact methods for the 2DISPP typically rely on mathematical programming formulations. Leao
et al. (2020) provide a comprehensive survey of the broad range of exact algorithms for irregular
C&P problems. Such approaches can generally only handle a small set of items, support few angles
of rotation and struggle with complex shapes. Although more recent work – such as the mixed-
integer formulation by Lastra-Dı́az and Ortuño (2024) – demonstrates continued advances, exact
approaches remain impractical for many academic instances, let alone complex real-world instances.



                                                       3
Construction-based heuristics
   Construction heuristics build solutions sequentially by placing one item at a time according
to a predetermined ordering in addition to a placement rule. To improve solution quality, many
methods embed a higher-level heuristic that explores different orderings and placement strategies.
Representative work has been conducted by Oliveira et al. (2000); Gomes and Oliveira (2002);
Burke et al. (2006); Bennell and Song (2010); Amaro Junior et al. (2017). These algorithms are
generally straightforward to implement and reproducible provided that sufficient detail is included
in the corresponding publication.
   However, the achievable solution quality of construction heuristics lags significantly behind
the SotA. We can attribute this to the nature of the 2DISPP, which does not lend itself well to
such approaches for two main reasons. First, even minor changes to the ordering of items or their
placement early in the construction process leads to unpredictable changes concerning final solution
quality. This chaotic nature undermines the effectiveness of the higher-level heuristics.
   Second, if one jumps ahead to the densely packed solutions in Figure 10, try to imagine the
orderings and placement rules needed to position the items one by one into similar configurations.
Maybe one could devise an effective placement strategy that works well for one of these instances,
but it is hard to imagine a single set of rules that would work well for all.

Iterative-improvement heuristics
   Most methods relying on iterative improvement begin with a complete solution and repeatedly
apply local modifications – such as shifting or swapping items – in an attempt to find new solutions
of higher quality. Early contributions include Egeblad et al. (2007); Umetani et al. (2009); Leung
et al. (2012). More recent advances by Elkeran (2013); Wang et al. (2017); Sato et al. (2019)
represent the SotA for the 2DISPP. The common theme across these methods is that they tolerate
temporary collisions between items. The strip gets converted into a container with fixed dimensions
and, every time a feasible solution is found, its length is reduced further. This shrinking leads to
new collisions, which the aforementioned methods attempt to gradually resolve in order to reach a
feasible solution for the shorter strip.
   While many of these iterative-improvements heuristics can achieve high-quality solutions, they
tend to be more complicated than construction-based heuristics. Even when their algorithmic flow is
presented clearly – as in Sato et al. (2019) – the absence of source code or sufficient implementation
details prevents true reproducibility.

Open source
   Solid, robust and publicly available implementations to solve the 2DISPP are scarce. A notable
exception is a tree-search heuristic by Fontan (2023). This heuristic has a unique approach to
handling the geometric challenge which involves decomposing shapes into trapezoids. Despite rep-
resenting a valuable open-source contribution, Fontan (2023)’s method is unrelated to the iterative-
improvement methods and cannot consistently compete with the academic SotA.


                                                  4
4. A sequence of feasibility problems

   As indicated in Section 3, the best-performing algorithms for the 2DISPP temporarily relax
the non-collision constraint (Equation 2) during their iterative search. These methods essentially
convert the optimization problem into a sequence of feasibility problems. Each feasibility
problem fixes strip length l and the goal becomes to find a single solution that is feasible.
   Umetani et al. (2009) referred to this subproblem as the ‘Overlap Minimization Problem’, but
we find this term somewhat misleading. Feasibility, not minimal overlap, is the true goal. Any
solution with overlap is ultimately invalid, regardless of how minimal it may be. Therefore, a more
appropriate name for this subproblem would probably be the ‘Overlap Elimination Problem’.
   The idea of exploring infeasible regions has existed for a long time (Glover, 1989) and is a
strategy commonly used in the irregular C&P literature. However, the reasons for its effectiveness
in nesting problems are rarely elaborated upon. We will therefore take this opportunity to offer
some intuition for why this conversion works so well.
   The 2DISPP is a highly constrained problem, with the non-collision constraint (Equation 2)
being the most significant. This constraint is so restrictive that virtually any local modification, such
as shifting or swapping the positions of items, would immediately render a solution infeasible. The
high-quality solutions we seek are effectively rare oases in a vast desert of infeasibility. Algorithms
that cannot venture outside the feasible region are prevented from making meaningful progress.
The best-performing algorithms therefore temporarily relax this non-collision constraint, enabling
them to traverse otherwise inaccessible routes towards high-quality solutions.




                          (a) Two colliding pairs of        (b) Feasible
                                   items

Figure 2: Example of an infeasible and feasible configuration of a set of items within containers of
                                        equal dimensions.

   In order to effectively solve the feasibility problem, an algorithm must be able to move from an
infeasible solution, such as the one depicted in Figure 2(a), towards a feasible solution like the one
in Figure 2(b). We identify three key components required to achieve this:

   • Assessing feasibility: A binary collision check to determine which constraints are violated.

                                                       5
   • Search algorithm: A strategy which explores the solution space in order to incrementally
        resolve collisions.

   • Quantifying infeasibility: As collisions are often not resolvable in a single step, a binary
        check is too coarse to effectively guide the search. A smooth, continuous metric is required
        to evaluate the severity of each collision and direct the search algorithm.

   Sections 5-8 introduce these components one by one and eventually combine them into a com-
plete algorithm to solve the feasibility problem. Finally, Section 9 will integrate everything into a
heuristic to solve the 2DISPP.


5. Detecting collisions

   The most elementary challenge involved in solving any feasibility problem is assessing whether
or not a constraint is violated. Given the geometric challenge that accompanies nesting problems,
checking the feasibility of a solution or even of a single placement in a way that is efficient, precise
and robust is not trivial. The fundamental ways of dealing with this geometric challenge have been
described by Bennell and Oliveira (2008). Currently, all state-of-the-art nesting algorithms rely on
either no-fit polygons (NFPs) or a raster to handle the geometric challenge. However, these two
approaches have serious limitations regarding robustness and precision, respectively.
   A third approach mentioned by Bennell and Oliveira (2008) is trigonometry: a simple, precise,
robust and general way of detecting collisions between two polygons. This approach was historically
very sensitive to the total number of edges in the shapes involved, and therefore seldom used in
practice.
   Recently, Gardeyn et al. (2025) introduced a Collision Detection Engine (CDE) to provide a
fast and reliable way for 2D nesting algorithms to assess feasibility. This CDE builds on trigono-
metric principles and includes a comprehensive suite of algorithmic enhancements to overcome
the traditional limitations of such trigonometric approaches. The CDE is implemented in an open-
source library called jagua-rs1 . jagua-rs supports irregular shapes for both items and containers,
continuous rotation and translation, and easily extends to problem variants containing additional
spatial constraints.
   The optimization algorithm we will introduce in this paper will be built on top of jagua-rs:
assessing feasibility through collision queries and issuing updates to reflect any changes in the
solution. All interactions with jagua-rs throughout this paper can be abstracted into the following
two functions:
jagua-rs::collisions(S) → C
  Returns the set of items C (⊆ I) that collide with shape S.
jagua-rs::move item(i, t)
  Moves item i to a new position defined by transformation t.

   1
       https://github.com/JeroenGar/jagua-rs


                                                    6
6. Quantifying collisions

      To facilitate an effective search algorithm, the binary feasibility check provided by the CDE
(Section 5) needs to be converted into a continuous one capturing the severity of the collision: an
expression of the expected difficulty to resolve it.

Algorithm 1 evaluate item pair(a, b)
 1: if a ∈ jagua-rs::collisions(Sb ) then
 2:      return quantify collision(Sa , Sb )                                                    ▷ Alg. 4
 3: else
 4:      return 0

      Let us begin by introducing Algorithm 1, the general function to evaluate any pair of items
a, b ∈ I. The procedure begins by querying the CDE to determine whether the two items are
colliding with each other. When no collision occurs, the function returns 0. When a collision
is detected, the shapes of the items involved will be passed to the quantify collision(Sa , Sb )
function.
      Many existing approaches for the 2DISPP quantify the severity of a collision in some way.
Imamichi et al. (2009) proposed using penetration depth, which denotes the smallest translation
needed to separate two colliding entities. Instead of the exact penetration depth, they measure
the minimum translation required along a single axis, such as horizontally or vertically. Leung
et al. (2012), Elkeran (2013), Wang et al. (2017) and Sato et al. (2019) each employ some variant of
penetration depth to quantify the severity of a collision. Regardless of the concrete implementation,
these penetration-depth derivatives are essentially all one-dimensional metrics.
      When relying on a trigonometric approach to detect collisions, such as jagua-rs, computing
penetration depth is impractical. We therefore need to find a different way to efficiently quantify
the severity of a collision. It is important to stress that this function will only serve to guide the
search towards a feasible solution as effectively as possible. It does not need to represent anything
tangible, nor does it need to be precise. We aim for a metric that supports continuous rotation
and is insensitive to the complexity of the shapes involved, for the sake of greater generality and
real-world applicability.
      The remainder of this section describes how we design our quantification function, eventually
leading to the complete quantify collision(Sa , Sb ) function that is called within Algorithm 1.

6.1. Area of overlap
      Figure 3 shows two shapes in three different placements, once separated and twice colliding.
Intuitively, the collision in Figure 3(c) appears harder to resolve than the one in Figure 3(b). The
intersection area – how much the shapes overlap – is an obvious candidate for measuring collision
severity. However, calculating this metric precisely is far too expensive to be practical in an iterative
improvement heuristic. Let us investigate whether we can use a shape’s pole of inaccessibility to
devise a cheap proxy.


                                                   7
               (a) Separated                (b) Collision (minor)        (c) Collision (major)

 Figure 3: Two shapes in different configurations, with their respective poles drawn. In (c), the
            penetration depth (δ) between the largest pair of poles is marked in red.


      A shape’s pole of inaccessibility is the point within its interior that lies furthest from the
boundary. This point, along with its distance to the boundary, defines the largest inscribable circle
in the shape. Figure 3 shows a sequence of such inscribed circles – referred to simply as poles from
now on – for each shape. Gardeyn et al. (2025) describe the precise procedure to compute these
sets of poles, extending the approach by Agafonkin (2016). The CDE leverages them to accelerate
the collision detection process and lower its sensitivity to the complexity of the shapes. The set
of poles of shape S is represented by P (S). Poles are generated once (in preprocessing) for every
base shape and can be efficiently transformed in unison with any rigid transformation applied to
the shape.

Algorithm 2 overlap proxy(Sa , Sb )
 1: for (pa , pb ) ∈ P (Sa ) × P (Sb ) do                                           ▷ all pairs of poles
 2:    δ ← penetration depth(pa , pb )
 3:    if δ > 0 then
 4:        α ← α + δ · min{(pa ), (pb )}                                              ▷ : diameter
 5: return α




      Algorithm 2 introduces a proxy for the overlap between two shapes that leverages these poles.
For every combination of poles from the two shapes, the penetration depth (δ) is calculated as the
sum of their radii minus the distance between their centers. All these penetration depths are then
weighted by the diameter of the smaller pole and combined into a weighted sum α, which provides
a suitable proxy for the area of overlap.
      Figure 4(a) visualizes the output of this function for the pair of items from Figure 3, with the
smaller item being positioned all around the larger one. The shapes and reference points of six
example placements are visualized. The region where the two items do not collide is colored green.
The region where they collide is shaded red, with the intensity of the red mapping to the output
of the function described in Algorithm 2. To help visualize the intensity further, Figure 4(b) maps
the value of this function to the height of a 3D surface.
      In theory, this proxy function has a quadratic complexity O(n2 ) regarding the number of poles.
In practice however, the computation time is manageable because (i) a relatively small number of
poles (8-16) suffices to capture most shapes and (ii) the loop can be vectorized in modern CPUs



                                                     8
                                           (a) 2D                    (b) 3D

   Figure 4: Visualization of the overlap proxy for the same pair of items from Figure 3.        :
                            feasible,       : overlap proxy(Sa , Sb ).


either automatically by the compiler or by explicitly leveraging SIMD2 instructions.
   This overlap proxy exhibits many desirable properties of a quantification function for the severity
of a collision: fast computation, a smooth gradient, and a value that consistently increases with the
amount of overlap. However, poles do not cover the entire item and therefore collisions may occur
without any pairs of poles overlapping. For the collision depicted in Figure 3(b) or throughout the
entire white region in Figure 4, Algorithm 2 will return 0 even though the CDE rightfully detects
a collision. This is problematic because these (minor) collisions are not contributing anything to
the quantification function and consequently provide no information to help guide the search.

6.2. Decaying penetration depth
   To address the aforementioned issue, we introduce a decaying version of the penetration depth
between pairs of poles. When δ is smaller than a certain threshold ε, we switch to a hyperbolic decay
function which asymptotically approaches 0 as the distance between the pair of poles increases. The
decaying penetration depth δ ′ is defined as follows:
                                                   
                                                   δ         if δ ≥ ε
                                              δ′ =                                                   (5)
                                                    ε2       otherwise
                                                    −δ+2ε


A comparison of the decaying variant and standard penetration depth function profiles is visualized
in Figure 5.
   Algorithm 3 describes the modified overlap proxy, which employs the decaying penetration
depth. Threshold ε is computed as the larger diameter of the shapes – the furthest distance
between any two of its points – multiplied by a small constant Rε . Figure 6 visualizes the new
function in the same way as Figure 4.
   Every collision now contributes to the quantification function and there is a smooth gradient
present everywhere. Additionally, a sharp drop-off is now present at the feasibility boundary,


   2
       Single Instruction, Multiple Data


                                                          9
                                               δ        f (x)
                                               δ′
                                                    ε
                                                    2           ε
                                                                     x

        Figure 5: Comparing the standard (δ) and decaying (δ ′ ) penetration depth functions.

Algorithm 3 overlap proxy decay(Sa , Sb )
 1: ε ← Rε · max{(Sa ), (Sb )}                                                       ▷ : diameter
 2: for (pa , pb ) ∈ P (Sa ) × P (Sb ) do
 3:    δ ← penetration depth(pa , pb )
 4:    if δ > ε then
 5:        δ′ ← δ
 6:    else
 7:        δ ′ ← ε2 /(−δ + 2ε)
 8:    α ← α + δ ′ · min{(pa ), (pb )}
 9: return α


resulting in a significant distinction between a colliding and a non-colliding placement.

6.3. Shape-based penalty
      The proxy provided by Algorithm 3 is a decent starting point for quantifying the severity of
a collision. However, the area of overlap is not necessarily the only factor which influences how
difficult a collision is to resolve. When quantifying collisions purely on the basis of the amount
of overlap, we noticed that our search algorithm had a strong tendency to converge to situations
with minor amounts of overlap between pairs of items with large and/or concave shapes. It seems
that resolving such collisions is disproportionately more disruptive to the structure of the overall
solution and therefore much harder compared to resolving collisions between smaller and/or more
convex items.
      To counter this, we experimented with adding a fixed term λ, that penalizes collisions involving




                                      (a) 2D                        (b) 3D

 Figure 6: Visualization of the decaying overlap proxy for the same pair of items from Figure 3.
                         : feasible,       : overlap proxy decay(Sa , Sb ).


                                                    10
such troublesome shapes. One candidate to base the penalty on is the area of a shape’s convex hull,
given that it captures both the size and the concavity of a shape. However, employing this area
directly penalized these troublesome shapes too excessively. The square root of this area instead
provides a much better balance. Therefore, we define shape Sa ’s penalty λa as:
                                             p
                                      λa =    area(convex hull(Sa ))                                 (6)

      Since a collision always takes place between a pair of shapes, we need to merge individual
penalties. From our experiments, we found that the geometric mean of the two penalties was the
most effective way to combine them. For a collision between Sa and Sb , we define the combined
penalty as:
                                                      p
                                              λab =    λa · λ b                                      (7)


Algorithm 4 quantify collision(Sa , Sb )
 1: α ← overlap proxy decay(Sa , Sb )                                                           ▷ Alg. 3
          √
 2: λab ← λa · λb                                                                                ▷ Eq. 7
           √
 3: return α · λab


      Algorithm 4 presents the full procedure for quantifying a collision between two shapes. We first
compute overlap proxy α, and then scale its square root by the combined penalty λab . Taking the
square root of α converts the proxy from an area-like (2D) metric into a one-dimensional one, making
it more comparable to the penetration depth derivatives commonly used in other approaches. This
function can now be used in Algorithm 1 to complete the evaluation of pairs of items.


7. Navigating a continuous search space

      All that now remains is to design a search algorithm which is able to gradually resolve collisions.
One of the most fundamental components of any local search algorithm is the move operation,
enabling the algorithm to transition from one solution to a neighboring one. Algorithm 5 introduces
the local search move our approach will employ. Its core idea – repositioning every colliding item,
one by one, in a randomized order – is shared by Umetani et al. (2009); Sato et al. (2019); Elkeran
(2013).

Algorithm 5 move items
 1: Ic ← {i ∈ I : |jagua-rs::collisions(Si )| > 1}                                     ▷ colliding items
 2: for i ∈ Ic in a random order do
 3:       t ← search position(i)                                                                ▷ Alg. 6
 4:       jagua-rs::move item(i, t)

      In 2D irregular C&P problems, items can be positioned in a continuous 2D space and sometimes
also rotated in a continuous manner. This means it is far too time-consuming to evaluate a full
neighborhood of all possible item positions. Previous approaches have handled this continuous

                                                      11
search space in a variety of ways. Sato et al. (2019) discretize the search space into a (multi-
resolution) grid. Meanwhile, approaches that rely on NFPs (Umetani et al., 2009; Elkeran, 2013)
narrow the search space down to a set of positions along the edges of the union of all NFPs. From
this (still continuous) set of positions, only a few specific points such as the vertices of the combined
NFP are typically considered. All of these approaches effectively restrict the search space to a finite
set of positions.
   Instead of restricting the search space, we will preserve its continuous nature by relying on
a sampling strategy to search for new item positions. Such an approach only evaluates a limited
number of sampled positions, but every position remains a possible candidate. The aim is to obtain
high-quality placements while keeping the number of samples to be evaluated as low as possible.

Algorithm 6 search position(i)
 1: f (i, t) 7→ e   ← evaluate sample(i, t)                                                     ▷ Alg. 7
 2: t∗ ← perform sampling(i, f (i, t) 7→ e)                                                     ▷ Fig. 7
 3: return t∗


   Algorithm 6 indicates how we search for a new position for a single item i. A sample is defined
as an item and an accompanying transformation: (i, t). We define a function to evaluate samples
f (i, t) 7→ e which will, for now, remain abstract: it takes as input a sample and returns a single
value e indicating the quality of that sample. This function, along with the item, is passed to the
sampling procedure, which returns t∗ , the best position it found to reposition item i to.
   Thanks to the open-source nature of our implementation, we can visually illustrate how the
perform sampling function inside Algorithm 6 works. This allows us to provide an intuitive
understanding of the process without relying on convoluted pseudocode or dense mathematical
notation. Readers interested in the concrete implementation details can refer directly to the source
code (Section 10).




      (a) Before           (b) Random        (c) Random samples    (d) Refinement        (e) After
                        samples in the strip: near the current      of 3 samples
                                Tdiv             position: Tf oc

 Figure 7: Searching for a new position for a single item (in bold) using the perform sampling
                                           procedure.

   Figure 7 illustrates the complete process of searching for a new position for the item highlighted

                                                    12
with a thick border in Figure 7(a). First, we generate a number of samples uniformly at random
within the container – the red overlays in Figure 7(b) – and collect them in a set Tdiv . Next, we
perform a number of samples uniformly at random in the vicinity of the item’s current position – the
blue overlays in Figure 7(c) – resulting in set Tf oc . This leads to a set of samples Tdiv ∪ Tf oc , which
is both diverse within the container and also focused around the item’s current position. While
this set may contain promising samples, it is unlikely that any of them will yield a high-quality
placement given they are all randomly generated.
      We therefore select some of the most promising samples ∈ Tdiv ∪ Tf oc to be refined into their
respective local optima. A sample is considered promising if it is among the best evaluated and
its transformation is sufficiently different from the other samples already selected. Figure 7(d)
visualizes this refinement process for three samples that are highlighted in lime, cyan and purple.
The refinement procedure is inspired by the adaptive coordinate descent approach described by
Loshchilov et al. (2011) and greedily shifts sampling in the direction of improving evaluation.
Figure 7(e) shows the position eventually chosen to move the item to.
      Provided that the cost of evaluating a sample is low enough, this approach is an effective way to
find high-quality placements while remaining completely agnostic to the underlying implementation
of f (i, t) 7→ e.


8. Solving the feasibility problem

      We have introduced how to detect collisions, how to quantify those collisions, and how to move
from one solution to a neighboring one by repositioning colliding items. The final step in solving the
feasibility problem is to combine all these components into a complete search algorithm, which
gradually resolves collisions with the ultimate aim of reaching a feasible configuration of items.

8.1. Guided local search
      How to search for a new position was explained in Algorithm 6, but the function to evaluate
samples was left abstract. A straightforward way to evaluate a sample would be to aggregate the
severity of all collisions that would occur if the item were placed at the sampled position, akin
to Algorithm 1. However, such a static evaluation function would cause the search to converge
to a local optimum within a couple of iterations. Approaches proposed by Umetani et al. (2009)
and Sato et al. (2019) avoid this issue by relying on Guided Local Search (GLS) (Voudouris et al.,
2010): a metaheuristic which dynamically modifies the evaluation function to escape local optima
and move towards promising regions of the search space.

Algorithm 7 evaluate sample(i, t)
 1: C ← jagua-rs::collisions(t(Si ))
 2: for c ∈ C \ {i} do                                                              ▷ ignore item i itself
 3:    wic ← weight of item-pair (i, c)
 4:    e ← e + wic · quantify collision(t(Si ), Sc )                                              ▷ Alg. 4
 5: return e


                                                    13
      Algorithm 7 introduces how we evaluate a sample (i, t). First, the CDE is queried to retrieve
the set of items C that would be colliding with item i if it were moved to the position defined by
transformation t. These prospective collisions are quantified, multiplied by the corresponding item-
pair weight wic , and summed up to a total evaluation value e. These dynamic item-pair weights
are the mechanism through which GLS modifies the evaluation function, thereby influencing the
search process.

Algorithm 8 update weights
 1: emax ← max{evaluate item pair(a, b): a, b ∈ I, a ̸= b}                                      ▷ Alg. 1
 2: for a, b ∈ I : a ̸= b do                                                        ▷ all pairs of items
 3:      e ← evaluate item pair(a, b)                                                           ▷ Alg. 1
 4:      if e > 0 then
 5:          m ← Ml + (Mu − Ml ) · (e/emax )
 6:      else
 7:          m ← Md
 8:      wab ← max{1, wab · m}


      All item-pair weights are initialized to 1 and every time Algorithm 8 is called, each weight
is updated by multiplying it by its corresponding factor m. If the pair of items is colliding, m
represents a linear mapping ∈ ]Ml , Mu ] of the severity of their collision e relative to the most severe
collision emax . Item pairs with more severe collisions will thus have their weight rise faster than
those with less severe collisions. If a pair is not in collision, their weight is multiplied by Md (< 1)
and eventually decays back to 1 over time.

8.2. Separation Procedure
      Simply looping move items (Algorithm 5) and update weights (Algorithm 8) would technically
suffice to traverse the solution space, but this approach lacks any mechanism to backtrack to
previous solutions. A more sophisticated approach that incorporates this ability should improve
the effectiveness of the search algorithm.
      Let us begin by defining the evaluation function for the entire solution:
                                     X
                                             evaluate item pair(a, b)                                (8)
                                     a,b∈I
                                      a̸=b


This function is the sum of the evaluation of every item pair (Algorithm 1). Whenever Equation 8
returns 0, all collisions have been resolved and a feasible solution has been reached.
      Algorithm 9 describes the complete procedure to solve the feasibility problem introduced in
Section 4. The separation procedure starts from an infeasible situation with colliding items and
attempts to resolve all of its collisions. At its core, the algorithm continually repositions items,
updates the item-pair weights and replaces the incumbent solution s∗ whenever improvements
are found with respect to Equation 8. Whenever feasibility is reached, the procedure stops and
immediately returns the solution. Once a certain number of iterations without improvements nmax

                                                     14
Algorithm 9 separate(mmax , nmax )
 1: s∗ ← current solution ; e∗ ← Eq. 8 ; m ← 0
 2: while m < mmax and e∗ > 0 do
 3:    restore to s∗ ; sinit ← s∗ ; n ← 0
 4:    while n < nmax and e∗ > 0 do                                                     ▷ an attempt
 5:        move items multi                                                                ▷ Alg. 10
 6:        update weights                                                                   ▷ Alg. 8
 7:        e ← Eq. 8 ; n ← n + 1
 8:        if e < e∗ then
 9:            s∗ ← current solution ; e∗ ← e
10:            n←0
11:    m←m+1                                                                           ▷ add a strike
12:    if s∗ ̸= sinit then
13:        m←0                                                                         ▷ reset strikes
14: return s∗


is reached, we conclude one attempt. If the incumbent solution was never updated during this
attempt, a strike is added. Conversely, if the attempt improved s∗ , the strike counter is reset to
0. As long as the number of strikes is below a certain threshold mmax , the procedure restores the
incumbent solution s∗ and starts a new attempt, continuing its quest for a feasible solution. Once
the number of strikes exceeds mmax , the procedure halts the search and returns s∗ , which will
unfortunately still be infeasible.
      The behavior we intend to generate through this procedure can be described as follows. GLS
ensures that item pairs colliding across consecutive iterations quickly reach prohibitively large
weights, especially pairs which are involved in the most severe collisions. By contrast, when a pair
of items manages to resolve its collision, the weight slowly decays back down to 1. When a collision
occurs in a region with low GLS weights, the items involved will often ‘transfer’ the collision to
neighboring pairs. Observing this process over multiple iterations reveals that items effectively
push and pull each other, constantly ‘fighting’ for their own space in the container. When the
search inevitably stalls, some items start to accumulate significant weights with all their neighbors.
This will cause them to jump away to an entirely different position in the container, effectively
escaping the local optimum. Readers who are curious to see this behavior in action are referred to
the repository (Section 10), which contains a simple visualizer.
      Figure 8 provides an overview of the separate procedure, where each of the previously intro-
duced components are hierarchically related with one another.




                                                 15
                           separate                A.9
                                                                 search_position      A.6
                      move_items_multi A.10
                                                              perform_sampling      F.8
                          move_items         A.5
                                                                evaluate_sample A.7
                       search_position
                                                               quantify_collision

                       update_weights         A.8

                    evaluate_item_pair A.1                     quantify_collision A.4

                     quantify_collision                       overlap_proxy_decay A.3



Figure 8: The separate procedure and all its underlying components presented in a hierarchical
    overview. Every component references its corresponding algorithm (A.∗) or figure (F.∗).


8.3. Balancing exploration and exploitation
   The random order in which Algorithm 5 repositions colliding items ensures that the search
algorithm can explore a wide range of neighboring solutions. However, in many cases, this random
order might be far from ideal. In order to strike a better balance between exploration and exploita-
tion, Algorithm 10 introduces an enhanced approach to move from one solution to a neighboring
one.

Algorithm 10 move items multi
 1: si ← current solution ; e∗ ← ∞
 2: for N WORKERS times do                                                                  ▷ parallelized
 3:     move items                                                                               ▷ Alg. 5
 4:     e ← Eq. 8
 5:     if e < e∗ then
 6:         s∗ ← current solution ; e∗ ← e
 7:     restore to si
 8: restore to s∗


   Algorithm 10 essentially executes Algorithm 5 multiple times with different random orders
of items. From these multiple neighboring solutions, the best one (Equation 8) is chosen. This
significantly increases the chances of finding improvement while preserving the diversity of the
search process. This enhanced version is employed in the separation procedure (Algorithm 9) to
solve the feasibility problem. Although presented here sequentially, Algorithm 10 is parallelized
across a pool of N WORKERS threads in our implementation.




                                                         16
9. Solving the 2D irregular strip packing problem

   Algorithm 9, which targets the feasibility problem introduced in Section 4, can now be inte-
grated into a complete heuristic to solve the actual 2DISPP. The complete heuristic we propose is
introduced in Algorithm 11 and is divided into two distinct phases. The exploration phase first
provides a lot of freedom to enable investigation of a wide range of solutions. Next, the compres-
sion phase attempts to shrink the strip as much as possible while remaining constrained to the
general configuration of items found at the end of the exploration phase.

Algorithm 11 solve ispp
 1: s∗ ← explore                                                                              ▷ Alg. 12
 2: s∗ ← compress(s∗ )                                                                        ▷ Alg. 13
 3: return s∗



9.1. Exploration phase

Algorithm 12 explore
 1: s∗ ← construct initial solution and shrink strip by Rx
 2: while TLx not reached do
 3:    s ← separate(Mx , Nx )                                                                  ▷ Alg. 9
 4:    if s is feasible then
 5:        s∗ ← s
 6:        shrink strip by Rx
 7:        S←∅
 8:    else
 9:        S ← S ∪ {s}                                                    ▷ pool of infeasible solutions
10:        ŝ ← select from S
11:        s′ ← disrupt ŝ by swapping two large items
12:        restore to s′
13: return s∗


   Algorithm 12 describes the exploration phase, which starts from an initial solution created by
a simple bottom-left-fill heuristic. This constructive heuristic will provide a feasible solution, after
which the strip is shrunk by a factor Rx . Each time the strip is shrunk, all items have to be
contained within these new boundaries. This is achieved by selecting a certain vertical axis within
the strip and shifting items positioned right of this axis to the left, most likely creating multiple
minor collisions.
   The separation procedure (Algorithm 9) attempts to convert this infeasible solution into a
feasible one. If successful, the returned solution s replaces the incumbent solution s∗ , after which
the strip is once again shrunk. If unsuccessful, s represents an infeasible local optimum which is
added to a pool of solutions S. For the next separation attempt, a random solution ŝ is chosen
from S, with those closer to feasibility (Equation 8) having a greater chance of being selected. A
new starting solution s′ is then created by swapping two large items from ŝ. This ensures s′ inherits


                                                  17
many high-quality placements from ŝ while, at the same time, being sufficiently disrupted so it can
escape from the local optimum. This procedure continues until time limit TLx is reached, at which
point the exploration phase returns the best feasible solution found s∗ .

9.2. Compression phase

Algorithm 13 compress(s∗ )
 1: while TLc not reached do
 2:    τ ← elapsed time in phase
 3:    r ← Rsc + (Rec − Rsc ) · (τ /TLc )
 4:    restore to s∗ and shrink strip by r
 5:    s′ ← separate(Mc , Nc )                                                                   ▷ Alg. 9
 6:    if s′ is feasible then
 7:        s∗ ← s′
 8: return s∗


      Algorithm 13 describes the compression phase, which starts from the best feasible solution s∗
the exploration phase generated. The procedure iteratively (i) restores to the incumbent solution
s∗ , (ii) shrinks the bin by ratio r and (iii) attempts to separate. If successful, the incumbent solution
is updated. If unsuccessful, the incumbent solution is restored and the process reattempted.
      Shrink ratio r is much smaller than during the exploration phase and decays linearly from Rsc
to Rec based on the phase’s remaining time limit TLc . This means that the separate procedure only
needs to resolve (progressively) less severe collisions, which it is often able to do without making
major changes to the configuration of items. Because the procedure always restores the best feasible
solution and then shrinks the strip, the search process’ freedom is restricted. The compression phase
is therefore focused on finding out how much further the strip can be shrunk without deviating too
far from the configuration of items provided by the exploration phase.


10. Implementation

      The implementation of our 2D nesting algorithm is written in Rust and called sparrow. It
is publicly available at: https://github.com/JeroenGar/sparrow. The codebase closely follows
the structure of this paper, making it straightforward to understand how sparrow relates to the
algorithms introduced in this paper. Throughout this project, we have strived for maximum com-
putational performance, robustness and leanness of both the algorithm and its implementation.
      The result of these priorities is an implementation that is relatively insensitive to the complexity
and the number of shapes involved, making sparrow suitable as either a practical tool to tackle
real-world problems or a basis for future research. The contribution of each individual algorithmic
component to the overall performance of sparrow was carefully evaluated and those without any
significant contribution were eliminated. As a result, the components presented in this paper
represent an irreducible set required to achieve the performance demonstrated in Section 11.



                                                    18
   It is important to note that, in contrast to some other approaches, sparrow will never produce
a feasible solution where items are ‘touching’ the container or each other. Instead, items will always
be completely separated, if only by a minuscule distance. Exact fits – where moving the position
of an item by even the smallest representable distance causes a collision – cannot be produced by
sparrow.
   There are two reasons for this. First, whenever two entities are extremely close to each other,
jagua-rs will err on the side of caution and report a collision. The CDE was deliberately designed
this way in order to avoid numerical instability due to floating point arithmetic. Second, when
searching new positions for an item, sparrow relies on a sampling approach (Section 7). While the
sampling is configured to be very precise, it cannot target one specific coordinate.
   So far, this limitation concerning exact fits only surfaces in artificial academic instances featuring
simple shapes and vertices with integer coordinates. Conditions which, generally, do not occur in
real-world applications.


11. Computational experiments

   In this section we will evaluate the performance of sparrow by conducting a series of computa-
tional experiments on a set of academic benchmark instances.

11.1. Experimental setup
   All experiments were performed on a machine equipped with an AMD Ryzen™ 9 7950X CPU.
System memory is irrelevant as the entire program easily fits within the 64 MB of L3 cache of the
CPU. Unless specified otherwise, each experiment was run for 20 minutes, with 3 threads active,
and configured with the parameters presented in Table 1.

                  Rε ← 1%                  ▷ Alg. 3 – diameter ratio to compute ε
      (Mu , Ml , Md ) ← (2.0, 1.2, 0.95)   ▷ Alg. 8 – upper, lower and decay weight multipliers
      N WORKERS ← 3                        ▷ Alg. 10 – how many times move items is executed
         (Mx , Nx ) ← (3, 200)             ▷ Alg. 12 – separation parameters for exploration
          (Mc , Nc ) ← (5, 100)            ▷ Alg. 13 – separation parameters for compression
                  Rx ← 0.1%                ▷ Alg. 12 – exploration shrink ratio
         (Rsc , Rec ) ← (0.05%, 0.001%)    ▷ Alg. 13 – compression shrink ratio range
       (TLx , TLc ) ← (0.8, 0.2) · 20′     ▷ Alg. 12,13 – time limits

 Table 1: Configuration of sparrow’s parameters throughout the experiments. The right column
           contains the relevant algorithm(s) and a short description for every entry.

   We used a combination of manual tuning and hyperparameter optimization (Bergstra et al.,
2013) to identify a suitable set of parameters for the algorithm. These parameters were optimized
for the maximum expected performance across all instances from the academic benchmark set when
subject to a 20-minute time limit. This single set of parameters was used for every instance in our
experiments.


                                                   19
11.2. Performance analysis
   To evaluate the performance of sparrow we will use academic benchmark instances from the
ESICUP website3 . We refer to Table 3 in Sato et al. (2019) for an overview of these instances and
their properties.
   Throughout the experiments, we report the quality of a solution in terms of its packing density
ρ. This is the ratio of the area of the items in the strip with respect to the area of the strip itself
expressed as a percentage:
                                             100 X
                                        ρ=       · area(Si )                                       (9)
                                             w·l
                                                   i∈I

   The expected quality E(ρ) and interquartile range of sparrow’s solutions in comparison to the
academic SotA algorithms for the 2DISPP and one open-source implementation are presented in
Table 2. The distributions of the solutions from Table 2 are visualized as violin plots in Figure 9.
One important thing to note is that the width of the strip for some of the most simple instances
– SHAPES0, SHAPES1, SHAPES2, FU, JAKOBS1 and JAKOBS2 – was inflated by 0.01%. This mi-
nuscule inflation should not affect which configurations of items are possible, but suffices to avoid
the issue concerning exact fits (described in Section 10) which would otherwise occur in these arti-
ficial instances. For academic purposes, the best solution produced by sparrow for each instance,
alongside the previous best-known solution, is presented in Table 3 and shown in Figure 10.
   sparrow generally dominates in terms of expected solution quality, both on individual instances
and across the entire benchmark set. Figure 9 reveals that for the three largest instances in terms
of number of items and complexity of their shapes – SWIM, SHIRTS and TROUSERS – sparrow’s
performance distribution lies entirely beyond the previous best-known singular solution. Indeed,
we were able to match or improve upon every previous best-known solution, in some cases by a
significant margin.
   The algorithms composing the academic SotA report only two values per instance: the best
and the expected density from a limited number of runs. This limits our ability to provide detailed
statistical or visual performance comparisons against them. However, to support future in-depth
comparisons against sparrow, we provide all solution data and a complete reproducibility guide in
the repository.
   In conclusion, sparrow establishes a new state of the art for the 2DISPP, consistently producing
solutions whose quality, in most cases, significantly exceeds any previous academic or open-source
results.

11.3. Time-sensitivity analysis
   Different use cases call for varying computational budgets, and therefore it is important to
understand how performance scales with time. Figure 11 presents a time-sensitivity analysis of
sparrow’s expected performance for the three most complex instances from the academic bench-
mark set, normalized to the 20-minute time limit from Table 2. No specific tuning was performed

   3
       https://www.euro-online.org/websites/esicup/data-sets


                                                   20
                                sparrow          ROMA GCS FLD ELS         PS
           instance    Q1(ρ)   Q3(ρ)    E(ρ)      E(ρ) E(ρ) E(ρ) E(ρ)      ρ
           ALBANO      89.39   89.58 89.47 ±0.03 87.55 87.47 88.01 87.38 84.95
           DAGLI       89.01   89.50 89.26 ±0.07 87.50 87.06 87.14 86.27 84.17
           FU          91.93   92.40 92.24 ±0.04 91.95 90.68 91.17 90.00 90.39
           JAKOBS1     89.09   89.09 89.09 ±0.00 89.09 88.90 88.96 88.35 81.67
           JAKOBS2     83.91   85.25 84.77 ±0.17 83.56 81.14 83.41 80.97 80.42
           MAO         85.84   86.45 86.14 ±0.08 83.76 82.93 82.28 82.57 75.94
           MARQUES     90.78   91.02 90.93 ±0.05 89.97 89.40 88.38 88.32 85.48
           SHAPES0     68.38   68.79 68.60 ±0.07 68.73 67.26 67.39 66.85 66.50
           SHAPES1     75.26   75.97 75.69 ±0.11 75.86 73.79 73.91 74.24 72.55
           SHAPES2     84.44   84.88 84.68 ±0.07 83.02 82.40   -   82.55 85.49
           SHIRTS      89.43   89.84 89.66 ±0.06 87.62 87.59 88.21 87.20 85.99
           SWIM        77.94   78.55 78.26 ±0.09 74.29 74.49 74.66 74.10 71.44
           TROUSERS    91.51   91.93 91.73 ±0.05 90.48 89.02 89.17 88.29 89.30

  Table 2: The expected solution quality E(ρ) on academic benchmarks obtained by sparrow,
  four algorithms from the literature: ROMA - Sato et al. (2019), GCS - Elkeran (2013), FLD
   - Wang et al. (2017), ELS - Leung et al. (2012) and one open-source implementation: PS -
  Fontan (2023). For sparrow, quartiles (Q1, Q3) and the margin of error (±) on E, defined as
   the half-width of the 95% confidence interval computed via non-parametric bootstrapping,
  are reported. The reported values for sparrow result from 100 independent runs, each with a
     time limit of 20 minutes. Values for ROMA, GCS, FLD and ELS were taken from their
    respective publications. PS is a deterministic algorithm and was run once under the same
          conditions as sparrow. For each instance, the best E(ρ) is highlighted in bold.


                                           sparrow    previous best
                                instance      ρ         ρ      by
                                ALBANO      89.82     89.58     E

                                DAGLI       90.17     89.51     E

                                FU          92.41     92.41     E

                                JAKOBS1     89.26     89.09 L/E/W/S
                                JAKOBS2     87.73     87.73    E/S

                                MAO         86.87     86.05     S

                                MARQUES     92.02     91.02     S

                                SHAPES0     69.98     68.79 E/W/S
                                SHAPES1     76.73     76.73    E/S

                                SHAPES2     86.23     84.84     E

                                SHIRTS      90.92     88.96    E/W

                                SWIM        79.83     75.94     E

                                TROUSERS    92.62     91.06     S


  Table 3: The best solution densities produced by sparrow for instances in the benchmark set,
 accompanied by the previous best-known density and the algorithm that produced it: l - Leung
et al. (2012). e - Elkeran (2013), w - Wang et al. (2017), s - Sato et al. (2019). Best densities are
                           highlighted in bold. Time limit is 20 minutes.


                                                 21
                               SWIM                                                        TROUSERS




    73%    74%    75%    76%    77%    78%     79%    80%    81%       87%    88%    89%    90%    91%     92%    93%    94%
                              SHIRTS                                                         MAO




    85%   86%    87%    88%    89%     90%    91%    92%    93%       81%    82%    83%    84%    85%    86%     87%    88%
                               DAGLI                                                        ALBANO




          85%    86%    87%    88%    89%    90%     91%    92%       85%    86%    87%    88%    89%    90%     91%    92%
                              MARQUES                                                      SHAPES2




    86%    87%    88%    89%    90%     91%    92%    93%              81%    82%    83%    84%    85%     86%    87%    88%
                              SHAPES0                                                      SHAPES1




       65%      66%    67%    68%    69%    70%     71%    72%         72%    73%    74%    75%    76%     77%    78%    79%
                                FU                                                         JAKOBS2




          88%    89%    90%    91%    92%     93%    94%    95% 80%     81%    82%    83%    84%     85%    86%    87%    88%



      E(sparrow)              E(ROMA)             E(GCS)           E(FLD)           E(ELS)         previous best solution

Figure 9: Distribution of sparrow’s solution quality ρ across the academic benchmark instances.
    Each dot represents an individual solution from the experiments composing Table 2. The
 expected solution qualities of ROMA - Sato et al. (2019), GCS - Elkeran (2013), FLD - Wang
  et al. (2017) and ELS - Leung et al. (2012) algorithms are shown. A star marks the previous
   singular best-known solution for each instance. JAKOBS1 is omitted since it virtually always
                                   produced the same density.


                                                                 22
     (a) SWIM - 79.83%                    (b) SHIRTS - 90.92%                    (c) MAO - 86.87%




          (d) ALBANO - 89.82%                        (e) SHAPES2 - 86.23%             (f) MARQUES
                                                                                       - 92.02%




                          (g) TROUSERS - 92.62%                                   (h)        (i)
                                                                                JAKOBS1   JAKOBS2
                                                                               - 89.26%   - 87.73%




(j) DAGLI - 90.17%       (k) SHAPES0 - 69.98%           (l) SHAPES1 - 76.73%       (m) FU - 92.41%

Figure 10: The best solutions obtained by sparrow (Table 3) and their respective densities. Bold
                         values indicate improved best-known solutions.




                                                23
                          +0.5%
                               0
                          −0.5%
                          −1.0%                                      SWIM
                                                                     SHIRTS
                          −1.5%
                                                                     TROUSERS
                          −2.0%
                                   0’   10’   20’        30’   40’     50’      60’

Figure 11: Scaling of the expected solution quality E(ρ) of sparrow for the three most challenging
instances across different time limits, normalized for 20 minutes. Each data point is composed of
20 independent runs and no specific tuning was performed to account for the different time limits.


to account for the different time limits. sparrow is able to quickly produce solutions within a
couple of percentage points of the achievable quality after just 20 minutes. Beyond 20 minutes, the
expected solution quality continues to improve, albeit at a diminishing rate.


12. Real-world benchmarks & future research directions

   In Section 11.2, we demonstrated that sparrow is capable of consistently producing high-quality
solutions across the entire set of traditional academic benchmark instances. This set, however, is
dated and contains many instances that were constructed artificially, featuring simple polygonal
shapes with vertices located at integer coordinates. For SWIM, TROUSERS and SHIRTS, arguably
the instances that most reflect real-world conditions, sparrow makes a significant leap forward.
However, these instances are few in number and only represent a single application domain: the
garment industry. We therefore take the opportunity to extend the set of academic benchmarks to
better capture the breadth and intricacies of real-world applications.
   We introduce ten new instances that span a variety of application domains and contain both
homogeneous and heterogeneous sets of items, as well as narrow and wider strips. Two variants are
provided for each instance: one which only allows discrete rotations in 90-degree increments and a
second which allows continuous rotation. The full dataset and experimental results are available in
sparrow’s repository.
   Figure 12 presents this new suite instances for the 2DISPP. Instances GARDEYN0 - 3 have been
derived from Lallier et al. (2022), a large dataset of nesting jobs originating from fashion industry
clients of Lectra4 . Instances GARDEYN4 - 8 are based on shapes from metalworking and shipbuild-
ing applications, provided by AlmaCAM5 . Finally, GARDEYN9 represents a direct-to-film printing
context, contributed by Tetrinest6 .


   4
     https://lectra.com/en
   5
     https://almacam.com/
   6
     https://tetrinest.com/


                                                    24
    (a) GARDEYN0               (b)                        (c) GARDEYN2
                            GARDEYN1




             (d) GARDEYN3                                       (e) GARDEYN4




      (f) GARDEYN5                                    (g) GARDEYN6




           (h) GARDEYN7                          (i) GARDEYN8                  (j) GARDEYN9

Figure 12: Ten new benchmark instances for the 2DISPP. The visualizations are solutions
                               produced by sparrow.




                                          25
   These new instances revealed a serious blind spot in the traditional academic benchmarks.
Highly homogeneous instances – such as GARDEYN4, 5, and 7 – often contain subsets of items that
can be clustered together in a compact way, and repeated many times throughout the strip. While
sparrow can generate these compact patterns at a local scale, it lacks a mechanism to repeat
them and is therefore unable to exploit the inherent ‘structure’ or ‘regularity’ made possible by the
homogeneity of the items. This characteristic is prevalent in real-world applications, but was not
captured by the traditional academic benchmarks.
   Extending sparrow with the ability to exploit this inherent structure/regularity is a promising
direction for future advances, as we are confident vastly superior solutions are attainable, especially
for the aforementioned homogeneous instances.


13. Conclusions and reflections

   This paper introduced a heuristic for the 2D irregular strip packing problem (2DISPP) that
redefines both the academic and open-source state of the art. Our implementation, sparrow, is
publicly available at: https://github.com/JeroenGar/sparrow. The core idea of the algorithm
is to decompose the 2DISPP into a sequence of feasibility problems, where the strip is converted
into a container with fixed dimensions and the items are temporarily allowed to collide with each
other. A local-search algorithm then iteratively moves colliding items around in an attempt to
gradually resolve them all and eventually reach feasibility. Although we focus on the 2DISPP, most
of the heuristic’s components operate on the feasibility problem and can easily be incorporated into
solution strategies for other 2D nesting problems such as bin packing or knapsack problems.
   The main contributions of this work are fourfold: (i) a reproducible and substantial improvement
in solution quality across both academic and open-source contexts, (ii) a highly-optimized and
robust implementation ready for deployment in practice or as a base for future research, (iii) a
number of foundational algorithmic ideas that can be iteratively improved upon or adapted to
other problem variants and (iv) a new set of academic benchmark instances designed to properly
reflect real-world nesting applications and uncover weaknesses in our approach.
   To be frank, the scale of improvements with respect to the previous SotA demonstrated in
the computational experiments (Section 11) should not have been possible on such a well-studied
problem using benchmark instances that are over 25 years old. On the most challenging instance,
SWIM, sparrow’s expected and best solution quality are both ∼5% more compact than the previous
best results. Such a margin of improvement confirms that stagnation with respect to 2DISPP
research was not a result of it already being solved to near optimality.
   Progress in this field has instead been held back for far too long by the issues we outlined in
the introduction: the persistence of high barrier to entry and a severe lack of reproducibility. In
an alternate scenario – where this paper were published without its open-source implementation
– the method we propose would have simply continued that trend and been nearly impossible to
reproduce in practice. Even worse, by raising the performance bar while simultaneously leaving



                                                  26
others unable to meaningfully verify or build upon our work, we could have inadvertently initiated
a new decade of stagnation.
   Reproducibility is a cornerstone of the scientific method. Without it, researchers are left in an
unhealthy and inefficient environment: forced to reinvent the wheel without the means to increment
on prior work or even validate its results. We strongly believe that an academic paper coupled with
a high-quality and open-source implementation delivers value significantly exceeding the sum of its
parts. Thankfully, the ethos we are advocating is not swimming against the current. The field of
Operations Research is undergoing a gradual cultural shift toward open-source practices (Petropou-
los et al., 2024). Vidal (2022), for example, recently published an open-source implementation of
their state-of-the-art algorithm for the capacitated vehicle routing problem. Many of the concerns
we raise here are in fact echoing sentiments already expressed in Vidal (2022).
   We hope this paper and sparrow will serve as catalysts for continued advances in 2D nesting
research as well as deterrents to non-reproducible research practices that have historically hindered
progress.


Acknowledgements

   The authors wish to explicitly thank Luke Connolly (Connolly Editorial) for editorial consul-
tation and Martial Luyts (LStat, KU Leuven) for statistical consultation. They also thank Teo
Mazars, Luc Libralesso, Thomas Piotaix, Corbin Linder, and Léo Gilbert for their contributions
to the creation of the new benchmark instances. This research was supported by the Research
Foundation — Flanders (FWO) under grant numbers 1S71222N and K804824N.


References

Agafonkin, V., 2016. Polylabel: a fast algorithm for finding the pole of inaccessibility of a polygon.
  https://github.com/mapbox/polylabel.

Amaro Junior, B., Pinheiro, P.R., Coelho, P.V., 2017. A parallel biased random-key genetic al-
  gorithm with multiple populations applied to irregular strip packing problems. Mathematical
  problems in engineering 2017, 1670709. doi:10.1155/2017/1670709.

Art Jr, R.C., 1966. An approach to the two dimensional irregular cutting stock problem. Ph.D.
  thesis. Massachusetts Institute of Technology.

Bennell, J.A., Oliveira, J.F., 2008. The geometry of nesting problems: A tutorial. European Journal
  of Operational Research 184, 397–415. doi:10.1016/j.ejor.2006.11.038.

Bennell, J.A., Song, X., 2010. A beam search implementation for the irregular shape packing
  problem. Journal of Heuristics 16, 167–188. doi:10.1007/s10732-008-9095-x.

Bergstra, J., Yamins, D., Cox, D., 2013. Making a science of model search: Hyperparameter
  optimization in hundreds of dimensions for vision architectures, in: Dasgupta, S., McAllester, D.

                                                 27
  (Eds.), Proceedings of the 30th International Conference on Machine Learning, PMLR, Atlanta,
  Georgia, USA. pp. 115–123. URL: https://proceedings.mlr.press/v28/bergstra13.html.

Burke, E., Hellier, R., Kendall, G., Whitwell, G., 2006. A new bottom-left-fill heuristic algorithm
  for the two-dimensional irregular packing problem. Operations Research 54, 587–601. doi:10.
  1287/opre.1060.0293.

Egeblad, J., Nielsen, B.K., Odgaard, A., 2007. Fast neighborhood search for two-and three-
  dimensional nesting problems.     European Journal of Operational Research 183, 1249–1266.
  doi:10.1016/j.ejor.2005.11.063.

Elkeran, A., 2013. A new approach for sheet nesting problem using guided cuckoo search and
  pairwise clustering. European Journal of Operational Research 231, 757–769. doi:10.1016/j.
  ejor.2013.06.020.

Fontan, F., 2023. packingsolver: A solver for (geometrical) packing problems. URL: https:
  //github.com/fontanf/packingsolver.

Fowler, R.J., Paterson, M.S., Tanimoto, S.L., 1981. Optimal packing and covering in the plane are
  NP-complete. Information processing letters 12, 133–137. doi:10.1016/0020-0190(81)90111-3.

Gardeyn, J., Vanden Berghe, G., Wauters, T., 2025. Decoupling geometry from optimization in 2D
  irregular cutting and packing problems: an open-source collision detection engine doi:10.48550/
  arXiv.2508.08341, arXiv:2508.08341.

Glover, F., 1989. Tabu search—part i. ORSA Journal on computing 1, 190–206. doi:10.1287/
  ijoc.1.3.190.

Gomes, A.M., Oliveira, J.F., 2002. A 2-exchange heuristic for nesting problems. European Journal
  of Operational Research 141, 359–370. doi:10.1016/S0377-2217(02)00130-3.

Imamichi, T., Yagiura, M., Nagamochi, H., 2009. An iterated local search algorithm based on
  nonlinear programming for the irregular strip packing problem. Discrete Optimization 6, 345–
  361. doi:10.1016/j.disopt.2009.04.002.

Lallier, C., Vézard, L., Pinaud, B., Blin, G., 2022. Nesting tasks dataset for 2d-nesting efficiency
  estimation. doi:10.5281/zenodo.7030786.

Lastra-Dı́az, J.J., Ortuño, M.T., 2024. Mixed-integer programming models for irregular strip
  packing based on vertical slices and feasibility cuts. European Journal of Operational Research
  313, 69–91. doi:10.1016/j.ejor.2023.08.009.

Leao, A.A., Toledo, F.M., Oliveira, J.F., Carravilla, M.A., Alvarez-Valdés, R., 2020. Irregular
  packing problems: A review of mathematical models. European Journal of Operational Research
  282, 803–822. doi:10.1016/j.ejor.2019.04.045.


                                                 28
Leung, S.C., Lin, Y., Zhang, D., 2012. Extended local search algorithm based on nonlinear program-
  ming for two-dimensional irregular strip packing problem. Computers & Operations Research
  39, 678–686. doi:10.1016/j.cor.2011.05.025.

Loshchilov, I., Schoenauer, M., Sebag, M., 2011. Adaptive coordinate descent, in: Proceedings
  of the 13th annual conference on Genetic and evolutionary computation, pp. 885–892. doi:10.
  1145/2001576.2001697.

Oliveira, J.F., Gomes, A.M., Ferreira, J.S., 2000. Topos–a new constructive algorithm for nesting
  problems. OR-Spektrum 22, 263–284. doi:10.1007/s002910050105.

Petropoulos, F., et al., 2024. Operational research: methods and applications. Journal of the
  Operational Research Society 75, 423–617. doi:10.1080/01605682.2023.2253852.

Sato, A.K., Martins, T.C., Gomes, A.M., Tsuzuki, M.S.G., 2019. Raster penetration map applied
  to the irregular packing problem. European Journal of Operational Research 279, 657–671.
  doi:10.1016/j.ejor.2019.06.008.

Umetani, S., Yagiura, M., Imahori, S., Imamichi, T., Nonobe, K., Ibaraki, T., 2009. Solving the
  irregular strip packing problem via guided local search for overlap minimization. International
  Transactions in Operational Research 16, 661–683. doi:10.1111/j.1475-3995.2009.00707.x.

UNESCO, 2021. Unesco recommendation on open science doi:10.54677/MNMH8546.

Vidal, T., 2022. Hybrid genetic search for the CVRP: Open-source implementation and swap* neigh-
  borhood. Computers & Operations Research 140, 105643. doi:10.1016/j.cor.2021.105643.

Voudouris, C., Tsang, E.P., Alsheddy, A., 2010. Guided local search, in: Handbook of metaheuris-
  tics. Springer, pp. 321–361. doi:10.1007/978-1-4419-1665-5_11.

Wang, Y., Xiao, R., Wang, H., 2017. A flexible labour division approach to the polygon packing
  problem based on space allocation. International journal of production research 55, 3025–3045.
  doi:10.1080/00207543.2016.1229070.




                                               29
