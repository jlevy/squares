# Evan Daniel’s Checker Files at `659ee62`, Pinned 2026-10-24

This packet pins the checker files of
[evand/square-packing](https://github.com/evand/square-packing) at `659ee62`, the commit
Mohsen Khalili and Sara Gharabaghi’s releases name for Evan Daniel’s `zmx2` and
`qx2_zm.py`: their $s(44) = 7$
([packet](../moh63-dev-s44-equals-7-2026-10-29/README.md), issue #842) and their
$s(k^2 - 5) = k$ family ([packet](../moh63-dev-k2m5-family-2026-11-13/README.md), issue
#973). It claims nothing of its own.
Its Frontier key is **[evand square-packing 2026-10-24]**.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/evand/square-packing> |
| Revision | `659ee62e4a9d39542a1146e8b011cc3ab6407ede`, tree `1e87853b3a7a14af9622470337aaa51dd5efad8f` |
| Committed | 2026-10-24T05:01:33Z |
| Licence | MIT, “Copyright (c) 2026 Evan Daniel” (`LICENSE`) |
| Retrieved | 2026-11-14T02:03Z, a depth-1 fetch of that commit |
| Scope | `LICENSE`, `CREDITS.md`, `search/qx2_zm.py`, `search/zm_mixed.py`, `search/zeromargin.py`, `search/mixed_cover.py`, `verify2/Cargo.toml`, `verify2/Cargo.lock` and `verify2/src/bin/zmx2.rs`: 9 files, 426,327 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | `LICENSE`, `CREDITS.md` and `search/zeromargin.py` (88,777 bytes), byte-identical under [`square-packing/`](square-packing/) |
| Pinned to earlier copies | The other six, each byte-identical to a copy an earlier packet retains, compared by `devtools.acquire_source --check`: `qx2_zm.py` (`6294052a…`), `zm_mixed.py` (`1fd20346…`) and `mixed_cover.py` (`bb89de15…`) to the [3 October packet](../evand-square-packing-2026-10-03/README.md)’s `k2m4` checker, and `zmx2.rs` (`e2bb84e9…`), `Cargo.toml` and `Cargo.lock` to the [4 October packet](../evand-square-packing-2026-10-04/README.md) |

`search/zeromargin.py` at this commit is SHA-256
`3cb95fb74ce44666654d6cc193c3f255bd07ba6c9afd864a6f93e364d428c5cc`. It is the
`640fe453…` that earlier packets retain with two guards added: an `int64` bound under
which `CHAIN` totals are disabled when they could overflow, and assertions that the
centre pitch divides `cy_max` and is at most $1/2$. `qx2_zm.py` and `zm_mixed.py` import
it and print that it differs from the digest `zm_mixed.py` pins.
Khalili and Gharabaghi’s `qx2_zm.py` runs used it, and the import lane of 14 November
2026 ran it, through `devtools.replay_k2m5_family`, on their root-9632 window and its
scaled control.

`CREDITS.md` says the work was produced by Claude (Anthropic) in a single session under
human direction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
