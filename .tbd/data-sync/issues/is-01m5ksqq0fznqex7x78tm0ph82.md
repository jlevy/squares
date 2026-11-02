---
type: is
id: is-01m5ksqq0fznqex7x78tm0ph82
title: "Validate: Hosono's zero-margin Lean proof of s(21) = 5 (T-234), build and axiom receipt (6-12 CPU-h estimate)"
kind: task
status: open
priority: 3
version: 6
delegate: null
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T07:13:50.094Z
updated_at: 2026-11-02T14:09:32.540Z
started_at: 2026-11-02T11:10:50.716Z
---
Validation part of think-f2bm (Hiroaki Hosono's hypothesis-free Lean proof that s(21) = 5, a formalization of T-055's point-only route; no issue). Created by c-lean-1023 under the 23 October intake epic, as the lane rules allow; it serves think-f2bm.

## Validation
- Claim: `SquarePacking.n21pts_eq_5 : minSide 21 = 5` in wand125/square-packing-bounds at 77636c63f45a90d9a829417a1722a3bf9bfef37d, `point_n21_L5/lean/zero-margin/`, on Evan Daniel's Lean library and `gen_zmtree.py` at evand/square-packing 6aa82ba457e9eaeaaa3af0833600f27f91a2fce3, certificate `n21-capture-one.txt` (SHA-256 9f631fba...). Checker: Lean v4.33.1's kernel, Mathlib 0df444a3. Packet: packing/resources/web/wand125-n21-zero-margin-lean-2026-09-29/.
- Run: stage `s12/` at 6aa82ba4 from the retained evand packets (every closure file is retained byte for byte; receipts/evand-library-closure-6aa82ba4.json lists them), then `build_zero_margin.sh` with its clone replaced by the staged tree: regenerate the 64 parts, compare with data-sha256.txt, `lake exe cache get`, build the parts one or two at a time and `Sqpack.N21PtsLower`, and `lake env lean N21PtsAxiomsZ.lean`. Accept only `[propext, Classical.choice, Quot.sound]` for `n21pts_eq_5`.
- Cost: 6 to 12 CPU-hours, central 9: generation 1,459 s on 6 workers and the kernel check about 3.5 h wall at 2 parts on the source's Apple M4 under load (its README); an estimate, not a receipt.
- Budget status: runnable under the owner's 40 CPU-hour item cap; above the 2 CPU-hour single run a writer lane of the 23 October pass may start, so it needs the coordinator's word, and a host with about 10 GB of free disk for the toolchain and Mathlib cache (the lane's host had 5.2 GB on 23 October).
- Possible subset: none needed under the cap; the generation alone (about 2.4 CPU-hours) checks data-sha256.txt and decides nothing.
- Depends on: think-f2bm's packet (pushed on claude/intake-2026-10-23-lean-sources); the stage 4 review.
- Done when: a build and axiom receipt is committed on a branch this bead names and registered as a `proof-assistant-checked`, `replayed-here` entry on T-234 (same-implementation: the source's recipe), or the owner dispositions it.
- Machine note: near 6 GB per part; one part at a time fits a 15 GB host. Not alongside a validation gate.

## Notes

2026-11-02 ~13:20Z bold-ritchie-l29 (strong-tier lane L29 of the 31 October intake pass, think-3guf; claimed 11:13Z): GENERATION RUN AND MATCHED; KERNEL CHECK NOT RUN, network policy.

Generation, the one recipe step that needs no Lean, ran here from the retained bytes: `devtools.replay_lean_packet generate wand125-n21 --nproc 2 --cpus 2,3` staged evand/square-packing 6aa82ba4's s12/ from the retained packets in place of the clone build_zero_margin.sh makes (the nine library modules at the closure receipt's Git blobs; gen_zmtree.py, zeromargin.py, ZMTree.lean and n21-capture-one.txt at the four SHA-256 the script pins; pins at the receipt's toolchain and package revisions; 0 kernel-escape tokens), then ran the source's generator under CPython 3.14.7 and NumPy 2.5.2. It wrote 2,076 chunks in 64 parts, 59,433 Z leaves, 5,876 E and 5,591 clips, the census the source reports, and all 66 files match data-sha256.txt (66 listed, 66 generated, 66 matched, none differing, missing or extra; 92,197,153 bytes, not retained). 8,658.0 CPU seconds (2.41 CPU-hours), 5,059.8 s wall, 11:25:29Z to 12:49:49Z, on two cores of a shared four-core x86-64 host under load 3 to 7. Receipt: packing/resources/web/wand125-n21-zero-margin-lean-2026-09-29/receipts/lean-build/generation.json and gen.log (`replay_lean_packet check-generation wand125-n21`: OK). Committed at 79d3f9dea on claude/bold-ritchie-xo28us-l29, draft PR https://github.com/jlevy/squares/pull/887; the packet README (Checks Made Here), E-n021-wand125-zero-margin-lean-report and T-234's next step and notes say so. No rung moves: T-234 stays V0/C0, as check_results derives.

Kernel check: not run. This environment's proxy refuses lakecache.blob.core.windows.net:443 (Mathlib's prebuilt cache; `lake exe cache get` downloaded 0 of 309 attempted files) and release.lean-lang.org:443 (elan's toolchain origin; the GitHub release asset does download). A source build of all of Mathlib (Basic.lean imports it) is far above this bead's price, so nothing was built, per the brief. CPU spent on this bead: 2.41 CPU-hours of the 6 to 12 priced.

To finish, on a host that reaches the cache, from packing/: `.venv/bin/python3 -m devtools.replay_lean_packet generate wand125-n21 --out W --nproc 2 --cpus 2,3` (about 2.4 CPU-hours again, since the 92 MB of parts are not retained), then `run wand125-n21 --out W --cpus 2,3 --jobs 1` (Pts, the 64 parts one lake process at a time, N21PtsLower, the axiom probe for n21pts_ge_5 and n21pts_eq_5, and three negative controls: minSide 21 = 4 given n21pts_eq_5's term, N21PtsLower.lean with n21pts_ge_5 claiming 21/4, and the statement proved by sorry), about 7 CPU-hours by the source's estimate and near 6 GB per part; receipts go to the packet's receipts/lean-build. Then the replayed-here proof-assistant-checked evidence entry on T-234 and a control path, and check_results derives the rung. A mutated-data control on one generated part (the kernel's decide must refuse it) is worth adding then; it needs the generated format, which this run produced but did not retain.

No reply is owed on #782: no rung moved. Draft, if the coordinator wants a status line there: "We regenerated the 64 parts of the zero-margin tree here from the retained generator and certificate on 2 November: all 66 files match data-sha256.txt. The kernel check has not run yet, because the host lacked network access to Mathlib's cache; T-234 stays V0/C0 until it does. The tool and receipt are in #887."

blocked_on: network policy — lakecache.blob.core.windows.net:443 (Mathlib's prebuilt cache; the toolchain installs from its GitHub release asset)
