# Review: The Verification and Confirmation Rungs of Register Entries T-120 to T-146

**Date:** 11 October 2026. **Verdict: every declared rung is supported, none is
over-rated and none under-rated.** For all 27 entries the rungs `devtools.check_results`
derives from the cited evidence and reviews equal the declared ones: ten stand at
`V0`/`C0` and seventeen at `V3`/`C3`. Every predicate under each `V3`/`C3` holds in the
retained files: the certificate path resolves, the packet’s custody check passes, the
replay command and a passing receipt are retained, the confirming origin and the
recorded code relation agree with the programs that decided, a control path exists, and
each review is mapped and accepts the claim.
Four upper-bound receipts (T-131, T-137, T-139, T-141) were replayed here again and
reproduce job for job, the third exact route decided 36 certificates of seven entries
with every control at its required outcome, and the retained receipts of T-133 and T-145
were judged again to byte-identical outputs.
No rung moves with compute alone: every `V3`/`C3` entry’s next rung is `V4`/`C4`, which
waits on a retained human oversight record, and every `V0`/`C0` entry’s next rung is a
replay priced in CPU-hours, an acquisition or a Lean build nobody has priced, or an
optional replay that moves no bound.
Nine findings are recorded.
None blocks a current rung; RR-1 must be settled before any `V4`/`C4` promotion.

This review was written by an AI agent (Claude, the operations tier, at the extra-high
reasoning setting its dispatch named), lane R1 of the 2026-10-11 intake pass under
`think-18b8` (epic `think-mq0k`), prompted by the pass’s coordinator separately from the
import lanes and from every review it reads, with no shared context.
The owner asked for a review of the verification levels on recent items.
Its relation to the results is `project`. It reviews the record’s ratings, not any
result’s mathematics, so it is no adversarial review of a result and no entry should
list it in `reviews`. It moves no rung, writes no register row and adopts no house; the
proposed record changes are listed at the end for the records lane.

## Claims Covered

| Entries | Kind | Counts | Source |
| --- | --- | --- | --- |
| T-120 to T-123 | upper bound, a reported exact algebraic side | 102, 106, 152, 177 | Evan Daniel, issue 419 |
| T-124 | restricted optimality, reported local minima | 178 configurations | Evan Daniel, issue 420 |
| T-125, T-126 | upper bound | 25 counts; 51 over $\mathbb{Q}(\sqrt2)$ | Ryan Xu, issue 432 |
| T-127 | upper bound | 17 counts | Siddharth Gupta’s refinements, issue 438 |
| T-128, T-130, T-134, T-140 | upper bound | 8, 5, 6 and 6 counts | Francisco Couzo, issues 451, 460, 476, 488 |
| T-129 | upper bound, historical certificates | 105, 130, 292 | Evan Daniel, issue 375 |
| T-131, T-139, T-141, T-146 | upper bound | 132; 126; 132 and 308; 15 counts | Evan Daniel, issues 465 and 489, and two releases with no issue |
| T-132, T-142, T-143 | lower bound, reported | 29, 28, 30 | wand125, issue 446 and two releases |
| T-133, T-145 | lower bound | 40 | Guzhou0806, issue 485 |
| T-135 | upper bound | 308 | Kevin Fang, issue 484 |
| T-136 | upper bound | 17 counts | Nate Chaoweeraprasit (SQUISH), issue 481 |
| T-137 | upper bound | 70 | Eric Deleeuw, issue 483 |
| T-138 | upper bound | 16 counts | Mishapolk, issue 470 |
| T-144 | lower bound, reported | 122 to 126 | wand125 |

**Read in full.** [epistemics.md](../../../epistemics.md) on Verification, Confirmation,
Which Code Confirmed It, Review Records, Status and Results by Others;
`derive_verification`, `derive_confirmation`, `_machine_proof_shaped`,
`adversarially_reviewed`, `overseen`, `confirmation_code` and the per-entry checks of
`devtools/check_results.py`; `devtools/check_certificate_citations.py` and its deferrals
file; the 27 register entries and their 48 evidence entries; the verifier registry rows
they name; the eleven reviews they cite, the two final reviews of 11 October in full and
the 10 October imports review whose shape this one follows; the beads `think-fvz4`,
`think-r333`, `think-i85v`, `think-nd7g` and `think-ux1v`; the README of the T-120 to
T-124 packet, and the replay sections of the Ry Xu packet’s.

## How a Rung Is Derived Here

`derive_verification` and `derive_confirmation` read the cited evidence entries and the
entry’s `reviews`. A *machine-shaped* entry is exact-algebraic, interval-certified or
kernel-checked with a non-empty `certificate`, a non-empty `replay` and
`replay_status: passed`; `V3` needs one of any origin, `C3` one of origin
`replayed-here`, `audited-here` or `independently-external`. `V4`/`C4` add two
adversarial AI reviews whose reviewer strings differ, the latest-dated review accepting,
and a human oversight record that checked the trust boundary, the certificate’s meaning
and the AI findings.
A `C3` entry must also name a control path that exists, and every review must be a
non-superseded review in the document map that covers the entry.

Two of those predicates are weaker in code than in words, and this review checked them
by hand. The `certificate` is held to be a non-empty string, not a path that resolves
(RR-2), and two reviews count as distinct when their `reviewer` strings differ (RR-1).

## Entry by Entry

“Declared” is the register’s `V`/`C`; “derived” is what `check_results` derives from the
retained evidence and reviews, run on this branch.
“Supported” is this review’s reading of the retained files.
Prices are from the register, the beads and the receipts; “quick” means minutes on this
host.

