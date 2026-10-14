# A214 -- THE C KERNEL for the hot integer loops (clang 22 installed by the PI, 2026-09-14). Opus. LAUNCH-AND-EXIT.
Compiler: C:\Program Files\LLVM\bin\clang.exe (clang 22.1.8, target x86_64-pc-windows-msvc; __int128 available).
Build a DLL with clang (-O2 -shared, plain C, no Python.h needed) loaded via ctypes; keep A213's Python-int path as
the reference and the fallback.
Targets, in order (A213's notes/int_polycore.md section 6 is the design; attempts/A213-int-polycore/code/polycore_int.py,
polycore_fast.py, polycore_vec.py are the reference implementations; A213b's pinclip_int.py when it lands):
 1. vertex certification (`vertex_ok` batches: N pieces x V vertices): the Phase-2 float filter in C (double arithmetic
    with A213's rigorous per-element error bound; a pair the filter cannot decide is returned as UNDECIDED and settled
    by the Python-int exact test) -- exactness preserved by construction; bit bound irrelevant on the C side;
 2. the exact tests themselves in C with three-limb 192-bit integer arithmetic (endpoint < 2^142, discriminant
    < 2^183 per A213's bound) so the fallback is also in C; differential-tested against Python ints;
 3. the rectangle-obstacle clip primitives (after A213b lands; same pattern).
Differential tests: A213's replay (441 rebuilds) and fuzz through the kernel with 0 mismatches; a build script
(code/build214.sh / .ps1) that compiles the DLL and runs the tests; graceful fallback to the Python path if the DLL is
missing or the machine differs (the DLL is committed in build/ with its sha256 and the clang version; rebuild is one
command).  Wire through A213's mbpatch213 behind A214_CKERNEL (default ON after 0 mismatches).  Measure per call and
on the Y0202 pad-0 900 s run (isolated dirs; baseline = the current code with A213 on).  Ops as A213's brief: never
edit the READ-ONLY libraries; never touch the running workers (A211 p2a/p2b, A212, k0; A213b and A211f are running
too -- do not edit their files; coordinate through mbpatch213's flag layer only); explicit-pathspec commits; no
monitors, no waiting turns.  notes/c_kernel.md (what is in C, the error bound used, the fallback protocol), results/
timing214.md, registry row, LOG entry.  Report once (per-call and per-run tables, mismatch counts, the build command,
commits) and EXIT.
