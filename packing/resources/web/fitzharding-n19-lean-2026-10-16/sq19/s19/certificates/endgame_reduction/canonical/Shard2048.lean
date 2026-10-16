import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard2048
open Sq19.Endgame.Reduction

theorem case3075 : checkNat 3075 = true := by native_decide
#print axioms case3075

theorem case3079 : checkNat 3079 = true := by native_decide
#print axioms case3079

theorem case3083 : checkNat 3083 = true := by native_decide
#print axioms case3083

theorem case3087 : checkNat 3087 = true := by native_decide
#print axioms case3087

theorem case3091 : checkNat 3091 = true := by native_decide
#print axioms case3091

theorem case3095 : checkNat 3095 = true := by native_decide
#print axioms case3095

theorem case3099 : checkNat 3099 = true := by native_decide
#print axioms case3099

theorem case3103 : checkNat 3103 = true := by native_decide
#print axioms case3103

theorem case3107 : checkNat 3107 = true := by native_decide
#print axioms case3107

theorem case3111 : checkNat 3111 = true := by native_decide
#print axioms case3111

theorem case3115 : checkNat 3115 = true := by native_decide
#print axioms case3115

theorem case3119 : checkNat 3119 = true := by native_decide
#print axioms case3119

theorem case3123 : checkNat 3123 = true := by native_decide
#print axioms case3123

theorem case3127 : checkNat 3127 = true := by native_decide
#print axioms case3127

theorem case3131 : checkNat 3131 = true := by native_decide
#print axioms case3131

theorem case3135 : checkNat 3135 = true := by native_decide
#print axioms case3135

theorem case3139 : checkNat 3139 = true := by native_decide
#print axioms case3139

theorem case3143 : checkNat 3143 = true := by native_decide
#print axioms case3143

theorem case3147 : checkNat 3147 = true := by native_decide
#print axioms case3147

theorem case3151 : checkNat 3151 = true := by native_decide
#print axioms case3151

theorem case3155 : checkNat 3155 = true := by native_decide
#print axioms case3155

theorem case3159 : checkNat 3159 = true := by native_decide
#print axioms case3159

theorem case3163 : checkNat 3163 = true := by native_decide
#print axioms case3163

theorem case3167 : checkNat 3167 = true := by native_decide
#print axioms case3167

theorem case3171 : checkNat 3171 = true := by native_decide
#print axioms case3171

theorem case3175 : checkNat 3175 = true := by native_decide
#print axioms case3175

theorem case3179 : checkNat 3179 = true := by native_decide
#print axioms case3179

theorem case3183 : checkNat 3183 = true := by native_decide
#print axioms case3183

theorem case3187 : checkNat 3187 = true := by native_decide
#print axioms case3187

theorem case3191 : checkNat 3191 = true := by native_decide
#print axioms case3191

theorem case3195 : checkNat 3195 = true := by native_decide
#print axioms case3195

theorem case3199 : checkNat 3199 = true := by native_decide
#print axioms case3199

theorem accepted :
    checkNat 3075 = true ∧
    checkNat 3079 = true ∧
    checkNat 3083 = true ∧
    checkNat 3087 = true ∧
    checkNat 3091 = true ∧
    checkNat 3095 = true ∧
    checkNat 3099 = true ∧
    checkNat 3103 = true ∧
    checkNat 3107 = true ∧
    checkNat 3111 = true ∧
    checkNat 3115 = true ∧
    checkNat 3119 = true ∧
    checkNat 3123 = true ∧
    checkNat 3127 = true ∧
    checkNat 3131 = true ∧
    checkNat 3135 = true ∧
    checkNat 3139 = true ∧
    checkNat 3143 = true ∧
    checkNat 3147 = true ∧
    checkNat 3151 = true ∧
    checkNat 3155 = true ∧
    checkNat 3159 = true ∧
    checkNat 3163 = true ∧
    checkNat 3167 = true ∧
    checkNat 3171 = true ∧
    checkNat 3175 = true ∧
    checkNat 3179 = true ∧
    checkNat 3183 = true ∧
    checkNat 3187 = true ∧
    checkNat 3191 = true ∧
    checkNat 3195 = true ∧
    checkNat 3199 = true := by
  exact ⟨case3075, case3079, case3083, case3087, case3091, case3095, case3099, case3103, case3107, case3111, case3115, case3119, case3123, case3127, case3131, case3135, case3139, case3143, case3147, case3151, case3155, case3159, case3163, case3167, case3171, case3175, case3179, case3183, case3187, case3191, case3195, case3199⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard2048
