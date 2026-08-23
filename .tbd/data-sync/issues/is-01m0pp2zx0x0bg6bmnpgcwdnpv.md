---
type: is
id: is-01m0pp2zx0x0bg6bmnpgcwdnpv
title: README and SYNOPSIS duplicate the reports index and the exactness rationale
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pp24qsn326dyxy9na7wc50
created_at: 2026-08-23T06:49:19.520Z
updated_at: 2026-08-23T07:01:51.820Z
closed_at: 2026-08-23T07:01:51.819Z
close_reason: "Resolved as a split rather than a deletion, since the two indexes are at different granularity and different coverage. README keeps the six-row reports table (scope of each report, for someone browsing the directory) and now points at the synopsis's document map for the full document set including reviews, specs and the runbook. The map's rows stay one line each, saying what a document owns rather than what is in it, and its README row now says README carries the report index. Verified the two do not contradict. The real duplication -- README re-arguing why exactness is needed, which SYNOPSIS owns as 'Why Exactness Is Not Optional' -- is gone: README states the conclusion in three lines and links. Residual risk that the two indexes diverge is now partly covered, since check_readme.py holds README's table against docs/project/research/ and check_synopsis.py holds the map's links."
resolution: null
duplicate_of: null
---
SYNOPSIS's document map and README's Reports table both index the six research reports with differing one-line descriptions. README's 'Why exactness needs more than precision' and SYNOPSIS's 'Why exactness is not optional' make the same argument twice. SYNOPSIS's own map assigns README 'what is in the directory, and how to run it', so README should keep Use / Verifying another packing / Scope and defer the rationale and the full index. Decide the split, apply it, and make the map say it.
