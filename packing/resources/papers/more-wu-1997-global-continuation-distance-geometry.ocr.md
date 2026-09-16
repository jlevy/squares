~ oof fine /ines/fF--
ARGONNE NATIONAL LABORATORY
9700 South Cass Avenue
a oon Argonne, Ilinois 60439
RECEIVED
Allg 12 1997
GLOBAL CONTINUATION FOR DISTANCE GEOMETRY
PROBLEMS
Jorge J. Moré and Zhijun Wu MAS ER
Mathematics and Computer Science Division
Preprint MCS-P505-0395
March 1995
DISCLAIMER
This report was prepared as an account of work sponsored by an agency of the United States
Government. Neither the United States Government nor any agency thereof, nor any of their
employees, makes any warranty, express or implied, or assumes any legal liability or responsi-
bility for the accuracy, completeness, or usefulness of any information, apparatus, product, or
Process disclosed, or represents that its use would not infringe privately owned rights. Refer-
ence herein to any specific commercial product, process, or service by trade name, trademark,
manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recom-
mendation, or favoring by the United States Government or any agency thereof. The views
and opinions of authors expressed herein do not necessarily state or reflect those of the
United States Government or any agency thereof.
Work supported by the Office of Scientific Computing, U.S. Department of Energy, under
Contract W-31-109-Eng-38 and by the Argonne Director’s Individual Investigator Program.

