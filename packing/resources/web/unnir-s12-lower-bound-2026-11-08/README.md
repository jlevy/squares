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
sweeps every bin of `[0°, 90°]` as `indep_check` does. With the range arguments it prints
`VERIFIED` for the range alone, so its receipts here are read by their arguments as well
as by their verdict lines.

## The Certificate, Derived Exactly

[`devtools.audit_s12_unnir_certificate`](../../../devtools/audit_s12_unnir_certificate.py)
reads the retained certificate and decides 16 checks in rational arithmetic, all passing
([`receipts/preflight.json`](receipts/preflight.json)):

- the digest, and the bytes are the canonical rendering of their integers;
- the header `15886400 4000000 / 4000000 / 9985226 / 4996`, so the container is
  `9929/2500`, `1/10000` above `T-095`’s `7943/2000`;
- every weight is positive, the least `1/9985226`; the points are distinct and in the
  closed container; the weighted multiset is invariant under the container’s eight
  symmetries, in 636 orbits (613 of eight points, 23 of four); and the total is
  `119787760/9985226`, below `12` by `34952/9985226`;
- at bin `39531` of `N = 96000`, where both of the producer’s checkers print their least
  captured weight, every open cell of the arrangement of the bin’s test square (side
  `σ = 499991/500000` as Daniel’s verifier rounds it, at the bin’s left angle) in a
  window of half side `1/1000` around `indep_scan`’s diagnostic centre is evaluated
  exactly. Of its 117 cells whose centre also centres a unit square at that angle that
  fits, the least captures 767 points of total weight exactly `9985226/9985226`, at the
  centre `(1.486821572…, 1.219308338…)`. The reported minimum is attained: the
  certificate has no slack at that bin, and a capture of exactly one is all the counting
  step needs. This bounds the minimum from above and decides nothing about coverage; and
- the four controls below, with the digests their receipts name.

The receipt also records, as a fact and not a check, that every one of `T-095`’s 1,736
points (Evan Daniel’s, `T-049`), dilated by `39716/39715` to this container, is among
this file’s points within one grid unit in both coordinates, at most `35663/39715` of a
unit, and that the other 3,260 points are new.

## Replays Here

On a four-core Linux container shared with another lane, which ran its own sweep at two
threads beside these; every heavy run here used at most two threads under `nice -n 19`,
so every wall time is contended. Each receipt of an external checker is written by
`devtools.replay_receipt` (command, working directory, load, exit status, wall and CPU),
and the checkers ran on the certificate as upstream bytes, SHA-256 `833b76a1…`.

| Checker | Built from | Run | Wall | CPU | Result |
| --- | --- | --- | ---: | ---: | --- |
| Daniel’s `verify` (external, the producer’s verifier) | this packet’s `verifier/rust/` (`main.rs` `aca2fa6f…`, the blob `f7c700c8` of `evand/square-packing` `0e76d9fe`), copied to scratch and built by cargo 1.97.0 `build --release --locked` with `CARGO_PROFILE_RELEASE_OVERFLOW_CHECKS=true`; binary SHA-256 `9f9dbeaf…`, the same in a second build into a fresh target ([build](receipts/daniel-verify-build.log)) | `verify s12_lower_3.9716.txt 12 96000 2 0` with `VERIFY_STATS=1` and no other `VERIFY_` or `TIGHT_` variable | 14,479 s | 28,028 s | VERIFIED over `k = 0..39765`, its two threads sweeping 19,901 and 19,864 bins, least captured weight `9985226/9985226` at bin `k = 39531`, exit 0; every line but the timing statistics equals `verification/logs/rust.log`, and the work it counted equals the source’s, 386,359,631 strips, 1,073,231,149,523 cells and 658,382,280,964 active ([receipt](receipts/daniel-verify-ovf-N96000.log)) |
| Ryu’s `indep_scan` (external, the producer’s second checker) | this packet’s `verifier/cpp/indep_scan.cpp` (`74146d48…`) by g++ 13.3.0 `-O2` ([build](receipts/indep-scan-build.log)); binary `fb0d4e2d…` | `indep_scan s12_lower_3.9716.txt 96000 1000000000000000 12`, no range arguments, so its own line reads `bins k = 0..95999 covering [0,90] deg` | 840 s | 834 s | VERIFIED, least `9985226/9985226` at `k = 39531`, exit 0; its output equals `verification/logs/cpp.log` byte for byte ([receipt](receipts/indep-scan-N96000.log)) |
| This repository’s native parent-core route (first party) | [`devtools.verify_evand_angle_net_native`](../../../devtools/verify_evand_angle_net_native.py), case `s12-unnir`, at commit `d1b96ff4` with a clean tree ([status](receipts/native-parent-core-N96000.git-status.txt)) | `--case s12-unnir --all --workers 2` | 18,576 s, 4,689 of them paused | 27,321 s | `PASS_COMPLETE`: all 39,765 rows certified at the threshold `9985226/9985226`, 416,547,583 boxes, no stalled box, no exhausted budget, no refutation. The least row bound is the threshold itself, first at row `1982`, and 1,045 rows end at it, the 26 rows `39531` to `39556` among them: where the branch and bound stopped, not the rows’ minima, as at `T-095`’s row `21524`. The native theorem gives the strict `s(12) > 9929/2500` ([receipt](receipts/native-parent-core-N96000.json), [row journal](receipts/native-parent-core-N96000.rows.jsonl.gz), [log](receipts/native-parent-core-N96000.log)) |

