import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0928
open Sq19.Endgame.Reduction

theorem case0928 : checkNat 928 = true := by native_decide
#print axioms case0928

theorem case1952 : checkNat 1952 = true := by
  apply check_of_normalize (Case.ofNat 1952)
  have he : (Case.ofNat 1952).normalize = Case.ofNat 928 := by decide
  rw [he]
  exact case0928
#print axioms case1952

theorem case2976 : checkNat 2976 = true := by
  apply check_of_normalize (Case.ofNat 2976)
  have he : (Case.ofNat 2976).normalize = Case.ofNat 928 := by decide
  rw [he]
  exact case0928
#print axioms case2976

theorem case4000 : checkNat 4000 = true := by
  apply check_of_normalize (Case.ofNat 4000)
  have he : (Case.ofNat 4000).normalize = Case.ofNat 928 := by decide
  rw [he]
  exact case0928
#print axioms case4000

theorem case0929 : checkNat 929 = true := by native_decide
#print axioms case0929

theorem case2977 : checkNat 2977 = true := by
  apply check_of_normalize (Case.ofNat 2977)
  have he : (Case.ofNat 2977).normalize = Case.ofNat 929 := by decide
  rw [he]
  exact case0929
#print axioms case2977

theorem case0930 : checkNat 930 = true := by native_decide
#print axioms case0930

theorem case1954 : checkNat 1954 = true := by
  apply check_of_normalize (Case.ofNat 1954)
  have he : (Case.ofNat 1954).normalize = Case.ofNat 930 := by decide
  rw [he]
  exact case0930
#print axioms case1954

theorem case0931 : checkNat 931 = true := by native_decide
#print axioms case0931

theorem case0932 : checkNat 932 = true := by native_decide
#print axioms case0932

theorem case1956 : checkNat 1956 = true := by
  apply check_of_normalize (Case.ofNat 1956)
  have he : (Case.ofNat 1956).normalize = Case.ofNat 932 := by decide
  rw [he]
  exact case0932
#print axioms case1956

theorem case2980 : checkNat 2980 = true := by
  apply check_of_normalize (Case.ofNat 2980)
  have he : (Case.ofNat 2980).normalize = Case.ofNat 932 := by decide
  rw [he]
  exact case0932
#print axioms case2980

theorem case4004 : checkNat 4004 = true := by
  apply check_of_normalize (Case.ofNat 4004)
  have he : (Case.ofNat 4004).normalize = Case.ofNat 932 := by decide
  rw [he]
  exact case0932
#print axioms case4004

theorem case0933 : checkNat 933 = true := by native_decide
#print axioms case0933

theorem case2981 : checkNat 2981 = true := by
  apply check_of_normalize (Case.ofNat 2981)
  have he : (Case.ofNat 2981).normalize = Case.ofNat 933 := by decide
  rw [he]
  exact case0933
#print axioms case2981

theorem case0934 : checkNat 934 = true := by native_decide
#print axioms case0934

theorem case1958 : checkNat 1958 = true := by
  apply check_of_normalize (Case.ofNat 1958)
  have he : (Case.ofNat 1958).normalize = Case.ofNat 934 := by decide
  rw [he]
  exact case0934
#print axioms case1958

theorem case0935 : checkNat 935 = true := by native_decide
#print axioms case0935

theorem case0936 : checkNat 936 = true := by native_decide
#print axioms case0936

theorem case1960 : checkNat 1960 = true := by
  apply check_of_normalize (Case.ofNat 1960)
  have he : (Case.ofNat 1960).normalize = Case.ofNat 936 := by decide
  rw [he]
  exact case0936
#print axioms case1960

theorem case2984 : checkNat 2984 = true := by
  apply check_of_normalize (Case.ofNat 2984)
  have he : (Case.ofNat 2984).normalize = Case.ofNat 936 := by decide
  rw [he]
  exact case0936
#print axioms case2984

theorem case4008 : checkNat 4008 = true := by
  apply check_of_normalize (Case.ofNat 4008)
  have he : (Case.ofNat 4008).normalize = Case.ofNat 936 := by decide
  rw [he]
  exact case0936
