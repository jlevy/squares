---
type: is
id: is-01m5frzbx5nq339srgw0c4q12b
title: "intake_sweep: say a read at a pinned head can be removed only when no commit it covers is left unretained"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: coord-intake-1021b
labels:
  - tooling
  - packing
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T17:43:34.564Z
updated_at: 2026-10-21T17:43:35.876Z
started_at: 2026-10-21T17:43:35.876Z
---
repositories_section in packing/devtools/intake_sweep.py prints "<url>: a packet now pins <head>, so intake-watch.yaml's read of it can be removed." for every read through the head whenever the head is among the repository's pins. It never asks whether that packet's declared scope retains the paths of the commits the read covers.

Measured on 21 October 2026 by the read-only triage c-triage-sweep-1021b with the sweep's own read_history. franciscouzo/square-packing's read through 7b6c87e is the head; couzo-issue678-2026-10-18 pins it but retains 90 of its 543 changed paths. With the read removed, _unretained lists 7b6c87e again ("7b6c87e Land 85 verified packing bounds and source provenance"). Following the note turns a clean sweep red, and a pass that trusts it removes a read the record needs.

Fix: derive the hint from what _unretained already computes. Say a read can be removed only when the history read without it finds no unretained commit; otherwise print nothing, or say the read stays because N commits it covers change paths no packet retains. Add tests beside the existing intake_sweep tests: a pinned head whose packet scope omits one changed path keeps its read and gets no removal note, and one whose packet retains the whole tree gets the note.

Done when the franciscouzo case prints no removal note and the tests run in --fast. Price: 1 to 2 agent-hours, no CPU.
blocked_on: none
