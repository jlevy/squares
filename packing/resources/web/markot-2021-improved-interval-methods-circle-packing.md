# Improved interval methods for solving circle packing problems in the unit square

**Authors:** Mihály Csaba Markót
**Venue:** Journal of Global Optimization 81 (2021)
**Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8550790/
**Archived:** 2026-08-22
**Extraction:** text extracted from the PMC HTML capture alongside as
`markot-2021-improved-interval-methods-circle-packing.html`.

---

Improved interval methods for solving circle packing problems in the unit square - PMC

 Skip to main content

 Official websites use .gov

 A
 .gov website belongs to an official
 government organization in the United States.

 Secure .gov websites use HTTPS

 A lock (

 Lock
 
 Locked padlock icon

) or https:// means you've safely
 connected to the .gov website. Share sensitive
 information only on official, secure websites.

Search PMC Full-Text Archive

Search in PMC

 Journal List

 User Guide

 PERMALINK

 Copy

 As a library, NLM provides access to scientific literature. Inclusion in an NLM database does not imply endorsement of, or agreement with,
 the contents by NLM or the National Institutes of Health.

 Learn more:
 PMC Disclaimer
 |
 
 PMC Copyright Notice

J Glob Optim
. 2021 Sep 29;81(3):773–803. doi: 10.1007/s10898-021-01086-z

Improved interval methods for solving circle packing problems in the unit square

Mihály Csaba Markót
Mihály Csaba Markót

1Faculty of Mathematics, Wolfgang Pauli Institute, University of Vienna, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

Find articles by Mihály Csaba Markót

1,✉

Author information

Article notes

Copyright and License information

1Faculty of Mathematics, Wolfgang Pauli Institute, University of Vienna, Oskar-Morgenstern-Platz 1, 1090 Vienna, Austria 

✉Corresponding author.

Received 2019 Sep 3; Accepted 2021 Aug 19; Issue date 2021.

© The Author(s) 2021, corrected publication 2022

Open AccessThis article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.

PMC Copyright notice

PMCID: PMC8550790  PMID: 34720422

Abstract

In this work computer-assisted optimality proofs are given for the problems of finding the densest packings of 31, 32, and 33 non-overlapping equal circles in a square. In a study of 2005, a fully interval arithmetic based global optimization method was introduced for the problem class, solving the cases 28, 29, 30. Until now, these were the largest problem instances solved on a computer. Using the techniques of that paper, the estimated solution time for the next three cases would have been 3–6 CPU months. In the present paper this former method is improved in both its local and global search phases. We discuss a new interval-based polygon representation of the core local method for eliminating suboptimal regions, which has a simpler implementation, easier proof of correctness, and faster behaviour than the former one. Furthermore, a modified strategy is presented for the global phase of the search, including improved symmetry filtering and tile pattern matching. With the new method the cases n=31,32,33 have been solved in 26, 61, and 13 CPU hours, giving high precision enclosures for all global optimizers and the optimum value. After eliminating the hardware and compiler improvements since the former study, the new proof technique became roughly about 40–100 times faster than the previous one. In addition, the new implementation is suitable for solving the next few circle packing instances with similar computational effort.

Keywords: Interval arithmetic, Global optimization, Branch and bound, Circle packing, Optimality proof
Introduction

In this paper we are dealing with optimal (densest) packings of equal circles in a unit square. During the last decades this problem class attracted the attention of many mathematicians and computer scientists. Although the problem has a very simple mathematical formulation, in many cases it is very challenging to find and prove the optimality of a packing configuration. Actually for n≥28 a whole ‘cookbook’ of various mathematical and numerical techniques is required to tackle the problems.

The paper is organized as follows. In Sect. 2 we review some possible problem models and the history of solving instances of the problem class. In Sects. 3 and 4 we briefly introduce the basics of interval arithmetic calculations and the interval branch–and–bound framework used in this study. In Sect. 5 we discuss the key local elimination procedure that uses a new, mathematically rigorous computer representation of convex polygons. In Sect. 6 we introduce techniques to speed up the global search phase of the optimality proofs. In Sect. 7 we detail the solution process for the problem instances n=31,32,33. In Sect. 8 we summarize the main achievements of the paper.
Problem statement and history

The informal description of the considered circle packing problem is the following: place a given number n of equal circles without overlapping into a unit square, maximizing the diameter of the circles. This problem is known (see, e.g. [1]) to be equivalent to the following point packing problem: place a given number n of points into the unit square, maximizing the minimal distance between the pairs of points. That is, there is a bijective mapping (based on simple geometric transformations) between the set of optimal solutions of the problems of packing n circles and n points. Therefore we consider the simpler point packing problem:

maximizemin1≤i<j≤n(xi-xj)2+(yi-yj)2,s.t.0≤xi,yi≤1,i=1,2,⋯,n,
1

where the unit square is [0,1]2, and the ith point is located at (xi,yi). The integer n≥2 is a parameter of the problem class, thus, one can refer to a particular point packing problem instance by specifying n.

Since the square root function is strictly monotone, in practice we solve the problem of maximizing

fn:R2n→R,fn(x,y)=min1≤i<j≤n(xi-xj)2+(yi-yj)2,s.t.0≤xi,yi≤1,i=1,2,⋯,n,
2

saving the evaluation of the square root. In the sequel we will use the shorthand notation sij=(xi-xj)2+(yi-yj)2 for the squared distance between the ith and jth point.

Up to now, only the optimal packings of 2,⋯,9,14,16,25, and 36 circles have been proved in a theoretical way. On the other hand, computer-assisted optimality proofs exist for n≤20 [2–4], for 21≤n≤27 [5], and for 28≤n≤30 [6]. The first two of these computer approaches use floating point arithmetic and bound rounding errors only during the geometric steps of the algorithms. The third approach by M.C. Markót and T. Csendes, in contrast, presents a fully interval arithmetic based procedure, providing interval enclosures of both the possible optimizers and the optimum values with high accuracy. The required CPU time for solving the cases n=28,29,30 was about 53, 50, and 21 hours, resp., on an at that time decent PC desktop architecture. The number of so-called tile combinations to be checked during the global search (a good indicator of the complexity of the optimality proof) is 4228, 4229, and 4230, resp., for these instances. The next three instances n=31,32,33 instead require the processing of 4831, 4832, and 4833 combinations. Thus, the case n=31 (resp., 32, 33) requires about 100 times more processing effort than the case n=28 (resp., 29, 30); see Sect. 6 for a detailed calculation. That is, with the method of [6], the estimated solution time would be 3–6 CPU months for n=31,32,33. The goal of the present paper is to improve the method of [6], and solve the cases n=31,32,33 again with reasonable computational effort.
Interval analysis

As mentioned above, the proof method uses interval computations to produce reliable numerical solutions with mathematical correctness. Below we give only a very brief survey on the basic interval definitions and properties; for more details we refer to, e.g., [7–9].

The set of compact intervals is denoted by I, where a=[inf(a),sup(a)]={a∈R|inf(a)≤a≤sup(a)} for all a∈I. Here inf(a),sup(a)∈R denote the lower bound (infimum) and the upper bound (supremum) of a, respectively. If inf(a)=sup(a), we call a a point interval. The width of an interval is defined by w(a):=sup(a)-inf(a). For a given set of real numbers D⊆R, I(D) denotes the set of all intervals in D.

The real arithmetic operations can be extended for intervals by applying the general set theoretic definition a∘b:={a∘b|a∈a,b∈b}.

Let f:D⊆R→R be a real elementary function which is continuous on all a∈I(D). The interval extension of f is defined by f:I(D)→I, f(a):={f(a)|a∈a}. The interval extension of a given elementary function can be calculated e.g. by invoking monotonicity properties.

The n-dimensional intervals (also called boxes) will also be denoted in boldface, with its indices marked in subscripts: a=(a1,a2,⋯,an), a∈In, and ai∈I for i=1,2,⋯,n. Moreover, for a given set of n-dimensional vectors D⊆Rn, I(D) will denote the set of n-dimensional boxes in D. For boxes a,b∈In,hull(a,b) denotes the rectangular (componentwise) hull of a and b. The arithmetic operators and one-dimensional functions are defined componentwise for boxes, similarly as for real vectors.

The interval extensions of compound real functions are called interval inclusion functions. We call f:I(D)→I an inclusion function of f:D⊆Rn→R, if f(x)={f(x)|x∈x}⊆f(x) holds for all x∈I(D), where f(x) denotes the range of f over x. One of the possible ways of constructing such interval functions is the so-called natural interval extension: in the real-type function expression the variables are replaced by intervals, and the operators and elementary functions are replaced by the corresponding interval ones. Note that usually f(x)⊂f(x) holds for the interval inclusion functions, that is, the interval evaluation overestimates the exact range.

For the computer implementation of interval calculations with finite precision floating-point arithmetic, it is essential to control the occurring rounding errors, in order to reach mathematical rigor for the results of calculations (e.g., to guarantee that the above basic inclusion properties hold). This is usually done by the respective interval software packages, using exactly representable floating-point numbers (also called machine numbers) as the bounds of the intervals, and applying directed outward rounding during the calculations.
An interval branch and bound algorithm

In this section an interval branch and bound method is presented for computing interval enclosures of all global maximizers and the f∗ maximum value of the global optimization problem

maxz∈zf(z),
3

where f:Rn→R is a continuous objective function and z∈In is the search box. The pseudo-code of the method is given in Algorithm 1.

