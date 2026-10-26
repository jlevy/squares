# An ordinary square, a foreign bar and two wall-marker exclusions force a crosspoint

All decimals are exact rationals. Every owned point is strictly inside an open square of side \(a>1\). Exclusions may touch a face. No wall, center or upper side bound is required.

**Theorem.** Suppose Q strictly owns
\[
 M=(.35,-.35),\qquad A=(1,-.26),\qquad B=(1,-.4),
                                                               \tag{1}
\]
and excludes
\[
 R=(1.086,0),\qquad H=(1.086,-1),\qquad
 I=[.26,.88]\times\{-1\}.                              \tag{2}
\]
Then Q strictly owns
\[
 X=(.5,0).                                             \tag{3}
\]
The point H and the segment I need not have a common foreign owner. Let F=(.26,−1), T=(.88,−1) denote the endpoints of I.

**Proof.** Write U,V for the lower square-face coordinates and J=U+a,K=V+a for the upper coordinates in the frame being considered. Every orientation has one of the two canonical representatives below.

## 1. Nonnegative canonical angles

Take \(u=(c,s),v=(-s,c)\), with \(c\ge s\ge0\) and \(c^2+s^2=1\). The target X has its lower u band from M, upper u band from A, and lower v band from M, by
\[
 u(X)-u(M)=.15c+.35s>0,
\quad u(A)-u(X)=.5c-.26s\ge.24c>0,
\quad v(X)-v(M)=.35c-.15s\ge.20c>0.
\]
If X were absent, it would therefore be upper v:
\[
 K\le-.5s.                                           \tag{4}
\]

At R its lower u band follows from M. A lower v exit would give \(a\le.586s<1\) against (4). It is therefore upper u or upper v. Suppose it were upper v, so K≤−1.086s. T has its upper u band from A and its upper v band from M. Its lower v exclusion would give a≤c−.206s≤1; hence T would be lower u. Strict M would then give both
\[
 .88c-s<.35(c-s),\qquad -.35(c+s)<-1.086s,
\]
or
\[
 \frac sc>\frac{53}{65},\qquad \frac sc<\frac{175}{368},
\]
which are incompatible. Consequently R is upper u:
\[
 J\le1.086c.                                         \tag{5}
\]

F has its upper u band from A and its upper v band from M, since
\[
 v(M)-v(F)=.65c-.09s\ge.56c>0.
\]
A lower v exit at F would give \(a\le c-.24s\le1\) by (4). Hence
\[
 U\ge.26c-s.                                         \tag{6}
\]

T has its upper u band from A and its upper v band from M. If T were lower u, (5) would give
\[
 a\le.206c+s\le\frac{1.206}{\sqrt2}<1.
\]
The expression increases on the entire canonical angle interval, so the displayed diagonal endpoint is its maximum. Thus
\[
 V\ge-.88s-c.                                        \tag{7}
\]

If s=0, equations (4) and (7) immediately give a≤1. Suppose s>0. On the whole segment I the upper bands are strict, as they are at both endpoints. Moreover F has its lower v band strictly, and T has its lower u band strictly, because their contrary exits were excluded above. A point (x,−1) has both lower bands precisely when
\[
 x>\frac{U+s}{c},\qquad x<\frac{-V-c}{s}.
\]
The first threshold lies in [.26,.88), while the second lies in (.26,.88]. If the first were smaller than the second, some point of the actual excluded segment would be strict in Q. Therefore
\[
 \frac{U+s}{c}\ge\frac{-V-c}{s},
 \qquad sU+cV\ge-1.                                 \tag{8}
\]
This is exactly the requirement that the square's closed lowest vertex stay on or above y=−1. Equality remains allowed.

On the other hand, (4)–(5) and a>1 give
\[
 sU+cV\le.586cs-a(c+s)<.586cs-(c+s)\le-1-.214cs<-1.
                                                               \tag{9}
\]
For the last inequality, put L=c+s. The elementary identity
\[
 L-1=\frac{2cs}{1+L}\ge.8cs
\]
uses only L≤√2<3/2. This contradicts (8).

## 2. Nonpositive canonical angles: a missing lower u band

