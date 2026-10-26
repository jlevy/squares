# C981: complete retained continuous entrance and negative-sector proofs

This companion reproduces two already completed continuous proofs from the recovered mathematical package. They are retained lemmas, not newly claimed simplifications. Their exact hypotheses and the new actual-owner applications are stated in `C981-COMMON-CYCLE.md`. The first proof includes the all-orientation ordinary wall-reach lemma used there. Every displayed terminating decimal is an exact rational number; strict owned points and weak exclusions retain their original meanings.

## A. Ordinary two-wall center theorem

ORDINARY TWO-WALL CENTER THEOREM
A complete continuous proof from the original genuine wall points
11 October 2026

This is the ordinary-wall center entrance used by the recovered C981
argument. It is different from the shortened-wall C1092 center theorem:
here genuine lower wall exclusions force farther wall points, and no
tangent-center cuts are needed. All geometric and scalar arguments needed
for this local theorem are included below.

THEOREM

Let A,R,T be open squares of the same side a>1. Let R and T be contained
in [0,4]^2. Suppose A has disjoint interior from each of R,T. Suppose
the following points are strictly owned by the stated actual squares:

    A: P=(2,2.26), Q=(2.26,2), M=(2.35,2.35);
    R: N_R=(3.086,2), H_R=(3,2.4);
    T: N_T=(2,3.086), H_T=(2.4,3).

Suppose also that

    A excludes G=(2.35,1.65), B=(1.65,2.35);
    R excludes (3,1.74);
    T excludes (1.74,3).

Then A strictly contains O=(2,2).

There is no restriction on the orientations of any of the three squares,
no upper bound on a, and no center-position assumption. A need not itself
be assumed contained in the box. R and T need not be assumed disjoint
from one another for this local implication.

In fact the containment hypothesis can be weakened to just R in x<=4
and T in y<=4: the proof below uses only those two actual outer walls.

1. SQUARE COORDINATES AND SUPPORTS

For a square with unit frame (c,s), write its strict bands as

    u<cx+sy<u+a,
    v<-sx+cy<v+a.

Faces may be relabeled by quarter turns without changing the square. In
particular there is always a frame c>0,s>=0. When needed, interchange x
and y and interchange the actual neighboring squares R,T. The theorem's
point hypotheses have this symmetry. Thus for A we may assume

    0<=s<=c, c^2+s^2=1.

For a square W and vector n, let L_W(n),U_W(n) denote its minimum and
maximum projection on its closure. If n has frame components alpha,beta
relative to W, then

    L_W(n)=alpha*u_W+beta*v_W
                     +a*min(alpha,0)+a*min(beta,0),
    U_W(n)=L_W(n)+a*(|alpha|+|beta|).

For two disjoint open squares, some face normal of one of them separates
their projection intervals. There are four possible unoriented axes and
two directions on each. Touching closure supports may be equal.

We repeatedly use the elementary inequality

    |c*dx+s*dy|<=sqrt(dx^2+dy^2),

and its transverse version. Thus a displacement of length at most one
is always shorter than the side a. No numerical angle sampling is used.

2. AN ALL-ORIENTATION WALL-REACH LEMMA

Let W have side a>1 and lie in x>=0. Suppose it strictly owns (.914,2)
and (1,2.4), and excludes (1,w) and (d0,2). If

    w<2, d0>1, z>=2.4,
    0<z-w<=14/17,
    (d0-1)^2+(2-w)^2<1,
    (z-2)^2+(d0-1)^2<1,

then W strictly owns (1,z).

Proof. Reindex W with frame (l,h), l>0,h>=0, and lower bands U,V.
The actual leftmost vertex gives

    l*U-h*(V+a)>=0.                                       (W)

The missing point (1,w) already satisfies both upper bands, so either

    U>=l+w*h, or V>=-h+w*l.                               (i)

The missing point (d0,2) already satisfies the lower U and upper V bands,
so either

    U+a<=d0*l+2h, or V>=-d0*h+2l.                        (ii)

The target (1,z) has both lower bands from the strict point (1,2.4).
If the first alternative of (i) holds, the first of (ii) would give

    a<=(d0-1)l+(2-w)h<1,

