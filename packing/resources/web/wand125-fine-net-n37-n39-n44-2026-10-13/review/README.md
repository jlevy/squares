# The Mathematical Review’s Programs, 14 October 2026

These are the programs the
[mathematical review](../../../../../docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md)
of wand125’s `mixed_n37_L64975`, `mixed_n39_L66625` and `mixed_n44_L69975` wrote and ran
on 14 October 2026, kept as they ran, with the output each printed in
[`outputs/`](outputs/). The review was the stage-4 mathematical review of the import
think-u0av, by an AI agent, Fable, strong tier, max reasoning, prompted separately from
the intake lane and working in a worktree of its own. Each program ran with the project
interpreter (Python 3.14.7, `python3 -I`), reading the three release assets of
`square-lower-bounds-v1`, unpacked in scratch space and digested against the packet’s
pins, as data. No program imports or executes anything of the source. The one program
run here that the review did not write is this repository’s reviewed `sqverify-fast`,
built from the crate source `d97758bb…` (binary SHA-256 `567a0fd5…`), which
`sample_directions.py` drives.

## What Its Authors Read

Before writing these programs the lane read the claim and lemmas N0 to N4, C1, D, A1,
A2, B1 to B5, Z1, Z2, I1, I2, F2 and F3 of `packing/sqverify_fast/SOUNDNESS.md`; the
crate’s `axis.rs`, `interval.rs`, `exact.rs` (`enclose`), `certificate.rs` (admission’s
net reading, `domain_upper`, `d4_images`, the expansion and `float_rect`) and `lib.rs`
(`run_direction_inner`); in `devtools`, the census control (`refusal_record`,
`domain_bounds`, `scaled_sweep`, `sweep_held`, `control`), the exact evaluator
`check_sqverify_fast.mixed_exact` and the premise readers of
`audit_wand125_declared_net` and `fine_net_followup`; and, as data, the source’s
candidate format, its digest rule and its receipts. The producer’s checker is the
source’s copy of this repository’s crate, so none of these programs is clean-room with
respect to it; none imports or copies any of it. `sweep_emulation.py` is, on purpose, a
transcription of the crate’s axis vertex sweep and of its directed rounding into Python
floats, written to reproduce the sweep’s certified bound and expose the enclosure it
does not report.

The source’s commits name Claude as co-author, and these programs were written by a
Claude agent, prompted separately from the source and from the intake lane.

## The Programs

| Program | What it does | Reads | Output |
| --- | --- | --- | --- |
| [`fine_net_exact.py`](programs/fine_net_exact.py) | The module the others import: a candidate read exactly with duplicate keys refused, the eight images and the merged expansion, the direction, lemma D’s per-bin domain, the rotated core, Sutherland–Hodgman clipping, the exact capture, lemma N0’s premises with the last-bin premise, and the source’s semantic digest | (a module) | — |
| [`check_candidate.py`](programs/check_candidate.py) | Every exact premise of one candidate: its SHA-256 against the pin, the claim’s count and side, the declared net’s keys, lemma N0’s (a) to (e) and (f), the rows, their containment and the exact mass sum against `total_mass` and $n - 1/100000$, the semantic digest, the densest row and image against lemma F3’s caps, and the per-bin domain’s least width over every node | the asset’s `candidate.json` | `check_candidate-n37.json`, `-n39.json`, `-n44.json` |
| [`check_source_logs.py`](programs/check_source_logs.py) | The source’s run log (every direction once, each verified at threshold one, the node total against the summary, the summary’s premises against the candidate), its axis row (the exact capture at the sweep’s least vertex against the certified bound), the twelve tightest oblique directions (the exact capture at each least-bound leaf centre), the check2 receipt, the pre-publication receipt and `bundle.json` against the candidate, and the control log (all 32 refusals of the 197/200 mutant evaluated again here at the crate’s witnesses) | the asset’s `check2/run.jsonl.gz`, `check2/control-197_200.jsonl.gz`, `check2/receipt.json`, `verification/prepublication-receipt.json`; the retained `bundle.json` | `check_source_logs-n37.json`, `-n39.json`, `-n44.json` |
| [`sweep_emulation.py`](programs/sweep_emulation.py) | The crate’s axis vertex sweep at one column, in binary64 with the crate’s directed steps, for the original or a mass-scaled mutant: the enclosure at the reported least vertex, its width, the least lower end over the column, the exact capture at the vertex and where it sits in the enclosure | the asset’s `candidate.json`; the sweep’s `argmin` and bound from the run log or the intake lane’s control sample | `sweep_emulation-n{37,39,44}-original.json`, `-scaled-99-100.json` |
| [`sample_directions.py`](programs/sample_directions.py) | Runs the reviewed `sqverify-fast` at chosen directions with `--confirm`, one thread, one at a time, on the candidate or on a copy with every mass scaled; compares each row with the source’s log; evaluates the exact capture at each verified direction’s least-bound leaf centre, and each refusal’s witness on the scaled measure, here | the asset’s `candidate.json` and `check2/run.jsonl.gz`; the binary | `sample-n{37,39,44}.json`, `-scaled-99-100.json`, and an empty `.err` each |
| [`nested_crate.py`](programs/nested_crate.py) | Unpacks the nested verifier archive into a fresh directory, lists its members, recomputes the `source_sha256` a build of it embeds by `build.rs`’s rule, and reports, file by file, what is byte-identical to and what differs from two reference crates, by line counts only; prints no line of the archive and deletes the unpacked copy | the n = 39 asset’s `check2/src/sqverify-proof-net-fe12e036c.tar.gz`; `git archive` copies of `packing/sqverify_fast` at `e020eb1e2` and at this tree’s head | `nested_crate.json` |

