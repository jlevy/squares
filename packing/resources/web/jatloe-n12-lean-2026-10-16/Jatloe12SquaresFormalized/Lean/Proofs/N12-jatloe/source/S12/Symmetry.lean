import S12.SymmetryBase
import S12.ShortCluster

namespace S12
open S12Pilot

/-- Both five-point templates at all eight container symmetries. -/
theorem five_point_transformed (g : Transform) (q : OpenSquare) (ha : 1 < q.side)
    (right : Bool)
    (h0 : (g.pull q).Inside (33/20) (33/20))
    (h1 : (g.pull q).Inside (if right then 2 else 1) (113/50)) :
    (g.pull q).Inside 1 (87/50) ∨ (g.pull q).Inside (33/20) (47/20) ∨
    (g.pull q).Inside 2 (87/50) := by
  have hs : 1 < (g.pull q).side := by simpa using ha
  cases right
  · exact five_point_left _ hs h0 h1
  · exact five_point_right _ hs h0 h1

/-- All eight copies of the side six-point template. `inside_pull` gives
exactly the transformed coordinates used by the classifier. -/
theorem six_point_transformed (g : Transform) (q : OpenSquare) (ha : 1 < q.side)
    (h0 : (g.pull q).Inside (457/500) 2)
    (h1 : (g.pull q).Inside 1 (87/50))
    (h2 : (g.pull q).Inside (87/50) 2) :
    (g.pull q).Inside 1 (8/5) ∨ (g.pull q).Inside 1 (12/5) ∨
    (g.pull q).Inside (33/20) (33/20) := by
  exact side_six_point _ (by simpa using ha) h0 h1 h2

#print axioms inside_pull
#print axioms five_point_transformed
#print axioms six_point_transformed
end S12
