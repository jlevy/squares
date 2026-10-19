import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1472
open Sq19.Endgame.Reduction

theorem case1921 : checkNat 1921 = true := by native_decide
#print axioms case1921

theorem case3969 : checkNat 3969 = true := by
  apply check_of_normalize (Case.ofNat 3969)
  have he : (Case.ofNat 3969).normalize = Case.ofNat 1921 := by decide
  rw [he]
  exact case1921
#print axioms case3969

theorem case1923 : checkNat 1923 = true := by native_decide
#print axioms case1923

theorem case1925 : checkNat 1925 = true := by native_decide
#print axioms case1925

theorem case3973 : checkNat 3973 = true := by
  apply check_of_normalize (Case.ofNat 3973)
  have he : (Case.ofNat 3973).normalize = Case.ofNat 1925 := by decide
  rw [he]
  exact case1925
#print axioms case3973

theorem case1927 : checkNat 1927 = true := by native_decide
#print axioms case1927

theorem case1929 : checkNat 1929 = true := by native_decide
#print axioms case1929

theorem case3977 : checkNat 3977 = true := by
  apply check_of_normalize (Case.ofNat 3977)
  have he : (Case.ofNat 3977).normalize = Case.ofNat 1929 := by decide
  rw [he]
  exact case1929
#print axioms case3977

theorem case1931 : checkNat 1931 = true := by native_decide
#print axioms case1931

theorem case1933 : checkNat 1933 = true := by native_decide
#print axioms case1933

theorem case3981 : checkNat 3981 = true := by
  apply check_of_normalize (Case.ofNat 3981)
  have he : (Case.ofNat 3981).normalize = Case.ofNat 1933 := by decide
  rw [he]
  exact case1933
#print axioms case3981

theorem case1935 : checkNat 1935 = true := by native_decide
#print axioms case1935

theorem case1937 : checkNat 1937 = true := by native_decide
#print axioms case1937

theorem case3985 : checkNat 3985 = true := by
  apply check_of_normalize (Case.ofNat 3985)
  have he : (Case.ofNat 3985).normalize = Case.ofNat 1937 := by decide
  rw [he]
  exact case1937
#print axioms case3985

theorem case1939 : checkNat 1939 = true := by native_decide
#print axioms case1939

theorem case1941 : checkNat 1941 = true := by native_decide
#print axioms case1941

theorem case3989 : checkNat 3989 = true := by
  apply check_of_normalize (Case.ofNat 3989)
  have he : (Case.ofNat 3989).normalize = Case.ofNat 1941 := by decide
  rw [he]
  exact case1941
#print axioms case3989

theorem case1943 : checkNat 1943 = true := by native_decide
#print axioms case1943

theorem case1945 : checkNat 1945 = true := by native_decide
#print axioms case1945

theorem case3993 : checkNat 3993 = true := by
  apply check_of_normalize (Case.ofNat 3993)
  have he : (Case.ofNat 3993).normalize = Case.ofNat 1945 := by decide
  rw [he]
  exact case1945
#print axioms case3993

theorem case1947 : checkNat 1947 = true := by native_decide
#print axioms case1947

theorem case1949 : checkNat 1949 = true := by native_decide
#print axioms case1949

theorem case3997 : checkNat 3997 = true := by
  apply check_of_normalize (Case.ofNat 3997)
  have he : (Case.ofNat 3997).normalize = Case.ofNat 1949 := by decide
  rw [he]
  exact case1949
#print axioms case3997

theorem case1951 : checkNat 1951 = true := by native_decide
#print axioms case1951

theorem case1953 : checkNat 1953 = true := by native_decide
#print axioms case1953

theorem case4001 : checkNat 4001 = true := by
  apply check_of_normalize (Case.ofNat 4001)
  have he : (Case.ofNat 4001).normalize = Case.ofNat 1953 := by decide
  rw [he]
  exact case1953
#print axioms case4001

theorem case1955 : checkNat 1955 = true := by native_decide
#print axioms case1955

theorem case1957 : checkNat 1957 = true := by native_decide
#print axioms case1957

theorem case4005 : checkNat 4005 = true := by
  apply check_of_normalize (Case.ofNat 4005)
  have he : (Case.ofNat 4005).normalize = Case.ofNat 1957 := by decide
  rw [he]
  exact case1957
#print axioms case4005

theorem case1959 : checkNat 1959 = true := by native_decide
#print axioms case1959

theorem case1961 : checkNat 1961 = true := by native_decide
#print axioms case1961

theorem case4009 : checkNat 4009 = true := by
  apply check_of_normalize (Case.ofNat 4009)
  have he : (Case.ofNat 4009).normalize = Case.ofNat 1961 := by decide
  rw [he]
  exact case1961
