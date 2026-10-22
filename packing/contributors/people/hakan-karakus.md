---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: hakan-karakus
  display_name: Hakan Karakuş
  surname: Karakuş
  real_name: Hakan Karakuş
  aliases:
  - Karakuş
  - Karakus
  sources:
  - id: primary-byline
    archive_path: packing/resources/papers/karakus-2026-counterexample-nagamochi-scoring-lemma.pdf
    url: https://arxiv.org/abs/2609.37410
    locator: 'PDF page 1: the byline names Hakan Karakuş, Boğaziçi University, Istanbul, Türkiye, and the paper
      is dated September 29, 2026.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: '[Karakuş 2026], authors[0], prints Karakuş; its source is arXiv:2609.37410. The atlas name_aliases
      retains the ASCII spelling Karakus.'
  - id: atlas-credit
    archive_path: packing/atlas/known-best/credit-attributions.json
    locator: name_aliases maps Hakan Karakuş and Karakus to Karakuş; lower_bounds.contributors records the full
      name and this source key.
  provenance:
  - field: /display_name
    sources:
    - primary-byline
  - field: /surname
    sources:
    - primary-byline
    - bibliography
  - field: /real_name
    sources:
    - primary-byline
  - field: /aliases
    sources:
    - primary-byline
    - atlas-credit
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
