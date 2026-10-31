# A Lean proof of optimal square packing for 19 unit squares

Nineteen unit squares fit in a square of side `L` exactly when
`L ≥ 3 + 4√2/3 ≈ 4.885618`, with arbitrary rotations and touching allowed.

```lean
Sq19.square19_optimality (L : ℝ) :
  Feasible19 L ↔ 3 + 4 * Real.sqrt 2 / 3 ≤ L
```

Definitions: [unit squares](Sq19Lean/SquareBase.lean#L20),
[the packing predicate](Sq19Lean/Assembly/PlainPacking.lean#L11),
[the explicit packing](Sq19Lean/EndpointPacking.lean),
[the theorem](Sq19Lean/Assembly/Optimality.lean#L9).

Axioms: `propext`, `Classical.choice`, `Quot.sound` and 4,320 `native_decide`
certificate checks, so Lean's compiler and native evaluator are trusted
([axiom report](verification/Square19Optimality.log)). All 13,143 modules in the
theorem's import closure, Mathlib included, pass a kernel replay.

**Clean source rebuild passed.** On 16 October 2026 a fresh clone of this repository,
with certificates fetched from the release, was rebuilt from source with
`scripts/verify.py --kernel-replay` on a 64-core Linux machine in 5 h 18 min:
`VERIFIED`, 0 kernel-replay failures ([receipt](verification/clean-build-receipt.json),
[log](verification/clean-build.log)).

## Verify

Linux x86-64 with [elan](https://github.com/leanprover/elan), Python 3.10+,
`curl`, `xz` and `libgmp`:

```sh
bash scripts/fetch.sh        # certificate sources from the v1.0.0 release, hash-checked
python3 scripts/verify.py    # build from source; prints VERIFIED if statement and axioms match
```

A full build takes several hours on a 64-core, 512 GB machine. Add
`--kernel-replay` to also replay every module through the kernel.

## Credits

Builds on the [s(17) formalization](https://github.com/ofitzharding/sq17-lean).
Thanks to everyone involved with the [Squares Project](https://github.com/jlevy/squares),
especially Manasseh Ahmed ([@Queuingtheorydotcom](https://github.com/Queuingtheorydotcom)).
Developed with substantial assistance from Claude and Codex.

MIT License.
