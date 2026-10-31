# Review: The Validation of Daniel’s Degree-7213 Minimal Polynomial of the s(29) Record Side

- **Date:** 31 October 2026 (round 2 the same day, after review A of #817)
- **Reviewer:** Claude, strong sub-agent tier (lane L5 of the intake pass of 31 October,
  `bold-ritchie-l5`, for the pass’s coordinator; beads `think-10m1` and `think-6gti`);
  the brief named no reasoning setting
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
  Every step of the argument but one is decided here deterministically, three of them
  (the Krawczyk zero, irreducibility and the root) also by code independent of the
  source’s. The one left is the pair of identity families that tie the side of the
  packing to p, and they still rest on random-prime checks.
  No finding is blocking.
- **Code:** the tools and receipts of #817:
  [`devtools/evand_s29_replay.py`](../../../packing/devtools/evand_s29_replay.py),
  [`devtools/check_exact_side_minpoly.py`](../../../packing/devtools/check_exact_side_minpoly.py),
  [`devtools/check_exact_side_packing.py`](../../../packing/devtools/check_exact_side_packing.py),
  and
  [`receipts/validation-2026-10-25/`](../../../packing/resources/web/evand-exact-data-2026-10-12/receipts/validation-2026-10-25/)
  in the exact-data packet, whose README gives each receipt’s command

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
Its only probabilistic input is step 4, which the source checks modulo random 62-bit
primes and rates Monte Carlo.
Steps 2, 3 and 5 are rated rigorous, and the source leaves open whether the
configuration at $t^*$ is a packing at all.

Step 1 is not load-bearing for anything this review accepts: the packing check below
shows every one of the 152 rows holding at $t^*$ directly (the 55 basis rows by the
interval solve, the other rows by exact elimination over $\mathbb{Q}(t)$), so a wrong
elimination could not make $S^*$ the side of a false packing.
It bears only on whether $t^*$ is the record configuration’s zero, which the matching of
every square to T-195’s witness, to $4.5 \times 10^{-71}$, settles.

## What the Validation Decided

| Step | How it was decided | Relation to the source’s code | Verdict |
| --- | --- | --- | --- |
| The inputs | The release asset held to its pinned SHA-256 and all 21 members to the sizes and digests `acquisition/release.json` records | premise check | held |
| 2. Krawczyk | `krawczyk.py` again (unique zero), and independently `sqpack.promote.krawczyk.certify` on the same system, which contracts the box to $2 \times 10^{-2618}$ | same implementation, then independent | decided |
| 3. Irreducibility | `irred.py` again over its 12 primes near $2^{61}$, and independently distinct-degree factorization modulo the five primes 40009, 40013, 40031, 40037 and 40039 (gmpy2 and numpy, no FLINT), after which no proper factor degree is possible; a reducible control, $p\,(x+1)$, is not proven irreducible | same implementation, then independent | decided |
| 5. The root | `link.py` again at `PREC=220000` (LINKED), and independently: p has exactly one root in the hull $S_{\mathrm{mid}} \pm 2 \times 10^{-48}$, by a sign change on dyadic points and $p'$ bounded away from zero on the hull, in exact integer arithmetic | same implementation, then independent | decided |
| 4. The identities | `verify_mod.py` modulo 10 fresh random primes (two runs of 5) and `contacts_mod.py` modulo 21; a control with one coefficient of p changed fails all three scripts | same implementation | **Monte Carlo** |
| The packing at $t^*$ | `check_exact_side_packing`: the configuration at the zero is solved over the box in interval arithmetic; 359 of 406 pairs and 97 of 116 square-wall constraints strictly separated, and each of the 66 touching constraints shown to be a contact row through a factor with no pole in the box. All 16 distinct rows off the solved basis, and the rows’ side against $S_n/S_d$, are decided at $t^*$ by exact elimination over $\mathbb{Q}(t)$: of the 11 the touching constraints use, 6 have a numerator divisible by an $F_k$ and 5 vanish identically | first-party, new; the source does not check it | decided |
| Against T-195 | p is negative at T-195’s exact rational and decreasing on the hull, and an 812-place bracket puts $\sigma$ below it by $3.90143354777 \times 10^{-799}$; the side $S^*$ at $t^*$, from the box contracted to $2 \times 10^{-2618}$, lies below it by the same amount | first-party | decided |

Round 2 re-ran the packing decision with the checker as fixed after review A (its
verdict now requires the elimination’s decisions, A1 of that review, and refuses a
contact factor or row coefficient with a pole in the box, A13), and regenerated the
comparison with T-195, the isolation and the price by their tools.
Each decision is unchanged.

The independent programs are this repository’s own and were written after their authors
had read the source’s scripts, so the relation for what they decide is *independently
re-implemented after reading the producer’s code, by a Claude agent, a system family the
producer also used* (N29.md’s source names Claude as its author under Daniel’s
direction).

**Trust boundaries.** `check_exact_side_packing` trusts mpmath’s interval arithmetic for
the enclosures and the strict separations, sympy’s rational-function field for the
elimination, and `sqpack.promote.krawczyk` for the re-certified box; its parser reads
the source’s exported system by a grammar and executes none of it.
`check_exact_side_minpoly` trusts gmpy2’s integers, numpy’s float64 arithmetic below
$2^{53}$ in the Frobenius steps, and Python’s `Fraction`; it imports `parse_system` from
the packing checker for the price, so the two share their reading of the system file.
Both, and the source’s scripts, use sympy, so a sympy fault in parsing polynomials could
reach the source’s identity checks and this repository’s elimination alike; the
irreducibility and isolation share none of it.
The replay trusts the author’s pinned python-flint 0.9.0 and mpmath 1.3.0.

## Findings

### F-1 (major, for the record): the identities are still Monte Carlo

Without step 4 the chain does not close: $\sigma$ and $S^*$ agree to about 810 places,
deterministically, and each is pinned in an interval that holds only one of its kind,
but nothing deterministic says they are equal.

The error can now be bounded rigorously, by this repository’s own resultant bound.
`check_exact_side_minpoly price` bounds, for each identity, the integer a false identity
would have to be divisible by: since p is irreducible (decided), the resultant of p and
the cleared numerator H is nonzero unless p divides H, and its Hadamard bound leaves at
most 111,197,409 primes above $2^{61}$ that could hide a false identity for the worst
one ($F_1$), and 25,351,013 for $S_n = x\,S_d$. `verify_mod.py` draws its primes
uniformly from the roughly $5.40 \times 10^{16}$ primes in $[2^{61}, 2^{62})$ by
rejection. Ten independent uniform primes then miss a false identity with probability at
most $(2.06 \times 10^{-9})^{10} \approx 1.4 \times 10^{-87}$ per identity, and the
source’s 48 with at most about $10^{-417}$. That bound treats the Mersenne Twister’s
outputs as independent uniform draws: the ten primes here come from two 32-bit seeds
(`evand_s29_replay.py`), so 64 bits of entropy were actually drawn, and no bound below
$2^{-64} \approx 5.4 \times 10^{-20}$ follows without that assumption.
The source has the same property.
The record’s evidence methods have no Monte Carlo kind, so the replay of step 4 cannot
be entered as `exact-algebraic` for T-246’s claim without overstating it.

The deterministic routes, priced by
[`price.json`](../../../packing/resources/web/evand-exact-data-2026-10-12/receipts/validation-2026-10-25/price.json),
the tool’s run on the machine it names:
- **Exact division.** Build each cleared numerator H in $\mathbb{Z}[x]$ and divide by p
  exactly: 6.6 CPU-hours and 0.61 GB for the sample identity $S_n = x\,S_d$, and 436.8
  CPU-hours, up to 11.8 GB, for all six, on a four-core x86-64 cloud container at a load
  of 3 to 7 (the receipt names it).
  The model prices schoolbook exact division of an H already built,
  $(\deg H - n + 1)(n + 1)$ products, at a multiplication time measured by wall clock on
  the host, so it moves with the host and its load: the same tool gave 23 and 717
  CPU-hours on 25 October and 6.2 and 486.6 for review A’s run.
  It does not price building H (about 5,073 terms, each a product of up to 26
  polynomials of degree at most 7212), and it ignores quasi-linear exact division by
  Kronecker substitution, which the module already uses for the factorizations, so the
  true cost could be well above or below these figures.
- **Modular.** Check every prime the resultant bound leaves: 111 million primes at the
  measured 286 CPU-seconds a prime for all six identities, about 8.8 million CPU-hours,
  and 25 million for the sample identity alone.

Neither is funded; the exact route should be priced again with H’s construction before
it is put to the owner.

### F-2 (major, for the owner): a deterministic upper bound below T-195, and T-246’s kind

The packing decision makes $S^* = S(t^*)$, the side at the unique zero of F in the box,
a decided upper bound: s(29) ≤ S*, with no Monte Carlo step, and $S^* < $ T-195’s exact
rational by $3.9 \times 10^{-799}$. It is an algebraic number given by a polynomial
system and an isolating box, not yet by p, and it is a re-solution of the same packing
at its exact side, not a new arrangement.
That is a separate claim from T-246’s: by
[epistemics.md’s first kind rule](../../../epistemics.md#result-kinds) it is an upper
bound, and whether to register it, and whether to move n = 29’s lanes, are the owner’s
decisions (#816).

T-246 stays `exact-side`. The kind rule makes an exact side an upper bound once the
packing is decided at the side the claim states; T-246 states $\sigma$, the root of p,
and the packing is decided at $S^*$. $S^* = \sigma$ is exactly the Monte Carlo step, so
T-246 cannot be re-kinded before F-1 is closed.

### F-3 (minor): N29.md writes s(29) for the record side

N29.md’s first line says “s(29) = 5.93383…”. It is the side of the best known packing,
an upper bound, and T-246’s claim already says so; replies on #545 and #816 should too.

### F-4 (minor): verify_mod.py ran over 10 primes here, not 50

The 50 the source’s README prescribes would have cost about 4.6 CPU-hours here, above
the owner’s cap of 25 October for the item (5 CPU-hours).
The replay is complete for every other script.

### F-5 (minor, for the author): the source’s logs record 48 and 20 primes, not 50 and 21

N29.md and the archive’s README say `verify_mod.py` ran over 50 primes and
`contacts_mod.py` over 21. The archive’s logs record six runs of eight,
`n29_vmod_11.log` to `n29_vmod_16.log`, each ending “all identities hold modulo 8 random
62-bit primes”, so 48; and `n29_cmod.log` ends “contact system consistent with S = x
modulo 20 random 62-bit primes”.

### F-6 (minor, for the author): the elimination’s program is not in the archive

`export_system.py` turns `minpoly.py`’s elimination into the five $F_k$, and the archive
holds the exported `n29_system.jl` but not `minpoly.py`. Step 1 is not load-bearing for
what is accepted here (above), but the elimination cannot be re-run from what is
published.

### N-1 (note): the free squares

The two squares the contact system does not constrain (`free-20` and `free-21` in
`nonoverlap.json`) are placed at T-195’s exact poses, shifted by
$(-1/1000000, -1/1000000)$ and $(-1/5000, -1/10000)$, and every pair and wall they enter
is strictly separated; the least margin of the whole check, $5.8 \times 10^{-7}$, is
between square 18 and `free-20`. A reader checking the decision should know that their
poses are chosen, not derived: any pose that separates would do, since they are free.

## Questions for the Author

1. Were 48 primes, not 50, and 20, not 21, the runs N29.md reports (F-5)?
2. Could `minpoly.py` and the elimination’s inputs be published, so step 1 can be re-run
   (F-6)?
3. Would the identity checks draw their primes from more than a 32-bit seed in a later
   run, so the error bound does not rest on the generator (F-1)?

## Rungs

**C1, read**, on T-246’s report entry (`E-n029-evand-minpoly-7213-report`): this review
as its `external_review`, `informally-verified`. Not C3: the same-implementation replay
of all five steps passed, but its load-bearing identity step is Monte Carlo (F-1), and
the independent runs decide every step but that one.
V stays V0 for the same reason; a modular identity check is not a numerical method with
recorded precision, so V1 does not apply either.
The rungs move to C3 and V3 once the identities are decided deterministically, or once
the owner rules that a Monte Carlo identity check with a stated error may stand for one.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **`verifiers.yaml`:** register `check_exact_side_minpoly` and
  `check_exact_side_packing` (both decide, first-party, with their independence records)
  and `evand_s29_replay` (premises; it runs the source’s scripts).
- **`evidence.yaml`:** the modular run as what it decides and no more: an
  `exact-algebraic`, `verified` entry for “the six identities hold modulo these ten
  primes” (and one for `contacts_mod.py`’s 21), cited by n-029.md and never by T-246,
  with F-1’s bound and its 64-bit seed caveat in `limitations`, so that no later run of
  more primes can make it derive C3 for T-246; an entry for each independent decision
  (irreducibility, isolation, Krawczyk, the packing at $t^*$, the comparison with
  T-195), cited by n-029.md and not by T-246; and this document as `external_review` on
  the report entry.
- **`results.yaml`:** T-246 to C1, its `reviews` gaining this document
  (`kind: confirming`, `reviewer_kind: ai`, `relation: project`, `verdict: accepted`;
  not adversarial, since the reviewer read the validation’s description and receipts
  first and ran only the tools’ regenerations).
  Its `next_rung` and its replay item on `main` say the source’s five-step replay earns
  C3; that was an overstatement, since two of its steps are not exact checks of the
  claim. Replace the item with one for the deterministic identities (F-1’s routes and
  price, rung C3), and its `composition` names the identity step as the part that sets
  V0 and C1.
- **The owner:** F-2, whether to register s(29) ≤ S* as an upper bound and move n = 29’s
  lanes; T-246 itself stays `exact-side` until F-1 is closed.

## What This Review Does Not Establish

It does not decide the identities of step 4, re-derive the elimination from the 152-row
system to the five $F_k$ by hand, or check the homotopy solve, which only produced the
roots p was rebuilt from and which nothing in the chain relies on once p is given.
It establishes no lower bound and no optimality.

## Independence and Disclosure

- **Read before these findings:** the brief; #817’s description and its receipts;
  T-246’s register entry; N29.md and the five scripts named above at `ad86d42`; the
  docstrings of #817’s three tools; for round 2, review A of #817 and its reviewer’s
  outputs.
- **Run by this review:** in round 1, nothing; the verdicts were the receipts’ of 25
  October. In round 2, the tools’ regenerations from the pinned asset, re-fetched and
  held to its digest: the packing decision with the fixed checker (31.7 CPU-s), the root
  isolation without the withdrawn comparison, the 812-place comparison with T-195, and
  the price; each receipt’s command is in the packet README.
- **Shared system family:** the reviewer is a Claude agent, the validation’s tools were
  written by Claude agents, and the source’s work is credited to Claude under Daniel’s
  direction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
