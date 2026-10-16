import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0032
open Sq19.Endgame.Reduction

theorem case0032 : checkNat 32 = true := by native_decide
#print axioms case0032

theorem case1056 : checkNat 1056 = true := by
  apply check_of_normalize (Case.ofNat 1056)
  have he : (Case.ofNat 1056).normalize = Case.ofNat 32 := by decide
  rw [he]
  exact case0032
#print axioms case1056

theorem case2080 : checkNat 2080 = true := by
  apply check_of_normalize (Case.ofNat 2080)
  have he : (Case.ofNat 2080).normalize = Case.ofNat 32 := by decide
  rw [he]
  exact case0032
#print axioms case2080

theorem case3104 : checkNat 3104 = true := by
  apply check_of_normalize (Case.ofNat 3104)
  have he : (Case.ofNat 3104).normalize = Case.ofNat 32 := by decide
  rw [he]
  exact case0032
#print axioms case3104

theorem case0033 : checkNat 33 = true := by native_decide
#print axioms case0033

theorem case2081 : checkNat 2081 = true := by
  apply check_of_normalize (Case.ofNat 2081)
  have he : (Case.ofNat 2081).normalize = Case.ofNat 33 := by decide
  rw [he]
  exact case0033
#print axioms case2081

theorem case0034 : checkNat 34 = true := by native_decide
#print axioms case0034

theorem case1058 : checkNat 1058 = true := by
  apply check_of_normalize (Case.ofNat 1058)
  have he : (Case.ofNat 1058).normalize = Case.ofNat 34 := by decide
  rw [he]
  exact case0034
#print axioms case1058

theorem case0035 : checkNat 35 = true := by native_decide
#print axioms case0035

theorem case0036 : checkNat 36 = true := by native_decide
#print axioms case0036

theorem case1060 : checkNat 1060 = true := by
  apply check_of_normalize (Case.ofNat 1060)
  have he : (Case.ofNat 1060).normalize = Case.ofNat 36 := by decide
  rw [he]
  exact case0036
#print axioms case1060

theorem case2084 : checkNat 2084 = true := by
  apply check_of_normalize (Case.ofNat 2084)
  have he : (Case.ofNat 2084).normalize = Case.ofNat 36 := by decide
  rw [he]
  exact case0036
#print axioms case2084

theorem case3108 : checkNat 3108 = true := by
  apply check_of_normalize (Case.ofNat 3108)
  have he : (Case.ofNat 3108).normalize = Case.ofNat 36 := by decide
  rw [he]
  exact case0036
#print axioms case3108

theorem case0037 : checkNat 37 = true := by native_decide
#print axioms case0037

theorem case2085 : checkNat 2085 = true := by
  apply check_of_normalize (Case.ofNat 2085)
  have he : (Case.ofNat 2085).normalize = Case.ofNat 37 := by decide
  rw [he]
  exact case0037
#print axioms case2085

theorem case0038 : checkNat 38 = true := by native_decide
#print axioms case0038

theorem case1062 : checkNat 1062 = true := by
  apply check_of_normalize (Case.ofNat 1062)
  have he : (Case.ofNat 1062).normalize = Case.ofNat 38 := by decide
  rw [he]
  exact case0038
#print axioms case1062

theorem case0039 : checkNat 39 = true := by native_decide
#print axioms case0039

theorem case0040 : checkNat 40 = true := by native_decide
#print axioms case0040

theorem case1064 : checkNat 1064 = true := by
  apply check_of_normalize (Case.ofNat 1064)
  have he : (Case.ofNat 1064).normalize = Case.ofNat 40 := by decide
  rw [he]
  exact case0040
#print axioms case1064

theorem case2088 : checkNat 2088 = true := by
  apply check_of_normalize (Case.ofNat 2088)
  have he : (Case.ofNat 2088).normalize = Case.ofNat 40 := by decide
  rw [he]
  exact case0040
#print axioms case2088

theorem case3112 : checkNat 3112 = true := by
  apply check_of_normalize (Case.ofNat 3112)
  have he : (Case.ofNat 3112).normalize = Case.ofNat 40 := by decide
  rw [he]
  exact case0040
