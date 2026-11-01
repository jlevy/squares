---
type: is
id: is-01m5w3r23g3vvnxq36gm6cqcsq
title: Audit wand125's ValidTilt9 build logs for a source-build admission of T-251 (V3, no Lean build) (#643)
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m51jy7f6haemzycjpxtrhbs7
created_at: 2026-10-26T12:42:42.672Z
updated_at: 2026-10-26T12:42:42.672Z
---
The source-build admission audit that could give T-251 V3 without a Lean build (epistemics.md, Reported Formal Proofs and Source Builds), finding M-1 of the stage 4 review docs/project/reviews/review-2026-10-26-wand125-validtilt9-lean.md (think-90po, #643). The retained receipts of wand125's ValidTilt9 run are main.log (the assembly of Main.lean and the axiom printout) and the README's table summed from tasks.jsonl; tasks.jsonl itself and the digests of the 1,275,911 generated modules are release assets pinned by digest in the packet's lean/receipts/ASSETS.sha256 and not retained.

## Validation
- Claim: T-251's reported build of SquarePacking.LemmaELeaf.validTilt9 / valid9 / bentz4 at wand125/square-packing 319a779 (Lean v4.33.1), whose generated sources SOURCES.sha256 lists and whose per-module kernel checks tasks.jsonl of both machines records; checker: the source's own run, read, not rerun.
- Run: download v9-logs.tar.zst (c3c856968207fd1482712efb5c0b1229572ca70fcb2088da695932fdaf0d29ab) and SOURCES.sha256.zst (0367b0e78b60e654273442d27f92f4509e7d0bb5a3ea940f1a39aab6d70739fd) and check them against ASSETS.sha256; retain them or what of them the audit needs, by OR-18's rule for bulk data; write a devtools program (OR-1) that checks every module SOURCES.sha256 lists has an exit-0 lean -o task (leaf, row group or root) under the v4.33.1 toolchain, that Main.lean and Axioms9.lean's runs are the main.log ones, and that the README's counts (140,466 leaf, 1,129,519 group, 16,309 root tasks; 10,483 passed twice; 102 killed and re-run) reconcile; then a qualifying audit record, as the 15 October Fitzharding admission audit did, assessing recoverability, build pins, completeness, statement fidelity and the trust boundary; register the source-build entry if it qualifies.
- Cost: minutes of CPU; the two assets' sizes were not read (the source's logs asset also holds every driver version and the hand-built certificates' logs).
- Budget status: runnable (well under the 40 CPU-hour cap), gated on disk on the shared host and on a records lane.
- Possible subset under the cap: not needed.
- Depends on: nothing; independent of think-rw3i.
- Done when: an audit record under docs/project/reviews/ admits or declines the source build, and, if admitted, a source-build evidence entry (assurance verified, method proof-assistant-checked, origin external, performed_by source-author, build_receipt and axioms_receipt retained) is cited by T-251, or the reason it does not qualify is recorded on T-251.
- Machine note: no Lean; a few hundred MB of disk at most, by estimate; can share the host with a gate.