| Entry | Declared, derived | What carries the rung | Supported | Next rung, and its price |
| --- | --- | --- | --- | --- |
| T-120 | `V0`/`C0`, same | a report, `replay_status: not-attempted` | `V0`/`C0` | `V3`/`C3`: acquire the `minpoly/data/` geometry the packet leaves out, check root identity and feasibility exactly; **unpriced**, with PR #403 (open). Superseded at 102 by T-125’s 10.6058…, so it moves no case bound (RR-7) |
| T-121, T-122, T-123 | `V0`/`C0`, same | reports | `V0`/`C0` | as T-120; each $\alpha_n$ lies 1.1 to 1.4 × 10⁻¹⁹ below the case’s rational ceiling of the same configuration, so the gain is the exact value, not a smaller side |
| T-124 | `V0`/`C0`, same | a report | `V0`/`C0` | `V3`/`C3`: audit the theorem and configuration bindings and build the pinned Lean tree; **long, unpriced** (no toolchain or build time is on record) |
| T-125 | `V3`/`C3`, same | `E-ryxu-432-rational-feasibility`: 25 positives and 50 controls admitted; one review (GPT-6 Astra) | `V3`/`C3` | `V4`/`C4`: a second adversarial AI review by a distinct reviewer (a Claude lane would be another model family; its replay, `ryxu_arrangement_reports check --replay`, took 330 s at two workers) **and a human oversight record** |
| T-126 | `V3`/`C3`, same | `E-ryxu-432-radical-n51-feasibility`: 3 jobs admitted; one review | `V3`/`C3` | as T-125; replay 19 s |
| T-127 | `V3`/`C3`, same | `E-gupta-438-exact-feasibility`: 17 positives and 34 controls admitted; one review | `V3`/`C3` | as T-125; replay 256 s at two workers, but its command overwrites the retained receipt (RR-4) |
| T-128 | `V3`/`C3`, same | `E-couzo-451-exact-feasibility`, `E-evand-465-record-hunt-exact-feasibility`; two reviews | `V3`/`C3` | `V4`/`C4`: **a human oversight record**, which must also decide RR-1 |
| T-129 | `V0`/`C0`, same | reports | `V0`/`C0` | `V3`/`C3`: **quick** compute (under a CPU-minute, F2-4 of the final upper-bound review) but needs an importer declaration and a retained receipt; superseded at all three counts, so optional |
| T-130 | `V3`/`C3`, same | `E-couzo-460-followup-exact-feasibility`; two reviews | `V3`/`C3` | as T-128 |
| T-131 | `V3`/`C3`, same | `E-evand-465-record-hunt-exact-feasibility`; two reviews | `V3`/`C3` | as T-128 |
| T-132 | `V0`/`C0`, same | a report; an eight-direction sample receipt | `V0`/`C0` | `V3`/`C3`: **long**, 4.3 to 5.5 CPU-hours, budget set by the owner; waits on unmerged tooling, the regularization stack and an owner question (RR-6) |
| T-133 | `V3`/`C3`, same | the 401-direction sqverify-fast replay (reproduced with the producer’s code) and the finite audit (independently re-implemented); two reviews | `V3`/`C3` | `V4`/`C4`: **a human oversight record**; superseded at 40 by T-145 (RR-5) |
| T-134 to T-141 | `V3`/`C3`, same | each import’s `…-exact-feasibility` entry; two reviews each | `V3`/`C3` | as T-128 |
| T-142 | `V0`/`C0`, same | a report; a sample receipt | `V0`/`C0` | `V3`/`C3`: **long**, 3.3 to 4.5 CPU-hours; its whole-net control is held on an owner decision (RR-6) |
| T-143 | `V0`/`C0`, same | a report; a sample receipt | `V0`/`C0` | `V3`/`C3`: **long**, 4.5 to 6.1 CPU-hours; as T-132 |
| T-144 | `V0`/`C0`, same | a report; a two-angle sample receipt | `V0`/`C0` | `V3`/`C3`: **long**, 11.2 CPU-hours (14.6 by the 11 October smoke run; the author’s own replay suggests up to 23) |
| T-145 | `V3`/`C3`, same | the two kernels’ replay (reproduced with the producer’s code), the finite audit and the crate’s axis sweep (independently re-implemented); two reviews | `V3`/`C3` | as T-133, and it holds the case’s lower bounds |
| T-146 | `V3`/`C3`, same | `E-evand-regularized-exact-feasibility`; two reviews | `V3`/`C3` | as T-128 |

**Under-rating.** None found.
The `V0`/`C0` entries hold sample receipts (T-132, T-142, T-143, T-144) or nothing
replayed here (T-120 to T-124, T-129); a sample is not a replay, and no qualifying read
is recorded on any of their evidence, so neither `C1` nor `C3` is earned.
The final upper-bound review’s own checker accepted T-129’s three certificates (F2-4),
but kept no receipt, so that run supports no rung.

## The Predicates, Checked Against the Retained Files

