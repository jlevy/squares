# Independent Review of the n = 90 Follow-Up

This packet retains an independent exact feasibility review of
[de Winter’s follow-up to #997](https://github.com/jlevy/squares/issues/997#issuecomment-7058975230).
The
[formal review](../../../../../docs/project/reviews/review-2026-11-21-de-winter-997-n90-rational-followup.md)
states the theorem and trust boundary.

The result is accepted: 90 unit squares, 1,440 wall inequalities, 4,005 pairs, 16,020
axis tests, and 13 predeclared controls.
The candidate’s least wall and selected pair margins are exactly zero.
No producer program was read or executed.

## Files and Authority

| File | Role |
| --- | --- |
| `verify_independent.py.txt` | Exact source-only program that produced the frozen result, preserved byte-for-byte |
| `verify_independent-working.py.txt` | Working copy with project style changes, checked by Ruff and BasedPyright and rerun |
| `run_observed.py.txt` | Exact historical one-worker launcher; starts the passive memory guard before mathematical work |
| `compare_replay.py` | Compares every result field except timings and the changed program digest; detects an altered verdict |
| `plan-frozen.json` | Preconditions, algorithm, scope, and 13 controls, frozen before the feasibility run |
| `result-frozen.json` | Authoritative source-only mathematical result |
| `receipt-frozen.json` | Run identity, trust boundary, read order, and retention mapping |
| `working-result.json`, `replay-comparison.json` | Separate working result and equality evidence |
| `execution.json`, `working-execution.json` | Commands, exits, worker limit, and scratch environment |
| `memory-observe.jsonl`, `working-memory-observe.jsonl` | Passive journals; no signals authorized or delivered |
| `archive-custody.json` | Pinned ZIP listing and exact equality of its four factual members |
| `quality-checks.json` | Full project configuration identity and targeted checks |
| `evidence/source/` | Four original factual members, unchanged |
| `evidence/source-manifest.json`, `evidence/author-comment-7058975230.json` | Input identities and the author’s coordinate convention |
| `evidence/candidate-pairs.csv.gz`, `evidence/input-pairs.csv.gz` | Every exact pair certificate, compressed for retention |

The first result froze before any project geometry, prior review, derived packet result,
or producer checker was read.
Afterward the reviewer read workflow/configuration documents and the existing #997
addendum. The working result’s `independence_at_freeze` field describes that original
mathematical freeze; the working replay occurred after those documentation reads.

The deciding program reads the four factual members.
The observer decides nothing about mathematics.
The comparison program decides equivalence of the retained results.
The two verifier versions share this reviewer’s implementation and count as one
independent implementation.

The result refers to decoded `.csv` pair-ledger names.
The retained `.csv.gz` files decompress to those exact bytes; `receipt-frozen.json`
records both identities.
The working replay produced the same decoded identities, so one retained copy serves
both runs.

## Archive Members and Replay

The 39,377-byte ZIP has SHA-256
`c04a0a60ca91f15922f6077c878c50b654e759ee659c14d43096cadaae574afa` and these members:

- `check_vertices.py`
- `envelope.py`
- `comparisons.csv`
- `90/input.json.gz`
- `90/candidate.json.gz`
- `90/previous-comparisons.json`
- `REPLAY.md`

The archive was listed without opening its producer programs.
Only the four factual members were extracted or compared.
There is no `n90-rational/` prefix.

For a replay on the review host, set `N90_SOURCE_ARCHIVE` to the retained ZIP, run from
the repository root, and choose a fresh external directory.
The historical launcher pins the interpreter and guard paths recorded in
`execution.json`. A different host must substitute its Python 3.14 interpreter and
observe-only guard in a separate launcher and retain that launcher with its new run.

```bash
set -eu
review=packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review
archive="$N90_SOURCE_ARCHIVE"
work=/Volumes/spud-ext2/agent-scratch/n90-independent-replay
test -d /Volumes/spud-ext2
test -w /Volumes/spud-ext2/agent-scratch
test ! -e "$work"
mkdir -p "$work/evidence/source/90" "$work/tmp" "$work/cargo-target" "$work/uv-cache"
export TMPDIR="$work/tmp"
export CARGO_TARGET_DIR="$work/cargo-target"
export UV_CACHE_DIR="$work/uv-cache"
export PYTEST_ADDOPTS="-o tmp_path_retention_policy=failed -o tmp_path_retention_count=1"

unzip -l "$archive"
for member in comparisons.csv 90/input.json.gz 90/candidate.json.gz 90/previous-comparisons.json
do
    unzip -p "$archive" "$member" > "$work/evidence/source/$member"
done

cp "$review/plan-frozen.json" "$work/plan-frozen.json"
cp "$review/evidence/source-manifest.json" "$work/evidence/source-manifest.json"
cp "$review/verify_independent.py.txt" "$work/verify_independent.py"
cp "$review/run_observed.py.txt" "$work/run_observed.py"

/Users/levy/wrk/github/squares/.worktrees/intake-scratch-20261120/venv/bin/python \
    -I -B "$work/run_observed.py"
```

The launcher records both process exits.
The worker prints the geometric controls, candidate/input outcomes, result identity,
control count, and verdict.
Both retained runs returned zero for worker and observer.
For a working replay, copy `verify_independent-working.py.txt` into another fresh
workspace as `verify_independent.py`. Run
`compare_replay.py FROZEN_JSON WORKING_JSON --out COMPARISON_JSON` with the project
interpreter to compare results.

## Compressed Files

| Stored file | Origin | Git blob of uncompressed bytes | Decompressed SHA-256 |
| --- | --- | --- | --- |
| `evidence/candidate-pairs.csv.gz` | receipt | `b207873108dde6923f5991c9bdd3a5a490578ee5` | `7f48f75294c083c55445dac6448530859a83738d772ae2a03189216f556235fa` |
| `evidence/input-pairs.csv.gz` | receipt | `b3284f0acf50227b1246af5578030bcb17b1a640` | `75f0dc25727f2fd9792c4f91757989cdcfbb376c5293a649ddc5b44c9bcd03b5` |

## Original Gzip Files

| Stored file | Origin | Git blob of stored bytes | SHA-256 of stored bytes |
| --- | --- | --- | --- |
| `evidence/source/90/candidate.json.gz` | upstream | `a348275c6786bf75c1b8d684a90846de2b9163f1` | `3a8e8913d0b87ac0b68c3fc4ac24d6ad042074c9696a2cdbfae3682b2e0b96c7` |
| `evidence/source/90/input.json.gz` | upstream | `f66f68b048284b97c23bde6a768ef3f3c5f6bcc3` | `c519aa1822709897d541e7b83efdb027054ad636059bfb340acdb3e9c4a5fb9b` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
