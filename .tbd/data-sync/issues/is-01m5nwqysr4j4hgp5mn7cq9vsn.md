---
type: is
id: is-01m5nwqysr4j4hgp5mn7cq9vsn
title: "Decision: how profiles count one report registered as two results (T-073/T-080 at n = 101-105; T-083/T-084 at the 16 counts k^2-1)"
kind: task
status: open
priority: 2
version: 3
labels:
  - decision
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T02:44:52.663Z
updated_at: 2026-10-24T04:50:54.615Z
---
Owner decision, raised by lane c-review-pending-1024 (think-rh4j) on 24 October 2026 from the owner's request to catch up every "Review pending" on the profiles.

## The question

How should the profiles' Records count one report that the register holds as two results? Two pairs are affected, and they are the only priority ties left in the record index (`python -m devtools.profile_records`).

## Context for a reader with none

- A profile's Records are the person's registered results that still hold a current bound. When two results hold the same bound at the same count, the earlier report gets it ("a tie stays with the earlier report", result-import.md, Several Reports at One Count). `devtools.profile_records` orders such a tie only by the source's publication date, and never by T-number or registration time. A tie it cannot order is "unordered", and a result with no other current facet then shows as "Review pending".
- **T-073 and T-080** register one certificate: Hiroaki Hosono's linear measure proving s(101) >= 257/25, which also gives n = 102 to 105. Both cite the same source key, `[wand125 linear certificates 2026-10-02]`, published 2026-10-02, and the same evidence, `E-n101-wand125-linear-1028-report` and `-source-replay`. Issue #294's single reported result `n101` maps to both. T-080 was registered on 3 October only because T-073 then carried an unreplayed count (n = 83); that reason lapsed the same day, when n = 83's replay passed (T-080's notes).
- **T-083 and T-084** register one paper: Hakan Karakuş, arXiv:2609.37410 (29 September 2026). T-084's lower half, s(k^2 - 1) >= k, is T-083's floor at N = k^2 - 1. Both cite `E-karakus-strip-lower` and `E-karakus-strip-measure-interval`, source key `[Karakuş 2026]`, published 2026-09-29.

## Why the rules leave it undecided

Report order needs two reports. Each pair is one report, so neither entry is earlier, and the only field the code orders by, `attribution.published`, is the same, truthfully, for both entries. No record change can order them without misstating the source.

## What the site shows now (main 5664ac1e8, and every open intake PR head)

- "Review pending" on profiles/hiroaki-hosono.html, on Hiroaki Hosono's row of profiles/index.html, and on the wand125/square-packing-bounds card of resources.html. T-073 and T-080 hold no other current bound.
- profiles/hakan-karakus.html lists T-083 and T-084 under "Facet comparisons awaiting review". Both still count as Records through other facets, so no "Review pending" label shows there.

## Options

- **A (recommended). One report, every entry credited.** When every tied candidate has the identical attribution (one source key, one date), the classifier gives the facet to each. Site: Hosono's Records rise by two (T-073 and T-080, S3 each), matching his Results, which already count both. "Review pending" disappears from his profile, the directory row and the project card, and Karakus's awaiting-review list empties. No record field changes. The patch is 11 lines in `classify_records` plus a test, priced and measured: the index goes from 118 current results and 4 unassessed to 120 and 0. It is saved at /tmp/claude-0/-home-user-squares/f8504540-2b5a-5f78-8968-eb4ffa4c4b64/scratchpad/review-pending/option-a-one-report.patch.
- **B. One report, one entry credited.** A new register field on the re-registering entry (say `restates: T-073` on T-080) redirects its facets to the named entry, as `first_certified_in` does for upper bounds. Site: Hosono's Records rise by one (T-073), and T-080 stays a Result only. It needs a schema field and a ruling on which of T-083 and T-084 restates the other, since both were registered on 2 October.
- **C. Retire the duplicate.** Fold T-080 into T-073. This is a register change to a bound entry, whose supersession today is only derived, never declared. It is the largest option, and it changes T-080's result page.

Recommendation: A. It follows the register as it stands, uses no registration order, and is narrow: only candidates with the identical attribution are joined.

## Notes

2026-10-24 coord-intake-1023: OWNER ANSWERS (in conversation). On a pair of register entries from one report (T-073/T-080, T-083/T-084), the owner selected "Credit both (Recommended)": when the tied entries carry identical attribution, both are credited as current (option A, the 11-line change to classify_records). On the nine pending results with no tracking issue (T-036, T-046, T-087, T-112, T-142, T-143, T-144, T-179, T-192), the owner selected "Open all nine (Recommended)": one issue per result, labelled intake, stating its current review state, updated at every change, and closed when the review lands.
