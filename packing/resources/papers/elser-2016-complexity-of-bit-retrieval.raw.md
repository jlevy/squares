                                                             The complexity of bit retrieval
arXiv:1601.03428v1 [cs.DS] 13 Jan 2016




                                                                                Veit Elser
                                                                          Department of Physics
                                                                           Cornell University



                                                                                   Abstract

                                                     Bit retrieval is the problem of reconstructing a binary sequence from its
                                                 periodic autocorrelation, with applications in cryptography and x-ray crys-
                                                 tallography. After defining the problem, with and without noise, we describe
                                                 and compare various algorithms for solving it. A geometrical constraint satis-
                                                 faction algorithm, relaxed-reflect-reflect, is currently the best algorithm for
                                                 noisy bit retrieval.



                                         1      Bit retrieval

                                         The bit retrieval problem is like the problem of factoring integers, but with some
                                         modifications to the rules of arithmetic. These modifications are illustrated below,
                                         where the calculation of 13 × 19 in base-2 is contrasted with the rules of bit re-
                                         trieval. There are two changes: (i) exponents in the binary expansion are periodic
                                         (columns “wrap around”), and (ii) the columns are summed without carrying. In
                                         both factoring and bit retrieval the problem is to reverse the process: find the binary
                                         sequences at the top, given their product at the bottom.

                                              Periodic or ring-like arrangements of integers that are combined with the rules
                                         just described are elements of the polynomial ring ZN = Z[x]/(xN − 1), where N
                                         is the period of the exponents (N = 5 in the example). Factoring elements in ZN
                                         is hard, even when we are told the coefficients of the factors are limited to 0 and
                                         1. We will see shortly that in bit retrieval it makes more sense to instead limit the
                                         coefficients to ±1; we therefore define the set

                                             SN = {s0 + s1 x + · · · + sN −1 xN −1 ∈ ZN : sk = ±1,           0 ≤ k ≤ N − 1}. (1)

                                                                                       1
                            1   1   0   1                    0   1   1   0   1
      ×                 1   0   0   1   1               ×    1   0   0   1   1
                            1   1   0   1                    0   1   1   0   1
                        1   1   0   1                        1   1   0   1   0
           1   1    0   1                                    1   0   1   1   0
           1   1    1   1   0   1   1   1                    2   2   2   2   1

      The rules of ordinary base-2 multiplication (left) are modified (right)
      so that exponents have period 5 and columns are summed without car-
      ries.



    “Retrieval” is a reference to phase retrieval, an important special case where
the two coefficient sequences are reflections of each other (one “ring” is the mirror
of the other). This brings us to our first formulation of bit retrieval:


Definition 1.1. Bit retrieval is the problem where, given a(x) ∈ ZN known to
have the form a(x) = s(x)s(1/x) for some s(x) ∈ SN , we must find s′ (x) ∈ SN
such that s′ (x)s′ (1/x) = a(x).



     The problem definition sidesteps the question of uniqueness. Clearly, if s′ (x)
is a solution, then so are ±s′ (x)xr and ±s′ (1/x)xr , for arbitrary r. We restricted
the solutions of bit retrieval to be elements of SN so that they form orbits in this
group of order 4N . Another nice property of ±1 sequences that will be useful later
(section 5) is that they have the same 2-norm.

    The fastest known algorithm for bit retrieval, as defined above, was discov-
ered by Howgrave-Graham and Szydlo [HGS] and was based on earlier work by
Gentry and Szydlo [GS] that proposed an attack on the NTRU digital signature
scheme. This algorithm has about the same complexity as factoring a number of
O(N log N ) bits; in fact, the first and hardest step of the algorithm is precisely
the factorization of a number of that size. However, a seemingly small change
can make bit retrieval much harder than this. Before we describe this change, we
further develop the relationship to phase retrieval.

    Bit retrieval is a highly idealized model of phase retrieval in crystallography.
In that setting, the polynomial coefficients s0 , . . . , sN −1 are samples within one
period of a periodic function (a 1D crystal), and the coefficients of the product

                                            2
a(x) = s(x)s(1/x) their (periodic) autocorrelation:
                              N
                              X −1               N
                                                 X −1
                       ak =          sl sl−k =          sl sl+k = a−k .             (2)
                              l=0                l=0

The indices in (2) are all taken mod N . In crystallography one would refer to s as
the contrast because one acquires information about it through its action on radi-
ation to produce diffraction patterns. Since the contrast elements are all ±1, the
central autocorrelation is trivial: a0 = N . There are ⌊N/2⌋ nontrivial autocorrela-
tions as a result of the reflection symmetry in (2).

    To complete the connection to phase retrieval, we start with the identity
                                     N −1    √
                             1 X i2πkq/N
                      âq = √      e     ak = N |ŝq |2 ,                           (3)
                             N k=0

where
                                            N −1
                                     1 X i2πkq/N
                              x̂q = √       e    xk                                 (4)
                                      N k=0
defines the Fourier transform of a periodic sequence x. From (3) we see that the
autocorrelations only give us the Fourier transform magnitudes |ŝ|2 , and without
knowledge of the phases of ŝ we are unable to invert the transform (4) to recover
the signs s. Phase retrieval refers to the strategy of discovering the unknown phases
of ŝ by demanding consistency with additional information we have about the con-
trast s. In the case of bit retrieval, this translates to the observation that only very
special sets of phases, when combined with the known magnitudes, produce con-
trast values comprising only ±1.

    To a mathematician, the Fourier magnitudes |ŝ|2 are algebraic numbers that
when examined in great enough detail will reveal the ±1 coefficients of s, even
without knowledge of the phases. By contrast, when these same numbers are mea-
sured in a diffraction experiment, they are known only to a finite precision. Given
that we are retrieving elements from a finite set, how much imprecision or noise
can be tolerated?

   The observation that the autocorrelation coefficients are always integers in the
same congruence class mod 4 as N (appendix 9.1) motivates the following set of
symmetric polynomials as the smallest “quanta” of autocorrelation noise:

        EN = {e(x) ∈ ZN : e0 = 0; ek = e−k = ±2, 1 ≤ k ≤ ⌊N/2⌋} .                   (5)

                                             3
Definition 1.2. Noisy bit retrieval is the problem where, given a noisy autocorre-
lation n(x) known to have the form n(x) = s(x)s(1/x) + e(x), where s(x) ∈ SN
and e(x) ∈ EN , we must find elements s′ (x) ∈ SN and e′ (x) ∈ EN such that
n(x) = s′ (x)s′ (1/x) + e′ (x).


    In noisy bit retrieval we know that all of the k 6= 0 noisy autocorrelations nk
are off by ±2, but we do not know whether the true autocorrelations are obtained
by rounding up by 2 or down by 2. We will see in the next section how even this
amount of noise in the data completely undermines the most efficient bit retrieval
algorithms. The fastest known algorithms for noisy bit retrieval have complexity
2cN ; algorithms and estimates of the constant c are discussed in sections 5 and 6.

    We would still like it to be true that the introduction of noise (5) does not, with
high probability, sacrifice solution uniqueness. This is supported by the following
theorem. Here we assume uniform probability distributions, both on the set of
sign sequences SN and the noise EN we apply to their autocorrelations; “random”
elements of these sets are elements sampled from the uniform distribution.

Theorem 1.1. Let s and e be random elements respectively of SN and EN , and
n(x) = s(x)s(1/x) + e(x) the corresponding noisy autocorrelation. Let s′ be the
same as s but with a single one of its N signs reversed. The probability, that there
exists an e′ ∈ EN such that s′ (x)s′ (1/x) + e′ (x) = n(x) (the modified s′ is also
compatible with n), is equal to (3/4)(N −1)/2 for odd N and (1/2)(3/4)N/2−1 for
even N .


Proof. First consider odd N . Without loss of generality we may assume the re-
versed sign is in position 0, so s′0 = −s0 , and s′k = sk for k 6= 0. Upon reversal,
the autocorrelations change as follows:

  a′k − ak = (s′0 − s0 )(sk + s−k ) = ±2(sk + s−k ),       1 ≤ k ≤ (N − 1)/2. (6)

Each change arises from a pair of independent signs, and is therefore 0 with prob-
ability 1/2 and ±4 with probability 1/2. Since the noisy data n has not changed,
e′k − ek = ak − a′k . Whenever a′k − ak = 0, an unchanged e′k = ek is compati-
ble with the modified s′ . However, whenever a′k − ak = ±4, both ek and e′k are
determined (their values are limited to ±2) and in particular, only one choice of ek
allows for s′ to be compatible with n. The net probability that there exists a com-
patible e′k is therefore (1/2)(1) + (1/2)(1/2) = 3/4 and the stated result follows
from the independence of the (N − 1)/2 outcomes for the different k. When N
is even, only the case k = N/2 is changed because the change in aN/2 is ±4 with

                                          4
probability 1. The probability that there exists a compatible e′N/2 therefore changes
from 3/4 to 1/2.


    We conjecture that uniqueness in the sense of the above theorem extends be-
yond the simple case of a single reversed sign. There is always non-uniqueness
stemming from the invariance of the autocorrelation with respect to the order 4N
group generated by cyclic-shifts, reflection and sign reversal. But this is a small
group and inconsequential if we view bit retrieval, in information-theoretic terms,
as the decoding stage of a noisy communication channel. In the “noisy autocor-
relator channel” an input signal of N bits, in the form of signs s, is encoded with
noise as s → a + e = n. The stronger result suggested by the theorem is that the
information capacity of this channel (an asymptotic property for large N ) is the
same as the entropy of the uniform distribution on the inputs.

    Turning the (probabilistically qualified and symmetry amended) uniqueness
