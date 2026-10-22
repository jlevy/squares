---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: darius-muglich
  display_name: Darius Muglich
  surname: Muglich
  real_name: Darius Muglich
  aliases: [Muglich, gfppoy]
  display_aliases: [gfppoy]
  links:
    - kind: github
      url: https://github.com/gfppoy
      handle: gfppoy
  sources:
    - id: source-intake
      archive_path: packing/resources/web/muglich-issue686-2026-10-19/README.md
      url: https://github.com/jlevy/squares/issues/686
      locator: 'Opening paragraph names Darius Muglich (gfppoy); Source and Credit records the human credit as Darius Muglich.'
    - id: issue-byline
      archive_path: packing/resources/web/muglich-issue686-2026-10-19/acquisition/issue-686.json
      url: https://github.com/jlevy/squares/issues/686
      locator: 'The retained issue has user gfppoy and opens “Credit name. Darius Muglich”; its body is signed Darius Muglich.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'The [Muglich issue 686 2026-10-19] entry uses author and credit label Muglich; credited_names maps Darius Muglich to Muglich.'
  provenance:
    - field: /display_name
      sources: [source-intake, issue-byline]
    - field: /surname
      sources: [bibliography]
    - field: /real_name
      sources: [source-intake, issue-byline]
    - field: /aliases/0
      sources: [bibliography]
    - field: /aliases/1
      sources: [source-intake, issue-byline]
    - field: /links/0
      sources: [issue-byline]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
