---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: david-ellsworth
  display_name: David Ellsworth
  surname: Ellsworth
  real_name: David Ellsworth
  aliases: [Ellsworth]
  links:
    - kind: github
      url: https://github.com/Davidebyzero
      handle: Davidebyzero
    - kind: publication
      url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
  sources:
    - id: catalogue-byline
      archive_path: packing/resources/web/kingbird-squares-in-squares.md
      url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
      locator: 'Page header: “SVG, high-precision, and other updates by David Ellsworth”, the name linked to https://github.com/Davidebyzero, “based on original compiled by Erich Friedman”; the parse_svg_packing.py link names github.com/Davidebyzero/packing_squares_in_squares__tools.'
    - id: catalogue-credits
      archive_path: packing/resources/web/kingbird-squares-in-squares.md
      locator: 'Entry credit lines naming David Ellsworth, such as entry 28, “Found by David Ellsworth in December 2025”, and entry 87, “Found by David Ellsworth in December 2024”; the case records read found_by and improved_by from these lines.'
    - id: picture-credits
      archive_path: packing/resources/web/known-best-packings/receipts/kingbird-2026-10-05-pictures.json
      locator: 'The n = 17 credits read from the catalogue SVG: “Exact polynomial root solution by David Ellsworth on June 4, 2023”, confirmed independently by Boris Alexeev the same day.'
    - id: tools-credit
      archive_path: packing/resources/web/casson-square-packing-2026-09-23/griffcass-square-packing/README.md
      locator: 'Credits section: the catalogue “maintained by David Ellsworth”, and Ellsworth’s parsing and checking tools at https://github.com/Davidebyzero/packing_squares_in_squares__tools.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'credited_names maps David Ellsworth to Ellsworth; the [Kingbird] entry quotes the page header naming him.'
  provenance:
    - field: /surname
      sources: [bibliography]
    - field: /display_name
      sources: [catalogue-byline]
    - field: /real_name
      sources: [catalogue-byline]
    - field: /aliases/0
      sources: [bibliography]
    - field: /links/0
      sources: [catalogue-byline, tools-credit]
    - field: /links/1
      sources: [catalogue-byline]
  bio_sources: [catalogue-byline, tools-credit]
---
David Ellsworth maintains the Squares in Squares catalogue, extending Erich Friedman’s
records with SVG drawings, high-precision values and algebraic descriptions.
He also develops packing parsers and checking tools.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
