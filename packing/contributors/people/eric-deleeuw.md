---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: eric-deleeuw
  display_name: Eric Deleeuw
  surname: Deleeuw
  real_name: Eric Deleeuw
  aliases: [Deleeuw, ebdeleeuw]
  links:
    - kind: github
      url: https://github.com/ebdeleeuw
      handle: ebdeleeuw
  sources:
    - id: source-intake
      archive_path: packing/resources/web/ebdeleeuw-n70-refinement-2026-10-10/README.md
      locator: Retained source and credit evidence for [Deleeuw n70 refinement 2026-10-10], including repository account ebdeleeuw.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Deleeuw n70 refinement 2026-10-10] records the author credit Deleeuw. '
    - id: project-catalogue
      archive_path: packing/devtools/overview_sections.py
      locator: OTHER_PROJECTS credits the ebdeleeuw/square-packing-n70 repository to Eric Deleeuw.
  provenance:
    - field: /display_name
      sources: [project-catalogue]
    - field: /real_name
      sources: [project-catalogue]
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
