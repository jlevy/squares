---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: robert-barnett
  display_name: Robert Barnett
  surname: Barnett
  real_name: Robert Barnett
  aliases: [Barnett, RobertBarnettProjects]
  links:
    - kind: github
      url: https://github.com/RobertBarnettProjects
      handle: RobertBarnettProjects
  sources:
    - id: source-intake
      archive_path: packing/resources/web/barnett-refinements-2026-10-11/README.md
      locator: Retained source and credit evidence for [Barnett refinements 2026-10-11], including repository account RobertBarnettProjects.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Barnett refinements 2026-10-11] records the author credit Barnett. credited_names maps Robert Barnett to Barnett.'
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