a DISTRIBUTION OF THIS DOCUMENT [IS UNLIMITED
The submitted manuscript has been authored (
by a contractor of the U.S. Government
under contract’ No. W-31-109-ENG-38.
Accordingly, the U. S. Government retains a
nonexclusive, royalty-free Sicense to publish
or reproduce the published form of this
contribution, or allow others to do so, for
U. S. Government purposes.

Be ee Citta eee
DISCLAIMER |
Portions of this document mzy be illegible
in electronic image products. Images are
_ produced from the best available original
. document. .
ABSTRACT
Distance geometry problems arise in the interpretation of NMR data and in the deter-
mination of protein structure. We formulate the distance geometry problem as a global
minimization problem with special structure, and show that global smoothing techniques
and a continuation approach for global optimization can be used to determine solutions of
distance geometry problems with a nearly 100% probability of success.
GLOBAL CONTINUATION FOR DISTANCE GEOMETRY
PROBLEMS
Jorge J. Moré and Zhijun Wu
1 Introduction
A molecule with m atoms can be described by specifying the positions 21,...,2m in R®
of all the atoms in the molecule. If we are given bond lengths 6; between a subset S of
the atom pairs, it is important to determine whether there is a molecule that satisfies these
bond length constraints. We pose this problem in terms of finding 71,..., 2, such that
Iti-ajl= 65, (5) €S. (1.1)

If there is no solution z1,...,2Zm, to these constraints, then the bond length specification
must be in error. This can happen, for example, if the triangle inequality

5:5 S bin + 54,3
is violated for atoms {i,j,k} with bond length constraints.

Distance geometry problems that arise in the interpretation of NMR data and in the
determination of protein structure are usually associated with the more general problem of
finding positions 71,...,2m in IR® such that

lg Sllei-ayllSuy, (EI) ES, (1.2)
where 1; ; and u;,; are lower and upper bounds on the distance constraints, respectively.
For surveys of work in this area, see Crippen and Havel [4], Havel [9], Kuntz, Thomason,
and Oshiro [16], and Briinger and Nilges [1]. We do not consider the general problem
(1.2) because the aim of this paper is to show that algorithms based on the continuation
approach for global optimization can be used to determine solutions of (1.1) with a nearly
100% probability of success. The techniques of this paper can be extended to (1.2), but the
theory is not as elegant.

Distance geometry problems are NP-hard. Crippen and Havel [4] proved this result
when all the atoms are restricted to R! by reducing the distance geometry problem to the
set partition problem: Given positive integers s,,...,5m, determine a partition of these
integers in sets S, and Sz such that

> 3; = > Sj.
. ieS1 ieS2

Work supported by the Office of Scientific Computing, U.S. Department of Energy, under Contract

W-31-109-Eng-38 and by the Argonne Director’s Individual Investigator Program.
1
The proof is instructive. Given an instance of the set partition problem, consider a distance
geometry problem in R! with m+ 1 atoms, where
641 = Si, Lotgm, 61m41 = 0.

If the distance geometry problem has a solution, then 6141 = 0 implies that tmii = 21,
and thus m

So (tit1 — 21) = Img1 — 21 = 0.

i=1
Since |z;41—2;| = 3;, the sets S$, = {¢: 2441 — 2; > O} and Sg = {7 : 34; — 2; < 0} solve the
set partition problem. For a general discussion of the complexity of the distance geometry
problem in R?, see Saxe [21].

We formulate the distance geometry problem (1.1) in terms of finding the global mini-
mum of the function ;

f(z) = > way (IIxi - 25)? - 62,) (1.3)

ijeS

where w;,; are positive weights. Clearly, z € IR” solves the distance geometry problem
if and only if f(z) = 0. We could use any global optimization algorithm (see [20], [12],
and [5] for global optimization background) in the search for a global minimum of f, but
these general algorithms do not take advantage of the structure in the distance geometry
problem. Other algorithms used in the solution of distance geometry problems (for example,
Hendrickson [10, 11], Havel [9], and Glunt, Hayden, and Raydan (7, 8]) must also rely on
general techniques, such as multistarts or simulated annealing, to claim convergence to a
global minimizer.

The continuation approach for global optimization hinges on the ability to gradually
transform the original function into a smoother function with fewer local minimizers. An
optimization algorithm is then applied to the transformed function, tracing their minimizers
back to the original function. The idea of transforming a function into a smoother function is
appealing; the main approaches include the diffusion equation method of Piela, Kostrowicki,
and Scheraga [19], the packet annealing method of Shalloway [24, 23], and the effective
energy simulated annealing method of Coleman, Shalloway, and Wu [2, 3]. In the diffusion
equation method the transformation can be written (see [13, 14] for details) in the form

2
a hk. f(y) exp (-H 2) dy, (1.4)
where T is a parameter (time). The smoothing properties of this transformation have been
studied by the researchers in Scheraga’s group, often in connection with the search for
the lowest energy conformation of a molecule (see, for example, [13, 14, 15, 22]). The
transformation used in the packet annealing method and in the effective energy simulated
2
annealing method can be written in the form

aaaAR f.. exp (-42) exp (-[|A“"(y - 2)||?) dy, (1.5)
where Kz is the Boltzmann constant, ¢ is a parameter (temperature), and A is a nonsin-
gular matrix (the sampling scale). Other transformations used in molecular conformation
problems are reviewed by Straub [25]. In this paper we follow the work of Wu [26] by devel-
oping the general properties and use of (1.4) in continuation algorithms for the solution of
large global optimization problems, since this transformation seems to have the strongest
mathematical properties.

We feel that (1.4) is likely to play an important role, not only in the molecular conforma-
tion problem, but in the solution of a wide variety of global optimization problems. For this
reason Section 2 introduces the term Gaussian transform to denote this transformation.
We also illustrate the smoothing properties of the general Gaussian transform on a sim-
ple two-dimensional problem. This example also provides motivation for the continuation
approach.

Section 3 presents some of the more interesting properties of the Gaussian transform.
We study, in particular, the computation of the Gaussian transform for the decomposable
functions. This is an important class of functions because many of the functions that arise
in applications are decomposable. This class of functions was introduced by Wu [26] under
the term generalized multilinear functions; we are using the term decomposable to avoid
confusion with the use of multilinear for a function that is linear in each argument.

Our approach for solving the distance geometry problem is outlined in Sections 4 and 5.
We compute the Gaussian transform of function (1.3) as a special case of more general
results in Section 4, while Section 5 presents the basic ideas behind global continuation
algorithms. We concentrate on an approach based on choosing a predetermined sequence of
smoothing parameters, since this approach already brings out the power of the continuation
algorithm. In future work we plan to address more sophisticated approaches for choosing
the smoothing parameters.

In Section 6 we consider a typical distance geometry problem and compare a basic global
continuation algorithm with a multistart method for global optimization. We are interested
in the solution of problems with a large number of atoms, and thus we performed our
numerical testing on the Argonne IBM SP system. This system has 128 nodes, each node
an IBM RS/6000-370 with 128 MB of memory. Our main conclusion from the numerical
results is that the continuation algorithm finds the solution of the distance geometry problem
in all cases but that the multistart method becomes increasingly unreliable and expensive
as the number of atoms increases. The reliability of the multistart method drops below 10%
for problems with m > 64 atoms. .

3
2 Continuation for Global Optimization

In the continuation approach for global optimization, the original function is gradually
transformed into a smoother function with fewer local minimizers. An optimization al-
gorithm is then applied to the transformed function, tracing the minimizers back to the
original function. In this section we define the transformation and provide motivation for
the continuation approach.

The transformed function depends on a parameter A that controls the degree of smooth-
ing. The original function is obtained if A = 0, while smoother functions are obtained as A
increases.

Definition 2.1 The Gaussian transform (f), of a function f :R® > R is
__1 lly - |)?
(f)a(®) = Saye I. f(y) exp (-te att dy. (2.1)

We are using the term Gaussian transform because we can view (f))(z) as the expected
value of f(z) with respect to the Gaussian density function

1 ilyll?
PCY) = ayn eXP (Wt (2.2)
The value (f),(x) of the Gaussian transformation is an average of f(z) in a neighborhood of
z, with the relative size of this neighborhood controlled by the parameter X. The size of the
neighborhood decreases as \ decreases so that when A = 0, the neighborhood is the center
z. We explore additional properties of the Gaussian transformation in the next section.

We illustrate the transformation process with the problem of finding the global maxi-
mizer for a function that is a linear combination of four Gaussian functions. The function
in the top left corner of Figure 2.1 is of the general form

4 2
L— 2;
fa) = Davexp — zl (2.3)
i=1 9;

where o; = 0.5 for 1 <i < 4, ay = 1.5, and a; = 1 for 1 = 2,3,4; the centers z; are the
vertices of the square [—0.5, 0.5] x [—0.5, 0.5]. As can be seen in Figure 2.1, the function has
four maximizers in [—2, 2] x [—2,2]. The Gaussian transforms of (2.3) for three values of A
also appear in Figure 2.1. The top right corner corresponds to 4 = 0.2, and in the bottom
row we have A = 0.3, 0.4.

Figure 2.1 clearly shows that the original function is gradually transformed into a
smoother function with fewer local maximizers, and that the smoothing increases as \ _
increases. We can view the Gaussian transform of a function as a coarse approximation to
the original function, with small and narrow maximizers being removed while the overall

4
2 1.4 Rr
NI
1s Xr 1 AYX\\
i a LiXiN
fr\\\ 08 as
' a LKXN 2 08 BOSSI
LION 5 HN RAM N
UIA 02 INN, Aen
O sleet eee eee // CTT (x) AANared Vins “Eiiiiims 0 algae Ny, Lif] {X) Nuit WSs Ss
2 +2 2 -2
12 Ry 12
1 AX 1 4)
“Xr
oe LEST os SESE
[PROSSER [SSSA
0.8. LYRCOX \N) 08 CIERRA IN
LSTA LRA
oa My HYSSNNON oA EERO
02 HAN 1 ETHOS
a \\ \\\ ie ; ee TAXON ee
A WO WWW ip Www
° SEE 1 py SSS 1
2-2 2 +2
Figure 2.1: The Gaussian transform of a function. The original function (A = 0) is in the
top left corner, with A = 0.2 in the top right corner, \ = 0.3 in the bottom left corner, and
A = 0.4 in the bottom right corner.
structure of the function is maintained. This property allows an optimization procedure
to skip less interesting local maximizers and to concentrate on regions with average high
function values, where a global maximizer is most likely to be located.

Another point that is apparent from Figure 2.1 is that a continuation process based on
the Gaussian transform will find the global maximizer. In general, we cannot expect that
the continuation process will succeed on an arbitrary function. In particular, the Gaussian
transform eliminates tall, narrow hills; hence, if the global maximizer lies in one of these
hills, the continuation approach is likely to fail.

5
3 The Gaussian Transform
We have defined the Gaussian transform for a function f : R” + R by (2.1). In many cases
it is preferable to make the change of variables y + z + Au in (2.1) to obtain that
(fala) = ay [fle + Au)exp (=lIul?) a 34
Mz) = afi fan SF u)exp (—|lul|*} du. (3.1)
In this section we explore some of the properties of this transformation.
The Gaussian transform is defined for a large class of functions. In particular, the
transformation is defined if f is continuous almost everywhere and if
|f(z)| < Bi exp(G2l|xl|) (3.2)
for positive constants G, and G2. These assumptions guarantee that f is bounded on compact
sets, but allow for unbounded f on R”. In the development that follows, we assume that f
satisfies assumptions (3.2).
An important property of this transformation is that (f), is a linear operator in the
sense that
(af), =a(f)a, (fi + feda = (fda + (f2)a
for any scalar a and functions f,; and fz. Also note that the Gaussian transform of the
identity function is unity; this result depends on the result
+00 &?
/ exp (-§) dé = x'/?),
tore)
More generally, if uw; < f(x) < pe for all z € R”, then wr < (f),(z) < pe also holds for
all z € R”. In particular, this shows that if f is bounded below, then (f), is also bounded
below.
Theorem 3.1 The Gaussian transform (f)) is a continuous function.
Proof. The proof is a direct consequence of general results (see, for example, Lang [17,
Chapter 13]) on the continuity of functions of the form
Lee | h(x, y) dy,
R"
where the mapping h is continuous in z and integrable in y. ll
Theorem 3.1 helps to support our claim that (f), is a smoother version of f. Indeed,
Theorem 3.1 is a special case of a more general result that establishes (f}, as an infinitely
differentiable function. This result can be established by showing that the mapping &
defined by . .
A(z, y) = F(y)pa(z -y);
6
where p) is given by (2.2), is infinitely differentiable with respect to z, and all the derivatives
are integrable.