#print axioms case4008

theorem case0937 : checkNat 937 = true := by native_decide
#print axioms case0937

theorem case2985 : checkNat 2985 = true := by
  apply check_of_normalize (Case.ofNat 2985)
  have he : (Case.ofNat 2985).normalize = Case.ofNat 937 := by decide
  rw [he]
  exact case0937
#print axioms case2985

theorem case0938 : checkNat 938 = true := by native_decide
#print axioms case0938

theorem case1962 : checkNat 1962 = true := by
  apply check_of_normalize (Case.ofNat 1962)
  have he : (Case.ofNat 1962).normalize = Case.ofNat 938 := by decide
  rw [he]
  exact case0938
#print axioms case1962

theorem case0939 : checkNat 939 = true := by native_decide
#print axioms case0939

theorem case0940 : checkNat 940 = true := by native_decide
#print axioms case0940

theorem case1964 : checkNat 1964 = true := by
  apply check_of_normalize (Case.ofNat 1964)
  have he : (Case.ofNat 1964).normalize = Case.ofNat 940 := by decide
  rw [he]
  exact case0940
#print axioms case1964

theorem case2988 : checkNat 2988 = true := by
  apply check_of_normalize (Case.ofNat 2988)
  have he : (Case.ofNat 2988).normalize = Case.ofNat 940 := by decide
  rw [he]
  exact case0940
#print axioms case2988

theorem case4012 : checkNat 4012 = true := by
  apply check_of_normalize (Case.ofNat 4012)
  have he : (Case.ofNat 4012).normalize = Case.ofNat 940 := by decide
  rw [he]
  exact case0940
#print axioms case4012

theorem case0941 : checkNat 941 = true := by native_decide
#print axioms case0941

theorem case2989 : checkNat 2989 = true := by
  apply check_of_normalize (Case.ofNat 2989)
  have he : (Case.ofNat 2989).normalize = Case.ofNat 941 := by decide
  rw [he]
  exact case0941
#print axioms case2989

theorem case0942 : checkNat 942 = true := by native_decide
#print axioms case0942

theorem case1966 : checkNat 1966 = true := by
  apply check_of_normalize (Case.ofNat 1966)
  have he : (Case.ofNat 1966).normalize = Case.ofNat 942 := by decide
  rw [he]
  exact case0942
#print axioms case1966

theorem case0943 : checkNat 943 = true := by native_decide
#print axioms case0943

theorem case0944 : checkNat 944 = true := by native_decide
#print axioms case0944

theorem case1968 : checkNat 1968 = true := by
  apply check_of_normalize (Case.ofNat 1968)
  have he : (Case.ofNat 1968).normalize = Case.ofNat 944 := by decide
  rw [he]
  exact case0944
#print axioms case1968

theorem case2992 : checkNat 2992 = true := by
  apply check_of_normalize (Case.ofNat 2992)
  have he : (Case.ofNat 2992).normalize = Case.ofNat 944 := by decide
  rw [he]
  exact case0944
#print axioms case2992

theorem case4016 : checkNat 4016 = true := by
  apply check_of_normalize (Case.ofNat 4016)
  have he : (Case.ofNat 4016).normalize = Case.ofNat 944 := by decide
  rw [he]
  exact case0944
#print axioms case4016

theorem case0945 : checkNat 945 = true := by native_decide
#print axioms case0945

theorem case2993 : checkNat 2993 = true := by
  apply check_of_normalize (Case.ofNat 2993)
  have he : (Case.ofNat 2993).normalize = Case.ofNat 945 := by decide
  rw [he]
  exact case0945
#print axioms case2993

theorem case0946 : checkNat 946 = true := by native_decide
#print axioms case0946

theorem case1970 : checkNat 1970 = true := by
  apply check_of_normalize (Case.ofNat 1970)
  have he : (Case.ofNat 1970).normalize = Case.ofNat 946 := by decide
  rw [he]
  exact case0946
#print axioms case1970

theorem case0947 : checkNat 947 = true := by native_decide
#print axioms case0947

theorem case0948 : checkNat 948 = true := by native_decide
#print axioms case0948