#print axioms case3112

theorem case0041 : checkNat 41 = true := by native_decide
#print axioms case0041

theorem case2089 : checkNat 2089 = true := by
  apply check_of_normalize (Case.ofNat 2089)
  have he : (Case.ofNat 2089).normalize = Case.ofNat 41 := by decide
  rw [he]
  exact case0041
#print axioms case2089

theorem case0042 : checkNat 42 = true := by native_decide
#print axioms case0042

theorem case1066 : checkNat 1066 = true := by
  apply check_of_normalize (Case.ofNat 1066)
  have he : (Case.ofNat 1066).normalize = Case.ofNat 42 := by decide
  rw [he]
  exact case0042
#print axioms case1066

theorem case0043 : checkNat 43 = true := by native_decide
#print axioms case0043

theorem case0044 : checkNat 44 = true := by native_decide
#print axioms case0044

theorem case1068 : checkNat 1068 = true := by
  apply check_of_normalize (Case.ofNat 1068)
  have he : (Case.ofNat 1068).normalize = Case.ofNat 44 := by decide
  rw [he]
  exact case0044
#print axioms case1068

theorem case2092 : checkNat 2092 = true := by
  apply check_of_normalize (Case.ofNat 2092)
  have he : (Case.ofNat 2092).normalize = Case.ofNat 44 := by decide
  rw [he]
  exact case0044
#print axioms case2092

theorem case3116 : checkNat 3116 = true := by
  apply check_of_normalize (Case.ofNat 3116)
  have he : (Case.ofNat 3116).normalize = Case.ofNat 44 := by decide
  rw [he]
  exact case0044
#print axioms case3116

theorem case0045 : checkNat 45 = true := by native_decide
#print axioms case0045

theorem case2093 : checkNat 2093 = true := by
  apply check_of_normalize (Case.ofNat 2093)
  have he : (Case.ofNat 2093).normalize = Case.ofNat 45 := by decide
  rw [he]
  exact case0045
#print axioms case2093

theorem case0046 : checkNat 46 = true := by native_decide
#print axioms case0046

theorem case1070 : checkNat 1070 = true := by
  apply check_of_normalize (Case.ofNat 1070)
  have he : (Case.ofNat 1070).normalize = Case.ofNat 46 := by decide
  rw [he]
  exact case0046
#print axioms case1070

theorem case0047 : checkNat 47 = true := by native_decide
#print axioms case0047

theorem case0048 : checkNat 48 = true := by native_decide
#print axioms case0048

theorem case1072 : checkNat 1072 = true := by
  apply check_of_normalize (Case.ofNat 1072)
  have he : (Case.ofNat 1072).normalize = Case.ofNat 48 := by decide
  rw [he]
  exact case0048
#print axioms case1072

theorem case2096 : checkNat 2096 = true := by
  apply check_of_normalize (Case.ofNat 2096)
  have he : (Case.ofNat 2096).normalize = Case.ofNat 48 := by decide
  rw [he]
  exact case0048
#print axioms case2096

theorem case3120 : checkNat 3120 = true := by
  apply check_of_normalize (Case.ofNat 3120)
  have he : (Case.ofNat 3120).normalize = Case.ofNat 48 := by decide
  rw [he]
  exact case0048
#print axioms case3120

theorem case0049 : checkNat 49 = true := by native_decide
#print axioms case0049

theorem case2097 : checkNat 2097 = true := by
  apply check_of_normalize (Case.ofNat 2097)
  have he : (Case.ofNat 2097).normalize = Case.ofNat 49 := by decide
  rw [he]
  exact case0049
#print axioms case2097

theorem case0050 : checkNat 50 = true := by native_decide
#print axioms case0050

theorem case1074 : checkNat 1074 = true := by
  apply check_of_normalize (Case.ofNat 1074)
  have he : (Case.ofNat 1074).normalize = Case.ofNat 50 := by decide
  rw [he]
  exact case0050
#print axioms case1074

theorem case0051 : checkNat 51 = true := by native_decide
#print axioms case0051

theorem case0052 : checkNat 52 = true := by native_decide
#print axioms case0052

