---
type: is
id: is-01m1w3p6hhmhnjqakekbqwa82f
title: Provide retained Git history to deferred review checks
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T19:38:54.384Z
updated_at: 2026-09-06T19:38:54.384Z
---
New PR97 slowTrump review reads exactretainedtheorem/archivebytes with gitshow. Both commits/pathsexist and aremainancestors, but deep-gate deferredcheckout remainsdepth1 under obsolete onlyprovenanceneedshistory assumption. PR98run34054616340 slowtestfailsmissinghistoricalobject; mainintegrationfetchesfullhistoryandpasses. Usefetch-depth0 fordeferred job andpinits requirementwithfocusedworkflowcontract. Preservefrozenrefs/paths anddo notfallbacktoHEAD orskipreview.
