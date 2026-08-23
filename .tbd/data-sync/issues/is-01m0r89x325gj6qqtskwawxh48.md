---
type: is
id: is-01m0r89x325gj6qqtskwawxh48
title: The golden's annealer_gap is a non-portable fixture, and the review's repair does not fix it
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0pqfp4rm5r4fy7ys6t03h0w
created_at: 2026-08-23T21:26:54.818Z
updated_at: 2026-08-23T21:26:54.818Z
---
Recorded 2026-08-23 after verifying the PR #15 review's F-16 reproduction claim and finding it does not hold. Read this BEFORE implementing F-16's stated repair.

WHAT THE REVIEW CLAIMS: "The committed file did not reproduce from the checked-in engine. After an explicit release build, fixed seed 7 at n=10 annealed to gap +0.077126752369 and quenched to (8 + 5*sqrt(2))/4 ... The standalone command did not build the engine, so an untracked stale binary could supply its supposedly fixed inputs." Its repair: build the source-locked engine before every standalone rebuild.

WHAT ACTUALLY HAPPENS: on merged main, after `cargo build --release` of the checked-in engine, n=10 seed 7 gives annealer gap +0.021003996487 and quenches to (6 + sqrt(2))/2 -- matching the committed golden. Three consecutive runs gave byte-identical 3.728110777674047. The fixture reproduces. n=5 matches too.

There are now THREE values for one nominally fixed input:
    +0.021003996488   committed golden on main
    +0.021003996487   this environment, clean build, 3/3 stable
    +0.077126752369   the PR #15 review text
    +0.000493446      PR #15's OWN committed golden

PR #15 does not touch sqsearch/ or perimeter_test.py, so the annealer source is identical on both branches. run_chain is budget-driven with no wall-clock term, chains are keyed by (seed, chain), and the reduction is a deterministic loop over a collected Vec -- so this is not core count, not scheduling, and both parties observed run-to-run stability.

THE REAL DEFECT: a simulated annealer is chaotic. One ULP in a single accept/reject comparison diverges the trajectory completely. With lto = "fat", codegen-units = 1, opt-level = 3, a different Rust version or target microarchitecture changes float contraction and the output changes entirely while staying perfectly deterministic within each environment. The fixture is not stale, it is NON-PORTABLE.

WHY THIS MATTERS MORE THAN THE DIAGNOSIS IT REPLACES:
- the prescribed repair does not fix it. Building the engine first is exactly what was done here, and it still differs from PR #15.
- PR #15's own committed golden carries the same defect. Its 0.000493446 will not reproduce elsewhere either. The branch shipped a fresh instance of the bug it diagnosed.
- an agent who implements the stated repair will believe the problem is solved.

FIX: the ladder's ORACLE is robust -- every environment quenched to the proved optimum and recognised the right closed form. Only the recorded trajectory scalar moves. So assert the oracle and stop committing the trajectory: drop annealer_gap from the byte-compared surface (keep it as printed diagnostic output), or store it with an explicit tolerance plus a recorded toolchain and CPU fingerprint. Do not chase build hermeticity for a chaotic search.
