# Four isolated exclusions rule out an inner corner and a central diagonal point

All decimals are exact rationals. Owned points are strict. Excluded points may touch any face. No wall, common-side neighbor, side upper bound or angle premise is used.

**Theorem.** No open square of side \(a>1\) can strictly own
\[
 O=(0,0),\qquad M=(.65,.65)
\]
and exclude all four points
\[
 H=(-.086,0),\quad T=(.12,0),\quad
 R=(-.086,1),\quad F=(.5,1).                         \tag{1}
\]

**Proof.** Every orientation has a nonnegative or nonpositive canonical representative with \(c\ge s\ge0\), \(c^2+s^2=1\). Write U,V for the lower face coordinates and A=U+a,B=V+a for the upper faces. Comparisons with a strict owned point remain strict when the projection increment is zero.

In the nonnegative frame \(u=(c,s),v=(-s,c)\), T's lower u and upper v bands follow from O; its upper u band follows from M. Thus
\[
 V\ge-.12s.                                           \tag{2}
\]
At H its upper u and lower v bands follow from O. Its upper v band follows from (2), because
\[
 v(H)-V\le.206s<1<a.
\]
Hence \(U\ge-.086c\).

At F its lower u band follows from O and its lower v band from M, since
\[
 v(F)-v(M)=.15s+.35c>0.
\]
An upper v exit would combine with (2) to give \(a\le c-.38s\le1\), impossible. Therefore F is upper u, and
\[
 1<a\le u(F)-u(H)=.586c+s.                           \tag{3}
\]
The right side increases on \(0\le s/c\le1/2\); at that endpoint it equals \(2.172/\sqrt5<1\), since \(2.172^2=4.717584<5\). Thus \(s/c>1/2\).

At R its lower u band now follows from O, since \(s-.086c>0\). Its lower v band follows from M, and its upper u band follows from M, with positive increments
\[
 v(R)-v(M)=.736s+.35c>0,\qquad
 u(M)-u(R)=.736c-.35s\ge.386c>0.
\]
It must be upper v. Together with (2) this gives
\[
 a\le c+.206s.
\]
This expression decreases for \(s/c\ge1/2\); its value at the endpoint is \(2.206/\sqrt5<1\), since \(2.206^2=4.866436<5\). This is a contradiction.

In the nonpositive frame \(u=(c,-s),v=(s,c)\), T has both lower bands from O and its upper v band from M. It must be upper u:
\[
 A\le.12c.
\]
The strict M requires \(.65c-.65s<.12c\), so \(s/c>53/65\); in particular the axial representative is already impossible.

At R the upper u band follows from M. Its lower v band follows from O, since \(c-.086s\ge.914c>0\). Its upper v band follows from M because
\[
 v(M)-v(R)=.736s-.35c
 >\left(.736\,\frac{53}{65}-.35\right)c>0.
\]
Thus R is lower u. The two opposed u faces yield
\[
 a\le u(T)-u(R)=.206c+s
 \le\frac{1.206}{\sqrt2}<1.
\]
The canonical expression increases up to \(s=c\), and \(1.206^2=1.454436<2\), proving the last bound.

Both canonical signs, both diagonal representatives, and the axial endpoint have been covered. All excluded-face inequalities were weak; strictness comes from owned-anchor comparisons and \(a>1\). ∎

## Actual C1089 use

Translate the local theorem by (1,1). The strict diagonal point becomes the original SW marker (1.65,1.65). In the MMMP sector, the four required exclusions are (.914,1), globally absent; (1.12,1), strict in the actual Q0 singleton; (.914,2), the actual Q8 marker; and (1.5,2), strict in the actual northwest central owner by its central crosspoint theorem. Consequently the SW central owner cannot strictly own (1,1). The full source derivation and subsequent duplicate point are recorded in C1089-MMMP-SINGLETON-ENDING.md.