We now show that if f is convex, the Gaussian transform is also a convex function.
This property is reassuring because it shows that the transformation does not introduce
difficulties if none exist.

Theorem 3.2 If f : R” +> R is convez, then (f}, ts also conver.
Proof. The result follows from (3.1) because the convexity of f implies that

f(az, + (1— a)rq + Au) < af(z, + Au) + (1- @)f(z2 + Au), 0<a<l,
for any z; and z2 in R”.

A serious drawback to the general use of the Gaussian transform for minimization is that
computing (f)) for a general function defined on R” is not possible because this requires
the computation of n-dimensional integrals. However, there is a large class of functions for
which the computation of the Gaussian transform is reasonable.

Definition 3.3 A function f : IR” +> R is decomposable if f can be written in the form
m n
f(z)= >> f(z), fez) = T] fess), (3.3)
k=1 j=l
for some set of functions {f,,;}, where fp: Rw R.

This class of functions was introduced by Wu [26] under the term generalized multilinear
functions; we are using decomposable to avoid confusion with the use of multilinear for a
function that is linear in each argument.

The decomposable functions are of interest with respect to the Gaussian transform
because computing the Gaussian transform of a decomposable function requires the com-
putation of only one-dimensional integrals. Indeed, a computation shows that if f is defined
by (3.3), then

