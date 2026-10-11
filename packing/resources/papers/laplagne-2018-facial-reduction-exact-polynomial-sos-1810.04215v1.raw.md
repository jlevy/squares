                                             FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF
                                                        SQUARES DECOMPOSITIONS
arXiv:1810.04215v1 [math.AG] 9 Oct 2018




                                                                            SANTIAGO LAPLAGNE


                                                  Abstract. We study the problem of decomposing a non-negative polynomial
                                                  as an exact sum of squares (SOS) in the case where the associated semidefinite
                                                  program is feasible but not strictly feasible (for example if the polynomial
                                                  has real zeros). Computing symbolically roots of the original polynomial and
                                                  applying facial reduction techniques, we can solve the problem algebraically
                                                  or restrict to a subspace where the problem becomes strictly feasible and a
                                                  numerical approximation can be rounded to an exact solution.
                                                      As an application, we study the problem of determining when can a rational
                                                  polynomial that is a sum of squares of polynomials with real coefficients be
                                                  written as sum of squares of polynomials with rational coefficients, and answer
                                                  this question for some previously unknown cases. We first prove that if f is
                                                  the sum of two squares with coefficients in an algebraic extension of Q of
                                                  odd degree, then it can always be decomposed as a rational SOS. For the
                                                  case of more than two polynomials we provide an example of an irreducible
                                                                                                                         3
                                                                                                                         √
                                                  polynomial that is the sum of three squares with coefficients in Q( 2) that
                                                  cannot be decomposed as a rational SOS.




                                                                              1. Introduction
                                             Decomposing a non-negative polynomial on Rn as a sum of squares is a classical
                                          problem. In 1888, D. Hilbert proved in a famous paper [3] that every non-negative
                                          polynomial in n variables and even degree d can be represented as a sum of squares
                                          of other polynomials if and only if either (a) n = 1 or (b) d = 2 or (c) n = 2
                                          and d = 4. The first explicit example of a non-negative polynomial that cannot be
                                          written as a sum of squares was found by T. Motzkin [9] in 1967. His example is
                                          f = x4 y 2 + x2 y 4 − 3x2 y 2 + 1.
                                             Recently, the algorithmic problem of determining whether a real polynomial is
                                          decomposable as a sum of squares, and if so to compute such a decomposition, has
                                          become an active area of research as new tools have been developed to tackle this
                                          problem. It provides a certificate of non-negativity and has therefore applications
                                          in different areas of mathematics. The strategy usually applied is to pose it as a
                                          semidefinite programming problem, a class of convex optimization problems which
                                          can be efficiently solved by numerical methods. In this setting, computing a sum of
                                          squares (SOS) decomposition is equivalent to finding a positive semidefinite matrix
                                          in a space of symmetric matrices.
                                             Using available software packages one can compute a numerical approximation
                                          to a solution, when it exists. In theoretical and practical applications, it is often
                                          desirable to obtain exact rational or algebraic solutions. In [11], H. Peyrl and P.
                                          Parrilo study how to construct a rational solution from a numerical approximation.
                                          Their method is applicable when the associated semidefinite program is strictly
                                          feasible, that is, if it admits a positive definite solution. In that case, they can round
                                                                                        1
2                               SANTIAGO LAPLAGNE


the solution to a sufficiently close rational point that preserves the positiveness of
the eigenvalues of the associated matrix.
   That strategy fails when the SDP is feasible but not strictly feasible. In the
presence of null eigenvalues there is no direct way to round the numerical solution
assuring that the eigenvalues close to zero become exact zeros. In some cases, for
example if the original polynomial has real roots, a positive definite solution cannot
exist and hence their method cannot be applied. In our work, using as a starting
point a suggestion in that paper, we extend their algorithm reducing the dimension
of the underlying search space, a technique called facial reduction. Combining the
restrictions imposed by the real zeros with other restrictions given by the properties
of the solution we are looking for, we are able to solve the problem in cases where
the previous algorithm could not succeed.
   As an application, we study the problem of determining when can a rational
polynomial that is a sum of squares of polynomials with coefficients in an algebraic
extension K of Q be written as sum of squares of polynomials with rational coeffi-
cients. This question was originally raised by B. Sturmfels. It is a natural question
in the context of polynomial optimization where one is interested in knowing in
which cases numerical solutions can be rounded to provide exact certificates.
   A first general result for this problem was given by C. Hillar [4], who showed that
the question has a positive answer when K is totally real. In [13], C. Scheiderer
gave the first family of counterexamples of polynomials that are the sum of squares
of polynomials with real coefficients that cannot be decomposed as rational SOS.
The examples in his work are obtained by multiplying pairs of conjugate linear
forms and are hence always sum of two squares over an extension K of Q of even
degree. In Section 5 of the referred paper, he posed some open questions. We are
interested in Question 5.3: let K be a number field of odd degree, and assume that
a form f is a sum of squares over K. Then is f a sum of squares over Q? In Section
4 we prove that this is indeed the case if f is the sum of two squares. In Section
5 we provide a negative answer to this question in the general case, providing an
explicit polynomial that is the sum of three squares of polynomials with coefficients
in an extension of Q if degree 3 that cannot be written as a sum or rational squares.
The counterexample we construct gives also a negative answer to Question 5.1: Are
there examples that are irreducible over C? The examples Scheiderer constructs are
products of linear forms and this simple structure allows him to prove his results.
For the case of irreducible polynomials there were no tools available to tackle the
problem, and this is what made the question relevant.
   For the implementation of our algorithms, we need to be able to work sym-
bolically with roots of systems of polynomials. For that purpose we use Maple
software [6] which can work efficiently in algebraic extension of the rational num-
bers. Linking Maple with Matlab [7] and SEDUMI [14] (a software for optimization
over symmetric cones) we combine symbolic and numerical methods to get a very
general and easy to use software package which we call rationalSOS.
   The main contributions in this paper are: algorithms to write a non-negative
polynomial with real roots as an exact sum of squares (Section 3) together with
a Maple package implementation of the algorithms; a proof that all rational poly-
nomials that can be written as sum of two polynomials with coefficients in an
algebraic extension of Q of odd degree can be written as a sum of squares of poly-
nomials with rational coefficients (Section 4); and new examples of non-negative
 FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF SQUARES DECOMPOSITIONS 3


polynomials with rational coefficients that are sum of squares of polynomials with
non-rational coefficients that cannot be written as sum of squares of polynomials
with rational coefficients (Section 5).

                         2. Preliminaries and notation
2.1. Sum of squares (SOS) decomposition. Let K[x] = K[x1 , . . . , xn ] be the
ring of polynomials with coefficients in a field Q ⊆ K ⊆ R. We use the multi-
index α ∈ Zn+ to denote the monomial xα = xα              αn
                                                 1 . . . xn and define the degree of
                                                   1

  α
x to be |α|= α1 + · · · + αn . A polynomial f ∈ K[x1 , . . . , xn ] that is non-negative
over Rn can always be homogenized adding a new variable without modifying the
non-negativity, and any SOS decomposition for one case can be easily modified
to the other case, therefore in this paper we will always work with homogeneous
polynomials, which are usually called forms.
    For a polynomial f ∈ K[x], we note fα the coefficient of xα in f . Let Md denote
the set of exponents of monomials of degree d: Md = {α ∈ Zn≥0 : |α|= d}. We note
md := |Md |, or simply m when d is clear, the number of monomials of degree d.
    We say that a non-negative f P ∈ K[x] admits a SOS (sum of squares) decompo-
                                     r
