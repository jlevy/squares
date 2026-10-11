---
type: is
id: is-01m42tjjknqbpm4n2rxvvn9n9f
title: Import wand125's 14 mixed certificates of 3-4 Oct (#282, n=42..95)
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m42sq026mszrdm4fwf5r8g8y
created_at: 2026-10-04T06:45:43.155Z
updated_at: 2026-10-06T08:32:58.548Z
closed_at: 2026-10-06T08:32:58.548Z
close_reason: "Superseded: the 14 certificates were retained (84274cc70, re-pinned e6e4fbb3c at 8aa6a10 with n69/n86) and registered as T-090 at V0/C1 (results.yaml, 16 counts n = 42..95). The ~146 CPU-h replay is owned by think-wpuu under think-wyf4, and the #282 reply by think-7gop."
resolution: canceled
duplicate_of: null
---
From #282 comments 5972753544..5977194758: mixed_n93_L988 (b321ac9) .. mixed_n95_L9965 (3554616); n = 42, 43, 44, 51, 56, 57, 67, 72, 75, 84, 88, 93, 94, 95, each above the record's reported value; 7 replace registered certificates (T-071 n84; T-082 n51,75,88,93,94,95). Runbook stages 1-4,7 (campaign/result-import.md): pin source head, packet wand125-mixed-bounds-2026-10-04, one new T entry (T-088 if #305 merges first), full replays with two mutated controls (~100 CPU-h), separately prompted review, acknowledgement then confirmation reply. Review checks: n=84 improvement_lower vs Green 9.26673353 upper enclosure (MX-2/LC-1), n=67 Green value misprint.
