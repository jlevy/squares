---
type: is
id: is-01m50wdta5k1jk1cvjx7hw5bjv
title: "Map the regularization pipeline: tools, inputs, cost per count, and what 'regularized' means in the record (regularized_drawings block, atlas)"
kind: task
status: closed
priority: 1
version: 5
delegate: ecstatic-edison-reg-audit
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m50wdwfc7a00s5yxqqq4p30r
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-15T22:55:17.317Z
updated_at: 2026-10-15T23:18:06.688Z
started_at: 2026-10-15T22:55:55.017Z
closed_at: 2026-10-15T23:18:06.688Z
close_reason: "Done: audit/root cause/map recorded in notes and scratchpad regularization-audit.md (2026-10-15)"
resolution: null
duplicate_of: null
---

## Notes

PIPELINE MAP (ecstatic-edison-reg-audit, 2026-10-15, origin/main 22a67ce4a).

What "regularized" means: policy docs/project/policies/regularization-policy.md (sections 3, 4, 11, 12) and guide docs/project/guides/regularization-process.md. A view is a derived drawing, admitted by decision-table row 10 after both exact routes accept it. Generators:
- regularize_axis_components/2: the reference and fallback. It snaps tilts under 1e-4 rad and is run by every --update-atlas.
- Evan Daniel's regularizer, through devtools.regularize_evand (vendored pin 675a5ea).
- regularize_grid_slack/0,1: the MILP port of his coincidence placement, straightening under 0.5, 1 or 5 degrees.

Selection is devtools.regularize_select, and admission is regularize_evand layer.

Records:
- regularized/index.json: status (92 regularized / 181 unchanged / 51 refused), generator, run, source.sha256 and view.sha256, plus a runs block of 17 receipts with aggregate decisions and cost only.
- default-drawings.json: only the 92 view counts, each with default and measures.
- results.yaml regularized_drawings: drawn views, with no default flag.
- Case-record regularization notes.
- Register `regularizations` items: a different sense, an exact re-solve of a packing.

Site: homepage and atlas draw the default, with a Regularized | Original toggle; the case page draws the default, with the house as published.

Commands, from packing/ (guide steps 1-7):
1. regularize_grid_slack --n N.. --run-dir R/grid-{0.5,1,5} [--near-axis-degrees 1|5]
2. regularize_evand run --run-dir R/evand --n N.. --workers K
3. regularize_select --evand-run .. --grid-run .. --output selection.json --markdown selection.md
4. The printed `regularize_evand layer` commands.
5. render_regularized_atlas --update; regularized_drawings; render_results --update; default_drawings --update; atlas README counts by hand; regularize_evand rungs.
6. A data commit, then release_pin --update and the re-pin commit.
7. packing-validate --records; --verify-atlas (deferred job); the seven test modules; release_pin --check.

Cost:
- grid-slack: 12 to 110 s per count per threshold (11.73 s measured here at n = 176, 5 deg; run means 37 to 106 CPU-s).
- evand: 140 to 220 CPU-s per count (adopt518-v2 8,047 / 37; rerun-2026-10-13 2,097 / 15; bound-1013 1,695 / 9).
- Selection: seconds to about 4 min per candidate view.
- Full evand pass over 324 counts: 49,302 CPU-s = 13.7 CPU-h (3.8 h wall at 4 workers). The guide and policy section 8 say "three to four CPU-hours", which is wall time mislabelled as CPU time (same kind as D068).
- The 20 pending counts: about 5 to 15 CPU-min each, 2 to 5 CPU-h in all, about 1 to 2 h wall at 3 workers.

Recorded afterwards: index entries (generator, run with rungs, source and view digests, exact_verification, regularization identity), the run receipt, regularized_drawings, case notes, default-drawings.json, renderings, RESULTS.md, the README counts and the release pin.

Automation and gate proposal:
- A driver (regularize_pending, or regularize_select --pending) computes the pending set from the record, runs grid-slack at 0.5, 1 and 5 degrees plus evand, then selects, admits and renders. It runs on request in intake with a receipt, since it exceeds OR-17's routine ceilings.
- A records-tier gate (digest comparisons only) puts every n <= 324 in one of: regularized (strong view drawn); regular-as-published (house U = N = 0); decided (the strong generators ran on this witness digest, with run ids and outcomes recorded, and drew nothing better); exempt (reason plus owner decision or bead). A pending count fails the gate. The first version allowlists today's 20 pending counts under think-rz8c, and the list may only shrink.
- Needed for it: the index keeps per-count run outcomes with the witness digest, update_atlas writes a `lapsed` block instead of printing, and default-drawings.json covers all 324 counts with state and measures (house-only counts measure in about 30 s single-threaded).

PR split:
1. Record and gate (think-gvke), before any T-174 adoption.
2. The intake step in result-import.md and adopt_houses (think-g3q7).
3. Runs (think-rz8c) by adoption commit: 3a = 60aa1d39e set with 176 first (105 129 146 156 176 204 271 272 303); 3b = 3b9fab84a set (153 154 207 211 237 241 302 304); 3c = 8a4d26fea set (175 232 264).
4. Residue: 102 236 258 263 269 and 39 55 290 291 (with think-yk2h), plus recording the decisions for 110 123 155 179 180.
