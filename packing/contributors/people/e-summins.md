---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: e-summins
  display_name: E. Summins
  surname: Summins
  aliases:
  - Summins
  sources:
  - id: source-intake
    archive_path: packing/resources/web/esummins-packing-2026-10-12/README.md
    locator: The opening and disclosure identify the n = 11 lab PI and requested credit name as
      E. Summins; no expanded first name is stated.
    url: https://github.com/Esummins/packing/tree/651a9a54688341880e9c0dc9fcfc19f2c04cd3cb
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: The [Summins stratification series 2026-10-12] entry names author Summins and identifies
      E. Summins (PI).
  provenance:
  - field: /display_name
    sources:
    - source-intake
  - field: /surname
    sources:
    - bibliography
  - field: /aliases/0
    sources:
    - bibliography
    - source-intake
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
