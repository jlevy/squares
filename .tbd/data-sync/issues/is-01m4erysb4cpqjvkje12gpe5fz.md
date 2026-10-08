---
type: is
id: is-01m4erysb4cpqjvkje12gpe5fz
title: "PR454 B1: clean private staging after handled publication failures"
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
hold: null
hold_until: null
created_at: 2026-10-08T22:08:19.298Z
updated_at: 2026-10-08T22:09:22.611Z
started_at: 2026-10-08T22:09:22.611Z
---
Security B1 Medium at64/ecb: installed strif.atomic_output_file leaves destination-local staging when Path.write_text partially writes then raises OSError; main returnsrefused and finaldestinationpreserved but resource residue persists. Own exclusiveprivate staging/completewrite/atomicreplacement/finallycleanup using maintainedlower-layer helper ifavailable. Preservefirsterror and exposecleanupfailure; tinyinjectedpartialwrite/cleanupcontrols. No strongercrashdurabilityclaim/nocapchange. Review https://github.com/jlevy/squares/pull/454#pullrequestreview-5463425903.
