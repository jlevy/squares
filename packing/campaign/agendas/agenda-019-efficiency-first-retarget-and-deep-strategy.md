---
title: "agenda-019 — efficiency first: the decision path, the retarget, and two deep strategy sessions"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-019
  title: "Efficiency First — the Decision Path, the Retarget, and Two Deep Strategy Sessions"
  updated: '2026-09-04'
  status: paused
  objective: >-
    Agenda 017's block moved seven registered cases and then hit a wall that is not
    mathematical. The exact event-cell sweep grew superlinearly with the atom count until
    a single decision cost hours, one search spent fifty-five minutes failing to finish
    its first round on a parameter that was tuned two container sides ago, and four lanes
    were run on four cores with no budget until the load average reached 10.6. None of
    that is a limit on the method; all of it is a limit on how many rungs a block can
    climb.
    This agenda buys throughput before it buys bounds, in that order, because the reach
    table now says the cases worth attacking sit at substantially larger container sides
    than the ones just climbed, while cost as a function of side has not yet been
    measured. Two
    efficiency-loop commitments carry measured baselines from Agenda 017's own logs and a
    named target each. Two insight-iteration sessions then ask the mathematical questions
    the ceiling proof opened, which is what should choose the next targets rather than
    the ladder's momentum. One research-loop commitment spends the throughput on the
    first high-prize case with a cost model recorded before the run, not after.
    The research wall is 480 elapsed minutes. The efficiency work is first because
    everything after it is measured in units the efficiency work changes.
  items:
  - id: BC-190
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11, 12, 17, 20]
    state: ready
    priority: 0
    question: >-
      The interval route decides more directions on fewer hypotheses than the exact sweep
      and did so between 22.7 and 44.2 times faster at the two largest identically timed
      atom counts, with the ratio widening between those measurements. Can the generator's own
      accept-or-reject decision move to it, keeping the exact sweep for retention and the
      exhaustive tier, and what does that do to the tail of a run?
    budget: >-
      120 elapsed minutes, Opus at maximum thinking, efficiency-loop throughout.
      The baseline is already reported and is the entry condition, not a conclusion:
      on the same frozen bytes, 425 atoms took the exact sweep 181 s against the interval
      route's 9.4 s; 1184 atoms took 1473 s against 65 s; and 2097 atoms took 4866 s
      against 110 s. The last two pairs were timed together and give ratios of 22.7 and
      44.2. Their two-point effective exponents are 2.09 for the exact sweep and 0.92 for
      the interval route. Those are empirical slopes between two certificates, not
      asymptotic complexity results.
      The introducing commit retains the last pair and the evidence entry retains its
      values, but no raw timing transcript, hardware description, or load trace survives;
      reproduce all three pairs before treating them as benchmark-quality measurements.
      0--30 profile the exact sweep at four atom counts spanning 168 to 2097 and fit the
      exponent, so the shape is measured rather than asserted. Record which phase
      dominates -- event-cell construction, the prefix sum,
      or the per-direction sweep -- because an algorithmic win is only available if one
      of them does.
      30--80 change the generator's decision to the interval route and measure the tail
      of a full run end to end against Agenda 017's recorded runs at the same sides.
      The equivalence guard is not optional and is the whole of the correctness argument:
      every certificate the interval decision accepts must still pass
      devtools.decide_certificate before retention, so the exact sweep moves from the
      inner loop to the gate and is never removed. Retention is unchanged.
      80--120 measure what the change buys on a case that could not be afforded before,
      and record the benchmark whether the answer is good or bad.
    entry: >-
      Agenda 017's run logs and certificate artifacts are retained. The newest paired
      times survive only in the introducing commit and evidence prose, so BC-190 begins
      by reproducing them. devtools.decide_certificate is the retention gate, and the
      fractional tier is green.
    exit: >-
      A benchmark record with the fitted cost exponent for the exact sweep, a named
      dominant phase, the measured end-to-end delta from moving the generator's decision,
      and either the change with its equivalence guard intact or a written rejection with
      the number that killed it.
    bead: think-jgeg
    workflows: [efficiency-loop]
    depends_on: []
    next_evidence: >-
      Whether the decision path is still the tail of a run, which decides whether BC-194
      is affordable at the side it names.
  - id: BC-191
    purpose: tool_validation
    owner_focus: efficiency
    instances: [12, 17, 18, 20]
    state: ready
    priority: 0
    question: >-
      Row generation is between 79 and 94 per cent of every round, the site grids do not
      scale with the container, and the rationalisation scale cost five times the margin
      that survived at the last rung. Which of the three is worth fixing, measured rather
      than guessed?
    budget: >-
      120 elapsed minutes, Opus at maximum thinking, efficiency-loop, in parallel with
      BC-190 on a separate core.
      Three measured baselines, all from Agenda 017's logs.
      First, round composition: at n = 12 a late round spent 1261 s in row generation
      against 86 s pricing; at n = 17, 472 to 761 s against 87 to 124 s; at n = 20, 500
      to 1158 s against 85 to 106 s. Row generation is the round.
      Second, site density. build_site_grid places a fixed count of points across the
      container, so the spacing grows with the side and the sites thin out relative to the
      B-square that has to cover them. At n = 20, side 24/5, grids (23, 31, 39) spent more
      than 3300 s without completing round 0; (29, 39, 49) completed it in 376 s. At least
      8.8 times, found by accident, on a parameter tuned when the sides were near 3.9.
      Third, rationalisation. The rounding loss is at most atoms/scale, and at n = 12,
      side 99/25, scale 200,000 and 2097 atoms it was 0.005314 -- five times the 0.001040
      margin the certificate ended with. The rung survived by luck. At scale 4,000,000 a
      simple inverse-scale estimate is about 0.000266 and the worst-case atoms/scale bound
      is 0.00052425; ceiling effects mean the actual loss must be measured. The atom count
      does not change with the scale.
      0--40 measure whether solve_rows re-solves from scratch each round or warm-starts,
      and what max_rounds and rows_per_direction actually cost at three sides. 40--80
      measure the site-density trade properly: denser grids buy fewer rows and cost more
      columns, and the crossover has never been located. 80--110 raise the default
      rationalisation scale and measure the verification cost it adds against the margin
      it returns. 110--120 record a core budget: four lanes ran on four cores at load 10.6
      and everything ran about two and a half times slower than it needed to.
    entry: >-
      The run logs for n = 12, 17, 18 and 20 at the sides named, and the two n = 20 runs
      at different grids, are retained and comparable.
    exit: >-
      A benchmark record for each of the three, a site-density rule expressed as a
      function of the container side rather than a constant, a decision on the default
      scale with its measured verification cost, a stated core budget, and every rejected
      change recorded with the measurement that rejected it.
    bead: think-ji0r
    workflows: [efficiency-loop]
    depends_on: []
    next_evidence: >-
      The cost per round as a function of the container side, which is the input BC-194's
      cost model needs and which nobody has yet measured across sides.
  - id: BC-192
    purpose: research
    owner_focus: insight
    instances: [11, 12, 17, 26, 51]
    state: blocked
    priority: 1
    question: >-
      The ceiling proof and the reach table changed the map: the cases this program spent
      itself on rank near the bottom, and eleven cases just above a perfect square are
      worth five to eight times more. Is that ranking the right one to act on, and what
      does the covering value do between here and there?
    budget: >-
      90 elapsed minutes, Opus at maximum thinking, insight-iteration. No experiment runs
      inside this commitment and no hypothesis is certified in it.
      The material is in the record: frontier/CERTIFICATE-REACH.md, the ceiling derivation
      in sqpack.fractional.certificate, and the six side-level program values reported
      for planning -- 11.0000 at 3.82, 11.9706 at 3.95, 11.9936 at 3.96, 16.9628 at
      4.58, 16.9303 at 4.59, and 18.0000 at 4.68. Only the 3.95 value is exactly
      reproducible from a retained artifact, where it is a feasible mass rather than a
      proved optimum; the reach table states the weaker evidence behind the other rows.
      The session's first duty is to be honest about that curve. The five values reported
      before the 4.68 run were described as consistent with a quadratic, but the raw runs
      are not all retained and the sixth value cannot simply be folded into that fit. No
      rung has ever been claimed from an extrapolation, and the reach table's prize column
      is what the ceiling allows rather than what a search reaches. If the session's
      conclusion depends on a fit, it must say so and name the retained measurement that
      would settle it.
      Questions worth the time: whether the covering value's growth has a derivation
      rather than a fit; whether a certificate found at one side transfers to a nearby
      side or to a larger n as a warm start, given that the covering program does not
      contain n at all; whether the cases above a perfect square are genuinely easier or
      merely have looser recorded bounds; and what the retained ladders say about how much
      of the gap between a restricted optimum and the covering value a search actually
      closes.
    entry: >-
      BC-190 and BC-191 are terminal, so the session knows what a run costs, and the reach
      table and ceiling derivation are retained and drift-checked.
    exit: >-
      One X-NNN report with the conclusions and their evidential status separated, any
      H-NNN candidates with mechanism, falsifier and expected information, an explicit
      statement of which conclusions rest on the fitted curve, and a ranked target list
      that BC-194 can take without re-deriving it.
    bead: think-9pfw
    workflows: [insight-iteration]
    depends_on: [BC-190, BC-191]
    next_evidence: >-
      A target ranking that accounts for cost as well as prize, which the reach table
      deliberately does not.
  - id: BC-193
    purpose: research
    owner_focus: insight
    instances: [11, 12]
    state: blocked
    priority: 2
    question: >-
      No single certificate on a fixed finite direction net exists above
      ceil(sqrt(n)) * B, so n = 12 is foreclosed on the current net against its
      conjectured 4. A refined-net family plus a limit is not excluded. What would a
      method that escapes the finite-net ceiling have to look like?
    budget: >-
      90 elapsed minutes, Opus at maximum thinking, insight-iteration, after BC-192.
      The ceiling has one mechanism and it is worth attacking directly: above
      ceil(sqrt(n)) * B a grid of ceil(sqrt(n))^2 pairwise disjoint axis-parallel
      B-squares fits inside the container, **Condition 5** gives each of them mass at
      least 1, and the
      total passes n. Every step of that is cheap, which is why the ceiling is sharp.
      Directions worth an hour and a half. The refuting grid is axis-parallel and uses
      direction 0 only; a condition that treated directions unequally would not be refuted
      by it, but **Condition 4**'s containment argument is what forces every direction
      to be covered,
      so the question is whether a weaker containment step exists. The shrink B is already
      maximal for its net, so raising it needs a finer net and the ceiling rises only as
      fast as D falls, which is about T/K. Whether an unavoidable set of shapes other than
      squares, or a condition on pairs rather than singles, changes the counting argument.
      And whether the foreclosure is worth accepting: n = 12 conjectured at 4 may simply
      not be this instrument's case, and saying so plainly is a legitimate outcome.
      A negative result here is a real result and is recorded as one.
    entry: >-
      BC-192 is terminal and the ceiling derivation with its four tests is retained.
    exit: >-
      One X-NNN report, either a candidate mechanism registered as an H-NNN with a
      falsifier, or a written argument that the ceiling is intrinsic to the counting step
      and the instrument's reach is what the reach table says it is.
    bead: think-z8ck
    workflows: [insight-iteration]
    depends_on: [BC-192]
    next_evidence: >-
      Whether the frontier beyond the ceiling is a research direction or a closed door,
      which decides whether any later agenda spends a block on it.
  - id: BC-194
    purpose: research
    owner_focus: correctness
    instances: [26, 30, 37, 51]
    state: blocked
    priority: 1
    question: >-
      With the decision path and the generator parameters measured, can a certificate be
      found at the first high-prize case -- a size just above a perfect square, where the
      lower bound is Nagamochi's closed form and the gap to the best known packing is near
      half a unit?
    budget: >-
      180 elapsed minutes, Opus at maximum thinking, research-loop, on the target BC-192
      ranks first.
      The cost model is recorded before the run and not after. At side 4.8 a round cost
      between 500 and 1158 s with grids scaled to the container; the sides in question are
      5.1 to 7.2, where the domain is between 1.1 and 2.3 times the area, so a round is
      estimated at 1400 to 3000 s before BC-191's changes and the estimate is written down
      so the run can be judged against it.
      The registered side is fixed before any command runs. The stop rule is the wall, not
      a converged objective: a run that does not close inside the budget is time-limited
      and its checkpoint carries to the next agenda, which is what happened to every long
      run in Agenda 017 and cost nothing because the checkpoints were sound.
      Retention is unchanged and is not negotiable: freeze the candidate before deciding
      it, decide the frozen bytes through devtools.decide_certificate, and retain only
      when both routes accept and agree on the value.
    entry: >-
      BC-190, BC-191 and BC-192 are terminal, a target and a side are registered, and the
      cost model is written down.
    exit: >-
      Either a retained certificate with both routes agreeing, or a measured negative with
      the restricted optimum the run reached, the loop's final least covered mass, and the
      cost per round against the model -- which is the number the next cost model needs.
    bead: think-48p0
    workflows: [research-loop]
    depends_on: [BC-190, BC-191, BC-192]
    next_evidence: >-
      The first measurement of what the generator costs and reaches outside the 3.8 to 4.8
      band every retained rung sits in.
  - id: BC-195
    purpose: tool_validation
    owner_focus: process
    instances: [11, 12, 17, 26]
    state: blocked
    priority: 3
    question: >-
      What did the efficiency work actually buy, which of Agenda 017's lessons are now
      enforced by a check rather than by a paragraph, and what is next?
    budget: >-
      60 elapsed minutes, review-planning-oversight. Classify every block with its stop
      reason, reconcile the benchmark records against the claims made from them, and
      confirm that the efficiency changes preserved every guard they were required to
      preserve -- retention through the gate, both routes agreeing on the value, the
      exhaustive tier still deciding what it decided.
      One question this closeout owns specifically: whether the exhaustive tier is still
      affordable. It held eleven marked nodes at the end of Agenda 017 and a single
      2097-atom certificate would add hours to it. D-438 was the same problem one tier
      down and it hid a real failure for hours.
    entry: >-
      BC-190 through BC-194 are terminal or explicitly stopped.
    exit: >-
      Per-block outcomes and stop reasons, a measured statement of what throughput
      changed, a decision on the exhaustive tier's budget, ranked candidates, and one
      selected next entry.
    bead: think-kibo
    workflows: [review-planning-oversight]
    depends_on: [BC-190, BC-191, BC-192, BC-193, BC-194]
    next_evidence: >-
      Whether the research bottleneck has moved off the decision path, which is what W5's
      contract says decides when it hands back to W6.
