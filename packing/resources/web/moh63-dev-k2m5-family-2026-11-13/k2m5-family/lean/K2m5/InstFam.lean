import K2m5.Fam10
import K2m5.InstData
/-! The `k² − 5` family as a `Fam10.Fam` (`R = 4`, Lebesgue from `38/10`, masses in units `1/(2·10¹²)`). -/
namespace SquarePacking
namespace K2m5Inst
open Fam10
def fam5 : Fam where
  R := 4
  A := 38
  den := 2000000000000
  tab := famTab
  tab2 := famTab2
theorem fam5_out : OutZero fam5 := by decide +kernel
end K2m5Inst
end SquarePacking

namespace SquarePacking
namespace K2m5Inst
open Fam10
/-- The keys of `gridKeys fam5 11` with orientation `o` (for splitting the kernel check in two). -/
def gkPart (o : Bool) : List ℕ :=
  (((List.range (10 * 11 + 1)).flatMap fun (i : ℕ) => (List.range (10 * 11 + 1)).flatMap fun (j : ℕ) =>
      [false, true].map fun b => ((o, (i : ℤ), (j : ℤ)), b)).filter fun s => wN fam5 11 s != 0).map keyN

theorem gridKeys_split : gridKeys fam5 11 = gkPart false ++ gkPart true := by
  simp only [gridKeys, gridList, gkPart, List.flatMap_cons, List.flatMap_nil, List.append_nil,
    List.filter_append, List.map_append]
end K2m5Inst
end SquarePacking
