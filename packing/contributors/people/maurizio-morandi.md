---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: maurizio-morandi
  display_name: Maurizio Morandi
  surname: Morandi
  real_name: Maurizio Morandi
  aliases:
  - Morandi
  sources:
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: 'Entry 69: Found by Maurizio Morandi in June 2010; the later Cantrell, hmbelvedere and Ellsworth improvements
      are credited separately.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names maps Maurizio Morandi to Morandi; bibliography source notes preserve the catalogue credit
      context.
  provenance:
  - field: /display_name
    sources:
    - catalogue-credit
    - bibliography
  - field: /surname
    sources:
    - catalogue-credit
    - bibliography
  - field: /real_name
    sources:
    - catalogue-credit
    - bibliography
  - field: /aliases
    sources:
    - catalogue-credit
    - bibliography
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
