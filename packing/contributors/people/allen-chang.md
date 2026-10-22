---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: allen-chang
  display_name: Allen Chang
  surname: Chang
  real_name: Allen Chang
  aliases:
  - Chang
  sources:
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: 'Entry 83: Improved by Allen Chang in September 2026, with GPT-5.6 Sol and GPT-6 Astra; polynomial
      root solution found by Allen Chang in September 2026. Entry 68 also names Allen Chang.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names maps Allen Chang to Chang; bibliography source notes preserve the catalogue credit context.
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
