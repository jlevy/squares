# Record square packings

Current arrangements and refinements credited to Francisco Couzo for packing
`n` unit squares in a square of side `s`. The table uses the reviewed public
registry, issues, PRs and construction bounds to select the records still held.

[Upper bounds](upper_bounds.json) cover every count through n=10000;
[lower bounds](lower_bounds.json) cover every count through n=1024.
The [reviewed public bounds](public_bounds.json) include the registry, open issues,
PRs and construction consequences. The [20 October reconciliation](certificates/review-20261020/README.md)
records the comparison and archived claims.
Exact certificate bounds, frozen reference comparisons,
and reported lower-bound or optimality claims retain their source and verification
status. The [closed-form lower-bound parameters](lower_bound_families.json) can be
evaluated with `lower_bounds.py`; evaluating the formula does not replay its proof.

Live packings are kept in one transactional store on CT105. The web app and Desktopo read its current bounds and immutable seeds; native results use the same exact acceptance path as browser results. Repository files are reviewed Git snapshots. See [Packing store](PACKING_STORE.md) for operation and record intake.

The [publication-order and attribution review](RECORD_PROVENANCE.md) separates
construction, refinement and certificate credit, with
[source metadata for every count through 1024](record_provenance.json).
Tighter certification preserves the original arrangement credit. Imported and
superseded packings remain available in the full catalogue and search archives.

[Kaggle export](KAGGLE.md) prepares the current packings for n=1–1000, with source credits and local verification against the competition metric.

<!-- current-records -->

## Current records

Reviewed 2026-10-24: **24 counts** — published records held by this project and improvements over the reviewed public bound.

Each n opens its packing. Certified sides and public comparisons are rounded upward to 12 decimal places. Matching our own published bound retains the record and its credit, as does another author’s re-certification within `1e-10` of a packing credited to us; a public bound stronger by more than that supersedes it. Matching another author’s record does not claim ownership. Construction, seed and certificate credits are linked for each packing. Updates to our own packings have no minimum gain: their exact certified bound must strictly decrease. The `1e-10` reporting tolerance applies only to claims of new improvements over another author’s public bound and to keeping a record credited to us.

Counts above 324 are not published while the Kaggle *Squares in Squares* competition runs; earlier public rows above 324 remain in the repository history.

| n | certified side s | reviewed public bound | standing | credits |
|---:|---:|---:|---|---|
| [68](n68.svg) | [8.798795237219](certificates/n68.cert) | [8.798795237219](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n68.json) |
| [106](n106.svg) | [10.822908044133](certificates/n106.cert) | [10.822908044133](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n106.json) |
| [110](n110.svg) | [10.996783396632](certificates/n110.cert) | [10.996783396632](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n110.json) |
| [130](n130.svg) | [11.902430645985](certificates/n130.cert) | [11.904483032516](https://github.com/jlevy/squares/issues/593) | Improvement over public bound | [credits](certificates/n130.json) |
| [152](n152.svg) | [12.830718800977](certificates/n152.cert) | [12.830718800977](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n152.json) |
| [156](n156.svg) | [12.979165853835](certificates/n156.cert) | [12.979165853835](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n156.json) |
| [172](n172.svg) | [13.618988956900](certificates/n172.cert) | [13.618988956900](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n172.json) |
| [177](n177.svg) | [13.822979734170](certificates/n177.cert) | [13.822979734170](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n177.json) |
| [206](n206.svg) | [14.860158663392](certificates/n206.cert) | [14.860158663392](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n206.json) |
| [210](n210.svg) | [14.973001116588](certificates/n210.cert) | [14.973001116588](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n210.json) |
| [211](n211.svg) | [14.993549626300](certificates/n211.cert) | [14.993549626300](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-211.cert.gz) | Published record held by this project | [credits](certificates/n211.json) |
| [227](n227.svg) | [15.563625652326](certificates/n227.cert) | [15.563625652326](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-227.cert.gz) | Published record held by this project | [credits](certificates/n227.json) |
| [237](n237.svg) | [15.902603638260](certificates/n237.cert) | [15.902603638260](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-237.cert.gz) | Published record held by this project | [credits](certificates/n237.json) |
| [240](n240.svg) | [15.969685337531](certificates/n240.cert) | [15.969685337531](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n240.json) |
| [241](n241.svg) | [15.987117095151](certificates/n241.cert) | [15.987117095151](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-241.cert.gz) | Published record held by this project | [credits](certificates/n241.json) |
| [260](n260.svg) | [16.637029558871](certificates/n260.cert) | [16.645753250520](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-260.cert.gz) | Improvement over public bound | [credits](certificates/n260.json) |
| [267](n267.svg) | [16.838815269949](certificates/n267.cert) | [16.838815269949](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n267.json) |
| [268](n268.svg) | [16.874361715870](certificates/n268.cert) | [16.874361715870](https://github.com/evand/square-packing/blob/659ee62e4a9d39542a1146e8b011cc3ab6407ede/search/packer/candidates/s268_lightning.cert) | Published record held by this project | [credits](certificates/n268.json) |
| [273](n273.svg) | [16.983925962651](certificates/n273.cert) | [16.983925962651](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n273.json) |
| [297](n297.svg) | [17.740417287544](certificates/n297.cert) | [17.740417287544](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n297.json) |
| [301](n301.svg) | [17.846667192844](certificates/n301.cert) | [17.846667192844](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n301.json) |
| [302](n302.svg) | [17.870013850405](certificates/n302.cert) | [17.870013850405](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n302.json) |
| [306](n306.svg) | [17.963433717492](certificates/n306.cert) | [17.963433717492](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n306.json) |
| [307](n307.svg) | [17.979251283689](certificates/n307.cert) | [17.980862784055](https://github.com/jlevy/squares/issues/593) | Improvement over public bound | [credits](certificates/n307.json) |

The [complete bound catalogue](certificates/best/README.md) covers n=1–10000 and retains 1089 finite source witnesses, including imported packings and classical constructions. Historical improvements and search seeds remain in the repository with their provenance.

<!-- /current-records -->
