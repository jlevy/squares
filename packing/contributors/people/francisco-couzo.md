---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: francisco-couzo
  display_name: 'Francisco Couzo'
  surname: Couzo
  real_name: 'Francisco Couzo'
  aliases: ['Couzo']
  sources:
    - id: primary-byline
      archive_path: packing/resources/web/franciscouzo-square-packing-2026-10-03/acquisition/sources.json
      locator: 'sources[0].commit_author and author retain Francisco Couzo from commit 6042c56.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
  provenance:
    - field: /surname
      sources: [primary-byline, bibliography]
    - field: /display_name
      sources: [primary-byline]
    - field: /real_name
      sources: [primary-byline]
    - field: /aliases
      sources: [primary-byline, bibliography]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
