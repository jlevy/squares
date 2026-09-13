---
title: session-125 — pushing s(11) past the point-atom ceiling, and integrating the owner line
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-125
  title: Pushing s(11) past the point-atom ceiling, and integrating the owner line
  date: '2026-09-08'
  started_at: '2026-09-08T23:31:43Z'
  branch: claude/n-11-stronger-result-d730ds
  resource_rollups: [packing/campaign/resource-usage/cd8c0aac-f931-5096-97c8-3cccdcaa8ba9.yaml]
  goal: Consider every way to push the n = 11 lower bound aggressively beyond 3.810025723614703, breadth first, then push each direction with a discriminating measurement; retain what moves the bound; integrate the concurrent ownership work of PR 137 and read the two lines together.
  workflow_phases:
  - workflow: research-survey
    focus: insight
    recording: retrospective
    objective: Map every direction for a stronger s(11) lower bound from the contributed note and the record; dispose of the note's proposals; spike the cheap directions in parallel lanes with disjoint deliverables.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 240
    started_at: '2026-09-08T23:31:43Z'
    deadline_at: null
    expected_output: X-023 with a direction map, the note checked in as a dated review, lane reports for the spikes.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: null
    fallback: null
    outcome: X-023 (three losses and a new atom), the review of the contributed note, lanes T, E, M0, A and B under agenda-034, the exact ceiling family at 191/50 with an independent reader, threshold atoms as a certificate language with a two-route exact decision.
    evidence: [packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md]
    stop_reason: The survey had a direction map and two of its spikes had produced retainable objects; further breadth would have cost more than freezing what was already in hand.
    next_action: Retain the finer-net dilation limit and the 191/50 threshold certificate, each by its own gate.
  - workflow: research-loop
    focus: correctness
    recording: retrospective
    objective: "Retain what moves the bound: freeze the finer-net certificates and register the dilation limit; verify and register the threshold certificate at 191/50 by a second route and an adversarial review."
    bead: think-hs7y
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The spikes had produced two retainable objects.
    budget_minutes: null
    started_at: null
    deadline_at: null
    expected_output: T-024 registered; the threshold certificate decided by two routes, reviewed, and registered as T-025.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: A route disagreement or a review finding against the theorem.
    fallback: Record the disagreement or finding and keep the candidate unretained.
    outcome: T-024 registered; the threshold certificate decided by the exact sweep and by an independent interval branch and bound, attacked by an adversarial review that found no soundness defect, registered as T-025; then re-certified on the 720- and 1440-step nets, both RETAINABLE with both routes agreeing, and registered as T-026.
    evidence: [packing/cases/n11_fractional_certificate/t-024-dilation-limit-proof.md, docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md]
    stop_reason: Every candidate the survey produced was either registered or refused. The original assessment of near-exhausted refinement is qualified by the September10 review; the measured finite nets do not decide another net.
    next_action: The certificate format has to widen before the strongest separable cuts can be frozen.
  - workflow: general-improvement
    focus: process
    recording: retrospective
    objective: Integrate PR 137 (the ownership and conditional-owner line) into this branch without identifier collisions, read the two lines together strategically, and settle by measurement which line to fund.
    status: completed
    entered_by: user_request
    switch_reason: The owner asked for the integration at a stopping point and for a strategic reading of both lines.
    budget_minutes: null
    started_at: '2026-09-09T06:42:41Z'
    deadline_at: null
    expected_output: A merge of e6a01449 with unions of every register; renumbered identifiers; X-024 with the plan and the division of labour.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: null
    fallback: null
    outcome: "PR 137 merged at 787cf1c9 of the pre-squash history, with unions of every register and this branch's identifiers renumbered around it first; X-024 written; the retained fractional family was mass-neutral on the screened endpoint-patch combinations. The broader strategic conclusion was withdrawn after the September10 review; routing and changed domains remain open."
    evidence: [packing/campaign/explorations/X-024-two-lines-at-eleven.md]
    stop_reason: The phase historically stopped after interpreting the X1 measurement as no added reach. That method-wide interpretation and its funding rationale were withdrawn by the September10 review; no comparative productivity result was established.
    next_action: Retain the five research lanes and file the defect the neutrality measurement exposed.
  - workflow: review-planning-oversight
    focus: process
    recording: retrospective
    objective: "Close the branch: retain the day's five research lanes as documents, file the defect the neutrality measurement exposed, remove the oversized receipt from the branch's own history, and certify the session."
    status: completed
    entered_by: user_request
    switch_reason: The owner's agenda moved from research to branch hygiene and to keeping the pull request current.
    budget_minutes: null
    started_at: '2026-09-09T14:56:14Z'
    deadline_at: null
    expected_output: Five lane documents registered in the document map, D-489 in the defect register, H-155 dispositioned, a squashed branch without the 12.6 MB receipt blob, and this record.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: null
    fallback: null
    outcome: This branch's own 26 commits squashed onto PR 137's head as 7ccb679c at the owner's instruction, dropping a 12,584,012-byte receipt blob from the branch and force-pushing once; retention then added 594caa3a, f84dd78f and 0443a193; D-489 filed; H-155 dispositioned as live rather than refuted and priced at no reach; twenty-one CI checks green on both the squashed head and the current head.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md, packing/defects.yaml]
    stop_reason: The branch is published, green and current, and the session record is the last artifact it was missing.
    next_action: Widen the certificate format to carry weighted and floor atoms, and generate sites by structure rather than by arrangement vertex.
  primary_bead: think-hs7y
  status: completed
  budget: {wall_minutes: 600, checkpoint_minutes: 30, slice_minutes: 30}
  stop_conditions:
  - The owner ends the task, or every open lane has a retained result or a recorded reason it stopped.
  progress:
    metric: The verified lower bound on s(11) in the frontier register, and the retained instruments behind it.
    before: 3.810025723614703 (T-022); the covering LP at 3.82 stops at exactly eleven on every site set; no explanation of the plateau; no certificate language past point atoms.
    after: s(11) >= 955000*sqrt(518400042893309449)/179696714646249 = 3.826447410572939 (T-026), reached through T-025's certificate instantiated at 191/50 = 3.82, the first result past the exact point-atom ceiling; the retained LP plateau has quantified depth violations and fixed-support cut results, without a complete diagnosis over unrestricted supports and a certificate language past point atoms exists with two independent decision routes.
  delegations:
  - task: Theory of cuts and routes (lane T); the sandwich lemma and the k-fold witness lemma.
    operator: Claude Fable, high
    recording: contemporaneous
    phase: 1
    status: completed
    outcome: Every one-body core choice is capped by the shrink tax; direction-dependent weights never help; the cut families that can pass the ceiling are named.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-t-theory-cuts-and-routes.md]
    files: []
    checks: [Document-map registration; footer; links resolve.]
    uncertainty: Analytic; no new bound.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Cited by X-023 and X-024.
  - task: Spike B, threshold atoms at 191/50; the exact point-atom ceiling; the loop; the accepted candidate.
    operator: Claude Fable, high (two runs)
    recording: contemporaneous
    phase: 1
    status: completed
    outcome: Ceiling family of weight exactly eleven and depth one at 191/50 (EXACT); a threshold certificate of budget 685457679/62500000 accepted by the exact route, then by the interval route.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-b-threshold-atoms-at-191-50.md]
    files: [packing/src/sqpack/fractional/threshold.py, packing/devtools/decide_threshold_certificate.py]
    checks: [decide_threshold_certificate RETAINABLE at 100000203/100000000; 29 tests; ruff and basedpyright clean.]
    uncertainty: The candidate rested on one decision route until the interval route was built; the loop scripts that produced it were scratch-only and carried two defects of their own.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Registration as T-025; the loop at 383/100.
  - task: Interval route for threshold certificates and the two-route gate.
    operator: Claude Fable, high
    recording: contemporaneous
    phase: 2
    status: completed
    outcome: threshold_interval.py; both routes agree on the frozen candidate; 361 doubled-net directions, 1,639,903 boxes, none stalled.
    evidence: [docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md]
    files: [packing/src/sqpack/fractional/threshold_interval.py, packing/tests/test_fractional_threshold_interval.py, packing/tests/test_decide_threshold_certificate.py]
    checks: [29 tests passed; ruff, format and basedpyright clean.]
    uncertainty: None on the decision; retention items were the case package and controls.
    elapsed_seconds: 2106
    elapsed_quality: platform_measured
    next_action: Registration.
  - task: Adversarial review of the threshold theorem and the decide tool.
    operator: Claude Fable, max
    recording: contemporaneous
    phase: 2
    status: completed
    outcome: Theorem sound as stated; Conditions 1 to 4 of the candidate recomputed without sqpack; Condition 5' matched at 23 of 181 directions by an independent sweep; fifteen findings, none a soundness defect.
    evidence: [docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md]
    files: []
    checks: [Review registered in the document map; footer; links resolve.]
    uncertainty: The other 158 directions rested on one route until the interval route agreed.
    elapsed_seconds: 1865
    elapsed_quality: platform_measured
    next_action: The review is the C5 artefact for T-025.
  - task: Retain spike A and spike B reports as lane documents (mechanical).
    operator: Claude Opus
    recording: contemporaneous
    phase: 2
    status: completed
    outcome: lane-a and lane-b documents with receipts under 1 MB; document-map entries; checkers pass.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a-net-refinement-and-shrink-tax.md]
    files: []
    checks: [check_documentation, render_document_map, check_synopsis pass.]
    uncertainty: None.
    elapsed_seconds: 636
    elapsed_quality: platform_measured
    next_action: None.
  - task: Renumber this branch's identifiers around PR 137 (mechanical; stopped by the owner before its report, completed and verified with repren by the coordinator).
    operator: Claude Opus
    recording: contemporaneous
    phase: 3
    status: canceled
    outcome: T-023 to T-024, agenda-032 to agenda-034, H-136 to H-138 to H-152 to H-154, idea rows 132 to 134 to 139 to 141; repren dry run found no remaining match outside caches.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/reconciliation-upstream-2026-09-09.md]
    files: []
    checks: [check_rung_figures, check_case_prose, check_synopsis, check_readme pass; check_results reports only the T-023 gap the merge closes.]
    uncertainty: None.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: None.
  - task: Read-only summary of PR 137's line of work.
    operator: Claude Opus
    recording: contemporaneous
    phase: 3
    status: completed
    outcome: A cited summary of PR 137's results, case-split architecture, experiments, instruments, points of contact and allocated identifiers.
    evidence: [packing/campaign/explorations/X-024-two-lines-at-eleven.md]
    files: []
    checks: [Read-only; no tree change.]
    uncertainty: None.
    elapsed_seconds: 701
    elapsed_quality: platform_measured
    next_action: Consumed by X-024.
  - task: Merge PR 137 into this branch (mechanical; stopped by the owner after the merge commit and before the push).
    operator: Claude Opus
    recording: contemporaneous
    phase: 3
    status: canceled
    outcome: Merge commit 787cf1c9 of the pre-squash history, with unions of every register and re-rendered views; records tier and checkers pass; the fast tier was rerun by the coordinator.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/reconciliation-upstream-2026-09-09.md]
    files: []
    checks: [records tier passed at 787cf1c9; eight checkers exit 0.]
    uncertainty: None.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: None.
  - task: The frozen threshold certificate on the 720- and 1440-step nets (X-024 slice A2).
    operator: Claude Opus
    recording: contemporaneous
    phase: 2
    status: completed
    outcome: The frozen atoms transfer at every net tried; crossing shrink equal at 720 and 1440, so the last 0.0011 of the limit comes from D halving alone; rescaled budgets 10.9963 against eleven, so net refinement is near exhausted on these atoms. Registered as T-026.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a2-threshold-certificate-on-finer-nets.md]
    files: []
    checks: [Both routes RETAINABLE and agreeing at least cell charge exactly 1 on both nets.]
    uncertainty: None on the decision; the budgets say this route is nearly spent.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Registered as T-026; no further net refinement is worth funding on these atoms.
  - task: The threshold loop at 383/100 (X-024 slice A3).
    operator: Claude Fable, medium-high
    recording: contemporaneous
    phase: 3
    status: completed
    outcome: No certificate on the accepted columns at 383/100 (11.018) or at 153/40 (exactly eleven); every plateau dual refused as a fractional packing, at depth 1.124 at a corner seam, 1.098 at an interior meeting, and 28/25 after site separation inside a sliver 0.0006 wide; one atom round moved 3e-9 and one site round with 2,304 sites moved nothing.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a3-threshold-loop-at-383-100.md]
    files: []
    checks: [Every reader verdict a rational; the three duals and their trajectories retained beside the lane report.]
    uncertainty: The reading that the sites rather than the atoms carry the plateau was a conjecture here and was confirmed afterwards by the separation lane.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: 'think-7rqw: close the sliver by structure, or show the plateau is a theorem about the method with its own sites.'
  - task: "Strategy: the cheapest conditioning that buys enough."
    operator: Claude Opus
    recording: contemporaneous
    phase: 3
    status: completed
    outcome: The retained family has corner-mark weight1 and additive deletion for the named endpoint-patch combinations. Its survivor families obstruct point covers on those relaxations. The broader no-rung conclusion is withdrawn by September10 review; the source-filter reuse defect is D489.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md]
    files: []
    checks: [The transport and the screen are PR 137's own; the survivor family read by the plateau reader at depth exactly 1.]
    uncertainty: Neutrality is exact for the screened family and endpoint patches. Physical routing, stronger domains and conditional threshold covers remain open; matching cut maxima establishes no runtime comparison.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Recorded in X-024 section 5; H-155 dispositioned; D-489 filed.
  - task: Survey of PR 137's owner instruments.
    operator: Claude Opus
    recording: contemporaneous
    phase: 3
    status: completed
    outcome: The single-corner theorem is standalone and its tooling exists at owner-count 1, but the side 96/25 is baked in and no ownership theorem exists elsewhere, so the conditional window was (3.82, 3.84] even before neutrality.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x2-owner-instrument-survey.md]
    files: []
    checks: [Read-only; every claim cited to a module constant or a theorem statement.]
    uncertainty: None.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Consumed by the H-155 disposition.
  - task: Containment atoms against the plateau families.
    operator: coordinator
    recording: contemporaneous
    phase: 3
    status: completed
    outcome: No exceedance was reported on the finite eight-step box grid. September10 review found the generic stacking capacity false; the narrower no-exceedance of the valid area bound survives, while the strip-capacity and method-closure conclusions are withdrawn.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x3-containment-atoms-do-not-cut.md]
    files: []
    checks: [Exact sweep; the two scripts retained beside the lane report.]
    uncertainty: The sweep is over one grid resolution; a finer grid was not measured because the families are exactly at capacity.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: None; the class is closed.
  - task: Separating the 1/25 plateau dual (X-024 slice A4).
    operator: Claude Opus
    recording: contemporaneous
    phase: 3
    status: completed
    outcome: All three atom classes violated, two-of-three at 133/100, a 42-member clique at 3/2, floor cuts to 8.27; the LP moved 2.2e-13 and every new column carries primal weight exactly zero. Read at the time as the site set pinning 3.825; corrected 2026-09-10 by lane A6, which exhibits a depth-one family of 64 placements totalling exactly 11, so the LP is at least eleven for every site set on this atom set and the atom language is what pins it. The measurement stands; only the inference changed. Atoms must be separated from the depth-one certificate rather than from a dual vertex.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a4-separating-the-plateau-dual-at-153-40.md]
    files: []
    checks: [Every separation verdict a rational, re-verified exactly; the seeded and control runs retained beside the lane report.]
    uncertainty: Finding P10 is the live blocker -- the certificate format cannot express the K5 and K6 atoms the reader separates, so none of these cuts can be frozen or gated today.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: 'think-g3j7: widen the certificate format; think-q0f4: generate sites by structure.'
  - task: The fixed-support maximum under the atom classes (X-024 slice A5).
    operator: Claude Opus
    recording: contemporaneous
    phase: 3
    status: completed
    outcome: nu_S = 32/3 exactly at both 153/40 and 383/100 under depth-one plus the complete budget-one class, falling to exactly 10 with floor cuts. No cap at either side.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a5-the-fixed-support-maximum-under-the-atom-classes.md]
    files: []
    checks: [Exact optima; the loop and no-atom controls retained beside the lane report.]
    uncertainty: The maximum is over this site set; it says the method has headroom here, not that a certificate exists.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: The headroom is real, so the blocker is the format and the sites rather than the method.
  - task: Retain the day's five research lanes as lane documents, file the defect the neutrality measurement exposed, and disposition H-155.
    operator: Claude Opus
    recording: contemporaneous
    phase: 4
    status: completed
    outcome: Five lane documents under results/agenda-034 with their receipts, registered in the document map and in X-024's sources (594caa3a); D-489 recorded with its evidence and every citation of exp-137 and exp-138 corrected (f84dd78f); X-024 section 5 rewritten, slices B1 and C1 withdrawn, A4 and A5 marked done, H-155 dispositioned at priority 3 as live rather than refuted and priced at no reach (0443a193); the scope of that disposition was restated later the same day against X-026, which states the argument as a six-step ladder and marks where it stops.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md, packing/defects.yaml]
    files: [packing/campaign/explorations/X-024-two-lines-at-eleven.md, packing/campaign/hypotheses/H-155-conditional-threshold-cover-on-an-owner-class.md, docs/project/document-map.yaml]
    checks: [records tier and fast tier green before the push; twenty-one CI checks green on 0443a193.]
    uncertainty: None.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Closeout.
  - task: "Close the session out: this record, the resource rollup, the close report, and the bead disposition."
    operator: Claude Opus
    recording: contemporaneous
    phase: 4
    status: completed
    outcome: This record; the Claude rollup for the session log committed under campaign/resource-usage rather than held out, so the pull request's cost block renders from the tree; session-close-report.yaml and the SYNOPSIS tables re-rendered; slices A5, B1 and C1 and the receipt-blob decision closed as beads and four follow-ups left open.
    evidence: [packing/campaign/agent-sessions/session-125-past-the-point-atom-ceiling.md, packing/campaign/session-close-report.yaml]
    files: [packing/campaign/resource-usage/cd8c0aac-f931-5096-97c8-3cccdcaa8ba9.yaml, SYNOPSIS.md]
    checks: [records tier and fast tier green on the closeout tree before the push.]
    uncertainty: The rollup is a snapshot taken while the session was still running, so its totals are a lower bound on the session's cost, as every live receipt here is.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: None.
  outputs:
  - packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md
  - packing/campaign/explorations/X-024-two-lines-at-eleven.md
  - packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md
  - packing/campaign/hypotheses/H-157-refined-owner-sector-patch-breaks-neutrality.md
  - packing/cases/n11_fractional_certificate/t-024-dilation-limit-proof.md
  - packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md
  - packing/cases/n11_threshold_certificate/t-026-dilation-limit-proof.md
  - docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md
  - packing/src/sqpack/fractional/threshold.py
  - packing/src/sqpack/fractional/threshold_interval.py
  - packing/devtools/decide_threshold_certificate.py
  - packing/devtools/plateau_reader.py
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x2-owner-instrument-survey.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x3-containment-atoms-do-not-cut.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a4-separating-the-plateau-dual-at-153-40.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a5-the-fixed-support-maximum-under-the-atom-classes.md
  checks:
  - 'full gate: fast at 0443a193: passed (re-run locally on the closeout tree, whose additions over it are records only)'
  - The records tier is green on that same closeout tree, with the session rollup in it rather than held out.
  - Twenty-one CI checks are green on the squashed head 7ccb679c and on the current head 0443a193.
  - The whole-suite tier ran once on the pre-squash tree and its cost record was re-recorded after the PR 137 merge; both of those commits left the branch in the squash and are no longer ancestors of this head.
  - Two fast-tier failures on this branch were real and were fixed rather than retried -- a mutation-snapshot source cap that the merged tree genuinely exceeded, moved from 128 to 160 MiB, and a dead document anchor.
  stop_reason: The owner's agenda moved to branch hygiene and to keeping the pull request current; every open lane has either a retained result or a recorded reason it stopped.
  next_action: Widen the certificate format to carry weighted and floor atoms, since the reader can already separate cuts the format cannot express; and generate sites by structure rather than by arrangement vertex.