conjecture into a theorem presents difficult challenges. There exist polynomials,
for example (N = 13)

           s(x) = 1 + x2 + x3 + x4 + x5 + x6 + x7 + x10 + x11                     (7)
            ′               2     3     4       7   9    10        11     12
          s (x) = 1 + x + x + x + x + x + x                   +x        +x ,      (8)

that have the same autocorrelation and yet are not in the same orbit of the order 4N
symmetry group. The equality of the autocorrelations is in this case explained by
the fact that

                s(x) = p(x)q(x) = (1 + x2 + x7 )(1 + x3 + x4 ),                   (9)

and s′ (x) = p(x)q(1/x). To prove the theorem one needs to bound this form
of non-uniqueness, which exists even without noise. Though extremely rare, the
phenomenon of factorizable solutions (contrast) is also known to occur in crystal-
lography[PS].

    By the standards of crystallography, the noise defined by (5) has an unrealistic
dependence on N . Since the noise coefficients e are O(1), so will be the difference
in the Fourier coefficients ê,√
                               between the true and noisy transforms, â and n̂. By
(3) this translates into O(1/ N ) errors in the Fourier magnitudes |ŝ|2 . Crystal-
lography experiments are noisier, being content with an O(1) signal-to-noise ratio
and√therefore noise amplitudes for e and ê in the bit retrieval model growing as
O( N ). This brings us to yet a third problem:

                                            5
Definition 1.3. Fixed-precision bit retrieval is the problem where, given precision
η > 0 and a noisy autocorrelation transform n̂ known to satisfy
                                    √
                     |ŝq |2 − n̂q / N < η,     0 ≤ q ≤ ⌊N/2⌋,                   (10)

for some Fourier transformed sequence of signs s, we must find such a sign se-
quence.

     This version of bit retrieval comes closest to the phase retrieval problem in
crystallography. There the data naturally arrives via the Fourier transform and is
always subject to noise. The order N of the cyclic group in bit retrieval corre-
sponds to the number of resolution elements, or voxels, in the representation of
the contrast. That the symmetry group of the 3D problem is not the cyclic group
of order N , but a direct product of three such groups having the same order, is
probably largely irrelevant to the complexity of bit retrieval. Finally, although a
strict two-valued contrast is a poor way to approximate a continuous contrast func-
tion (electron density), it is not a bad model for representing a dilute collection of
equally scattering atoms at low resolution.

     The fastest algorithms for solving fixed-precision bit retrieval, like noisy bit
retrieval, have complexity 2cN , where the constant c now depends on the noise
parameter η. But unlike the noisy version, solutions in the fixed-precision version
have extensive entropy, that is, grow in number exponentially with N . This can be
argued non-rigorously as follows.

    Take N large and consider flipping a large random subset of M signs, while
keeping M ≪ N . The Fourier transform changes as ŝq → ŝq + ∆ŝq where, using
a result of Freedman and Lane [FL], the ∆ŝq are independent complex-normal
random variables with zero mean and variance O(M/N ). The probability that
the flips violate any of the corresponding inequalities in (10), in the limit of small
variance, is an integral over the tail of a Gaussian distribution and depends on η as
Bq exp (−bq N η 2 /M ) for some positive constants Bq and bq . The probability that
no inequality is violated behaves as
                        ⌊N/2⌋
                         Y
                                1 − Bq exp (−bq N η 2 /M ) .
                                                          
                                                                                 (11)
                         q=0

Now consider the limit N → ∞ with M/N held fixed and M/N ≪ η 2 . In this
limit (11) approaches 1 for any of the sets of flipped signs which, for fixed M/N ,
have extensive entropy. Solutions therefore have extensive entropy for any η > 0.

                                          6
Crystallography with fixed η can escape this source of non-uniqueness by keeping
N under a bound proportional to 1/η 2 .

     Fixed-precision bit retrieval would reduce to noise-free bit retrieval if instead
of fixing η (as N increases) we were allowed to take the limit η → 0. In this limit,
the Fourier transform of the noisy n̂, after rounding the coefficients, is the autocor-
relation a of bit retrieval. We get a variant of noisy bit retrieval if instead we take
limits such that N η 2 = O(1), i.e. keeping η just small enough to preserve solution
uniqueness. The fixed-precision version lends itself naturally to geometrical con-
straint satisfaction algorithms, two of which we shall describe in detail. Unlike the
algebraic algorithms developed for solving the noise-free problem, the geometric
algorithms are easily adapted to solve any of the three problems. Not surprisingly,
the complexity of the geometric algorithms is relatively insensitive to η.




2    Symmetry and noise

To appreciate the effect of noise on bit retrieval complexity, we focus in this section
on instances where it is known that the signs s have a reflection symmetry. We are
then free to target the rotated polynomial s′ (x) = xr s(x) that has the property
s′ (x) = s′ (1/x). To avoid complications in the presentation that do not alter the
main ideas, we restrict ourselves to prime N in this section.

   Symmetric bit retrieval is very easy. Dropping the prime on our reflection
symmetric signs, we define b(x) ∈ ZN with coefficients bk = (1 − sk )/2 ∈ {0, 1}.
The coefficients a′k of the corresponding autocorrelation a′ (x) = b(x)b(1/x) =
b(x)2 are related to the sign autocorrelations as follows:

                                                             !
                                 1                 X
                           a′k =     ak + N − 2         sl       .                 (12)
                                 4
                                                    l



By (2) the sum of the signs is one of the square roots of the sum of the ak ’s. Exercis-
ing symmetry to always select the non-negative root, the transformed a′ (x) ∈ ZN
is known. We now observe there are exactly as many bits of information in the sym-
metric b(x) as there are parity bits in the a′ (x) coefficients. This suggests reducing

                                           7
all the coefficients mod 2, so we are working in the ring (Z/2)[x]/(xN − 1):
                                                             2
                                       (N −1)/2
                                         X
                     a′ (x) = b0 +             bk (xk + x−k )              (13)
                                               k=1
                                           (N −1)/2
                                             X
                               = b0 +                 bk (x2k + x−2k ).              (14)
                                             k=1

Since N is a prime greater than 2, there is a unique element 2−1 in the field of N
elements and an explicit formula for bit retrieval:

                                    bk = a′2−1 k    (mod 2).                         (15)


     By reducing the transformed autocorrelation coefficients mod 2 we have made
our bit retrieval algorithm maximally vulnerable to noise. Indeed, with the ±2 un-
certainty in ak of noisy bit retrieval, the parities of the a′k ’s are completely uncer-
tain and so it would seem, the bits bk . However, we next consider a more elaborate
polynomial-time algorithm whose noise tolerance is somewhat better. Since sign
reversal s → −s is the only symmetry remaining in reflection symmetric bit re-
trieval, it is not surprising that this special case of the problem can be reduced to a
shortest lattice vector problem, which shares this symmetry.

     When the signs s have reflection symmetry, from (4) we see that ŝ is purely
real and we can write ŝq = |ŝq |yq , where yq = ±1. We then have the following
equations relating the signs xk of the unknown sequence and the unknown signs yq
of its Fourier transform:
                            (N −1)/2
   √                          X
       N |ŝq | yq = x0 +              2 cos (2πkq/N ) xk ,     0 ≤ q ≤ (N − 1)/2.   (16)
                              k=1

Since y−q = yq , there are just as many independent equations and Fourier signs,
M = (N + 1)/2, as there are unknown signs in the reflection-symmetric sequence
we are attempting to retrieve.

    The observation that (16) should hold for arbitrary levels √ of precision, in nu-
merical approximations of the cosine functions and the data N |ŝq |, leads to a
polynomial time bit retrieval algorithm for sequences known to have reflection
symmetry. Unlike the q = 0 equation, which only reveals the number of +1 signs
(up to overall sign reversal), the other equations, individually, become nontrivial
instances of the integer partitioning problem when their coefficients are multiplied

                                                8
by a large number K = 2P and then rounded to the nearest integer. Unlike the
usual integer partitioning problem, here we require only that the partition produces
a sum consistent with the round-off errors. Nevertheless, it is easy to produce
arbitrarily good approximate integer equations because the round-off has a fixed
bound while arbitrarily large P -bit approximations of the Fourier coefficients can
be computed in time that grows as a polynomial in P .

    It is straightforward to adapt the method of Lagarias and Odlyzko [LO], for
solving low density subset sum problems, to solve symmetric bit retrieval. Low
density in our context corresponds to setting the number of bits P , in the approx-
imation of the coefficients, sufficiently large in comparison to the number of un-
known signs, 2M . However, rather than use just one of the q 6= 0 equations, and
the information in just one of the Fourier magnitudes, we construct a lattice Λ from
information provided by all M equations. The generators of Λ are the rows of the
following 2M × 2M matrix:
                                                     
                                     ⌊KD⌉        0
                             G=                         ,                        (17)
                                     ⌊KC⌉ IM ×M

where ⌊ · · · ⌉ denotes rounding to the nearest integer and the M × M blocks C and
D are defined by
                           
                             1,                   k=0
                   Ckq =                                                      (18)
                             2 cos (2πkq/N ), 1 ≤ k ≤ M − 1,
                                √                   √          
                     D = diag − N |ŝ0 | , . . . , − N |ŝM −1 | .            (19)
By construction, Λ has two short vectors:

      v1 = [w0 · · · wM −1 1 · · · 1] = [0 · · · 0 1 · · · 1] · G                  (20)
      vs = [z0 · · · zM −1 s0 · · · sM −1 ] = [y0 · · · yM −1 s0 · · · sM −1 ] · G, (21)

where w0 , . . . , wM −1 and z0 , . . . , zM −1 are sets of small integers produced by
round-off. Vector v1 is small because each of the columns of the matrix C has
zero sum while vs is small by equations (16).

    Each column of (21) represents one instance of the integer partitioning prob-
