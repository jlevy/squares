---
type: is
id: is-01m29kqwefbzzpt7bngm68pq6p
title: "[epic] Benchmark the annealing as a search, and improve it"
kind: epic
status: open
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
child_order_hints:
  - is-01m29krxcs3exnz8e3zznsq84b
  - is-01m29krxs2y6kpy25e6ptvfwy7
  - is-01m29kqwxw2fh44xqzf0v5jbae
  - is-01m29n9q19bfnmxmyknc927dt1
created_at: 2026-09-12T01:29:34.406Z
updated_at: 2026-09-12T01:56:47.260Z
---
Owner, 2026-09-11: "iteratively improve the simulated annealing and physics simulations and similar, to try to improve their quality... make a list of hypotheses and then iteratively improve to see if we can figure out how to accurately benchmark and improve the search for n = 11, n = 17, and a few other minimal ones below 100... see if we can find parameters that work accurately... we need to set up a full test harness for this and then iteratively improve it."

**The question.** The workbench's physics is a search. In blind mode it is told nothing about where the squares are meant to end up: it starts from the packing of n in an inflated container, drops the new square into the emptiest place a coarse grid finds, and closes the walls in with contacts, walls and a decaying jiggle. Whether it can rediscover a known-best packing on its own -- and how often, and under what parameters -- is a measurable question that nobody has measured.

That question is worth answering for two separate reasons, and they should not be confused:
- **As an animation**, a blind run that lands near the record is a more honest picture than one snapped onto it.
- **As a search**, an annealer that reliably finds s(11) from nothing is evidence about the method, and the method is the thing the atlas campaign uses at scale.

**Why the small n.** n = 11 and n = 17 are the classic hard small cases -- tilted squares, irrational sides, a record that no grid reaches -- and they are small enough to run thousands of trials on a laptop. If the annealing cannot find them, no amount of parameter tuning at n = 100 means anything; if it can, the success rate per parameter set is a number that can be optimised.

**Order of work, and the first is not optional.** A harness that reports a defensible number comes first (think-f2ya). Then the hypotheses, written down BEFORE the sweeps so the sweep tests them rather than generating them (think-3ktv). Then the sweep itself (think-x1nb), then whatever the sweep says.

Runs on its own branch, stacked on the workbench branch, so the physics changes do not hold up the page work.