which is impossible. Thus the second of (ii) holds. The upper target
bands now follow respectively from

    (z-w)h<1<a,
    (z-2)l+(d0-1)h<1<a.

If the second alternative of (i) holds, the upper V target band follows
from (z-w)l<1<a. If its upper U band failed, U+a<=l+zh; together with
(W) and V>=-h+wl this would give

    1+(z-w)lh>=a(l+h)>l+h.

But H=l+h satisfies H<=sqrt(2)<10/7 and

    H-1=2lh/(H+1)>=(14/17)lh>=(z-w)lh.

This is a contradiction, including when h=0. All target bands are strict.

Apply the lemma to R after reflection x to 4-x, with

    (w,d0,z)=(1.74,1.74,2.56).

Its second excluded point is the actual point Q in A. The checks are

    .82<14/17, .74^2+.26^2=.6152<1,
    .56^2+.74^2=.8612<1.

Hence R strictly owns (3,2.56), and convexity with H_R gives (3,2.5).
Apply the same argument to T in coordinates (X,Y)=(4-y,x), with its
second exclusion supplied by P. It strictly owns (2.56,3), and hence

    (2.5,3) belongs strictly to T.                        (T+)

3. A MISSING CENTER FORCES A HALF-ANGLE CROSSING

Assume for contradiction that O is not in A. Its upper U band follows
from M and both V bands follow from P,Q. Consequently

    u>=2(c+s), u<2c+2.26s.                                (E1)

In particular s>0. The point H_T is absent from A. Its lower U and V
bands follow from M,Q, and its upper U band follows from (E1) and

    .4c+s<=.7(c+s)<=.7sqrt(2)<1<a.

Thus

    v+a<=3c-2.4s.                                        (E2)

First suppose s>=16c/25. The genuine wall point

    Z=(3.03655,2.23)=(17/40)N_R+(23/40)H_R

lies strictly in R. It lies in A as well. Its lower U band follows from
M because .68655c-.12s>0. Its upper V band follows from P because

    V_A(P)-V_A(Z)=1.03655s+.03c>0.

Its lower V band follows from (E2) and

    |Z-H_T|^2=.63655^2+.77^2
               =399238361/400000000<1.

For its upper U band, put p=s/c. On 16/25<=p<=1, the function

    (1.03655+.23p)/sqrt(1+p^2)

is decreasing, since its derivative has the sign of .23-1.03655p<0.
At p=16/25 its squared value is

    896809/902144<1.

Therefore U_A(Z)-U_A(O)=1.03655c+.23s<1<a. Equation (E1) puts Z
strictly below u+a. This contradicts the disjointness of A and R.

We have proved s<16c/25. Set

    z=s/(1+c), C_z=(3,2+z).

Then z>=0, sz=1-c, cz=s-z, and z<.32<.4. By (T+), A excludes
H=(2.5,3). Its lower U and V bands follow from M,Q; its upper U band
follows from (E1) because

    1-(c/2+s)^2=c*(3c/4-s)>=0.

Hence

    v+a<=3c-2.5s.                                        (E3)

The half-angle identities give

    U_A(C_z)=U_A(O)+1,
    V_A(C_z)=V_A(O)-z.

Its lower U band follows from Q, since its U projection exceeds that
of Q by 1-.26c>0. Its upper U band follows from (E1) and a>1. Its
upper V band follows from P. For its lower V band use (E3) and

    V_A(H)-V_A(C_z)=c-s/2+z<=1;

the last inequality is equivalent, via s=(1+c)z, to
z*(1-c-2s)<=0, which follows from c+s>=1. Thus

    C_z lies strictly in A.                              (CROSS)

4. THE PHYSICAL RIGHT WALL TURNS FARTHER THAN A

Reindex R with frame (r,t), r>0,t>=0. No angle upper bound is assumed.
Since C_z is in A, it is absent from R. The two genuine points N_R,H_R
and 0<=z<.4 place it strictly inside both V_R bands and below R's upper
U face. Its only possible escape is therefore

    u_R>=3r+(2+z)t.

