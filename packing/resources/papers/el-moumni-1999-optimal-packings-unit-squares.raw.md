                    Studia Scientiarum Mathematicarum Hungarica 35 (1999), 281-290

       OPTIMAL PACKINGS OF UNIT SQUARES IN A SQUARE

                                   S. EL MOUMNI




                                      A b stra ct

    Let s(n) denote the edge length of the smallest square in which one can pack n unit
squares whose interiors are pairwise disjoint. We prove that s (7) = 3 and s(15) = 4.




                                  1. Introduction


    In this note we determine, for n = 7 and n = 15, the edge length s(n) of
the smallest square in which one can pack n unit squares whose interiors are
pairwise disjoint.
    In 1975, P. Erdős and R. Graham [1] proved a remarkable theorem: If we
denote by m(z) the maximum number of unit squares that one can pack in a
square of side z, and if w(z) = z2 —m(z), then w(z) = 0 ( z 7/ n ) (7/11 = 0.636).
According to M. Gardner [2], H. Montgomery has improved this asymptotic

result slightly, by proving that w(z) —                        —^ -^ = 0 .6 3 3 ^ .   In

1978, K. Roth and R. Vaughan [4] showed that w(z) ^ 10_100(||z ||z)1/ 2, where
||z|| = inf(|z — [z\\, Iz — |zj —1|)- F. Göbel remarked in [3] that, apart from
the trivial result s(k2) = k for every &€ No, the only values of n for which
s(n) is known are n = 2, 3, 5 (s(2) = 2, s(3) = 2, s(5) —2 + ^ ) , and that E.
Bajmoczy in Budapest established that s(7) = 3, but the proof of this result
has apparently never been published.
      We are going to prove the following results:

    T heorem 1. s(7) = 3.

    T heorem 2. s(15) = 4.



    1991 Mathematics Subject Classification. Primary 52C15.
    Key words and phrases. Packing, squares.
                                   0081-6906/99/$ 5.00 ©1999 Akadémiai Kiadó, Budapest
282                                   S. EL MOUMNI


                              2. Proof of Theorem 1
      We first prove the following propositions:
    PROPOSITION 1. If we pack a unit square C\ in a square C whose edge
length is less than 2, then the center of C belongs necessarily to the interior
of C l
    PROOF. Suppose, on the contrary, that we can pack a unit square C\
in a square C = (abed) of side 2 —2e (e > 0) in such a way that the center o
                              O
of C is not in the interior C i of C\. We denote by a', b', c', d! , respectively,
                                                   O
the midpoint of [a, b], [fo, c], [c, d\, [d,a]. If C\ intersects each of the open
                                                          O
squares (aa'od'), (a'bb'o), (ob'cc'), (d'oe'd), then o E C i , a contradiction. Up
                                                                  O    ____
to a symmetry of the square (abed), we may assume that C\ IT(ob'cc') = (f>.
Denote by C 2 = (oefg) the unit square such that
                         [o, b'] C [o, e] and [o, d] C [o, g\.
Thus we have packed two unit squares C\ and C 2 in a square of side 2 —e,
contradicting the fact that s(2) = 2.
    P roposition 2. If we draw infinitely many parallel lines Aj (i E Z ) in
the euclidean plane E 2 in such a way that the distance between any two
consecutive lines is a constant d satisfying ^  d < 1, then for any unit
square C ,
                       Y \CnAi| ^inf(2 (y/2- d) , l) .
                       ie z
                                   o
    P roof . Since d < 1, we have C d ( |J Aj) ^ f . We now distinguish two
                                        ie z
cases:                                                 O
    Case 1. There exists j E Z such that Aj intersects C in a segment ]pj,qj[,
                                                              O
where pj and qj belong to two opposite sides of C. Then |C D A j| ^ 1, and
so
                       ^ |C lT A .,|;> in f ( 2 ( V 2 - d )   ,l) .
                       iez
                                      o
    Case 2. For each i £ Z , if A; IT C ^ <f>and Aj fl C = \pi, qf\, then pi and qi
belong to two consecutive sides of C. Consider the following two subcases:

    Subcase 1. C intersects only one Aj.
                 O
    Subcase 2. C intersects two consecutive lines Aj and A j+i (it is impos-
          O
sible for C to intersect three consecutive lines, because the diameter of C is
y/2 and 2d^y/2).
                                OPTIMAL PACKINGS                                        283


    Let s i,S 2;S3,S4 be the vertices of C. We have A j D C = \pj, qj], where
Pj and qj belong to two consecutive sides of C. Denote by S3 the vertex
common to these two consecutive sides, by si the vertex opposite to s3 (as
in Figure 2), by a the angle between one of the sides of C containing S] and
the line parallel to A j passing through si (0 < a < n / 2 ).

    Study of the 1st subcase.        Let d! = d (s i, A j).     We have \pjQj\ =
sin a + cos a —d'      ,   ,     , ^ / r-    ,\     1 r-     \
                 -, and so \pjqj\ ^ 2 (\/2 —d ) ^ 2 ( \f 2 —d ) .
    sin a cos a
    Study of the 2nd subcase. We have
                                                  sin a + cos a —d
                     I'PjQjl + \Pj + i Qj + i \
                                                     sin a cos a
We conclude that in both subcases

                 JUIC'D Ai| ^ 2 ( v ^ - d ) ^ i n f ( l , 2 (>/2 - d ) ) .
                 iez
    P r o o f o f T h e o r e m 1. Suppose that one can pack 7 unit squares in a
square (abef) of side 3 —a (a > 0). Since s(5) = 2 +                we have 3 —a ^ 2+
and s o a i l - y .
   We dissect (abef) into 9 little squares of side 1 —e (where a —3e), as
shown in Figure 1.




                                       (I1              b'
                                                               bi



                                                        e      e2
                                       f



                            f              A

                                               Fig. 1

     Let V be a packing of 7 unit squares in the square (abef). Note first
that there are at least 3 unit squares whose interior does not contain any
of the 4 points a', b e', /' , otherwise (by the pigeonhole principle) there
would exist 2 unit squares whose interior contains one of the points a', b',
e', f , contradicting the fact that the interiors of the 7 squares are pairwise
disjoint.
284                                  S. EL MOUMNI


    Call C i, C2, C 3 these 3 unit squares. We will prove that the center
Oj of Ci (i = 1,2,3) belongs necessarily to the union of the open rectangles
(a i& iei/i) and (02^262/ 2)- In order to do this, we will prove that, if it is
not the case, then one of the points o',       e', f belongs necessarily to the
interior of Ci. Indeed, up to a symmetry of the square, we may assume that
01 belongs to the closed square (aaio'ß2). We have Ci C (ab\e' $2 ) (of side
                                      O
2 —2e) and, by Proposition 1, a' EC{.
    Thus we have shown that the centers o\, 02, 03 of the 3 squares C\ , C'2, C 3
belong to {a\b\b'a') U (a'b'e' f ) U {b'b^^e') U (e 'e if if ) U (ß2a ' / ' / 2). How­
ever, two of the centers 01, 02,03 cannot belong simultaneously to one of
these 5 squares of side 1 —e, otherwise there would be two centers Oi and
Oj at distance ^ 1 belonging to a square (S1S2S3S4) of side (1 —e), where
                0    0                           O

si, 52, S3, S4 t C i U C j . Since the open disc D(ol, 1/ 2) of center o; and radius
                          O             O     O
1/2 is contained in Ci and since D(oj, 1/2) C C i , we would have

                           { oi , oj } n U D{sk, 1/2) = 0,
                                         k= 1
and so ot- and Oj would belong to the shaded portion of Figure 2.




     Let r i,r 2,r 3,r4 be the midpoints of the sides of the square (S1S2S3S4).
We have o; G ( r i r 2 r 3 r 4 ) and oj E ( ^ 2 ^ 4 ). But the diameter of the square
                                                         O O
(rir2r3r4) is 1 —e. Therefore |e>iOj| < 1, and so Ci D Cj ^ cf>, a contradiction.
     Let Oi be the center of the square Ci (i = 1, . . . ,7). It follows from the
preceding arguments that any distribution of the centers of the 3 squares Ci,
C'2, C*3 is equivalent (up to a symmetry of the large square) to one of the 3
cases represented in Figure 3.
   Case 1. We first prove that | fl[ ö2&2]I = |C i n [ a ' 6 ']|. We have D(o\, 1/2)
C Ci<z{abef), thus d(oi, [ai, 6 i])^ l/2 . On the other hand, cf([ai, 61], [a', b']) =
                                                   OPTIMAL PACKINGS                                                         285



                                                                                   b    a

                                                                  X 0,
                    x *,                                                                                    x «>
           a'                 b'                         a'                 b’                       a'                b'
                                                                    X 03                                                Xo3
                                                     \                                       X ° 2



        r                     e'                         r                  e                        /'                e'
                Xo3


/                                                                                        f
                1   st case                                   2   nd case                                 3rd   case

                                                                   Fig. 3


    1 —e < 1. It follows that d(oi, [a', 6']) < 1/2. Therefore D(oi, 1/2) D [a', 6'] ^ 0,
                    o                                                       o            o
    and so C\ D [o', 6'] ^ </>. The fact that a' ^ (7i and 6' ^ C\, together with the
                 O
    convexity of C\, imply that

                                                 C ifl [a'2, 62] = Ci D [a7, 67].

    A similar argument shows that

                                              C3 H [ß2, / 2] = C 3 n [e7, /'].

    By Proposition 2,
                                            |C i ("I [a', b']\      2 \/2 —2(1 —e)
    and
                                            |C*3 n [er, / 7]| ^ 2\/2 —2(1 —e).
       o                                     o
    If C 2 ft [o', 6'] ^ <f>, then C 2 fl [o', 6'] is a segment whose endpoints belong to
    two neighbourly opposite sides of C 2 (otherwise \a'b'\ ^ 1, a contradiction).
    The same holds for C 2 fl [6', er], C 2 fl [e7, /'], C 2 fl [/', a7] and, by the convexity
       O
    of C 2 , we have

                    C2 n [a2l ^2] = C2 fl [a7, 67]                and      C 2 D [e2,   = C2 n [e7, /'].

    By Proposition 2,

                                   |C2 n [a7, 67]| + IC-2 n [e7, / 7]| ^ 2 V 2 - 2(1 - e).
286                                      S. EL MOUMNI


Therefore

                 £ ICi n [a', b']\ + \Ci n [e', /']| ^ \a'b'\ + |e'/'|,
                 i=1

from which we deduce that 3 {2\f2 —2 + 2e) ^ 2 —2e, that is 6\/2 < 8, a
contradiction. We conclude that this first case is impossible.


     Cases 2 and 3. In each of these cases, the centers oi and 02 of the
squares C\ and C2 belong to the open squares {ab\b'a') and (a2a '/ '/2) of
side 1 — e (the center Oj (i = 1, 2) cannot belong to the segments [a i,/i],
[61, ei], [a2, 62], [/*2, 02]), otherwise one of the points a', 6', e', f would be in
 O
Ci, a contradiction.
     In the same way as in the 1st case, we have


                          |C i n [ a ' , 6 ' ] |^ 2 \ / 2 - 2 ( l - e ) .


On the other hand, C\ D [a\ , o'] ^ </>, otherwise C\ would be contained in the
                                                              O
square (aibe^f) of side 2 —2e and, by Proposition 1, b' E C 1, contradicting
the assumption that the interior of C\ does not contain any of the 4 points
a', 6 ', e', /' .
     Similarly, we have


              |C*2 n ÍV, f ']\^ 2 V 2 —2(1 —e) and C 2 O [a', 02] 7^ </>•


Consider the points p, q, r, s, t, u such that


                   p,q£[aJ)'],                   [pb1] = \aq\ = 2\Í2 —2
                   r,se[a',f'],                  \rf'\ = |fl/,s| = 2\Í2 —2
                         O                               O
                     t E Ci n [cti, a'],             uE C2 0 [a2, a'].

                             o                                  o
The points p, 9, f belong to C \ . Similarly, r, s, u belong to C2. The situation
is summarized in Figure 4.
                                    OPTIMAL PACKINGS                                       287




                                /           /,

                                                  Fig. 4
                                O          O                               0               0

    By the convexity of C\ and C 2 , the triangles (pqt) C C 1 and (r s u ) C C2-
                                                                    O
Suppose that there exists a square C4 such that a! 6 C 4 . Thus we have
O                          O
C 4 D (pqt) = <t>and C 4 Pi (rsu) = <j>, and we deduce that C4 is contained in the
polygon ( a a \p b 2 e j \ r a 2 )- Consider the points p \ r' such that
                  p ' G[ai,p], r ' e [ a 2 ,r] , \p'r'\ = 1 and p ' r ' / / a i a 2.
We distinguish two cases:
     Case 1. The center 04 of C4 belongs to the pentagon (a a i p r a 2)• Now
d ( o 4 , [ai,p]) ^   d (o \ , [0 2 , r]) ^ 5 , |p'r'| = 1, |pr| = 2 \/ 2 - 4 —e < 1. We deduce
that 04 does not belong to the polygon (p ' p r r '), otherwise by drawing the line
A parallel to r 'p ' and passing through 0 1 , we would have A D \p ',p ] — p " and
A n [r ',r ] = r " , and so \p"r"\ ^ 1, contradicting the fact that |pr| < \p "r"\ <
\p'r'\ = 1. Therefore 0 4 G (a a \ p ' r ' a 2 )■
     But two vertices of C4 cannot belong to the open polygon ( r 'p 'b 2 e f i ) be­
cause in this case the other two vertices would belong to (aaip V a 2 ), therefore
the intersection of C4 and \p',r'} would be a segment whose endpoints belong
to two opposite sides of C4 , and this implies \p'r'\ > 1 , a contradiction.
     Hence there are three vertices of C4 belonging to ( a a i p 'r 'a 2), from which
we deduce that there are two vertices of C 4 at distance \ / 2 and belonging to
the pentagon (a a \ p ' r ' a 2 )■
     We are going to prove that the diameter of the pentagon ( a a \ p ' r ' a 2) is
less than %/2, which yields a contradiction. For this it suffices to prove that

                                        l-'l
                                        \ir I= \ip I < — ■

But
                              2 - V 2 - t\       ( \ / 2 ( l —e) —1
               Ii p ' V =                                                  +
                                y/2-1                      2
288                                     S. EL MOUMNI


                                   V2
and so we have Iir 1     \ip'\ <
                                    2

     Case 2. The center o\ of C 4 belongs to the pentagon (rpb'e'/'). There is
                                                               O
a vertex si of C 4 such that si ^ ( r p ' e 1f ) because a ' E C 4 . The other vertices
cannot belong to (r ' p ' p r ). We denote by S2 and S3 the vertices of C 4 adjacent
to s i. We have
                                    •S2 S 1 S 3 =   tt/ 2 .

But                                          ___
                 S2ű's3 > S2S153 = 7t/ 2 and ra'p t S20.'s% > 7t/2,
a contradiction.
    Therefore a' is not in the interior of any of the other 4 squares.              In
conclusion:
     If C \ and C2 are packed as in the 2nd case, then a! cannot belong to
the interior of any of the other 4 squares packed in (abef), therefore there is
another square C4 whose interior does not contain any of the points a', b1,
e1, f , and so we have necessarily a packing of three unit squares equivalent
to the 1st case, which is impossible.
     If we are in 3rd case, the above arguments imply that a1 and b' cannot
belong to the interior of any of the other 4 unit squares packed in (abef),
thus there are two other squares C 4 and C5 whose interior does not contain
any of the points a', 6', e!, / ' , and so we have necessarily a packing equivalent
to the 1st case, which is impossible.
     We conclude that it is impossible to pack 7 unit squares in a square of
side 3 —0! (with a > 0).
     On the other hand, one can clearly pack 7 unit squares in a square of
side 3.


                              3. Proof of Theorem 2

      We first prove the following proposition:
      P roposition 3. If n is an integer ^ 3 and if s ( n ) ^ \\/n\, then


                                       n         2\/2:n
                       s(n) ^ inf
                                      U /nJ’  2n
                                                    + iVn}
                                    \        IV™]

     PROOF. For any integer n ' t 3, we have y/n Ú s ( n ) ^ [\/n] (indeed, n ^
s(n )2 ^ \y/n}2)-
                                  OPTIMAL PACKINGS                                                289


    Let V be a packing of n unit squares Ci (i —1 ,..., «) in a square (abef)
of side s(n), and let aj, bj (j = 1 , . . . , \_\/n\) be the points such that

                                                                        s(n)
                           laal| —\a [^/n\f\ ~~ laf aj + l| —

and
                                                  s{n)
            \bbi\ = \bly/H\e\ = \bjbj+ i\ =                    (j =               [ V n \ - 1).

If s(n) < I~y/n\, Proposition 2 shows that for every Ci

                    W™\                            /     /              / \ \
                                                                                  .1        •

Moreover,
                     n ív7«!                        [\/nJ
                    E          IC'tn [aj»&j]| ^ E            \a j b j \ = [ V n \ { n ) .
                    1=1 j= 1                        j= 1
Thus
                        n.inf
                          ] ^2 ^ \ / 2 -                         ^   lV n\s{n),

and so
                n^                 or 2n f \/2 —       ^ [xAiJs(n).
                                         V       W n\J
Therefore
                                 n                                   2\/2n
                        s(n) ^ -—-pr- or s(?ij d.
                                Wn\                            2n
                                                                       + 1\/™J
                                                             IV™1
We deduce that

                                        (                                    \
                                              n              2\/2r
                          s(n) íi inf
                                            Lv^J ’ ...2 n .....+ 1 ^ 1
                                                   \Vn] + LVnJ

      P roof   of   T h e o r e m 2. Suppose that s (1 5 )^ 4 .                     Then, by Proposi-

tion 3, s(15) ^ inf I 5, —              ■ > 4, contradicting the fact that 5(15) ^ 4.
                                7 J
Therefore s(15) = 4 .
   In the same way, we can show that s(8) = 3 without using Theorem 1.
290                           S. EL MOUMNI: OPTIMAL PACKINGS


    A c k n o w l e d g e m e n t . I would like to thank Professor Jean Doyen for
his encouragements throughout the preparation of this paper.

                                        REFERENCES

[1]   E r d ő s , P . and G raham , R. L., On packing squares with equal squares, J. Combina­
               torial Theory Ser. A 19 (1975), 119-123. MR 51 #6595
[2]   G a r d n e r , M., Some packing problems that cannot be solved by sitting on the suitcase,
               Scientific American 241 (1979), No. 4, 22-26.
[3]   G ö b e l , F ., Geometrical packing and covering problems, Packing and covering in com­
                 binatorics, A. Schrijver ed., Math. Centrum Tracts 106, Mathematisch Cen­
                 trum, Amsterdam, 1979, 179-199. MR 81b:05001
[4]   R o t h , K. F. and Vaugh an , R. C., Inefficiency in packing squares with unit squares,
                 J. Combinatorial Theory Ser. A 24 (1978), 170-186. MR 58 #7407

                                    (Received January 24, 1996)

UNIVERSITÉ LIBRE DE BRUXELLES
DEPARTEMENT DE MATHÉMATIQUE
CAMPUS PLAINE C.P. 216
BD DU TRIOMPHE
B—1050 BRUXELLES
BELGIUM

smoumni@cso.ulb.ac.be
