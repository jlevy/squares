import S12.ShortCluster.Projections

namespace S12
open S12Pilot
set_option maxHeartbeats 0

/-- Base five-point implication, first endpoint. All 64 excluding-face choices
are covered, with strict interior and boundary exterior conventions. -/
theorem five_point_left (q : OpenSquare) (ha : 1 < q.side)
    (h0 : q.Inside (33/20) (33/20)) (h1 : q.Inside 1 (113/50)) :
    q.Inside 1 (87/50) ∨ q.Inside (33/20) (47/20) ∨ q.Inside 2 (87/50) := by
  have d01 := short_projections q (1-33/20) (87/50-47/20) (by norm_num)
  have d02 := short_projections q (1-2) (87/50-87/50) (by norm_num)
  have d12 := short_projections q (33/20-2) (47/20-87/50) (by norm_num)
  rcases d01 with ⟨d0,d1,d2,d3⟩
  rcases d02 with ⟨d4,d5,d6,d7⟩
  rcases d12 with ⟨d8,d9,d10,d11⟩
  rcases h0 with ⟨a0,a1,a2,a3⟩
  rcases h1 with ⟨b0,b1,b2,b3⟩
  cancel_denoms at d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11 a0 a1 a2 a3 b0 b1 b2 b3
  by_contra he
  simp only [OpenSquare.Inside, InBands, not_or, not_and_or, not_lt] at he
  rcases he with ⟨he0,he1,he2⟩
  rcases he0 with e0 | e0 | e0 | e0 <;>
    rcases he1 with e1 | e1 | e1 | e1 <;>
    rcases he2 with e2 | e2 | e2 | e2 <;>
    (cancel_denoms at e0 e1 e2
     linarith (config := { oracle := .simplexAlgorithmDense }) only
       [ha,d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,a0,a1,a2,a3,b0,b1,b2,b3,e0,e1,e2])


end S12
