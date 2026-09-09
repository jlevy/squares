# Agenda 034: reconciliation against the in-flight upstream branches, 2026-09-09

Retained read-only review by an Opus sub-agent for
[X-023](../../../../explorations/X-023-three-losses-and-a-new-atom.md), made from the
branch `claude/n-11-stronger-result-d730ds` after `origin/main` (`e8508598`) was merged.
No git state was changed; everything is `git show`, `git diff` and
`git merge-tree --write-tree` against remote refs.
The report is reproduced as delivered; the coordinator acted on its first recommendation
(X-022 became X-023 and `results/agenda-031/` became `results/agenda-032/`) before
committing it, and the same directory became `results/agenda-034/` later on 2026-09-09,
once PR 137 advanced and took `agenda-032` as well.

**Amended later on 2026-09-09, after PR 137 moved past the head this report read.**
`origin/codex/n11-ownership-continuation` has since registered its own `T-023` (a
five-dot four-owner branch exclusion), `H-136` through `H-142`, `agenda-032` and its
results directory, and `ideas.md` rows through 138. PR 137 wins every collision, so this
branch renumbered a second time: its result became `T-024`, and its three hypotheses,
its results directory and its idea rows each moved up one allocation.
The allocations this branch took are updated below; every column reporting an upstream
ref still reads as of `a1fc0306`.

**Amended a third time on 2026-09-09, before PR 145’s head was merged.** The same codex
line advanced through PR 142 and PR 145, taking `H-143` through `H-151`, `agenda-033`
and an agenda document to go with it, `session-114` through `session-122`, and
`ideas.md` rows through 147. This branch renumbered a third time, so every identifier it
owns reads at its final value throughout this document: hypotheses `H-152` through
`H-157`, results directory `results/agenda-034/`, session record `session-123`, and idea
rows 148 to 153. The upstream columns are unchanged and still read as of `a1fc0306`; the
dated reconciliation for PR 145 in this directory carries the third audit in full.

**Headline: every identifier this branch had allocated was already taken by
`origin/codex/n11-ownership-continuation` (PR 137, head `a1fc0306`, one commit ahead of
main).** X-022, agenda-031, H-135, BC-305 and session-111 are all live there with
different meanings. The two bodies of work are scientifically complementary, and one
result here (the exact ceiling family at 191/50) partly settles the question upstream’s
unrun pricing round was funded to explore.

## 1. Identifier collisions

| Identifier | Allocated upstream as | Our intended use | Resolution |
| --- | --- | --- | --- |
| `X-022` | `explorations/X-022-segment-ownership-continuation.md`, “Segment Ownership Constraints After the PR 127 Review”, dated 2026-09-08, `proposes: [H-135]` | the three-losses exploration, dated 2026-09-09 | **Renumbered to X-023.** Upstream is a day earlier, is the funded PR 127 continuation, and is already cited from its own agenda, ledger, `ideas.md` and SYNOPSIS. |
| `agenda-031` | `agendas/agenda-031-ownership-and-pricing.md` (status `active`, BC-305 to BC-308) plus `results/agenda-031/` holding 18 ownership files | this branch’s results directory | **Moved to `results/agenda-032/`**; `agenda-032` is taken when an agenda is registered. The two result sets shared a directory name but no filenames, so a merge would have silently mixed two unrelated agendas’ evidence. |
| `H-135` | `hypotheses/H-135-paired-full-support-pricing.md`, registered 2026-09-08, lane `proof`, open | “H-135 onward” | **Start at H-152.** |
| `BC-305` | agenda-031 BC-305 (ownership replay, in progress, bead `think-qfog`); BC-306 (ready, `think-7lp3`), BC-307 (tentative), BC-308 (blocked) | “BC-305 onward” | **Start at BC-309.** |
| `session-111` | `session-111-ownership-and-pricing.md` on the ownership branch **and** `session-111-font-startup-stability.md` on `origin/codex/math-startup-stability`, both dated 2026-09-08 | none yet | Not ours to fix; flagged: session-111 is double-allocated between two upstream branches. This branch takes session-112 onward. |
| `exp-134`, `exp-135` | `exp-134` preregistered by BC-306/H-135 (never launched); `exp-135` named as BC-307’s reserve | none yet | **Start at exp-136.** |
| `T-024` | free on all seven refs | the finer-net dilation bound | Renumbered with the amendment above; no collision at `T-024`. |
| next defect id | free: main and the ownership branch both stop at D-488 | none | No action. |
| idea row `131` | ownership adds idea 131 | none yet | **Start at 139.** |
| devtool filenames | `corner_ownership_audit.py`, `outer_pair_corner_audit.py`, `outer_segment_pair_screen.py`, `price_cutting_state_dual.py` | `decide_threshold_certificate.py`, `measure_net_refinement.py`, `expand_frozen_measure.py`, `polish_ceiling_family.py`, `independent_ceiling_reader.py` | No collision. |

