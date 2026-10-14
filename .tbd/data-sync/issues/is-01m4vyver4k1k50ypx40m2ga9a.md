---
type: is
id: is-01m4vyver4k1k50ypx40m2ga9a
title: "Document independence of confirmations: structured independence record, an independence ladder, and registering every run's code"
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m4v5ne8b1dq1gyybx5mj689d
created_at: 2026-10-14T01:01:29.218Z
updated_at: 2026-10-14T02:11:28.894Z
---
Owner, 14 October 2026: 'I'd like to make sure the validation we do that's independent is documented, and the degree to which it's independent is also documented. Was this the same code, or is this all independently validated with our own code? Level of confidence in the confirmation should be a matter of process that we document.' Change epistemics.md (Which Code Confirmed It) and packing/campaign/result-import.md stage 4: (1) a structured independence record required for each new confirming run (what its authors read: mathematics, proof text, specification or the producer's code; clean-room or not; shared components; authors, people and AI models with versions, and whether the lineage overlaps the producer's; coverage, full or N of M); (2) a documented independence ladder saying what each level rules out (reproduced with the producer's code; shared components; independent after reading the producer's code; clean-room from the mathematics), with coverage and authoring diversity as separate attributes; (3) any review or lane that runs code retains and registers it with that record, or states that the run decides nothing; (4) devtools.verifier_registry refuses a new independent entry without the structured record. Lands in the formalization follow-up PR (think-8e0p), after the writer finishes; sub-agent review before merge.

## Notes

2026-10-14, writer lane on claude/stoic-clarke-jhfnru (local commits, not pushed): 071987e8b and 407849ead. epistemics.md: The Independence Record (independence block: read, clean_room per program, shares, written_by by system family, overlaps_producer with separate_prompt and separate_code; coverage on evidence), The Independence Ladder (four levels, coverage and diversity beside, the order in which stated confidence follows), Every Run's Code Is Kept. verifier_registry refuses a first-party decider or a new independent entry without the record (42 programs and 187 entries exempt by name, lists only shrink); check_results counts no sample toward a rung. Tests in test_verifier_registry.py.
