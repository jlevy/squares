import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0992
open Sq19.Endgame.Reduction

theorem case0992 : checkNat 992 = true := by native_decide
#print axioms case0992

theorem case2016 : checkNat 2016 = true := by
  apply check_of_normalize (Case.ofNat 2016)
  have he : (Case.ofNat 2016).normalize = Case.ofNat 992 := by decide
  rw [he]
  exact case0992
#print axioms case2016

theorem case3040 : checkNat 3040 = true := by
  apply check_of_normalize (Case.ofNat 3040)
  have he : (Case.ofNat 3040).normalize = Case.ofNat 992 := by decide
  rw [he]
  exact case0992
#print axioms case3040

theorem case4064 : checkNat 4064 = true := by
  apply check_of_normalize (Case.ofNat 4064)
  have he : (Case.ofNat 4064).normalize = Case.ofNat 992 := by decide
  rw [he]
  exact case0992
#print axioms case4064

theorem case0993 : checkNat 993 = true := by native_decide
#print axioms case0993

theorem case3041 : checkNat 3041 = true := by
  apply check_of_normalize (Case.ofNat 3041)
  have he : (Case.ofNat 3041).normalize = Case.ofNat 993 := by decide
  rw [he]
  exact case0993
#print axioms case3041

theorem case0994 : checkNat 994 = true := by native_decide
#print axioms case0994

theorem case2018 : checkNat 2018 = true := by
  apply check_of_normalize (Case.ofNat 2018)
  have he : (Case.ofNat 2018).normalize = Case.ofNat 994 := by decide
  rw [he]
  exact case0994
#print axioms case2018

theorem case0995 : checkNat 995 = true := by native_decide
#print axioms case0995

theorem case0996 : checkNat 996 = true := by native_decide
#print axioms case0996

theorem case2020 : checkNat 2020 = true := by
  apply check_of_normalize (Case.ofNat 2020)
  have he : (Case.ofNat 2020).normalize = Case.ofNat 996 := by decide
  rw [he]
  exact case0996
#print axioms case2020

theorem case3044 : checkNat 3044 = true := by
  apply check_of_normalize (Case.ofNat 3044)
  have he : (Case.ofNat 3044).normalize = Case.ofNat 996 := by decide
  rw [he]
  exact case0996
#print axioms case3044

theorem case4068 : checkNat 4068 = true := by
  apply check_of_normalize (Case.ofNat 4068)
  have he : (Case.ofNat 4068).normalize = Case.ofNat 996 := by decide
  rw [he]
  exact case0996
#print axioms case4068

theorem case0997 : checkNat 997 = true := by native_decide
#print axioms case0997

theorem case3045 : checkNat 3045 = true := by
  apply check_of_normalize (Case.ofNat 3045)
  have he : (Case.ofNat 3045).normalize = Case.ofNat 997 := by decide
  rw [he]
  exact case0997
#print axioms case3045

theorem case0998 : checkNat 998 = true := by native_decide
#print axioms case0998

theorem case2022 : checkNat 2022 = true := by
  apply check_of_normalize (Case.ofNat 2022)
  have he : (Case.ofNat 2022).normalize = Case.ofNat 998 := by decide
  rw [he]
  exact case0998
#print axioms case2022

theorem case0999 : checkNat 999 = true := by native_decide
#print axioms case0999

theorem case1000 : checkNat 1000 = true := by native_decide
#print axioms case1000

theorem case2024 : checkNat 2024 = true := by
  apply check_of_normalize (Case.ofNat 2024)
  have he : (Case.ofNat 2024).normalize = Case.ofNat 1000 := by decide
  rw [he]
  exact case1000
#print axioms case2024

theorem case3048 : checkNat 3048 = true := by
  apply check_of_normalize (Case.ofNat 3048)
  have he : (Case.ofNat 3048).normalize = Case.ofNat 1000 := by decide
  rw [he]
  exact case1000
#print axioms case3048

theorem case4072 : checkNat 4072 = true := by
  apply check_of_normalize (Case.ofNat 4072)
  have he : (Case.ofNat 4072).normalize = Case.ofNat 1000 := by decide
  rw [he]
  exact case1000
