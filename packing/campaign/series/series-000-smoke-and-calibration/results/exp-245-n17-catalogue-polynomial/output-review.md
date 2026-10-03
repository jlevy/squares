# H265 Catalogue Polynomial Identity: Independent Output Review

Reviewed on 2026-10-02 after the single target run at frozen commit
`603d5cb36ed3c9195513956cd5b5c20e5f2cddda`. The retained receipt satisfies
[H265’s acceptance criterion](../../../../hypotheses/H-265-n17-catalogue-polynomial-identity.md):
the one factor of the side resultant that vanishes at the certified H255 root equals the
degree-18 polynomial recorded in `packing/frontier/n-017.md` with rational unit **1**,
that polynomial is irreducible over $\mathbb{Q}$, and an independent recomputation in
this review agrees on every count.
There is no mathematical, input-binding, receipt, or resource blocker to acceptance.
The coordinator owns the recorded verdict.

This review read the frozen tool and its 24 tests, the exp-237 certificate and checker
it binds, the W3 review that defines $\Pi_2$, $\Pi_3$ and $S(t)$, and the run receipt.
It then recomputed the result in its own code, which imports nothing from the tool:
[`recheck.py.txt`](audit/recheck.py.txt) and
[`primes_and_digits.py.txt`](audit/primes_and_digits.py.txt), with their outputs,
retained under [`audit/`](audit/) with a `.txt` suffix as earlier independent reviews
were.

## Inputs and Binding

The tool reads $\Pi_2$ and $\Pi_3$ from the certificate’s `[t_power, b_power, c]` terms,
the convention the exp-237 producer serialises with `midpoint[0]` as $t$, and refuses
them unless they equal its own sympy rebuild of the W3 formulas.
My separate transcription of those formulas equals both.
The certificate is accepted only with its schema, `criterion_passed`, empty failures,
the checker’s `verification_passed`, and the checker’s $q$ and inclusion bounds equal to
the certificate’s. The receipt binds the certificate, checker, `n-017.md` and the module
by SHA-256; all four match the working tree at the frozen commit.
The $t$-box is the certificate midpoint $\pm10^{-12}$, inside $[0.36,0.37]$. My own
parse of the catalogue string gives the same nineteen coefficients, content 1 and
leading coefficient $4775=5^2\cdot191$.

## Soundness of Each Step

**The map to the side.** $S'=4(t^2+3t-2)/K^2$ with $K=1+2t-t^2$. The tool requires $K>0$
and $t^2+3t-2<0$ at both endpoints; $K$ is concave and the numerator convex, so both
hold across the box and $S$ is strictly decreasing.
Rounding is floor and ceiling at thirty digits, so the interval is outward.
The exact image $[S(t_{hi}),S(t_{lo})]$ has width $2.47\times10^{-12}$ and sits inside
the tool’s interval with slack $7.4\times10^{-31}$ and $5.0\times10^{-31}$.

**The primary route.** A resultant lies in the ideal of its inputs, so
$\operatorname{res}_b(\Pi_2,\Pi_3)$ vanishes at $(t^*,b^*)$ and
$\operatorname{res}_t(R,G)$ at $(t^*,S^*)$, with no leading-coefficient caveat.
The carrying-factor rule, the endpoint check, and the unit ratio are implemented as
stated. `factor_list` normalises each factor to a positive leading coefficient; the raw
$\operatorname{res}_t(R_{18},G)$ is $-C$, which is the same identification up to a unit.

**Rabin’s test.** The reduction is made monic after refusing $p\mid4775$, so the degree
is kept; $x^{p^k}$ is built by iterated $p$-th powers modulo $f$; the test checks
$x^{p^{18}}\equiv x$ and $\gcd(f,x^{p^{18/q}}-x)=1$ for $q\in\{2,3\}$ from
`_prime_divisors(18)`, with Euclid normalising each divisor to monic before reduction.
That is Rabin’s criterion, implemented correctly, with controls for $x^2+1$, a product
of two cubics modulo 2, and $x^4+1$. Primes 2 and 3 fail, 5 is skipped, 7 certifies.
Irreducibility modulo 7 with degree preserved gives irreducibility over $\mathbb{Q}$.