m n
(fya(e) = 30 { T (fes) (2s) J -
k=1 \j=l
Thus, computing (f), for a decomposable function requires the computation of only the
one-dimensional integrals for each (fi,j),-

Table 3.1 shows the Gaussian transformation of several elementary functions. We will
justify the correctness of the entries later; here we note that the Gaussian transform of any
decomposable function with component functions drawn from this table can be calculated
explicitly. For example, using these results, we can show that if f is the general quadratic

f(z) = 427 Qa t+ efx
7
Table 3.1: The Gaussian transformation of elementary functions
(f)a(2)
x Lz
1
Py x? 412
sin(x) | sin(x) exp(—4A?)
cos(z) | cos(z) exp(—4.?)
exp(z) | exp(z) exp(4A*)
for some Q € R"*” and c € R”, then
n
(f)a(z) = 327 QztcTa+ 4 (>> as) (3.4)
t=1
In particular, this shows that (f),(z) = f(x) for linear functions.
Table 3.1 includes only the most commonly occurring functions; there are many other
functions with an easily computable Gaussian transform. For example,
1 x?
IG) = Gaya? (ary)
is the Gaussian transform of f(z) = exp(—z?).
In addition to quadratic functions, the decomposable functions include the polynomial
functions, that is, functions that are linear combinations of terms of the form
at rh? eae xPr,
for arbitrary integer powers p; > 0. The following result is needed to compute (f)) for a
polynomial function.
Theorem 3.4 If f: Rt R is the monic polynomial f(z) = x*, then
[k/2] ai
_ k} r k-2
(F)a(e) = py (a — 2! i) (5) vo
Proof. Since f is a polynomial we can expand f(z + Aw) in (3.1) and obtain that
| Ly yn)” j 2
(M2) = aR LPF Jw ex (-Ilul?) du,
8
and since the integrals with odd powers vanish by symmetry,
[k/2| 2l
1 X
_ (2!) 2i _ tay fl2
(Mle) = Sp Le MAE [wee (-Il?) ae
We can complete the proof if we show that
1 1 (21)!
xia [| wt exp (-Ilul?) du = Sr. (3.5)
This identity can be established by defining Jy; to be the integral in (3.5) and noting that
integration by parts yields
21-1 (21)(21 - 1)
In = 7 hat-2 = aT 2-2
An induction argument, based on this relationship and using the result Ip = 1, shows that
(3.5) holds, and thus completes the proof. &f

Theorem 3.4 was obtained by Kostrowski and Piela [13], but with a completely different
approach. We will elaborate on this point below.

We can extend Theorem 3.4 by noting that if f is analytic, the Taylor series of f(z+Au)
as a function of u converges for all Au. Thus we can proceed as in the proof of Theorem 3.4
to obtain

1 an, A™ 21 2
(Me) = Fa LIM @ ay [tex (-llull?) au.

Hence, (3.5) shows that

+00 1 21 r (21)

(fale) =O 55%) (S) (3.6)

[=0 ~
This relationship holds, in particular, for the functions in Table 3.1. A short computation
shows that this expression justifies the entries in this table.

Expression (3.6) was used by Piela, Kostrowski, and Scheraga [19] to define the trans-
formation for the diffusion equation method. A disadvantage of this definition is that it
requires an analytic f, while (3.1) requires only the integrability of f. On the other hand,
as we have noted, this expression is quite useful for determining the Gaussian transform of
several important functions. In particular, Kostrowski and Piela [13] obtained Theorem 3.4
with this approach.

The Gaussian transform for functions that are related by a scaling or a translation of
the variables can be computed by noting that if

fo(z) = f(az — zr)
for some scalar @ and vector Zo, then
(fo)a(z) = (f)aalax — 20).
9
For example, if f(z) = sin(az), then

(f),(z) = sin(azr) exp (-3(aa)”) ,
This result suggests that (f), tends to dampen the high-frequency components in a function,
since if a is large, then the exponential term produces a larger damping effect. See Wu (26,
Section 4] for a discussion of the effect of the Gaussian transform on the high-frequency
components of a general function.

We have defined the Gaussian transform of a real-valued function f : R”® — R by
(3.1), but this definition extends immediately to vector-valued functions. This remark is
of interest because in addition to transforming the function, we could also transform the
gradient and the Hessian of f. We now show that the Gaussian transform of the gradient
(Hessian) is the gradient (Hessian) of (f),. This result can be deduced by differentiating
under the integral sign in (3.1) to obtain that

1
V(Foala) = pe [Vile + Au) exp (-Ilull?) du = (VA)a(2), (3.7)
which is the desired result for the gradient. If we repeat the process, we obtain that
l
V*(f)a(e) = sag [, V2Fe + Au) exp (-Ilul?) du=(V7A)a(z), (8.8)
so that the Gaussian transform of the Hessian matrix is the Hessian of (f)).

We guarantee the validity of differentiating under the integral sign in (3.8) by assuming

that V?f is continuous almost everywhere and that
V7 F(z)I < 11 exp(rallall) (3.9)
holds for some positive constants 7; and 72. This result requires a technical lemma.
Lemma 3.5 /f f: R° +> R is twice differentiable on R” and (3.9) holds for some positive
constants 7; and y2, then
IV F(z)I] < 26, exp (Aallzll), — [F(z)| S$ 361 exp (Gallzl|) ,
where 6, > max{71, ||Vf(0)|], | f(0)|} and G2 > 2+ 72.
Proof. The standard estimate
IV F(z) — VF(O)|| S$ _sup [|V7F(r2)I| lel,

O<r<1

together with the estimate ||z|| < exp(||z||), implies that
IV F(z)I] < NV F(0)|| + 1 exp (valle) Ill] < 41 + Fr exp((1 + v2)ll2ll),
10
and thus
IV F(2)|| <$ 261 exp ((1 + 72)fleIl),
which is clearly of the desired form. We complete the proof by using this estimate and
repeating the above argument, but with V/ is replaced by f. In this case we obtain
If(2)| < |F(0)| + 241 exp ((1 + 72)Il21)) loll $ G1 + 261 exp((2 + va)llell),
as desired. &

We now show that the assumption (3.9) guarantees that (3.7) and (3.8) hold.
Theorem 3.6 /f f : R” +> R is twice continuously differentiable almost everywhere on IR”
and (3.9) holds for some positive constants y, and 72, then

Vif)x(e) =(VF)a(z), V4 F)a(e) = (Vf) a(z).
Proof. Assumption (3.9) guarantees that the function
ure V7 f(2 + Au) exp (—l}e)?)
is bounded by an integrable function, for any fixed c and A. The validity of (3.8) now
follows from standard results that guarantee differentiation under the integral sign (see, for
example, Lang [17, Chapter 13]). Lemma 3.5 shows that the same argument can be used
to validate (3.7). fl

Theorem 3.6 was stated informally by Wu [26]; the above argument supplies the pieces
needed to give a formal proof of this result. Theorem 3.6 is of interest from a computational
viewpoint because optimization algorithms require the gradient and Hessian of (f)). This
result shows that the gradient and Hessian of (f), are also smooth functions in the sense
that they are obtained by transforming the gradient and Hessian, respectively.

In this section we have concentrated on obtaining explicit expressions for the Gaussian
transform of various functions. We have also experimented with other approaches. In one
of the approaches, the Gaussian transform is approximated by a Gaussian quadrature. This
approach hinges on the ability to evaluate Gaussian integrals efficiently with ORTHOPOL
(Gautschi [6]). Another approach is based on approximating the function by a decom-
posable function and using the Gaussian transform of the decomposable function as an
approximation to the Gaussian transform of the original function. We plan to pursue these
approaches in future work.

