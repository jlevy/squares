---
type: is
id: is-01m5vbhr9d1rxpjb3fah1588s9
title: Replay wand125's ValidTilt9 kernel proof (about 7,400 CPU-hours, 230 GB), held above the cap (#643)
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
dependencies: []
parent_id: is-01m51jy7f6haemzycjpxtrhbs7
created_at: 2026-10-26T05:39:50.188Z
updated_at: 2026-10-26T05:39:50.188Z
---
The kernel replay of wand125's (Hiroaki Hosono's) Lean proof of Evan Daniel's ValidTilt9, and with his reduction of s(k^2 - 4) = k for every k >= 8, registered on 26 October 2026 as a reported formalization of T-081 (#643, think-jh0n, w-imports-1026). The lean/ directory is retained in packing/resources/web/wand125-validtilt9-lean-2026-10-16/ at wand125/square-packing 319a779, with the release validtilt9-lean-v1's three assets pinned by digest in its lean/receipts/ASSETS.sha256.

## Validation
- Claim: validTilt9 : Bentz4.ValidTilt9, valid9 : Bentz4.Valid9 and bentz4 : ∀ k ≥ 8, minSide (k ^ 2 - 4) = k (generated Sqpack/V9/Main.lean, SHA-256 39f42605…), axioms propext, Classical.choice and Quot.sound; checker: Lean v4.33.1's kernel, on Daniel's library at evand 060c1a1..44a105e with RowMinN.lean and a changed LemmaEKM.lean.
- Run: fetch v9-certs.tar.zst (109 MB), regenerate the 1,275,911 Lean files with driver/run9.py and compare with SOURCES.sha256, build every module in import order, Main.lean and Axioms9.lean.
- Cost: about 7,390 CPU-hours of kernel checks (leaf modules 2,694, row groups 4,665, roots 31) plus 177 CPU-hours of certificate generation (skippable with v9-certs.tar.zst), peaks of 22 to 32 GB per module and 230 GB for Main.lean over 1.27 million oleans (about 340 GB of disk), by the source's receipts as the 16 October triage read them.
- Budget status: held: about 185 times the owner's 40 CPU-hour item cap, and far beyond this host (15 GB of memory).
- Possible subset under the cap: rebuild a handful of light roots from v9-certs.tar.zst with driver/run9.py and compare the generated sources with SOURCES.sha256 (about 27 CPU-minutes a root on average, after a 5 GB Lean and Mathlib setup); a component check that moves no rung.
- Depends on: the owner raising the cap for this item or approving a subset; a 256 GB, 400 GB-disk host for Main.lean.
- Done when: a complete build's receipts and axiom output are retained and cited by the formalization entry (T-250) as replayed-here evidence, or the owner declines the replay and that is recorded on #643.
- Machine note: cannot share a host with anything at its peaks; a subset runs on 32 GB.
