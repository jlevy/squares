---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: muhammad-maaz
  display_name: Muhammad Maaz
  surname: Maaz
  real_name: Muhammad Maaz
  aliases:
  - Maaz
  sources:
  - id: source-intake
    archive_path: packing/resources/web/kleddamag-n17-candidate-2026-10-12/README.md
    url: https://github.com/Kleddamag/the-seventeenth-square-candidate/tree/653b9589d0f8a152f01adc56b1d48ba53d49abc3
    locator: Source and Credit table transcribes CREDITS.md naming Muhammad Maaz for the semidefinite
      leaves.
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: The [Overbeck n17 candidate 2026] entry credits Maaz; its retained-source note names
      Muhammad Maaz for the semidefinite leaves.
  provenance:
  - field: /display_name
    sources:
    - source-intake
    - bibliography
  - field: /real_name
    sources:
    - source-intake
  - field: /surname
    sources:
    - bibliography
  - field: /aliases/0
    sources:
    - bibliography
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
