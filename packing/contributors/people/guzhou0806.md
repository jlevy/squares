---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: guzhou0806
  display_name: 'Guzhou0806'
  sources:
    - id: primary-byline
      archive_path: packing/resources/web/n17-guzhou-r071-2026-09-30/n17-square-packing/CITATION.cff
      locator: 'authors.name is Guzhou0806; repository-code names the public repository.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
  provenance:
    - field: /display_name
      sources: [primary-byline]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
