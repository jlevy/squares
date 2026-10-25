# An inward neighbour also excludes the southwest inner corner

All decimals are exact rationals. Membership in the open square of side \(a>1\) is strict; every exclusion may touch a face. There is no wall or orientation hypothesis.

**Theorem.** Let
\[
 .50\le k\le.54,\qquad1.01\le q\le1.04.
\]
No square of side \(a>1\) can strictly own \(O=(0,0)\) and \(M=(.65,.65)\), while excluding
\[
 H=(-.086,0),\quad T=(.12,0),\quad R=(-.086,1),
 \quad D=(.74,1),\quad K=(k,q).                         \tag{1}
\]

**Proof.** In the positive canonical frame \(u=(c,s),v=(-s,c)\), \(c\ge s\ge0\), \(c^2+s^2=1\), the same comparisons as in INNER-CORNER-FOUR-EXCLUSIONS.md give
\[
 V\ge-.12s,\qquad U\ge-.086c.                         \tag{2}
\]
They use only strict O,M and the excluded T,H: T is lower v, and H has its upper v band because the opposite width is at most .206s<1.

D has its lower u band from O and lower v band from M:
\[
 v(D)-v(M)=.35c-.09s\ge.26c>0.
\]
An upper v exit would imply \(a\le c-.62s\le1\) by (2). Hence D is upper u, and
\[
 1<a\le.826c+s.
\]
For \(s/c\le1/6\), the increasing expression is at most \(5.956/\sqrt{37}<1\). Thus \(s/c>1/6\).

At R its lower u band follows from O, since \(s-.086c>0\). Its upper u and lower v bands follow from M, with increments \(.736c-.35s\ge.386c>0\) and \(.736s+.35c>0\). Therefore R is upper v, and
\[
 a\le c+.206s.
\]
For \(s/c\ge4/9\) this expression decreases and is at most \(9.824/\sqrt{97}<1\), since \(9.824^2=96.510976<97\). Consequently
\[
 \frac16<\frac sc<\frac49.                            \tag{3}
\]

The point K has its lower u band from O and its lower v band from M, because \(k,q>0\) and
\[
 v(K)-v(M)=(.65-k)s+(q-.65)c>0.
\]
An upper v exit, using (2), would give
\[
 a\le qc+(.12-k)s\le1.04c-.38s
 <5.86/\sqrt{37}<1.
\]
Here the last expression decreases with angle and (3) applies. Thus K is upper u. Together with the lower u face in (2),
\[
 a\le(k+.086)c+qs\le.626c+1.04s
 <9.794/\sqrt{97}<1.
\]
The middle expression increases throughout \(s/c\le4/9\), and \(9.794^2=95.922436<97\). This is impossible.

For the nonpositive canonical frame \(u=(c,-s),v=(s,c)\), the negative-sign part of INNER-CORNER-FOUR-EXCLUSIONS.md uses only O,M,T,R, all present here. Explicitly, T is upper u, so strict M forces \(s/c>53/65\). Then R has both v bands and its upper u band from O,M, and is lower u. Their opposite u width is at most \(.206c+s\le1.206/\sqrt2<1\), a contradiction.

Both signs and both canonical endpoints are covered. Bounds on k,q may be equalities: all final point comparisons remain strict because they compare with strict anchors or with \(1<a\). ∎

## Two exact intended points

After translating by (1,1), the parameter rectangle includes both (1.54,2.01) and (1.50,2.04). These are the two strict inward-neighbour points used in C1089-LAST-SECTOR-REDUCTION.md. The excluded D becomes G3=(1.74,2); H is the globally absent (.914,1), T is the actual Q0 point (1.12,1), and R is the actual left-wall marker.

