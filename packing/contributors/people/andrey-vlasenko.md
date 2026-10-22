---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: andrey-vlasenko
  display_name: Andrey Vlasenko
  surname: Vlasenko
  real_name: Andrey Vlasenko
  aliases:
  - chelokot
  - Vlasenko
  links:
  - kind: github
    url: https://github.com/chelokot
    handle: chelokot
  sources:
  - id: public-profile
    url: https://api.github.com/users/chelokot
    locator: 'Public GitHub profile checked 2026-10-21: login chelokot, name Andrey Vlasenko, type User.'
  - id: source-packet
    archive_path: packing/resources/web/chelokot-nagamochi-counterexample-2026-09-05/README.md
    url: https://github.com/chelokot/square-packing-archive
    locator: The packet identifies chelokot/square-packing-archive and retains the source credit to chelokot for
      project direction, with AI-produced research and Lean formalizations attributed separately.
  - id: atlas-credit
    archive_path: packing/atlas/known-best/credit-attributions.json
    locator: name_aliases maps chelokot and Andrey Vlasenko to Vlasenko; lower_bounds.contributors and optimality.contributors
      retain this same public-profile identity and source association.
  provenance:
  - field: /display_name
    sources:
    - public-profile
  - field: /surname
    sources:
    - public-profile
    - atlas-credit
  - field: /real_name
    sources:
    - public-profile
  - field: /aliases
    sources:
    - public-profile
    - source-packet
    - atlas-credit
  - field: /links
    sources:
    - public-profile
    - source-packet
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
