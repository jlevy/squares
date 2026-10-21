---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: f-gobel
  display_name: 'F. Göbel'
  surname: Göbel
  aliases: ['Göbel', 'Gobel']
  sources:
    - id: primary-byline
      archive_path: packing/resources/papers/gobel-1979-geometrical-packing-and-covering-problems.pdf
      locator: 'Page 1 title and F. GOBEL byline; initial retained rather than expanding a name.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
  provenance:
    - field: /surname
      sources: [primary-byline, bibliography]
    - field: /display_name
      sources: [primary-byline]
    - field: /aliases
      sources: [primary-byline, bibliography]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
