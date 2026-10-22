# Profile Coverage and Result-Intake Boundaries, 21 October 2026

This review closes the contributor identity audit for the current profile integration.
New mathematical result registrations are a separate intake, as the owner confirmed.
The reusable audit is `packing/devtools/profile_coverage.py` (`think-uwd6`); identity
additions and reviewed joins are tracked by `think-nd1y` and `think-eigy`. The parent
work item for remaining population and mathematical coverage is `think-m7il`.

## Reproduce the audit

From `packing/`, using the pinned Python environment, run:

```bash
uv run --frozen --all-extras --group dev python -m devtools.profile_coverage --minimum-significance 1 --json
```

Use `--minimum-significance 4` to prioritize S5/S4 relationships.
The audit reads the profile registry, reviewed occurrence manifest, bibliography, result
register, case records, source-coverage ledger and existing contributor census.
It writes nothing. Exact alias matches identify review candidates; they never authorize
identity joins. `pending_identity_labels` groups repeated spans into distinct labels
while preserving candidate IDs, roles and related results.
The full gap rows retain exact field addresses, raw labels and offsets.

A profile’s Results are distinct registered results for which reviewed attribution
establishes primary authorship.
Credits are distinct nonprimary person/result associations, disjoint from that person’s
Results; significance comes from the result doing the credit.
Publication and activity years come from reviewed own-work evidence, never later
citations, archive dates or import dates.
A source author’s appearance as a prerequisite does not make that person the primary
author of the citing result.

## Closing snapshot

After the final manifest handoff, the audit loads **75 profiles**, with **217 distinct
registered results** having reviewed primary profile authorship and **714 nonprimary
person/result credit associations**. The structured census has 1,465 resolved spans, 78
non-person spans and seven unresolved spans.
Together with ten manual-origin spans, these account for all 1,560 manifest occurrences.
The seven unresolved spans are four distinct labels: three collective-project `Levy`
mentions, one `BuddenPing` account, one `register seed data from Levy` clause and two
`hmbelvedere` mentions.
Their retained scope or identity uncertainty is explicit; no clear personal label in the
audited structured fields remains without a reviewed profile join.

The census records ten manual origins, including the reviewed figure credit JSON
origins. The broad PDF/prose inspection backlog remains separate from these structured
identity dispositions.
Counts are reproducible from the command above rather than embedded as assertions in
source records or tests.

The closing receipt includes upstream `7eeab1f5e`: all 178 branch bibliography sources
were preserved and Evan Daniel’s n343 source added as source 179. Seven exact new
bibliography spans were reviewed and resolved, preserving prior spans, raw credit text,
roles and inspection receipts.
The retained credits explicitly name Joshua Levy, supporting that source-specific
identity join. The n343 work remains an existing beyond-horizon source claim; it adds no
T result and does not change the profile tallies.
The integration is tracked by `think-65yl`.

## Identity dispositions

The approved batch adds profiles only where retained bylines, attribution records or
catalogue credits establish a public personal name.
Initials remain unexpanded when the source gives initials.
Accounts, institutional affiliations and AI assistance do not supply additional personal
identities.

| Remaining label or boundary | Disposition |
| --- | --- |
| `PingYou Ltd` | Corporate credit, explicitly requested by the retained PR 574 packet; non-person. Its source credits refinements separately from original construction authorship. |
| `BuddenPing` | Submission account associated with that corporate corpus; operator identity is unknown. Keep unresolved rather than inventing a person. |
| Three collective-project `Levy` credit spans | Intentional unresolved collective/project references, distinguished from reviewed personal Joshua Levy credits. Exact spelling alone cannot settle scope. |
| `register seed data from Levy` | Clause and project-data attribution requiring boundary review, not an inferred personal byline. |
| `hmbelvedere` | Public label whose person-versus-entity identity remains uncertain; keep unresolved. |
| EvolvingPrograms | Reviewed entity/affiliation credit; do not infer a person from the formalization credit block. |
| Names in uninspected PDFs or prose-only references | Pending inspection; the structured-field audit is not a claim that every cited author or acknowledgment has been exhausted. |

Friedman’s retained DS7 introduction and reference 12 provide the matching full Said El
Moumni name and 1999 paper; that identity is resolved rather than an open exception.

The central policy records the intentional identity exceptions.
The census records explicit PDF inspection receipts.
The coverage tool associates PDFs only through explicit source-coverage paths or result
artifacts; it does not infer that a nearby transcription, directory or prose citation
means the entire PDF has been inspected.

## Mathematical work awaiting normal intake

