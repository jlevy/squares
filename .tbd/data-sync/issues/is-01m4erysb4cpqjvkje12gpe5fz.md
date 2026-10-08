---
type: is
id: is-01m4erysb4cpqjvkje12gpe5fz
title: "PR454 B1: clean private staging after handled publication failures"
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
hold: null
hold_until: null
created_at: 2026-10-08T22:08:19.298Z
updated_at: 2026-10-08T22:32:08.163Z
started_at: 2026-10-08T22:09:22.611Z
closed_at: 2026-10-08T22:32:08.163Z
close_reason: "Exclusive destination-local staging now handles short writes, cleanup and secondary diagnostic preservation. Reviewed70e7 repair identical at publisheda7ce. Seven publication controls within whole18 PASS; static clean. B1 disposition: https://github.com/jlevy/squares/pull/454#issuecomment-6070354200 . No stronger crash-durability claim; shared CIqualification remainsopen."
resolution: null
duplicate_of: null
---
Security B1 Medium at64/ecb: installed strif.atomic_output_file leaves destination-local staging when Path.write_text partially writes then raises OSError; main returnsrefused and finaldestinationpreserved but resource residue persists. Own exclusiveprivate staging/completewrite/atomicreplacement/finallycleanup using maintainedlower-layer helper ifavailable. Preservefirsterror and exposecleanupfailure; tinyinjectedpartialwrite/cleanupcontrols. No strongercrashdurabilityclaim/nocapchange. Review https://github.com/jlevy/squares/pull/454#pullrequestreview-5463425903.