#print axioms case4072

theorem case1001 : checkNat 1001 = true := by native_decide
#print axioms case1001

theorem case3049 : checkNat 3049 = true := by
  apply check_of_normalize (Case.ofNat 3049)
  have he : (Case.ofNat 3049).normalize = Case.ofNat 1001 := by decide
  rw [he]
  exact case1001
#print axioms case3049

theorem case1002 : checkNat 1002 = true := by native_decide
#print axioms case1002

theorem case2026 : checkNat 2026 = true := by
  apply check_of_normalize (Case.ofNat 2026)
  have he : (Case.ofNat 2026).normalize = Case.ofNat 1002 := by decide
  rw [he]
  exact case1002
#print axioms case2026

theorem case1003 : checkNat 1003 = true := by native_decide
#print axioms case1003

theorem case1004 : checkNat 1004 = true := by native_decide
#print axioms case1004

theorem case2028 : checkNat 2028 = true := by
  apply check_of_normalize (Case.ofNat 2028)
  have he : (Case.ofNat 2028).normalize = Case.ofNat 1004 := by decide
  rw [he]
  exact case1004
#print axioms case2028

theorem case3052 : checkNat 3052 = true := by
  apply check_of_normalize (Case.ofNat 3052)
  have he : (Case.ofNat 3052).normalize = Case.ofNat 1004 := by decide
  rw [he]
  exact case1004
#print axioms case3052

theorem case4076 : checkNat 4076 = true := by
  apply check_of_normalize (Case.ofNat 4076)
  have he : (Case.ofNat 4076).normalize = Case.ofNat 1004 := by decide
  rw [he]
  exact case1004
#print axioms case4076

theorem case1005 : checkNat 1005 = true := by native_decide
#print axioms case1005

theorem case3053 : checkNat 3053 = true := by
  apply check_of_normalize (Case.ofNat 3053)
  have he : (Case.ofNat 3053).normalize = Case.ofNat 1005 := by decide
  rw [he]
  exact case1005
#print axioms case3053

theorem case1006 : checkNat 1006 = true := by native_decide
#print axioms case1006

theorem case2030 : checkNat 2030 = true := by
  apply check_of_normalize (Case.ofNat 2030)
  have he : (Case.ofNat 2030).normalize = Case.ofNat 1006 := by decide
  rw [he]
  exact case1006
#print axioms case2030

theorem case1007 : checkNat 1007 = true := by native_decide
#print axioms case1007

theorem case1008 : checkNat 1008 = true := by native_decide
#print axioms case1008

theorem case2032 : checkNat 2032 = true := by
  apply check_of_normalize (Case.ofNat 2032)
  have he : (Case.ofNat 2032).normalize = Case.ofNat 1008 := by decide
  rw [he]
  exact case1008
#print axioms case2032

theorem case3056 : checkNat 3056 = true := by
  apply check_of_normalize (Case.ofNat 3056)
  have he : (Case.ofNat 3056).normalize = Case.ofNat 1008 := by decide
  rw [he]
  exact case1008
#print axioms case3056

theorem case4080 : checkNat 4080 = true := by
  apply check_of_normalize (Case.ofNat 4080)
  have he : (Case.ofNat 4080).normalize = Case.ofNat 1008 := by decide
  rw [he]
  exact case1008
#print axioms case4080

theorem case1009 : checkNat 1009 = true := by native_decide
#print axioms case1009

theorem case3057 : checkNat 3057 = true := by
  apply check_of_normalize (Case.ofNat 3057)
  have he : (Case.ofNat 3057).normalize = Case.ofNat 1009 := by decide
  rw [he]
  exact case1009
#print axioms case3057

theorem case1010 : checkNat 1010 = true := by native_decide
#print axioms case1010

theorem case2034 : checkNat 2034 = true := by
  apply check_of_normalize (Case.ofNat 2034)
  have he : (Case.ofNat 2034).normalize = Case.ofNat 1010 := by decide
  rw [he]
  exact case1010
#print axioms case2034

theorem case1011 : checkNat 1011 = true := by native_decide
#print axioms case1011

theorem case1012 : checkNat 1012 = true := by native_decide
#print axioms case1012

