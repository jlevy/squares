---
softschema:
  contract: packing.squares:Contributor/v1
  schema: contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: mira
  display_name: Mira
  aliases: [Mira-acc]
  links:
    - kind: github
      url: https://github.com/Mira-acc
      handle: Mira-acc
  sources:
    - id: repository-citation
      archive_path: packing/resources/web/n17-github-certificates-2026/mira-17squares/CITATION.cff
      locator: authors.name and repository-code identify Mira and the Mira-acc repository.
  provenance:
    - field: /display_name
      sources: [repository-citation]
    - field: /aliases/0
      sources: [repository-citation]
    - field: /links/0
      sources: [repository-citation]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
