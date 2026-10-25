import S12.GeneralWall
import Mathlib.Tactic.Positivity
namespace S12
open S12Pilot
set_option maxHeartbeats 0
noncomputable def wallCubic (w delta t : ℝ) : ℝ := (1-w)+(2*delta-1)*t+(1+w)*t^2-t^3

theorem wall088_0 (t : ℝ) (h0 : 0≤t) (h1 : t≤(1/4)) :
    0≤wallCubic (22/25) (43/500) t := by
  have hl : 0≤t-0 := sub_nonneg.mpr h0
  have hu : 0≤(1/4)-t := sub_nonneg.mpr h1
  have hid : wallCubic (22/25) (43/500) t = (192/25)*(t-0)^0*((1/4)-t)^3 + (1224/125)*(t-0)^1*((1/4)-t)^2 + (508/125)*(t-0)^2*((1/4)-t)^1 + (119/125)*(t-0)^3*((1/4)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall088_1 (t : ℝ) (h0 : (1/4)≤t) (h1 : t≤(1/2)) :
    0≤wallCubic (22/25) (43/500) t := by
  have hl : 0≤t-(1/4) := sub_nonneg.mpr h0
  have hu : 0≤(1/2)-t := sub_nonneg.mpr h1
  have hid : wallCubic (22/25) (43/500) t = (119/125)*(t-(1/4))^0*((1/2)-t)^3 + (206/125)*(t-(1/4))^1*((1/2)-t)^2 + (124/25)*(t-(1/4))^2*((1/2)-t)^1 + (408/125)*(t-(1/4))^3*((1/2)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall088_2 (t : ℝ) (h0 : (1/2)≤t) (h1 : t≤(3/4)) :
    0≤wallCubic (22/25) (43/500) t := by
  have hl : 0≤t-(1/2) := sub_nonneg.mpr h0
  have hu : 0≤(3/4)-t := sub_nonneg.mpr h1
  have hid : wallCubic (22/25) (43/500) t = (408/125)*(t-(1/2))^0*((3/4)-t)^3 + (1828/125)*(t-(1/2))^1*((3/4)-t)^2 + (2622/125)*(t-(1/2))^2*((3/4)-t)^1 + (1077/125)*(t-(1/2))^3*((3/4)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall088_3 (t : ℝ) (h0 : (3/4)≤t) (h1 : t≤1) :
    0≤wallCubic (22/25) (43/500) t := by
  have hl : 0≤t-(3/4) := sub_nonneg.mpr h0
  have hu : 0≤1-t := sub_nonneg.mpr h1
  have hid : wallCubic (22/25) (43/500) t = (1077/125)*(t-(3/4))^0*(1-t)^3 + (768/25)*(t-(3/4))^1*(1-t)^2 + (4264/125)*(t-(3/4))^2*(1-t)^1 + (1376/125)*(t-(3/4))^3*(1-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall088_nonnegative (t : ℝ) (h0 : 0≤t) (h1 : t≤1) :
    0≤wallCubic (22/25) (43/500) t := by
  by_cases h2 : t≤(1/4)
  · exact wall088_0 t (by linarith) h2
  by_cases h3 : t≤(1/2)
  · exact wall088_1 t (by linarith) h3
  by_cases h4 : t≤(3/4)
  · exact wall088_2 t (by linarith) h4
  exact wall088_3 t (by linarith) h1

theorem wall0956_0 (t : ℝ) (h0 : 0≤t) (h1 : t≤(1/8)) :
    0≤wallCubic (239/250) (6/25) t := by
  have hl : 0≤t-0 := sub_nonneg.mpr h0
  have hu : 0≤(1/8)-t := sub_nonneg.mpr h1
  have hid : wallCubic (239/250) (6/25) t = (2816/125)*(t-0)^0*((1/8)-t)^3 + (4288/125)*(t-0)^1*((1/8)-t)^2 + (2084/125)*(t-0)^2*((1/8)-t)^1 + (487/125)*(t-0)^3*((1/8)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall0956_1 (t : ℝ) (h0 : (1/8)≤t) (h1 : t≤(1/4)) :
    0≤wallCubic (239/250) (6/25) t := by
  have hl : 0≤t-(1/8) := sub_nonneg.mpr h0
  have hu : 0≤(1/4)-t := sub_nonneg.mpr h1
  have hid : wallCubic (239/250) (6/25) t = (487/125)*(t-(1/8))^0*((1/4)-t)^3 + (838/125)*(t-(1/8))^1*((1/4)-t)^2 + (1796/125)*(t-(1/8))^2*((1/4)-t)^1 + (264/25)*(t-(1/8))^3*((1/4)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall0956_2 (t : ℝ) (h0 : (1/4)≤t) (h1 : t≤(3/8)) :
    0≤wallCubic (239/250) (6/25) t := by
  have hl : 0≤t-(1/4) := sub_nonneg.mpr h0
  have hu : 0≤(3/8)-t := sub_nonneg.mpr h1
  have hid : wallCubic (239/250) (6/25) t = (264/25)*(t-(1/4))^0*((3/8)-t)^3 + (6124/125)*(t-(1/4))^1*((3/8)-t)^2 + (9494/125)*(t-(1/4))^2*((3/8)-t)^1 + (913/25)*(t-(1/4))^3*((3/8)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall0956_3 (t : ℝ) (h0 : (3/8)≤t) (h1 : t≤(1/2)) :
    0≤wallCubic (239/250) (6/25) t := by
  have hl : 0≤t-(3/8) := sub_nonneg.mpr h0
  have hu : 0≤(1/2)-t := sub_nonneg.mpr h1
  have hid : wallCubic (239/250) (6/25) t = (913/25)*(t-(3/8))^0*((1/2)-t)^3 + (17896/125)*(t-(3/8))^1*((1/2)-t)^2 + (22928/125)*(t-(3/8))^2*((1/2)-t)^1 + (9472/125)*(t-(3/8))^3*((1/2)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall0956_4 (t : ℝ) (h0 : (1/2)≤t) (h1 : t≤(5/8)) :
    0≤wallCubic (239/250) (6/25) t := by
  have hl : 0≤t-(1/2) := sub_nonneg.mpr h0
  have hu : 0≤(5/8)-t := sub_nonneg.mpr h1
  have hid : wallCubic (239/250) (6/25) t = (9472/125)*(t-(1/2))^0*((5/8)-t)^3 + (33904/125)*(t-(1/2))^1*((5/8)-t)^2 + (39848/125)*(t-(1/2))^2*((5/8)-t)^1 + (15291/125)*(t-(1/2))^3*((5/8)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall0956_5 (t : ℝ) (h0 : (5/8)≤t) (h1 : t≤(3/4)) :
    0≤wallCubic (239/250) (6/25) t := by
  have hl : 0≤t-(5/8) := sub_nonneg.mpr h0
  have hu : 0≤(3/4)-t := sub_nonneg.mpr h1
  have hid : wallCubic (239/250) (6/25) t = (15291/125)*(t-(5/8))^0*((3/4)-t)^3 + (51898/125)*(t-(5/8))^1*((3/4)-t)^2 + (58004/125)*(t-(5/8))^2*((3/4)-t)^1 + (21272/125)*(t-(5/8))^3*((3/4)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall0956_6 (t : ℝ) (h0 : (3/4)≤t) (h1 : t≤(7/8)) :
    0≤wallCubic (239/250) (6/25) t := by
  have hl : 0≤t-(3/4) := sub_nonneg.mpr h0
  have hu : 0≤(7/8)-t := sub_nonneg.mpr h1
  have hid : wallCubic (239/250) (6/25) t = (21272/125)*(t-(3/4))^0*((7/8)-t)^3 + (69628/125)*(t-(3/4))^1*((7/8)-t)^2 + (75146/125)*(t-(3/4))^2*((7/8)-t)^1 + (5333/25)*(t-(3/4))^3*((7/8)-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall0956_7 (t : ℝ) (h0 : (7/8)≤t) (h1 : t≤1) :
    0≤wallCubic (239/250) (6/25) t := by
  have hl : 0≤t-(7/8) := sub_nonneg.mpr h0
  have hu : 0≤1-t := sub_nonneg.mpr h1
  have hid : wallCubic (239/250) (6/25) t = (5333/25)*(t-(7/8))^0*(1-t)^3 + (84844/125)*(t-(7/8))^1*(1-t)^2 + (89024/125)*(t-(7/8))^2*(1-t)^1 + (6144/25)*(t-(7/8))^3*(1-t)^0 := by
    dsimp [wallCubic]; ring
  rw [hid]
  positivity

theorem wall0956_nonnegative (t : ℝ) (h0 : 0≤t) (h1 : t≤1) :
    0≤wallCubic (239/250) (6/25) t := by
  by_cases h2 : t≤(1/8)
  · exact wall0956_0 t (by linarith) h2
  by_cases h3 : t≤(1/4)
  · exact wall0956_1 t (by linarith) h3
  by_cases h4 : t≤(3/8)
  · exact wall0956_2 t (by linarith) h4
  by_cases h5 : t≤(1/2)
  · exact wall0956_3 t (by linarith) h5
  by_cases h6 : t≤(5/8)
  · exact wall0956_4 t (by linarith) h6
  by_cases h7 : t≤(3/4)
  · exact wall0956_5 t (by linarith) h7
  by_cases h8 : t≤(7/8)
  · exact wall0956_6 t (by linarith) h8
  exact wall0956_7 t (by linarith) h1

#print axioms wall088_nonnegative
#print axioms wall0956_nonnegative
end S12