---
# Agenda 019 — Efficiency First: the Decision Path, the Retarget, and Two Deep Strategy Sessions

## Workflow Entry Point

This agenda is paused.
It becomes active when the operator has reviewed Agenda 017’s pull request and chosen
between this agenda and
[Agenda 018](agenda-018-ten-hour-continuation-ladders-theorems-and-wave-two.md), which
is also paused on the same review.

Begin at `BC-190` and `BC-191` together, on separate cores, both under
`efficiency-loop`. They are the only two commitments that start `ready`, and everything
else depends on at least one of them.
That ordering is the agenda’s whole argument.

## State at handoff

Written for whoever picks this up cold, so that nothing below has to be reconstructed
from the pull request.

**Retained and closed.** Seven registered cases carry a first-party weighted fractional
unavoidable-set certificate, and every one was decided twice from frozen bytes by two
methods that fail differently and agreed on the least covered mass to the digit.

| Case | Side | Result | `S` |
| --- | --- | --- | --- |
| `n = 11` | `381/100` | `T-018` | `S5` |
| `n = 12` | `99/25` | `T-017` | `S4` |
| `n = 17`, `18` | `459/100` | `T-019` | `S4` |
| `n = 19`, `20`, `21` | `24/5` | `T-020` | `S4` |

**Open, with different evidence boundaries.** Two sides were attacked and neither
settled. The n = 11 artifacts are retained; the n = 18 figures are an operator report
without its raw log, checkpoint, or candidate, so that run must be reproduced before
its details can be treated as validated measurements.

