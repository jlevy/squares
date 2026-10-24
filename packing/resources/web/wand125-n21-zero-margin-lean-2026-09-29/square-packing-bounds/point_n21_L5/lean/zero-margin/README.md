# Hypothesis-free Lean proof of the point-only s(21) = 5

```lean
theorem SquarePacking.n21pts_eq_5 : minSide 21 = 5
-- depends on axioms: [propext, Classical.choice, Quot.sound]
```

The [reduction in `../`](../README.md) proves `minSide 21 = 5` from one computational hypothesis, the
capture bound. This directory removes that hypothesis. It follows Evan Daniel's zero-margin route, which
he used for `s(13) = 4` and `s(32) = 6`:

- the certificate is `../../certificates/n21-capture-one.txt`, the point-only cover normalised so that
  every closed unit square in `[0,5]^2` captures weight at least 1 (4,604 entries, weights
  `w/999948000000`, total `20998900000168/999948000000 < 21`);
- his generator `lean/scripts/gen_zmtree.py` (untrusted, deterministic) builds a zero-margin box tree over
  the D4 roots: 59,433 `Z` leaves (22,016 ADM, 13,526 one-chain, 23,891 two-chain), 5,876 `E` leaves and
  5,591 clips, in 2,076 chunks split over 64 files;
- every chunk is `decide +kernel` of his `ZMTree.check`, proved sound once (`ZMTree.sound`);
- `N21PtsLower.lean` applies his generic `BoxTree.le_minSide` (as in his `S13Lower.lean`) for
  `5 ≤ minSide 21`, and the 5×5 grid (`packs_grid`) for the equality.

Only `N21PtsLower.lean`, the axiom report and the build script are ours. The Lean library and the generator
are fetched from [evand/square-packing](https://github.com/evand/square-packing) at the pinned commit
`6aa82ba457e9eaeaaa3af0833600f27f91a2fce3` (MIT; see `../../UPSTREAM-LICENSE.txt`). The generated data
(88 MB) is not distributed. It is regenerated, and `data-sha256.txt` lists the hashes of the 66 generated
files for comparison.

## Reproduce

Needs `git`, Python 3 with `numpy`, and [elan](https://github.com/leanprover/elan). From this directory:

```sh
sh build_zero_margin.sh /tmp/n21-zero-margin 2 4    # new directory; 2 parts built at once; 4 generator workers
```

The script pins the upstream commit and checks the hashes of the generator, its oracle, `ZMTree.lean` and
the certificate. It regenerates the tree, compares the data with `data-sha256.txt`, downloads the Mathlib
cache, and builds all 64 parts and `Sqpack.N21PtsLower`. It then requires the axiom report to be exactly the
three standard axioms, and ends with `N21_POINTS_HYPOTHESIS_FREE_VERIFIED`.

Reference runs on an Apple M4 under heavy unrelated load: generation 1,459 s wall (6 workers); the kernel
check took about 3.5 h wall with 2 parts at a time, peaking near 6 GB per part. `build_zero_margin.sh`
was also run end to end from an empty directory: the regenerated data matched `data-sha256.txt` and it
ended with `N21_POINTS_HYPOTHESIS_FREE_VERIFIED`.

This is a proof-assistant proof of the point-only bound. The certificate itself came from the
computer-assisted search described in `../../README.md`; the rational replay there is no longer needed for
the theorem, but is kept as an independent check.
