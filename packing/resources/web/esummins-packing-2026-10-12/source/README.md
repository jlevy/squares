# Square-packing lab: the n = 11 case

> ## Start here — 2026-09-10
>
> * **[`writeup/`](writeup/) — the six write-up documents.** Begin with
>   **[`writeup/01_summary.md`](writeup/01_summary.md)**, the two-page brief.
> * **[`writeup/05_status_sheet.md`](writeup/05_status_sheet.md) — the canonical status table**, pinned to a
>   commit: every result and every unfinished family, with the verifier sha behind each certificate and the
>   concrete Lean theorem behind each `[L]`. **Nothing else in this repository may state a status that
>   disagrees with that file.**
> * **[`writeup/06_compute_plan.md`](writeup/06_compute_plan.md) — the capped compute plan**: reconciled
>   components, the $300–500 calibration pilot, stop conditions, and the exit criteria for "only compute
>   remains".
>
> **Current headline, in one line:** `3.82 ≤ s(11) ≤ 3.877084`, the lower bound unconditional and Lean-checked
> end to end; the complete optimality-and-uniqueness theorem is **not** proved and is **not** merely waiting on
> compute — three Lean obligations are open, two classes are theory-limited with no priced route, and no k0
> cell is closed. See the status sheet before quoting anything.
>
> Everything below and in `LOG.md`, `attempts/` and `docs/` is the working record, kept accessible behind this
> pointer. Historical documents are not retro-edited; where one disagrees with the status sheet, the status
> sheet is right.

**Problem.** Let s(n) be the side of the smallest square that contains n non-overlapping unit
squares (rotations allowed). Determine s(11).

**Status at project start (2026-08-16), verified by A01 — see `docs/known_results.md`.**

| bound | value | source |
|---|---|---|
| upper (best known packing) | 3.877084… (root of an octic; Trump 1979 contact structure, refined Gensane–Ryckelynck 2005) | Friedman survey DS7 |
| lower (proof) | 2 + 2·sqrt(4/5) = 3.788854… | Stromquist 2003, EJC 10 R8 |

Gap ≈ 0.088.

**Lab result (2026-08-18): s(11) ≥ 3.82** — measure/LP certificates in `certs/`, two independent exact verifiers,
Lean 4 theorems in `lean/PackingCert`. See `docs/results.md`. Remaining gap 3.82 ≤ s(11) ≤ 3.877084.

**Goals** (either closes the project):
1. Raise the lower bound and/or lower the upper bound until they meet; or
2. An ab-initio construction method for optimal packings for given n.

**Final deliverable for any proven claim: a Lean 4 certificate** (see `lean/`).

## Repository layout

```
README.md              this file
LOG.md                 chronological lab notebook (advisor + agents append here)
docs/known_results.md  state of the art, with citations
docs/literature.md     literature sweep results
docs/papers/           downloaded PDFs
docs/ideas.md          idea board: proposed attacks, with status
attempts/REGISTRY.md   every attempt (successful or failed) with outcome — READ BEFORE STARTING WORK
attempts/<id>/         per-attempt working directory (code, data, notes.md)
code/                  shared library code (geometry, verifiers, optimizers)
certs/                 machine-checkable certificates (JSON) + Python verifiers
lean/                  Lean 4 project for the final certificate
```

## Rules for all agents (postdocs / students)

1. Before starting, read `attempts/REGISTRY.md` and `docs/ideas.md`. Do not re-run a failed idea
   unchanged; if you vary it, say what is different.
2. Every attempt gets an id `A<nn>-<slug>`, a directory `attempts/<id>/` with `notes.md`
   (goal, method, result, why it failed / what it proved, next steps), and one line in the REGISTRY.
3. Numerical claims must state precision and method. Anything called "proved" must be either
   exact rational/integer arithmetic, rigorous interval arithmetic, or a human proof written out.
4. Do not overwrite other agents' directories. Shared code goes in `code/` with a short docstring.
5. Append a dated entry to `LOG.md` when you finish (what, where, outcome).
