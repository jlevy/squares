# Lean 4 reduction for the point-only s(21) = 5 certificate

This directory formalises everything in the point-only proof **except** the
all-pose capture computation. It is a conditional result, at the same level as
Evan Daniel's Lean treatment of his own s(21) certificate:

```lean
theorem n21pts_eq_five (h : N21PtsRegionCover) : minSide 21 = 5
theorem n21pts_eq_five_of_checker (h : N21PtsCheckerCover) : minSide 21 = 5
```

The single hypothesis is the capture bound. `N21PtsCheckerCover` states that every
closed unit square with centre in `[0,5/2]^2` and angle `2 arctan t`,
`t ∈ [0,5/12]`, lying in the side-5 box has point mass at least
`q = 249987/250000`. That is the domain checked by the rational replay in the
parent directory; the replay itself is not formalised. Both theorems depend only
on the standard axioms `propext`, `Classical.choice` and `Quot.sound`.

Proved in Lean, by kernel evaluation where data is involved:

- the point data, generated exactly from `../certificates/n21-original.txt`
  (SHA256 `84a7dae7…`, 4,604 entries);
- total mass `2624862500021/125000000000`, nonnegativity and D4 invariance;
- normalisation by `q`, giving total normalised mass below 21;
- sufficiency of `t ≤ 5/12` for all angles (`tan(π/8) < 5/12`) and the D4
  reduction from the checker domain to all poses;
- the scaling argument excluding every side below 5, and the 5-by-5 grid
  packing for the matching upper bound.

## Files

Only our additions are distributed here:

- `Sqpack/N21PtsData.lean` — generated point data;
- `Sqpack/N21Pts.lean` — the reduction and the theorems above;
- `Sqpack/N21PtsAxioms.lean` — `#print axioms` for both theorems;
- `scripts/gen_n21pts_data.py` — exact generator (no floating point); the
  `Source:` line in the generated header records the original research path;
- `build_lean.sh` — reproducible overlay build.

They build on Evan Daniel's unmodified Lean project `s12/lean` at
[evand/square-packing](https://github.com/evand/square-packing) commit
`6e1223cf7ef2be4c70baaa36c0e7e7197076735a` (MIT; see `../UPSTREAM-LICENSE.txt`),
which is fetched rather than copied. The only upstream edit is appending two
import lines to `Sqpack.lean`, whose original SHA256 is checked first.

## Reproduce

Requires `git`, Python 3, and [elan](https://github.com/leanprover/elan)
(the toolchain `leanprover/lean4:v4.33.1` is selected by the upstream project).
From this directory:

```sh
sh build_lean.sh /tmp/n21-lean-build
```

The work directory must not exist. The script clones and pins the upstream
commit, overlays the files, regenerates the data with `--check`, rejects
`sorry`, `native_decide` and `axiom` declarations in the overlay, downloads
the Mathlib cache, runs `lake build`, and requires both axiom reports to be
exactly the three standard axioms. It ends with `LEAN_OVERLAY_BUILD_VERIFIED`.
A fresh run from an empty directory on an Apple M4 took about 24 minutes and
about 8 GB of disk, mostly the Mathlib checkout and cache.

This reduction alone is not a complete formal proof. The capture hypothesis is
discharged by the rational replay described in `../README.md`, and, inside Lean,
by the hypothesis-free proof in [zero-margin/](zero-margin/README.md).
