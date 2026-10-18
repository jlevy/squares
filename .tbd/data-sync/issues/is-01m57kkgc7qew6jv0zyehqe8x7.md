---
type: is
id: is-01m57kkgc7qew6jv0zyehqe8x7
title: "Review exact-source mathematics for Evan Daniel n155 request #669"
kind: task
status: closed
priority: 2
version: 4
delegate: claude-code@spud10.local
labels:
  - result-import
dependencies: []
parent_id: is-01m5733t1298tmxrt5h2pw772s
hold: null
hold_until: null
created_at: 2026-10-18T13:35:47.590Z
updated_at: 2026-10-18T13:40:55.858Z
started_at: 2026-10-18T13:36:12.768Z
closed_at: 2026-10-18T13:40:55.857Z
close_reason: Completed bounded read-only mathematical/source review with findings and next steps in notes. Full replay, controls, mapped Stage 4 review and import remain owned by parent import beads; no V/C upgrade.
resolution: null
duplicate_of: null
---
Bounded read-only mathematical/source review of the retained n155 packet at upstream 59326b86291b76c39d843f3f156e8f25fa0f6e3f. Inspect standalone verifier soundness, rational certificate and numerical-side distinction, exact decimal rounding, and missing negative controls. No full certificate replay, no V/C rung, no source edits or GitHub comments. Import and final author response remain owned by think-n1ga.

## Notes

2026-10-18 bounded mathematical/source review, Codex strong tier, xhigh reasoning. Scope: packing/resources/web/evand-n155-explorer-2026-10-17/ at upstream 59326b86291b76c39d843f3f156e8f25fa0f6e3f. Workflow: tbd shortcut review-code-correctness plus review-code. Packet READMEs and import custody notes were read before the code; no earlier mathematical review was consulted. This is intake readiness work, not the mapped, isolated Stage 4 review or a complete certificate replay.

Verdict: no blocking mathematical error identified in the accepted-certificate implication for these well-formed positive-count certificates under the normal interpreter. Acceptance of the data remains untested here. No V/C rung is claimed.

Invariants checked by source reasoning: rational t gives c=(1-t^2)/(1+t^2), s=2t/(1+t^2), hence c^2+s^2=1 and orthogonal unit axes (source/search/exact/verify_cert.py:23-31). Wall extent e=(abs(c)+abs(s))/2 is exact; positive margins imply containment (39-43,63). On each unit face normal a, support radius is (abs(a.u)+abs(a.v))/2; a positive separating gap proves disjointness (55-63). Unit-square circumradius is sqrt(1/2), so centre distance squared >2 proves disc separation (51-52). The second checker constructs CCW corners, checks closed containment and proper/touching/collinear segment intersection, including coincident squares (verify_cert2.py:15-38,50-66). Strict contact rejection is conservative. The algorithms share authorship, Fraction arithmetic, format and disc shortcut; source self-checks do not establish outside independent confirmation.

Exact header expansion: S=12.952260944650564035267179660865, with 12.952260944650 < S < 12.952260944651. Both certificates have this side. The source S_exact=12.952260944650564035137657... is numerical and cannot replace S. The local-minimum/31-flat-mode report (s155_ex2.json:208) and regularized JSON verify_80.ok=true with min_gap=-4.8192e-70 are numerical diagnostics, not exact feasibility or local-minimality proofs. The display certificate needs its own replay despite sharing S.

N155-A (Medium, nonblocking for retained files): parser/invocation boundary. Both checkers use assert for row count. With assertions disabled, verify_cert2.py:49,50-67 statically accepts a header-only '1 0' with exit 0: the geometry loops are empty. This is a static trace, not an executed reproduction. Both parsers ignore surplus rows. Future replay wrapper should validate positive expected n and exactly n triples, require assertions-enabled execution, and test malformed counts. No source changes requested in this bounded slice.

Next step, think-n1ga: retain complete exact replays for each consumed original/display certificate and two rejected geometry mutants per original/checker: duplicate the first square into the second row; set one centre x=0. Include an analytic passing control and touching/collinear refusal controls. None ran here. Resolve regularized.json's Couzo attribution before consuming it; preserve the explicit Ostashev start credit. Formal Stage 4 review and receipts remain pending.

Evidence: nl -ba read both full verifiers; cmp against both n229 packets exited 0 for each; head read certificate headers; wc -l reported 157 for each n155 certificate; jq inspected numerical report fields. No source program was imported/executed, no gate/test ran, no source/worktree file or GitHub comment was written. Related n229 review: think-dcvm. Import owner think-n1ga was not edited or reclaimed.
