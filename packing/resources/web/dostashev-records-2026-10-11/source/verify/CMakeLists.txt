# sqverify: fast double screen, MPFR precise recheck, exact GMP certificate.

find_package(Threads REQUIRED)

set(_sqv_hints /opt/homebrew /usr/local)
find_path(GMP_INCLUDE_DIR gmp.h HINTS ${_sqv_hints} PATH_SUFFIXES include)
find_path(GMPXX_INCLUDE_DIR gmpxx.h HINTS ${_sqv_hints} PATH_SUFFIXES include)
find_path(MPFR_INCLUDE_DIR mpfr.h HINTS ${_sqv_hints} PATH_SUFFIXES include)
find_library(GMP_LIBRARY gmp HINTS ${_sqv_hints} PATH_SUFFIXES lib)
find_library(GMPXX_LIBRARY gmpxx HINTS ${_sqv_hints} PATH_SUFFIXES lib)
find_library(MPFR_LIBRARY mpfr HINTS ${_sqv_hints} PATH_SUFFIXES lib)
foreach(v GMP_INCLUDE_DIR GMPXX_INCLUDE_DIR MPFR_INCLUDE_DIR GMP_LIBRARY GMPXX_LIBRARY MPFR_LIBRARY)
  if(NOT ${v})
    message(FATAL_ERROR "verify/: ${v} not found. Install GMP and MPFR (brew install gmp mpfr).")
  endif()
endforeach()
message(STATUS "sqverify: GMP ${GMP_LIBRARY}, MPFR ${MPFR_LIBRARY}")

# External libraries as IMPORTED targets (like a find_package config would provide), so their
# headers are consumed as third-party headers rather than compiled as part of this project.
if(NOT TARGET sqv::gmp)
  add_library(sqv::gmp UNKNOWN IMPORTED)
  set_target_properties(sqv::gmp PROPERTIES IMPORTED_LOCATION ${GMP_LIBRARY}
    INTERFACE_INCLUDE_DIRECTORIES ${GMP_INCLUDE_DIR})
  add_library(sqv::gmpxx UNKNOWN IMPORTED)
  set_target_properties(sqv::gmpxx PROPERTIES IMPORTED_LOCATION ${GMPXX_LIBRARY}
    INTERFACE_INCLUDE_DIRECTORIES ${GMPXX_INCLUDE_DIR} INTERFACE_LINK_LIBRARIES sqv::gmp)
  add_library(sqv::mpfr UNKNOWN IMPORTED)
  set_target_properties(sqv::mpfr PROPERTIES IMPORTED_LOCATION ${MPFR_LIBRARY}
    INTERFACE_INCLUDE_DIRECTORIES ${MPFR_INCLUDE_DIR} INTERFACE_LINK_LIBRARIES sqv::gmp)
endif()

set(SQV_WARNINGS -Wall -Wextra -Wpedantic)

add_library(sqverify_core STATIC
  src/numparse.cpp
  src/sqpk.cpp
  src/verifier.cpp
  src/json_out.cpp
)
target_include_directories(sqverify_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_link_libraries(sqverify_core PUBLIC sqv::mpfr sqv::gmpxx sqv::gmp Threads::Threads)
target_compile_features(sqverify_core PUBLIC cxx_std_20)
target_compile_options(sqverify_core PRIVATE ${SQV_WARNINGS})

add_executable(sqverify src/sqverify.cpp)
target_link_libraries(sqverify PRIVATE sqverify_core)
target_compile_options(sqverify PRIVATE ${SQV_WARNINGS})

# ---- tests ---------------------------------------------------------------
set(SQV_TEST_DATA ${CMAKE_CURRENT_SOURCE_DIR}/tests/data)
add_executable(sqverify_tests tests/test_sqverify.cpp)
target_link_libraries(sqverify_tests PRIVATE sqverify_core)
target_compile_options(sqverify_tests PRIVATE ${SQV_WARNINGS})
target_compile_definitions(sqverify_tests PRIVATE SQV_TEST_DATA="${SQV_TEST_DATA}")

set(SQV_UNIT_TESTS
  decimal_parser
  rational_parser
  sat_formula_vs_bruteforce
  trivial_grid
  goebel5
  overlap_pair
  poking_out
  overlap_1e20_axis
  overlap_1e20_rotated
  touching_rotated
  single_free_square
  certify_rejects_overlap
  certify_roundtrip_check_cert
  check_cert_good
  check_cert_bad
  check_cert_pythagorean
  malformed_input
)
foreach(t ${SQV_UNIT_TESTS})
  add_test(NAME sqverify.${t} COMMAND sqverify_tests ${t})
endforeach()

# CLI exit-status tests.
add_test(NAME sqverify.cli_valid_exit0
  COMMAND sqverify --precise --certify ${SQV_TEST_DATA}/grid9.sqpk ${SQV_TEST_DATA}/goebel5.sqpk)
add_test(NAME sqverify.cli_overlap_exit1
  COMMAND sqverify --precise ${SQV_TEST_DATA}/overlap_pair.sqpk)
set_tests_properties(sqverify.cli_overlap_exit1 PROPERTIES WILL_FAIL TRUE)
add_test(NAME sqverify.cli_outside_exit1
  COMMAND sqverify ${SQV_TEST_DATA}/poking_out.sqpk)
set_tests_properties(sqverify.cli_outside_exit1 PROPERTIES WILL_FAIL TRUE)
add_test(NAME sqverify.cli_1e20_double_exit0
  COMMAND sqverify ${SQV_TEST_DATA}/overlap_1e20_axis.sqpk)
add_test(NAME sqverify.cli_1e20_precise_exit1
  COMMAND sqverify --precise ${SQV_TEST_DATA}/overlap_1e20_axis.sqpk)
set_tests_properties(sqverify.cli_1e20_precise_exit1 PROPERTIES WILL_FAIL TRUE)
add_test(NAME sqverify.cli_certify_fail_exit1
  COMMAND sqverify --certify ${SQV_TEST_DATA}/overlap_1e3.sqpk)
set_tests_properties(sqverify.cli_certify_fail_exit1 PROPERTIES WILL_FAIL TRUE)
add_test(NAME sqverify.cli_check_cert_good_exit0
  COMMAND sqverify --check-cert ${SQV_TEST_DATA}/grid4.sqcert ${SQV_TEST_DATA}/pythagorean.sqcert)
add_test(NAME sqverify.cli_check_cert_bad_exit1
  COMMAND sqverify --check-cert ${SQV_TEST_DATA}/grid4_bad.sqcert)
set_tests_properties(sqverify.cli_check_cert_bad_exit1 PROPERTIES WILL_FAIL TRUE)
add_test(NAME sqverify.cli_missing_file_exit1
  COMMAND sqverify ${SQV_TEST_DATA}/does_not_exist.sqpk)
set_tests_properties(sqverify.cli_missing_file_exit1 PROPERTIES WILL_FAIL TRUE)