sition if it can be written as f = i=1 p2i for some pi ∈ R[x], 1 ≤ i ≤ r, and we say
that f admits a rational SOS decomposition if we can take pi ∈ Q[x], 1 ≤ i ≤ r.
This is equivalent to the existence of ci > 0 ∈ Q and pi ∈ Q[x], 1 ≤ i ≤ r, such that
                                          r
                                          X
                                     f=         ci p2i ,
                                          i=1

because any rational number p/q can be written as the sum of pq times (1/q)2 (it
can however change the number of polynomials required for such decomposition).
We will usually work with the latter decomposition in this paper, which is more
consistent with the matrix factorization tools we will use.
Remark 2.1. Let C(f ) := conv({α | fα 6= 0}) be the convex hull of the exponents
set of f . B. Reznick proved in [12] that only monomials with exponents contained
in 12 C(f ) can appear in a SOS decomposition. In particular, if f is homogeneous
of degree 2d, then the polynomials pi , 1 ≤ i ≤ r, in the SOS decomposition must
be homogeneous polynomials of degree d.
2.2. The semidefinite programming (SDP) formulation. Let S m ⊂ Rm×m
be the space of symmetric matrices. A matrix A ∈ S m is called positive semidefinite
if v t Av ≥ 0, ∀v ∈ Rm , and it is called positive definite if v t Av > 0, ∀v ∈ Rm \ {0}.
We call S0m and S+  m
                      the subsets of S m of positive semidefinite and positive definite
matrices respectively.
    Starting with a form f ∈ R[x1 , . . . , xn ] of degree 2d we first recall how to pose
the problem of computing a SOS decomposition as a semidefinite programming
problem. We express the given polynomial as a quadratic form
(2.1)                             f (x) = v(x)t Qv(x),
where v(x) is the vector of all monomials of degree d, i.e., vα (x) = xα , α ∈ Md , and
Q ∈ S Md (the set of symmetric matrices with rows and columns indexed by the
elements in Md ). Since the components of v(x) satisfy algebraic relations, Q is in
general not unique and formula (2.1) gives a set of linear equations for the entries
4                                 SANTIAGO LAPLAGNE


of Q. Hence the set of all matrices Q for which (2.1) holds is an affine subspace of
the set of symmetric matrices. We denote this affine subspace by
                         L := {Q ∈ S Md |f (x) = v(x)t Qv(x)},
and LQ := L ∩ Qmd ×md . The connection between SOS decompositions and the
space L is given by the following lemma (see [8, p.106] and [11]):
Lemma 2.2. Let f (x) ∈ R[x]. Then f (x) admits a SOS decomposition if and
only if there exists a positive semidefinite matrix Q ∈ L. Moreover, f (x) admits a
rational SOS decomposition if and only if there exists a positive semidefinite matrix
Q ∈ LQ .
   By this lemma, we can pose the problem as a semidefinite program (SDP), a
class of convex optimization problems. The advantage is that SDPs can be effi-
ciently solved by interior point methods, which makes SOS problems computation-
ally tractable. There are several numerical solvers that can compute effectively a
positive semidefinite matrix in L. We use SEDUMI [14] in our implementation.
Example 2.3. Let f (x, y) = 10x4 + 2x3 y + 27x2 y 2 − 24xy 3 + 5y 4 ∈ R[x, y]. Solving
Equation (2.1) we get
                                                               2
                                      10        1         a        x
             f (x, y) = x2 xy y 2  1 −2a + 27 −12 xy 
                                  
                                       a      −12         5        y2
for any a ∈ R. Hence L = {W (a) : a ∈ R}, with W (a) the 3 × 3 matrix in the
identity above. There existes a SOS decomposition of f if and only if there exists
a ∈ R such that W (a) is positive semidefinite.
   H. Peyrl and P. Parrilo [11] studied the problem of computing exact rational
SOS decompositions. If the SDP problem is strictly feasible, that is, if it admits
a positive definite solution, a numerical solver that maximizes the value of the
minimum eigenvalue will compute a positive definite solution matrix if it exists. In
that case, one expects that the approximation computed can be rounded to a close
enough rational solution that does not change the positivity of the eigenvalues.
If the problem is feasible but not strictly feasible, that is, it admits a positive
semidefinite matrix solution but not a positive definite one, then rounding the
approximate solution is likely to introduce negative eigenvalues.
   In our work, to tackle this problem, we add linear restrictions to the search space
in order to reduce the dimension. We expect to find a space where the problem
becomes strictly feasible and an approximate solution can be rounded to an exact
solution. For simplicity, we will work with linear affine parametrizations of the
resulting subspaces (also called image representations in [11, Section 3.2]). For
example, matrix W (a) in Example 2.3 is a parametrization of L.
   For any parametrization W (a1 , . . . , as ) of L or a linear subspace, we can com-
pute its rank as a matrix in R[a1 , . . . , as ]md ×md . This rank is independent of the
parametrization chosen and it is equal to the maximum rank over all possible spe-
cializations of the parameters. For short, we will from now on refer to the rank and
kernel of a parametrization of L (or a subspace) as the rank and kernel of L (or
the subspace). The set of values of the parameters for which the maximum rank
is attained is open and dense in the space of all possible values, hence by giving
random values to the parameters we can almost always compute the correct rank.
This is more efficient than computing the rank of the matrix in R[a1 , . . . , as ]md ×md .
 FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF SQUARES DECOMPOSITIONS 5


Example 2.4. (See [5, Worksheet A] for the computations in Maple.) Let
   f (x, y, z) = 10x4 + 6x3 y − 22x3 z + 39x2 y 2 − 24x2 yz +
                   33x2 z 2 − 20xy 2 z + 8xyz 2 − 20xz 3 + 25y 4 + 10y 3 z + y 2 z 2 + 4z 4 .
   Solving the equations for the entries of Q from (2.1), indexing the columns by
v = (x2 , xy, xz, y 2 , yz, z 2), we get the parametrization of L:

(2.2)
                   10              3            −11        a1,4   −12 − a2,3       a1,6
                                                                                          

            3                  39 − 2 a1,4      a2,3        0     −10 − a3,4    4 − a3,5 
                                                                                        
      
                                                                                        
         −11                     a2,3       33 − 2 a1,6   a3,4      a3,5         −10 
   W =
                                                                                        
                                                                                         
      
         a1,4                     0            a3,4       25           5         a4,6  
       −12 − a2,3           −10 − a3,4         a3,5        5     1 − 2 a4,6       0
                                                                                        
                                                                                         
                  a1,6          4 − a3,5        −10        a4,6         0            4
   This matrix has rank 6 (it can be easily computed assigning random values to
the unknowns). To find a SOS decomposition of f , we look for a positive semidef-
inite matrix of this shape. We run the numerical solver SEDUMI to compute an
approximate solution that maximizes the minimum eigenvalue. The output matrix
has the following eigenvalues:
           {−0.5356 × 10−8 , 0.2776 × 10−7 , 4.2732, 16.5132, 28.9722, 46.9092}.
Intuitively, we interpret these values as two null eigenvalues and four positive eigen-
values, that is, a positive semidefinite solution was found. However, there is no
direct way to round the solution matrix so that the approximate zeros become ex-
act zeros. That is, an exact SOS decomposition cannot be directly computed from
the approximate SOS decomposition. We will show how to handle this case in the
following sections, using as a starting point a suggestion given in [11].

                                    3. Facial reduction
   Facial reduction is a general technique to simplify SDPs with no strictly feasible
