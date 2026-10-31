# Review: The Validation of Daniel’s Degree-7213 Minimal Polynomial of the s(29) Record Side

- **Date:** 31 October 2026
- **Reviewer:** Claude, strong sub-agent tier (lane L5 of the intake pass of 31 October,
  `bold-ritchie-l5`, for the pass’s coordinator; beads `think-10m1` and `think-6gti`)
- **Subject:** T-246, Evan Daniel’s report that the side of the best known packing of 29
  unit squares is a root of an irreducible integer polynomial p of degree 7213, from
  [`N29.md`](../../../packing/resources/web/evand-exact-and-local-reports-2026-10-12/source/search/exact/homotopy/N29.md)
  at evand/square-packing `ad86d42` and the release `exact-data-2026-10-12`
  (`s29-minpoly.tar.zst`, SHA-256 `708e1b8b…6f3729c`), retained in
  [`evand-exact-and-local-reports-2026-10-12`](../../../packing/resources/web/evand-exact-and-local-reports-2026-10-12/)
  and pinned by
  [`evand-exact-data-2026-10-12`](../../../packing/resources/web/evand-exact-data-2026-10-12/README.md);
  and the validation that draft PR #817 ran for it on 25 October 2026 under issue #816
- **Verdict:** accepted, with one Monte Carlo step.
  Every step of the argument but one is decided here deterministically, two of them by
  code independent of the source’s. The one left is the pair of identity families that
  tie the side of the packing to p, and they still rest on random-prime checks.
  No finding is blocking.
- **Code:** the tools and receipts of #817:
  [`devtools/evand_s29_replay.py`](../../../packing/devtools/evand_s29_replay.py),
  [`devtools/check_exact_side_minpoly.py`](../../../packing/devtools/check_exact_side_minpoly.py),
  [`devtools/check_exact_side_packing.py`](../../../packing/devtools/check_exact_side_packing.py),
  and
  [`receipts/validation-2026-10-25/`](../../../packing/resources/web/evand-exact-data-2026-10-12/receipts/validation-2026-10-25/)
  in the exact-data packet

## The Claim and Its Chain

N29.md’s conclusion is that the side of the record configuration, $\sigma \approx
5.933833462676929189689460616352\ldots$, is a root of the irreducible integer polynomial
p, so p is its minimal polynomial.
The chain it gives, read here against `link.py`, `verify_mod.py`, `contacts_mod.py`,
`irred.py` and `krawczyk.py` at `ad86d42`:

1. The record’s 152-row contact system, in 55 unknowns, is eliminated to five
   consistency polynomials $F_1, \ldots, F_5$ in the half-angle tangents
   $t_1, \ldots, t_5$ of its five tilted orientation classes, with the side
   $S = S_n / S_d$ a rational function of $t_3, t_4$.
