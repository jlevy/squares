---
type: is
id: is-01m5vbhnfjacz0nb5shhmjmrw2
title: "Valid7 in the Lean kernel: the owner's choice of a sample rebuild, the full 798 CPU-hour build, or neither (#537)"
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
dependencies: []
parent_id: is-01m4pcbr88e5we5fgkmf7qhfgv
created_at: 2026-10-26T05:39:47.313Z
updated_at: 2026-10-26T05:39:47.313Z
---
The rebuild decision for wand125's (Hiroaki Hosono's) Lean kernel proof of Evan Daniel's Valid7, registered on 26 October 2026 as a reported formalization of T-064 (#537, think-0ayk, w-imports-1026). Version 1 is retained in packing/resources/web/evand-valid7-lean-2026-10-11/ (the closure at evand/square-packing 060c1a1, the generators, VALID7.md, and the root-name audit receipts/root-names.json, which pins the release asset v7cert.tar.zst by SHA-256); version 2 is pinned by digest in packing/resources/web/wand125-valid7-lean-v2-2026-10-17/ (wand125/square-packing 649a920, release valid7-lean-v2).

## Validation
- Claim: theorem valid7 : Bentz.Valid7, theorem bentz : ∀ k ≥ 6, minSide (k ^ 2 - 3) = k and theorem validTilt7, with axioms propext, Classical.choice and Quot.sound; checker: Lean v4.33.1's kernel. Version 2: 62,626 generated files (generated-sources.sha256), on Daniel's library at wand125 c5c7f00 (upstream 3f004b7 plus RowMinN.lean and a changed LemmaEKM.lean).
- Run, full: version 2's fetch.sh into a checkout of the library commit, then verify.py --jobs N (library digests, every generated module in import order, Main.lean, Axioms7.lean against expected/).
- Run, sample: the same, for a chosen set of roots (each root's leaf and row-group modules, then its root module), compared with generated-sources.sha256; Main.lean cannot be checked without every root.
- Cost, full: about 798 CPU-hours by version 2's README (re-certification 19.4, sources 0.3, leaf modules 639.3, row groups 127.3, root modules 11.4, Main.lean and Axioms7.lean under a minute each; the components sum to 797.7), peaks of 37.0 GB for a leaf module and 50.6 GB for Main.lean, the 345 MB v7-sources.tar.zst; version 1 about 6,650 CPU-hours by VALID7.md. The 18 October note on #537 that the components do not sum to the total is resolved by the README's own table.
- Cost, sample: about 4.8 CPU-minutes a root on average (the leaf, row-group and root modules' 778 CPU-hours over 9,800 roots), so 100 roots about 8 CPU-hours, plus Lean and Mathlib (about 5 GB) and the 345 MB sources asset; roots whose heaviest module fits the host's memory only, so not a uniform sample on a 15 GB host. An estimate from the README, not a receipt.
- Budget status: gated on decision. The full build is about 20 times the owner's 40 CPU-hour item cap and needs a host with at least 51 GB; a sample fits the cap but is a component check that substantiates no whole value (epistemics.md) and moves no rung.
- Possible subset under the cap: a sample of about 100 roots, chosen by the task log in v7r-logs.tar.zst (2.9 MB) to cover light and heavy roots that fit the host, compared with generated-sources.sha256: about 8 CPU-hours.
- Depends on: the owner's decision between a sample, the full build, or neither (#537; #543's budget lines).
- Done when: the owner's choice is recorded on #537 and in result-requests.yaml; for a full build, its receipts and axiom output are retained and an evidence entry with origin replayed-here is cited by the formalization entry (T-249); for a sample, its receipt is retained as a component check.
- Machine note: the full build needs a 48-vCPU, 376 GB class machine as the source used (29.4 hours there); a sample can run beside nothing else on a 15 GB host.
