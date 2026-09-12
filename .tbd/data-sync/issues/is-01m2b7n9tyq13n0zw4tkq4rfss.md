---
type: is
id: is-01m2b7n9tyq13n0zw4tkq4rfss
title: "[epic] Three aspects, one set of building blocks: Pack, Search, Animate"
kind: epic
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
created_at: 2026-09-12T16:36:55.773Z
updated_at: 2026-09-12T16:36:55.773Z
---
Owner, 2026-09-12: "we have to have everything exposed in the workbench in a way that you can show this to me. It may be that we have another tab called Search and organize it logically. Packing could be more prescriptive and have various settings for a single run. Search would be for many runs. Animation is a completely different thing. But they're built from the same building blocks."

Three aspects, one set of parts:

- **Pack** -- one n, one run, prescriptive. The settings that shape a single trajectory.
- **Search** -- one n, many runs. The settings that shape a campaign: how many trials, what varies between them, and what the distribution of outcomes looks like.
- **Animate** -- a range of n played end to end. A presentation of finished records, not a computation.

They already share the machinery: one physics, one force law, one seed, one beat. What is missing is that two of the three have no home on the page. Everything the first night's benchmark measured -- validity, best-of-k, the distribution, the parameter sweep -- lives in a Python harness and is invisible in the thing the owner actually looks at.

**The foundational chunk is not the tab.** It is the resolver (think-r8kp): the page has no way to say whether an arrangement is a packing, and its blind and free styles draw arrangements that are not. Until the page can separate overlapping squares and report the container the separated arrangement needs, a Search tab would display the same invalid numbers the first two benchmark rounds did. Moving it into the page fixes the animation as well as the search.

Chunks:
- **think-r8kp** -- the page can tell a packing from an overlap, and resolve one into the other.
- **think-e2mq** -- Search as a third mode, with its own controls and its own readout.
- **think-9h5d** -- the controls reorganised so each group belongs to a mode, which is think-cz99 with a third mode to place them in.

What must not happen: three copies of the physics. The modes differ in how many runs they ask for and what they show, never in what a run is.
