---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: michael-j-kearney
  display_name: 'Michael J. Kearney'
  surname: Kearney
  real_name: 'Michael J. Kearney'
  aliases: ['Kearney']
  sources:
    - id: primary-byline
      archive_path: packing/resources/papers/kearney-shiu-2002-efficient-packing-unit-squares.md
      locator: 'Opening paper byline names Michael J. Kearney and Peter Shiu.'
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
