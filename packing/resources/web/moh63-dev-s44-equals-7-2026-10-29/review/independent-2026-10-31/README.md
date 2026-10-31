# Independent Review Programs, 31 October 2026

These are the programs and run logs of the independent correctness pass on Mohsen Khalili
and Sara Gharabaghi’s $s(44) = 7$ (T-252, issue
[842](https://github.com/jlevy/squares/issues/842)).
The pass is part of Review A on pull request
[851](https://github.com/jlevy/squares/pull/851#pullrequestreview-5721837491), posted on
31 October 2026 at 07:38:43Z against head `e88b6e0`. Its record is
[`review-2026-10-31-s44-independent-correctness-pass.md`](../../../../../../docs/project/reviews/review-2026-10-31-s44-independent-correctness-pass.md).

The reviewer was Claude (AI review), strong tier (`tbd-strong-max`) at maximum reasoning.
It ran as a separately prompted lane in its own worktree and shared no context with the
import lane that retained this packet and replayed the checker.
It wrote these programs and ran them on a shared four-core host at `nice 5`, with at
most two threads.

The import lane moved them here from the review lane’s scratch directory on the same
day, as option (a) of the review’s finding A2 asks. The programs and every output are
byte for byte as the review lane left them. `outputs/program-digests.sha256` gives each
program’s SHA-256, and the files here match it.

**They decide nothing.** No evidence entry cites them, and none is registered in
[`verifiers.yaml`](../../../../../frontier/verifiers.yaml).
The `--d4` run is a second run of the producer’s checker, `zmx2.rs` `e2bb84e9`, which
the reviewer built by hand from the retained bytes. It repeats the replay; it adds no
method. The exact preflight and the control generator are the reviewer’s own, written
from the format statement, and import nothing from the source, from Daniel’s checkers or
from this repository.

## What Each File Is

| File | What it is |
| --- | --- |
| `programs/exact_check.py COVER` | The reviewer’s exact preflight, in integers and `fractions.Fraction`, with its own parser. It checks well-formedness, the total and its slack below 44, and $D_4$ invariance of the point measure and of the line measure, each line’s density taken as a canonical step function, under all eight symmetries |
| `programs/make_controls.py COVER OUTDIR` | It writes the review’s three mutated covers. `scale99` changes $W$ from $10^8$ to 101,010,102. `drop1pt` drops the first point row alone, without its orbit. `drop1seg` drops the first segment row alone |
| `programs/fn_compare.py OLD.rs NEW.rs` | It compares two `zmx2.rs` versions function by function: identical, changed, removed or added |
| `outputs/d4_receipt.log` | The console of `zmx2 cert s44_cover_7.txt --d4 --threads 2 --log d4_roots.log`, wrapped in the reviewer’s start and end lines: VERIFIED-D4, 4,900 roots, 16,792,446 boxes, 0 uncertified, exit 0, 119.1 s wall, 236 CPU-s |
| `outputs/d4_roots.log.gz` | That run’s root log, stored as deterministic gzip ([Compressed Files](../../README.md#compressed-files)) |
| `outputs/controls/log_s44_cover_7_scale99_x18y24b1.log`, `…_x12y14b3.log` | `scale99` under `zmx2 cert --d4` on two root cells. The first is the D4 image of the source’s float minimum, and the second is the hardest root. NOT VERIFIED, with 212 and 209 uncertified boxes |
| `outputs/controls/log_s44_cover_7_x18y24b1.log`, `…_x12y14b3.log` | The published cover on the same two cells: clean, 37,817 and 378,875 boxes |
| `outputs/program-digests.sha256` | Each program’s SHA-256 as it ran |

`drop1pt` and `drop1seg` stop at `zmx2`’s $D_4$ precondition before any root runs, so they
left no root log. Their messages, quoted in the review record, are
`ERROR: --d4: cover is not D4-invariant: point (2900,600) weight 10026 has no D4 image
at (600,2900)` and `vertical line x=1000 density not matched by x=6000`, both exit 2.

## What Is Left Out

Some of the review lane’s scratch files are not kept. Each can be regenerated from what
the packet retains:

- The decompressed cover. The packet keeps it as
  `s44-equals-7/certificate/s44_cover_7.txt.gz`.
- The three mutated covers, which `make_controls.py` regenerates from the cover. Their
  SHA-256 values:
  - `scale99`: `f5409e87cfae83f26264538d38330f88b0e9c26cd1c2feb8cfe30a999f49ec80`
  - `drop1pt`: `7da2a21087de972c5cdb6a7037e340f2f3b46eb8ac385decf144d6ac04ae5613`
  - `drop1seg`: `46aa26b48151c7321e9564a0027ee858c768cebbe1c825a608e3138cb8d7dce4`
- The reviewer’s comparison extracts. These are every `ROOT` line, without `ms`, from its
  own run, from this packet’s receipts and from the source’s logs, in both modes.
  `devtools.audit_evand_mixed_covers compare-zmx2` makes the same comparison from the
  retained logs.

## The Import Lane’s Reruns

`outputs/import-lane-reruns/` holds what the import lane printed when it ran these
programs again on 31 October before retaining them. It also holds the repository’s own
comparison of the reviewer’s root log. None of it is the reviewer’s output:

| File | Command, from `packing/` |
| --- | --- |
| `exact-check-n44.txt` | `exact_check.py` on the decompressed cover: PASS, total 2199755099/50000000, slack 0.00489802, both measures $D_4$-invariant, as the review’s §4 reports |
| `make-controls.txt` | `make_controls.py` on the cover. The three digests are the ones listed above |
| `fn-compare-6b7f0f79-e2bb84e9.txt`, `fn-compare-92a4cfe8-e2bb84e9.txt` | `fn_compare.py` on the retained `zmx2.rs` copies of 28 September, 30 September and 4 October |
| `compare-d4-with-replay.json`, `compare-d4-with-source.json` | `audit_evand_mixed_covers compare-zmx2 --case 44 --mode d4`, the reviewer’s root log against `receipts/n44_zmx2_d4_roots.log` and against the source’s `verification/logs/zmx2_d4.log`: headers identical, 4,900 of 4,900 roots identical |

## How They Were Run

The reviewer’s own account, from the review:

- It assembled `verify2/` by hand from the retained `zmx2.rs` `e2bb84e9`, `Cargo.toml`
  and `Cargo.lock`, without going through `devtools.replay_evand_zmx2`.
- It ran `cargo build --release --bin zmx2 -j 2` with rustc 1.97.0 (`2d8144b78
  2026-07-07`), which took 17.5 s.
- The binary’s SHA-256 is
  `d68a2e3540344a0e5ad8af33847e3c473b099cf922b150afd184cc715e038787`. That equals
  [`receipts/n44_zmx2_build.log`](../../receipts/n44_zmx2_build.log)’s, though the build
  ran in another directory.
- It ran `zmx2 cert s44_cover_7.txt --d4 --threads 2 --log d4_roots.log` and each control
  under `cert --d4`, the single-root runs restricted to the regions their headers name.
- It ran the Python programs under `python -I`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