solution. It was first introduced in [1] and used successfully in many applications.
In our case it can be applied in a very nice and simple way. We recall that the
principle of facial reduction is based on the following result (the nice graphical
presentation is taken from F. Permenter talk [10]).
Lemma 3.1. Fix U ∈ Rm×ℓ . Then

                                                                   X̂           Ut
             X∈S0m
        range X⊂range U   ⇐⇒             X         =       U



for some X̂ ∈ S0ℓ .
   Assume X has rank ℓ and let Ω ⊂ {1, . . . , m} be a set of indices of ℓ linearly
independent columns of X. There exists U as in the lemma such that it is the iden-
tity matrix in the rows indexed by Ω (apply Gaussian elimination to the columns
6                                SANTIAGO LAPLAGNE


indexed by Ω). Hence, if X ∈ S0m has rank ℓ ≤ m, there exists a positive definite
                           ℓ
principal submatrix X̂ ∈ S+   that satisfies the formula of the lemma.
   Our general strategy is then to find linear relations in the space L ∩ S0m that
reduce the rank of the matrices in the search space, so that we can restrict to
a principal submatrix of the parametrization where the associated SDP program
becomes strictly feasible. We can then compute a positive definite solution using a
numerical solver, and plug the values found in the original parametrization matrix
to get a positive semidefinite matrix with ℓ positive eigenvalues and m − ℓ exact
null eigenvalues.
3.1. Real zeros of the polynomial. The first step for facial reduction is based
on the following observation in [11]: let Q ∈ L ∩ S0m and x⋆ ∈ Rn be such that
f (x⋆ ) = 0, then Qv(x⋆ ) = 0. That is v(x⋆ ) is in the kernel of L ∩ S0m . This follows
from the following more general property:
Proposition 3.2. If v ∈ Rm , Q ∈ S0m and v t Qv = 0 then Qv = 0.
  Hence, exact real solutions of f (x) = 0 provide linear restrictions to the search
space that can reduce its dimension.
Remark 3.3. For our facial reduction strategy we need to compute real solutions
symbolically. Since we are assuming the polynomial to be non-negative, the real
solutions must be local minima and we can look for them by solving the system
                                                                
                                 ∂f                   ∂f
                      f (x) = 0,     (x) = 0, . . . ,     (x) = 0 .
                                 ∂x1                  ∂xn
   In our implementation in Maple we use the procedure solve to obtain real
solutions, which computes parametrizations in algebraic extensions of Q of different
branches of solutions, and we look for real points in them. Alternatively, one can
compute the prime components of the above system using primary decomposition
algorithms, and look for real points in them. Computing these exact solutions can
be the bottle neck in some high degree examples. However, we will see in Section 5
and Appendix A that using these techniques we can solve many interesting problems
which are otherwise difficult to handle.
3.2. Algebraic conjugates of the real zeros. Let Q̄ be the algebraic closure of
Q and let x⋆ ∈ (Q̄ ∩ R)n be an algebraic real zero of f . An important observation
when we are looking for rational SOS decompositions, is that for L a minimal
algebraic extension of Q containing all the entries of v(x⋆ ) and G a splitting field
of L, if Q ∈ L ∩ S0m has rational entries,
             0 = f (x⋆ ) ⇒ 0 = Qv(x⋆ ) ⇒ 0 = σ(Qv(x⋆ )) = Qσ(v(x⋆ )),
where σ ∈ Aut(G/Q) and abusing the notation, σ(v) = (σ(v1 ), . . . , σ(vm )) for
v ∈ Lm . That is, σ(v(x⋆ )) ∈ ker(Q) for any σ ∈ Aut(G/Q), and so is any linear
combination of these elements. Of special interest is the following special case.
Proposition 3.4. Let x⋆ ∈ (Q̄∩R)n . Let L be a minimal extension of Q containing
all the entries of v(x⋆ ). Assume Q ∈ LQ ∩ S0m . Then TraceL/Q (v(x⋆ )) ∈ Qm is in
the kernel of Q.
   The importance of this proposition is that it provides a vector with rational
coordinates in the kernel of LQ ∩ S0m , and hence the linear relations derived are
simple and easy to handle. One could alternatively work in the splitting field G of
 FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF SQUARES DECOMPOSITIONS 7


L and add all the equations for the conjugates, but computing a splitting field of
L can be very expensive even for small degree extensions. In contrast, the trace of
elements in L can be easily obtained from the coefficients of the minimal polynomial
of a primitive element for the extension L/Q.
Example 3.5. Carrying on Example 2.4, we look for real solutions of f (x, y, z) = 0.
Using the command solve from Maple to solve the system
                                                                              
                           ∂f                ∂f                ∂f
          f (x, y, z) = 0,    (x, y, z) = 0,    (x, y, z) = 0,    (x, y, z) = 0 .
                           ∂x                ∂y                ∂z
we get the solution:
                                                       
                                 1 3        2
                   γ(t) = t, αt, (α t + 128α + 25α + 73)
                                46
where α is a root of m(Z) = 50Z 4 + 28Z 3 − Z 2 + 23Z − 8. This polynomial has
two real roots.
   We fix t = 1 and use this solution to reduce the dimension of the search space as
explained above. That is, we define L1 = L ∩ {Q ∈ R6×6 : Q.v(s(1)) = 0}. This is
equivalent to solving the system of linear equations given by W.v(s(1)) = 0, where
W is the parametrization of L given in Example 2.4. Solving these equations we
get that the dimension of L1 is 3 and the rank of the parametrization matrix is 5.
   We could now take a principal submatrix of the parametrization of L1 of size
and rank 5 and use SEDUMI to compute numerically a positive semidefinite matrix
in the shape of that principal submatrix. The problem is not strictly feasible, the
solution we get has still an approximate null eigenvalue and we cannot use it to
compute an exact solution to the problem.
   If instead of using the equation W.v(s(1)) = 0 we compute the trace of v(s(1))
for the extension Q(α) ֒→ Q, ṽ = (4, −14/25, 53/10, 221/625, −396/125, 1209/100),
and we solve W.ṽ = 0 for W the parametrization of L, we find that there is only
one solution:
                          10     3    −11 15        3    2
                                                           

                       3        9    −15     0     0    6 
                                                           
                                                           
                       −11 −15 29 −10 −2 −10 
                                                           
                                                           
                       15       0    −10 25        5    0 
                                                           
                       3        0     −2     5     1    0 
                                                           

                         2      6    −10     0     0     4
  Diagonalizing this matrix, we obtain a rational solution to our original problem:
             f = (x2 + 3xy − 5xz + 2z 2 )2 + (3x2 − 2xz + yz + 5y 2 )2
(the decomposition obtained from the matrix is not unique, different diagonaliza-
tions can give different outputs).
3.3. Ghost solutions. In the last subsection we used real zeros x⋆ of f to obtain
elements v(x⋆ ) in the kernel of L ∩ S0m . Based on Remark 3.2, we can in many
cases obtain other elements that must be in that kernel.
   Null entries in the diagonal. If a parametrization matrix W of L (or a
subspace of L obtained after intersecting with some linear restrictions) has a null
value in the diagonal, this is an obstruction for the matrices in L being positive
8                                 SANTIAGO LAPLAGNE


definite, all the entries in the diagonal of a positive definite matrix are positive.
This is an easy to remove obstruction by the following simple lemma.
Lemma 3.6. If Q ∈ S0m×m and Qkk ≡ 0 then etk .Q.ek = 0 and therefore Q.ek = 0,
where ek is the k-th canonical vector.
   Hence, Wkk = 0 gives m − 1 new equations to reduce the dimension of the search
