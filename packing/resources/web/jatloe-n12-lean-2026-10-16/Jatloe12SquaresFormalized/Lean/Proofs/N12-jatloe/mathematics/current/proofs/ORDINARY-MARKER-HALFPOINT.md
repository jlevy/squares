# An ordinary central pair needs only the foreign wall marker to reach its halfpoint

All decimals are exact rationals. Every owned point is strict; every excluded point may lie on a face. No wall, center bound, or upper side bound is required for the point theorem.

## 1. The local theorem

**Theorem 1.** Let (0\le d\le.26). An open square C of side (a>1) strictly owning

\[
 M=(.35,-.35),\qquad A=(1,-.26),\qquad B=(1,-.4),
\]

and excluding

\[
 D=(.26,0),\quad R=(1+d,0),\quad K=(1,-1),\quad F=(.26,-1)
\]

strictly owns (Y=(1,-.5)).

**Proof.** Write U,V for lower face coordinates. Every orientation has one of the canonical frames below, with (c\ge s\ge0) and (c^2+s^2=1).

First take (u=(c,s),v=(-s,c)). At K the lower-u band follows from M and both upper bands follow from B; their increments are (.65(c-s)\ge0,.6s\ge0,.6c>0). Hence K is lower v:

\[
 V\ge-s-c.                                           \tag{1}
\]

At R both lower bands are strict by M and B. In particular

\[
 v(R)-v(B)=.4c-ds\ge(.4-d)c>0.
\]

If R were upper v, (1) would imply (a\le c-ds\le1), impossible. Thus (U+a\le(1+d)c). At D, the upper-u and lower-v bands follow from A and M. A lower-u exit would give (a\le(.74+d)c\le1), again impossible. Therefore

\[
 V+a\le-.26s.                                       \tag{2}
\]

At Y the lower-u band follows from M and both upper bands follow from B. Its lower-v band follows strictly from (2), because

\[
 v(D)-v(Y)=.74s+.5c\le\sqrt{.7976}<1<a.
\]

Thus Y is strict throughout the nonnegative sign, including (s=0) and (c=s).

Now take (u=(c,-s),v=(s,c)). The lower-u band of Y follows from M and its upper-v band from B. If Y were not strict, it would therefore be lower v or upper u.

Suppose first (V\ge v(Y)=s-.5c). At D its upper-u and lower-v bands follow from M, since (u(M)-u(D)=.09c+.35s>0) and (v(D)-v(M)=.35c-.09s>0). An upper-v exit would give (a\le v(D)-v(Y)=.5c-.74s<1). Consequently D is lower u, (U\ge.26c).

Both lower bands of R follow from M and B. If R were upper v, its gap from the hypothesized lower-v face at Y would give

\[
 a\le v(R)-v(Y)=ds+.5c\le\sqrt{.3176}<1.
\]

Hence R is upper u. Together with D lower u this gives (a\le(.74+d)c\le1), impossible. Thus Y cannot be lower v.

It remains to suppose (U+a\le u(Y)=c+.5s). At D its upper-u and lower-v bands again follow from M. A lower-u exit would give

\[
 a\le u(Y)-u(D)=.74c+.5s\le\sqrt{.7976}<1.
\]

Therefore D is upper v, (V+a\le.26s). At K its lower-u and upper-v bands follow from M, because the increments are (.65(c+s)>0) and (.65(c-s)\ge0). It cannot be lower v: the cap at D would give

\[
 a\le v(D)-v(K)=c-.74s\le1.
\]

Thus K is upper u, (U+a\le c+s).

At F its upper-v band follows from M, and its lower-v band follows from D's cap because (v(D)-v(F)=c\le1<a). If F were lower u, K's cap would give (a\le u(K)-u(F)=.74c<1). Hence F is upper u, (U+a\le.26c+s). But strict ownership of B would then require

\[
 c+.4s<.26c+s,\qquad .74c<.6s\le.6c,
\]

which is impossible. Thus Y's upper-u band is strict as well.

The two signs cover every canonical orientation and every diagonal representative. All face exits were weak; strictness of the completed bands follows from the owned anchors or (a>1). This proves the theorem. ∎

The value (d=.086) is the actual original wall marker. Taking (d=0) also recovers the earlier ordinary-halfpoint conclusion with a foreign wall origin. No origin needs to be proved before using the present theorem.

## 2. Exact C1089 reverse-cyclic application

Consider the remaining C1089 wall sector (Y_8\le2,Y_{10}\ge2,X_{11}\le2). Once its original covering alternatives and the shared mixed-span/outward-corner deductions have given

\[
 Q4:\ F4,G3;\qquad Q7:\ F1,G1;\qquad Q11:\ G4,
                                                                  \tag{3}
\]

Theorem 1 applies to the actual northwest Q7 under the simultaneous map from its local coordinates

\[
 (\xi,\eta)\longmapsto(2-\xi,2-\eta),\qquad d=.086.
\]

Its strict M,A,B become the NW marker,F1,G1. Its four excluded D,R,K,F become, respectively, G3 in Q4, the left-wall marker ((.914,2)) in Q8, the paired NW-corner point ((1,3)) in Q3, and G4 in Q11. Therefore

\[
 (1,2.5)\in Q7\quad\hbox{strictly}.                  \tag{4}
\]

In particular, it is excluded from the different actual corner Q3. Theorem 7 of `C1092-DIRECT-WALL-POINT.md`, in the reflected chart ((x,4-y)), now applies with its actual K=Q3 and B=Q11, (b=.914,\ell=1.74). The corner's strict points are the original ((1,3.086),(1,3)); its required exclusion is (4). The boundary owns its original marker ((2,3.086)) and G4=(1.74,3). Its genuine top wall becomes the required bottom wall. Consequently

\[
 (2,3)\in Q11\quad\hbox{strictly}.                  \tag{5}
\]

This transfer uses no left-wall origin and no corner data from the singleton Q0. Its only conditional entrance is the explicit actual ownership (3), to be established in the whole-sector reduction.