lem: assigning M + 1 signs to the same number of P -bit integers to produce a
small sum. In the equivalent subset sum problem we must find a subset of M + 1
P -bit integers to produce a given target sum, again with neglect of the low order
round-off bits. In base-2 arithmetic, a solution is checked by verifying that nearly
P column sums (low order bits excepted) are all even, where these were equally

                                           9
likely to have been either parity in a randomly guessed subset. Reasoning prob-
abilistically, we conclude that P must be at least as large as M if we expect to
recover a unique subset, or choice of signs in the equivalent integer partitioning
problem. Fewer bits should suffice when the same set of signs is required to solve
all M − 1 non-trivial (q 6= 0) integer partitioning problems represented by (21). In
fact, the necessary number of bits would be bounded if the information provided
by each partitioning problem is in some sense independent of the others.

    The question of how to efficiently find a partition places different demands
on the number of bits in our integer approximation of the symmetric bit retrieval
problem. The Lagarias-Odlyzko algorithm, associated with a single one of our
M − 1 partitioning problems, and assuming the specific non-random integers in
G are well modeled by average-case behavior, requires P = O(M 2 ). We have
not attempted to extend the analysis of the algorithm to the generator matrix G,
and instead have performed experiments with the symmetric Hadamard sequence
instances, defined in appendix 9.1, that we believe to be among the hardest. In each
experiment we apply the Mathematica implementation of the LLL lattice reduction
algorithm [LLL] to G and record a success when among the reduced basis we find
a vector av1 + bvs , where b 6= 0.

    In Figure 1 we show the dependence of the bit length P on successful retrieval
of symmetric Hadamard sequences by LLL basis reduction of the generator ma-
trix G given in (17). At each N for which such a sequence exists we plot the
smallest P for which the retrieval was successful. We see that P appears to grow
linearly with N . This behavior is below the quadratic growth required by LLL for
solving a single random subset sum problem of the same size, but well above the
probabilistically argued bounded bit-length required for solution uniqueness.

    Whereas any polynomial growth of the required bit length of the Fourier mag-
nitude “data” is consistent with a polynomial-time algorithm, that the data preci-
sion must grow at all eliminates the fixed-precision variant of bit retrieval. We
will use the symmetric Hadamard instances to show that the lattice basis reduction
algorithm also fails to solve noisy bit retrieval.

    Symmetric Hadamard sequences (appendix 9.1) exist for all prime lengths N ≡
1 (mod 4) and are interesting because of their low autocorrelations, ak ∈ {−3, 1},
k 6= 0. For any such sequence there exists an e ∈ EN such that the noisy autocor-
relation n = a + e has nk = −1, k 6= 0. The smallness of the k 6= 0 autocorrela-
tions, relative to a0 = N , has by (3) the effect that the q 6= 0 Fourier magnitudes
are nearly equal. Using the fact that the symmetric Hadamard sequences have the



                                        10
Figure 1: Growth in the minimum bit length P required for successful bit retrieval
of symmetric Hadamard sequences of length N by the LLL basis reduction algo-
rithm.

                      √
property ŝq = sq + 1/ N , their Fourier magnitudes take two values:

                       √                    1 2
                  âq / N = |ŝq |2 = ±1 + √    ,            q 6= 0.             (22)
                                             N

When this noise-free data for a symmetric instance of bit retrieval is given as input
to the LLL basis reduction algorithm above, we can retrieve the sequence in poly-
nomial time. But suppose we are instead given the noisy data, where nk = −1,
k 6= 0. What should we expect of the LLL method when the Fourier magnitudes,
                                √       1
                           n̂q / N = 1 − ,          q 6= 0                       (23)
                                        N

obtained from n are used instead of (22)? Experiment shows that the algorithm
in this case succeeds only up to N = 73, and then only up to a maximum bit
length Pmax . For P > Pmax the difference between (22) and (23) has grown to
be so large in the basis G that vs , defined by (21), is no longer a short vector (and
found by LLL); in particular, Pmax = 5 when N = 73. With the addition of noise
our polynomial-time algorithm did not simply suffer a decline in performance: it
ceased being an algorithm altogether.

                                         11
    We expect a similar vulnerability to noise of the best known algorithm for non-
symmetric instances of bit retrieval. This is the algorithm developed by Howgrave-
Graham and Szydlo [HGS], recently generalized by Lenstra and Silverberg [LS] to
other groups. The first step of the HGS algorithm calls for the prime factorization
of the product
                         NY−1 √        NY    −1
                                                   N |ŝq |2 ,
                                                            
                                  N âq =                                      (24)
                              q=1                      q=1

a perfect square integer whose square root coincides with the norm of s when
the latter is viewed as an integer in the cyclotomic number field. This first step
dominates the complexity, growing as exp O(M 1/3 ) when using the number field
sieve to factor M -bit norms, where M = O(N log N ). Still, this growth is far
superior to any known algorithm that tolerates noise. However, were we to replace
â in (24) with its noisy counterpart n̂, we have a problem because the resulting
integer already fails at being a perfect square1 .



3       Hardness

The product of the Fourier magnitudes of the sign sequence being retrieved has
already made two appearances. First, in the lattice basis reduction algorithm for
symmetric instances, we see from the generator matrix (17) that this product is the
sequence-dependent factor in the lattice determinant. The second appearance was
in the cyclotomic-integer norm (24) that has to be factored in the sub-exponential-
time HGS algorithm as a first step in solving general instances. In the pres-
ence of noise, when neither of these algorithms can be used, we will see that the
exponential-time algorithms that take their place have a similarly strong depen-
dence on the Fourier magnitude product. These observations motivate the follow-
ing definition of a hardness index:

Definition 3.1. The bit retrieval hardness index h(s) of a sequence s is the geo-
metric mean of the Fourier magnitudes

                                   |ŝq |2 : q 6≡ −q
                               
                                                       (mod N ) ,                             (25)

that is, those where the corresponding phases are not restricted to ±1.
    1
     While there is noise in cryptography too, this was not the case for the intended application of
HGS, where by averaging sufficiently many digital signatures and rounding, one has access to the
true norm.


                                                 12
    The index is useful because it is easily computed from the bit retrieval input. It
vanishes if any one of the magnitudes vanishes. This is appropriate, since the mag-
nitude constraints for those q can then be replaced by simple equality constraints.
When N is odd, the arithmetic-geometric mean inequality gives the following up-
per bound:
                                              N −1
                                      1 X
                        h(s) ≤            |ŝq |2                                (26)
                                    N −1
                                           q=1
                                    N − |ŝ0 |2
                                =                                               (27)
                                      N −1
                                    N − (1/N )           1
                                 ≤                =1+ .                         (28)
                                       N −1             N
The two means are equal    √ if and only if all the q 6= 0 Fourier magnitudes are
equal; this and |ŝ0 | = 1/ N may be taken as the defining properties of the perfect
Hadamard sequences (appendix 9.1). The latter require N ≡ 3 (mod 4); when
N ≡ 1 the slightly imperfect, though symmetric Hadamard sequences that take
their place have two-valued q 6= 0 Fourier magnitudes and the slightly smaller
index h(s) = 1 − 1/N . When N is even the estimate must be modified since |ŝ0 |
can vanish; the resulting upper bound is then 1 + 2/(N − 2).

    The relationship of the hardness index to the complexity of constraint satisfac-
tion algorithms is particularly direct. Consider the autocorrelation constraint set
A(a) ⊂ RN defined (for general N ) by
                    n                       √                       o
            A(a) = x ∈ RN : |x̂q |2 = âq / N , 0 ≤ q ≤ ⌊N/2⌋ .                 (29)

Geometrically A(a) is the Cartesian product of pairs of points, associated with
q = 0 and also q = N/2 when N is even, as well as ⌊(N − 1)/2⌋ circles associated
with the remaining q for which q 6≡ −q (mod N ). A reasonable general strategy
for bit retrieval is to devise a scheme that systematically samples A(a) at some
resolution, identifying promising candidates by the proximity of their coordinates
to ±1. With uniform sampling, the number of sample points at fixed resolution
will be proportional to the volume of A(a):
                                                 ⌊(N−1)/2⌋
                            vol(A(a)) ∝ h(s)         4       .                   (30)

     The RRR constraint satisfaction algorithm (section 6) generates samples by
iterating a map RN → RN constructed from the projection to A(a) and also the
projection to the hypercube,
                  B = x ∈ RN : xk = ±1, 0 ≤ k ≤ N − 1 .
                       
                                                                           (31)

                                         13
Figure 2: Growth in the iteration count of the RRR constraint satisfaction algo-
rithm (section 6) with the hardness index h. Shown are data for N = 101, 10
random instances at each of five values of the index. The circular markers give the
geometric means of the data in each group.



Figure 2 shows the behavior of the RRR iteration count when solving random N =
101 instances selected for five values of the hardness index. The h ≈ 1 symmetric
Hadamard sequence is too difficult for these experiments, but if we include an
extrapolation from shorter symmetric Hadamard sequences that can be solved (Fig.
15), the iteration count has an upper range near 2 × 1011 . The RRR algorithm is
currently the best known for bit retrieval with noise. Since the volume (30) for
N = 101 changes by 1.6×109 as h ranges between 0.3 and 0.7, the RRR algorithm
must be doing something better than uniformly sampling the set A(a) because the
iteration count between those extremes changes by only 3.5 × 104 .

    It is for the hardest, or noisy versions of bit retrieval that the hardness index
provides the greatest utility. The Fourier
                                       √ magnitudes√ are then approximated by the
noisy autocorrelations: |ŝq |2 = âq / N ≈ n̂q / N . Again, the hardness index
will vanish if any of the magnitude approximations is consistent with zero when
noise is taken into account.

    We define average-case instances by the property that their hardness index is
near the median for random sequences of the same length. To generate these, we
start with many random sequences, sort them by their indices, and extract a small

                                         14
