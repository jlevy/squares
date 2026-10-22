---
type: is
id: is-01m5gh8r272jj3mnamermgjyst
title: Reconcile profile attribution after T-223 adoption and T-225 integration
kind: task
status: in_progress
priority: 1
version: 3
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:48:07.750Z
updated_at: 2026-10-22T00:57:26.781Z
started_at: 2026-10-22T00:49:15.962Z
---
Reconcile exact profile attribution after upstream d7923b8d8: T-223 adoption at n204/n260 and T-225 Daniel regularized views. Resolve the assigned additive adopt_houses, resource-index and generated RESULTS/SYNOPSIS conflicts, retaining both branch behaviors and canonical output. Reconcile source-reviewed existing-profile spans and source-specific evidence without fuzzy identities or new historical results. Preserve original authorship, prerequisite roles, assurance lanes and raw source text. Validate census/schema/model/source/citation behavior; coordinator owns release, URL, merge, build and final CI work.

## Notes

Data/source write freeze for merge of origin/main d7923b8d8a8def4d6b738608910211d8d4f295bc (PR #706 T-223 adoption and PR #716 T-225). The coordinator expanded this worker's owned conflict set to packing/devtools/adopt_houses.py, packing/resources/README.md, packing/frontier/RESULTS.md and SYNOPSIS.md, plus exact occurrence/evidence reconciliation. The additive adoption conflict retains both our _n29_history and upstream _STAGED_SENTENCE/staged_history because merged callers use both. The resource index retains the new T-225 packet row and canonical Hosono wording. RESULTS and the SYNOPSIS result-headline/document-map blocks are canonical and conflict-free. Only assigned paths were staged; no commit or push by this worker.

Canonical contributor reconciliation removed two current-case n204 improver fields (PingYou Ltd and Mishapolk) that upstream removed; prior packing lineage remains in result sources and case history. It proposed two replacement Francisco Couzo finders at n204/n260 and six new [Daniel regularized lists 2026-10-20] bibliography spans. All eight were reviewed and bound to existing profiles, preserving raw labels, offsets and roles. Daniel is the sole source author; Couzo, de Winter, Polkovskyi and Levy are prerequisite credits. The retained new packet CREDITS.md explicitly names Joshua Levy (jlevy), so that source-specific personal evidence was added to his existing profile as daniel-regularized-credit. Unrelated collective-project Levy exceptions remain unresolved. The canonical reconciliation tool also reflowed existing notes without changing their values. No mathematical record was rewritten and no new profile or historical result was invented.

Final counts: 75 profiles; 1,524 structured spans plus 10 manual origins, 1,534 total. Structured dispositions are 1,440 resolved / 77 non-person / 7 unresolved. Census --stale is empty. Reviewed primary-authored Results increase from 213 to 214 and person-result Credits from 701 to 705. There are 115 current Records primary-authored by profiles and 117 global current Records; global-only T-174/T-195 have corporate source ownership. The five previously unassessed IDs remain unassessed. T-225 is the only newly current ID and has four reported facets; verified lane ownership stays T-223 at 204/260, T-196 at 227 and T-199 at 229. The split Couzo source-coverage rows do not duplicate T-223 ownership or counts. The 146-PDF pending inventory is unchanged.

Validation: 72 focused tests passed in 38.72 seconds across contributor occurrences, site tallies, profile coverage, Records, the T-225 regularized packet and both n29/staged adoption-history controls. adopt_houses BasedPyright reports 0 errors, 0 warnings, 0 notes; Ruff and format checks pass. Canonical bound-citation check passes. Source coverage reconciles 324 cases, 371 superseded reports, 309 tracked beyond horizon and 580 printed facts with 0 divergences. Canonical RESULTS, SYNOPSIS headline and document-map checks pass, and assigned paths pass git diff --check. Astra independently reviewed semantic occurrence changes, original authorship, exact lineage and lane ownership without a blocker. Frontend was notified once the manifest was frozen so it can rerun its one blocked resource check.

Read-only CLI receipts are upstream-706-716-occurrence-reconcile.json, upstream-706-716-census.json, upstream-706-716-profile-coverage.json, upstream-706-716-profile-coverage-full.json and upstream-706-716-profile-records.json under /Volumes/spud-ext2/agent-scratch/about-profiles-20261020. The authored/global Records distinction is the intersection of the reusable coverage and Records JSON outputs. Coordinator owns merge commit, release pin, source-custody budget, full gates, build and final-head CI; this bead remains in progress until that integration acceptance is recorded.