theorem case1972 : checkNat 1972 = true := by
  apply check_of_normalize (Case.ofNat 1972)
  have he : (Case.ofNat 1972).normalize = Case.ofNat 948 := by decide
  rw [he]
  exact case0948
#print axioms case1972

theorem case2996 : checkNat 2996 = true := by
  apply check_of_normalize (Case.ofNat 2996)
  have he : (Case.ofNat 2996).normalize = Case.ofNat 948 := by decide
  rw [he]
  exact case0948
#print axioms case2996

theorem case4020 : checkNat 4020 = true := by
  apply check_of_normalize (Case.ofNat 4020)
  have he : (Case.ofNat 4020).normalize = Case.ofNat 948 := by decide
  rw [he]
  exact case0948
#print axioms case4020

theorem case0949 : checkNat 949 = true := by native_decide
#print axioms case0949

theorem case2997 : checkNat 2997 = true := by
  apply check_of_normalize (Case.ofNat 2997)
  have he : (Case.ofNat 2997).normalize = Case.ofNat 949 := by decide
  rw [he]
  exact case0949
#print axioms case2997

theorem case0950 : checkNat 950 = true := by native_decide
#print axioms case0950

theorem case1974 : checkNat 1974 = true := by
  apply check_of_normalize (Case.ofNat 1974)
  have he : (Case.ofNat 1974).normalize = Case.ofNat 950 := by decide
  rw [he]
  exact case0950
#print axioms case1974

theorem case0951 : checkNat 951 = true := by native_decide
#print axioms case0951

theorem case0952 : checkNat 952 = true := by native_decide
#print axioms case0952

theorem case1976 : checkNat 1976 = true := by
  apply check_of_normalize (Case.ofNat 1976)
  have he : (Case.ofNat 1976).normalize = Case.ofNat 952 := by decide
  rw [he]
  exact case0952
#print axioms case1976

theorem case3000 : checkNat 3000 = true := by
  apply check_of_normalize (Case.ofNat 3000)
  have he : (Case.ofNat 3000).normalize = Case.ofNat 952 := by decide
  rw [he]
  exact case0952
#print axioms case3000

theorem case4024 : checkNat 4024 = true := by
  apply check_of_normalize (Case.ofNat 4024)
  have he : (Case.ofNat 4024).normalize = Case.ofNat 952 := by decide
  rw [he]
  exact case0952
#print axioms case4024

theorem case0953 : checkNat 953 = true := by native_decide
#print axioms case0953

theorem case3001 : checkNat 3001 = true := by
  apply check_of_normalize (Case.ofNat 3001)
  have he : (Case.ofNat 3001).normalize = Case.ofNat 953 := by decide
  rw [he]
  exact case0953
#print axioms case3001

theorem case0954 : checkNat 954 = true := by native_decide
#print axioms case0954

theorem case1978 : checkNat 1978 = true := by
  apply check_of_normalize (Case.ofNat 1978)
  have he : (Case.ofNat 1978).normalize = Case.ofNat 954 := by decide
  rw [he]
  exact case0954
#print axioms case1978

theorem case0955 : checkNat 955 = true := by native_decide
#print axioms case0955

theorem case0956 : checkNat 956 = true := by native_decide
#print axioms case0956

theorem case1980 : checkNat 1980 = true := by
  apply check_of_normalize (Case.ofNat 1980)
  have he : (Case.ofNat 1980).normalize = Case.ofNat 956 := by decide
  rw [he]
  exact case0956
#print axioms case1980

theorem case3004 : checkNat 3004 = true := by
  apply check_of_normalize (Case.ofNat 3004)
  have he : (Case.ofNat 3004).normalize = Case.ofNat 956 := by decide
  rw [he]
  exact case0956
#print axioms case3004

theorem case4028 : checkNat 4028 = true := by
  apply check_of_normalize (Case.ofNat 4028)
  have he : (Case.ofNat 4028).normalize = Case.ofNat 956 := by decide
  rw [he]
  exact case0956
#print axioms case4028

theorem case0957 : checkNat 957 = true := by native_decide
#print axioms case0957