#print axioms case4009

theorem case1963 : checkNat 1963 = true := by native_decide
#print axioms case1963

theorem case1965 : checkNat 1965 = true := by native_decide
#print axioms case1965

theorem case4013 : checkNat 4013 = true := by
  apply check_of_normalize (Case.ofNat 4013)
  have he : (Case.ofNat 4013).normalize = Case.ofNat 1965 := by decide
  rw [he]
  exact case1965
#print axioms case4013

theorem case1967 : checkNat 1967 = true := by native_decide
#print axioms case1967

theorem case1969 : checkNat 1969 = true := by native_decide
#print axioms case1969

theorem case4017 : checkNat 4017 = true := by
  apply check_of_normalize (Case.ofNat 4017)
  have he : (Case.ofNat 4017).normalize = Case.ofNat 1969 := by decide
  rw [he]
  exact case1969
#print axioms case4017

theorem case1971 : checkNat 1971 = true := by native_decide
#print axioms case1971

theorem case1973 : checkNat 1973 = true := by native_decide
#print axioms case1973

theorem case4021 : checkNat 4021 = true := by
  apply check_of_normalize (Case.ofNat 4021)
  have he : (Case.ofNat 4021).normalize = Case.ofNat 1973 := by decide
  rw [he]
  exact case1973
#print axioms case4021

theorem case1975 : checkNat 1975 = true := by native_decide
#print axioms case1975

theorem case1977 : checkNat 1977 = true := by native_decide
#print axioms case1977

theorem case4025 : checkNat 4025 = true := by
  apply check_of_normalize (Case.ofNat 4025)
  have he : (Case.ofNat 4025).normalize = Case.ofNat 1977 := by decide
  rw [he]
  exact case1977
#print axioms case4025

theorem case1979 : checkNat 1979 = true := by native_decide
#print axioms case1979

theorem case1981 : checkNat 1981 = true := by native_decide
#print axioms case1981

theorem case4029 : checkNat 4029 = true := by
  apply check_of_normalize (Case.ofNat 4029)
  have he : (Case.ofNat 4029).normalize = Case.ofNat 1981 := by decide
  rw [he]
  exact case1981
#print axioms case4029

theorem case1983 : checkNat 1983 = true := by native_decide
#print axioms case1983

theorem accepted :
    checkNat 1921 = true ∧
    checkNat 1923 = true ∧
    checkNat 1925 = true ∧
    checkNat 1927 = true ∧
    checkNat 1929 = true ∧
    checkNat 1931 = true ∧
    checkNat 1933 = true ∧
    checkNat 1935 = true ∧
    checkNat 1937 = true ∧
    checkNat 1939 = true ∧
    checkNat 1941 = true ∧
    checkNat 1943 = true ∧
    checkNat 1945 = true ∧
    checkNat 1947 = true ∧
    checkNat 1949 = true ∧
    checkNat 1951 = true ∧
    checkNat 1953 = true ∧
    checkNat 1955 = true ∧
    checkNat 1957 = true ∧
    checkNat 1959 = true ∧
    checkNat 1961 = true ∧
    checkNat 1963 = true ∧
    checkNat 1965 = true ∧
    checkNat 1967 = true ∧
    checkNat 1969 = true ∧
    checkNat 1971 = true ∧
    checkNat 1973 = true ∧
    checkNat 1975 = true ∧
    checkNat 1977 = true ∧
    checkNat 1979 = true ∧
    checkNat 1981 = true ∧
    checkNat 1983 = true ∧
    checkNat 3969 = true ∧
    checkNat 3973 = true ∧
    checkNat 3977 = true ∧
    checkNat 3981 = true ∧
    checkNat 3985 = true ∧
    checkNat 3989 = true ∧
    checkNat 3993 = true ∧
    checkNat 3997 = true ∧
    checkNat 4001 = true ∧
    checkNat 4005 = true ∧
    checkNat 4009 = true ∧
    checkNat 4013 = true ∧
    checkNat 4017 = true ∧
    checkNat 4021 = true ∧
    checkNat 4025 = true ∧
    checkNat 4029 = true := by
  exact ⟨case1921, case1923, case1925, case1927, case1929, case1931, case1933, case1935, case1937, case1939, case1941, case1943, case1945, case1947, case1949, case1951, case1953, case1955, case1957, case1959, case1961, case1963, case1965, case1967, case1969, case1971, case1973, case1975, case1977, case1979, case1981, case1983, case3969, case3973, case3977, case3981, case3985, case3989, case3993, case3997, case4001, case4005, case4009, case4013, case4017, case4021, case4025, case4029⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1472
