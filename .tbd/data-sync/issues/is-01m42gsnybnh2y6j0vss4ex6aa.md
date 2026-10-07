---
type: is
id: is-01m42gsnybnh2y6j0vss4ex6aa
title: N17 raw-piece row-support witnesses without full graph expansion
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
assignee: Guzhou0806
delegate: guzhou0806-codex-t0
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: null
hold_until: null
created_at: 2026-10-04T03:54:50.186Z
updated_at: 2026-10-07T06:23:10.673Z
started_at: 2026-10-04T03:55:17.450Z
closed_at: 2026-10-04T05:00:18.231Z
close_reason: |
  # P01D bounded diagnostic return

  Session171 is stopped with administrative closeout; upstream think-tmz6 ownership is preserved.
  Source/evidence published to Draft PR333 as `58af8cdedc64cb6fc4695e4e6f677df708fb6672`; its hosted checks are terminal
  19pass/36skipped, required checks all SUCCESS. Final metadata CI remains to be observed.

  D1:55/96rows,49selections,100000nodes/12069unique pairs,31.553s;41unknown.
  D2:69/96rows (+14),57selections,76nodes/50000unique pairs,13.529s;27unknown.
  Root independently replayed D2's855pairs; all49D1selections are an exact prefix and
  all55D1rows survive. No unsupported row, geometric feasibility or exclusion is claimed.
  D2 observed worker peak157319168B; independent replay151908352B; every Job cleaned up.
  44focused tests, Ruff/types and record/doc/synopsis/ledger/clock/gate/integrity/PR-body checks pass.
  D1 stale completed-delegation CI metadata was corrected without weakening clocks/caps.

  Frozen D2 caps:50000unique pairs,100000nodes,180s,512MiB,240sJob; same raw atoms/predicate.
  No full graph, producer/kernel/capture/Flag2/checker/admission edits, cap increase or further target.
  Code:packing/devtools/probe_n17_raw_row_support.py; tests:packing/tests/test_n17_raw_row_support.py.
  Report/compact receipts:packing/campaign/explorations/X048-session-171-raw-row-support/.
  Local B packet/progress/Job: runs/p01d-D2-B-packet.json, runs/p01d-D2-B-packet.partial.json,
  runs/p01d-D2-B-search/; root replay:runs/p01d-D2-independent-replay.json and matchingJobdirectory.
  Exact executable/cwd/argv and resources are in each Job final.json; portableexamples are in D2_REPORT.md.
  Native aggregate only:packing/campaign/resource-usage/codex-session-171.yaml,
  start2026-10-04T03:56:55.800523+00:00,end2026-10-04T04:55:27.9636830+00:00; one interval, privacy-safe aggregates.
  Live-task and boundary caveats remain; branch attribution is declared, not harness-observed.
  No native remeasurement is planned; later final metadata/CI observation is outside that lower bound.
  Recovery:fixedsearch remains default; D1 revisionf0b94b047 and its evidence remain frozen.

  Next:conditional one separately contracted P01E capacity completion only after finalmetadataCI.
  Rough250k same-mixestimate~68s and20–40MiB cachegrowth is not a measured guarantee.
resolution: null
duplicate_of: null
---
# P01D — lazy raw-piece row-support witnesses

Authorized by Guzhou's six-hour autonomous continuation (2026-10-04 10:50:13 to16:50:13 +08). Entry: W3 strategic selection, then W7 diagnostic implementation and W6 bounded measurement. This is a new protocol, not a relaxation or rerun of B1's refused full-graph protocol.

## Input, purpose and boundaries

Repository `squares`, branch `guzhou/n17-residual-compatibility`, baseline526a6c3a3330dddfae61be69bd44a0bdd1488d50; parent PR3071525d4e03b891d6cbc9a7c0bb3fd1880765cfb65. Existing cold-checked B/16bins/2round node under `runs/p01b-B-objects/` is the sole target. Existing endpoint6/4bins/1round is the positive control. No new producer run. Frozen B has2522 raw pieces,96 owner-angle rows,6owners.

Question: can every live row be extended to a complete six-owner selection of raw pieces whose15 sorted-owner pair predicates all remain unknown-compatible? One witness per row suffices to prove no sound consistency/search procedure on this exact pairwise graph can eliminate a complete row. It does not prove geometrical feasibility. Missing support after a cap is unknown, never unsupported.