- `n = 18` at `117/25 = 4.68`. Three site sets, 538, 578 and 618 orbits, all returned a
  restricted optimum of exactly `18.000000`, the third after 157 row rounds and 7056 s.
  Adding sites can only lower a restricted optimum and it did not move.
  Either the covering value is at or above eighteen, or the optimum sits on a degenerate
  vertex. `T-019`’s `next_rung` carries both readings and the evidence for each.
- `n = 11` at `19/5 + 1/100 = 3.82`. Two independent site sets stop at exactly eleven,
  and the rejection route is far from closing: the exact maximum pointwise depth is
  `1925/1152`, which caps the feasible total at `1152/175` against the eleven a ceiling
  needs. `T-018`’s `next_rung` has the full account.

**Where the method stops, which is now proved rather than guessed.** No certificate for
`n` exists above `ceil(sqrt(n)) * B`. `n = 12` is foreclosed against its conjectured
`4`. At `n = 20` and `n = 21`, the ceiling leaves `0.1885` above the current result and
prevents this method from reaching within less than `0.0115` of the upper bound; it does
not show that certificates fill that runway. `n = 11`, `17`, `18` and `19` are limited
by their best known packings rather than by the ceiling.

**What the next block must not skip.** `BC-190` and `BC-191` come first because the
retention gate is now the dominant observed cost: one operator report gives `5378 s` at
2260 atoms. The few retained timing reports suggest steep growth but do not establish a
complexity law. Reproduce the measurements and reduce the gate cost before committing a
block to larger certificates.

