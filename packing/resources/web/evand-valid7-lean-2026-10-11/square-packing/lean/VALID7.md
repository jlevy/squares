# Valid7 in the kernel

`Sqpack/V7/Main.lean` (generated) proves

```lean
theorem valid7 : Bentz.Valid7
theorem bentz : ∀ k : ℕ, 6 ≤ k → minSide (k ^ 2 - 3) = k   -- Bentz.bentz_of_valid7 valid7
theorem validTilt7 : Bentz.ValidTilt7                        -- the open part of ValidSplit7.lean
```

in namespace `SquarePacking.LemmaELeaf`, with

```
'SquarePacking.LemmaELeaf.valid7' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePacking.LemmaELeaf.bentz' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePacking.LemmaELeaf.validTilt7' depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorry`, no `native_decide`, no new axioms.

## Certificates

The 9,800 per-root certificates (one pickle per root of the k2m3 tree, from `scripts/run_v7.py`) are
not in the repository. They are in the release
<https://github.com/wand125/square-packing/releases/tag/data/valid7-lean-certs-v1>:
`v7cert.tar.zst` (the directory `v7cert/` and the list `v7cert.sha256`), with SHA-256 sums of every
file. The certificates are Python pickles: load them only after checking the sums.

## Rebuilding

From `lean/`, with the certificates unpacked into `v7cert/`:

1. `lake build Sqpack.V7.Bridge` and `python3 scripts/gen_face.py Sqpack/V7/Face.lean && lake build Sqpack.V7.Face`.
2. Root modules: `python3 scripts/emit_v7.py --cert DIR --chunk 40 --nproc N`. The checked build
   emitted the roots listed in `scripts/v7_xroots.txt` with `V7_X=1` (EXACT leaves through
   `LemmaELeafX`, which avoids enumerating the segment alternatives) and the other roots without it;
   use the same split (for example, `--cert` directories of symlinks to each group's pickles).
3. Kernel checks of the roots: `python3 scripts/runB.py --lo 0 --hi 9800 --jobs J` (one `lean` per
   module into `.lake/build`; `--mem/--floor/--guard` bound the memory).
4. `python3 scripts/gen_main.py`, then `lake env lean -o .lake/build/lib/lean/Sqpack/V7/Main.olean Sqpack/V7/Main.lean`,
   then `#print axioms` on `SquarePacking.LemmaELeaf.valid7`, `.bentz` and `.validTilt7`.

Measured on 64-core, 512 GB machines (at most 55 `lean` processes each): all 9,800 roots passed;
`Face` 9 min (47 GB), `Bridge` 7 min (24 GB), `Main` 2 min 17 s (58 GB). The root checks are the bulk
of the cost (roughly 10^4 CPU-hours in total).
