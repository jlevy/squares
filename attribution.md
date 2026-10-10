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
An account’s transient display name need not become the preferred credit name.

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

## Website and PDF Presentation

Use the same preferred person credit in records, notes, tables and paper credits.
Link a person’s name to their profile wherever that surface supports it.
The profile can supply handles, the optional biography and identity evidence; a compact
credit line does not need to repeat `Joshua Levy (jlevy, ojoshe)` on each occurrence.

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

These decisions were recorded on 2026-10-10. Each row states its scope and remaining
work; identity evidence remains in the linked profile or source packet.

| Subject | Decision | Evidence and scope | Tracking |
| --- | --- | --- | --- |
| Joshua Levy | Preferred compact person credit `Levy`; full name `Joshua Levy`; GitHub `jlevy`, X `ojoshe`. The Squares Project remains the project name. | Owner instruction; [profile](packing/contributors/joshua-levy.md), project license and retained owner announcement. Preserve collaborators and project/tool attribution. | `think-t3a9`, `think-vix3` |
| Ahmed / Queuingtheorydotcom | One person; compact bibliography credit `Ahmed`, stable profile ID `queuingtheorydotcom`. Current and historical handles are aliases, not extra authors. | Owner confirmation and [retained announcement receipts](packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/README.md#source-and-pin) link `ManassehA06` and the former `MathCompSciFTW` account. Retain the evidence distinction for full-name spelling. | `think-t3a9` |
| EvolvingPrograms / Lewis | Personal credit is `Lewis` (`ctjlewis`); EvolvingPrograms is an affiliated organization, not an additional human author or a proved personal alias. Keep organization/repository credit only where its infrastructure role is supported. | [Lewis’s GitHub profile](https://github.com/ctjlewis) lists the affiliation; [EvolvingPrograms](https://github.com/EvolvingPrograms) is an organization. The retained [acknowledgments](packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/11SquaresFormalized/ACKNOWLEDGEMENTS.md) credit both for infrastructure. Affiliation does not prove entity identity. Profile population and per-occurrence role review remain tracked. | `think-8yk4` |
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