**Certificates.** Every `certificate` the 48 evidence entries name resolves: 41 from the
repository root, and the seven of T-133 and T-145, which name wand125’s `rect_n40_L67`
density by a path under `packing/` (RR-2). Evidence entries carry no digest; custody is
the packet’s. `python -m devtools.acquire_source --check PACKET` printed
`PACKET_MATCHES_ITS_CONTRACT` for all seventeen declared packets in scope (the T-120 to
T-124, T-127, T-128, T-129 (two), T-131, T-133, T-134 to T-141, T-145 and T-146
packets). Of the six packets without a declaration, two were admitted by their own
modules: `ryxu_arrangement_reports check` (25 positives, 50 controls) and
`ryxu_radical_n51 check` (exit 0) for T-125 and T-126, and
`couzo_followup_reports check-packet` (five certificates rebuilt to their pinned blobs)
and `check` (5 certificates, 15 jobs) for T-130. The density packet of T-133 and T-145
(`wand125-rectangle-certificates-2026-10-01`) is bound by their audits’ `check`, which
holds the retained density to the release’s candidate digest and the input derived from
it to the one the release receipts name (run below); the three wand125 packets of T-132
and T-142 to T-144 hold reported facts and sample receipts, and their certificates are
kept outside Git.

**Replay commands, receipts, status.** Every `V3`/`C3` entry cites a confirming entry
with a replay command and `replay_status: passed`, and its receipt is retained:
`receipts/exact-certification.json.xz` in each upper-bound packet (seventeen shards at
T-136), and the 401-direction receipt, run record, finite audit and replay check at
T-133 and the slab, axis, crate and control receipts at T-145.
`gupta_refinement_reports check` admitted T-127’s 17 positives and 34 controls,
`couzo_refinement_reports check` T-128’s 8 certificates and 24 jobs.

**Origin and code relation.** Every confirming entry is `replayed-here` or
`audited-here`. The deciding programs agree with each recorded relation.
At T-128, T-130, T-134 and T-140 one maintained route, `V-sqpack-verify`, is the
verifier the source ran (RD-4, RI-4, RL-5), and the entry’s `independent-implementation`
rests on `V-check-rational-witness-independent` and the third route, which share none of
the producer’s code; the limitations say so.
At Evan Daniel’s entries (T-131, T-139, T-141, T-146) `V-evand-exact-certificates` is
this repository’s parser for his format, `role: premises`, not his code.
T-133’s and T-145’s nodal and kernel replays are `same-implementation`, as their
compositions say, and the derived attribute for both is *reproduced with the producer’s
code*; every other `V3`/`C3` entry derives *independently re-implemented*.

**Controls.** Every `V3`/`C3` entry names control paths that exist.
At T-125 and T-127 they include the receipt that holds the control jobs; at the eleven
later upper-bound entries they are test files, and the sharp third-route controls the
reviews rely on are retained nowhere (RR-3).

**Reviews.** All eleven cited reviews are mapped as retained reviews, accept, and cover
the entries that cite them; `check_results` passed (146 results; 11 recorded, 2
reviewed, 132 confirmed, 1 incomplete, register-wide).

## Spot Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) on this worktree at
`3a5a91a90` (`main`), one process at a time, on a four-core host that four other lanes
held at a load average of 4 to 15. Each wall includes the interpreter’s start.

