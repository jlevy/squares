---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: mykhailo-polkovskyi
  display_name: Mykhailo Polkovskyi
  surname: Polkovskyi
  real_name: Mykhailo Polkovskyi
  aliases: [Polkovskyi, Mishapolk, Mikhail Polk]
  links:
    - kind: github
      url: https://github.com/Mishapolk
      handle: Mishapolk
  sources:
    - id: source-intake
      archive_path: packing/resources/web/mishapolk-records-2026-10-14/README.md
      locator: What the Issue Reports retains source credit spellings Mishapolk (Mykhailo Polkovskyi) and Mishapolk (Mikhail Polk); the opening links Mishapolk/square-packing-records.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Mishapolk records 2026-10-14] credits Polkovskyi; credited_names maps Mykhailo Polkovskyi to Polkovskyi. The profile follows this curated name and preserves the other source spelling as an alias.'
  provenance:
    - field: /display_name
      sources: [bibliography, source-intake]
    - field: /real_name
      sources: [bibliography, source-intake]
    - field: /surname
      sources: [bibliography]
    - field: /aliases/0
      sources: [bibliography]
    - field: /aliases/1
      sources: [source-intake]
    - field: /aliases/2
      sources: [source-intake]
    - field: /links/0
      sources: [source-intake]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
