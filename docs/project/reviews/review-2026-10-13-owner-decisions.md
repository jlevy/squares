# Owner Decisions of 13 October: s(11) Retired, s(17) Suspended, Duplicates Closed

**Status:** Applied under `think-z21j`; the questions under
[Open Questions](#open-questions) remain with the owner.

## The Decisions

On 13 October 2026 the owner wrote, in session:

> yes we can retire items obsolete if s(11) is now resolved, consolidate and close
> duplicate tasks.
> 
> future new work on s(17) should be suspended as we likely have it subsumed by
> Overbeck’s new proof #560, #571

T-060 settles s(11): Trump’s eleven-square packing is globally optimal.
Marc Leonard Overbeck’s #557 claims s(17) = L; PR #560 registers it as T-153 at V0/C1,
S5, reported, and PR #571 credits him by name.
Before the review, both PRs’ head was merged into this branch so that T-153’s records,
packet and receipts were readable.

## Method

The round continues [round 2](review-2026-10-12-bead-reconciliation-round-2.md) with the
same tools. Three read-only lanes on Opus at high effort reviewed 584 beads and five
plans, each against one decision: 263 beads that concern n = 11, 268 that concern n = 17
(beads touching both got both rules), and 125 duplicate candidates.
The candidates came from `reconcile_work --duplicates`, which pairs beads whose titles
share most of their words, and from open beads whose titles name the same issue, cell or
result. A follow-up covered six more candidates the duplicates lane found.
The coordinator added four items and two holds, merged the lanes, and applied the
result.
Where lanes disagreed, a close outranked a hold and a hold outranked a retain; no
field conflicted. The [applied record](review-2026-10-13-owner-decisions-applied.json)
holds the final disposition for each bead and plan and its receipt, apart from the
native-rectangle status edit described under Results.

## Results

| Disposition | Count | Beads |
| --- | --- | --- |
| Retired, s(11) settled | 12 | Agenda 028’s lower-bound lane (`think-pxv5` and four cells), BC-208 (`think-7nxe`), BC-300 (`think-dfof`), the M3 hand-proof route (`think-k4vb`), the T-059 replay (`think-190a`), and the n = 11 settlement cells BC-388 to BC-390 (`think-7c17`, `think-91yk`, `think-nho8`) |
| Suspended, s(17) | 45 held paused | Coordination, the eight-hour block’s lanes, instruments, and n = 17 contributor intakes; each carries a dated note on what resumes it |
| Closed as duplicate | 10 | `think-esdm` to `think-9nil`, `think-dpmt` to `think-eq0n`, `think-j30w` to `think-rdee`, `think-lhtz` and `think-kkj2` to `think-fvz4`, `think-dc0p` to `think-ndvg`, `think-5q0v` to `think-6q88`, `think-i52z` to `think-tn0j`, `think-tswc` to `think-tcns`, `think-qluo` to `think-ng1e` |
| Closed as finished | 11 | Work found delivered while reviewing, among them the retained Kleddamag n = 17 artifact (`think-9ll1`, `think-0rnb`, `think-7qto`), the refuted weighted-vertex lane (`think-geid`), and the #496 review beads (`think-zn2q`, `think-nbk8`) |
| Updated without a hold | 26 | 20 notes: survivors of duplicates carry what the closed bead alone recorded, and mixed beads name their live part; 7 re-homes from the archived n = 11 plan |
| Retained | 480 | Live and unaffected |

The work on Overbeck’s proof stays live and unchanged: the #557 intake (`think-00y8`),
T-153’s records (`think-07jt`), the #560 calibration (`think-idrr`), the #571 credits
(`think-ugbi`), the independent checks of its computations (`think-r7m8`), and their
epic (`think-6iv7`). Work kept for T-060 includes its verification, replay and
formalization, the papers and site pages, and tools whose value does not depend on s(11)
being open.

Two n = 11 beads are obsolete but stay open, held paused: Sessions 151 and 138 name
`think-gvlg` and `think-qqzs` as `certification_pending` owners, and the session gate
fails a closed owner.

Two plans moved, and two plans’ status lines changed.
The n = 11 daytime strategy plan is archived, superseded by T-060. The n = 17
three-block session plan joins the eight-hour proof block in `future/`, and the
eight-hour block’s status line now marks it suspended pending Overbeck’s proof too.
The native-rectangle plan’s status line no longer lists the retired replay
(`think-190a`); that edit is the one plan change missing from the applied record’s
`specs` list.
Links, the document map and SYNOPSIS follow the moves, and 168 closed beads
naming the two moved plans were repointed.

`reconcile_work --verify` reports 44 checks with no problems, and fresh bead records
confirm all 45 holds and 65 notes.
No cited commit is off `main`. `check_bead_tree` passes after the sync, and round 2’s
applied record still verifies.

## Open Questions

- **R070/R071 artifacts:** `think-7hq0`’s CI artifacts expire around 29 December, during
  the suspension. Should they be fetched anyway?
- **Contributor issues:** should the open n = 17 issues (#358, #413, #494, #495 and
  #523) get a short note that admissions and compute are suspended?
- **Two calls to confirm:** `think-t5va` (a Burns topology reconstruction for the atlas,
  upper-bound work) was suspended with the rest; `think-tmz6` is held while its record
  and CI children stay live, which reparenting may make cleaner.
- **Agenda cells:** the cells behind the retired beads (BC-208, BC-270, BC-272, BC-274,
  BC-300, BC-359, BC-388 to BC-390) still read tentative or blocked.
  Mark them stopped?

Gate-bound beads stay open with their holds: `think-x4v4` and `think-bmwd` own deferrals
in `result-requests.yaml` and `intake-watch.yaml`, and `think-sb9c`, `think-uutz` and
`think-haqw` close only when their children resolve.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
