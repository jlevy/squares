---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: walter-trump
  display_name: 'Walter Trump'
  surname: Trump
  real_name: 'Walter Trump'
  aliases: ['Trump']
  sources:
    - id: primary-byline
      archive_path: packing/resources/papers/trump-2023-packing-11-unit-squares.raw.md
      locator: 'Opening byline: Walter Trump, 2023-02-27, last update 2023-03-05.'
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
