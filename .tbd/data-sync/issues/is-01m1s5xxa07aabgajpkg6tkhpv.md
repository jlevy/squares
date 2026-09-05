---
type: is
id: is-01m1s5xxa07aabgajpkg6tkhpv
title: "Atlas: lower-bound line and new-result stars on the 1-100 composite"
kind: feature
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T16:20:20.928Z
updated_at: 2026-09-05T16:20:35.919Z
closed_at: 2026-09-05T16:20:35.919Z
close_reason: "Done in f5de1929. Survey (sub-agent) produced a verified 100-row table with file:line citations: 35 exact, 7 first-party lower bounds, none missing. Implemented through the figure record rather than the drawing: build_composite_figure_data gains a 'lower' field (value, shown, display, first_proved_here, evidence) and a lower_bound_first_proved_here total, schema extended, star criterion read from evidence.yaml typed fields (claim lower-bound, performed_by repository, novelty apparently/confirmed-novel) giving n=11,12,17,18,19,20,21. Display truncates toward zero because the stored 12-digit literals round to nearest and would overstate 33 bounds. Star drawn as a polygon because Helvetica substitutes render U+2605 as tofu. Canvas 2676->2846 keeping every clearance. PNG now drawn by cairosvg, fixing a pre-existing defect where ImageMagick set the italic s on top of the ( in every bound line. Consumers updated: explainer img dimensions, alt and caption (count derived), README, atlas README, FIGURE-PLAYBOOK. All drift gates and 47 tests green."
resolution: null
duplicate_of: null
---
Owner's direction 2026-09-05: show both bounds on every cell of the top-level 100-packings figure, star the lower bounds new to this project, put the star in the legend in a distinctive palette colour, verify the bounds systematically against the frontier documents first, and regenerate the PDF.
