# C1092 MMMP: the right far auxiliary is always owned

All decimals are exact. The squares are the actual original owners, with common side 1<a<=1.001, strict ownership, and pairwise disjoint interiors.

**Corollary 1.** Every original MMMP alternative has G9=(3,2.4) strictly in Q10. Thus the entire segment {3}×[2,2.4] is strict in that same actual square.

The original Q10 G-covering row requires at least one member of {G6,G8,G9}. The all-angle theorem `C1092-MMMP-RIGHT-INNER-EXCLUSION.md` excludes G6 from Q10. If G9 is not already owned, the row therefore forces G8. The audited theorem `C1092-MMMP-RIGHT-DOUBLE-SPAN.md` then forces G9 into Q10 as well. This proves strict G9 in all cases. The earlier `C1092-MMMP-RIGHT-ORIGIN.md` puts (3,2) in Q10; convexity gives the whole stated segment. No auxiliary point has been presumed owned merely because another square excludes it.

## A sharper full positive face table for the northeast square

Use the common chart (X,Y)=(2-y,x-2). By `C1092-MMMP-NORTHEAST-ANGLE.md`, the actual B=Q6 has positive canonical frame

    u=(b,t), v=(-t,b), b>=t>0, b^2+t^2=1.

Its strict anchors are M=(-.35,.35), H1=(-1,.26), H2=(-1,.4). Write p,q for its lower faces. The following are genuine exclusions from this same B:

| Local point | Original point | Actual source |
|---|---|---|
| I=(-.4,0) | (2,2.4) | Strict half-unit segment in Q7 |
| J=(-.4,1) | G9=(3,2.4) | Corollary 1 |
| W=(-1.086,0) | (2,3.086) | Original top marker in Q11 |
| K=(-1,1) | (3,3) | Original paired northeast corner Q2 |

**Corollary 2.** These actual exclusions force

    p>=-1.086b, p+a<=t-.4b,
    q>=.4t, q+a<=b+t.                                (1)

Consequently

    a<=.686b+t,
    t/(1+b)>157/843.                                 (2)

At I, the lower u-band follows from H2, while both upper bands follow from M:

    u(I)-u(H2)=.6b-.4t>=.2b>0,
    u(M)-u(I)=.05b+.35t>0,
    v(M)-v(I)=.35b-.05t>=.30b>0.

Thus I is lower v. At J both lower bands follow from H2 and M respectively. Its upper-v alternative would give a<=b by the lower face from I. Therefore J is upper u. At K both lower bands follow from H2. An upper-u K would contradict strict M, because u(M)-u(K)=.65(b-t)>=0. Thus K is upper v.

Finally W has strict upper u-band from M. If it were upper v, the I lower face would give a<=(1.086-.4)t<1. If it were lower v, K's upper face would give a<=b-.086t<=1. Therefore W must be lower u. This proves every face in (1), including all weak exterior equalities.

The two u faces give a<=.686b+t. Set h=t/(1+b), so 0<h<1. The exact half-angle identity is

    (1+h^2)(.686b+t-1)=(1-h)(843h-157)/500.

Since a>1, it implies h>157/843 and proves (2). Neither a top-origin point nor any boundary center bound was used in the face-table argument. The conclusion is an entrance for the remaining positive northeast block, not a standalone exclusion of the whole MMMP sector.