sample at the center of the sorted list. In the limit of large N the random variable
h(s) has a narrow distribution (appendix 9.2) so that average-case instances are
characterized by the average hardness:

                                hhiδ ∼ 4δ(1 − δ)e−γ .                               (32)

Here γ ≈ 0.577 is Euler’s constant and h· · · iδ denotes the expectation value in
a slightly generalized distribution, where the signs are still independent but might
have a bias:
                       hsk iδ = 1 − 2δ,      0 ≤ k ≤ N − 1.                     (33)
The parameter δ corresponds to the density of −1’s in the sequence. For unbiased
signs the average-case hardness is e−γ ≈ 0.561. Not surprisingly, small δ corre-
sponds to an easy limit of bit retrieval.



4      Sparsity

When the density δ of −1’s in a sequence s is small, the Fourier magnitude |ŝ0 |2
is large and all others small; the resulting hardness h(s) will then be low. A more
direct way to see that bit retrieval in this limit is easy is to consider the polynomials
b(x) ∈ ZN introduced in section 2 with coefficients bk = (1 − sk )/2 ∈ {0, 1}.
These polynomials are sparse in the usual sense of having only a few terms. The
autocorrelation b(x)b(1/x) is now the input for bit retrieval and may also be sparse.
Bit retrieval in the low density limit is therefore the problem of reconstructing a
sparse polynomial from its sparse autocorrelation.

    Our analysis of sparse bit retrieval is limited to the noise free case and uses
the framework of cyclic difference sets. The difference set D is the set of powers
in b(x) while the group set G is the multiset of nonzero elements in D − D that
appear in b(x)b(1/x). For example, if N = 5 and

                                 b(x) = 1 + x + x2 ,                                (34)

then

                               D = {0, 1, 2}                                        (35)
                               G = {1, 1, 2, 3, 4, 4}.                              (36)

When D has K elements the number of elements in G is K(K − 1). Cyclic
difference sets are combinatorial designs where D’s are constructed such that G

                                           15
contains all the elements 1, . . . , N − 1 with equal multiplicity. This property is far
from satisfied in the sparse limit K ≪ N . Bit retrieval in the language of cyclic
difference sets is the problem of reconstructing D given G.

    We will analyze a simple back-tracking tree search algorithm for reconstructing
a difference set D from a group set G. The depth k in the tree corresponds to the
number of elements of D that have been proposed. When depth k = K is reached,
and the differences D − D coincide with G, the algorithm terminates.

    Without loss of generality we may take the first element of D to be 0. Subse-
quent elements are proposed from the perspective of the 0 element of D. Specifi-
cally, each of the remaining K − 1 elements of D must at least be elements of G.
In addition, for each proposed new element of D the differences with the nonzero
elements of D must also be checked for membership in G. When a proposal at
depth k is successful, the newly added kth element of D is said to claim k − 1 el-
ements of G and make them unavailable for subsequent proposals at greater depth
in the tree. This can be done efficiently by maintaining a set G′ of unclaimed el-
ements of G. The elements in G′ are proposed in turn until a successful one is
found whereupon the depth is incremented. If none of the elements in G′ produces
a successful proposal, the depth is decremented, the proposal at that level declared
unviable, and the next element of G′ (for that level) is considered.

    By ordering the elements in G, and preserving that order in the unclaimed
elements G′ , set membership can be checked efficiently. The ordering of G also
determines the order in which the elements of D are proposed.

    Our analysis of the runtime is in the limit of large N , and where the average
multiplicity of the elements of G is held constant. In the language of bit retrieval,
this corresponds to the limit where the average coefficient of b(x)b(1/x) stays
constant (excepting the coefficient of x0 ). We define the mean multiplicity as

                                      K(K − 1)   K2
                                µ=             ∼    = δ2 N.                         (37)
                                       N −1      N
                                                                                p
By keeping µ constant in the large N limit, the density decreases as δ ∼            µ/N
and so does the hardness, since h ∼ (4e−γ )δ.

    There are two regimes, depending on the frequency of the zero multiplicity
elements (differences completely missing from G). We model2 the elements of a
random G as Poisson samples from the set {1, . . . , N − 1}. In this model, the
   2
       This is a model insofar as only very special G correspond to any D.


                                                  16
probability of multiplicity 0 is e−µ . When an element of G is proposed as an
element of D at depth k of the tree, the probability of success is less than
                                    (1 − e−µ )k−1 ,                            (38)

because the mean multiplicity µ of the unclaimed elements G′ decreases with the
depth k. The simplest regime is the case µ ≪ 1, where the success probability
in our random model decays as µk . This means that proposals are almost never
successful by luck, but only because the proposed element belongs to the true dif-
ference set D. In this regime of µ there is almost never any backtracking: the
algorithm simply runs through the elements of G in turn, collecting those elements
that belong to D and skipping over the rest (which are eventually removed as dif-
ferences to non-zero elements). The runtime has a O(K 2 ) contribution from the
proposals aborted almost always after a single G-membership check, and another
O(K 2 ) contribution, cumulatively, from checks that proved successful. Altogether
then, the complexity is O(µN ) when µ ≪ 1.

    When µ ≫ 1 the search tree acquires width and backtracking contributes sig-
nificantly to the complexity. Again using the Poisson model, an estimate of the
number of successful proposals at depth k (search tree nodes) is
                                        
                                  N −1                k
                        n(k) =             (1 − e−µ )(2) .                 (39)
                                   k−1
Apart from the 0 element at depth k = 1, the algorithm will try all combinations
of the nonzero elements because the probability any of them has zero multiplicity,
e−µ , is very small. We restrict ourselves to depths k ≪ K so that our estimate (39)
is still accurate when we account for the fact that proposals at lower depths have
claimed a fraction (k/K)2 of the elements of G. Applying Sterling’s approxima-
tion and µ ≫ 1 to (39), we find (details in appendix 9.3) that the search tree has
maximum width n(k∗ ) for
                             k∗ ∼ eµ log N,      N → ∞.                        (40)
                         √
This is subdominant to       µN ∼ K, consistent with our assumption k ≪ K.

   Our runtime estimate for the case µ ≫ 1 is the work performed up to reaching
depth k∗ , where the tree has the most nodes. The algorithm will make
                               
                         N −1           µ
                                   ∼ N e log N ,    N →∞                   (41)
                         k∗ − 1
proposals before it finds one of the n(k∗ ) successful ones, and one of these in
particular that has a branch that extends all the way to k = K. Since solutions

                                          17
(difference set reconstructions) are unique up to symmetry when there is no noise,
the algorithm will make this number of proposals, reduced by symmetry, before
a correct k∗ -element subset of D is discovered. As there are 2K solutions that
have 0 ∈ D, the symmetry reduction is O(δN ) and subdominant relative to (41).
There are (k∗ − 1)(k∗ − 2)/2 checks of G-membership that go with each proposal,
but since this is O((log N )2 ), its contribution to the complexity, multiplicatively,
is subdominant. Contributions from work performed at greater depths are also
subdominant.

     Our analysis shows that the complexity of difference set reconstruction by
back-tracking tree search crosses over from O(N ), in problems where the mean
multiplicity µ is fixed at small values, to the variable-exponent form (41), when
µ is fixed at large values. Though the latter case still corresponds to ever sparser
problems as N grows, the exponential behavior of the exponent with µ makes the
back-tracking algorithm impractical for even modest µ. This behavior is in sharp
contrast with the RRR algorithm, whose behavior with respect to hardness was al-
ready reported in section 3. Figure 3 shows the behavior of the RRR iteration count
with N when µ is fixed at 2, 4, 6 and 8. Although there is exponential growth in the
iteration count with µ, the exponent of N in all cases is small, perhaps even con-
sistent with zero. Since the complexity of a single RRR iteration is O(N log N ),
the RRR algorithm apparently maintains a low exponent complexity with N in a
sparseness regime (large µ) where the back-tracking algorithm does not.

     Phase retrieval in crystallography, to the extent that it can be modeled by bit
retrieval, corresponds to the sparse limit. In a protein crystal the nitrogen, carbon
and oxygen atoms scatter x-rays with similar strength and much more strongly than
hydrogen. It is therefore not a bad approximation to model the contrast as equal
1 bits in a field of 0’s. The number density of non-hydrogen atoms in a protein
                            3
crystal is roughly 10−2 /Å , and the best diffraction data can resolve the contrast
                  3
to a scale of 1 Å voxels. From these two numbers we infer δ ≈ 10−2 . However,
as the analysis of the back-tracking algorithm has shown, bit retrieval can be hard
even when δ is small. The more relevant parameter is the mean multiplicity, given
by the product µ = δK, where K is the number of 1’s (number of non-hydrogen
atoms). It is interesting that the largest structures solved by strict phase retrieval,
or “direct methods” [US], have K ≈ 103 and therefore µ ≈ 10.




                                          18
Figure 3: Slow growth of the RRR iteration count with N when the mean multi-
plicity µ is held fixed. The four plot symbols correspond to the indicated µ values.
Each solid data point is the geometric mean of 20 random instances; empty circles
show the scatter in the 20 instances for the series with µ = 2.

5    Convex relaxation

In the presence of noise, and without sparsity, we do not even have a sub-expo-
nential-time algorithm for bit retrieval. The challenge is then to find the algorithm
that minimizes c in the exponential complexity 2cN . While always bleak in prac-
tical terms, from a theoretical perspective an exponential complexity has the re-
deeming feature that we can be cavalier about the implementation, as those details
usually contribute only a polynomially dependent factor.

    As a first attempt to bound c away from 1 we can ask: How small of a fraction
of the signs, upon being given guessed values, allows for an easy determination
of the extensibility of the guess into a complete solution? Here “easy” refers to
any polynomial-time computation. Perhaps the simplest algorithm of this kind is
based on the observation, that if the first k signs are guessed and only the remaining
N − k are treated as unknowns, then for suitable k there will be at least N − k
of the quadratic autocorrelation equations (2) that are linear in the unknowns. By
simple counting we arrive at the sufficient condition

                                k ≥ N − ⌊N/2⌋/2.                                 (42)

                                         19