The native run was paused (`SIGSTOP`) from 15:15:51Z to 16:34:00Z, while the other
lane’s sweep held the cores this lane would otherwise have taken, and then resumed; its
wall includes the pause and its CPU, read by `wait4`, does not. The row that straddled
the pause reports 4,688 seconds in the journal, so the journal’s summed row seconds,
37,107, overstate the work.

The native reader builds the rows `[k/N, (k+1)/N]` of half-tangents, the core side
Daniel’s `σ_k` rounded down to `10⁻⁶`, at `N = 96000`, and decides each by
directed-rounding branch and bound over centre boxes, sharing no code with either sweep.

**Which runs carry the confirmation.** The source does not say how its points and
weights were found, or whether a search stopped on either of its checkers, and the
weights’ exact tie under Daniel’s core suggests they were fitted to his cells (the
review’s F3). So Daniel’s full sweep and `indep_scan`, both the producer’s code, are the
producer’s evidence. The confirmation rests on the two deciders no search could have
consulted: the native route above and the stage 4 review’s exact sweep of all 39,765
bins, below.

**Pricing.** Each run was priced from a sample here before it ran
([`receipts/pricing/`](receipts/pricing/)): `verify` on three windows of 40 bins at one
thread, 81.4 CPU seconds, so about 27,000 for all 39,765 bins; `indep_scan` on three
windows of 200 bins, 5.3 CPU seconds, so about 850 for all 96,000; the native route on
33 rows, about 0.72 seconds a row, so about 29,000 for all 39,765. The item’s cap was 40
CPU hours.

## Controls

[`devtools.audit_s12_unnir_certificate --write-controls`](../../../devtools/audit_s12_unnir_certificate.py)
writes four controls. The source’s two are rebuilt as its `verification/replay.py
--controls` writes them, on one line: `double-denominator`, `W` doubled with every
numerator kept (SHA-256 `7d13e224…`), and `truncated`, the last point dropped with the
count kept (`63161c11…`). Two are added here: `lowered-tight-orbit`, the eight-point
orbit of the heaviest point the tight pose above captures, `(6281612, 7246143)` at
weight `136132/9985226`, lowered by `1/9985226` a point, the least change a weight can
take, which drops the tight pose to `9985224/9985226` since it captures two of the
orbit’s points (`95ff8408…`); and `regrid-3999600`, the same integers read over
`D = 3999600`, which dilates the container to `39716/9999`, as `T-095`’s source did with
its own certificate (`4857a83c…`).

| Checker | `double-denominator` | `truncated` | `lowered-tight-orbit` | `regrid-3999600` |
| --- | --- | --- | --- | --- |
| `verify` | bin `39531` as the source runs it (`VERIFY_FULLSWEEP=1`): FAIL, `1/2`, exit 4 ([receipt](receipts/controls/daniel-verify-double-denominator-bin-39531.log)) | input error, exit 2 ([receipt](receipts/controls/daniel-verify-truncated-bin-39531.log)) | bin `39531`: FAIL, `9985224/9985226`, exit 4 ([receipt](receipts/controls/daniel-verify-lowered-tight-orbit-bin-39531.log)) | bin `0`: FAIL, `9453881/9985226`; bin `39531` passes at `9985226/9985226` ([0](receipts/controls/daniel-verify-regrid-3999600-bin-0.log), [39531](receipts/controls/daniel-verify-regrid-3999600-bin-39531.log)) |
| `indep_scan` | bin `39531` as the source runs it: NOT VERIFIED, `1/2`, exit 1 ([receipt](receipts/controls/indep-scan-double-denominator-bin-39531.log)) | input error, exit 2 ([receipt](receipts/controls/indep-scan-truncated-bin-39531.log)) | every bin: NOT VERIFIED, least `9985224/9985226` at `k = 39531`, 832 CPU s ([receipt](receipts/controls/indep-scan-lowered-tight-orbit-N96000.log)) | every bin: NOT VERIFIED, least `9453881/9985226` at `k = 0`, 818 CPU s ([receipt](receipts/controls/indep-scan-regrid-3999600-N96000.log)) |
| Native | row `39531` refuted with an admissible witness of charge `4593338/4992613` ([receipt](receipts/controls/native-double-denominator.json)) | its reader refuses the file, “point count does not match the file” ([log](receipts/controls/native-truncated.log)) | row `39531` refuted with an admissible witness of charge `9985225/9985226` ([receipt](receipts/controls/native-lowered-tight-orbit.json)) | row `0` refuted with an admissible witness of charge `4972138/4992613`; row `39531` certified ([receipt](receipts/controls/native-regrid-3999600.json)) |

