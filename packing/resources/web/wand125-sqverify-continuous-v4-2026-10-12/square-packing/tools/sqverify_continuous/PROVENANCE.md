# Provenance of `sqverify_continuous/`

`sqverify_fast/` is `tools/fine_net_verifier/sqverify_fast/` of this repository, with a
continuous-angle mode added. That directory is in turn `packing/sqverify_fast` of
[jlevy/squares](https://github.com/jlevy/squares) (base commit
`dee22b882499a295b05424ca5a25121195259ebf`) with our `proof_net` change; see
`tools/fine_net_verifier/PROVENANCE.md`.

The change (`patches/continuous.diff`, a unified diff from
`tools/fine_net_verifier/sqverify_fast/` to `sqverify_fast/`):

| file | status |
|---|---|
| `src/slab.rs` | new: the continuous-angle branch and bound (lemmas C1 to C6 of `CONTINUOUS.md`) |
| `src/slab_tests.rs` | new: property tests against the exact rational oracle |
| `src/lib.rs` | one line: `pub mod slab;` |
| `src/main.rs` | new command-line options `--continuous`, `--core`, `--tau`, `--eps`, `--last-t`, `--axis-core`, `--cuts`, `--roots`, `--resume`, and the function that runs the mode |
| `CONTINUOUS.md` | new: the claim, the lemmas, the tests and the limits |
| every other file | unchanged from `tools/fine_net_verifier/sqverify_fast/` (upstream code and documentation) |

What the new mode reuses from the upstream crate, unchanged:

- the outward-rounded binary64 interval arithmetic (`src/interval.rs`, lemma I1 of `SOUNDNESS.md`);
- admission of the certificate and its D4 expansion (`src/certificate.rs`, `src/exact.rs`);
- the exact axis-direction event sweep (`src/axis.rs`, lemmas A1 and A2), used for the near-axis range;
- the exact rational oracle (`src/oracle.rs`), used by the tests and for the exact capture reported at a refused pose.

The upstream documentation in `sqverify_fast/` (`README.md`, `SOUNDNESS.md`,
`INDEPENDENCE.md`, `independence-record.yaml`) describes the upstream net verifier. It does
not cover the continuous mode, which `CONTINUOUS.md` documents.

## Relation to Guzhou0806/n40-square-packing

[Guzhou0806/n40-square-packing](https://github.com/Guzhou0806/n40-square-packing) (MIT) has
its own continuous-pose kernel, `verifier/continuous_pose.cpp`. It was the first to prove an
n = 40 bound over all angles this way (commit `71c97d0`, s(40) > 1340000/199529).

- This mode shares no code with that kernel. It is Rust, written on top of the upstream
  crate above.
- Its author read `continuous_pose.cpp` while reviewing it (see jlevy/squares#485) before
  writing this mode. The two share the same outline:
  - a branch and bound over (u, v, t = tan(θ/2)) with centre x = L/2 + uE(t);
  - a lower bound from concave sections;
  - translation derivatives;
  - an axis-aligned patch near t = 0.

  They differ in the details listed in `README.md`.
- So this is independent code, but not an independent method.
- No file of that repository is included here. `examples/n40/prepare.py` downloads its two
  density files at fixed commits and checks their SHA-256.

## Version

| version | source_sha256 (printed in every summary) | change |
|---|---|---|
| v3 | `1266a8b90f9a355d74772e211a7b9a52d0236b0d33cc4113d2f897d8a1044f33` | first published version |
| v4 | `619b3c00bd918b329b4141c24ee30b027af7f88b86bcf2886e3c18855a61c7f5` | `--resume`: take over verified root ranges of an earlier run (matched by `run_key`); root lines are written as each range ends and carry `run_key`. The search and every verdict are unchanged from v3 |

v3 was the first published version. The same mode was used before publication as v2
(`a8668d70…`). v3 differs from v2 only in the following, and the n = 40 results were
re-run with v3:

- `cargo fmt`;
- three clippy fixes:
  - a NaN-safe comparison written with `partial_cmp`;
  - an `if let` in place of a single-arm `match`;
  - removing redundant casts in a test.

The `source_sha256` covers `Cargo.toml`, `Cargo.lock`, `build.rs` and every `src/*.rs`. A
stray file such as a macOS `._*.rs` in `src/` changes it without changing the code.

## Licences

The code in `sqverify_fast/` is MIT: upstream code by Joshua Levy, our changes under this
repository's MIT licence.

Its upstream documentation (`README.md`, `SOUNDNESS.md`, `INDEPENDENCE.md`,
`independence-record.yaml`) is CC BY 4.0: "Joshua Levy, the squares project
(https://github.com/jlevy/squares)".

`CONTINUOUS.md`, this file, `README.md`, `patches/` and `examples/` are ours (MIT). See
`../THIRD_PARTY_NOTICES.md`.