theorem case3005 : checkNat 3005 = true := by
  apply check_of_normalize (Case.ofNat 3005)
  have he : (Case.ofNat 3005).normalize = Case.ofNat 957 := by decide
  rw [he]
  exact case0957
#print axioms case3005

theorem case0958 : checkNat 958 = true := by native_decide
#print axioms case0958

theorem case1982 : checkNat 1982 = true := by
  apply check_of_normalize (Case.ofNat 1982)
  have he : (Case.ofNat 1982).normalize = Case.ofNat 958 := by decide
  rw [he]
  exact case0958
#print axioms case1982

theorem case0959 : checkNat 959 = true := by native_decide
#print axioms case0959

theorem accepted :
    checkNat 928 = true ∧
    checkNat 929 = true ∧
    checkNat 930 = true ∧
    checkNat 931 = true ∧
    checkNat 932 = true ∧
    checkNat 933 = true ∧
    checkNat 934 = true ∧
    checkNat 935 = true ∧
    checkNat 936 = true ∧
    checkNat 937 = true ∧
    checkNat 938 = true ∧
    checkNat 939 = true ∧
    checkNat 940 = true ∧
    checkNat 941 = true ∧
    checkNat 942 = true ∧
    checkNat 943 = true ∧
    checkNat 944 = true ∧
    checkNat 945 = true ∧
    checkNat 946 = true ∧
    checkNat 947 = true ∧
    checkNat 948 = true ∧
    checkNat 949 = true ∧
    checkNat 950 = true ∧
    checkNat 951 = true ∧
    checkNat 952 = true ∧
    checkNat 953 = true ∧
    checkNat 954 = true ∧
    checkNat 955 = true ∧
    checkNat 956 = true ∧
    checkNat 957 = true ∧
    checkNat 958 = true ∧
    checkNat 959 = true ∧
    checkNat 1952 = true ∧
    checkNat 1954 = true ∧
    checkNat 1956 = true ∧
    checkNat 1958 = true ∧
    checkNat 1960 = true ∧
    checkNat 1962 = true ∧
    checkNat 1964 = true ∧
    checkNat 1966 = true ∧
    checkNat 1968 = true ∧
    checkNat 1970 = true ∧
    checkNat 1972 = true ∧
    checkNat 1974 = true ∧
    checkNat 1976 = true ∧
    checkNat 1978 = true ∧
    checkNat 1980 = true ∧
    checkNat 1982 = true ∧
    checkNat 2976 = true ∧
    checkNat 2977 = true ∧
    checkNat 2980 = true ∧
    checkNat 2981 = true ∧
    checkNat 2984 = true ∧
    checkNat 2985 = true ∧
    checkNat 2988 = true ∧
    checkNat 2989 = true ∧
    checkNat 2992 = true ∧
    checkNat 2993 = true ∧
    checkNat 2996 = true ∧
    checkNat 2997 = true ∧
    checkNat 3000 = true ∧
    checkNat 3001 = true ∧
    checkNat 3004 = true ∧
    checkNat 3005 = true ∧
    checkNat 4000 = true ∧
    checkNat 4004 = true ∧
    checkNat 4008 = true ∧
    checkNat 4012 = true ∧
    checkNat 4016 = true ∧
    checkNat 4020 = true ∧
    checkNat 4024 = true ∧
    checkNat 4028 = true := by
  exact ⟨case0928, case0929, case0930, case0931, case0932, case0933, case0934, case0935, case0936, case0937, case0938, case0939, case0940, case0941, case0942, case0943, case0944, case0945, case0946, case0947, case0948, case0949, case0950, case0951, case0952, case0953, case0954, case0955, case0956, case0957, case0958, case0959, case1952, case1954, case1956, case1958, case1960, case1962, case1964, case1966, case1968, case1970, case1972, case1974, case1976, case1978, case1980, case1982, case2976, case2977, case2980, case2981, case2984, case2985, case2988, case2989, case2992, case2993, case2996, case2997, case3000, case3001, case3004, case3005, case4000, case4004, case4008, case4012, case4016, case4020, case4024, case4028⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0928
