---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: hiroshi-nagamochi
  display_name: 'Hiroshi Nagamochi'
  surname: Nagamochi
  real_name: 'Hiroshi Nagamochi'
  aliases: ['Nagamochi']
  sources:
    - id: primary-byline
      archive_path: packing/resources/papers/nagamochi-2005-packing-unit-squares-in-a-rectangle.raw.md
      locator: 'Paper title and Hiroshi Nagamochi byline in the opening lines.'
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
