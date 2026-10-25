---
type: is
id: is-01m5rtjypv9b36ww3nn7rc9ejt
title: Replay Daniel's s(29) degree-7213 minimal polynomial checks from the pinned release (T-244, C3, about 2.5 CPU-hours)
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-25T06:04:54.875Z
updated_at: 2026-10-25T06:04:54.875Z
---
The C3 confirmation that T-244 lists: the source's five-step replay of Evan Daniel's degree-7213 minimal polynomial of the s(29) record side, from the release exact-data-2026-10-12 of evand/square-packing (tag commit 31523f87316bdfda00f5459dd9077928e264f133).

**Inputs.** s29-minpoly.tar.zst, 87,237,962 bytes, SHA-256 708e1b8b45894667f90a0d18b55bb35ed6079b84d33f9656976fd5cfa6f3729c, pinned by digest in packing/resources/web/evand-exact-data-2026-10-12/acquisition/release.json (fetch it, check the digest and every member's against the record, unpack outside the repository). The scripts are retained at ad86d42 in packing/resources/web/evand-exact-and-local-reports-2026-10-12/source/search/exact/homotopy/ and run under search/exact/env.sh (python-flint 0.9.0, mpmath 1.3.0).

**Steps** (the archive README's five commands): irred.py over 12 primes; krawczyk.py at radius 1e-50; link.py with PREC=220000 (at the default it prints NOT LINKED); verify_mod.py over 50 primes (about 2.5 min a prime); contacts_mod.py over 21 primes (about 20 s a prime). Add a control: a perturbed p (one coefficient changed) must fail irred.py's or link.py's check.

**Price.** About 2.5 CPU-hours by the author's measure (issue 545 comment of 12 October 2026), almost all in verify_mod.py; 3 CPU-hours high. Same-implementation: a reproduction with the producer's code, two of whose steps are Monte Carlo; the packing's non-overlap at the exact side is checked by none of it.

**Waits on** an owner compute budget (think-6gti's triage). Not started.
