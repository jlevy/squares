# Mathematical Review: Ryu’s Upper Bounds of Order k^{3/8} for the Deficiency c*(k)

Reviewed 2026-10-10 UTC, stage 1 and the mathematical lane of stage 4 of the result
import for [jlevy/squares#471](https://github.com/jlevy/squares/issues/471) (version
1.0) and [jlevy/squares#486](https://github.com/jlevy/squares/issues/486) (version 1.1)
of Sungjoon Ryu’s preprint “Packing $k^2-c$ unit squares: an upper bound of order
$k^{3/8}$ for the deficiency”.
The reviewer is an AI agent, `claude-fable-5-1` at its maximum reasoning setting,
prompted as the mathematical lane of the 2026-10-10 intake pass; it shares no context
with the lane that retains the sources.
No source packet existed when it was written, so the sources were read from the Zenodo
archives and the GitHub release commits named below.

**This is one AI review, not a referee’s report.** No human has refereed the preprint.
The source’s own reviews and all its programs were written by AI systems that its author
describes as “of the same family”; this reviewer is of that family too.
Nothing below says a theorem is proved by the record.
Three words are used exactly: *proved* means the complete argument was re-derived here
and no gap was found; *checked by computation here* means a finite statement was decided
by code written here from the text, or the source’s program was replayed here with the
stated result; *reported* means the source states it and nothing here has checked it.

**In one line:** every proof in both versions was re-derived here without finding a
blocking defect; the constants of Theorem 1.2 and of version 1.0’s Theorem 1.1 were
recomputed here in independent code, the five certificates of Theorem 1.6 were decided
by an independent checker at all five $k$, and the source’s twelve tier coverings of
version 1.1 were replayed here with every stated constant reproduced; the two further
coverings per version that the source reports, its direct un-normalised covering for the
tiers C1–C3, and its fifteen large end packings are not in the release and remain
reported. Ten findings are recorded, none blocking.

## 1. Sources, Pins and Custody

| Item | Version 1.0 (#471) | Version 1.1 (#486) |
| --- | --- | --- |
| Archive | [10.5281/zenodo.23256655](https://doi.org/10.5281/zenodo.23256655), published 2026-10-09 | [10.5281/zenodo.23278927](https://doi.org/10.5281/zenodo.23278927), published 2026-10-10 |
| Archive file | `squarepacker/k2-minus-c-upper-v1.0.zip`, 9,284,622 bytes, md5 `667f1a1ea308da2df5d309ec674c82c8`, sha256 `87de5c9a…0dfc26` | `squarepacker/k2-minus-c-upper-v1.1.zip`, 9,542,766 bytes, md5 `d9e681e599152a533f056eaf82d85c0c`, sha256 `2926895f…b82ab2` |
| Release commit | tag `v1.0`, `700668795e6b95f0bf2a2c6de104adaf3a3ebce0`, 2026-10-09 07:02 UTC | tag `v1.1`, `5742311db220b4bd8e825167aeae689a1bd65ce9`, 2026-10-10 09:20 UTC |
| Paper | `paper/paper.tex`, 1,883 lines, sha256 `2530f727…31deb9`; 30 pages | `paper/paper.tex`, 2,688 lines, sha256 `2c3b7349…627fba`; 43 pages |
| Concept DOI | [10.5281/zenodo.23256654](https://doi.org/10.5281/zenodo.23256654), both versions | same |

Both archives were downloaded here and their md5 digests match the Zenodo records.
Every file of the version 1.0 archive (35 files) has the git blob id of the `v1.0`
commit’s tree, and `sha256sum -c SHA256SUMS` passes; for version 1.1 the 20 files at the
top level and under `paper/`, `data/` and `code/*.py` match the `v1.1` tree, the 99
files of its `SHA256SUMS` verify, and the recorded outputs under `code/checker_outputs/`
carry the blob ids the GitHub API lists.
So the archived bytes are the committed bytes.
The five data files of Theorem 1.6 are byte-identical in both versions (same blob ids),
as are `cert3e.py`, `chk.py`, `const_stair.py`, `r38.py`, `run_z.py` and
`stair_check.py`; `stair_dump.py` differs by one word of a comment.
The paper is CC BY 4.0, the programs and data MIT. The author is Sungjoon Ryu; the
paper, its README and `.zenodo.json` say it was developed with the assistance of Claude
(Anthropic), including the proofs, the text and the programs, that all reviews so far
are by AI systems, and that no human expert has reviewed it.

Issue #486 was opened at 09:46 UTC on 2026-10-10, 27 minutes after the `v1.1` tag, so
the pin the coordinator asked for (version 1.0) and the current head of the repository
differ; this review covers both, and the register mapping below treats version 1.1 as a
later release that raises the earlier entry’s values.

## 2. The Claim and Its Place

Let $s(n)$ be the side of the smallest square containing $n$ unit squares with disjoint
interiors and, for an integer $k\ge2$, $c^*(k):=\max\{c:\ s(k^2-c)=k\}$. This is the
$d_{\max}(k)$ of
[X-049](../../../packing/campaign/explorations/X-049-families-shading-and-the-large-n-limit.md)
and the $c^*(k)$ of the
[waste register](../../../packing/frontier/asymptotic-waste-bounds.yaml), with the same
quantifier. The paper’s results, with their evidential status after this review:

| Statement | Version 1.0 | Version 1.1 | Status here |
| --- | --- | --- | --- |
| Theorem 1.3: $N(k,b)$ squares pack in side $<k$, so $c^*(k)\le k^2-N(k,b)-1<6b+4k/b-3$ for $2\le b\le k$ | stated | unchanged | proved; checked by computation here |
| Theorem 1.4: $c^*(k)\le8\lceil\sqrt{k-4}\,\rceil-1$ for $k\ge6$ | stated | unchanged | proved; checked by computation here for $k\le2000$ |
| Proposition 1.5: $k^2-N(k,b)>8\sqrt k-14$ | stated | unchanged | proved; checked by computation here |
| Theorem 1.2: $c^*(k)<20.668\,k^{2/5}+0.623$ for $k\ge1.6\cdot10^7$ | stated | unchanged | proved, with its one interval evaluation recomputed here |
| Theorem 1.1, version 1.0: $c^*(k)<43.06\,k^{3/8}+2\cdot10^{-5}$ for $k\ge4\cdot10^{26}$ | stated | kept as the row “v1.0”, superseded by tier A5 | proved modulo the covering, which was replayed here |
| Theorem 1.1, version 1.1: twelve tiers $c^*(k)<C_ik^{3/8}+a_i$ for $k\ge k_i$, down to $42.09\,k^{3/8}+0.05$ for $k\ge2.48\cdot10^{12}$ | — | stated | proved modulo the coverings, which were replayed here |
| Theorem 1.6: $c^*(10^5)\le1583$, $c^*(10^6)\le3972$, $c^*(10^7)\le10039$, $c^*(3.825\cdot10^7)\le16988$, $c^*(10^8)\le24790$ | stated | unchanged | the frame proved; the data decided here by an independent checker at all five $k$ |

**The reduction and the direction of the bound.** Lemma 2.1 (lines 260–275 of the v1.0
TeX) shows $c^*(k)=k^2-m(k)-1$ with $m(k)=\max_{1\le x<k}M(x)$, and Lemma 2.2 that a
packing of $N$ squares in a square of side $S<k$ gives $c^*(k)\le k^2-N-1$. Both were
re-derived: $s(n)<k$ holds exactly when $n\le m(k)$, because the infimum $s(n)$ lies
below $k$ only if some side $x<k$ holds $n$ squares, and conversely $M(x)$ is attained.
So an *upper* bound on $c^*(k)$ is shown by a *packing* in a square of side less than
$k$, and the “$-1$” is the strict inequality $k^2-c>m(k)$. This is the direction X-049
uses: at $x=k-\varepsilon$ a packing of $k^2-c$ squares gives $s(k^2-c)<k$, hence
$d_{\max}(k)\le c-1$. The paper’s Section 2 also notes that $m(k)$ equals the largest
number of unit squares in $[0,k]^2$ that are pairwise disjoint as closed sets, which is
the convention of the register’s three Ryu rows (there $c^*(k)=W_{\min}(k)-1$); the
dilation argument of the
[v1.1 review of the first preprint](review-2026-10-05-squarepacker-k2-minus-c.md#1-the-reduction)
is the bridge, and the two definitions agree.

**Roth and Vaughan’s obstruction.** The register records their theorem in the primary’s
form: $w(\alpha)\gg(\alpha\lVert\alpha\rVert)^{1/2}$ when $\alpha(\alpha-[\alpha])>1/6$,
with $\lVert\alpha\rVert$ the distance to the nearest integer in the bound and the
fractional part in the side condition.
For $x\to k^-$ the side condition holds and the bound tends to $0$, so it says nothing
about $c^*(k)$; a bound $W(x)\le Cx^\alpha$ valid for *all* large $x$ must have
$\alpha\ge1/2$ because of the half-integers, and such a bound translated through Lemma
2.1 can never give $c^*(k)=o(\sqrt k)$. The paper’s Section 10.3 says exactly this, and
its footnote records that the form with $x-\lfloor x\rfloor$ in the bound, quoted on
page 1 of McClenagan 2026, would contradict Theorem 1.2; the register’s 2026-08-22
resolution against the primary is the same reading.
The constructions escape the obstruction by using bands of width $b-\varepsilon$ just
below an integer, with $\varepsilon$ of order $b^{-3}$: the whole packing has side
$S=k-b+f(\theta)<k$ with $k-S<2b/(b^2-1)^2$, so it is a statement about the one-sided
limit $x\to k^-$ and not about $W$ at a generic $x$. Theorem 1.4’s order $\sqrt k$ is
the order Erdős and Graham guessed for $W(x)$ itself; Theorems 1.2 and 1.1 go below it
only just below integers.

**Against the record.** X-049 derives $d_{\max}(k)=O(k^{3/5})$ from $W(x)=O(x^{3/5})$
(Bui 2025, McClenagan 2026) and $d_{\max}(k)\le k-1$ for $k\ge12$ (Arslanov, Mustafin
and Shangitbayev); the register’s `open_problem` places $c^*(k)$ between order $\log k$
and $O(k^{3/5})$. If the preprint holds, the upper side becomes
$8\lceil\sqrt{k-4}\rceil-1$ for every $k\ge6$ (which beats $k-1$ from $k=65$ on),
$20.668\,k^{2/5}+0.623$ from $k=1.6\cdot10^7$, and $O(k^{3/8})$ with explicit constants
from $k=2.48\cdot10^{12}$ (version 1.1) or $4\cdot10^{26}$ (version 1.0). Together with
the cube-root lower bound of #414 (reported, not checked here), the exponent of $c^*(k)$
lies in $[1/3,3/8]$; both ends are reported and unrefereed, and the paper says so.
Theorem 1.4 is consistent with every best-known value in the atlas: for $k\le18$ it is
weaker than the grid region the atlas holds ($d_{\max}(13)=13$ best known against the
theorem’s $c^*(13)\le23$), and the paper’s reading of the Squares-in-Squares page,
$c^*(k)\le k-2$ for $k=16,17,18$, matches X-049’s $d_{\max}=14,15,16$. Nothing in the
preprint settles a count $n\le324$, so no case record moves.

## 3. Theorems 1.3 and 1.4 and Proposition 1.5: Proved by Hand, Checked by Computation

The L-shaped packing of Section 4 is a $(k-b)^2$ grid in $[0,k-b]^2$, a right band of
$R_1$ rows of $b$ unit squares tilted by $\theta$ in $[k-b,S]\times[0,S]$, and a top
band of $R_2$ rows in $[0,k-b]\times[k-b,S]$, with $S=k-b+f(\theta)$,
$f(\theta)=b\cos\theta+\sin\theta$. Every lemma was re-derived.

- **Lemma 3.2 (width).** $f(\theta)=\sqrt{b^2+1}\cos(\theta-\varphi)$ with
  $\tan\varphi=1/b$, so $f(2\varphi)=b$ and $f<b$ on $(2\varphi,\pi/2]$ because
  $\theta-\varphi$ then lies in $(\varphi,\pi/2-\varphi]$, inside $(0,\pi)$ where cosine
  decreases. This is the “width just below an integer”.
- **Lemma 3.3 (stacking)** is the rigid motion $(u\cdot(z-P_0),v\cdot(z-P_0))$, under
  which the rows are the rectangles $[i+j\tan\theta,i+1+j\tan\theta]\times[j,j+1]$.
- **Lemma 4.2 (the angle).** With $M=14kb^2+1$, $\theta=2\arctan(M/(bM-1))$ lies in
  $(\theta_0,\theta_0+\tau]$, $\tau=1/(7kb^4)$, and the slack $g(L)\ge1/(b^4-1)$ (an
  integer divided by $(b^2-1)D$) beats the drift $7k\tau=1/b^4$ of the length
  conditions. The derivative bounds $d'\le4$, $h'\le b$, $|f'|\le b+1$ on
  $[\theta_0,\theta_0+\tau]$ use $\cos\ge3/5-1/224\ge1/2$. The cosine and sine are
  rational, so every vertex is rational.
- **Theorem 1.3’s count (5.1).** $(L-h_0)\gamma_0=L-3-\eta_L$ with
  $\eta_L=(2L-10)/D+8/D^2$, so $R(L)=\max(0,L-3-\lfloor\eta_L\rfloor)$ and
  $k^2-N(k,b)\le6b+b(\lfloor\eta\rfloor+\lfloor\eta'\rfloor)$, with equality when
  $k-b\ge2$; then $\lfloor\eta\rfloor+\lfloor\eta'\rfloor\le2\eta-2b/D$ gives
  $k^2-N<6b+4k/b-2$ because $2-20b+16b/D<0$ for $b\ge2$.
- **Theorem 1.4.** With $b=\lceil\sqrt{k-4}\,\rceil$ and $k\ge6$: $2\le b\le k$,
  $D\ge k-3$, and $\eta\le2-(4(k-3)-8)/(k-3)^2<2$, so both floors are at most $1$ and
  (5.1) gives $k^2-N\le8b$, hence $c^*(k)\le8b-1<8\sqrt{k-4}+7$. The proof is complete
  as printed.
- **Proposition 1.5** and **Corollary 5.1** ($c^*(k)<4\sqrt6\sqrt k$ for $k\ge6$) were
  re-derived, including the AM–GM step with $x=b+1/b$ and the case $b\in\{k-1,k\}$.

**Checked by computation here.** A program written from the text (`thm13_14_check.py`,
exact rationals) built the packing of Lemma 4.2 for every $2\le b\le k\le30$ (434
packings), checked containment in $[0,S]^2$ and interior-disjointness of every pair of
squares whose bounding boxes overlap by exact separating axes, and found every packing
valid with exactly $N(k,b)$ squares; it checked (5.1) with its equality case, Theorem
1.3’s inequality, Proposition 1.5, Theorem 1.4 and Corollary 5.1 for every
$2\le b\le k\le2000$ with no failure.
Remark 5.2’s side claim that both floors equal $1$ for $b=\lceil\sqrt{k-4}\rceil$ and
$23\le k\le2000$ holds, and $k=22$ fails as the remark says.
The first $k$ at which Theorem 1.4 improves on $k-1$ is $65$. For $6\le k\le30$ the
construction’s own value $k^2-N(k,b)-1$ equals $8b-1$ at $k=13,18,19,20$ and
$23,\dots,30$ and is below it elsewhere.

## 4. Theorem 1.2: The Staircase End

**The frame (Section 6).** Lemma 6.1 was re-derived: in the strip frame the rows lie in
$\{0\le\beta'\le R\}$, $\operatorname{Reg}(y_0)\subset\{\beta'\le0\}$ because its upper
side is the line through $P_0$ with direction $u$, and the rotation $\rho$ maps
$\operatorname{Reg}(y_1)$ into $\{\beta'\ge R\}$ because
$\rho(P_{R-1}+bu+v)=(\sigma,y_1)$ and $v\cdot(P_{R-1}+bu+v-P_0)=R$. Proposition 6.3, the
waste identity $wL_b-bR-|\mathcal C_0|-|\mathcal C_1|=(R-1)\tan\theta+E(y_0)+E(y_1)$,
follows from $wL_b=A_0(y_0)+A_0(y_1)+(R-1)dw+b$ and $dw-b=\tan\theta$; the area
$A_0(y)=yw+\frac12\gamma\sigma(1+b^2)$ exceeds the area of $\operatorname{Reg}(y)$ by
the triangle $\frac12\tan\theta$, which is why $E(y)=U(y)+\frac12\tan\theta$.

**The end lemma (Lemma 7.3).** The construction (S1)–(S6) and all nine parts of the
proof were re-derived: the slab coordinate $\lambda=X+Y\tan\alpha$ is constant along the
long sides of a column (Lemma 7.1(i), $\lambda=\xi+a\sec\alpha$); $t\ge t^*$ of Lemma
7.2 is exactly $m\cos\alpha+\sin\alpha\le g_0$, since
$(1+t^2)(m\cos\alpha+\sin\alpha-g_0)=-F(t)$; every slab up to the right wall receives a
column with $0\le J_i\le m-1$ and a gap below $1-\cos\alpha$; the four separation
statements of (e) are each a line; the partition (f) into wedge, column parts and layer
part is exhaustive; and the seven terms of $B^*$ are the parallelogram $n+\tan\alpha$
plus a sliver of height $<(1-\cos\alpha)+\mu(\sec\alpha+m\tan\alpha)$ per column, the
layer rows ($<1+\frac12\tan\alpha$ each, $\le\lfloor\bar g\rfloor$ of them), the right
corner $\omega(1+\mu\omega)$ (using $j_1\ge J_{I-1}-1$ and the maximality of $j_1$), the
wedge rows and the left corner.
No step uses a small-angle expansion, as the paper says.

**Corollary 7.4.** The band facts ($t_\theta\le1.00000002/b$,
$\sigma\mu\le4.1\cdot10^{-8}$, $w\ge b-2.1/b$), the ranges of $g_0,\bar g,m,\delta$, the
tilt bound $t\le x\vartheta(x)$ with
$\vartheta(x)=(x+\sqrt{x^2+A\kappa})/(2p(x))+x^2/16$, the seven normalised terms
$T_1,\dots,T_7$ and the monotonicity of $\Phi$ on $(0,10^{-4/3}]$ were each re-derived.
The proof of Theorem 1.2 in Section 7.3 (the choice $b=\lceil b_*\rceil$, the lifts
$y_0=\frac14\lceil3b^{2/3}\rceil$ and $y_1\in[y_0,y_0+d)$ inside the window, the three
parts of $k^2-N$, $\lambda'<1$, and the closed form) is complete.

**Checked by computation here.** `phi_interval.py`, written from the formulas of the
corollary in `mpmath.iv` at 50 digits, gives
$\Phi(10^{-4/3})\in[5.0162487675,5.0162487676]$ (the paper: $[5.0162487,5.0162488]$),
the limit $\Phi(0)=\sqrt{A/\kappa}+3/2=4.32842\ldots$, $\bar t\le0.0672$ and
$\bar\tau\le0.1349$, and the constants $(20/3)(3/2)^{2/5}5.03^{3/5}\le20.66741<20.668$,
$(8/3)5.03\cdot10^{-4/3}\le0.62260<0.623$,
$(2/3)\,5.03\cdot10^{20/3}\le1.5565\cdot10^7$, the $\lambda'$ bound $5.35\cdot10^{-4}$
and the limit coefficient $18.886$; a subdivision of $[0,x_0]$ into 400 intervals gives
the same supremum without the monotonicity argument.
The source’s `const_stair.py` replayed here prints `ALL CHECKS: True` with the recorded
values.
`stair_build.py`, an exact implementation of (S1)–(S6) written from the text with
$Q$ the least power of two at least $16b$, built the end packing for $(b,y)=(400,41)$,
$(1600,103)$, $(10^4,1393/4)$ and $(10^4,1399/4)$ (the last two in the window of the
corollary), checked every piece exactly (shape, containment in $\operatorname{Reg}(y)$,
separating axes on 3,279 to 301,111 bounding-box pairs) and found
$U\le B^*\le\Phi(x)b^{2/3}$ in every case, with $U/b^{2/3}$ between $3.47$ and $3.79$
and $B^*/b^{2/3}$ between $4.51$ and $5.47$. The paper’s Remark 7.5 reports $U/b^{2/3}$
between $3.26$ and $4.36$ over its 25 runs, which agrees.

## 5. Theorem 1.1, Version 1.0: The Chained Wall Filler

**Lemma 8.1 (wall filler).** The construction ZC and every part of the proof were
re-derived, with these points worth recording:

- The invariants (I1)–(I3) pass from a block to its successor: (I3) because $F'$ is a
  maximum; (I1) because the drift $C_\beta=\sum(\kappa_\gamma+\delta_Q)$ is bounded by
  $\Delta_{\rm dr}$ through (8.1) $q\le(\zeta\Lambda_\beta+1+\zeta\tan\alpha)/N_0$ and
  the count $\beta+1\le\bar K$; (I2) because $M'\le M-1+N_0$ and
  $\hat\xi\ge s+\Lambda\ge M\tan\alpha+N_0\tan\alpha_0$ by (W1).
- $J'_0\le J_{\rm L}$ needs
  $n_{\rm L}+\sin\alpha-N_0\cos\alpha'+\zeta(1+\sec\alpha+M\tan\alpha)+(1+\zeta\tan\alpha')/q'\le1$;
  with $n_{\rm L}\le1+\zeta\sec\alpha/q$ this is implied by (W3), which carries one
  spare $\zeta$.
- The phase $\omega$ makes the aligned closings’ lengths satisfy
  $\ell_j\equiv(\omega-\omega_0)+(j-J_{\rm lo})\eta+(1-f_j)(\sec\alpha-1)\pmod1$, a sum
  of three terms in $[0,1/Q_f)$, $[0,N_0\delta_Q)$ and $(0,\sec\alpha_0-1]$, whence
  $\operatorname{frac}(\ell_j)\le\varepsilon_W$ (relation (R)); this was re-derived from
  $p(j)\sec\alpha\equiv p(j)(\sec\alpha-1)$ and $B(\sec\alpha-1)=\kappa$.
- The accounting (f) is a genuine partition of $Z$ into cells and stretch regions, and
  each of the six bounds of (f3) holds as stated.
  One sentence is missing (finding RF-1): a stretch with left end $x=0$ is placed only
  if $j+1\le\chi$, which holds for every row block $0$ does not block because
  $j+1\le J_{0,0}\le H(J_{0,0})\le\Gamma_{0,0}=\chi$; version 1.1’s Lemma 8.7 (F0)
  writes this line.

**Lemma 8.2 (end lemma for the exponent 3/8).** The main staircase with the shift
$D_\ell$, the cut at $\ell_0=\xi_{N-1}+\omega_m$, the three wall regions and their maps
were re-derived; the maps are exact rotations, so $Z_{\rm L}=Z(\xi_0-g_0\tan\alpha,
\tan\alpha,g_0)$, $Z_{\rm LR}=Z(w-\ell_0,\tau,J_{\rm L})$ and
$Z_{\rm UR}=Z(w-\xi_N+J_{\rm L}
\tan\alpha,\tan\alpha,Y_u-J_{\rm L})$ as stated, with $\chi\in[D_r+\sec\alpha-1,
D_r+2\sec\alpha]$ for $Z_{\rm LR}$ because $N$ is maximal.
The row ceiling, the containment of the walls, the disjointness lines and the partition
of (d) hold; the hypothesis (E-iv) in the form $\varepsilon_m+\tau<1$ is what forces
$\ell_j\ge0$ from $\ell_j\ge-\tau$, and it is the form the programs check.

**Corollary 8.3 and the proof of Theorem 1.1.** The ranges of (i) were re-derived,
including $t^*\ge\sqrt{\delta'/D'}$ from below and the substitution $D'\ge2m-3.000001$,
$\delta'\le3.000001$ into the formula for $t^*$ from above, and the normalisation (ii):
every term of Lemma 8.2 and of $B_W$ times $z^3=m^{-3/4}$ is a function of $z$,
$\hat b=bz^5$, $t/z^2$, $\chi z^3$, $Lz^4\le1$ and the enclosed inputs with non-negative
powers of $z$, so that $z=0$ is admissible and the covering of
$[0,z_0]\times[\text{range of }t/z^2]$ covers every integer $b\ge10^{16}$ and every lift
in the window. The two right walls’ $L$-linear parts are bounded by the larger
coefficient because $L_{\rm LR}+L_{\rm UR}=Y_u<m$, and the remaining terms by their
values at $L=m$, which is legitimate because $B_W$, (W2) and (W3) are non-decreasing in
$L$. Section 8.4’s derivation of
$c^*(k)<\frac{32}5(\frac53)^{3/8}C_E^{5/8}k^{3/8}+\frac{12}5C_E\cdot10^{-32/5}$ is the
same computation as Section 7.3 with the exponents $5/8$ and $3/5$; the closed form,
$k_1$ and $\lambda'$ were recomputed here (`phi_interval.py`): $43.05564<43.06$,
$1.485\cdot10^{-5}\le2\cdot10^{-5}$, $3.712\cdot10^{26}\le4\cdot10^{26}$, and
$C_E^{\rm cert}=96.477\cdot12^{-3/4}(1+60.000012\cdot10^{-64/5})^{3/4}\le14.9637$.

**What the computer-assisted part must establish, and whether the code does.** The proof
needs, for every box of a cover of $\{z\in[0,z_0]\}\times\{t/z^2\text{ in its
range}\}$: the hypotheses (E-i)–(E-iv) of Lemma 8.2, the hypotheses (W1)–(W5) of Lemma
8.1 for each of the three walls with $L=m$, and the enclosure of $\Psi=z^3\times$(bound
of Lemma 8.2) with $B_W$ for each wall.
`cert3e.py` was read line by line against Appendix A and against the lemmas; every
normalised quantity (the 27 margins and the pieces of $\Psi$) is the transcription the
appendix states, and each transcription was checked against the un-normalised lemma: for
example $\Lambda z^3=(q_{\min,n}N_0z^3-z-\zeta_na_nz^4)/\zeta_n$ is Lemma 8.1’s
$\Lambda$ times $z^3$, $X_1=(N_0z^3-z^3)((\varepsilon_W/z^2)z+a_n)$ is
$(N_0-1)(\varepsilon_W+\tan\alpha_0)z^2$, and $J_0z^3\le(4\tau_nz^2+2z^4)/(16\hat bq_n)$
follows from $J_0\le(4mt+2)/(Qq)$, which itself follows from $|dH(0)/dt|\le4mt+2$ and
$t-t^*\le1/Q$. The $z$-intervals are $[z_0i/N_Z,z_0(i+1)/N_Z]$ with shared endpoints,
the $t$-range of each is the lower end of the lower bound and the upper end of the upper
bound evaluated on the whole $z$-interval, every margin is taken as a lower end and
$\Psi$ as an upper end, and the inputs $\hat b$, $\mu b$, $\Delta$, $D_\ell z^3$,
$D_rz^3$, $\delta_Q$ and $1/Q_f$ are intervals that over-cover their ranges.
So the program decides what the proof needs.

**Replayed and cross-checked here.** `cert3e.py 160 64` run here under the project’s
Python 3.14.7 and mpmath 1.4.1 (18.6 s) printed `all_positive: true`,
`Psi_sup 96.47689098…` and `C_E_cert 14.96364392…`, and its output JSON is semantically
identical to the recorded `checker_outputs/cert3e_out_160_64.json` (the bytes differ in
formatting only). `e38_point.py`, an un-normalised evaluation of Lemmas 8.1 and 8.2
written from their statements and not from the appendix, at $b=10^{16}$ (three lifts),
$10^{17}$, $10^{20}$, $10^{26}$ and $10^{40}$, found every hypothesis margin positive
and the bound, assembled as the covering assembles it, equal to $86.7$, $90.3$, $91.0$,
$92.2$ and $90.7$ in units of $m^{3/4}$, each below $\Psi_{\sup}=96.477$, and between
$13.4$ and $14.3$ in units of $b^{3/5}$, below $C_E=15.54$; the covering’s worst box
sits at the top of the $t$-range, above the construction’s actual $t$, which is why the
point values are smaller.
These point checks are diagnostics of the transcription; they are not a covering.
The paper’s statement that the asymptotic regime cannot be tested by explicit
computation is right: one end at $b=10^{16}$ has about $10^{16}$ pieces.

The source’s other two coverings of version 1.0 (`mpmath.iv` with $200\times64$ boxes,
and `python-flint` arb) are not in the release; the statement “certified by three
independent full-range coverings” is reported, and the certification the release itself
carries is `cert3e.py`, replayed here.
`run_z.py 10000 1 0.5 4` (the wall filler alone at $m=10^4$, with the exact checker
`chk.py`) replayed here in 3 s with exactly the recorded result: 3 blocks, 25,289
pieces, 28,402 exact pair decisions, no overlap, 7,611 aligned closings with largest
residual $0.0056087\le\varepsilon_W=0.0056093$, $U_Z=6712\le B_W\le19615$.

## 6. Version 1.1: What Changed and Whether the Tiers Are Established

**The changes.** The diff of `paper.tex` has 1,185 changed lines.
The mathematics of Sections 2–7 and 9 is unchanged (the diff there is wording and table
numbers), and Theorems 1.2, 1.4, 1.6 and Proposition 1.5 are stated as before.
Section 8 changes in four ways:

1. **Parameters.** The construction E38 is stated with six parameters
   $(b_0,c_y,c_D,c_R,a_w,\varpi)$; version 1.0 is the row $(10^{16},1/12,4,4,3/2,0.65)$.
   No lemma is changed for this.
   Two arguments are added: the error of the wall tilts in (E6) for all $t\le1/10$
   ($d\log\tan\alpha/d\log t=(1+t^2)/(1-t^2)\le1.020203$ on $(0,1/10]$, so a relative
   error $10^{-12}$ in $t$ is a relative error at most
   $1.0203\cdot10^{-12}\le\epsilon'=1.03\cdot10^{-12}$ in $\tan\alpha$; version 1.0’s
   $t\le0.0014$ and $\epsilon'=1.00001\cdot10^{-12}$ hold for its row and not in
   general), and the room for the lifts ($y_0\le\sqrt k+1$ needs
   $c_y(5/(3C_E))^{1/2}\le1$ and $c_y\le3/4$, checked per tier).
   Both were re-derived and hold.
   The tilt condition is now $t_{\rm up}<1/10$ by the exact half-angle formula.
2. **The variant ZC′ and Lemmas 8.2–8.5** (tiers B1, B1s, B2, marked $\dagger$). (Z4′)
   starts a row at $a^*=\max(a,0,(j+1-\chi)/\zeta)$, the least abscissa at which the row
   fits under the ceiling; by Observation (O) it coincides with ZC wherever ZC places a
   piece. Lemma 8.2: containment and the three separation facts survive because the piece
   still lies in $[a,a^+]\times[j,j+1]$ and $\lambda_\beta$, $\lambda_{\beta_2}$
   increase in $X$. Lemma 8.3 bounds the transition rows of a complete block with a
   successor by
   $A_T'=(h_T+1)(1+\tan\alpha_0)+(2+\zeta(w_T+\tan\alpha_0+\zeta\tan\alpha_0))(w_T+\tan\alpha_0)$:
   at most $h_T+1$ rows (their points have $Y<J_{\rm L}+h_T$ by Lemma 8.1(f3)), left
   ends positive because $h_T-1<N_0\cos\alpha_0$ by (W3) and
   $\hat\xi>(M+N_0)\tan\alpha$, good rows waste $<1+\tan\alpha_0$, bad rows waste
   $\le w_T+\tan\alpha_0$ and lie in a half-open interval of length
   $\le1+\zeta(w_T+\tan\alpha_0+\zeta\tan\alpha_0)$, hence number at most one more.
   Each inequality of the interval computation was re-derived.
   Lemma 8.4 replaces the end term $w_e(4+2\zeta w_e)$ by $w_e$ through the partial
   layer $P_z=\{\lfloor r(X)\rfloor\le Y\le r(X)\}$, whose area over any $X$-interval is
   at most its length, and the split of each end row at $a_j$ and $a_j^*$; the parts
   (iii) of different rows and the rows above $\lfloor r(L)\rfloor$ are disjoint subsets
   of $P_z\cap\{L-w_e<X\le L\}$. Lemma 8.5 assembles $B_W''$ with a spare
   $2(1+\tan\alpha_0)$. All four hold.
3. **The sawtooth accounting, Lemmas 8.6–8.8** (tiers C1–C3, marked $\ddagger$). Lemma
   8.6: for $x_j=c\pm j\nu+d_j$ with $0<\nu<1$ and $d_j\in[0,\epsilon]$,
   $\sum_{j<n}\operatorname{frac}(x_j)\le n(1+\nu)/2+n\epsilon+1/(8\nu)$; the proof by
   runs between wraps was re-derived, the first run’s excess $(r-r^2\nu)/2$ being at
   most $1/(8\nu)$, and the constant is attained in the limit, as the paper and its
   exact adversarial test say.
   Lemma 8.7(a): the start rows $J_{0,0}\le j\le\lfloor\chi\rfloor-1$ have lengths
   $\ell_j=(s_0-\tan\alpha_0)-j\tan\alpha_0$, an arithmetic progression with step
   $\tan\alpha_0\in(0,0.21]$ by (W5), waste
   $\operatorname{frac}(\ell_j)+\frac12\tan\alpha_0$ each (including
   $\ell_j\in[-\tan\alpha_0,0)$), total
   $\le\lfloor\chi\rfloor(\frac12+\tan\alpha_0)+1/(8\tan\alpha_0)$. Lemma 8.7(b): the
   final stretches split into rows blocked by nothing (F0, waste $<1$ each, at most
   $2+N_0q_0+(1+\zeta\tan\alpha_0)/q_{\min}$ of them), rows whose last blocking block is
   $\beta$ with $j<J_{\beta,\rm L}$ (F1, lengths $\equiv c'_\beta+j\nu_\beta+d_j$ with
   $\nu_\beta=\tan\alpha_\beta-\kappa_\beta\ge\nu_*$ by (I1) and (W6), the same
   derivation as (R)), the end rows before the first failure of the placement conditions
   (F2a, step $\tan\alpha\in[\varpi\tan\alpha_0,\tan\alpha_0]$) and the tail (F2b, fewer
   than $1+\zeta L+\zeta w_e$ rows, their parts (iii) inside $P_z\cap E_{\rm end}$); the
   chunks number at most $\bar K+2$. Lemma 8.8 assembles $B_{W4}$. The new hypothesis
   (W6) $\nu_*=\varpi\tan\alpha_0-q_0^2/\zeta>0$ is what keeps $1/(8\nu_*)$ finite.
   All three hold.
4. **The lift choice, Lemma 8.11, and Corollary 8.12** (tiers $\ddagger$). For a band
   $(L_b,h,d)$ and $\alpha_0\ge0$ with $L_b-h-1\ge2\alpha_0$, the lift $y_0=Y_{R^*}$
   with $Y_R=(S_R-\epsilon_R)/2$, $\epsilon_R$ the parity correction of
   $\lfloor S_R+2c_0\rfloor$, gives $R$ rows, $y_1-y_0=\epsilon_R\in\{0,1\}$, and
   $\operatorname{frac}(\bar g(y_0))=\operatorname{frac}(\bar g(y_1))\ge\frac12$ because
   $\bar g(Y_R)=(n+\phi_R)/2$ with $n$ odd; $Y_R$ decreases in steps of at most
   $(d+1)/2$, so $y_0\in[\alpha_0,\alpha_0+(d+1)/2)$ and $y_1<\alpha_0+2.00005$.
   Re-derived and correct.
   With $\operatorname{frac}(\bar g)\ge\frac12$ one has $m\le\bar g+\frac12$ and
   $\delta=m-g_0\le2.500001$, which lowers the main tilt’s range (the program uses
   $4.5002$ and $2.500002$, both conservative).
   The paper’s paragraph on real lifts is right: Lemma 6.1, Corollary 6.2 and
   Proposition 6.3 are statements about one band with any real $y_0\ge0$, $R\ge1$ and
   $y_1\ge0$, and the two bands may have different lifts because their strips are
   disjoint regions of $[0,S]^2$.

**The tiered proof of Theorem 1.1** is Section 8.4 of version 1.0 with the tier’s
$(b_0,c_y,C_E)$ and the conditions $C_i\ge\frac{32}5(\frac53)^{3/8}C_E^{5/8}$,
$k_i\ge\frac35C_Eb_0^{8/5}$, $a_i\ge\frac{12}5C_Eb_0^{-2/5}$, the $\lambda'$ bound and
the two room conditions; for the tiers $\ddagger$ the lifts of Lemma 8.11 replace
$\frac14\lceil4c_yb^{4/5}\rceil$ and $k_i\ge10^{12}$ supplies the room.
Re-derived; the constant $\frac{32}5(\frac53)^{3/8}\approx7.751277$ is right.

**The programs.** `cert_v3.py` is `cert3e.py` with the parameters, the exact half-angle
test $t_{\rm up}<1/10$, the margin $\chi-4$, (E-iv) as $1-\varepsilon_m-\tau$, and, for
the parts “ABC”, $X_3=A_T'z^2$ and $R_e=(w_e+2(1+\tan\alpha_0))z^3$; each of these was
checked against Appendix A and against Lemmas 8.3 and 8.5. `cert_v4.py` adds the
per-wall tilt factors, the margin (W6) as $\varpi a_n-q_{0,n}^2z/\zeta_n$, the
enclosures with $4.5002$ and $2.500002$, and the terms $R_{\rm start}$ and $R_{\rm end}$
of $B_{W4}$; each term was checked against Appendix B and against Lemma 8.8 (for example
$(\bar K+2)z^3/(8\nu_*)=((\bar Kz)z+2z^2)/(8\nu_*/z)$). Both merge steps check that the
slices cover every $z$-interval exactly once, that every margin’s exact lower end is
positive, and the stated constants of the tier in interval arithmetic.
`cert_v4.py` also fixes the last $t$-piece’s upper end to the range’s upper end; in
`cert3e.py` and `cert_v3.py` it is $t_\ell+(t_u-t_\ell)N_T/N_T$, which can fall short of
$t_u$ by one unit in the last place at 120 bits (finding RF-3), harmless because the
$t$-range carries slack of relative order $10^{-7}$ from $\delta'\le3.000001$.

**Replayed here.** Every one of the twelve tiers was recomputed on this machine with the
source’s programs at the source’s resolution ($320\times128$ boxes), in one slice per
tier, and merged with the stated constants; the table is filled from those runs
(`replay/v11/m_<tier>.json`).

| Tier | Boxes | $\Psi_{\sup}$ here | $\Psi_{\sup}$ recorded | $C_E^{\rm cert}$ here | $C_E$ stated | Smallest margin here | Merge |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1† | 320×128 | 65.9030816399 | 65.9030816399 | 17.46021991 | 17.461 | (W2) of $Z_{\rm L}$, 0.01733 | valid, theorem checks true |
| B1s† | 320×128 | 67.0680425442 | 67.0680425442 | 16.96721215 | 16.968 | (W2), 0.01670 | valid, true |
| B2† | 320×128 | 67.7914201489 | 67.7914201489 | 16.72078458 | 16.721 | (W2), 0.01411 | valid, true |
| A1 | 320×128 | 85.6480563666 | 85.6480563666 | 18.96098158 | 18.961 | (W2), 0.01447 | valid, true |
| A1s | 320×128 | 85.6690521631 | 85.6690521631 | 18.72101720 | 18.722 | (W2), 0.01466 | valid, true |
| A2 | 320×128 | 87.6230931509 | 87.6230931509 | 17.52221442 | 17.523 | (W2), 0.01569 | valid, true |
| A3 | 320×128 | 92.1362538750 | 92.1362538750 | 15.85844696 | 15.859 | (W2), 0.01577 | valid, true |
| A4 | 320×128 | 101.1581128379 | 101.1581128379 | 14.77798713 | 14.778 | (W2), 0.01450 | valid, true |
| A5 | 320×128 | 90.8527530931 | 90.8527530931 | 14.15236483 | 14.153 | (W2), 0.01563 | valid, true |
| C1‡ | 320×128 | 58.9137796683 | 58.9137796683 | 14.47250922 | 14.473 | (W2), 0.01628; (W6), 0.5911 | all 14 checks true |
| C2‡ | 320×128 | 58.5181311816 | 58.5181311816 | 14.80458900 | 14.805 | (W2), 0.01574; (W6), 0.5725 | all 14 checks true |
| C3‡ | 320×128 | 57.8715620717 | 57.8715620717 | 14.98287272 | 14.983 | (W2), 0.01561; (W6), 0.5962 | all 14 checks true |

Every value agrees with the recorded merges (`merged_v3.json`, `C1.json`–`C3.json`) to
every printed digit, every one of the 27 (A/B) or 33 (C) margins is positive on all
40,960 boxes of each tier, and each merge’s theorem checks (`C_E` stated at least the
certified value, $C_i\ge\frac{32}5(\frac53)^{3/8}C_E^{5/8}$,
$k_i\ge\frac35C_Eb_0^{8/5}$, $a_i\ge\frac{12}5C_Eb_0^{-2/5}$, $\lambda'<1$, the room
conditions, and $k_i\ge10^{12}$ for the tiers ‡) hold; the largest $\lambda'$ bound is
$2.97\cdot10^{-7}$ (C3). The runs took 80 to 300 s per tier on a loaded four-core
machine; the recorded regression of `cert_v3.py` on the row v1.0 reproduces
`cert3e.py`’s $\Psi_{\sup}$ and $C_E^{\rm cert}$, so the two programs agree where they
overlap.
So the tiers are established by the code the release contains, in the sense that
the proof needs: on a covering of the whole parameter range of each tier, the hypotheses
of Lemmas 8.1, 8.2, 8.5 or 8.8 and of Corollary 8.3 or 8.12 hold and the normalised
bound is at most $\Psi_{\sup}$; what remains is the transcription from the lemmas to the
normalised inequalities, which this review checked by hand term by term and which the
source’s own statement calls the weak point of its three same-family coverings.

The reported values that the release does not contain remain reported: the three further
coverings per tier (two verification agents, one reviewer), the direct un-normalised
`python-flint` covering of C1–C3 for $b_0\le b\le10^{16}$ with suprema $13.910$,
$14.235$, $14.319$, the 133-instance exact re-implementation, and the 15 complete end
packings for C1–C3 at $b$ from $1.41\cdot10^7$ to $2.30\cdot10^7$ with
$U\le0.69\,C_Eb^{3/5}$. The exact tests the release does contain were replayed:
`sl_t2_test.py 3000 500` reproduces the recorded output (0 failures of Lemma 8.6 in
3,000 random and 4 adversarial cases, excess up to $0.99999$ of $1/(8\nu)$; 0 failures
of Lemma 8.11 in 500 bands).

## 7. Theorem 1.6: The Certified Packings

The theorem’s structural part is Corollary 6.2 with Lemma 2.2, proved above; its finite
part is the data: for each of four ends per $k$, a lift $y$, a tilt
$(\cos\alpha,\sin\alpha)$ with $\tan(\alpha/2)$ on the grid $2^{-40}$, and every piece
as exact rationals (tilted $1\times n$ columns by their lowest vertex, horizontal
layers, left-wall rows).
The rows of the bands are not in the data; their validity rests on Lemmas 3.3 and 6.1,
which is a trust boundary the paper states.
The checker must recompute, from $(k,b,y_0)$ alone, the band ($w<b$, $S<k$, $d$, $h$),
$R=\lfloor(L_b-h-2y_0)/d\rfloor+1\ge1$ and $y_1\in[y_0,y_0+d)$ for both bands, check
that the file’s lifts equal $y_0$ and $y_1$, and decide (C0)–(C4) and the count.

| Checker | Decides | Arithmetic | Relation to the generator |
| --- | --- | --- | --- |
| `stair_check.py` (source) | band, rows, lifts, shapes, containment of every vertex in $\operatorname{Reg}(y)$, separating axes on every pair whose bounding boxes overlap (float candidates with margin $10^{-6}$, decided exactly), $N$, $c$, the waste identity; 7 negative controls | `gmpy2.mpq` or `Fraction` | written from a description of the construction, does not import `stair_dump.py`; same author and AI family |
| `cert_data_indep.py` (this review) | the same statements, written from Section 9 and the data description only | `gmpy2.mpq` | shares no code with the source |

**Checked by computation here.** `cert_data_indep.py` decided $k=10^5$ (0.2 s), $10^6$
(1.3 s) and $10^7$ (10 s): every end passes with 0 shape, containment and overlap
failures, the lifts match, and $N=9{,}999{,}998{,}416$, $999{,}999{,}996{,}027$ and
$99{,}999{,}999{,}989{,}960$ with $c=1584$, $3973$ and $10040$ and the waste identity
exact, which reproduces the paper’s Table 2 and gives $c^*(10^5)\le1583$,
$c^*(10^6)\le3972$, $c^*(10^7)\le10039$. Two mutations were refused: a column moved
right by $10^{-7}$ (one overlap) and a layer lengthened by one (one containment
failure). The two largest certificates were decided the same way after the tier replays
had freed the machine: $k=3.825\cdot10^7$ (32 s; 2,730,501 exact pair decisions,
$N=1{,}463{,}062{,}499{,}983{,}011$, $c=16989$, identity exact, so
$c^*(3.825\cdot10^7)\le16988$) and $k=10^8$ (73 s; 5,748,521 exact pair decisions, the
same count the source’s checker reports, $N=9{,}999{,}999{,}999{,}975{,}209$, $c=24791$,
identity exact, so $c^*(10^8)\le24790$). So all five rows of Table 2 are reproduced by
code that shares nothing with the source’s. The source’s `stair_check.py` replayed here
at $k=10^5$ passes with the recorded numbers (22,274 exact pair decisions) and its seven
negative controls are all rejected (`MUTATION TEST: PASS`). The generator’s rules are
not part of the verification, as the paper says; the certificates prove the five listed
bounds and nothing more.

## 8. Findings

None is blocking.

| Id | Pinpoint | Blocking | What it is | What would resolve it |
| --- | --- | --- | --- | --- |
| RF-1 | Lemma 8.1 (f3), unaligned closings and final stretches with left end $x=0$ | No | The placement needs $j+1\le r(0)=\chi$, which the proof does not say; it holds because such a row has $j<J_{0,0}\le H(J_{0,0})\le\Gamma_{0,0}=\chi$. Version 1.1’s Lemma 8.7 (F0) supplies the line for the tiers $\ddagger$ | One sentence in Lemma 8.1 |
| RF-2 | Lemma 8.1, hypothesis (W3) | No | The proof of $J'_0\le J_{\rm L}$ needs $\zeta(1+\sec\alpha_0+M_{\max}\tan\alpha_0)$ where (W3) has $\zeta(2+\cdots)$; slack, not a gap | None |
| RF-3 | `cert3e.py` line 135, `cert_v3.py` line 211 | No | The last $t$-piece ends at $t_\ell+(t_u-t_\ell)N_T/N_T$, which can be one unit in the last place below $t_u$; the range has slack of relative order $10^{-7}$, and `cert_v4.py` sets the end to $t_u$ | Set the end to $t_u$, as `cert_v4.py` does |
| RF-4 | `cert_v3.py` `wall()`, `flag` | No | A non-positive wall slope is replaced by $10^{-40}$ and flagged, and the flag is not counted as a failure; it coincides with the (E-iii) margin, which is counted. `cert_v4.py` counts it (`sigpos_`) | None for the record |
| RF-5 | Section 1, “[AMS] proved $c^*(k)\le k-1$ for $k>12$” | No | The archived paper’s abstract states $s(n^2-n)<n$ for all $n\ge12$, with Figure 6 for $n=12$; the preprint’s “$k>12$” is a weaker reading | Wording |
| RF-6 | Theorem 1.6 and Section 9 | No | The band rows are not in the certificates and no checker replays them; Lemmas 3.3 and 6.1 carry them, and the paper says so. At $k=10^8$ the rows hold about $10^{10}$ squares, so an exact replay is out of reach and unnecessary | None; a records lane states the boundary |
| RF-7 | Version 1.0, (E6) and Corollary 8.3(i) | No | $t\le0.0014$ and $\epsilon'=1.00001\cdot10^{-12}$ are valid for the row $b\ge10^{16}$ ($\tan\alpha_0\le0.00276$) and not for general parameters; version 1.1 replaces them | Done in version 1.1 |
| RF-8 | Status sections of both versions | No | The “three independent coverings”, the direct un-normalised covering of C1–C3, the 15 large end packings and the 133-instance re-implementation are not in the release. The release’s certification of the constants is one covering per version, replayed here | Publish the other coverings, or a records lane writes an independent covering (section 10) |
| RF-9 | `cert_v3.py`, `finalize_v3.py` | No | Both read `tiers_v3.json` from the current directory and the finaliser shells out to `python` on `PATH`; reproducible only from inside `code/cert_v3`. Replayed here through a wrapper with a copy of the tier table | A path relative to the program |
| RF-10 | `packing/frontier/asymptotic-waste-bounds.schema.yaml`, `upper_bounds.exponent` | No (record, not paper) | The schema floors `exponent` at $0.5$ because Roth and Vaughan rule out any uniform exponent below $1/2$; the new bounds have exponents $3/8$ and $2/5$ and are not bounds on $W(x)$ for all $x$. They cannot be entered under `upper_bounds` as the schema stands | A new list for bounds on $c^*(k)$ (the one-sided limit), with its own description of the side condition |

## 9. Credit, Status and Significance

The preprint, its README and `.zenodo.json` name Sungjoon Ryu as the sole author.
Its Section 1.2 credits the L-shaped skeleton to Erdős and Graham and to Chung and
Graham, the tilted block to Arslanov, Mustafin and Shangitbayev, and the staircase and
the chained wall stairs to H. D. Bui (arXiv:2508.04603v2, Sections 3–4), and says the
proofs are self-contained and use none of Bui’s arguments; the record’s reading of Bui’s
Sections 3–4 (archived under `packing/resources/papers/`) agrees that the primitive
quadrilateral with layers under tilted columns and the chain of trapezoids with
decreasing tilt are Bui’s. A credit line should carry that ("Ryu after Bui" for Theorems
1.1 and 1.2); the bibliography key is the records lane’s. The novelty statement rests on
a literature search dated 2026-10-08 and cannot prove absence; nothing here contradicts
it, and the record’s own asymptotic survey (X-049, 2026-10-02) knew no bound below
$O(k^{3/5})$ for $c^*(k)$.

If registered, the draft significance is `S4`: a bound family with a new exponent and
explicit constants for a quantity the record carries as an open problem; it moves no
case and settles no count, so not `S5`. The verification rung the record can derive is
the one the earlier asymptotic rows hold: the proof is public and its computer-assisted
parts are machine certificates that replay (`V3`), and this project’s confirmation is
one AI read of the analytic chain with the certificates reproduced by the producer’s
code and, for Theorems 1.2–1.6, decided again by independent code written here (`C1` for
the read; the replays become `C3` for their parts once a records lane commits them).
No human has checked any of it.

## 10. For the Records Lane

**Stage 2, retain.** Two packets at the pinned revisions above, whole: the paper (`tex`,
`pdf`, `LICENSE`), `README.md`, `.zenodo.json`, `SHA256SUMS`, `LICENSE`, all of `code/`
(version 1.1 adds `cert_v3/`, `cert_v4/`, `zc_tests/` and 69 recorded outputs) and
`data/`. The five data files (8.5 MB) are byte-identical across the versions and can be
bound once; so can the six unchanged programs.
Each packet README records the AI-assistance and no-human-review statements in the
source’s words, the licences, the Zenodo md5 and the GitHub blob ids.
Two bibliography keys with `dated` 2026-10-09 and 2026-10-10 and `lineage: independent`
(the source credits this repository only as a problem collection, “[Le]”).

**Stage 4, replay**, all priced on this machine (4 cores shared), none in CPU-hours:

| Check | Program | Relation | Cost here |
| --- | --- | --- | --- |
| Theorem 1.6, five certificates and 7 controls at $k=10^5$ and $10^8$ | `stair_check.py` | same-implementation | 0.2 s, 1.3 s, 10 s, 30 s, 60 s with `gmpy2` |
| Theorem 1.6, five certificates, independently | `cert_data_indep.py` of this review, to be adopted as a maintained tool with a mutation test | independent-implementation | 0.2 s to about 2 min |
| Theorem 1.2, $\Phi(10^{-4/3})$ and the constants | `const_stair.py`; `phi_interval.py` of this review | same; independent | 2 s each |
| Theorem 1.1 v1.0, the covering | `cert3e.py 160 64` | same-implementation | 19 s |
| Theorem 1.1 v1.1, nine tiers | `cert_v3.py run --tier T --nz 320 --nt 128`, then `merge` | same-implementation | about 80 s per tier |
| Theorem 1.1 v1.1, tiers C1–C3 | `cert_v4.py run --lb0 … --params …`, then `merge --stated …` | same-implementation | about 130 s per tier |
| Theorems 1.3–1.4, Proposition 1.5 | `thm13_14_check.py` of this review | independent | 1 min for $k\le30$ packings and $k\le2000$ formulas |
| Wall filler and ZC′ at $m=10^4$ | `run_z.py 10000 1 0.5 4`; `zc_tests/p3test/p3test.py 10000 0.5 4 3/2 0.65 1` | same | 3 s; about 100 s |
| Lemmas 8.6 and 8.11, exact random tests | `cert_v4/sl_t2_test.py 3000 500` | same | 5 s |

What can be decided without the source’s code: Theorems 1.3 and 1.4 entirely (hand proof
plus the exact packings above); Theorem 1.2’s constants (one interval evaluation of
seven closed-form terms); Theorem 1.6’s data (an independent checker exists above).
What cannot: the coverings of Theorem 1.1, whose only route besides replaying the
source’s programs is an independent covering written from Appendices A and B, which is a
W7 slice of about a day of agent work and minutes of CPU, and would also be the first
check of the appendix transcription that does not come from the source’s AI family.
The review’s five programs are in the reviewer’s scratch space at `scratchpad/tools/`
(`thm13_14_check.py`, `stair_build.py`, `phi_interval.py`, `cert_data_indep.py`,
`e38_point.py`); adopting them under `packing/cases/asymptotic/` with tests, as
`ryu_k2_minus_c_constants.py` and `quarter_cube_constants.py` were, is the way to make
the independent replays count.

## 11. What Was Not Checked

- The two further coverings per version, the direct un-normalised covering of C1–C3, the
  133-instance re-implementation and the 15 large end packings that the source reports
  and does not include.
- The exact tests under `code/zc_tests/` other than `run_z.py` and `sl_t2_test.py`
  (`p3test.py`, `e38_zc/`, `e38_zcprime/`; their recorded outputs were read).
- The literature claims of Section 10 beyond Roth–Vaughan,
  Arslanov–Mustafin–Shangitbayev and the Squares-in-Squares reading, and the `[WDL]`
  constant beyond what the register already holds.
- Remarks 11.1–11.3 (the $k^{3/7}$ construction, the Chung–Graham Type 3 route, the wall
  wedges), which the paper does not use.
- The lower bounds of [R], [Q] and [T]; their status is the record’s (reported, with the
  reviews of 5 and 8 October 2026).

**A note on method.** Every program of the source was read before it was run, run under
`python -I` from outside its directory through a wrapper that resolves its sibling
imports, under `nice`, with at most two processes at once; nothing tracked in this
repository changed except this document and its map entry.

## 12. Verdict

**`accepted`.** No blocking defect is open.

- **What was re-derived.** Both versions in full: the reduction, the L-shaped frame and
  its count, the lifted rows and the waste identity, the staircase end lemma and
  Corollary 7.4, the wall filler and the end lemma for the exponent $3/8$, Corollary 8.3
  with its normalisation, version 1.1’s parameters, ZC′ and Lemmas 8.2–8.5, the sawtooth
  Lemmas 8.6–8.8, the lift choice 8.11, Corollary 8.12 and the tiered proof.
  No error was found; one sentence is missing (RF-1).
- **What was decided by code written here.** Theorems 1.3 and 1.4 for $k\le2000$;
  Theorem 1.2’s constants and the staircase construction at four sizes; Theorem 1.6’s
  certificates at all five $k$ with two mutations refused; the un-normalised bound of
  Lemma 8.2 at five sizes.
- **What was replayed with the source’s code.** `const_stair.py`, `cert3e.py`,
  `stair_check.py` with its controls, `run_z.py`, `sl_t2_test.py`, and the twelve tier
  coverings of version 1.1 with their merges.
- **What rests on reports.** The independent coverings and re-implementations the source
  describes and does not include.
  Theorem 1.1 in either version therefore stands, as far as this record can say today,
  on one AI read of its proof and on the producer’s own covering reproduced here.
- **The limit of this verdict.** It is one AI reviewer’s reading, of the same family as
  the author’s assistants.
  It is not a referee’s acceptance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
