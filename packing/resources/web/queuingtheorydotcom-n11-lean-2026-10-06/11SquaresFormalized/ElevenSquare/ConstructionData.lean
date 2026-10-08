import ElevenSquare.Endpoint
import ElevenSquare.Geometry
import Mathlib.Data.Fin.VecNotation

/-!
Exact coordinates in Q(u). The generator produces identities and Bernstein
positivity witnesses; Lean checks them using `ring` and `positivity`.
No result of the Python generator is trusted without those proofs.
-/
namespace ElevenSquare
noncomputable section
set_option maxHeartbeats 4000000

theorem construction_u_bounds : (3657/10000 : ℝ) < u ∧ u < 3658/10000 := by
  have h := u_bounds
  norm_num [rootLo, rootHi] at h ⊢
  constructor <;> linarith

def constructionCos : ℝ := (1 / 4) * u^7 - (5 / 8) * u^6 - (1 / 10) * u^5 + (11 / 8) * u^4 + (7 / 20) * u^3 - (79 / 40) * u^2 - (1 / 10) * u + (41 / 40)
def constructionSin : ℝ := - (1 / 8) * u^7 + (27 / 40) * u^5 - (1 / 4) * u^4 - (67 / 40) * u^3 - (1 / 5) * u^2 + (77 / 40) * u + (1 / 20)
def constructionSide : ℝ := (25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + (5 / 2)

theorem construction_cos_pos : 0 < constructionCos := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionCos = ((30563207104367442892320062993 / 4) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (106968896094710022084363420047 / 2) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 160449850919207615689513013477 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 267410596048945765805207126230 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 267404773787592002227842476620 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 160439370848781478299292561768 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 53478625786018975879851281264 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 7639637323828199373605389088 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    dsimp only [constructionCos, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_sin_pos : 0 < constructionSin := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSin = ((51611161927044375654218712007 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (180643530973246983141518017453 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (270971992417699694649877636523 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 225815573325380031055900249385 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 225821152648437423964863511690 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 135496038990345858120241169116 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 45166462066356977959634359368 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 6452511105487161244693105456 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    dsimp only [constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_cos_sq_add_sin_sq : constructionCos^2 + constructionSin^2 = 1 := by
  have hz : constructionCos^2 + constructionSin^2 - 1 = 0 := by
    have hid : constructionCos^2 + constructionSin^2 - 1 = ((1 / 64) * u^6 - (1 / 32) * u^5 - (7 / 320) * u^4 + (3 / 40) * u^3 + (19 / 320) * u^2 - (3 / 32) * u - (17 / 320)) * endpointPolynomial u := by
      dsimp only [constructionCos, constructionSin, endpointPolynomial]
      ring
    rw [hid, u_polynomial, mul_zero]
  linarith

theorem constructionSide_eq_T : constructionSide = T := by
  dsimp only [T]
  apply (eq_div_iff (ne_of_gt endpoint_denominator_pos)).mpr
  have hid : (6*u+4) - constructionSide * (1+2*u-u^2) =
      ((5 / 8) * u - (3 / 2)) * endpointPolynomial u := by
    dsimp only [constructionSide, endpointPolynomial]
    ring
  rw [u_polynomial, mul_zero] at hid
  linarith

def constructionCenter : Fin 11 → Point :=
  ![((1 / 2), (1 / 2)),
    ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2, (1 / 2)),
    ((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2, (25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2),
    ((1 / 2), (25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2),
    ((3 / 2), (25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2),
    ((1 / 2), (25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1),
    ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400), (79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400)),
    ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80), (1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80)),
    ((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400), (191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400)),
    ((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400), (117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400)),
    ((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80), (43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80))]

def constructionAxis (tilted : Bool) : Point :=
  if tilted then (constructionCos, constructionSin) else (1, 0)

theorem constructionAxis_unit (tilted : Bool) : normSq (constructionAxis tilted) = 1 := by
  cases tilted
  · norm_num [constructionAxis, normSq, dot]
  · simpa [constructionAxis, normSq, dot, sq] using construction_cos_sq_add_sin_sq

def constructionSquare (i : Fin 11) : UnitSquare :=
  ⟨constructionCenter i, constructionAxis (decide (6 ≤ i.val)),
    constructionAxis_unit _⟩

def constructionSeparator : Fin 4 → Point :=
  ![(1,0), (0,1), (constructionCos, constructionSin), (-constructionSin, constructionCos)]

def constructionRadius (i : Fin 11) : ℝ :=
  if i.val < 6 then 1/2 else (constructionCos + constructionSin)/2

def constructionSepRadius (i : Fin 11) (k : Fin 4) : ℝ :=
  if decide (i.val < 6) = decide (k.val < 2) then 1/2 else (constructionCos + constructionSin)/2

theorem construction_bound_0_0_0 : 0 ≤ (constructionCenter 0).1 - constructionRadius 0 := by
  have hid : (constructionCenter 0).1 - constructionRadius 0 = (0) * endpointPolynomial u := by
    change ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_0_0_1 : 0 ≤ constructionSide - (constructionCenter 0).1 - constructionRadius 0 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 0).1 - constructionRadius 0 = ((230143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (805518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1208302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 1006940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 1006961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 604189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 201400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 28772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_0_1_0 : 0 ≤ (constructionCenter 0).2 - constructionRadius 0 := by
  have hid : (constructionCenter 0).2 - constructionRadius 0 = (0) * endpointPolynomial u := by
    change ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_0_1_1 : 0 ≤ constructionSide - (constructionCenter 0).2 - constructionRadius 0 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 0).2 - constructionRadius 0 = ((230143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (805518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1208302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 1006940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 1006961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 604189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 201400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 28772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_1_0_0 : 0 ≤ (constructionCenter 1).1 - constructionRadius 1 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 1).1 - constructionRadius 1 = ((230143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (805518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1208302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 1006940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 1006961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 604189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 201400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 28772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_1_0_1 : 0 ≤ constructionSide - (constructionCenter 1).1 - constructionRadius 1 := by
  have hid : constructionSide - (constructionCenter 1).1 - constructionRadius 1 = (0) * endpointPolynomial u := by
    change constructionSide - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_1_1_0 : 0 ≤ (constructionCenter 1).2 - constructionRadius 1 := by
  have hid : (constructionCenter 1).2 - constructionRadius 1 = (0) * endpointPolynomial u := by
    change ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_1_1_1 : 0 ≤ constructionSide - (constructionCenter 1).2 - constructionRadius 1 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 1).2 - constructionRadius 1 = ((230143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (805518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1208302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 1006940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 1006961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 604189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 201400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 28772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_2_0_0 : 0 ≤ (constructionCenter 2).1 - constructionRadius 2 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 2).1 - constructionRadius 2 = ((40649188169818456990100314965 / 2) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 142273585414264103272817100235 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 426825037043603815934380134770 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 711382196975989813854571262300 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 711389332781380166188424766200 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 426837881493372024084925617680 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 142280721219763745522512812640 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 20326021246031014928053890880 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_2_0_1 : 0 ≤ constructionSide - (constructionCenter 2).1 - constructionRadius 2 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 2).1 - constructionRadius 2 = ((67546567424263885972061539965 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (236424134693931038397935662735 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (354652925532841610897424417385 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 295558041211039899080764003075 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 295571978168452232445821441550 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 177351549289776664024343954420 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 59119970630917857162068203160 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 8446108319524558098517672720 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_2_1_0 : 0 ≤ (constructionCenter 2).2 - constructionRadius 2 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 2).2 - constructionRadius 2 = ((230143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (805518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1208302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 1006940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 1006961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 604189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 201400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 28772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_2_1_1 : 0 ≤ constructionSide - (constructionCenter 2).2 - constructionRadius 2 := by
  have hid : constructionSide - (constructionCenter 2).2 - constructionRadius 2 = (0) * endpointPolynomial u := by
    change constructionSide - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_3_0_0 : 0 ≤ (constructionCenter 3).1 - constructionRadius 3 := by
  have hid : (constructionCenter 3).1 - constructionRadius 3 = (0) * endpointPolynomial u := by
    change ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_3_0_1 : 0 ≤ constructionSide - (constructionCenter 3).1 - constructionRadius 3 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 3).1 - constructionRadius 3 = ((230143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (805518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1208302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 1006940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 1006961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 604189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 201400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 28772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_3_1_0 : 0 ≤ (constructionCenter 3).2 - constructionRadius 3 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 3).2 - constructionRadius 3 = ((230143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (805518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1208302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 1006940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 1006961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 604189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 201400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 28772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_3_1_1 : 0 ≤ constructionSide - (constructionCenter 3).2 - constructionRadius 3 := by
  have hid : constructionSide - (constructionCenter 3).2 - constructionRadius 3 = (0) * endpointPolynomial u := by
    change constructionSide - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_4_0_0 : 0 ≤ (constructionCenter 4).1 - constructionRadius 4 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 4).1 - constructionRadius 4 = (1 * (u - 3657/10000)^0 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((3 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_4_0_1 : 0 ≤ constructionSide - (constructionCenter 4).1 - constructionRadius 4 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 4).1 - constructionRadius 4 = ((150143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (525518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (788302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 656940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 656961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 394189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 131400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 18772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((3 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_4_1_0 : 0 ≤ (constructionCenter 4).2 - constructionRadius 4 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 4).2 - constructionRadius 4 = ((230143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (805518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1208302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 1006940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 1006961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 604189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 201400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 28772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_4_1_1 : 0 ≤ constructionSide - (constructionCenter 4).2 - constructionRadius 4 := by
  have hid : constructionSide - (constructionCenter 4).2 - constructionRadius 4 = (0) * endpointPolynomial u := by
    change constructionSide - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_5_0_0 : 0 ≤ (constructionCenter 5).1 - constructionRadius 5 := by
  have hid : (constructionCenter 5).1 - constructionRadius 5 = (0) * endpointPolynomial u := by
    change ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_5_0_1 : 0 ≤ constructionSide - (constructionCenter 5).1 - constructionRadius 5 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 5).1 - constructionRadius 5 = ((230143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (805518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1208302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 1006940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 1006961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 604189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 201400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 28772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((1 / 2)) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_5_1_0 : 0 ≤ (constructionCenter 5).2 - constructionRadius 5 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 5).2 - constructionRadius 5 = ((150143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (525518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (788302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 656940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 656961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 394189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 131400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 18772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_5_1_1 : 0 ≤ constructionSide - (constructionCenter 5).2 - constructionRadius 5 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 5).2 - constructionRadius 5 = (1 * (u - 3657/10000)^0 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1) - (1/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_6_0_0 : 0 ≤ (constructionCenter 6).1 - constructionRadius 6 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 6).1 - constructionRadius 6 = ((227034668624976507264185697503 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (794638376877678448379921385837 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1191983123684354675930033306867 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 198668114230850079067269833733 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 198672375069869645929924634002 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (596029909393584846722998492764 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (198680898414903124731160484872 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (28383594417295901599495512624 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_6_0_1 : 0 ≤ constructionSide - (constructionCenter 6).1 - constructionRadius 6 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 6).1 - constructionRadius 6 = ((759994051213815755203834111657 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (2660047389063923672514874644803 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (3990173403135316907756371810373 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 665045954581853837006958056027 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 665063009443933326511615585438 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (1995240195326521911725680713316 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (665097121576625119494316390968 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (95016311263905160441869832656 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_6_1_0 : 0 ≤ (constructionCenter 6).2 - constructionRadius 6 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 6).2 - constructionRadius 6 = ((299141383488805752997458655741 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (1047022700336309747011090854239 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1570575839021169665765653448649 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 261769604811090375335868654551 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 261776570006796549636288013494 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (785350606272038863622574742708 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (261790501062772411647928703384 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (37399638131872534782187098128 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_6_1_1 : 0 ≤ constructionSide - (constructionCenter 6).2 - constructionRadius 6 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 6).2 - constructionRadius 6 = ((687887336349986509470561153419 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (2407663065605292373883705176401 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (3611580687798501917920751668591 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 601944464001613540738359235209 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 601958814507006422805252205946 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (1805919498448067894826104463372 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (601987518928755832577548172456 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (86000267549328527259178247152 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_7_0_0 : 0 ≤ (constructionCenter 7).1 - constructionRadius 7 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 7).1 - constructionRadius 7 = ((49266079088246669139122043909 / 4) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (172437472688870234173843023111 / 2) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 258665503601174774058153525201 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 431124664861649681879435015990 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 431140158301394974669382696060 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 258693391792802829989028402984 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 86234229784324624724946656432 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 12319618460068411781878458144 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_7_0_1 : 0 ≤ constructionSide - (constructionCenter 7).1 - constructionRadius 7 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 7).1 - constructionRadius 7 = ((49436792895632557107679937007 / 4) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (173031103905289977915636579953 / 2) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 259550149080792384310486986523 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 432589403951054234194792873770 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 432595226212407997772157523380 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 259560629151218521700707438232 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 86521374213981024120148718736 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 12360362676171800626394610912 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_7_1_0 : 0 ≤ (constructionCenter 7).2 - constructionRadius 7 := by
  have hid : (constructionCenter 7).2 - constructionRadius 7 = (0) * endpointPolynomial u := by
    change ((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_7_1_1 : 0 ≤ constructionSide - (constructionCenter 7).2 - constructionRadius 7 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 7).2 - constructionRadius 7 = (24675717995969806561700495229 * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 172734288297080106044739801532 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 518215652681967158368640511724 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 863714068812703916074227889760 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 863735384513802972441540219440 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 518254020944021351689735841216 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 172755603998305648845095375168 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 24679981136240212408273069056 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_8_0_0 : 0 ≤ (constructionCenter 8).1 - constructionRadius 8 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 8).1 - constructionRadius 8 = ((250969120789296938466370275811 / 20) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (878414867098844378403642278769 / 10) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1317656720523409217253491813879 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 439230381256473805951057806642 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 439241856795495902546752073748 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (1317760000374792621124474867736 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (439264811244840229696144594128 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (62753755736469354218404305376 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_8_0_1 : 0 ≤ constructionSide - (constructionCenter 8).1 - constructionRadius 8 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 8).1 - constructionRadius 8 = ((242545239130099192767639628769 / 20) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (848928015871956682043755736551 / 10) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1273421542886426574589710744741 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 424483687556230110123170083118 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 424493527718307069894788145692 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (1273510104345314137324204338344 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (424513208746688014529332281712 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (60646149944731707822961039904 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_8_1_0 : 0 ≤ (constructionCenter 8).2 - constructionRadius 8 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 8).2 - constructionRadius 8 = ((593519407393660938393761783349 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (2077352026552392594727339376871 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (3116079196990578074815881803361 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 519355060050559306543566361439 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 519363588294598425033094682566 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (1558116352691975286322567272212 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (519380647858850711976804578776 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (74198454168469524127205192592 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_8_1_1 : 0 ≤ constructionSide - (constructionCenter 8).2 - constructionRadius 8 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 8).2 - constructionRadius 8 = ((393509312445131324074258025811 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (1377333739389209526167456653769 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (2066077329829093508870523313879 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 344359008762144609530661528321 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 344371796219204547408445536874 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (1033153752028131472126111933868 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (344397372132677532248672297064 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (49201451512731537914160152688 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_9_0_0 : 0 ≤ (constructionCenter 9).1 - constructionRadius 9 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 9).1 - constructionRadius 9 = ((767564363836084061059775293209 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (2686566084208712650165793402811 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (4029985353374211499158485572901 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 671686931887273408763222988899 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 671709640027021231286210135806 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (2015197049945221924346618389892 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (671755061751560228589717391416 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (95968253619515511528301083472 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_9_0_1 : 0 ≤ constructionSide - (constructionCenter 9).1 - constructionRadius 9 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 9).1 - constructionRadius 9 = ((219464356002708201408244515951 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (768119681732889470729002627829 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1152171173445460084527919544339 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 192027136925430507311004900861 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 192025744486781741155330083634 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (576073054774884834102060816188 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (192022958239968015635759484424 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (27431652061685550513064261808 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_9_1_0 : 0 ≤ (constructionCenter 9).2 - constructionRadius 9 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 9).2 - constructionRadius 9 = ((36797252988106898174537890951 / 5) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (257582331554020711929062130658 / 5) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (772751678984704204525114177356 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 257585455239468931207697706888 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 257587018287801875396806669072 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (772765746419936422699992529504 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (257590146796078300328875875392 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (36798816036596989345018094464 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_9_1_1 : 0 ≤ constructionSide - (constructionCenter 9).2 - constructionRadius 9 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 9).2 - constructionRadius 9 = ((86581336991742134633964585194 / 5) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (606089109931379818294636877002 / 5) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1818326584425131587318088381264 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 606128613573234984866530182872 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 606148366226001097044733550368 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (1818504358300170335748686676576 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (606187873195449943896601000448 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (86601089644604072696347250816 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_10_0_0 : 0 ≤ (constructionCenter 10).1 - constructionRadius 10 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 10).1 - constructionRadius 10 = (24675717995969806561700495229 * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 172734288297080106044739801532 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 518215652681967158368640511724 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 863714068812703916074227889760 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 863735384513802972441540219440 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 518254020944021351689735841216 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 172755603998305648845095375168 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 24679981136240212408273069056 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_10_0_1 : 0 ≤ constructionSide - (constructionCenter 10).1 - constructionRadius 10 := by
  have hid : constructionSide - (constructionCenter 10).1 - constructionRadius 10 = (0) * endpointPolynomial u := by
    change constructionSide - ((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_bound_10_1_0 : 0 ≤ (constructionCenter 10).2 - constructionRadius 10 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : (constructionCenter 10).2 - constructionRadius 10 = ((130874415023734188120027447853 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (458075343056001304046224633487 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (687135352220945063361320033017 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 572631409821322768214655762915 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 572650027731735201908422254510 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 343601188349291666885134648564 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 114537453674540683964638453272 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 16363025460100429957377585424 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change ((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_bound_10_1_1 : 0 ≤ constructionSide - (constructionCenter 10).2 - constructionRadius 10 := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : constructionSide - (constructionCenter 10).2 - constructionRadius 10 = ((66531328944024264373576513979 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (232861810132319120132734572641 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (349295953142989253375960990431 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 291082658991381147859572126845 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 291085356782067770533117964930 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 174652832594729684804601192652 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 58218150323764964880456921896 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 8316955676139782450895483632 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change constructionSide - ((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((constructionCos+constructionSin)/2) = _
    dsimp only [constructionSide, constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_0_1 : 0 ≤ dot (constructionCenter 1 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 1 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 1 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 1 0) = ((150143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (525518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (788302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 656940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 656961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 394189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 131400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 18772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((1 / 2))) * (1) + (((1 / 2)) - ((1 / 2))) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_0_2 : 0 ≤ dot (constructionCenter 2 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 2 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 2 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 2 0) = ((20649188169818456990100314965 / 2) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 72273585414264103272817100235 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 216825037043603815934380134770 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 361382196975989813854571262300 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 361389332781380166188424766200 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 216837881493372024084925617680 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 72280721219763745522512812640 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 10326021246031014928053890880 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((1 / 2))) * (1) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((1 / 2))) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_0_3 : 0 ≤ dot (constructionCenter 3 - constructionCenter 0) (constructionSeparator 1) - (constructionSepRadius 0 1 + constructionSepRadius 3 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 3 - constructionCenter 0) (constructionSeparator 1) - (constructionSepRadius 0 1 + constructionSepRadius 3 1) = ((150143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (525518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (788302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 656940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 656961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 394189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 131400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 18772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((1 / 2)) - ((1 / 2))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((1 / 2))) * (1) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_0_4 : 0 ≤ dot (constructionCenter 4 - constructionCenter 0) (constructionSeparator 1) - (constructionSepRadius 0 1 + constructionSepRadius 4 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 4 - constructionCenter 0) (constructionSeparator 1) - (constructionSepRadius 0 1 + constructionSepRadius 4 1) = ((150143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (525518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (788302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 656940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 656961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 394189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 131400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 18772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((3 / 2)) - ((1 / 2))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((1 / 2))) * (1) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_0_5 : 0 ≤ dot (constructionCenter 5 - constructionCenter 0) (constructionSeparator 1) - (constructionSepRadius 0 1 + constructionSepRadius 5 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 5 - constructionCenter 0) (constructionSeparator 1) - (constructionSepRadius 0 1 + constructionSepRadius 5 1) = ((70143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (245518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (368302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 306940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 306961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 184189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 61400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 8772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((1 / 2)) - ((1 / 2))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1) - ((1 / 2))) * (1) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_0_6 : 0 ≤ dot (constructionCenter 6 - constructionCenter 0) (constructionSeparator 2) - (constructionSepRadius 0 2 + constructionSepRadius 6 2) := by
  have hid : dot (constructionCenter 6 - constructionCenter 0) (constructionSeparator 2) - (constructionSepRadius 0 2 + constructionSepRadius 6 2) = ((43 / 640) * u^6 - (83 / 320) * u^5 + (699 / 3200) * u^4 + (273 / 800) * u^3 - (1183 / 3200) * u^2 - (171 / 320) * u + (1949 / 3200)) * endpointPolynomial u := by
    change (((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400)) - ((1 / 2))) * (constructionCos) + (((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400)) - ((1 / 2))) * (constructionSin) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_0_7 : 0 ≤ dot (constructionCenter 7 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 7 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 7 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 7 0) = ((9266079088246669139122043909 / 4) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (32437472688870234173843023111 / 2) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 48665503601174774058153525201 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 81124664861649681879435015990 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 81140158301394974669382696060 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 48693391792802829989028402984 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 16234229784324624724946656432 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 2319618460068411781878458144 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80)) - ((1 / 2))) * (1) + (((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80)) - ((1 / 2))) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_0_8 : 0 ≤ dot (constructionCenter 8 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 8 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 8 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 8 0) = ((50969120789296938466370275811 / 20) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (178414867098844378403642278769 / 10) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (267656720523409217253491813879 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 89230381256473805951057806642 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 89241856795495902546752073748 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (267760000374792621124474867736 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (89264811244840229696144594128 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (12753755736469354218404305376 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400)) - ((1 / 2))) * (1) + (((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400)) - ((1 / 2))) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_0_9 : 0 ≤ dot (constructionCenter 9 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 9 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 9 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 9 0) = ((367564363836084061059775293209 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (1286566084208712650165793402811 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1929985353374211499158485572901 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 321686931887273408763222988899 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 321709640027021231286210135806 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (965197049945221924346618389892 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (321755061751560228589717391416 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (45968253619515511528301083472 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400)) - ((1 / 2))) * (1) + (((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400)) - ((1 / 2))) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_0_10 : 0 ≤ dot (constructionCenter 10 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 10 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 10 - constructionCenter 0) (constructionSeparator 0) - (constructionSepRadius 0 0 + constructionSepRadius 10 0) = (14675717995969806561700495229 * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 102734288297080106044739801532 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 308215652681967158368640511724 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 513714068812703916074227889760 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 513735384513802972441540219440 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 308254020944021351689735841216 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 102755603998305648845095375168 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 14679981136240212408273069056 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((1 / 2))) * (1) + (((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((1 / 2))) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_1_2 : 0 ≤ dot (constructionCenter 2 - constructionCenter 1) (constructionSeparator 1) - (constructionSepRadius 1 1 + constructionSepRadius 2 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 2 - constructionCenter 1) (constructionSeparator 1) - (constructionSepRadius 1 1 + constructionSepRadius 2 1) = ((150143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (525518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (788302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 656940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 656961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 394189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 131400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 18772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((1 / 2))) * (1) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_1_3 : 0 ≤ dot (constructionCenter 1 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 1 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 1 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 1 0) = ((150143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (525518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (788302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 656940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 656961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 394189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 131400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 18772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((1 / 2))) * (1) + (((1 / 2)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_1_4 : 0 ≤ dot (constructionCenter 1 - constructionCenter 4) (constructionSeparator 0) - (constructionSepRadius 4 0 + constructionSepRadius 1 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 1 - constructionCenter 4) (constructionSeparator 0) - (constructionSepRadius 4 0 + constructionSepRadius 1 0) = ((70143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (245518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (368302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 306940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 306961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 184189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 61400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 8772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((3 / 2))) * (1) + (((1 / 2)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_1_5 : 0 ≤ dot (constructionCenter 1 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 1 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 1 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 1 0) = ((150143320103537713932462799825 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (525518476350987451489204063675 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (788302999620049242766184686925 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 656940238187029712935335265375 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 656961310949832398634246207750 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 394189430783148688109269572100 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 131400691850681602684581015800 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 18772129565555573026571563600 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((1 / 2))) * (1) + (((1 / 2)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1)) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_1_6 : 0 ≤ dot (constructionCenter 1 - constructionCenter 6) (constructionSeparator 0) - (constructionSepRadius 6 0 + constructionSepRadius 1 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 1 - constructionCenter 6) (constructionSeparator 0) - (constructionSepRadius 6 0 + constructionSepRadius 1 0) = ((359994051213815755203834111657 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (1260047389063923672514874644803 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1890173403135316907756371810373 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 315045954581853837006958056027 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 315063009443933326511615585438 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (945240195326521911725680713316 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (315097121576625119494316390968 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (45016311263905160441869832656 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400))) * (1) + (((1 / 2)) - ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400))) * (0) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_1_7 : 0 ≤ dot (constructionCenter 1 - constructionCenter 7) (constructionSeparator 0) - (constructionSepRadius 7 0 + constructionSepRadius 1 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 1 - constructionCenter 7) (constructionSeparator 0) - (constructionSepRadius 7 0 + constructionSepRadius 1 0) = ((9436792895632557107679937007 / 4) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (33031103905289977915636579953 / 2) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 49550149080792384310486986523 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 82589403951054234194792873770 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 82595226212407997772157523380 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 49560629151218521700707438232 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 16521374213981024120148718736 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 2360362676171800626394610912 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80))) * (1) + (((1 / 2)) - ((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80))) * (0) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_1_8 : 0 ≤ dot (constructionCenter 1 - constructionCenter 8) (constructionSeparator 0) - (constructionSepRadius 8 0 + constructionSepRadius 1 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 1 - constructionCenter 8) (constructionSeparator 0) - (constructionSepRadius 8 0 + constructionSepRadius 1 0) = ((42545239130099192767639628769 / 20) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (148928015871956682043755736551 / 10) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (223421542886426574589710744741 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 74483687556230110123170083118 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 74493527718307069894788145692 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (223510104345314137324204338344 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (74513208746688014529332281712 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (10646149944731707822961039904 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400))) * (1) + (((1 / 2)) - ((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400))) * (0) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_1_9 : 0 ≤ dot (constructionCenter 9 - constructionCenter 1) (constructionSeparator 3) - (constructionSepRadius 1 3 + constructionSepRadius 9 3) := by
  have hid : dot (constructionCenter 9 - constructionCenter 1) (constructionSeparator 3) - (constructionSepRadius 1 3 + constructionSepRadius 9 3) = ((43 / 640) * u^6 - (3 / 20) * u^5 - (151 / 3200) * u^4 + (263 / 800) * u^3 + (357 / 3200) * u^2 - (63 / 160) * u + (219 / 3200)) * endpointPolynomial u := by
    change (((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (-constructionSin) + (((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400)) - ((1 / 2))) * (constructionCos) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_1_10 : 0 ≤ dot (constructionCenter 10 - constructionCenter 1) (constructionSeparator 1) - (constructionSepRadius 1 1 + constructionSepRadius 10 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 10 - constructionCenter 1) (constructionSeparator 1) - (constructionSepRadius 1 1 + constructionSepRadius 10 1) = ((50874415023734188120027447853 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (178075343056001304046224633487 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (267135352220945063361320033017 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 222631409821322768214655762915 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 222650027731735201908422254510 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 133601188349291666885134648564 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 44537453674540683964638453272 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 6363025460100429957377585424 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) + (((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((1 / 2))) * (1) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_2_3 : 0 ≤ dot (constructionCenter 2 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 2 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 2 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 2 0) = ((20649188169818456990100314965 / 2) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 72273585414264103272817100235 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 216825037043603815934380134770 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 361382196975989813854571262300 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 361389332781380166188424766200 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 216837881493372024084925617680 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 72280721219763745522512812640 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 10326021246031014928053890880 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((1 / 2))) * (1) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_2_4 : 0 ≤ dot (constructionCenter 2 - constructionCenter 4) (constructionSeparator 0) - (constructionSepRadius 4 0 + constructionSepRadius 2 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 2 - constructionCenter 4) (constructionSeparator 0) - (constructionSepRadius 4 0 + constructionSepRadius 2 0) = ((649188169818456990100314965 / 2) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 2273585414264103272817100235 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 6825037043603815934380134770 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 11382196975989813854571262300 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 11389332781380166188424766200 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 6837881493372024084925617680 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 2280721219763745522512812640 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 326021246031014928053890880 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((3 / 2))) * (1) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_2_5 : 0 ≤ dot (constructionCenter 2 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 2 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 2 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 2 0) = ((20649188169818456990100314965 / 2) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 72273585414264103272817100235 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 216825037043603815934380134770 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 361382196975989813854571262300 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 361389332781380166188424766200 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 216837881493372024084925617680 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 72280721219763745522512812640 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 10326021246031014928053890880 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((1 / 2))) * (1) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1)) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_2_6 : 0 ≤ dot (constructionCenter 2 - constructionCenter 6) (constructionSeparator 0) - (constructionSepRadius 6 0 + constructionSepRadius 2 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 2 - constructionCenter 6) (constructionSeparator 0) - (constructionSepRadius 6 0 + constructionSepRadius 2 0) = ((2782651761562040667940801479 / 5) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (19481678898567120131299082782 / 5) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (58454387735554426634624861724 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 19487913370813937926194052952 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 19491031275481094065794143888 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (58482448877638591603960941216 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (19497268422035833683975375168 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (2785769666282369949281469056 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400))) * (1) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400))) * (0) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_2_7 : 0 ≤ dot (constructionCenter 2 - constructionCenter 7) (constructionSeparator 1) - (constructionSepRadius 7 1 + constructionSepRadius 2 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 2 - constructionCenter 7) (constructionSeparator 1) - (constructionSepRadius 7 1 + constructionSepRadius 2 1) = (14675717995969806561700495229 * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 102734288297080106044739801532 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 308215652681967158368640511724 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 513714068812703916074227889760 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 513735384513802972441540219440 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 308254020944021351689735841216 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 102755603998305648845095375168 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 14679981136240212408273069056 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80))) * (1) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_2_8 : 0 ≤ dot (constructionCenter 2 - constructionCenter 8) (constructionSeparator 2) - (constructionSepRadius 8 2 + constructionSepRadius 2 2) := by
  have hid : dot (constructionCenter 2 - constructionCenter 8) (constructionSeparator 2) - (constructionSepRadius 8 2 + constructionSepRadius 2 2) = ((23 / 640) * u^6 - (29 / 160) * u^5 + (639 / 3200) * u^4 + (99 / 400) * u^3 - (1383 / 3200) * u^2 - (61 / 160) * u + (1789 / 3200)) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400))) * (constructionCos) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400))) * (constructionSin) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_2_9 : 0 ≤ dot (constructionCenter 2 - constructionCenter 9) (constructionSeparator 1) - (constructionSepRadius 9 1 + constructionSepRadius 2 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 2 - constructionCenter 9) (constructionSeparator 1) - (constructionSepRadius 9 1 + constructionSepRadius 2 1) = ((36581336991742134633964585194 / 5) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (256089109931379818294636877002 / 5) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (768326584425131587318088381264 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 256128613573234984866530182872 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 256148366226001097044733550368 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (768504358300170335748686676576 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (256187873195449943896601000448 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (36601089644604072696347250816 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400))) * (1) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_2_10 : 0 ≤ dot (constructionCenter 2 - constructionCenter 10) (constructionSeparator 3) - (constructionSepRadius 10 3 + constructionSepRadius 2 3) := by
  have hid : dot (constructionCenter 2 - constructionCenter 10) (constructionSeparator 3) - (constructionSepRadius 10 3 + constructionSepRadius 2 3) = ((1 / 128) * u^6 - (1 / 8) * u^5 + (163 / 640) * u^4 + (1 / 20) * u^3 - (289 / 640) * u^2 - (3 / 16) * u + (329 / 640)) * endpointPolynomial u := by
    change (((5 / 2) * u^7 - (25 / 4) * u^6 + (3 / 2) * u^5 + (15 / 2) * u^4 + (5 / 2) * u^3 - (19 / 4) * u^2 + (5 / 2) * u + 2) - ((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80))) * (-constructionSin) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80))) * (constructionCos) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_3_4 : 0 ≤ dot (constructionCenter 4 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 4 0) := by
  have hid : dot (constructionCenter 4 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 4 0) = (0) * endpointPolynomial u := by
    change (((3 / 2)) - ((1 / 2))) * (1) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_3_5 : 0 ≤ dot (constructionCenter 3 - constructionCenter 5) (constructionSeparator 1) - (constructionSepRadius 5 1 + constructionSepRadius 3 1) := by
  have hid : dot (constructionCenter 3 - constructionCenter 5) (constructionSeparator 1) - (constructionSepRadius 5 1 + constructionSepRadius 3 1) = (0) * endpointPolynomial u := by
    change (((1 / 2)) - ((1 / 2))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1)) * (1) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_3_6 : 0 ≤ dot (constructionCenter 3 - constructionCenter 6) (constructionSeparator 1) - (constructionSepRadius 6 1 + constructionSepRadius 3 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 3 - constructionCenter 6) (constructionSeparator 1) - (constructionSepRadius 6 1 + constructionSepRadius 3 1) = ((287887336349986509470561153419 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (1007663065605292373883705176401 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1511580687798501917920751668591 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 251944464001613540738359235209 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 251958814507006422805252205946 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (755919498448067894826104463372 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (251987518928755832577548172456 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (36000267549328527259178247152 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((1 / 2)) - ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400))) * (1) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_3_7 : 0 ≤ dot (constructionCenter 7 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 7 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 7 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 7 0) = ((9266079088246669139122043909 / 4) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (32437472688870234173843023111 / 2) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 48665503601174774058153525201 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 81124664861649681879435015990 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 81140158301394974669382696060 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 48693391792802829989028402984 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 16234229784324624724946656432 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 2319618460068411781878458144 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80)) - ((1 / 2))) * (1) + (((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_3_8 : 0 ≤ dot (constructionCenter 8 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 8 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 8 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 8 0) = ((50969120789296938466370275811 / 20) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (178414867098844378403642278769 / 10) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (267656720523409217253491813879 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 89230381256473805951057806642 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 89241856795495902546752073748 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (267760000374792621124474867736 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (89264811244840229696144594128 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (12753755736469354218404305376 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400)) - ((1 / 2))) * (1) + (((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_3_9 : 0 ≤ dot (constructionCenter 9 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 9 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 9 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 9 0) = ((367564363836084061059775293209 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (1286566084208712650165793402811 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1929985353374211499158485572901 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 321686931887273408763222988899 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 321709640027021231286210135806 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (965197049945221924346618389892 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (321755061751560228589717391416 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (45968253619515511528301083472 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400)) - ((1 / 2))) * (1) + (((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_3_10 : 0 ≤ dot (constructionCenter 10 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 10 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 10 - constructionCenter 3) (constructionSeparator 0) - (constructionSepRadius 3 0 + constructionSepRadius 10 0) = (14675717995969806561700495229 * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 102734288297080106044739801532 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 308215652681967158368640511724 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 513714068812703916074227889760 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 513735384513802972441540219440 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 308254020944021351689735841216 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 102755603998305648845095375168 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 14679981136240212408273069056 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((1 / 2))) * (1) + (((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_4_5 : 0 ≤ dot (constructionCenter 4 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 4 0) := by
  have hid : dot (constructionCenter 4 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 4 0) = (0) * endpointPolynomial u := by
    change (((3 / 2)) - ((1 / 2))) * (1) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1)) * (0) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_4_6 : 0 ≤ dot (constructionCenter 4 - constructionCenter 6) (constructionSeparator 1) - (constructionSepRadius 6 1 + constructionSepRadius 4 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 4 - constructionCenter 6) (constructionSeparator 1) - (constructionSepRadius 6 1 + constructionSepRadius 4 1) = ((287887336349986509470561153419 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (1007663065605292373883705176401 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1511580687798501917920751668591 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 251944464001613540738359235209 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 251958814507006422805252205946 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (755919498448067894826104463372 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (251987518928755832577548172456 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (36000267549328527259178247152 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((3 / 2)) - ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400))) * (1) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_4_7 : 0 ≤ dot (constructionCenter 4 - constructionCenter 7) (constructionSeparator 1) - (constructionSepRadius 7 1 + constructionSepRadius 4 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 4 - constructionCenter 7) (constructionSeparator 1) - (constructionSepRadius 7 1 + constructionSepRadius 4 1) = (14675717995969806561700495229 * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 102734288297080106044739801532 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 308215652681967158368640511724 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 513714068812703916074227889760 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 513735384513802972441540219440 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 308254020944021351689735841216 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 102755603998305648845095375168 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 14679981136240212408273069056 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((3 / 2)) - ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80))) * (1) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_4_8 : 0 ≤ dot (constructionCenter 4 - constructionCenter 8) (constructionSeparator 3) - (constructionSepRadius 8 3 + constructionSepRadius 4 3) := by
  have hid : dot (constructionCenter 4 - constructionCenter 8) (constructionSeparator 3) - (constructionSepRadius 8 3 + constructionSepRadius 4 3) = ((1 / 640) * u^6 - (41 / 320) * u^5 + (943 / 3200) * u^4 + (23 / 400) * u^3 - (1861 / 3200) * u^2 - (79 / 320) * u + (2353 / 3200)) * endpointPolynomial u := by
    change (((3 / 2)) - ((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400))) * (-constructionSin) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400))) * (constructionCos) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_4_9 : 0 ≤ dot (constructionCenter 4 - constructionCenter 9) (constructionSeparator 1) - (constructionSepRadius 9 1 + constructionSepRadius 4 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 4 - constructionCenter 9) (constructionSeparator 1) - (constructionSepRadius 9 1 + constructionSepRadius 4 1) = ((36581336991742134633964585194 / 5) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (256089109931379818294636877002 / 5) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (768326584425131587318088381264 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 256128613573234984866530182872 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 256148366226001097044733550368 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (768504358300170335748686676576 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (256187873195449943896601000448 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (36601089644604072696347250816 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((3 / 2)) - ((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400))) * (0) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2) - ((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400))) * (1) - (((constructionCos+constructionSin)/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_4_10 : 0 ≤ dot (constructionCenter 10 - constructionCenter 4) (constructionSeparator 0) - (constructionSepRadius 4 0 + constructionSepRadius 10 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 10 - constructionCenter 4) (constructionSeparator 0) - (constructionSepRadius 4 0 + constructionSepRadius 10 0) = (4675717995969806561700495229 * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 32734288297080106044739801532 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 98215652681967158368640511724 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 163714068812703916074227889760 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 163735384513802972441540219440 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 98254020944021351689735841216 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 32755603998305648845095375168 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 4679981136240212408273069056 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((3 / 2))) * (1) + (((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 2)) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_5_6 : 0 ≤ dot (constructionCenter 5 - constructionCenter 6) (constructionSeparator 3) - (constructionSepRadius 6 3 + constructionSepRadius 5 3) := by
  have hid : dot (constructionCenter 5 - constructionCenter 6) (constructionSeparator 3) - (constructionSepRadius 6 3 + constructionSepRadius 5 3) = ((39 / 640) * u^6 - (21 / 80) * u^5 + (827 / 3200) * u^4 + (279 / 800) * u^3 - (1599 / 3200) * u^2 - (19 / 32) * u + (2657 / 3200)) * endpointPolynomial u := by
    change (((1 / 2)) - ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400))) * (-constructionSin) + (((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1) - ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400))) * (constructionCos) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_5_7 : 0 ≤ dot (constructionCenter 7 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 7 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 7 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 7 0) = ((9266079088246669139122043909 / 4) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (32437472688870234173843023111 / 2) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 48665503601174774058153525201 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 81124664861649681879435015990 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 81140158301394974669382696060 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 48693391792802829989028402984 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 16234229784324624724946656432 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 2319618460068411781878458144 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80)) - ((1 / 2))) * (1) + (((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1)) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_5_8 : 0 ≤ dot (constructionCenter 8 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 8 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 8 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 8 0) = ((50969120789296938466370275811 / 20) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (178414867098844378403642278769 / 10) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (267656720523409217253491813879 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 89230381256473805951057806642 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 89241856795495902546752073748 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (267760000374792621124474867736 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (89264811244840229696144594128 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (12753755736469354218404305376 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400)) - ((1 / 2))) * (1) + (((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1)) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_5_9 : 0 ≤ dot (constructionCenter 9 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 9 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 9 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 9 0) = ((367564363836084061059775293209 / 40) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (1286566084208712650165793402811 / 20) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (1929985353374211499158485572901 / 10) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 321686931887273408763222988899 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 321709640027021231286210135806 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (965197049945221924346618389892 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (321755061751560228589717391416 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (45968253619515511528301083472 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400)) - ((1 / 2))) * (1) + (((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1)) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_5_10 : 0 ≤ dot (constructionCenter 10 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 10 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 10 - constructionCenter 5) (constructionSeparator 0) - (constructionSepRadius 5 0 + constructionSepRadius 10 0) = (14675717995969806561700495229 * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 102734288297080106044739801532 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 308215652681967158368640511724 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 513714068812703916074227889760 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 513735384513802972441540219440 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 308254020944021351689735841216 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 102755603998305648845095375168 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 14679981136240212408273069056 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((1 / 2))) * (1) + (((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((25 / 8) * u^7 - (15 / 2) * u^6 + (15 / 8) * u^5 + 8 * u^4 + (35 / 8) * u^3 - 5 * u^2 + (37 / 8) * u + 1)) * (0) - ((1/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_6_7 : 0 ≤ dot (constructionCenter 6 - constructionCenter 7) (constructionSeparator 3) - (constructionSepRadius 7 3 + constructionSepRadius 6 3) := by
  have hid : dot (constructionCenter 6 - constructionCenter 7) (constructionSeparator 3) - (constructionSepRadius 7 3 + constructionSepRadius 6 3) = ((3 / 320) * u^6 - (23 / 160) * u^5 + (227 / 800) * u^4 + (19 / 200) * u^3 - (883 / 1600) * u^2 - (47 / 160) * u + (567 / 800)) * endpointPolynomial u := by
    change (((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400)) - ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80))) * (-constructionSin) + (((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400)) - ((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80))) * (constructionCos) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_6_8 : 0 ≤ dot (constructionCenter 8 - constructionCenter 6) (constructionSeparator 2) - (constructionSepRadius 6 2 + constructionSepRadius 8 2) := by
  have hid : dot (constructionCenter 8 - constructionCenter 6) (constructionSeparator 2) - (constructionSepRadius 6 2 + constructionSepRadius 8 2) = (- (9 / 160) * u^6 + (31 / 320) * u^5 + (151 / 1600) * u^4 - (161 / 800) * u^3 - (113 / 400) * u^2 + (43 / 320) * u + (471 / 1600)) * endpointPolynomial u := by
    change (((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400)) - ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400))) * (constructionCos) + (((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400)) - ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400))) * (constructionSin) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_6_9 : 0 ≤ dot (constructionCenter 9 - constructionCenter 6) (constructionSeparator 2) - (constructionSepRadius 6 2 + constructionSepRadius 9 2) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 9 - constructionCenter 6) (constructionSeparator 2) - (constructionSepRadius 6 2 + constructionSepRadius 9 2) = ((1985464334759680736902295881 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (6952369304969341612296703299 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (10433420992677474460830579109 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 8698574052718251188256760455 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 8702631307758737767876301270 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 5224013555463209366099325028 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 1742149581368815803175890744 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 248994492887454936150007248 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + ((13 / 320) * u^6 - (9 / 80) * u^5 - (1 / 100) * u^4 + (241 / 800) * u^3 + (17 / 1600) * u^2 - (87 / 160) * u + (97 / 800)) * endpointPolynomial u := by
    change (((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400)) - ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400))) * (constructionCos) + (((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400)) - ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400))) * (constructionSin) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_6_10 : 0 ≤ dot (constructionCenter 10 - constructionCenter 6) (constructionSeparator 0) - (constructionSepRadius 6 0 + constructionSepRadius 10 0) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 10 - constructionCenter 6) (constructionSeparator 0) - (constructionSepRadius 6 0 + constructionSepRadius 10 0) = ((49076542633729862002384980423 / 10) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (171785193312647133990912589267 / 5) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (515407465927371138805926746494 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 171819785207528040145850680412 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 171837083007903900318909597128 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (515563146130885229628012058896 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (171871682314745350296888187808 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (24555569117328357350377359936 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((147 / 80) * u^7 - (75 / 16) * u^6 + (581 / 400) * u^5 + (419 / 80) * u^4 + (729 / 400) * u^3 - (1549 / 400) * u^2 + (771 / 400) * u + (361 / 400))) * (1) + (((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((79 / 80) * u^7 - (45 / 16) * u^6 + (717 / 400) * u^5 + (173 / 80) * u^4 + (53 / 400) * u^3 - (843 / 400) * u^2 + (947 / 400) * u + (327 / 400))) * (0) - (((constructionCos+constructionSin)/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_7_8 : 0 ≤ dot (constructionCenter 8 - constructionCenter 7) (constructionSeparator 1) - (constructionSepRadius 7 1 + constructionSepRadius 8 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 8 - constructionCenter 7) (constructionSeparator 1) - (constructionSepRadius 7 1 + constructionSepRadius 8 1) = ((3728940839345578899933449173 / 5) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (26111352684764364544028772284 / 5) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (78360362855001722335681742988 / 5) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 26128890676233509682458985824 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 26137661858568998840388694256 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + (78439303496338604224898617792 / 5) * (u - 3657/10000)^5 * (3658/10000 - u)^2 + (26155208596970942779376375616 / 5) * (u - 3657/10000)^6 * (3658/10000 - u)^1 + (3737712021892721035712719872 / 5) * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400)) - ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80))) * (0) + (((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400)) - ((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80))) * (1) - (((constructionCos+constructionSin)/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_7_9 : 0 ≤ dot (constructionCenter 9 - constructionCenter 7) (constructionSeparator 2) - (constructionSepRadius 7 2 + constructionSepRadius 9 2) := by
  have hid : dot (constructionCenter 9 - constructionCenter 7) (constructionSeparator 2) - (constructionSepRadius 7 2 + constructionSepRadius 9 2) = (- (9 / 160) * u^6 + (31 / 320) * u^5 + (151 / 1600) * u^4 - (161 / 800) * u^3 - (113 / 400) * u^2 + (43 / 320) * u + (471 / 1600)) * endpointPolynomial u := by
    change (((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400)) - ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80))) * (constructionCos) + (((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400)) - ((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80))) * (constructionSin) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_7_10 : 0 ≤ dot (constructionCenter 10 - constructionCenter 7) (constructionSeparator 1) - (constructionSepRadius 7 1 + constructionSepRadius 10 1) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 10 - constructionCenter 7) (constructionSeparator 1) - (constructionSepRadius 7 1 + constructionSepRadius 10 1) = ((4534209721988731670292152465 / 2) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + 15873504973333569183994943985 * (u - 3657/10000)^1 * (3658/10000 - u)^6 + 47631828982415068666208184770 * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 79405240446996971353548387300 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 79424101295705775715716266200 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 47665778510164330465600917680 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 15892365822164730125152812640 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 2270877030785069339079090880 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + (0) * endpointPolynomial u := by
    change (((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((53 / 16) * u^7 - (125 / 16) * u^6 + (119 / 80) * u^5 + (141 / 16) * u^4 + (431 / 80) * u^3 - (471 / 80) * u^2 + (289 / 80) * u + (79 / 80))) * (0) + (((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((1 / 16) * u^7 - (5 / 16) * u^6 + (23 / 80) * u^5 + (9 / 16) * u^4 - (53 / 80) * u^3 - (87 / 80) * u^2 + (73 / 80) * u + (43 / 80))) * (1) - (((constructionCos+constructionSin)/2) + ((constructionCos+constructionSin)/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_8_9 : 0 ≤ dot (constructionCenter 8 - constructionCenter 9) (constructionSeparator 3) - (constructionSepRadius 9 3 + constructionSepRadius 8 3) := by
  have hid : dot (constructionCenter 8 - constructionCenter 9) (constructionSeparator 3) - (constructionSepRadius 9 3 + constructionSepRadius 8 3) = ((3 / 320) * u^6 - (23 / 160) * u^5 + (227 / 800) * u^4 + (19 / 200) * u^3 - (883 / 1600) * u^2 - (47 / 160) * u + (567 / 800)) * endpointPolynomial u := by
    change (((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400)) - ((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400))) * (-constructionSin) + (((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400)) - ((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400))) * (constructionCos) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

theorem construction_gap_8_10 : 0 ≤ dot (constructionCenter 10 - constructionCenter 8) (constructionSeparator 2) - (constructionSepRadius 8 2 + constructionSepRadius 10 2) := by
  have ha : 0 < u - 3657/10000 := by linarith [construction_u_bounds.1]
  have hb : 0 < 3658/10000 - u := by linarith [construction_u_bounds.2]
  have hid : dot (constructionCenter 10 - constructionCenter 8) (constructionSeparator 2) - (constructionSepRadius 8 2 + constructionSepRadius 10 2) = ((1985464334759680736902295881 / 8) * (u - 3657/10000)^0 * (3658/10000 - u)^7 + (6952369304969341612296703299 / 4) * (u - 3657/10000)^1 * (3658/10000 - u)^6 + (10433420992677474460830579109 / 2) * (u - 3657/10000)^2 * (3658/10000 - u)^5 + 8698574052718251188256760455 * (u - 3657/10000)^3 * (3658/10000 - u)^4 + 8702631307758737767876301270 * (u - 3657/10000)^4 * (3658/10000 - u)^3 + 5224013555463209366099325028 * (u - 3657/10000)^5 * (3658/10000 - u)^2 + 1742149581368815803175890744 * (u - 3657/10000)^6 * (3658/10000 - u)^1 + 248994492887454936150007248 * (u - 3657/10000)^7 * (3658/10000 - u)^0) + ((3 / 40) * u^6 - (11 / 40) * u^5 + (257 / 1600) * u^4 + (403 / 800) * u^3 - (257 / 800) * u^2 - (131 / 160) * u + (777 / 1600)) * endpointPolynomial u := by
    change (((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((113 / 80) * u^7 - (45 / 16) * u^6 - (101 / 400) * u^5 + (241 / 80) * u^4 + (1691 / 400) * u^3 - (371 / 400) * u^2 + (309 / 400) * u + (619 / 400))) * (constructionCos) + (((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((191 / 80) * u^7 - (85 / 16) * u^6 - (7 / 400) * u^5 + (577 / 80) * u^4 + (1837 / 400) * u^3 - (1947 / 400) * u^2 + (863 / 400) * u + (683 / 400))) * (constructionSin) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero, add_zero]
  positivity

theorem construction_gap_9_10 : 0 ≤ dot (constructionCenter 10 - constructionCenter 9) (constructionSeparator 2) - (constructionSepRadius 9 2 + constructionSepRadius 10 2) := by
  have hid : dot (constructionCenter 10 - constructionCenter 9) (constructionSeparator 2) - (constructionSepRadius 9 2 + constructionSepRadius 10 2) = (- (7 / 320) * u^6 - (21 / 320) * u^5 + (53 / 200) * u^4 + (1 / 800) * u^3 - (983 / 1600) * u^2 - (9 / 64) * u + (527 / 800)) * endpointPolynomial u := by
    change (((49 / 16) * u^7 - (115 / 16) * u^6 + (127 / 80) * u^5 + (119 / 16) * u^4 + (403 / 80) * u^3 - (313 / 80) * u^2 + (297 / 80) * u + (157 / 80)) - ((231 / 80) * u^7 - (95 / 16) * u^6 - (87 / 400) * u^5 + (527 / 80) * u^4 + (3117 / 400) * u^3 - (1177 / 400) * u^2 + (983 / 400) * u + (653 / 400))) * (constructionCos) + (((43 / 16) * u^7 - (85 / 16) * u^6 - (111 / 80) * u^5 + (125 / 16) * u^4 + (561 / 80) * u^3 - (311 / 80) * u^2 + (199 / 80) * u + (119 / 80)) - ((117 / 80) * u^7 - (45 / 16) * u^6 - (609 / 400) * u^5 + (449 / 80) * u^4 + (1519 / 400) * u^3 - (1539 / 400) * u^2 + (281 / 400) * u + (571 / 400))) * (constructionSin) - ((1/2) + (1/2)) = _
    dsimp only [constructionCos, constructionSin, endpointPolynomial]
    ring
  rw [hid, u_polynomial, mul_zero]

end
end ElevenSquare
