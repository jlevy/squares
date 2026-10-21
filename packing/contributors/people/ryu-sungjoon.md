---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: ryu-sungjoon
  display_name: 'Ryu Sungjoon'
  real_name: 'Ryu Sungjoon'
  aliases: ['Ryu', 'squarepacker']
  sources:
    - id: primary-byline
      archive_path: packing/resources/web/squarepacker-s12-lower-bound-2026-10-05/s12-lower-bound/README.md
      locator: 'Credits section: Author: Ryu Sungjoon (@squarepacker).'
    - id: zenodo-creator
      archive_path: packing/resources/web/squarepacker-s12-lower-bound-2026-10-05/zenodo-23157015.json
      url: https://zenodo.org/records/23157015
      locator: 'metadata.creators[0].name is “Ryu, Sungjoon”, family name first, for version 1.1 of the s(12) lower-bound record.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
  provenance:
    - field: /display_name
      sources: [primary-byline, zenodo-creator]
    - field: /real_name
      sources: [primary-byline, zenodo-creator]
    - field: /aliases
      sources: [primary-byline, bibliography, zenodo-creator]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
