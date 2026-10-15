---
type: is
id: is-01m4wtv34pphy5w434wk13b85x
title: Resolve four scheduled main test-time ceiling overruns without weakening assertions
kind: bug
status: in_progress
priority: 1
version: 23
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
child_order_hints:
  - is-01m4wzs72rh8db5f4mp5y8w4wr
  - is-01m4x4c32d5wdje51ep66pbzmm
  - is-01m4x4c3gx5fggqnt3ha5v8gpw
  - is-01m4x5q04a41ca6rsj99gpd11d
  - is-01m4x9zbx706gftwnvmxgsnd0g
  - is-01m4xatk8zfjpdxv9kq2gv4yn1
  - is-01m4xes8ehmmxzpjctygnawq8h
  - is-01m4xjdycq4m3d047sdrdcfba9
  - is-01m4xjdytsg7x53t8pg6zja54b
  - is-01m4xjdz83t1r1pk7kcw3cvsaj
  - is-01m4xk1h2skppdp58y4zr0kvph
  - is-01m4yezgymfksx798467evpv4h
  - is-01m4yf4yff5se96qajm94jvwdy
  - is-01m4yf4ywh62ajt7cc9zfbcjcn
  - is-01m4yf4z92dxbp2k4amma0mrq3
hold: null
hold_until: null
created_at: 2026-10-14T09:10:37.460Z
updated_at: 2026-10-15T00:24:47.137Z
started_at: 2026-10-14T10:03:10.224Z
---
Optional scheduled full integration run38536321398 at f73 passes functional tests but violates12s per-test ceiling for four nodes: site_forwarders no-script redirect13.08s; results_register full-part citations T15312.17s; overview_sections no-script canonical atlas20.10s; regularized_drawings edited-block check13.44s. Main push full gate and Pages deployment passed sameSHA. Diagnose full integration contention/cold-path cost, optimize or explicitly classify measured expensive cases while preserving assertions and meaningful CI coverage; avoid broad ceiling increases.

## Notes

Latest checkpoint2026-10-14: remotePR599head08d23c06 remainsfailed strict38597483408; no speedup/merge-readyclaim. Local078512df457d0743d6604e9f53f87cf768f883b7 cleancommitaddsbounded8-file recorded-cost-first native loadfileordering with explicitno-loadscope-reorder. IndependentAstraPreliminaryM caughtactualxdistworker dist=no handoffbugM1 andmissingpublicationexemptionM2; bothfixed andfollowupM hasnofindings onall8paths. Real2workerregression passed1test2.65s, all12syntheticnodesexactlyonce heavyfirstonbothworkers withsupportedmetadata. Bothaffectedregisteredcontrol positivespassed1each; bothregisteredmutantsrejectedexpected1failureeach throughmaintainedrunner, allfourchildJUnits0errors0skips. Uniqueevidence .codex/regularization-closeout-evidence-2026-10-13/ci599-controls-current/ andM-followup. Localcheckpointnotpushed toavoidduplicatedhostedcohorts beforeNews604lands. Next integrateNews604main preserving25rewrittenentries/topics/site0.7, confirmcombinedsource/releaseimpacts, publishcurrentheadreviews andrunappropriatecurrentstrictcohort/frontend. Currentordinarymain37 separatelyunchanged. SystemicCI/overnightretrospectiveisAstra-authoredconcreteplan docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md committeda1ddb6f22 separatebranch think-kxmq/d4ub.900deadline rootcauseunproved think-ma3y;210ordinaryrequiredChromeomissions think-zvp7. Neitherfailurefixedbyraisingceilings.
