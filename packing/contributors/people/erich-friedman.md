---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: erich-friedman
  display_name: 'Erich Friedman'
  surname: Friedman
  real_name: 'Erich Friedman'
  aliases: ['Friedman']
  sources:
    - id: primary-byline
      archive_path: packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md
      locator: 'Opening paper byline, Authors: Erich Friedman.'
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
