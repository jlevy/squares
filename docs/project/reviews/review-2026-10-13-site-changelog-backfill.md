# Site Changelog Backfill Review

The initial record covers exactly the 36 PRs selected by the
[changelog plan](../specs/active/plan-2026-10-13-site-changelog.md), from #479 to #588.
It contains 20 editorial entries representing 23 PRs and thirteen explicit omissions.
The entries and retained merge metadata live in
[`packing/site-changelog.yaml`](../../../packing/site-changelog.yaml).

## Evidence and Editorial Boundary

The acquisition read each PR’s title, body, UTC merge timestamp, base branch and full
merge commit through `gh pr view --json`. All 36 returned merged timestamps and
`baseRefName: main`; `git merge-base --is-ancestor MERGE_COMMIT origin/main` returned
zero for every delivery at the frozen main head `df9767225`.

The review inspected the local merge-parent diffs, their changed-file inventories and
linked records.
The GitHub `files` response stops at 100 paths for large PRs; it is not a
complete changed-file inventory.
Full local diffs, acquired JSON and the deployment log were retained in the task’s
external scratch. Their durable evidence is the merge identity in the YAML, the linked
source PRs and this review’s dispositions; rendering requires none of the scratch files
and makes no network request.

The prose records the delivered contribution and its merge-time claim limits.
Current artifact links may show later corrections; their labels say “Current” where that
matters. No moving download URL is presented as an archived historical edition.

Editorial selection prioritizes results, public papers and documentation, substantive
policy and tooling that protects intake or publication.
Internal plans, tracker and document-layout maintenance, temporary CI budgets and small
test-only repairs stay in the coverage audit without adding reader entries.
The record is a selected history, not an exhaustive announcement list.

### Verified stack grouping