space. Note that all the entries in the k-th row and column of the parametrization
of L∩{Q ∈ Rm×m : Qek = 0} become zero and we can ignore that row and column.
   In practice, it is a common situation that a parametrization matrix has null
values in the diagonal and so this is a very simple and useful technique in the facial
reduction strategy.
   Note that there could be no real point x = (x1 , . . . , xn ) such that v(x) = ek .
That is, we may be using solutions of v t Qv = 0 that do not come from solutions of
f = 0.
   Principal submatrices with zero determinant. The case of the last para-
graph can be extended to any principal submatrix of size ℓ < m with zero determi-
nant.
Lemma 3.7. Let Q ∈ S0m×m and Ω ⊂ {1, . . . , m} be such that det(QΩ ) = 0, where
QΩ is the principal submatrix of Q with rows and columns indexed by Ω. Let ṽ ∈ Rℓ ,
ℓ = |Ω|, be a vector in ker(QΩ ). Let v ∈ Rm be the extension of ṽ to Rm with zeros
in the other entries (that is, vij = ṽj if ij ∈ Ω and vi = 0 if i 6∈ Ω). Then Q.v = 0.
    To apply this lemma, we look for principal submatrices of a parametrization
W of the search space with zero determinant and derive the corresponding linear
restrictions. In practice, searching among all possible principal submatrices for
those with zero determinant can be time consuming, so in our implementation we
consider only 2 × 2 principal submatrices. This usually provides new conditions
and decrease the rank of L.
    Note again that since a parametrization W of L is a matrix with parameters,
if we take large submatrices it can be more efficient to replace the parameters by
random values to determine whether the determinant is zero or not. Also, in theory
it could happen that the vector ṽ in the kernel contains parameters of W , and hence
it cannot be used to get linear relations. However this theoretical situation never
occurred in our examples.
3.4. Rational entries. The last tool we use to reduce the dimension of the space
when we are looking for rational solutions is to force all coefficients of non-rational
numbers in the entries √       of a parametrization matrix
                                                        √ to be 0. For example, if an
entry of the matrix is 2t and another one is 3t, these two entries cannot be
rational at the same time, unless t = 0, hence in this case we can impose t = 0.
Since the entries of the matrix can be more complicated with many unknowns and
different coefficients, it can be difficult to derive these type of restrictions. We
simplify this restriction as follows. Let a = a0 + a1 t1 + · · · + as ts , ai ∈ Q̄ for
0 ≤ i ≤ s, be an entry of the matrix and α a primitive element for the extension
Q(a0 , a1 , . . . , as ) ֒→ Q. That is, we can regard the elements ai as polynomials ai (α)
with rational coefficients. Now we force all the coefficients of the positive powers
of α in a to be zero, and we use the resulting equations to reduce the dimension
                                                  √3
                                                          √
                                                          3  2      √3
                                                                           √
                                                                           3  2
of the problem. For example if a = 1 + ( 2 + 2 2 )t1 + ( 2 + 2 )t2 , we add
the restrictions t1 + t2 = 0 and 2t1 + t2 = 0, from which we derive t1 = t2 = 0.
 FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF SQUARES DECOMPOSITIONS 9


Note that the restrictions we add are not in general necessary conditions, even in
the case of rational solutions, and hence we can be losing solutions. This strategy
turns out to be very effective in practice to find rational solutions, but it cannot
be used if we are trying to find all solutions or prove that there are no rational
solutions. Looking more carefully at the coefficients and the relations among them
we can use this strategy to derive necessary conditions, but we do not carry further
this analysis in this paper.
Example 3.8. (See [5, Worksheet B] for the computations in Maple.) We apply
the above techniques in the following example:
f (x, y, z) = 3618x8 + 468x7 y + 6504x7 z − 1104x6y 2 + 2616x6yz + 57481x6z 2 −
                144x5 y 3 − 1652x5 y 2 z − 16440x5yz 2 + 23420x5 z 3 + 160x4 y 4 +
                1392x4 y 3 z − 2520x4 y 2 z 2 − 28448x4yz 3 + 91320x4 z 4 − 240x3 y 4 z+
                1728x3 y 3 z 2 + 10524x3y 2 z 3 − 85500x3 yz 4 + 34740x3z 5 − 3696x2 y 3 z 3 +
                28920x2 y 2 z 4 − 15192x2yz 5 − 57267x2z 6 + 720xy 4 z 3 − 3312xy 3z 4 −
                3168xy 2 z 5 + 26352xyz 6 − 40176xz 7 + 720y 4z 4 + 864y 3z 5 − 9072y 2z 6 +
                46656z 8.
This polynomial is a sum of three squares of polynomials with coefficients in Q(α)
with α a root of Z 3 − 2 and we want to see if we can write it as a sum of squares of
polynomials with rational coefficients (we will show in Section 5 how this polynomial
was constructed).
    Since f is homogenous of degree 8 in x, y, z, the parametrization matrix W
of the space L of solutions to (2.1) is a 15 × 15 matrix with rows and columns
indexed by v(x, y, z) = (x4 , x3 y, x3 z, x2 y 2 , x2 yz, x2 z 2 , xy 3 , xy 2 z, xyz 2 , xz 3 , y 4 , y 3 z,
y 2 z 2 , yz 3 , z 4 ). The space L has dimension 75 and rank 15.
    If we use the numeric solver SEDUMI to compute a positive semidefinite matrix
in L we get a solution with 10 positive eigenvalues and 5 (approximate) null eigen-
values. We need to reduce the generic rank of the parametrization matrix to 10 so
that we can find a 10 × 10 principal submatrix of full rank, use the numerical solver
to compute a positive definite solution in that space, and extend the solution to a
15 × 15 matrix with 10 positive eigenvalues and 5 exact zero eigenvalues.
    We solve the system of equations
                                                                                          
                                   ∂f                ∂f                ∂f
                  f (x, y, z) = 0,    (x, y, z) = 0,    (x, y, z) = 0,     (x, y, z) = 0
                                   ∂x                ∂x                ∂x
in Maple and obtain the following three branches of solutions:
                s1 (t) = (0, t, 0),
                s2 (t) = (0, −3t, t),
                              1
                s3 (t) = (t, (648α4 − 327α3 + 152α2 − 777α − 36)t, αt),
                             60
where α is a root of 648Z 5 −327Z 4 +152Z 3 −921Z 2 −36Z +36. This last polynomial
has odd degree so it contains at least one real root.
   From the first solution we derive the condition W.v(0, 1, 0) = 0 and from the
second solution we derive the condition W.v(0, −3, 1) = 0. For the last solution
10                               SANTIAGO LAPLAGNE


we derive first the trace condition for t = 1, W. Tr(v(s3 (1))) = 0 These restrictions
reduce the problem to L1 ⊂ L of dimension 39 and rank 12.
   Now we use the ghost solutions coming from null values in the diagonal of the
parametrization of L1 . There are three null values, and adding the corresponding
restrictions we reduce to L2 ⊂ L1 of dimension 23 and rank 10.
   If we solve numerically this problem, the solution we get has 5 exact null eigen-
values as expected, but also 4 approximate null eigenvalues. We need to further
reduce the dimension of the problem to get an exact solution.
   We use the third solution with t = 1 and reduce the problem to L3 with di-
