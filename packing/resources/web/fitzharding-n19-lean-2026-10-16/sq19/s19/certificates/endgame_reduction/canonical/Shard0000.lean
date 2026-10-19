import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0000
open Sq19.Endgame.Reduction

theorem case0000 : checkNat 0 = true := by native_decide
#print axioms case0000

theorem case1024 : checkNat 1024 = true := by
  apply check_of_normalize (Case.ofNat 1024)
  have he : (Case.ofNat 1024).normalize = Case.ofNat 0 := by decide
  rw [he]
  exact case0000
#print axioms case1024

theorem case2048 : checkNat 2048 = true := by
  apply check_of_normalize (Case.ofNat 2048)
  have he : (Case.ofNat 2048).normalize = Case.ofNat 0 := by decide
  rw [he]
  exact case0000
#print axioms case2048

theorem case3072 : checkNat 3072 = true := by
  apply check_of_normalize (Case.ofNat 3072)
  have he : (Case.ofNat 3072).normalize = Case.ofNat 0 := by decide
  rw [he]
  exact case0000
#print axioms case3072

theorem case0001 : checkNat 1 = true := by native_decide
#print axioms case0001

theorem case2049 : checkNat 2049 = true := by
  apply check_of_normalize (Case.ofNat 2049)
  have he : (Case.ofNat 2049).normalize = Case.ofNat 1 := by decide
  rw [he]
  exact case0001
#print axioms case2049

theorem case0002 : checkNat 2 = true := by native_decide
#print axioms case0002

theorem case1026 : checkNat 1026 = true := by
  apply check_of_normalize (Case.ofNat 1026)
  have he : (Case.ofNat 1026).normalize = Case.ofNat 2 := by decide
  rw [he]
  exact case0002
#print axioms case1026

theorem case0003 : checkNat 3 = true := by native_decide
#print axioms case0003

theorem case0004 : checkNat 4 = true := by native_decide
#print axioms case0004

theorem case1028 : checkNat 1028 = true := by
  apply check_of_normalize (Case.ofNat 1028)
  have he : (Case.ofNat 1028).normalize = Case.ofNat 4 := by decide
  rw [he]
  exact case0004
#print axioms case1028

theorem case2052 : checkNat 2052 = true := by
  apply check_of_normalize (Case.ofNat 2052)
  have he : (Case.ofNat 2052).normalize = Case.ofNat 4 := by decide
  rw [he]
  exact case0004
#print axioms case2052

theorem case3076 : checkNat 3076 = true := by
  apply check_of_normalize (Case.ofNat 3076)
  have he : (Case.ofNat 3076).normalize = Case.ofNat 4 := by decide
  rw [he]
  exact case0004
#print axioms case3076

theorem case0005 : checkNat 5 = true := by native_decide
#print axioms case0005

theorem case2053 : checkNat 2053 = true := by
  apply check_of_normalize (Case.ofNat 2053)
  have he : (Case.ofNat 2053).normalize = Case.ofNat 5 := by decide
  rw [he]
  exact case0005
#print axioms case2053

theorem case0006 : checkNat 6 = true := by native_decide
#print axioms case0006

theorem case1030 : checkNat 1030 = true := by
  apply check_of_normalize (Case.ofNat 1030)
  have he : (Case.ofNat 1030).normalize = Case.ofNat 6 := by decide
  rw [he]
  exact case0006
#print axioms case1030

theorem case0007 : checkNat 7 = true := by native_decide
#print axioms case0007

theorem case0008 : checkNat 8 = true := by native_decide
#print axioms case0008

theorem case1032 : checkNat 1032 = true := by
  apply check_of_normalize (Case.ofNat 1032)
  have he : (Case.ofNat 1032).normalize = Case.ofNat 8 := by decide
  rw [he]
  exact case0008
#print axioms case1032

theorem case2056 : checkNat 2056 = true := by
  apply check_of_normalize (Case.ofNat 2056)
  have he : (Case.ofNat 2056).normalize = Case.ofNat 8 := by decide
  rw [he]
  exact case0008
#print axioms case2056

