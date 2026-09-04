# Lean Feasibility Spike for the `s(11) ≥ 381/100` Certificate

This directory is a feasibility spike.
It does not prove condition C4, replay the 1,121-atom certificate, or prove the headline
theorem `s(11) ≥ 381/100`. Its Lean source contains no `sorry` terms, custom axioms, or
uses of `native_decide`. The spike was checked with Lean 4.32.1 and Mathlib 4.32.1. The
complete local toolchain and Mathlib cache occupied approximately 10 GB; after the cache
was present, `Kernel.lean` checked in 3.6–4.6 seconds in the prototype.
Two clean project builds using the populated dependency cache took 5.7 and 9.4 seconds;
their axiom audits took 2.6–2.7 seconds on the development machine.
The [one-minute proof](../PROOF.md) and [minimal exact checker](../minimal_verify.py)
remain the recommended primary presentation because together they are complete and the
checker is self-contained, uses only Python’s standard library, and decides every
condition from C0 through C4.

## What the Spike Proves

[`Kernel.lean`](Kernel.lean) contains 149 lines, including comments.
It proves:

- the finite nonnegative counting inequality behind a weighted unavoidable-set proof;
- the set-based form that derives a unique atom owner from pairwise-disjoint membership;
- preservation of atomic mass under an involution represented by a permutation of the
  atoms;
- the certificate’s exact C1, C2, and C3 scalar inequalities; and
- the final algebraic inequality used in the support-function containment step.

The counting core is the contradiction

```text
11 ≤ Σⱼ μ(Qⱼ) ≤ μ(K) = 434547/40000 < 11.
```

The exact C3 value checked by Lean is

```text
(9977/10000) · (1 + 207107/90000000)
  = 899996306539/900000000000 < 1.
```

[`AxiomAudit.lean`](AxiomAudit.lean) prints the dependencies of every exported theorem.
They are Mathlib’s standard `propext`, `Classical.choice`, and `Quot.sound`; no theorem
depends on a spike-specific axiom.

## Reproduce the Check

Install [Elan](https://github.com/leanprover/elan) by its documented method, then run
these commands in this directory:

```shell
lake exe cache get
lake build Kernel
lake env lean AxiomAudit.lean
```

The committed `lean-toolchain`, `lakefile.toml`, and `lake-manifest.json` pin Lean,
Mathlib, and Mathlib’s transitive dependencies.
Do not run `lake update` when checking this snapshot: that command is for deliberately
changing dependency resolutions and rewrites the manifest.
Lake consumes the committed manifest and fetches its exact revisions during the commands
above. `.lake/` contains downloaded and built files and is not part of this package.

## Missing Proof Layers

The spike does not define oriented squares, packings, or the infimum `s(n)`. It also
does not prove the diagonal-reflection orientation reduction, nearest-angle lemma,
half-angle tangent formula, or continuum-to-finite arrangement reduction used by C4. It
contains no certificate data and performs no 181-direction computation.

A complete Lean proof would need a proof-producing C4 checker.
Direct kernel evaluation of the Python verifier’s 567,130,649 rational placement cells
is unlikely to be practical.
A smaller certificate could record the feasible vertical interval and range minimum for
each breakpoint row, reducing the retained obligations to at most roughly 181 times
2,243 rows. Lean would still need a proof that those row certificates cover every
admissible center.

`native_decide` could run a larger executable check, but Lean admits its result through
a compiler-trusting axiom.
That trust boundary does not meet the purpose of a kernel-checkable headline theorem, so
this spike does not use it.

## Why the Python Proof Remains Primary

The Python checker sits beside the certificate and decides all five conditions with
exact rational arithmetic.
A reader can copy those two files and run them with CPython 3.8 or later without
installing dependencies.
This Lean spike proves that the short mathematical kernel formalizes cleanly; it does
not yet replace the complete certificate replay.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