mension 16 and rank 9. Now the parametrization matrix contains non-rational
coefficients. To look for rational solutions, we can apply the strategy in Section
3.4. This reduces the search space to L4 of dimension 4 and rank 6. We choose
a 6 × 6 principal submatrix of full rank of the parametrization of L4 and use the
numeric solver SEDUMI to compute a positive semidefinite matrix in that space.
The problem is now strictly feasible, the solver finds a positive definite solution.
From this solution, we obtain a solution to the original problem that has 9 exact
null eigenvalues and 6 positive eigenvalues (the rank was 6), hence we have solved
the problem.
Remark 3.9. If we compute the characteristic polynomial of the resulting matrix, we
obtain a polynomial of the form χ(x) = x9 (x6 −a5 x5 +a4 x4 −a3 x3 +a2 x2 −a1 x+a0 ),
with ai ∈ Q>0 . Since the second factor has alternating signs by Descarte’s rule we
know that it has exactly 6 positive roots.
3.5. A step by step algorithm. The ideas developed above are to be considered
more as a set of tools to handle the problem than as a fixed algorithm. Depending
on the problem, some of the tools will provide results where others may not, and in
some cases applying repeatedly some of the tools can speed up the computations.
In particular, it seems to be a good strategy to add the equations corresponding to
null values in the diagonal as soon as such a value appears.
   Nevertheless, for clarity and definiteness we present in this section a step by
step algorithm. This is essentially the algorithm that is implemented in procedure
exactSOS of the Maple package rationalSOS. For simplicity, we assume that we are
looking for exact rational solutions and we use only the equations coming from the
trace of real solutions, as the plain equations (without taking trace) may introduce
non-rational coefficients.

     4. Sum of squares of two polynomials over a field of odd degree
  We now turn to the problem of determining when does a rational polynomial
that allows a R-SOS decomposition allow also a Q-SOS decomposition.
   In [13, Section 5] the author poses some open questions. Question 5.3 is: “Let
K be a number field of odd degree, and assume that a form f over Q is a sum of
squares over K. Then, is f a sum of squares over Q?” We provide in this section
an affirmative answer for the case of a sum of two squares over K.
Theorem 4.1. Let f ∈ Q[x1 , . . . , xn ] be such that
                                     f = p21 + p22 ,
with p1 , p2 ∈ Q(α)[x1 , . . . , xn ] and Q(α) ֒→ Q an algebraic extension of odd degree.
 FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF SQUARES DECOMPOSITIONS11


Algorithm 1 Exact sum of squares decomposition
Input: f ∈ Q[x1 , . . . , xn ] homogenous of degree 2d ∈ N.
Output: {p1 , . . . , ps } ⊂ Q[x1 , . . . , xn ] homogenous of degree d and {c1 , . . . , cs } ⊂
  Q such that f = c1 p21 + · · · + cs p2s , if such decomposition is found. 0 if no
  decomposition is found.
  S := {ωi = (ωi,1 , . . . , ωi,n )}{1≤i≤t} ⊂ Q̄n , a set of solutions of f = 0 (which can
                                                          ∂f
  be computed by solving the system {f = 0} ∩ { ∂x           i
                                                               = 0}1≤i≤n )
  v := vector of all the monomials of degree d in n variables, vα = xα for α ∈ Md
  W := matrix parametrization of L = {Q ∈ S Sd |f (x) = v(x)t Qv(x)}
  for i:=1 to t do
     u := TrQ(ωi,1 ,...,ωi,n )/Q (v(ωi ))
     Set L = L ∩ {Q ∈ S Sd |Q.u = 0}
     W := parametrization of L, computed by solving the linear equations
  Set L = L ∩ {Q ∈ S Sd |Q.ei = 0 for all i such that W (i, i) = 0}
  W (T1 , . . . , Tk ) := parametrization of L
  s := rank(W )
  Ws := principal submatrix of W of rank s
  (t1 , . . . , tk ) := numerical solution to the problem of maximizing the minimal
  eigenvalue of Ws (T1 , . . . , Tk )
  if Ws (t1 , . . . , tk ) is positive definite then
     Compute an LU decomposition of W (t1 , . . . , tk ): P, D, U ∈ Qmd ×md with P a
     permutation matrix, U upper triangular with all entries in the diagonal equal
                              md ×md
     to 1, and D ∈ Q≥0                 diagonal matrix such that W (t1 , . . . , tk ) = P U t DU
     (by Gaussian elimination)
     for i:=1Pto s do
                     r
          pi = j=1 Ui,j vj (x1 , . . . , xn )
     return {p1 , . . . , ps }, {D1,1 , . . . , Ds,s }
  else
     return 0


   There exist q1 , q2 ∈ Q[x1 , . . . , xn ] such that

                                         f = q12 + q22 .

   For the proof we need the following result [2, Theorem A]:

Theorem 4.2. Let A be a unique
                            √     factorization domain (UFD) and F the quotient
field of A. Assume that I = −1 6∈ F , and that A[I] = {a1 + a2 I : a1 , a2 ∈ A} is
also a UFD. If a ∈ A is a sum of two squares in F then a is a sum of two squares
in A.

   Taking A = Q[x1 , . . . , xn ] we get:

Corollary 4.3. Let f ∈ Q[x1 , . . . , xn ] and assume that f is a sum of two squares
in Q(x1 , . . . , xn ). Then it is already a sum of two squares in Q[x1 , . . . , xn ].

Proof of Theorem 4.1. Let m(Z) ∈ Q[Z] be the minimal polynomial of α over Q.
Let L be a splitting field of m(Z) over Q and let α = α0 , α1 , . . . , αd−1 be the roots
of m(Z) in L. Let σi , 0 ≤ i ≤ d − 1, be elements of Gal(L/Q) such that σi (α) = αi .
12                                   SANTIAGO LAPLAGNE


   We can factorize f = p21 + p22 = (p1 + Ip2 )(p1 − Ip2 ), where I 2 = −1. For each
0 ≤ i ≤ d − 1, we extend σi to an automorphisms of L(I), and we call the extension
also σi . Taking the product of the conjugates:

                d−1
                Y                                      d−1
                                                       Y
           d
          f =         σi ((p1 + Ip2 )(p1 − Ip2 )) =          σi (p1 + Ip2 )σi (p1 − Ip2 ).
                i=0                                    i=0

  Since σi (I) is either I or −I, σi (p1 +Ip2 )σi (p1 −Ip2 ) = (σi (p1 )+Iσi (p2 ))(σi (p1 )−
Iσi (p2 )) and we can regroup the factors:
                         d−1
                                                 ! d−1                     !
                         Y                          Y
                fd =         σi (p1 ) + Iσi (p2 )      σi (p1 ) − Iσi (p2 )
                           i=0                          i=0

which we can rewrite as
                                 f d = (P1 + IP2 ) (P1 − IP2 ) ,
with P1 , P2 symmetric polynomials on the d conjugates of α. Hence P1 and P2 are
fixed by Gal(L/Q) and they are therefore polynomials in Q[x1 , . . . , xn ].
   We obtain
                                     P12     P22
                               f = d−1    + d−1
                                    f       f
with d − 1 even. Hence f if the sum of the squares of two rational functions. By
Corollary 4.3, this implies that f can be written as the sum of two polynomials
with rational coefficients.
                                                                               

Remark 4.4. The polynomials P1 and P2 can be constructed following the above
steps (assuming we are able to compute in the splitting field of Q(α)). The proof
of Theorem A in [2] is also constructive. The above proof is then an algorithm for
computing the Q-SOS decomposition.
Example 4.5. (See [5, Worksheet C] for the computations in Maple.) Let
      p1 (x, y, z) = 2α2 x2 z − 2α2 yz 2 + 2αx3 − 2αxyz − 2x3 + x2 y − 2xz 2 + y 3 ,
      p2 (x, y, z) = 2α2 x3 − 2α2 xyz + 2αx2 y − 2αy 2 z − x3 + 2x2 z − xy 2 + 2z 3 ,