4 The Gaussian Transform for the Distance Geometry Problem
Our continuation algorithms for the distance geometry problem are based on the function
2
, OO f(z) = > way (I]ze - e5l|? - 85) (4.1)
ijeS
11
where w;,; are positive weights, and 6;; are distances. Computing the Gaussian transform
of (4.1) is not difficult because f is decomposable. In fact, f is a polynomial function in
the components of x. The development below shows that f has considerable structure and
that this structure can be used to simplify the computation for the Gaussian transform.
In the standard formulation of the distance geometry problem, the components 2; € R°.
We assume that z; € R? because this assumption does not lead to extra complications. We
thus consider the general problem where f is of the form
f(x) = So wishig(ai — 25) (4.2)
ijeS
and h;; : R? + R is defined by
2
his(2) = (loll? - 62;) (4.3)
The following result shows that computing the Gaussian transform of (4.2) requires only
the Gaussian transform on h;,;.
Theorem 4.1 If f: RR” —> R andh: R? +} R are related by
f(z) = (P72),
for some matriz P € R"*? such that P™ P = o7I, then
(f)x(z) = (h)oa(P7 2).
Proof. Define Q € R'"~?)*" such that
1
R=-
s( 2)
is an orthogonal matrix. By definition,
(f)a(z) = —; | h(PT 2 + APTu) exp (—|lull?) du
rr/2 Jpn ,
so that if we make the change of variables u++ Rv in (3.1), we obtain
__! T T 2
(f),(z) = =a f, h(PT2 + APT Ro) exp (—|lell”) dv,
since R is an orthogonal matrix. Now note that P?R = o(I 0), and thus the above
integral reduces to an integral over R?, that is,
__} T 2) 4 T
{f)a(z) = =a i. h({ P* xc + Aov) exp (-Ilel ) dv = (h)g)(P* 2).
i
12
The application of Theorem 4.1 to the distance geometry problem requires that we
specify how the vectors z; are related to x. Let the +th component of the vector xz; be
the c(i, 7) components of x. In other words, c(i, 7) specifies how the components of z; are
stored in z € R”. Another way of defining c(z,j) is by the relationship

[t]G,3) = [zs]:-
With this choice we can set
P= (ec(a,) _ €c(1,5)> sey €c(p,i) ~ ex(0.3))
and obtain P? x = 2; — z;. In particular, PT P = o7 I, where o? = 2.
As an application of these results, note that Theorem 4.1 implies that
(f)(2) = (A) yay (ti — 25).
is the Gaussian transform of f(z) = h(x; — 2;). We can apply this result to the distance
geometry problem, where h is given by (4.3), by computing the Gaussian transform of the
functions f; :R? +> R and fz: IR? + R defined by
f(z) ={l2\?, f(z) = [Iel*.
Since f; is a quadratic,
(fi)a(z) = [zl]? + 3p? (4.4)
is just a special case of (3.4). We now claim that Theorem 3.4 shows that
(f2)(x) = [lzll* + [3 + (p — 1D]A* ||? + Gp(p + 2)A*. (4.5)
We prove (4.5) by noting that .
Pp 2 Pp Pp
(Le) <Dat+L eh).
i=1 t=1 t#3
and thus Theorem 3.4 implies that
P P
(fo)a(z) = D> (a + 3472? + 3a4) + SO ((2? + 4a?)(2? + 4%)).
t=1 tH
Identity (4.5) is now a direct consequence of this expression.
Theorem 4.2 [fh :R? + R is defined by
2
h(x) = (|lell? - 8),
then :
(h)\(2) = h(x) + [3 + (p— 1)]A? eI? + Fp(p + 2)d* — pd? 7.
13
Proof. Since
A(z) = fo(x) — 26° fi(x) + 6,
the result follows from (4.4) and (4.5). I

The computation of the Gaussian transform for the distance geometry problem now

follows from the results that we have obtained.
Theorem 4.3 If f: R” + R is defined by (4.2) and (4.3), then
(f)a(z) = F(z) + SD (2wi,5[3 + - DP Mle: - #1?) +7,
igeS

where y is the constant

1= > (ep t+ 2)A4 — 282,97) wi.5.

ijeS
Proof. Recall that we can write f in the form
i,j€S

where PLP, ; = 071, with o? =2. I

Theorem 4.3 shows that the Gaussian transform of the distance geometry function de-
fined by (4.2) and (4.3) can be computed quite easily. Moreover, this result also shows that
the gradient and the Hessian matrix of the Gaussian transform are also readily computable
at a fractional increase in cost.

We conclude this section by discussing the relationship between Theorem 4.1 and the
anisotropic Gaussian transform defined by Wu [26]. Given a nonsingular matrix A € R”*”,
the anisotropic Gaussian transform of f is defined by

_ 1 -1 2
(Nal2) = Spar gern fan Fo ex (“IIA — 2)1P) a. (4.6)
Clearly, this transformation generalizes Definition 2.2, where A = XJ.

From a computational viewpoint, the anisotropic transformation is important when A
is a diagonal matrix, and is closely related to the isotropic transformation when f is a
decomposable function. In particular, if f is defined by (3.3) and A = diag(A;), then

™m T%
(Foa(z) = D0 | [1 fasda, (es) | -
k=1 \j=l
The following result, a generalization of Theorem 4.1, provides further motivation for the
anisotropic transformation.
14
Theorem 4.4 /f f: R° +> R andh: R? } R are related by
f(a) = h(P*2)
for some matriz P € R"*? such that P™P = D™D, where D is a diagonal matriz, then
(f)x(2) = (h)ap(P*2).
Proof. The proof follows that of Theorem 4.1. In this case we define Q € R'"-?)*” such
that
is an orthogonal matrix, and obtain that
__} T 2\ dy.
(f),\(z) = my I, h(P* « + ADv) exp (= Ile ) dv.
The result now follows from the definition of the anisotropic transformation because the
change of variables y +> z + Du in (4.6) shows that
(h)p(2) = +o [ble + Du)exp (—Ilul?) du
D ar/2 R"

is the anisotropic transformation of h.
5 Continuation Algorithms
The basic idea behind the continuation approach is to trace a curve {z(A): A > 0}, where
each z(A) is a minimizer of (f),. In the simplest approach we choose a sequence {A;} of
smoothing parameters that converges to zero, and compute a minimizer zr, of each (f)),.
A more sophisticated approach is to rely on a differential equation to trace the curve. For
this approach, we define h: R” x R+ R by

A(z, A) = (f)a(z) (5.1)
and note that, since z(A) is a stationary point of (f)),

0, h[x(A), A] = 0.
We now differentiate with respect to to obtain

Ozch{x(A), A}x'(A) + Ayzh[x(A), A] = 0.
This differential equation, together with an initial value zo, defines a curve if the coefficient
matrix 0,,h[z(A), A] is nonsingular. In this paper we concentrate on the approach based on
15
choosing a predetermined sequence of smoothing parameters, since this approach already
brings out the power of continuation algorithms.

We wish to analyse the ideal situation where we are able to determine a global minimizer
zy of (f),, for some sequence {A,} converging to zero. This requires that we show that
the function h: R” x Re R defined by (5.1) is continuous on R” x R. Without loss of
generality we show continuity at (z*,0). We had previously noted the continuity of A with
respect to z and 4; we now establish the joint continuity with respect to (zx, .).

Lemma 5.1 Assume that f : R” + R is continuous on R” and satisfies (3.2). If {x,}
converges to x* and {Ax} converges to zero, then
lim _(f)aa(2e) = S(2*).
Proof. Let B, be the ball of radius r centered at the origin, and let C, be the complement
of B,, that is,
C, = {2 €R*: [lel] > r}.

We first show that for any « > 0 we can choose r > 0 and kg so that

[, lelen + daw) - f(a) exp (Ilul?) duce, b> ho. (5.2)
Assumption (3.2) implies that there is a constant yu > 0 such that

[f(ae + Anu) — f(2")| < wexp CAzllull),
and since Allul| < 4/lul|* for \ < § and |lul] > 1,
J flee + Ava) = f2)Lexp (-llulP?) du su exp (-Hlul?) du
Cr fom

if A, < i and r > 1. This estimate proves (5.2) because, if r is sufficiently large, the integral
of exp (—4llell?) over C’, is arbitrarily small. Now note that the continuity of f at z* shows
that for given r and ko we can choose k; > ko so that

i |f(ze + Agu) — f(z*)| exp (—le(!?) du <e, k> ky.
This estimate and (5.2) imply that

K(f )a, (te) _ f(z*)| < 2e, k> ky,

which is the desired result.

A variation on Lemma 5.1 would be to show that the gradient and Hessian matrix of h
are continuous. The proof of this variation would be entirely similar to that for Lemma 5.1.

16
Theorem 5.2 Assume that f : RR” > R is continuous on R” and satisfies (3.2). Let {Ax}
be any sequence converging to zero. If x, is a global minimizer of (f),, and {xx} converges
to x*, then x* is a global minimizer of f.
Proof. Since z, is a global minimizer of (f),,,
(F)ac(te) S (f(t), «ER.
Lemma 5.1 now implies that f(z*) < f(z) for any z € R”. Hence, z* is a global minimizer
of f. i
Given A,, we need an algorithm to determine a minimizer z; of (f),,. A trust region
version of Newton’s method based on the work of Moré and Sorensen [18] is an attractive
choice because it has strong global and local convergence properties.
At each iteration of a trust region Newton method for the minimization of f: R" + R,
we have an iterate z,, a bound Ax, a scaling matrix D;,, and a quadratic model gq, : R® > R
of the possible reduction f(z,+w)— f(2,) for || D,wl| < Ay. The developments in Section 4
show that the gradient and Hessian matrix can be easily obtained for the distance geometry
problem. Thus
= T 1,,.Tw2
gw) = Vi(re) w+ gw V*f(2,)w
is our choice for the quadratic model.
An important ingredient in a trust region method is the choice of step s,. In general 3;
is an approximate solution to the trust region subproblem
min {q.(w) : ||Dew|| < Ax}
with 9z(s,) < 0. We use the algorithm described by Moré and Sorensen [18] because it
provides an approximate global solution to the subproblem. In particular, if x; is a saddle
point so that Vf(z,) = 0 and V?f(z,) is indefinite, we still have q,(s,) < 0.
Given the step s,, the test for acceptance of the trial point rz, + s, depends on a
parameter 79 > 0. The following algorithm summarizes the main computational steps:
For k = 0,1,..., maxiter
Compute the quadratic model gg.
Compute a scaling matrix D,.
Compute an approximate solution s, to the trust region subproblem.
Compute the ratio p; of actual to predicted reduction.
Set p41 = 24+ Sx if px > No; otherwise set r~41 = re. Update Ax.
Given a step sz such that ||Dzsx|| < A, and g,(s,~) < 0, the rules for updating the iterate
x, and the bound A, depend on the ratio
py = Leet se) = flee) oe
qk(Sk)
17
of the actual reduction in the function to the predicted reduction in the model. See, for
example, Moré and Sorensen [18] for details on these rules.

