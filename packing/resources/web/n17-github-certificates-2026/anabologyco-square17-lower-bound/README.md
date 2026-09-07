# Compressed exact certificate candidate for packing 17 unit squares: side at least 4.5705

This repository contains an internally exact, finite computer-assisted proof candidate for

$$\boxed{\,s(17)\ \ge\ 4.5705 = \tfrac{9141}{2000}\,}$$

i.e. no 17 pairwise interior-disjoint unit squares fit in a square of side less than 4.5705.
The best known packing of 17 unit squares (Bidwell) has side ≈ 4.6756; the trivial area
lower bound is $\sqrt{17}\approx 4.1231$. It does not claim a strict inequality, Bidwell
optimality, or a new packing.

The certificate is a nonnegative atomic measure with 71 dihedral support orbits,
560 expanded atoms, coordinates in `(1/4000) Z^2`, weights in `(1/10^12) Z`, and exact mass
`16.994734834452 < 17`. The finite audit proves that every closed unit square contained in
`C=[0,4.5705]^2`, at every orientation, captures mass at least 1; seventeen interior-disjoint
unit squares would therefore need total mass at least 17.

The verification pipeline independently regenerates 1,344,862 geometric event polynomials
(byte-identical to the bundled originals), exactly discards 1,194,331 root-free events using
integer Bernstein coefficients, verifies an exact 148,936-root orientation partition via
Sturm chains and gcd common-root checks, checks both endpoint orientations, and audits all
148,937 open orientation cells (278,950,150 maximal subthreshold runs, every feasible
intersection excluded) using arbitrary-precision integer geometry. Every proof decision is
an exact integer or rational comparison; floating point appears only in timing/reporting and
in the exploratory tooling that *found* the certificate (which is not part of the
verification chain).

## Verifying

Requirements: `g++` (C++20, OpenMP), Boost headers (`libboost-dev`), `python3` with `numpy`.

```bash
./verify_core.sh
```

This checks exact mass, exact Bernstein filtering, the exact Sturm/gcd event partition, and
both endpoint orientations; every stage prints an explicit `... PASS` line.

The full open-cell coverage audit is process-isolated because the inherited OpenMP wrapper
can stall nondeterministically in a long-lived process:

```bash
./scripts/run_coverage_ranges.sh
```

Every range invokes the same arbitrary-precision integer checker in a fresh process and must
emit `EXACT SEGMENT COVERAGE PASS`. The bundled original run is summarized in
`data/coverage_summary_final.json`.

**Reproduction notes.** The scripts compile with `-std=c++17` deliberately: with older
Boost (≤ 1.74), building the Sturm/endpoint verifiers as C++20 routes
`boost::multiprecision` rational arithmetic through a pathological slow path (observed
100×+: the event partition goes from ~24 s to hours, and the multithreaded run then looks
indistinguishable from a spin-stall). The coverage checker (pure `cpp_int`) is unaffected.
If the event-partition stage appears hung, run it single-threaded
(`build/verify_event_partition 1 ...`) and check your Boost version before suspecting the
data. All stages of this pipeline, including the full 148,937-cell coverage audit
(278,950,150 subthreshold runs), have been re-run end-to-end on a second machine
(4-core EPYC-Milan VM, g++ 11.4, Boost 1.74) with results identical to the bundled logs.

## Lean formalization

`lean/` contains a Lean 4 formalization of the finite computation layer, rebuilt for this
certificate: the geometry constants were re-derived independently from the container
`[0, 9141/2000]^2` on the `1/4000` grid and cross-checked against the C++ verifiers. The
kernel-accepted theorems (`native_decide`) cover certificate arithmetic + D4 symmetry, both
endpoint audits, and the per-orientation coverage audit — a fast 152-sample subset theorem
in the default target and the full 148,937-orientation replay in `FullTheorem.lean`. See
`lean/README.md` for the trust model and what remains unformalized.

## Layout

- `docs/PROOF.md` — the mathematical argument and finite reduction.
- `docs/AUDIT.md` — audited quantities and pipeline results.
- `AUDIT_RESULTS.txt`, `run_summary.json` — machine summaries of the bundled audit.
- `lean/` — Lean 4 formalization of the finite computation layer.
- `src/`, `scripts/`, `verify_core.sh` — the verification chain.
- `data/` — certificate, event polynomials, orientation samples, bundled results.
- `logs/` — reference logs from the release environment.
- `SHA256SUMS` — checksums of data, docs, scripts, sources, and Lean sources.
- `legacy/4p57/` — the complete earlier release proving s(17) ≥ 4.57 (also tagged
  `4p57-final`), including its own Lean formalization, kept frozen for provenance.

## Provenance

- **Certificate and pipeline**: constructed with the same GPT 5.6 Sol Pro (OpenAI)
  optimization pipeline as the 4.57 release in `legacy/4p57`.
- **Audit and reproduction**: Claude Fable 5 (Anthropic) — core verification chain and the
  full 148,937-cell coverage audit re-run on the release-compilation machine.
- **Lean formalization**: Claude Fable 5 — independently re-derived constants,
  cross-checked against the C++ verifiers, theorems kernel-accepted via `native_decide`.
- **External human peer review**: pending.

## Review status

All reported proof decisions are exact integer/rational decisions and the bundled pipeline
passes end-to-end on the release machine. This certificate has not yet been peer reviewed
or reproduced by a fully independent external implementation. Treat the result as a
complete proof candidate pending that review.

## History

- **v0.2.0** — this release: s(17) ≥ 4.5705, 71 orbits / 560 atoms, Lean layer rebuilt.
- **v0.1.1** — s(17) ≥ 4.57 (52 orbits / 408 atoms), now frozen under `legacy/4p57/`.
