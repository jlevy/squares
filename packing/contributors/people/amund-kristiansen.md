---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: amund-kristiansen
  display_name: Amund Kristiansen
  surname: Kristiansen
  real_name: Amund Kristiansen
  aliases: [Kristiansen, amundsk]
  links:
    - kind: github
      url: https://github.com/amundsk
      handle: amundsk
  sources:
    - id: source-intake
      archive_path: packing/resources/web/amundsk-n303-2026-10-23/README.md
      locator: What the Issue Reports retains issue 755's credit name, “Amund Kristiansen (GitHub @amundsk)”, filed by the GitHub account amundsk, and the gist README's “(Amund Kristiansen, 2026-10-23)”; the opening links the gist amundsk/78f9f0e7b4669f2f509a281845081768.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Kristiansen n303 2026-10-23] credits Kristiansen; credited_names maps Amund Kristiansen to Kristiansen.'
  provenance:
    - field: /display_name
      sources: [bibliography, source-intake]
    - field: /real_name
      sources: [source-intake]
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
