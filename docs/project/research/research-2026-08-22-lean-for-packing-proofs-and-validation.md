# Research: Lean for Square-Packing Proofs and Validation

**Date:** 2026-08-22 (local proof status reconciled 2026-09-06)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Survey complete; partial Lean source retained, current Lean replay pending

## Overview

Lean can reduce the code a third party must trust when checking a packing result.
The immediate target is now the computer-assisted lower bound `s(11) ≥ 381/100 = 3.81`:
the [proof card](../../../packing/cases/n11_fractional_certificate/t-018-proof-card.md)
states the argument, and the 329-line
[minimal verifier](../../../packing/cases/n11_fractional_certificate/minimal_verify.py)
decides its five certificate conditions with exact arithmetic.
A complete Lean formalization would check both the geometric implication and the
certificate computation against stated axioms and the kernel.

- **The upper bound has a finite algebraic formalization target.** `s(11) ≤ 3.877084…`
  is a single explicit witness plus 55 pairwise disjointness facts plus containment —
  finitely many polynomial inequalities over one number field.
  The original survey located no formal theorem about `s(n)` for non-trivial `n`; that
  dated search does not establish that none exists.
- **The lower bound has mathematics to formalize.** The retained
  [Lean spike](../../../packing/cases/n11_fractional_certificate/lean-spike/README.md)
  has nine theorem proofs for counting, atomic-mass symmetry, and scalar inequalities
  used in Conditions 2–4. Its source reports a historical Lean 4.32.1/Mathlib 4.32.1
  build and axiom audit.
  This continuation port has source checks only: the pinned Lean toolchain and cache are
  absent on the host, so neither compilation nor a kernel check was replayed.
  The spike does not formalize the geometry, replay Condition 5’s **567,130,649 cells**,
  or prove the full `s(11)` theorem.
- **The lemma layer of the solved cases supplies smaller formalization targets.** A
  formal proof can expose a missing hypothesis in a human argument even before a whole
  optimality theorem is formalized.
- **Use Lean to check retained results before considering it in the search loop.**
  Formal verification of nonlinear inequalities ran about **3,000× slower** than the
  equivalent C++ in the cited Flyspeck experiment.
  That historical measurement motivates separating search from proof replay; it is not a
  benchmark of the current Lean toolchain or this certificate.

## Questions to Answer

1. What is Lean, what exactly does its kernel guarantee, and why would that matter for a
   packing result?
2. What are its performance characteristics, and where do they help or hurt here?
3. What has Lean actually been used for recently, in cases involving genuine invention
   or heavy computation — and what is transferable?
4. Which parts of this problem could be formalized *today*, which could be later, and
   which cannot in principle until the mathematics moves?
5. What would a third-party-verifiable certificate for a packing result look like?
6. What is the cost, and what is the smallest first step worth taking?

## Scope

**Included:** the August 2026 survey of Lean 4 and Mathlib; the recent formalization
record where it bears on computational or newly-discovered mathematics; the specific fit
to upper bounds, lower bounds, the nonavoidance lemma layer, and unavoidable-set
decisions; certificate design; and cost.
The 2026-09-06 reconciliation checks local proof status and certificate values; it does
not repeat the survey’s external literature search.

**Excluded:** a tutorial on dependent type theory; comparison of Lean against Coq/Rocq,
Isabelle or HOL Light on general merits (they appear only where a precedent used them);
and a new search for a packing proof within this formalization reconciliation.

## Findings

### What Lean is, and the one property that matters here

Lean 4 is a dependently-typed programming language and proof assistant.
Its mathematical library, **Mathlib**, is approaching two million lines and covers most
of an undergraduate and much of a graduate curriculum across algebra, analysis, geometry
and number theory.

