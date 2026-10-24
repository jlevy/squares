# Square Packing Archive

[![CI](https://github.com/chelokot/square-packing-archive/actions/workflows/ci.yml/badge.svg)](https://github.com/chelokot/square-packing-archive/actions/workflows/ci.yml)
[![Lean](https://img.shields.io/badge/Lean-4.33.0-62f5c8)](formal/lean-toolchain)
[![Code license](https://img.shields.io/badge/code-Apache--2.0-70ddff)](LICENSE)
[![Data license](https://img.shields.io/badge/data-CC%20BY%204.0-b9a4ff)](LICENSE-DATA)

How small a square can contain `n` unit squares? Write `s(n)` for its minimum
side length. Squares may rotate; their interiors cannot overlap.

**[Open the interactive archive →](https://chelokot.github.io/square-packing-archive/)**

[![Packing results for 1–100 squares. Green: proved optimal; amber: nontrivial bound; white: basic grid bound. Click to explore.](docs/assets/coverage.svg)](https://chelokot.github.io/square-packing-archive/#explore)

**Every result has a kernel-checked Lean proof.** Green cells mark proved optima;
amber cells mark nontrivial bounds; white cells mark basic grid bounds.
Select a count to inspect the packing, coordinates,
authors, sources, and proof.

## Selected results

Formalized published optima and checked upper-bound constructions:

| Result                         | Background                                                                                             | Lean                                                                   |
| ------------------------------ | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| `s(n²−2) = n`, integer `n ≥ 2` | [Replacement compensation proof](docs/nagamochi-compensation-proof.md)                                 | [Theorem](formal/SquarePackingArchive/NagamochiPackingTheorem.lean)    |
| `s(6) = 3`                     | [Stromquist’s point-set argument](docs/small-records-formalization.md#why-six-squares-need-side-three) | [Theorem](formal/SquarePackingArchive/Records/Square6Exact.lean)       |
| `s(10) = 3 + √2 / 2`           | [Stromquist’s point-set argument](docs/small-records-formalization.md)                                 | [Theorem](formal/SquarePackingArchive/Records/Square10Exact.lean)      |
| `s(13) = 4`                    | [Bentz’s strategy, with corrected auxiliary sets](docs/bentz-13-formalization.md)                      | [Theorem](formal/SquarePackingArchive/Records/Square13Exact.lean)      |
| `s(22) = 5`                    | [Bentz’s staggered-lattice argument](docs/bentz-lattice-formalization.md)                              | [Theorem](formal/SquarePackingArchive/Records/Square22.lean)           |
| `s(33) = 6`                    | [Bentz’s staggered-lattice argument](docs/bentz-lattice-formalization.md)                              | [Theorem](formal/SquarePackingArchive/Records/Square33.lean)           |
| `s(68) ≤ 8.80339`              | [Inspect the construction](https://chelokot.github.io/square-packing-archive/?n=68#explore)            | [Certificate proof](formal/SquarePackingArchive/Records/Square68.lean) |
| `s(69) ≤ 8.8272`               | [Inspect the construction](https://chelokot.github.io/square-packing-archive/?n=69#explore)            | [Certificate proof](formal/SquarePackingArchive/Records/Square69.lean) |

### Nagamochi’s lemma and a replacement proof

The archive contains a [Lean-checked counterexample to Lemma 1](docs/nagamochi-score-counterexample.md)
in Nagamochi’s 2005 paper. **It contradicts the individual-square score lemma,
not the packing theorem.** A [replacement argument](docs/nagamochi-compensation-proof.md)
proves `s(n²−2) = n` without assuming that lemma. It covers square containers,
not the paper’s full rectangular-container theorem.

## What is checked

Every catalogued claim, including historical entries, is checked against a Lean
theorem with the stated square count, relation, and exact formal value. The
dependency audit permits only `propext`, `Classical.choice`, and `Quot.sound`;
it rejects unfinished proofs, custom axioms, and native-evaluation oracles.
See the [data model](docs/data-model.md) for provenance and display conventions.

An upper bound proves that a packing exists, not that it is optimal or best known.
The historical catalog is incomplete. Counts without a catalogued record use
the basic grid bound `s(n) ≤ ⌈√n⌉`; these do not count as historical records.
Publication dates and formalization dates are kept separate.

## Run and verify

Requires [Bun](https://bun.sh/), Python 3, and [elan](https://github.com/leanprover/elan).
The Bun dependencies, Lean toolchain, and Mathlib revision are pinned.

```console
bun install --frozen-lockfile
bun run dev
```

To check the site, archive, and proofs from the repository root:

```console
bun run build
bun run check
bun run test
(cd formal && lake exe cache get)
python3 scripts/build-lean-certificates.py
```

The memory-bounded build checks the quadratic certificates one at a
time, then the complete library. See [tracker imports](docs/tracker-imports.md)
for the reconstructed current and historical layouts.

See the [development guide](docs/development.md) for architecture, imports,
additional tests, and deployment. GitHub Pages updates only after CI passes.

## Contribute

- **A result with a Lean proof:** open a pull request following [CONTRIBUTING.md](CONTRIBUTING.md).
- **A result awaiting formalization:** open an [issue](https://github.com/chelokot/square-packing-archive/issues), with sources, coordinates, and attribution.
- Corrections, historical sources, and viewer improvements are welcome too.

For example, the stronger reported 11-square bound is tracked in [issue #16](https://github.com/chelokot/square-packing-archive/issues/16);
the public construction currently proves only `s(11) ≤ 3.88`.

## Sources and gratitude

Project concept and product direction: **chelokot**. AI research and
formalizations: **GPT 6 Astra**. These credits are separate from the original
researchers' discovery and proof credits.

This archive builds on [Erich Friedman’s survey](https://doi.org/10.37236/28),
the [Squares in Squares tracker](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
maintained by David Ellsworth, and the original authors linked from each result.
Discoverers, optimizers, and provers retain their separate credits.
See [ATTRIBUTION.md](ATTRIBUTION.md).

## License

[Apache-2.0](LICENSE) for code and Lean sources; [CC BY 4.0](LICENSE-DATA) for archive
metadata, original prose, and generated visualizations. Linked papers and
external materials retain their own licenses.
