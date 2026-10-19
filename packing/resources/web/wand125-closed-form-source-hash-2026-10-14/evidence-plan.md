# Evidence-Update Plan: replay4d 0.1.1 on the Closed-Form Bound

This is the plan the records lane applies to T-180, wand125’s closed-form lower bound,
as the 14 October records PR #602 registers it (head `429aa0b6`). The validation lane
`vcheap` wrote it on 14 October 2026 for bead think-4wgw and changed no register.
Apply it in PR #602 or after it.
Nothing here is on `main`. Every number comes from this packet’s [README](README.md) and
[`receipts/source-hashes.json`](receipts/source-hashes.json).

## The Claim Map

By [result-import.md](../../../campaign/result-import.md#stage-1-triage), new evidence
or an author’s answer about a registered entry takes no new entry: the source retained
at the revision that holds it (this packet, at `1c661b7`), and an evidence update.

| Claim of the source | Register action |
| --- | --- |
| replay4d 0.1.1’s source hash covers `b3d_sort.rs`: `f8cafeab…` over 11 files, against `92002e0e…` over 10 at 0.1.0 | `V-wand125-replay4d` gains a version row for 0.1.1 and `b3d_sort.rs` in its `source`; both hashes recomputed here |
| `b3d_sort.rs` is `23be1db0…` in the replayed and the published sources and has not changed | Stated in `E-wand125-closed-form-report`; checked here for the published revisions only |
| Each 0.1.1 result records `env.B3_PLAIN_RF`; no run in the receipts set it | Stated in `E-wand125-closed-form-report` as the source’s statement; the receipts themselves do not record it |
| `receipts/structure.json` regenerated with the published `validate_family.py` (`22e55f17…`) | The `fdd61866…` clauses of `E-wand125-closed-form-report` and `V-wand125-closed-form-structure` are rewritten |
| The theorem, the intervals, the release and the replay receipts | Unchanged: the folder’s other files are byte-identical, and the replay receipts are still 0.1.0 |

No rung moves, at any count: the update is about which bytes the source’s receipts
identify, not about how much of the certificate has been checked.

## `E-wand125-closed-form-report`

In `limitations`, replace

> with its results equal to the source’s receipt, whose validate_family digest
> (fdd61866…) is not the published script’s (22e55f17…), and two mutations refused;

with

> with its results equal to the source’s receipt, and two mutations refused.
> The receipt as first published named validate_family.py at fdd61866…, a revision never
> published; at 1c661b7 (2026-10-14T12:17Z) it names the published 22e55f17… with every
> result unchanged, and the author says on #600 that the published script was rerun.

and append

> At 1c661b7 replay4d 0.1.1’s source hash also covers seam4d_core/src/b3d_sort.rs, which
> b3d.rs compiles in: f8cafeab… over 11 files, recomputed here from the packets with
> 92002e0e… over 10 files for 0.1.0
> (packing/resources/web/wand125-closed-form-source-hash-2026-10-14/receipts/source-hashes.json).
> The replay receipts stay at 0.1.0: the full replay’s 306ad4b5… and the published
> build’s 92002e0e… do not identify b3d_sort.rs, which the source says was 23be1db0…,
> unchanged, in both. From 0.1.1 each result records B3_PLAIN_RF; the source says no
> receipted run set it, and the receipts do not record it.

Add the packet README to the entry’s artifacts if the records lane lists them:
`packing/resources/web/wand125-closed-form-source-hash-2026-10-14/README.md`.

## `V-wand125-replay4d`

Add to `source`:

```yaml
- packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/checker/seam4d_core/src/b3d_sort.rs
```

Add to `versions`:

```yaml
- sha256: f8cafeab078e1de31bacdef9c5c08ad70938f1b1b20fd3a2e1e54de9f73f1742
  path: packing/resources/web/wand125-closed-form-source-hash-2026-10-14/square-packing/problems/closed-form/checker/replay4d/src/main.rs
  note: >-
    replay4d 0.1.1 (wand125/square-packing 1c661b7), its printed source hash, which from
    this version also covers seam4d_core/src/b3d_sort.rs; the only other change is that
    each result records env.B3_PLAIN_RF. Recomputed here
    (wand125-closed-form-source-hash-2026-10-14/receipts/source-hashes.json).
```

and to the 0.1.0 row’s note: “It does not cover `b3d_sort.rs`.”

## `V-wand125-closed-form-structure`

Replace the note’s second sentence, “The source’s receipt names validate_family.py at
fdd61866…, which is not the published file.”, with: “The source’s receipt named
validate_family.py at fdd61866…, never published; at 1c661b7 it names the published
22e55f17… with the same results.”

## What It Can Move, and What It Cannot

It moves no rung and no standing bound.
It closes, for the record, review findings F1 (the structure digest) and F3 (the setting
is recorded from 0.1.1, for future runs), and the hash half of F2. The order check after
the sort that F2 also recommends is not in the code: `b3d.rs` is byte-identical at
`1c661b7`. A replay with 0.1.1 is what would identify `b3d_sort.rs` in a receipt.
The full replay waits on the owner’s budget (think-wu73).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