`authored_sources_without_primary_results` means that a reviewed authored source has no
primary attribution in the T register.
It does **not** mean that its claims are missing from every project record.
Each row exposes source-coverage disposition, representation paths, a retained claims
record, and any existing beyond-horizon rows.
Their assurance and supersession dispositions remain unchanged.

| Work and retained evidence | Disposition and next work |
| --- | --- |
| Gensane and Ryckelynck, *Improved Dense Packings of Congruent Squares in a Square* (2005), DOI 10.1007/s00454-004-1129-z; retained raw paper abstract and Section 7 | Published source reports improved packings for 11, 29 and 37, and an alternative optimal packing of 18; review original claims and their historical attribution through normal intake, `think-jtp4`. A source’s optimality wording is not an independent verification here. |
| Stromquist, *Packing 10 or 11 Unit Squares in a Square* (2003), retained paper and its annotated source errata | Original exact n=10, unrestricted lower n=11, and restricted-angle n=11 statements require distinct scopes and the already recorded proof limitations. Historical registration review is `think-jtp4`; later use of the method does not extend Stromquist’s activity to 2026. |
| Arslanov, Mustafin and Shangitbayev, *Improved packings of n(n−1) unit squares in a square* (2021), DOI 10.37236/8586 | Retained title-page bylines and explicit 5 November 2021 publication date now have bibliography author joins. The source claims $s(k^2-k)<k$ for every $k\ge12$, plus $s(307)<18$, $s(273)<17$ and $s(241)<16$. These need normal original-claim intake, `think-jtp4`; author/date metadata does not validate those claims. |
| Schadt’s 2025 n=29 repository | Already represented by case n-029, retained decimal/rational witnesses and report/replay evidence in source-coverage. It lacks primary T attribution; assess a historical projection under `think-mdb2`, not a duplicate untracked packing. The source’s 5.9338857998 report and the relaxed exact witness must stay distinct. |
| MacIver’s 8 August 2026 n=17 manuscript and n=18 corollary | Claimed strict lower bound is weaker than this project’s independently verified bound. Fourteen essential interval–Farkas certificate files and their cited replay programs are absent from the inspected pinned source. A reported, unreplayed intake with these limits belongs to `think-o3j2`; no optimality or local replay is inferred. |
| Gensane’s 2004 sphere-packing paper | Original publication supports an evidenced profile activity year, but concerns spheres in a cube. Do not manufacture a square-packing result from it. |
| Kingbird catalogue, Daniel’s regularizer and Atlas, formalization/replay and method-support resources | Resource or supporting-work records need their own disposition. Catalogue compilation, solver use, or replay does not transfer primary authorship of all associated packings. Review missing source/result projections through `think-mdb2`. |
| Muglich issue 686, Fang direct certificates, Couzo extended-range reports, and Daniel composition packets | Existing source-specific and beyond-case-corpus ledgers already retain claims. Muglich alone has 100 beyond-horizon rows. Preserve their original source, count, assurance and supersession identity; `think-mdb2` decides how this canonical work appears on profiles without duplicating T records or inventing significance scores. |

The MacIver source is pinned at `9e2cd597047e040a63b7dcd103e79962cfc2d781`; its retained
packet is `packing/resources/web/maciver-square-packing-2026-09-07/README.md`. The
Schadt source representation is declared under `schadt-n29-2025` in
`packing/frontier/source-coverage.yaml`. The Muglich source is
`muglich-issue686-2026-10-19`, whose retained claims record and all 100 ledger rows are
exposed by the coverage report.
These are existing evidence records, not new mathematical findings from this audit.

Tej Stead’s retained Kingbird credit explicitly dates refinements to June 2026, but
there is no structured `improved_year` or reviewed dated-contribution contract in the
current activity model.
`think-0ltn` owns that gap.
Keep the activity field unknown until an explicit contribution record can support it; do
not assign the catalogue’s publication year or a later case’s discovery date to the
improver.

## Validation and limits

Focused helper tests cover disjoint coauthor/credit membership, per-source prerequisite
exceptions, result-scoped project credits, historical publication years, exact case
activity roles, missing dates, duplicate spans, source/beyond-horizon tracking and
manual JSON credit origins.
Ruff and BasedPyright cover both helpers and their tests.
Citation contracts check that bibliography author/year metadata agrees with the retained
archive index. Contributor schema and semantic loaders check each new profile and the
live reviewed manifest.

The audit’s test is reachable through the existing static import graph, and the normal
Python test suite includes it.
`check_site_scripts` inventories published browser code; the audit introduces no browser
program or executable HTML. No full mathematical replay or new T result registration is
part of this identity audit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