## How to Run Them

From this directory, with `$ASSET` the directory an asset unpacks to (holding
`candidate.json`, `check2/` and `verification/`), `$PY` the project interpreter and
`$BINARY` the reviewed binary:

```sh
$PY -I programs/check_candidate.py $ASSET/candidate.json <candidate sha256 from bundle.json>
$PY -I programs/check_source_logs.py $ASSET/candidate.json $ASSET/check2/run.jsonl.gz \
    $ASSET/check2/control-197_200.jsonl.gz $ASSET/check2/receipt.json \
    $ASSET/verification/prepublication-receipt.json \
    ../square-packing/problems/square-lower-bounds/certificates/<directory>/bundle.json 12
$PY -I programs/sweep_emulation.py $ASSET/candidate.json 1 <argmin x> <argmin y> <bound>
$PY -I programs/sweep_emulation.py $ASSET/candidate.json 99/100 <argmin x> <argmin y> <bound>
$PY -I programs/sample_directions.py $BINARY 567a0fd5…ed4 $ASSET/candidate.json 39 533/80 \
    --log $ASSET/check2/run.jsonl.gz --expect-source d97758bb…c88 1 7 1036 1500 1804 2071
$PY -I programs/sample_directions.py $BINARY 567a0fd5…ed4 $ASSET/candidate.json 39 533/80 \
    --factor 99/100 --expect-source d97758bb…c88 1 1036
$PY -I programs/nested_crate.py <archive.tar.gz> e495f9bf…e81 ab6e33e1…d7c \
    e020eb1e2=<crate at e020eb1e2> d97758bb-main=<crate at head>
```

The arguments each run took are in its output: the digests, the directions, the
factor, the vertex and the bound. The sweep emulation’s vertices and bounds are the run
logs’ axis rows (the originals) and the intake lane’s
[`receipts/control-sample-n*.json`](../receipts/) (the 99/100 mutants).

## What They Printed

- **`check_candidate`.** For all three: every key as the format wants it, `points`
  empty, no `scaling_factor`, every row positive, inside the container and
  nondegenerate, the mass equal to `total_mass` and to $n - 1/100000$, the digest equal
  to the one stated throughout, lemma N0’s (a) to (f) holding with
  $B(1 + D) = 25009997/25010000$, $t_{\max}^2 + 2t_{\max} - 1 = 367/6255001$ and the
  tangent form $500400014977/500400075000$, the per-bin domain nonempty at every node
  (least width 5.08, 5.25 and 5.58 at node 2072), and the densest image at 25,439,
  15,368 and 19,392 (eight times it below $2^{32}$).
- **`check_source_logs`.** For all three: 2,073 rows at indices 0 to 2072 once, every
  one `verified` at threshold `1`, the oblique nodes summing to the summary’s, the
  summary’s premises those of the candidate (its `input_sha256` the published
  candidate’s), the receipt’s embedded summary equal to the log’s, the pre-publication
  run on the same build and the published bytes, `bundle.json` stating this digest and
  net; the certified axis bound a true lower bound on the exact capture at its vertex,
  6.9e-11, 1.28e-9 and 1.30e-10 below it; the twelve tightest leaf centres all in their
  domains with exact captures of at least 1.0022, 1.0026 and 1.0036; and all 32 control
  refusals genuine (each witness in its domain with a scaled capture below one, the 31
  oblique ones equal to the crate’s `exact_coverage` digit for digit).
- **`sweep_emulation`.** In all six runs the emulated lower end equals the crate’s
  certified bound to the last digit, and the exact capture lies inside the enclosure,
  at its midpoint: widths of 1.38e-10 (n = 37, vertex 766 of 3,970), 2.55e-9 (n = 39,
  vertex 4,497 of 4,498) and 2.60e-10 (n = 44, vertex 1,565 of 3,935) for the originals,
  and 1.37e-10, 2.53e-9 and 2.57e-10 for the mutants.
- **`sample_directions`.** Eighteen directions, six per certificate, all `verified` with
  the source log’s node counts and bounds exactly, built from `d97758bb…`; the exact
  capture at every least-bound leaf centre at least the certified bound and at least
  one (least 1.0020 at n = 44, direction 1036); 38.6, 40.1 and 91.8 CPU seconds. Six
  99/100 mutant runs, all `counterexample-candidate` with a witness in the domain whose
  scaled capture is below one and equals the crate’s (least 0.99256, greatest
  0.99999999985); about four CPU seconds in all.
- **`nested_crate`.** Twenty members; `source_sha256` `ab6e33e1…`, the digest every
  receipt names; against `e020eb1e2`, sixteen files byte-identical (every `src/` file but
  `certificate.rs`, the lockfile, `build.rs`, the toolchain and independence files), and
  `certificate.rs` +32 −2, `tests/adversarial.rs` +55, `README.md` +5 −2, `SOUNDNESS.md`
  +11 lines; against this tree’s head, `certificate.rs` +38 −98, `lib.rs` −3,
  `rotated_tests.rs` −1, no `tests/declared_net.rs`.

## What Decides What

`fine_net_exact.capture` decides the capture at the poses it evaluated: the 96 control
witnesses, the 36 tightest leaf centres, and the 24 leaf centres and witnesses of the
runs here. `sample_directions.py` decides, with the reviewed binary, the 18 directions it
ran and the refusal of the mutant at 6 others. Everything else checks premises, and
`sweep_emulation.py` decides nothing: it is a diagnostic of the census control’s axis
tolerance. No program here is a replay, and none is cited by an evidence entry yet; the
review proposes the registry entries.

The computation totalled about three CPU-minutes, the samples apart under 20 CPU
seconds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
