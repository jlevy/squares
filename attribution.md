# Attribution Policy

This document owns how this project names contributors and assigns credit in its own
records, notes, website and PDFs.
It also records identity decisions and exceptions.
[Epistemics](epistemics.md#results-by-others) owns the evidential status of a result;
[conventions](conventions.md#6-provenance) owns provenance;
[the design guide](packing/devtools/templates/paper-design.md#the-papers-front) owns
credit typography and layout.
Those documents reference this policy rather than maintain separate naming rules.

## People, Projects and Assistance

Credit the person responsible for a contribution, using their preferred public name or
the handle under which they publish.
A verified handle and a person’s name identify one contributor, not two authors.
Do not infer a real name, merge accounts from similar spellings, or expand a pseudonym
without evidence.

Use **The Squares Project** for the general project, its website, software and
collective record. Use **Levy** for Joshua Levy’s personal result credits, and **Joshua
Levy** where a full name is appropriate, including human-oversight lines.
His public handles are `jlevy` on GitHub and `ojoshe` on X. A result with other
contributors keeps those contributors and their roles; project ownership is not sole
authorship of every result.

Keep distinct roles explicit: original proof, construction, formalization, method or
checker, independent verification, exposition, infrastructure and human oversight.
Replaying someone else’s result does not transfer its authorship.
Verification rungs do not change its credit.

AI agents are never credited authors.
Preserve declared AI assistance in the source’s own terms in the case record, register
and README prose about that result, and distinguish it from human oversight.
`devtools.state_ai_assistance` reports a case record that cites an AI-assisted source
without stating that assistance.
Papers may have a separate **Agents** line under the existing publication format; that
line records assistance, not authorship.
Credit software, repositories and infrastructure in the appropriate method or source
role; do not count a person’s project or organization as a second person merely because
both names occur in an acknowledgment.

## One Identity, Several Public Labels

Each person has one stable contributor ID. Their profile holds sourced names, aliases
and public account links.
Changing a preferred display label does not change that ID or break existing links.
The full `aliases` array retains evidenced spellings for reviewed credit matching.
The optional `display_aliases` array selects which of those spellings a profile shows;
it defaults to empty and does not require a second provenance claim for the selection.
Show meaningful alternate public names rather than repeating the current name, surname,
obvious spelling variants or accounts already linked below the name.
An account’s transient display name need not become the preferred credit name.

Inline profile links use one registry-wide naming rule: an evidenced surname when
unique, the full public name when surnames collide, then an evidenced handle or stable
ID if the full names also collide.
The optional `surname` field names the family name explicitly and requires provenance;
word position never establishes it.
A person without an established surname uses their public account handle, preferring
GitHub when available, or their public display name.
The directory sorts by that same surname or handle, but displays full real or public
names beside reviewed-credit counts, cited-resource counts and public account links.
Full profile headings and identity metadata also retain the full public name.
Home and About invite readers to the directory without listing names.

Identity evidence may include the person’s public account or publication, linked
profiles, retained account identifiers, and an explicit confirmation recorded by the
project owner. Record which evidence supports each name or link.
Distinguish primary account evidence from a curated source or owner confirmation; do not
represent the latter as a primary byline.
A disputed spelling may remain an alias with its source while the optional real-name
field stays empty.

A profile alias is not permission for a global text replacement.
Each credited source span is joined explicitly to its contributor ID, with its original
label and evidence. Ambiguous occurrences remain unlinked until reviewed.
Deduplicate a person within the same contribution and role only; preserve separate
roles, works, and independently credited stages of a result.

## Credit Text and Lineage

A source’s `credit` in [bibliography.yaml](packing/resources/bibliography.yaml) is the
single home of its curated credit text: authors, then `after` and the antecedents the
source names, such as `Daniel after Burns, Massaccesi`. A chain through an intermediate
author retains every supported link.
Hand-written prose may explain it but does not silently drop authors or antecedents.
Do not infer lineage from a resemblance between methods.

Where the atlas’s 66-character line cannot hold the full credit, use the source’s
`short_credit`: the same authors and the first of the same antecedents, ending in
`et al.` as needed. `devtools.build_bound_citations` checks this shape.
Figures that reuse that line show the same short form.
Every other renderer prints the full credit and lineage; a link to the source record
does not replace them.

Method credit travels with the result.
A result using another person’s proof, method, solver or checker retains that person’s
supported role and lineage in the same credit line.
An external result is credited `after Levy` only where its source itself says so.
A first-party result uses `Levy`, or `Levy after …` when appropriate.
Its `builds_on.credit` in [results.yaml](packing/frontier/results.yaml) names authors of
evidence the result actually cites.
Repairing a proof is `after` its author; proving a new property of a packing does not,
by itself, make the packing’s finder a methodological antecedent.

A regularization leaves the packing with its finder.
A certificate that rearranges a packing the record already credits, for display or after
solving it to an exact side, does not take the packing’s credit.
The finder keeps the packing through the register result that holds it, which the
regularized result names as `of` in its `regularizations`, one item a count.
The regularizer is credited with the regularization, and with the certificate where it
is theirs, and is typed there as `by`, with the method, the side and what the
regularization changed: `T-146` regularizes Ryan Xu’s, Mishapolk’s and SQUISH’s packings
and is credited `Daniel after Xu, Chaoweeraprasit, Mishapolk, Levy`. The record never
says in its own voice that a regularization is the same packing as the one it was made
from unless the item’s `identity.basis` is `measured`, a decision made here.
Otherwise it says whose claim the identity is, as `T-146` says that each view’s identity
rests on Evan Daniel’s sampled path test; measurements made here are recorded beside the
claim and decide nothing.

## Website and PDF Presentation

Use the same preferred person credit in records, notes, tables and paper credits.
Link a person’s name to their profile wherever that surface supports it.
The profile can supply handles, the optional biography and identity evidence; a compact
credit line does not need to repeat `Joshua Levy (jlevy, ojoshe)` on each occurrence.

News entries link people directly to their profiles using the shared surname-or-handle
label, including first mentions.
Author the link to `packing/contributors/people/<id>.md` in the changelog record; the
website resolves it to `profiles/<id>.html`, and GitHub keeps the repository link.
Retained PR titles, quotations and source identifiers keep their original wording.

Authored site introductions, case narratives and open-question notes, result claims,
summaries and explanatory notes, declared reader-document articles, News summaries and
details, and profile biographies link exact full names that identify one published
profile. Soft-wrapped names match across whitespace; linked labels use the shared
surname-or-handle rule, with possessive punctuation retained outside the link.
Existing account links may lead to that profile only when both their exact verified URL
and visible name or handle identify the same person.
This presentation pass does not match surnames or raw aliases, infer missing identities,
change reviewed identities, or enter headings, quotations, source evidence, code,
mathematics and existing publication links.
Resolved credit spans use the same short label while retaining the original reviewed
wording in link data; unresolved spans keep their source wording.
A biography does not link its subject back to the same profile.
Ambiguous names remain plain text.

Profiles show public account handles or URLs with shared platform icons and accessible
platform names. Keep these public website destinations external.
The homepage’s curated external resources share one projection with profile Resources
lists and directory resource counts.
Only the resource’s explicit byline establishes its person relationship: a unique whole
public label or exact unique full names in a compound byline.
Preserve lineage words such as “after”; do not infer ownership from a URL, description
or organization name.
Exact artifact and comment URLs remain distinct, and shared resources appear once for
each explicitly credited person.
Personal account links remain separate from resources and reviewed credits.
Related News links come from explicit person-record links in eligible News summaries or
details; the announcement supplies its existing title, date and stable entry address.
Do not maintain a duplicate chronology in the person record.

A paper explaining another person’s proof leads with the original proof and its author,
then distinguishes the paper’s exposition, oversight and assistance.
Keep a direct link to the actual source work: a person profile does not replace a
publication citation.
In PDFs and other static formats use ordinary hyperlinks, not a dependence on popovers.
Project branding belongs in the site identity, footer or software attribution, not as a
substitute for the person in a result byline.

Preserve the wording of archived PDFs, source transcriptions, quotations and retained
receipts. Update first-party curated credits and generated output from their source
records. If an upstream source credits a repository and a person together, explain any
reviewed normalization in the decision record rather than silently rewriting the
archived acknowledgment.
Existing first-party wording awaiting migration is tracked work, not an implicit
exception to this policy.

## Decisions and Exceptions

These decisions were recorded on 2026-10-10 unless a row gives its own date.
Each row states its scope and remaining work; identity evidence remains in the linked
profile or source packet.

| Subject | Decision | Evidence and scope | Tracking |
| --- | --- | --- | --- |
| Joshua Levy | Preferred compact person credit `Levy`; full name `Joshua Levy`; GitHub `jlevy`, X `ojoshe`. The Squares Project remains the project name. | Owner instruction; [profile](packing/contributors/people/joshua-levy.md), project license and retained owner announcement. Preserve collaborators and project/tool attribution. | `think-t3a9`, `think-vix3` |
| Manasseh Ahmed / Queuingtheorydotcom | Updated 2026-10-13. One person, credited by name: `Ahmed` in compact credits, as every surname is, and `Manasseh Ahmed` on his profile, `manasseh-ahmed`, and in unlinked prose. `Queuingtheorydotcom` on GitHub and `@ManassehA06` on X, formerly `@MathCompSciFTW`, are his handles: aliases, not extra authors. The earlier curated spelling `Mannaseh` is corrected and kept as an alias. | The owner’s confirmation of 13 October 2026; the n = 17 edition’s CREDITS.md prints “Manasseh Ahmed”; the [retained announcement receipts](packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/README.md#source-and-pin) link `ManassehA06` and the former `MathCompSciFTW` account; [profile](packing/contributors/people/manasseh-ahmed.md). | `think-t3a9`, `think-vqk8` |
| EvolvingPrograms / Lewis | Personal credit is `Lewis` (`ctjlewis`); EvolvingPrograms is an affiliated organization, not an additional human author or a proved personal alias. Keep organization/repository credit only where its infrastructure role is supported. | [Lewis’s GitHub profile](https://github.com/ctjlewis) lists the affiliation; [EvolvingPrograms](https://github.com/EvolvingPrograms) is an organization. The retained [acknowledgments](packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/11SquaresFormalized/ACKNOWLEDGEMENTS.md) credit both for infrastructure. Affiliation does not prove entity identity. Profile population and per-occurrence role review remain tracked. | `think-8yk4` |
| Marc Leonard Overbeck / Kleddamag | Recorded 2026-10-13. One person, credited by name: `Overbeck` in compact credits, `Marc Leonard Overbeck` on his profile and in unlinked prose. `Kleddamag` on GitHub and `@kleddamag` on X are his handles, linked from the profile; they are aliases, not a second author. Identifiers, URLs, quotations and archived text keep the handle. | The owner’s instruction of 12 and 13 October 2026, and the `CITATION.cff` and README of his [12 October edition](https://github.com/Kleddamag/the-seventeenth-square-candidate/tree/653b9589d0f8a152f01adc56b1d48ba53d49abc3); [profile](packing/contributors/people/marc-leonard-overbeck.md). The profile joins both the `Kleddamag` labels still in the record and the `Overbeck` labels that replace them. | `think-ugbi` |
| Hiroaki Hosono / wand125 | Recorded 2026-10-13. One person, credited by name: `Hosono` in compact credits, `Hiroaki Hosono` on his profile and in unlinked prose. `wand125` on GitHub and `@wand_125` on X are his handles, linked from the profile; they are aliases, not a second author. Bibliography keys, identifiers, URLs, quotations and archived text keep the handle. | The owner’s instruction of 13 October 2026; the commit authorship his retained packets record and his GitHub profile’s name; [profile](packing/contributors/people/hiroaki-hosono.md). | `think-m7il` |
| Ryan Xu / ry-xu | Recorded 2026-10-14. One person, credited by name: `Xu` in compact credits, `Ryan Xu` on his profile, in case-record finder lists and in unlinked prose. `ry-xu` on GitHub and `@small_LM` on X are his handles, linked from the profile; they are aliases, not a second author. Bibliography keys, identifiers, module names, packet paths, URLs, the `author` field that names the account filing an issue, quotations, archived text and dated reviews keep the handle. | The owner’s instruction of 14 October 2026; the GitHub account `ry-xu` gives the name Ryan Xu and links the X account; [profile](packing/contributors/people/ryan-xu.md). | `think-g2ga` |
| Nate Chaoweeraprasit / natcha | Recorded 2026-10-20. One person, credited as `Chaoweeraprasit` in compact links and `Nate Chaoweeraprasit` on his profile. `natcha`, GitHub `itsnaka` and X `thatennine` are aliases. | The owner’s confirmation of 20 October 2026 identifies Nate as the person behind `natcha` and [the X account](https://x.com/thatennine); the X profile was not independently inspected. The [SQUISH intake](packing/resources/web/squish-401-2026-10-07/README.md) already records Nate Chaoweeraprasit (itsnaka). See his [profile](packing/contributors/people/nate-chaoweeraprasit.md). | `think-notn` |
| Historical first-party atlas/PDF lines | Migrate project-as-person credit to the preferred person name from the generating records. Do not edit archived third-party sources. | The existing `Squares Project (Levy)` display is a migration target, not the naming rule for new work. Rebuild and review affected figures and PDF credits together. | `think-vix3`, `think-jn87` |

An exception needs a named scope, reason, supporting evidence, owner and review
condition in this section.
It does not establish a new default.
Record unresolved identities as pending decisions rather than granting an exception that
invents an identity.

## Applying a Change

Review the source and roles, update the profile and curated credit record, then review
each affected occurrence mapping.
Source-drift checks must pass without hiding a wording change.
Regenerate affected pages and publications; check names, links, lineage and the print
credit line. Record the decision and its bead here when it establishes a new convention
or an exception. Routine additional alias evidence belongs in the profile rather than a
second policy document.

The
[contributor plan](docs/project/specs/active/plan-2026-10-10-contributor-profiles.md)
tracks population and renderer coverage, and the
[intake runbook](packing/campaign/result-import.md) applies this policy to new results.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
