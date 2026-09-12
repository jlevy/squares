---
type: is
id: is-01m29krxs2y6kpy25e6ptvfwy7
title: Sweep the parameters the hypotheses name, not a grid
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-12T01:30:08.545Z
updated_at: 2026-09-12T01:30:08.545Z
---
The sweep, and it only begins once the harness reports a defensible number (think-k2fr) and the hypotheses are written down (think-3zt6).

**The parameters in play**, all already in the page's tables and all already settable through the API, which is why this is a sweep rather than a rewrite:
- `BLIND.inflate` -- how much larger than the record the container starts.
- `PHYS.jiggle` and `PHYS.jiggleTorque` -- the shake's amplitude, and its decay exponent (1.5 today).
- `PHYS.jiggleHz` -- the frequency band a body's shake is drawn from.
- The force law's four parameters -- rigidity, repulsion, attraction, range -- which are the contact model itself.
- `PHYS.shutFrom` and the contraction's overlap tolerance -- how fast the walls close and what stops them.
- The step count, which is the search's time.
- `state.anneal`, the dial that scales the whole shake, 0 to 10.

**How to sweep, and the discipline matters more than the coverage.** A full grid over eight parameters is not a measurement, it is a way to find noise. Start from the hypotheses: each one names two or three parameters and predicts a shape. Sweep those axes at a resolution that could distinguish the prediction from its negation, with enough trials per cell that the confidence interval is smaller than the differences being claimed.

Report per cell: success rate with an interval, the failure distribution, cost, and the seeds. A cell that wins by running longer is not a better parameter set and the report has to make that visible.

**What counts as a result.** A parameter set that beats the shipped defaults on success rate at equal cost, reproduced on a held-out set of n that was not swept over. Anything else is a hypothesis for the next round.