theorem case3080 : checkNat 3080 = true := by
  apply check_of_normalize (Case.ofNat 3080)
  have he : (Case.ofNat 3080).normalize = Case.ofNat 8 := by decide
  rw [he]
  exact case0008
#print axioms case3080

theorem case0009 : checkNat 9 = true := by native_decide
#print axioms case0009

theorem case2057 : checkNat 2057 = true := by
  apply check_of_normalize (Case.ofNat 2057)
  have he : (Case.ofNat 2057).normalize = Case.ofNat 9 := by decide
  rw [he]
  exact case0009
#print axioms case2057

theorem case0010 : checkNat 10 = true := by native_decide
#print axioms case0010

theorem case1034 : checkNat 1034 = true := by
  apply check_of_normalize (Case.ofNat 1034)
  have he : (Case.ofNat 1034).normalize = Case.ofNat 10 := by decide
  rw [he]
  exact case0010
#print axioms case1034

theorem case0011 : checkNat 11 = true := by native_decide
#print axioms case0011

theorem case0012 : checkNat 12 = true := by native_decide
#print axioms case0012

theorem case1036 : checkNat 1036 = true := by
  apply check_of_normalize (Case.ofNat 1036)
  have he : (Case.ofNat 1036).normalize = Case.ofNat 12 := by decide
  rw [he]
  exact case0012
#print axioms case1036

theorem case2060 : checkNat 2060 = true := by
  apply check_of_normalize (Case.ofNat 2060)
  have he : (Case.ofNat 2060).normalize = Case.ofNat 12 := by decide
  rw [he]
  exact case0012
#print axioms case2060

theorem case3084 : checkNat 3084 = true := by
  apply check_of_normalize (Case.ofNat 3084)
  have he : (Case.ofNat 3084).normalize = Case.ofNat 12 := by decide
  rw [he]
  exact case0012
#print axioms case3084

theorem case0013 : checkNat 13 = true := by native_decide
#print axioms case0013

theorem case2061 : checkNat 2061 = true := by
  apply check_of_normalize (Case.ofNat 2061)
  have he : (Case.ofNat 2061).normalize = Case.ofNat 13 := by decide
  rw [he]
  exact case0013
#print axioms case2061

theorem case0014 : checkNat 14 = true := by native_decide
#print axioms case0014

theorem case1038 : checkNat 1038 = true := by
  apply check_of_normalize (Case.ofNat 1038)
  have he : (Case.ofNat 1038).normalize = Case.ofNat 14 := by decide
  rw [he]
  exact case0014
#print axioms case1038

theorem case0015 : checkNat 15 = true := by native_decide
#print axioms case0015

theorem case0016 : checkNat 16 = true := by native_decide
#print axioms case0016

theorem case1040 : checkNat 1040 = true := by
  apply check_of_normalize (Case.ofNat 1040)
  have he : (Case.ofNat 1040).normalize = Case.ofNat 16 := by decide
  rw [he]
  exact case0016
#print axioms case1040

theorem case2064 : checkNat 2064 = true := by
  apply check_of_normalize (Case.ofNat 2064)
  have he : (Case.ofNat 2064).normalize = Case.ofNat 16 := by decide
  rw [he]
  exact case0016
#print axioms case2064

theorem case3088 : checkNat 3088 = true := by
  apply check_of_normalize (Case.ofNat 3088)
  have he : (Case.ofNat 3088).normalize = Case.ofNat 16 := by decide
  rw [he]
  exact case0016
#print axioms case3088

theorem case0017 : checkNat 17 = true := by native_decide
#print axioms case0017

theorem case2065 : checkNat 2065 = true := by
  apply check_of_normalize (Case.ofNat 2065)
  have he : (Case.ofNat 2065).normalize = Case.ofNat 17 := by decide
  rw [he]
  exact case0017
#print axioms case2065

theorem case0018 : checkNat 18 = true := by native_decide
#print axioms case0018

theorem case1042 : checkNat 1042 = true := by
  apply check_of_normalize (Case.ofNat 1042)
  have he : (Case.ofNat 1042).normalize = Case.ofNat 18 := by decide
  rw [he]
  exact case0018
#print axioms case1042

theorem case0019 : checkNat 19 = true := by native_decide
#print axioms case0019

