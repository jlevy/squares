# replay4d 0.1.1: the Closed-Form Checker’s Source Hash Covers `b3d_sort.rs`

On 14 October 2026, wand125/square-packing published replay4d 0.1.1, the source’s own
checker of the closed-form certificate for $s(N) \ge a(N)$ at every non-square
$N \ge 49$. The commit answers three minor findings of this project’s
[mathematical review](../../../../docs/project/reviews/review-2026-10-14-wand125-closed-form-lower-bound.md)
(F1, F2, F3), which this project asked about on jlevy/squares#600 at 11:30:40Z. wand125
answered there at 12:28:15Z, citing this commit.
The source hash that replay4d prints now covers `seam4d_core/src/b3d_sort.rs`. Each
result records the `B3_PLAIN_RF` setting, and `receipts/structure.json` names the
published `validate_family.py`. The bound is retained at the earlier pin in
[`../wand125-closed-form-2026-10-14/`](../wand125-closed-form-2026-10-14/README.md),
which the records lane registers as T-180 (PR #602). This packet is a later revision of
the same source and is new evidence about that entry.
It retains the changed files, recomputes every hash the commit states from the packets
alone, and gives the records lane an [evidence-update plan](evidence-plan.md).
No standing bound or rating changes here.

| Item | Value |
| --- | --- |
| Source | [`problems/closed-form`](https://github.com/wand125/square-packing/tree/1c661b705422b58b5eb169589776b50c14be2a2f/problems/closed-form) |
| Pinned revision | `1c661b705422b58b5eb169589776b50c14be2a2f`, the head of `main`, committed 2026-10-14T12:17:00Z, tree `cde505c0…` |
| Earlier pins | `746e2c5`, its parent, in `wand125-closed-form-cfcheck-2026-10-14/`; `9a28a84`, in `wand125-closed-form-2026-10-14/` |
| What changed | Seven files of the folder: `README.md`, `SPEC.md`, `checker/Cargo.lock`, `checker/replay4d/Cargo.toml`, `checker/replay4d/src/main.rs`, `checker/replay_all.py`, `receipts/structure.json`; nothing else in the tree |
| Retrieved | 2026-10-14T17:26:58Z; `git ls-remote` still read `1c661b7` as the head |
| Author’s answer | [#600, 2026-10-14T12:28:15Z](https://github.com/jlevy/squares/issues/600#issuecomment-6168332700) |
| Release | `closed-form-v1`, unchanged: `ASSET.json` is one of the identical files |
| Bead | think-4wgw, under think-tsox |

## The Claim

The folder README adds two paragraphs.
On the hash:

> `b3d_sort.rs` (included by `b3d.rs`) was not covered by either hash.
> Its SHA-256 is 23be1db0de55790110ff97c966bf34a6046c1d224a0f5bad98c6639866895928 in the
> sources used for the replay and in the published sources, and the file has not changed
> since. From version 0.1.1 the source hash also covers `b3d_sort.rs`; the published
> sources of 0.1.1 hash to
> f8cafeab078e1de31bacdef9c5c08ad70938f1b1b20fd3a2e1e54de9f73f1742. Nothing else in the
> checker changed except that each result now records `B3_PLAIN_RF` (below).

On the arithmetic switch:

> `B3_PLAIN_RF=1` switches the rational-function arithmetic to the step-by-step
> reduction of the Python reference, for cross-checking; the reduced form, and so every
> decision, is the same.
> No run in the receipts set it: neither the replay driver nor the commands of
> `published_checker.json` set the variable, so all runs used the default path.
> From version 0.1.1 each result records its value (`env.B3_PLAIN_RF`, `unset` if not
> set), and `replay_all.py` prints it.

SPEC.md §9.4 says the same about coverage.
The commit message says the structure receipt was “regenerated with the published
validate_family.py”.
The answer on #600 adds that the old receipt “was written about 20 seconds before a last
edit to `validate_family.py`”, that the intermediate revision was not kept, and that
`structure_all.py` was rerun with the published script on the published assets, ALL
STRUCTURE OK, with every per-interval result identical.
It also says that the 28 tests pass and that the existing receipts keep their hashes.

## What Was Checked Here

[`devtools.audit_wand125_closed_form`](../../../devtools/audit_wand125_closed_form.py)
`hashes` reads the three packets through their acquisition records.
A pinned-only file is read from the copy it names, and every file must have its
manifest’s digest. At each revision it recomputes the source hash by the rule in that
revision’s own `main.rs` (`source_hash()`, lines 64–78 at this pin): for each covered
file in order, the name, a NUL byte, the length as a 64-bit big-endian integer, and the
bytes, then the SHA-256 of the whole.
Its receipt is [`receipts/source-hashes.json`](receipts/source-hashes.json).
It took 0.2 CPU-seconds and ran nothing of the source.

| Revision | replay4d | Files covered | Source hash recomputed | Stated by the source | Equal |
| --- | --- | ---: | --- | --- | --- |
| `9a28a84` | 0.1.0 | 10 | `92002e0e…c193` | `92002e0e…` (README, `published_checker.json`) | yes |
| `746e2c5` | 0.1.0 | 10 | `92002e0e…c193` | unchanged | yes |
| `1c661b7` | 0.1.1 | 11 | `f8cafeab…1742` | `f8cafeab…` (README) | yes |

The eleventh file is `b3d_sort.rs`. `Cargo.toml` and `Cargo.lock` both name 0.1.1 at
this pin.

- **Controls.** Flipping one bit of `b3d_sort.rs` leaves the 0.1.0 hash unchanged at
  `9a28a84` and `746e2c5` and changes the 0.1.1 hash.
  The same flip in `b3d.rs` changes all three.
  So the file is covered from 0.1.1 and was not before.
- **Unchanged files.** `b3d_sort.rs` is `23be1db0…` at `9a28a84` and `1c661b7`, the
  value the README states, and `validate_family.py` is `22e55f17…` at both.
- **The structure receipt.** `receipts/structure.json` named `fdd61866…` at `9a28a84`
  and names `22e55f17…` here, the published script.
  That is the only field that changed; every result is the same.
  The intake’s own run of the published script on all 68 families
  ([`../wand125-closed-form-2026-10-14/receipts/structure-check/`](../wand125-closed-form-2026-10-14/receipts/structure-check/run.json))
  gave those same results, so the new receipt is consistent with it and with the
  author’s account of a rerun, which the bytes alone cannot show.
- **`B3_PLAIN_RF`.** `main.rs` at this pin writes `env.B3_PLAIN_RF` into the summary
  JSON; at `9a28a84` it did not.
- **The compiled programs.** The calibration of bead think-au7j built both versions with
  rustc 1.86.0 and the locked crates
  ([`../wand125-closed-form-2026-10-14/receipts/calibration/`](../wand125-closed-form-2026-10-14/receipts/calibration/calibration.json)).
  The 0.1.0 binary printed `92002e0e…` and the 0.1.1 binary printed `f8cafeab…`, with
  `env.B3_PLAIN_RF` recorded as `unset`. So the programs agree with the recomputation.

## What It Answers, and What It Does Not

| Finding of the review | At `1c661b7` |
| --- | --- |
| F1: the structure receipt names a `validate_family.py` that was never published | Answered: the receipt names the published script, with unchanged results |
| F2: the source hash omits `b3d_sort.rs`; add a post-sort order check | The hash covers the file from 0.1.1. The order check, which the review recommended and #600 did not ask for, is not added: `b3d.rs` is byte-identical |
| F3: no receipt records `B3_PLAIN_RF` | For future runs: 0.1.1 records it. The existing receipts do not; the source states that none set it |

The receipts of the replays stay at 0.1.0. The full replay’s `receipts/replay.json`,
4,294 CPU-hours, names source hash `306ad4b5…`, of sources that are not published and
differ, the source says, in comments only.
`receipts/published_checker.json` names `92002e0e…`. Neither hash identifies
`b3d_sort.rs`, and no result in `replay.json` records a version or the switch.
What ties those runs to the published `b3d_sort.rs` is the source’s statement that the
file has not changed, which the bytes here cannot check.
A replay run with 0.1.1 identifies it.

## Retained Here

`devtools.acquire_source` retained 11 of the 60 files in scope, byte-identical under
`square-packing/`, from the declaration in
[acquisition/declaration.json](acquisition/declaration.json):
[acquisition/sources.json](acquisition/sources.json) is the record, and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the
manifest of all 60. The other 49 are byte-identical to the copies the two earlier
packets retain and are pinned against them, so the manifest shows that nothing else
changed.

| Path | What it is |
| --- | --- |
| `square-packing/problems/closed-form/README.md`, `SPEC.md` | The claim and specification, as changed at the pin |
| `square-packing/problems/closed-form/checker/replay4d/Cargo.toml`, `src/main.rs`, `checker/Cargo.lock` | replay4d 0.1.1: the version, the source-hash list and the `env` field |
| `square-packing/problems/closed-form/checker/replay_all.py` | The driver, which now prints the setting |
| `square-packing/problems/closed-form/checker/seam4d_core/src/b3d_sort.rs`, `CPYTHON_SORT_LICENSE` | The file the hash now covers, unchanged, and its licence notice |
| `square-packing/problems/closed-form/receipts/structure.json` | The regenerated structure receipt |
| `square-packing/problems/closed-form/LICENSE`, `square-packing/LICENSE.md` | The folder’s MIT notice, and the repository’s statement that each folder keeps its own licence |
| `receipts/source-hashes.json` | The recomputation above |
| `evidence-plan.md` | The evidence update for the records lane |

## Sources and Notices

`problems/closed-form/LICENSE` is MIT, Copyright (c) 2026 wand125. `b3d_sort.rs` is a
port of CPython’s list sort and keeps the Python Software Foundation licence beside it
in `CPYTHON_SORT_LICENSE`. The root `LICENSE.md` says the repository has no single
licence and that each folder keeps its own.
The commit names Hiroaki Hosono as author and Claude Opus 5.5 as co-author; the folder
prose says nothing more about AI assistance.
Credit stays with the bibliography key of the bound, `[wand125 closed form 2026-10-14]`.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source wand125-closed-form-source-hash-2026-10-14 --check
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_closed_form hashes --check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
