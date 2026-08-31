---
title: agenda-009 — fix what the rollups exposed, then decide what the machinery is now good for
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-009
  title: Fix what the rollups exposed, then decide what the machinery is now good for
  updated: '2026-08-31'
  status: active
  objective: >-
    Eight to twelve hours. The first three commitments are hygiene and come first because
    each of them cost this project real time in the session that found them, and because
    they are what makes the research after them cheaper: a control suite six of whose
    members were not firing, a pre-push floor that let three red pushes through in one
    day, and a session-closing procedure that is a documented sequence rather than a tool.
    None is research and none should take long.

    `BC-088` is the pivot and everything after it is `tentative` on purpose. The machinery
    changed a great deal this month -- exact construction over `Q(sqrt 2)`, interval
    certification, the promote pipeline, an assurance record that now says which results
    are ours -- and the research queue was written before most of it existed. Deciding
    what to run next is itself a piece of work with an exit, not a preamble to one, and
    the four candidate blocks below are inputs to that decision rather than commitments
    already made.

    The question behind the whole agenda is the owner's: where could a stricter, better
    informed search actually produce a packing nobody has, for some `n` under 100? Three
    measurements bound the answer and are recorded in `BC-088`'s entry. They are the
    reason this agenda exists in this order.
  items:
  - id: BC-085
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 11, 29]
    state: complete
    priority: 0
    question: >-
      Can a negative control that has stopped matching its own anchor be refused in
      seconds, rather than discovered in a thirty-minute log nobody runs on a branch?
    hypotheses: []
    budget: >-
      about 60 minutes, W5, in slices of 20
    entry: >-
      `D-403`. Six of a hundred and fifty controls were not firing when checked on
      2026-08-30. One had been broken hours earlier by inserting `novelty_basis` into the
      middle of the field block it anchored on; two anchor a `touches=(...)` tuple in a
      one-line form the formatter has since wrapped; two agenda-map controls no longer
      match their blocks; one is masked by a link that resolves in the repository but not
      inside the packing-scoped snapshot the runner builds. The suite runs only in the
      full gate, and a pull request runs `--fast`, so none of this was visible on the
      branch that caused it.
    exit: >-
      A `--records` step asserting every `replace` source in `devtools/controls.yaml`
      appears exactly once in its declared file, without executing a mutation, plus the
      five controls still stale repaired or restated. The snapshot-scope one is a
      legitimate exception if the runner's scope is deliberate, and saying so is an
      acceptable answer -- but it must be said rather than left looking like a failure.
    bead: think-9k5k
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Discharged by commit d2b6ba3: `check_control_anchors` resolves all 150 anchors by
      string containment in under a second, wired as the records-tier step "control
      anchors still resolve", reusing the runner's own `resolve_control_target` so it
      cannot drift. Four remaining broken anchors repaired and verified firing (the sixth
      was fixed in 8307ee3); the snapshot-scope case is handled by resolving against the
      real checkout, which the checker states in its own comment. Five tests, including
      that a missing anchor and a doubled anchor are both refused. Verified against the
      tree on 2026-08-31 by session-049 before this state changed.
    artifacts:
    - devtools/check_control_anchors.py
    - devtools/controls.yaml
    - src/sqpack/cli/validate.py
    - tests/test_control_anchors.py
  - id: BC-086
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 29, 40]
    state: complete
    priority: 0
    question: >-
      What is the cheapest tier that would have caught each of this session's three red
      pushes, and is it cheap enough to be run every time?
    hypotheses: []
    budget: >-
      about 90 minutes, W5, in slices of 30
    entry: >-
      Three CI reds in one day, each a single step, each self-inflicted. `D-394`'s
      consumer guard and the type floor were both missed because `--edit` does not run
      tests (`D-381`, `D-393`); the third was missed because a local full gate held
      `.gate-running` and the push went out rather than waiting 26 seconds for
      `basedpyright`. The rollup prices the habit: 3580 tool calls, 77 errors, and
      `--edit` invoked far more often than any tier that runs a test.
    exit: >-
      Either a tier between `--edit` and `--fast` that runs the tests reachable from the
      changed paths -- `Step.touches` and `--since` already exist and already select
      steps this way -- or a measured statement that no such tier is cheaper than
      `--fast` and the floor should simply be `--fast` before a push. Either answer ends
      the guessing. A lock held by one's own gate must also stop being a reason to skip a
      floor: the tiers that need no marker should say so.
    bead: think-u5q2
    depends_on: []
    workflows: [pipeline-improvement, efficiency-loop]
    next_evidence: >-
      Discharged by session-049. The tier exists: `packing-validate --push` runs the edit
      tier plus a "reachable behavioral tests" step, with `devtools.reachable_tests`
      selecting test files by import closure, text mention, and an always-run walker set,
      erring toward inclusion exactly as `Step.touches` does. Measured 2026-08-31 in one
      container: `--push` 58s wall (126 reachable tests of 1,045 collected) against
      `--fast` at 646s, essentially serial. All three 2026-08-30 red pushes are covered:
      the D-381 pair falls in the import closure of `validate.py`, and the sweeps are
      walkers that run every time. The marker half is also done: `.gate-running` is a load
      lock, so `--records`, `--edit`, and a narrow `--push` take no marker and say so,
      while broad or full selections still refuse a second gate. The tier caught two real
      problems in its first hour: a D-358 clock violation in the session record being
      written, and its own test file's lint exemption.
    artifacts:
    - devtools/reachable_tests.py
    - src/sqpack/cli/validate.py
    - tests/test_reachable_tests.py
  - id: BC-087
    purpose: tool_validation
    owner_focus: process
    instances: [5]
    state: complete
    priority: 1
    question: >-
      Is closing a session a tool, or a sequence a session has to remember?
    hypotheses: []
    budget: >-
      about 60 minutes, W7, in slices of 20
    entry: >-
      The closing cycle -- regenerate the session rollup, roll up every sub-agent log not
      already recorded, declare them all in `resource_rollups`, render the ledger,
      validate -- was reconstructed by hand twice on 2026-08-30, and the second pass found
      two sub-agent logs the first had missed. `OR-1` says a repeated measurement belongs
      in a tool. The checker is also one-directional: it refuses a terminal session
      declaring no rollups, and says nothing about a rollup file no session declares. Ten
      such files exist; all ten turn out to be legitimately grandfathered, which is only
      knowable by looking.
    exit: >-
      `devtools/close_session.py` performing the cycle idempotently, plus orphan
      visibility in `check_session_rollups` -- reported, not refused, since a pre-field
      session legitimately declares nothing. A session closed by the tool should need no
      manual step and no memory of the order.
    bead: think-5w14
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Discharged by commit 9a6dd3e: `devtools/close_session.py` performs the cycle
      idempotently and `--render` prints the cost block as its last act (OR-9).
      Grandfathered sessions are reported rather than refused -- the records tier prints
      the 44 sessions closed before the field existed by name. Session-048 closed itself
      with the tool, which is the exercised proof. Verified against the tree on
      2026-08-31 by session-049 before this state changed.
    artifacts:
    - devtools/close_session.py
    - devtools/check_session_rollups.py
    - campaign/session-close-report.yaml
    - campaign/schemas/session-close-report.schema.yaml
  - id: BC-088
    purpose: research
    owner_focus: insight
    instances: [28, 29, 51, 68, 69]
    state: complete
    priority: 0
    question: >-
      Given machinery that did not exist when the research queue was written, where is a
      new packing actually reachable, and in what order should the attempts run?
    hypotheses: []
    budget: >-
      about 180 minutes, W3, in slices of 30, with three to five sub-agents on
      read-only investigation per `OR-2`
    entry: >-
      Three measurements taken 2026-08-30 bound the search space, and none of them was
      available when agendas 001 through 008 were written.

      First, the gap between best known and proved lower bound is about 0.5 for every open
      case, and it is the lower bound that is weak rather than the packing that is loose.
      Ranking by that gap ranks nothing.

      Second, 31 of the 65 open cases report the trivial grid as their best known --
      n = 12, 20, 21, 30 through 32, 42 through 45, 56 through 61, 72 through 78, and 90
      through 97 -- clustering just below each perfect square. Nobody has beaten the grid
      at any of them. Whether that is because it cannot be beaten or because nobody has
      tried hard enough is exactly the question, and the two have very different answers.

      Third, 10 open cases have a best known found by simulated annealing -- n = 28, 29,
      39, 41, 50, 51, 53, 55, 71, 87. A stochastic incumbent is the one kind of record a
      better search can plausibly beat, because nothing about it claims optimality.

      Also available now and not before: exact construction over a named field with a
      verifier that decides contacts rather than tolerating them, interval certification,
      the promote pipeline from numerical pose to exact field, and an assurance record
      that distinguishes what this project established from what it is repeating.
    exit: >-
      A sequenced research plan naming which of the four candidate blocks below to run and
      in what order, with the ones not chosen given a reason rather than left silent. New
      hypotheses registered where the review finds them. Where a block is judged
      unreachable, the measurement that says so, not an impression -- `D-402` is what an
      impression costs. The plan must state, for at least one specific `n`, what would
      have to be true for a new packing to exist and how the attempt would know it had
      failed.
    bead: think-bxqv
    depends_on: [BC-085, BC-086]
    workflows: [research-pass, insight-iteration]
    next_evidence: >-
      Discharged by session-049 phase 3; the plan is X-009 and it registers H-049 and
      H-050. Sequencing: BC-089 first (14 of 15 trailing cases verify exactly at their
      published side per the delegated scan, one of them -- n = 82 at 6 + (5/2)sqrt(2) --
      re-verified first-hand under exact_sign this session), paired with the
      robust-rational sweep the machinery inventory measured at 33s for 34 decimal
      witnesses; BC-091 narrowed to the n = 90 primitive question (H-049) with n = 61
      parked in the proof lane; BC-090 gated on an instrument beating exp-011's measured
      grid-return at n = 17 before any target is spent, n = 71 first when taken (H-050);
      BC-092 folded into BC-090's instrument design -- the enumeration price (9.3e9 raw
      orbit work at n = 5, hard size cap at 5) rules it out as its own block.
    artifacts:
    - campaign/explorations/X-009-where-a-new-packing-is-reachable.md
    - campaign/hypotheses/H-049-squeezable-20-in-4x6.md
    - campaign/hypotheses/H-050-n71-angle-split-load-bearing.md
  - id: BC-089
    purpose: research
    owner_focus: correctness
    instances: [18, 19, 26, 27, 38, 50, 52, 54, 66, 67, 82, 84, 85, 86]
    state: ready
    priority: 0
    question: >-
      Which of the 15 trailing cases with a published exact side are materialisations of a
      published rule, the way `n = 40` turned out to be?
    hypotheses: []
    budget: >-
      about 180 minutes, W3 with sub-agents, in slices of 30
    entry: >-
      15 open cases carry a published exact side and a verified ceiling that trails it.
      Ten are in `Q(sqrt 2)` -- n = 19, 26, 27, 38, 52, 66, 67, 82, 84, 85 -- which is the
      field this project already computes in. Three are in `Q(sqrt 7)`, `n = 50` is
      rational at `7 + 4/7`, and `n = 54` is a nested radical.
      The pattern has fired twice: `D-389` and `D-398` both found a construction published
      and unbuilt here.
    exit: >-
      For each of the 15, a statement of whether its witness is a materialisation of a
      published rule, with the construction built and verified exactly where it is, and a
      typed refusal where it is not. Knowing the exact side is not knowing the pose --
      `D-402` established that recovering a pose from these decimals fails -- so the win
      here is recognition, and a case that needs pose recovery belongs in `BC-090` rather
      than being forced here.
    bead: think-d0j1
    depends_on: [BC-088]
    workflows: [research-pass, research-loop]
    next_evidence: >-
      Sequenced first by X-009, with n = 53 moved to BC-090's pool (its two extra tilt
      classes yield no stable relation at 49 digits) and the block widened by the
      machinery inventory's sweep: robust-rational promotion of the decimal known-best
      witnesses, measured at 33s for 34 sizes, then exact constructions replacing the
      relaxed ceilings where a published rule exists. Session-049 phase 4 takes n = 82
      first -- verified first-hand this session as gobel_family(4,5) plus one L of 17,
      exact over Q(sqrt 2) at 6 + (5/2)sqrt(2), with the eighteenth L square refused.
      Owned by think-d0j1 with the sweep on think-3nc4; think-xdly stays on BC-049.
  - id: BC-090
    purpose: research
    owner_focus: insight
    instances: [28, 29, 39, 41, 50, 51, 53, 55, 71, 87]
    state: tentative
    priority: 2
    question: >-
      Can a stricter, better informed search beat a stochastic incumbent at any of the ten
      sizes whose best known came from simulated annealing?
    hypotheses: []
    budget: >-
      about 240 minutes, W3 and W6, in slices of 30
    entry: >-
      Ten open cases have a best known found by annealing and no claim of optimality. This
      project now has an exact verifier, a quench stack with a measured floor, contact
      enumeration, and a promote pipeline -- so a candidate found numerically can be
      pushed toward exactness rather than left as a decimal. What it does not have is a
      search that uses the structural knowledge the contact work produced.
    exit: >-
      Either a packing strictly better than the retained best known at some `n`, verified
      exactly or interval-certified and offered as a first-party result with its novelty
      basis stated -- or a measured account of why the search does not reach, naming what
      it would take. A negative answer with a number is the expected outcome and is worth
      recording; `n = 28`'s near miss at 0.004 is the shape of it.
    bead: think-xdly
    depends_on: [BC-088]
    workflows: [research-loop, insight-iteration]
    next_evidence: >-
      Sequenced third by X-009 and gated: no target is spent until an instrument reaches
      s(17) within 1e-4 on one of five seeds -- exp-011 measured the stock annealer
      returning the grid there, and the machinery inventory's own cold runs returned the
      grid at n = 29, 41 and 51. When the gate passes, n = 71 goes first (the one size
      whose catalogue records cold search failing; H-050 is its cheapest question) and
      n = 53 joins the pool from BC-089. Certification is not the bottleneck: a
      candidate pose reaches an independently verified rational bound in seconds.
  - id: BC-091
    purpose: research
    owner_focus: insight
    instances: [90]
    state: ready
    priority: 1
    question: >-
      At the 31 open sizes where nobody has beaten the trivial grid, is the grid optimal or
      merely unbeaten?
    hypotheses: []
    budget: >-
      about 240 minutes, W3, in slices of 30
    entry: >-
      31 of 65 open cases report the trivial grid, clustering just below each perfect
      square: 12, 20, 21, 30-32, 42-45, 56-61, 72-78, 90-97. Nagamochi's Theorem 2 proves
      `s(N) = m` exactly for `N` in `{m^2, m^2-1, m^2-2}`, which is why those are closed;
      these are the sizes further below, where the same argument gives a bound strictly
      under `m` and the grid is only the best anyone has recorded.
    exit: >-
      A statement, per size or per family, of whether the gap between Nagamochi's bound and
      the grid can be entered at all -- and if a construction is found, the same exact
      treatment the family constructions get. The honest expected outcome is that this is a
      hard open problem the catalogue has already absorbed, and establishing that with a
      measurement is worth more than attempting all 31.
    bead: think-7t9u
    depends_on: [BC-088]
    workflows: [research-pass]
    next_evidence: >-
      Narrowed by X-009 from 31 cases to one: n = 90 via Arslanov's decomposition, which
      reduces to H-049 -- whether 20 unit squares pack squeezably in a 4 by 6 rectangle.
      The staircase measurement (no k <= m - 2 case beaten anywhere in the catalogue to
      n = 324) absorbs the other 29 as hard-open; n = 61 stays parked in the proof lane
      under H-033. The s(m^2 - m) = m boundary is m < 11 (Cantrell, February 2025,
      retained in the Kingbird archive), not the m < 17 the frontier still quotes --
      filed as a record repair.
  - id: BC-092
    purpose: research
    owner_focus: insight
    instances: [5, 11, 29, 40]
    state: stopped
    priority: 2
    question: >-
      Does the contact structure give a search anything the pose alone does not -- can the
      assembly grammar generate candidates rather than only describe retained ones?
    hypotheses: []
    budget: >-
      about 240 minutes, W3, in slices of 30
    entry: >-
      `BC-019` closed with 17 certificates and 13 typed limitations over `n <= 30`, and
      named the missing grammar move rather than guessing it: a primitive for axis-aligned
      polyominoes that are not a bar, rectangle or corner L. `BC-024` established that the
      whole residue is axis-aligned -- every `other-polyomino` in the corpus has angle
      exactly 0 -- so extending the grammar is a question about axis-aligned pieces, not
      tilted assemblies. The contact machinery has so far only ever run backwards, from a
      retained pose to its structure.
    exit: >-
      Either a generative use of the grammar -- enumerate candidate contact structures at
      some `n` and ask which are realizable, which is the direction `contact_realization`
      already supports -- or a typed statement of why the enumeration does not close. This
      is the structural route to `BC-090`: a search informed by which contact graphs can
      exist is a different object from annealing on coordinates.
    bead: think-xdly
    depends_on: [BC-088]
    workflows: [research-pass, insight-iteration]
    next_evidence: >-
      X-009 answers the one-block-or-two question: one, owned by BC-090. The enumeration
      is priced out of reach as its own block (canonical orbits grow 1, 1, 7, 124,
      11,013 through size five with 9.3e9 raw orbit work already at n = 5, and the code
      caps scaffolds at size five by typed refusal), while the structural corpus's real
      value at a target n is proposer information -- which contact shapes and angle-class
      structures carry records -- inside BC-090's instrument.
---
# Agenda-009 — Hygiene First, Then Decide What the Machinery Is For

Three short commitments, then a decision.

`BC-085`, `BC-086` and `BC-087` are each here because they cost time in the session that
found them, and none is research.
A control suite with six members not firing, a pre-push floor that let three red pushes
through in a day, and a closing procedure that is a sequence to remember rather than a
tool.

`BC-088` is the pivot.
The research queue was written before most of the current machinery existed, and the
four blocks after it are `tentative` because deciding what to run is itself work with an
exit. Its entry carries the three measurements that bound the search: the lower bound is
what is weak rather than the packings being loose, 31 open sizes have never been beaten
past the grid, and ten have an incumbent that came from annealing and claims no
optimality.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
