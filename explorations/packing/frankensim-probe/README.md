# FrankenSim probes

Two experiments run against
[FrankenSim](https://github.com/Dicklesworthstone/frankensim) while researching
[research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md](../docs/project/research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md).
Both ask a question our square-packing work actually needs answered.

Nothing from FrankenSim is vendored here — these are our own sources, dropped into a
local checkout’s `examples/` directories and removed afterwards.

```bash
./run.sh /path/to/frankensim
```

The checkout must have its constellation siblings materialized
(`cargo run --manifest-path tools/bootstrap/Cargo.toml`) and, as of the pins recorded in
`constellation.lock`, one manifest fix — see the research doc’s methodology.

## `packing_sat.rs` — can certified interval arithmetic verify a packing?

Runs the separating-axis test on Trump’s 11-unit-square packing from f64 coordinates,
once with `fs_ivl::Interval` (outward-rounded) and once with `fs_ivl::orient2d`
(Shewchuk’s adaptive exact predicate).

Result: intervals prove 41 of 55 pairs strictly separated and cannot settle the other 14
— exactly the 14 pairs our own exact verifier finds touching with zero gap.
Independent confirmation, from two unrelated implementations, that interval arithmetic
buys precisely the strict separations and nothing more.

The exact predicate settles 47 and finds **8 pairs with no separating axis at all**: at
16 significant digits the published packing genuinely overlaps.
That is a proof about the rounded configuration, since `orient2d` is exact for f64
inputs.

## `schedule_invariance.rs` — is a counter-based stream schedule-independent?

Draws 64 tiles × 32 values from `fs_rand`’s Philox stream in sequential, reversed, and
worker-interleaved order, and folds each into a hash.

Result: all three hashes identical; `Stream::at(index)` matches the sequential prefix;
seeking to index 2^63 costs the same as index 0. This is the property a parallel packing
search needs — the answer is a function of `(seed, kernel, tile, index)`, never of which
thread ran when.

## Licence

FrankenSim and its sibling repositories are MIT **with an OpenAI/Anthropic rider** that
grants no rights to those parties or anyone acting on their behalf.
Read it before depending on any of that code.
These probe sources are ours and carry this repository’s terms.
