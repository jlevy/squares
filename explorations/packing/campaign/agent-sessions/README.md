# Agent Sessions

These are the durable handoffs for the outer autonomous work loop.
They complement, and do not replace, the scientific record:

- `tbd` owns the work queue and dependencies;
- exploration, hypothesis, and experiment artifacts own mathematical ideas and
  measurements;
- `defects.yaml` owns actual mistakes; and
- an agent-session artifact records focus, budget, delegated work, elapsed time,
  integration evidence, stopping reason, and the exact next action.

One session has one primary focus and one integration bead.
The parent agent owns shared-file integration.
A delegated task should have a bounded, preferably disjoint write scope and return the
same compact contract represented in the frontmatter: outcome, evidence, files, checks,
uncertainty, next action, and elapsed wall time.

The controller may be a coding agent, a native long-running goal, an external watchdog,
or a human. The repository contract is portable across them: the session records the
objective, budget, slice clocks, stop conditions, evidence, and next action; `tbd` owns
the queue; and commits own integrated state.
A platform goal or watchdog should read and enforce this record rather than become a
second, private source of truth.
These documents are records, not schedulers, and [`runner.py`](../runner.py) remains the
executor for preregistered numerical rounds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
