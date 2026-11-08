# unnir’s `s(12) ≥ 9929/2500`, Pinned 2026-11-08

unnir (Numaro) reports `s(12) ≥ 9929/2500 = 3.9716`, which is `1/10000` above this
record’s verified `s(12) ≥ 7943/2000` (`T-095`).
The certificate is a plain weighted-point certificate in Evan Daniel’s format: 4,996
points on the grid `1/4000000` in the container `9929/2500`, weights over
`W = 9985226`, exactly D4-symmetric, total `119787760/9985226 < 12`.
Daniel’s verifier and Ryu Sungjoon’s `indep_scan.cpp`, both vendored in the source, accept
it on the angle net `N = 96000`, each with least captured weight exactly
`9985226/9985226 = 1` at bin `39531`.
The claim reached this repository as
[jlevy/squares#924](https://github.com/jlevy/squares/issues/924), opened by unnir on
2026-11-08 at 14:21 UTC.

The new certificate instance is unnir’s; the source credits the weighted closed-cover
reduction and both verifiers to Evan Daniel and Ryu Sungjoon, and the framework to Sam
Burns and Gustavo Massaccesi, Daniel, Ryu and this project.
It claims no new technique and no optimality.
This packet holds the source at a pinned commit, the exact audit of its premises, and
the replays and controls run here.
What the record makes of the claim is decided in the frontier records.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/unnir/s12-lower-bound-3.9716> |
| Revision | [`064c2955670765321aaf1c0a2d5c778949daab6b`](https://github.com/unnir/s12-lower-bound-3.9716/tree/064c2955670765321aaf1c0a2d5c778949daab6b), the repository’s only commit, `main` and `HEAD` when fetched |
| Committed | 2026-11-08T14:20:03Z (`15:20:03+01:00` by the author’s clock), “Publish s(12) >= 3.9716 certificate and replay evidence” |
| Retrieved | 2026-11-08T14:57Z, a complete clone |
| Licence | MIT. `LICENSE` grants it for the new certificate, the packet documentation and the replay helper, copyright unnir (Numaro); the vendored verifiers keep their upstream MIT notices in `LICENSES/`, Evan Daniel’s for `verifier/rust/` and Ryu Sungjoon’s for `verifier/cpp/` |
| Request | [jlevy/squares#924](https://github.com/jlevy/squares/issues/924) |

**Credit and AI assistance, as the source states them.** The README asks that the new
certificate and bound instance be credited to “unnir (Numaro), building on Levy, Evan
Daniel and Ryu Sungjoon’s work”, says the weighted-cover reduction and the verifier
implementations are theirs, and claims no ownership or novelty over them.
It says “Numaro Autonomous Research (agentic autonomous autoresearch) assisted the
work”, and that acceptance rests on the certificate and the executable checks, not on
agent agreement. It calls the two checks producer evidence, separately written but not
method-distinct, and lists as not done an external replay, an independent mathematical
review, a Lean replay and a parent-core interval replay.

## What Is Retained

The tree has 20 files. The 15 that are the source’s own are retained under
[`s12-lower-bound-3.9716/`](s12-lower-bound-3.9716/), byte-identical after decompression,
260,015 bytes. Five are pinned by digest only: `.gitignore`, which would act on this
repository’s tree, and four files this repository already retains byte for byte, which
the check compares: the two licence notices in `LICENSES/` and Daniel’s `Cargo.toml` and
`Cargo.lock`. The manifest is
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) and the
record [`acquisition/sources.json`](acquisition/sources.json), both written by
`devtools.acquire_source` from [`acquisition/declaration.json`](acquisition/declaration.json).
Every digest in the source’s `SHA256SUMS` matched the clone (`sha256sum -c`, 19 files).

| Upstream path | What it is |
| --- | --- |
| `certificate/s12_lower_3.9716.txt` | The certificate, SHA-256 `833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd`, as the issue states (stored as `.gz`) |
| `verifier/rust/src/main.rs` | Daniel’s `verify`, Git blob `f7c700c8`, SHA-256 `aca2fa6f…` |
| `verifier/cpp/indep_scan.cpp` | Ryu’s range-restricted checker, SHA-256 `74146d48…` |
| `verification/logs/` | The producer’s two complete runs, unedited |
| `verification/controls/` | The producer’s four control runs and their summary |
| `verification/replay.py`, `verification/summary.json` | The replay helper, which also writes the controls, and the machine-readable summary |
| `README.md`, `LICENSE`, `SHA256SUMS` | The claim and its account, the licence, the author’s digests of every file but `SHA256SUMS` |

From `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source unnir-s12-lower-bound-2026-11-08 --check`
re-derives the packet from its manifest.

**The vendored verifiers are the upstream bytes, except for one include line.** In a
blobless clone of `evand/square-packing` fetched on 2026-11-08, `git ls-tree 0e76d9fe`
gives `verify/src/main.rs`, `Cargo.toml` and `Cargo.lock` as blobs `f7c700c8`,
`7c956f54` and `946d942c`, which `git hash-object` gives for the vendored copies, as the
source says. That `main.rs` is not the copy this repository already retains: the
26 September evand packet keeps `s12/verify/src/main.rs` at blob `0e8035a3` (SHA-256
`226ef3f1…`, the bytes T-049 to T-095 ran), and the two differ in three places only, all
from the upstream commit `cca7bf1` of 7 October 2026: the doc comment on line 5 now says
the square is closed, “as in FORMAT.md”, and the program now exits `0` on VERIFIED, `1`
on a complete sweep that refuses, and `4` on a partial run, where it exited `0`
whatever its verdict. Nothing it computes changed. The manifest and lockfile are the
26 September packet’s, byte for byte. `verifier/cpp/indep_scan.cpp` is
`tools/indep_scan.cpp` of `squarepacker/s12-lower-bound` at `7a96bec3` (the
2026-10-05 packet’s copy, SHA-256 `35465554…`) with its one `#include <bits/stdc++.h>`
replaced by ten standard headers, as the source says; nothing else differs.
`indep_scan.cpp` is in turn `tools/indep_check.cpp` (`T-078`, `T-095`) with three
optional arguments that restrict the sweep to a range of bins and print each bin below a
threshold; given only the certificate, `N`, `Q` and `n`, as the producer ran it, it
sweeps every bin of `[0°, 90°]` as `indep_check` does.

## Compressed Files

Each is stored as deterministic gzip made by `gzip -9n`, by `devtools.acquire_source`;
the table gives the Git blob and SHA-256 of the decompressed bytes, which for an
upstream file are its blob and digest at `064c2955`. The repository’s readers take the
upstream path and decompress transparently through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `s12-lower-bound-3.9716/certificate/s12_lower_3.9716.txt.gz` | upstream | `90ba2625b3619938bb36ae73387aeed5f9720f15` | `833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
