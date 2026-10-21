---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: thomas-schadt
  display_name: Thomas Schadt
  surname: Schadt
  real_name: Thomas Schadt
  aliases: [Schadt, BalthasarStrauss]
  links:
    - kind: github
      url: https://github.com/BalthasarStrauss
      handle: BalthasarStrauss
  sources:
    - id: source-intake
      archive_path: packing/resources/web/schadt-s29-2025/README.md
      locator: Results table credits the new solution to Thomas Schadt (2025).
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: credited_names maps Thomas Schadt to Schadt.
    - id: project-catalogue
      archive_path: packing/devtools/overview_sections.py
      locator: OTHER_PROJECTS credits BalthasarStrauss/Squares-packing_S-29-_New-Record to Thomas Schadt.
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
      sources: [project-catalogue]
    - field: /links/0
      sources: [project-catalogue]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
