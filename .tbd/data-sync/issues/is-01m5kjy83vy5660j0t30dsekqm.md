---
type: is
id: is-01m5kjy83vy5660j0t30dsekqm
title: "Tracker audit 2026-10-23 part a: open and in-progress result-import beads (scratchpad audit/part-a.txt)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-audit-a-1023
labels:
  - audit
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T05:15:04.187Z
updated_at: 2026-10-23T05:34:23.472Z
started_at: 2026-10-23T05:15:05.197Z
---

## Notes

# Tracker audit, part a (c-audit-a-1023, review bead think-s4ld)

Read-only audit of 70 beads against origin/main 31584003e, 2026-10-23. Main moved to
44df28b07 (#743) during the audit; `git diff` shows that change touches nothing under
packing/frontier, packing/campaign or epistemics.md, so the findings still hold. One row
per bead is in `result-a.tsv`.

## Counts (primary class)

| class | n |
| --- | --- |
| DONE | 19 |
| ACTIONABLE | 20 |
| WAITING-OWNER | 15 |
| EPIC-OPEN (epic waiting on open children; not a brief class) | 6 |
| SUPERSEDED/DUPLICATE | 5 |
| WAITING-COMPUTE | 2 |
| WAITING-EXTERNAL | 1 |
| STALE-CLAIM as primary (think-u1kq) | 1 |
| UNSURE (think-mt6e) | 1 |

STALE-CLAIM, counted across all classes: 23 of the 24 in_progress beads (every in_progress
bead except think-om5l). None of them has a 2026-10-23 delegate.

**Close now (DONE or SUPERSEDED, nothing names them in a live record deferral):**
think-3jsj, think-znpk, think-jl4z, think-0fkt (also edit T-097's prose),
think-krbs (also edit T-088/T-089's prose), think-1qms, think-klm7, think-1cvf,
think-1545, think-o061, think-utky, think-8wie, think-tln9, think-ijv2, think-mtwe,
think-ffh8, think-ghbx. Close after re-parenting children: think-zcnr (dtun, 2uc1),
think-fvz4 (j1a4), think-l360 (upzs), think-edo8 (with 0mlq).

**Close only together with a record edit (live deferral, `check_bead_tree` invariant 3):**
- think-3oi5: move #485's answer_bead to think-xzob.
- think-jpre: close #470 first. It is closeable per `--report`, and its final reply already
  says it is closed.
- think-om5l: update the franciscouzo read through 337078c.

## ACTIONABLE, by value

1. **think-jpre / #470.** Close the issue and record `closed`. Minutes.
2. **think-wop1.** Register s(31) >= 2391/400 and replay it with sqverify-fast (about
   2 CPU-h). Hours. Raises n = 31 if confirmed.
3. **think-nd7g.** T-144 linear replay, 11.2-14.6 CPU-h, under the 40 CPU-h cap. The
   tooling must first be landed from unmerged claude/wand125-confirmations-2026-10-11
   (7 ahead, 3057 behind). A PR plus about 7 h wall.
4. **think-eth9.** One register entry for #446's four values at n = 19, 20, 26, 27. About
   1 h, no CPU. The n = 19 value is superseded on entry by T-194.
5. **think-63vx.** #419 Lean build of the 41 asked counts (2.1 process-h, under the cap),
   then evidence entries for T-120..T-124. A PR.
6. **think-oyd4.** Evidence entry and T-049 next_rung fix now (1 h). The 7.3 CPU-h build
   needs a host with 32 GB or more.
7. **think-xk3f.** Retain the s(59) = 8 Lean proof at f9a77b7 and price its build. 1-2 h.
8. **think-f2bm.** Retain wand125's hypothesis-free s(21) Lean proof (77636c63) for T-055.
   1-2 h.
9. **think-jtlq.** Three evand beyond-horizon rows (964, 1092, 1228). 1-2 h.
10. **think-kf3o.** Format T route to T-046: about 1.4 CPU-h, plus a review and a mass-rule
    decision. Hours.
11. **think-du1e.** Make bead required for queued items in the schema (every queued item
    already has one). 30 min.
12. **think-g6d5** (merge with think-0qrn), **think-506q** and **think-j5so**. Three gate
    PRs of 1-4 h each, no CPU.
13. **think-ri84.** Re-check and fix the --draft defects. Hours.
14. **think-nr59.** Refuse a one-word significance.by. Minutes.
15. **think-u1kq** via think-k3tk (Lemma 4.10 re-implementation), **think-5i1z**, **think-daa8**
    with think-4kng folded in, **think-4qga** and **think-j0dd**. Optional or low value.

**Parallelism with #742, #736 and the #719 branch claude/intake-2026-10-23:**
- Gate and tool PRs run in parallel: g6d5 (only its new check; the coverage entries
  conflict), 506q, j5so, nr59, ri84 and mt6e's negative control.
- Records PRs that touch source-coverage.yaml, results.yaml or result-requests.yaml
  should follow those merges: jtlq, eth9, wop1, f2bm, xk3f, oyd4, du1e, and the three
  deferral edits above.
- CPU runs (nd7g, wop1, kf3o) can start at any time, but they are heavy for a shared
  host.

## Owner questions found

- #543 (all boxes unchecked):
  - RR-1 (think-18b8).
  - D1-D6 (think-66e5).
  - Policy paragraph and three pairs (think-qh3s).
  - Check2 candidates in Git (think-r333, think-i85v).
  - T-142 control tolerance (think-i85v).
  - Valid7 sample or rebuild (think-0ayk).
- n = 17 suspension of 2026-10-13: lift or keep. This gates think-x4v4, think-ybmt,
  think-lkbe and think-nmfl.
- think-7hq0: may the R070/R071 CI-artifact fetch proceed during the suspension? The
  artifacts expire around 2026-12-29, and lane G's commit 8b9788ee2 is gone.
- think-3j6u: budget for the ValidTilt9 replay, 118-435 CPU-h (think-hwpr).
- think-sk6b: publish hosted release data/squarepacker-k2-minus-c-upper-certificates-v1.
  It does not exist yet.
- think-rt8s: which red-star rule to adopt.
- think-stc2: second certificate versus second and simpler proof as the meaning of
  "simplification".
- think-5n3o: the reported-lane witness at T-098's 48 counts.
- think-691c: move T-088/T-089 published to the SVG dates and rename three keys.
- Cap note: the owner's 2026-10-14 rule (think-lh7d) holds only items above 40 CPU-h. The
  #543 budget lines for #419 (2.1-10.3 process-h) and s(12) (7.3 CPU-h) predate it, so
  under that rule they are runnable. Confirm this reading.

## UNSURE

- **think-mt6e.** Rungs are now derived, and check_standing keeps C0/C1 entries out of the
  verified lane in its logic. I found no gate that fails a verified-field value from
  another author when it has neither a replayed-here entry nor a mapped review. Decide by a
  negative control.
- **think-om5l.** It was updated today at 02:26Z by lane c-lane-couzo-residue-1022, under
  delegate claude-code@vm. I did not mark it stale.