In Algorithm 1 we maintain two sets: W stores the current leaves of the B&B tree, while in R the candidate enclosures of the global maximizers are stored. In both of these sets we store the pairs (u,sup(f(u)) for the subbox u, where f is an interval inclusion function of f. In each iteration cycle (between Step 2 and Step 11 of Algorithm 1), a leaf is chosen and bisected. The leaf selection method is discussed in the next paragraph. The bisection methods used in the current study are very specific to the problem and are detailed in Sect. 7. Then for both uk subboxes we attempt to delete those parts of uk that cannot contain a global optimizer (Step 8). If the remaining part of uk (denoted also by uk in the algorithm) fulfills the termination criterion, we store it in R (Step 10), otherwise we place it in W for further processing (Step 11). The search is completed when W becomes empty.

In the current study both W and R have been implemented with the multiset container of the Standard Template Library, storing the elements in decreasing order according to the sup(f(u)) field. Hence in Step 3, the function head returns the leaf with the largest upper bound of the interval inclusion function value.

The algorithmic details discussed up to this point basically followed the techniques used in standard interval B&B frameworks; for further information we therefore refer to the basic textbooks on the subject, e.g., [7, 8]. In contrast, the remaining details of the algorithm, such as the evaluation of f(u), the update of f~, and the accelerating devices (Step 8) are specific for the present packing problem and will be discussed below:

An interval inclusion function of the objective function of the point packing problem. We use the same inclusion function as in [6], first given in [10]:

Theorem 1

[10]: Let (x,y)⊆[0,1]2n, and let sij=(xi-xj)2+(yi-yj)2 for all i,j∈{1,2,…,n}. An inclusion function of fn(x,y) over the 2n-dimensional box (x,y) is given by

fn(x,y):=[min1≤i<j≤ninf(sij),min1≤i<j≤nsup(sij)].

Note that in general the above inclusion function overestimates the exact function range.

Updating
f~. In Algorithm 1, the value f~ denotes the currently best known guaranteed lower bound for the global maximum, used for eliminating suboptimal boxes (or parts of them). In a general framework, this value is initialized as early as possible, and is updated regularly, e.g., by computing the interval inclusion function value on feasible points.

For practical considerations, we will use the notations f0~ and f~ as the lower bounds of the objective functions in (1) and (2), resp. For the present packing problem instances these initial values were determined from the currently best-known packing configurations (see Sect. 7.2 for details). Although a simple updating mechanism was built into the algorithm, the initial values had never been updated, because as we expected the known best configurations have been proven to be the globally optimal ones.

Accelerating devices. In general, in Step 8 of Algorithm 1 several tests are performed to delete those parts of uk that cannot contain global maximizer points. In some cases the whole box can be rejected. Using the lessons learned from the predecessor interval algorithms in [6, 10], in the current algorithm we employ only one accelerating test, the so-called method of active areas, that is actually the key local method of the whole computer-assisted proof. This method is originated from the first non-interval based computer-aided proofs of the problem class [2, 5, 11].

The method is outlined as follows: Assume we have a validated f0~ value. Consider uk in the form of (x,y)⊆[0,1]2n; then for each i=1,⋯,n, the pair (xi,yi)⊆[0,1]2 is a rectangle in the unit square containing the ith point to be placed. These rectangles are called the initial active regions.

During the procedure, from each active region Ri we can delete those points that have a distance smaller than f0~ to all points of another active region Rj,j≠i. Once a region is reduced, it can be further used to reduce the ‘neighboring’ regions, thus, the elimination step can be repeated iteratively for all pairs of regions. The procedure ends when either a region becomes empty (which proves that uk is suboptimal, hence, it can be fully eliminated) or a pre-given iteration limit is reached. In the latter case, uk can be updated with the remaining active regions. For a more detailed description and a pseudo-code see [6].

The most crucial part of the algorithm is the representation of the intermediate active areas (i.e., the Ri regions). As pointed out in [6], the set of points of a two-dimensional geometric object having a distance at least f0~ from all points of another object may be nonconvex or even non-connected. However, a good approximation of the active (and inactive, i.e., erasable) point sets is essential for the efficient execution of the method. In [2] the initial active regions have been split horizontally and vertically into small rectangular pieces. In [11] a similar approach was used, but using splittings in only one direction. The most effective approximation of the non-interval methods was the one of Nurmela and Östergård [5], that approximated the active regions by polygons.

The predecessor interval method [6] of the present study also used a polygon approach. In that method, the polygons have been represented by a sequence of machine representable points (pairs of machine numbers), and in all elimination steps, reliable calculations have been made to ensure that the result polygon always encloses the one that would be computed by exact calculations. However, that approach resulted in a quite complex algorithm with a tedious proof of correctness, and it led to a large, hard-to-maintain, and relatively slow code. The full description of that method actually required a separate paper [12].

In the present paper we introduce a much simpler reliable polygon representation that saves most of the tedious calculations and case examinations, thus, it results in a simpler proof of correctness and a more efficient program code. The new method will be detailed in the next section.
An improved method of active areas using interval polygons

In this section, a convex polygon
R⊆R2 will be defined by the sequence of its vertices r1,⋯,rm,ri∈R2,i=1,⋯,m, so that the edges of R are the line segments r1r2¯,r2r3¯,⋯,rmr1¯. When emphasizing the vertices of R we will use the notation R(r1,⋯,rm). We consider the cases m=1 (i.e., a single point) and m=2 (i.e., a line segment) also as polygons. The set of vertices of R will be denoted by V(R), i.e., V(R)={r1,⋯,rm}.

The euclidean distance between two points p and q will be denoted by d(p, q). If Q is a set of points, the maximum distance between p and Q will be denoted by d(p, Q), i.e., d(p,Q)=maxq∈Qd(p,q). If P and Q are sets of points, we will use the notation d(P,Q)=maxp∈P,q∈Qd(p,q).

We begin by introducing an exact version of the active area elimination method, originated from [5]:

Lemma 1

[5]: If a point p is at distance less than f0~ from all vertices of a polygon R, it is at distance less than f0~ from all points of R. Formally: d(p,V(R))<f0~⇒d(p,R)<f0~.
Theorem 2

[5]: Assume that p1,⋯,pk are distinct points on the boundary of a polygon Ri, so that the line segments pℓpℓ+1¯ for 2≤ℓ≤k-2 are successive edges of Ri, and that p1p2¯ and pk-1pk¯ lay on the edges of Ri. Furthermore, assume that d(pi,V(Rj))<f0~ for 1≤i≤k. Then for the polygon R=R(p1,p2,⋯,pk) we have d(R,Rj)<f0~.

Figure 1 illustrates the method based on the above theorem for k=6 (indexing the vertices so that they fit to the index settings of the theorem), reducing the polygon Ri(p0,⋯,p7). The theorem can be applied by drawing arcs of radius f~1<f0~ from all vertices of Rj, and setting that of the intersection point on p0p2¯ (resp., p5p7¯) to p1 (resp., p6) which is the ‘closest’ to p2 (resp., to p5). Then all points of the shaded polygon can be eliminated by the active area method, and the polygon Ri′=Ri′(p0,p1,p6,p7) can be considered in place of Ri as the remaining active region.

Fig. 1.

Open in a new tab

An example of using Theorem 2
Due to the importance of the special intersection points we introduce the following definition:
Definition 1

Let p0p2¯ be a line segment and Q be a set of points, and assume that d(p2,Q)<f0~. Then a point p∈p0p2¯ with d(p,Q)<f0~ will be called a reduction point on p0p2¯ with respect to Q.

Thus, the above theorem says that any pair of reduction points p1 and pk w.r.t. V(Rj) are suitable to form the remaining active region. Also note that if p1 and pk are reduction points, then any points on the line segments p1p2¯ and pk-1pk¯, resp., are also reduction points.

It is important to note that if the polygons Ri,i=1,⋯,n are initialized as convex sets (as in the current study, since we start with rectangles), then they remain convex after each elementary reduction made by Theorem 2. This is because the remaining polygons will always be the intersection of a convex polygon and one of the half planes determined by p1pk¯.

However, like for many geometric algorithms, the points p1 and pk cannot be evaluated exactly with finite precision floating point arithmetic. Hence we need a mathematically rigorous version of the above method.

Next, we introduce the interval concepts and notation to develop the alternative interval version of the method in [6, 12].
Definition 2

A convex interval polygon R is defined by the sequence of its vertices r1,⋯,rm, where m≥1 and ri∈I2,i=1,⋯,m are two-dimensional, pairwise disjoint intervals. As a set theoretical definition, R is the set of all convex polygons R=R(r1,⋯,rm),i=1,⋯,m, where ri∈ri,i=1,⋯,m.

Note that a convex interval polygon given by r1,⋯,rm may be empty if no convex polygon can be formed from its vertices.

The disjointedness of the interval vertices in the definition is important to get the enclosed polygons easily. This assumption substantially simplifies — in contrast to the predecessor algorithm of [6, 12] — the treated polygon shapes. Note that the disjointedness may fail during the iterative execution of the algorithm, in particular, when the interval vertices are getting so large (due to interval overestimation), that their size is comparable to the polygon itself. However, this actually causes no significant problem for the present method, since we anyway limit the number of iterative area reduction steps, as mentioned above. The disjointedness of the computed interval vertices is very easy to verify, and whenever this criterion fails, we make no area reduction of that interval polygon in the particular reduction step. Furthermore, in the final local refinement phase of the optimality proof we switch to a version that limits the growth of the interval vertices, thus, allows high precision estimates of the final remaining regions (see Sect. 5.2 below for the details).

The distance notation of the exact version can be naturally used to intervals and rectangles the following way:

The maximum euclidean distance between two two-dimensional intervals p and q is given by d(p,q)=maxp∈p,q∈qd(p,q). If Q is a set of two-dimensional intervals, the maximum distance between p and Q is given by d(p,Q)=maxq∈Qd(p,q). If P and Q are sets of two-dimension intervals, we have d(P,Q)=maxp∈P,q∈Qd(p,q).

It is important to note that since we are working with two-dimensional boxes, tight interval enclosures of the above quantities can be computed very fast using interval arithmetic. Let d denote the interval inclusion function of d. If we obtain, for example, that sup(d)<f~0, then we have d<f~0, that is, we have the mathematical guarantee that all distances within the arguments of d are certainly less than f~0.

The interval version of the area elimination method is given in Algorithm 2. The method is demonstrated in Fig. 2. In the figure Ri has five vertices (marked either with ‘−’ or with ‘+’ during the execution of the algorithm), while Rj has three. A possible contained polygon is depicted for both of them by solid lines. The remaining polygon Ri′ (that is an enclosure of an exact remaining polygon, see Theorem 3 below) consists of the vertices p1,p5,q0,q1. The case s=2 could be visualized by considering the interval line segment with endpoints p0 and p2 as Ri.

Fig. 2.

Open in a new tab

The interval area elimination method
The detailed analysis of the algorithm will be provided at the proof of its correctness below:
Theorem 3

Algorithm 2 is correct in the sense that for any pair of convex polygons Ri∈Ri,Rj∈Rj, the reduced polygon Ri′ contains that of the polygon that would be a possible output of the exact area elimination method carried out for Ri and Rj.
Proof

Let Ri∈Ri, that is, bℓ∈bℓ,ℓ=1,⋯,s, and let Rj∈Rj. Observe that the condition sup(d(bℓ,V(Rj))<f0~ in line 2 implies d(bℓ,V(Rj))<f0~. Hence if we find that sup(d(bℓ,V(Rj)))<f0~ holds for all ℓ, then d(bℓ,V(Rj))<f0~ holds for all ℓ as well, so Ri∈Ri can be fully eliminated by the exact algorithm. Since Ri and Rj are chosen arbitrarily, in this case we can eliminate Ri as a whole in line 4. If all vertices are marked with a ‘+’, then we cannot compute reduction points, therefore in line 5 we return Ri′=Ri with no reduction. Now we continue by analyzing the cases for the different s values.

First consider the case s=1, that is, Ri=Ri(b1), and Ri(b1)∈Ri(b1). By the above discussion, if sup(d(b1,V(Rj)))<f0~, then any b1∈b1 can be eliminated by the exact algorithm. In this case we eliminate Ri (line 4). Otherwise, b1∈b1 may or may not be eliminated by the exact algorithm, so a possible correct output of the exact algorithm is to keep b1. In this case we keep Ri=Ri(b1) as a whole (line 5).

Next consider s=2. If we arrive at line 7, then we have Ri=Ri(p0,p2), where p0 is marked with ‘−’ and p2 is marked with ‘+’. Then in line 9 we compute p1, which is by definition the enclosure of possible reduction points for all choices p0∈p0,p2∈p2. That is, for any Ri(p0,p2)∈Ri(p0,p2) (i.e., p0∈p0,p2∈p2), a possible reduction point of the exact algorithm will be contained in p1. Hence, a possible outcome of the exact algorithm is to have Ri′=Ri′(p0,p1) as the remaining polygon, that will be contained in the output polygon Ri′(p0,p1) of line 10.

In line 10 we also check whether p1 is disjoint from p0, so that we are able to form a convex interval polygon. If this is not the case, in line 11 we return the original polygon as a whole, which is also a correct output for the exact algorithm. This completes the proof for s=2.

Finally consider s≥3. The line of thought is similar to s=2, using two reduction points: if we are in line 12, then we have the consecutive vertices p2,⋯,
pk-1 marked with ‘−’. In lines 15 and 16 we compute the enclosures p1 and pk of possible reduction points p1 and pk for all choices of p0∈p0,p2∈p2 and pk-1∈pk-1,pk+1∈pk+1, resp. That is, for any Ri∈Ri a possible outcome of the exact algorithm is to have Ri′=Ri′(p1,pk,d0∈q0,⋯,ds-k+1∈qs-k+1) as the remaining polygon.

If the disjointedness property of the rectangles p1,pk,q0,⋯,qs-k+1 holds in line 18, then we have Ri′=Ri′(p1,pk,q0,⋯,qs-k+1) and thus Ri′∈Ri′. If the disjointedness fails, we can legally consider p2 and pk-1 instead p1 and pk as reduction points of the exact algorithm. The exact algorithm will then result in Ri′=Ri′(p2,pk-1,d0∈q0,⋯,ds-k+1∈qs-k+1), which is again contained in the Ri′ polygon constructed in line 19. This concludes the proof.□

Note that in Algorithm 2, p0=pk+1 may hold after Steps 13 and 14; in this case we construct Ri′ without duplicating q0=pk+1 and qs-k+1=p0 in the result polygon.
Computing reduction rectangles

The only remaining part of Algorithm 2 to discuss is the construction of the enclosure rectangles in Steps 9, 15, and 16. Likewise to the exact version, we will call these enclosures reduction rectangles on the respective interval line segment with respect to the set of reducing points.

In the current packing algorithm the computation of the reduction rectangles is implemented in two flavours. In the first method we consider p0p2¯ as a simple interval extension of a line segment, where both endpoints are rectangles instead of points. The computation of a reduction rectangle w.r.t. a single vertex q is based on solving the interval system describing the intersection of p0p2¯ (with sup(d(p2,q))<f0~) with a set of circles of radius f1~<f0~ centered at any q∈q. The solution procedure is essentially identical to the method described in [12] for the previous implementation, the only difference is that in [12] the endpoints of the line segment and the circle center were treated as thin intervals, while in the present version they are most often thick intervals. However, the interval calculations go exactly the same way, so in the present paper we skip its details. The method is safeguarded in such a way that in case of any computational errors (e.g. an interval-valued discriminant containing negative numbers due to overestimation) the procedure returns p2 as the reduction rectangle, which is, by definition, always a proper choice.

In order to compute a reduction rectangle w.r.t. a set of interval vertices (such as V(Rj) as in Algorithm 2) we first compute the reduction intervals w.r.t. each vertex one by one, and then create the final p1 w.r.t. V(Rj) by properly merging (some of the) the individual reduction rectangles. This merging procedure is also described in [12].
An improved method for computing reduction rectangles

The above first method of computing reduction rectangles w.r.t. V(Rj) has been found to be very fast and efficient in the current implementation, however, it has one drawback. Since the endpoints of the input line segments and the centers of the reducing sets are all intervals (vertices of interval polygons), an excessive blowup of the resulting reduction rectangles (the new polygon vertices) occur after a few iterations, due to interval overestimation. Our experience of solving the packing problems revealed that the initial phases of the algorithm profit from this method, since it eliminates most of the suboptimal search space even before the blowup takes its effect. The final refinement phase of the optimality proof requires, however, a version with smaller overestimation, in order to produce high precision enclosures for the global maximizers.

The second, high precision method is based on the idea that instead of computing the intersection of circles with all possible line segments in an interval line segment (a stripe), the reduction rectangle can be computed by intersecting only with the extremal line segments of the stripe. The theorem below shows how this is carried out (using the notation of Algorithm 2). The application of the theorem is shown in Fig. 3.

Fig. 3.

Open in a new tab

The improved method for computing reduction rectangles
Theorem 4

Let p0 and p2 be interval vertices and assume that Algorithm 2 marks p2 with ‘−’ (i.e., sup(d(p2,V(Rj)))<f0~) and p0 with ‘+’, resp. Let conv(p0,p2) denote the convex hull of p0 and p2, and let a0a2¯ and b0b2¯ be the line segments on the boundary of conv(p0,p2) that join p0 and p2. Assume that these two line segments do not lie on the same line. Compute the reduction rectangles on a0a2¯ and b0b2¯ w.r.t. V(Rj), denoted by a1 and b1, resp. Then p1:=hull(a1,b1) is a reduction rectangle for p0p2¯ w.r.t. V(Rj).
Proof

Assume the contrary of the statement, that is, that p1 is not a proper reduction rectangle. Then there exists a line segment c0c2¯∈p0p2¯ for which c0c2¯∩p1 contains no reduction point w.r.t. V(Rj). That is, ∀p∈c0c2¯∩p1 we have d(p,V(Rj))≥f0~. This implies the existence of a set Q⊆V(Rj) such that d(p,Q)≥f0~∀p, i.e., c0c2¯∩p1 contains no reduction point w.r.t. Q. Let ar∈a1 denote a reduction point on a0a2¯ w.r.t. Q, and let br∈b1 denote a reduction point on b0b2¯ w.r.t. Q. (Such points exist, because a1 and b1 are reduction rectangles w.r.t. V(Rj), and thus, also w.r.t. Q.) Then we have d(ar,Q)<f0~,d(br,Q)<f0~, that is, d(ar,q)<f0~,d(br,q)<f0~,∀q∈Q. Let c1=c0c2¯∩arbr¯∈p1. Then, by Lemma 1 we have d(c1,q)<f0~,∀q∈Q, that is, d(c1,Q)<f0~. This means that c1 is a reduction point on c0c2¯ w.r.t. Q. But this contradicts the previous assumption that c0c2¯∩p1 contains no reduction point on c0c2¯ w.r.t. Q.□

In this second version we thus calculate reduction rectangles for two real line segments (i.e., with thin intervals as their endpoints), which significantly reduce the overestimation. Then the reduction rectangle for the whole p0p2¯ is constructed by taking their rectangular hull. Note that computing the required convex hull of two rectangles and determining a0a2¯ and b0b2¯ can be carried out fast, thus the time requirement of executing this improved method is roughly twice of the first one. Also note that if a0a2¯ and b0b2¯ lie on the same line, then we necessarily have thin components in p0 and p2, and we can compute the reduction rectangle by one application of the first method.

In addition to the easier implementation, proof of correctness, and improved efficiency, the reduction algorithm presented in this section has one more important advantage over the predecessor method of [6, 12]. Namely, in the current implementation the complexity of the data structure, i.e., the number of interval vertices, can be kept better under control during the execution of the algorithm. In particular, the present method so closely resembles that of the exact area reduction method, that in most cases the number of interval vertices of each polygon was found to be close to the number of possibly neighboring (i.e., reducing) other polygons of the packing configuration plus the number of sides of the unit square on which the polygon was possibly located.
A global elimination procedure

In the previous two sections we introduced the branch–and–bound framework designed for point packing problems, with the method of active areas as its key element. The latter method works well for cases where the locations of the points of the packing are at least approximately known. It is clear that if we start the global search from the whole initial box [0,1]2n, branching alone will not be sufficient to reach this state in a reasonable amount of steps, due to the problem dimensionality and the difficulties caused by the permutation and symmetry of the points to be packed. Thus, special methods are needed to tackle the initial phase of the global search. The most important such method, used already in [2, 5, 6, 10, 11], is called tiling:

Assume that a lower bound f0~ for the maximum value of the point packing problem (1) is given. Split the unit square into regions (tiles), so that the distance between any two points in each tile is less than f0~ (or equivalently, that the squared distance between any two points in each tile is less than f~ for (2)). Then for each packing configuration attaining objective function value greater than or equal to f0~ each tile can contain at most one point of the packing. The packing problem can be solved to global optimality by running a search procedure on all possible tile combinations.

Due to the rectangular branch-and-bound framework, in our study we prefer a rectangular splitting of the square. Furthermore, we require a regular splitting in order to be able to exploit symmetry and the tile pattern methods (introduced later in this section). If we split the unit square into k×l rectangles (in a regular way), the minimal number of initial tile combinations is given by

minnk·l|k,l≥1integers,(1/k2+1/l2)1/2<f0~.

In the studies prior to [6], all tile combinations have been eliminated one after the other. Nevertheless, the growth of the number of tile combinations obstructs the solution of the problem instances n≥28 with this strategy in acceptable time. For n=28,29,30 at least a 6×7 tiling is needed, which gives 4228≈5.29·1010, 4229≈2.55·1010, and 4230≈1.11·1010 tile combinations, resp., to be checked.

One of the key ideas of the predecessor method [6] was the observation that instead of processing all tile combinations consisting of n tiles, we can first investigate subsets of the full tile combinations, in order to discover patterns of tile sets that cannot contain components of an optimal solution. Then the higher dimensional subproblems containing any of these patterns can be discarded. With the resulting method we were able to solve those three instances in about 53, 50, and 21 CPU hours, with an at that time decent computer architecture.

For the next problems n=31,32,33, an 6×8 tiling gives the smallest number of combinations, resulting in 4831≈4.24·1012, 4832≈2.25·1012, and 4833≈1.09·1012 cases, an increase of about 100 times as compared to the previous three cases for each pair of problem instances. Clearly, to reach again a reasonable solution time (and to lay the foundations of solving further instances) we need an improvement of the global phase methods of [6] as well.

Let us denote P(m,x1,⋯,xm,y1,⋯,ym) a point packing problem instance where m is the number of points to be packed, (xi,yi)∈I,i=1,⋯m are the components of the starting box (i.e., the rectangle (xi,yi) is the location of the ith point), and the objective function is given by (2). The theorem and its corollary below from [6] demonstrate how to apply a result achieved on a 2m-dimensional packing problem for a higher dimensional problem with 2k dimensions, k≥m≥2.

Theorem 5

[6] Let k≥m≥2 be integers and let

Pm=P(m,z1,⋯,zm,w1,⋯,wm)=P(m,(z,w)),andPk=P(k,x1,⋯,xk,y1,⋯,yk)=P(k,(x,y))

be point packing problem instances (xi,yi,zi,wi∈I,xi,yi,zi,wi⊆[0,1]). Run Algorithm 1 on Pm using a hypothetical f~ cutoff value in the accelerating devices and skipping Step 7 (the update of f~), and stop after an arbitrary, preset number of iteration steps. Denote (z1′,⋯,zm′,w1′,⋯,
wm′):=(z′,w′) the componentwise hull of all elements placed on W and on R. Assume that there exists an invertible, distance-preserving geometrical transformation φ with φ(zi)=xi and φ(wi)=yi,∀i=1,⋯,m. Then for each point packing (x,y)∈R2k satisfying (x,y)∈(x,y) and fk(x,y)≥f~, the statement

(x,y)∈(φ(z1′),⋯,φ(zm′),xm+1,⋯,xk,φ(w1′),⋯,φ(wm′),ym+1,⋯,yk):=(x′,y′)

also holds.

Informally Theorem 5 states the following: assume that we are able to reduce some search regions on a tile set S′. When processing a higher dimensional subproblem (using the same cutoff value) on a tile set S containing the image of S′, it is enough to consider the image of those of the remaining regions of
S′ for the particular components of S.
Corollary 1

[6] Let Pm,Pk, f~, and φ be as in Theorem 5. Let φ be the identity transformation and assume that Algorithm 1 stops with W=∅ and R=∅, i.e. the whole search region (z,w)=(z1,⋯,zm,w1,⋯,wm)=(x1,⋯,xm,
y1,⋯,ym) is eliminated by the accelerating devices using f~. Then (x,y) does not contain any (x,y)∈R2k vectors for which fk(x,y)≥f~ holds.

Corollary 1 states that if it is proved that S′ cannot contain point packings attaining at least f~ function value, then all higher dimensional problems with the tile set S, S′⊆S can be eliminated at once (when using the same f~).

In the present study the global search phase is improved by using the two additional theorems below:
Theorem 6

Let k≥2 and let

Pk=P(k,x1,⋯,xk,y1,⋯,yk)=P(k,(x,y))

be a point packing problem instance (xi,yi∈I,xi,yi⊆[0,1]). Run Algorithm 1 on Pk using a hypothetical f~1 cutoff value in the accelerating devices and skipping Step 7 (the update of f~1), and stop after an arbitrary, preset number of iteration steps. Denote (x1′,⋯,xk′,y1′,⋯yk′):=(x′,y′) the componentwise hull of all elements placed on W and on R and let f~2>f~1. Then for any point packing (x,y)∈(x,y) with fk(x,y)≥f~2 we have (x,y)∈(x′,y′).
Proof

Consider a point packing (x, y) with (x,y)∈(x,y) and fk(x,y)≥f~2 and assume that (x,y)∉(x′,y′). Then (x, y) is discarded by Algorithm 1 using f~1. This implies that fk(x,y)<f~1, which together with f~2>f~1 gives fk(x,y)<f~2, a contradiction.□
Remark 1

The importance of Theorem 6 is that if some search regions on a tile set S can be eliminated by a f~1 cutoff value, then it is sufficient to consider only the reduced regions (on the same tile set) when using a larger f~2 cutoff value. Note that the cutoff values are computed from the best-known optimal packing solutions, and we have f~31>f~32>f~33, see Sect. 7.2. Thus for our present problem instances the remaining regions computed on the subproblems of
n=33
can be used for the solution process for
n=32
and
n=31, and similarly, the remaining regions computed for
n=32
can be used when solving the case
n=31. That is, as a completely new idea, we solve the largest of the considered problem instances first (which anyway consists of the smallest number of tile combinations), and in this way avoid many of the repeated search space reductions for the smaller problem instances.

Another new theorem that helps to improve the global search phase is based on the already known optimal solution for 10 circles. It gives an important property of the tile patterns to be considered.
Theorem 7

No optimal packing of n=31,32,33 points, resp., can contain 10 or more points in a region of size 0.5×0.5 in the unit square.
Proof

Assume that there exists an optimal arrangement of n=31 (resp., 32, 33) points in the unit square, for which a region of size 0.5×0.5 contains 10 points. Let the smallest distance between the pairs of points in this arrangement be denoted by f31 (resp., f32,f33). From the best known packing values of n=31 (resp., 32, 33), see [13], we have f31>0.2175 (resp., f32>0.2131 and f33>0.2113). Enlarging the mentioned region to the size of a unit square, we get an arrangement of 10 points with the smallest pairwise distance between them being at least 2f31>0.435 (resp., 2f32>0.4262 and 2f33>0.4226). But this contradicts the fact that the known optimum of the problem of packing 10 points is f10∗<0.4213.□

To achieve mathematical correctness during the application of the symmetry transformations, it is essential that the tiles have identical size even in their computer representation. Therefore, for the 6×8 tiling we enlarge the unit square to [0,24]2 so that each tile has integer coordinates. (Of course, we also increase the used f~ values accordingly for the B&B search.) Figure 4 shows the row, column, and tile numbering used in the present study.

Fig. 4.

Open in a new tab

Row, column, and tile numbering for n=31,32,33
The method of [6] was based on the following strategy (on a 7×6 rectangular tiling): in phase 1, we run the B&B algorithm on the tile combinations of size 7×3 (filtering cases out by using the symmetry group of a rectangle), and stored the remaining combinations together with the rectangular enclosure of each of their remaining tile regions. In phase 2, we computed the possible combinations of size 7×4 (again together with their remaining regions) by adding one column to the results of phase 1 (after extracting symmetric cases when needed). In phase 3, we joined the remaining combinations from phase 2 on columns 1 to 4 and on columns 3 to 6, by checking feasible tile patterns and their active regions on the joint columns 3 and 4. This led us to the remaining regions on the whole square with n active regions, one from each tile. The proof process had been completed with two local refinement phases. Although leading to a successful solution, both phases 2 and 3 required quite complicated algorithms, fully detailed in [6].

The goal of the present study is to improve this strategy in such a way that we use simpler algorithms and improve the tile combination reduction techniques by employing Theorem 6 and Theorem 7 and using more advanced data structures for storing tile combinations and their remaining areas. As we will see later, it is enough to use only two phases for the global part: in phase 1, we compute tile combinations on the half square (size 6×4), then in phase 2 we merge them into the full square. At the same time we can keep the number of intermediate combinations of phase 1 to a manageable size (around one million), so that they all fit into memory for a fast execution of the second phase. Our new global strategy will be introduced in detail in the next section.
Optimality for n=31,32, and 33

Hardware and software environment

The optimization procedure was carried out on a laptop computer with an Intel T2080 1.73 GHz CPU and 2 Gbytes RAM, under the Linux operating system. (The mentioned processor has two physical cores, however, we run the whole process sequentially, so only one core was used at a time.) The algorithms have been implemented in C++, using the C–XSC interval arithmetic library [14].
Guaranteed lower bounds for the maximum

The currently known best packings have been found by R.L. Graham and B.D. Lubachevsky for n=31 and n=33 [15], and by D.W. Boll et al. for n=32 [16]. In [13] the maximum values and the maximizers are given with the precision of 30 digits. The f~0 lower bounds have been obtained from the given optimizers, cut to 16 digits after the decimal dot:

f~0,31=0.2175472916191244,f~0,32=0.2131745625898765,f~0,33=0.2113283841432631.

Note that one needs to verify that these numbers (more precisely, the double precision floating point numbers created from these decimal constants) are indeed lower bounds of the problem. This check has been done by variable precision calculations with GNU Octave, using the above mentioned high precision coordinates. The actual lower bounds used during the calculations (recall that we optimize on [0,24]2 for squared distances) have been constructed by computing (24·f~0,n)2 with interval arithmetic and taking the infimum of the result.
Optimality proof for n=33

During the optimality proof we work on sets of tile combinations, where each combination is represented by k<n rectangles. Each of these rectangles is initialized with the bounds of the respective full tile and during the process it contains the rectangular enclosure of the remaining region of that tile (after, e.g., running Algorithm 1 or using tile pattern techniques based on Theorems 5–7). In particular, S4k will denote the sets of tile combinations where k tiles are taken from columns 1 to 4 (i.e., the left half) of the square. Furthermore, S8ℓ,r with ℓ+r=n will denote sets where ℓ tile regions are considered from the left half and r regions are considered from the right half of the square. Finally, S8n denotes the set of combinations where n tile regions are taken from the full square. (In the notation we do not differentiate whether these sets are the initial ones with full tiles or they are ones with reduced regions. During the discussion the actual state of these sets will always be made clear.)

The tile positions of the tile combinations were represented by the Standard Template Library (STL) bitset of length 48. This allows fast manipulation of the tile combinations, since symmetry transformations and shifting can be carried out very efficiently on this data structure. Furthermore, ordering relations can also be easily defined on bitsets (e.g., by a lexicographical ordering on all or parts of the bits), thus, fast (logarithmic) searches can be performed on them when looking for a given tile combination (or a combination with a given subset). It was found that the use of this data structure also contributed to the performance improvement as compared to [6] (where simple binary strings had been used for representing tile positions).

Below we detail the procedure for n=33 only, since it is running essentially the same way for all three problem instances. The differences arising for n=32 and n=31 (e.g., the use of Theorem 6) will be discussed in the next subsection. The whole process consists of three phases: in phase 1 tile combinations in S4k are processed for the required k values. In phase 2 the sets S8ℓ,r, built from the remaining combinations of phase 1, are processed. These two phases consist of the global part of the search, devoted to reduce the tile combinations in S8n. In the last, local phase, the (small number of) remaining combinations in S8n are processed to provide high precision enclosures for all global maximizers.

Phase 1

As mentioned above, we start by processing tile combinations in S4k. For n=33 Theorem 7 implies that there is no need to deal with k≥19 (since in this case a quarter of the square would contain at least 10 tiles, which is impossible for tile combinations containing a global maximizer). Thus, we start with k=18. Since at this point there is no previous information about the possible tile locations, we generate the elements of S418 consisting of full tiles. The resulting 2418 combinations are first filtered by using the symmetry group of the rectangle. In practice this means that for each combination we consider its bitset representation, compute the bitsets of the transformed combinations (horizontal and vertical reflection, and rotation around the midpoint), and keep the original combination for further processing only if it gives the smallest bitset among the four. Otherwise the combination is filtered out. Note that since the tiles are rectangular, we are able to use only the symmetries of the rectangle. If the tile combination survives the symmetry filtering, we perform tile pattern filtering on it, using Theorem 7: if it is found that the combination contains at least 10 tiles in any 3×4 tile region of the half square, then the combination is filtered out.

After these two filtering procedures, we proceed by running Algorithm 1 on the combination, to reduce its active regions within each tile. In phase 1, the following settings of the algorithm are used: 

The maximum number of iterations of the algorithm is set to 20. Note that in this initial phase there is no need to run the algorithm long (a lesson learned from [6]). The goal here is to make some initial area reductions and to eliminate tile combinations that are easily found to be suboptimal.

The direction along which the current box is subdivided is determined the following way: First search for the rectangle (xi,yi) with the largest area, and bisect this rectangle perpendicular to its larger side. The goal of this subdivision strategy is to apply branching on components for which the method of active areas worked the least efficiently.

The reduction rectangles in Algorithm 2 are computed by the method of Sect. 5.1 (the faster one with larger overestimation). This is because in this phase the primary goal is to eliminate combinations fast and it is less important to go for high precision results.

The stopping tolerance ε used in Step 10 of Algorithm 1 is set to 10-12 (also in the later phases). However, in this phase the termination of the algorithm is mainly controlled by the maximum number of iterations.

If the algorithm stops with no subboxes left, the tile combination cannot be a subset of an optimal combination (see Corollary 1). Otherwise, the tile combination is stored together with the rectangular enclosures of its remaining tile regions for the next phase.

Table 1 contains the computational details of the steps of the optimality proof for n=33, grouped by the successive phases. The table is organized the following way: the first column is the notation of the particular set of tile combinations. The second column, marked by |S|th, contains, as a reference, the (approximate) theoretical size of this set with no elimination. That is, the exact values in this column are 24k for S4k, 24ℓ·24r for S8ℓ,r, and 48n for S8n. The third column, marked by |S|filt, contains the size of this set of tile combinations after performing symmetry filtering, tile pattern filtering (and in phase 2, tile region filtering). This is the size of the set that is passed one by one to the B&B algorithm. The fourth column, marked by |S|red contains the size of the set of remaining tile combinations after running the B&B algorithm. The last column contains the overall running time of the B&B method on this set of tile combinations. (Note that the tile generating, filtering, and other auxiliary methods took only about half minute for the whole optimality proof altogether, hence their running times are not displayed in the table.)

Table 1.

Computational details of solving the packing problem of n=33 points

S

|S|th (approx.)
|S|filt
|S|red
CPUt (min.)

Phase 1

S418
1.34×105
6 672
5
0.5

S415
1.31×106
274 384
153 593
235.3

S416
7.35×105
39 108
37 825
57.2

S417
3.46×105
3 152
2 935
4.8

Phase 2

S818,15
1.76×1011
87 372
45
3.6

S817,16
2.55×1011
15 096 352
346
446.1

Phase 3

S833
1.09×1012
391
4
11.3

S833
1.09×1012
4
4
14.0

∑
–
15 507 435
194 757
772.8

Open in a new tab
In the example of processing S418, the first line of the table is thus interpreted as follows: the total number of combinations in this set is 2418≈1.34·105. After filtering out by symmetry and by the maximum number of tiles in a quarter, we obtained 6 672 combinations. Algorithm 1 reduced the number of tile combinations in this set to 5, with a running time of 0.5 minute. The subsequent lines of the table are interpreted the same way.

After processing S418, we proceed the same way with its (to be) complement tile combinations on the whole square, that is, with S415. Next, the set S416 is processed. In this step we employ a technique (that is also a novelty of the present study) we call incremental tile generation. This is based on the observation that a good portion of the area elimination procedures on 16 full tiles on the half square would be a repeated work of what has been already done for 15 tiles. More precisely, from Theorem 5 it is enough to consider the remaining combinations (together with their remaining tile regions) from the processed set of S415, and extend these with one more full tile. So for S416 we proceed as follows: we take each element of the reduced set of S415, extract its rectangular symmetry, and add one more full tile in all possible ways to the extracted tile combinations. Then we continue by filtering by symmetry and by the number of tiles in a quarter, and process the filtered combinations with the B&B algorithm, just like for S418 and S415. The tile combinations of S417 are also processed in this incremental way, using the result combinations of S416.

As a result of phase 1, we have all possible tile combinations of S4k,k=15,16,17,18 (apart from the filtered symmetry), that can be a subset of the tile combination of any optimal packing. Furthermore, the tile regions of each remaining combination are reduced so that they still certainly contain the subset of all optimal packing configurations. Note that it is not necessary to process the sets S4k for k<14. The reason of this, on the one hand, is that such a tile combination cannot be a half of an optimal configuration. On the other hand, by decreasing k, the number of tile combinations to process will grow (until k=12), and at the same time we will be able to extract less and less information on the possible remaining regions.
Phase 2

In the second global phase the sets S8ℓ,r are created and processed. We consider the cases ℓ≥r only (note that this also filters out some symmetry). The processing is initiated by loading S4k,k=15,⋯,18 into memory (also extracting the symmetric instances for all tile combinations), and sorting them for each k according to the bitset representation of their tile combination for fast searching. (Thus, in the sequel S4k,k=15,⋯,18 will denote all remaining combinations after extracting symmetry.) The method given below is done first for ℓ=18,r=15, then for ℓ=17,r=16:

For each pairs of tile combinations Tℓ∈S4ℓ and Tr∈S4r we create a tile combination T∈S8ℓ,r, after shifting Tr to the right half square. T thus initially contains a tile pattern bitset and the corresponding remaining regions, both joined together from the respective data of Tℓ and Tr. We process T with the following algorithm (observe that the algorithm starts with the cheaper filtering methods and continues with the more and more expensive ones): 

If Tℓ can be filtered out by horizontal reflection, then filter out T.

Count the tiles of T in the horizontal half square sized regions of the tiling (i.e., in the regions consisting of rows 1–4, 2–5, 3–6). If this count is greater than 18 in any such region, filter out T (by Theorem 7).

Next count the tiles of T in the vertical half square sized regions (i.e., the regions consisting of rows 2–5, 3–6, 4–7; note that the regions of columns 1–4 and 5–8 are the two input regions, so they do not have to be checked). If this count is greater than 18 in any such region, then filter out T.

Next check the tile patterns (the bitsets) in all the above vertical half square sized regions. If the tile count in any vertical half is between 15 and 18, then search for the corresponding tile pattern in S4k,k=15,⋯,18. If the pattern is not found, filter out T by Corollary 1.

If T passed all tile count and tile pattern tests so far, then check the remaining regions of the vertical half square sized regions. If the tile count in any vertical half is between 15 and 18, then, by the previous step, we have the remaining tile regions of these halves stored in S4k,k=15,⋯,18. In this case, by Theorem 5 we can update the respective tile regions of T by intersecting them with the remaining regions from S4k. (Of course, the latter regions are always shifted to the right column positions.) If during any intersection steps a tile region becomes empty, then filter out T by Corollary 1.

Finally, process the remaining regions of T with the B&B algorithm (using the same settings as in phase 1), to create the reduced S8ℓ,r.

The respective lines of Table 1 contains the computational details of phase 2. |S|filt again refers to the number of those combinations that survived the filtering process (steps 1 to 5 above), and were passed to the B&B search, and |S|red are the number of combinations remained after the B&B search. It is worth observing that both the filtering steps and the B&B algorithm contributed significantly to the reduction of the tile combinations. As a result of phase 2 we had 391 combinations left, which were merged into the initial S833 for the next phase.
Phase 3

In the third, local refinement phase, we execute the B&B algorithm for all elements in S833 one by one. There is no filtering in this phase, so here |S|filt just refers to the number of input tile combinations. The settings of the B&B algorithm are the following for this phase: 

The maximum number of iterations is increased to 20 000, to let the algorithm run much longer than in the previous phases.

The method for selecting the subdivision direction is also changed: we choose that of the rectangle of the current box for subdivision that followed the index of the last split rectangle of this box (starting at index 1 for the first selection), and bisect it perpendicular to its larger side. This method is based on the observation that, due to the large number of iterations of the local refinement phase, some components may remain significantly larger than the others (e.g., those that are constrained by less neighboring points in the packing or those that contain a free point, see below). Hence selecting the component with the largest area can easily cause excessive (and unnecessary) subdivisions. Splitting with equal frequency in all components helps to reduce this effect.

The reduction rectangles of Algorithm 2 are computed by the method of Sect. 5.2 (the improved one with reduced amount of overestimation), designed for the refinement phase to reach higher precision. Since the number of remaining subproblems is already small at this point, the additional amount of extra processing time was not significant in overall.

The first step of the local refinement phase reduces the number of remaining tile combinations to four. To reach a precision of the enclosures that is close to double precision, two additional small tools are used:

First, since the algorithm runs long for the four remaining combinations, we need to do a simple clustering of the subboxes remaining in W and R. This gathers the unnecessary split subboxes together, and also, it is done with the purpose of identifying nearby but separate optimal solutions (although in theory this is possible, for the present three problem instances we did not find such solutions).

The second tool we use at this point is to guess free points (that is, points in optimal configurations that can slightly move without affecting optimality) in the remaining regions. This tool was used, in a somewhat different form, also in [6]. In detail, we employ the following lemma:

Lemma 2

Let I⊂{1,⋯,n} be an index set, (x,y)⊆[0,1]2n be a box, (xi,yi)∈(xi,yi) for all I, and let f¯ be an upper bound of the global maximum of the point packing problem (with squared distances). Assume that

inf((xi-xj)2+(yi-yj)2)>f¯∀i∈I,∀j∉I,and
4

(xi-xj)2+(yi-yj)2>f¯∀i,j∈I,i≠j.
5

If {(xj∗,yj∗)∈(xj,yj),j∉I} are the components of any optimal point packing, then these components can be extended with {(xi,yi),i∈I} as free points, to get an optimal packing.
Proof

Consider an optimal packing {(xi∗,yi∗)∈(xi,yi),i=1,⋯,n} (with objective function value less than or equal to f¯), and replace its ith components with (xi,yi) for all i∈I. Then from (4) and (5) we have

(xi-xj∗)2+(yi-yj∗)2>f¯∀i∈I,∀j∉I,and(xi-xj)2+(yi-yj)2>f¯∀i,j∈I,i≠j,

which implies that (xi,yi) can be slightly moved without affecting the objective function value, that is, optimality.□

For n=31,32,33 we used the free points of the best known packings to create {(xi,yi)} (after applying symmetry transformations, when necessary), with 4, 3, and 1 free points, resp. (See also Fig. 5 in Sect. 7.5.) The interval-based verification of (4) and (5) was successful for all remaining (x,y) boxes at the end of the first step of phase 3 (with the exception of n=31, where one more refining step was needed to reduce the remain regions, so the free points have been detected after the second step of phase 3). The importance of the detection is that for the next local refinement step we can switch off bisecting the components in I, thus we can further accelerate the search and avoid unnecessary subdivisions.

Fig. 5.

Open in a new tab

The optimal packings of n=31,32,33 circles
For n=33, after clustering the results and identifying possible free points, in the second step of phase 3 we re-run the B&B search on the remaining 4 boxes (with the same settings) to increase the precision of the results. After analyzing the final four boxes, we recognized that the first and second one are from neighboring tile combinations. (Recall that every initial box passed to the B&B algorithm back in phase 1 was an individual tile combination.) The reason of this is that the possible locations of the (only) free point spread over two tile regions. The situation was the same for the third and fourth boxes. Furthermore, the first two and the last two boxes were proven to be symmetric to one of the diagonals of the square. (Note that since we filtered by the symmetry of the (rectangular) tile regions, it was not guaranteed that we filter out all symmetries in the square.) The optimal solution (taking the componentwise hull of the first two boxes) is given in Table 4, after transforming the results back to [0,1]2. In the table underlines indicate the width of the enclosure intervals, that is, the precision of the result: if the width is d·10-p where 1≤d<10, then the first p digits are underlined for both bounds. The table shows that it was possible to provide very tight enclosures in all components (except the free point) with the precision of 13 to 15 digits.

Table 4.

The enclosure of the global maximizers for packing 33 points

i
xi
yi

1

[0.0000000000000_00,0.0000000000000_10],
[0.00000000000000_0,0.00000000000000_6]

2

[0.105678610816_670,0.105678610816_785],
[0.1830074237850_40,0.1830074237851_09]

3

[0.000000000000_000,0.000000000000_220],
[0.366014847570_080,0.366014847570_212]

4

[0.00000000000000_0,0.00000000000000_5],
[0.577343231713_343,0.577343231713_475]

5

[0.00000000000000_0,0.00000000000000_5],
[0.788671615856_606,0.788671615856_738]

6

[0.00000000000000_0,0.00000000000000_5],
[0.999999999999_869,1.000000000000_000]

7

[0.211357221633_341,0.211357221633_564],
[0.0000000000000_00,0.0000000000000_66]

8

[0.2113572182268_59,0.2113572182268_69],
[0.36601484953729_9,0.36601484953730_3]

9

[0.21132838414326_2,0.21132838414326_8],
[0.57734323171347_1,0.57734323171347_5]

10

[0.21132838414326_2,0.21132838414326_9],
[0.78867161585673_4,0.78867161585673_8]

11

[0.21132838414326_2,0.21132838414326_8],
[0.99999999999999_7,1.00000000000000_0]

12

[0.317035829043_529,0.317035829043_645],
[0.1830074257521_94,0.1830074257522_62]

13

[0.4227144364537_18,0.4227144364537_28],
[0.00000000000000_0,0.00000000000000_3]

14

[0.422714429643_971,0.422714429644_197],
[0.3660148554366_53,0.3660148554367_18]

15

[0.4226567682865_25,0.4226567682865_31],
[0.5773432317134_09,0.5773432317134_75]

16

[0.4226567682865_25,0.4226567682865_32],
[0.7886716158566_72,0.7886716158567_38]

17

[0.4226567682865_25,0.4226567682865_31],
[0.9999999999999_35,1.0000000000000_00]

18

[0.528393037054_160,0.528393037054_275],
[0.1830074296844_55,0.1830074296845_24]

19

[0.634071637654_601,0.634071637654_825],
[0.000000000000_000,0.000000000000_129]

20

[0.6341713076398_21,0.6341713076398_36],
[0.36595726821002_0,0.36595726821002_8]

21

[0.63398514456328_2,0.63398514456328_8],
[0.57728557035602_0,0.57728557035602_9]

22

[0.63398515046269_7,0.63398515046270_3],
[0.7886427817731_23,0.7886427817731_42]

23

[0.63398515242978_9,0.63398515242979_4],
[0.99999999999999_2,1.00000000000000_0]

24

[0.845400021797_864,0.845400021798_088],
[0.000000000000_000,0.000000000000_238]

25

[0.7_42408052211766,0.8_17880315336449],
[0.1_84532761712745,0.2_56698005516485]

26

[0.820133056170_537,0.820133056170_612],
[0.466346082467_272,0.466346082467_400]

27

[0.81699257424780_1,0.81699257424780_9],
[0.6829641709564_60,0.6829641709564_71]

28

[0.81699257621488_9,0.81699257621489_7],
[0.8943213891833_19,0.8943213891833_30]

29

[0.999999999999_778,1.000000000000_000],
[0.144078217245_015,0.144078217245_254]

30

[0.999999999999_863,1.000000000000_000],
[0.355406601388_278,0.355406601388_517]

31

[0.99999999999999_4,1.00000000000000_0],
[0.5772855635462_64,0.5772855635462_83]

32

[0.99999999999999_7,1.00000000000000_0],
[0.78864277836665_1,0.78864277836665_9]

33

[0.9999999999999_89,1.0000000000000_00],
[0.9999999999999_82,1.0000000000000_00]

Open in a new tab

 Underlines indicate the width of the result intervals 

Optimality proofs for n=32,31

The processes of finding all optimal packings of 32 and 31 points are very similar to the first instance. The only significant difference is the use of Theorem 6 in phase 1 (see also Remark 1): namely, when solving n=32, the initial sets of S4k are the reduced ones computed for n=33 (if they are available). Similarly, when solving n=31, the input S4k sets are the output sets S4k computed for n=32 (if they are available). In both cases we can avoid a lot of repeated area reductions, though we estimate that this technique reduced the overall running time only by about 1 to 2%. The computational results of the two instances are shown in Tables 2 and 3.

Table 2.

Computational details of solving the packing problem of n=32 points

S

|S|th (approx.)
|S|filt
|S|red
CPUt (min.)

Phase 1

S418
1.34×105
5
1
0.0

S414
1.96×106
457 340
292 900
380.8

S415
1.31×106
153 593
113 833
165.3

S416
7.35×105
37 825
22 391
36.7

S417
3.46×105
2 935
1 177
2.2

Phase 2

S818,14
2.64×1011
25 818
0
1.5

S817,15
4.53×1011
23 108 558
4 699
760.2

S816,16
5.41×1011
61 663 679
7 804
1 991.8

Phase 3

S832
2.25×1012
12 503
3
295.9

S832
2.25×1012
3
3
10.4

∑
–
85 462 259
442 811
3 644.8

Open in a new tab
Table 3.

Computational details of solving the packing problem of n=31 points

S

|S|th (approx.)
|S|filt
|S|red
CPUt (min.)

Phase 1

S418
1.34×105
1
0
0.0

S414
1.96×106
292 900
189 650
243.0

S415
1.31×106
113 833
54 833
79.6

S416
7.35×105
22 391
6 501
11.1

S417
3.46×105
1 177
110
0.2

Phase 2

S817,14
6.79×1011
1 024 058
0
36.2

S816,15
9.62×1011
36 228 141
1 984
1131.3

Phase 3

S831
4.24×1012
1 984
1
40.0

S831
4.24×1012
1
2
8.6

S831
4.24×1012
2
1
4.3

∑
–
37 684 488
253 082
1 554.3

Open in a new tab
After the end of phase 3, the number of result boxes was three for n=32, with symmetry properties similar to n=33: here the first two boxes come from neighboring tile combinations, due to a free point expanding in two neighboring tiles. The third box is diagonally symmetric to the first two, however, for this symmetric case the possible locations of the mentioned free point all fit into one tile. For n=31 we had only one box left. The enclosures of all global maximizers (apart from symmetry) are given in Tables 5 and 6. Both the computational complexity and the precision reached for the final results are similar to those obtained for n=33.

Table 5.

The enclosure of the global maximizers for packing 32 points

i
xi
yi

1

[0.0000000000000_00,0.0000000000000_10],
[0.0000000000000_00,0.0000000000000_10]

2

[0.1065872812949_34,0.1065872812949_48],
[0.1846145866434_64,0.1846145866434_75]

3

[0.00000000000000_0,0.00000000000000_9],
[0.3692291732869_29,0.3692291732869_42]

4

[0.0000000000000_00,0.0000000000000_21],
[0.5824037358768_06,0.5824037358768_19]

5

[0.0429736452139_39,0.0429736452139_63],
[0.7912018679384_00,0.7912018679384_10]

6

[0.0000000000000_00,0.0000000000000_18],
[0.99999999999999_4,1.00000000000000_0]

7

[0.2131745625898_76,0.2131745625898_90],
[0.0000000000000_00,0.0000000000000_14]

8

[0.2131745625898_76,0.2131745625898_90],
[0.3692291732869_33,0.3692291732869_43]

9

[0.2131745625898_76,0.2131745625899_03],
[0.5824037358768_09,0.5824037358768_19]

10

[0.2131745625898_76,0.2131745625899_01],
[0.99999999999999_5,1.00000000000000_0]

11

[0.3197618438848_11,0.3197618438848_32],
[0.1846145866434_65,0.1846145866434_80]

12

[0.2561482078038_18,0.2561482078038_39],
[0.79120186793840_2,0.79120186793841_0]

13

[0.4263491251797_52,0.4263491251797_67],
[0.00000000000000_0,0.00000000000000_8]

14

[0.4263491251797_52,0.4263491251797_87],
[0.3692291732868_98,0.3692291732869_42]

15

[0.426349125179_752,0.426349125179_893],
[0.582403735876_774,0.582403735876_818]

16

[0.4693227703936_95,0.4693227703937_16],
[0.7912018679383_96,0.7912018679384_09]

17

[0.4263491251797_52,0.4263491251797_96],
[0.9999999999999_90,1.0000000000000_00]

18

[0.6395236877696_29,0.6395236877696_44],
[0.0000000000000_00,0.0000000000000_17]

19

[0.5_32936406474687,0.6_29399401634653],
[0.1_84614586635930,0.2_28792625209860]

20

[0.6286416704729_41,0.6286416704729_80],
[0.4364684494146_58,0.4364684494147_04]

21

[0.6287106033254_52,0.6287106033254_96],
[0.6496430008593_54,0.6496430008593_99]

22

[0.628660434414_802,0.628660434415_328],
[0.93281720241_7104,0.93281720241_8201]

23

[0.8153854133565_08,0.8153854133565_75],
[0.1204825614309_68,0.1204825614310_63]

24

[0.8153854133564_87,0.8153854133565_37],
[0.333657124020_851,0.333657124020_946]

25

[0.816410131219_076,0.816410131219_211],
[0.548587167955_480,0.548587167955_710]

26

[0.7_88120834443415,0.8_15385413356685],
[0.7_61667643841610,0.7_91176644707691]

27

[0.830971743649_852,0.830971743650_190],
[0.999999999999_752,1.000000000000_000]

28

[0.99_1247138943389,1.00_0000000000000],
[0.0_00000000000000,0.0_13895280136112]

29

[0.9999999999999_84,1.0000000000000_00],
[0.2270698427259_62,0.2270698427259_88]

30

[0.9999999999999_88,1.0000000000000_00],
[0.4402444053158_39,0.4402444053158_66]

31

[0.999999999999_790,1.000000000000_000],
[0.656929930595_115,0.656929930595_554]

32

[0.999999999999_727,1.000000000000_000],
[0.870104493184_992,0.870104493185_431]

Open in a new tab

 Underlines indicate the width of the result intervals 

Table 6.

The enclosure of the global maximizers for packing 31 points

i
xi
yi

1

[0.1060708146559_16,0.1060708146560_01],
[0.0000000000000_00,0.0000000000000_22]

2

[0.0000000000000_00,0.0000000000000_22],
[0.1899363218792_92,0.1899363218793_25]

3

[0.1103465838237_57,0.1103465838238_38],
[0.3774208693204_81,0.3774208693205_41]

4

[0.000000000000_000,0.000000000000_148],
[0.5649054167616_64,0.5649054167617_52]

5

[0.0000000000000_00,0.0000000000000_36],
[0.7824527083807_88,0.7824527083808_76]

6

[0.0000000000000_00,0.0000000000000_88],
[0.9999999999999_13,1.0000000000000_00]

7

[0.217525087176_831,0.217525087177_171],
[0.186828181031_627,0.186828181031_845]

8

[0.2206554324665_92,0.2206554324666_52],
[0.5649276212040_19,0.5649276212040_45]

9

[0.2175472916191_24,0.2175472916191_60],
[0.7824527083808_51,0.7824527083808_76]

10

[0.2175472916191_24,0.2175472916192_12],
[0.9999999999999_75,1.0000000000000_00]

11

[0.328979359697_667,0.328979359698_338],
[0.000000000000_000,0.000000000000_129]

12

[0.3278716710005_90,0.3278716710006_70],
[0.3743127284729_90,0.3743127284730_58]

13

[0.439325943521_455,0.439325943521_771],
[0.187484547441_183,0.187484547441_420]

14

[0.4381805196434_27,0.4381805196435_05],
[0.5618194803564_98,0.5618194803565_73]

15

[0.4350723787959_55,0.4350723787960_05],
[0.7793445675333_30,0.7793445675334_20]

16

[0.4350945832382_48,0.4350945832383_25],
[0.999999999999_877,1.000000000000_000]

17

[0.549672527345_206,0.549672527345_397],
[0.0000000000000_00,0.0000000000000_50]

18

[0.5_69997950979352,0.6_11243121634352],
[0.3_88756547950396,0.4_30001290371418]

19

[0.6225791306794_61,0.6225791306795_21],
[0.8896534161761_72,0.8896534161762_49]

20

[0.656865616334_467,0.656865616334_787],
[0.189305218532_634,0.189305218532_913]

21

[0.6256872715269_44,0.6256872715270_02],
[0.672128328999_314,0.672128328999_416]

22

[0.7_66888790693767,0.7_84360116798573],
[0.0_00000000000000,0.0_28744823250302]

23

[0.810694781467_086,0.810694781467_316],
[0.343134383665_284,0.343134383665_530]

24

[0.812515452558_638,0.812515452558_813],
[0.560674056478_302,0.560674056478_535]

25

[0.813171818968_167,0.813171818968_404],
[0.782474912822_919,0.782474912823_169]

26

[0.8100636781206_69,0.8100636781207_12],
[0.9999999999999_85,1.0000000000000_00]

27

[0.9_76779422158677,1.0_00000000000000],
[0.0_00000000000000,0.0_16475699215404]

28

[0.9_87877831772954,1.0_00000000000000],
[0.2_16908432391140,0.2_32791951566360]

29

[0.9999999999999_58,1.0000000000000_00],
[0.450327472654_608,0.450327472654_788]

30

[0.999999999999_868,1.000000000000_000],
[0.671020640301_839,0.671020640302_304]

31

[0.9999999999999_78,1.0000000000000_00],
[0.8939291853440_19,0.8939291853440_93]

Open in a new tab

 Underlines indicate the width of the result intervals 

Summary of results

The results of the previous two subsections are summarized as follows: Let
n∈{31,32,33}. Apart from the symmetries of the square, all globally optimal solutions of the problem of packing
n
points are located in the boxes given in Tables 4, 5, and  6, resp. Except the components containing possibly free points and one component for n=32 with the precision of 12 digits, all enclosures are given to the precision of 13–15 digits.

Furthermore, from the result boxes we computed that the enclosure of the global optimum of the problem of packing n points is

f31∗=[0.21754729161912_43,0.21754729161912_80],w(f31∗)≈4·10-15,f32∗=[0.21317456258987_64,0.21317456258987_79],w(f32∗)≈1·10-15,f33∗=[0.21132838414326_31,0.21132838414326_45],w(f33∗)≈1·10-15,

resp., that is, the exact global optima differ from the currently best known function values by at most w(fn∗).

The total CPU time required for solving the three instances was approximately 26, 61, and 13 hours, resp., instead of the months of CPU time estimated by the earlier method [6]. Although it is very hard to compare the performance of the present and that of the former interval-based computer aided proofs (since different problems have been solved on different hardware-software architectures), below we give a rough estimate for the improvement: If we use the number of total tile combinations to represent the overall hardness of a problem instance, and take the time needed to solve n=28,29,30, we find that the new solution procedure tackled n=31,32,33 about 255, 93, and 165 times faster than it was predicted with the use of the former method. The speedup between the present hardware-software environment and that of in [6] (Intel P4 1400 MHz CPU and the Profil/BIAS interval library [17]) is about 2.5 for interval operations, the algorithms the most depending on (this number somewhat include the compiler improvements as well). Thus if we correct the above time ratios with this number, we obtain that the performance of the new method was roughly 40 to 100 times better than that of the predecessor method.

Figure 5 shows the optimal packings for n=31,32,33, transformed to the visually more attractive circle packing problem. (Due to the high precision enclosures the centers appears as points.) In the figure the shaded circles are the free ones. The center of two circles (or a center and a side of the square) is connected if their interval distance is so that they may touch each other in an optimal solution. On the other hand, if they are not connected, then they certainly do not touch each other in any optimal solution. The depicted packings are actually identical to those of the best found ones so far [13], so the displayed possible touchings are indeed touchings in those configurations.
Conclusions and future work

In this work an interval based optimization method was presented for solving circle (point) packing problems. A similar former method was revisited and improved, and with the new algorithm the open problem instances n=31,32,33 have been solved to global optimality. High precision enclosures were given for all optimal solutions and the global optimum value in all three cases. The most important contributions that led to the success of the new method were the following:

We introduced a new, mathematically rigorous representation of polygons, and presented a new area elimination method that resulted in a simpler implementation, easier proof of correctness, and faster source code than its predecessor.

We implemented the key part of the area elimination method in two versions: a faster one with more overestimation, to be used in the initial phases of the proof, and a second one with reduced overestimation, to provide high precision final enclosures.

For the global phase (devoted to reduce the number of tile combinations) we
Used advanced basic data structures (based on bitsets) for the fast manipulation and search of tile combinations;

Extended the previous tile reduction tools with two more, one for bounding the number of tiles in a subregion by an already known optimal packing of lower dimension, and one for utilizing the partial results of a higher problem instance when solving the previous one;

Employed more thorough symmetry filtering and tile pattern matching techniques than before;

 so that with these tools we were able to reduce the number of global phases from three to two, as compared to the former method.

It is strongly believed that with simple modifications of the current method, the instances n=34,35 can also be tackled with similar computing efforts. This would close the gap in the solved problem instances (up to now, the cases 2,⋯,9,14,16,25, and 36 are solved by hand, and every other instance n<36 except n=34,35 are solved on a computer), which would be a milestone in the half-century old history of solving these problems. Furthermore, the interval polygon structure is designed in such a way that it can be generalized for solving similar problems, for example point packing problems on the sphere.
Funding

Open access funding provided by University of Vienna.
Data availibility

Data sharing not applicable to this article as no datasets were generated or analysed during the current study.
Footnotes

This work was supported by the Austrian Science Fund (FWF) Grant No. P25648-N25.

The original article has been revised: Open access funding provided by University of Vienna has been added as funding note.

Publisher's Note

Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

References

1.Szabó PG, Markót MC, Csendes T, Specht E, Casado LG, García I. New Approaches to Circle Packing in a Square. US: Springer; 2007. [Google Scholar]

2.de Groot, C., Monagan, M., Peikert, R. Würtz, D.: Packing circles in a square: review and new results. In P. Kall (ed.), System Modeling and Optimization (Proc. 15th IFIP Conf. Zürich, 1991), Lecture Notes in Control and Information Services 180, pp. 45–54 (1992)

3.de Groot, C., Peikert, R., Würtz, D.: The optimal packing of ten equal circles in a square, IPS Research Report 90–12. ETH, Zürich (1990)

4.Peikert R. Dichteste Packungen von gleichen Kreisen in einem Quadrat. Elem. Math. 1994;49:17–25. [Google Scholar]

5.Nurmela KJ, Östergård PRJ. More optimal packings of equal circles in a square. Discret. Comput. Geom. 1999;22:439–457. doi: 10.1007/PL00009472. [DOI] [Google Scholar]

6.Markót MC, Csendes T. A new verified optimization technique for the “packing circles in a unit square" problems. SIAM J. Optim. 2005;16:193–219. doi: 10.1137/S1052623403425617. [DOI] [Google Scholar]

7.Hansen E. Global Optimization using Interval Analysis. New York: Marcel Dekker; 1992. [Google Scholar]

8.Moore RE, Kearfott RB, Cloud MJ. Introduction to Interval Analysis. Philadelphia: SIAM; 2009. [Google Scholar]

9.Ratschek H, Rokne J. New Computer Methods for Global Optimization. Chichester: Ellis Horwood; 1988. [Google Scholar]

10.Markót MC. An interval method to validate optimal solutions of the “packing circles in a unit square" problems. Central Eur. J. Oper. Res. 2000;8:63–78. [Google Scholar]

11.Nurmela,K.J., Östergård, P.R.J. : Optimal packings of equal circles in a square. In Y. Alavi, D.R. Lick, and A. Schwenk (eds.): Combinatorics, Graph Theory, and Algorithms (Proc. 8th Quadrennial International Conference on Graph Theory, Combinatorics, Algorithms, and Applications), pp. 671–680 (1999)

12.Markót MC, Csendes T. A reliable area reduction technique for solving circle packing problems. Computing. 2006;77:147–162. doi: 10.1007/s00607-005-0155-x. [DOI] [Google Scholar]

13.http://www.packomania.com, maintained by Eckard Specht

14.Hofschuster, W., Krämer, W.: C-XSC 2.0: A C++ library for extended scientific computing. In: Numerical Software with Result Verification, Lecture Notes in Computer Science 2991, pp. 15–35 (2004)

15.Graham RL, Lubachevsky BD. Repeated patterns of dense packings of equal disks in a square. Electron. J. Combin. 1996;3(R16):211–227. [Google Scholar]

16.Boll DW, Donovan J, Graham RL, Lubachevsky BD. Improving dense packings of equal disks in a square. Electron. J. Comb. 2000;7(R46):1–9. [Google Scholar]

17.Knüppel, O.: PROFIL: Programmer’s runtime optimized fast interval library. Bericht 93.4., Technische Universität Hamburg-Harburg (1993)

Associated Data

This section collects any data citations, data availability statements, or supplementary materials included in this article.

Data Availability Statement

Data sharing not applicable to this article as no datasets were generated or analysed during the current study.

 ACTIONS

 View on publisher site

 PDF (599.3 KB)

 Cite

 Collections

 Permalink

 PERMALINK

 Copy

 RESOURCES

 Similar articles

 Cited by other articles

 Links to NCBI Databases

 Cite

 Copy

 Download .nbib
 .nbib

 Format:

 AMA

 APA

 MLA

 NLM

 Add to Collections

 Create a new collection

 Add to an existing collection

 Name your collection
 *

 Choose a collection

 Unable to load your collection due to an error

 Please try again

 Add

 Cancel

 Back to Top