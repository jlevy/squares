---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: joost-de-winter
  display_name: Joost de Winter
  surname: de Winter
  real_name: Joost de Winter
  aliases: [de Winter, JoostdeWinter]
  links:
    - kind: github
      url: https://github.com/JoostdeWinter
      handle: JoostdeWinter
  sources:
    - id: source-intake
      archive_path: packing/resources/web/de-winter-square-packing-211-2026-09-16/README.md
      locator: Retained source and credit evidence for [de Winter n211 2026-09-16], including repository account JoostdeWinter.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[de Winter n211 2026-09-16] records the author credit de Winter. credited_names maps Joost de Winter to de Winter.'
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
    - field: /links/0
      sources: [source-intake]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
