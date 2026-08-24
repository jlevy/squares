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

The persistent platform goal is the controller.
These documents are records, not a second scheduler, and [`runner.py`](../runner.py)
remains the executor for preregistered numerical rounds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
