# D1: lazy raw-piece row support on the frozen B state

D1 found freshly replayed (same implementation, no search) complete abstract supports
for **55 of 96 live rows**. It stopped at the preregistered 100,000 DFS-node ceiling;
the remaining 41 rows are unresolved.
No row was reported exhaustively unsupported and nothing was excluded.

This is a new protocol after the raw full-graph guard refusal, not a relaxation of that
protocol or a new producer run.
It uses the existing B/16-bin/2-round saved objects and their cold `PASS_SAVED_STALL`
receipt. Baseline revision: `526a6c3a3330dddfae61be69bd44a0bdd1488d50`; frozen parent PR
307: `1525d4e03b891d6cbc9a7c0bb3fd1880765cfb65`.

## Model and inference

An atom is the hull of one original convex residual polygon, including points and
segments, paired with its accepted row’s strict core.
Row/source references, residuals, outer domains and intervals are checked; strict
containment is rechecked.
Pairs use the same exact `universal_collision` predicate and sorted-owner direction as
the frozen residual graph.
A present edge means only that this test did not prove universal collision, not that two
geometric poses can be simultaneously realised.

Each retained six-owner clique is a full solution of this frozen binary constraint
network.
AC/PC preserve every full solution, so a clique touching a row prevents complete
deletion of that row by these rules.
Thus the 55 supported rows cannot be wholly deleted by AC/PC on these exact atoms and
this exact predicate.
This does not demonstrate a common realisable packing, and does not apply to stronger
predicates or changed atoms.

Owners are forced-row first, then numeric.
Within each owner candidates are ordered by descending exact twice-area, then row and
piece. Every original nonempty residual is retained.
A complete witness marks all six rows it touches.
Pair results are cached only after a successful predicate decision.
No full graph or PC sweep is constructed.

## Frozen limits and actual result

The whole run had ceilings of 50,000 unique exact pair tests, 100,000 DFS nodes, 180
seconds protocol wall, 4,096 atoms, six owners, 128 live rows, 64 MiB decompressed
input, and 512 MiB actual worker peak.
The Job supervisor had a 240-second timeout and 512 MiB worker/review thresholds, with
system available RAM at least 8 GiB.

| Quantity | Actual |
| --- | ---: |
| Raw atoms / live rows | 2,522 / 96 |
| Retained complete selections / supported rows | 49 / 55 |
| Unique pair tests / DFS nodes | 12,069 / 100,000 |
| Protocol wall / CPU | 31.5530502 s / 31.484375 s |
| Supervised whole-job wall | 34.766 s |
| Actual observed worker peak WS | 152,653,824 B |
| Exhaustively unsupported rows | 0 |

Supported rows by owner: 8:16, 10:16, 17:16, 18:4, 19:2, 22:1. The deterministic run
stopped during an unresolved row’s search; it did not treat the cap as exhaustive
failure. The full packet and last progress packet were retained.
No limits were enlarged.

## Controls and fresh replay

The focused new and reused controls passed: **34 tests in 2.97 seconds**; Ruff and
basedpyright passed.
Controls cover exhaustive tiny finite models, canonical pair direction,
node/pair/wall/memory caps, no timeout cache entry, contact, empty/degenerate inputs,
source and witness mutations, omitted row claims and bounded packet input.
Pure graph tests isolate the shared CI process’s historical memory counter; the actual
standalone CLI memory guard is separately tested.

Existing `endpoint6`: 148 raw atoms and 24 rows; all rows supported after 90 unique
pairs and 91 nodes. A fresh process checked 14 selections and 210 pairs, replaying the
exact endpoint enclosure’s row/piece inclusion.
Search/replay actual worker peaks were 142,917,632 B / 143,577,088 B; each whole Job
took 3.328 seconds.

The coordinator ran B `--verify` again in a separate supervised process: a fresh replay
by the same implementation, without search.
It reconstructed atoms from the source, did not invoke DFS or consume its cache, and
checked all **49 selections / 735 fresh pairs**, reproducing **55/96 supported rows**.
Outcome: `PASS_REPLAYED_PARTIAL_SUPPORT`; protocol wall 0.3148229 s, CPU 0.3125 s;
whole-job wall 3.672 s; actual worker peak 153,407,488 B.

Every retained Job receipt reports zero active processes, confirmed tree cleanup and no
cleanup errors. Working-set sums and Job committed memory are separately labelled; these
are observed live-process peaks, not a perfect instantaneous tree RSS maximum.
Import startup is included in supervised wall but excluded from protocol wall.

## Retained artefacts and invocation

- `receipts/D1_B-support-packet.json`: complete raw-row witness packet (compact JSON;
  semantically identical to the 147,330-byte local pretty original).
- `receipts/D1_B-independent-replay.json`: coordinator’s fresh replay receipt (same
  implementation, no search; the file name predates that wording).
- `receipts/D1_endpoint-support-packet.json`, `receipts/D1_endpoint-replay.json`.
- `receipts/D1_result-summary.json`: exact revisions, counts, check results and
  separately labelled Job resource/cleanup summaries.
- Local progress: `runs/p01d-B-packet.partial.json`; full Job logs and receipts:
  `runs/p01d-B-search/` and `runs/p01d-B-independent-replay/`.

Published support packets are compacted copies with checked semantic JSON equality;
local pretty originals are preserved.
The replay receipt’s packet hash identifies canonical JSON content, so it is unchanged
by whitespace compaction.
Git identifies the published file bytes.

The exact executable, cwd and argv are retained in each local Job’s `final.json`; they
use the explicit project venv Python and `-m devtools.probe_n17_raw_row_support`, with
`--verify` only in the fresh replay.
The new implementation is identified by this publication’s revision and
`packing/devtools/probe_n17_raw_row_support.py`.

Portable CLI examples, from `packing/`, with an explicit Python 3.14 interpreter and
supplied saved-object/receipt paths (the frozen run additionally used the local Job
supervisor with the limits above):

```powershell
$ProjectPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$InputObjects = 'PATH/TO/SAVED-OBJECTS'
$ColdReceipt = 'PATH/TO/COLD-RECEIPT.json'
$Out = 'PATH/TO/OUT.json'
& $ProjectPython -m devtools.probe_n17_raw_row_support $InputObjects --checked-receipt $ColdReceipt --output $Out
& $ProjectPython -m devtools.probe_n17_raw_row_support $InputObjects --checked-receipt $ColdReceipt --verify $Out --output 'PATH/TO/REPLAY.json'
```

On Linux, from `packing/` with the project’s Python 3.14 environment.
Each run requires the cold saved-check receipt (`--checked-receipt`) for the same saved
seed and node:

```sh
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_raw_row_support \
  PATH/TO/SAVED-OBJECTS --checked-receipt PATH/TO/COLD-RECEIPT.json --output PATH/TO/OUT.json
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_raw_row_support \
  PATH/TO/SAVED-OBJECTS --checked-receipt PATH/TO/COLD-RECEIPT.json \
  --verify PATH/TO/OUT.json --output PATH/TO/REPLAY.json
```

Source/test editing began after session readiness at 11:56:55 +08; control checkpoint
was retained at 12:07:33, independent entry gate passed at 12:09:21, and the only B
search ran 12:09:56–12:10:30 on 2026-10-04. No parent, kernel, capture, Flag2, producer,
standing checker, certificate grammar or admission path was edited.

D1 is frozen as **partial supported / bounded incomplete**, not a whole-route falsifier.
Any change to search ordering requires a separately preregistered continuation with the
same model and explicit caps; no default larger run follows from this record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
