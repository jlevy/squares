---
type: is
id: is-01m5j6xtx90b07z09cavtqdgw4
title: "PR #727 A1: correct completed domain verification in migration plan"
kind: bug
status: in_progress
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-doc-fix
labels: []
dependencies: []
parent_id: is-01m5j10qmw6d55ghhfxg9ekww1
hold: null
hold_until: null
created_at: 2026-10-22T16:25:53.319Z
updated_at: 2026-10-22T16:27:10.611Z
started_at: 2026-10-22T16:26:06.436Z
---
Address senior Review A finding A1 (Low) on PR #727: https://github.com/jlevy/squares/pull/727#pullrequestreview-5617479538.

The Open Operational Items section at docs/project/specs/active/plan-2026-10-22-squaremath-domain.md:154 still instructs the operator to obtain the GitHub verification TXT value, although the owner verified domain ownership and Phase 2 marks that step complete. Remove the completed prerequisite, retain the requirement to preserve its TXT record, and leave DNS routing, TLS, legacy redirects, and live deployment checks pending.

Write scope: only that plan document. No DNS changes. Coordinator retains commit, push, and PR disposition publication.

## Notes

A1 working-tree correction completed in docs/project/specs/active/plan-2026-10-22-squaremath-domain.md:154. Replaced the completed TXT-acquisition instruction with pending Pages domain binding and DNS routing, explicitly preserving the existing ownership verification TXT record. Opening verified-ownership status and completed Phase 2 verification checkbox remain consistent; legacy redirects, TLS, and live verification remain pending. Applied pprose common/de-slop guidance; pinned flowmark-rs 0.4.0 formatting and git diff --check pass. No DNS change, commit, push, or PR reply. Awaiting coordinator commit and disposition publication before closing.