For this project, one architectural property carries almost all the value: **the trusted
computing base is a small kernel.** A Lean proof is a term; checking it means
type-checking that term against a kernel of a few thousand lines.
Tactics, automation, elaboration, and any AI that produces the proof emit terms that the
kernel checks. The theorem statement and its axiom dependencies also need review: a
kernel check does not establish an unproved assumption or show that the statement
describes the intended geometry.
Independent third-party kernel implementations exist and can re-check the same proof
term.

That is exactly the property the requirement asks for.
The chain of trust for a claim like `s(11) ≤ 3.877084…` becomes:

| Level | What you must trust | Independent? |
| --- | --- | --- |
| Float verifier with a tolerance | The tolerance is the blind spot; **no tolerance both accepts exact contacts and rejects small overlaps** | No — and it is provably unsound for this problem |
| Our exact verifier (Python, or planned Rust) | ~500 lines of our arithmetic, our SAT implementation, our field construction | No — one implementation, one author |
| Two independent exact implementations agreeing | Both, but a shared bug is now unlikely | Partly |
| **A Lean proof** | **Lean’s kernel** | **Yes — small, specified, re-implementable** |

The third row is not hypothetical here: the
[FrankenSim study](research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md)
already ran an unrelated Rust interval implementation against our exact verifier and got
the same partition of the 55 pairs into 41 strictly separated and 14 touching, and
called that agreement “the strongest evidence in either research document.”
A Lean proof can remove dependence on the project’s verifier implementation.
It still requires checking the formal statement and its assumptions against the intended
packing problem.

### Performance characteristics: where Lean is fine, and where it is hopeless

Lean’s cost profile is unusual and needs stating precisely, because the naive summary
("proof assistants are slow") is both true and useless for deciding where to use one.

**Three ways to discharge a computational goal**, with very different trade-offs:

| Mechanism | How it works | Speed | Trust |
| --- | --- | --- | --- |
| `decide` | The kernel reduces the decision procedure directly | Slowest; can time out or fail to reduce at all on structures the kernel’s evaluator handles poorly | **Kernel only** — the strongest guarantee |
| `native_decide` | Compiles the decision procedure and admits its result through a compiler-trusting axiom | Faster for many large checks | The kernel accepts a proof term that depends on the additional axiom; it does not independently evaluate the compiled computation |
| Certificate + reflection | An external tool searches; Lean *checks* a certificate with a verified checker | Fast search, kernel-checked result | **Kernel only** |