**The second route and the cofactor.** Eliminating $t$ first gives degree 60; the
catalogue polynomial divides it exactly once; the degree-42 cofactor is excluded by the
Taylor bound $|H(c)|>\sum_{k\ge1}|h_k|r^k$, which is rigorous, and `count_roots` is a
Sturm count. Nothing in either route is vacuous: the toy chart with hand-derived side
polynomial $S^2-2S-12$, three perturbed catalogues, a rootless box, and a swapped
formula pair are all refused where they should be.

## Independent Recomputation

All of the following were computed in this review’s own code with exact arithmetic.

| Check | Result |
| --- | --- |
| $C$ at exact image endpoints | $C(s_{lo})\approx-2.88\times10^{-2}$, $C(s_{hi})\approx+2.88\times10^{-2}$ |
| Own Sturm chain (length 19, squarefree) | one root in $(s_{lo},s_{hi}]$; four real roots in all |
| Descartes on $(1+x)^{18}C\bigl(\tfrac{s_{lo}+s_{hi}x}{1+x}\bigr)$ | one sign variation, so exactly one root |
| sympy `factor_list` over $\mathbb{Q}$ | one factor, degree 18 |
| Degree patterns modulo primes $<80$ | only 7 gives $[18]$; e.g. 3: $[5,13]$, 11: $[6,12]$, 13: $[2,2,3,4,7]$ |
| Certifying primes below 1000 | 7, 103, 167, 173, 359, 419, 509, 743, 769, 883 |
| Own distinct-degree test | irreducible at 7, 103, 167, 173; refuses $x^2+1$ mod 5 and $C$ mod 2 |
| $\operatorname{res}_b(\Pi_2,\Pi_3)$ | degree 28: $t^2(t-1)^2(t+1)^2(t^2+1)^2R_{18}$; only $R_{18}$ has a root in the box |
| $\operatorname{res}_t(R,G)$ | $(S-6)^2(S-5)^2(S+1)^2(2S^2-10S+13)^2C$; only $C$ has a root in the interval |
| Second route | degree 60; $C$ divides once; cofactor degree 42 has Sturm count 0 on the interval |

The cofactor count by Sturm is a different exclusion from the tool’s Taylor bound.
The receipt’s enclosure gives $S^*=4.6755300936045509516341112704831466487671\ldots$ to
width $10^{-40}$. The registered rational ceiling $4.6755300936045509516342148538535054$
exceeds it by $1.04\times10^{-22}$ and has $C>0$, consistent with its status as a
ceiling rather than an identity, and the catalogue’s printed $4.67553009360455$ agrees
to every digit.

## Execution

[run-001](run-001/command.txt) ran in a detached worktree at the frozen commit with a
clean tracked tree, exited 0, and took 0.745 seconds real and 0.688 user under Python
3.14.7. `stdout.log` and [receipt.json](run-001/receipt.json) are byte-identical,
SHA-256 `b11169edf0633d8ca8f17829b48cde73ccc8ba0abdd51a8e10d8c7bf9d91d948`, and the
receipt equals the lane’s pre-run receipt exactly.
The tool’s 24 tests pass in about one second.

## Criterion and Scope

All three clauses hold: the vanishing factor equals the catalogue polynomial with unit
1; irreducibility is certified by factorization and by Rabin at $p=7$, and here again at
three further primes; and the tool’s second route and this review’s separate route
agree. The result identifies the side of the certified H255 chart root as an algebraic
number of degree 18. It is not a packing, feasibility, rigidity or optimality claim, it
leaves the admitted rational ceiling and the open status of $s(17)$ unchanged, and the
catalogue’s own derivation of the polynomial remains unreviewed source material.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