theorem case1076 : checkNat 1076 = true := by
  apply check_of_normalize (Case.ofNat 1076)
  have he : (Case.ofNat 1076).normalize = Case.ofNat 52 := by decide
  rw [he]
  exact case0052
#print axioms case1076

theorem case2100 : checkNat 2100 = true := by
  apply check_of_normalize (Case.ofNat 2100)
  have he : (Case.ofNat 2100).normalize = Case.ofNat 52 := by decide
  rw [he]
  exact case0052
#print axioms case2100

theorem case3124 : checkNat 3124 = true := by
  apply check_of_normalize (Case.ofNat 3124)
  have he : (Case.ofNat 3124).normalize = Case.ofNat 52 := by decide
  rw [he]
  exact case0052
#print axioms case3124

theorem case0053 : checkNat 53 = true := by native_decide
#print axioms case0053

theorem case2101 : checkNat 2101 = true := by
  apply check_of_normalize (Case.ofNat 2101)
  have he : (Case.ofNat 2101).normalize = Case.ofNat 53 := by decide
  rw [he]
  exact case0053
#print axioms case2101

theorem case0054 : checkNat 54 = true := by native_decide
#print axioms case0054

theorem case1078 : checkNat 1078 = true := by
  apply check_of_normalize (Case.ofNat 1078)
  have he : (Case.ofNat 1078).normalize = Case.ofNat 54 := by decide
  rw [he]
  exact case0054
#print axioms case1078

theorem case0055 : checkNat 55 = true := by native_decide
#print axioms case0055

theorem case0056 : checkNat 56 = true := by native_decide
#print axioms case0056

theorem case1080 : checkNat 1080 = true := by
  apply check_of_normalize (Case.ofNat 1080)
  have he : (Case.ofNat 1080).normalize = Case.ofNat 56 := by decide
  rw [he]
  exact case0056
#print axioms case1080

theorem case2104 : checkNat 2104 = true := by
  apply check_of_normalize (Case.ofNat 2104)
  have he : (Case.ofNat 2104).normalize = Case.ofNat 56 := by decide
  rw [he]
  exact case0056
#print axioms case2104

theorem case3128 : checkNat 3128 = true := by
  apply check_of_normalize (Case.ofNat 3128)
  have he : (Case.ofNat 3128).normalize = Case.ofNat 56 := by decide
  rw [he]
  exact case0056
#print axioms case3128

theorem case0057 : checkNat 57 = true := by native_decide
#print axioms case0057

theorem case2105 : checkNat 2105 = true := by
  apply check_of_normalize (Case.ofNat 2105)
  have he : (Case.ofNat 2105).normalize = Case.ofNat 57 := by decide
  rw [he]
  exact case0057
#print axioms case2105

theorem case0058 : checkNat 58 = true := by native_decide
#print axioms case0058

theorem case1082 : checkNat 1082 = true := by
  apply check_of_normalize (Case.ofNat 1082)
  have he : (Case.ofNat 1082).normalize = Case.ofNat 58 := by decide
  rw [he]
  exact case0058
#print axioms case1082

theorem case0059 : checkNat 59 = true := by native_decide
#print axioms case0059

theorem case0060 : checkNat 60 = true := by native_decide
#print axioms case0060

theorem case1084 : checkNat 1084 = true := by
  apply check_of_normalize (Case.ofNat 1084)
  have he : (Case.ofNat 1084).normalize = Case.ofNat 60 := by decide
  rw [he]
  exact case0060
#print axioms case1084

theorem case2108 : checkNat 2108 = true := by
  apply check_of_normalize (Case.ofNat 2108)
  have he : (Case.ofNat 2108).normalize = Case.ofNat 60 := by decide
  rw [he]
  exact case0060
#print axioms case2108

theorem case3132 : checkNat 3132 = true := by
  apply check_of_normalize (Case.ofNat 3132)
  have he : (Case.ofNat 3132).normalize = Case.ofNat 60 := by decide
  rw [he]
  exact case0060
#print axioms case3132

theorem case0061 : checkNat 61 = true := by native_decide
#print axioms case0061