theorem case2036 : checkNat 2036 = true := by
  apply check_of_normalize (Case.ofNat 2036)
  have he : (Case.ofNat 2036).normalize = Case.ofNat 1012 := by decide
  rw [he]
  exact case1012
#print axioms case2036

theorem case3060 : checkNat 3060 = true := by
  apply check_of_normalize (Case.ofNat 3060)
  have he : (Case.ofNat 3060).normalize = Case.ofNat 1012 := by decide
  rw [he]
  exact case1012
#print axioms case3060

theorem case4084 : checkNat 4084 = true := by
  apply check_of_normalize (Case.ofNat 4084)
  have he : (Case.ofNat 4084).normalize = Case.ofNat 1012 := by decide
  rw [he]
  exact case1012
#print axioms case4084

theorem case1013 : checkNat 1013 = true := by native_decide
#print axioms case1013

theorem case3061 : checkNat 3061 = true := by
  apply check_of_normalize (Case.ofNat 3061)
  have he : (Case.ofNat 3061).normalize = Case.ofNat 1013 := by decide
  rw [he]
  exact case1013
#print axioms case3061

theorem case1014 : checkNat 1014 = true := by native_decide
#print axioms case1014

theorem case2038 : checkNat 2038 = true := by
  apply check_of_normalize (Case.ofNat 2038)
  have he : (Case.ofNat 2038).normalize = Case.ofNat 1014 := by decide
  rw [he]
  exact case1014
#print axioms case2038

theorem case1015 : checkNat 1015 = true := by native_decide
#print axioms case1015

theorem case1016 : checkNat 1016 = true := by native_decide
#print axioms case1016

theorem case2040 : checkNat 2040 = true := by
  apply check_of_normalize (Case.ofNat 2040)
  have he : (Case.ofNat 2040).normalize = Case.ofNat 1016 := by decide
  rw [he]
  exact case1016
#print axioms case2040

theorem case3064 : checkNat 3064 = true := by
  apply check_of_normalize (Case.ofNat 3064)
  have he : (Case.ofNat 3064).normalize = Case.ofNat 1016 := by decide
  rw [he]
  exact case1016
#print axioms case3064

theorem case4088 : checkNat 4088 = true := by
  apply check_of_normalize (Case.ofNat 4088)
  have he : (Case.ofNat 4088).normalize = Case.ofNat 1016 := by decide
  rw [he]
  exact case1016
#print axioms case4088

theorem case1017 : checkNat 1017 = true := by native_decide
#print axioms case1017

theorem case3065 : checkNat 3065 = true := by
  apply check_of_normalize (Case.ofNat 3065)
  have he : (Case.ofNat 3065).normalize = Case.ofNat 1017 := by decide
  rw [he]
  exact case1017
#print axioms case3065

theorem case1018 : checkNat 1018 = true := by native_decide
#print axioms case1018

theorem case2042 : checkNat 2042 = true := by
  apply check_of_normalize (Case.ofNat 2042)
  have he : (Case.ofNat 2042).normalize = Case.ofNat 1018 := by decide
  rw [he]
  exact case1018
#print axioms case2042

theorem case1019 : checkNat 1019 = true := by native_decide
#print axioms case1019

theorem case1020 : checkNat 1020 = true := by native_decide
#print axioms case1020

theorem case2044 : checkNat 2044 = true := by
  apply check_of_normalize (Case.ofNat 2044)
  have he : (Case.ofNat 2044).normalize = Case.ofNat 1020 := by decide
  rw [he]
  exact case1020
#print axioms case2044

theorem case3068 : checkNat 3068 = true := by
  apply check_of_normalize (Case.ofNat 3068)
  have he : (Case.ofNat 3068).normalize = Case.ofNat 1020 := by decide
  rw [he]
  exact case1020
#print axioms case3068

theorem case4092 : checkNat 4092 = true := by
  apply check_of_normalize (Case.ofNat 4092)
  have he : (Case.ofNat 4092).normalize = Case.ofNat 1020 := by decide
  rw [he]
  exact case1020
#print axioms case4092

theorem case1021 : checkNat 1021 = true := by native_decide
#print axioms case1021