In the absence of noise, the N − k linear equations for N − k real variables can
be solved by Gaussian elimination or, in the presence of noise, the linear inequal-
ities are solved by linear programming. We are done if there is a solution/feasible
point where all the variables are ±1 and also satisfy the remaining quadratic equa-
tions/inequalities; if not, we make another guess for the first k signs and repeat.
This analysis fails for the class of instances where every k-subsequence of the so-
lution signs gives a singular matrix for the linear system. Assuming our instance
is not in this class, then trying all 2k guesses gives an algorithm with c = 3/4 by
(42). This is surely a very poor bound on c since the method uses only half of the
available autocorrelation data3 .

     We can get a smaller constant c with an algorithm that uses all the autocorre-
lation data, as well as bounds on the variables. Starting from the constraint sets
A(a) and B introduced in section 3, the improved algorithm follows from the ob-
servation that all x ∈ B have the same 2-norm and therefore the autocorrelation
constraint set may be made convex:
                     n                      √                       o
             A(a) = x ∈ RN : |x̂q |2 ≤ âq / N , 0 ≤ q ≤ ⌊N/2⌋ .               (43)

The statement x ∈ A(a) ∩ B implies x ∈ A(a) ∩ B because all the inequalities
in (43) have to be saturated in order that x has the required 2-norm. Bit retrieval
remains hard because B is still non-convex.

    The feasibility of a partial assignment of ±1 values to the variables in the
constraint satisfaction problem can now be tested by solving a convex problem.
Choosing to assign values in consecutive order, we define the following convex
relaxations (facets) of the hypercube constraint set:
                                                                      
                                         x = sk , k ∈ {1, . . . , K}
          B(s1 , . . . , sK ) = x ∈ RN : k                               .  (44)
                                         |xk | ≤ 1, k ∈
                                                      / {1, . . . , K}

If we find that the convex set A(a)∩B(s1 , . . . , sK ) is empty, then we know that the
solution does not have consecutive signs s1 , . . . , sK . The tree of sign assignments
is searched exactly as in the branch and bound algorithm for integer programming.
Whenever the set intersection is not empty, K is incremented; otherwise, xK is
assigned the other sign, or if that has already been tried, K is decremented.

   The problem to be solved at each node of the branch and bound tree is finding
a point in the intersection of two convex sets or producing a proof that such a
   3
     Curiously, when N is divisible by 3 the bound drops to c = 2/3. Rather than guess the first k
signs, in this case we guess the signs at all k ≡ ±1 (mod 3) and solve N/3 equations/inequalities
that are linear in the remainder.


                                               20
point does not exist. This is solved by the ellipsoid method [K] in polynomial
time when we are provided with two things: (i) a lower bound on the volume
of any feasible region, and (ii) a polynomial-time separation oracle. The first
condition simply excuses us from failing to find feasible points when the volume of
the feasible region is too small. We should therefore only use the proposed branch
and bound algorithm for fixed-precision bit retrieval, where the noise parameter η
gives us license to very slightly weaken the inequalities in (43) as well as thicken
the hypercube facets (44) so as to make them full-dimensional. These refinements
give the volume of the feasible region a lower bound.

    A separation oracle for convex set C, when given a point x, either declares
x ∈ C or returns a hyperplane that separates x from C. Such an oracle can be
implemented in polynomial time when, as in our problem, C = A ∩ B is the
intersection of two convex sets and projections PA and PB to these sets can be
computed in polynomial time. The projection of point x to A (and analogously for
B) is a point PA (x) ∈ A that minimizes the 2-norm to x up to a bound set by the
precision4 .

    The implementation of the separation oracle with projections encounters two
cases. After computing pA = PA (x) and pB = PB (x), either x = pA = pB
and we know x ∈ C, or one of the projections, say pA , is distinct from x. The
required hyperplane, in the second case, is the co-dimension-1 hyperplane that
passes through pA and is orthogonal to the line passing through x and pA . That
this is a valid separating hyperplane is explained in the caption to Figure 4.

    The projections to A(a) and B(s1 , . . . , sK ) can be computed in O(N log N )
and O(N ) time, respectively. To project to A(a) we note that since the Fourier
transform preserves the 2-norm, we may work with the inequalities in (43) di-
rectly. The 2-norm minimizing projection map either leaves x̂q unchanged, if the
magnitude inequality is satisfied, or replaces the magnitude of x̂q by the magni-
tude that saturates the bound (leaving the phase unchanged). The complexity of
the computation is dominated by the fast Fourier transform, first from x to x̂, and
then back to x. Projecting to the facet (44) involves either replacing xk by sk
when k ∈ {1, . . . , K}, or when k ∈ / {1, . . . , K}, leaving xk unchanged when its
magnitude does not exceed 1, or replacing it by ±1, whichever has the same sign.
Both projections are easily modified, with almost no additional effort, when the
constraint sets are replaced by their noisy counterparts.

   4
     The computed projection is within a ball of radius set by η of a true distance minimizing point
in A. Note that in the finite precision context A is a finite set and one makes no distinction between
the closed and open topology.


                                                 21
Figure 4: Separating hyperplane construction by projections. The point x has been
projected to pA = PA (x), the nearest point on convex set A. The proposed hyper-
plane is shown passing through pA and orthogonal to the line between pA and x,
with the feasible region that contains C = A ∩ B shown shaded. If there existed a
point p′ ∈ C not in the region defined by the hyperplane, then because C is convex,
all the convex combinations of pA and p′ (dashed line) would also belong to C. But
that is impossible because then there would be a point in C ⊂ A closer to x than
pA (in the convex combination and close to pA ).

    Because we have a lower bound on the volume of the feasible set and a sep-
aration oracle that can be implemented in polynomial time, the convex feasibility
problems we need to solve at the nodes of our branch and bound tree can be solved
in polynomial time. The complexity is therefore dominated by the exponential
growth in the number of nodes. Finding good bounds on the number of nodes at
depth K, n(K), is a difficult problem for a general instance with autocorrelation a.
However, using sampling techniques we have been able to learn much about n(K)
and estimate the constant c of the branch and bound algorithm.

   We can express the number of nodes at depth K as
                               n(K) = 2K p(K|a),                               (45)
where p(K|a) is the probability, conditional on the autocorrelation a of the con-

                                        22
Figure 5: Scaled log-tree-width w(y) versus fractional tree depth y, of the branch
and bound bit retrieval algorithm for five average-case N = 48 instances.

straint (43), that a randomly selected facet (44) produces a feasible point in the
convex constraint problem. By sampling many random facets of the hypercube
(length-K sign sequences) this probability can be determined to sufficient preci-
sion that we get a good estimate of n(K). Anticipating exponential growth, we
define the scaled logarithmic tree-width:
                       1                   1
                 w=      log2 n(K) = K/N +   log2 p(K|a).                     (46)
                       N                   N
For small K almost all sign sequences produce a feasible point, n(K) ∼ 2K , and
w ∼ K/N . When K is near the upper end of its range, w will return to zero in the
case of low noise, since solutions and n(N ) have vanishing entropy. This behavior
is displayed in Figure 5 for five N = 48 average-case instances we sampled. The
log-width w is plotted against the fractional depth y = K/N because we anticipate
that w(y) will have a similar shape for different sizes N , at least when comparing
instances of the same hardness.

    To determine the exponential complexity we note that, due to the symmetry
of solutions, on average a O(1/N ) fraction of the nodes at the fractional depth
y ∗ = K ∗ /N of maximum log-width w(y ∗ ) have to be explored before a branch is
found that extends to K = N . Including the work performed at other depths only
contributes a polynomial factor (the total depth is N ), as does the polynomial-

                                        23
                                                                    ∗
time work performed at each node. Since n(K ∗ ) = 2w(y )N , we estimate the
complexity constant as
                              c = max w(y).                            (47)
                                            y

Although there is considerable variation from one instance to another, we see from
Figure 5, that at least for average-case N = 48, the tree has greatest width near
y = 0.5 and c ≈ 0.36.

     We obtain much better evidence of w(y) converging to a large-N limit (as in
statistical mechanics) when we consider special families of instances. We chose
the perfect Hadamard sequences as these maximize the hardness index. The con-
stant (47) derived from this family should be a strong candidate for the worst-case
complexity of the branch and bound algorithm. Figure 6 shows the log-widths for
perfect Hadamard instances of size N = 20, 40, 80 and 160. The noise free, k 6= 0
autocorrelations for all these instances is ak = −1. Though solutions in the ab-
sence of noise exist only for particular odd N , the small noise required to have
solutions at the chosen N should have negligible effect on the complexity of this
algorithm, which is determined by the widest part of the tree. Since we are mostly
interested in the complexity bound, our samples were confined to depths where the
search trees have their greatest width.

    The maxima of the four w(y) curves for prefect Hadamard instances have a
systematic behavior5 with N and enable us to extrapolate, in Figure 7, both the
fractional depth of the maximum and the value at the maximum to their N = ∞
values. We find y∞ ≈ 0.630 and w(y∞ ) ≈ 0.564. Our bound for the exponential
complexity constant is therefore c < 0.564. Although much worse than average-
case, this is still significantly better than the bound c < 3/4 obtained at the start
of this section, where the tree is searched exhaustively to fractional depth y = 3/4
and the remaining variables are found by solving linear equations.



6       Relaxed-reflect-reflect algorithm

The RRR algorithm has an element of randomness making the run-time unpre-
dictable. Figure 8 plots the distribution of run-times (iterations) in 2 × 105 solu-
tions of the N = 43 Hadamard instance. The most probable runtime is near zero
and the distribution decays exponentially, for a mean run-time of 1.7 × 105 itera-
    5
    We have no reason to suspect that those values of N for which perfect Hadamard sequences
