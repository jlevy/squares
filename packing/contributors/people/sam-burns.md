---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: sam-burns
  display_name: 'Sam Burns'
  surname: Burns
  real_name: 'Sam Burns'
  aliases: ['Burns']
  sources:
    - id: primary-byline
      archive_path: packing/resources/web/n17-lower-bounds-2026/burns-near-record-arrangement.html
      locator: 'First-party title and meta author attribute name Sam Burns.'
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