- **Stack 498:** [#497](https://github.com/jlevy/squares/pull/497) and
  [#509](https://github.com/jlevy/squares/pull/509) explicitly name their positions in
  formal stack 498 and its seven PRs.
  The grouped entry includes only those two delivered layers and takes #509’s UTC merge
  date. The driver, re-solve, grid cleanup, gallery and admission layers (#511, #530,
  #548, #549, #559) remain outside the delivered record.
  The PR bodies’ old proposed T-154 for #549 is stale: T-154 belongs to #588, and no
  regularization result ID is announced here.
  Stack 498 is a stack identity, not issue or PR #498.
- **Stack 517:** [#518](https://github.com/jlevy/squares/pull/518) and
  [#553](https://github.com/jlevy/squares/pull/553) explicitly identify formal stack
  517\. The first entry groups delivered #512, #516 and #518; the subsequent #553 entry
  shares the stack identity but keeps its own membership.
  These separate entries preserve the distinction between four admissions and 42
  adoptions, then T-151/T-152 and nine later adoptions.
  No other related intake or acknowledgement PR is silently added to either entry.

GitHub reports #560’s merge commit as `5584b2283`; that commit is on main and its
first-parent merge title names #577, the proof stack’s review delivery.
The selected window still contains #560 only.
The candidate-proof entry describes the report and sampled checks, with no claim that a
complete replay or a new verification rung landed.

## Publication and Editions

The
[verified deployment](https://github.com/jlevy/squares/actions/runs/38475195836/job/115566109702)
ran at frozen main `df9767225`. Pages deployed on 2026-10-13 at 22:09:24 UTC, and the
verification job completed at 22:15:30 UTC with **4,104 of 4,104 checks passed**. Its
log confirms HTTP 200 for every retained result page, all four papers’ HTML/Markdown/PDF
outputs, both canonical infographic PDFs and SVGs, and the overview, atlas, results,
papers and About pages.
Structured artifact destinations were checked against the canonical live entries in
`packing/site-urls.yaml`.

The changelog retains this run’s verification URL beside every entry with public
artifacts.
It confirms that the advertised artifacts have launched by this deployment; it
does not establish each historical first-live date.
Those dates remain absent except for T-154, first delivered and verified on 2026-10-13
by this run.

| Delivered change | Evidenced edition references | Public destination and limit |
| --- | --- | --- |
| #477 methods revision | `paper:square-packing-methods-survey` v0.2.0 in `PACKING_METHODS_HISTORY` | Direct current tutorial and PDF links; the later served tutorial is v0.2.1 |
| #492 typography correction | `paper:n11-lower-bounds-explainer` v0.4.5 and `paper:square-packing-methods-survey` v0.2.1 in their retained histories | Deployment audit confirms both printed editions; all four papers and their PDFs are directly reachable |
| #474 atlas redesign and later record redraws | No invented release reference | Current 100- and 324-packing SVG/PDF links; historical redraws retained v0.5.0, rather than establishing another edition |
| Other site, result and pipeline deliveries | No invented release reference | A merged data change or data-pin suffix is not a component release |

The edition evidence comes from
[`sqpack.release`](../../../packing/src/sqpack/release.py), the #477/#492 diffs and the
successful deployment audit.
The dated PDF suffix `20261008` is the retained public filename, not a semantic version
or proof of first publication.
The n = 11 series and methods tutorial all have current direct HTML and PDF links in the
typography entry; this backfill adds no synthetic first-launch entries outside the
selected window.

## PR Coverage

Each selected PR appears once below and either belongs to an editorial entry or has an
omission reason. Entry membership and dates are also retained in `frozen_entries`.

| PR | UTC Merge | Disposition | Evidence Limit or Omission Reason |
| --- | --- | --- | --- |
| [#588](https://github.com/jlevy/squares/pull/588) | 2026-10-13T22:04:08Z | `fitzharding-n17-reported-proof` | T-154 is V0/C1; complete Lean build not replayed. |
| [#509](https://github.com/jlevy/squares/pull/509) | 2026-10-13T20:19:14Z | `regularization-foundations` | Vendored provenance and pin check; no regularized admission. |
| [#497](https://github.com/jlevy/squares/pull/497) | 2026-10-13T18:14:15Z | `regularization-foundations` | Policy, assessment and comparison tool; no drawing or bound moved. |
| [#581](https://github.com/jlevy/squares/pull/581) | 2026-10-13T17:45:00Z | `drawn-packing-verification-gaps` | Review and defect record; proposed drawing gate not built. |
| [#560](https://github.com/jlevy/squares/pull/560) | 2026-10-13T17:07:04Z | `overbeck-n17-candidate-proof` | T-153 is V0/C1; verified case remains open. |
| [#579](https://github.com/jlevy/squares/pull/579) | 2026-10-13T08:31:35Z | Omitted | Internal work reconciliation, tracker cleanup and agent-ownership procedures; no independent public result or publication. |
| [#576](https://github.com/jlevy/squares/pull/576) | 2026-10-13T05:28:00Z | Omitted | Internal documentation moves, filename normalization and layout/link maintenance; no public contribution needing its own announcement. |
| [#507](https://github.com/jlevy/squares/pull/507) | 2026-10-12T23:07:24Z | `publication-audit-and-import-scoping-repairs` | Dependency attribution, audit deadline and retry repairs to #496. |
| [#558](https://github.com/jlevy/squares/pull/558) | 2026-10-12T21:24:02Z | `pingyou-ai-assistance-disclosure` | Author disclosure correction and supporting checks; no new admission. |
| [#556](https://github.com/jlevy/squares/pull/556) | 2026-10-12T18:14:49Z | Omitted | Routine reply-tracker correction; no result, bound, admission or public artifact change. |
| [#553](https://github.com/jlevy/squares/pull/553) | 2026-10-12T17:56:19Z | `replayed-upper-bound-admissions` | T-151/T-152 V3/C3; nine adoptions and nine verified beyond-horizon rows. |
| [#555](https://github.com/jlevy/squares/pull/555) | 2026-10-12T16:41:07Z | Omitted | Recorded final replies and issue closures after the 42-bound adoption; no new admission or bound. |
| [#518](https://github.com/jlevy/squares/pull/518) | 2026-10-12T15:11:27Z | `october-eleven-intake-and-adoption` | 42 case adoptions; no new result registration. |
| [#551](https://github.com/jlevy/squares/pull/551) | 2026-10-12T13:59:44Z | Omitted | Recorded four confirmation replies for T-147 through T-150, whose admissions are covered by the intake delivery. |
| [#516](https://github.com/jlevy/squares/pull/516) | 2026-10-12T13:14:01Z | `october-eleven-intake-and-adoption` | T-147 through T-150 at V3/C3; adoption belongs to #518. |
| [#547](https://github.com/jlevy/squares/pull/547) | 2026-10-12T12:49:25Z | Omitted | Test-only repair to the atlas interruption probe; no user-facing animation or capability change. |
| [#546](https://github.com/jlevy/squares/pull/546) | 2026-10-12T10:41:36Z | Omitted | Routine intake-label administration and sweep maintenance; no new result or public artifact. |
| [#531](https://github.com/jlevy/squares/pull/531) | 2026-10-12T08:09:46Z | `edited-intake-comment-detection` | Includes edited-comment detection, beyond reply bookkeeping. |
| [#512](https://github.com/jlevy/squares/pull/512) | 2026-10-12T06:37:28Z | `october-eleven-intake-and-adoption` | Finite audit of reported 6.718 bound; full 43-slab replay pending. |
| [#519](https://github.com/jlevy/squares/pull/519) | 2026-10-12T05:54:56Z | Omitted | Recorded 21 acknowledgements of results already delivered to main; no new result, rung or adoption. |
| [#520](https://github.com/jlevy/squares/pull/520) | 2026-10-12T05:49:02Z | Omitted | Test-only navigation-wait repair; no user-facing results or navigation change. |
| [#513](https://github.com/jlevy/squares/pull/513) | 2026-10-11T22:44:05Z | `public-site-prose-and-reading-width` | Presentation and editorial corrections; 16 substantive follow-ups retained. |
| [#508](https://github.com/jlevy/squares/pull/508) | 2026-10-11T20:41:26Z | `evan-daniel-attribution-corrections` | Credit corrections; no new result or rung. |
| [#502](https://github.com/jlevy/squares/pull/502) | 2026-10-11T19:32:41Z | `website-front-door-and-result-reports` | README front door, shared report invitation and credit-name form. |
| [#496](https://github.com/jlevy/squares/pull/496) | 2026-10-11T06:07:36Z | `bounded-publication-audits` | Bounded audit and scoped push checks; no general speedup claimed. |
| [#499](https://github.com/jlevy/squares/pull/499) | 2026-10-11T05:43:16Z | Omitted | Corrected stale intake wording and acknowledgement metadata after #487; no independent result, capability or publication. |
| [#487](https://github.com/jlevy/squares/pull/487) | 2026-10-11T04:46:46Z | `october-ten-intake-replays` | T-128 through T-146 reconciled; confirmed certificates and pending reports distinguished. |
| [#462](https://github.com/jlevy/squares/pull/462) | 2026-10-11T01:27:57Z | `unified-site-navigation` | Unified overview, atlas and results controls and navigation. |
| [#492](https://github.com/jlevy/squares/pull/492) | 2026-10-10T22:49:17Z | `paper-typography-and-title-case` | Paper typography and two evidenced paper edition references. |
| [#477](https://github.com/jlevy/squares/pull/477) | 2026-10-10T21:03:34Z | `illustrated-packing-methods-tutorial` | Illustrated tutorial v0.2.0, without standing-bound adoption. |
| [#491](https://github.com/jlevy/squares/pull/491) | 2026-10-10T20:49:26Z | Omitted | Internal scheduling and resource planning for an unlaunched research agenda; no new result. |
| [#474](https://github.com/jlevy/squares/pull/474) | 2026-10-10T11:30:22Z | `readable-atlas-and-print-exports` | Atlas and export redesign; no new mathematical claim or edition inferred. |
| [#478](https://github.com/jlevy/squares/pull/478) | 2026-10-10T01:59:56Z | `daniel-record-hunt-source-intake` | T-131 initially V0/C0; exact replay and review/adoption kept separate. |
| [#482](https://github.com/jlevy/squares/pull/482) | 2026-10-10T01:13:05Z | Omitted | Internal proof/confirmation component planning; no new result or public deliverable. |
| [#480](https://github.com/jlevy/squares/pull/480) | 2026-10-10T00:28:55Z | Omitted | Temporary CI-budget maintenance and retained measurements; the structural efficiency improvement remains future work. |
| [#479](https://github.com/jlevy/squares/pull/479) | 2026-10-10T00:28:20Z | `dated-beyond-horizon-reports` | Unreplayed beyond-horizon reports with dated supersession. |

## Verification and Remaining Limits

- Acquisition covered 36 of 36 selected PRs; main-branch ancestry passed for every
  retained merge commit.
- Editorial coverage is 23 represented PRs in 20 entries and thirteen omissions.
  Only verified formal stack deliveries are grouped.
- Publication evidence confirms all advertised current artifact destinations and the two
  paper corrections’ visible editions.
  Historical first-live dates and uncaptured editions remain unknown.
- The backfill does not replay mathematical proofs or certificates.
  It preserves the admission and confirmation status established by the source
  deliveries and their retained records, including the unreplayed T-153 and T-154
  proofs.

## Subsequent Main Deliveries

The initial 36-PR window and its twenty entries remain intact.
The 14 October integration adds the remaining nine layers of formal stack 498 as one
regularization delivery: #511, #530, #548, #549, #559 and #580 share main merge
`aeef99ef0`; #585, #587 and #591 share main merge `9f48ccc80`. Each row retains its
actual GitHub base branch and UTC merge timestamp.
Seven rows retain a separate `delivery_to_main` receipt, acquired by verifying the merge
commit on local main’s first-parent history.

The regularization entry cites the completed
[9f48ccc80 deployment verification](https://github.com/jlevy/squares/actions/runs/38527537367/job/115733950233).
Its T-155/T-156 statements retain the exact-side scope and distinguish T-156’s existing
monotonicity implication from a new bound.

The related #592/#595 entry groups proof-report classification, evidence coverage and
public explanation without asserting a formal stack.
Their actual main merges are `f73e9de13` and `b8c930338`. The completed
[f73e9de13 deployment verification](https://github.com/jlevy/squares/actions/runs/38536230832/job/115761676874)
confirms the current linked artifacts.
T-153 and T-154 remain V0/C1; no complete proof replay or new verified optimum is
announced.

The integrated record contains 22 entries, 47 retained deliveries and the original
thirteen omissions. Current artifact links name moving views rather than archived
editions. The selected infographic v0.6.0 and explainer v0.4.6 exports are still release
preparation work and are not attributed to these already verified launches.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
