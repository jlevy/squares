---
type: is
id: is-01m4p3at09yh81zwvqyx5pat9d
title: Move the files the added-blob guard grandfathers (over 5 MiB on main) to hosted data
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m44m1c47h22mb1g0kzppc54q
created_at: 2026-10-11T18:24:19.975Z
updated_at: 2026-10-11T18:24:19.975Z
---
The added-blob guard (devtools.check_added_blobs, PR #406, review A2) grandfathers every path whose blob at a pull request's base already exceeds the 5 MiB per-blob ceiling: changing such a file is the status quo, while a new large blob on a new path is refused. That was the owner's decision on 2026-10-11 ("Grandfather at base"), with this bead to move the grandfathered files out of Git into hosted data (OR-18; development.md, Publishing Hosted Data; python -m devtools.hosted_data).

Once a path leaves the tree it stops being grandfathered, so the exemption shrinks by itself as files move; no list is kept.

Overlap: the 13 oversized PDFs under packing/resources/papers/ are already published as data/source-pdfs-v1 by think-286j, and their removal from the tree rides the PR #403 -> #435 stack (think-okcb). Check that stack before moving any PDF here.

Needs a decision per group, not a mechanical move:
- packing/atlas/known-best/known-best-1-324.svg is generated and regenerated routinely (#462, #474): hosted data, splitting, or generation at build time.
- exp-29x/30x replay.json and certificate.json under packing/campaign/series/series-000-smoke-and-calibration/results/ (added 2026-10-07, after OR-18 was set): publish as a data release with a manifest, keep receipts in Git.
- the literature-refresh tarball and the n11 adaptive-source.json.gz receipts.

Paths over 5 MiB on main at 5b0eb012e (2026-10-11):
- packing/atlas/known-best/known-best-1-324.svg (7.6 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json (5.0 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-recovery-01-state.json (5.5 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/bc-306-unit-state-at-q.json (5.5 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-137-corner-dual-salvage.json.gz (11.0 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-atoms-2566-orbits.json (6.4 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/exp-222-n17-repricing-cells.jsonl (6.8 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.checkpoint.json (9.8 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.checkpoint.json (10.4 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.json (10.4 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-239-n17-endpoint-features/run-001/certificate.json (5.9 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-260-widened-lp-reconnaissance/run.json (18.6 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-289-complete-partner-coupling/structural-intake.json (6.8 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-291-complete-partner-coupling-amended/certificate.json (33.0 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-291-complete-partner-coupling-amended/replay.json (33.0 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-292-full-square-partner-coupling/certificate.json (33.2 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-292-full-square-partner-coupling/replay.json (33.2 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-293-guard-conditioned-ownership/certificate.json (9.0 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-293-guard-conditioned-ownership/replay.json (9.0 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-296-collective-row-coverage/certificate.json (5.8 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-296-collective-row-coverage/replay.json (5.8 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-297-regional-row-coverage/certificate.json (11.4 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-297-regional-row-coverage/replay.json (11.4 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-300-one-round-direct-regional-propagation/certificate.json (6.7 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-300-one-round-direct-regional-propagation/replay.json (6.7 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-301-one-round-fixed-core-regional-propagation/certificate.json (6.1 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-301-one-round-fixed-core-regional-propagation/replay.json (6.1 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-302-two-child-collective-propagation/certificate.json (16.3 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-302-two-child-collective-propagation/replay.json (16.3 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-305-case-preserving-owned-propagation/certificate.json (14.6 MiB)
- packing/campaign/series/series-000-smoke-and-calibration/results/exp-305-case-preserving-owned-propagation/replay.json (14.6 MiB)
- packing/resources/papers/antonova-yang-jatavallabhula-2022-rethinking-optimization-differentiable-simulation.pdf (12.0 MiB)
- packing/resources/papers/bender-muller-macklin-2017-survey-position-based-dynamics.pdf (29.4 MiB)
- packing/resources/papers/debnath-tiwari-sadekar-2025-rasp-shadow-guided-packing.pdf (7.0 MiB)
- packing/resources/papers/el-moumni-1999-optimal-packings-unit-squares.pdf (24.6 MiB)
- packing/resources/papers/klement-engel-2021-newtonian-event-chain-monte-carlo-collision-prediction-polyhedra.pdf (7.5 MiB)
- packing/resources/papers/macklin-storey-lu-2019-small-steps-physics-simulation.pdf (7.8 MiB)
- packing/resources/papers/maher-stillinger-torquato-2021-kinetic-frustration-2d-convex-packings.pdf (8.1 MiB)
- packing/resources/papers/mazhar-heyn-pazouki-2013-chrono-parallel-multiphysics-library.pdf (6.7 MiB)
- packing/resources/papers/muller-macklin-chentanez-2020-detailed-rigid-body-xpbd.pdf (19.2 MiB)
- packing/resources/papers/stuyck-chen-2023-diffxpbd.pdf (23.2 MiB)
- packing/resources/papers/wang-lu-2024-image-space-collage-and-packing-differentiable-rendering.pdf (22.4 MiB)
- packing/resources/papers/zhang-lyu-rudra-2026-sequential-object-placement-convex-decomposition.pdf (5.6 MiB)
- packing/resources/papers/zhou-he-zheng-2023-geometric-batch-optimization-equal-circles.pdf (16.3 MiB)
- packing/resources/web/literature-refresh-2026-09-05/s17-gt-89-20.tar.gz (41.8 MiB)
- packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-pilot/adaptive-source.json.gz (20.3 MiB)
- packing/resources/web/wand125-valid7-independent-check-2026-10-02/receipts/replay/wand125_shard01_1.jsonl.gz (5.3 MiB)
- packing/resources/web/wand125-valid7-independent-check-2026-10-02/receipts/replay/wand125_shard14_2.jsonl.gz (5.5 MiB)
