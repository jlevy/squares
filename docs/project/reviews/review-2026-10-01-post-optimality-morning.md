---
title: October 1 Post-optimality Research Findings
date: 2026-10-01
status: completed
---
# October 1 Post-optimality Research Findings

The overnight work certifies an exact physical endpoint for the known n17 packing and an
attained minimum within a stated family.
It does **not** establish unrestricted local or global optimality for n17. The strongest
new search preparation is a complete closed-cell cover with an exact occupancy census
and a reviewed symmetry quotient.

[Session 165](../../../packing/campaign/agent-sessions/session-165-post-optimality-overnight.md)
records the execution;
[X-048](../../../packing/campaign/explorations/X-048-n17-optimality-after-n11.md)
connects it to the transfer program following the n11 proof.
The source intake is retained in companion
[PR267](https://github.com/jlevy/squares/pull/267); this session did not repeat that
intake or perform a broad external replay.

## What Is Established

| Result | Evidence and scope |
| --- | --- |
| Existing rational n17 packing | [H253](../../../packing/campaign/hypotheses/H-253-n17-retained-rational-upper.md): two local exact separating-axis implementations and the source checker accept the Kleddamag reconstruction of Bidwell’s packing at side $4675530093604551/10^{15}$. This is replay and admission, not a new packing discovery. |
| Exact chart and root | [H254](../../../packing/campaign/hypotheses/H-254-n17-contact-chart-fidelity.md) checks 458 chart clauses; [H255](../../../packing/campaign/hypotheses/H-255-n17-exact-polynomial-root.md) proves existence and uniqueness of the two-polynomial root inside its fixed rational box. Separate implementations use the same contraction argument. |
| Physical algebraic endpoint | [H256](../../../packing/campaign/hypotheses/H-256-n17-exact-endpoint-feasibility.md) proves 68 wall and 136 pair constraints at the root. A separate auditor reproduces all 187 interval bounds exactly; the zero identities have separate analytic review. The frontier now admits the rational outward ceiling 4.6755300936045509516342148538535054. |
| Complete contact features | [H257](../../../packing/campaign/hypotheses/H-257-n17-endpoint-contact-features.md) checks 168 owner-axis alternatives, 60 corner-to-active-wall gaps (29 zero and 31 positive) and 9 tangential offsets. The independent audit matches all 175 strict interval records. |
| Conditional minimum | The [projection theorem](review-2026-10-01-n17-projection-branches.md) supplies necessary inequalities under 19 directed separation premises and stated orientation/parameter restrictions. Their minimum is attained by the certified endpoint. Several exact-angle assumptions have been removed; unrestricted nearby configurations have not been captured. |
| Complete occupancy cover | [H259](../../../packing/campaign/hypotheses/H-259-n17-mixed-capacity-cover.md) proves 16 boundary cells have capacity one and 9 interior cells capacity two at cap $1169/250$. Exact DP and an independent binomial audit count 161,100,756 states summing to 17, versus 8,597,496,600 for the binary baseline. |
| Symmetry quotient | [H260](../../../packing/campaign/hypotheses/H-260-n17-closed-cell-symmetry.md) uses existential closed-cell assignments. The single target reports 20,155,518 D4 orbits with all eight fixed counts independently checked. The experiment and independent output review record acceptance. These are necessary occupancy cases, with no geometric case excluded. |
| Low-n alternative | The [n12 graph review](review-2026-10-01-n12-weighted-cycle-capture.md) derives the arbitrary-weight finite-row inequality, proves that canonical wall repair at side 4 preserves every nonpositive-bound certificate on a fixed edge support, and checks three hand controls. Universal valid-support coverage remains missing. No n12 bound was advanced. |

The verified n17 bound is an upper bound: it says a packing exists.
A global optimality proof also needs a matching lower bound: every packing with smaller
side must be impossible.
The current [n17 frontier record](../../../packing/frontier/n-017.md) keeps that
distinction and remains open.

## What Still Prevents Optimality

1. **Capture of arbitrary packings.** The 19 directed projection inequalities are
   stronger than arbitrary nonoverlap.
   We have not shown that every smaller packing, or even every nearby packing, satisfies
   one of the covered branches and orientation premises.
   The parameter box also does not cover distant configurations.
2. **Geometric exclusions for the occupancy cases.** Counting the closed-cover states
   provides a finite scaffold; each state still allows continuously varying positions
   and orientations. None of the counted cases has been excluded by H259 or H260. The cap
   4.676 contains the known endpoint, so excluding every case at that cap would
   contradict the accepted packing.
   A lower-bound argument must retain the actual side variable below the endpoint, or a
   declared smaller rational cap.
   The symmetry review specifies the centred embedding needed to retain the fixed-grid
   action at smaller sides.
3. **First-order and higher-order arguments.** The complete contact inventory supports a
   two-branch first-order model.
   H258 did not produce a target stress certificate.
   Even an accepted stress would require a separate argument for local optimality; local
   optimality alone would not establish global optimality.

The **identification with the catalogue polynomial** is a separate question, not a
prerequisite for proving the chart endpoint optimal.
The chart root is certified, but equality with the catalogue’s degree-18 algebraic
specification has not been proved here.
The admitted rational ceiling does not depend on that identification.
The established lower bound 4.66044 is unchanged.

Slider freedoms and a rotational rattler also rule out an unqualified rigidity claim.
The conditional theorem and exact feasible family must be stated with those freedoms.

## Refusals and Efficiency

H258 stopped after three synthetic symbolic preparation failures: approximately 120
seconds interrupted, then 90 seconds and 90 seconds at the guards.
No target stress was evaluated.
The
[preparation record](../../../packing/campaign/explorations/X048-stress-preparation/preparation-2026-10-01.json)
retains the observed evidence and its limitations.
The two draft CLIs refuse target inputs.
This is an instrument-readiness failure, not a refutation of the mathematical candidate;
no further attempt was admitted overnight.

| Work | Observed wall time | Interpretation |
| --- | ---: | --- |
| H253 replay command group | 7.91s | Includes source replay and controls; individual receipts retained |
| H254 chart | 1.13s | Complete 458-clause target |
| H255 root producer and checker | 0.67s + 0.09s | Two implementations of the same exact contraction test |
| H256 endpoint and independent interval audit | 43.45s + 5.005s | Producer symbolic work 25.797s; intervals and serialization 16.419s |
| H257 features and independent interval audit | 41.80s + 11.275s | Producer symbolic work 24.506s; intervals and formatting 16.093s |
| H259 two counts and two independent audits | 0.35s | Process startup and JSON included; no geometric exclusions measured |
| H260 count and independent audit | 0.14s | Eight fixed-count terms and quotient; no geometric exclusions measured |

Mathematical derivation, controls, review and integration account for most elapsed time.
Several target runs occurred under substantial unrelated host contention; these timings
are observations, not controlled language, library or worker-count benchmarks.
The exact interval implementations use Python arbitrary-size integers; no measured
comparison establishes that a Rust replacement would improve this workload.
The separate `think-am9e` task preserves a controlled compact-arithmetic/serialization
benchmark with an unchanged acceptance contract.

Hosted CI runs beside research.
General slow local suites and atlas geometry rebuilds were kept off the proof critical
path. The guarded `--restamp-only` publication command completed in 17.41 seconds with
strict preflight and postflight checks.
It changed only the two SVG footer stamps and refreshed their PNG/PDF export families,
without rebuilding any packing geometry.
[Its command and timing receipts](../../../packing/campaign/agent-sessions/session-165-validation/restamp-command.txt)
are retained under `think-zypq`, separately from scientific target cost.
Six focused controls and independent code review cover the source and byte-preservation
guards. The fast path conservatively permits only the reviewed n17 frontier metadata
change and refuses other case changes; broader support needs its own guarded review.
The combined release/restamp check passed 19 tests in 2.18 seconds.
This observed run is not a controlled speedup comparison against earlier host-contended
atlas builds. The
[native task-tree receipt](../../../packing/campaign/resource-usage/session-165-codex-task-tree.yaml)
measures the interval 10:31:42–14:29:33 UTC. It records 47,342.718 aggregate
agent-active seconds across 14,270.128 active-union seconds: about 13.15 agent-hours
across 3.96 hours with activity, or 3.32 concurrently active agents on average during
that union.
The 33,072.590 seconds of parallel overlap are the difference, not additional
wall time.

Within that interval, the retained lower-bound model stream is 16,454.464 seconds,
command-tool activity 4,490.837 seconds, and 18 compactions total 2,420.620 seconds.
These categories are recursive client measurements, can overlap, and are neither
provider inference latency nor process CPU. They must not be summed into an elapsed-time
claim. The snapshot has two live sessions and excludes final closeout, so it remains a
lower bound on the task tree’s eventual total.
Source logs contain no Git branch field; Session 165 explicitly attributes this interval
to the research branch.

The observed bottleneck is therefore broader than proof arithmetic: mathematical
analysis, review, context retention and repeated record integration consume substantial
time. A future W5 pass should reduce duplicated context and consolidate registry/view
updates while preserving independent review and immutable target criteria.

## Review Level and Next Work

The exact outputs have independent implementation checks and Astra max mathematical,
code and receipt reviews, with coordinator reconciliation.
Independence is specified per component: the root checker shares the contraction method;
the interval auditors trust the accepted root and reviewed symbolic identities; the
occupancy auditors use a different arithmetic formulation.
No proof-assistant verification or human referee confirmation is claimed.

The next n17 priority is `think-11ma`: preregister one small exact geometric
discriminator for the closed occupancy domains below the endpoint, with an independent
certificate checker.
This is preferable to launching a broad 20-million-case enumeration without a measured
leaf-exclusion method.
`think-wrgx` retains the stopped stress instrument; `think-am9e` retains the arithmetic
benchmark. These are separate obligations with unchanged scientific acceptance
requirements.

The scientific and export checkpoint `4f312e21e` passed all scheduled hosted checks,
including `packing-required`, `pages-required` and `merges-into-main`. Deferred jobs
skipped by scope are not claimed as executed.
The final record-only checkpoint is checked separately in PR265.

The fixed overnight deadline is 15:00 UTC on October 1, with finalization from 14:30
UTC. No new research starts during finalization.
[PR265](https://github.com/jlevy/squares/pull/265) remains stacked on
[PR261](https://github.com/jlevy/squares/pull/261); no merge or deployment is part of
this session.

## Scope Note After the Route Review

*Added 2026-10-01 by Session 166, after PR 265 merged.* The conditional-minimum row
above holds inside the H254 box, $S\in[4.675,4.676]$ with an angle window reaching
$0.17^\circ$ below the endpoint, not down to the lower bound $4.66044$. It assumes exact
common orientation of squares 9, 10, 11, 12 and 14, so it cannot be the terminal
theorem.
The [route review](review-2026-10-01-n17-route-after-pr265.md) found no error in
this report’s mathematics.
It also finds H258’s candidate stress valid in exploratory checks, and replaces the
`think-11ma` next entry with the BC-406 coordinator.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