with α a root of Z 3 − 2. Let f (x, y, z) = p21 + p22 = 5x6 + 12x5 y + 12x5 z +
3x4 y 2 + 12x4 z 2 − 4x3 y 3 − 36x3 y 2 z − 36x3yz 2 − 4x3 z 3 + 3x2 y 4 + 12x2 z 4 + 12xy 3 z 2 +
12xy 2 z 3 + y 6 + 4z 6 ∈ Q[x, y, z] (see Section 5 for the details on how this example
was constructed).
   Let σi beQas in Theorem 4.1. Recalling that P1 and P2 are defined so that
P1 + IP2 = 2i=0 (σi (p1 ) + Iσi (p2 )), we get
                    P1 = σ0 (p1 )σ1 (p1 )σ2 (p1 ) − σ0 (p1 )σ1 (p2 )σ2 (p2 )
                         − σ0 (p2 )σ1 (p1 )σ2 (p2 ) − σ0 (p2 )σ1 (p2 )σ2 (p1 )
                    P2 = σ0 (p2 )σ1 (p1 )σ2 (p1 ) + σ0 (p1 )σ1 (p2 )σ2 (p1 )
                           + σ0 (p1 )σ1 (p1 )σ2 (p2 ) − σ0 (p2 )σ1 (p2 )σ2 (p2 )
which in this example gives
 FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF SQUARES DECOMPOSITIONS13


   P1 = −10x9 − 39x8 y − 24x8 z − 42x7 y 2 − 36x7 yz + 6x7 z 2 + 4x6 y 3 + 72x6 y 2 z
        + 108x6 yz 2 + 80x6 z 3 + 18x5 y 4 + 120x5 y 3 z + 126x5 y 2 z 2 + 12x5 yz 3
        + 48x5 z 4 − 6x4 y 5 − 36x4 y 3 z 2 − 240x4 y 2 z 3 − 252x4 yz 4 − 24x4 z 5
        − 6x3 y 6 − 36x3 y 5 z − 54x3 y 4 z 2 − 40x3 y 3 z 3 + 64x3 z 6 + 84x2 y 3 z 4
        + 72x2 y 2 z 5 − 12x2 yz 6 + 18xy 6 z 2 + 12xy 5 z 3 + 24xz 8 + y 9 + 4y 3 z 6 ,
   P2 = 5x9 + 12x8 y + 42x8 z − 12x7 y 2 + 72x7 yz + 84x7 z 2 − 40x6 y 3 − 54x6 y 2 z
        − 36x6 yz 2 + 58x6 z 3 − 6x5 y 4 − 24x5 y 3 z − 252x5 y 2 z 2 − 240x5 yz 3
        − 36x5 z 4 + 12x4 y 5 + 126x4 y 4 z + 120x4 y 3 z 2 + 18x4 y 2 z 3 + 48x4 z 5
        − 8x3 y 6 + 80x3 y 3 z 3 + 108x3 y 2 z 4 + 72x3 yz 5 + 12x3 z 6 + 6x2 y 6 z
        − 36x2 y 5 z 2 − 42x2 y 4 z 3 − 3xy 8 − 24xy 3 z 5 − 36xy 2 z 6 − 2y 6 z 3 − 8z 9 ,
and we verify in Maple that f 3 = P12 + P22 .
                                                  P2     P2
   The last step is to convert the expression f = f 12 + f 22 into a sum of squares
of polynomials in Q[x, y, z], as guaranteed by Corollary 4.3. In this case this is
immediate, since P1 and P2 are divisible by f .
   We get
        f (x, y, z) = (2x3 + 3x2 y − 6xz 2 − y 3 )2 + (x3 + 6x2 z − 3xy 2 − 2z 3 )2 .

 5. Sum of squares of three polynomials over a field of odd degree
   In this section we provide a negative answer to [13, Question 5.3] stated above
for the case of a sum of squares of three polynomials over an algebraic extension of
Q of odd degree (which trivially implies a negative answer for any larger number
of polynomials). We exhibit a polynomial that can be decomposed as the sum of
three squares of polynomials with coefficients in an algebraic extension Q(α) of Q
of odd degree that cannot be decomposed as sum of squares of polynomials with
coefficients in Q. The example also provides an affirmative answer to the first
question in [13, Question 5.1]: “Are there examples of forms in Q[x1 , . . . , xn ] that
are sums of squares over R, but not over Q, that are irreducible over C?”.
   To construct the example, we first explain a method to build polynomials in
Q[x] = Q[x1 , . . . , xn ] that are sum of squares of polynomials with coefficients in
an algebraic extension of Q. In [4], the author shows that if Q(α) is a totally real
extension of Q then every sum of squares with coefficients in Q(α) is also a sum of
squares of polynomials with coefficients in Q. So, to construct a counterexample,
we must look for extensions that are not totally real. For simplicity, let α be a root
of Z 3 − 2.
   We start with three generic polynomials pi ∈ Q(α)[x], 1 ≤ i ≤ 3, which we can
write as
                               pi = ai (x) + bi (x)α + ci (x)α2 ,
ai , bi , ci ∈ Q[x]. From the desired identity f = p21 + p22 + p23 , using the fact that
α3 = 2, we derive an expression
(5.1)     f = A(a1 , a2 , . . . , c3 ) + B(a1 , a2 , . . . , c3 )α + C(a1 , a2 , . . . , c3 )α2 .
with
                      B = 2a1 b1 + 2a2 b2 + 2a3 b3 + 2c21 + 2c22 + 2c23 ,
                      C = 2a1 c1 + 2a2 c2 + 2a3 c3 + b21 + b22 + b23
14                                    SANTIAGO LAPLAGNE


Since we want f ∈ Q[x], we must have B ≡ 0 and C ≡ 0. Note that the expressions
for B and C are linear in a1 , a2 . If we solve the equations for these two coefficients,
we get
               2a3 b2 c3 − 2a3 b3 c2 + b21 b2 + b32 + b2 b23 − 2c21 c2 − 2c32 − 2c2 c23
          a1 =
                                            b 1 c2 − b 2 c1
                 2a3 b1 c3 − 2a3 b3 c1 + b31 + b1 b22 + b1 b23 − 2c31 − 2c1 c22 − 2c1 c23
          a2 = −
                                               b 1 c2 − b 2 c1
    For any number of polynomials over a number field of degree 3 it is easy to
derive similar rational expressions for a1 and a2 . For larger degree extensions, the
expression we can derive will involve roots of polynomials and hence the polynomials
should be chosen carefully so that the expressions in the output are also rational
expressions.
    Plugging the expressions for a1 and a2 in (5.1) and multiplying by the common
denominator b1 c2 −b2 c1 , we obtain that for any a3 , b1 , b2 , b3 , c1 , c2 , c3 ∈ Q[x], (b1 c2 −
b2 c1 )f ∈ Q[x] is the sum of the squares of three polynomials with coefficients in
Q(α)[x]. We call f this polynomial from now on.
    For our concrete example we pick arbitrary polynomials in Q(α)[x, y, z, w] setting
