---
softschema:
  contract: packing.squares:Contributor/v1
  schema: contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: joshua-levy
  display_name: 'Joshua Levy'
  real_name: 'Joshua Levy'
  aliases: ['Levy']
  sources:
    - id: primary-byline
      archive_path: LICENSE
      locator: 'Copyright notices and required attribution name Joshua Levy.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
  provenance:
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