theorem case0020 : checkNat 20 = true := by native_decide
#print axioms case0020

theorem case1044 : checkNat 1044 = true := by
  apply check_of_normalize (Case.ofNat 1044)
  have he : (Case.ofNat 1044).normalize = Case.ofNat 20 := by decide
  rw [he]
  exact case0020
#print axioms case1044

theorem case2068 : checkNat 2068 = true := by
  apply check_of_normalize (Case.ofNat 2068)
  have he : (Case.ofNat 2068).normalize = Case.ofNat 20 := by decide
  rw [he]
  exact case0020
#print axioms case2068

theorem case3092 : checkNat 3092 = true := by
  apply check_of_normalize (Case.ofNat 3092)
  have he : (Case.ofNat 3092).normalize = Case.ofNat 20 := by decide
  rw [he]
  exact case0020
#print axioms case3092

theorem case0021 : checkNat 21 = true := by native_decide
#print axioms case0021

theorem case2069 : checkNat 2069 = true := by
  apply check_of_normalize (Case.ofNat 2069)
  have he : (Case.ofNat 2069).normalize = Case.ofNat 21 := by decide
  rw [he]
  exact case0021
#print axioms case2069

theorem case0022 : checkNat 22 = true := by native_decide
#print axioms case0022

theorem case1046 : checkNat 1046 = true := by
  apply check_of_normalize (Case.ofNat 1046)
  have he : (Case.ofNat 1046).normalize = Case.ofNat 22 := by decide
  rw [he]
  exact case0022
#print axioms case1046

theorem case0023 : checkNat 23 = true := by native_decide
#print axioms case0023

theorem case0024 : checkNat 24 = true := by native_decide
#print axioms case0024

theorem case1048 : checkNat 1048 = true := by
  apply check_of_normalize (Case.ofNat 1048)
  have he : (Case.ofNat 1048).normalize = Case.ofNat 24 := by decide
  rw [he]
  exact case0024
#print axioms case1048

theorem case2072 : checkNat 2072 = true := by
  apply check_of_normalize (Case.ofNat 2072)
  have he : (Case.ofNat 2072).normalize = Case.ofNat 24 := by decide
  rw [he]
  exact case0024
#print axioms case2072

theorem case3096 : checkNat 3096 = true := by
  apply check_of_normalize (Case.ofNat 3096)
  have he : (Case.ofNat 3096).normalize = Case.ofNat 24 := by decide
  rw [he]
  exact case0024
#print axioms case3096

theorem case0025 : checkNat 25 = true := by native_decide
#print axioms case0025

theorem case2073 : checkNat 2073 = true := by
  apply check_of_normalize (Case.ofNat 2073)
  have he : (Case.ofNat 2073).normalize = Case.ofNat 25 := by decide
  rw [he]
  exact case0025
#print axioms case2073

theorem case0026 : checkNat 26 = true := by native_decide
#print axioms case0026

theorem case1050 : checkNat 1050 = true := by
  apply check_of_normalize (Case.ofNat 1050)
  have he : (Case.ofNat 1050).normalize = Case.ofNat 26 := by decide
  rw [he]
  exact case0026
#print axioms case1050

theorem case0027 : checkNat 27 = true := by native_decide
#print axioms case0027

theorem case0028 : checkNat 28 = true := by native_decide
#print axioms case0028

theorem case1052 : checkNat 1052 = true := by
  apply check_of_normalize (Case.ofNat 1052)
  have he : (Case.ofNat 1052).normalize = Case.ofNat 28 := by decide
  rw [he]
  exact case0028
#print axioms case1052

theorem case2076 : checkNat 2076 = true := by
  apply check_of_normalize (Case.ofNat 2076)
  have he : (Case.ofNat 2076).normalize = Case.ofNat 28 := by decide
  rw [he]
  exact case0028
#print axioms case2076

theorem case3100 : checkNat 3100 = true := by
  apply check_of_normalize (Case.ofNat 3100)
  have he : (Case.ofNat 3100).normalize = Case.ofNat 28 := by decide
  rw [he]
  exact case0028
#print axioms case3100

