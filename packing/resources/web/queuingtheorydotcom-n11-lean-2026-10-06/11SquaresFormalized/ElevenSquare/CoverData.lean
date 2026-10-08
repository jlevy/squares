import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.VecNotation

/-! The sixteen rational sites, in the unchanged source order. Closed cells are
nearest-site Voronoi cells intersected with the unit square. The dyadic witness
used to verify their covering radius does not change these cells. -/
noncomputable section
namespace ElevenSquare

def coverSite (i : Fin 16) : ℝ × ℝ :=
  (![((104991 / 1000000), (265837 / 2000000)),
    ((186601 / 500000), (45503 / 1000000)),
    ((1267243 / 2000000), (34689 / 250000)),
    ((1731123 / 2000000), (25701 / 250000)),
    ((206181 / 2000000), (400379 / 1000000)),
    ((742311 / 2000000), (312933 / 1000000)),
    ((635257 / 1000000), (166409 / 400000)),
    ((445439 / 500000), (167763 / 500000)),
    ((54561 / 500000), (332237 / 500000)),
    ((364743 / 1000000), (233591 / 400000)),
    ((1257689 / 2000000), (687067 / 1000000)),
    ((1793819 / 2000000), (599621 / 1000000)),
    ((268877 / 2000000), (224299 / 250000)),
    ((732757 / 2000000), (215311 / 250000)),
    ((313399 / 500000), (954497 / 1000000)),
    ((895009 / 1000000), (1734163 / 2000000))] : Fin 16 → ℝ × ℝ) i

def coverRadius : ℝ := 173 / 1000

def coverCap : ℝ := 387708359002281417731 / 100000000000000000000

end ElevenSquare
end
