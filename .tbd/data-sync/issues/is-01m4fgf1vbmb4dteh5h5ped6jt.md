---
type: is
id: is-01m4fgf1vbmb4dteh5h5ped6jt
title: Keep collapsed Atlas previews on complete rows at every width
kind: feature
status: in_progress
priority: 1
version: 4
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
updated_at: 2026-10-09T05:15:49.420Z
started_at: 2026-10-09T04:59:31.236Z
---
Collapsed dedicated Atlas shows around100cases rather than a strict cutoff. In Grid choose a whole number of rectangular rows for actual responsive column count at every width and tile size; in Triangle finish complete mathematical square-number groups. Recompute onresize, size and view changes with shared layout/animation and persistent case links. Expandedalwaysall324cases, strictmaximum; neverdropcases tofilllastrow. Keep accessible counts/state, navigation targets, noJS and case popovers. Ownerexplicitlyconfirmed previewadjusts and all324 remain whenexpanded.

## Notes

Implementedsharedpre-arrange callback forview/size/resize. CollapsedGrid choosesnearest complete rectangularrowcount around100 usingactualCSScolumns; Triangle finishes100=10square-numbergroups. Existingboundaryanchorsmovebetweenvisible/restcontainers withoutclones; all324 remainstrictwhenexpanded. ARIAlabelsreflectcurrentpreviewcount. Opensteppedpopover preservesvisibleprefix forfocusreturn; layoutcompletesbeforecollapsescrollsettles. Focusedlive5casespassed36.40s at1280/390 inclresize/sizes/explicitGridreload/strict324/hash/noJS/persistentnodes/reducedmotion/homeunchanged. Regressionproof99casecollapsebuttonvisible andopenpopoverretains108after9columnresize/returnsfocus100. Measurementtoolreportsactualcounts/previewfilenames;14helpertests and41Nodechecks passed. Astraboundedreviewclean. Source/previewimplemented; publicationverification stillopen.
