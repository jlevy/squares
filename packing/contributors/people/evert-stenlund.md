---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: evert-stenlund
  display_name: Evert Stenlund
  surname: Stenlund
  real_name: Evert Stenlund
  aliases:
  - Stenlund
  sources:
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: 'Entry 66: Found by Evert Stenlund in early 1980. Entry 67 again names Evert Stenlund as finder.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names maps Evert Stenlund to Stenlund; bibliography source notes preserve the catalogue credit
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
