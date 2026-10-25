---
type: is
id: is-01m5rtjypv9b36ww3nn7rc9ejt
title: "Validate Daniel's s(29) degree-7213 minimal polynomial (T-246, #816, #817): replay, independent checks, packing at the exact side"
kind: task
status: in_progress
priority: 3
version: 4
delegate: w-s29-validate-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-25T06:04:54.875Z
updated_at: 2026-10-25T17:25:55.915Z
started_at: 2026-10-25T15:41:58.506Z
---
The validation of Evan Daniel's degree-7213 minimal polynomial of the s(29) record side, T-246, from the release exact-data-2026-10-12 of evand/square-packing (tag commit 31523f87316bdfda00f5459dd9077928e264f133), tracked by the owner's issue #816 and delivered on draft PR #817 (branch claude/friendly-einstein-gf9z0h-s29-validation), owner w-s29-validate-1025.

**Inputs.** s29-minpoly.tar.zst, 87,237,962 bytes, SHA-256 708e1b8b45894667f90a0d18b55bb35ed6079b84d33f9656976fd5cfa6f3729c, pinned in packing/resources/web/evand-exact-data-2026-10-12/acquisition/release.json; fetched 25 October into scratch, every member held to the pinned digest. The source's scripts at ad86d42 in packing/resources/web/evand-exact-and-local-reports-2026-10-12/.

**Budget.** The owner's per-item cap of 25 October: 10 CPU-hours, revised to 3, then 5.

**Steps and status (25 October).**
1. Same-implementation replay (C3): devtools.evand_s29_replay runs the five scripts under python-flint 0.9.0 and mpmath 1.3.0, with four controls (perturbed p for link, verify_mod and contacts_mod; p(x+1) for irred). Running: verify_mod cut to 10 fresh random primes (about 250 CPU-s a prime here; the README's 50 would be about 3.5 CPU-hours); all four controls refuse as required.
2. Independent irreducibility and root isolation: DONE. devtools.check_exact_side_minpoly: distinct-degree factorization modulo 5 primes near 40000 empties the degree certificate (1,300 CPU-s); exactly one root of p in S_mid +- 2e-48, in exact integer arithmetic (290 CPU-s).
3. Deterministic identities: PRICED, not run. Exact route about 717 CPU-hours (numerators up to 11.8 GB); modular route about 1.1e8 primes. Both far over the cap; the identities stay Monte Carlo.
4. Non-overlap at the exact side: DONE, deterministic. devtools.check_exact_side_packing: the configuration at the unique zero t* of F in the Krawczyk box is a packing; the whole contact system is consistent at t* by exact elimination over Q(t). So s(29) <= S* with no Monte Carlo step.
5. Against T-195: BEING RE-DECIDED against T-195's exact rational (an earlier comparison used T-155's printed interval endpoint by mistake).
6. Review document: OPEN.