---
# Pushing s(11) Past the Point-Atom Ceiling, and Integrating the Owner Line

**Review update, September 10, 2026.** This retrospective session retains the original
measurements and decisions.
Its old comparative judgments are superseded by
[X-024’s current combined reading](../explorations/X-024-two-lines-at-eleven.md#current-combined-reading--september-10-2026)
and the corrected
[X-026](../explorations/X-026-what-conditioning-does-and-does-not-buy.md).
The global T-026 bound remains `3.826447410572939744...`. X1 neutrality concerns the
screened fractional family and endpoint patches; it does not settle physical owner
routing or all conditional approaches.
The unconditional cap needs additional owner premises before conditional transfer.
X3’s stacking capacity is invalid.
A4/A5’s conclusions remain tied to their finite supports and searches.
The historical body below is not evidence of a universal method ranking.

The session set out to push the n = 11 lower bound as hard as it would go, and it moved
twice.
The exact ceiling family at 191/50 closed the one-body point-atom method for good,
capping it at unit side 3.8288; threshold atoms then passed that ceiling and proved
s(11) >= 3.82 at the side itself, decided from frozen bytes by two routes that fail
differently and attacked first by an adversarial review.
Re-certifying the same atoms on finer nets carried the exact endpoint to
3.826447410572939. Alongside that, PR 137’s conditional ownership line was merged in and
read against this one.

What the session did not expect was to reverse the direction it had been leaning toward.
Corner conditioning looked like the way past the plateau, because four owners take a
required cover from eleven to five.
The measurement says otherwise, exactly: the ceiling family carries weight one at each
corner mark and the corner deletions are disjoint, so every rung of the ladder gives up
exactly as much threshold as it takes back.
The record had read otherwise because the instrument that screened it can only accept
families that fall short of mass eleven — that is D-489.

**The scope of that, corrected later the same day.** The first summaries of the
measurement said conditioning was *refuted*, and that is wider than what was measured.
Refutation covers the conditional method by **point covers** on the residual domain, and
nothing else; the survivor family violates the two-of-three inequalities, charging `5/4`
against a budget of one, so it does not block a conditional threshold certificate.
The general result is **neutrality**: conditioning subtracts exactly `m` from both the
obstruction and the requirement, so it cannot turn a failing method into a succeeding
one. That argument is stated in full, term by term, in
[X-026](../explorations/X-026-what-conditioning-does-and-does-not-buy.md), which also
names the one cheap unrun measurement that could overturn it — a sixteen-sector
refinement of the owner patches, registered as `H-157`.

With conditioning priced as neutral, the two remaining measurements located the real
barrier: the method has at least a third of headroom at 3.825, every atom class is
violated by the plateau dual, and adding those cuts moves the value by nothing because
the site set, not the language, is what pins it.

## What the phase record is, and is not

No session record was kept in the tree while this ran, so the four phases above are
reconstructed at closeout from the branch’s own evidence — the commits, the lane
documents, the retained receipts, and the owner’s messages that opened phases three and
four. Each phase is marked `retrospective` for that reason, and the fields a contract
would have carried in advance — phase budgets, kill conditions, fallbacks — are left
null rather than written after the fact.
The objectives, expected outputs and validation commands are the ones the work actually
ran under.

The branch was squashed once, at the owner’s instruction, and force-pushed: this
branch’s own twenty-six commits became `7ccb679c` on PR 137’s head, which removed a
12,584,012-byte lane E completion receipt from the branch rather than leaving it
reachable behind the commit that slimmed it to its 201,836-byte decision-bearing
content. PR 137’s commits were untouched.
Three retention commits followed and nothing has been rewritten since.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