## Why efficiency before bounds

Agenda 017 moved seven registered cases in a day.
It also spent its time like this.
The 2,097- and 2,260-atom pairs are operator-reported same-run measurements preserved
in introducing prose without raw timing transcripts, machine descriptions, or load
traces:

| Where the time went | Measured |
| --- | --- |
| Exact sweep, 425 atoms | `181 s` — against the interval route’s `9.4 s` on identical bytes |
| Exact sweep, 1184 atoms | `1473 s` — against `65 s` |
| Exact sweep, 2097 atoms | `4866 s` — against `110 s`; raw timing transcript not retained |
| Exact sweep, 2260 atoms | `5378 s` — against `173 s`; raw timing transcript not retained |
| Row generation, share of a round | `79%` to `94%` at every side measured |
| `n = 20` round 0, grids `(23, 31, 39)` | over `3300 s`, did not finish |
| `n = 20` round 0, grids `(29, 39, 49)` | `376 s` |
| Rationalisation loss at `n = 12`, side `99/25` | `0.005314`, against a surviving margin of `0.001040` |
| Load average, four lanes on four cores | `10.6` |

Three of those are not close calls.

The interval route decides **361 directions where the exact sweep decides 181**, needs
one fewer hypothesis — deciding on the doubled net it never invokes the `D4` reflection,
so it does not need **Condition 1** at all — and ran 22.7, 44.2, and 31 times faster in
the three reported pairs at 1184, 2097, and 2260 atoms.
The ratios are neither monotone nor controlled for machine load. The effective slopes
that can be fitted to these few observations describe those reports only; `BC-190`
exists to reproduce them and determine whether any scaling pattern persists.
The exact sweep belongs at the retention gate, where correctness is the only thing that
matters and a long checkpoint is affordable.
Whether it belongs in the generator’s inner loop is a question nobody has asked, and
`BC-190` asks it.

