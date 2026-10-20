---
type: is
id: is-01m4x4c3gx5fggqnt3ha5v8gpw
title: Keep the complete malformed-coverage schema gate within the enforced call ceiling
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-14T11:57:12.092Z
updated_at: 2026-10-14T13:35:07.154Z
started_at: 2026-10-14T11:58:08.714Z
---
Actual PR599 complete run38555598547 head472 malformed coverage schema-gate call12.100s/CPU lower11.40s violates unchanged12s ceiling. Retain full evidence document, malformed list field, whole validate_schemas main and exact diagnostic assertions. Replace slow safe Python serialization with semantically equal safe C emitter/fallback, prove whole-document round trip and gate refusal in measured call; no hidden setup, schema narrowing, marker or ceiling changes.

## Notes

Csafeemitter and wholeloadroundtrip are semanticallycorrect but actuale709full CALL13.42s stillfails12s. Strongread-only profile total11.22/main10.70,1287artifactchecks7.46,YAMLparse7.97overall,defectchecks2.00;fixtureparse/dump/roundtrip0.52. Do notpretend emitter-onlyfixsufficient. Diagnose repeatedparsedoc/schemawork in actualcompleteproductionaudit and optimizeboundedinvocation reuse while preserving duplicatekeyrefusal, allartifacts/schema checks, cross/defectchecks, diagnosticcollection and gateexitcode. No skipped/narrowed wholeaudit or hidingcostinsetup. Rootowns source correction; strongindependentreview and realhostedfloor proof required.