(5.2)        b1 = x, b3 = y, c1 = z, c3 = w, b2 = 3x, c2 = x + 7z, a3 = 21z.
Theorem 5.1. Let
f (x, y, z, w) = 4w4 x2 + 56w4 xz + 200w4 z 2 − 504w3 x2 z − 3696w3 xz 2 − 112w2 x4
                  − 656w2 x3 z − 12w2 x2 y 2 + 168w2 x2 yz + 20008w2 x2 z 2 − 88w2 xy 2 z
                  + 2352w2 xyz 2 + 11200w2xz 3 + 8400w2 yz 3 + 20000w2 z 4
                  + 16wx4 y + 7896wx4 z + 128wx3 yz − 10752wx3 z 2 + 840wx2 y 2 z
                  − 10328wx2 yz 2 − 76944wx2 z 3 − 77616wxyz 3 − 184800wxz 4
                  + 932x6 − 1656x5 z + 188x4 y 2 − 2352x4yz − 10020x4z 2 − 256x3 y 2 z
                  − 13776x3yz 2 + 3520x3z 3 + 10x2 y 4 − 252x2 y 3 z − 68x2 y 2 z 2
                 + 49728x2yz 3 + 175824x2z 4 − 1848xy 3 z 2 + 20296xy 2z 3
                 + 235200xyz 4 + 420000xz 5 + 88200y 2z 4 + 420000yz 5 + 500000z 6
               ∈ Q[x, y, z, w].
The polynomial f can be decomposed as a sum of squares of three polynomials in
Q(α)[x, y, z, w], α a root of Z 3 − 2, but it cannot be decomposed as a sum of squares
of polynomials in Q[x, y, z, w]. Moreover, f is irreducible over C.
Proof. (See [5, Worksheet D] for the computations in Maple.) This polynomial was
computed as explained above, using the substitutions in (5.2), and it is therefore a
sum of squares of three polynomials in Q(α)[x, y, z, w].
   To prove that it cannot be written as a sum of rational squares, we can apply
the implementation in Maple of Algorithm 3.5 (see [5, Example 3]), which outputs
that the only positive semidefinite solution to the problem has non-rational entries.
For convenience, we provide next a step by step proof that the only solution for
Q in (2.1) being positive semidefinite is the one corresponding to the solution in
Q(α)[x, y, z, w] described above.
   The corresponding matrix Q is a 20×20 matrix with rows and columns indexed by
the monomials v(x, y, z, w) = (x3 , x2 y, xy 2 , y 3 , x2 z, xyz, y 2 z, xz 2 , yz 2 , z 3 , x2 w, xyw,
 FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF SQUARES DECOMPOSITIONS15


y 2 w, xzw, yzw, z 2 w, xw2 , yw2 , zw2 , w3 ) . The space L has dimension 126 and rank
20.
    We first find real roots of f . In this case, equating f and its partial derivatives
to 0 we get a system that cannot be solved by Maple command solve. We add the
equations {p1 = 0, p2 = 0, p3 = 0}, which must also be verified by all real solutions,
and for the new system we get 4 branches of solutions:
                                                                                 
                                                           α(s, t)        s
                                                x = s, y =         ,z = − ,w = t ,
                                                             2            4
                                                  {x = 0, y = s, z = t, w = β(s, t)} ,
                                                 {x = 0, y = s, z = 0, w = t} ,
                      (100δ ξ − 441δ ξ + 28δξ 4 + 2ξ 4 + 1764δ 2 − 20ξ 2 )s
                           2 4      2 3
        
         x = s, y = −                                                          ,
                                               84δξ
                                (100δ 2 ξ 2 − 441δ 2 ξ + 28δξ 2 + 2ξ 2 − 20)s
                                                                              
                    z = δs, w =                                                  ,
                                                      84δ

where α(s, t) is a root of m1 (Z) = 4Z 2 − 21sZ + 8t2 − 168st + 165s2 , β(s, t) is a
root of m2 (Z) = Z 2 + 21uv + 50t2 , ξ is a root of m3 (Z) = Z 3 − 2 and δ is a root of
a polynomial m4 (Z) of degree 12 with 2 real roots. Note that the first and second
branches involve algebraic extensions that depend on the choices of the parameters,
while the third and fourth equation do not.
   We start with the third branch. By giving different values to s and t we obtain
different vectors that must be in the kernel of L. Note that there are 4 different
monomials in v(0, s, 0, t) = (0, 0, 0, s3 , 0, 0, 0, 0, 0, 0, 0, 0, s2t, 0, 0, 0, 0, st2, 0, t3 ), so by
giving different values to s and t we can get at most 4 independent vectors. We use
the following choices {s = 1, t = 1}, {s = 1, t = 0}, {s = 0, t = 1}, {s = −1, t = 1}.
After solving the corresponding equations, we get L1 ⊂ L of dimension 71 and rank
16.
   Next, we plugin the equations corresponding to the ghost solutions of zeros in
the diagonal and 2 × 2 principal submatrices with null determinant. We reduce to
L2 ⊂ L1 of dimension 29 variables and rank 12.
   Now we use the first branch. We have to choose real values of s and t that give
real solutions, that is, that the polynomial 4Z 2 − 21sZ + 165s2 − 168st + 8t2 has
real roots. We choose {s = 1, t = 1}, {s = 1, t = 2}, {s = 1, t = 3}. This step
reduces the space to L3 ⊂ L2 of dimension 8 and rank 9. Other choices of s and t
tested did not reduce further the dimension.
   For the second branch, we take {s = −3, t = 1}, and reduce the space to L4 ⊂ L3
of dimension 6 and rank 8. Other choices of s and t tested did not reduce further
the dimension.
   Plugging again the equations corresponding to ghost solutions from null entries
in the diagonal, we obtain L5 ⊂ L4 of dimension 3 and rank 7.
   Finally we use the fourth branch, which depends only on s. We take s = 1.
After plugging in this solution, the system is completely solved and an exact solu-
tion is found. The solution has non-rational entries, and corresponds to the same
matrix that is obtained from the original R-SOS decomposition. By Lemma 2.2,
we conclude that f does not allow a Q-SOS decomposition.
   We verify that f is absolutely irreducible (that is, irreducible over C) using Maple
procedure evala(AIrreduc(f)).                                                                          
16                             SANTIAGO LAPLAGNE


Remark 5.2. To prove the theorem we used only exact computations, we did not
in this case need to call the numerical solver SEDUMI. The zeros of f found by
Maple can be easily verified to be correct by plugging them in the polynomial f .

                  Appendix A. rationalSOS package usage
    For the computations in this work, we developed a Maple package rationalSOS
[5], which is freely available for download and use. The main procedure for comput-
ing an exact SOS decomposition is exactSOS. We provide in this Appendix some
examples of usage.
Example A.1. To compute a decomposition of the polynomial given in Example
2.4, we use the following code (we assume the file rationalSOS.mpl is in the current
working directory):
read("rationalSOS.mpl");
with(rationalSOS);
p1 := x^2 + 3*x*y - 5*x*z + 2z^2;
p2 := 3x^2 - 2*x*z + y*z + 5*y^2;
f := expand(p1^2 + p2^2);
out := exactSOS(f);
--> "Facial reduction results:"
--> "Original matrix"
--> " - Rank: ", 6,
--> " - Number of indeterminates: ", 6
--> "Matrix after facial reduction"
--> " - Rank: ", 2
--> " - Number of indeterminates: ", 0
--> "An exact solution was found without calling the numerical
     solver. The solution matrix is unique under the specified
     conditions."
out[1];
--> [10, 81/10]
out[2];
--> [x^2+(3/10)*x*y-(11/10)*x*z+(3/2)*y^2+(3/10)*y*z+(1/5)*z^2,
     x*y-(13/9)*x*z-(5/9)*y^2-(1/9)*y*z+(2/3)*z^2]
   The first element of the output is the list of coefficients of the polynomials in