The trust region method outlined above is attractive for the distance geometry problem
provided the number of molecules m is moderate, say m < 50. For larger problems we can
still use the trust region method provided the set S in (4.1) is sparse and the computation
of the step s, makes use of sparsity. We plan to address this case in future work.

6 Numerical Results
Consider a molecule with m = s? atoms located in the three-dimensional lattice
{(#1, 72,23) :0 < p< s,0<S%< 5, 0<23< s}
for some integer s > 1. Figure 6.1 shows a molecule with 64 atoms (s = 4). We specify an
ordering for the atoms in this molecule by letting atom 7 be the atom at position (71, 22, 73),
where
t=1+i + sig t 87ig.

Given a subset S of the pairwise distances 6;,; between atoms i and j, we consider the
distance geometry problem
where the set S is defined in terms of an integer r by

S = {(4,7):|t-gl <r}. (6.2)
With this definition the set S is sparse in the sense that it contains only rm pairs, out of a
possible m? pairs. Figure 6.2 shows an 8-atom problem defined by a sparse S with r = 3.

The construction of our model problem is realistic in the sense that distance constraints

are imposed only on nearby atoms. A computation shows that for the model problem
1
6:5 S$ (2(s- 1)? +1)? < v2s.
Our construction shows that the distance geometry problem defined by (6.1) and (6.2)
always has at least one solution.

We attack the distance geometry problem by using the global continuation approach to
obtain a global minimum of the function

f(x)= >> (Ihei - 2yll? - 625), (6.3)
(,j)eS
18
LL HH
—ATVAGVAURVA
ee a
ANA (YY
ZAG VE anard
7 iy
ZABVEVEVAns
UA [YAY yY
Z,YYY
Figure 6.1: An example lattice structure of 64 atoms
where 6;; is the distance between atoms i and 7 in the lattice. We need the Gaussian
transform of f and, for the trust region Newton method, the gradient and Hessian matrix
of the transform. Theorem 4.3 shows that
(fya(z) = SD (Iles — all? — 67)? + 107 fxs - z5l]?) +7 (6.4)
(z)eS
is the Gaussian transform of f, where y is a constant. The gradient and Hessian matrix
can be obtained from this expression.
For this problem, to determine 4 so that (f}) is convex, we study the dependence of
(f), on A in terms of the function
h(r) = (7? - 6)" + 10\?r?.
Note that if h is convex, then 2 ++ A(||z; — z;||) is convex, and thus (f)) is also convex. If
we choose X so that A is convex, then
RY (r) = 12r? — 86? + 202?
shows that we must have A > (2)16 = 0.636. In particular, for a fixed value of A, terms
with a smaller 6 have smaller regions of nonconvexity than those with larger values of 6.
Also note that if
2\1/2
A> (2) max {6;,; : (7,7) € S},
then (f)) is convex.
19
Figure 6.2: An example lattice structure with sparse distance constraints

