import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1600
open Sq19.Endgame.Reduction

theorem case2178 : checkNat 2178 = true := by native_decide
#print axioms case2178

theorem case3202 : checkNat 3202 = true := by
  apply check_of_normalize (Case.ofNat 3202)
  have he : (Case.ofNat 3202).normalize = Case.ofNat 2178 := by decide
  rw [he]
  exact case2178
#print axioms case3202

theorem case2179 : checkNat 2179 = true := by native_decide
#print axioms case2179

theorem case2182 : checkNat 2182 = true := by native_decide
#print axioms case2182

theorem case3206 : checkNat 3206 = true := by
  apply check_of_normalize (Case.ofNat 3206)
  have he : (Case.ofNat 3206).normalize = Case.ofNat 2182 := by decide
  rw [he]
  exact case2182
#print axioms case3206

theorem case2183 : checkNat 2183 = true := by native_decide
#print axioms case2183

theorem case2186 : checkNat 2186 = true := by native_decide
#print axioms case2186

theorem case3210 : checkNat 3210 = true := by
  apply check_of_normalize (Case.ofNat 3210)
  have he : (Case.ofNat 3210).normalize = Case.ofNat 2186 := by decide
  rw [he]
  exact case2186
#print axioms case3210

theorem case2187 : checkNat 2187 = true := by native_decide
#print axioms case2187

theorem case2190 : checkNat 2190 = true := by native_decide
#print axioms case2190

theorem case3214 : checkNat 3214 = true := by
  apply check_of_normalize (Case.ofNat 3214)
  have he : (Case.ofNat 3214).normalize = Case.ofNat 2190 := by decide
  rw [he]
  exact case2190
#print axioms case3214

theorem case2191 : checkNat 2191 = true := by native_decide
#print axioms case2191

theorem case2194 : checkNat 2194 = true := by native_decide
#print axioms case2194

theorem case3218 : checkNat 3218 = true := by
  apply check_of_normalize (Case.ofNat 3218)
  have he : (Case.ofNat 3218).normalize = Case.ofNat 2194 := by decide
  rw [he]
  exact case2194
#print axioms case3218

theorem case2195 : checkNat 2195 = true := by native_decide
#print axioms case2195

theorem case2198 : checkNat 2198 = true := by native_decide
#print axioms case2198

theorem case3222 : checkNat 3222 = true := by
  apply check_of_normalize (Case.ofNat 3222)
  have he : (Case.ofNat 3222).normalize = Case.ofNat 2198 := by decide
  rw [he]
  exact case2198
#print axioms case3222

theorem case2199 : checkNat 2199 = true := by native_decide
#print axioms case2199

theorem case2202 : checkNat 2202 = true := by native_decide
#print axioms case2202

theorem case3226 : checkNat 3226 = true := by
  apply check_of_normalize (Case.ofNat 3226)
  have he : (Case.ofNat 3226).normalize = Case.ofNat 2202 := by decide
  rw [he]
  exact case2202
#print axioms case3226

theorem case2203 : checkNat 2203 = true := by native_decide
#print axioms case2203

theorem case2206 : checkNat 2206 = true := by native_decide
#print axioms case2206

theorem case3230 : checkNat 3230 = true := by
  apply check_of_normalize (Case.ofNat 3230)
  have he : (Case.ofNat 3230).normalize = Case.ofNat 2206 := by decide
  rw [he]
  exact case2206
#print axioms case3230

theorem case2207 : checkNat 2207 = true := by native_decide
#print axioms case2207

theorem case2210 : checkNat 2210 = true := by native_decide
#print axioms case2210

theorem case3234 : checkNat 3234 = true := by
  apply check_of_normalize (Case.ofNat 3234)
  have he : (Case.ofNat 3234).normalize = Case.ofNat 2210 := by decide
  rw [he]
  exact case2210
#print axioms case3234

theorem case2211 : checkNat 2211 = true := by native_decide
#print axioms case2211

theorem case2214 : checkNat 2214 = true := by native_decide
#print axioms case2214

theorem case3238 : checkNat 3238 = true := by
  apply check_of_normalize (Case.ofNat 3238)
  have he : (Case.ofNat 3238).normalize = Case.ofNat 2214 := by decide
  rw [he]
  exact case2214
#print axioms case3238

theorem case2215 : checkNat 2215 = true := by native_decide
#print axioms case2215

theorem case2218 : checkNat 2218 = true := by native_decide
#print axioms case2218

theorem case3242 : checkNat 3242 = true := by
  apply check_of_normalize (Case.ofNat 3242)
  have he : (Case.ofNat 3242).normalize = Case.ofNat 2218 := by decide
  rw [he]
  exact case2218