Take \(u=(c,-s),v=(s,c)\), again with \(c\ge s\ge0\) and \(c^2+s^2=1\). The target has its upper u band from A and lower v band from M:
\[
 u(A)-u(X)=.5c+.26s>0,
 \qquad v(X)-v(M)=.15s+.35c>0.
\]
If absent, it is lower u or upper v. First suppose
\[
 U\ge.5c.                                            \tag{10}
\]
Strict M implies .35(c+s)>.5c, hence s/c>3/7.

R has its two lower bands from M and A. An upper u exit at R would give a≤.586c<1 by (10). Consequently
\[
 K\le1.086s.                                         \tag{11}
\]
At H its lower u band follows from M and its upper v band follows from A. A lower v exit would give a≤c≤1 against (11). Thus
\[
 J\le1.086c+s,
 \qquad a\le.586c+s.                                \tag{12}
\]
If s/c≤1/2, the latter expression is at most
\[
 \frac{2.172}{\sqrt5}<1,
\]
because it increases throughout that interval. Therefore s/c>1/2.

T has its lower u band from M and its upper v band from A. An upper u exit, combined with (10), gives
\[
 a\le.38c+s\le\frac{1.38}{\sqrt2}<1.
\]
Hence T is lower v: V≥.88s−c. Together with (11),
\[
 a\le c+.206s\le\frac{2.206}{\sqrt5}<1.               \tag{13}
\]
The expression decreases for s/c≥1/2, so its maximum is the displayed endpoint. The exact squared comparisons are 2.172²=4.717584<5 and 2.206²=4.866436<5. This rules out (10), including every boundary possibility.

## 3. Nonpositive canonical angles: a missing upper v band

It remains to suppose
\[
 K\le.5s.                                            \tag{14}
\]
T again has its lower u and upper v bands from M and A. A lower v exit would give a≤c−.38s≤1 by (14). Hence
\[
 J\le.88c+s.                                         \tag{15}
\]
F has its upper u band from A, since u(A)−u(F)=.74(c−s)≥0, and its upper v band from B. Its lower u exclusion would give a≤.62c<1 by (15). Therefore
\[
 V\ge.26s-c.                                         \tag{16}
\]

For s=0, (14) and (16) give a≤1. Suppose s>0. On I, the lower u band is strict by its value at F, and the upper v band is strict by its value at T. The two remaining strict bands would hold when
\[
 x<\frac{J-s}{c},\qquad x>\frac{V+c}{s}.
\]
The first threshold is in (.26,.88], and the second is in [.26,.88). The whole-segment exclusion therefore implies
\[
 \frac{V+c}{s}\ge\frac{J-s}{c},
 \qquad -sJ+cV\ge-1.                                \tag{17}
\]
This is the same closed lowest-vertex condition for this frame.

Strict A gives J>c+.26s, while (14) gives V≤.5s−a. Hence
\[
 -sJ+cV<-c-.5cs-.26s^2\le-1.                        \tag{18}
\]
For the last step, c≥s implies
\[
 c+.5cs+.26s^2\ge c+.76s^2
 =1+(1-c)(.76c-.24)\ge1,
\]
since c≥1/√2>1/2. This contradicts (17).

Both missing bands are impossible for the nonpositive frame, and Section 1 handles the nonnegative frame. Strict anchors preserve strict comparison when two point projections coincide at the axial or diagonal endpoint; all weak face exits and all segment tangencies were included. Therefore X belongs strictly to Q. ∎

## 4. Exact C1089 application

In the final sector of C1089-LAST-SECTOR-REDUCTION.md, A=Q4 has the ordinary southwest pair F0,G0. Apply the theorem under the map from its local chart to the original container
\[
 (\xi,\eta)\longmapsto(2-\xi,2+\eta).
\]

| Local theorem datum | Original point or segment | Actual reason |
|---|---|---|
| Strict M,A,B | SW marker,F0,G0 | One actual Q4 |
| Excluded R | (.914,2) | Strict original marker of Q8 |
| Excluded H | (.914,1) | Globally absent original marker |
| Whole excluded I | [1.12,1.74]×{1} | One actual Q0 compulsory singleton hull |
| Strict target X | (1.5,2) | The conclusion in actual Q4 |

Thus (1.5,2) belongs strictly to A, with no center or point premise on the southeast owner. If Q8 owned G3=(1.74,2), the strict segment between its original marker (.914,2) and G3 would contain (1.5,2), contradicting this conclusion. Therefore Q8's optional label10242 is impossible and its exact original label is2050. No owner is assigned to G3 by this exclusion.