theorem case2109 : checkNat 2109 = true := by
  apply check_of_normalize (Case.ofNat 2109)
  have he : (Case.ofNat 2109).normalize = Case.ofNat 61 := by decide
  rw [he]
  exact case0061
#print axioms case2109

theorem case0062 : checkNat 62 = true := by native_decide
#print axioms case0062

theorem case1086 : checkNat 1086 = true := by
  apply check_of_normalize (Case.ofNat 1086)
  have he : (Case.ofNat 1086).normalize = Case.ofNat 62 := by decide
  rw [he]
  exact case0062
#print axioms case1086

theorem case0063 : checkNat 63 = true := by native_decide
#print axioms case0063

theorem accepted :
    checkNat 32 = true ∧
    checkNat 33 = true ∧
    checkNat 34 = true ∧
    checkNat 35 = true ∧
    checkNat 36 = true ∧
    checkNat 37 = true ∧
    checkNat 38 = true ∧
    checkNat 39 = true ∧
    checkNat 40 = true ∧
    checkNat 41 = true ∧
    checkNat 42 = true ∧
    checkNat 43 = true ∧
    checkNat 44 = true ∧
    checkNat 45 = true ∧
    checkNat 46 = true ∧
    checkNat 47 = true ∧
    checkNat 48 = true ∧
    checkNat 49 = true ∧
    checkNat 50 = true ∧
    checkNat 51 = true ∧
    checkNat 52 = true ∧
    checkNat 53 = true ∧
    checkNat 54 = true ∧
    checkNat 55 = true ∧
    checkNat 56 = true ∧
    checkNat 57 = true ∧
    checkNat 58 = true ∧
    checkNat 59 = true ∧
    checkNat 60 = true ∧
    checkNat 61 = true ∧
    checkNat 62 = true ∧
    checkNat 63 = true ∧
    checkNat 1056 = true ∧
    checkNat 1058 = true ∧
    checkNat 1060 = true ∧
    checkNat 1062 = true ∧
    checkNat 1064 = true ∧
    checkNat 1066 = true ∧
    checkNat 1068 = true ∧
    checkNat 1070 = true ∧
    checkNat 1072 = true ∧
    checkNat 1074 = true ∧
    checkNat 1076 = true ∧
    checkNat 1078 = true ∧
    checkNat 1080 = true ∧
    checkNat 1082 = true ∧
    checkNat 1084 = true ∧
    checkNat 1086 = true ∧
    checkNat 2080 = true ∧
    checkNat 2081 = true ∧
    checkNat 2084 = true ∧
    checkNat 2085 = true ∧
    checkNat 2088 = true ∧
    checkNat 2089 = true ∧
    checkNat 2092 = true ∧
    checkNat 2093 = true ∧
    checkNat 2096 = true ∧
    checkNat 2097 = true ∧
    checkNat 2100 = true ∧
    checkNat 2101 = true ∧
    checkNat 2104 = true ∧
    checkNat 2105 = true ∧
    checkNat 2108 = true ∧
    checkNat 2109 = true ∧
    checkNat 3104 = true ∧
    checkNat 3108 = true ∧
    checkNat 3112 = true ∧
    checkNat 3116 = true ∧
    checkNat 3120 = true ∧
    checkNat 3124 = true ∧
    checkNat 3128 = true ∧
    checkNat 3132 = true := by
  exact ⟨case0032, case0033, case0034, case0035, case0036, case0037, case0038, case0039, case0040, case0041, case0042, case0043, case0044, case0045, case0046, case0047, case0048, case0049, case0050, case0051, case0052, case0053, case0054, case0055, case0056, case0057, case0058, case0059, case0060, case0061, case0062, case0063, case1056, case1058, case1060, case1062, case1064, case1066, case1068, case1070, case1072, case1074, case1076, case1078, case1080, case1082, case1084, case1086, case2080, case2081, case2084, case2085, case2088, case2089, case2092, case2093, case2096, case2097, case2100, case2101, case2104, case2105, case2108, case2109, case3104, case3108, case3112, case3116, case3120, case3124, case3128, case3132⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0032
