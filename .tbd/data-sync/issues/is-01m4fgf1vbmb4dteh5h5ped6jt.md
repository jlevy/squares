---
type: is
id: is-01m4fgf1vbmb4dteh5h5ped6jt
title: Keep collapsed Atlas previews on complete rows at every width
kind: feature
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T04:59:09.544Z
updated_at: 2026-10-10T18:55:57.176Z
started_at: 2026-10-09T04:59:31.236Z
closed_at: 2026-10-10T18:55:57.176Z
close_reason: |-
  Completed the reviewed implementation and CI repair published in PR462 (https://github.com/jlevy/squares/pull/462) at exact head d3c99face8fa81fd6ad265111265e4f6a6067106. The coordinator's sole final CI watch exited 0: 31 PASS, 26 intentional SKIP, 0 failures, 0 pending; frontend PASS and all final-head checks green.

  Final behavior supersedes stale descriptions: single centered n=53 hero; homepage Triangle preview 36→100→324→36; About H1; inline homepage video; complete Atlas and Frontier Survey, shared navigation/design and case/result previews retained. The canceled scientific PDF change is excluded. No assertion, 300ms startup bound or scientific content is changed by this closeout.

  Earlier local 901-second incomplete validation and the 195c80948 startup failure remain preserved in prior notes and durable receipts; final hosted success does not relabel those runs. This closes implementation and CI-repair beads only. Full checkpoint think-xio5, epic think-2u4x, process owner think-ht59 and scoping follow-up think-9k61 remain open.
resolution: null
duplicate_of: null
---
Collapsed dedicated Atlas shows around100cases rather than a strict cutoff. In Grid choose a whole number of rectangular rows for actual responsive column count at every width and tile size; in Triangle finish complete mathematical square-number groups. Recompute onresize, size and view changes with shared layout/animation and persistent case links. Expandedalwaysall324cases, strictmaximum; neverdropcases tofilllastrow. Keep accessible counts/state, navigation targets, noJS and case popovers. Ownerexplicitlyconfirmed previewadjusts and all324 remain whenexpanded.

## Notes

Implementedsharedpre-arrange callback forview/size/resize. CollapsedGrid choosesnearest complete rectangularrowcount around100 usingactualCSScolumns; Triangle finishes100=10square-numbergroups. Existingboundaryanchorsmovebetweenvisible/restcontainers withoutclones; all324 remainstrictwhenexpanded. ARIAlabelsreflectcurrentpreviewcount. Opensteppedpopover preservesvisibleprefix forfocusreturn; layoutcompletesbeforecollapsescrollsettles. Focusedlive5casespassed36.40s at1280/390 inclresize/sizes/explicitGridreload/strict324/hash/noJS/persistentnodes/reducedmotion/homeunchanged. Regressionproof99casecollapsebuttonvisible andopenpopoverretains108after9columnresize/returnsfocus100. Measurementtoolreportsactualcounts/previewfilenames;14helpertests and41Nodechecks passed. Astraboundedreviewclean. Source/previewimplemented; publicationverification stillopen.
