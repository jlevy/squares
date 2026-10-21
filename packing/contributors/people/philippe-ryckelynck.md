---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: philippe-ryckelynck
  display_name: Philippe Ryckelynck
  real_name: Philippe Ryckelynck
  aliases: [Ryckelynck]
  sources:
    - id: paper-byline
      archive_path: packing/resources/papers/gensane-ryckelynck-2005-improved-dense-packings.raw.md
      url: https://doi.org/10.1007/s00454-004-1129-z
      locator: 'Opening byline, “Thierry Gensane and Philippe Ryckelynck”, LMPA, Université du Littoral, Calais; Discrete Comput Geom 34:97–109 (2005); the abstract and the cases n = 17, 18, 29 and 37.'
    - id: picture-credits
      archive_path: packing/resources/web/known-best-packings/receipts/kingbird-2026-10-05-pictures.json
      locator: 'The n = 17 credits read from the catalogue SVG: “First high-precision analytic solution by Thierry Gensane and Philippe Ryckelynck before May 19, 2004.”'
    - id: catalogue-credits
      archive_path: packing/resources/web/kingbird-squares-in-squares-compared.md
      locator: 'Entries 18, 29 and 37: “Alternative found by” and “Found by Thierry Gensane and Philippe Ryckelynck in April 2004, using a computer program they wrote”; entry 37, “Improved by Thierry Gensane and Philippe Ryckelynck in April 2004, using a computer program they wrote, but didn''t set a record”, beside the better packing “Improved by David W. Cantrell in September 2002”.'
    - id: archive-index
      archive_path: packing/resources/README.md
      locator: 'Papers table: the key [Gensane–Ryckelynck 2005], under which the frontier records cite the paper, with authors “T. Gensane, P. Ryckelynck”.'
  provenance:
    - field: /display_name
      sources: [paper-byline, catalogue-credits]
    - field: /real_name
      sources: [paper-byline]
    - field: /aliases/0
      sources: [paper-byline, archive-index]
  bio_sources: [paper-byline, picture-credits, catalogue-credits]
---
Philippe Ryckelynck was at the Université du Littoral in Calais in 2005, when he and
Thierry Gensane published “Improved Dense Packings of Congruent Squares in a Square” in
Discrete & Computational Geometry.
For 17 squares the two authors gave the first high-precision analytic solution of John
Bidwell’s packing, solving a system of four polynomial equations to 20 digits.
The Squares in Squares catalogue says they found their packings of 18, 29 and 37 squares
in April 2004, using a computer program they wrote.
Their packing of 37 squares improved Erich Friedman’s of 1997 but did not set a record,
since David W. Cantrell had found a better one in 2002.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
