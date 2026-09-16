// Self-test: a math text seam whose table installer and restore do nothing.
() => {
  globalThis.kpressMathText = /** @type {KpressMathText} */ (
    /** @type {unknown} */ ({ installTablesFor: () => null, restore: () => undefined })
  );
};
