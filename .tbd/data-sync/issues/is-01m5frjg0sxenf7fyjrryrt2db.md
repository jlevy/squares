---
type: is
id: is-01m5frjg0sxenf7fyjrryrt2db
title: Include evidenced years in profile biographies
kind: task
status: closed
priority: 2
version: 6
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T17:36:32.792Z
updated_at: 2026-10-21T21:45:33.739Z
started_at: 2026-10-21T17:36:39.880Z
closed_at: 2026-10-21T21:45:33.739Z
close_reason: Completed bounded implementation, reviewed evidence and local/hosted feature acceptance. Final-head CI and separate runtime/evidence followups remain open.
resolution: null
duplicate_of: null
---
Review profile biographies, starting with Thierry Gensane: include evidenced years for dated work and link named papers/projects to retained source or tracking pages. Use existing biography sources, keep one concise paragraph of at most five sentences, preserve supported identity metadata and avoid redundant handle filler.

## Notes

Seven existing biographies now include evidenced years and named-work links; 38 empty biographies unchanged. All 45 profiles load; seven softschema checks valid with no repairs; whitespace check clean. Awaiting integrated build and PR publication.

Completed the bounded biography cleanup: all seven existing nonempty biographies include evidenced work years and named-work links, retain one paragraph of at most five sentences and explicit bio_sources, and avoid unsupported identity or account filler. Gensane/Ryckelynck use the 2005 publication year rather than the DOI/copyright year; the 2004 spheres paper remains distinct. The other biographies preserve the retained publication chronology and qualifiers. Empty optional biographies were not invented. Seven SoftSchema checks passed without repairs during the edit; the complete 75-profile loader/schema and rendered biographies passed later integrated validation and hosted tests.

Final integration evidence: the scoped work is committed and published in https://github.com/jlevy/squares/pull/578, currently at db3cb6d4fe5f00a44d04a8ef91018aa2b365bad8. Hosted validation at e162a870a899a61cc77cd47fa2f56c0ff388c8ea passed Pages, Packing Validate and suites B/C; suite A passed all 4,364 assertion tests, then failed only the separate project-tally CALL wall guard. That independent runtime defect is fixed in e3e33171bf1d687190cc957a40e25fbbc9dbb23c and remains tracked by think-rolz while final-head CI runs. The exact final db3 CI verdict is not claimed here. This closure is for completed bounded acceptance; the overall think-zpfo handoff, think-uwd6 coverage parent, historical registrations, pending PDF census and real evidence gaps remain open.