For independent checking of the certificate computation, the third row is the target.
An axiom audit distinguishes it from a proof that trusts a compiled decision procedure.
The retained spike uses no `native_decide`, custom axiom, or placeholder proof;
[its README](../../../packing/cases/n11_fractional_certificate/lean-spike/README.md#verification-status)
separates source inspection, historical reported builds, current replay, and the
remaining formal theorem.

**The concrete slowdown figure.** Flyspeck — the formal proof of the Kepler conjecture,
and the closest existing analogue to a formal packing-optimality proof — verified about
1,000 nonlinear inequalities using interval arithmetic with Taylor approximations, and
its authors measured the formal procedure at roughly **3,000× slower than an informal
C++ implementation** of the same check.

Map that onto this project’s
[measured latency tiers](research-2026-08-22-infrastructure-for-packing-exploration.md):

| Task | Native cost (measured) | × 3,000 | Verdict |
| --- | --- | --- | --- |
| One separating-axis pair test | 57 ns | ~170 µs | Fine in isolation |
| One full `n = 11` verification (55 pairs) | ~3 µs of predicate work | ~10 ms | **Entirely fine** |
| One annealing basin (`s(51)`, published) | ~23.6 s | ~20 hours | **Hopeless** |
| A 3,004-basin campaign | ~4.9 GPU-hours | ~14,700 device-hours, or 1.68 device-years | Arithmetic illustration only; GPU throughput and formal proof replay are different workloads |

These multiplications illustrate why a small retained check is a better first target
than instrumenting a search loop with proof replay.
They do not predict Lean performance: the factor comes from a different formal system,
machine, and workload.

### Deep dive: what Lean has actually been used for recently

Four cases, chosen because each isolates a different question this project has.

#### Sphere packing in dimensions 8 and 24 — the domain-adjacent case

The formalization of Viazovska’s Fields-Medal solution began at EPFL in March 2024, led
by Hariharan with Viazovska, and later Birkbeck, Mehta and Lee.
A sorry-free dimension-8 proof was announced **23 February 2026**; the final push was
made by **Gauss**, Math, Inc.'s autoformalization agent, which took the codebase from
about 20,000 to 60,000 lines in **five days**. Dimension 24 optimality and periodic
uniqueness followed in roughly two weeks, using the paper plus autonomous literature
search.

*What it establishes:* a packing-optimality theorem of real depth is formalizable on a
months-not-decades timescale, and the marginal cost of formalization has collapsed
recently. *What it does not establish:* that formalization finds anything.
Viazovska’s proof existed; the project checked it.

#### Flyspeck — the computational-proof case, and the closest analogue

Hales’s formal proof of the Kepler conjecture, completed 2014 in HOL Light and Isabelle
after roughly a decade.
Its shape is the one a square-packing optimality proof would take:

- The geometric conditions become **nonlinear inequalities**, about 1,000 of them,
  discharged by **interval arithmetic with Taylor approximations** on rectangular
  domains, with domain subdivision where needed.
- A separate layer **relaxes the nonlinear system to a linear program** and shows the LP
  is infeasible, hence the nonlinear system is inconsistent.
- The combinatorial explosion is handled by **classifying “tame” plane graphs** into an
  archive that is imported into the proof, rather than re-derived inside it.

Every one of those three moves has a direct counterpart here.
Unavoidable-point arguments *are* nonlinear inequalities over `(x, y, θ)`. The
[`n = 11` report’s](research-2026-08-22-packing-11-unit-squares.md) observation that the
lower-bound methods can be interpreted as resource constraints led to the **fractional
certificate** now retained for `s(11) ≥ 381/100`. Enumerating contact classes raises a
separate completeness obligation analogous to the tame-graph archive problem; a list of
contact graphs alone is not a proof that every packing has been represented.

*The caution:* a decade, and the 3,000× figure comes from this project.

#### `K₈(4,2) = 23` — the certificate case, and the best template

A 2026 result determining a covering-code parameter, structured exactly as this project
should structure its own:

- **Upper bound:** an explicit 23-word code, verified by checking coverage over all `8⁴`
  ambient words — a finite exhaustive check on a witness.
- **Lower bound:** layered combinatorial arguments eliminating `≤ 21` words, then for
  the 22-word case a reduction to six missing-pair graphs, with the remaining
  incompatibility discharged by **two Lean-checked LRAT refutations of stored CNF
  instances**.
- Critically: **no external SAT solver runs during proof replay.** The solver’s output
  is a certificate; Lean checks the certificate.

This is the pattern to copy, and it answers the “third-party-verifiable” requirement
directly.
The search may be as fast, heuristic and untrusted as we like — a GPU annealer,
an SMT solver, an LLM — provided it emits a certificate a verified Lean checker can
replay. Tooling for exactly this exists (`LRAT-Catcher` imports SAT certificates into
Lean 4 by reflection).

#### AlphaProof Nexus — the invention case, and a correction to our own docs

*Advancing Mathematics Research with AI-Driven Formal Proof Search* (Tsoukalas et al.,
arXiv:2605.22763, 21 May 2026) reports agents that pair a frontier LLM with the Lean
compiler in a loop: given a theorem with `sorry` in place of a proof, iterate until Lean
accepts. Results: **9 of 353 open Erdős problems** resolved autonomously, **44 of 492**
open OEIS conjectures proved, a 15-year-old algebraic-geometry question settled, and an
open convergence bound in convex optimization improved — at **a few hundred dollars per
problem**. A post-hoc analysis found the *simplest* agent, using only an LLM and
compiler feedback, could prove all nine, merely at higher cost on the hardest.

*Why this matters here beyond novelty:* both the
[`n = 11` report](research-2026-08-22-packing-11-unit-squares.md) and the
[tooling report](research-2026-08-22-square-packing-algorithms-and-tooling.md) state
that formalization only ever checks a proof that already exists — “neither project
discovered its theorem.”
**That was true of the projects cited and is no longer true in general**, and those
documents are updated accordingly.
The realistic reading is still narrow: the solved Erdős problems were ones with short
proofs once found, and nothing in that result suggests an LLM-plus-Lean loop will
produce a lower bound for `s(11)`. But it does mean the loop is now a *search* method
with a correctness guarantee attached, not merely a transcription method — and the cost
is hundreds of dollars, not decades.

### What could be formalized here, in order of tractability

#### 1. The upper bound — available today, and unclaimed

`s(11) ≤ 3.87708359002281417730789706010096…` unfolds to: *there exist eleven unit
squares, pairwise disjoint in their interiors, all contained in a square of that side.*

Every part of that is finite and algebraic:

- The witness is explicit — six axis-aligned squares and a five-square block at angle
  `a`, with coordinates rational in `u = tan(a/2)`, where `u` is a root of a known
  irreducible degree-8 polynomial.
- Non-overlap for each of the 55 pairs is the separating-axis condition: four candidate
  axes, eight dot products each, **no divisions and no square roots**, so every tested
  quantity is a polynomial in `u`.
- Containment is the same predicate against four container edges.
- 14 of the 55 pairs touch with **exactly zero** gap, which is why this must be done in
  the number field and not numerically — but exact zero in `ℚ(u)` is a decidable
  syntactic test, not an analytic one.

Mathlib has what this needs: polynomial rings, algebraic elements, and `IsAdjoinRoot`
for working in `ℚ[X]/(m)`. The work is stating the geometry cleanly and discharging a
few hundred polynomial sign conditions.
The geometry and sign arguments still require proof development.
The original estimate was weeks rather than days, but no complete upper-bound
formalization has been timed here.

**Why start here even though it proves nothing new:** it delivers the requirement.
A Lean file plus its kernel check is a third-party-verifiable certificate that a
specific packing is valid, replacing “trust our verifier” with “run the checker.”
It is also the natural interchange format for the record corpus: one theorem per
analytically-optimized record.

#### 2. The nonavoidance lemma layer of the solved cases — available, and diagnostic

Friedman’s Lemmas 1–3 and Stromquist’s Lemmas 1–6 are single-variable calculus arguments
— minimise `D(θ)`, differentiate, find the critical angle — done by hand and checkable
by a referee with a pencil.
Lemma 2 is representative and small: *any box whose centre lies in the interior of a
triangle with all sides at most 1 must contain one of its vertices.*

Formalizing these lemmas would test assumptions used in several nontrivial solved cases.
The original survey located no machine-checked version of those particular arguments.
The [`n = 11` report’s](research-2026-08-22-packing-11-unit-squares.md) own correction
history is the argument for bothering — the structure of Stromquist’s Theorem 2 was
misread in this repository until the archived paper was read line by line, and the error
was in exactly this layer.

Then `s(10)` (Stromquist’s Theorem 1): ten points, each region covered by one of Lemmas
1, 2 or 4, then a named-box case analysis.
That is a complete, published optimality proof for a nontrivial `n`.

#### 3. Unavoidable-set verification — the interesting middle

*Does every unit square placed inside `[0,k]²` contain a point of `P`?* is a `∀` over a
compact three-parameter family `(x, y, θ)`. It is not finite, so it needs interval
arithmetic plus subdivision — Flyspeck’s first move, at much smaller scale.

Lean 4 now has the pieces: `LeanCert` provides verified interval arithmetic over dyadic
rationals with a “golden theorem” architecture connecting a fast boolean check to
`∀ x ∈ I, f(x) ≤ c`, and `ComputableReal` gives computable reals.
Both are young.

This is the first item with genuine research value rather than only assurance value: it
would let existing lower-bound proofs be machine-checked, and — more interestingly — let
*candidate* point sets be searched for rather than constructed by hand, which the
[`n = 11` report](research-2026-08-22-packing-11-unit-squares.md) identifies as the
plausible route to a new bound.

#### 4. A lower bound for an open case — a partial formalization

The retained fractional unavoidable-set certificate establishes `s(11) ≥ 381/100`. Its
human implication is short: eleven disjoint inner squares, each covering at least unit
atom mass, would require total mass at least eleven; the certificate carries only
`434547/40000 = 10.863675`. The exact Python checker decides the five hypotheses needed
to apply that argument.
The [result record](../../../packing/frontier/results.yaml) carries T-018’s evidence and
confirmation status, including its method-distinct interval confirmation.

The retained
[`lean-spike`](../../../packing/cases/n11_fractional_certificate/lean-spike/README.md)
contains counting and symmetry lemmas, scalar inequalities with the certificate’s
numbers, and the final algebraic inequality in the support-radius step.
These are partial formalization source, with a historical build reported but no current
Lean replay on this host.
They do not check the atom data or prove that the net and geometry imply coverage at
every orientation.

Condition 5 says every contained side-`9977/10000` square at each of 181 rational
directions covers mass at least one; the retained minimum is `4001/4000`. The Python
verifier reduces the continuum of centers to **567,130,649 reachable event cells**. The
separate interval verifier confirms the same certificate on a doubled net of 361
directions, without needing the diagonal-reflection reduction.
Formalizing the continuum reduction and checking a compact partition or range-minimum
receipt remain proposed work.
The 329-line Python checker already decides the retained certificate; neither its
runtime nor a source-only Lean audit constitutes a Lean proof of the packing theorem.

### What a third-party-verifiable certificate would look like

Pulling the pieces together into the artifact the requirement actually asks for.

**For a packing (an upper bound), which is what we can do now:**

```
theorem s11_le : squarePackingSide 11 ≤ trump11Side := ...
```

with `trump11Side` defined as the root of the degree-8 polynomial in an isolating
interval, the eleven squares given explicitly over `ℚ(u)`, and the proof discharging
containment plus 55 pairwise separations.
The deliverable is a Lean file and a checking command.
A third party runs the kernel; they need not read our Rust, our Python, or this
repository at all.

**For anything found by search**, follow `K₈(4,2) = 23`: the search stays fast and
untrusted, and emits a certificate.
Two shapes are already supported — LRAT refutations from a SAT solver, replayed inside
Lean with no external solver, and sum-of-squares certificates for polynomial
inequalities, which is directly relevant since
[Positivstellensatz certificates](research-2026-08-22-packing-11-unit-squares.md) are
listed there as the one modern proof technique never attempted on this problem.
An SOS certificate is a small object that is expensive to find and cheap to check —
which is the definition of a good certificate.

**The discipline this imposes on our own code** is worth stating, because it is free and
immediate: design the verifier’s output as a *certificate*, not a boolean.
“Valid” is unverifiable; “valid, and here are the 14 pairs that touch with exact zero
and the 41 separating axes with their signs” is a checkable object.
The
[infrastructure plan’s](research-2026-08-22-infrastructure-for-packing-exploration.md)
`Result<Certified, NotProven>` is the right type; this says what should be inside
`Certified`.

## Key Insights

1. **The upper bound reduces to a finite algebraic witness.** The original survey
   located no formal theorem about `s(n)` for non-trivial `n`; `s(11) ≤ 3.877084…` needs
   only finitely many polynomial sign conditions over one degree-8 number field.
2. **Measure formal replay on a retained result first.** The historical Flyspeck
   slowdown suggests that a small result check is a more useful first experiment than an
   entire campaign; it does not establish this project’s eventual slowdown.
3. **The exact-zero contacts are what make this a formalization problem rather than a
   numerical one — and they are also what makes it tractable.** Fourteen of the 55 pairs
   touch with exactly zero gap, which no floating-point or interval method can certify;
   but in `ℚ(u)` exact zero is a *syntactic* test, which is precisely the kind of thing
   a kernel checks well.
4. **Audit axioms as well as build success.** A theorem can build with a placeholder or
   custom axiom; `native_decide` adds trust in compiled computation.
   Independent certificate verification requires an explicit account of those
   dependencies.
5. **The certificate pattern decouples search speed from trust completely.**
   `K₈(4,2) = 23` ran a SAT solver and shipped LRAT refutations checked inside Lean with
   no solver at replay.
   Our annealer can be as fast and unprincipled as it likes provided it emits something
   checkable — which also means the choice of search technology stops being a trust
   question.
6. **Formalization has stopped being only transcription, and our other documents needed
   updating.** AlphaProof Nexus resolved 9 open Erdős problems and 44 OEIS conjectures
   autonomously at a few hundred dollars each.
   That work did not produce this project’s later `s(11)` certificate, but it is
   evidence against the blanket claim that formalization never participates in
   discovery.
7. **The nonavoidance lemmas are small diagnostic targets.** They support several solved
   cases, and this repository has already found one misreading in that layer.
8. **Flyspeck’s three moves map one-to-one onto this problem.** Nonlinear inequalities
   by interval arithmetic; relaxation to an infeasible LP; a pre-classified
   combinatorial archive imported rather than re-derived.
   The [`n = 11` report’s](research-2026-08-22-packing-11-unit-squares.md) proposed
   fractional route now has the retained `381/100` certificate.
   A compact, formally checked coverage receipt is a further assurance target.

## Comparison Matrix

Where each layer of assurance stands, for a claim of the form “this packing is valid”.

| Approach | Catches exact contacts? | Third-party verifiable? | Cost to produce | Cost to check | Status here |
| --- | --- | --- | --- | --- | --- |
| Float SAT with tolerance | **No — provably cannot** | No | Trivial | Microseconds | Implemented, and unsound for this purpose |
| Interval arithmetic | No (proves `>`, never `=`) | No | Low | Milliseconds | Implemented in the FrankenSim probe |
| Exact arithmetic in `ℚ(α)` | Yes | Only if you read our code | Low | 0.35 s (Python) | **Implemented and passing** |
| Two independent exact implementations | Yes | Partly — a shared bug is unlikely | Medium | Seconds | **Achieved once**, Rust vs Python |
| Lean proof, `native_decide` | Possible | Adds compiler trust | Depends on the formalization | Workload-dependent | Not used in the retained spike |
| Lean proof without a computation-trusting axiom | Possible | Kernel and declared axioms, with statement review | Unmeasured for the full packing theorem | Unmeasured here | Nine partial lower-bound theorem proofs retained as source; historical build reported, current replay pending; no full packing theorem |

## Recommendations

Ordered by value per unit of effort, and deliberately small at the start.

1. **Replay the retained Lean spike before relying on its formal status.** Use the
   committed toolchain and manifest, retain build output, and inspect the nine-theorem
   axiom audit. No mathematical research is needed for this operational prerequisite.
2. **Design a compact proof-producing Condition 5 receipt.** The `381/100` result has a
   short human implication and complete exact Python replay.
   A partition or range-minimum receipt, with a proof of its coverage, could reduce the
   cost of independent formal checking.
   The spike README gives the proposed event-strip decomposition and its missing
   obligations; no receipt checker has been implemented.
3. **Make packing verifiers emit certificates suitable for independent checking.** For
   upper bounds, record the separating axis and its sign for each strictly separated
   pair and the exact-zero witness for each contact.
4. **Formalize the nonavoidance lemma layer** — Friedman’s Lemmas 1–3, Stromquist’s 1–6.
   These small calculus arguments support several solved cases.
   Check their hypotheses against the published statements before formalizing them.
5. **Formalize `s(11) ≤ 3.877084…` from the exact witness.** Scope it as one packing
   first; if it works, the record corpus becomes a theorem per analytically-optimized
   entry.
6. **Then `s(10) = 3 + ½√2`**, Stromquist’s Theorem 1, a complete published optimality
   proof at human scale.
   This is where the lemma layer pays off.
7. **Evaluate `LeanCert` and `ComputableReal` on one nonavoidance lemma** before
   committing to the unavoidable-set decision procedure.
   Both are young; a single lemma is a cheap probe of whether the interval-arithmetic
   layer is ready.
8. **Evaluate an LLM-plus-Lean loop on small, independently stated lemmas.** The
   survey’s formal-proof-search examples motivate an experiment; they do not price this
   project’s geometry or receipt checker.

Keep formalization separate from the active numerical search until measurements justify
integration. Start with a compact receipt design before attempting kernel evaluation of
hundreds of millions of rational cells.
The Python verifier remains the decision procedure for the retained lower bound while
those formal proof layers are unfinished.

## Open Questions

- [ ] How hard is the `s(11)` upper bound in practice?
  The estimate of weeks assumes discharging a few hundred polynomial sign conditions
  over `ℚ(u)` is routine in Mathlib.
  A single pair, done end to end, would calibrate it — and is the obvious first
  experiment.
- [ ] Does Mathlib’s `IsAdjoinRoot` / `AdjoinRoot` machinery give usable `decide`-able
  equality in `ℚ[X]/(m)` at degree 8, or does the kernel’s evaluator struggle as it
  reportedly does with some `Fin.foldl` structures?
- [ ] Is there a formal statement of “packing” in Mathlib already, from the
  sphere-packing project, that the square case could reuse rather than redefine?
- [ ] What does an SOS certificate for a square-packing lower bound even look like, and
  is the Positivstellensatz route more tractable *because* it produces a checkable
  object?
- [ ] Could the Gauss-style autoformalization agents that finished dimension 8 be
  pointed at the lemma layer, and at what cost?
- [ ] What partition or range-minimum receipt lets Lean check the full `n = 11`
  Condition 5 coverage fact without replaying the search or trusting compiled execution?
- [ ] Does the 3,000× Flyspeck figure still hold in Lean 4 with modern interval tooling,
  or has it improved? It is a 2013-era measurement on HOL Light.

## Methodology

Conducted 2026-08-22 by web research plus analysis against this repository’s existing
documents and code.

The 2026-09-06 reconciliation reviewed the seven-file spike and proposed note update
from commit `04127189a7f08cab35b3c3b6e098d7cc9a729ee0` as untrusted source material.
The six Lean/build files were retained after source inspection; their README was
corrected against the current certificate, proof card, and result record.
The checker at integration commit `7e932f1b` has 329 physical lines, and the current top
rung has 567,130,649 reachable event cells.
The source branch reported Lean 4.32.1/Mathlib 4.32.1 builds and an axiom audit using
standard axioms only.
This host lacks that pinned toolchain and cache, so the port did not replay syntax,
elaboration, or kernel checking and does not treat the historical report as a current
verification receipt.

**Sources consulted directly.** The sphere-packing formalization project pages and
arXiv:2604.23468; the Flyspeck literature, principally the Taylor-interval verification
work (arXiv:1301.1702) and the formal-proof account; arXiv:2606.16688 for
`K₈(4,2) = 23`, fetched and read for its certificate structure; arXiv:2605.22763
(*Advancing Mathematics Research with AI-Driven Formal Proof Search*), fetched for its
exact title, authors, dates and reported results; and the `LeanCert` and
`ComputableReal` project descriptions.

**Claims grounded in this repository rather than the literature.** The 55-pair /
14-contact structure of Trump’s packing, the degree-8 field, and the 0.35 s verification
time are from `packing/` and were re-verified in earlier sessions.
The 57 ns and 23.6 s figures used in the slowdown table are from the
[infrastructure study’s](research-2026-08-22-infrastructure-for-packing-exploration.md)
measurements and the record page respectively.

**Not established.** Neither Condition 5 nor the full `s(11)` theorem has a retained
Lean formalization. The nine-theorem spike is source-reviewed here but awaits current
Lean replay. Every estimate of the remaining formalization effort is a judgement, not a
measurement, including the “weeks, not days” estimate for the `s(11)` upper bound.
The claim that no formal theorem about `s(n)` exists for non-trivial `n` is a negative
result from search and is weak in the usual way: nothing was found, which is not the
same as nothing existing.
The 3,000× figure is quoted from Flyspeck’s own authors, measured on HOL Light in 2013,
and is used here as an order of magnitude rather than a current benchmark.

**Confidence.** High for the trust argument and the tier placement, which follow from
Lean’s architecture and from measurements already in this repository.
High for the four precedents, each read from its primary or its project page.
Medium for the tractability ordering of the formalization targets.
Low for effort estimates.

## References

- **Lean and Mathlib** — [lean-lang.org](https://lean-lang.org/fro/about/);
  [Mathlib](https://leanprover-community.github.io/), approaching two million lines.
- **Sphere packing in Lean** —
  [project page](https://thefundamentaltheor3m.github.io/Sphere-Packing-Lean/),
  [repository](https://github.com/math-inc/Sphere-Packing-Lean),
  [arXiv:2604.23468](https://arxiv.org/abs/2604.23468). Sorry-free in dimension 8 on 23
  February 2026; Gauss took it from ~20k to ~60k lines in five days.
- **Flyspeck** — Hales et al., *A Formal Proof of the Kepler Conjecture*, Forum of
  Mathematics Pi (2017); Solovyev and Hales,
  [*Formal Verification of Nonlinear Inequalities with Taylor Interval Approximations*](https://arxiv.org/abs/1301.1702)
  — the ~3,000× figure and the ~1,000 inequalities;
  [a critical retrospective](https://arxiv.org/pdf/2402.08032).
- **`K₈(4,2) = 23`** — [arXiv:2606.16688](https://arxiv.org/pdf/2606.16688). Explicit
  witness for the upper bound; layered combinatorics plus two Lean-checked LRAT
  refutations for the lower, with no external SAT solver at replay.
- **AlphaProof Nexus** — Tsoukalas et al., *Advancing Mathematics Research with
  AI-Driven Formal Proof Search*, [arXiv:2605.22763](https://arxiv.org/abs/2605.22763)
  (21 May 2026; revised 8 June 2026). 9 of 353 Erdős problems, 44 of 492 OEIS
  conjectures, at a few hundred dollars per problem.
- **Certificate tooling** — [LeanCert](https://github.com/alerad/leancert) (verified
  interval arithmetic over dyadic rationals);
  [ComputableReal](https://github.com/Timeroot/ComputableReal);
  [LRAT-Catcher](https://arxiv.org/pdf/2607.00815) (SAT certificates into Lean 4 by
  reflection);
  [SOS certificates from LLM-generated conjectures](https://arxiv.org/pdf/2605.15445).

Companion documents in this repository:

- [Packing 11 Unit Squares in a Square](research-2026-08-22-packing-11-unit-squares.md)
  — the mathematics, the lemma layer, and the research programme.
- [Algorithms and Tooling for Square Packing](research-2026-08-22-square-packing-algorithms-and-tooling.md)
  — why exactness is required, and the formalization precedents as first recorded.
- [FrankenSim as a Rust Toolkit for Square Packing](research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md)
  — the independent-implementation agreement this document extends.
- [Infrastructure for Square-Packing Exploration](research-2026-08-22-infrastructure-for-packing-exploration.md)
  — the latency tiers Lean is placed into, and the `Certified` type it would populate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
