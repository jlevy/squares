---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: david-w-cantrell
  display_name: David W. Cantrell
  surname: Cantrell
  real_name: David W. Cantrell
  aliases:
  - Cantrell
  sources:
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: 'Entry 37: Found by David W. Cantrell in September 2002, improving the packing of 37 squares found
      by Evert Stenlund in early 1980.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names maps David W. Cantrell to Cantrell; bibliography source notes preserve the catalogue
      credit context.
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
