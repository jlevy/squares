---
type: is
id: is-01m2m2zmky0p8gw5m4zctfnfex
title: "Workbench motion: gentle, smooth, chunking, and a setting for the append-to-resize delay"
kind: task
status: open
priority: 1
version: 7
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
child_order_hints:
  - is-01m2nhc3zsdr07t84vxt8xy3qf
  - is-01m2nhcg6g9a6k67dsz5n7363v
  - is-01m2nhycvy9kh5cht5e3a0dn08
  - is-01m2nk6ptyczkzdneyv6k2757w
created_at: 2026-09-16T03:08:21.501Z
updated_at: 2026-09-16T17:11:04.797Z
---
Owner feedback on the published page, 2026-09-15:

> Seems to be like the rigidity is too high or something. Also, I'd like to have a little more control over when the red new square is added versus when the page shrinks. There should be a little bit more of a delay there, and we should have a setting for that.

> They were a little more gentle in their motions before, and now they're jumping around. When we make them fully rigid, it's even more extreme, but I'd like to see it more gentle, with some repulsion, some attraction, and generally pushing the blocks to connect with each other (so that we are closer to the chunks that are needed for the final optimal packings).

> softer is good but we also like to see a good amount of jiggle due to the strong annealing style motion but still motions should be smooth, not jumping all over every frame

**Measured on the published page at `21a68102`** (n = 17, over the moving span, excluding the appended square; "reversals" is the fraction of frames whose step reverses against the previous step, the ringing signature):

| law | reversals | mean step/frame | largest step/frame |
| --- | ---: | ---: | ---: |
| shipped `{rigidity 0.35, repulsion 950, attraction 80, range 0.15}` | 0.066 | 0.0166 | 0.4551 |
| `{0.35, 400, 80, 0.15}` | 0.064 | 0.0175 | 0.4885 |
| `{0.35, 250, 160, 0.3}` | 0.087 | 0.0188 | 0.5028 |
| `rigid` preset `{0.01, 4000, 0, 0}` | 0.367 | 0.2078 | 1.0645 |

Three findings:
- **Stiffness is what makes it spastic.** The `rigid` preset reverses direction in 37% of frames and moves a whole square width in one: explicit integration at k = 4000 with dt = 1/120 s is far past stable, and the walls at 2500 are marginal. A preset that shakes the page apart is a defect, not a setting.
- **The clamp turns ringing into teleporting.** `PHYS.maxSpeed` is 40 units per move, which at the shipped beat is 0.463 units per frame -- the 0.4551 measured, nearly half a square's width.
- **The shake level is not the cause.** Levels 3, 5, 6, 7 and 9 all show the same spikes.

**Targets:** reversals at or below 0.03 (0.05 for the `rigid` preset), largest step at or below 0.1 units (0.15 for `rigid`), mean step within about 20% of today's 0.017 so the jiggle stays. The lever is stability first -- physics substeps and contact damping -- then the law's shape, the clamps and `PHYS.jiggleHz` (2.5 to 4 cycles per move is 5 to 8 Hz at the shipped beat: a buzz rather than a swirl). Attraction should gather neighbours into chunks; measure contacting pairs and mean neighbour gap, do not eyeball it.

**Also in scope:** the owner's timing setting. Today `BOUND_CLEAR` 0.3 of the dwell, `BOUND_GROW` 0.2 and `BOUND_FADE` 0.12 of the move, `BOX_FIRST` holding every other motion back, and `PHYS.appear` 0.15. The page needs a control in THE STEP ANIMATION panel for the gap between the new square appearing and the container's resize, defaulting longer than today, reaching the API like `dwell`, `move`, `correct` and `settle`.

**State:** branch `claude/workbench-motion-and-step-timing` exists off `main` at `21a68102` with the measurement script at `attic/motion-measure.js`; no implementation yet. The delegated session was cut off by a rate limit before its first commit.

Changing these defaults moves the physics again: X-034 and H-211 already say no shake level has been measured under the current ones, and this needs a dated note when it lands.

## Notes

2026-09-16: attic/motion-measure.js lives in a gitignored directory, so it dies with the worktree. When this work resumes, commit the measurement as a probe file under the package probes directory; OR-1 requires a reusable tool.

2026-09-16 current-main diagnosis at a4f801e8: Not fixed. PRs #180 and #181 did not change the simulation. Pack uses force-law substeps, but Animate buildTrajectory does not. Current-corpus reproduction: 16 to 17 rigid reaches 0.3699 square widths per stored step, 0.7399 second difference, 945 reversals and 0.6484 penetration; the helper-required two finer steps reduce this to 0.1617, 0.0754, zero reversals and 0.0558. 89 to 90 falls from 7,832 reversals to 3. The cap-to-cap pattern identifies stiff-spring ringing plus maxSpeed, not missing renderer interpolation.

Two mergeable children own the fix: think-o4wo stabilizes Animate and adds continuity budgets; think-5tyy makes the controls truthful and setting changes continuous. The architectural constraint/projection follow-up remains think-r2qd.