| Command (`python -m devtools.…`) | Entry | What it decides | Outcome | Wall |
| --- | --- | --- | --- | --- |
| `upper_bound_reports ebdeleeuw-n70-refinement-2026-10-10 check --replay` | T-137 | 3 jobs, both maintained routes | all equal to the retained rows | 12.8 s |
| `upper_bound_reports evand-trio126-2026-10-09 check --replay` | T-139 | 3 jobs | all equal | 44.1 s |
| `evand_hunt_reports check --replay` | T-131 (and T-128’s n155 equal side) | 6 jobs | all equal | 96.5 s |
| `upper_bound_reports evand-record-hunt3-2026-10-10 check --replay` | T-141 | 15 jobs, five counts (132, 305, 308, 343, 344) | all equal | 1,319 s, at a load average of 9 to 15 (308.7 s alone on 10 October) |
| `… check-claims`, for each of the four | the same | each frozen comparison rebuilt | all rebuilt equal | 1.2 to 6.6 s |
| `upper_bound_reports PACKET check` and `check-claims`, for the other six importer packets | T-134, T-135, T-136, T-138, T-140, T-146 | each receipt admitted structurally, each frozen comparison rebuilt | 91 certificates and 273 jobs admitted; all rebuilt equal | about 2 s each |
| `check_half_angle_area decide --workers 1` | T-128, T-130, T-131 | 15 certificates, 90 controls | no problem; 213,064 pairs, every control at its required outcome | 69.0 s |
| `check_half_angle_area decide-imports --workers 1 --imports '#483' trio126 '#489' regularized` | T-137, T-139, T-141, T-146 | 21 certificates (#489’s 343 and 344 among them), 126 controls, every cross-check and T-146’s arrangement measurements | no problem; 543,091 pairs (9,146 clipped), every control at its required outcome | 574.3 s |
| `check_half_angle_area decide-imports --workers 1 --imports '#483' --upstream ebdeleeuw-n70-refinement-2026-10-10 DIR` | T-137 | the derived fact against `certificate.json` fetched from `raw.githubusercontent.com` at `24221d5`, whose SHA-256 (`eeebf55c…`) is the packet’s pin | the fact is the packing the pinned file states; its printed side checked | 7.3 s |
| `audit_clipped_corner_transfer check`, then `check-replay --rank` | T-133 | the finite steps again; the retained 401-direction and control receipts judged | `FINITE_STEPS_HOLD`, `REPLAY_HOLDS`; both outputs byte-identical to `receipts/finite-audit.json` and `receipts/replay-check.json` | 3.5 s; 61.0 s |
| `audit_continuous_pose check`, then `check-replay` | T-145 | the same for the continuous-pose packet | `FINITE_STEPS_HOLD`, `REPLAY_HOLDS`; both byte-identical to the packet’s receipts | 3.9 s; 1.2 s |

T-146’s kernel replay (45 jobs, 476 s alone on 10 October and 535.5 s beside two other
runs on 11 October, both recorded in its evidence) was not run: at T-141’s wall under
this load it would have taken about half an hour beside the four import lanes, and the
third route above decided all fifteen of its certificates.
Without `--rank`, T-133’s `check-replay` omits the control-point check and its output
differs from the receipt; the README’s command has `--rank`, as the evidence’s replay
text implies.

## Next Rungs and Their Prices

**Waiting on a human record (seventeen entries).** Every `V3`/`C3` entry’s next rung is
`V4`/`C4`, and each needs a retained human oversight record (`kind: oversight`,
`checked` including `trust-boundary`, `certificate-meaning` and `ai-findings`). T-128,
T-130, T-131, T-133 to T-141, T-145 and T-146 already hold two accepted adversarial AI
reviews whose reviewer strings differ; T-125, T-126 and T-127 hold one (GPT-6 Astra) and
also need a second AI review by a distinct reviewer, an agent lane whose replays cost
minutes. No compute closes any of these.

**Long (CPU-hours), budgeted and blocked.** T-132, T-142, T-143 and T-144 need complete
replays: 4.3, 3.3, 4.5 and 11.2 CPU-hours at the central estimates, 23.3 in all, 39.1 at
the register’s upper ends.
The owner set the budget on 11 October and then put the regularization stack
(`think-ux1v`) ahead of it; the tooling the commands need is on the unmerged branch
`claude/wand125-confirmations-2026-10-11` (`44eb6a017`), and two owner questions are
open (RR-6).

**Unpriced.** T-120 to T-123 need the source’s `minpoly/data/` geometry, which the
packet leaves out, and an exact root-identity check, with PR #403; T-124 needs a build
of the pinned Lean tree.
No one has priced either.

**Quick but of no rung value.** T-129’s replay (under a minute; the entry is superseded
at all three counts).
And three quick improvements that move no rung: retaining the third route’s controls
(RR-3), a replay mode for T-127 (RR-4), and resolving certificate paths in the checker
(RR-2).

## Adoption per Count

Every `V3`/`C3` upper-bound entry from T-128 on states a side below the case’s verified
ceiling at some count, and no case record cites it: the case records wait for PR #403,
which rewrites all of them and is still open (last updated 2026-10-11 02:46 UTC), as the
coordinator recorded on `think-fvz4`. `devtools.check_standing --list --cases` reads 39
counts where such an entry is below the ceiling; the table names the smallest exact side
at each, which is the house the reviews recommend, and every other entry below the
ceiling there. Each house’s confirming evidence is excused from
`check_certificate_citations` by a deferral in
`packing/devtools/certificate-citation-deferrals.yaml` (bead `think-fvz4`, blocked on
jlevy/squares#403). A deferral fails once the evidence register’s `last_reviewed` is
more than 30 days after it was recorded: **those recorded on 2026-10-10 fail from
2026-11-10, and T-146’s, recorded on 2026-10-11, from 2026-11-11.**

| n | Case’s verified ceiling, as printed and cut | House to adopt, its side rounded up | Below the ceiling by | Its deferral, recorded, fails from | Also below the ceiling |
| --- | --- | --- | --- | --- | --- |
| 70 | 8.8809603717088810 | T-146, 8.8809603715555796 | 1.53e-10 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-137 |
| 84 | 9.6980520605096981 | T-130, 9.6979347990149214 | 1.17e-04 | `E-couzo-460-followup-exact-feasibility`, 2026-10-10, 2026-11-10 | T-138 |
| 86 | 9.8205657300098206 | T-130, 9.8205354074967423 | 3.03e-05 | `E-couzo-460-followup-exact-feasibility`, 2026-10-10, 2026-11-10 | T-138 |
| 102 | 10.605828696510605 | T-146, 10.6058286964315784 | 7.90e-11 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | none |
| 103 | 10.679232047510679 | T-146, 10.6792320473613065 | 1.49e-10 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-138 |
| 105 | 10.790676575410790 | T-130, 10.7893037837481589 | 1.37e-03 | `E-couzo-460-followup-exact-feasibility`, 2026-10-10, 2026-11-10 | T-138, T-128 |
| 108 | 10.904824785110904 | T-128, 10.9048210123203565 | 3.77e-06 | `E-couzo-451-exact-feasibility`, 2026-10-10, 2026-11-10; `E-evand-465-record-hunt-exact-feasibility`, 2026-10-10, 2026-11-10 | T-138 |
| 123 | 11.591378145711591 | T-146, 11.5913781454976982 | 2.14e-10 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | none |
| 126 | 11.742640687211742 | T-139, 11.7426406871192852 | 9.25e-11 | `E-evand-trio126-exact-feasibility`, 2026-10-10, 2026-11-10 | none |
| 127 | 11.810936647511811 | T-128, 11.8108787875891799 | 5.79e-05 | `E-couzo-451-exact-feasibility`, 2026-10-10, 2026-11-10; `E-evand-465-record-hunt-exact-feasibility`, 2026-10-10, 2026-11-10 | T-138 |
| 129 | 11.872029849211872 | T-146, 11.8720298490811800 | 1.31e-10 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | none |
| 131 | 11.951150044911951 | T-136, 11.9496595880358604 | 1.49e-03 | `E-squish-481-exact-feasibility`, 2026-10-10, 2026-11-10 | T-128, T-138 |
| 132 | 11.991327887691501 | T-141, 11.9856801988458089 | 5.65e-03 | `E-evand-489-exact-feasibility`, 2026-10-10, 2026-11-10 | T-140, T-134, T-138, T-131 |
| 146 | 12.583782277512583 | T-146, 12.5837822774150769 | 9.75e-11 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | none |
| 153 | 12.879679373329314 | T-146, 12.8720298490811800 | 7.65e-03 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-136 |
| 154 | 12.926562245852347 | T-136, 12.9230702023011408 | 3.49e-03 | `E-squish-481-exact-feasibility`, 2026-10-10, 2026-11-10 | none |
| 155 | 12.952503202604512 | T-128, 12.9524989440140074 | 4.26e-06 | `E-couzo-451-exact-feasibility`, 2026-10-10, 2026-11-10; `E-evand-465-record-hunt-exact-feasibility`, 2026-10-10, 2026-11-10 | none |
| 175 | 13.768899276613768 | T-140, 13.7671207246923133 | 1.78e-03 | `E-couzo-488-exact-feasibility`, 2026-10-10, 2026-11-10 | T-130, T-138 |
| 180 | 13.917653417450184 | T-128, 13.9169935224778325 | 6.60e-04 | `E-couzo-451-exact-feasibility`, 2026-10-10, 2026-11-10; `E-evand-465-record-hunt-exact-feasibility`, 2026-10-10, 2026-11-10 | T-138 |
| 207 | 14.887992258302657 | T-136, 14.8855063088416777 | 2.49e-03 | `E-squish-481-exact-feasibility`, 2026-10-10, 2026-11-10 | none |
| 209 | 14.949617952200398 | T-140, 14.9462232264464511 | 3.39e-03 | `E-couzo-488-exact-feasibility`, 2026-10-10, 2026-11-10 | T-136 |
| 228 | 15.604602454546056 | T-128, 15.6046014757296743 | 9.79e-07 | `E-couzo-451-exact-feasibility`, 2026-10-10, 2026-11-10; `E-evand-465-record-hunt-exact-feasibility`, 2026-10-10, 2026-11-10 | none |
| 232 | 15.77817459305203 | T-136, 15.7674283499418417 | 1.07e-02 | `E-squish-481-exact-feasibility`, 2026-10-10, 2026-11-10 | none |
| 236 | 15.867800839419916 | T-146, 15.8639557471592675 | 3.85e-03 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-136 |
| 237 | 15.903676235189138 | T-140, 15.9029496076778317 | 7.27e-04 | `E-couzo-488-exact-feasibility`, 2026-10-10, 2026-11-10 | T-136, T-134 |
| 258 | 16.563448002139154 | T-146, 16.5634480021337894 | 5.36e-12 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-138 |
| 259 | 16.602568490493364 | T-136, 16.5913781454976982 | 1.12e-02 | `E-squish-481-exact-feasibility`, 2026-10-10, 2026-11-10 | none |
| 263 | 16.740419679538776 | T-146, 16.7331660078993790 | 7.25e-03 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-136, T-134 |
| 267 | 16.838831961116838 | T-134, 16.8388152699482623 | 1.67e-05 | `E-couzo-476-exact-feasibility`, 2026-10-10, 2026-11-10 | T-138 |
| 269 | 16.905967058583840 | T-146, 16.9015135821891322 | 4.45e-03 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-136 |
| 270 | 16.937807228446029 | T-140, 16.9297753535413596 | 8.03e-03 | `E-couzo-488-exact-feasibility`, 2026-10-10, 2026-11-10 | T-136, T-134, T-130, T-138 |
| 292 | 17.597249391156465 | T-146, 17.5913781454976982 | 5.87e-03 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-136 |
| 295 | 17.704232791517704 | T-146, 17.7042327907360304 | 7.82e-10 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | none |
| 302 | 17.881306218095808 | T-146, 17.8720298490811800 | 9.28e-03 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-136, T-138 |
| 303 | 17.920312372920349 | T-146, 17.9130654627385324 | 7.25e-03 | `E-evand-regularized-exact-feasibility`, 2026-10-11, 2026-11-11 | T-136, T-134, T-138 |
| 305 | 17.952959459015527 | T-140, 17.9511397722069976 | 1.82e-03 | `E-couzo-488-exact-feasibility`, 2026-10-10, 2026-11-10 | T-136 |
| 306 | 17.963438139764002 | T-128, 17.9634337174914258 | 4.42e-06 | `E-couzo-451-exact-feasibility`, 2026-10-10, 2026-11-10; `E-evand-465-record-hunt-exact-feasibility`, 2026-10-10, 2026-11-10 | T-138 |
| 307 | 17.981030548633310 | T-136, 17.9808627840546911 | 1.68e-04 | `E-squish-481-exact-feasibility`, 2026-10-10, 2026-11-10 | none |
| 308 | 18 | T-141, 17.9982698795262559 | 1.73e-03 | `E-evand-489-exact-feasibility`, 2026-10-10, 2026-11-10 | T-135 |

At every count the house’s side was compared exactly with the others’: the least margins
are $2.2 \times 10^{-17}$ (T-146 below T-136 at 302) and $3.3 \times 10^{-16}$ (at 236),
each between T-146’s certificate and the T-136 packing its `regularizations` say it
regularizes there.
Every house recommendation in the entries’ `next_rung` agrees with the
table, though T-136’s names only some of its counts (RR-9). Seven of the eight houses
wait on private-worker custody as well (RD-5, RI-5, RK-10, RL-6, RG-7); T-128’s is on
file (`receipts/private-custody-668cc1a-v1.json`). T-131, T-135, T-137 and T-138 are the
house at no count (RR-8).

Outside the `V3`/`C3` entries, `check_standing` also reads as pending adoption the
reported lower bounds T-132, T-142, T-143 and T-144, each above both of its case’s lower
bounds, which as reports can take only the reported lane; and T-121 to T-123, whose
exact values lie about $10^{-19}$ below their cases’ rational ceilings, the exact-value
integration PR #403 owns.
No deferral covers them, since no verified certificate of theirs is retained.

## Findings

**RR-1, non-blocking for the current rungs, blocking for any `V4`/`C4` promotion: the
register says the two AI reviews are by distinct reviewers, and the second one leaves
that to the owner.** `packing/frontier/results.yaml`, `next_rung` of T-128, T-130,
T-131, T-134 to T-141 and T-146: “two accepted adversarial reviews by distinct AI
reviewers are retained, the 10 October review and the 11 October final review”; of T-133
and T-145: “the two adversarial AI reviews by distinct reviewers are retained”.
The final upper-bound review ends its verdict table with the opposite caution: whether
it “counts as a distinct reviewer under epistemics.md (‘a different model family, or a
separately prompted independent lane with no shared context’) is for the owner”.
Both reviews of each entry are Claude lanes, and the final reviews read the stage 4
reviews in full before writing; the final lower-bound review calls itself distinct for
T-133 and T-145 on the same footing.
`adversarially_reviewed` counts distinct `reviewer` strings, and the strings differ, so
one human oversight record covering the fourteen would derive `V4`/`C4` at all of them
at once without anyone having decided the question.
The rule admits a separately prompted lane, so the ratings may well stand; the defect is
that the record states as settled what its own review left open.
Fix: open each of the fourteen `next_rung`s with “V4 and C4 need a retained human
oversight record.
Two accepted adversarial AI reviews are retained, the 10 October review
and the 11 October final review
(docs/project/reviews/review-2026-10-11-final-upper-bounds.md), both separately prompted
Claude lanes; whether the second counts as a distinct reviewer is the owner’s decision,
which the oversight record states.”, with the final lower-bound review’s path at T-133
and T-145. The oversight record, when written, records that decision under
`ai-findings`.

**RR-2, non-blocking: the derivation reads `certificate` as a non-empty string, not as a
path.** `_machine_proof_shaped` in `packing/devtools/check_results.py` tests
`bool(entry.get("certificate"))`; the evidence schema asks for a non-empty string;
`check_results` resolves artifact, control and review paths but not certificate paths,
and no other check found here does.
In scope every certificate resolves (41 from the repository root, the seven T-133 and
T-145 entries from `packing/`), so no rung here is affected.
Register-wide, 388 evidence entries name a `packing/`-relative certificate and four name
prose rather than a file (`E-basic-grid-upper`, `E-basic-area-lower`,
`E-n012-monotonicity-lower`, `E-n011-h236-rung0-reduction`); a mistyped path would leave
a `V3`/`C3` standing.
Fix, for a tool lane: resolve the `certificate` of every machine-shaped entry in
`check_results`, from the repository root and, while the record carries them, from
`packing/`, naming the four prose certificates as exceptions; then make the 388 paths
repository-relative in one mechanical change, as the rule on declared paths in
`AGENTS.md` (Architecture Overview) asks of the record’s other paths.

**RR-3, non-blocking: the sharp controls are not retained, and the later upper-bound
entries’ control paths name tests rather than the receipts that hold the controls.** At
T-128, T-130, T-131, T-134 to T-141 and T-146, `controls` lists test files only.
Each certificate’s kernel controls, the duplicated square and the square moved by
$S + 2$, are jobs in the packet’s `receipts/exact-certification.json.xz`, which T-125
and T-127 list as a control and these entries do not; and they are gross (RD-2, RI-3,
RK-8, RL-4, RG-5). The sharp, two-sided controls that the stage 4 and final reviews rely
on to show that the routes decide at the certificates’ scale (exact far-wall contact
accepted, $10^{-40}$ past it refused, the closest pair in contact accepted, pushed
$10^{-30}$ further refused) are written by
`check_half_angle_area decide`/`decide-imports --json` and retained nowhere; they exist
as review prose. A control path exists, so the predicate holds and no rung moves.
Fix: retain each packet’s third-route output, with its timing fields left out, as a
receipt beside the kernel’s (this lane’s runs price it: 69 s at one worker for the
fifteen `decide` certificates, 574 s for 21 import certificates under a load average of
12), and list it and the packet receipt among each entry’s `controls`.

**RR-4, non-blocking: T-127’s replay command overwrites the receipt it should be held
to.** `E-gupta-438-exact-feasibility.replay` is
`python -m devtools.gupta_refinement_reports certify --jobs-dir … --workers 2`.
`certify` decides the 51 jobs and writes `receipts/exact-certification.json.xz` anew
(`save_xz(receipt_path(), …)`), and `check` admits the receipt without deciding
geometry; the module has no mode that holds fresh decisions to the retained rows, as
T-128’s module had none before `replay-t128` (RD-1). Following the recorded replay
replaces the evidence it is meant to reproduce, and a difference would show only as a
changed file whose bytes differ by their timings anyway.
Fix, for a tool lane: a `check --replay` in `gupta_refinement_reports` that holds each
fresh job to its retained row with the kernel’s `replay_receipt`, as the later modules
do, and the evidence’s `replay` rewritten to it; the source host’s run took 256 s of
wall at two workers and 445 route CPU seconds (`receipts/batch-cost.json`).

**RR-5, non-blocking: T-133’s significance rationale is stale, and its `next_rung`
offers work that moves no bound.** Its `significance.rationale` opens “The strongest
lower bound on record at n = 40”, but T-145 superseded it the same day: its own notes
say so since F1-1, `check_standing` reads it as superseded, beaten at $n = 40$, and both
lanes of `n-040.md` cite T-145. This is F2-1’s pattern at T-138. Its `next_rung` still
proposes a method-distinct decision of the 401-direction nodal statement (Tokoharu’s
`verify.cpp`, about twice 6,521 s of wall upstream, after an input generator, a W7 slice
and a budget) and a census row; on a superseded entry these would add an attribute and
move no case bound. Fix: the rationale to “The strongest lower bound on record at n = 40
when registered, until T-145 the same day, 0.00854 above T-068 …”; and in `next_rung`,
“T-145 supersedes this entry at n = 40, so a method-distinct decision of its nodal
statement would move no case bound, and none is planned.”

**RR-6, non-blocking: the four reported lower bounds do not record what holds up their
replays.** T-132, T-142, T-143 and T-144 say each run “is queued … after the
regularization work (jlevy/squares#497)”. Their beads add three facts.
The commands need tooling that is only on the unmerged branch
`claude/wand125-confirmations-2026-10-11` (`44eb6a017`): on `main` the fine-net packets
are not in `sqverify_fast_census.MIXED_PACKETS` and `audit_wand125_linear` does not
register $n = 122$. Two questions are with the owner: whether to retain the three check2
candidates in Git (T-132, T-142, T-143), and, for T-142, the census’s axis tolerance,
since the 99/100 mutant’s exact capture at the axis direction sits $2.15 \times 10^{-9}$
above the vertex sweep’s certified bound, beyond `AXIS_ROUNDING` ($10^{-9}$), so the
whole-net control would write `CONTROL_FAILED` after 1.6 to 2.2 CPU-hours although the
refusal is sound.
And the smoke runs of 11 October that moved each price to its upper end
(T-144’s to 14.6 CPU-hours) kept their receipts in the coordinator’s scratch only, as
three of the four price bases say.
A question with the owner is what `activity` with `state: waiting` and `party: owner`
records. Fix: an `activity` (waiting, owner, the open question, since 2026-10-11, the
bead) on T-132, T-142 and T-143; the branch named in all four `next_rung`s; T-142’s
`unfinished_confirmations.what` saying the whole-net control is held on the
axis-tolerance decision; T-144’s price basis recording the smoke run and its 14.6; and
the smoke receipts retained in the packets when the branch lands, or “revised” dropped
from the bases.

**RR-7, non-blocking: T-120 to T-124’s unfinished confirmations have no owner and no
price, and T-120’s would move no bound.** Each item has no `link` and no
`estimated_cost`; the backlog prints “C3: not priced” with no bead.
The packet README says that the referenced `minpoly/data/` geometry payloads are outside
the retained scope and that PR #403, still open, owns exact-value integration.
T-120’s $\alpha_{102} = 10.6071746\ldots$ lies above the case’s verified ceiling,
10.6058286965… (T-125, another packing), so `check_standing` reads T-120 as superseded
and its `C3` would move no case bound; T-121 to T-123 would gain only the exact value,
about $10^{-19}$ below their rational ceilings.
Fix: link T-120 to T-123’s items to jlevy/squares#403 and T-124’s to issue #420 or a
bead; state “not priced: needs the `minpoly/data/` geometry at `f58a017` and an exact
root-identity check” (and, for T-124, the pinned Lean build); and add to T-120’s
`next_rung` that the confirmation would move no case bound, as T-129’s says.

**RR-8, non-blocking, for the adoption round: the deferrals expire before PR #403 may
land, and four confirming entries have no house to land in.** The eleven deferrals
recorded on 2026-10-10 fail `check_certificate_citations` once the evidence register’s
`last_reviewed` reaches 2026-11-10, and T-146’s on 2026-11-11; PR #403 is open.
By the adoption table T-131, T-135, T-137 and T-138 are the house at no count, so no
house move will cite `E-fang-484-exact-feasibility` (T-135, 308),
`E-deleeuw-483-exact-feasibility` (T-137, 70) or `E-mishapolk-470-exact-feasibility`
(T-138), and `E-evand-465-record-hunt-exact-feasibility` only if `n-155.md` cites
Daniel’s equal side as the 10 October review proposed.
The check passes a certificate cited from any `evidence` list of a case record, the case
roster’s included, which can carry a verified certificate that is not selected.
Fix: the adoption change cites those four in the rosters of their counts (308; 70;
T-138’s sixteen; 132 and 155), so that the deferral file empties; if #403 has not landed
by 2026-11-09, each deferral is re-dated with what happened since, as the file’s header
asks. A dated reminder on `think-fvz4` would carry it.

**RR-9, non-blocking: two entries list later replacements in part.** T-125’s notes name
T-146 as smaller at seven counts; by the sides registered, a `V3`/`C3` entry below
T-125’s certificate is pending at 16 of the 17 counts where the case records cite T-125,
all but 261: T-146 at 70, 102, 103, 123, 129, 146 and 295; T-130 at 84, 86 and 105;
T-128 at 108 and 127; T-139 at 126; T-136 at 131; T-140 at 175; T-134 at 267. T-127 is
cited at fourteen counts, and smaller entries are pending at seven (T-146 at 153 and
236, T-136 at 154 and 207, T-128 at 180, T-140 at 209 and 237); its prose names none,
which is consistent, since standing is derived and never stored.
T-136’s `next_rung` names its own six houses and T-146’s seven counts and is silent at
209, 237, 270 and 305, where T-140 is smaller by $4.3 \times 10^{-7}$ to
$5.6 \times 10^{-5}$. Fix: replace T-125’s T-146 sentence with “Later certificates below
these are pending adoption at 16 of the 17 counts the case records cite this entry for,
as `devtools.check_standing --list --cases` shows”, and add to T-136’s `next_rung` “At
209, 237, 270 and 305 the house recommendation goes to T-140.”

## Proposed Record Changes

None of these changes a rung.
This review writes none of them.

- **For the records lane, in `packing/frontier/results.yaml`:** the fourteen
  `next_rung`s of RR-1; T-133’s `significance.rationale` and `next_rung` (RR-5); an
  `activity` on T-132, T-142 and T-143, the branch in all four of T-132, T-142, T-143
  and T-144’s `next_rung`s, T-142’s `unfinished_confirmations.what` and T-144’s price
  basis (RR-6); a `link` and a “not priced” statement on T-120 to T-124’s unfinished
  confirmations and a sentence in T-120’s `next_rung` (RR-7); T-125’s notes and T-136’s
  `next_rung` (RR-9); and each packet’s `receipts/exact-certification.json.xz` (at
  T-136, its seventeen shards) added to the `controls` of T-128, T-130, T-131, T-134 to
  T-141 and T-146 (RR-3).
- **For a tool lane:** certificate paths resolved by `check_results` (RR-2); a
  third-route receipt retained in each upper-bound packet (RR-3); a replay mode for
  `gupta_refinement_reports` and T-127’s `replay` rewritten to it (RR-4).
- **For the adoption round after PR #403:** the per-count houses of the adoption table,
  each earlier house kept as history; the four confirming entries of RR-8 cited in their
  counts’ rosters; every deferral removed in the change that cites its evidence; the
  private-worker custody of the seven houses that lack it first; and, if #403 has not
  landed by 2026-11-09, the deferrals re-dated.
- **For the owner:** the RR-1 decision, in the human oversight record that `V4`/`C4`
  needs at seventeen entries; and the two questions of RR-6.

## What This Review Does Not Establish

No mathematics of any result: this is a review of the ratings against the retained
files, not an adversarial review, and it adds nothing to any entry’s `reviews`. No full
kernel replay of the T-125 to T-128, T-130, T-134 to T-136, T-138, T-140 and T-146
receipts here (each was admitted here, and the runs that wrote or replayed it are on
record in its evidence); no run of `decimal_pose_margins` or of
`decide-imports --upstream` beyond #483; no source program; no replay of T-133’s or
T-145’s kernels or crate runs (their retained receipts were judged by the first-party
audits only); no Lean build; no price measured here for T-120 to T-124. No house
adoption, case-record change or private-worker custody.

## Status, 14 October

`main` moved past parts of this review after it was written, and review A of the pull
request that carries it (#563, finding A2) found that nothing said so.
The findings above are left as written on 11 October; this note says what has changed.
It was checked against `main` at `b8c930338`.

- **The adoption section, `RR-8` and `RR-9` are overtaken by #518,** which merged at
  15:11 UTC on 12 October and adopted the houses without waiting for PR #403, still
  open. `packing/devtools/certificate-citation-deferrals.yaml` reads `deferrals: []`, so
  no deferral can expire.
  Six counts are now held by imports registered after the table, not by the house it
  names:

| n | The table’s house | The house on `main` |
| --- | --- | --- |
| 146 | T-146 | T-150 |
| 153 | T-146 | T-148 |
| 155 | T-128 | T-149 |
| 207 | T-136 | T-147 |
| 270 | T-140 | T-151 |
| 305 | T-140 | T-152 |

`T-125`’s notes now say it holds no case record and name the adoption, and `T-136`’s
`next_rung` names no houses, so `RR-9`’s fixes have nothing left to change.

- **`RR-1` misquotes `T-146`.** Its `next_rung` reads “the 11 October review and the 11
  October final review”, not “the 10 October review”; the other thirteen read as quoted.
  A change that applies `RR-1`’s proposed text keeps “11 October” at `T-146`.

- **`RR-6` quotes the four `next_rung`s as of 11 October.** On `main` each now reads
  “after the regularization of every packing (think-ux1v, planned in jlevy/squares#497)”
  where it read “after the regularization work (jlevy/squares#497)”. None of `RR-6`’s
  fix is on `main`: no `activity` on `T-132`, `T-142` or `T-143`, no branch named,
  `T-142`’s control and `T-144`’s price basis as they were, and the smoke receipts still
  unretained.

- **`RR-1` to `RR-7` otherwise stand.** The fourteen `next_rung`s still say the two
  reviews are by distinct reviewers; `T-133`’s rationale still calls it the strongest
  lower bound at $n = 40$, which `T-145` superseded; `T-132` and `T-142` to `T-144`
  carry no `activity`; and `44eb6a017`, the tooling `RR-6` names, is not on `main`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