actually exist would deviate from the observed behavior.


                                            24
Figure 6: Behavior of the scaled log-tree-width w(y) of the branch and bound
bit retrieval algorithm as the sizes of Hadamard instances are doubled. Both the
location and value of the maximum appear to be converging. Extrapolations of the
location y ∗ and value w(y ∗ ) from these data are shown in Figure 7.




Figure 7: Extrapolations of the data in Figure 6, assuming the finite-N corrections
to y ∗ and w(y ∗ ) are respectively proportional to N −1 and N −1/2 .




                                        25
Figure 8: Exponential distribution of run-times (iterations) of the RRR algorithm
in 2 × 105 solutions of the N = 43 Hadamard instance.


tions. These statistics are consistent with an algorithm that blindly and repeatedly
reaches into an urn of M solution candidates, terminating when it has retrieved
one of the 4 × 43 solutions. Two questions immediately come to mind. The easier
of these is: How can an algorithm that is deterministic over most of its run-time
behave randomly? The much harder question is: How did the M = 243 solution
candidates get reduced, apparently, to only about 1.7 × 105 × (4 × 43) ≈ 225 ?

    A very simple strategy for expanding the reach of naive sampling uses the pro-
jections to the two constraint sets introduced in section 3, A(a) and B. Projection
PA(a) (x) is the sequence having smallest 2-norm distance to x and autocorrelation
a, and PB (x) is the ±1 sequence obtained from x by rounding. Suppose we start
with a sequence of signs x0 . If PA(a) (x0 ) = x0 we are done, because our guessed
signs have the correct autocorrelation; otherwise, we construct the nearest sign se-
quence: x1 = PB (PA(a) (x0 )). We continue doing this until we find a solution or,
more probably, a fixed point xi+1 = PB (PA(a) (xi )) = xi that is not a solution
(PA(a) (xi ) 6= xi ). From experiments we find that non-solution fixed points are
encountered after just a few iterations and differ from the initial guess by a Ham-
ming distance of only about N/30, for Hadamard instances of size N . Although
this method is an improvement over naive sampling, the fraction of signs that the
projections modify is too small to make a useful algorithm.

                                        26
     The RRR algorithm is a far superior method of generating samples. Origi-
nally proposed (without relaxation) by Bauschke, Combettes and Luke6 [BCL] as
a method for finding two points that achieve the minimum distance between two
convex sets, much of the analysis that applies in that setting has little relevance
for the highly non-convex constraints of bit retrieval. In particular, it is no longer
useful to study convergence, or the notion that the algorithm makes systematic
progress towards solutions. A potentially more productive goal, given the circum-
stances, is to discover general principles for iteratively constructing good samples,
and in particular, understanding how this is achieved by the RRR algorithm. This
is the approach that we will take.

     The algorithm is usually initialized with some x ∈ RN produced by a random
number generator. This is the only explicit use of randomness and provides a means
for exploring statistical properties, such as the run-time distribution in Figure 8.
There are no initial x that are inherently better or worse than others; in fact, the
initial x may even be a sequence of signs. After selecting the initial x, the following
map is applied iteratively:
                 x 7→ x′ = x + β PA(a) (2PB (x) − x) − PB (x) .
                                                                    
                                                                                   (48)
Here β is a real parameter with the restriction 0 < β < 2 as explained below.
The samples of interest to bit retrieval are PB (x), not x. Unlike the earlier scheme
for generating samples, here we find that fixed points are always associated with
solutions. Suppose x∗ is a fixed point; then, since
                          0 = PA(a) (2PB (x∗ ) − x∗ ) − PB (x∗ ),                             (49)
we see that PB (x∗ ) is in the range of PA(a) , indicating it is a sequence having the
required autocorrelation.

     For the fixed points of the RRR map to be the basis of an algorithm, it is
necessary that these are attractive. To analyze this local property we consider a
pB ∈ B that is either a solution, so pB ∈ A(a) ∩ B, or a near solution. A near
solution pB ∈ B has the property that the projection pA = PA(a) (pB ) is very close
to pB , as measured by the 2-norm. In either case, we can study the behavior of the
map for x that are near to both pA and pB . For such x, PB (x) = pB , since all other
elements of the hypercube B are more distant, and A(a) may be approximated by
its tangent space, an affine space whose proximal point to pB is pA . The dimension
of the affine space is M = ⌊(N − 1)/2⌋, the number of circles in the Cartesian
product description of A(a).
   6
     Although Douglas and Rachford are usually given credit for the first application, [BCL] were
the first to notice, more generally, the averaged-alternating-reflection structure of the iteration.


                                                27
    For the local analysis of the near solution case we use pB as the origin and the
orthogonal decomposition RN = R1 ⊕ RM ⊕ RN −M −1 , where the first component
is parallel to pA − pB , the second component is the linear space (approximation of)
A(a) − pA , and the last component is the orthogonal complement of these. In this
decomposition a general point is written as

                                x = x1 ⊕ xA ⊕ x⊥ ,                              (50)

and the two constraint sets have the form

                             A(a) = dA ⊕ RM ⊕ 0                                 (51)
                               pB = 0 ⊕ 0 ⊕ 0,                                  (52)

where dA = kpA − pB k. Using the following formulas for general (local) projec-
tions,

                           PA(a) (x) = dA ⊕ xA ⊕ 0                              (53)
                              PB (x) = 0 ⊕ 0 ⊕ 0,                               (54)

we obtain the result of one iteration of the RRR map (48):

                      x′ = (x1 + βdA ) ⊕ (1 − β)xA ⊕ x⊥ .                       (55)

This formula is valid also for the true solution case, dA = 0, the only difference
being that there now is no longer a distinction between the R1 and RN −M −1 com-
ponents of the orthogonal decomposition.

    When dA = 0, we see from (55) that we have the stable fixed points

                                x∗ = x1 ⊕ 0 ⊕ x⊥                                (56)

if and only if |1 − β| < 1, the condition asserted earlier. A more precise statement
is that we have a N − M dimensional space of fixed points. All points in this
space produce the same bit retrieval sample, pB = PB (x∗ ), a solution. In the
case of a near solution, dA > 0, although there is no longer a fixed point, the
RRR map is still contracting in the M -dimensional tangent space approximation of
A(a). While it is the unidirectional motion in the first component, x′1 = x1 + βdA
(purposeful escape from a non-solution), that is usually credited for the algorithm’s
success [ETR], the contracting behavior that goes with it may be just as significant.

   The algorithm’s name derives from the fact that the map (48) can be written
more compactly,

                     x 7→ x′ = (1 − γ)x + γ RA(a) ◦ RB (x),                     (57)

                                         28
Figure 9: Cartoon showing a single application of the RRR map to the point x. The
result after two reflections, first RB and then RA , is averaged with x according to
the value of the parameter γ (a point along the dashed line). When the distance
between A and B is smaller than the distance of either set to x, the chief effect of
the map is to move x parallel to the tangent space of A.


in terms of the reflections

                              RA(a) (x) = 2PA(a) (x) − x                       (58)
                                RB (x) = 2PB (x) − x,                          (59)

and where γ = β/2 looks like a relaxation parameter. Figure 9 shows how the com-
bination of two reflections followed by the γ-average has the effect of contracting
along the tangent space of the A(a) constraint. The case γ = 1/2 is called AAR
for averaged-alternating-reflections [BCL]. We argue later in this section that, in
combinatorially hard feasibility problems such as bit retrieval, it is important to
keep γ small.

    Part of the attractiveness of the RRR algorithm is the ease of its implementa-
tion. The computations involve almost exclusively floating point numbers. Most of
the work in one iteration of (48) is the pair of FFT’s needed to perform the rescal-
ing of the Fourier magnitudes to their known values. Even with single precision

                                         29
floating point numbers, so that η in (10) is of order 10−7 , we do not compromise
solution uniqueness until N has grown as large as η −2 . For all practical purposes
then, we can use a floating point RRR implementation to solve noise-free bit re-
trieval.

    Since solutions correspond to fixed points of the RRR map, termination is
linked to the value of kx′ − xk. To eliminate any doubt that this floating point num-
ber has reached a small enough value, we can keep track of the smallest-achieved
value over the course of a run and, whenever there is an improvement, compute
the autocorrelation of PB (x) using integer arithmetic for a foolproof termination
check.

     One concern when using a map to generate samples, when its global behav-
ior is complex, is that the iterates might converge on an unproductive cycle. This
almost never happens for large N ; for the N = 23 Hadamard instance the proba-
bility of convergence to a cycle is already less than 10−3 . Since both PA(a) and PB
have strongly branching behavior when certain numbers (complex and real, respec-
tively) are small in magnitude, it is no mystery why stable cycles are rare. Strongly
mixing dynamics is also the best interpretation of the exponential run-time distri-
bution (Fig. 8) with which we introduced this section. The latter can even be used
to defend a simple safeguard against cycles: frequent random restarts. However,
we did not implement this policy for the RRR results presented here.

    Although it is certainly possible that the optimal value of β depends on N and
the hardness index, we sought a single value for all the experiments performed in
this study. We determined this value by solving the N = 43 Hadamard instance
1000 times from random starts over a range of β values. The median iteration
counts, plotted in Figure 10, have a broad minimum near β = 0.3. The upturn
at small β is explained by the fact that the β → 0 limit of (48) is a system of
differential equations, with β as the time step. In this limit most of the time is
spent between branch points, where the trajectory is only weakly affected by β.
Because the branch points continue to scramble the trajectories for arbitrarily small
β, the character of the trajectory will not change in the β → 0 limit. Since the
probability of stumbling upon a solution (per branch point encountered along the
way) is constant, the median iteration count per solution should scale in proportion
to the number of steps between branch points, β −1 . This explanation is supported
by the data in Figure 10, where we have factored out this time-step dependence and
see that the result is independent of β in the small β limit. Because it looks like the
continuous time limit of (48) is well approximated already with time-step β = 0.3,
we have used this value in all of our experiments unless stated otherwise.


                                          30