The site grids do not scale with the container.
`build_site_grid` places a fixed *count* of points across the side, so at `4.80` the
coarsest grid spaces sites `0.126` apart against `0.104` at `3.96` — 21% sparser
relative to the `B`-square that has to cover them.
One parameter change bought at least `8.8×` on a single round, and it was found by
accident while diagnosing a run that appeared wedged.

The rationalisation scale nearly cost a rung.
At `n = 12`, side `99/25`, the rounding loss was five times the margin the certificate
ended with. Raising the scale twentyfold does not change the atom count, but its actual
rounding and verification costs have not been measured; that is part of `BC-191`.

## Why the retarget needs a strategy session and not a sort

`CERTIFICATE-REACH.md` ranks all 100 cases and puts eleven above `+0.49` against
`+0.0671` at `n = 11`. It would be easy to read that as a work queue.
It is not one, for two reasons the table itself states.

The prize column is what the **ceiling** allows.
The real limit is the covering value at that side, and six side-level program values
have been reported.
Only the displayed 3.95 value is exactly reproducible from a retained
artifact; the other run objectives lack raw logs or checkpoints here.
The first five were described as consistent with a quadratic, but incomplete retention
and the later 4.68 report make even that fit planning conjecture.
No rung on this branch was ever claimed from one.

And cost grows with the container.
The high-prize cases sit at sides `5.1` to `7.2` against the `3.8` to `4.8` band every
retained rung occupies.
A round at `4.8` cost up to `1158 s`; nobody has measured a round at `5.5`.

`BC-192` is the session that turns a ranking into a plan, and it runs *after* the two
efficiency commitments precisely so that it can price its candidates.
`BC-193` asks the harder question underneath: the ceiling is sharp and its mechanism is
four cheap steps, so what would a method that escapes it have to change?
A written argument that the ceiling is intrinsic is a real outcome and is recorded as
one.

## What does not change

Agenda 017’s discipline is the reason its results survived contact with four of its own
mistakes, and none of it is on the table here.

Retention still means freezing the candidate before deciding it, deciding the frozen
bytes through `devtools.decide_certificate`, and retaining only when both routes accept
**and agree on the value**. `BC-190` moves the exact sweep out of the generator’s inner
loop and not out of the gate; the equivalence guard is the whole correctness argument
and its absence is a reason to reject the change.

A candidate still counts only when its row loop stopped for want of a violated
placement, and the loop’s final least covered mass is still reported beside the
objective.

And rule seven still holds: read the evidence, not a reconstruction of it.
The one pair without a retained raw transcript is labelled above, and the estimate of a
round at `5.5` is labelled as an estimate and written down before the run so the run can
contradict it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