`origin/codex/n11-structural-dot-plans` adds one commit past merged PR 121 (`c08a9016`):
a `SYNOPSIS.md` fix registering H-126 in the hypothesis-status table and bumping the
open-question count from twenty-three to twenty-four.
No new identifiers, no research content.

`origin/codex/n11-hybrid-overnight` allocates BC-260 to BC-283, session-092,
session-098, and updates X-018, H-118, H-120, VE-003/VE-004, all below main’s high-water
marks and inside the gap main already left; nothing collides.

## 2. Overlapping and reconcilable ideas

| Upstream result or idea | Related direction here | Action | How |
| --- | --- | --- | --- |
| `support_entries(..., support_cap: int \| None)` in `sqpack/fractional/cutting.py`: `None` retains every positive dual row | X-023’s D6/D16, full-dual pricing | **Incorporate** | Exactly the instrument change D16 asks for, already written and controlled upstream; this branch does not touch `cutting.py`, so it lands cleanly. |
| H-135 / BC-306 paired pricing (open, never run): price the transported BC-232 state, compare the first 32 positive dual rows against the full positive support at the same witness | spike E’s “does full-dual pricing move the 3.82 value” | **Reconcile, and report the ceiling to that agenda** | The BC-232 leg-01 state H-135 prices *is* the 3.82 state (side `191/50`, shrink `9977/10000`, 181 directions, 12,761 sites, 9,868 rows, best depth-one family `10.384212408377214`). The ceiling family at `191/50` (88 placements, total exactly 11, exact maximum depth 1 over 20,376 vertices, SHA-256 `95cf0647…6427`) proves that no D4-symmetric point-atom measure of mass below eleven covers there, so more rows or sites at 3.82 cannot drop the restricted value below eleven. H-135 stays well posed as a pointwise mechanism test; its motivating hope is closed. |
| The 3.82 plateau | the ceiling result; H-133 | **Cite, one direction only** | The ownership branch says nothing about the plateau, depth-one families, finer nets, threshold or clique cuts (zero hits for `3.82`, `191/50`, `plateau`, `clique`, `finer net`, `depth-one` in its new files). |
| Ownership capacities at `q = 96/25`, `δ = 3/500` (proved, independently reviewed): outer middle-row segments have sharp owner capacity two; the other eight segments capacity four, owner centres within `1/√2 + 7/125 < 4/5` of the midpoint | X-023’s D10 | **Cite** | These sharpen the H-134 eleven-mark ownership lemma; they change no measured headroom, and upstream states they do not compose into a global exclusion at `96/25`. |
| Separator and signed-angle exclusions (proved): for two owners of one outer segment, every weak unit separating normal obeys `v_y ≥ 1/280` and `56 v_y ≥ 62|v_x| − 1`; pairs with both half-tangents in `[1997/6000, √2 − 1]` (about `36.7°` to `45°`) are excluded with exact margin `501/1000000` | the angle reading of the 3.82 dual | **Cite as a constraint on the integral side** | The excluded band is `36.7°` to `45°`; the fractional dual’s tilted mass sits near `29°`, so these exclusions do not touch the structures threshold atoms target. |
| Two exact four-square counterexamples: outer-pair ownership coexists with two distinct adjacent corner owners; four diamond squares give two owners for each of two adjacent corner-pair mark sets, marks strictly inside their canonical cores | the disposition of the contributed note’s §7 | **Incorporate into that disposition** | They close the two shortcuts a conditioned case split would most naturally try, which is the reason §7 stays reserved. |
| The one fixed-pattern exclusion (exact): with the lower outer owners fixed at the capacity-witness axis squares, two further squares owning the forced bottom marks would both contain `(48/25, 2336/3175)` | — | **Cite only** | Scoped to that fixed pattern. |
| hybrid-overnight BC-282 residual skeleton: the ten-square domain reduces to a seven-parameter skeleton; the proposed translation fence is not target-ready | D10 and the note-§7 disposition | **Cite in D10** | The coupled route has a complete domain and no admission argument; that is why D10 stays reserved. |
| hybrid-overnight guarded central-band capacity (accepted by independent audit): complement capacity at most four, excluding seven residual full squares; BC-279’s seven-core target unresolved | the integrality-gap framing and D7 | **Cite, not merge** | Their capacity theorem is an integral restriction; threshold atoms are the fractional-side cut with the same intent. Neither has produced a bound. |
| hybrid-overnight signed release exclusions (accepted): both slide signs excluded on `t ∈ [2/5, 1/2]` and on the closed axis neighbourhoods | — | **Cite once** | Confirms that case splits so far bought no headroom. |
| hybrid-overnight BC-283 strategy review (`review-2026-09-07-upstream-research-reconciliation.md`, unmerged): organise around a complete no-fit proof at 3.84 | the whole framing of X-023 | **Cite as the prior recommendation being answered** | — |