Falsifier: independently checked support for all96rows retires whole-row deletion by this raw-piece pair predicate on this exact saved state. Completed exhaustive failure for a row is an abstract candidate only, requiring additional independent review before any conclusion. Partial support leaves the remainder unresolved. No full dense graph, no PC sweep, no bitset rewrite, no producer/kernel/standing-checker/certificate/admission changes; Flag2/capture remain upstream-owned.

## Responsibility and owned writes

Primary executor: existing GPT6.1Sol xhigh delegate, after finishing its temporary W3 recommendation; no second executor or routine reviewer. It owns new `packing/devtools/probe_n17_raw_row_support.py`, `packing/tests/test_n17_raw_row_support.py`, narrowly scoped documentation/receipts under `packing/campaign/explorations/X048-session-171-raw-row-support/`, local `runs/p01d-*` and `control/p01d-*`. Existing graph module is read-only unless coordinator approves a concrete minimal need.

Coordinator owns Git/bead/PR/shared-session records and independent witness/soundness acceptance. New source may be included in our existing Draft PR333 as a separately recorded continuation. No parent writes or main merge. Receiver: jlevy review through our Draft PR, no unsolicited messages.

## Bounded protocol

Use exact project Python3.14.7, cwd `squares/packing`, and adopted local `control/supervise.py` v2. Never PATH Python. Reconstruct raw atoms from accepted source rows/cores using existing exact atom construction; match the cold saved receipt to generated inputs. Stable owner,row,piece indexing. Force the requested row owner first, then remaining owners in ascending numeric order. Within each owner sort by descending exact twice-area of domain, then row and piece. Retain points/segments. Reuse complete witnesses to support their six rows. Query only edges needed by bounded search; cache canonical sorted-owner pairs. Each complete selection must choose one atom per owner and include a raw atom from the forced row.

Search implementation/control slot <=30minutes, first retained checkpoint<=20minutes. Target ceiling<=180seconds,<=50,000 unique exact pair tests,<=100,000 search nodes,<=4096 raw atoms total,<=6owners,<=128rows,512MiB actual worker; input<=64MiB decompressed. No arbitrary truncation or dropping degenerate pieces. Cold verification of all retained witnesses is a separate process, with fresh pair checks and no search cache;<=120seconds and512MiB worker. Explicit process-tree supervisor timeout<=240seconds and worker/review thresholds512MiB, system available8GiB. Each controlled job serial; no large allocations. Whole project target<=90minutes including>=15minutes finalization; terminate/replan at the slice boundary instead of silently extending. Outer user deadline unchanged.

Before shared-source editing AND immediately before committing source, fetch parent307 and compare relevant files/mechanism to frozen1525. If overlap, stop only affected code and preserve all evidence. Ordinary deterministic local/test/CI fixes within these files may be made automatically; no scope widening or limit relaxation after a guard. Save stdout,stderr,start/heartbeat/final Job receipts and diagnostic progress/partial witness receipts. Use new output paths for retries; no deletion.

## Acceptance and controls

| Item | Pass criterion | Evidence / owner |
| --- | --- | --- |
| Input identity | Cold saved stalled-check receipt exactly matches seed/node; accepted strict cores rechecked | CLI receipt; executor |
| Search soundness | Every complete returned assignment has one atom per owner, forced-row inclusion and all15 unknown-compatible predicates | Direct verifier independent of DFS/cache; coordinator |
| Controls | Exhaustive tiny finite cases agree; cap never means unsupported; touching not collision; empty/invalid refused; witness mutation rejected; exact endpoint survives | Focused tests + fresh endpoint control |
| Target | All96rows supported and fresh replayed => finite row-deletion ceiling; completed exhaustive unsupported row => candidate only; limits => guard-refused/inconclusive | Structured target and replay receipts |
| Resource | Every run within declared caps, actual worker RAM and owned tree cleanup recorded | Supervisor v2 final receipt |
| Delivery | Reusable tool, compact witnesses, honest local return, focused checks, Draft current-head CI terminal/classified, synced bead | Coordinator |

Exit: `handoff/P01D_RETURN.md` with counts, commands, status, elapsed/peak, scope, independent review and limitations. Keep original B1/B2/B3 unchanged. Rollback is to leave new diagnostic unused; no production path changed. Next project requires another explicit evidence-based scope decision inside the remaining user window; no automatic full graph or additional geometric target.