The strict marker and the actual rightmost vertex of R give

    tz<.086r,
    rtz<1-r-.086t^2.                                    (W1)

For the latter, use r(u_R+a)-t*v_R<=4 and
v_R<-3.086t+2r, followed by a>1.

These imply z<1/5. Indeed, if z>=1/5 then t/r<.43 and r>.9. The case
t=0 is already impossible in the second inequality. Dividing it by rt
gives

    z<(t/r)*(1/(1+r)-.086).

Multiply by z and use tz<.086r. It follows that

    z^2<.086*(10/19-.086)
        =179869/4750000<1/25,

a contradiction. Since s/c=2z/(1-z^2), we obtain

    12s<5c, c>=12/13.                                    (ANGLE)

The wall angle must be strictly larger than A's:

    ct>sr.                                               (TURN)

Otherwise r>=c>=12/13 and the wall half-angle z_R=t/(1+r) is at most
z. But (W1) gives

    z<z_R*[1-.086(1+r)]/r<z_R,

because r>=12/13>457/543. This is impossible.

5. ALL TRANSVERSE AND REVERSE SEPARATORS ARE EXCLUDED

The missing marker G now forces its lower V face:

    v>=1.65c-2.35s.                                      (E4)

Its lower U band follows from P and 12s<=5c; its upper U and V bands
follow from M and P. The missing marker B then forces

    u>=1.65c+2.35s:                                      (E5)

its lower V band follows from Q, its upper U band from M, and its upper
V band from (E4) and .7(c+s)<1<a.

These give the genuine strict outer point

    E=(2.35,2.65) in A.                                  (OUTER)

Its lower U band follows from M. Its upper U band follows from (E5)
and |E-B|^2=.7^2+.3^2<1. Its lower V band follows from (E2), since
V_A(H_T)-V_A(E)=.35c-.05s<1. Its upper V band follows from (E4),
since V_A(E)-V_A(G)=c<=1<a.

On A's V axis, H_R is strictly in A's projection interval. Its
projection is above that of Q by .4c-.74s>0, and above that of G
by .75c-.65s<1<a. On R's V axis, C_z is strictly in R's projection
interval. Thus both directions on both transverse axes are impossible.

The reverse U directions are impossible because Q in A and N_R in R
have equal y coordinates and N_R.x-Q.x=.826>0. All supports are strict
at these points. Only the two forward possibilities remain:

    u+a<=L_R(c,s), or U_A(r,t)<=u_R.                      (SAT)

Put d=cr+st>0, k=ct-sr>0. The exact support formulas are

    L_R(c,s)=d*u_R-k*(v_R+a),
    U_A(r,t)=d*(u+a)+k*(v+a).

6. THE CENTRAL LONGITUDINAL SEPARATOR IS IMPOSSIBLE

Suppose the first alternative in (SAT) holds. First it forces t<r.
Indeed if t>=r, the two genuine wall points imply

    L_R(c,s)<3.086c+2s-k*(.4r+.086t)<=3c+2s,

where the last inequality follows from

    k*(.4r+.086t)-.086c
      =r*[(t-r)*(.4c-.086s)+r*(.314c-.486s)]>=0.

Every factor is nonnegative using (ANGLE). But (E1) implies
u+a>2c+2s+1>=3c+2s, a contradiction.

With t<r, containment and the marker give the full support bound

    r*L_R(c,s)<=r*(4c+2s)+.914st-a*r*(d+k).

To verify it directly, expand its left side as

    d*[r*(u_R+a)-t*v_R]+s*v_R-a*r*(d+k),

then use the actual right wall and v_R<-3.086t+2r. The separator and
(E1) would therefore imply

    a*r*(1+d+k)<=2cr+.914st.

Lemma P below gives r*(1+d+k)>=2cr+.914st. Since a>1 and r>0 this
is impossible.

7. THE WALL LONGITUDINAL SEPARATOR IS IMPOSSIBLE

Suppose the second alternative in (SAT) holds. Equations (E1),(E4)
and the support formula imply

    U_A(r,t)>=r*X+t*Y+a*(d+k),
    X=2+.35s^2+.35cs,
    Y=1.65+.35s^2-.35cs.

