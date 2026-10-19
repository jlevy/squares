#!/bin/sh
# A214 -- build the C kernel DLL (ONE command):   sh attempts/A214-c-kernel/code/build214.sh
# clang 22.1.8, target x86_64-pc-windows-msvc.  Flags that matter:
#   -ffp-contract=off -fno-fast-math : no FMA contraction, one rounding per operation -- exactly what the float
#                                      filter's forward error bound assumes (and no reassociation).
#   -nostdlib -Wl,-noentry           : this machine has clang but no MSVC CRT import libraries; the kernel needs
#                                      no CRT (it supplies _fltused and memset itself).
# No Python.h, no build system: a plain DLL loaded with ctypes.  Writes build/ckernel214.dll{,.sha256}.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
OUT="$HERE/../build/ckernel214.dll"
CLANG=${CLANG:-"/c/Program Files/LLVM/bin/clang.exe"}
mkdir -p "$HERE/../build"
"$CLANG" -O2 -shared -nostdlib -Wl,-noentry -ffp-contract=off -fno-fast-math -Wall -Wextra -std=c11 \
    -o "$OUT" "$HERE/ckernel214.c"
rm -f "$HERE/../build/ckernel214.lib" "$HERE/../build/ckernel214.exp"   # linker by-products, not needed by ctypes
"$CLANG" --version | head -1
python - "$OUT" <<'PY'
import hashlib, sys
p = sys.argv[1]
h = hashlib.sha256(open(p, "rb").read()).hexdigest()
print("%s  sha256 %s" % (p, h))
open(p + ".sha256", "w").write(h + "  ckernel214.dll\n")
PY
echo "built $OUT"
