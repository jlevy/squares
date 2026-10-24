---
type: is
id: is-01m58w3jngtrtqbg6qxpy896y1
title: Review Fang's public Lean formalization at 947bdae before T-163 rung change
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-fang-note-1024
labels: []
dependencies: []
parent_id: is-01m4wv278cdppm9155311gb6y5
hold: null
hold_until: null
created_at: 2026-10-19T01:23:37.262Z
updated_at: 2026-10-24T05:54:34.746Z
started_at: 2026-10-19T01:23:53.493Z
---
#603 comment 6255103888 reports TheSnakeFang/squarepack-lean at 947bdae, a Lean 4 route to Theorem 1, the side n-1/10000 version, and the single-step Theorem 2 form, atop Evan Daniel's unchanged Spec.lean; source claims standard three axioms, no sorry/native_decide. Squarepack-certs 0e9be796 also adds note draft v0.8. Intake read only: no independent build, statement audit, source closure, or checker replay yet. Retain exact source pin and note; compare theorem statements and hypotheses against T-163, review proof and axiom closure, run reproducible build when priced, and decide whether any rung change is warranted. Keep current T-163 V2/C1 until these checks. Coordinate distinct Daniel Lean route think-57ei; Section 5 composites remain separate think-rn2y.

## Notes

## Stages 1 to 3, 2026-10-24 (lane c-fang-note-1024, branch claude/intake-2026-10-24-fang-note, PR #781, draft)

Packets: packing/resources/web/fang-excess-note-2026-10-19/ (Zenodo record 23463481 v0.9, PDF MD5 beadf4508e65444d956a475e31f0e99e SHA-256 a44402f8…d95d5, tex zip MD5 653bd4d3…, main.tex SHA-256 532b233f…; squarepack-certs 9ffba0f3a84b38f0c92790c1d3089f979ef53f0b, tree 33f93a88, note/fang-2026-n2-n-1.md SHA-256 a510541c…) and packing/resources/web/fang-excess-lean-2026-10-18/ (squarepack-lean 947bdaec40ead1105cfb00c2968e2484b7d1b40b, tree d4c36ad8, 141 files: 130 retained, 11 pinned; receipts/lean-closure.json.gz). Keys [Fang excess note 2026-10-19], [Fang excess Lean 2026-10-18].

Statement audit: note Theorems 1 and 2 = T-163's claim (hypotheses and conclusions); construction side n - 1/20000 = claim. Fang Lean theorem1 = Theorem 1 over Daniel's Spec.lean (same blob fa4a6248); main stronger (side n - 1/10000); theorem2 with jExc = F(n) for 15 <= n <= 51, one short at 52..56, never more. Daniel's T-236 theorem1/theorem2 = Theorems 1 and 2 in full. Closure (devtools.lean_closure): 109 modules, Mathlib only outside import, zero escape tokens, Sqlean.Pieces.N211 missing (gitignored). No build (host 4.7 GB free; needs ~9 GB).

Rung: T-163 V2 -> V3 on E-fang-excess-note-proof (verified published-proof with proof block; epistemics.md Verification table, V3 structural support). C stays C1: C3 needs a confirming machine replay (a Lean build here), not a review; unfinished_confirmations C3 think-dgrc, C4 think-pxxi (new, under think-ezt8: the note's stage 4 review, with the build and oversight). E-fang-excess-lean-report reported on T-163.

### Draft #603 status reply (not posted; stage 7, on the owner's word, after #781 merges)

Thank you, @TheSnakeFang, for publishing the note and the Lean pin. Where T-163 stands in the record on `main` now that the retention has merged:

- **T-163 is now V3/C1.** The note, draft v0.9 ([10.5281/zenodo.23463481](https://doi.org/10.5281/zenodo.23463481)), is retained from the Zenodo record (the PDF, the LaTeX source and their checksums) with the same text in Markdown from squarepack-certs at `9ffba0f`. It is recorded as a published proof (`E-fang-excess-note-proof`), which is what V3 asks for; V2, a proof asserted but not publicly recoverable, stopped applying once the note was public. C1 still rests on the review of 14 October, which re-derived both theorems from the bundle before the note was out. The four finite bounds at 211, 241, 273 and 307 stay re-verified here on both of our exact routes, independently re-implemented after reading Daniel's checker of the certificate format.
- **The statements match.** The note's Theorems 1 and 2, hypotheses and conclusions, are the ones T-163 states, and so is the construction's side n − 1/20000.
- **Your Lean proof is retained, not yet built.** squarepack-lean at `947bdae` is in its own packet. `theorem1` is Theorem 1 over Evan Daniel's `Spec.lean` (the same bytes as his), and `main` is stronger, at side n − 1/10000. `theorem2` uses `jExc n`, the larger of the two single-step bounds: that equals F(n) for 15 ≤ n ≤ 51 and is one short at n = 52 to 56, where one step of each kind gains, as the note says. We read the axiom claim and the absence of `sorry` and `native_decide` from the source text only. No build ran here; the toolchain and the Mathlib cache need about 9 GB of disk this host does not have.
- **Two small points, neither about the mathematics.** The squarepack-lean README's first line still says "Kernel-checked Lean 4 proof of Theorems 1 and 2", and `Theorem2.lean` calls `jExc` "The excess of Theorem 2", where the note and the squarepack-certs README say Theorem 1 and the unmixed bounds. And Section 6's "the mixed-step bound is proved here [FanL26]" can be read as citing the Lean repository for the mixed-step bound.
- **Still to come.** A Lean build here with its axiom receipt of Evan Daniel's proof of both theorems (T-236, about 2 to 3 CPU-hours) would take T-163 to C3; a build of yours (about a quarter of a CPU-hour) would reach C3 for Theorem 1 and the single-step bounds. A stage 4 review of the note's own proofs against the 14 October reconstruction, with that build and a human oversight record, is what C4 needs. Nothing is needed from you for either.

Evidence: `E-fang-excess-note-proof` (published proof), `E-fang-excess-lean-report` (reported). On `main`: [RESULTS.md](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), [the note packet](https://github.com/jlevy/squares/blob/main/packing/resources/web/fang-excess-note-2026-10-19/README.md), [the Lean packet](https://github.com/jlevy/squares/blob/main/packing/resources/web/fang-excess-lean-2026-10-18/README.md).

---
_Generated by [Claude Code](https://claude.ai/code)_
