import Sqpack.SpecBridge
import Sqpack.SpecFC
import Sqpack.S11Lower
import Sqpack.S12HLower
import Sqpack.S13Lower

/-!
# The headline results in the canonical shapes of `Sqpack/Spec.lean`

`s(13) = 4` (exact), `s(12) ≥ 15680/3951`, `s(11) ≥ 3040/797`, stated for
`UnitSquarePacking.Packs` with no hypothesis; and `s13_fc`, `s(13) = 4` in formal-conjectures'
formulation (via `Sqpack/SpecFC.lean`).

Opt-in (not imported by `Sqpack.lean`): needs the generated data sets `S11`, `S12H`, `S13`
(`lean/scripts/gen_data.sh`), built as `LADDER.md` describes, then `lake build Sqpack.SpecHeadline`.

`s(32) = 6` follows the same way from `Sqpack/S32Lower.lean` (data `S32Z`, opt-in); with
`import Sqpack.S32Lower` added above it is the one-liner
```
theorem s32 : IsLeast {s | Packs 32 s} 6 := s32_isLeast_of_checker SquarePacking.s32_checkerCover
```
-/

namespace UnitSquarePacking

/-- **`s(13) = 4`**: 13 unit squares fit in `[0,4]²` and in no smaller square. -/
theorem s13 : IsLeast {s | Packs 13 s} 4 :=
  isLeast_of_le_minSide (by norm_num) (minSide_eq 13 ▸ SquarePacking.s13_ge_4)
    (by simpa using packs_grid 4 13 (by norm_num))

/-- **`s(12) ≥ 15680/3951 = 3.968616…`**. -/
theorem s12_lower : ∀ s, Packs 12 s → (15680 / 3951 : ℝ) ≤ s :=
  lower_of_le_minSide (by norm_num) (minSide_eq 12 ▸ SquarePacking.s12_ge_15680_3951)

/-- **`s(11) ≥ 3040/797 = 3.8143036…`**. -/
theorem s11_lower : ∀ s, Packs 11 s → (3040 / 797 : ℝ) ≤ s :=
  lower_of_le_minSide (by norm_num) (minSide_eq 11 ▸ SquarePacking.s11_ge_3040_797)

/-- **`s(13) = 4`** for formal-conjectures' definitions (`Sqpack/FCSquarePacking.lean`): open unit
squares placed by isometries of `EuclideanSpace ℝ (Fin 2)` in the open square `(0, x)²`. -/
theorem s13_fc : IsLeast {x : ℝ | Nonempty (FCSquarePacking.Packing 13 FCSquarePacking.UnitSquare
    (FCSquarePacking.Square x))} 4 :=
  setOf_packs_eq 13 ▸ s13

end UnitSquarePacking