In this paper we have shown that the continuation method has strong theoretical prop-
erties. We now use numerical results to show that the continuation method is superior to
the multistart approach, a standard procedure for finding the global minimizer of f.

We are interested in the solution of problems with a large number of atoms, and thus
we performed our numerical testing on the Argonne IBM SP system. This system has 128
nodes, each node an IBM RS/6000-370 with 128 MB of memory.

In the multistart method we choose a random starting point z, and use the trust region
method from this starting point to determine a local minimizer x}. If x} satisfies

lits- 2-636 AES, (6.5)
for some tolerance ¢, then 2% is declared to be a solution to the distance geometry problem
(6.1), and we terminate the multistart method. If z¥ does not satisfy (6.5), we repeat the
procedure with another starting point. The multistart method fails if (6.5) is not satisfied
after trying ten starting points.

The global continuation method that we use is similar to the multistart method, except
that the continuation algorithm of Section 5 is used to determine a local minimizer 2% of
f. We start the continuation algorithm with the random starting point z, and Ap > 0. We
compute p major iterations, where p is the number of continuation steps. The kth major
iterate xz, is computed by applying a trust region algorithm, with z,_; as a starting point,
to the transformed function (f),,, where

Pp
20
Table 6.1: Performance of the multistart and continuation methods (z, € rand(B))
Table 6.2: Performance of the multistart and continuation methods (z, € 2 rand(B))
Since A, = 0, the final major iterate z, is a local minimizer of f, so we set x} = Zp.

In Tables 6.1 and 6.2 we present the results obtained by the global continuation method
and the multistart method on two sets of starting points. The number of molecules in these
tables are of the form m = s° for 3< s <6. The parameter r in (6.2) was set to r = s?.

Since the solution of the distance geometry problems defined by (6.1) and (6.2) lie in

B={eteER":0<2;,< 8-1},
it is reasonable to choose the starting points randomly in B by setting each component of
the starting point to a random number in (0,s— 1). These results appear in Table 6.1.
Similarly, for the results shown in Table 6.2 we choose the starting point randomly in 2B.

For these results we used Ay = 0.5 and p = 10 continuation steps. (Later we consider
how the performance of the continuation method depends on po and p.)

Performance is measured in terms of the number of function and gradient evaluations,
nfev and ngev, used to find a global minimizer. The results marked by F are the cases
where no global minimizer was found after trying 10 starting points.

We have not included execution times in Tables 6.1 and 6.2 because the distance ge-
ometry problems under consideration give rise to sparse minimization problems, but the /

21
Table 6.3: Probability of success of the multistart and continuation methods
algorithm that we have used does not take advantage of sparsity. Our concern in this pa-
per is mainly with the ability of the continuation method to solve these problems with a
reasonable number of function and gradient evaluations. In future work we will consider
problems with more atoms and the use of algorithms that take advantage of sparsity.

These results show that the continuation method finds a global minimizer in all cases,
and with fewer function and gradient evaluations than the multistart method. Moreover,
the performance of the continuation method seems to be relatively insensitive to the choice
of starting point. The multistart method, on the other hand, requires a large number of
function and gradient evaluations to determine a global minimizer, and is unable to find a
global minimizer for problems with m = 216 atoms. Also note that the performance of the
multistart method seems to be sensitive to the choice of starting point.

The reliability of the continuation and multistart methods can be measured by the
probability of success of these methods, that is, the percentage of successful runs (the
global minimizer is found) in all ten starting points. The results in Table 6.3 clearly show
that the multistart method had little success in finding a global minimizer, especially for
problems with m > 64 atoms. However, the continuation method succeeded 100% in most
of the cases. Even for m = 64, the probability of success is much higher for the continuation
method.

One might wonder why the continuation method was not able to find the global mini-
mizer for m = 64 in all ten runs. A simple answer to this question is that the initial Ap = 0.5
value was too small for smoothing the function in this problem. Therefore, we repeated the
tuns for the problem with m = 64 atoms, but with Ag = 1 and p = 20. The continuation
method then found the global minimizer for all ten starting points.

The results in Table 6.4 compare the average performance of the multistart and the
continuation method when Ap = 1 and p = 20. When m = 64 and z, € rand(B), the
multistart method fails in all cases, so the results in Table 6.4 measure the effort required

~  to-find a local minimizer. In contrast, the continuation method succeeds in all cases, so the
22
Table 6.4: Average performance for the multistart and continuation method (Ap = 1, p = 20)
|
27) 9] 61.2 50.5} 251.1 211.1] 574 98.7 | 240.9 200.9
64 16) 121.1 100.9 | 267.9 212.4] 118.3 98.7 | 272.2 217.0
125 25 | 241.2) 197.3 | 328.4 249.2 | 212.1 176.5) 344.9 265.5
216 36 | 339.7 278.2 | 446.9 340.8 | 341.6 280.2 | 472.6 361.7
z, € rand(B) zs, € 2rand(B)
results measure the effort required to find a global minimizer. This is interesting because,
in general, we expect the effort required to find a global minimizer to be much larger than
the effort needed to find a local minimizer. A similar conclusion is reached when m = 64
and z, € 2rand(B), since in this case the multistart method only succeeds in one case.
When m = 216, the effort (measured by the number of function and gradient evaluations)
required to find a global minimizer is less than 30% more than the effort required to find a
local minimizer.
Acknowledgment. Special thanks go to Paul Bash, Danny Ripoll, and Tamar Schlick for
the time that they spent talking to us about problems in biology and the relevant literature.
Thanks also go to Tom Coleman and Bruce Hendrickson for sharing their experiences with
the distance geometry problem.
References
[1] A. T. BRUNGER AND M. NILGES, Computational challenges for macromolecular struc-
ture determination by X-ray crystallography and solution NMR-spectroscopy, Q. Rev.
Biophys., 26 (1993), pp. 49-125.
[2] T. F. CoLEMAN, D. SHALLOWaY, AND Z. WU, Isotropic effective energy simulated
annealing searches for low energy molecular cluster states, Comp. Optim. Applications,
2 (1993), pp. 145-170.
[3] ——, A parallel build-up algorithm for global energy minimizations of molecular clusters
using effective energy simulated annealing, J. Global Optim., 4 (1994), pp. 171-185.
[4] G. M. Crippen AND T. F. Havel, Distance Geometry and Molecular Conformation,
: , - John Wiley & Sons, 1988.
23
/ -
[5] C. FLouDAS AND P. PARDALOS, eds., Recent Advances in Global Optimization, Prince-
ton University Press, 1992.