theorem case3069 : checkNat 3069 = true := by
  apply check_of_normalize (Case.ofNat 3069)
  have he : (Case.ofNat 3069).normalize = Case.ofNat 1021 := by decide
  rw [he]
  exact case1021
#print axioms case3069

theorem case1022 : checkNat 1022 = true := by native_decide
#print axioms case1022

theorem case2046 : checkNat 2046 = true := by
  apply check_of_normalize (Case.ofNat 2046)
  have he : (Case.ofNat 2046).normalize = Case.ofNat 1022 := by decide
  rw [he]
  exact case1022
#print axioms case2046

theorem case1023 : checkNat 1023 = true := by native_decide
#print axioms case1023

theorem accepted :
    checkNat 992 = true ∧
    checkNat 993 = true ∧
    checkNat 994 = true ∧
    checkNat 995 = true ∧
    checkNat 996 = true ∧
    checkNat 997 = true ∧
    checkNat 998 = true ∧
    checkNat 999 = true ∧
    checkNat 1000 = true ∧
    checkNat 1001 = true ∧
    checkNat 1002 = true ∧
    checkNat 1003 = true ∧
    checkNat 1004 = true ∧
    checkNat 1005 = true ∧
    checkNat 1006 = true ∧
    checkNat 1007 = true ∧
    checkNat 1008 = true ∧
    checkNat 1009 = true ∧
    checkNat 1010 = true ∧
    checkNat 1011 = true ∧
    checkNat 1012 = true ∧
    checkNat 1013 = true ∧
    checkNat 1014 = true ∧
    checkNat 1015 = true ∧
    checkNat 1016 = true ∧
    checkNat 1017 = true ∧
    checkNat 1018 = true ∧
    checkNat 1019 = true ∧
    checkNat 1020 = true ∧
    checkNat 1021 = true ∧
    checkNat 1022 = true ∧
    checkNat 1023 = true ∧
    checkNat 2016 = true ∧
    checkNat 2018 = true ∧
    checkNat 2020 = true ∧
    checkNat 2022 = true ∧
    checkNat 2024 = true ∧
    checkNat 2026 = true ∧
    checkNat 2028 = true ∧
    checkNat 2030 = true ∧
    checkNat 2032 = true ∧
    checkNat 2034 = true ∧
    checkNat 2036 = true ∧
    checkNat 2038 = true ∧
    checkNat 2040 = true ∧
    checkNat 2042 = true ∧
    checkNat 2044 = true ∧
    checkNat 2046 = true ∧
    checkNat 3040 = true ∧
    checkNat 3041 = true ∧
    checkNat 3044 = true ∧
    checkNat 3045 = true ∧
    checkNat 3048 = true ∧
    checkNat 3049 = true ∧
    checkNat 3052 = true ∧
    checkNat 3053 = true ∧
    checkNat 3056 = true ∧
    checkNat 3057 = true ∧
    checkNat 3060 = true ∧
    checkNat 3061 = true ∧
    checkNat 3064 = true ∧
    checkNat 3065 = true ∧
    checkNat 3068 = true ∧
    checkNat 3069 = true ∧
    checkNat 4064 = true ∧
    checkNat 4068 = true ∧
    checkNat 4072 = true ∧
    checkNat 4076 = true ∧
    checkNat 4080 = true ∧
    checkNat 4084 = true ∧
    checkNat 4088 = true ∧
    checkNat 4092 = true := by
  exact ⟨case0992, case0993, case0994, case0995, case0996, case0997, case0998, case0999, case1000, case1001, case1002, case1003, case1004, case1005, case1006, case1007, case1008, case1009, case1010, case1011, case1012, case1013, case1014, case1015, case1016, case1017, case1018, case1019, case1020, case1021, case1022, case1023, case2016, case2018, case2020, case2022, case2024, case2026, case2028, case2030, case2032, case2034, case2036, case2038, case2040, case2042, case2044, case2046, case3040, case3041, case3044, case3045, case3048, case3049, case3052, case3053, case3056, case3057, case3060, case3061, case3064, case3065, case3068, case3069, case4064, case4068, case4072, case4076, case4080, case4084, case4088, case4092⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0992
