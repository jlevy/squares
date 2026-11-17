---
type: is
id: is-01m5b0b16d78pyv7jb4b5bqs28
title: "Attribute the Animate view play-check message ('play did not carry on from step to step: the stage showed n = [5, 6]') to load or to a regression (#538)"
kind: bug
status: closed
priority: 3
version: 5
delegate: w-records-1026
labels:
  - testing
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-19T21:16:04.685Z
updated_at: 2026-10-26T10:25:22.688Z
started_at: 2026-10-26T10:18:08.310Z
closed_at: 2026-10-26T10:25:22.687Z
close_reason: "Attributed to load in #827 (abdbaf95a, merged at 909ddc76e): 6x CPU throttling reproduces the exact play message with play still running; the play check now waits on the page's clock and reports frames, slowest frame and clock, so a stop is told from load. #538 closed with its final reply (issuecomment-6413623627)."
resolution: null
duplicate_of: null
---
Narrowed from think-1bm2 (#538). The trajectory timing half of #538 landed in #685 (02b644c6f, merged 14fd9e27f): best of three fresh builds against 400 ms, ceilings unchanged. Neither #685 nor earlier work attributed the second message #538 records: on #546 the Animate view check (check_animate_view.plays_across_steps, 3.5 s of real play) failed twice locally at 8a5e72e65 on a host at load 13-18 over 4 CPUs with 'play did not carry on from step to step: the stage showed n = [5, 6]', while hosted frontend passed at the same commit (run 38229096917) and #546 changed no workbench code. n and n + 1 only is also the signature of the 2026-09-21 regression that stopped playback after the first step. Done when the next occurrence (or a deliberate loaded-host reproduction) is attributed to load or to a regression in this bead, with the run, host load and stage sequence, and #538's record and reply say so.

## Notes

2026-10-19 lane-645 (review G2 on #646): after #646 merges, post the #538 follow-up rendered from main with `check_requests --draft 538`: the timing ask is done in #685 (02b644c6f, 14fd9e27f; frontend job 118266427235), the play ask is queued on this bead, and close_when narrowed to the play attribution. This bead answers #538 from then on.
