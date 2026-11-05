#!/usr/bin/env bash
# Run one review program under the project's Python 3.14 in isolated mode (-I), at
# nice 19, with the programs directory on sys.path, and print its CPU time.
# Usage: run.sh PROGRAM.py ARGS...
set -euo pipefail
PROG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKING="${PACKING:-/home/user/squares/packing}"
prog="$1"; shift
TIMEFORMAT="cpu: user %U s, sys %S s, wall %R s"
cd "$PACKING"
time nice -n 19 "$HOME/.local/bin/uv" run --frozen --all-extras --group dev python -I -B -c \
  "import sys, runpy; sys.path.insert(0, sys.argv[1]); sys.argv = sys.argv[2:]; runpy.run_path(sys.argv[0], run_name='__main__')" \
  "$PROG_DIR" "$PROG_DIR/$prog" "$@"