2. A Krawczyk box of radius $10^{-50}$ holds exactly one zero $t^*$ of F.
3. p is irreducible over $\mathbb{Q}$.
4. A shape-lemma parametrization $\tau_i(x) = g_i(x) / (d_i\,p'(x))$, rebuilt
   numerically from all 7213 roots, satisfies $F_k(\tau) = 0$ and
   $S_n(\tau) = x\,S_d(\tau)$ in $\mathbb{Q}[x]/(p)$, and the full contact system is
   consistent at $\tau$ with every unknown determined.
5. p has a root $\sigma$ on an interval $I$ of radius $10^{-38000}$, where $p'$ has no
   zero, $\tau(I)$ lies inside the Krawczyk box and $S_d$ has no zero on the box.

Given 4, $\tau(\sigma)$ is a zero of F in the box, so it is $t^*$ by 2, and
$S(t^*) = \sigma$. That inference is sound.
Its only probabilistic input is step 4, which the source checks modulo 50 and 21 random
62-bit primes and rates Monte Carlo.
Steps 2, 3 and 5 are rated rigorous, and the source leaves open whether the
configuration at $t^*$ is a packing at all.

## What the Validation Decided

| Step | How it was decided | Relation to the source’s code | Verdict |
| --- | --- | --- | --- |
| The inputs | The release asset held to its pinned SHA-256 and all 21 members to the sizes and digests `acquisition/release.json` records | premise check | held |
| 2. Krawczyk | `krawczyk.py` again (unique zero), and independently `sqpack.promote.krawczyk.certify` on the same system, which contracts the box to $2 \times 10^{-2618}$ | same implementation, then independent | decided |
| 3. Irreducibility | `irred.py` again over its 12 primes near $2^{61}$, and independently distinct-degree factorization modulo the five primes 40009, 40013, 40031, 40037 and 40039 (gmpy2 and numpy, no FLINT), after which no proper factor degree is possible; a reducible control, $p\,(x+1)$, is not proven irreducible | same implementation, then independent | decided |
| 5. The root | `link.py` again at `PREC=220000` (LINKED), and independently: p has exactly one root in the hull $S_{\mathrm{mid}} \pm 2 \times 10^{-48}$, by a sign change on dyadic points and $p'$ bounded away from zero on the hull, in exact integer arithmetic | same implementation, then independent | decided |
| 4. The identities | `verify_mod.py` modulo 10 fresh random primes (two runs of 5) and `contacts_mod.py` modulo 21; a control with one coefficient of p changed fails all three scripts | same implementation | **Monte Carlo** |
| The packing at $t^*$ | `check_exact_side_packing`: the configuration at the zero is solved over the box in interval arithmetic; 359 of 406 pairs and 97 of 116 square-wall constraints strictly separated, and each of the 66 touching constraints shown to be a contact row; the 11 rows off the solved basis vanish at $t^*$ by exact elimination over $\mathbb{Q}(t)$, each numerator divisible by one $F_k$ | first-party, new; the source does not check it | decided |
| Against T-195 | p is negative at T-195’s exact rational and decreasing on the hull, and an 812-place bracket puts $\sigma$ below it by $3.90143354777 \times 10^{-799}$; the side $S^*$ at $t^*$, from the box contracted to $2 \times 10^{-2618}$, lies below it by the same amount | first-party | decided |

The independent programs are this repository’s own and were written after their authors
had read the source’s scripts, so the relation for what they decide is *independently
re-implemented after reading the producer’s code, by a Claude agent, a system family the
producer also used* (N29.md’s source names Claude as its author under Daniel’s
direction).

## Findings

### F-1 (major, for the record): the identities are still Monte Carlo

Without step 4 the chain does not close: $\sigma$ and $S^*$ agree to about 810 places,
deterministically, and each is pinned in an interval that holds only one of its kind,
but nothing deterministic says they are equal.
The error the source states, below $10^{-400}$ for 50 primes, assumes a height bound of
about $10^{10}$ digits on the integer a false identity would have to divide, which it
gives as a heuristic, not a proof.
Under the same assumption the ten fresh primes here leave an error below about
$10^{-80}$. The record’s evidence methods have no Monte Carlo kind, so the replay of
step 4 cannot be entered as `exact-algebraic` without overstating it.
The deterministic routes are priced on #817: an exact build of each cleared numerator in
$\mathbb{Z}[x]$ with a divisibility test by p, about 23 CPU-hours and 0.61 GB for the
sample identity $S_n = x\,S_d$ and about 717 CPU-hours, up to 11.8 GB, for all six; or a
modular route against an explicit resultant bound, about 25 and 111 million primes.

### F-2 (major, for the owner): a deterministic upper bound below T-195

The packing decision makes $S^* = S(t^*)$, the side at the unique zero of F in the box,
a decided upper bound: s(29) ≤ S*, with no Monte Carlo step, and $S^* < $ T-195’s exact
rational by $3.9 \times 10^{-799}$. It is an algebraic number given by a polynomial
system and an isolating box, not yet by p, and it is a re-solution of the same packing
at its exact side, not a new arrangement.
Whether to register it, and whether to re-kind T-246 from `exact-side` to an upper
bound, are the owner’s decisions (#816).

### F-3 (minor): N29.md writes s(29) for the record side

N29.md’s first line says “s(29) = 5.93383…”. It is the side of the best known packing,
an upper bound, and T-246’s claim already says so; replies on #545 and #816 should too.

### F-4 (minor): verify_mod.py ran over 10 primes, not 50

The 50 the source’s README prescribes would have cost about 4.6 CPU-hours here, above
the owner’s cap of 25 October for the item (5 CPU-hours).
The replay is complete for every other script.

### N-1 (note): the free squares

The two squares the contact system does not constrain (`free-20` and `free-21` in
`nonoverlap.json`) are placed at T-195’s exact poses, shifted by
$(-1/1000000, -1/1000000)$ and $(-1/5000, -1/10000)$, and every pair and wall they enter
is strictly separated; the least margin of the whole check, $5.8 \times 10^{-7}$, is
between square 18 and `free-20`. A reader checking the decision should know that their
poses are chosen, not derived: any pose that separates would do, since they are free.

## Rungs

**C1, read**, on T-246’s report entry (`E-n029-evand-minpoly-7213-report`): this review
as its `external_review`, `informally-verified`. Not C3: the same-implementation replay
of all five steps passed, but its load-bearing identity step is Monte Carlo (F-1), and
the independent runs decide every step but that one.
V stays V0 for the same reason.
The rungs move to C3 and V3 once the identities are decided deterministically, or once
the owner rules that a Monte Carlo identity check with a stated error may stand for one.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **`verifiers.yaml`:** register `check_exact_side_minpoly` and
  `check_exact_side_packing` (both decide, first-party, with their independence records)
  and `evand_s29_replay` (premises; it runs the source’s scripts).
- **`evidence.yaml`:** a replay entry (`same-implementation`, `replayed-here`) for the
  five-step replay, with coverage naming the 10 of the source’s 50 `verify_mod` primes;
  an entry for each independent decision (irreducibility, isolation, Krawczyk, the
  packing at $t^*$, the comparison with T-195), cited by n-029.md and not by T-246; and
  this document as `external_review` on the report entry.
- **`results.yaml`:** T-246 to C1, its `reviews` gaining this document
  (`kind: adversarial`, `reviewer_kind: ai`, `relation: project`, `verdict: accepted`),
  its `next_rung` and `unfinished_confirmations` naming the deterministic identities and
  their price, and the replay item marked run.
- **The owner:** F-2, whether to register s(29) ≤ S* and re-kind T-246.

## What This Review Does Not Establish

It does not decide the identities of step 4, re-derive the elimination from the 152-row
system to the five $F_k$ by hand, or check the homotopy solve, which only produced the
roots p was rebuilt from and which nothing in the chain relies on once p is given.
It establishes no lower bound and no optimality.

## Independence and Disclosure

- **Read before these findings:** the brief; #817’s description and its receipts;
  T-246’s register entry; N29.md and the five scripts named above at `ad86d42`; the
  docstrings of #817’s three tools.
- **Not run by this review:** anything.
  The verdicts above are the receipts’ of 25 October, read here; this review’s own
  contribution is the reading of the chain and the findings.
- **Shared system family:** the reviewer is a Claude agent, the validation’s tools were
  written by Claude agents, and the source’s work is credited to Claude under Daniel’s
  direction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
