---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: karoly-hajba
  display_name: Károly Hajba
  surname: Hajba
  real_name: Károly Hajba
  aliases:
  - Hajba
  sources:
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: 'Entry 83: Found by Károly Hajba in September 2024; the subsequent Stenlund antecedent and Cantrell,
      Chang and Ellsworth improvements are credited separately.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names maps Károly Hajba to Hajba; bibliography source notes preserve the catalogue credit
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