The source’s two controls, run by the commands of its `replay.py` (`VERIFY_FULLSWEEP=1
VERIFY_BINS=39531:39531` for `verify`, the range `39531` to `39532` for `indep_scan`),
print every line of the source’s own outputs in `verification/controls/`. A bin refused
in a window is refused in the full sweep, since each bin is computed alone and one
refused bin makes the sweep refuse. The native control receipts ran at commit
`a3d81046`, and the regrid’s at `83b6b31b`, each with a clean tree.
[`tests/test_s12_unnir_certificate.py`](../../../tests/test_s12_unnir_certificate.py)
holds every receipt here and regenerates every control.

## The Review

A separately prompted review lane (L58), blind to these replays, read the source and
both checkers and re-derived the argument
([review](../../../../docs/project/reviews/review-2026-11-08-s12-unnir-3.9716.md)): it
accepts with findings, none blocking and none major. Its programs and receipts are in
[`review/review-2026-11-08/`](review/review-2026-11-08/README.md), moved here from the
packet path the lane guessed. Its exact decider, whose digest was recorded before its
authors read the producer’s checkers, decided all 39,765 bins in 9,494 CPU seconds: the
least core minimum is exactly `W` at the 24 bins `39532` to `39555`, and every bin
outside a band of 79 near 44.76° to 44.88° clears `W` by at least `2702/W`. Its
emulation of Daniel’s core puts exactly `W` at the 26 bins `39531` to `39556`, the band
where this packet’s native row journal ends at the threshold too. Its F1 (minor) is the
range-argument behaviour of `indep_scan` noted above; its F2 (minor), that the source’s
controls do not touch the geometry, is what the two controls added here answer; its F3
is why the producer’s checkers are the producer’s evidence. The blind findings, frozen at
15:20:50Z, are its `out/findings-blind.md`, SHA-256 `89e94eca…`.

## Reproduce

From `packing/`, with `SCRATCH` any directory outside the repository:

```bash
uv run --frozen --all-extras --group dev python -m devtools.audit_s12_unnir_certificate \
  --output SCRATCH/preflight.json --write-controls SCRATCH/controls
uv run --frozen --all-extras --group dev python -c "from pathlib import Path; \
from devtools.retained_data import read_retained_bytes as r; \
Path('SCRATCH/s12_lower_3.9716.txt').write_bytes(r(Path( \
'resources/web/unnir-s12-lower-bound-2026-11-08/s12-lower-bound-3.9716/certificate/s12_lower_3.9716.txt')))"
cp -r resources/web/evand-square-packing-2026-09-26/square-packing/s12/verify SCRATCH/verify
cp resources/web/unnir-s12-lower-bound-2026-11-08/s12-lower-bound-3.9716/verifier/rust/src/main.rs \
  SCRATCH/verify/src/main.rs
(cd SCRATCH/verify && CARGO_PROFILE_RELEASE_OVERFLOW_CHECKS=true cargo build --release --locked)
VERIFY_STATS=1 SCRATCH/verify/target/release/verify SCRATCH/s12_lower_3.9716.txt 12 96000 2 0
g++ -O2 -o SCRATCH/indep_scan \
  resources/web/unnir-s12-lower-bound-2026-11-08/s12-lower-bound-3.9716/verifier/cpp/indep_scan.cpp
SCRATCH/indep_scan SCRATCH/s12_lower_3.9716.txt 96000 1000000000000000 12
uv run --frozen --all-extras --group dev python -m devtools.verify_evand_angle_net_native \
  --case s12-unnir --all --workers 2 --output SCRATCH/native.json
```

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
| `receipts/native-parent-core-N96000.rows.jsonl.gz` | receipt | `77c4184e5c769488e757c6039de72d80fdcf0e16` | `73062feba1cd6b6bfdd3c8e459a0eab342d8e194b70c5285a852376d9ce8b380` |
| `review/review-2026-11-08/out/full-sweep-margins.tsv.gz` | receipt | `704009a42605b36d18e7884d60687620d48c8669` | `025b78be8246d4d8dffa48dbec86a37b428e5a512c82ceabef7608ef2f072cba` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