[6] W. Gautscul, Algorithm 726: ORTHOPOL - A package of routines for generating
orthogonal polynomials and Gauss-type quadrature rules, ACM Trans. Math. Software,
20 (1994), pp. 21-62. .

. [7] W. Gtunt, T. L. HAYDEN, AND M. RayDaNn, Molecular conformation from distance
matrices, J. Comp. Chem., 14 (1993), pp. 114-120.

[8] ———, Preconditioners for distance matriz algorithms, J. Comp. Chem., 15 (1994),
pp. 227-232.

{9] T. F. HaveL, An evaluation of computational strategies for use in the determination .
of protein structure from distance geometry constraints obtained by nuclear magnetic
resonance, Prog. Biophys. Mol. Biol., 56 (1991), pp. 43-78.

[10] B. A. HENDRICKSON, The molecule problem: Determining conformation from pairwise
distances, PhD thesis, Cornell University, Ithaca, New York, 1991.

{11] ———, The molecule problem: Exploiting structure in global optimization, SIAM J. Op-
timization, (1995). To Appear.

[12] R. Horst anD H. Tuy, Global Optimization, Springer-Verlag, 1990.

[13] J. KosTROwIcKI AND L. PIELA, Diffusion equation method of global minimization:
Performance for standard functions, J. Optim. Theory Appl., 69 (1991), pp. 269-284.

{14] J. KosTrowick!, L. PIELA, B. J. CHERAYIL, AND H. A. SCHERAGA, Performance of
the diffusion equation method in searches for optimum structures of clusters of Lennard-
Jones atoms, J. Phys. Chem., 95 (1991), pp. 4113-4119.

. KOSTROWICKI AND H. A. SCHERAGA, Application of the diffusion equation metho

[15] J. K H.A.S Application of the diffusi J hod
for global optimization to oligopeptides, J. Phys. Chem., 96 (1992), pp. 7442-7449.

{16] I. D. Kuntz, J. F. THOMASON, AND C. M. OsuirRo, Distance geometry, in Methods
in Enzymology, N. J. Oppenheimer and T. L. James, eds., vol. 177, Academic Press,
1993, pp. 159-204.

[17] S. LANG, Real Analysis, Addison-Wesley, second ed., 1983.

{18] J. J. Moré ano D. C. SORENSEN, Computing a trust region step, SIAM J. Sci.
Statist. Comput., 4 (1983), pp. 553-572.

24
-_ t nm :

[19] L. PreLa, J. KoSTROWICKI, AND H. A. ScHERAGA, The multiple-minima problem in
the conformational analysis of molecules: Deformation of the protein energy hypersur-
face by the diffusion equation method, J. Phys. Chem., 93 (1989), pp. 3339-3346.

[20] A. H. G. Rinnooy Kan anpb G. T. TiMMkER, Global optimization, in Optimization,
G. L. Nemhauser, A. H. G. Rinnooy Kan, and M. J. Todd, eds., North-Holland, 1989,
pp. 631-662.

[21] J. B. SAXE, Embeddability of weighted graphs in k-space is strongly NP-hard, in Proc.
17th Allerton Conference in Communications, Control and Computing, 1979, pp. 480—
489.

[22] H. A. SCHERAGA, Predicting three-dimensional structures of oligopeptides, in Reviews
in Computational Chemistry, K. B. Lipkowitz and D. B. Boyd, eds., vol. 3, VCH
Publishers, 1992, pp. 73-142.

[23] D. SHALLOWAY, Application of the renormalization group to deterministic global min-
imization of molecular conformation energy functions, J. Global Optim., 2 (1992),
pp. 281-311.

[24] D. SHALLOWAY, Packet annealing: A deterministic method for global minimization,
application to molecular conformation, in Recent Advances in Global Optimization,
C. Floudas and P. Pardalos, eds., Princeton University Press, 1992, pp. 433-477.

[25] J. E. Srraus, Optimization techniques with applications to proteins, preprint, Boston
University, Department of Chemistry, Boston, Massachusetts, 1994.

[26] Z. Wu, The effective energy transformation scheme as a special continuation approach
to global optimization with application to molecular conformation, Preprint MCS-P442-
0694, Argonne National Laboratory, Argonne, Llinois, 1994.

25
