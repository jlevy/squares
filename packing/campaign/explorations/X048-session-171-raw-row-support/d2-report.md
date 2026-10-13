# D2: forward checking and MRV on the same raw graph

D2 supports **69 of 96 rows** by fresh replay (same implementation, no search), adding
**14** to D1. It stopped at 50,000 unique exact pairs after 76 nodes and 13.529 seconds.
The remaining 27 rows are unresolved; no row was exhaustively unsupported and no
exclusion was made.

The separately preregistered continuation uses D1 revision
`f0b94b047ada6c22ae69fd3a4b49ca13cd206fee`, parent PR 307
`1525d4e03b891d6cbc9a7c0bb3fd1880765cfb65`, and the same cold-checked B saved state.
No producer or model change occurred.
[D1](d1-report.md) remains frozen.

## Search and preservation

All 49 D1 selections were rebuilt from exact piece/domain/core/source provenance, then
their edges were rechecked through the ordinary budgeted cache.
This retained their 55 rows and consumed 259 unique pairs (735 edge requests with
reuse). Imported cache and row claims were not trusted.
D2 then searched only missing rows.

The requested row’s owner remains first.
After each assignment, forward checking retains every compatible value in every
remaining owner domain.
An empty domain backtracks; otherwise MRV chooses the smallest filtered domain, with
numeric-owner ties. Candidate order remains descending exact twice-area, row, piece.
A cap during filtering is incomplete.
Fixed search remains the CLI default.

Filtering preserves all solutions; MRV changes only branch order.
Every retained clique is a complete solution of the frozen binary constraint network,
whose edges mean only that universal collision was not proved.
Thus its touched rows cannot be wholly removed by sound consistency reasoning on this
exact network. It does not establish a common geometric pose or apply to stronger
predicates or changed atoms.

## Controls, cost and disposition

44 focused tests passed in 2.90 seconds; Ruff and types were clean.
Controls compare both strategies with exhaustive tiny models, exercise a mid-filter cap,
and reject mutated seeds or collisions.
`endpoint6` retained all 24 rows and the exact endpoint; its 14 selections were freshly
replayed with 210 pair checks.

The coordinator rebuilt B atoms afresh with the same implementation and directly checked
all **57 selections / 855 fresh pairs**, reproducing 69 supported rows.
It used neither DFS nor the search cache.
The extra-row acceptance criterion passed; all-row completion did not.
This is incremental evidence, not a cold performance comparison with D1.

All frozen ceilings remain: 50,000 unique pairs, 100,000 nodes, 180 protocol seconds,
512 MiB worker, 4,096 atoms, six owners and 128 rows; decompressed input 64 MiB. The
target Job timeout was 240 seconds.
Search protocol CPU was 13.5 seconds.
Replay protocol wall was 0.3695591 seconds; its whole Job took 3.891 seconds and
observed worker peak was 151,908,352 bytes.
Exact search Job resources and cleanup are in
[the result summary](receipts/D2_result-summary.json); every Job cleaned up.
Working-set peaks and Job committed memory are separately labelled observations.

## Replay and retained evidence

[B packet](receipts/D2_B-support-packet.json),
[fresh replay](receipts/D2_B-independent-replay.json) (same implementation, no search)
and endpoint receipts retain exact provenance.
Published support packets are compact JSON copies checked equal to local pretty
originals. Receipt hashes identify canonical JSON content.
Large saved inputs and local partial/Job logs remain outside Git.

From `packing/`, using explicit Python 3.14 and supplied saved input paths:

```powershell
$ProjectPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$InputObjects = 'PATH/TO/SAVED-OBJECTS'
$ColdReceipt = 'PATH/TO/COLD-RECEIPT.json'
$D1Packet = 'PATH/TO/D1_B-support-packet.json'
$Out = 'PATH/TO/D2_OUT.json'
& $ProjectPython -m devtools.probe_n17_raw_row_support $InputObjects --checked-receipt $ColdReceipt --strategy forward-mrv --seed-packet $D1Packet --output $Out
& $ProjectPython -m devtools.probe_n17_raw_row_support $InputObjects --checked-receipt $ColdReceipt --verify $Out --output 'PATH/TO/REPLAY.json'
```

On Linux, from `packing/` with the project’s Python 3.14 environment.
Each run requires the cold saved-check receipt (`--checked-receipt`) for the same saved
seed and node:

```sh
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_raw_row_support \
  PATH/TO/SAVED-OBJECTS --checked-receipt PATH/TO/COLD-RECEIPT.json --strategy forward-mrv \
  --seed-packet campaign/explorations/X048-session-171-raw-row-support/receipts/D1_B-support-packet.json \
  --output PATH/TO/D2_OUT.json
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_raw_row_support \
  PATH/TO/SAVED-OBJECTS --checked-receipt PATH/TO/COLD-RECEIPT.json \
  --verify PATH/TO/D2_OUT.json --output PATH/TO/REPLAY.json
```

The frozen run additionally used the declared local Job supervisor.
No full graph, PC sweep, parent/kernel/capture/Flag2/checker/admission change or further
target followed. A larger completion slice requires a separate evidence-based contract.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
