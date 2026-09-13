---
type: is
id: is-01m29kqwefbzzpt7bngm68pq6p
title: "[epic] Benchmark the annealing as a search, and improve it"
kind: epic
status: open
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
child_order_hints:
  - is-01m29krxcs3exnz8e3zznsq84b
  - is-01m29krxs2y6kpy25e6ptvfwy7
  - is-01m29kqwxw2fh44xqzf0v5jbae
  - is-01m29n9q19bfnmxmyknc927dt1
  - is-01m2chknz8861931tannzahgvh
  - is-01m2chkqr9wvm46hk56ehfzrqw
created_at: 2026-09-12T01:29:34.406Z
updated_at: 2026-09-13T04:52:31.788Z
---
Owner, 2026-09-11: "iteratively improve the simulated annealing and physics simulations and similar, to try to improve their quality... make a list of hypotheses and then iteratively improve to see if we can figure out how to accurately benchmark and improve the search for n = 11, n = 17, and a few other minimal ones below 100... see if we can find parameters that work accurately... we need to set up a full test harness for this and then iteratively improve it."

**The question.** The workbench's physics is a search. In blind mode it is told nothing about where the squares are meant to end up: it starts from the packing of n in an inflated container, drops the new square into the emptiest place a coarse grid finds, and closes the walls in with contacts, walls and a decaying jiggle. Whether it can rediscover a known-best packing on its own -- and how often, and under what parameters -- is a measurable question that nobody has measured.

That question is worth answering for two separate reasons, and they should not be confused:
- **As an animation**, a blind run that lands near the record is a more honest picture than one snapped onto it.
- **As a search**, an annealer that reliably finds s(11) from nothing is evidence about the method, and the method is the thing the atlas campaign uses at scale.

**Why the small n.** n = 11 and n = 17 are the classic hard small cases -- tilted squares, irrational sides, a record that no grid reaches -- and they are small enough to run thousands of trials on a laptop. If the annealing cannot find them, no amount of parameter tuning at n = 100 means anything; if it can, the success rate per parameter set is a number that can be optimised.

**Order of work, and the first is not optional.** A harness that reports a defensible number comes first (think-f2ya). Then the hypotheses, written down BEFORE the sweeps so the sweep tests them rather than generating them (think-3ktv). Then the sweep itself (think-x1nb), then whatever the sweep says.

Runs on its own branch, stacked on the workbench branch, so the physics changes do not hold up the page work.

## Notes

OVERNIGHT, 2026-09-12. The epic's question is answered, and the answer is not the one any of the hypotheses predicted.

**The blocker first.** think-kbwb: every generator on the page was seeded from n alone, so there was one blind trial per n and a rate was 0 or 1. setSeed fixed it, bit-identical at seed 0 (d1ea06e6).

**Then the instrument, and then the instrument's own bug.** The harness (e1b5a864) reported clean numbers for two rounds -- a uniform 'closes about half the record-to-grid gap' and a promising best-of-k tail -- and all of it was wrong, because nothing checked that a run's arrangement was a packing. Thirty parameter cells reported a container BELOW the known-best side. That should have been the tell.

**The finding (ee27f8e3, H-210, exp-206).** 15,000 of 15,000 blind trials end with squares overlapping, 0.03 to 0.12 of a unit side, at every n and every shake level including zero. The control that makes the tolerance a measurement: the snapped run, which ends on the record's poses by construction, scores 5.5e-7 to 1.0e-6. The workbench's physics does not settle to a packing -- the animation looks right because its last frame is snapped.

**The corrected picture (1eab3313).** Projecting each run to a packing makes every trial valid, and over 30,000 valid trials: median closed is NEGATIVE at every n -- run once, the method is worse than the trivial grid -- while best-of-1000 reaches 0.974 at n = 5 and 0.947 at n = 10, valid packings within 0.28% and 0.42% of the records. At n = 11, 17, 29 the tail barely clears the grid.

So there is a difficulty gradient and it runs opposite to the invalid rounds': the search works where there are few squares.

Open, and the next things to do: whether a resolver that rotates scores these same runs higher (every number above is a lower bound); whether the tail keeps paying past k = 1000 at n = 5 and 10; and whether the physics can be given a resolution phase of its own, which would make the ANIMATION honest as well as the search.