## 3. Next free number per family across the seven refs

| Family | main | this branch | ownership | dot-plans | hybrid | pr-stack-ci | math-startup | **Next free** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `X-0xx` | X-021 | X-023 | X-022 | X-019 | X-018 | X-018 | — | **X-024** |
| `agenda-0xx` | 030 | (034 reserved) | 031 | 029 | 028 | 028 | 030 | **agenda-035 after 034** |
| `H-1xx` | H-134 | H-134 | H-135 | H-126 | H-124 | H-124 | H-134 | **H-152** |
| `BC-3xx` | BC-304 | BC-304 | BC-308 | BC-290 | BC-283 | BC-283 | BC-304 | **BC-309** |
| `session-1xx` | 110 | 110 | 111 | 099 | 098 | 106 | 111 | **session-112** |
| `exp-1xx` | exp-133 | exp-133 | exp-135 | exp-130 | exp-129 | exp-129 | exp-133 | **exp-136** |
| `T-0xx` | T-022 | T-022 | T-022 | T-022 | T-022 | T-022 | T-022 | **T-024** |
| defects | D-488 | D-488 | D-488 | D-480 | D-480 | D-488 | D-488 | the one after D-488 |
| `ideas.md` row | 130 | 130 | 131 | — | 118 | 118 | — | **139** |

## 4. Textual merge exposure

`git merge-tree --write-tree HEAD <branch>`, no merge performed:
`n11-ownership-continuation` clean; `n11-structural-dot-plans` one conflict
(`SYNOPSIS.md`); `n11-hybrid-overnight` nine conflicts in shared registries and
generated views; `review-pr-stack-ci-0dorfw` eight; `math-startup-stability` clean.
None of `threshold.py`, the new devtools, `test_fractional_threshold.py`, or the
agenda-034 results is touched by any upstream branch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
