import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1504
open Sq19.Endgame.Reduction

theorem case1985 : checkNat 1985 = true := by native_decide
#print axioms case1985

theorem case4033 : checkNat 4033 = true := by
  apply check_of_normalize (Case.ofNat 4033)
  have he : (Case.ofNat 4033).normalize = Case.ofNat 1985 := by decide
  rw [he]
  exact case1985
#print axioms case4033

theorem case1987 : checkNat 1987 = true := by native_decide
#print axioms case1987

theorem case1989 : checkNat 1989 = true := by native_decide
#print axioms case1989

theorem case4037 : checkNat 4037 = true := by
  apply check_of_normalize (Case.ofNat 4037)
  have he : (Case.ofNat 4037).normalize = Case.ofNat 1989 := by decide
  rw [he]
  exact case1989
#print axioms case4037

theorem case1991 : checkNat 1991 = true := by native_decide
#print axioms case1991

theorem case1993 : checkNat 1993 = true := by native_decide
#print axioms case1993

theorem case4041 : checkNat 4041 = true := by
  apply check_of_normalize (Case.ofNat 4041)
  have he : (Case.ofNat 4041).normalize = Case.ofNat 1993 := by decide
  rw [he]
  exact case1993
#print axioms case4041

theorem case1995 : checkNat 1995 = true := by native_decide
#print axioms case1995

theorem case1997 : checkNat 1997 = true := by native_decide
#print axioms case1997

theorem case4045 : checkNat 4045 = true := by
  apply check_of_normalize (Case.ofNat 4045)
  have he : (Case.ofNat 4045).normalize = Case.ofNat 1997 := by decide
  rw [he]
  exact case1997
#print axioms case4045

theorem case1999 : checkNat 1999 = true := by native_decide
#print axioms case1999

theorem case2001 : checkNat 2001 = true := by native_decide
#print axioms case2001

theorem case4049 : checkNat 4049 = true := by
  apply check_of_normalize (Case.ofNat 4049)
  have he : (Case.ofNat 4049).normalize = Case.ofNat 2001 := by decide
  rw [he]
  exact case2001
#print axioms case4049

theorem case2003 : checkNat 2003 = true := by native_decide
#print axioms case2003

theorem case2005 : checkNat 2005 = true := by native_decide
#print axioms case2005

theorem case4053 : checkNat 4053 = true := by
  apply check_of_normalize (Case.ofNat 4053)
  have he : (Case.ofNat 4053).normalize = Case.ofNat 2005 := by decide
  rw [he]
  exact case2005
#print axioms case4053

theorem case2007 : checkNat 2007 = true := by native_decide
#print axioms case2007

theorem case2009 : checkNat 2009 = true := by native_decide
#print axioms case2009

theorem case4057 : checkNat 4057 = true := by
  apply check_of_normalize (Case.ofNat 4057)
  have he : (Case.ofNat 4057).normalize = Case.ofNat 2009 := by decide
  rw [he]
  exact case2009
#print axioms case4057

theorem case2011 : checkNat 2011 = true := by native_decide
#print axioms case2011

theorem case2013 : checkNat 2013 = true := by native_decide
#print axioms case2013

theorem case4061 : checkNat 4061 = true := by
  apply check_of_normalize (Case.ofNat 4061)
  have he : (Case.ofNat 4061).normalize = Case.ofNat 2013 := by decide
  rw [he]
  exact case2013
#print axioms case4061

theorem case2015 : checkNat 2015 = true := by native_decide
#print axioms case2015

theorem case2017 : checkNat 2017 = true := by native_decide
#print axioms case2017

theorem case4065 : checkNat 4065 = true := by
  apply check_of_normalize (Case.ofNat 4065)
  have he : (Case.ofNat 4065).normalize = Case.ofNat 2017 := by decide
  rw [he]
  exact case2017
#print axioms case4065

theorem case2019 : checkNat 2019 = true := by native_decide
#print axioms case2019

theorem case2021 : checkNat 2021 = true := by native_decide
#print axioms case2021

theorem case4069 : checkNat 4069 = true := by
  apply check_of_normalize (Case.ofNat 4069)
  have he : (Case.ofNat 4069).normalize = Case.ofNat 2021 := by decide
  rw [he]
  exact case2021
#print axioms case4069

theorem case2023 : checkNat 2023 = true := by native_decide
#print axioms case2023

theorem case2025 : checkNat 2025 = true := by native_decide
#print axioms case2025

theorem case4073 : checkNat 4073 = true := by
  apply check_of_normalize (Case.ofNat 4073)
  have he : (Case.ofNat 4073).normalize = Case.ofNat 2025 := by decide
  rw [he]
  exact case2025