the rational SOS decomposition and the second element is the list of polynomials.
In this case, the decomposition consists of two polynomials. We can verify the
solution:
p := out[1][1]*out[2][1]^2+out[1][2]*out[2][2]^2;
expand(p);
--> 10*x^4+6*x^3*y-22*x^3*z+39*x^2*y^2-24*x^2*y*z+33*x^2*z^2-
     20*x*y^2*z+8*x*y*z^2-20*x*z^3+25*y^4+10*y^3*z+y^2*z^2+4*z^4
expand(f-p);
--> 0
   The third element in the output (not printed) is a positive semidefinite matrix
satisfying (2.1). In this case, the decomposition was obtained by purely algebraic
methods, by first computing an exact real solution of f = 0. This implies that the
matrix is the only rational matrix satisfying (2.1).
 FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF SQUARES DECOMPOSITIONS17


Example A.2. To compute a decomposition of the polynomial given in Example
3.8, we use option forceRational = "yes" that implements the strategy explained
in Section 3.4.
read("rationalSOS.mpl");
with(rationalSOS);
f(x,y,z) = 3618*x^8 + 468*x^7*y + 6504*x^7*z - 1104*x^6*y^2
+ 2616*x^6*y*z + 57481*x^6*z^2 - 144*x^5*y^3 - 1652*x^5*y^2*z
- 16440*x^5*y*z^2 + 23420*x^5*z^3 + 160*x^4*y^4 + 1392*x^4*y^3*z
- 2520*x^4*y^2*z^2 - 28448*x^4*y*z^3 + 91320*x^4*z^4 - 240*x^3*y^4*z
+ 1728*x^3*y^3*z^2 + 10524*x^3*y^2*z^3 - 85500*x^3*y*z^4
+ 34740*x^3*z^5 - 3696*x^2*y^3*z^3 + 28920*x^2*y^2*z^4
- 15192*x^2*y*z^5 - 57267*x^2*z^6 + 720*x*y^4*z^3 - 3312*x*y^3*z^4
- 3168*x*y^2*z^5 + 26352*x*y*z^6 - 40176*x*z^7 + 720*y^4*z^4
+ 864*y^3*z^5 - 9072*y^2*z^6 + 46656*z^8
out := exactSOS(f, forceRational = "yes");
--> "Facial reduction results:"
--> "Original matrix"
--> " - Rank: ", 15, "
--> " - Number of indeterminates: ", 75
--> "Matrix after facial reduction"
--> " - Rank: ", 6
--> " - Number of indeterminates: ", 4
--> "Calling numerical solver SEDUMI to find the values of the
    remaining indeterminates..."
--> "Problem solved. Positive definite matrix found for the reduced
    problem."
f - expand(add(i, i = out[1]*~out[2]*~out[2]));
--> 0
  The command add(i, i = out[1]*~out[2]*~out[2]) computes the sum of
                                 P6
squares obtained by the procedure i=1 ci gi2 and we verify that it is equal to f .

Example A.3. We can easily verify that the Motzkin polynomial does not al-
low a SOS decomposition. Since we are looking for any real SOS decomposition
and trace equations are only valid when looking for rational SOS, we set option
traceEquations = "no".
read("rationalSOS.mpl");
with(rationalSOS);
f := x^4*y^2 + x^2*y^4 - 3*x^2*y^2*z^2+z^6;
exactSOS(f, traceEquations = "no");
--> "Facial reduction results:"
--> "Original matrix"
--> " - Rank: ", 10
--> " - Number of indeterminates: ", 27
--> "Matrix after facial reduction"
--> " - Rank: ", 4
--> " - Number of indeterminates: ", 0
--> "An exact solution was found without calling the numerical
    solver. The solution matrix is unique under the specified
18                                  SANTIAGO LAPLAGNE


    conditions."
--> "The solution is not positive semidefinite. A SOS decomposition
    does not exist under the specified conditions."
Example A.4. We can also verify that the concrete example given in [13, Section
2] does not allow a rational SOS decomposition.
read("rationalSOS.mpl");
with(rationalSOS);
f:= x^4+x*y^3+y^4-3*x^2*y*z-4*x*y^2*z+2*x^2*z^2+x*z^3+y*z^3+z^4;
exactSOS(f);
--> "Option eqTrace: yes - Only valid when looking for rational
     decompositions."
--> "Facial reduction results:"
--> "Original matrix"
--> " - Rank: ", 6, "
--> " - Number of indeterminates: ", 6
--> "Matrix after facial reduction"
--> " - Rank: ", 5
--> " - Number of indeterminates: ", 0
--> "An exact solution was found without calling the numerical
--> solver. The solution matrix is unique under the specified
     conditions."
--> "The solution is not positive semidefinite. A SOS decomposition
     does not exist under the specified conditions."

                                   Acknowledgments
   The author would like to thank Gabriela Jeronimo and Daniel Perrucci for many
fruitful discussions.

                                        References
 1. Jon M. Borwein and Henry Wolkowicz, Facial reduction for a cone-convex programming prob-
    lem, J. Austral. Math. Soc. Ser. A 30 (1980/81), no. 3, 369–380. MR 614086
 2. M. D. Choi, T. Y. Lam, B. Reznick, and A. Rosenberg, Sums of squares in some integral
    domains, J. Algebra 65 (1980), no. 1, 234–256. MR 578805
 3. David Hilbert, Ueber die Darstellung definiter Formen als Summe von Formenquadraten,
    Math. Ann. 32 (1888), no. 3, 342–350. MR 1510517
 4. Christopher J. Hillar, Sums of squares over totally real fields are rational sums of squares,
    Proc. Amer. Math. Soc. 137 (2009), no. 3, 921–930. MR 2457431
 5. Santiago Laplagne, rationalSOS, a Maple package for exact SOS decomposition,
    https://bitbucket.org/slaplagne/rationalsos, 2018.
 6. Maple, Version 2015.1, Maple is a trademark of Waterloo Maple Inc., 2015.
 7. Matlab, Version r2016b, The MathWorks Inc., Natick, Massachusetts, 2016.
 8. B. Reznick M.D. Choi, T.Y. Lam, Sums of squares of real polynomials, J. Algebra 65 (1980),
    no. 1, 234–256. MR 578805
 9. T. S. Motzkin, The arithmetic-geometric inequality, Inequalities (Proc. Sympos. Wright-
    Patterson Air Force Base, Ohio, 1965), Academic Press, New York, 1967, pp. 205–224.
    MR 0223521
10. Frank Permenter, Partial facial reduction: simplified, equivalent sdps via approximations of
    the psd cone, presented at the Mosek Workshop, October 6th, 2014.
11. Helfried Peyrl and Pablo A. Parrilo, Computing sum of squares decompositions with rational
    coefficients, Theoret. Comput. Sci. 409 (2008), no. 2, 269–281. MR 2474341
12. Bruce Reznick, Extremal PSD forms with few terms, Duke Math. J. 45 (1978), no. 2, 363–374.
 FACIAL REDUCTION FOR EXACT POLYNOMIAL SUM OF SQUARES DECOMPOSITIONS19


13. Claus Scheiderer, Sums of squares of polynomials with rational coefficients, J. Eur. Math.
    Soc. (JEMS) 18 (2016), no. 7, 1495–1513. MR 3506605
14. Jos F. Sturm, Using sedumi 1.02, a matlab toolbox for optimization over symmetric cones,
    Optimization Methods and Software 11 (1999), no. 1-4, 625–653.

   Departamento de Matemática, FCEN, Universidad de Buenos Aires - Ciudad Univer-
sitaria, Pabellón I - (C1428EGA) - Buenos Aires, Argentina
   E-mail address: slaplagn@dm.uba.ar