The marker and right wall give

    r*u_R+a*r+3.086t^2-2rt<=4.                            (W2)

The strict actual point E in (OUTER), the separator, and the marker
give .65t<.736r. Thus, putting

    p=s/c, q=t/r, w=1/r=sqrt(1+q^2),

we have p<=q<23/20. Combining the separator and (W2) yields

    r^2*[M+(a-1)*J]<=0,
    J=w+(c-s)+q*(c+s)>0,
    M=w+(c-s)+q*(c+s)+X-4+q*(Y-2)-.914q^2.

Lemma L below gives M>=0. The term (a-1)*J is strictly positive,
so this is impossible. Both remaining separators have been eliminated.
The contradiction proves that the original center O belongs strictly
to A. The initial coordinate interchange covers the other orientation
sector. This completes the theorem.

8. SCALAR LEMMA P: ORDERED POSITIVE NORMALS

Let (c,s),(r,t) be unit normals with 0<=s<=c, 0<=t<=r,
12s<=5c and ct>=sr. Then

    1+(c-s)r+(c+s)t-2c-.914s*(t/r)>=0.                   (P)

Set P0=2-r-t, Q0=r-t+.914(t/r). Then 0<=P0<=Q0. For the nontrivial
comparison, multiplication by r*(1+r) gives

    r*(1+r)*(Q0-P0)=t*[.914(1+r)-2rt]>=0.

The bracket is positive: 2rt<=1 and r>=1/sqrt(2) makes
.914(1+r)>1. For fixed P0,Q0, the function
P0*cos(theta)+Q0*sin(theta) is nondecreasing on [0,pi/4], because
its derivative is Q0*cos(theta)-P0*sin(theta)>=0.

The central angle is at most both the wall angle and atan(5/12).
If 12t<=5r, compare to the wall normal. At that endpoint

    r*[1-P0*r-Q0*t]=(1-r)*[2r-.914(1+r)]>=0,

since r>=12/13. If 12t>=5r, compare to (12/13,5/13). The remaining
inequality is

    7r+17t-11-4.57(t/r)>=0.

Put q=t/r, so 5/12<=q<=1. Both sides of

    7+17q >= (11+4.57q)*sqrt(1+q^2)

are nonnegative. Squaring reduces the claim to F(q)>=0, where

    F(q)=-72+(6873/50)q+(1471151/10000)q^2
                -(5027/50)q^3-(208849/10000)q^4.

The following exact identity proves it on the entire interval:

    24010000*F(q)
      =604136975*(1-q)^4
       +26807920080*(q-5/12)*(1-q)^3
       +76776711696*(q-5/12)^2*(1-q)^2
       +69975280512*(q-5/12)^3*(1-q)
       +18900905472*(q-5/12)^4.

Every term is nonnegative. Finally (P) is exactly 1-P0*c-Q0*s>=0.

9. SCALAR LEMMA L: THE WALL'S OWN NORMAL

Let c>=12/13, s>=0, c^2+s^2=1, p=s/c, p<=q<=23/20,
and w=sqrt(1+q^2). With X,Y as in Section 7,

    w+(c-s)+q*(c+s)+X-4+q*(Y-2)-.914q^2>=0.             (L)

The hypotheses imply 0<=s<=2/5, p<=5/12, and

    c>=1-(13/25)s^2,

because 1-c=s^2/(1+c)<=13s^2/25.

If p<=q<=1/2, use the unit-normal inequality w>=c+s*q. It leaves

    K+Lq-.914q^2,
    K=-2+.35s^2+.35cs+2c-s,
    L=-.35+.35s^2-.35cs+c+2s.

Its value at p is nonnegative by the exact identity

    (1+c)*[K+Lp-.914p^2]=p^2*(1.086c-.914)>=0.

Its increase from p to q equals

    (q-p)*[L-.914(q+p)].

The bracket is positive. Indeed p<=13s/12, q<=1/2, cs<=s give

    L-.914(q+p)
      >=12/13-807/1000+(3959/6000)s+(7/20)s^2>0.