#print axioms case3242

theorem case2219 : checkNat 2219 = true := by native_decide
#print axioms case2219

theorem case2222 : checkNat 2222 = true := by native_decide
#print axioms case2222

theorem case3246 : checkNat 3246 = true := by
  apply check_of_normalize (Case.ofNat 3246)
  have he : (Case.ofNat 3246).normalize = Case.ofNat 2222 := by decide
  rw [he]
  exact case2222
#print axioms case3246

theorem case2223 : checkNat 2223 = true := by native_decide
#print axioms case2223

theorem case2226 : checkNat 2226 = true := by native_decide
#print axioms case2226

theorem case3250 : checkNat 3250 = true := by
  apply check_of_normalize (Case.ofNat 3250)
  have he : (Case.ofNat 3250).normalize = Case.ofNat 2226 := by decide
  rw [he]
  exact case2226
#print axioms case3250

theorem case2227 : checkNat 2227 = true := by native_decide
#print axioms case2227

theorem case2230 : checkNat 2230 = true := by native_decide
#print axioms case2230

theorem case3254 : checkNat 3254 = true := by
  apply check_of_normalize (Case.ofNat 3254)
  have he : (Case.ofNat 3254).normalize = Case.ofNat 2230 := by decide
  rw [he]
  exact case2230
#print axioms case3254

theorem case2231 : checkNat 2231 = true := by native_decide
#print axioms case2231

theorem case2234 : checkNat 2234 = true := by native_decide
#print axioms case2234

theorem case3258 : checkNat 3258 = true := by
  apply check_of_normalize (Case.ofNat 3258)
  have he : (Case.ofNat 3258).normalize = Case.ofNat 2234 := by decide
  rw [he]
  exact case2234
#print axioms case3258

theorem case2235 : checkNat 2235 = true := by native_decide
#print axioms case2235

theorem case2238 : checkNat 2238 = true := by native_decide
#print axioms case2238

theorem case3262 : checkNat 3262 = true := by
  apply check_of_normalize (Case.ofNat 3262)
  have he : (Case.ofNat 3262).normalize = Case.ofNat 2238 := by decide
  rw [he]
  exact case2238
#print axioms case3262

theorem case2239 : checkNat 2239 = true := by native_decide
#print axioms case2239

theorem accepted :
    checkNat 2178 = true ∧
    checkNat 2179 = true ∧
    checkNat 2182 = true ∧
    checkNat 2183 = true ∧
    checkNat 2186 = true ∧
    checkNat 2187 = true ∧
    checkNat 2190 = true ∧
    checkNat 2191 = true ∧
    checkNat 2194 = true ∧
    checkNat 2195 = true ∧
    checkNat 2198 = true ∧
    checkNat 2199 = true ∧
    checkNat 2202 = true ∧
    checkNat 2203 = true ∧
    checkNat 2206 = true ∧
    checkNat 2207 = true ∧
    checkNat 2210 = true ∧
    checkNat 2211 = true ∧
    checkNat 2214 = true ∧
    checkNat 2215 = true ∧
    checkNat 2218 = true ∧
    checkNat 2219 = true ∧
    checkNat 2222 = true ∧
    checkNat 2223 = true ∧
    checkNat 2226 = true ∧
    checkNat 2227 = true ∧
    checkNat 2230 = true ∧
    checkNat 2231 = true ∧
    checkNat 2234 = true ∧
    checkNat 2235 = true ∧
    checkNat 2238 = true ∧
    checkNat 2239 = true ∧
    checkNat 3202 = true ∧
    checkNat 3206 = true ∧
    checkNat 3210 = true ∧
    checkNat 3214 = true ∧
    checkNat 3218 = true ∧
    checkNat 3222 = true ∧
    checkNat 3226 = true ∧
    checkNat 3230 = true ∧
    checkNat 3234 = true ∧
    checkNat 3238 = true ∧
    checkNat 3242 = true ∧
    checkNat 3246 = true ∧
    checkNat 3250 = true ∧
    checkNat 3254 = true ∧
    checkNat 3258 = true ∧
    checkNat 3262 = true := by
  exact ⟨case2178, case2179, case2182, case2183, case2186, case2187, case2190, case2191, case2194, case2195, case2198, case2199, case2202, case2203, case2206, case2207, case2210, case2211, case2214, case2215, case2218, case2219, case2222, case2223, case2226, case2227, case2230, case2231, case2234, case2235, case2238, case2239, case3202, case3206, case3210, case3214, case3218, case3222, case3226, case3230, case3234, case3238, case3242, case3246, case3250, case3254, case3258, case3262⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1600