Figure 10: Solid circles: Median number of iterations, out of 1000 trials, required
by the RRR algorithm to solve the N = 43 Hadamard instance over a range of β
values. Open circles: Same data but with the inverse time step, β −1 , divided out.



    For RRR to be a proper algorithm for combinatorial search, we should at the
very least have a model of the space wherein the search takes place. Developing
such a model is the subject of ongoing research, and we can only offer some inter-
esting, possibly relevant observations. We take as our primary clue the upturn of
the median iteration count with increasing β, shown in Figure 10. It appears that
RRR performs best in the flow limit, β → 0.

     We have direct information about the β → 0 search space from the statistics
of the magnitudes of the individual components of x. Recall that the iterates x
of the RRR algorithm are rather indirectly linked to the constraint sets. A small
magnitude of component xk , for instance, corresponds to a strong uncertainty in
the sign sk of the projection PB (x). Figure 11 shows the distribution |x| over
all components taken from a single run of the algorithm on an instance with the
Hadamard autocorrelation ak = −1, k 6= 0, but with N = 41 so there is no
solution. We believe RRR is ergodic on these kinds of insoluble instances, and use
a single long run to sample statistical data. To be sure to see flow limit behavior,
we have set β = 0.01. There is a clear anomaly in the distribution at |x| = 0
whose width (detail in right panel of Fig. 11) scales with β. On average about

                                        31
Figure 11: Distribution of the magnitudes of the components of x (detail on right)
in the flow limit (β = 0.01). Data is taken from an insoluble n = 41 Hadamard
instance. As the weight in the anomaly at |x| = 0 is about 15%, or 6 components
of x, the RRR search is confined to codimension-6 Voronoi facets of the discrete
set B.


six of the components of x are exceptionally small in magnitude, the remainder
being broadly distributed. Since zeroes in the components of x correspond to the
Voronoi cell faces of the hypercube B, we conclude that the search (in the flow
limit) is confined to Voronoi cell facets whose codimension is about six in this
problem instance.

     The facet attraction property exhibited by the data in Figure 11 raises two
questions about the RRR algorithm: (1) What is the mechanism for this attraction,
and (2) is this property responsible for the algorithm’s good performance? The
answer to the first question can be explained with the flow field in Figure 12. This
example was constructed to have the codimension-2 attractor (Voronoi-facet) x1 =
x2 = 0. Near the origin of the (x1 , x2 ) plane, the point pB = PB (x) jumps
discontinuously between the four possibilities {−1, 1}2 and this in turn determines
four discontinuous points pA = PA (2pB − x). The RRR flow field is parallel to
pA − pB , and near the origin has the discontinuous structure shown. For finite β
the RRR iterates make finite jumps but stay within a distance of scale β from the
origin. We do not know what determines the codimension of the facets that RRR is
attracted to. The codimension for Hadamard instances appears to be about 0.15N .

                                        32
Figure 12: Facet attraction is a simple consequence of particular flow fields (β → 0
limit of RRR), shown here for a codimension-2 facet. In each orthant of the space
orthogonal to the facet (just four in this example), the flow field (shown projected
into the plane) near the origin is parallel to pA − pB , where pB = PB (x) is the
vector of signs that goes with each orthant and pA = PA (2pB − x). The origin is
a fixed point for the flow shown.



     For the second question above we need to establish that the facet attraction
property has the effect of narrowing the search to a smaller domain that has an
increased rate of finding solutions. A possibly relevant statistic in this regard is
a clustering property of the projections pA . Suppose we have an instance of bit
retrieval with solution pB . Not only do we know that pB ∈ A, but perturbations of
pB will at least be close to points pA ∈ A. If we now consider a set of perturbations
of pB , all with a nearby point pA , then by the triangle inequality we will have a set
of points pA ∈ A all within some bounded distance of each other. The existence
of such a cluster in the set A comes from the fact that the original point pB was a
solution.

    The RRR facet attraction property is our motivation for the following pertur-
bation of a solution pB . Let J be the index set of the components of x that vanish
on a facet whose codimension is |J|. Define xJ as the point obtained from pB

                                          33
by setting to zero all components with indices in J. The projection PB (xJ ) is
undefined on the zero components but arbitrarily small perturbations x̃J , when
projected PB (x̃J ), produce a hypercube of 2|J| points in the space orthogonal to
the facet. The argument of the projection PA in RRR is 2PB (x̃J ) − x̃J , a vector
whose components match the solution pB on the indices not in J and includes all
combinations of ±2 in the rest. This is our special set of perturbations of pB and as
argued earlier, when projected by PA the resulting set of points will cluster when
pB is a solution. What remains is to argue the converse: that the facet attraction
property promotes clustering and thereby increases the odds that a pB generated
by RRR is a solution.

    The relationship between facet attraction and clustering of the projections pA
(of the perturbations of pB ) is also explained in Figure 12. Note that there are
constraints on the vectors pA − pB such that the corresponding flow field is at-
tracting for the origin. These vectors must all lie within solid angles subtended
at vertices of the hypercube {−1, 1}|J| , constraints that are particularly strong in
high dimensions (large |J|). Together with mild assumptions on the magnitudes
kpA − pB k, the effect of these constraints is to bring the pA into proximity of each
other (clustering).

    The N = 41 Hadamard instance we used in our demonstration of facet at-
traction is also well suited to demonstrate the degree of clustering of the points
pA = PA (x′ ) obtained by projecting perturbations x′ of a particular pB . As above,
we consider the set of 2|J| perturbations x′ specified by index set J, where x′
matches pB for indices not in J and has values ±2 on the others. We use the
root-mean-square measure of clustering
                               2
                              σA = h kpA − hpA ik2 i,                            (60)

where the angle brackets are averages over the 2|J| projections pA . Figure 13 shows
distributions of σA for three choices of the base point pB being perturbed. The
distribution with the smallest mean, not surprisingly, is generated by solution points
pB . To produce this distribution we used the two-valued symmetric-Hadamard
autocorrelations ak ∈ {−3, 1}, k 6= 0 rather than ak = −1 (for which there are
no solutions). The σA values have a distribution because we uniformly sample the
index sets J, for |J| = 6.

    For the other two distributions in Figure 13 we used the insoluble autocorrela-
tion data ak = −1, k 6= 0. The distribution with the largest mean was generated
by uniformly sampling pB ∈ B. That the mean for this distribution is higher than
the distribution for a solution point is of course not surprising; the separation of

                                         34
Figure 13: Cluster size (σA ) distributions on constraint set A generated by pertur-
bations of three types of points pB ∈ B: solutions (lowest mean), random samples
(highest mean), samples generated by RRR (intermediate mean). Data are for the
N = 41 Hadamard instance and codimension-6 facets.


the distributions just establishes the scale of the clustering effect. The most inter-
esting distribution is the middle one, for pB samples generated by iterating RRR
(with β = 0.01). We see that RRR has the desired effect of generating samples
pB with better clustering, or solution likelihood, than random samples. Moreover,
the mechanism for the improved clustering is linked to the facet attraction property
(Fig. 12).

    The complexity of the RRR algorithm for bit retrieval can be assessed by the
exponential growth in the number of iterations, since the work in each iteration
has only O(N log N ) growth from the pair of FFTs in the PA(a) projection. Our
experiments support the growth law, ecN , where c is hardness dependent. We report
values of the median of the iteration counts obtained in 20 trials, since we have seen
no exceptions to the exponential form of the iteration distribution on individual
instances (Fig. 8). Figure 14 shows the exponential growth in the median for
average-case instances (h ≈ 0.56). Results are shown for ten instances at each N ,
as well as the geometric means of the ten instances. While there is considerable
scatter with respect to instance, the averages are consistent with an exponential
growth law and c ≈ 0.212.

                                         35
Figure 14: Median iteration count of the RRR algorithm when solving average-
case instances of bit retrieval. Results are shown for ten instances at each N (open
circles) as well as their geometric means (filled circles).




    Figure 15 shows the much faster exponential growth for instances at the upper
limit of the hardness index, h ≈ 1. This study also compares the performance of
the RRR algorithm with and without noise. In the instances with N ≡ 3 (mod 4),
where there exist perfect Hadamard sequences, we gave the noise-free autocorrela-
tion data ak = −1, k 6= 0 as input. In the other set of instances, N ≡ 1 (mod 4),
we specified the noisy autocorrelation nk = −1 ± 2, k 6= 0 for solutions to be
compatible with the symmetric Hadamard sequences. While in the second case
it would have been easy to specialize the constraint projections for symmetric se-
quences, we chose not to in order to have noise be the only contrasting feature. The
results suggest that noise has negligible effect on the complexity constant (slope):
c ≈ 0.513, N ≡ 3 and c ≈ 0.494, N ≡ 1. The scatter of the data points about
the straight lines in the plot is larger than our errors in estimating the median and
therefore is intrinsic to each N . It is interesting that N ≡ 1 instances are easier by
about a factor 180 relative to the N ≡ 3 group.

                                          36
Figure 15: Median iteration count of the RRR algorithm when solving Hadamard
instances. Errors in the estimates of the median are smaller than the scatter of the
points about the straight lines.


7    Summary

We defined three versions of the bit retrieval problem. The noise-free problem
arises in cryptographic attacks of digital signature schemes based on polynomial
rings. While this is the easiest version, the best known algorithm still has subex-
ponential complexity. With noise, even at a level that has no effect on solution
uniqueness, the best algorithms have exponential complexity. This is the version
of bit retrieval that in x-ray crystallography is known as the phase problem.

     Bit retrieval instances of the same size N can have very different difficulty
