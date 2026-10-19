#!/usr/bin/env bash
# Run a command in the environment for exactsolve / minpoly / verify_exact:
# msolve and python 3.13 from nixpkgs; a venv (.venv, gitignored) with pinned numpy, scipy, mpmath, sympy, python-flint.
#   ./env.sh python3 minpoly.py ...
# The versions are those of the 10-05 batch: exactsolve's Newton is sensitive to LAPACK/BLAS details (n = 18 diverges
# with numpy 2.5.2 / scipy 1.18.1 and converges with 2.4.2 / 1.17.0).  msolve 0.10.1 tested.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
if [ -z "${EXACT_ENV:-}" ]; then
  exec nix --extra-experimental-features 'nix-command flakes' shell --impure --expr \
    'with import (builtins.getFlake "nixpkgs") {}; [ msolve python313 ]' \
    -c env EXACT_ENV=1 "$0" "$@"
fi
if [ ! -x "$here/.venv/bin/python3" ]; then
  python3 -m venv "$here/.venv"
  "$here/.venv/bin/pip" install -q numpy==2.4.2 scipy==1.17.0 mpmath==1.3.0 sympy==1.14.0 python-flint==0.9.0
fi
export PATH="$here/.venv/bin:$PATH" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
exec "$@"
