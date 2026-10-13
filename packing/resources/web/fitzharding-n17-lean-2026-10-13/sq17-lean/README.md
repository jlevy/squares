# A Lean proof of optimal square packing for 17 unit squares

Seventeen unit squares can be packed in a square of side `L` exactly when
`L` is at least **4.675530093604551…**, the exact algebraic side length of
Bidwell's packing. Arbitrary rotations are allowed, and touching boundaries
are allowed.

The Lean theorem is:

```lean
Sq17.square17_optimality (L : ℝ) :
  Sq17.HalfPlaneAssembly.PlainPacking L ↔ Sq17.EndpointGeometry.side ≤ L
```

`PlainPacking L` means that 17 independently translated and rotated closed unit
squares, with pairwise disjoint interiors, fit inside an axis-aligned square of
side `L`. The exact algebraic constant `EndpointGeometry.side` is approximately
**4.675530093604551**. Thus the theorem states optimality, including existence at
the endpoint. Its statement has no remaining certificate-acceptance or
case-exclusion premise.

The underlying definitions are [unit squares](Sq17Lean/SquareBase.lean#L18),
[their coordinate parametrization](Sq17Lean/SquareBase.lean#L14),
[the container](Sq17Lean/PropagationWall.lean#L10),
[the exact endpoint](Sq17Lean/EndpointGeometry.lean#L17), and
[the packing predicate](Sq17Lean/PackingStatement.lean#L7).
The [endpoint witness](Sq17Lean/PackingStatement.lean#L34) supplies existence.

The theorem compiled in the research checkout with Lean 4.34.1 and the pinned
Mathlib dependencies. Concrete certificate checks use `native_decide`; the Lean
compiler and native evaluator are part of the trust boundary, alongside
`propext`, `Classical.choice` and `Quot.sound`. The research theorem's axiom
report contains 13,343 Lean-generated native-check facts and no `sorryAx`.
The geometric soundness arguments are checked by Lean's kernel. The large
finite certificate checks are evaluated as compiled native code and introduced
through `native_decide`. This follows the same trust model used by the
[eleven-square formalization](https://github.com/Queuingtheorydotcom/11SquaresFormalized).
This is not a kernel-only computation claim.

**Clean source rebuild passed.** All 4,951 modules in the final theorem's
import closure were rebuilt from the published sources on Linux with Lean
4.34.1. No precompiled project proof objects from the research checkout were
used; the pinned third-party dependency cache was reused. Independent checks
were distributed between two Linux machines, with source, dependency and
native-library hashes checked before accepting their outputs. The final
theorem's axiom set exactly matches the local build, and both optional controls
passed. See the [verification receipt](verification/clean-build-receipt.json)
and [full axiom report](verification/Square17Optimality.log).

The trust boundary includes the Lean compiler, native evaluator and C toolchain.
The receipt records successful reproduction; it does not replace the proof
sources or the stated trust assumptions.

## Verify and build

Download all three certificate source archives from the
[v1.0.0 release](https://github.com/ofitzharding/sq17-lean/releases/tag/v1.0.0)
and place them under `certificates/`, as listed in `manifest.json`. They contain Lean source, not precompiled proof objects. Every
module has an individual SHA256 hash. The main package follows the final theorem's
import closure; two optional validation modules are marked separately in the
manifest. The package omits exploratory search code and original traces.

Install Lean through elan and a C toolchain supported by Lean. Then, from this
directory:

```sh
python3 scripts/unpack.py
lake exe cache get
python3 scripts/reproduce.py build --jobs 40 --proof-jobs 8
```

Use Python 3.10 or newer. Lower the job counts for smaller machines; full replay
requires substantial CPU time and tens of gigabytes of disk and memory. The
first job limit controls core certificate checks; the second controls modules
depending on Mathlib. Native checker libraries are compiled from the included
Lean sources. No Python mathematics package or trace converter is required.

`scripts/unpack.py --verify-only` checks the package without expanding it. The
extractor rejects unlisted members, duplicate paths, links, path traversal and
checksum mismatches. It refuses an incomplete release by default.

Successful compilation prints `REPRODUCTION_ACCEPTED
Sq17Lean.Square17Optimality`. The exact theorem and axiom report are in
`reproduction/logs/build/Sq17Lean.Square17Optimality.log`. The build driver has
passed small real-Lean integration tests on macOS and Linux; those tests do not
replace the full packing replay.

After the main build, optional controls check a feasible two-square packing,
nonvacuity of the production wrappers, and legal boundary contact. Their finite
checks use kernel reduction:

```sh
lake env lean Sq17Lean/HalfPlanePositiveControl.lean -o .lake/build/lib/lean/Sq17Lean/HalfPlanePositiveControl.olean
lake env lean Sq17Lean/HalfPlaneBoundaryControl.lean -o .lake/build/lib/lean/Sq17Lean/HalfPlaneBoundaryControl.olean
```

The statement and interfaces were reviewed for quantifiers, frames, owner
reindexing, symmetry, boundary contact, and potentially vacuous hypotheses.
The positive controls supplement that review; they do not replace checking the
mathematical definitions and the complete proof.

## Credits

John Bidwell discovered the packing in 1998, improving Pertti Hämäläinen's
1980 arrangement; see [Friedman's survey](https://erich-friedman.github.io/papers/squares.pdf).
The [Squares Project](https://github.com/jlevy/squares) collects the wider
research record. Mannaseh Ahmed and collaborators' [eleven-square
formalization](https://github.com/Queuingtheorydotcom/11SquaresFormalized)
provided a useful reference for computer-assisted formalization and its trust
boundary. David MacIver's [earlier Lean work](https://github.com/DRMacIver/square-packing-research)
concerns a lower bound for seventeen squares.

A search on 12 October 2026 of public Lean repositories, theorem statements,
the Squares Project records, arXiv and public Lean-community indexing found no
earlier complete Lean proof of this optimality result. Earlier formalizations
of seventeen-square constructions or weaker lower bounds do not establish
its global optimality.

Marc Overbeck published an independent [candidate proof of seventeen-square
optimality](https://github.com/Kleddamag/the-seventeenth-square-candidate)
on 12 October 2026, using mathematical arguments and Python and JavaScript
certificate checkers. This repository presents a separate Lean formalization.

This project was developed with substantial assistance from Claude and Codex.
The published theorem, source files and explicit trust boundary are the basis
for assessing the result.

Project sources are licensed under the [MIT License](LICENSE). Dependencies,
including Mathlib, retain their own licenses.
