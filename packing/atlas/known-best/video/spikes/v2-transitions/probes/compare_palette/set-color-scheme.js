// Paint the stage in one colouring, one of those `colorSchemes()` reported. Takes {scheme}.
/** @param {{scheme: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasScheme}} o */
(o) => window.atlasTransitions.setColorScheme(o.scheme);
