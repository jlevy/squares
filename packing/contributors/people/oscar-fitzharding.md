---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: oscar-fitzharding
  display_name: Oscar Fitzharding
  surname: Fitzharding
  real_name: Oscar Fitzharding
  aliases: [Fitzharding, ofitzharding, '@ofitzharding']
  links:
    - kind: github
      url: https://github.com/ofitzharding
      handle: ofitzharding
    - kind: twitter
      url: https://x.com/ofitzharding
      handle: ofitzharding
  sources:
    - id: citation-cff
      archive_path: packing/resources/web/fitzharding-n17-lean-2026-10-13/sq17-lean/CITATION.cff
      url: https://github.com/ofitzharding/sq17-lean/blob/e6ee548090dc1dbf938ecf8590481de837a6a454/CITATION.cff
      locator: 'authors gives given-names Oscar and family-names Fitzharding; repository-code is github.com/ofitzharding/sq17-lean.'
    - id: licence
      archive_path: packing/resources/web/fitzharding-n17-lean-2026-10-13/sq17-lean/LICENSE
      locator: 'MIT licence, “Copyright (c) 2026 Oscar Fitzharding”.'
    - id: packet
      archive_path: packing/resources/web/fitzharding-n17-lean-2026-10-13/README.md
      locator: 'Opening paragraphs: the author Oscar Fitzharding announced the proof on X as @ofitzharding, and the owner set Oscar Fitzharding as the definitive name. Source and Pin table: author and committer ofitzharding; issue #565 opened by ofitzharding.'
    - id: announcement
      archive_path: packing/resources/web/fitzharding-n17-lean-2026-10-13/receipts/announcement/tweet-2109798000008597616.json
      url: https://x.com/ofitzharding/status/2109798000008597616
      locator: 'The post of 2026-10-13T00:06:56Z from @ofitzharding (display name “Oscar”, account 2097726704118603776) announcing the first complete Lean proof of optimality for Bidwell’s 1998 packing of 17 squares.'
    - id: release-readme
      archive_path: packing/resources/web/fitzharding-n17-lean-2026-10-13/sq17-lean/README.md
      locator: 'Credits and the closing note: “This project was developed with substantial assistance from Claude and Codex.”'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'credited_names maps Oscar Fitzharding to Fitzharding; the [Fitzharding n17 Lean 2026] entry credits Fitzharding.'
  provenance:
    - field: /surname
      sources: [citation-cff, bibliography]
    - field: /display_name
      sources: [citation-cff, licence, packet]
    - field: /real_name
      sources: [citation-cff, licence]
    - field: /aliases/0
      sources: [citation-cff, bibliography]
    - field: /aliases/1
      sources: [packet, citation-cff]
    - field: /aliases/2
      sources: [announcement]
    - field: /links/0
      sources: [citation-cff, packet]
    - field: /links/1
      sources: [announcement, packet]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
