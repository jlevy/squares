# Independent audit of the weakened negative entrance

## Conclusion

In the conditional negative pinwheel geometry, the lower central-center bound may be weakened from

\[
C_x\ge 283/200
\]

to

\[
C_x\ge27/20.
\]

The entire geometric entrance proof remains valid for maximal half-angle \(0\le h\le1/8\), provided every other original point, center-displacement, boundary-angle, and container premise is retained. This is a conditional theorem: checking those other premises in a particular original state remains necessary.

The older proof uses its lower bound on \(C_x\) only to lower-bound the abscissa of the right-lower central vertex in the wall-strip argument. All other uses of central center coordinates involve \(C_x\le3/2\), \(C_y\ge3/2\), or the stated center displacements. No second use of \(C_x\ge283/200\) occurs in its face, support, or cyclic arguments.

## Exact replacement in the wall-strip proof

For a nonpositive central angle, write its actual normals as

\[
(C,-S),\quad(S,C),\qquad C=c(q),\ S=s(q),\quad0\le q\le h\le1/8.
\]

Then

\[
C\ge63/65,\qquad0\le S\le16/65<1/4,
\qquad C-S\ge47/65.
\]

The original strict anchors \((1,87/50),(87/50,2)\), together with exclusion of \((1,2)\), force the same lower first face. With \(C_x\le3/2\) and \(C_y\ge3/2\), this gives \(a\le C+S\). The right-lower vertex is

\[
Z=\left(C_x+\frac a2(C-S),\ C_y-\frac a2(C+S)\right).
\]

The weakened lower bound and \(a>1\) give

\[
Z_x>\frac{27}{20}+\frac{47}{130}
=\frac{89}{52}
>\frac{17}{10}.
\]

The existing upper estimate remains

\[
Z_x\le\frac32+\frac12(C+S)(C-S)\le2.
\]

The boundary square has normals \((b_c,b_s),(-b_s,b_c)\), with \(b_c\ge49/50\) and \(|b_s|\le19/100\). The original wall proof establishes that, whenever \(b_s>0\),

\[
Q=(2-b_s/10,1+b_s/2)
\]

is strictly inside the boundary square. This construction uses only its original anchors \((2,1),(8/5,1)\), the bottom container wall, \(B_x\le9/5\), and the boundary-angle bounds; it uses no bound on \(C_x\).

If \(Z_y\le1\), then

\[
\begin{aligned}
(-b_s,b_c)\cdot(Z-Q)
&<b_s\left(\frac3{10}-\frac{b_s}{10}-\frac{b_c}{2}\right)\\
&<0,
\end{aligned}
\]

because \(b_c/2\ge49/100>3/10\). This replaces the older coefficient \(1/5\), which came from the unnecessarily stronger estimate \(Z_x>9/5\). For a central upward separating normal, or a boundary upward normal with \(b_s\le0\), the unchanged upper bound \(Z_x\le2\) makes comparison with the strict boundary point \((2,1)\) contradictory. Thus every case still yields

\[
Z_y>1,\qquad C_y>1+\frac a2(C+S).
\]

Boundary contact causes no gap: \(Z\) is a closed central point, whereas the comparison point in the boundary square is strict. Weak separation therefore makes their projection comparison strict in the opposite direction.

## Other constants that must be widened with the interval

The angle interval change does not require any new geometric premise. The following replacements verify all former uses of the smaller sine bound:

1. For the central/boundary pair, \(|C_x-B_x|\le1/4\) and \(0\le C_y-B_y\le3/2\) give horizontal-normal projection magnitude at most
   \[
   \frac14+\frac32\frac{16}{65}=\frac{161}{260}<\frac58<1.
   \]
   The boundary normal itself has the stronger bound \(1/4+(3/2)(19/100)=107/200<1\). A downward second normal cannot separate because the upward projection is bounded below by \(-(1/4)(16/65)>-1\).

2. For neighboring central squares, \(0\le\Delta x\le11/10\) and \(-1/2\le\Delta y\le0\) give second-normal projection magnitude at most
   \[
   \frac12+\frac{11}{10}\frac{16}{65}=\frac{501}{650}<1.
   \]
   The reverse first-normal order is likewise excluded by a lower projection bound greater than \(-1\). Thus the same forward first-normal alternatives exhaust separation.

3. For the negative-parameter branch of the central upper functional bound, the required elimination coefficient stays positive:
   \[
   c(r)[c(h)-s(h)]-[c(h)+s(h)]s(r)
   \ge\frac{63\cdot47-79\cdot16}{65^2}
   =\frac{1697}{4225}>0.
   \]

The forced-face comparisons use only the same strict anchors and the sign of the central sine. The positive-parameter rational identity is valid throughout \(0\le q\le h<1\). The new negative scalar theorem in C1092-CYCLES.md already applies on \([0,1/8]\). Its transport identities, edge-gain decomposition, separate convexity reduction, anchored four-cycle variation bound, and strict common-side step were also independently checked without finding a mathematical error.

## Scope

This audit proves the weakened conditional entrance and verifies compatibility with the new scalar theorem. It does not independently derive the retained center-displacement premises for every original representative; those original-state mappings are a separate part of the main C1092 proof.
