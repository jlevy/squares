---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: ryu-sungjoon
  display_name: 'Ryu Sungjoon'
  surname: Ryu
  real_name: 'Ryu Sungjoon'
  aliases: ['Ryu', 'squarepacker']
  display_aliases: [squarepacker]
  sources:
    - id: primary-byline
      archive_path: packing/resources/web/squarepacker-s12-lower-bound-2026-10-05/s12-lower-bound/README.md
      locator: 'Credits section: Author: Ryu Sungjoon (@squarepacker).'
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
