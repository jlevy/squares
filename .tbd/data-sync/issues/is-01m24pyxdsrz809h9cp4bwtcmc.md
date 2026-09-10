---
type: is
id: is-01m24pyxdsrz809h9cp4bwtcmc
title: "PR139 R1: validate the corrected combined head with the full checkpoint"
kind: task
status: in_progress
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m24nswnk9b76cq0hdgenfceq
created_at: 2026-09-10T03:49:38.352Z
updated_at: 2026-09-10T05:05:14.063Z
---
Fast34433755569 passed at58ee1782; deferred34433755622 skipped substantive lanes. After corrections freeze, run one full checkpoint, verify checkoutSHA/base/headparents and constituent results, and link evidence to PR139. PR147 full34430565799 already passed and must not be rerun. ReviewR1: https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994

## Notes

The corrected PR139 head is d21c27b90be18ba5e96d2e712e673c0b30efd9a2. Hosted full run34437682106 uses synthetic merge6dbd4839c20f7b822bc38c424fd92df9771c1ebc, with exact parents main1c1db463447cb08f8987d3355ba32a1c72ccd31a and d21. Both revisions have Git tree10bdc9bb4e42c7ec7f6e8ebef6ec88365894497f.

Sol verified successful screen and slow jobs and the completed deferred selection. The dispatch used main's older workflow, so its deferred-steps job ran four rather than eight steps. The four new T024/T026720/1440 checks are therefore not covered by that aggregate. Root launched those exact four current packing-validate selections locally on the identical clean tree, with jobs2 and inner-jobs2; session52259, log /private/tmp/pr139-certificate-supplement.log and artifacts /private/tmp/pr139-certificate-supplement-artifacts. This is a coverage supplement, not a blind repeat or a full pass yet.

Before closure: require all four supplemental checks, the hosted exhaustive job and aggregate, and the matching current fast surface. Publish a union-of-coverage receipt that distinguishes the workflow revision from its checkout, plus all verdicts and source identities. Fix the misleading dispatch guidance and obsolete seven-deferred-step wording in the next bounded documentation/efficiency slice; do not mutate the source while these numeric checks run.
