# {{TITLE}}

{{OPENING_CLAIM}}

This document carries every executable input for that claim.
It embeds one standard-library verifier and the exact certificate bytes.
{{LIMIT_INPUT_SENTENCE}}
Save this Markdown file.
Then copy the `python` block under “Verifier” into `verify_claim.py` and run the command
below with CPython 3.12 or later:

```bash
python verify_claim.py {{FILE_NAME}}
```

The verifier reads the marked JSON blocks from this document.
It prints `VERIFIED` and exits with status 0 only after recomputing the certificate’s
closed-form conditions and its full event-cell sweep.
{{LIMIT_DECISION_SENTENCE}}

Certificate SHA-256: `{{CERT_SHA256}}`; bytes: `{{CERT_BYTES}}`.
{{LIMIT_IDENTITY_LINE}}

## Definitions and Finite Certificate Theorem

Let $s(n)$ be the infimum of the side lengths of squares that contain $n$ unit squares
with pairwise disjoint interiors; rotations are allowed.
Fix positive integers $n$ and $K$, positive rational numbers $L$ and $B$, and a rational
number $T$ with $0<T<1$. Put $Q=[0,L]^2$ and $t_k=T k/K$ for $k=0,\ldots,K$. Parameter
$t_k$ represents the direction $2\arctan(t_k)$.

A **point atom** $(p,w)$ assigns weight $w\geq0$ to a closed $B$-square $P$ when
$p\in P$. A **threshold atom** $(S,k,w)$ consists of a finite set $S$ of distinct
points, an integer $1\leq k\leq |S|$, and a weight $w\geq0$; it assigns weight $w$ to
$P$ when $|P\cap S|\geq k$. The **charge** of $P$ is the sum of all weights assigned to
it by these two rules.
A point atom has budget $w$. A threshold atom has budget $w\lfloor |S|/k\rfloor$. The
certificate’s total budget is the sum of those budgets.

The eight symmetries of $Q$ form the group D4. A point-atom family is D4-invariant when
each image point has the same weight.
A threshold-atom family is D4-invariant when each image $(gS,k)$ occurs with the same
weight.

Define

$$
D=\max_{0\leq j<K}\frac{t_{j+1}-t_j}{1+t_jt_{j+1}}.
$$

The following five conditions prove $s(n)\geq L$:

1. the point atoms are D4-invariant;
2. the threshold atoms are D4-invariant;
3. the total budget is strictly below $n$;
4. $T^2+2T-1\geq0$ and $B(1+D)<1$;
5. every closed side-$B$ square at a net direction that lies in $Q$ has charge at least
   one.

For the proof, suppose $n$ unit squares with disjoint interiors fit in $Q$. Consider
each packed square $U$ separately, and represent its direction modulo $\pi/2$ in
$[0,\pi/2)$. If that direction exceeds $\pi/4$, let $g$ be the diagonal reflection;
otherwise let $g$ be the identity.
The angle condition places $g(U)$ in the net’s covered arc.
Choose the nearer net direction.
If its mismatch is $d$, then $\tan d\leq D$, and a concentric closed side-$B$ square has
half-width across either edge normal at most $B(1+D)/2<1/2$. It lies strictly inside
$g(U)$. Pull that core back by $g^{-1}$. D4 invariance preserves its charge, and
Condition 5 makes the resulting core inside $U$ have charge at least one.

The cores are closed subsets of the interiors of the packed unit squares, so they are
pairwise disjoint. Each point atom assigns its weight to at most one core.
For a threshold atom $(S,k,w)$, traces of disjoint cores on $S$ are disjoint.
If $r$ cores meet its threshold, then $rk\leq|S|$, hence $r\leq\lfloor|S|/k\rfloor$.
Summing the charges gives

$$
n\leq\sum_i \operatorname{charge}(P_i)
\leq \text{total budget}<n,
$$

a contradiction.

## Why the Exact Sweep Is Finite

At a fixed net direction, rotate coordinates with the core.
The centers of cores that contain a point $p$ form a closed axis-parallel square $R_p$
of side $B$. The edges of all $R_p$, together with the extreme coordinates of the
admissible-center domain, cut the plane into finitely many open cells.
Every point-membership trace is constant on a cell.
On a boundary, a closed core contains every point contained throughout any adjacent
cell, so its charge cannot be smaller.
Every admissible center is in the closure of a cell meeting the domain.
The minimum charge is therefore attained on an open event cell.

For a threshold atom with $m=|P\cap S|$, the verifier uses the exact identity

$$
[m\geq k]=\sum_{j=k}^{|S|}(-1)^{j-k}
\binom{j-1}{k-1}\binom{m}{j}.
$$

Each $j$-subset contributes on the intersection of its $R_p$ rectangles.
The verifier adds those signed rectangle terms with a range-add/range-min tree, sweeps
one slab at a time, and checks its least-cell witness by direct membership counting.
It rejects a certificate if any net direction’s admissible-center domain lacks interior;
both retained inputs satisfy this restriction.
The signs only implement the displayed identity; every certificate weight is
nonnegative.

## This Certificate

{{CERTIFICATE_FACTS}}

{{CLAIM_DERIVATION}}

## Evidence and Scope

{{EVIDENCE}}

The verifier is an additional standard-library implementation of the exact event-cell
decision. It uses the same certificate and theorem.
The retained exact sweep and interval branch-and-bound remain separate repository
decisions. {{SCOPE}}

## Verifier

The following block is byte-for-byte [`verify_claim.py`]({{VERIFIER_URL}}), SHA-256
`{{VERIFIER_SHA256}}`.

```python
{{VERIFIER_SOURCE}}
```

## Certificate

The marked block is byte-for-byte [`{{CERT_NAME}}`]({{CERT_URL}}).

<!-- BEGIN THRESHOLD CERTIFICATE -->
```json
{{CERTIFICATE_JSON}}
```
<!-- END THRESHOLD CERTIFICATE -->

{{LIMIT_RECORD_BLOCK}}

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