depending on the hardness index h. In the Howgrave-Graham-Szydlo algebraic
algorithm the hardness index appears as the norm of the cyclotomic integer that
must be factored (as an ordinary integer), while in constraint satisfaction algorithms
it corresponds to the measure of a constraint set. Low-autocorrelation instances of
bit retrieval, the most extreme form of which are solved by Hadamard sequences,
have the highest hardness index.

    The phase problem of x-ray crystallography normally corresponds to the sparse

                                         37
limit of bit retrieval. However, even sparse problems have a difficult regime, as
quantified by the mean multiplicity µ of differences (atom-atom separations), in
the cyclic difference set description of bit retrieval. Iterative constraint satisfaction
algorithms are indispensable in this application of bit retrieval, having solved an
estimated one million crystal structures [S]. Even so, these algorithms have not
received the theoretical scrutiny that normally goes with algorithms that provide a
basic service to scientific investigations.

    We have made a special effort to obtain the best estimates of the constant c
in the exponential complexity 2cN achieved by algorithms that solve the noisy
variant of bit retrieval. There is a simple algorithm that achieves c = 3/4. For
the branch and bound algorithm, based on convex relaxation of the non-convex
constraints of bit retrieval, we obtain the numerical estimate c ≈ 0.564 for the
hardest (h ≈ 1) instances. The best performance, c ≈ 0.504, is achieved by
the least understood algorithm, relaxed-reflect-reflect or RRR. While there is a
vast literature on the application of algorithms like RRR to problems with convex
constraints, their continued success on highly non-convex problems is a curiosity
that has not received the explanation it deserves.

    In bit retrieval there is a simple argument why branch and bound, the RRR al-
gorithm’s closest competitor, is suboptimal. As in integer programming, branching
is performed on a subset of the signs, with bounds arising from convex inequalities
imposed on their complement. But unlike integer programming, in bit retrieval we
are also forced to relax a second set of constraints, on the Fourier magnitudes, in
order that the feasibility subproblems are convex and easily solved. The second
relaxation does not change the feasible set of the complete problem (see section
5), but this manifests itself only once all the signs have been set to definite values.
The branch and bound algorithm may thus follow branches that would have been
discarded by an algorithm that did not need to attenuate the Fourier magnitude
constraints.

    The superior performance of RRR on noisy bit retrieval, relative to well es-
tablished algorithms, is motivation for a better theoretical understanding of this
algorithm. It is likely that the effectiveness of RRR, on hard non-convex problems,
is only weakly linked to its properties in the convex domain. A possible alternative
approach to its analysis was brought to light by our investigations of the flow limit
(β → 0). After correcting for the trivial ‘time-step’ scaling, this limit optimizes
performance. RRR search in the flow limit is confined to facets of the Voronoi cells
of the discrete point set B, the hypercube of signs. A bias in the RRR sampling of
B that favors solutions is consistent with this facet attraction property.


                                           38
8    Acknowledgements

The author thanks the many individuals who have helped shape his understand-
ing of bit retrieval over the years: J. Borwein, J. Buhler, C. Clement, P. Diaconis,
N. Howgrave-Graham, G. Kuperberg, C. Moore, I. Rankenburg, J. Rosenberg, M.
Szydlo. Support was provided by the Simons Foundation and DOE grant DE-
FG02-11ER16210. Most of the work was carried out while the author was a visit-
ing scientist at SLAC.



9    Appendix

9.1 Hadamard sequences

For odd N we define Hadamard sequences to be those ±1 sequences whose sum is
1 and whose k 6= 0 autocorrelations are as small as they can be. To expand on the
last property, note that the identity

                             s1 s2 ≡ s1 + s2 − 1 (mod 4)                       (61)

for signs s1 and s2 implies that

                      N
                      X −1
               ak ≡          sl + sl−k − 1 ≡ 2 − N ≡ N     (mod 4).            (62)
                      l=0

Also, because a0 = N and the sum of the autocorrelations is the square of the sum
of the sign sequence, or 1, the average of the k 6= 0 autocorrelations must be −1.
When N ≡ 3 (mod 4) we can insist that ak = −1, k 6= 0, while for N ≡ 1
(mod 4) the best we can have is ak ∈ {−3, 1}, k 6= 0. The first class of Hadamard
sequences is called perfect.

   For either oddness of N there is a simple construction of Hadamard sequences
when N is prime:
                                 
                           sk =        k
                                         1, k = 0                         (63)
                                       N , k 6= 0.

Because sk is explicitly given by the Legendre symbol, these are called Legendre
sequences. Legendre sequences have the remarkable property [H] that the k 6= 0

                                         39
components of their Fourier transforms are simply obtained by applying a shift
and, in one case, a complex rotation to the sequence itself:
                                   √
                             sk + 1/√N , N ≡ 1 (mod 4)
                    ŝk =                                                (64)
                            isk + 1/ N , N ≡ 3 (mod 4).

For N ≡ 3 the k 6= 0 Fourier magnitudes are perfectly equal while in the other
case the magnitudes become uniform with increasing N . The N ≡ 1 Legendre
sequences are symmetric because their Fourier transform is real.

    In addition to the perfect Hadamard sequences given for prime N by the Legen-
dre symbol, there are also constructions whenever N is the product of twin primes
or one less than a power of two [B].


9.2 Hardness distribution

Freedman and Lane [FL] proved that the distribution of the Fourier transform coef-
ficients ŝq of a sequence s0 , . . . , sN −1 of independently and identically distributed
real random variables converges, for large N , to a distribution of independent and
identical complex-normal distributions for q = 1, . . . , M = ⌊(N − 1)/2⌋. To char-
acterize the distribution we therefore only need to compute the mean and variance
of one of these Fourier coefficients. In the sequence distribution where −1 has
density δ,

                        hŝq iδ = 0,                                                 (65)
                                                 X
                          2
                     h|ŝq | iδ =    hs20 iδ +          i2πkq/N
                                                        e         hs0 sk iδ          (66)
                                                 k6=0
                                = 1 − hs0 s1 iδ = 4δ(1 − δ).                         (67)

Moreover, since
                                                  M
                                         1 X
                              log h(s) =     log |ŝq |2                             (68)
                                         M
                                                 q=1

is the average of M independent and identically distributed real random variables,
it has the central limit property in the limit of large M when the mean and variance
exist. To check the latter, we note that if t = |ŝq |2 is the magnitude of a complex
normal random variable of zero mean and variance σ 2 = 4δ(1 − δ), then t has
probability density
                                                    2
                                             e−t/σ
                                     ρ(t) =           .                          (69)
                                               σ2

                                           40
For large N we therefore know that the log-hardness is concentrated at its mean
value:                        Z ∞
                hlog h(s)iδ =      ρ(t) log t dt = log σ 2 − γ.             (70)
                                    0



9.3 Backtracking tree-width

Applying Stirling’s formula and the asymptotic conditions

                             1 ≪ k ≪ N,        1≪µ                          (71)

to (39) we obtain

                                   k2 −µ
                    log n(k) ∼ −     e + k log N − k log k + k.             (72)
                                   2
We identify the maximum k∗ by the vanishing of the derivative with respect to k:

                        k∗ e−µ ∼ log N − log k∗ ∼ log N.                    (73)

The maximum will be consistent with (71),

                               k∗ ∼ eµ log N ≪ N                            (74)

provided we keep µ fixed (but large) as we take the limit N → ∞.



References

[HGS] N. Howgrave-Graham and M. Szydlo, A method to solve cyclotomic norm
    equations, in Duncan A. Buell, editor, ANTS, Lect. Notes in Comp. Sci. 3076,
    Springer 2004, 272-279.

[GS] C. Gentry and M. Szydlo, Cryptanalysis of the revised NTRU signature
    scheme, Advances in Cryptology, EUROCRYPT 2002, Lect. Notes in Comp.
    Sci. 2332, Springer 2002, 299-320.

[PS] L. Pauling and M. D. Shappell, The crystal structure of bixbyite and the C-
     modification of the sesquioxides, Zeits. f. Krist. 75, 128-142 (1930).

[FL] D. Freedman and D. Lane, The empirical distribution of Fourier coefficients,
     Ann. Statist. 8, 1244-1251 (1980).

                                         41
[LO] J. C. Lagarias and A. M. Odlyzko, Solving low-density subset sum problems,
    J. Assoc. Comp. Mach. 32, 229-246 (1985).

[LLL] A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with
    rational coefficients, Mathematische Annalen 261, 515534 (1982).

[LS] H. W. Lenstra Jr. and A. Silverberg, Revisiting the Gentry-Szydlo algorithm,
     Advances in Cryptology, CRYPTO 2014, Lect. Notes in Comp. Sci. 8616,
     Springer 2014, 280-296.

[US] I. Usón and G. M. Sheldrick, Advances in direct methods for protein crystal-
    lography, Curr. Opin. Struct. Biol. 9, 643-648 (1999).

[K] L. G. Khachiyan, A polynomial algorithm in linear programming, Doklady
    Akademii Nauk SSSR 244, 1093-1096 (1979) [translated in Soviet Mathe-
    matics Doklady 20, 191-194, (1979)].

[BCL] H. H. Bauschke, P. L. Combettes and D. R. Luke, Finding best approxi-
    mation pairs relative to two closed convex sets in Hilbert spaces, J. Approx.
    Theory 79, 418-443 (1994).

[ETR] V. Elser, I. Rankenburg and P. Thibault, Searching with iterated maps,
    PNAS 104, 418-423 (2007).

[S] G. M. Sheldrick, private communication.

[H] B. K. P. Horn, Interesting eigenvectors of the Fourier transform, Trans. R.
    Soc. S. Afr. 65, 100-106 (2010).

[B] L. D. Baumert, Difference sets, SIAM J. Appl. Math. 17, 826-833 (1969).




                                       42