If 1/2<=q<=23/20, use the other unit-normal inequality
w>=4/5+(3/5)q. It leaves the concave quadratic

    G(q)=K1+L1*q-.914q^2,
    K1=-6/5+.35s^2+.35cs+c-s,
    L1=1/4+.35s^2-.35cs+c+s.

Its endpoint bounds follow from c>=1-13s^2/25 and 0<=s<=2/5:

    G(1/2)>=393/2000-(22/65)s-(51/200)s^2.

This lower quadratic is decreasing. Its value at s=2/5 is
2641/130000>1/50. At the other endpoint,

    G(23/20)>=5747/200000+(39/400)s-(731/2000)s^2.

This lower quadratic is concave and its endpoint minimum is at least
1851/200000>9/1000. Therefore both endpoint values of G are positive,
and concavity gives G(q)>=9/1000 throughout. This proves (L).

10. BOUNDARIES AND THE ROLE OF THIS LEMMA

Every point asserted to be owned is strict. An excluded point may lie on
a square's face, and every non-strict face or separation inequality above
allows equality. The side condition a>1 turns all unit-length limiting
displacements into strict band inclusions. The angle s=0 is explicitly
eliminated by (E1) under the assumed center escape. The wall angle t=0
is explicitly eliminated by (W1); steep wall angles are retained until
the appropriate full-support inequality eliminates them.

This result supplies the original ordinary-wall center entrance. To use
it for a specific C981 row, the row must provide the listed actual elbow
points, the two absent other central markers, and the two original low
wall exclusions after a rigid square symmetry. Those ownership facts are
the separate finite entrance; the theorem proves their continuous
geometric consequence without additional angle or center assumptions.

The proof was recovered and simplified from the original central-wall
argument as ordinary mathematics. Its wall-reach lemma, the direct
half-angle bounds, and the two displayed continuous scalar arguments
are all written out here. No formal-system work is required to read it.


## B. Complete negative/negative two-square exclusion

C981: COMPLETE NEGATIVE-C / NEGATIVE-B SECTOR
A standalone continuous proof from actual original points
11 October 2026

This proof fills out the recovered negative/negative ending in ordinary
plaintext mathematics. Every directed separating axis and every relative
angle order is included. Its local hypotheses are weaker than the full
original-row hypotheses: the outer square A and the container walls do
not enter once the listed original points and exclusions are supplied.

All terminating decimals denote exact rationals.

THEOREM

Let C and B be disjoint open squares of a common side a>1, with canonical
frames

    C: (d,-S), 0<=S<=d, d^2+S^2=1;
    B: (b,-t), 0<=t<=b, b^2+t^2=1.

Suppose C strictly contains

    O=(2,2), D=(2,1.5), M_C=(1.65,1.65),

and excludes G=(2.35,1.65). Suppose B strictly contains

    M_B=(1.65,2.35), H=(1,2.4),

and excludes the three genuine foreign points

    P=(1.6,3), K=(1,3), W=(.914,2).

These hypotheses are inconsistent.

In the original C981 rows, P is in the actual top wall square, K is in
the actual paired northwest corner square, and W is the original left
wall marker. C's center and bottom crosspoint are supplied by the complete
center and crosspoint arguments. Thus none of these absences is a guessed
clearance or an auxiliary assignment added to an original row.

1. BANDS, THE SOUTHEAST CAP, AND THE THREE REMAINING AXES

Write C's bands as

    u_C<d*x-S*y<u_C+a,
    v_C<S*x+d*y<v_C+a,

and similarly B's bands as u_B<b*x-t*y<u_B+a and
v_B<t*x+b*y<v_B+a. A unit canonical pair satisfies

    7/10<d,b<=1, 0<=S,t<=5/7,
    1<=d+S<=10/7, 1<=b+t<=10/7.

At G, C's lower U and upper V bands follow from O. Its lower V band
follows from D. Therefore its genuine exclusion forces

    u_C+a<=2.35d-1.65S.                                  (CAP)

For a direction n, write L_Q(n),U_Q(n) for the closure support interval
of a square Q. If n has frame components alpha,beta, these are obtained
by taking the corresponding lower or upper band endpoint according to
the sign of each component. Two disjoint squares must separate along a
face normal of one of them.

