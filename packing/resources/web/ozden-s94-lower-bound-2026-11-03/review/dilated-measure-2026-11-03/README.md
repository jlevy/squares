# Stage 4 Review of the Dilated n = 94 Measure: Programs and Receipts

These are the programs and receipts of the stage 4 mathematical review of Doğa Özden’s
$s(94) \ge 1993/200$ certificate, issue
[#890](https://github.com/jlevy/squares/issues/890)
([the review](../../../../../../docs/project/reviews/review-2026-11-03-ozden-s94-dilated-measure.md)).
They were written on 3 November 2026 by a separately prompted review lane, an AI
reviewer of the Claude family (Anthropic) at the strong sub-agent tier
(`tbd-strong-max`) and maximum reasoning, in a worktree of its own at the pull request’s
head `e78e5963a`.

The programs import nothing from this repository, from the census tools or from the
packet’s `source/`. They use the standard library and, from the project environment,
`numpy`, `scipy` and `gmpy2`. Their author read the following before writing them:

- `packing/sqverify_fast/SOUNDNESS.md`;
- the crate’s format reader, admission, `declared_net`, `domain_upper` and `direction`
  in `src/certificate.rs`, and the lines of `src/rotated.rs`, `src/axis.rs` and
  `src/lib.rs` that set each direction’s search box. That crate is the checker the
  author decided the certificate with, so this is the producer’s code;
- Hosono’s description of format M, in the
  [wand125-continuous-n28 packet](../../../wand125-continuous-n28-2026-10-15/square-packing/problems/square-lower-bounds/certificates/continuous_n28_L5745/check2/src/SPEC.md);
- the packet’s READMEs and the receipts, as data.

The author’s second checker was read only after the first seven programs were written.
`devtools/audit_dilated_measure.py` was not read at all.
`second-checker/GRADE.md` and `GRADE.json`, the earlier referee report, were read only
after the review’s findings were committed (`5ad487b72`). `dm_compare.py` was written
after that, and reads `GRADE.json` as data.

Every program ran with CPython 3.14.7 (`packing/.venv/bin/python3 -I`) under `nice`, at
most two processes at a time, on a shared four-core host.
Each receipt records the SHA-256 of the program that wrote it and of `dmlib.py`.

## What Each Program Does

| Program | Role | What it read | Receipt |
| --- | --- | --- | --- |
| `dmlib.py` | shared code, deciding nothing on its own. A strict reader (one gzip member, duplicate keys refused, exact rational tokens), the D4 expansion with merging, the net and the per-bin domain, and the exact capture $F_r(c)$ by two methods: clipping each rectangle by the square’s four half-planes, and integrating the vertical section between its breakpoints. Also a binary64 section method, used for searching only | (library) | none |
| `dm_selftest.py` | checks the evaluators: known areas at oblique net angles; method 1 against method 2 and binary64 at 50 seeded poses; the census control’s exact capture at the least-bound leaf; the author’s $n = 31$ refusal | the certificate; the control receipt; `notes/n31-negative/` | `outputs/selftest.json` |
| `dm_premises.py` | **decides** every premise of the theorem except coverage, in exact rationals: the file, the mass, lemma N0 (a)–(e), the net’s coverage of $[0, \tan(\pi/8)]$, the per-bin domain at all 600 nodes. Also records the facts of the dilation | the certificate; Hosono’s `mixed_n94_L995` candidate | `outputs/premises.json` |
| `dm_axis.py` | **decides** direction $r = 0$ in full: every vertex of the event grid, evaluated as one matrix product with a rigorous a-priori bound on its rounding, then the lowest vertices exactly; compares with the census row at $r = 0$ | the certificate; the census capture | `outputs/axis-r0.json` |
| `dm_sample.py` | **samples** and decides no direction: exact captures at the centre and four corners of every oblique direction’s least-bound leaf; a binary64 search for low captures at 19 directions, with the lowest poses evaluated exactly; the dilation identity at shared directions | the certificate; Hosono’s candidate; the census capture | `outputs/sample.json`, `outputs/leaf-poses.jsonl` |
| `dm_receipts.py` | checks the records against the candidate: the author’s two receipts and the census capture, the census row, the control receipt; recomputes all 600 refusals of the control’s 99/100 mutant, and its near-threshold witness, exactly | the receipts; `census.json`; the control receipt; `outputs/premises.json` | `outputs/receipts.json` |
| `dm_mutants.py` | builds five mutants in memory and refuses each for the reason it names: Hosono’s net, one direction short, the core left undilated, masses times 99/100, masses times the largest $k/10^9$ below $1/F^*$ | the certificate; Hosono’s candidate; `outputs/sample.json` | `outputs/mutants.json` |
| `dm_compare.py` | written after the findings were committed: holds the referee report’s values to `dmlib`’s evaluator (its least capture at $r = 144$, its ×0.998 mutant) and searches its two other coverage mutants for exact witnesses | the certificate; Hosono’s candidate; `source/second-checker/GRADE.json`, as data | `outputs/compare-grade.json` |

## How to Run Them

From any directory, with `PKT` this packet, `REPO` the repository root and `OUT` this
directory’s `outputs/`:

```bash
PY="$REPO/packing/.venv/bin/python3 -I"
P="$PKT/review/dilated-measure-2026-11-03/programs"
CERT="$PKT/source/certificate/n94_L9965.json.gz"
BASE="$REPO/packing/resources/web/wand125-mixed-bounds-evening-2026-10-04/square-packing-bounds/certificates/mixed_n94_L995/candidate.json.gz"
CENSUS="$REPO/packing/benchmarks/measure-verifier/census-mixed"
CAPTURE="$CENSUS/ozden-s94-lower-bound-2026-11-03/mixed_n94_L9965.jsonl.gz"
CONTROL="$CENSUS/ozden-s94-lower-bound-2026-11-03/mixed_n94_L9965.control-failed-v2.json"
$PY $P/dm_selftest.py "$CERT" "$CONTROL" "$PKT/source/notes/n31-negative/n31_L5978.json.gz" \
  "$PKT/source/notes/n31-negative/d529.jsonl" "$OUT/selftest.json"
$PY $P/dm_premises.py "$CERT" "$BASE" "$OUT/premises.json"
OPENBLAS_NUM_THREADS=2 $PY $P/dm_axis.py "$CERT" "$OUT/axis-r0.json" "$CAPTURE"
$PY $P/dm_sample.py "$CERT" "$BASE" "$CAPTURE" "$OUT"
$PY $P/dm_receipts.py "$CERT" "$PKT/source/receipts/sqverify-fast-rustc1.98-full.jsonl" \
  "$PKT/source/receipts/sqverify-fast-rustc1.93-full.jsonl" "$CAPTURE" "$CENSUS/census.json" \
  "$CONTROL" "$OUT/premises.json" "$OUT/receipts.json"
$PY $P/dm_mutants.py "$CERT" "$BASE" "$OUT/sample.json" "$OUT/mutants.json"
$PY $P/dm_compare.py "$CERT" "$BASE" "$PKT/source/second-checker/GRADE.json" "$OUT/compare-grade.json"
```

## What They Printed

| Program | Status | Main values | CPU |
| --- | --- | --- | --- |
| `dm_selftest.py` | `PASSED` | 12 synthetic areas exact; methods 1 and 2 equal at 50 poses, binary64 within $4.4 \times 10^{-13}$; equal to the crate’s exact capture at the $r = 277$ leaf; the $n = 31$ receipt is the retained file’s capture times $10000003/10000000$, and the retained file captures $0.99999969508$ there | 1.2 s |
| `dm_premises.py` | `PREMISES_HOLD` | $B(1 + D) = 2387749705363/2388000000000$; $t_{\max}^2 + 2t_{\max} - 1 = 3860089/14400000000$; tangent form $1146119721592254871/1146239862908900000$; $M = 94 - 1/100000$; 6,720 images; $\tan(\pi/8)$ in bin 599 only; least $\rho(a_r)$ minus the core’s half-extent $5.30 \times 10^{-5}$ (node 1); domain growth $3/3986$ at $r = 0$, $6.55 \times 10^{-5}$ to $1.062 \times 10^{-3}$ at the other shared nodes | 1.2 s |
| `dm_axis.py` | decided at least 1 | 5,430 × 5,430 events, the crate’s counts; least $1.003117185664143$ at $(32310351317604646637/4975000000000000000, 1893/200)$, the crate’s argmin; rounding bound $3.19 \times 10^{-9}$; least on Hosono’s domain $1.0031817020943$ | 6.5 s |
| `dm_sample.py` | `CONSISTENT` | 2,995 leaf poses at or above their certified bounds (least margin $0.00231$, $r = 537$); least capture found $1.0017633082$ ($r = 277$); at the walls at least $1.0031$; the dilation identity exact at 8 poses | 100.2 s |
| `dm_receipts.py` | `RECORDS_HOLD` | the three runs identical at all 600 directions; census row items 2–5 hold; control `CONTROL_FAILED` on the axis rule only (gap $1.123 \times 10^{-9}$); all 600 witnesses hold exactly | 11.0 s |
| `dm_mutants.py` | `EVERY_MUTANT_REFUSED` | Hosono’s net by N0 (b); `last` 598 by (c); the undilated core by a capture of $0.67849$ at $r = 0$; masses × 99/100 and × $199647959/200000000$ by exact captures below 1 at $r = 277$ | 13.2 s |
| `dm_compare.py` | `REFEREE_VALUES_HOLD` | the referee’s least capture, $1.001123004123937$ at $r = 144$, inside its stated interval; its ×0.998 mutant equal to its floor; its heaviest-orbit mutant refused here by $0.24998$ ($r = 0$) and its $L = 9.975$ mutant by $0.99766$ ($r = 144$) | 4.5 s |

## Registration

This review was asked to commit only the review, these programs and the document map’s
row. Registering the deciding programs in `packing/frontier/verifiers.yaml`, and an
evidence entry for each thing a run decides or samples, are the records lane’s. The
record each needs is:

- **Decides:** `dm_premises.py` decides the premises, and `dm_axis.py` decides direction
  0, full coverage of that one direction. `dm_sample.py` and `dm_receipts.py` sample:
  599 directions at five poses each, 19 searched directions, and 600 control witnesses.
  `dm_mutants.py` and `dm_selftest.py` are controls. `dm_compare.py` compares with the
  referee report and decides nothing; its record’s `read` also includes
  `earlier-review`.
- **Independence:**
  - `read`: mathematics, specification, certificate-format, producer-code (the crate’s
    admission, declared net, per-bin domain and search box, which the producer ran) and
    producer-output (the receipts, read to compare);
  - `clean_room`: false;
  - `shares`: none;
  - `written_by`: Claude (Anthropic), stage 4 reviewer, `tbd-strong-max`, maximum
    reasoning;
  - `overlaps_producer`: `system-family` (the author’s lab and the crate’s authors used
    Claude agents), with `separate_prompt` and `separate_code` both true.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