theorem case0029 : checkNat 29 = true := by native_decide
#print axioms case0029

theorem case2077 : checkNat 2077 = true := by
  apply check_of_normalize (Case.ofNat 2077)
  have he : (Case.ofNat 2077).normalize = Case.ofNat 29 := by decide
  rw [he]
  exact case0029
#print axioms case2077

theorem case0030 : checkNat 30 = true := by native_decide
#print axioms case0030

theorem case1054 : checkNat 1054 = true := by
  apply check_of_normalize (Case.ofNat 1054)
  have he : (Case.ofNat 1054).normalize = Case.ofNat 30 := by decide
  rw [he]
  exact case0030
#print axioms case1054

theorem case0031 : checkNat 31 = true := by native_decide
#print axioms case0031

theorem accepted :
    checkNat 0 = true ∧
    checkNat 1 = true ∧
    checkNat 2 = true ∧
    checkNat 3 = true ∧
    checkNat 4 = true ∧
    checkNat 5 = true ∧
    checkNat 6 = true ∧
    checkNat 7 = true ∧
    checkNat 8 = true ∧
    checkNat 9 = true ∧
    checkNat 10 = true ∧
    checkNat 11 = true ∧
    checkNat 12 = true ∧
    checkNat 13 = true ∧
    checkNat 14 = true ∧
    checkNat 15 = true ∧
    checkNat 16 = true ∧
    checkNat 17 = true ∧
    checkNat 18 = true ∧
    checkNat 19 = true ∧
    checkNat 20 = true ∧
    checkNat 21 = true ∧
    checkNat 22 = true ∧
    checkNat 23 = true ∧
    checkNat 24 = true ∧
    checkNat 25 = true ∧
    checkNat 26 = true ∧
    checkNat 27 = true ∧
    checkNat 28 = true ∧
    checkNat 29 = true ∧
    checkNat 30 = true ∧
    checkNat 31 = true ∧
    checkNat 1024 = true ∧
    checkNat 1026 = true ∧
    checkNat 1028 = true ∧
    checkNat 1030 = true ∧
    checkNat 1032 = true ∧
    checkNat 1034 = true ∧
    checkNat 1036 = true ∧
    checkNat 1038 = true ∧
    checkNat 1040 = true ∧
    checkNat 1042 = true ∧
    checkNat 1044 = true ∧
    checkNat 1046 = true ∧
    checkNat 1048 = true ∧
    checkNat 1050 = true ∧
    checkNat 1052 = true ∧
    checkNat 1054 = true ∧
    checkNat 2048 = true ∧
    checkNat 2049 = true ∧
    checkNat 2052 = true ∧
    checkNat 2053 = true ∧
    checkNat 2056 = true ∧
    checkNat 2057 = true ∧
    checkNat 2060 = true ∧
    checkNat 2061 = true ∧
    checkNat 2064 = true ∧
    checkNat 2065 = true ∧
    checkNat 2068 = true ∧
    checkNat 2069 = true ∧
    checkNat 2072 = true ∧
    checkNat 2073 = true ∧
    checkNat 2076 = true ∧
    checkNat 2077 = true ∧
    checkNat 3072 = true ∧
    checkNat 3076 = true ∧
    checkNat 3080 = true ∧
    checkNat 3084 = true ∧
    checkNat 3088 = true ∧
    checkNat 3092 = true ∧
    checkNat 3096 = true ∧
    checkNat 3100 = true := by
  exact ⟨case0000, case0001, case0002, case0003, case0004, case0005, case0006, case0007, case0008, case0009, case0010, case0011, case0012, case0013, case0014, case0015, case0016, case0017, case0018, case0019, case0020, case0021, case0022, case0023, case0024, case0025, case0026, case0027, case0028, case0029, case0030, case0031, case1024, case1026, case1028, case1030, case1032, case1034, case1036, case1038, case1040, case1042, case1044, case1046, case1048, case1050, case1052, case1054, case2048, case2049, case2052, case2053, case2056, case2057, case2060, case2061, case2064, case2065, case2068, case2069, case2072, case2073, case2076, case2077, case3072, case3076, case3080, case3084, case3088, case3092, case3096, case3100⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0000
