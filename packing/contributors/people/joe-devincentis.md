---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: joe-devincentis
  display_name: Joe DeVincentis
  surname: DeVincentis
  real_name: Joe DeVincentis
  aliases:
  - DeVincentis
  sources:
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: 'Entry 70: Found by Joe DeVincentis in April 2014. Entry 87 also identifies the packing of 54 squares
      found by Joe DeVincentis in April 2014.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names maps Joe DeVincentis to DeVincentis; bibliography source notes preserve the catalogue
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
