---
type: is
id: is-01m29kqwxw2fh44xqzf0v5jbae
title: A harness that reports a defensible success rate
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-12T01:29:34.907Z
updated_at: 2026-09-13T04:52:33.124Z
---
The first chunk, and nothing downstream means anything without it.

**What exists already, and should be reused rather than replaced:**
- `grade_motion.py` grades a run on two axes already -- outcome (residual, mean, turn at lock-in) and motion (wander, jerk, overlap) -- with WEIGHTS and a LOCK_IN_AT of 0.88. That is the scoring half.
- Blind mode (`setBlind`, `BLIND.inflate`) is the search half: a run with no knowledge of the target.
- The page's API drives both headlessly, and `check_revision6.py` already runs a blind sweep -- and does not finish, see think-i15w, which is a warning about how this harness must be built.

**What the harness has to report, per (n, parameter set):**
- **Success rate**: the fraction of trials whose final side is within a stated tolerance of the record. The tolerance has to be argued for, not picked -- the record's own poses score 0 to 1.3e-5 of summed overlap, so anything looser than that is not "found it".
- **Distance when it fails**: the distribution of the final side, not just the pass count. A method that lands 0.1% above the record every time is a different thing from one that scatters.
- **Cost**: wall time and step count per trial, so a parameter set that wins by running ten times longer is visible as such.
- **Reproducibility**: every trial keyed by its seed, so a claimed improvement can be re-run.

**Two design constraints, both learnt the hard way here:**
1. **It must finish.** `check_revision6.py` runs a blind sweep over 323 pairs and has never completed -- 57 minutes without finishing, measured. This harness samples a named set of n, reports incrementally, and has a declared budget.
2. **It is a program in `devtools`, not a script in the spike tree.** OR-1: never leave a measurement in one-off code. It comes under the lint and type floors like everything else, and its output is a file the repository can keep.

Done when: one command reports, for a named n and parameter set, a success rate with a confidence interval, a cost, and a seed list that reproduces it.
