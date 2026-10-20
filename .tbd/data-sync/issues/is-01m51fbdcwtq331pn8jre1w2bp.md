---
type: is
id: is-01m51fbdcwtq331pn8jre1w2bp
title: "Validation backlog, intake pass 2026-10-16 (#639, #640; owner cap 40 CPU-h per item)"
kind: task
status: open
priority: 2
version: 2
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m51e5r3sg4h1wcrh7c826v7b
created_at: 2026-10-16T04:26:01.500Z
updated_at: 2026-10-17T02:51:48.713Z
---
The validation backlog of the 2026-10-16 intake pass (epic think-mdnn), under the owner's cap of 40 CPU-h per item (2026-10-14; think-lh7d holds the earlier passes' rows). Each row's bead carries a `## Validation` block.

| Bead | Item | CPU-h | Status | Depends on |
| --- | --- | --- | --- | --- |
| think-g59l | #639: the source's verify_exact.py on 23 data files at evand 7d1407a, with mutated controls (under think-phyb) | <= 0.6 (source's wall x 8 processes) | gated on stage 2 retention (no owner decision) | think-phyb's packet |
| think-nqnl | #640: sq19 full from-source build, axiom check and kernel replay (under think-a4x3) | ~190-380, plus <= 40 kernel replay (estimate from "several hours on 64 cores") | held | owner budget; a machine of hundreds of GB; think-a4x3's packet |
| think-nqnl (subset) | #640: fetch.sh hash check, the existence half (Sq19Lean.EndpointPacking), and one generated module timed to price the build | unmeasured; an estimate of 1-3 | proposed, on the owner's word | Lean 4.34.1 and the Mathlib cache installed |

Not validation, tracked here for completeness: think-o40t, the mathematical review of #640 (a strongest-tier review lane, tokens rather than CPU), which starts once stage 2 retains sq19.

## Totals

- Runnable after stage 2, no decision: about 0.6 CPU-h (think-g59l).
- Held: about 190-420 CPU-h (think-nqnl), with a proposed subset of an estimated 1-3 CPU-h.

## Not established from the record

- think-nqnl: the source publishes no CPU time; the build's price is an estimate from its wall time and core count, and the unpacked size of the archives is unmeasured.
- think-g59l: the irreducibility check and a second route over number fields (a W7 converter, no bead) are unpriced.

## Machine

4 CPUs, 15 GB and 16 GB of free disk, shared with gates: think-g59l fits; think-nqnl's full run does not.

blocked_on: none

## Notes

Rows added 17 Oct (coordinator), from #660's addressing passes:
| think-3mry | Adopt T-174 at its 50 staged rational counts (house rule, #660); regularize each in the adoption's PR | ~10 (about 0.2 CPU-h per count: Daniel driver plus grid-slack at 0.5/1/5 degrees; witnesses 2.84 MB stored, 19.25 MB in a checkout) | open, waits on #660 | #660 |
| think-ot5c | Algebraic house writer, then adopt T-174 at 70, 153 and 207, and T-193 at its 16 counts (#658) | writer: code; runs ~4 | open, waits on #660 and #658 | #660, #658 |
