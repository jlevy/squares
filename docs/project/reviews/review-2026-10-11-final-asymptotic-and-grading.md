# Final Review: Ryu’s $k^{3/8}$ Deficiency Bounds and the Grading of T-128 to T-146

**Date:** 11 October 2026. **Verdicts: accepted on all three scopes; no blocking
finding.** The four `deficiency_upper_bounds` rows of the waste register state exactly
what Sungjoon Ryu’s preprint proves, what the release’s programs certify, what this
repository decided again with its own code, and what is only reported; the proof of the
$k^{3/8}$ bounds was re-derived here from the reduction to the tiered constants without
finding a gap; the four first-party checkers decide what the 10 October review says they
decide, and all four pass again here; the nineteen register entries T-128 to T-146 carry
the rungs the checker derives, scores consistent with the rubric and with the entries
nearest to them, and generated views that agree with the register; and the fourteen
issues of the batch map each reported result to the right entry or to a recorded reason
for having none. Eight findings are recorded, none blocking; six are wording or
bookkeeping in record fields, with the replacement text given.

The reviewer is an AI agent (Claude, at maximum reasoning effort), lane F3 of the final
mathematical review of PR 487, prompted separately from the import, replay and stage 4
review lanes, with no shared context.
Its relation to the results is `project`. It moves no rung, writes no register row and
changes no tracked file but this one; the record changes it asks for are listed under
[For the Records Lane](#for-the-records-lane).
Three words are used exactly, as the 10 October review uses them: *proved* means the
argument was re-derived here and no gap was found; *checked by computation here* means a
finite statement was decided by code written in this repository from the text, or the
source’s program was replayed here with the stated result; *reported* means the source
states it and nothing here has checked it.
Where a result is called *confirmed*, the kind follows: reproduced with the producer’s
code, or independently re-implemented.

## Claims Covered

| Scope | What was reviewed | Where it lives |
| --- | --- | --- |
| 1. The deficiency bounds | Theorems 1.1 (versions 1.0 and 1.1), 1.2, 1.3, 1.4 and 1.6 and Proposition 1.5 of the preprint reported on [#471](https://github.com/jlevy/squares/issues/471) and [#486](https://github.com/jlevy/squares/issues/486), as the four rows citing `[squarepacker k2-minus-c-upper 2026]` and `[squarepacker k2-minus-c-upper v1.1 2026]` record them, against the retained TeX of both versions | `packing/frontier/asymptotic-waste-bounds.yaml` (`deficiency_upper_bounds`, `open_problem`, `relevance_to_small_n`), its schema, the two packets, the hosted-data manifest, the 10 October review, `packing/cases/asymptotic/ryu_upper_*.py` and their tests |
| 2. Grading | `verification`, `confirmation`, `significance`, `novelty`, `composition`, the *confirmed* sentences, `unfinished_confirmations`, `regularizations` and the generated views for T-128 to T-146 | `packing/frontier/results.yaml`, `RESULTS.md`, `SYNOPSIS.md`, `devtools.check_results`, `devtools.result_status`, `devtools.check_requests --backlog` |
| 3. The issues | #375, #446, #451, #465, #470, #471, #476, #481, #483, #484, #485, #486, #488, #489 | `packing/campaign/result-requests.yaml` |

**Read in full.** Version 1.1’s `paper.tex` (2,688 lines), with version 1.0’s Section 1
and the diff of the two for Section 8; the four waste-register rows, the `open_problem`
and `relevance_to_small_n` paragraphs and the schema; both packet READMEs and their
replay receipts; the hosted-data manifest; the 10 October review with its two
corrections; the first-party modules `ryu_upper_l_packing.py`, `ryu_upper_constants.py`,
`ryu_upper_staircase.py`, `ryu_upper_certificates.py`, `ryu_upper_runner.py` and the job
table and runner of `ryu_upper_replay.py`, with their five test modules; the nineteen
register entries and the comparators T-098, T-115, T-116, T-117, T-119, T-125 and T-127;
the evidence entries the nineteen cite; the seven stage 4 reviews the entries list; the
fourteen issue entries of `result-requests.yaml`;
[epistemics.md](../../../epistemics.md) and
[stage 4 of the import process](../../../packing/campaign/result-import.md#stage-4-validate).

## The Re-derivation

### What the Bounds Say, and for Which $k$

$s(n)$ is the infimum of the sides of squares that hold $n$ unit squares with pairwise
disjoint interiors; for an integer $k\ge2$,
$c^*(k)=\max\{c\in\mathbb Z:0\le c\le k^2-1,\s(k^2-c)=k\}$. Lemma 2.1 was re-derived:
with $M(x)$ the largest number of unit squares in a square of side $x$ (attained, by
compactness) and $m(k)=\max_{1\le x<k}M(x)$, one has $s(n)<k$ exactly when $n\le m(k)$,
because $s(n)<k$ gives a packing in some side $x<k$ by the definition of the infimum,
and $n\le M(x)$ with $x<k$ gives $s(n)\le x$; as $s(n)\le k$ for $n\le k^2$ (the grid),
$s(k^2-c)=k$ iff $k^2-c>m(k)$, so $c^*(k)=k^2-m(k)-1$, and $W(x)=x^2-M(x)\to k^2-m(k)$
as $x\to k^-$ because $M$ is constant on some $[x_1,k)$. Lemma 2.2 follows: a packing of
$N$ squares in a square of side $S<k$ gives $N\le M(S)\le m(k)$, hence
$c^*(k)\le k^2-N-1$. The register’s definition, $c^*(k)=\lim_{x\to k^-}W(x)-1$, is this
lemma.

So a statement $c^*(k)<Ck^{3/8}+a$ for every integer $k\ge k_0$ means: for each such $k$
the paper exhibits $N$ unit squares in a square of side $S<k$ with $k^2-N-1<Ck^{3/8}+a$;
equivalently $s(k^2-c)<k$ for every integer $c\ge Ck^{3/8}+a$, while $s(k^2-c)=k$ is
asserted for no $c$ by any of these theorems (the lower bounds are the other
preprints’). The ranges, read from the statements and their proofs:

| Statement | Holds for | What fixes the range |
| --- | --- | --- |
| Theorem 1.4, $c^*(k)\le8\lceil\sqrt{k-4}\,\rceil-1$ | every integer $k\ge6$ | $b=\lceil\sqrt{k-4}\,\rceil\ge2$, $2k-10>0$ and $k-3>2$ in the proof |
| Theorem 1.2, $c^*(k)<20.668\,k^{2/5}+0.623$ | every integer $k\ge1.6\cdot10^7$ | $b_*=(3k/(2C_E))^{3/5}\ge10^4$, the floor of Corollary 7.4, needs $k\ge\frac23C_E10^{20/3}=1.5565\cdot10^7$ |
| Theorem 1.1 of version 1.1, $c^*(k)<C_ik^{3/8}+a_i$, twelve tiers | every integer $k\ge k_i$; the least $k_i$ is $2.48\cdot10^{12}$ (tier C3) | $k_i\ge\frac35C_{E,i}b_{0,i}^{8/5}$ puts $b_*\ge b_{0,i}$, the floor of the tier’s covering; everything else holds far below |
| Theorem 1.1 of version 1.0, $c^*(k)<43.06\,k^{3/8}+2\cdot10^{-5}$ | every integer $k\ge4\cdot10^{26}$ | the row $(b_0,c_y,c_D,c_R,a_w,\varpi)=(10^{16},1/12,4,4,3/2,0.65)$ with $C_E=15.54$, kept in version 1.1 and superseded by tier A5 ($40.62\,k^{3/8}+1.4\cdot10^{-5}$ for $k\ge3.4\cdot10^{26}$) |
| Theorem 1.6 | $k=10^5,10^6,10^7,3.825\cdot10^7,10^8$ | the five data files |

For $k<1.6\cdot10^7$ only Theorem 1.4 and the certificates at $10^5$, $10^6$ and $10^7$
apply; the tiers beat Theorem 1.2 from $2.48\cdot10^{12}$ (C3), from $5.07\cdot10^{13}$
(B1s) without the sawtooth tiers, and from $6.1\cdot10^{14}$ (A1s) with the lemmas of
version 1.0 alone. The register’s rows say this in these words.

### The Frame, Theorems 1.3 and 1.4 and Proposition 1.5: Proved

The tilted block $B(P)$ of $b$ unit squares at angle $\theta$ has width
$f(\theta)=b\cos\theta+\sin\theta$ and height $h(\theta)=b\sin\theta+\cos\theta$ (Lemma
3.1, by linearity of the coordinates on $[0,b]\times[0,1]$). With
$\theta_0=2\arctan(1/b)$ the half-angle formulas give $\cos\theta_0=(b^2-1)/D$,
$\sin\theta_0=2b/D$, $D=b^2+1$, so $f(\theta_0)=b$ and $h(\theta_0)=h_0=(3b^2-1)/D$; and
$f(\theta)=\sqrt{b^2+1}\cos(\theta-\varphi)$ with $\tan\varphi=1/b$ decreases on
$[\theta_0,\pi/2]$, so $f<b$ above $\theta_0$ (Lemma 3.2): the band is narrower than $b$
by $\varepsilon=b-f(\theta)>0$ and the whole packing has side $S=k-b+f(\theta)<k$. Rows
stacked at the vertical spacing $\sec\theta$ have, in the frame
$(u\cdot(z-P_0),v\cdot(z-P_0))$, the form $[i+j\tan\theta,i+1+j\tan\theta]\times[j,j+1]$
(Lemma 3.3), so they are disjoint, and a band of $R$ rows fits in height $L$ when
$(R-1)\sec\theta+h\le L$ (Lemma 3.4). The grid $[0,k-b]^2$, the right band in
$[k-b,S]\times[0,S]$ and the reflected top band in $[0,k-b]\times[k-b,S]$ have interiors
separated by the lines $x=k-b$ and $y=k-b$ (Lemma 4.1), which gives Theorem 1.3’s
packing of $N(k,b)=(k-b)^2+b(R(k)+R(k-b))$ squares once the angle is chosen.

Lemma 4.2 chooses $\theta=2\arctan(M/(bM-1))$, $M=14kb^2+1$: it lies in
$(\theta_0,\theta_0+\tau]$ with $\tau=1/(7kb^4)$ because
$\theta-\theta_0\le2(M/(bM-1)-1/b)=2/(b(bM-1))\le2/(14kb^4)$; the slack
$g(L)=L-h_0-(R(L)-1)d_0$ is a positive integer multiple of $1/((b^2-1)D)$, hence at
least $1/(b^4-1)$; and on $[\theta_0,\theta_0+\tau]$ the derivatives $d'\le4$,
$h'\le b$, $|f'|\le b+1$ (using $\cos\ge3/5-1/224\ge1/2$) make the drift of the length
conditions at most $7k\tau=1/b^4<1/(b^4-1)$, so (L1) and (L2) hold with $R_1=R(k)$,
$R_2=R(k-b)$. The cosine and sine are rational, so every vertex is rational, which is
what lets a checker decide the packing exactly.

The count (5.1): $(L-h_0)\gamma_0=L-3-\eta_L$ with $\eta_L=(2L-10)/D+8/D^2$ (from
$h_0=3-4/D$, $\gamma_0=1-2/D$), so $R(L)=\max(0,L-3-\lfloor\eta_L\rfloor)$ and
$k^2-N(k,b)\le6b+b(\lfloor\eta\rfloor+\lfloor\eta'\rfloor)$, with equality when
$k-b\ge2$ since then both ceilings are non-negative.
Then $\lfloor\eta\rfloor+\lfloor\eta'\rfloor\le2\eta-2b/D$ gives $k^2-N<6b+4k/b-2$
because $2-20b+16b/D<0$ for $b\ge2$: Theorem 1.3. With $b=\lceil\sqrt{k-4}\,\rceil$ and
$k\ge6$, $D\ge k-3$ and $\eta\le2-(4(k-3)-8)/(k-3)^2<2$, so both floors are at most $1$
and $k^2-N\le8b$: Theorem 1.4, $c^*(k)\le8b-1<8\sqrt{k-4}+7$. Proposition 1.5
($k^2-N>8\sqrt k-14$) follows from $\lfloor z\rfloor>z-1$, the substitution $x=b+1/b$
and the inequality of means, with the cases $b\in\{k-1,k\}$ by hand.
Each of these steps was re-derived; the proofs are complete as printed.

**Checked by computation here.** `ryu_upper_l_packing` builds the packing of Lemma 4.2
in exact rationals for all 434 pairs $2\le b\le k\le30$, $(k,b)\ne(2,2)$, and finds
every one valid with exactly $N(k,b)$ squares, and decides (5.1) with its equality case,
Theorem 1.3, Proposition 1.5, Theorem 1.4, Corollary 5.1 and Remark 5.2 in integers for
$2\le b\le k\le2000$; it also decides that $8\lceil\sqrt{k-4}\rceil-1<k-1$ first at
$k=65$, and fails again exactly at $k=69$ to $72$, which is what the register’s
corollary states (for $\lceil\sqrt{k-4}\rceil=n\ge10$ the bound is below $k-1$ at every
$k$ of the block, since $n^2-10n+5\ge0$; for $n=9$ it fails on the block’s first four
values).

### Lifted Rows and the Waste Identity: Proved

In a band’s strip frame $\Sigma=[0,w]\times[0,L_b]$ the rows are $B(P_j)$,
$P_j=(\sigma,y_0+jd)$, and $y_1=L_b-h-(R-1)d-y_0$; the end region
$\operatorname{Reg}(y)$ is the part of the strip below the line through $(\sigma,y)$
with direction $u$. Lemma 6.1: the rows have $x$-projection $[0,w]$ and $y$-projection
inside $[y_0,L_b-y_1]$; $\operatorname{Reg}(y_0)\subset\{\beta'\le0\}$ because
$\beta'(x',y')=-\sigma(x'-\sigma)+\gamma(y'-y_0)\le0$ is
$y'\le y_0+(x'-\sigma)\tan\theta$; the rotation $\rho$ by $\pi$ about the strip’s centre
sends the highest vertex $P_{R-1}+bu+v$ of the last row to $(\sigma,y_1)$, and since
$v\cdot(P_{R-1}+bu+v-P_0)=R$, $\rho(\operatorname{Reg}(y_1))\subset\{\beta'\ge R\}$. The
three regions have disjoint interiors, so end packings in $\operatorname{Reg}(y_0)$ and
$\operatorname{Reg}(y_1)$ and the rows form a packing in $\Sigma$. Proposition 6.3,
$wL_b-bR-|\mathcal C_0|-|\mathcal C_1|=(R-1)\tan\theta+E(y_0)+E(y_1)$, is the area
decomposition $wL_b=A_0(y_0)+A_0(y_1)+(R-1)dw+b$ with
$A_0(y)=yw+\frac12\gamma\sigma(1+b^2)$ (the integral of the first row’s lower boundary)
and $dw-b=\tan\theta$; $A_0(y)$ exceeds the area of $\operatorname{Reg}(y)$ by the
triangle $\frac12\tan\theta$, so $E(y)=U(y)+\frac12\tan\theta$. Both bands may carry
different lifts, since each statement is about one strip.
Re-derived; complete.

### The Staircase End and Theorem 1.2: Proved, with the Constants Checked Here

Lemma 7.2 is the identity $(1+t^2)(m\cos\alpha+\sin\alpha-g_0)=-F(t)$ with
$F(t)=D_mt^2-2t-\delta$, so $m\cos\alpha+\sin\alpha\le g_0$ iff
$t\ge t^*=(1+\sqrt{1+D_m\delta})/D_m$, and $t^*$ increases in $\delta$ and decreases in
$D_m$. Lemma 7.3’s construction (S1)–(S6) and its nine proof parts were re-derived step
by step; the points that carry the bound:

- Every slab up to the right wall gets a column, since
  $H(J)=J+(m-J)\cos\alpha+\sin\alpha$ is affine with slope $1-\cos\alpha>0$,
  $H(0)\le g_0\le\Gamma_i$ by the tilt and $H(m)>\bar g\ge\Gamma_i$, so
  $0\le J_i\le m-1$, the $J_i$ are non-decreasing and each gap $\Gamma_i-H(J_i)$ is
  below $1-\cos\alpha$.
- A column part costs at most
  $\tan\alpha+\sec\alpha(1-\cos\alpha)+\sec\alpha\,\mu(\sec\alpha+m\tan\alpha)$: the
  parallelogram $\{\xi_i\le\lambda\le\xi_i+\sec\alpha,\J\le Y\le H(J)\}$ lies in
  $\operatorname{Reg}$ and has area $\sec\alpha(n\cos\alpha+\sin\alpha)=n+\tan\alpha$,
  and above it the sections are at most $\sec\alpha$ long and at most
  $\Gamma_i+\mu(\sec\alpha+m\tan\alpha)-H(J_i)$ high.
  Summed with $I\sec\alpha\le w$ this is
  $w\sin\alpha+w(1-\cos\alpha)+\Delta(\sec\alpha+m\tan\alpha)$, the first three terms of
  $B^*$.
- The layer rows $0\le j\le j_1$ waste less than $1+\frac12\tan\alpha$ each, there are
  at most $\lfloor\bar g\rfloor$ of them, and the right corner above $j_1+1$ has area
  below $\omega(1+\mu\omega)$, $\omega=\sec\alpha+\bar g\tan\alpha$, because
  $j_1\ge J_{I-1}-1$ (every $j\le J_{I-1}-1$ has $g(a_j)\ge\Gamma_{p(j)}\gej+1$) and the
  maximality of $j_1$ gives $\bar g-(j_1+1)<1+\mu\omega$.
- The wedge rows waste less than $1+\frac12\tan\alpha$ each in $\lfloor g_0\rfloor$
  rows, and the left corner has area below
  $(\delta+1)\tan\alpha(1+\mu(\delta+1)\tan\alpha)$.

Corollary 7.4 was re-derived from the band facts ($t_\theta=b/(b^2-1)$,
$bt_\theta\le1.00000002$, $\mu\le2.000001/b$, $\sigma\mu\le4.1\cdot10^{-8}$,
$w\ge b-2.1/b$), the ranges of $g_0$, $\bar g$, $m$, $\delta\le3.000001$, the tilt bound
$t\le x\vartheta(x)$ with $\vartheta(x)=(x+\sqrt{x^2+A\kappa})/(2p(x))+x^2/16$ (from
Lemma 7.2 with $\nu=p(x)u^2$ and $Q\ge16b$), the seven normalised terms $T_1,\dots,T_7$
divided by $u^2=b^{2/3}$, and the monotonicity of each in $x$. The proof of Theorem 1.2
in Section 7.3 (the room for the lifts, $y_1\in[y_0,y_0+d)$ inside the window of length
$2>\sec\theta$, the three parts of $k^2-N$, the bound $\lambda'\le8.001\,k/b^3+4.1/b<1$,
and the closed form through $4k/b\le\frac83C_Eb_*^{2/3}$ and
$b^{2/3}\le b_*^{2/3}+\frac23b_*^{-1/3}$) is complete.

**Checked by computation here.** `ryu_upper_constants` recomputes the seven terms at
$x_0=10^{-4/3}$ on `mpmath` intervals at 50 digits and finds
$\Phi(x_0)\in[5.01624876754,5.01624876755]$, inside the paper’s $[5.0162487,5.0162488]$
and below $C_E=5.03$; a supremum over 400 subintervals of $[0,x_0]$ without the
monotonicity argument gives the same value; $\bar t\le0.0672$, $\bar\tau\le0.1349$; the
closed forms $20.66740\ldots<20.668$, $0.62259\ldots<0.623$, the threshold
$1.5565\cdot10^7\le1.6\cdot10^7$, $\lambda'<1$ and the limit coefficient
$18.886\le18.89$; 77 checks, none failing.
`ryu_upper_staircase` builds (S1)–(S6) exactly at $(b,y)=(400,41)$, $(1600,103)$,
$(10^4,1393/4)$ and $(10^4,1399/4)$, decides every piece (shape, four vertices in
$\operatorname{Reg}(y)$, exact separating axes on 3,279 to 301,111 bounding-box pairs)
and finds $U\le B^*\le\Phi(x)\,b^{2/3}$ in each, with $U/b^{2/3}$ between $3.47$ and
$3.79$.

### The Wall Filler and the Exponent $3/8$: Proved Modulo the Covering

Lemma 8.1 fills the trapezoid $Z(\chi,\zeta,L)$ by chained staircases whose tilt drops
by $\kappa_\beta=q_\beta^2/\zeta$ from block to block, $q=1-\cos\alpha$. The invariants
were re-derived: (I3) passes to the next block because $F'$ is a maximum; (I1) because
the drift $C_\beta$ of the tilts is bounded through (8.1)
$q\le(\zeta\Lambda_\beta+1+\zeta\tan\alpha)/N_0$ and the block count $\beta+1\le\bar K$
by $\Delta_{\rm dr}<(1-\varpi)\tan\alpha_0$, hypothesis (W2); (I2) because
$M'\le M-1+N_0$ and $\hat\xi\ge M\tan\alpha+N_0\tan\alpha_0$ by (W1). The step
$J_0'\le J_{\rm L}$ needs
$n_{\rm L}+\sin\alpha-N_0\cos\alpha'+\zeta(1+\sec\alpha+M\tan\alpha)+(1+\zeta\tan\alpha')/q'\le1$,
which (W3) supplies with one spare $\zeta$ (RF-2 of the 10 October review, re-derived
here). The relation (R) for the aligned closings was re-derived from
$p(j)=\lceil B(j+1-A)\rceil$: modulo $1$,
$\ell_j\equiv(\omega-\omega_0)+(j-J_{\rm lo})\eta+(1-f_j)(\sec\alpha-1)$, three terms in
$[0,1/Q_f)$, $[0,N_0\delta_Q)$ and $(0,\sec\alpha_0-1]$, whose sum is $\varepsilon_W<1$
by (W4); with $\ell_j\ge\sec\alpha-\tan\alpha'>0$ this gives
$\operatorname{frac}(\ell_j)\le\varepsilon_W$. The partition of $Z$ into cells and
stretch regions and the six bounds of (f3) hold as printed; RF-1’s missing sentence (a
stretch with left end $x=0$ is placed only if $j+1\le\chi$, true because
$j<J_{0,0}\le\Gamma_{0,0}=\chi$) is supplied by version 1.1’s Lemma 8.7 (F0).

Lemma 8.9 (E38) was re-derived: the shifted main staircase with the tilt from
$t^*(m,g_D)$; the cut at $\ell_0=\xi_{N-1}+\omega_m$ with tilt
$\tau\le\tan\alpha-\kappa_m$, where (E-iv) in the form $\varepsilon_m+\tau<1$ forces
$\ell_j\ge0$ from $\ell_j\ge-\tau$; and the three walls as exact rotations of
$Z(\xi_0-g_0\tan\alpha,\tan\alpha,g_0)$, $Z(w-\ell_0,\tau,J_{\rm L})$ and
$Z(w-\xi_N+J_{\rm L}\tan\alpha,\tan\alpha,Y_u-J_{\rm L})$, each inside
$\operatorname{Reg}(y)$ ($Y_u$ solves $Y=g(\xi_N-Y\tan\alpha)$, and $J_{\rm L}\leY_u$
because $J_{\rm L}\le\Gamma_{N-1}\le g(\xi_N-J_{\rm L}\tan\alpha)$). The separations
were checked line by line, including the main rows against $Z_{\rm LR}$ (the top right
corner of a row piece has $X+Y\tau\le\ell_0$) and the partition of (d), whose row
regions reach past $\lambda=\xi_N$ where $J_{\rm L}\hat\kappa$ is large, as they must; a
row region has area $\ell_j+\frac12(\tan\alpha+\tau)$ and wastes at most
$\varepsilon_m+\tan\alpha$.

Version 1.1’s additions were re-derived as the 10 October review describes them and no
gap was found: the error of the wall tilts for all $t\le1/10$ (the logarithmic
derivative of $\tan\alpha$ in $t$ is at most $1.020203$), the room for the lifts
($c_y(5/(3C_E))^{1/2}\le1$ and $c_y\le3/4$ in every row), the variant ZC$'$ with
Observation (O) and Lemmas 8.2–8.5
($A_T'=(h_T+1)(1+\tan\alpha_0)+(2+\zeta(w_T+\tan\alpha_0+\zeta\tan\alpha_0))(w_T+\tan\alpha_0)$
for the transition rows, and the partial layer $P_z$ of area at most $L$ for the end
region), the sawtooth Lemma 8.6 (runs between wraps; the first run’s excess
$(r-r^2\nu)/2\le1/(8\nu)$), Lemma 8.7 on the start rows and the four classes of final
stretches with the new hypothesis (W6) $\nu_*=\varpi\tan\alpha_0-q_0^2/\zeta>0$, and
Lemma 8.11’s lift $Y_R=(S_R-\epsilon_R)/2$ with
$\operatorname{frac}(\bar g(y_0))=\operatorname{frac}(\barg(y_1))\ge\frac12$, which
lowers $\delta$ to $2.500001$.

**The normalisation, checked by hand here.** Corollary 8.10 multiplies every term of
Lemma 8.9 and of $B_W$ by $z^3=m^{-3/4}$ and writes it in $\hat b=bz^5$, $t/z^2$,
$\chi z^3$, $Lz^4\le1$ and the wall inputs, so that $z=0$ is admissible and a box cover
of $[0,z_0]$ times the range of $t/z^2$ covers every integer $b\ge b_0$ and every lift
in the window; the two right walls’ $L$-linear parts take the larger coefficient since
$L_{\rm LR}+L_{\rm UR}\le m$, and their other terms the value at $L=m$, legitimate
because $B_W$, $B_W''$, $B_{W4}$, (W2) and (W3) are non-decreasing in $L$ and (W6) is
free of $L$. Twenty-three enclosures of Appendices A and B were re-derived from the
un-normalised lemmas, independently of the 10 October review’s term-by-term check: the
$t$-range (from $t^*\ge\sqrt{\delta'/D'}$ with $D'\le2m$,
$\delta'>2(1-D_\ell/b-2.1/b^2)$, and from the monotonicity of $t^*$ with
$D'\ge2m-3.000001$, $\delta'\le3.000001$, or $2.500002$ for the tiers $\ddagger$);
(E-ii) as $z^5(w-D_\ell-D_r-m\tan\alpha-\sec\alpha)$ from below; (E-iii) with
$\kappa_m/z^2\le q_n^2\hat bz/(\mu b)$; $J_0\le(4mt+2)/(Qq)$, from $|dH(0)/dt|\le4mt+2$
and $t-t^*\le1/Q$; $\Lambda z^3=(q_{\min,n}N_0z^3-z-\zeta_na_nz^4)/\zeta_n$; the three
terms of $\Delta_{\rm dr}/z$; (W3) term by term; $c_{\rm col}/z$;
$X_1=(N_0z^3-z^3)((\varepsilon_W/z^2)z+a_n)$, $X_2$, $X_3=h_T(w_Tz)z$ and its $B_W''$
form; $h_T$, $w_Tz$, $w_0$, $w_ez^2$ and $R_e$ in both forms;
$\frac12\mu h_{\rm L}^2z^3$ and $\mu w_R^2z^3$ with
$h_{\rm L}\in[D_\ell,D_\ell+3.000001\tan\alpha]$ and
$w_R<D_r+\sec\alpha+\bar g\tan\alpha$; and for Appendix B the margin
$\nu_*/z=\varpi a_n-q_{0,n}^2z/\zeta_n$ and the terms $R_{\rm start}$ and $R_{\rm end}$
of $B_{W4}$, among them $(\bar K+2)z^3/(8\nu_*)=((\bar Kz)z+2z^2)/(8\nu_*/z)$ and
$z^3/(8\tan\alpha_0)=z^2/(8a_n)$. Every one is the stated quantity times the stated
power of $z$. This is the second hand check of the transcription that the paper itself
names as the weak point of its coverings; both checks are by AI reviewers, and no
covering written outside the source’s AI family exists.

**The tiered proof.** Section 8.4 with $b_*=(5k/(3C_E))^{5/8}$,
$b=\lceil b_*\rceil\ge b_0$, $y_0=\frac14\lceil4c_yb^{4/5}\rceil$ (for the tiers
$\ddagger$, Lemma 8.11’s lift with $\alpha_0=c_yb^{4/5}$ in each band), and
$k^2-N<4k/b+4C_Eb^{3/5}+\lambda'$ gives, with $\lambda'<1$,
$c^*(k)<\frac{32}5C_Eb_*^{3/5}+\frac{12}5C_Eb_0^{-2/5}=\frac{32}5(\frac53)^{3/8}C_E^{5/8}k^{3/8}+\frac{12}5C_Eb_0^{-2/5}$;
the constant $\frac{32}5(\frac53)^{3/8}=7.751277\ldots$ was recomputed here.
The bound on $\lambda'$, $8.001\cdot\frac35C_Eb_0^{-7/5}+4.1/b_0$, is about
$8.3\cdot10^{-8}$ for B1 and $2.9\cdot10^{-7}$ for C3 (the paper: $8.32\cdot10^{-8}$ and
$2.97\cdot10^{-7}$), and the room conditions hold in every row
($c_y(5/(3C_E))^{1/2}\le0.053$ at B1). `ryu_upper_constants` decides, for each of the
twelve tiers, $C_i\ge\frac{32}5(\frac53)^{3/8}C_E^{5/8}$, $k_i\ge\frac35C_Eb_0^{8/5}$,
$a_i\ge\frac{12}5C_Eb_0^{-2/5}$, $a_i<0.623$ and the table’s crossing column
$\max(k_i,(C_i/20.668)^{40})$, and for version 1.0 $43.05564\ldots<43.06$,
$1.485\cdot10^{-5}\le2\cdot10^{-5}$, $3.712\cdot10^{26}\le4\cdot10^{26}$ and
$C_E^{\rm cert}=14.9636\ldots\le14.964$ from the covering’s $\Psi_{\sup}=96.477$.

So Theorem 1.1 in both versions stands on: the lemmas, proved; the transcription to the
normalised inequalities, hand-checked twice; and one covering per tier, the author’s,
whose program was replayed here with the producer’s code (the 10 October packets, and
two of its jobs again below).
The register’s rows say exactly this and nothing more.

### Theorem 1.6: the Frame Proved, the Data Decided Here

The theorem is Corollary 6.2 with Lemma 2.2 applied to the five data files, each giving,
for the four ends, a lift and every piece as exact rationals; the band rows are not in
the data and rest on Lemmas 3.3 and 6.1, the boundary the paper and the register both
state. `ryu_upper_certificates`, written from Section 9 and sharing no code with
`stair_check.py` or `stair_dump.py`, recomputes the band from $(k,b,y_0)$, the rows
$R=\lfloor(L_b-h-2y_0)/d\rfloor+1$ and the upper lifts $y_1$, and decides (C0)–(C4) and
the waste identity. Its code was read against the proof: the lift comparison, the
positivity of every count, $w<b$, $R\ge1$, $y_0\le y_1<y_0+d$, the exact shape test
($|u|^2=1$, $u\cdot v=0$, $|v|^2=n^2$, the fourth vertex), containment of the four
vertices in the convex $\operatorname{Reg}(y)$, the separating axis test along both
rectangles’ edge directions on every pair whose bounding boxes overlap (exact for convex
polygons, touching allowed), and the identity
$k^2-N=(k^2-S^2)+\sum[(R-1)\tan\theta+U+\frac12\tan\theta]$ are each the statement the
proof needs. It decides what the 10 October review says it decides.

## Replays Here

Run from `packing/` with the project interpreter (Python 3.14.7, mpmath 1.3.0, gmpy2
2.3.1) on the shared four-core host, at most two processes at once, each under
`nice -n 10`; CPU is user time.
The two certificates hosted outside Git ($k=3.825\cdot10^7$ and $10^8$) are not in this
checkout, so the jobs that read them were not run; their receipts in the 2026-10-09
packet stand.

| Command (`python -m …`) | Decides | Outcome | CPU |
| --- | --- | --- | --- |
| `cases.asymptotic.ryu_upper_constants` | Theorem 1.2’s constants, version 1.0’s closed forms, the twelve tiers’ inequalities | 77 checks, all hold | 0.2 s |
| `cases.asymptotic.ryu_upper_l_packing` (packings to 30, formulas to 2000) | Theorems 1.3 and 1.4, Proposition 1.5, Corollary 5.1, Remark 5.2 | 434 packings valid, every formula holds | 45.5 s |
| `cases.asymptotic.ryu_upper_staircase` | Lemma 7.3 and Corollary 7.4 at four sizes | all four pass, $U\le B^*\le\Phi b^{2/3}$ | 4.7 s |
| `cases.asymptotic.ryu_upper_certificates --k 100000 --k 1000000 --k 10000000` with the six controls each | Theorem 1.6 at three $k$ | $N=9{,}999{,}998{,}416$, $999{,}999{,}996{,}027$, $99{,}999{,}999{,}989{,}960$; $c=1584$, $3973$, $10040$; identity exact; 22,274, 119,522 and 969,664 pair decisions; all 18 controls refused | 43.3 s |
| `devtools.check_results`, `devtools.result_status`, `devtools.check_requests --backlog` | the register’s structural checks, the derived statuses, the backlog | 146 results, every check passes; 11 recorded, 2 reviewed, 132 confirmed, 1 incomplete | about 3 s |
| the source’s `cert3e.py 160 64` (version 1.0’s covering), through the tool’s own `run_job` | $\Psi_{\sup}$, $C_E^{\rm cert}$ and the 27 margins on 10,240 boxes | equals the recorded `cert3e_out_160_64.json` field for field (wall time apart) | 22.5 s wall |
| the source’s `cert_v4.py` for tier C3, both slices (`--iz0 0 --iz1 160`, `--iz0 160 --iz1 320`), their merge with the stated constants, and the merge of the recorded slices, the same way | the 33 margins on 40,960 boxes and the stated constants of C3 | both slices equal the recorded `30_C3_s0.json` and `31_C3_s1.json`; the merge gives $\Psi_{\sup}=57.87156\ldots$, $C_E^{\rm cert}=14.98287\ldots\le14.983$, smallest margins (W2) $0.01561$ and (W6) $0.5962$, $\lambda'\le2.97\cdot10^{-7}$, every one of its fourteen checks true (the cover of every $z$-interval exactly once, every margin positive, the three inequalities of the tier, the room conditions, $k_i\ge10^{12}$), and the recorded slices merge to the same | 60.6 s and 57.3 s wall for the slices, 0.1 s each merge |
| `pytest` is not re-run: the five test modules were read, and their assertions are the values above |  |  |  |

Total CPU about four minutes (94 s for the four checkers, 140 s for the replay driver
with its tree assembly, a few seconds for the register tools), against the twenty-minute
ceiling. The replay tool itself could not assemble its trees here (finding F3-7), so its
`run_job` and comparison functions were driven from a scratch script that builds the
same trees without the two hosted files; the comparison is the tool’s own.

## Trust Boundaries

| Program | Decides | Trusts | Relation to the source’s code |
| --- | --- | --- | --- |
| `ryu_upper_l_packing` | the packings of Lemma 4.2 for $k\le30$, exactly; the counting formulas for $k\le2000$, in integers | Lemma 4.3 (that $N(k,b)$ counts a valid packing) beyond $k=30$; `fractions` | written from Sections 3–5; shares nothing |
| `ryu_upper_constants` | the closed forms and tier inequalities on intervals at 50 digits | each tier’s $C_E$ and version 1.0’s $\Psi_{\sup}$ as inputs, which come only from the source’s coverings; the seven terms of Corollary 7.4 (iv) as transcribed from the text, re-derived above; `mpmath.iv` | written from the text; shares nothing |
| `ryu_upper_staircase` | validity and $U\le B^*$ exactly, $B^*\le\Phi b^{2/3}$ on intervals, at four sizes | nothing of the source; it tests the lemma where the proof does not need it and is not the proof | written from Section 7; shares nothing |
| `ryu_upper_certificates` | (C0)–(C4), $N$, $c$ and the waste identity for the data files | Lemmas 3.3 and 6.1 for the band rows; the hosted manifest’s digests for the two largest files; `gmpy2` | written from Section 9 and the data format; shares nothing |
| `cert3e.py`, `cert_v3.py`, `cert_v4.py` (replayed) | the normalised inequalities of Appendices A and B on each box | the transcription from the lemmas; `mpmath.iv` at 120 bits; one covering per tier | the producer’s code: reproduced with the producer’s code |
| `stair_check.py` (replayed in the packets) | (C0)–(C4) on the data files | as above; same author and AI family as the generator | the producer’s code |

The two maintained routes of the register entries T-128 to T-146 (the `sqpack` rational
witness verifier and the independent rational corner checker, with the third route of
the stage 4 reviews) are outside this review’s scope and were not re-run; their
relation, independently re-implemented, is what the evidence entries record.

## The Record Against the Mathematics

Every statement of the four `deficiency_upper_bounds` rows was read against the TeX of
both versions. The rows state the theorems with their ranges, the exact count (5.1), the
end constants ($C_E=5.03$ from $\Phi(10^{-4/3})\le5.0163$; $15.54$ from `cert3e.py`’s
$C_E^{\rm cert}\le14.964$; the twelve $(b_0,C_E)$ pairs of Tables 6 and 7), the lemmas
each tier uses (ZC$'$, Lemmas 8.2–8.5; the sawtooth accounting and the lift, Lemmas
8.6–8.8 and 8.11, numbered as in version 1.1), the crossing points, the supersession of
version 1.0’s statement by tier A5, and the parts that are only reported: the two
further coverings of version 1.0 and the three per tier of version 1.1, the direct
un-normalised covering of C1–C3 for $b\le10^{16}$, the 133-instance re-implementation
and the fifteen large end packings, none in the release.
Every “CHECKED BY COMPUTATION HERE” and “REPLAYED” sentence names a program this review
ran or a receipt it read, and each number in them was reproduced above.
The `open_problem` paragraph states the reported upper side correctly and the reported
exponent interval $[1/3,3/8]$ with both ends unrefereed; the cube-root row’s corollary
names the $k^{3/8}$ rows; the Theorem 1.4 corollary’s comparison with $k-1$ (below it at
$k=65$ to $68$ and from $k=73$) is what the checker decides; and the 10 October review’s
two corrections are reflected.
The schema’s `deficiency_upper_bounds` list, with its exponent floor at $0$ and its
description of why Roth and Vaughan’s obstruction does not reach $x\to k^-$, is right:
their bound is on $W$ at $x$ with $\lVert x\rVert$ bounded away from zero and vanishes
in the limit the rows are about.
Three wording items remain (F3-4 to F3-6): a `complementary_case` that counts five
certificates where three apply, a `relevance_to_small_n` paragraph written before the
rows had explicit constants, and the 2026-10-05 row’s corollary, which still gives
$O(k^{3/5})$ as the upper side.

## Grading of T-128 to T-146

**Rungs.** `devtools.check_results` derives every declared `V` and `C` and passes; the
batch’s rungs follow its evidence: V3/C3 where a `replayed-here` exact-algebraic or
interval-certified entry with a passing replay and a mapped accepted review exists
(T-128, T-130, T-131, T-133 to T-141, T-145, T-146), V0/C0 where only a report entry
without an `external_review` exists (T-129, T-132, T-142 to T-144). `result_status`
reads them as confirmed or recorded, with T-129 superseded by T-117, T-125 and T-127,
T-133 superseded by T-145, T-145 current best and the rest pending adoption.
The RESULTS.md and SYNOPSIS table rows of all nineteen were compared with the register
by a script: counts, rungs, score, novelty and status agree, and SYNOPSIS’s
research-status row, 146 results and 116 by others, is the register’s count.

**Composition.** T-133 and T-145 name the part that sets the rung (the nodal statement
and the continuous cover, each decided by the producer’s code, so the result is
confirmed, reproduced with the producer’s code, although the finite steps are
independently re-implemented); T-132, T-142, T-143 and T-144 say that a replay would be
re-implemented sharing the producer’s components.
The upper-bound entries have one deciding kind of evidence and need no note.
The only sentences that say *confirmed* in `claim`, `composition` or `next_rung` are
T-133’s and T-145’s, and each says which kind.

**Unfinished confirmations and regularizations.** The four priced items (T-132 at 4.3
CPU-hours, T-142 at 3.28, T-143 at 4.49, T-144 at 11.24 with an upper end of 23) each
name rung C3, above the entry’s C0, a bead and a basis dated on or before the register’s
last review; the backlog sums them.
The V3/C3 entries list none, since their next rung is a review record and not a replay;
T-129’s next rung names no concrete work.
T-146’s fifteen regularizations each name a registered packing no later on the count
(T-125, T-136, T-138), a source of its own, `basis: source-claim` with the measurements
beside it, and the claim says the identity is the author’s; RESULTS.md’s Regularizations
section prints them.

**Novelty.** All nineteen are `previously-published` with `attribution`, as results by
others must be.

**Significance.** The rubric scores the claim: S2 for a citable detail that changes no
theorem, S3 for a substantive case result.
The batch’s own practice, read off the rationales, draws the line where the earlier
entries drew it: an exact re-solve of a packing the record already credits, lowering its
side at the scale of its rounding ($10^{-10}$ and below: T-098, T-117), is S2; a packing
moved by refinement or search to a new optimum, or a new construction, lowering a case
ceiling by $10^{-7}$ to $10^{-2}$ (T-119, T-125, T-127), is S3; a lower bound raised at
one count by a certificate kind the record holds (T-102 to T-111, T-099) is S3. Each
score below was compared with that line and with the nearest entries.
Each verdict confirms the score.

| id | kind | V/C | S | scored by | verdict and comparator |
| --- | --- | --- | --- | --- | --- |
| T-128 | upper bound, 8 counts | V3/C3 | S3 | think-edo8 (no draft mark) | confirm: refinements by basin hopping and `refine_packing`, $9.79\cdot10^{-7}$ (228) to $6.60\cdot10^{-4}$ (180) below the case ceilings of 10 October, as T-127 |
| T-129 | upper bound, 3 counts | V0/C0 | S1 | think-tiou (no draft mark) | confirm: historical custody of sides already superseded; bookkeeping |
| T-130 | upper bound, 5 counts | V3/C3 | S3 | think-88r0 (no draft mark) | confirm: $3.03\cdot10^{-5}$ (86) to $1.74\cdot10^{-3}$ (175) below the case ceilings, as T-127 |
| T-131 | upper bound, 132 | V3/C3 | S3 | think-iyij (no draft mark) | confirm: a different local minimum, $4.23\cdot10^{-3}$ below, as T-119 |
| T-132 | lower bound, 29 | V0/C0 | S3 | think-r333 (draft) | confirm: as T-102 to T-111, scored as a claim |
| T-133 | lower bound, 40 | V3/C3 | S3 | think-3oi5 (draft, as the review suggests) | confirm: as T-099; the transfer is noted and is one count, not a family, so not S4 |
| T-134 | upper bound, 6 counts | V3/C3 | S3 | think-m8ck (no draft mark) | confirm: $5.33\cdot10^{-6}$ to $4.37\cdot10^{-3}$ below, as T-127 |
| T-135 | upper bound, 308 | V3/C3 | S3 | think-ar8g (no draft mark) | confirm: a new two-wedge construction below the grid, $6.90\cdot10^{-4}$, as T-119 |
| T-136 | upper bound, 17 counts | V3/C3 | S3 | think-ac4h (no draft mark) | confirm: $1.68\cdot10^{-4}$ to $1.12\cdot10^{-2}$ below, as T-115 and T-116 |
| T-137 | upper bound, 70 | V3/C3 | S2 | think-8m3u (no draft mark) | confirm: Ryan Xu’s packing refined in place by $1.43\cdot10^{-10}$, as T-117 |
| T-138 | upper bound, 16 counts | V3/C3 | S3 | think-jpre (draft; rationale after the review) | confirm: the smallest known at six counts when published, up to $4.37\cdot10^{-3}$ below; the two refinements in place (103, 258) do not lower the maximum of the claim |
| T-139 | upper bound, 126 | V3/C3 | S2 | think-ilwc (no draft mark) | confirm: a more precise certificate of the same arrangement, $9.25\cdot10^{-11}$, as T-098 |
| T-140 | upper bound, 6 counts | V3/C3 | S3 | think-6uv7 (no draft mark) | confirm: $7.27\cdot10^{-4}$ to $8.03\cdot10^{-3}$ below, as T-127 |
| T-141 | upper bound, 132 and 308 | V3/C3 | S3 | think-xm4h (no draft mark) | confirm: $1.73\cdot10^{-3}$ and $5.65\cdot10^{-3}$ below, as T-119 |
| T-142 | lower bound, 28 | V0/C0 | S3 | think-i85v (draft) | confirm: as T-132 |
| T-143 | lower bound, 30 | V0/C0 | S3 | think-i85v (draft) | confirm: as T-132 |
| T-144 | lower bound, 122 to 126 | V0/C0 | S3 | think-nd7g (draft) | confirm: as T-080, five counts by monotonicity |
| T-145 | lower bound, 40 | V3/C3 | S3 | think-xms6 (draft, as the review suggests) | confirm: as T-133; the interval kernel is one count, not yet a family, so not S4; a second count by it would reopen the question |
| T-146 | upper bound, 15 counts | V3/C3 | S2 | the 11 October review | confirm: regularized views of credited packings, $2.21\cdot10^{-17}$ to $7.82\cdot10^{-10}$ below the least side held, as T-098 |

The gaps for T-128 and T-130 were computed here from the sixteen-place case ceilings
tabulated in the
[10 October refinement review](review-2026-10-10-couzo-daniel-refinement-replays.md#adoption-per-count):
at 105, 108, 127, 131, 155, 180, 228 and 306 they are $5.83\cdot10^{-5}$,
$3.77\cdot10^{-6}$, $5.79\cdot10^{-5}$, $4.47\cdot10^{-5}$, $4.26\cdot10^{-6}$,
$6.60\cdot10^{-4}$, $9.79\cdot10^{-7}$ and $4.42\cdot10^{-6}$; at 84, 86, 105, 175 and
270 they are $1.17\cdot10^{-4}$, $3.03\cdot10^{-5}$, $1.37\cdot10^{-3}$,
$1.74\cdot10^{-3}$ and $1.08\cdot10^{-3}$.

One rubric rule is not met in the fields (F3-1): a score set when a result is registered
is a draft, `by` says so, and once the reviewing lane has compared it, `by` names that
review. Eleven entries name an import bead with no draft mark and no review, and none of
the five stage 4 reviews that cover the upper-bound entries records a significance
verdict (the regularized review does, for T-146; the two Guzhou reviews suggest S3 and
say the score is the registering lane’s). This review is the comparison the rule asks
for, so the fix is to let `by` name it, with `scored` re-dated.

## The Issues

`result-requests.yaml` was read for the fourteen issues.
Each reported result maps to the register entry that holds it or to a `not_registered`
reason, and no entry claims more than the register holds:

| Issue | Reported results | Register |
| --- | --- | --- |
| #375 | 48 exact optima; 273 certificates; 77 ceilings; KKT; n105; n17; the dated 105, 130 and 292 reports | T-098, T-101, T-129; the rest `not_registered` with reasons |
| #446 | seven fine-net bounds and the n27 follow-up as evidence; the n29 follow-up at 291/50 | T-132 for the n29 follow-up; the asks name the priced replay |
| #451 | eight refinements; the five follow-ups of the PR 460 comment | T-128; T-130 |
| #465 | s(132); s(155) equal to T-128’s side; KKT | T-131; T-128 as an evidence update; KKT not registered |
| #470 | fourteen counts below the case, two README counts; fourteen above the case; the withdrawn n105 fraction | T-138 (sixteen counts); evidence only; withdrawn |
| #471 | Theorems 1.1 (v1.0), 1.2, 1.4, 1.6 | each `not_registered`: recorded in the waste register, settling no count $n\le324$; the asks are done with the 70 replay jobs |
| #476 | six certificates | T-134 |
| #481 | fifteen new packings and the smaller 154 and 237 | T-136 (seventeen counts) |
| #483 | the n70 refinement | T-137 |
| #484 | s(308); s(343), s(344) | T-135; beyond-horizon evidence only |
| #485 | clipped-corner and full-core bounds; the continuous-pose bound | T-133 (both); T-145 |
| #486 | the twelve tiers | `not_registered`: a row of its own in the waste register |
| #488 | six certificates; KKT; the unnamed 303, 338, 340 | T-140; not registered with reasons |
| #489 | 132 and 308; 343 and 344; KKT | T-141; beyond-horizon evidence; not registered |

T-139, T-142, T-143, T-144 and T-146 are reported on no issue, as their claims say, and
have no entry here. #486’s summary and claim state the tiers as Table 1 prints them.

## Findings

None is blocking.

| Id | Pinpoint | Blocking | What it is | Exact fix |
| --- | --- | --- | --- | --- |
| F3-1 | `packing/frontier/results.yaml`, `significance.by` of T-128, T-129, T-130, T-131, T-134, T-135, T-136, T-137, T-139, T-140, T-141 | No | Each names an import bead and neither says *draft* nor names a review, against the rubric (epistemics.md, Significance and Novelty: the registering lane drafts and `by` says so; the reviewing lane confirms and `by` then names the review). A reader takes a draft for a reviewed score. | For each of the nineteen entries set `scored: '2026-10-11'` and `by: the 11 October final review (docs/project/reviews/review-2026-10-11-final-asymptotic-and-grading.md), confirming the draft of <bead>`, where `<bead>` is the current `by` text’s bead; for T-146 keep its `by` and add `, confirmed by the 11 October final review` |
| F3-2 | `results.yaml`, T-128 and T-130 `significance.rationale` | No | “Eight smaller finite construction sides; no lower bound or optimum” and its five-count twin state no magnitude or nature, so the S2/S3 line cannot be read from them, unlike every other S3 rationale of the batch | T-128: `Eight smaller finite construction sides at n = 105, 108, 127, 131, 155, 180, 228 and 306, 9.79e-07 to 6.60e-04 below the case ceilings, each an earlier packing refined to a new optimum by basin hopping and refine_packing; no lower bound or optimum.` T-130: `Five smaller finite construction sides at n = 84, 86, 105, 175 and 270, 3.03e-05 to 1.74e-03 below the case ceilings, each an earlier packing refined to a new optimum; no lower bound or optimum.` |
| F3-3 | `docs/project/reviews/review-2026-10-10-squarepacker-k2-minus-c-upper.md`, section 5, “mpmath 1.4.1”; section 6, “Corollary 8.3 or 8.12” | No | The lock pins mpmath 1.3.0, the packets’ receipts record 1.3.0, this run used 1.3.0, and the register rows say 1.3.0; the review’s version is wrong. Version 1.1’s band-end corollary is 8.10 (8.3 is version 1.0’s number) | Append a dated correction section, as the review’s two existing corrections were added, with this text: “Section 5 says `cert3e.py` ran under mpmath 1.4.1; the project pins mpmath 1.3.0, which the receipts record and under which the covering was replayed again on 11 October with the recorded output. Section 6’s ‘Corollary 8.3 or 8.12’ reads ‘Corollary 8.10 or 8.12’ in version 1.1’s numbering. No finding, rung or verdict changes.” |
| F3-4 | `packing/frontier/asymptotic-waste-bounds.yaml`, line 424, the Theorem 1.2 row’s `complementary_case` | No | “Below 1.6*10^7 only Theorem 1.4 and the five certificates apply”: two of the five are at $k>1.6\cdot10^7$ | `Below 1.6*10^7 only Theorem 1.4 and the three certificates at k = 10^5, 10^6 and 10^7 apply.` |
| F3-5 | `asymptotic-waste-bounds.yaml`, `relevance_to_small_n`, line 549 | No | “asymptotic statements with unspecified or astronomically weak constants” no longer describes the file: Theorem 1.4 holds with the constant 8 at every $k\ge6$ and five packings are explicit. The conclusion, none at $n\le324$, stands, since the theorem is weaker than the atlas for $k\le18$ | Replace the first two sentences with: `None. The bounds on W(x) are asymptotic statements with unspecified or astronomically weak constants, describing behaviour as x -> infinity; the deficiency bounds are explicit from k = 6 but weaker than every atlas value for k <= 18 (deficiency_upper_bounds).` and keep the rest |
| F3-6 | `asymptotic-waste-bounds.yaml`, the 2026-10-05 row of `[squarepacker k2-minus-c 2026]`, `corollary`, last sentence | No | “c*(k) lies between order log k and O(k^{3/5})” was the record’s state on 5 October; true but silently weaker than `open_problem` and the cube-root row, which cite the reported $k^{3/8}$ rows | Append: ` As of 2026-10-05; the October 2026 upper bounds of order k^{3/8}, reported, are in deficiency_upper_bounds.` |
| F3-7 | `packing/cases/asymptotic/ryu_upper_replay.py`, `assemble`, line 146; the hosted release `data/squarepacker-k2-minus-c-upper-certificates-v1` | No | The release does not exist (`gh release view`: not found), so a fresh clone holds neither large certificate, and `assemble` copies them for every job, so `--only cert3e_160_64` stops with `HostedDataMissingError` before running anything; the packets’ receipts stand because the import lane had local copies | Publish the release (the owner); and in `assemble` copy a hosted certificate only when a selected job reads it, or catch `HostedDataMissingError` for files no selected job names and lower the manifest count check by the files skipped, so the coverings replay in a clone without the data |
| F3-8 | `results.yaml`, T-117 and T-125 `claim` (outside the batch, noticed in comparison) | No | “Complete exact replay confirms …” and “Complete independently reviewed exact replay confirms …” use the word in a form the checker’s regular expression does not read (`confirmed` only), and name no kind | T-117: `Complete exact replay, independently re-implemented, confirms …`; T-125: `Complete exact replay, independently re-implemented and reviewed, confirms …`, after checking each entry’s evidence relation; and widen the checker’s pattern so that it reads `confirms` as well as `confirmed` |

## For the Records Lane

- Apply F3-1 and F3-2 to `results.yaml`, F3-4 to F3-6 to `asymptotic-waste-bounds.yaml`,
  and append F3-3’s correction to the 10 October review; re-render `RESULTS.md` and the
  site after F3-1 and F3-2, since `scored` and the rationale print there.
- Map this document in `docs/project/document-map.yaml` as a non-superseded `review`
  (`role: review, authority: record, lifecycle: retained`). It is not listed in any
  entry’s `reviews`, because it moves no rung: it is a reviewing lane for significance
  and a second read of the preprint, and the entries’ V4/C4 still need the oversight
  record and a review each names.
- F3-7 is a tooling change and the owner’s release; F3-8 is outside the batch.

## What Was Not Checked

- The certificates at $k=3.825\cdot10^7$ and $10^8$, absent from this checkout; their
  decisions are the 2026-10-09 packet’s receipts (94 s and 244 s of wall there, with the
  six controls at $10^8$ refused).
- Ten of the twelve tier coverings and the regression of `cert_v3.py` on the row v1.0,
  which at 80 to 300 s per tier would exceed the CPU ceiling; the 2026-10-10 packet’s
  receipts record all 52 jobs matching, and tier C3 and `cert3e.py` were replayed here.
- The coverings, re-implementation and end packings the source reports and does not
  include; the exact tests under `code/zc_tests/` beyond what the packets replayed;
  Remarks 11.1–11.3; the literature claims of Section 10 beyond Roth and Vaughan.
- The two maintained exact routes and the third route behind T-128 to T-146, which lane
  F2 covers, and the lower-bound replays of T-132, T-133 and T-142 to T-145, which lane
  F1 covers.

## Verdicts

- **Scope 1, the deficiency bounds: accepted.** The register states exactly what is
  proved (Theorems 1.3, 1.4, 1.2 and the frame of 1.6, re-derived here), what the
  release certifies (one covering per tier, replayed with the producer’s code) and what
  is reported, and no statement in the file contradicts another; the cheap checkers
  decide what the 10 October review says and pass again.
- **Scope 2, grading: accepted.** Rungs, statuses and views agree with the checker;
  every score is confirmed at its value, and the `by` fields are brought to the rubric
  by F3-1.
- **Scope 3, the issues: accepted.** Every reported result maps to the right entry or to
  a recorded reason.
- **The limit.** One AI reviewer’s reading, of the same family as the author’s
  assistants and as the earlier reviewers; it is not a referee’s report, and nothing
  here raises any rung.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