Neither direction on C's U axis is possible. C-before-B is excluded by
O and M_B, whose U projections differ by .35(d+S)>0. For B-before-C,
(CAP) gives

    u_C<=2.35d-1.65S-a<1.65d-2.35S,

because the two point projections differ by .7(d+S)<=1<a. Since M_B is strictly in B,
its projection lies strictly below U_B(d,-S), excluding that direction.

On B's U axis, C-before-B is impossible since O in C has projection
greater than that of H in B by b+.4t>0. The reverse direction remains.

On either positive transverse normal (S,d) or (t,b), B-before-C is
impossible by M_C,M_B: their x coordinates are equal and their positive
y projections differ strictly. Consequently the exhaustive remaining
alternatives are

    u_B+a<=L_C(b,-t),                                    (LONG)
    v_C+a<=L_B(S,d),                                     (CV)
    U_C(t,b)<=v_B.                                       (BV)

Closure supports may be equal in all three alternatives.

2. BOTH TRANSVERSE ALTERNATIVES FORCE THE ABSENT TOP POINT

The target P=(1.6,3) already satisfies three strict B bands. Its lower U
band follows from H because the increment is .6(b-t)>=0. Its upper U
band follows from M_B because the increment is -.05b-.65t<=0. Its
lower V band follows from M_B because the increment is .65b-.05t>0.
Its absence therefore forces

    v_B+a<=3b+1.6t.                                     (TOP)

Alternative (BV) is now immediately impossible: C's strict center gives

    2(b+t)<U_C(t,b)<=v_B<=3b+1.6t-a,

so 1<a<b-.4t<=1.

For (CV), put

    h=bS-td, alpha=bd+tS>0.

These are the U and V frame components of (S,d) in B. C's strict center
gives v_C+a>2(d+S).

If h>=0, then L_B(S,d)=h*u_B+alpha*v_B. The actual H and (TOP),
together with a>1, give

    L_B(S,d)<h*(b-2.4t)+alpha*(3b+1.6t-1).

Subtracting 2(d+S) from this upper bound yields d*f+S*g, where

    f=1-b-.6t^2+.6bt,
    g=-1-t+.6t^2+.6bt.

Here g<=-1-.4t+.6t^2<0, since b<=1 and t<=1. The exact cancellation

    b*f+t*g=b-1-.4t<=0

gives

    b*(d*f+S*g)=d*(b*f+t*g)+h*g<=0.

Thus L_B(S,d)<2(d+S), contradicting (CV).

If h<=0, then L_B(S,d)=h*(u_B+a)+alpha*v_B. The actual M_B and
(TOP) give

    L_B(S,d)<h*(1.65b-2.35t)+alpha*(3b+1.6t-1).

Subtracting 2(d+S) now yields d*f2+S*g2, where

    f2=1-b-.65t^2-.05bt,
    g2=-.35-.05t^2+.65bt-t.

The elementary identity 1-b=t^2/(1+b)<=.6t^2, using b>7/10,
implies f2<=0. Also g2<=-.35-.35t<0. This again gives
L_B(S,d)<2(d+S), contradicting (CV).

The two relative-angle branches cover h=0 as well. Both transverse
alternatives are impossible, so only (LONG) remains.

3. A SHALLOW NEGATIVE B CANNOT USE ITS LONGITUDINAL AXIS

First suppose h=bS-td>=0. The B-U direction has C-frame components

    alpha=bd+tS>0, h=bS-td>=0.

Therefore L_C(b,-t)=alpha*u_C+h*v_C. The actual C point D and (CAP)
give

    L_C(b,-t)
      <=alpha*(2.35d-1.65S-1)+h*(2S+1.5d).

Subtract the projection 1.65b-2.35t of M_B. The difference is
b*F+t*G, where

    F=.7-d-.35S^2-.15dS,
    G=.85-S-.15S^2+.35dS.

We have G>=.85-S+.2S^2>0, since d>=S and S<=5/7. The exact identity

    d*F+S*G=.7(d+S)-1<=0

