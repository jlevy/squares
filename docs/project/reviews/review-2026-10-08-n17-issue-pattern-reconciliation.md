---
title: n17 Reported-Pattern Reconciliation
date: 2026-10-08
status: partial-intake
---
# n17 Reported-Pattern Reconciliation

The retained
[source snapshot](../../../packing/campaign/issue-intake/n17-20261008/github-issues.json)
and [result](../../../packing/campaign/issue-intake/n17-20261008/reconciliation.json)
incorporate all 33 explicitly reported #413 rows and both #358 classes as metadata.
Every count is **hypothetical combinatorial applicability**, conditional on the ordinary
cover at 1169/250. Certificate domain, custody, complete replay and admission remain
unjoined. No LP, proof target, bulk acquisition or registry change ran.

## Exact Join and Priorities

The frozen PR #404 baseline has 60 admitted classes, 36,768 surviving states in 4,683 D4
orbits; the distance-two subset is 95 orbits/744 states.
The first-eight pilot comprises canonical masks 849919, 850943, 851839, 851903, 916351,
980927, 981887, 1630207. Pilot state counts below include all 64 distinct D4 images, not
eight executed LPs.

| Pattern roster | Complete-residue applicability (orbits / states) | Distance-two applicability | First-eight applicability |
| --- | ---: | ---: | ---: |
| All 33 #413 rows, deduplicated union | 2234 / 17604 | 1 / 8 | 0 / 0 |
| #413 row 33 alone | 192 / 1520 | 0 / 0 | 0 / 0 |
| Row 33 marginal after rows 1–32 | 76 / 608 | 0 / 0 | 0 / 0 |
| #358 C1 and C2 union | 21 / 148 | 0 / 0 | 0 / 0 |

Only **row 23** matches a distance-two orbit, mask 1965787 (eight states).
Its class mask is 935012; source status remains **Computed**: a certificate is
unpublished and its generation/availability is unknown.
Prioritize a complete package/domain enquiry for that single orbit while retaining the
first-eight pilot unchanged.
Row 33’s 76-orbit fixed-order marginal matches the reported number under this declared
ordering; individual applicability is 192 orbits.
Its roughly 116-million-node/480 GB certificate remains an ungenerated estimate.

All 35 reported/companion classes are D4-distinct; none equals an admitted class or
contains an admitted smaller pattern.
Rows 15, 19 and 26 are strict subpatterns of the admitted Tail A/B whole assignments.
That reverse containment does not make the rows redundant.
Tail A/B are distance-eight admissions already removed from this baseline.
Individual projections overlap; the result retains ascending-row marginal counts, D4
equality, both strict containment directions and exact tail/pilot masks separately.
The endpoint assignment contains no D4 image of any candidate.

The
[row 14 correction](https://github.com/jlevy/squares/issues/413#issuecomment-6064272233)
identifies its omitted fast-verifier promotion: the current explicit roster is 22
certificate-verified and 11 computed rows.
The earlier 21/12 mismatch remains in the retained history, marked resolved by that
correction. The
[FULL retraction](https://github.com/jlevy/squares/issues/413#issuecomment-6064443079)
withdraws the former rows 3/4 standing FULL designation: they used parallel standing
node checks plus the fast verifier, and unmodified FULL did not fit in memory.
Only rows 1/2 and both #358 classes have current contributor-reported unmodified FULL
receipts. No maintained FULL replay or custody assurance follows from those reports.
The
[package update](https://github.com/jlevy/squares/issues/413#issuecomment-6051483962)
promises fresh standing receipts and regrouped objects.
Each changed manifest needs a fresh object/receipt join; names alone preserve no FULL
assurance. Complete closed independent-angle coverage and boundary/guard premises remain
required for every admission.

The
[contributor comparison](https://github.com/jlevy/squares/issues/413#issuecomment-6064503349)
also reports both census baselines, row 23’s single hard-tail orbit, and rows 15/19/26
inside Tail A/B. Its conditional remainder 19,164 states/2,449 orbits agrees with
subtracting this metadata union from the frozen 60-entry baseline.
It is a source-reported hypothetical subtraction, with no admitted census change.

## Reproduction and Controls

From `packing/`, using the project 3.14 environment:

```bash
uv run --frozen --all-extras --group dev python -m devtools.reconcile_n17_issue_patterns \
  --source campaign/issue-intake/n17-20261008/github-issues.json \
  --check campaign/issue-intake/n17-20261008/reconciliation.json
```

The maintained tool reconstructs the finite residue, joins the ledger/census, checks
endpoint distances, catalogue names and D4 action, and refuses missing/changed rosters.
It has a cooperative 60-second metadata-work ceiling and bounded input/output sizes.
Five focused tests cover equality versus containment, D4 overlap/marginals, unexplained
status promotions, repeated/unknown cells, changed cap, incomplete pilot and expired
deadline. The earlier capture/cache-disabled run passed in 5.40 s; the source-refresh
five controls passed in 17.68 s. Fresh reconstruction, focused Ruff and BasedPyright
checks also passed after the corrections.
Astra’s independent geometry review and reconstruction found no blockers.
The edit tier failed four steps in 390.56 s against its declared 240 s ceiling at a
non-reference host shape.
Missing PATH tools, pinned browser binaries and vendor/kpress files explain the
environment failures; the new review’s missing document-map entry was repaired with its
generated synopsis row.
No gate or ceiling was relaxed.
A later pytest FD-capture attempt hit external-scratch I/O error; the
capture/cache-disabled final controls are reported separately in the handoff.
The new files use the existing primary project interpreter with this worktree’s sources;
no environment or source file in the primary checkout was changed.

## Proposed Issue Updates

These drafts await the coordinator’s reviewed publication.

**#358:** The exact metadata join reproduces C1 = 14 orbits/104 states, C2 = 13/84 and
union 21/148, with zero distance-two or first-eight applicability.
Neither class duplicates a #413 row.
The maintained C2 FULL run remains INCOMPLETE 480.468 s; acquire/join the revised
complete packages and repair the measured guard before separately selecting full replay.

**#413:** All 33 explicit rows are now reconciled against the 60-entry baseline.
Their hypothetical union is 2234 orbits/17604 states; row 23 alone touches one
distance-two orbit, and none touches the first eight.
Row 14’s corrected promotion resolves 22/11. Rows 3/4 have parallel standing node checks
plus fast verification; current unmodified FULL reports cover only rows 1/2 and both
#358 classes. Please provide row 23’s certificate availability/domain alongside the
complete rows 1/2 packages; rows 3/4 need separate complete standing replay.
Row 33 remains ungenerated; its individual 192 orbits and fixed-order marginal 76
differ.

**#375:** Preserve the n17 certificate hold separately from already confirmed
other-count batches.
Its
[recorded disposition](https://github.com/jlevy/squares/issues/375#issuecomment-6007913483)
says it was not imported, replayed or recorded.
The later 324/324 source report and INVALID-script fix do not discharge that hold.
Request the exact immutable n17 rational object and matching commands for a bounded,
reviewed replay; numerical KKT evidence supplies no optimum.
The open held-certificate owner is `think-00e3`; the earlier generic import bead
`think-t6ok` is closed.

**#419:** The pinned exact-form catalogue contains n17’s degree 18 side/field,
configuration pointer and source `verify_exact`/`lean_packs` flags; its `lean_local_min`
field is empty.
Join that n17 packet to #403/#435’s polynomial/root identity intake, then
independently check exact configuration feasibility and retained Lean statement/receipt
custody. Source flags supply neither a local-minimum theorem nor global optimality.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
