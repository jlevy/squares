import S12.ShortCluster.Projections

namespace S12
open S12Pilot
set_option maxHeartbeats 0

/-- The side six-point template. -/
theorem side_six_point (q : OpenSquare) (ha : 1 < q.side)
    (h0 : q.Inside (457/500) 2) (h1 : q.Inside 1 (87/50))
    (h2 : q.Inside (87/50) 2) :
    q.Inside 1 (8/5) ∨ q.Inside 1 (12/5) ∨ q.Inside (33/20) (33/20) := by
  have d01 := short_projections q (1-1) (8/5-12/5) (by norm_num)
  have d02 := short_projections q (1-33/20) (8/5-33/20) (by norm_num)
  have d12 := short_projections q (1-33/20) (12/5-33/20) (by norm_num)
  rcases d01 with ⟨d0,d1,d2,d3⟩
  rcases d02 with ⟨d4,d5,d6,d7⟩
  rcases d12 with ⟨d8,d9,d10,d11⟩
  rcases h0 with ⟨a0,a1,a2,a3⟩
  rcases h1 with ⟨b0,b1,b2,b3⟩
  rcases h2 with ⟨c0,c1,c2,c3⟩
  cancel_denoms at d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11 a0 a1 a2 a3 b0 b1 b2 b3 c0 c1 c2 c3
  by_contra he
  simp only [OpenSquare.Inside, InBands, not_or, not_and_or, not_lt] at he
  rcases he with ⟨he0,he1,he2⟩
  rcases he0 with e0 | e0 | e0 | e0 <;>
    rcases he1 with e1 | e1 | e1 | e1 <;>
    rcases he2 with e2 | e2 | e2 | e2 <;>
    (cancel_denoms at e0 e1 e2
     linarith (config := { oracle := .simplexAlgorithmDense }) only
       [ha,d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,a0,a1,a2,a3,b0,b1,b2,b3,c0,c1,c2,c3,e0,e1,e2])

end S12
