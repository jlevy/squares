---
type: is
id: is-01m5j6xtx90b07z09cavtqdgw4
title: "PR #727 A1: correct completed domain verification in migration plan"
kind: bug
status: in_progress
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-doc-fix
labels: []
dependencies: []
parent_id: is-01m5j10qmw6d55ghhfxg9ekww1
hold: null
hold_until: null
created_at: 2026-10-22T16:25:53.319Z
updated_at: 2026-10-22T16:26:06.438Z
started_at: 2026-10-22T16:26:06.436Z
---
Address senior Review A finding A1 (Low) on PR #727: https://github.com/jlevy/squares/pull/727#pullrequestreview-5617479538.

The Open Operational Items section at docs/project/specs/active/plan-2026-10-22-squaremath-domain.md:154 still instructs the operator to obtain the GitHub verification TXT value, although the owner verified domain ownership and Phase 2 marks that step complete. Remove the completed prerequisite, retain the requirement to preserve its TXT record, and leave DNS routing, TLS, legacy redirects, and live deployment checks pending.

Write scope: only that plan document. No DNS changes. Coordinator retains commit, push, and PR disposition publication.