then gives

    d*(b*F+t*G)=b*(d*F+S*G)-h*G<=0.

It follows that L_C(b,-t)<=1.65b-2.35t<u_B+a, contradicting (LONG).
This includes the equal-angle case h=0.

4. THE OTHER LONGITUDINAL ORDER FORCES TWO CORNER FACES

It remains that k=td-bS>0. Put alpha=bd+tS>0, and define the actual
upper-face excesses of C by

    u=u_C+a-2(d-S),
    v=v_C+a-2(d+S).

Strict center membership and (CAP) give

    v>0, u<=.35(d+S).                                   (EX)

The exact longitudinal support is

    L_C(b,-t)=alpha*u_C-k*(v_C+a)
             =2(b-t)+alpha*u-alpha*a-k*v.

Using M_B in (LONG) and a>1 gives the strict scalar cut

    0<.35(b+t)-alpha*(1-u)-k*v.                           (CUT)

This forces b<4t. Otherwise k>0 and b>=4t would imply 4S<d and hence
S<1/4, d>=24/25. Then u<=.35*(1+1/4)=7/16 and alpha>=24b/25.
The right side of (CUT) would be at most

    .35*(5b/4)-(24b/25)*(9/16)
       =(7/16-27/50)*b<0,

a contradiction.

At the missing left wall marker W=(.914,2), the two U bands and upper V
band of B are strict. Relative to H, its U increase is
.4t-.086b>0 because b<4t. Its U projection is smaller than that of
M_B by .736b-.35t>0; its V projection is smaller than that of M_B by
.736t+.35b>0. Consequently its absence forces

    v_B>=2b+.914t.                                      (CORNER-V)

The slope b<4t and b>7/10 imply t>7/40>.172. Since
b<=1-t^2/2, this gives

    b+.086t<1.

At the missing corner K=(1,3), its upper U and lower V bands follow
from H. Its upper V band follows from (CORNER-V), because

    V_B(K)-(2b+.914t)=b+.086t<1<a.

Its only possible escape is therefore

    u_B>=b-3t.                                         (CORNER-U)

Both faces were selected by actual foreign points; no new clearance
assumption or smaller replacement square was used.

5. A UNIFORM RATIONAL CONTRADICTION

Substitute (CORNER-U) and the exact support into (LONG). It gives

    a*(1+alpha)<=b+t+alpha*u-k*v.

Since a>1, alpha>0, k>0 and (EX) holds, this implies

    1<b+t-(bd+tS)*(1-.35(d+S)).                           (NEC)

The right side is uniformly at most 27/28. Indeed put

    H0=d+S, q=1-.35H0.

Then 1<=H0<=10/7, q>=0, and

    H0*q-.65=(H0-1)*(.65-.35H0)>=0.

Furthermore

    2(bd+tS)-(b+t)H0=(b-t)(d-S)>=0.

Consequently

    b+t-(bd+tS)*q
      <=(b+t)*(1-H0*q/2)
      <=(10/7)*(1-.65/2)=27/28<1.

This contradicts (NEC) and completes the theorem.

6. BOUNDARY AND SCOPE CHECK

The argument treats S=0, t=0, the diagonal canonical frames, equality
of relative angles, and contact along any separator. All exclusions are
non-strict face exclusions. Strict ownership and a>1 supply the strict
contradictions. In particular, no subdivision into finitely many sampled
orientations occurs.

For original C981 rows 34 and 41, the exact common point ancestry is
given in contributions/central_geometry/
C981/02_C981_original_points_and_crosspoints.txt. Its complete center input
is proved in walls/07_ordinary_two_wall_center_theorem.txt. The present theorem
therefore excludes their entire closed sector with both canonical sines
nonpositive. It establishes this one sector, not the two positive-C
sectors or the remaining negative-C/positive-B sector by itself.

Recovered mathematical source ancestry, without source syntax:
the negative central-face cap; the genuine top-endpoint transverse
argument; and the negative/negative full-square support ending. The
proof above makes each dependency explicit and shortens several scalar
steps using one cancellation and the rational uniform margin 27/28.