#print axioms case4073

theorem case2027 : checkNat 2027 = true := by native_decide
#print axioms case2027

theorem case2029 : checkNat 2029 = true := by native_decide
#print axioms case2029

theorem case4077 : checkNat 4077 = true := by
  apply check_of_normalize (Case.ofNat 4077)
  have he : (Case.ofNat 4077).normalize = Case.ofNat 2029 := by decide
  rw [he]
  exact case2029
#print axioms case4077

theorem case2031 : checkNat 2031 = true := by native_decide
#print axioms case2031

theorem case2033 : checkNat 2033 = true := by native_decide
#print axioms case2033

theorem case4081 : checkNat 4081 = true := by
  apply check_of_normalize (Case.ofNat 4081)
  have he : (Case.ofNat 4081).normalize = Case.ofNat 2033 := by decide
  rw [he]
  exact case2033
#print axioms case4081

theorem case2035 : checkNat 2035 = true := by native_decide
#print axioms case2035

theorem case2037 : checkNat 2037 = true := by native_decide
#print axioms case2037

theorem case4085 : checkNat 4085 = true := by
  apply check_of_normalize (Case.ofNat 4085)
  have he : (Case.ofNat 4085).normalize = Case.ofNat 2037 := by decide
  rw [he]
  exact case2037
#print axioms case4085

theorem case2039 : checkNat 2039 = true := by native_decide
#print axioms case2039

theorem case2041 : checkNat 2041 = true := by native_decide
#print axioms case2041

theorem case4089 : checkNat 4089 = true := by
  apply check_of_normalize (Case.ofNat 4089)
  have he : (Case.ofNat 4089).normalize = Case.ofNat 2041 := by decide
  rw [he]
  exact case2041
#print axioms case4089

theorem case2043 : checkNat 2043 = true := by native_decide
#print axioms case2043

theorem case2045 : checkNat 2045 = true := by native_decide
#print axioms case2045

theorem case4093 : checkNat 4093 = true := by
  apply check_of_normalize (Case.ofNat 4093)
  have he : (Case.ofNat 4093).normalize = Case.ofNat 2045 := by decide
  rw [he]
  exact case2045
#print axioms case4093

theorem case2047 : checkNat 2047 = true := by native_decide
#print axioms case2047

theorem accepted :
    checkNat 1985 = true ∧
    checkNat 1987 = true ∧
    checkNat 1989 = true ∧
    checkNat 1991 = true ∧
    checkNat 1993 = true ∧
    checkNat 1995 = true ∧
    checkNat 1997 = true ∧
    checkNat 1999 = true ∧
    checkNat 2001 = true ∧
    checkNat 2003 = true ∧
    checkNat 2005 = true ∧
    checkNat 2007 = true ∧
    checkNat 2009 = true ∧
    checkNat 2011 = true ∧
    checkNat 2013 = true ∧
    checkNat 2015 = true ∧
    checkNat 2017 = true ∧
    checkNat 2019 = true ∧
    checkNat 2021 = true ∧
    checkNat 2023 = true ∧
    checkNat 2025 = true ∧
    checkNat 2027 = true ∧
    checkNat 2029 = true ∧
    checkNat 2031 = true ∧
    checkNat 2033 = true ∧
    checkNat 2035 = true ∧
    checkNat 2037 = true ∧
    checkNat 2039 = true ∧
    checkNat 2041 = true ∧
    checkNat 2043 = true ∧
    checkNat 2045 = true ∧
    checkNat 2047 = true ∧
    checkNat 4033 = true ∧
    checkNat 4037 = true ∧
    checkNat 4041 = true ∧
    checkNat 4045 = true ∧
    checkNat 4049 = true ∧
    checkNat 4053 = true ∧
    checkNat 4057 = true ∧
    checkNat 4061 = true ∧
    checkNat 4065 = true ∧
    checkNat 4069 = true ∧
    checkNat 4073 = true ∧
    checkNat 4077 = true ∧
    checkNat 4081 = true ∧
    checkNat 4085 = true ∧
    checkNat 4089 = true ∧
    checkNat 4093 = true := by
  exact ⟨case1985, case1987, case1989, case1991, case1993, case1995, case1997, case1999, case2001, case2003, case2005, case2007, case2009, case2011, case2013, case2015, case2017, case2019, case2021, case2023, case2025, case2027, case2029, case2031, case2033, case2035, case2037, case2039, case2041, case2043, case2045, case2047, case4033, case4037, case4041, case4045, case4049, case4053, case4057, case4061, case4065, case4069, case4073, case4077, case4081, case4085, case4089, case4093⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1504
