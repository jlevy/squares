# Archived: montanher-2018-rigorous-packing-unit-squares-circle

**Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6394747/
**Archived:** 2026-08-22
**Method:** curl + html2text; original HTML preserved alongside as `montanher-2018-rigorous-packing-unit-squares-circle.html`.

---

Skip to main content 

An official website of the United States government 

Here's how you know

Here's how you know

**Official websites use .gov**   
A **.gov** website belongs to an official government organization in the United States. 

**Secure .gov websites use HTTPS**   
A **lock** (  Lock Locked padlock icon  ) or **https://** means you've safely connected to the .gov website. Share sensitive information only on official, secure websites. 

[ ](https://www.ncbi.nlm.nih.gov/)

Search 

Log in

  * [ Dashboard ](https://www.ncbi.nlm.nih.gov/myncbi/)
  * [ Publications ](https://www.ncbi.nlm.nih.gov/myncbi/collections/bibliography/)
  * [ Account settings ](https://www.ncbi.nlm.nih.gov/account/settings/)
  * Log out 



Search…  Search NCBI 

Primary site navigation 

Search 

Logged in as: ****

  * [ Dashboard ](https://www.ncbi.nlm.nih.gov/myncbi/)
  * [ Publications ](https://www.ncbi.nlm.nih.gov/myncbi/collections/bibliography/)
  * [ Account settings ](https://www.ncbi.nlm.nih.gov/account/settings/)



Log in 

[](/ "Home")

Search PMC Full-Text Archive Search in PMC

  * [ Journal List ](/journals/)
  * [ User Guide ](/about/userguide/)



  *   * [ ](https://doi.org/10.1007/s10898-018-0711-5 "View on publisher site")
  * [ ](pdf/10898_2018_Article_711.pdf "Download PDF")
  *   *   * ## PERMALINK

Copy




As a library, NLM provides access to scientific literature. Inclusion in an NLM database does not imply endorsement of, or agreement with, the contents by NLM or the National Institutes of Health.  
Learn more: [PMC Disclaimer](/about/disclaimer/) | [ PMC Copyright Notice ](/about/copyright/)

J Glob Optim

. 2018 Oct 3;73(3):547–565. doi: [10.1007/s10898-018-0711-5](https://doi.org/10.1007/s10898-018-0711-5)

  * [Search in PMC](https://pmc.ncbi.nlm.nih.gov/search/?term="J%20Glob%20Optim"\[jour\])
  * [Search in PubMed](https://pubmed.ncbi.nlm.nih.gov/?term="J%20Glob%20Optim"\[jour\])
  * [View in NLM Catalog](https://www.ncbi.nlm.nih.gov/nlmcatalog?term="J%20Glob%20Optim"\[Title%20Abbreviation\])
  * [Add to search](?term="J%20Glob%20Optim"\[jour\])



# Rigorous packing of unit squares into a circle

[Tiago Montanher](https://pubmed.ncbi.nlm.nih.gov/?term="Montanher%20T"\[Author\])

### Tiago Montanher

1Wolfgang Pauli Institute, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

2Faculty of Mathematics, University of Vienna, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

Find articles by [Tiago Montanher](https://pubmed.ncbi.nlm.nih.gov/?term="Montanher%20T"\[Author\])

1,2,✉, [Arnold Neumaier](https://pubmed.ncbi.nlm.nih.gov/?term="Neumaier%20A"\[Author\])

### Arnold Neumaier

2Faculty of Mathematics, University of Vienna, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

Find articles by [Arnold Neumaier](https://pubmed.ncbi.nlm.nih.gov/?term="Neumaier%20A"\[Author\])

2, [Mihály Csaba Markót](https://pubmed.ncbi.nlm.nih.gov/?term="Csaba%20Mark%C3%B3t%20M"\[Author\])

### Mihály Csaba Markót

1Wolfgang Pauli Institute, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

2Faculty of Mathematics, University of Vienna, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

Find articles by [Mihály Csaba Markót](https://pubmed.ncbi.nlm.nih.gov/?term="Csaba%20Mark%C3%B3t%20M"\[Author\])

1,2, [Ferenc Domes](https://pubmed.ncbi.nlm.nih.gov/?term="Domes%20F"\[Author\])

### Ferenc Domes

2Faculty of Mathematics, University of Vienna, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

Find articles by [Ferenc Domes](https://pubmed.ncbi.nlm.nih.gov/?term="Domes%20F"\[Author\])

2, [Hermann Schichl](https://pubmed.ncbi.nlm.nih.gov/?term="Schichl%20H"\[Author\])

### Hermann Schichl

2Faculty of Mathematics, University of Vienna, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

Find articles by [Hermann Schichl](https://pubmed.ncbi.nlm.nih.gov/?term="Schichl%20H"\[Author\])

2

  * Author information
  * Article notes
  * Copyright and License information



1Wolfgang Pauli Institute, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

2Faculty of Mathematics, University of Vienna, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

✉

Corresponding author.

Received 2018 Jan 27; Accepted 2018 Sep 25; Issue date 2019.

© The Author(s) 2018

**Open Access** This article is distributed under the terms of the Creative Commons Attribution 4.0 International License (<http://creativecommons.org/licenses/by/4.0>/), which permits unrestricted use, distribution, and reproduction in any medium, provided you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license, and indicate if changes were made.

[PMC Copyright notice](/about/copyright/)

PMCID: PMC6394747 PMID: [30880874](https://pubmed.ncbi.nlm.nih.gov/30880874/)

## Abstract

This paper considers the task of finding the smallest circle into which one can pack a fixed number of non-overlapping unit squares that are free to rotate. Due to the rotation angles, the packing of unit squares into a container is considerably harder to solve than their circle packing counterparts. Therefore, optimal arrangements were so far proved to be optimal only for one or two unit squares. By a computer-assisted method based on interval arithmetic techniques, we solve the case of three squares and find rigorous enclosures for every optimal arrangement of this problem. We model the relation between the squares and the circle as a constraint satisfaction problem (CSP) and found every box that may contain a solution inside a given upper bound of the radius. Due to symmetries in the search domain, general purpose interval methods are far too slow to solve the CSP directly. To overcome this difficulty, we split the problem into a set of subproblems by systematically adding constraints to the center of each square. Our proof requires the solution of 6, 43 and 12 subproblems with 1, 2 and 3 unit squares respectively. In principle, the method proposed in this paper generalizes to any number of squares.

### Electronic supplementary material

The online version of this article (10.1007/s10898-018-0711-5) contains supplementary material, which is available to authorized users.

**Keywords:** Square packing into a circle, Interval branch-and-bound, Tiling constraints, Computer-assisted proof

## Introduction

Let S1,…,Sn be _n_ open unit squares and denote by Cr the closed circle of radius _r_ centered at the origin. This paper deals with the problem of finding the smallest value of _r_ such that one can pack S1,…,Sn into Cr without overlapping. Formally, we can write the problem as

minrs.t.Si⊆Cr1≤i≤nSi∩Sj=∅1≤i,j≤n,i≠j. | 1  
---|---  
  
Packing identical objects into a container is an attractive part of geometrical optimization. The subject drew the attention of a considerable number of researchers, who contributed to problems similar to the one discussed in this paper.

The circle packing is the simplest packing problem in 2 dimensions in the sense that it does not involve the angles of the objects. Markót studied the packing of circles into a square from the interval analysis point of view in a series of papers [15, 16, 24]. In particular, he proved rigorous bounds for n=28,29 and 30 circles. For a survey of the circle packing under the global optimization point of view, see [5]. The website _Packomania_ [22] maintains an updated list of the best-known values for the packing of equal circles into several containers.

Kallrath and Rebennack [12] studied the packing of ellipses into rectangles using state-of-the-art complete global optimization solvers. He succeeded to find the global optimum for the case n=3 without rigor. For the packing of ellipsoids, see [2, 3].

Erdös and Graham [8] inaugurated the packing of unit squares into a square. They show that the wasted area in a container with side length _l_ is O(l711). The proof relies on geometrical arguments and not on rigorous computations. Recent contributions in the packing of unit squares into a square include new bounds for the wasted area [6], the optimality proof for the cases n=5,…,10,13 and 46 [1, 10, 23] and the optimality proof for n-2 and n-1 whenever _n_ is a square [19]. Again, none of these contributions rely on computer-assisted proofs. For a dynamic survey on the packing of unit squares in a square, see [10].

The packing of unit squares into general containers received considerably less attention than the circle or the unit square packing into a square. For example, Friedman [9] maintains a list of proved and best-known values for the packing of unit squares into circles, triangles, L-shapes, and pentagons. In each case, only trivial arrangements are proved optimal. For the subject of interest in this paper, the packing of unit squares into a circle, the first open case is n=3. For a list of figures of squares packed into a circle, see [https://www2.stetson.edu/~efriedma/squincir/](https://www2.stetson.edu/%7eefriedma/squincir/).

### Contribution and outline

This paper introduces a computer-assisted method for finding rigorous enclosures for _r_ in Problem (1) and the corresponding optimal arrangements. The method is of theoretical interest since it proves optimality instead of only presenting a feasible arrangement. Therefore, it is suitable for small values of _n_ only.

Our approach relies on the interval branch-and-bound framework. We implement the algorithm in _C++_ using the forward-backward constraint propagation [21] to reduce the search domain. Section 2 introduces the solver. The code is available at [http://www.mat.univie.ac.at/~montanhe/publications/n3.zip](http://www.mat.univie.ac.at/%7emontanhe/publications/n3.zip).

Section 3 formulates Problem (1) as a constraint satisfaction problem (CSP). This paper uses the concept of sentinels [4, 18] to model non-overlapping conditions and the convexity of the circle to write containment constraints. Given an upper bound r¯n for rn, the CSP asks for every feasible arrangement satisfying r≤r¯n. Our software produces a list of small interval vectors with the property that every optimal arrangement of (1) belongs to at least one element in the list.

General purpose interval solvers are usually not capable of solving packing problems due to symmetries in the search domain. To overcome this difficulty, Sect. 4 shows how to split the original CSP into a set of subproblems by systematically adding constraints to the center of each square. We call them tiling constraints as the idea resembles the one proposed in [15, 16, 24]. The tiling divides the search domain into a set of isosceles triangles that must contain the center of at most one unit square. Then, one can replace the original CSP by a set of Kn subproblems, where _K_ is the number of triangles in the tiling.

Our procedure iterates on the number of squares to avoid the exponential growth of subproblems. At the _i_ -th iteration, we look at every possible combination of _i_ triangles which can accommodate _i_ unit squares into a circle with the radius at most r¯n. The rationale behind this strategy is twofold: (i) It allows us to discard a large number of hard subproblems by proving the infeasibility of more straightforward cases and (ii) It propagates the reduction on the search domain through the iterations. We also show that some combinations of triangles are symmetric by construction. Then one can discard them without any processing. This observation in addition to our iterative method reduces the number of hard cases considerably.

Section 5 illustrates the capabilities of our method. We find a mathematically rigorous enclosure for r3 and the corresponding optimal arrangement. If one set r¯=51716 as pointed by Friedman [9], the tiling produces 36 triangles. Our approach requires the solution of 6 subproblems with one square, 43 with two and only 12 subproblems with 3 squares to conclude the proof. It is <1% of all possible 363=7140 combinations. The method could also be used to find optimal configurations for higher values of _n_ (e.g., n=4,5,6).

### Interval notation

This paper is an application of the interval branch-and-bound framework [11, 13]. We assume that the reader is familiar with concepts from interval analysis [20]. Let a_,a¯∈R with a_≤a¯. Then a=[a_,a¯] denotes the interval with inf(a):=min(a):=a_ and sup(a):=max(a):=a¯. We denote the width of the interval a by wid(a):=a¯-a_.

The set of nonempty compact real intervals is given by

IR:={[a_,a¯]∣a_≤a¯,a_,a¯∈R}.  
---  
  
Let S⊆R be any set. Then the interval hull  of _S_ is the smallest interval containing _S_.

An interval vector (also called box) x:=[x_,x¯] is the Cartesian product of the closed real intervals xi:=[x_i,x¯i]∈IR. We denote the set of all interval vectors of dimension _n_ by IRn. We apply the width operator component wise on vectors. Therefore max(wid(x)):=max(wid(x1),…,wid(xn)). Interval operations and functions are defined as in [13, 20]. The absolute value of the interval a is given by

|a|:=aifinf(a)≥0,[0,max(-inf(a),sup(a))]if0∈a,-aifsup(a)≤0.  
---  
  
Let a and b be two intervals. The maximum of a and b is defined by

max(a,b):=[max(inf(a),inf(b)),max(sup(a),sup(b))].  
---  
  
Let F:Rn→Rm be a function defined on x∈IRn and let f∈IRm. We denote the natural interval extension of the function _F_ by F. A constraint satisfaction problem (CSP) is the task of finding every point satisfying

F(x)∈f,x∈x.  
---  
  
We call x the search domain and the problem is said to be infeasible if there is no x∈x satisfying F(x)∈f. We also denote constraint satisfaction problems by the triplet (F,f,x).

## The algorithm

This section describes the algorithm designed for solving the subproblems of form (1) using interval arithmetic [11, 13, 20] The solver consists of two components, the memory, and the reducer. The former manages the branch-and-bound tree while the latter is responsible for processing the current box. There is also a post-processing step called cluster builder to group close boxes in the solution list.

The memory keeps the list of unprocessed boxes. It is also responsible for the box selector, and to split the boxes coming from the reducer that cannot be discarded or saved as a solution. In this paper, the selector is a depth-first search procedure while the splitter creates two boxes by dividing the input in the midpoint of the coordinate with maximum width.

The reducer contains a list of rigorous methods to reduce or discard boxes. This paper uses the forward-backward constraint propagation [21] and a feasibility verification method [7]. We consider a CSP of form (F,x,f) in the next paragraphs to overview each method.

The forward-backward constraint propagation decomposes F into a set of simple functions (like the exponential function or the sum of several elements) and displays the pieces in a graph. The forward step is a procedure to evaluate F(x) systematically. In this case, the data flow from the decision variable nodes of the graph to the constraint nodes F1,…,Fm. At the end of this step, each constraint node contains an enclosure of Fi(x)∩fi. The backward step acts reversely. It starts from the constraint nodes F(x)∩f and walks the graph applying inverse functions until reaching x1,…,xn. At the end of the backward step, we have a new box x′⊆x with the reduced search domain.

This paper employs the following feasibility verification method. Let x be a box and define the midpoint of x as x∗. Then, we build a small box x∗ around the x∗ and check its feasibility. The box x∗ is a feasible if F(x∗)⊆f. We also save a box x as solution if it satisfies max(wid(x))<ϵx for a given ϵx>0.

The order into which we call the rigorous methods to process x may influence the efficiency of the branch-and-bound procedure. In this paper, the methods follow the finite state machine described in Table 1.

### Table 1.

The finite state machine for the inner loop of the Algorithm 1

Current state | Next state | Condition  
---|---|---  
Forward CP [21] | Exit | Box x is infeasible  
Backward CP | Otherwise  
Backward CP [21] | Forward CP |  GRel(x,x′)>ϵT  
Feasibility verification | Otherwise  
Feasibility verification [7] | Exit | True  
  
[Open in a new tab](table/Tab1/)

The parameter ϵT>0 is the threshold tolerance which controls the relative gain of the box x′⊆x with the help of the following function

GRel(x,x′):=maxi=1,…,n;wid(xi)>0wid(xi′)wid(xi).  
---  
  
It is clear that the input of GRel at each iteration is the box x and the outcome of the rigorous method, x′.

After processing every box in the memory, we run a post-processing step to build clusters of solutions. This method supports the analysis of the solution list since it reduces the number of boxes on it. Given two intervals a and b, we define the gap between a and b by

gap(a,b):=inf(b)-sup(a)ifinf(b)>sup(a),inf(a)-sup(b)ifinf(a)>sup(b),0ifa∩b≠∅.  
---  
  
We save two boxes x,y∈IRn in the same group if

maxi=1,…,ngap(xi,yi)<ϵC  
---  
  
where ϵC is the cluster builder tolerance. After assigning a group to every box in the solution set, we return the interval hull of each group and conclude the procedure.

Algorithm 1 summarizes the interval branch-and-bound method. We implement the algorithm in _C++_ using two interval arithmetic libraries, the _Filib_ [14] and the _Moore_ [17]. The user can choose any of these implementations in the verification of the proof. We report only results from the test with _Filib_ in this paper. The supplementary material also reports the results utilizing _Moore_. They are consistent with each other.[](https://www.ncbi.nlm.nih.gov/core/lw/2.0/html/tileshop_pmc/tileshop_pmc_inline.html?title=Click%20on%20image%20to%20zoom&p=PMC3&id=6394747_10898_2018_711_Figa_HTML.jpg)

## The standard model

This section introduces the mathematical model for the containment and the non-overlapping conditions of (1). We call the resulting model the standard constraint satisfaction problem since it is the same for every subproblem. We assume that the squares have side length _s_. The inequalities for the containment condition follow from the convexity of the circle. On the other hand, non-overlapping constraints rely on the concept of sentinels [4, 18].

### Containment

Let Cr be the closed circle of radius _r_ and centered at the origin. The convexity of the circle implies that c∈Cr for any point _c_ in the segment of line ab¯ if a,b∈Cr. Then, a given square belongs to Cr if and only if its vertices belong to Cr.

Let S0,0 be the open square centered at the origin, with no rotation angle and side length _s_. Then

S0,0:={x∈R2∣max(|x1|,|x2|)-s2<0}.  
---  
  
We denote the closure of a set _S_ by S¯. The set of vertices of S¯0,0 is given by

V0,0:={VNW,VSW,VNE,VSE}  
---  
  
where

VNW:=-s2s2,VSW:=-s2-s2,VNE:=s2s2,VSE:=s2-s2.  
---  
  
For any c∈R2 and θ∈R, we define the displacement operator as

h(c,θ,x):=c+Aθx | 2  
---|---  
  
where Aθ is the rotation matrix

Aθ:=cos(θ)-sin(θ)sin(θ)cos(θ).  
---  
  
The open square centered at c∈R2, with rotation angle θ∈[0,π2) and side length _s_ is the set given by

Sc,θ:={z∈R2∣z=h(c,θ,x),x∈S0,0}. | 3  
---|---  
  
The set of vertices of S¯c,θ, denoted by Vc,θ, is the union of the following points

Vc,θP:=c+AθVP,P∈{NW,SW,NE,SE}.  
---  
  
Finally, we denote the circle of radius _r_ and centered at the origin by Cr. Then

Cr:={x∈R2∣x12+x22≤r2}.  
---  
  
#### Proposition 1

Let gr(x):=x12+x22-r2 and consider the following inequalities

gr(Vc,θP)≤0,P∈{NW,SW,NE,SE} | 4  
---|---  
  
Then

S¯c,θ⊆Cr⇔(4)hold.  
---  
  
#### Proof

If S¯c,θ⊆Cr then Vc,θ⊆Cr and (4) hold. Conversely, since S¯c,θ is a bounded polytope, it is given by the convex hull of the elements of Vc,θ. The result follows from the convexity of the circle. □

### Non-overlapping

This subsection shows that two squares Sc1,θ1 and Sc2,θ2 are non-overlapping if and only a set of nine points defined on Sc1,θ1 do not belong to Sc2,θ2 and vice-versa. We call such sets sentinels of a square. Figure 1 illustrates the need of the sentinels in the non-overlapping formulation.

#### Fig. 1.

[](https://www.ncbi.nlm.nih.gov/core/lw/2.0/html/tileshop_pmc/tileshop_pmc_inline.html?title=Click%20on%20image%20to%20zoom&p=PMC3&id=6394747_10898_2018_711_Fig1_HTML.jpg)

[Open in a new tab](figure/Fig1/)

**a** Non-overlapping squares. **b** Vertex sentinel violation. **c** Mid-point sentinel violation. **d** Center sentinel violation

The set of sentinels of S0,0 is given by

T0,0:=V0,0∪{VN,VS,VE,VW,VO}  
---  
  
where

VN:=0s2,VS:=0-s2,VE:=s20,VW:=-s20,VO:=00.  
---  
  
We denote the set of sentinels of Sc,θ by Tc,θ. This set is given by the union of the following points

Tc,θP:=c+AθVP,P∈{NW,SW,NE,SE,N,S,E,W,O}.  
---  
  
The next theorem states that the non-overlapping condition between two squares reduces to the containment verification of their sets of sentinels. It is a particular case of the sentinels theorem proved in [18].

#### Theorem 1

Let Sci,θi and Scj,θj be two squares defined by (3) and let Tci,θi and Tcj,θj be their corresponding sets of sentinels. Then

Sci,θi∩Scj,θj=∅⇔Sci,θi∩Tcj,θj=∅andScj,θj∩Tci,θi=∅.  
---  
  
In order to check conditions of form Sci,θi∩Tcj,θj=∅ numerically, we need the definition of the inverse of the displacement operator (2)

h-1(c,θ,z):=AθT(z-c).  
---  
  
#### Lemma 1

Let z∈R2 and Sc,θ be a square defined by (3). Then

z∈Sc,θ⇔max(|h1-1(c,θ,z)|,|h2-1(c,θ,z)|)-s2<0.  
---  
  
where h1-1 and h2-1 are the coordinates of the inverse operator.

#### Proof

If z∈Sc,θ then there exists x∈S0,0 such that x=h-1(c,θ,z) and the implication follows immediately. Conversely, let x:=h-1(c,θ,z). The left hand side of the equivalence implies that x∈S0,0. If we let z′:=c+Aθx then z′=c+AθAθT(z-c)=z. Therefore z∈Sc,θ and the result follows. □

Applying the inverse of the displacement operator of the square Sci,θi to the point Tcj,θjP∈Tcj,θj gives

h-1(ci,θi,Tcj,θjP)=AθiT(cj+AθjVP-ci),VP∈T0,0. | 5  
---|---  
  
Let cj,1 and cj,2 be the coordinates of the vector cj. Then the coordinates of (5) are given by

u1(ci,cj,θi,θj,V):=cos(θi)(cj,1-ci,1)-sin(θi)(cj,2-ci,2)+cos(θi-θj)V1+sin(θi-θj)V2  
---  
  
and

u2(ci,cj,θi,θj,V):=sin(θi)(cj,1-ci,1)+cos(θi)(cj,2-ci,2)+-cos(θi-θj)V1+cos(θi-θj)V2.  
---  
  
The following proposition shows that the verification of Sci,θi∩Tcj,θj=∅ reduces to the evaluation of nine non-smooth functions.

#### Proposition 2

Let Sci,θi and Tcj,θj be as in Theorem 1 and define the function

u(ci,cj,θi,θj,VP):=max(|u1(ci,cj,θi,θj,VP)|,|u2(ci,cj,θi,θj,VP)|).  
---  
  
Then

Sci,θi∩Tcj,θj=∅⇔u(ci,cj,θi,θj,VP)-s2≥0for allVP∈T0,0.  
---  
  
#### Proof

Follows from the application of the Lemma 1 to the elements of Tcj,θj. □

### The standard model

We conclude this section with the formal statement of the standard constraint satisfaction problem. Here and throughout we assume, without loss of generality, that the angle of the first square is always 0. This condition follows from the proper rotation of the remaining squares into the circle.

#### Definition 1

[SCSP] Let r¯>0 be an upper bound for the radius of the smallest circle into which one can pack _n_ non-overlapping unit squares and _s_ be a scaling factor. We denote the following problem by standard constraint satisfaction problem (SCSP)

find(r,c1,θ1,…,cn,θn)s.t.u(ci,cj,θi,θj,VP)-s2≥0gr(Vci,θiP)≤0ci,1,ci,2∈[-r,r]θi∈[0,π2]θ1=0r≤r¯ | 6  
---|---  
  
where i,j=1,…,n with i≠j, VP∈T0,0 and Vci,θiP∈Vci,θi. Functions gr and _u_ are given by Propositions 1 and 2 respectively.

## Tiling

General purpose interval branch-and-bound procedures cannot solve the SCSP in a reasonable amount of time even for small values of _n_ due to symmetries in the search space. This section introduces a tiling method to split (6) into a set of subproblems suitable for the Algorithm 1.

We employ the _Matlab_ -like notation g:=a:s:b to denote the array with k:=⌊b-as⌋+1 elements where gi:=a+is for i=0,…,k-1. In addition, we denote the array with the midpoints of _g_ by gc. Then,

gc,i:=gi+gi+12,i=0,…,k-2.  
---  
  
Let r¯>0 be an upper bound for the SCSP. Then, the step length

l:=2r¯⌊2r¯+1⌋ | 7  
---|---  
  
splits [-r¯,r¯] into ⌊2r¯+1⌋ equally divided intervals. Let V:={v∈R∣v=-r¯+il,i∈Z}∩[-r¯,r¯] be the end points of each interval, satisfying vi:=-r¯+il for i=0,…,p:=⌊2r¯+1⌋. Moreover, we write the midpoints of _V_ as Vc where vc,i:=vi+l2 for i=0,…,p-1. Let  and . We denote the elements of  by vi,j:=vivj for vi,vj∈v and 0≤i,j≤p. In the same way, we write the elements of  as ci,j:=vi,j+l2l2 for  and 0≤i,j≤p-1. Algorithm 2 produces the sets  and .[](https://www.ncbi.nlm.nih.gov/core/lw/2.0/html/tileshop_pmc/tileshop_pmc_inline.html?title=Click%20on%20image%20to%20zoom&p=PMC3&id=6394747_10898_2018_711_Figb_HTML.jpg)

Let ▵ABC be the triangle with vertices A,B,C∈R2. Then, we define the following triangles for 0≤i,j≤p-1

▵i,jT:=▵vi,j+1vi+1,j+1ci,j,▵i,jL:=▵vi,j+1vi,jci,j,▵i,jD:=▵vi,jvi+1,jci,j,▵i,jR:=▵vi+1,jvi+1,j+1ci,j.  
---  
  
Here, _T_ ,  _L_ ,  _D_ and _R_ stand for top, left, down and right respectively. Figure 2 shows that the definition aims to split the square with vertices vi,j, vi+1,j, vi+1,j+1 and vi,j+1 into four triangles. One can easily verify that the triangles can be written as

▵i,jT:={x∈R2∣x2-x1≥gj-gi,x2+x1≥gi+gj+1,x1∈[gi,gi+1],x2∈[gj+l2,gj+1]}, | 8  
---|---  
▵i,jL:={x∈R2∣x2-x1≥gj-gi,x2+x1≤gi+gj+1,x1∈[gi,gi+l2],x2∈[gj,gj+1]}, | 9  
---|---  
▵i,jD:={x∈R2∣x2-x1≤gj-gi,x2+x1≤gi+gj+1,x1∈[gi,gi+1],x2∈[gj,gj+l2]}, | 10  
---|---  
▵i,jR:={x∈R2s∣x2-x1≤gj-gi,x2+x1≥gi+gj+1,x1∈[gi+l2,gi+1],x2∈[gj,gj+1]}. | 11  
---|---  
  
### Fig. 2.

[](https://www.ncbi.nlm.nih.gov/core/lw/2.0/html/tileshop_pmc/tileshop_pmc_inline.html?title=Click%20on%20image%20to%20zoom&p=PMC3&id=6394747_10898_2018_711_Fig2_HTML.jpg)

[Open in a new tab](figure/Fig2/)

The geometrical meaning of ▵i,jo for 0≤i,j≤p-1 and o∈{T,L,D,R}

Lemma 2 is a collection of results needed in this section. In particular, Lemma 2-6 shows that the union of triangles ▵i,jo for 0≤i,j≤p-1 and o∈{T,L,D,R} tiles the search domain associated to the center variables in the SCSP.

### Lemma 2

Let  and ▵i,jo be defined as above. Then,

  1. l<1.

  2. x∈v⇒-x∈v.

  3. If  then  where vi,j90:=-vjvi,vi,j180:=-vi-vj,vi,j270:=vj-vi,vi,jx:=vi-vj,vi,jy:=-vivj,vi,jId:=vjvi,vi,j-Id:=-vj-vi.  
---  
  
  4. If  then  where the vectors are defined analogously as above.

  5. ▵i,jo is an isosceles triangle with base length _l_ and legs with length l22 for 0≤i,j≤p-1 and o∈{T,L,D,R}.

  6. [-r¯,r¯]2≡⋃0≤i,j≤po∈{T,L,D,R}▵i,jo.  
---  
  



### Proof

  1. For a>0, we have ⌊a+1⌋=a+1-δ where δ∈[0,1) is the fractional part of a+1. Then 1-δ>0 and ⌊a+1⌋>a. The result follows by taking a=2r¯.

  2. If x∈v then -x=r¯-il for some i∈0,…,p. Let y=-r¯+jl and we need to verify if there exists some j∈0,…,p such that y=-x. The equality holds by taking j=p-i.

  3. If  then  and the result follows from the application of Lemma 2-2 of this proposition to each case.

  4. The proof is similar to the case above.

  5. For ▵i,jT, we have ‖vi,j+1-vi+1,j+1‖=l and ‖vi,j+1-ci,j‖=‖vi+1,j+1-ci,j‖=l22.  
---  
The proof is similar for o∈{L,D,R}.

  6. Let Si,j be the closed square with vertices vi,j, vi+1,j, vi+1,j+1, vi,j+1. Since v0=-r¯ and vp=r¯ it is clear that [-r¯,r¯]2≡⋃0≤i,j≤p-1Si,j.  
---  
The result follows by noting that Si,j≡⋃o∈{T,L,D,R}▵i,jo.  
---  
□




We also assign a label to each triangle in the tiling. It helps us to easily identify a specific triangle during the proof of the case n=3 in Sect. 5. Triangles of form ▵i,jT receive an index that is divisible by 4. In the same way, we assign labels to the left, down and right triangles with the congruence classes 1, 2 and 3 modulo 4, respectively. We denote the triangle with label _i_ by Ti. Figure 3-Left shows the tiling for the best known upper bound of r3.

#### Fig. 3.

[](https://www.ncbi.nlm.nih.gov/core/lw/2.0/html/tileshop_pmc/tileshop_pmc_inline.html?title=Click%20on%20image%20to%20zoom&p=PMC3&id=6394747_10898_2018_711_Fig3_HTML.jpg)

[Open in a new tab](figure/Fig3/)

Left: Tiling for the square [-r¯3,r¯3]2 where r¯3=51716. Right: Tiling for the square [-3,3]2

We show now that each triangle of form ▵i,jo contains the center of at most one unit square.

### Lemma 3

The minimal distance between the centers of two non-overlapping unit squares is 1.

### Proof

Assume the contrary, let _pq_ be a line segment of the centers with lower than 1. Let Cp and Cq the circles of radius 12 drawn into the squares. Then Cp and Cq intersect. But then since the squares are supersets of Cp and Cq, respectively, they also intersect. A contradiction. □

### Proposition 3

Let ▵i,jo for 0≤i,j≤p-1 and o∈{T,L,D,R} be as defined above. If Sc1,θ1 and Sc2,θ2 are two unit squares such that c1,c2∈▵ABC then Sc1,θ1∩Sc2,θ2≠∅.

### Proof

Lemma 2-1 shows that l<1 and Lemma 2-5 gives that the base length of ▵i,jo is _l_ while its legs have length l22. The result follows from Lemma 3. □

Let K:=4p2 be the number of triangles in the tiling. Proposition 3 states that we can split the SCSP into a set of Kn subproblems. In each subproblem, we enforce that the center of each square belongs to a given triangle. For example, one can define the subproblem T0T19T33 in the same tiling displayed in Fig. 3-Left. In this case, we set the standard constraint satisfaction problem defined in (1) and add to the model the linear inequalities given by Eqs. (8)–(11) for ▵0,0T, ▵1,1R and ▵2,2L respectively.

We conclude this subsection by proving that several subproblems can be discarded without any processing due to symmetries in  and . Let f90,f180,f270:R2→R2 be the linear mappings that rotate the vector x∈R2 by an angle of 90, 180 and 270 degrees respectively. In the same way, define the linear mappings fx,fy,fId,f-Id:R2→R2 as the reflections around the lines x=0, y=0, y=x and y=-x respectively.

### Proposition 4

Let ▵i,jo for 0≤i,j≤p-1 and o∈{T,L,D,R} be a triangle of form (8) to (11). Then, fop(▵i,jo) for op∈{90,180,270,r,x,Id,-Id} is a triangle of form ▵i′,j′o′ with 0≤i′,j′≤p-1 and o′∈{T,L,D,R}.

### Proof

The triangle ▵i,jo has two vertices in  and one vertex in . Let _A_ and _B_ be the vertices in  and _C_ be the vertex in . Lemma 2-3 ensures that  while Lemma 2-4 gives that . Since rotations and reflections are rigid transformations, the result holds. □

Proposition 4 allows us to discard subproblems that are symmetric by rotations or reflections. For example, let r¯3=51716 and r3,Sc1,θ1,Sc2,θ2,Sc3,θ3 be a feasible arrangement for (6) with c1∈T7, c2∈T12 and c3∈T22. Then, Proposition 4 ensures that there exists a feasible arrangement r3,Sc1′,θ1′,Sc2′,θ2′,Sc3′,θ3′ satisfying c1′∈T19, c2′∈T12 and c3′∈T22. Moreover, since T19T12T22 is obtained by a reflection around the _y_ axis of T7T12T22, we know that ci′=fy(ci) for i=1,2,3.

The tiling produced by Algorithm 2 suffices if one wants to use a complete global optimization approach for the packing problem. On the other hand, it is not suitable for a rigorous approach since the elements in  and  are floating point vectors subject to rounding errors. To overcome this problem, we introduce a scaled tiling. In this case, we ensure that the points at  and  are integer vectors to the cost of working with squares that are not unit but have the side length contained in a small interval s. Algorithm 3 produces the scaled vertices for the tiling as well as the interval s.[](https://www.ncbi.nlm.nih.gov/core/lw/2.0/html/tileshop_pmc/tileshop_pmc_inline.html?title=Click%20on%20image%20to%20zoom&p=PMC3&id=6394747_10898_2018_711_Figc_HTML.jpg)

The elements in  and  are integer vectors by construction. Then, the Eqs. (8)–(11) are exactly representable. On the other hand, we replace the constant _s_ in the Problem (6) by the interval s to keep the mathematical certainty of our statements. The lemmas and propositions in the last section remain valid after the proper scaling. Figure 3-Right illustrates the scaled tiling for r¯3=5(17)16. Note that the tiling would be the same for r¯4=2 and the only difference between both cases would be the scaling interval s.

Markót and Csendes [24] propose tiling constraints for the circle packing problem based on rectangles. The same idea could be used for the packing of squares into a circle. On the other hand for the case n=3, one would need to split the search domain in 144 squares instead of 36 as proposed in this paper.

## Packing 3 unit squares

Friedman [9] gives an upper bound for the case n=3, r¯3=51716. Algorithm 3 gives the tiling displayed in Fig. 3-Right and the interval scaling factor

s:=[2.328342000348_79,2.328342000348_80]. | 12  
---|---  
  
Figure 4-Left displays an optimal configuration associated to the scaled version of the problem. This section proves the theorem below.

### Fig. 4.

[](https://www.ncbi.nlm.nih.gov/core/lw/2.0/html/tileshop_pmc/tileshop_pmc_inline.html?title=Click%20on%20image%20to%20zoom&p=PMC3&id=6394747_10898_2018_711_Fig4_HTML.jpg)

[Open in a new tab](figure/Fig4/)

Left: An optimal configuration for n=3. Right: Triangles 7, 12 and 22 contain an optimal arrangement

### Theorem 2

Let r3 be the solution of (1) for n=3. Then,

r3∈[1.288470508005_47,1.288470508005_53].  
---  
  
Moreover, the parameters of Sc1,θ1, Sc2,θ2 and Sc3,θ3 belong to the boxes in Table 6.

#### Table 6.

Enclosures of the optimal arrangement for n=3

**Square** |  c1 |  c2 |  θ  
---|---|---|---  
1 |  [-0.68750000000001,-0.68749999999988] |  [-0.00000000000018,0.00000000000023] | [0.0, 0.0]  
2 | [0.31249999999993, 0.31250000000014] |  [-0.50000000000007,-0.49999999999989] | [1.57079632679426, 1.57079632679491]  
3 | [0.31249999999993, 0.31250000000011] | [0.49999999999992, 0.50000000000007] |  [-0.00000000000001,0.00000000000050]  
1 |  [-0.68750000000001,-0.68749999999988] |  [-0.00000000000021,0.00000000000012] | [0.0, 0.0]  
2 | [0.31249999999998, 0.31250000000019] |  [-0.50000000000003,-0.49999999999990] |  [-0.00000000000001,0.00000000000036]  
3 | [0.31249999999993, 0.31250000000009] | [0.49999999999995, 0.50000000000007] |  [-0.00000000000001,0.00000000000029]  
1 |  [-0.68750000000001,-0.68749999999991] |  [-0.00000000000012,0.00000000000016] | [0.0, 0.0]  
2 | [0.31249999999993, 0.31250000000011] |  [-0.50000000000007,-0.49999999999993] | [1.57079632679463, 1.57079632679491]  
3 | [0.31249999999998, 0.31250000000014] | [0.49999999999993, 0.50000000000004] | [1.57079632679453, 1.57079632679491]  
1 |  [-0.68750000000001,-0.68749999999992] |  [-0.00000000000014,0.00000000000014] | [0.0, 0.0]  
2 | [0.31249999999998, 0.31250000000011] |  [-0.50000000000003,-0.49999999999995] |  [-0.00000000000001,0.00000000000027]  
3 | [0.31249999999998, 0.31250000000011] | [0.49999999999995, 0.50000000000004] | [1.57079632679463, 1.57079632679491]  
  
[Open in a new tab](table/Tab6/)

There are 4 clusters, each of them separated by a blank line. The first coordinate of the center of the _i_ -th square is given by c1 and the second coordinate by c2. The rotation angle is given by θ

### Proof

We perform the computational part of the proof in a _core i7_ processor with a frequency of 2.6 GHz, 6 GB of RAM and _Windows 10_. We compiled the code using the _g++ 7.3_ compiler with the option -O3. A supplementary material for the proof, containing the statistics and the log files for each subproblem is available in [http://www.mat.univie.ac.at/~montanhe/publications/n3.zip](http://www.mat.univie.ac.at/%7emontanhe/publications/n3.zip)

We prove the theorem in three phases. At the _i_ -th iteration, we consider instances of form (6) and define subproblems by adding tiling constraints of form (8)–(11) accordingly.

The proof considers the scaled version of the problem to ensure the mathematical certainty of our statements. Therefore, the CSPs in this section are of form (6) with the constant _s_ replaced by the interval s in Eq. (12). We obtain the unscaled interval for r3 and Table 6 by dividing every box found in the last iteration by s.

We also assume the labeling scheme for the triangles introduced in Sect. 4 and displayed on Fig. 3-Right. Therefore, the subproblem T7T12T22 refers to the SCSP with the interval scaling factor s and such that c1∈T7:=▵0,1R, c2∈T12:=▵1,0T and c3∈T22:=▵1,2D.

**Phase 1** In this iteration, we are interested in reducing the search domain of each subproblem and finding triangles which can contain the center of squares with no rotation. The tiling has 36 triangles, but the symmetries in  and  reduce the number of subproblems to 6. Table 2 shows the instances discarded without any processing in the first phase.

#### Table 2.

Instances discarded in the first phase without processing

Instance | Symm. to | Symm. type | Instance | Symm. to | Symm. type  
---|---|---|---|---|---  
T2 |  T1 | Ref. y=x |  T21 |  T6 | Rot. 90∘  
T3 |  T0 | Ref. y=x |  T22 |  T12 | Rot. 180∘  
T6 |  T4 | Ref. x=0 |  T23 |  T6 | Ref. y=-x  
T8 |  T2 | Ref. x=0 |  T24 |  T3 | Rot. 270∘  
T9 |  T2 | Rot. 90∘ |  T25 |  T3 | Ref. y=0  
T10 |  T3 | Rot. 90∘ |  T26 |  T2 | Ref. y=0  
T11 |  T3 | Ref. x=0 |  T27 |  T2 | Rot. 270∘  
T12 |  T7 | Rot. 270∘ |  T28 |  T6 | Rot. 180∘  
T13 |  T6 | Ref. y=x |  T29 |  T12 | Rot. 270∘  
T14 |  T5 | Rot. 270∘ |  T30 |  T6 | Ref. y=0  
T15 |  T6 | Rot. 270∘ |  T31 |  T14 | Rot. 270∘  
T17 |  T16 | Rot. 270∘ |  T32 |  T2 | Rot. 180∘  
T18 |  T17 | Rot. 270∘ |  T33 |  T3 | Rot. 180∘  
T19 |  T17 | Rot. 180∘ |  T34 |  T3 | Ref. y=-x  
T20 |  T14 | Rot. 180∘ |  T35 |  T2 | Ref. y=-x  
  
[Open in a new tab](table/Tab2/)

Symm. to stands for symmetric to. Symm. type shows the operation needed to obtain Instance from the element in the second column

Instances T0, T1, T4, T5, T7 and T16 require processing. We run the Algorithm 1 with ϵT=10-1, ϵC=10-11, ϵx=10-13 and time limit of 300 s. In this phase, we remove the condition θ1=0 in Problem (6). Table 3 summarizes the results of the processed instances on phase 1. It shows that T1 and T5 are infeasible and any combination containing one of these triangles or their symmetric counterparts could be removed in the next phases. Moreover, it shows that only triangles T7 and T16 can contain the center of a square with rotation angle 0. Since we are assuming that θ1=0 in the optimal configuration for n=3, we only have to check the combinations containing at least one of these triangles.

#### Table 3.

Statistics for the processed instances on phase 1

Instance | Status | Time(s) | Steps |  θ  
---|---|---|---|---  
T0 | Timeout | 300 | 428253 | [0.38528, 1.21015]  
T1 | Infeasible | 1 | 1 | -  
T4 | Timeout | 300 | 421457 | [0.33751, 1.51529]  
T5 | Infeasible | 1 | 1 | -  
T7 | Timeout | 300 | 398689 | [0, 1.5708]  
T16 | Timeout | 300 | 336345 | [0, 1.5708]  
  
[Open in a new tab](table/Tab3/)

Status gives the termination status of the instance. Time(s) gives the processing time in seconds. Column steps displays the number of calls of the state machine described in Table 1. Column θ is a rigorous enclosure for the rotation angle

**Phase 2** This phase aims to discard as many instances as possible to reduce the number of hard subproblems in the last iteration. There are 630 possible combinations of 36 triangles taken 2 by 2. After eliminating symmetric and previously discarded cases, we obtain 43 instances. We also propagate any reduction in the search domain in the first phase to the subproblems in the second phase. Again, we remove the condition θ1=0 from Problem (6).

We run the Algorithm 1 with ϵT=10-1, ϵC=10-11, ϵx=10-13 and time limit of 3600 s. We stop the algorithm as soon as the feasibility verification method described in Sect. 2 succeeds in finding a feasible point. The supplementary material contains the list of all instances discarded without processing. Table 4 gives the statistics for the 43 processed instances.

#### Table 4.

Statistics for the processed instances on phase 2

Instance | Status | Time(s) | Steps | Instance | Status | Time(s) | Steps  
---|---|---|---|---|---|---|---  
T7T17 | Infeasible | 1 | 17697 |  T0T28 | Feasible | 1 | 1  
T7T19 | Feasible | 1 | 1 |  T0T29 | Feasible | 1 | 1  
T7T29 | Feasible | 1 | 1 |  T0T30 | Infeasible | 1 | 11395  
T16T17 | Feasible | 1 | 3 |  T0T33 | Feasible | 1 | 1  
T16T18 | Feasible | 1 | 2 |  T0T34 | Feasible | 1 | 1  
T0T3 | Infeasible | 1 | 81 |  T4T6 | Infeasible | 2 | 1603  
T0T4 | Infeasible | 2 | 1211 |  T4T7 | Infeasible | 1 | 2657  
T0T6 | Infeasible | 2 | 233 |  T4T12 | Feasible | 1 | 1  
T0T7 | Infeasible | 2 | 2219 |  T4T13 | Infeasible | 1 | 13771  
T0T10 | Infeasible | 1 | 861 |  T4T15 | Feasible | 1 | 1  
T0T11 | Infeasible | 2 | 1059 |  T4T16 | Infeasible | 1 | 24983  
T0T12 | Infeasible | 1 | 2527 |  T4T17 | Infeasible | 1 | 4923  
T0T13 | Infeasible | 1 | 243 |  T4T18 | Feasible | 1 | 1  
T0T15 | Infeasible | 2 | 1535 |  T4T19 | Feasible | 1 | 1  
T0T16 | Feasible | 1 | 1 |  T4T21 | Infeasible | 1 | 705  
T0T17 | Infeasible | 1 | 3397 |  T4T22 | Infeasible | 2 | 19323  
T0T18 | Infeasible | 1 | 3889 |  T4T28 | Feasible | 1 | 1  
T0T19 | Feasible | 1 | 1 |  T4T29 | Feasible | 1 | 1  
T0T21 | Infeasible | 1 | 8021 |  T4T30 | Feasible | 1 | 1  
T0T22 | Feasible | 1 | 1 |  T7T12 | Feasible | 1 | 1  
T0T23 | Feasible | 1 | 1 |  T7T16 | Feasible | 1 | 1  
T0T24 | Infeasible | 2 | 1227 |  |  |  |   
  
[Open in a new tab](table/Tab4/)

Status gives the termination status of the instance. Time(s) gives the processing time in seconds. Column steps displays the number of calls of the state machine described in Table 1

We conclude the second phase with 22 infeasible subproblems. Again, any case in the next phase containing a combination found infeasible in this step can be discarded without any processing.

**Phase 3** In this phase we set the full model in Problem (6), including the constraint θ1=0. Table 3 shows that c1∈T7 or c1∈T16. Therefore, after removing the cases where one of these conditions do not hold and eliminating symmetric and already proved infeasible subproblems, we obtain 12 instances of the 7140 possible ones.

If an instance contains both triangles T7 and T16, we denote by T7∗T16Tx the case where we enforce the angle of the square centered in T7 to be zero. In the same way, we write T7T16∗Tx for the instances where the square centered in T16 has no rotation angle.

For the last phase, we run Algorithm 1 with ϵT=10-1, ϵC=10-11, ϵx=10-13 and no time limit. Table 5 provides the statistics of the processed instances. Moreover, Table 5 shows that it is the only instance containing the optimal configurations for n=3. Figure 4-Right shows an approximation of the center of each square in the optimal case.

#### Table 5.

Statistics for the processed instances on phase 3

Instance | Status | Time(s) | Steps  
---|---|---|---  
T7∗T12T16 | Infeasible | 33 | 146629  
T7T12T16∗ | Infeasible | 134 | 440307  
T7T12T22 | Clusters found | 628 | 2183739  
T7∗T16T18 | Infeasible | 3 | 16901  
T7T16∗T18 | Infeasible | 3 | 18273  
T7∗T16T19 | Infeasible | 4 | 19729  
T7T16∗T19 | Infeasible | 1 | 5491  
T7∗T16T29 | Infeasible | 8 | 40345  
T7T16∗T29 | Infeasible | 2 | 11071  
T16T17T18 | Infeasible | 2 | 7319  
T0T16T19 | Infeasible | 0 | 2833  
T0T16T29 | Infeasible | 2 | 9317  
  
[Open in a new tab](table/Tab5/)

Status gives the termination status of the instance. Time(s) gives the processing time in seconds. Column steps displays the number of calls of the state machine described in Table 1

Algorithm 1 produces 4 clusters for the instance T7T12T22. The maximum width of a cluster is 6.23∗10-13. The precision is smaller than ϵx due to the cluster builder procedure described in Sect. 2. Table 6 gives the unscaled clusters.□

## Conclusion

This paper presents a framework for the rigorous optimization of the packing of unit squares into a circle. We express the question as the standard constraint satisfaction problem stated by Definition 1. The model considers the concept of sentinels to formulate non-overlapping constraints and the convexity of the squares and the circle to describe containment conditions.

General purpose rigorous optimization solvers cannot achieve the solution of the standard constraint satisfaction problem due to symmetries in the search domain. To overcome this difficulty, we propose a tiling method that splits the search space related to the center of each unit square into isosceles triangles. Our tiling divides the original problem into a set of subproblems that are suitable for the interval branch-and-bound approach. We also ensure that the parameters in each subproblem are free of rounding errors by introducing a proper scaling of the search domain.

To show the capabilities of our approach, we solve the first open case reported in the literature, n=3. We implement the interval branch-and-bound in the _C++_ and the code is publicly available. We perform the proof on an ordinary laptop with 6 GB of RAM and a core _i7_ processor.

The proof of the case n=3 requires the solution of 6 subproblems with one square, 43 with two and only 12 with three squares. We discard most subproblems without processing due to symmetries in the tiling. Among the 61 subproblems, just 6 require more than 100 s to conclude the search. At the end of the process, we obtained 4 boxes with the following properties

  1. The maximum width of any coordinate of the resulting boxes is 6.23∗10-13.

  2. If one disregard symmetries, every solution of (1) is contained in at least one of the 4 boxes




The method proposed in this paper could, in principle, be used to find the optimal arrangement for higher values of _n_ (e.g., n=4,5,6.).

## Electronic supplementary material

Below is the link to the electronic supplementary material. 

[Supplementary material 1 (zip 65514 KB)](/articles/instance/6394747/bin/10898_2018_711_MOESM1_ESM.zip) (64MB, zip) 

## Acknowledgements

Open access funding provided by Austrian Science Fund (FWF).

## Footnotes

This research was supported through the research Grants P25648-N25 and P27891 of the Austrian Science Fund (FWF).

## Contributor Information

Tiago Montanher, Email: tiago.de.morais.montanher@univie.ac.at.

Arnold Neumaier, Email: Arnold.Neumaier@univie.ac.at.

Mihály Csaba Markót, Email: mihaly.markot@univie.ac.at.

Ferenc Domes, Email: ferenc.domes@univie.ac.at.

Hermann Schichl, Email: hermann.schichl@univie.ac.at.

## References

  * 1.Bentz W. Optimal packings of 13 and 46 unit squares in a square. Electron. J. Comb. 2010;17(1):R126. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Electron.%20J.%20Comb.&title=Optimal%20packings%20of%2013%20and%2046%20unit%20squares%20in%20a%20square&author=W%20Bentz&volume=17&issue=1&publication_year=2010&pages=R126&)]
  * 2.Birgin EG, Lobato RD, Martínez JM. Packing ellipsoids by nonlinear optimization. J. Glob. Optim. 2016;65(4):709–743. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Glob.%20Optim.&title=Packing%20ellipsoids%20by%20nonlinear%20optimization&author=EG%20Birgin&author=RD%20Lobato&author=JM%20Mart%C3%ADnez&volume=65&issue=4&publication_year=2016&pages=709-743&)]
  * 3.Birgin EG, Lobato RD, Martínez JM. A nonlinear programming model with implicit variables for packing ellipsoids. J. Glob. Optim. 2017;68(3):467–499. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Glob.%20Optim.&title=A%20nonlinear%20programming%20model%20with%20implicit%20variables%20for%20packing%20ellipsoids&author=EG%20Birgin&author=RD%20Lobato&author=JM%20Mart%C3%ADnez&volume=68&issue=3&publication_year=2017&pages=467-499&)]
  * 4.Birgin EG, Martínez JM, Mascarenhas WF, Ronconi DP. Method of sentinels for packing items within arbitrary convex regions. J. Oper. Res. Soc. 2006;57(6):735–746. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Oper.%20Res.%20Soc.&title=Method%20of%20sentinels%20for%20packing%20items%20within%20arbitrary%20convex%20regions&author=EG%20Birgin&author=JM%20Mart%C3%ADnez&author=WF%20Mascarenhas&author=DP%20Ronconi&volume=57&issue=6&publication_year=2006&pages=735-746&)]
  * 5.Castillo I, Kampas FJ, Pintér JD. Solving circle packing problems by global optimization: Numerical results and industrial applications. Eur. J. Oper. Res. 2008;191(3):786–802. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Eur.%20J.%20Oper.%20Res.&title=Solving%20circle%20packing%20problems%20by%20global%20optimization:%20Numerical%20results%20and%20industrial%20applications&author=I%20Castillo&author=FJ%20Kampas&author=JD%20Pint%C3%A9r&volume=191&issue=3&publication_year=2008&pages=786-802&)]
  * 6.Chung F, Graham RL. Packing equal squares into a large square. J. Comb. Theory Ser. A. 2009;116:1167–1175. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Comb.%20Theory%20Ser.%20A&title=Packing%20equal%20squares%20into%20a%20large%20square&author=F%20Chung&author=RL%20Graham&volume=116&publication_year=2009&pages=1167-1175&)]
  * 7.Domes F, Neumaier A. Rigorous verification of feasibility. J. Glob. Optim. 2015;61:255–278. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Glob.%20Optim.&title=Rigorous%20verification%20of%20feasibility&author=F%20Domes&author=A%20Neumaier&volume=61&publication_year=2015&pages=255-278&)]
  * 8.Erdös P, Graham RL. On packing squares with equal squares. J. Comb. Theory (A) 1975;19(1):9–123. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Comb.%20Theory%20\(A\)&title=On%20packing%20squares%20with%20equal%20squares&author=P%20Erd%C3%B6s&author=RL%20Graham&volume=19&issue=1&publication_year=1975&pages=9-123&)]
  * 9.Friedman, E.: Erich packing center. [http://www2.stetson.edu/~efriedma/packing.html](http://www2.stetson.edu/%7eefriedma/packing.html). Accessed 4 Dec 2017
  * 10.Friedman, E.: Packing unit squares in squares: a survey and new results. Electron. J. Comb. (2009)
  * 11.Hansen ER. Global Optimization Using Interval Analysis. New York: Marcel Dekker Inc.; 1992.  [[Google Scholar](https://scholar.google.com/scholar_lookup?title=Global%20Optimization%20Using%20Interval%20Analysis&author=ER%20Hansen&publication_year=1992&)]
  * 12.Kallrath J, Rebennack S. Cutting ellipses from area-minimizing rectangles. J. Glob. Optim. 2014;59(2):405–437. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Glob.%20Optim.&title=Cutting%20ellipses%20from%20area-minimizing%20rectangles&author=J%20Kallrath&author=S%20Rebennack&volume=59&issue=2&publication_year=2014&pages=405-437&)]
  * 13.Kearfott RB. Rigorous Global Search: Continuous Problems. Norwell: Kluwer Academic Publishers; 1996.  [[Google Scholar](https://scholar.google.com/scholar_lookup?title=Rigorous%20Global%20Search:%20Continuous%20Problems&author=RB%20Kearfott&publication_year=1996&)]
  * 14.Lerch M, Tischler G, Gudenberg JWV, Hofschuster W, Krämer W. Filib++, a fast interval library supporting containment computations. ACM Trans. Math. Softw. 2006;32(2):299–324. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=ACM%20Trans.%20Math.%20Softw.&title=Filib++,%20a%20fast%20interval%20library%20supporting%20containment%20computations&author=M%20Lerch&author=G%20Tischler&author=JWV%20Gudenberg&author=W%20Hofschuster&author=W%20Kr%C3%A4mer&volume=32&issue=2&publication_year=2006&pages=299-324&)]
  * 15.Markót MC. Interval methods for verifying structural optimality of circle packing configurations in the unit square. J. Comput. Appl. Math. 2007;199(2):353–357. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Comput.%20Appl.%20Math.&title=Interval%20methods%20for%20verifying%20structural%20optimality%20of%20circle%20packing%20configurations%20in%20the%20unit%20square&author=MC%20Mark%C3%B3t&volume=199&issue=2&publication_year=2007&pages=353-357&)]
  * 16.Markót MC, Csendes T. A new verified optimization technique for the “packing circles in a unit square” problems. SIAM J. Optim. 2005;16:193–219. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=SIAM%20J.%20Optim.&title=A%20new%20verified%20optimization%20technique%20for%20the%20%E2%80%9Cpacking%20circles%20in%20a%20unit%20square%E2%80%9D%20problems&author=MC%20Mark%C3%B3t&author=T%20Csendes&volume=16&publication_year=2005&pages=193-219&)]
  * 17.Mascarenhas WF. Moore: interval arithmetic in C++20. In: Barreto GA, Coelho R, editors. Fuzzy Information Processing. Cham: Springer; 2018. pp. 519–529. [[Google Scholar](https://scholar.google.com/scholar_lookup?title=Fuzzy%20Information%20Processing&author=WF%20Mascarenhas&publication_year=2018&)]
  * 18.Mascarenhas WF, Birgin EG. Using sentinels to detect intersections of convex and nonconvex polygons. Comput. Appl. Math. 2010;29(2):247–267. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Comput.%20Appl.%20Math.&title=Using%20sentinels%20to%20detect%20intersections%20of%20convex%20and%20nonconvex%20polygons&author=WF%20Mascarenhas&author=EG%20Birgin&volume=29&issue=2&publication_year=2010&pages=247-267&)]
  * 19.Nagamochi H. Packing unit squares in a rectangle. Electron. J. Comb. 2005;12(1):R37. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Electron.%20J.%20Comb.&title=Packing%20unit%20squares%20in%20a%20rectangle&author=H%20Nagamochi&volume=12&issue=1&publication_year=2005&pages=R37&)]
  * 20.Neumaier A. Interval Methods for Systems of Equations. Cambridge: Cambridge University Press; 1990.  [[Google Scholar](https://scholar.google.com/scholar_lookup?title=Interval%20Methods%20for%20Systems%20of%20Equations&author=A%20Neumaier&publication_year=1990&)]
  * 21.Schichl H, Neumaier A. Interval analysis on directed acyclic graphs for global optimization. J. Glob. Optim. 2005;33(4):541–562. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=J.%20Glob.%20Optim.&title=Interval%20analysis%20on%20directed%20acyclic%20graphs%20for%20global%20optimization&author=H%20Schichl&author=A%20Neumaier&volume=33&issue=4&publication_year=2005&pages=541-562&)]
  * 22.Specht, E.: Packomania. <http://www.packomania.com/>. Accessed 4 Dec 2017
  * 23.Stromquist W. Packing 10 or 11 unit squares in a square. Electron. J. Comb. 2003;10(8):1–11. [[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Electron.%20J.%20Comb.&title=Packing%2010%20or%2011%20unit%20squares%20in%20a%20square&author=W%20Stromquist&volume=10&issue=8&publication_year=2003&pages=1-11&)]
  * 24.Szabó PG, Markót MC, Csendes T, Specht E, Casado LG, García I. New Approaches to Circle Packing in a Square—With Program Codes. Berlin: Springer; 2008.  [[Google Scholar](https://scholar.google.com/scholar_lookup?title=New%20Approaches%20to%20Circle%20Packing%20in%20a%20Square%E2%80%94With%20Program%20Codes&author=PG%20Szab%C3%B3&author=MC%20Mark%C3%B3t&author=T%20Csendes&author=E%20Specht&author=LG%20Casado&publication_year=2008&)]



## Associated Data

_This section collects any data citations, data availability statements, or supplementary materials included in this article._

### Supplementary Materials

[Supplementary material 1 (zip 65514 KB)](/articles/instance/6394747/bin/10898_2018_711_MOESM1_ESM.zip) (64MB, zip) 

* * *

Articles from Journal of Global Optimization are provided here courtesy of **Springer**

## ACTIONS

  * [ View on publisher site ](https://doi.org/10.1007/s10898-018-0711-5)
  * [ PDF (696.7 KB) ](pdf/10898_2018_Article_711.pdf)
  * Cite
  * Collections
  * Permalink

## PERMALINK

Copy




## RESOURCES

###  Similar articles 

###  Cited by other articles 

###  Links to NCBI Databases 

## Cite

  * Copy
  * Download .nbib .nbib
  * Format: AMA  APA  MLA  NLM 




## Add to Collections

Create a new collection

Add to an existing collection

Name your collection *

Choose a collection 

Unable to load your collection due to an error  
Please try again

Add  Cancel 

Follow NCBI 

[ NCBI on X (formerly known as Twitter) ](https://twitter.com/ncbi) [ NCBI on Facebook ](https://www.facebook.com/ncbi.nlm) [ NCBI on LinkedIn ](https://www.linkedin.com/company/ncbinlm) [ NCBI on GitHub ](https://github.com/ncbi) [ NCBI RSS feed ](https://ncbiinsights.ncbi.nlm.nih.gov/)

Connect with NLM 

[ NLM on X (formerly known as Twitter) ](https://twitter.com/nlm_nih) [ NLM on Facebook ](https://www.facebook.com/nationallibraryofmedicine) [ NLM on YouTube ](https://www.youtube.com/user/NLMNIH)

[National Library of Medicine   
8600 Rockville Pike  
Bethesda, MD 20894](https://www.google.com/maps/place/8600+Rockville+Pike,+Bethesda,+MD+20894/%4038.9959508,
            -77.101021,17z/data%3D!3m1!4b1!4m5!3m4!1s0x89b7c95e25765ddb%3A0x19156f88b27635b8!8m2!3d38.9959508!
            4d-77.0988323)

  * [ Web Policies ](https://www.nlm.nih.gov/web_policies.html)
  * [ FOIA ](https://www.nih.gov/institutes-nih/nih-office-director/office-communications-public-liaison/freedom-information-act-office)
  * [ HHS Vulnerability Disclosure ](https://www.hhs.gov/vulnerability-disclosure-policy/index.html)


  * [ Help ](https://support.nlm.nih.gov/)
  * [ Accessibility ](https://www.nlm.nih.gov/accessibility.html)
  * [ Careers ](https://www.nlm.nih.gov/careers/careers.html)



  * [ NLM ](https://www.nlm.nih.gov/)
  * [ NIH ](https://www.nih.gov/)
  * [ HHS ](https://www.hhs.gov/)
  * [ USA.gov ](https://www.usa.gov/)



Back to Top
  *[*]: required
