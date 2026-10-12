#!/bin/sh
# Build the verifier and check every record three ways:
#   1. sqverify --precise --certify : high-precision check, then an exact rational certificate
#   2. sqverify --check-cert        : the shipped certificates, checked exactly (no tolerance)
#   3. tools/crosscheck_mpmath.py   : an independent 80-digit check written in Python
# Needs a C++20 compiler, CMake, GMP and MPFR (e.g. `brew install gmp mpfr`,
# `apt-get install libgmp-dev libmpfr-dev`), and Python 3.10+ with mpmath (or uv).
set -eu
cd "$(dirname "$0")"
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release > /dev/null
cmake --build build -j > /dev/null
ctest --test-dir build --output-on-failure
echo "== 1. precise check + exact certificate"
./build/verify/sqverify --precise --certify --cert-dir build/certs records/*.sqpk
echo "== 2. shipped certificates, exact"
./build/verify/sqverify --check-cert records/*.sqcert
echo "== 3. independent mpmath cross-check (80 digits)"
if command -v uv > /dev/null 2>&1; then uv run python tools/crosscheck_mpmath.py --list records/*.sqpk
else python3 tools/crosscheck_mpmath.py --list records/*.sqpk; fi
